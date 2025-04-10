from Engine.driver import LLM_Agent, LLM_Driver
from dotenv import load_dotenv
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from Tools.web_searcher import WebSearcher



import os


load_dotenv('application.env')

API_KEY = os.environ.get("groq.api.key1")
BASE_URL = os.environ.get("groq.api.url")
MODEL = os.environ.get("groq.model1")
MAX_TOKENS = int(os.environ.get("groq.max_tokens", 1000))

@LLM_Driver(api_key=API_KEY, base_url=BASE_URL, model_name=MODEL, max_tokens=MAX_TOKENS, use_chatlite=True)
class SearchingAgent():

    @LLM_Agent("searching_agent")
    def searching_agent(self):
        return {
            "role": "searching_agent",
            "goal": "Find the best solution to a problem.",
            "backstory": "You are an expert in problem-solving and finding solutions.",
            "description": lambda query: f"Search for the best solution to the problem: {query}",
            "expected_output": "The best solution found. in just 50 words",
        }
    
    @LLM_Agent("searching_agent_advanced")
    def searching_agent_advanced(self):
        return {
            "role": "searching_agent_advanced",
            "goal": "Find the best solution to a problem with advanced techniques.",
            "backstory": "You are an expert in advanced problem-solving techniques.",
            "description": lambda query: f"Search for the best solution to the problem using advanced techniques: {query}",
            "expected_output": "The best solution found using advanced techniques. in just 100 words",
            "tools": [WebSearcher()]
        }
    

if __name__ == "__main__":
    agent = SearchingAgent()
    result = agent.run("searching_agent_advanced", query="How to optimize a supply chain?")
    print(result)