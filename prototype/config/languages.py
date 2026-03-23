"""Language Configuration - Codes, Voices, and Wait Messages"""

SUPPORTED_LANGUAGES = {
    "en": {
        "name": "English",
        "name_native": "English",
        "code": "en-IN",
        "tts_code": "en-IN",
        "script": "latin",
    },
    "hi": {
        "name": "Hindi",
        "name_native": "हिन्दी",
        "code": "hi-IN",
        "tts_code": "hi-IN",
        "script": "devanagari",
    },
    "hi_roi": {
        "name": "Hinglish",
        "name_native": "Hinglish",
        "code": "hi-IN",
        "tts_code": "hi-IN",
        "script": "latin",
    },
    "bn": {
        "name": "Bengali",
        "name_native": "বাংলা",
        "code": "bn-IN",
        "tts_code": "bn-IN",
        "script": "bengali",
    },
    "ta": {
        "name": "Tamil",
        "name_native": "தமிழ்",
        "code": "ta-IN",
        "tts_code": "ta-IN",
        "script": "tamil",
    },
    "te": {
        "name": "Telugu",
        "name_native": "తెలుగు",
        "code": "te-IN",
        "tts_code": "te-IN",
        "script": "telugu",
    },
    "kn": {
        "name": "Kannada",
        "name_native": "ಕನ್ನಡ",
        "code": "kn-IN",
        "tts_code": "kn-IN",
        "script": "kannada",
    },
    "ml": {
        "name": "Malayalam",
        "name_native": "മലയാളം",
        "code": "ml-IN",
        "tts_code": "ml-IN",
        "script": "malayalam",
    },
    "mr": {
        "name": "Marathi",
        "name_native": "मराठी",
        "code": "mr-IN",
        "tts_code": "mr-IN",
        "script": "devanagari",
    },
    "gu": {
        "name": "Gujarati",
        "name_native": "ગુજરાતી",
        "code": "gu-IN",
        "tts_code": "gu-IN",
        "script": "gujarati",
    },
    "pa": {
        "name": "Punjabi",
        "name_native": "ਪੰਜਾਬੀ",
        "code": "pa-IN",
        "tts_code": "pa-IN",
        "script": "gurmukhi",
    },
    "or": {
        "name": "Odia",
        "name_native": "ଓଡ଼ିଆ",
        "code": "or-IN",
        "tts_code": "or-IN",
        "script": "odia",
    },
}

INDIAN_LANGUAGE_CODES = [
    "en", "hi", "bn", "ta", "te", "kn", "ml", "mr", "gu", "pa", "or"
]

LANGUAGE_TO_SARVAM_CODE = {
    "en": "en-IN",
    "hi": "hi-IN",
    "hi_roi": "hi-IN",
    "bn": "bn-IN",
    "ta": "ta-IN",
    "te": "te-IN",
    "kn": "kn-IN",
    "ml": "ml-IN",
    "mr": "mr-IN",
    "gu": "gu-IN",
    "pa": "pa-IN",
    "or": "or-IN",
}

LANGUAGE_TO_VOICE = {
    "en": {"male": "abhilash", "female": "anushka", "default": "anushka"},
    "hi": {"male": "abhilash", "female": "anushka", "default": "anushka"},
    "hi_roi": {"male": "abhilash", "female": "anushka", "default": "anushka"},
    "bn": {"male": "karun", "female": "manisha", "default": "manisha"},
    "ta": {"male": "arul", "female": "divya", "default": "divya"},
    "te": {"male": "charan", "female": "samantha", "default": "samantha"},
    "kn": {"male": "nandeesh", "female": "spandana", "default": "spandana"},
    "ml": {"male": "midhun", "female": "nanditha", "default": "nanditha"},
    "mr": {"male": "swapnil", "female": "prajakta", "default": "prajakta"},
    "gu": {"male": "dhruv", "female": "jenisha", "default": "jenisha"},
    "pa": {"male": "gagan", "female": "jasleen", "default": "jasleen"},
    "or": {"male": "prashant", "female": "mousumi", "default": "mousumi"},
}

WAIT_MESSAGES = {
    "en": "Wait, I will give you the response to your query.",
    "hi": "प्रतीक्षा करें, मैं आपके प्रश्न का उत्तर देता हूं।",
    "hi_roi": "Thoda wait karo, answer de raha hoon.",
    "bn": "অপেক্ষা করুন, আমি আপনার প্রশ্নের উত্তর দিচ্ছি।",
    "ta": "காத்திருக்கவும், உங்கள் கேள்விக்கு பதில் தருகிறேன்.",
    "te": " వేait చేసుకోండి, మీ ప్రశ्नకు సమాధానం ఇస్తాను.",
    "kn": "ಕಾಯಿರಿ, ನಿಮ್ಮ ಪ್ರಶ್ನೆಗೆ ಉತ್ತರ ಕೊಡುತ್ತಿದ್ದೇನೆ.",
    "ml": "കാത്തിരിക്കുക, നിങ്ങളുടെ ചോദ്യത്തിന് ഉത്തരം നൽകാം.",
    "mr": "थांबा, मी तुमच्या प्रश्नाचे उत्तर देतो.",
    "gu": "રાહ જુઓ, હું તમારા પ્રશ્નનો જવાબ આપું છું.",
    "pa": "ਰੁਕੋ, ਮੈਂ ਤੁਹਾਡੇ ਸਵਾਲ ਦਾ ਜਵਾਬ ਦੇ ਰਿਹਾ ਹਾਂ।",
    "or": "ଅପେକ୍਷ା କରୁଥିਬେ, ମୁଁ ଆପଣଙ୍କ ପ୍ਰଶ୍ନର ଉତ୍ਤਰ ଦେଉଛି।",
}

FASTTEXT_LANGUAGE_MAP = {
    "__label__en": "en",
    "__label__hi": "hi",
    "__label__hi_roi": "hi_roi",
    "__label__bn": "bn",
    "__label__ta": "ta",
    "__label__te": "te",
    "__label__kn": "kn",
    "__label__ml": "ml",
    "__label__mr": "mr",
    "__label__gu": "gu",
    "__label__pa": "pa",
    "__label__or": "or",
    "__label__mlt": "ml",
    "__label__ne": "hi",
    "__label__sa": "hi",
}