"""
Vocabulary Analyzer - Collects stories and extracts new vocabulary using the same model.
"""

import torch
from transformers import AutoProcessor, Qwen2VLForConditionalGeneration


class VocabularyAnalyzer:
    """Collects stories and extracts new vocabulary."""

    _model_cache = None
    _processor_cache = None

    def __init__(self):
        self.stories: list[str] = []

    def add_story(self, story: str) -> None:
        """Add a generated story to the internal list."""
        if story:
            self.stories.append(story.strip())

    def _load_model(self):
        """Lazy-load the model/processor (shared across instances)."""
        if VocabularyAnalyzer._model_cache is not None and VocabularyAnalyzer._processor_cache is not None:
            return VocabularyAnalyzer._model_cache, VocabularyAnalyzer._processor_cache

        model_name = "Qwen/Qwen2-VL-2B-Instruct"
        processor = AutoProcessor.from_pretrained(model_name, trust_remote_code=True)
        model = Qwen2VLForConditionalGeneration.from_pretrained(
            model_name,
            device_map="auto",
            trust_remote_code=True,
            load_in_4bit=True  # keep memory low
        )

        VocabularyAnalyzer._model_cache = model
        VocabularyAnalyzer._processor_cache = processor
        return model, processor

    def extract_new_vocabulary(self) -> str:
        """Extract one new vocabulary item from all stored stories."""
        if not self.stories:
            return "No stories available yet."

        model, processor = self._load_model()
        device = "cuda" if torch.cuda.is_available() else "cpu"

        stories_text = "\n\n".join(self.stories[-20:])  # limit context to recent items

        # Build messages (text-only)
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a vocabulary tutor for children. Given the stories below, extract exactly ONE useful new noun."
                    "If the word is already listed before, pick another. "
                    "Format exactly:\n"
                    "Vocabulary: <word>\n"
                ),
            },
            {
                "role": "user",
                "content": f"Stories:\n{stories_text}\n\nExtract one new vocabulary item.",
            },
        ]

        text = processor.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs = processor(
            text=[text],
            return_tensors="pt",
        ).to(device)

        with torch.no_grad():
            output = model.generate(
                **inputs,
                max_new_tokens=64,
                temperature=0.6,
            )

        result = processor.batch_decode(output, skip_special_tokens=True)[0]
        return result.strip()


    def learn_vocabulary(self):
        vocabulary = self.extract_new_vocabulary()
        # INSERT_YOUR_CODE
        # Call speakText to give positive feedback and encourage drawing using the new vocabulary
        phrase = f"Good job! You learned new vocabulary! Can you draw {vocabulary}?"
        if hasattr(self, "speakText"):
            self.speakText(phrase, "en")

        return vocabulary