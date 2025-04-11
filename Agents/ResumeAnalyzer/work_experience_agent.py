from Engine.driver import LLM_Agent, LLM_Driver, load_config

config = load_config('llm_config.yaml')

API_KEY=config['groq']['api']['key3']
BASE_URL=config['groq']['url']
MAX_TOKENS=config['groq']['max_tokens']
MODEL=config['groq']['model']['llama-3.3-70b-versatile']

@LLM_Driver(base_url=BASE_URL, api_key=API_KEY, model_name=MODEL, max_tokens=MAX_TOKENS, use_chatlite=True)
class WorkExperienceAgent():


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