from Engine.driver import LLM_Driver, LLM_Agent
from dotenv import load_dotenv
import os

load_dotenv('application.env')

API_KEY = os.environ.get("groq.api.key2")
BASE_URL = os.environ.get("groq.api.url")
MODEL = os.environ.get("groq.model2")
MAX_TOKENS = int(os.environ.get("groq.max_tokens", 1000))


@LLM_Driver(base_url=BASE_URL, api_key=API_KEY, model_name=MODEL, max_tokens=MAX_TOKENS, use_chatlite=True)
class Evaluator:

    @LLM_Agent("evaluator")
    def create_evaluator(self):
        return {
            "role": "Candidate Evaluator",
            "goal": "Evaluate candidate answers and determine scores based on correctness",
            "backstory": (
                "An evaluator that reviews candidate answers in real time. "
                "It compares the candidate's answer to the correct answer provided by the question generator."
            ),
            "description": lambda candidate_answer, correct_answer: (
                f"Evaluate the candidate's answer.\n\n"
                f"Candidate's Answer: {candidate_answer}\n"
                f"Correct Answer: {correct_answer}\n\n"
                f"If the candidate's answer matches the correct answer, return 'correct'; otherwise, return 'incorrect'."
            ),
            "tools": []
        }
