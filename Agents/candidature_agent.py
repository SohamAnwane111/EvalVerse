from Engine.driver import llm_driver, llm_agent
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = os.getenv("GROQ_API_URL")
MODEL = os.getenv("GROQ_MODEL")
MAX_TOKENS = os.getenv("GROQ_MAX_TOKENS", 100)


@llm_driver(base_url=BASE_URL, api_key=API_KEY, model_name=MODEL, max_tokens=MAX_TOKENS)
class CandidatureAnalyzer:

    @llm_agent.register_module("candidature_evaluator")
    def create_candidature_evaluator(self):
        return {
            "role": "Candidature Evaluator",
            "goal": "Analyze how closely a candidate's resume aligns with a specific job requirement with just hints (no strong decision) of making any final hiring recommendation.",
            "backstory": (
                "An unbiased analytical assistant that compares a job requirement with a candidate's resume. "
                "Focus is on factual match percentages and reasoned observations. "
                "Final hiring decisions are deferred to a human recruiter."
            ),
            "description": lambda resume_text, job_req_text: (
                f"You are to analyze the candidate's resume in the context of the provided job requirement.\n\n"
                f"Resume:\n{resume_text}\n\n"
                f"Job Description:\n{job_req_text}\n\n"
                f"Please output your analysis under the following headings:\n\n"
                f"### Candidature Analysis\n"
                f"- **Skill Match (%):** Estimate percentage of matching skills with explanation.\n"
                f"- **Qualification Match:** Yes / Partially / No — include justification.\n"
                f"- **Experience Relevance:** Comment on how well the candidate's projects or internships align.\n"
                f"- **Gaps / Missing Criteria:** Highlight any important job criteria missing from the resume.\n"
                f"- **Strengths Not Explicitly Asked For:** Note any impressive aspects of the resume not directly requested in the JD.\n"
            ),
            "tools": []
        }
