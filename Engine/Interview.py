from uuid import uuid4
from Agents.InterviewAnalyzer.interview_ques_gen import InterviewQGen
from Agents.InterviewAnalyzer.interview_ques_eval import InterviewQEval
import random
from Engine import str2json, voice2text
from Security.security_filter import SecurityFilter


question_gen = InterviewQGen()
evaluator = InterviewQEval()


def get_category():
    categories = [
        'hr',
        'situational',
        'ethical',
        'communication',
        'leadership',
        'conflict',
        'creative',
        'decision-making'
    ]
    category = random.choice(categories)
    print(f"🎯 Randomly selected category: {category}")
    return category




def generate_interview_question(category, seen_questions):
    question_id = str(uuid4())

    @SecurityFilter(fallback=None, toxic_threshold=0.3, similarity_threshold=0.1, context=category)
    def generate_one_question():
        return question_gen.run(
            'interview_ques_gen',
            category=category,
            question_id=question_id,
            seen_questions=seen_questions
        )
    
    retries = 5
    response = None
    while retries > 0:
        response = str2json.extract_first_json_safe(str(generate_one_question()))
        if response is None:
            print("❌ Failed to generate a question. Retrying...")
            retries -= 1
        else:
            break

    return {
        "id": question_id,
        "category": category,
        "text": response['question_text']
    }


def get_candidate_answer(question_text, duration=20):
    print(f"\n📝 Interview Question:\n{question_text}")
    input(f"\n⏺️ Press Enter to start recording your answer ({duration})...")

    audio_path = voice2text.record_audio(duration=20)
    transcript = voice2text.transcribe_audio(audio_path)

    print(f"\n📄 Transcribed Answer: {transcript}")
    return transcript



def evaluate_answer(question_text, answer, category):
    eval_response = str2json.extract_first_json_safe(str(evaluator.run('interview_ques_eval',
        category=category,
        question=question_text,
        answer=answer
    )))
    return {
        "rating": eval_response.get("rating", "UNKNOWN"),
        "rationale": eval_response.get("rationale", "No explanation provided.")
    }


def print_evaluation(result):
    print("\n📊 Evaluation Result:")
    print(f"🏷️ Rating: {result['rating'].upper()}")
    print(f"🧠 Reasoning: {result['rationale']}")


def run_one_question_interview():
    print("\n👩‍💻 Welcome to the One-Question Interview!\n")
    category = get_category()
    seen_questions = [] 

    q_data = generate_interview_question(category, seen_questions)
    seen_questions.append(q_data['text'])

    answer = get_candidate_answer(q_data['text'])

    evaluation = evaluate_answer(q_data['text'], answer, category)

    print_evaluation(evaluation)


if __name__ == "__main__":
    run_one_question_interview()
