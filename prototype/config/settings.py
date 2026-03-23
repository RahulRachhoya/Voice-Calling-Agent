"""ARYA Settings - All configuration in one place"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    """ARYA Agent Configuration Settings"""

    videosdk_auth_token: str = os.getenv("VIDEOSDK_AUTH_TOKEN", "")
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    sarvam_api_key: str = os.getenv("SARVAM_API_KEY", "")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")

    # OpenRouter LLM Configuration (free LLM)
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "meta-llama/llama-3.3-70b-instruct:free")
    llm_base_url: str = os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1")

    agent_id: str = os.getenv("AGENT_ID", "ARYA_Careers360")
    host: str = os.getenv("HOST", "localhost")
    port: int = int(os.getenv("PORT", "8081"))
    max_processes: int = int(os.getenv("MAX_PROCESSES", "10"))

    enable_sarvam_tts: bool = os.getenv("ENABLE_SARVAM_TTS", "true").lower() == "true"
    enable_college_search: bool = os.getenv("ENABLE_COLLEGE_SEARCH", "true").lower() == "true"
    enable_language_detection: bool = os.getenv("ENABLE_LANGUAGE_DETECTION", "true").lower() == "true"

    fasttext_model_path: str = os.getenv("FASTTEXT_MODEL_PATH", "models/lid.176.bin")
    transcripts_dir: str = os.getenv("TRANSCRIPTS_DIR", "transcripts")
    audio_dir: str = os.getenv("AUDIO_DIR", "audio")

    def is_configured(self) -> bool:
        """Check if all required API keys are set."""
        return bool(
            self.videosdk_auth_token
            and self.openrouter_api_key
            and self.sarvam_api_key
            and self.tavily_api_key
        )

    def get_missing_keys(self) -> list[str]:
        """Get list of missing required API keys."""
        missing = []
        if not self.videosdk_auth_token:
            missing.append("VIDEOSDK_AUTH_TOKEN")
        if not self.openrouter_api_key:
            missing.append("OPENROUTER_API_KEY")
        if not self.sarvam_api_key:
            missing.append("SARVAM_API_KEY")
        if not self.tavily_api_key:
            missing.append("TAVILY_API_KEY")
        return missing


settings = Settings()