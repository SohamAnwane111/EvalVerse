import re
import pickle

class ContentFilter:
    _default_instance = None
    _default_banned_words_path = "Security/Components/.hidden/filter.sys_dump.key"  

    def __init__(self, banned_words=None):
        print("🧠 Initializing ContentFilter...")
        print(f"📂 Loading banned words...")

        try:
            with open(self._default_banned_words_path, "rb") as f:
                self.banned_words = pickle.load(f)
            print(f"✅ Loaded {len(self.banned_words)} banned words from file.")
        except FileNotFoundError:
            print("❌ Banned words file not found. Initializing with empty list.")
            self.banned_words = []

        if banned_words:
            print(f"➕ Merging {len(banned_words)} additional banned words...")
            added_words = [word for word in banned_words if word not in self.banned_words]
            self.banned_words += added_words
            print(f"📈 Total banned words after merge: {len(self.banned_words)}")

        self.patterns = [re.compile(rf"\b{re.escape(word)}\b", re.IGNORECASE) for word in self.banned_words]
        print("🔧 Compiled regex patterns for banned words.")

    def contains_banned(self, text: str) -> bool:
        print(f"🔍 Scanning text for banned words: \"{text}\"")
        found = any(p.search(text) for p in self.patterns)
        print("🚫 Banned word found!" if found else "✅ Text is clean.")
        return found

    def guard(self, fallback=None, extra_words=None):
        print("🛡️ Setting up ContentFilter decorator...")
        all_patterns = self.patterns.copy()

        if extra_words:
            print(f"➕ Adding {len(extra_words)} extra words to filter dynamically.")
            extra_patterns = [re.compile(rf"\b{re.escape(word)}\b", re.IGNORECASE) for word in extra_words]
            all_patterns += extra_patterns

        def decorator(func):
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                if isinstance(result, str) and any(p.search(result) for p in all_patterns):
                    print("🚫 Output blocked by ContentFilter")
                    return fallback
                print("✅ Passed by ContentFilter")
                return result
            return wrapper
        return decorator

    @classmethod
    def static_guard(cls, fallback=None, extra_words=None, additional_words=None):
        if cls._default_instance is None:
            print("🚀 Creating default ContentFilter instance...")
            cls._default_instance = cls(banned_words=additional_words)
        return cls._default_instance.guard(fallback=fallback, extra_words=extra_words)
