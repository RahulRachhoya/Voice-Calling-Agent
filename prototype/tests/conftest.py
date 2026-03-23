"""Pytest Configuration and Shared Fixtures"""

import pytest
import os
from unittest.mock import MagicMock, patch
from pathlib import Path

TEST_DATA_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def mock_fasttext_model():
    """Mock FastText model for testing."""
    mock_model = MagicMock()
    mock_model.predict.return_value = ("__label__en", 0.95)
    return mock_model


@pytest.fixture
def sample_texts():
    """Sample texts in different languages for testing."""
    return {
        "en": [
            "What are the best engineering colleges in India?",
            "I want to know about MBA courses and fees",
            "Tell me about IIT admissions",
        ],
        "hi": [
            "भारत में सबसे अच्छे इंजीनियरिंग कॉलेज कौन से हैं?",
            "मैं MBA कोर्स के बारे में जानना चाहता हूं",
            "IIT प्रवेश के बारे में बताओ",
        ],
        "hi_roi": [
            "Bhai, college ka fees kitna hai?",
            "IIT me admission kaise hoti hai",
            "Engineering college list batao",
        ],
        "bn": [
            "ভারতের সেরা ইঞ্জিনিয়ারিং কলেজ কোনগুলো?",
            "MBA কোর্সের ফি কত?",
        ],
        "ta": [
            "இந்தியாவில் சிறந்த பொறியியல் கல்லூரிகள் எவை?",
            "MBA படிப்பு கட்டுரைகள் பற்றி தெரிவு",
        ],
        "te": [
            "భారతదేశంలో అత్యుత్తమ ఇంజనियరింగ్ కళాశాలలు ఏవి?",
            "MBA కోర్సు ఫీజు ఎంత?",
        ],
        "kn": [
            "ಭಾರತದ ಅತ್ಯುತ್ತಮ ಎಂಜಿನಿಯರಿಂಗ್ ಕಾಲೇಜುಗಳು ಯಾವುವು?",
            "MBA ಕೋರ್ಸ್ ಶುಲ್ಕವೆಷ್ಟು?",
        ],
        "ml": [
            "ഇന്ത്യയിലെ മികച്ച എഞ്ചിനീറിംഗ് കോളേജുകൾ ഏവയാണ്?",
            "MBA കോഴ്സിന്റെ ഫീസ് എത്ര?",
        ],
        "mr": [
            "भारतातील सर्वोत्तम अभियांत्रिकी महाविद्यालये कोणती?",
            "MBA कोर्साची फी किती आहे?",
        ],
        "gu": [
            "ભારતમાં સૌથી વધુ શ્રેષ્ઠ એન્જિનિયરિંગ કોલેજો કયાં છે?",
            "MBA કોર્સની ફી કેટલી?",
        ],
        "pa": [
            "ਭਾਰਤ ਦੀਆਂ ਸਭ ਤੋਂ ਵਧੀਆ ਇੰਜੀਨੀਅਰਿੰਗ ਕਾਲਜ ਕਿਹੜੇ ਹਨ?",
            "MBA ਕੋਰਸ ਦੀ ਫੀਸ ਕਿੰਨੀ ਹੈ?",
        ],
        "or": [
            "ଭାରତର ସର୍ବୋତ୍ਤମ ଇଞ୍ਜିନିୟਰਿଂଗ କଲେଜ କେଉଁଗୁଡ଼ିକ?",
            "MBA କୋର୍ସ ଫି କେତେ?",
        ],
    }


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing."""
    monkeypatch.setenv("VIDEOSDK_AUTH_TOKEN", "test_token")
    monkeypatch.setenv("GOOGLE_API_KEY", "test_google_key")
    monkeypatch.setenv("SARVAM_API_KEY", "test_sarvam_key")
    monkeypatch.setenv("TAVILY_API_KEY", "test_tavily_key")
    monkeypatch.setenv("AGENT_ID", "ARYA_Test")


@pytest.fixture
def temp_model_dir(tmp_path):
    """Create temporary directory for model storage."""
    model_dir = tmp_path / "models"
    model_dir.mkdir()
    return model_dir


@pytest.fixture(autouse=True)
def reset_module_cache():
    """Reset module cache after each test to ensure fresh imports."""
    yield
    import sys
    modules_to_remove = [key for key in sys.modules.keys() if key.startswith("src.")]
    for module in modules_to_remove:
        del sys.modules[module]