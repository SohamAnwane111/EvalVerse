from typing import Dict, Callable
import types
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew

# ================================================================
# Agent Registration Class
# ================================================================
class llm_agent:
    """
    Class to register agent configuration modules.
    Each module is a function returning a config dictionary that
    includes keys like 'role', 'goal', 'backstory', 'tools', 'description'.
    The 'description' must be a callable (usually a lambda) that accepts
    dynamic input and returns a description string.
    """
    _registry: Dict[str, Callable] = {}

    @staticmethod
    def register_module(name: str):
        """
        Decorator to register a method as a named agent module.

        Usage:
            @llm_agent.register_module("agent_name")
            def create_agent(self):
                return {
                    "role": "...",
                    "goal": "...",
                    "backstory": "...",
                    "description": lambda **kwargs: f"... {kwargs['something']}"
                }
        """
        def decorator(func):
            llm_agent._registry[name] = func
            return func
        return decorator


# ================================================================
# Main Driver Decorator
# ================================================================
def llm_driver(base_url, api_key, model_name, temperature=0.1, max_tokens=1000):
    """
    Class decorator that wires up LLM-powered agent/task creation.
    Supports dynamic inputs via keyword arguments passed to the description function.
    """

    def decorator(cls):
        # Store LLM configuration for access later
        cls._llm_config = {
            'base_url': base_url,
            'api_key': api_key,
            'model_name': model_name,
            'temperature': temperature,
            'max_tokens': max_tokens
        }

        # Storage for agent instances and corresponding task templates
        cls._agents = {}
        cls._task_templates = {}  # Stores {expected_output, description_fn}

        # Create agents and store their task templates
        for agent_name, method in llm_agent._registry.items():

            def create_agent_template(method=method, name=agent_name):
                config = method(cls)

                # Choose correct LLM backend (Groq or OpenAI)
                llm = (
                    ChatGroq if model_name.startswith("groq")
                    else ChatOpenAI
                )(
                    base_url=base_url,
                    api_key=api_key,
                    model=model_name,
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                # Create and store the Agent
                agent = Agent(
                    role=config["role"],
                    goal=config["goal"],
                    backstory=config["backstory"],
                    tools=config.get("tools", []),
                    verbose=True,
                    llm=llm
                )
                cls._agents[name] = agent

                # Store the task template with dynamic description function
                cls._task_templates[name] = {
                    "expected_output": config.get("expected_output", "Final result or analysis"),
                    "description_fn": config["description"]
                }

            # Immediately create agent and store config
            create_agent_template()

        # ---------------------------------------------------------------
        # Method to run a specific agent with dynamic input
        # ---------------------------------------------------------------
        def run(self, name: str, **kwargs):
            """
            Run a specific agent with dynamic input.

            Args:
                name (str): The registered name of the agent.
                **kwargs: Dynamic inputs passed to the description function.

            Returns:
                Crew result after executing the task.
            """
            if name not in self._agents or name not in self._task_templates:
                raise ValueError(f"No agent or task found for '{name}'")

            agent = self._agents[name]
            desc_fn = self._task_templates[name]["description_fn"]
            expected_output = self._task_templates[name]["expected_output"]

            # Dynamically generate the task description
            task_description = desc_fn(**kwargs)

            # Create the task and execute
            task = Task(
                agent=agent,
                description=task_description,
                expected_output=expected_output,
                async_execution=False
            )

            crew = Crew(agents=[agent], tasks=[task], verbose=False)
            return crew.kickoff()

        cls.run = run

        # ---------------------------------------------------------------
        # Block run_all for dynamic use-case (not supported)
        # ---------------------------------------------------------------
        def run_all(self):
            """
            Not implemented because tasks need dynamic inputs.
            """
            raise NotImplementedError("run_all not supported with dynamic inputs.")

        cls.run_all = run_all

        # ---------------------------------------------------------------
        # Add run_<agent_name>(**kwargs) methods dynamically
        # ---------------------------------------------------------------
        original_init = cls.__init__ if hasattr(cls, '__init__') else lambda self: None

        def __init__(self, *args, **kwargs):
            # Call the original constructor
            original_init(self, *args, **kwargs)

            # Add dynamic runner method per agent, e.g., run_skill_extractor(...)
            for agent_name in cls._agents:
                def make_runner(an):
                    def run_agent(self, **kwargs):
                        return self.run(an, **kwargs)
                    return run_agent
                setattr(self, f"run_{agent_name}", types.MethodType(make_runner(agent_name), self))

        cls.__init__ = __init__

        return cls

    return decorator
