from Engine.driver import llm_driver, llm_agent
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = os.getenv("GROQ_API_URL")
MODEL = os.getenv("GROQ_MODEL")
MAX_TOKENS = os.getenv("GROQ_MAX_TOKENS", 100)


@llm_driver(base_url=BASE_URL, api_key=API_KEY, model_name=MODEL, max_tokens=MAX_TOKENS)
class JobRequirementAnalyzer:

    @llm_agent.register_module("job_req_extractor")
    def create_job_requirement_extractor(self):
        return {
            "role": "Job Requirement Extractor",
            "goal": "Extract structured and concise job requirements from unstructured job descriptions containing noise or unnecessary details.",
            "backstory": (
                "You are a specialized NLP agent that processes noisy, verbose job descriptions "
                "and extracts clean, structured requirements that are actually useful to candidates. "
                "You ignore filler text, perks, benefits, and company propaganda, and focus on what the candidate "
                "needs to know: qualifications, responsibilities, skills required, and preferred experiences."
            ),
            "description": lambda noisy_job_desc: (
                f"Clean the following job description and extract only the most relevant requirements. "
                f"Organize your output under clear headers such as 'Position', 'Location', "
                f"'Required Qualifications', 'Technical Skills', 'Bonus Skills', and 'Responsibilities'.\n\n"
                f"Job Description:\n{noisy_job_desc}"
            ),
            "tools": []
        }