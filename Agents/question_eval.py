from Engine.driver import llm_driver, llm_agent
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = os.getenv("GROQ_API_URL")
MODEL = os.getenv("GROQ_MODEL")
MAX_TOKENS = os.getenv("GROQ_MAX_TOKENS", 1000)


@llm_driver(base_url=BASE_URL, api_key=API_KEY, model_name=MODEL, max_tokens=MAX_TOKENS)
class Evaluator:

    @llm_agent.register_module("evaluator")
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
