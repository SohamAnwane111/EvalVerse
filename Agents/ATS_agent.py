from Engine.driver import LLM_Agent, LLM_Driver, load_config

config = load_config('llm_config.yaml')

API_KEY = config['openrouter']['api']['key1']
BASE_URL = config['openrouter']['url']
MAX_TOKENS = config['openrouter']['max_tokens']
MODEL = config['openrouter']['model']['gemini-2.5-pro-exp-03-25:free']

@LLM_Driver(base_url=BASE_URL, api_key=API_KEY, model_name=MODEL, max_tokens=MAX_TOKENS, use_chatlite=True)
class AtsScorer:

    @LLM_Agent("ATS_scorer")
    def score_resume(self):
        return {
            "role": "ATS Resume Scorer",
            "goal": "Score a resume against a job description using ATS-like logic",
            "backstory": (
                "An intelligent ATS module that evaluates resumes by checking for keyword matches, skill alignment, "
                "relevant experience, and overall suitability for the job profile."
            ),
            "description": lambda resume_text, job_description: (
                f"Evaluate the resume for suitability to the given job description.\n\n"
                f"Resume:\n{resume_text}\n\n"
                f"Job Description:\n{job_description}\n\n"
                f"Return a JSON object with two keys:\n"
                f"- 'score' (an integer from 0 to 100 indicating the match percentage)\n"
                f"- 'reasoning' (a short paragraph explaining the score in terms of skills, experience, and relevance)."
            ),
            "tools": []
        }
