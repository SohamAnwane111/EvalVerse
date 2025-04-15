from Engine.driver import LLM_Driver, LLM_Agent, load_config
config = load_config('llm_config.yaml')

API_KEY=config['groq']['api']['key4']
BASE_URL=config['groq']['url']
MAX_TOKENS=config['groq']['max_tokens']
MODEL=config['groq']['model']['llama-3.3-70b-versatile']


@LLM_Driver(base_url=BASE_URL, api_key=API_KEY, model_name=MODEL, max_tokens=MAX_TOKENS, use_chatlite=True)
class JobRequirementAnalyzer:

    @LLM_Agent("job_req_extractor")
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