from Agents.question_gen import QuestionGenerator
from Agents.question_eval import Evaluator
from Security.security_filter import SecurityFilter

import re
import json
import uuid
import time


def extract_first_json_safe(text):
    """Extracts and returns the first valid JSON object from the string."""
    try:
        text = text.strip().strip("`")
        for candidate in re.findall(r'\{.*?\}', text, re.DOTALL):
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                continue
    except Exception as e:
        print("❌ JSON Extraction Failed:", e)
    print("❌ No valid JSON object found.")
    return None


def get_question(skills, difficulty_levels, seen_questions):
    """Handles question generation with retry logic and security filter."""
    question_agent = QuestionGenerator()
    question_id = str(uuid.uuid4())[:8]

    @SecurityFilter(fallback=None, toxic_threshold=0.3, similarity_threshold=0.1, context=str(skills))
    def mcq_generator():
        return question_agent.run(
            "question_generator",
            prev_performance=str(skills),
            current_difficulty=difficulty_levels,
            seen_questions=seen_questions,
            question_id=question_id
        )

    for _ in range(5):
        mcq_response = mcq_generator()
        if mcq_response:
            return mcq_response
        time.sleep(3)
    return None


def run_oa_session(skills, difficulty_levels, points, rounds=5):
    evaluator = Evaluator()
    current_difficulty = 0
    seen_questions = set()
    points_scored = 0

    for round_num in range(1, rounds + 1):
        print(f"\n📝 Round {round_num}: Generating MCQ (Difficulty: {difficulty_levels[current_difficulty]})")
        mcq_response = get_question(skills, difficulty_levels, seen_questions)

        if not mcq_response:
            print("⚠️ Question generation failed. Skipping.")
            continue

        mcq_dict = extract_first_json_safe(str(mcq_response))
        if not mcq_dict:
            print("⚠️ Invalid MCQ format. Skipping.")
            continue

        try:
            question_text = mcq_dict.get("question_text", "")
            if question_text in seen_questions:
                print("⚠️ Duplicate question detected. Skipping.")
                continue
            seen_questions.add(question_text)

            print(f"\n❓ Question: ({difficulty_levels[current_difficulty]}, {points[current_difficulty]} points)")
            print(question_text)
            for idx, option in enumerate(mcq_dict["options"], start=1):
                print(f"  {chr(96 + idx)}) {option}")

            candidate_choice = input("\n🧠 Your Answer (a/b/c/d): ").strip().lower()
            option_index = ord(candidate_choice) - 97

            if 0 <= option_index < len(mcq_dict["options"]):
                candidate_answer = mcq_dict["options"][option_index]
            else:
                print("❌ Invalid choice.")
                continue

            result = evaluator.run(
                "evaluator",
                candidate_answer=candidate_answer,
                correct_answer=mcq_dict["correct_answer"]
            )

            print("\n🎯 Evaluation Result:")
            print(result)

            result_str = str(result).strip().lower()
            if result_str == "correct":
                print("✅ Correct! Increasing difficulty.")
                points_scored += points[current_difficulty]
                if current_difficulty < len(difficulty_levels) - 1:
                    current_difficulty += 1
            elif result_str == "incorrect":
                print("❌ Incorrect! Decreasing difficulty.")
                if current_difficulty > 0:
                    current_difficulty -= 1

        except Exception as e:
            print("❌ Unexpected error:", e)

    print("\n📊 Final Score Summary:")
    print(f"✅ Total Score: {points_scored}")
