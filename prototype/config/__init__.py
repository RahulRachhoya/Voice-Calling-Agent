"""ARYA Configuration Package"""

from config.languages import (
    SUPPORTED_LANGUAGES,
    LANGUAGE_TO_SARVAM_CODE,
    LANGUAGE_TO_VOICE,
    WAIT_MESSAGES,
    INDIAN_LANGUAGE_CODES,
)
from config.settings import Settings

__all__ = [
    "Settings",
    "SUPPORTED_LANGUAGES",
    "LANGUAGE_TO_SARVAM_CODE",
    "LANGUAGE_TO_VOICE",
    "WAIT_MESSAGES",
    "INDIAN_LANGUAGE_CODES",
]