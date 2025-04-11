from Engine.driver import LLM_Agent, LLM_Driver, load_config

config = load_config('llm_config.yaml')

API_KEY=config['groq']['api']['key2']
BASE_URL=config['groq']['url']
MAX_TOKENS=config['groq']['max_tokens']
MODEL=config['groq']['model']['llama-3.3-70b-versatile']

@LLM_Driver(base_url=BASE_URL, api_key=API_KEY, model_name=MODEL, max_tokens=MAX_TOKENS, use_chatlite=True)
class SkillExtractorAgent():


    @LLM_Agent('skill_extractor')
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