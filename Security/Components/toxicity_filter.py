from transformers import pipeline

class ToxicityFilter:

    _default_instance = None 

    def __init__(self, model_name="unitary/toxic-bert"):
        self.model_name = model_name
        self.pipeline = pipeline("text-classification", model=self.model_name)

    def is_toxic(self, text: str, threshold: float = 0.5) -> bool:
        """
        Check if a single text string is toxic above a given threshold.
        """
        result = self.pipeline(text)[0]  
        score = result['score'] 

        return score >= threshold


    def filter_toxicity(self, text_list: list) -> list:
        """
        Filters out toxic texts from a list.
        """
        return [text for text in text_list if not self.is_toxic(text)]

    def guard(self, fallback=None, threshold: float = 0.5):
        """
        Decorator to filter the return value of a function.
        If the returned string is toxic, return `fallback` instead.
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                if isinstance(result, str) and self.is_toxic(result, threshold):
                    print(f"🚫 Output blocked by ToxicityFilter:")
                    return fallback
                print('✅ Passed by ToxicityFilter')
                return result
            return wrapper
        return decorator

    @classmethod
    def static_guard(cls, fallback=None, threshold: float = 0.5):
        if cls._default_instance is None:
            cls._default_instance = cls()
        return cls._default_instance.guard(fallback=fallback, threshold=threshold)