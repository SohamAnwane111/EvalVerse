from typing import Dict, Callable
import types
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatLiteLLM
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

# ================================================================
# Agent Registration Decorator
# ================================================================
class _LLM_AgentRegistry:
    _registry: Dict[str, Callable] = {}

    @staticmethod
    def register(name: str):
        def decorator(func):
            _LLM_AgentRegistry._registry[name] = func
            return func
        return decorator

LLM_Agent = _LLM_AgentRegistry.register

# ================================================================
# Main Driver Decorator
# ================================================================
def LLM_Driver(base_url, api_key, model_name, temperature=0.1, max_tokens=1000, use_chatlite=False):
    """
    Decorator that sets up LLM-powered agents using LangChain + CrewAI.
    Supports OpenAI, Groq, and ChatLite — explicitly use `use_chatlite=True` to route via ChatLite.
    """

    def decorator(cls):
        if(model_name == None):
            print("Model name is not set. Please set the model name.")
        cls._llm_config = {
            'base_url': base_url,
            'api_key': api_key,
            'model_name': model_name,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'use_chatlite': use_chatlite 
        }

        cls._agents = {}
        cls._task_templates = {}

        for agent_name, method in _LLM_AgentRegistry._registry.items():

            def create_agent_template(method=method, name=agent_name):
                config = method(cls)

                # ✨ Pick LLM class based on flag
                if use_chatlite:
                    llm_cls = ChatLiteLLM
                elif model_name.startswith("groq"):
                    llm_cls = ChatGroq
                else:
                    llm_cls = ChatOpenAI

                # 🔌 LLM instance
                llm = llm_cls(
                    base_url=base_url,
                    api_key=api_key,
                    model=model_name,
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                # 👷 Agent setup
                agent = Agent(
                    role=config["role"],
                    goal=config["goal"],
                    backstory=config["backstory"],
                    tools=config.get("tools", []),
                    verbose=True,
                    llm=llm
                )

                if config.get("tools"):
                    print(f"📦 TOOLS ENABLED for '{name}': {[tool.__class__.__name__ for tool in config['tools']]}")
                else:
                    print(f"🚫 NO TOOLS attached for '{name}'")
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
            results = {}
            for agent_name in self._agents:
                run_method = getattr(self, f'run_{agent_name}', None)
                if callable(run_method):
                    print(f"\n🚀 Running agent '{agent_name}'...")
                    try:
                        result = run_method()
                        results[agent_name] = result
                    except Exception as e:
                        results[agent_name] = f"❌ Failed: {e}"
                else:
                    results[agent_name] = "❌ No runner method found"
            return results

        cls.run_all = run_all

        # Inject `run_<agent>` methods
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
