from Engine.driver import LLM_Agent, LLM_Driver, load_config

config = load_config('llm_config.yaml')

API_KEY=config['groq']['api']['key1']
BASE_URL=config['groq']['url']
MAX_TOKENS=config['groq']['max_tokens']
MODEL=config['groq']['model']['llama-3.3-70b-versatile']

@LLM_Driver(base_url=BASE_URL, api_key=API_KEY, model_name=MODEL, max_tokens=MAX_TOKENS, use_chatlite=True)
class InterviewQGen:

    @LLM_Agent("interview_ques_gen")
    def create_question_generator(self):
        return {
            "role": "Interview Question Generator",
            "goal": "Generate unique interview questions (technical, HR, or situational)",
            "backstory": (
                "This agent generates fresh, non-repetitive questions tailored to different interview categories "
                "such as technical, HR, and situational."
            ),
            "description": lambda seen_questions=[], question_id="", category="technical": (
                f"You're generating a **{category}** interview question.\n"
                f"❗ Make sure it's unique and doesn't repeat or resemble any of the following questions:\n"
                f"{seen_questions}\n\n"
                f"🆔 Question ID: {question_id}\n\n"
                f"Instructions by category:\n"
                f"🔹 'technical': Ask a direct coding or computer science question (no options).\n"
                f"🔹 'hr': Ask a behavioral or personality question that reflects soft skills.\n"
                f"🔹 'situational': Give a realistic scenario and ask how the candidate would handle it.\n\n"
                f"Respond with a JSON object:\n"
                f"  - 'question_id': string (UUID)\n"
                f"  - 'category': 'technical' | 'hr' | 'situational'\n"
                f"  - 'question_text': string\n"
                f"  - 'expected_response': string (only for 'hr' or 'situational')"
            ),
            "tools": []
        }
