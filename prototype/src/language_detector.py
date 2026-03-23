"""Language Detector Module - FastText-based Indian Language Detection"""

import os
import logging
from pathlib import Path
from typing import Optional

import fasttext

from config.languages import (
    SUPPORTED_LANGUAGES,
    WAIT_MESSAGES,
    FASTTEXT_LANGUAGE_MAP,
)

logger = logging.getLogger(__name__)

DEFAULT_MODEL_URL = "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin"


class LanguageDetector:
    """FastText-based language detector for 12 Indian languages + English."""

    def __init__(self, model_path: str = "models/lid.176.bin"):
        self.model_path = model_path
        self._model = None
        self._load_model()

    def _load_model(self) -> None:
        """Load or download the FastText model."""
        model_file = Path(self.model_path)
        
        if not model_file.exists():
            logger.info(f"Model not found at {self.model_path}, downloading...")
            self._model = self._download_model()
        else:
            logger.info(f"Loading model from {self.model_path}")
            self._model = fasttext.load_model(str(model_file))

    def _download_model(self):
        """Download the FastText model from Facebook's CDN."""
        import urllib.request
        import shutil
        
        model_file = Path(self.model_path)
        model_file.parent.mkdir(parents=True, exist_ok=True)
        
        temp_path = model_file.with_suffix(".bin.tmp")
        
        logger.info(f"Downloading FastText model from {DEFAULT_MODEL_URL}")
        urllib.request.urlretrieve(DEFAULT_MODEL_URL, temp_path)
        
        shutil.move(str(temp_path), str(model_file))
        logger.info("Model downloaded successfully")
        
        return fasttext.load_model(str(model_file))

    def detect(self, text: str) -> str:
        """
        Detect the language of the given text.
        
        Args:
            text: Input text in any language
            
        Returns:
            Language code (e.g., 'en', 'hi', 'ta', 'hi_roi')
        """
        if not text or not text.strip():
            return "en"
        
        text = text.strip()
        
        prediction = self._model.predict(text, k=1)
        
        if isinstance(prediction[1], (list, tuple)):
            detected_label = prediction[0][0]
            confidence = prediction[1][0] if prediction[1] else 0.0
        else:
            detected_label = prediction[0]
            confidence = prediction[1]
        
        logger.info(f"Detected: {detected_label} (confidence: {confidence:.2f})")
        
        lang_code = FASTTEXT_LANGUAGE_MAP.get(detected_label, "en")
        
        if lang_code == "hi" and self._is_romanized_hindi(text):
            lang_code = "hi_roi"
        
        return lang_code

    def _is_romanized_hindi(self, text: str) -> bool:
        """
        Check if the text is in Romanized Hindi (Hinglish).
        
        Args:
            text: Input text
            
        Returns:
            True if text appears to be Romanized Hindi
        """
        romanized_hindi_indicators = [
            "ka", "ki", "ko", "ke", "kaa", "kee", "kya", "kyu",
            "hai", "hain", "tha", "thi", "the", "ho", "hua",
            "me", "ko", "se", "pe", "par", "ke", "ka",
            "aur", "ya", "lekin", "to", "phir", "iska", "uska",
            "ye", "wo", "kya", "kaise", "kitna", "kab", "kaha",
            "college", "fees", "admission", "course", "karo",
            "hai", "mil", "jana", "aana", "jana", "dekho",
        ]
        
        text_lower = text.lower()
        words = text_lower.split()
        
        hindi_roman_count = sum(1 for word in words if word in romanized_hindi_indicators)
        
        return hindi_roman_count >= 2

    def get_wait_message(self, lang_code: str) -> str:
        """
        Get the wait message in the specified language.
        
        Args:
            lang_code: Language code (e.g., 'en', 'hi', 'ta')
            
        Returns:
            Wait message in the specified language
        """
        return WAIT_MESSAGES.get(lang_code, WAIT_MESSAGES["en"])

    def get_supported_languages(self) -> list[str]:
        """Get list of supported language codes."""
        return list(SUPPORTED_LANGUAGES.keys())

    def is_supported(self, lang_code: str) -> bool:
        """Check if a language is supported."""
        return lang_code in SUPPORTED_LANGUAGES


def get_language_detector(model_path: str = "models/lid.176.bin") -> LanguageDetector:
    """Factory function to get a LanguageDetector instance."""
    return LanguageDetector(model_path=model_path)