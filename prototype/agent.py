"""
ARYA Agent - Career Counselor Voice Agent for Careers360
Handles inbound and outbound voice calls using Gemini Live API
"""

import os
import json
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from videosdk.agents import Agent, function_tool
from prompts import BASE_SYSTEM_PROMPT

from config.settings import settings
from config.languages import WAIT_MESSAGES

logger = logging.getLogger(__name__)

try:
    from src.language_detector import LanguageDetector
except ImportError:
    LanguageDetector = None

try:
    from src.college_search import CollegeSearch
except ImportError:
    CollegeSearch = None


class ARYAAgent(Agent):
    """
    ARYA - AI Career Counselor Agent
    
    Provides voice-based career counseling for Indian students.
    Uses Gemini Live API for natural conversation handling.
    Includes:
    - Language detection (12 Indian languages)
    - Wait messages in user's language
    - College search via Tavily (Careers360 only)
    - Sarvam TTS for non-English responses
    """

    def __init__(self):
        super().__init__(instructions=BASE_SYSTEM_PROMPT)
        # Disabled thinking audio for instant response - faster latency
        # self.set_thinking_audio()  # Commented out for speed
        self.hold_music_path = Path("audio/hold_music.mp3")
        self.transcript_file = None
        self.call_start_time = None
        self.call_id = None
        self.detected_language = "en"
        
        self.transcripts_dir = Path("transcripts")
        self.transcripts_dir.mkdir(exist_ok=True)
        
        self._init_services()

    def _init_services(self):
        """Initialize language detector and college search services."""
        if settings.enable_language_detection and LanguageDetector:
            try:
                self.language_detector = LanguageDetector()
                print("[OK] Language detector initialized")
            except Exception as e:
                print(f"[WARN] Language detector failed: {e}")
                self.language_detector = None
        else:
            self.language_detector = None
            
        if settings.enable_college_search and CollegeSearch:
            try:
                self.college_search = CollegeSearch(api_key=settings.tavily_api_key)
                print("[OK] College search initialized")
            except Exception as e:
                print(f"[WARN] College search failed: {e}")
                self.college_search = None
        else:
            self.college_search = None

    @function_tool
    def search_colleges(self, query: str) -> str:
        """
        Search for college information from Careers360 website.
        
        Use this when user asks about colleges, courses, admissions, fees,
        rankings, scholarships, or entrance exams.
        
        Args:
            query: The search query about colleges/courses/admissions
            
        Returns:
            Formatted search results from Tavily (Careers360 only)
        """
        logger.info(f"[TOOL] search_colleges called with query: {query}")
        
        if not self.college_search:
            logger.warning("[TOOL] College search service not available")
            return "College search service is not available. Please try again later."
        
        try:
            # Add careers360.com to search query for targeted results
            search_query = f"{query} site:careers360.com"
            logger.info(f"[TOOL] Executing search: {search_query}")
            
            results = self.college_search.search(search_query)
            
            logger.info(f"[TOOL] Search returned results: {results[:200] if results else 'No results'}")
            
            if not results:
                logger.warning("[TOOL] No results found for query")
                return "I couldn't find specific information for your query. Please try asking about a different college or course."
            
            # Format results for voice response (keep under 50 words)
            return results
            
        except Exception as e:
            logger.error(f"[TOOL] College search failed: {e}")
            logger.error(f"[TOOL] Traceback: {traceback.format_exc()}")
            return "I encountered an error while searching. Let me try a different approach."

    async def on_enter(self) -> None:
        """
        Called when the agent enters the session.
        This is triggered when a call is connected.
        """
        self.call_start_time = datetime.utcnow()
        self.call_id = f"call_{self.call_start_time.strftime('%Y%m%d_%H%M%S')}_{id(self)}"
        
        self.transcript_file = self.transcripts_dir / f"{self.call_id}.jsonl"
        
        print(f"\n[CALL CONNECTED] {self.call_id}")
        print(f"[TRANSCRIPT] {self.transcript_file}\n")
        
        self._log_event("system", "Call connected", {
            "timestamp": self.call_start_time.isoformat(),
            "call_id": self.call_id
        })
        
        try:
            greeting = (
                "Hello! I'm ARYA, your career counselor from Careers Three-Sixty. "
                "I'm here to help you with college admissions, courses, and career guidance. "
                "How can I assist you today?"
            )
            
            await self.session.say(greeting)
            self._log_event("arya", greeting)
            print(f"[AGENT SPEAKING] Greeting delivered\n")
            
        except Exception as e:
            error_msg = f"Error delivering greeting: {str(e)}"
            print(f"[ERROR] {error_msg}")
            self._log_event("system", error_msg)
            traceback.print_exc()

    async def on_exit(self) -> None:
        """
        Called when the agent exits the session.
        This is triggered when the call ends.
        """
        try:
            goodbye_msg = (
                "Thank you for talking with ARYA. "
                "Good luck with your career journey. Goodbye!"
            )
            
            await self.session.say(goodbye_msg)
            self._log_event("arya", goodbye_msg)
            
            if self.call_start_time:
                duration = (datetime.utcnow() - self.call_start_time).total_seconds()
                self._log_event("system", "Call ended", {
                    "duration_seconds": duration,
                    "call_id": self.call_id
                })
                print(f"\n[CALL ENDED] Duration: {duration:.1f}s")
                print(f"[TRANSCRIPT SAVED] {self.transcript_file}\n")
            
        except Exception as e:
            print(f"[ERROR] Error in on_exit: {str(e)}")
            traceback.print_exc()

    def _log_event(self, role: str, message: str, metadata: dict | None = None):
        """
        Log conversation event to transcript file.
        
        Args:
            role: Who spoke (arya, user, system)
            message: The message content
            metadata: Additional data to log
        """
        try:
            if self.transcript_file:
                entry = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "role": role,
                    "message": message
                }
                if metadata:
                    entry.update(metadata)
                
                with open(self.transcript_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"[ERROR] Failed to log event: {e}")

    def _detect_language(self, text: str) -> str:
        """
        Detect language from user text.
        
        Args:
            text: User's input text
            
        Returns:
            Language code (e.g., 'en', 'hi', 'ta')
        """
        if self.language_detector:
            try:
                lang = self.language_detector.detect(text)
                print(f"[LANG] Detected: {lang}")
                return lang
            except Exception as e:
                print(f"[WARN] Language detection failed: {e}")
        
        return "en"

    def _get_wait_message(self, lang_code: str) -> str:
        """
        Get wait message in the specified language.
        
        Args:
            lang_code: Language code
            
        Returns:
            Wait message in the specified language
        """
        if self.language_detector:
            try:
                return self.language_detector.get_wait_message(lang_code)
            except Exception:
                pass
        
        return WAIT_MESSAGES.get(lang_code, WAIT_MESSAGES["en"])

    def _is_college_query(self, text: str) -> bool:
        """
        Check if the query is related to colleges/courses/admissions.
        
        Args:
            text: User's input text
            
        Returns:
            True if it's a college-related query
        """
        if not text:
            return False
        
        text_lower = text.lower()
        
        college_keywords = [
            "college", "colleges", "university", "universities",
            "admission", "admissions", "apply", "application",
            "fees", "fee", "cost", "expense",
            "course", "courses", "degree", "diploma",
            "B.Tech", "BBA", "MBA", "BCA", "BE", "ME",
            "engineering", "medical", "science", "commerce",
            "rank", "ranking", "placement", "placements",
            "hostel", "campus", "facility",
            "entrance", "exam", "JEE", "NEET", "CAT", "CLAT",
            "scholarship", "loan",
        ]
        
        return any(keyword in text_lower for keyword in college_keywords)

    def _search_college_info(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for college information on Careers360.
        
        Args:
            query: Search query
            
        Returns:
            List of search results
        """
        if not self.college_search:
            print("[WARN] College search not initialized")
            return []
        
        try:
            print(f"[SEARCH] Query: {query}")
            results = self.college_search.search_colleges(query, max_results=5)
            print(f"[SEARCH] Found {len(results)} results")
            return results
        except Exception as e:
            print(f"[ERROR] College search failed: {e}")
            return []

    async def speak_wait_message(self, language: str = "en") -> None:
        """
        Speak wait message in the user's language (replaces hold music).
        
        Args:
            language: Language code for the wait message
        """
        wait_msg = self._get_wait_message(language)
        print(f"[WAIT] {language}: {wait_msg}")
        
        try:
            await self.session.say(wait_msg)
            self._log_event("arya", wait_msg)
        except Exception as e:
            print(f"[ERROR] Failed to speak wait message: {e}")

    async def speak_college_results(self, results: List[Dict[str, Any]]) -> None:
        """
        Speak college search results to the user.
        
        Args:
            results: List of college search results
        """
        if not results:
            msg = "I couldn't find any relevant college information. Please try a different query."
            await self.session.say(msg)
            self._log_event("arya", msg)
            return
        
        if self.college_search:
            formatted = self.college_search.format_for_voice(results)
            await self.session.say(formatted)
            self._log_event("arya", formatted[:500])
        else:
            for result in results[:3]:
                await self.session.say(f"{result.get('title', 'College')}. {result.get('content', '')[:200]}")
                self._log_event("arya", f"Shared: {result.get('title', '')}")

    async def play_hold_music(self):
        """Play hold music during long operations."""
        try:
            if self.hold_music_path.exists():
                self._log_event("system", "Hold music started")
                await self.play_background_audio(
                    file=str(self.hold_music_path),
                    looping=True,
                    override_thinking=True,
                )
                print("[AUDIO] Hold music started")
            else:
                print("[WARN] Hold music file not found, using wait message instead")
                await self.speak_wait_message(self.detected_language)
        except Exception as e:
            print(f"[ERROR] Failed to play hold music: {e}")
            await self.speak_wait_message(self.detected_language)

    async def stop_hold_music(self):
        """Stop hold music."""
        try:
            self._log_event("system", "Hold music stopped")
            await self.stop_background_audio()
            print("[AUDIO] Hold music stopped")
        except Exception as e:
            print(f"[ERROR] Failed to stop hold music: {e}")

    async def on_error(self, error: Exception) -> None:
        """Handle errors during the conversation."""
        logger.error(f"[AGENT ERROR] {error}")
        logger.error(f"[AGENT ERROR] Traceback: {traceback.format_exc()}")
        
        # Try to speak error message to user
        try:
            await self.session.say("I'm having trouble processing your request. Please try again.")
        except Exception as speak_error:
            logger.error(f"[AGENT ERROR] Failed to speak error: {speak_error}")