from Engine.driver import LLM_Agent, LLM_Driver, load_config

config = load_config('llm_config.yaml')

API_KEY=config['groq']['api']['key3']
BASE_URL=config['groq']['url']
MAX_TOKENS=config['groq']['max_tokens']
MODEL=config['groq']['model']['llama3-70b-8192']


@LLM_Driver(base_url=BASE_URL, api_key=API_KEY, model_name=MODEL, max_tokens=MAX_TOKENS, use_chatlite=True)
class QuestionEvaluator:

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
