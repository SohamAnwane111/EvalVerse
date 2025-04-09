from Engine.text_extractor import TextExtractor
from Agents.resume_analyzer import ResumeAnalyzer
from Agents.job_req_analyzer import JobRequirementAnalyzer
from Agents.candidature_agent import CandidatureAnalyzer
from Engine.OA_session import run_oa_session
import time

def main():
    # === Step 1: Extract Resume Text ===
    resume_extractor = TextExtractor("Resume.pdf")
    resume_text = str(resume_extractor)

    resume_analyzer = ResumeAnalyzer()

    print("🔍 Skills Extracted:")
    skills = resume_analyzer.run("skill_extractor", resume_text=resume_text)
    print(skills)

    print("\n🧑‍💼 Experience Extracted:")
    experience = resume_analyzer.run("experience_extractor", resume_text=resume_text)
    print(experience)

    # === Step 2: Run OA Simulation ===
    difficulty = ["very easy", "easy", "medium", "hard", "very hard"]
    points = [100, 200, 300, 400, 500]
    rounds = 5
    time.sleep(5)
    run_oa_session(skills, difficulty, points, rounds)

    # Time so that rate limit is not hit
    time.sleep(10)

    # === Step 3: Extract and Analyze Job Requirements ===
    job_requirement_extractor = TextExtractor("Job_Requirements.pdf")
    job_requirement_text = str(job_requirement_extractor)

    job_requirement_analyzer = JobRequirementAnalyzer()
    print("\n📄 Job Requirements Extracted:")
    clean_job_requirement = job_requirement_analyzer.run("job_req_extractor", noisy_job_desc=job_requirement_text)
    print(clean_job_requirement)

    # === Step 4: Evaluate Candidature ===
    print("\n📊 Candidature Evaluation:")
    candidature_analyzer = CandidatureAnalyzer()
    evaluation = candidature_analyzer.run(
        "candidature_evaluator",
        resume_text=resume_text,
        job_req_text=clean_job_requirement
    )
    print(evaluation)

if __name__ == "__main__":
    main()
