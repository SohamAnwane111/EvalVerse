from sentence_transformers import SentenceTransformer, util

class ContextRelevanceFilter:
    _default_instance = None

    def __init__(self, model_name='BAAI/bge-small-en-v1.5'):
        print("🔍 Loading semantic similarity model...")
        self.model = SentenceTransformer(model_name)

    def get_similarity_score(self, context: str, question: str) -> float:
        """
        Returns cosine similarity between context and question.
        """
        embeddings = self.model.encode([context, question], convert_to_tensor=True)
        return util.cos_sim(embeddings[0], embeddings[1]).item()

    def is_related(self, context: str, question: str, threshold: float = 0.5) -> bool:
        """
        Returns True if the question is contextually related to the context based on cosine similarity.
        """
        score = self.get_similarity_score(context, question)
        print(f"🧠 Similarity Score: {score:.2f}")
        return score >= threshold

    def filter_unrelated(self, pairs: list[tuple], threshold: float = 0.5) -> list[tuple]:
        """
        Filters out (context, question) pairs that are not contextually related.
        """
        return [(ctx, q) for ctx, q in pairs if self.is_related(ctx, q, threshold)]

    def guard(self, context: str, fallback=None, threshold: float = 0.5):
        """
        Decorator to check if the returned question is relevant to the given context.
        If not, return fallback.
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)

                # Handle string, dict, or object output
                question = None
                if isinstance(result, str):
                    question = result
                elif isinstance(result, dict):
                    question = result.get('question') or result.get('question_text')
                elif hasattr(result, 'question'):
                    question = getattr(result, 'question')

                if question and not self.is_related(context, question, threshold):
                    print("🚫 Output blocked by ContextRelevanceChecker")
                    return fallback

                print("✅ Passed by ContextRelevanceChecker")
                return result
            return wrapper
        return decorator

    @classmethod
    def static_guard(cls, context: str, fallback=None, threshold: float = 0.5):
        if cls._default_instance is None:
            cls._default_instance = cls()
        return cls._default_instance.guard(context=context, fallback=fallback, threshold=threshold)
