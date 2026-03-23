"""Tests for Sarvam TTS Module"""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from pathlib import Path


class TestSarvamTTS:
    """Test cases for SarvamTTS class."""

    @patch("src.sarvam_tts.SarvamAI")
    def test_initialization_with_api_key(self, mock_sarvam):
        """Test that SarvamTTS initializes with API key."""
        mock_client = MagicMock()
        mock_sarvam.return_value = mock_client
        
        from src.sarvam_tts import SarvamTTS
        tts = SarvamTTS(api_key="test_key")
        
        assert tts.api_key == "test_key"

    @patch("src.sarvam_tts.SarvamAI")
    def test_initialization_with_env_var(self, mock_sarvam, monkeypatch):
        """Test that SarvamTTS uses env var if no key provided."""
        monkeypatch.setenv("SARVAM_API_KEY", "env_key")
        mock_client = MagicMock()
        mock_sarvam.return_value = mock_client
        
        from src.sarvam_tts import SarvamTTS
        tts = SarvamTTS()
        
        assert tts.api_key == "env_key"

    @patch("src.sarvam_tts.SarvamAI")
    def test_synthesize_english(self, mock_sarvam):
        """Test TTS synthesis for English."""
        mock_client = MagicMock()
        mock_sarvam.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.audio = "base64_audio_data"
        mock_client.text_to_speech.convert.return_value = mock_response
        
        from src.sarvam_tts import SarvamTTS
        tts = SarvamTTS(api_key="test_key")
        
        result = tts.synthesize("Hello, welcome to Careers360.", "en-IN", "anushka")
        
        assert result == "base64_audio_data"
        mock_client.text_to_speech.convert.assert_called_once()

    @patch("src.sarvam_tts.SarvamAI")
    def test_synthesize_hindi(self, mock_sarvam):
        """Test TTS synthesis for Hindi."""
        mock_client = MagicMock()
        mock_sarvam.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.audio = "base64_hindi_audio"
        mock_client.text_to_speech.convert.return_value = mock_response
        
        from src.sarvam_tts import SarvamTTS
        tts = SarvamTTS(api_key="test_key")
        
        result = tts.synthesize("नमस्ते, कैरियर्स360 में आपका स्वागत है।", "hi-IN", "anushka")
        
        assert result == "base64_hindi_audio"

    @patch("src.sarvam_tts.SarvamAI")
    def test_synthesize_tamil(self, mock_sarvam):
        """Test TTS synthesis for Tamil."""
        mock_client = MagicMock()
        mock_sarvam.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.audio = "base64_tamil_audio"
        mock_client.text_to_speech.convert.return_value = mock_response
        
        from src.sarvam_tts import SarvamTTS
        tts = SarvamTTS(api_key="test_key")
        
        result = tts.synthesize("கேரியர்ஸ்360விற்கு வரவேற்கிறோம்.", "ta-IN", "divya")
        
        assert result == "base64_tamil_audio"

    @patch("src.sarvam_tts.SarvamAI")
    def test_synthesize_with_custom_model(self, mock_sarvam):
        """Test TTS with custom model parameter."""
        mock_client = MagicMock()
        mock_sarvam.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.audio = "audio_data"
        mock_client.text_to_speech.convert.return_value = mock_response
        
        from src.sarvam_tts import SarvamTTS
        tts = SarvamTTS(api_key="test_key")
        
        result = tts.synthesize("Test text", "en-IN", "anushka", model="bulbul:v3")
        
        call_args = mock_client.text_to_speech.convert.call_args
        assert call_args.kwargs.get("model") == "bulbul:v3"

    @patch("src.sarvam_tts.SarvamAI")
    def test_synthesize_with_preprocessing(self, mock_sarvam):
        """Test TTS with preprocessing enabled."""
        mock_client = MagicMock()
        mock_sarvam.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.audio = "audio_data"
        mock_client.text_to_speech.convert.return_value = mock_response
        
        from src.sarvam_tts import SarvamTTS
        tts = SarvamTTS(api_key="test_key")
        
        result = tts.synthesize("Test 123 text", "en-IN", "anushka", enable_preprocessing=True)
        
        call_args = mock_client.text_to_speech.convert.call_args
        assert call_args.kwargs.get("enable_preprocessing") is True

    @patch("src.sarvam_tts.SarvamAI")
    def test_get_voice_for_language(self, mock_sarvam):
        """Test getting default voice for language."""
        mock_client = MagicMock()
        mock_sarvam.return_value = mock_client
        
        from src.sarvam_tts import SarvamTTS
        tts = SarvamTTS(api_key="test_key")
        
        assert tts.get_voice_for_language("en") == "anushka"
        assert tts.get_voice_for_language("hi") == "anushka"
        assert tts.get_voice_for_language("ta") == "divya"
        assert tts.get_voice_for_language("te") == "samantha"

    @patch("src.sarvam_tts.SarvamAI")
    def test_get_voice_for_language_male(self, mock_sarvam):
        """Test getting male voice for language."""
        mock_client = MagicMock()
        mock_sarvam.return_value = mock_client
        
        from src.sarvam_tts import SarvamTTS
        tts = SarvamTTS(api_key="test_key")
        
        assert tts.get_voice_for_language("en", gender="male") == "abhilash"
        assert tts.get_voice_for_language("hi", gender="male") == "abhilash"
        assert tts.get_voice_for_language("ta", gender="male") == "arul"

    @patch("src.sarvam_tts.SarvamAI")
    def test_map_language_code(self, mock_sarvam):
        """Test language code mapping."""
        mock_client = MagicMock()
        mock_sarvam.return_value = mock_client
        
        from src.sarvam_tts import SarvamTTS
        tts = SarvamTTS(api_key="test_key")
        
        assert tts.map_language_code("en") == "en-IN"
        assert tts.map_language_code("hi") == "hi-IN"
        assert tts.map_language_code("hi_roi") == "hi-IN"
        assert tts.map_language_code("bn") == "bn-IN"
        assert tts.map_language_code("ta") == "ta-IN"

    @patch("src.sarvam_tts.SarvamAI")
    def test_error_handling_empty_text(self, mock_sarvam):
        """Test error handling when text is empty."""
        from src.sarvam_tts import SarvamTTS
        
        mock_client = MagicMock()
        mock_sarvam.return_value = mock_client
        
        tts = SarvamTTS(api_key="test_key")
        
        with pytest.raises(ValueError, match="Text is required"):
            tts.synthesize("", "en-IN", "anushka")

    @patch("src.sarvam_tts.SarvamAI")
    def test_error_handling_api_error(self, mock_sarvam):
        """Test error handling when API returns error."""
        mock_client = MagicMock()
        mock_sarvam.return_value = mock_client
        
        mock_client.text_to_speech.convert.side_effect = Exception("API Error")
        
        from src.sarvam_tts import SarvamTTS
        tts = SarvamTTS(api_key="test_key")
        
        with pytest.raises(Exception, match="API Error"):
            tts.synthesize("Test text", "en-IN", "anushka")


class TestSarvamTTSIntegration:
    """Integration tests for SarvamTTS."""

    @patch("src.sarvam_tts.SarvamAI")
    def test_full_synthesis_flow_english(self, mock_sarvam):
        """Test complete synthesis flow for English."""
        mock_client = MagicMock()
        mock_sarvam.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.audio = "base64_encoded_audio"
        mock_client.text_to_speech.convert.return_value = mock_response
        
        from src.sarvam_tts import SarvamTTS
        tts = SarvamTTS(api_key="test_key")
        
        text = "What are the best engineering colleges in India?"
        lang_code = tts.map_language_code("en")
        voice = tts.get_voice_for_language("en")
        
        result = tts.synthesize(text, lang_code, voice)
        
        assert result == "base64_encoded_audio"
        mock_client.text_to_speech.convert.assert_called_once_with(
            target_language_code="en-IN",
            text="What are the best engineering colleges in India?",
            model="bulbul:v2",
            speaker="anushka",
            enable_preprocessing=False
        )

    @patch("src.sarvam_tts.SarvamAI")
    def test_full_synthesis_flow_hindi(self, mock_sarvam):
        """Test complete synthesis flow for Hindi."""
        mock_client = MagicMock()
        mock_sarvam.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.audio = "base64_hindi_audio"
        mock_client.text_to_speech.convert.return_value = mock_response
        
        from src.sarvam_tts import SarvamTTS
        tts = SarvamTTS(api_key="test_key")
        
        text = "भारत में सबसे अच्छे इंजीनियरिंग कॉलेज कौन से हैं?"
        lang_code = tts.map_language_code("hi")
        voice = tts.get_voice_for_language("hi")
        
        result = tts.synthesize(text, lang_code, voice)
        
        assert result == "base64_hindi_audio"

    @patch("src.sarvam_tts.SarvamAI")
    def test_get_supported_languages(self, mock_sarvam):
        """Test getting list of supported languages."""
        mock_client = MagicMock()
        mock_sarvam.return_value = mock_client
        
        from src.sarvam_tts import SarvamTTS
        tts = SarvamTTS(api_key="test_key")
        
        languages = tts.get_supported_languages()
        
        assert "en" in languages
        assert "hi" in languages
        assert "ta" in languages
        assert len(languages) == 12