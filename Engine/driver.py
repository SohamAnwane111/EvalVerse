from typing import Dict, Callable
import types
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew

# ================================================================
# Agent Registration Decorator
# ================================================================
class _LLM_AgentRegistry:
    _registry: Dict[str, Callable] = {}

    @staticmethod
    def register(name: str):
        """
        Decorator to register a method as a named agent module.
        """
        def decorator(func):
            _LLM_AgentRegistry._registry[name] = func
            return func
        return decorator


# Exported alias for decorator usage
LLM_Agent = _LLM_AgentRegistry.register

# ================================================================
# Main Driver Decorator
# ================================================================
def LLM_Driver(base_url, api_key, model_name, temperature=0.1, max_tokens=1000):
    """
    Class decorator that wires up LLM-powered agent/task creation.
    Supports dynamic inputs via keyword arguments passed to the description function.
    """

    def decorator(cls):
        # Store LLM configuration
        cls._llm_config = {
            'base_url': base_url,
            'api_key': api_key,
            'model_name': model_name,
            'temperature': temperature,
            'max_tokens': max_tokens
        }

        cls._agents = {}
        cls._task_templates = {}

        # Register agents using stored configs
        for agent_name, method in _LLM_AgentRegistry._registry.items():

            def create_agent_template(method=method, name=agent_name):
                config = method(cls)

                llm_cls = ChatGroq if model_name.startswith("groq") else ChatOpenAI
                llm = llm_cls(
                    base_url=base_url,
                    api_key=api_key,
                    model=model_name,
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                agent = Agent(
                    role=config["role"],
                    goal=config["goal"],
                    backstory=config["backstory"],
                    tools=config.get("tools", []),
                    verbose=True,
                    llm=llm
                )
                cls._agents[name] = agent

                cls._task_templates[name] = {
                    "expected_output": config.get("expected_output", "Final result or analysis"),
                    "description_fn": config["description"]
                }

            create_agent_template()

        def run(self, name: str, **kwargs):
            if name not in self._agents or name not in self._task_templates:
                raise ValueError(f"No agent or task found for '{name}'")

            agent = self._agents[name]
            desc_fn = self._task_templates[name]["description_fn"]
            expected_output = self._task_templates[name]["expected_output"]

            task_description = desc_fn(**kwargs)
            task = Task(
                agent=agent,
                description=task_description,
                expected_output=expected_output,
                async_execution=False
            )

            crew = Crew(agents=[agent], tasks=[task], verbose=False)
            return crew.kickoff()

        cls.run = run

        def run_all(self):
            raise NotImplementedError("run_all not supported with dynamic inputs.")

        cls.run_all = run_all

        original_init = cls.__init__ if hasattr(cls, '__init__') else lambda self: None

        def __init__(self, *args, **kwargs):
            original_init(self, *args, **kwargs)

            for agent_name in cls._agents:
                def make_runner(an):
                    def run_agent(self, **kwargs):
                        return self.run(an, **kwargs)
                    return run_agent
                setattr(self, f"run_{agent_name}", types.MethodType(make_runner(agent_name), self))

        cls.__init__ = __init__

        return cls

    return decorator
