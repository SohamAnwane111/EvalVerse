import re

class ContentFilter:
    _default_instance = None 

    def __init__(self, banned_words=None):
        self.banned_words = banned_words or [
            "stupid", "idiot", "dumb", "moron", "shit", "fuck", "faggot", "bitch", "nigger", "slut",
            "kill yourself", "go die", "rape", "bomb", "terrorist", "suicide", "you people", "your kind",
            "lazy indians", "dumb americans", "fat pig", "why are you like that", "disgusting",
            "i hate you", "you’re useless", "what’s wrong with your country", "back to your country",
            "too poor", "no education", "third world", "are you even human"
        ]

        self.patterns = [re.compile(rf"\b{re.escape(word)}\b", re.IGNORECASE) for word in self.banned_words]

    def contains_banned(self, text: str) -> bool:
        return any(p.search(text) for p in self.patterns)

    def guard(self, fallback=None, extra_words=None):
        all_patterns = self.patterns.copy()
        if extra_words:
            all_patterns += [re.compile(rf"\b{re.escape(word)}\b", re.IGNORECASE) for word in extra_words]

        def decorator(func):
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                if isinstance(result, str) and any(p.search(result) for p in all_patterns):
                    print(f"🚫 Output blocked by ContentFilter:")
                    return fallback
                print('✅ Passed by ContentFilter')
                return result
            return wrapper
        return decorator

    @classmethod
    def static_guard(cls, fallback=None, extra_words=None):
        if cls._default_instance is None:
            cls._default_instance = cls()
        return cls._default_instance.guard(fallback=fallback, extra_words=extra_words)
