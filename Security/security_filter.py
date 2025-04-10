from Security.Components.content_filter import ContentFilter
from Security.Components.toxicity_filter import ToxicityFilter
from Security.Components.context_relevance_filter import ContextRelevanceFilter

class SecurityFilter:
    _default_instance = None
    _banner_shown = False  

    def __init__(self, fallback=None, extra_words=None, toxic_threshold=0.5, similarity_threshold=0.5, context="Assume Everything"):
        self.fallback = fallback
        self.extra_words = extra_words or []
        self.toxic_threshold = toxic_threshold
        self.similarity_threshold = similarity_threshold
        self.context = context

        print("🛠️  Initializing SecurityFilter with:")
        print(f"   • Toxicity Threshold: {self.toxic_threshold}")
        print(f"   • Similarity Threshold: {self.similarity_threshold}")
        print(f"   • Context: \"{self.context}\"\n")

        self.content_security = ContentFilter(banned_words=self.extra_words)
        self.toxicity_security = ToxicityFilter()
        self.context_relevance_security = ContextRelevanceFilter()

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            if not SecurityFilter._banner_shown:
                self._show_ascii_banner()
                SecurityFilter._banner_shown = True

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

    def _show_ascii_banner(self):
        print(r"""
 _____                      _ _          ______ _ _ _            
/  ___|                    (_| |         |  ___(_| | |           
\ `--.  ___  ___ _   _ _ __ _| |_ _   _  | |_   _| | |_ ___ _ __ 
 `--. \/ _ \/ __| | | | '__| | __| | | | |  _| | | | __/ _ | '__|
/\__/ |  __| (__| |_| | |  | | |_| |_| | | |   | | | ||  __| |   
\____/ \___|\___|\__,_|_|  |_|\__|\__, | \_|   |_|_|\__\___|_|   
                                   __/ |                         
                                  |___/                          
                                                        
        """)

