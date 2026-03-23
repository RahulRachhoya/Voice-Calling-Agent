"""Tests for Language Detector Module"""

import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path


class TestLanguageDetector:
    """Test cases for LanguageDetector class."""

    @patch("src.language_detector.fasttext")
    def test_initialization_with_default_path(self, mock_fasttext):
        """Test that LanguageDetector initializes with default model path."""
        mock_model = MagicMock()
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        assert detector.model_path == "models/lid.176.bin"

    @patch("src.language_detector.fasttext")
    def test_initialization_with_custom_path(self, mock_fasttext):
        """Test that LanguageDetector accepts custom model path."""
        mock_model = MagicMock()
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector(model_path="custom/path/model.bin")
        
        assert detector.model_path == "custom/path/model.bin"

    @patch("src.language_detector.fasttext")
    def test_detect_english_text(self, mock_fasttext):
        """Test detection of English text."""
        mock_model = MagicMock()
        mock_model.predict.return_value = ("__label__en", 0.95)
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        result = detector.detect("What are the best colleges in India?")
        assert result == "en"

    @patch("src.language_detector.fasttext")
    def test_detect_hindi_text_devanagari(self, mock_fasttext):
        """Test detection of Hindi text in Devanagari script."""
        mock_model = MagicMock()
        mock_model.predict.return_value = ("__label__hi", 0.92)
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        result = detector.detect("भारत में सबसे अच्छे कॉलेज कौन से हैं?")
        assert result == "hi"

    @patch("src.language_detector.fasttext")
    def test_detect_hindi_text_romanized(self, mock_fasttext):
        """Test detection of Hindi text in Roman script (Hinglish)."""
        mock_model = MagicMock()
        mock_model.predict.return_value = ("__label__hi", 0.85)
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        result = detector.detect("Bhai college ka fees kitna hai?")
        assert result == "hi_roi"

    @patch("src.language_detector.fasttext")
    def test_detect_tamil_text(self, mock_fasttext):
        """Test detection of Tamil text."""
        mock_model = MagicMock()
        mock_model.predict.return_value = ("__label__ta", 0.93)
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        result = detector.detect("இந்தியாவில் சிறந்த கல்லூரிகள் எவை?")
        assert result == "ta"

    @patch("src.language_detector.fasttext")
    def test_detect_bengali_text(self, mock_fasttext):
        """Test detection of Bengali text."""
        mock_model = MagicMock()
        mock_model.predict.return_value = ("__label__bn", 0.91)
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        result = detector.detect("ভারতের সেরা কলেজ কোনগুলো?")
        assert result == "bn"

    @patch("src.language_detector.fasttext")
    def test_detect_telugu_text(self, mock_fasttext):
        """Test detection of Telugu text."""
        mock_model = MagicMock()
        mock_model.predict.return_value = ("__label__te", 0.90)
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        result = detector.detect("భారతదేశంలో ఉత్తమ కళాశాలలు ఏవి?")
        assert result == "te"

    @patch("src.language_detector.fasttext")
    def test_detect_kannada_text(self, mock_fasttext):
        """Test detection of Kannada text."""
        mock_model = MagicMock()
        mock_model.predict.return_value = ("__label__kn", 0.89)
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        result = detector.detect("ಭಾರತದ ಉತ್ತಮ ಕಾಲೇಜುಗಳು ಯಾವುವು?")
        assert result == "kn"

    @patch("src.language_detector.fasttext")
    def test_detect_malayalam_text(self, mock_fasttext):
        """Test detection of Malayalam text."""
        mock_model = MagicMock()
        mock_model.predict.return_value = ("__label__ml", 0.88)
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        result = detector.detect("ഇന്ത്യയിലെ മികച്ച കോളേജുകൾ ഏവയാണ്?")
        assert result == "ml"

    @patch("src.language_detector.fasttext")
    def test_detect_marathi_text(self, mock_fasttext):
        """Test detection of Marathi text."""
        mock_model = MagicMock()
        mock_model.predict.return_value = ("__label__mr", 0.91)
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        result = detector.detect("भारतातील सर्वोत्तम महाविद्यालये कोणती?")
        assert result == "mr"

    @patch("src.language_detector.fasttext")
    def test_detect_gujarati_text(self, mock_fasttext):
        """Test detection of Gujarati text."""
        mock_model = MagicMock()
        mock_model.predict.return_value = ("__label__gu", 0.90)
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        result = detector.detect("ભારતમાં સૌથી શ્રેષ્ઠ કોલેજો કયાં છે?")
        assert result == "gu"

    @patch("src.language_detector.fasttext")
    def test_detect_punjabi_text(self, mock_fasttext):
        """Test detection of Punjabi text."""
        mock_model = MagicMock()
        mock_model.predict.return_value = ("__label__pa", 0.89)
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        result = detector.detect("ਭਾਰਤ ਦੀਆਂ ਸਭ ਤੋਂ ਵਧੀਆ ਕਾਲਜ ਕਿਹੜੇ ਹਨ?")
        assert result == "pa"

    @patch("src.language_detector.fasttext")
    def test_detect_odia_text(self, mock_fasttext):
        """Test detection of Odia text."""
        mock_model = MagicMock()
        mock_model.predict.return_value = ("__label__or", 0.88)
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        result = detector.detect("ଭାରତର ସର୍ବୋତ୍ਤਮ କଲେଜ କେଉଁଗୁଡ଼ਿਕ?")
        assert result == "or"

    @patch("src.language_detector.fasttext")
    def test_get_wait_message_english(self, mock_fasttext):
        """Test wait message generation for English."""
        mock_model = MagicMock()
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        msg = detector.get_wait_message("en")
        assert msg == "Wait, I will give you the response to your query."

    @patch("src.language_detector.fasttext")
    def test_get_wait_message_hindi(self, mock_fasttext):
        """Test wait message generation for Hindi."""
        mock_model = MagicMock()
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        msg = detector.get_wait_message("hi")
        assert msg == "प्रतीक्षा करें, मैं आपके प्रश्न का उत्तर देता हूं।"

    @patch("src.language_detector.fasttext")
    def test_get_wait_message_hinglish(self, mock_fasttext):
        """Test wait message generation for Hinglish."""
        mock_model = MagicMock()
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        msg = detector.get_wait_message("hi_roi")
        assert msg == "Thoda wait karo, answer de raha hoon."

    @patch("src.language_detector.fasttext")
    def test_get_wait_message_tamil(self, mock_fasttext):
        """Test wait message generation for Tamil."""
        mock_model = MagicMock()
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        msg = detector.get_wait_message("ta")
        assert msg == "காத்திருக்கவும், உங்கள் கேள்விக்கு பதில் தருகிறேன்."

    @patch("src.language_detector.fasttext")
    def test_get_wait_message_bengali(self, mock_fasttext):
        """Test wait message generation for Bengali."""
        mock_model = MagicMock()
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        msg = detector.get_wait_message("bn")
        assert msg == "অপেক্ষা করুন, আমি আপনার প্রশ্নের উত্তর দিচ্ছি।"

    @patch("src.language_detector.fasttext")
    def test_get_wait_message_telugu(self, mock_fasttext):
        """Test wait message generation for Telugu."""
        mock_model = MagicMock()
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        msg = detector.get_wait_message("te")
        assert "చే" in msg or "prashna" in msg

    @patch("src.language_detector.fasttext")
    def test_get_wait_message_kannada(self, mock_fasttext):
        """Test wait message generation for Kannada."""
        mock_model = MagicMock()
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        msg = detector.get_wait_message("kn")
        assert msg == "ಕಾಯಿರಿ, ನಿಮ್ಮ ಪ್ರಶ್ನೆಗೆ ಉತ್ತರ ಕೊಡುತ್ತಿದ್ದೇನೆ."

    @patch("src.language_detector.fasttext")
    def test_get_wait_message_malayalam(self, mock_fasttext):
        """Test wait message generation for Malayalam."""
        mock_model = MagicMock()
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        msg = detector.get_wait_message("ml")
        assert msg == "കാത്തിരിക്കുക, നിങ്ങളുടെ ചോദ്യത്തിന് ഉത്തരം നൽകാം."

    @patch("src.language_detector.fasttext")
    def test_get_wait_message_marathi(self, mock_fasttext):
        """Test wait message generation for Marathi."""
        mock_model = MagicMock()
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        msg = detector.get_wait_message("mr")
        assert msg == "थांबा, मी तुमच्या प्रश्नाचे उत्तर देतो."

    @patch("src.language_detector.fasttext")
    def test_get_wait_message_gujarati(self, mock_fasttext):
        """Test wait message generation for Gujarati."""
        mock_model = MagicMock()
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        msg = detector.get_wait_message("gu")
        assert msg == "રાહ જુઓ, હું તમારા પ્રશ્નનો જવાબ આપું છું."

    @patch("src.language_detector.fasttext")
    def test_get_wait_message_punjabi(self, mock_fasttext):
        """Test wait message generation for Punjabi."""
        mock_model = MagicMock()
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        msg = detector.get_wait_message("pa")
        assert msg == "ਰੁਕੋ, ਮੈਂ ਤੁਹਾਡੇ ਸਵਾਲ ਦਾ ਜਵਾਬ ਦੇ ਰਿਹਾ ਹਾਂ।"

    @patch("src.language_detector.fasttext")
    def test_get_wait_message_odia(self, mock_fasttext):
        """Test wait message generation for Odia."""
        mock_model = MagicMock()
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        msg = detector.get_wait_message("or")
        assert "ଅପେକ" in msg or "prashna" in msg

    @patch("src.language_detector.fasttext")
    def test_detect_returns_default_for_unknown_language(self, mock_fasttext):
        """Test that unknown languages return default (English)."""
        mock_model = MagicMock()
        mock_model.predict.return_value = ("__label__unknown", 0.50)
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        result = detector.detect("Some random text")
        assert result == "en"

    @patch("src.language_detector.fasttext")
    @patch("src.language_detector.Path")
    def test_model_loads_if_exists(self, mock_path, mock_fasttext):
        """Test that model is loaded if file exists."""
        mock_path.return_value.exists.return_value = True
        
        mock_model = MagicMock()
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        mock_fasttext.load_model.assert_called_once()

    @patch("src.language_detector.fasttext")
    def test_get_supported_languages(self, mock_fasttext):
        """Test getting supported languages list."""
        mock_model = MagicMock()
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        languages = detector.get_supported_languages()
        assert "en" in languages
        assert "hi" in languages
        assert "ta" in languages

    @patch("src.language_detector.fasttext")
    def test_is_supported(self, mock_fasttext):
        """Test is_supported method."""
        mock_model = MagicMock()
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        assert detector.is_supported("en") is True
        assert detector.is_supported("hi") is True
        assert detector.is_supported("unknown") is False


class TestLanguageDetectorIntegration:
    """Integration tests for LanguageDetector with real-like scenarios."""

    @patch("src.language_detector.fasttext")
    def test_detect_college_query_english(self, mock_fasttext):
        """Test detection of a typical college search query in English."""
        mock_model = MagicMock()
        mock_model.predict.return_value = ("__label__en", 0.93)
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        result = detector.detect("Which are the best engineering colleges in India with low fees?")
        assert result == "en"

    @patch("src.language_detector.fasttext")
    def test_detect_college_query_hindi(self, mock_fasttext):
        """Test detection of a typical college search query in Hindi."""
        mock_model = MagicMock()
        mock_model.predict.return_value = ("__label__hi", 0.88)
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        result = detector.detect("भारत में कम फीस वाले इंजीनियरिंग कॉलेज कौन से हैं?")
        assert result == "hi"

    @patch("src.language_detector.fasttext")
    def test_detect_course_query_hinglish(self, mock_fasttext):
        """Test detection of a course query in Hinglish."""
        mock_model = MagicMock()
        mock_model.predict.return_value = ("__label__hi", 0.82)
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        result = detector.detect("MBA karne ke liye konsa college best hai?")
        assert result == "hi_roi"

    @patch("src.language_detector.fasttext")
    def test_full_flow_detect_and_get_message(self, mock_fasttext):
        """Test complete flow: detect language and get wait message."""
        mock_model = MagicMock()
        mock_model.predict.return_value = ("__label__hi", 0.90)
        mock_fasttext.load_model.return_value = mock_model
        
        from src.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        detected = detector.detect("IIT में admission कैसे मिलेगा?")
        wait_msg = detector.get_wait_message(detected)
        
        assert detected in ["hi", "hi_roi"]
        assert "प्रतीक्षा" in wait_msg or "wait" in wait_msg.lower()