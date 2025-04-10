from Engine.driver import LLM_Driver, LLM_Agent
from dotenv import load_dotenv
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
import random
import os

load_dotenv()
load_dotenv('application.env')

# Load API config
API_KEY = os.environ.get("groq.api.key5")
BASE_URL = os.environ.get("groq.api.url")
MODEL = os.environ.get("groq.model1")
MAX_TOKENS = int(os.environ.get("groq.max_tokens", 1000))

# 🔮 Random topic generator
def get_random_topic():
    topics = [
        "latest machine learning papers",
        "distributed systems in production",
        "edge computing vs cloud computing",
        "LLMs in software engineering",
        "real-world system design interviews",
        "trending Python performance tips",
        "Kubernetes architecture issues",
        "Web3 security vulnerabilities",
        "Open-source DevOps tools",
        "advanced database optimization"
    ]
    return random.choice(topics)

@LLM_Driver(api_key=API_KEY, base_url=BASE_URL, model_name=MODEL, max_tokens=MAX_TOKENS, use_chatlite=True)
class WebQuestionGen():
    """
    Agent that randomly searches the web and generates high-quality tech questions.
    """

    @LLM_Agent("question_generator")
    def question_generator(self):
        return {
            "role": "Web-based Technical Question Generator",
            "goal": "Search the web for cutting-edge tech trends and craft MCQs around them.",
            "backstory": (
                "You're a genius-level AI that scouts the internet for trending technical insights. "
                "Your mission is to transform these insights into engaging and challenging multiple-choice questions "
                "for technical learners and candidates."
            ),
            "description": lambda random_topic: (
                f"🎯 Generate a challenging multiple-choice technical question based on trending real-world topics.\n\n"
                
                f"🔍 First, use the `SerperDevTool` to search for a **random technical topic**.\n"
                f"Example usage:\n"
                f"{{'tool': 'SerperDevTool', 'input': {{'search_query': '{random_topic}'}} }}\n\n"
                
                f"🔗 Then, use the `ScrapeWebsiteTool` to fetch deep content from one or two of the result links if necessary.\n\n"
                
                f"📤 Final Output should be a **JSON object** with:\n"
                f"  - 'question_text': One MCQ-style question\n"
                f"  - 'options': List of 4 answer choices\n"
                f"  - 'correct_answer': Exact correct option from the list\n\n"
                
                f"🧠 Be creative, relevant, and don't repeat anything.\n"
                f"🔥 If no web data is good, generate something smart anyway!"
            ),
            "tools": [SerperDevTool(n_results=1), ScrapeWebsiteTool()],
        }

if __name__ == "__main__":
    agent = WebQuestionGen()
    topic = get_random_topic()
    result = agent.run("question_generator", random_topic=topic)

    print(f"\n📦 Generated Question on topic: {topic}")
    print(result)
