from Engine.text_extractor import TextExtractor
from Agents.ResumeAnalyzer.candidate_profile_agent import CandidateProfileAgent
from Agents.ResumeAnalyzer.skill_extractor_agent import SkillExtractorAgent
from Agents.ResumeAnalyzer.work_experience_agent import WorkExperienceAgent
from Agents.JobAnalyzer.job_req_analyzer import JobRequirementAnalyzer
from Agents.ATS_agent import AtsScorer
import Engine.OA_session as OA
import Engine.Interview as Interview
from concurrent.futures import ThreadPoolExecutor
from Engine import str2json
import time

def main():
    # === Step 1: Extract Resume & Job Description PDFs ===
    resume_text = str(TextExtractor("Resume.pdf"))
    job_text = str(TextExtractor("Job_Requirements.pdf"))

    # === Step 2: Initialize Agents ===
    profile_agent = CandidateProfileAgent()
    skill_extractor = SkillExtractorAgent()
    work_extractor = WorkExperienceAgent()
    job_agent = JobRequirementAnalyzer()
    ats = AtsScorer()

    # === Step 3: Run Agents Concurrently ===
    with ThreadPoolExecutor() as executor:
        future_profile = executor.submit(profile_agent.run, 'candidate_profile_agent', resume_text=resume_text)
        future_skills = executor.submit(skill_extractor.run, 'skill_extractor', resume_text=resume_text)
        future_experience = executor.submit(work_extractor.run, 'experience_extractor', resume_text=resume_text)
        future_job = executor.submit(job_agent.run, 'job_req_extractor', noisy_job_desc=job_text)

        extracted_profile = future_profile.result()
        extracted_skills = future_skills.result()
        extracted_experience = future_experience.result()
        extracted_job = future_job.result()

    # === Step 4: Print Extracted Info ===
    print("\n🔍 Skills Extracted:", str(extracted_skills))
    print("\n👤 Candidate Profile Extracted:\n", str2json.extract_first_json_safe(str(extracted_profile)))
    print("\n🧑‍💼 Experience Extracted:", str(extracted_experience))
    # print("\n📄 Job Description Extracted:\n", extracted_job)

    # === Step 5: Run OA + Interview ===
    difficulty = ["very easy", "easy", "medium", "hard", "very hard"]
    points = [100, 200, 300, 400, 500]
    rounds = 3
    time.sleep(5)
    OA.run_oa_session(str(extracted_skills), difficulty, points, rounds)
    Interview.run_one_question_interview()

    # === Step 6: ATS Scoring ===
    ats_score = ats.run('ATS_scorer',resume_text=resume_text, job_description=extracted_job)
    print("\n📊 ATS Score:", ats_score)


if __name__ == "__main__":
    main()
