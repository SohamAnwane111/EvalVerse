from Engine.driver import llm_driver, llm_agent
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = os.getenv("GROQ_API_URL")
MODEL = os.getenv("GROQ_MODEL")
MAX_TOKENS = os.getenv("GROQ_MAX_TOKENS", 1000)


@llm_driver(base_url=BASE_URL, api_key=API_KEY, model_name=MODEL, max_tokens=MAX_TOKENS)
class QuestionGenerator:

    @llm_agent.register_module("question_generator")
    def create_question_generator(self):
        return {
            "role": "Dynamic Question Generator",
            "goal": "Generate an on-the-fly technical question with an adaptive difficulty level",
            "backstory": (
                "This agent creates questions dynamically for an adaptive interview session. "
                "It increases the difficulty based on the candidate's prior performance while generating questions."
            ),
            "description": lambda prev_performance, current_difficulty, seen_questions=[], question_id="": (
                f"Generate a unique technical multiple-choice question that is not similar to previously asked questions. "
                f"Use a unique question ID: {question_id}. "
                f"The current difficulty level is {current_difficulty}.\n\n"
                f"❗ Avoid repeating or resembling any of these past questions:\n"
                f"{seen_questions}\n\n"
                f"Candidate performance summary:\n{prev_performance}\n\n"
                f"Return a JSON object with the following keys:\n"
                f"  - 'question_id' (UUID)\n"
                f"  - 'question_text'\n"
                f"  - 'options' (list of 4)\n"
                f"  - 'correct_answer'"
            ),
            "tools": []
        }
