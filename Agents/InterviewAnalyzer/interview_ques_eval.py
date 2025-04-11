from Engine.driver import LLM_Agent, LLM_Driver, load_config

config = load_config('llm_config.yaml')

API_KEY=config['groq']['api']['key3']
BASE_URL=config['groq']['url']
MAX_TOKENS=config['groq']['max_tokens']
MODEL=config['groq']['model']['llama-3.3-70b-versatile']

@LLM_Driver(base_url=BASE_URL, api_key=API_KEY, model_name=MODEL, max_tokens=MAX_TOKENS, use_chatlite=True)
class InterviewQEval:

    @LLM_Agent("interview_ques_eval")
    def create_question_evaluator(self):
        return {
            "role": "Interview Question Evaluator",
            "goal": "Evaluate the depth, clarity, and relevance of candidate responses to interview questions",
            "backstory": (
                "This agent critically analyzes a candidate’s answer based on relevance, depth, clarity, and impact. "
                "It gives a qualitative score (e.g., poor, average, good, excellent) and explains the reasoning."
            ),
            "description": lambda question, answer, category="technical": (
                f"🧠 You're evaluating a candidate's response to a **{category}** interview question.\n\n"
                f"📄 Question:\n{question}\n\n"
                f"🗣️ Candidate's Answer:\n{answer}\n\n"
                f"📌 Instructions by category:\n"
                f"- For 'technical': Assess correctness, depth of knowledge, clarity of logic.\n"
                f"- For 'hr': Assess emotional intelligence, self-awareness, alignment with company culture.\n"
                f"- For 'situational': Assess problem-solving, adaptability, communication.\n\n"
                f"🎯 Output a JSON with the following:\n"
                f"  - 'category': category of question\n"
                f"  - 'rating': one of ['poor', 'fair', 'good', 'very good', 'excellent']\n"
                f"  - 'rationale': explain *why* this rating was assigned, with specifics from the answer\n"
            ),
            "tools": []
        }

