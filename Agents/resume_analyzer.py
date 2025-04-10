from Engine.driver import LLM_Agent, LLM_Driver
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = os.getenv("GROQ_API_URL")
MODEL = os.getenv("GROQ_MODEL")
MAX_TOKENS = os.getenv("GROQ_MAX_TOKENS", 100)


@LLM_Driver(base_url=BASE_URL, api_key=API_KEY, model_name=MODEL, max_tokens=MAX_TOKENS)
class ResumeAnalyzer:

    @LLM_Agent("skill_extractor")
    def create_skill_extractor(self):
        return {
            "role": "Resume Skill Extractor",
            "goal": "Extract detailed technical skills from candidate resumes",
            "backstory": (
                "A specialized agent that reads resumes and identifies all relevant technical "
                "skills, tools, frameworks, libraries, programming languages, platforms, and certifications "
                "mentioned by the candidate."
            ),
            "description": lambda resume_text :(
                f"Analyze the resume and extract a detailed list of technical skills.\n\n"
                f"Resume:\n{resume_text}"
            ),
            "tools": []
        }

    @LLM_Agent("experience_extractor")
    def create_experience_extractor(self):
        return {
            "role": "Resume Experience Extractor",
            "goal": "Extract and summarize all work experience entries from candidate resumes",
            "backstory": (
                "A resume analysis agent with expertise in understanding and extracting work experience, "
                "job roles, durations, companies, responsibilities, and achievements from resumes."
            ),
            "description": lambda resume_text :(
                f"Summarize all work experience from resume, including title, company, "
                f"duration, and key responsibilities.\n\nResume:\n{resume_text}"
            ),
            "tools": []
        }