"""Sarvam TTS Module - Text-to-Speech using Sarvam AI"""

import os
import logging
from typing import Optional

from config.languages import LANGUAGE_TO_SARVAM_CODE, LANGUAGE_TO_VOICE

logger = logging.getLogger(__name__)

try:
    from sarvamai import SarvamAI
except ImportError:
    SarvamAI = None


class SarvamTTS:
    """Sarvam AI Text-to-Speech service for Indian languages."""

    def __init__(self, api_key: Optional[str] = None):
        if SarvamAI is None:
            raise ImportError("sarvamai package not installed. Run: pip install sarvamai")
        
        self.api_key = api_key or os.getenv("SARVAM_API_KEY")
        if not self.api_key:
            raise ValueError("SARVAM_API_KEY is required")
        
        self.client = SarvamAI(api_subscription_key=self.api_key)
        logger.info("Sarvam TTS client initialized")

    def synthesize(
        self,
        text: str,
        language_code: str,
        speaker: str = "anushka",
        model: str = "bulbul:v2",
        enable_preprocessing: bool = False,
    ) -> str:
        """
        Synthesize text to speech.
        
        Args:
            text: Text to synthesize
            language_code: Sarvam language code (e.g., 'en-IN', 'hi-IN')
            speaker: Voice speaker name
            model: TTS model to use
            enable_preprocessing: Enable text preprocessing
            
        Returns:
            Base64 encoded audio data
        """
        if not text:
            raise ValueError("Text is required for synthesis")
        
        if not self.api_key:
            raise ValueError("API key is required")
        
        logger.info(f"Synthesizing: {text[:50]}... ({language_code}, {speaker})")
        
        response = self.client.text_to_speech.convert(
            target_language_code=language_code,
            text=text,
            model=model,
            speaker=speaker,
            enable_preprocessing=enable_preprocessing,
        )
        
        logger.info("TTS synthesis completed")
        return response.audio

    def get_voice_for_language(
        self,
        lang_code: str,
        gender: str = "female"
    ) -> str:
        """
        Get default voice for a language.
        
        Args:
            lang_code: Language code (e.g., 'en', 'hi')
            gender: 'male' or 'female'
            
        Returns:
            Speaker name
        """
        voice_config = LANGUAGE_TO_VOICE.get(lang_code, {})
        
        if gender == "male":
            return voice_config.get("male", "abhilash")
        return voice_config.get("default", "anushka")

    def map_language_code(self, lang_code: str) -> str:
        """
        Map internal language code to Sarvam format.
        
        Args:
            lang_code: Internal language code (e.g., 'en', 'hi')
            
        Returns:
            Sarvam language code (e.g., 'en-IN', 'hi-IN')
        """
        return LANGUAGE_TO_SARVAM_CODE.get(lang_code, "en-IN")

    def get_supported_languages(self) -> list[str]:
        """Get list of supported language codes."""
        return list(LANGUAGE_TO_SARVAM_CODE.keys())

    def is_supported(self, lang_code: str) -> bool:
        """Check if language is supported."""
        return lang_code in LANGUAGE_TO_SARVAM_CODE


def get_tts_service(api_key: Optional[str] = None) -> SarvamTTS:
    """Factory function to get TTS service instance."""
    return SarvamTTS(api_key=api_key)