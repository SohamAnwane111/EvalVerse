from Engine.driver import LLM_Agent, LLM_Driver, load_config

config = load_config('llm_config.yaml')

API_KEY=config['groq']['api']['key1']
BASE_URL=config['groq']['url']
MAX_TOKENS=config['groq']['max_tokens']
MODEL=config['groq']['model']['llama-3.1-8b-instant']

@LLM_Driver(base_url=BASE_URL, api_key=API_KEY, model_name=MODEL, max_tokens=MAX_TOKENS, use_chatlite=True)
class CandidateProfileAgent():


    @LLM_Agent('candidate_profile_agent')
    def create_candidate_profile(self):
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