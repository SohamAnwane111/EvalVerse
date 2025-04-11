from Engine.text_extractor import TextExtractor
from Agents.ResumeAnalyzer.candidate_profile_agent import CandidateProfileAgent
from Agents.ResumeAnalyzer.skill_extractor_agent import SkillExtractorAgent
from Agents.ResumeAnalyzer.work_experience_agent import WorkExperienceAgent
import Engine.OA_session as OA
import Engine.Interview as Interview
from concurrent.futures import ThreadPoolExecutor
from Engine import str2json
import time

def main():

    resume_extractor = TextExtractor("Resume.pdf")
    resume_text = str(resume_extractor)

    profile_agent = CandidateProfileAgent()
    skill_extractor = SkillExtractorAgent()
    work_extraactor = WorkExperienceAgent()

    # === Step 2: Run Agents Concurrently ===
    with ThreadPoolExecutor() as executor:
        future_profile = executor.submit(profile_agent.run, 'candidate_profile_agent', resume_text=resume_text)
        future_skills = executor.submit(skill_extractor.run, 'skill_extractor', resume_text=resume_text)
        future_experience = executor.submit(work_extraactor.run, 'experience_extractor', resume_text=resume_text)

        extracted_profile = future_profile.result()
        extracted_skills = future_skills.result()
        extracted_experience = future_experience.result()

    print("\n🔍 Skills Extracted:", str(extracted_skills))
    print("\n👤 Candidate Profile Extracted:"
          f"\n{str2json.extract_first_json_safe(str(extracted_profile))}")
    print("\n🧑‍💼 Experience Extracted:", str(extracted_experience))

    difficulty = ["very easy", "easy", "medium", "hard", "very hard"]
    points = [100, 200, 300, 400, 500]
    rounds = 2
    time.sleep(5)
    OA.run_oa_session(str(extracted_skills), difficulty, points, rounds)
    Interview.run_one_question_interview()


    

if __name__ == "__main__":
    main()
