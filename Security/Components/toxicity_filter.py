from transformers import pipeline

class ToxicityFilter:
    _default_instance = None 
    _default_model_name = "facebook/roberta-hate-speech-dynabench-r1-target"

    def __init__(self, model_name=None):
        self.model_name = model_name or self._default_model_name

        print("🧠 Initializing ToxicityFilter...")
        print(f"📦 Loading model: {self.model_name}")
        
        try:
            self.pipeline = pipeline("text-classification", model=self.model_name, truncation=True)
            print("✅ Model loaded successfully.")
        except Exception as e:
            print("❌ Failed to load the model.")
            raise e

    def is_toxic(self, text: str, threshold: float = 0.5) -> bool:
        """
        Check if a single text string is toxic (label = 'LABEL_1') above a given threshold.
        """
        print(f"🔍 Checking text: {text}")
        result = self.pipeline(text)[0]  
        label, score = result['label'], result['score']

        print(f"🧪 Result: Label={label}, Score={score:.4f}")
        return label == "LABEL_1" and score >= threshold

    def filter_toxicity(self, text_list: list, threshold: float = 0.5) -> list:
        """
        Filters out toxic texts from a list.
        """
        print("📜 Filtering list of texts for toxicity...")
        return [text for text in text_list if not self.is_toxic(text, threshold=threshold)]

    def guard(self, fallback=None, threshold: float = 0.5):
        """
        Decorator to filter the return value of a function.
        If the returned string is toxic, return `fallback` instead.
        """
        print("🛡️ Setting up ToxicityFilter decorator...")

        def decorator(func):
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                if isinstance(result, str) and self.is_toxic(result, threshold):
                    print(f"🚫 Output blocked by ToxicityFilter.")
                    return fallback
                print("✅ Passed by ToxicityFilter.")
                return result
            return wrapper
        return decorator

    @classmethod
    def static_guard(cls, fallback=None, threshold: float = 0.5):
        """
        Singleton-based decorator for easy usage across large codebases.
        """
        if cls._default_instance is None:
            print("🚀 Creating default ToxicityFilter instance...")
            cls._default_instance = cls()
        return cls._default_instance.guard(fallback=fallback, threshold=threshold)
