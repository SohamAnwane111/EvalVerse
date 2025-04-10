from Engine.driver import LLM_Driver, LLM_Agent
from dotenv import load_dotenv
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
import os
import uuid

load_dotenv('application.env')

API_KEY = os.environ.get("groq.api.key3")
BASE_URL = os.environ.get("groq.api.url")
MODEL = os.environ.get("groq.model3")
MAX_TOKENS = int(os.environ.get("groq.max_tokens", 1000))


def filtered_tool(tool_instance, top_n_chars=100):
    class FilteredTool(tool_instance.__class__):
        def run(self, *args, **kwargs):
            result = super().run(*args, **kwargs)
            # Only return top N characters or just extract summary if available
            return result[:top_n_chars] if isinstance(result, str) else str(result)[:top_n_chars]
    return FilteredTool()


@LLM_Driver(base_url=BASE_URL, api_key=API_KEY, model_name=MODEL, max_tokens=MAX_TOKENS, use_chatlite=True)
class QuestionGenerator:

    @LLM_Agent("question_generator")
    def create_question_generator(self):
        try:
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
        except Exception as e:
            print(f"[!] Web tools failed: {e}\n--> Fallback to no-tool generation")

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
