from Engine.driver import LLM_Agent, LLM_Driver, load_config
from Tools.web_searcher import WebSearcher

config = load_config('llm_config.yaml')
API_KEY=config['groq']['api']['key4']
BASE_URL=config['groq']['url']
MAX_TOKENS=config['groq']['max_tokens']
MODEL=config['groq']['model']['deepseek-r1-distill-qwen-32b']

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
                "tools": [WebSearcher()]
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