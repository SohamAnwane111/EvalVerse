from Security.Components.content_filter import ContentFilter
from Security.Components.toxicity_filter import ToxicityFilter
from Security.Components.context_relevance_filter import ContextRelevanceFilter

class SecurityFilter:
    _default_instance = None

    def __init__(self, fallback=None, extra_words=None, toxic_threshold=0.5, similarity_threshold=0.5, context="Assume Everything"):
        self.fallback = fallback
        self.extra_words = extra_words or []
        self.toxic_threshold = toxic_threshold
        self.similarity_threshold = similarity_threshold
        self.context = context

        self.content_security = ContentFilter(banned_words=self.extra_words)
        self.toxicity_security = ToxicityFilter()
        self.context_relevance_security = ContextRelevanceFilter()

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            result_text = str(result)

            print("\n🔒 [Security Check] Starting filter chain...\n")

            # Content Filter
            print("🛡️ ContentFilter: Checking for banned words...")
            if self.content_security.contains_banned(result_text):
                print("🚫 Blocked by ContentFilter\n")
                return self.fallback
            print("✅ Passed ContentFilter")

            # Toxicity Filter
            print("☣️ ToxicityFilter: Evaluating toxicity level...")
            if self.toxicity_security.is_toxic(result_text, self.toxic_threshold):
                print("🚫 Blocked by ToxicityFilter\n")
                return self.fallback
            print("✅ Passed ToxicityFilter")

            # Context Relevance Filter
            print("📚 ContextRelevanceFilter: Checking contextual similarity...")
            if not self.context_relevance_security.is_related(self.context, result_text, self.similarity_threshold):
                print("🚫 Blocked by ContextRelevanceFilter\n")
                return self.fallback
            print("✅ Passed ContextRelevanceFilter")

            print("🎉 ✅ Passed ALL Security Filters\n")
            return result

        return wrapper
