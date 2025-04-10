from Engine.driver import LLM_Agent, LLM_Driver
from dotenv import load_dotenv
import os

load_dotenv('application.env')

API_KEY = os.environ.get("groq.api.key3")
BASE_URL = os.environ.get("groq.api.url")
MODEL = os.environ.get("groq.model3")
MAX_TOKENS = int(os.environ.get("groq.max_tokens", 1000))


@LLM_Driver(base_url=BASE_URL, api_key=API_KEY, model_name=MODEL, max_tokens=MAX_TOKENS, use_chatlite=True)
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
    
    @LLM_Agent("personal_info_extractor")
    def create_personal_info_extractor(self):
        return {
            "role": "Resume Personal Info Extractor",
            "goal": "Extract personal details from candidate resumes",
            "backstory": (
                "An expert agent in identifying and extracting personal information from resumes. "
                "Specialized in locating key identity and contact details such as name, email, phone number, "
                "address, LinkedIn profile, GitHub, date of birth, and other relevant personal identifiers."
            ),
            "description": lambda resume_text :(
                f"Extract only the candidate's personal information from the resume. "
                f"Ignore work experience, education, or skills.\n\n"
                f"Return the response in JSON format with the following fields:\n"
                f"- full_name\n- email\n- phone\n- address\n- linkedin\n- github\n- dob\n- nationality\n- gender\n\n"
                f"If any field is missing, set its value to null.\n\n"
                f"Resume:\n{resume_text}"
            ),
            "expected_output": """{
                "full_name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1 123 456 7890",
                "address": "123, Baker Street, London",
                "linkedin": "https://linkedin.com/in/johndoe",
                "github": "https://github.com/johndoe",
                "dob": "1990-01-01",
                "nationality": "British",
                "gender": "Male"
            }""",
            "tools": []
        }
