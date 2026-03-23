"""Tests for Agent Integration - Standalone Functions"""

import os
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path


class TestLanguageDetection:
    """Test language detection in agent context."""

    def test_detect_english(self):
        """Test English detection."""
        with patch("src.language_detector.fasttext") as mock_ft:
            mock_model = MagicMock()
            mock_model.predict.return_value = ("__label__en", 0.95)
            mock_ft.load_model.return_value = mock_model
            
            from src.language_detector import LanguageDetector
            detector = LanguageDetector()
            
            result = detector.detect("What are the best colleges?")
            assert result == "en"

    def test_detect_hindi(self):
        """Test Hindi detection."""
        with patch("src.language_detector.fasttext") as mock_ft:
            mock_model = MagicMock()
            mock_model.predict.return_value = ("__label__hi", 0.90)
            mock_ft.load_model.return_value = mock_model
            
            from src.language_detector import LanguageDetector
            detector = LanguageDetector()
            
            result = detector.detect("कॉलेज के बारे में बताओ")
            assert result == "hi"

    def test_detect_hinglish(self):
        """Test Hinglish detection."""
        with patch("src.language_detector.fasttext") as mock_ft:
            mock_model = MagicMock()
            mock_model.predict.return_value = ("__label__hi", 0.85)
            mock_ft.load_model.return_value = mock_model
            
            from src.language_detector import LanguageDetector
            detector = LanguageDetector()
            
            result = detector.detect("College ka fees kitna hai?")
            assert result == "hi_roi"

    def test_detect_tamil(self):
        """Test Tamil detection."""
        with patch("src.language_detector.fasttext") as mock_ft:
            mock_model = MagicMock()
            mock_model.predict.return_value = ("__label__ta", 0.92)
            mock_ft.load_model.return_value = mock_model
            
            from src.language_detector import LanguageDetector
            detector = LanguageDetector()
            
            result = detector.detect("கல்லூரி பற்றி தெரிவு")
            assert result == "ta"


class TestWaitMessages:
    """Test wait messages for all languages."""

    def test_wait_message_english(self):
        """Test English wait message."""
        from config.languages import WAIT_MESSAGES
        assert "Wait, I will give you the response to your query." in WAIT_MESSAGES["en"]

    def test_wait_message_hindi(self):
        """Test Hindi wait message."""
        from config.languages import WAIT_MESSAGES
        assert "प्रतीक्षा" in WAIT_MESSAGES["hi"]

    def test_wait_message_hinglish(self):
        """Test Hinglish wait message."""
        from config.languages import WAIT_MESSAGES
        assert "wait" in WAIT_MESSAGES["hi_roi"].lower()

    def test_wait_message_all_languages(self):
        """Test all languages have wait messages."""
        from config.languages import SUPPORTED_LANGUAGES
        
        for lang_code in SUPPORTED_LANGUAGES:
            from config.languages import WAIT_MESSAGES
            assert lang_code in WAIT_MESSAGES, f"Missing wait message for {lang_code}"


class TestCollegeSearch:
    """Test college search functionality."""

    @patch("src.college_search.TavilyClient")
    def test_search_returns_results(self, mock_tavily):
        """Test college search returns results."""
        mock_client = MagicMock()
        mock_tavily.return_value = mock_client
        
        mock_response = {
            "results": [
                {"title": "IIT Bombay", "content": "Top college", "url": "https://careers360.com/iit-bombay"},
                {"title": "IIT Delhi", "content": "Premier institute", "url": "https://careers360.com/iit-delhi"},
            ]
        }
        mock_client.search.return_value = mock_response
        
        from src.college_search import CollegeSearch
        search = CollegeSearch(api_key="test_key")
        
        results = search.search_colleges("IIT colleges")
        
        assert len(results) == 2

    @patch("src.college_search.TavilyClient")
    def test_search_limits_to_careers360(self, mock_tavily):
        """Test that searches are limited to Careers360."""
        mock_client = MagicMock()
        mock_tavily.return_value = mock_client
        mock_client.search.return_value = {"results": []}
        
        from src.college_search import CollegeSearch
        search = CollegeSearch(api_key="test_key")
        
        search.search_colleges("engineering")
        
        call_kwargs = mock_client.search.call_args.kwargs
        domains = call_kwargs.get("include_domains", [])
        
        assert any("careers360.com" in d for d in domains)

    @patch("src.college_search.TavilyClient")
    def test_format_for_voice(self, mock_tavily):
        """Test formatting results for voice."""
        mock_client = MagicMock()
        mock_tavily.return_value = mock_client
        
        from src.college_search import CollegeSearch
        search = CollegeSearch(api_key="test_key")
        
        results = [
            {"title": "IIT Bombay", "content": "Top engineering college"},
            {"title": "IIT Delhi", "content": "Premier institute"},
        ]
        
        formatted = search.format_for_voice(results)
        
        assert "IIT Bombay" in formatted
        assert "IIT Delhi" in formatted


class TestSettings:
    """Test configuration settings."""

    def test_feature_flags(self):
        """Test feature flags are defined."""
        from config.settings import settings
        
        assert hasattr(settings, "enable_sarvam_tts")
        assert hasattr(settings, "enable_college_search")
        assert hasattr(settings, "enable_language_detection")

    def test_is_configured_requires_all_keys(self):
        """Test is_configured checks all required keys."""
        from config.settings import Settings
        
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings(
                videosdk_auth_token="",
                google_api_key="",
                sarvam_api_key="",
                tavily_api_key=""
            )
            assert settings.is_configured() is False

    def test_get_missing_keys(self):
        """Test getting list of missing keys."""
        from config.settings import Settings
        
        settings = Settings(
            videosdk_auth_token="token",
            google_api_key="",
            sarvam_api_key="",
            tavily_api_key=""
        )
        
        missing = settings.get_missing_keys()
        assert "GOOGLE_API_KEY" in missing
        assert "SARVAM_API_KEY" in missing
        assert "TAVILY_API_KEY" in missing


class TestTTSMapping:
    """Test language to TTS mapping."""

    def test_language_to_sarvam_code(self):
        """Test language code mapping."""
        from config.languages import LANGUAGE_TO_SARVAM_CODE
        
        assert LANGUAGE_TO_SARVAM_CODE["en"] == "en-IN"
        assert LANGUAGE_TO_SARVAM_CODE["hi"] == "hi-IN"
        assert LANGUAGE_TO_SARVAM_CODE["ta"] == "ta-IN"
        assert LANGUAGE_TO_SARVAM_CODE["hi_roi"] == "hi-IN"

    def test_language_to_voice(self):
        """Test voice mapping."""
        from config.languages import LANGUAGE_TO_VOICE
        
        assert LANGUAGE_TO_VOICE["en"]["default"] == "anushka"
        assert LANGUAGE_TO_VOICE["hi"]["default"] == "anushka"
        assert LANGUAGE_TO_VOICE["ta"]["default"] == "divya"

    def test_supported_languages_count(self):
        """Test that 12 languages are supported."""
        from config.languages import SUPPORTED_LANGUAGES
        
        assert len(SUPPORTED_LANGUAGES) == 12