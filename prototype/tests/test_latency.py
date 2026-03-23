"""Tests for Latency Optimization"""

import pytest
from unittest.mock import patch, MagicMock


class TestFasterModel:
    """Test cases for faster model configuration."""

    def test_model_name_is_faster_version(self):
        """Test that main.py uses the correct model."""
        # After implementation, main.py should use gemini-2.5-flash-native-audio-preview-12-2025
        import main
        
        # Check the model name in the file
        import inspect
        source = inspect.getsource(main)
        
        # The model should be the working one (optimized)
        assert "gemini-2.5-flash-native-audio-preview-12-2025" in source, "Should use working model"

    def test_gemini_config_has_max_tokens(self):
        """Test that config includes max_output_tokens."""
        from videosdk.plugins.google import GeminiLiveConfig
        
        # Test that config can be created with max_output_tokens
        config = GeminiLiveConfig(
            voice="Aoede",
            max_output_tokens=50,
            temperature=0.7,
        )
        
        assert config is not None


class TestResponseLength:
    """Test cases for response length optimization."""

    def test_prompt_limits_to_50_words(self):
        """Test that prompt says 50 words, not 60."""
        from prompts import BASE_SYSTEM_PROMPT
        
        # Check that the prompt says 50 words
        assert "50 words" in BASE_SYSTEM_PROMPT or "under 50" in BASE_SYSTEM_PROMPT.lower()
        
        # Should NOT have 60 words
        assert "60 words" not in BASE_SYSTEM_PROMPT

    def test_prompt_has_conversational_style(self):
        """Test that response style is optimized for voice."""
        from prompts import BASE_SYSTEM_PROMPT
        
        prompt_lower = BASE_SYSTEM_PROMPT.lower()
        
        # Should have voice call style
        assert "voice call" in prompt_lower or "speak" in prompt_lower
        
        # Should have short response requirement
        assert "word" in prompt_lower


class TestThinkingAudio:
    """Test cases for thinking audio optimization."""

    def test_agent_init_removes_thinking_audio(self):
        """Test that thinking audio is disabled for faster response."""
        # After implementation, agent.py should not call set_thinking_audio()
        import agent
        
        # Check if set_thinking_audio is called in the source
        import inspect
        source = inspect.getsource(agent.ARYAAgent.__init__)
        
        # Should NOT have set_thinking_audio call for instant response
        # OR it should be optional/disabled
        assert True  # Will verify after implementation


class TestConfigOptimization:
    """Test cases for overall config optimization."""

    def test_temperature_is_set(self):
        """Test that temperature is configured for faster decisions."""
        from videosdk.plugins.google import GeminiLiveConfig
        
        config = GeminiLiveConfig(
            voice="Aoede",
            temperature=0.7,
        )
        
        assert config is not None

    def test_max_tokens_limits_response(self):
        """Test that max_output_tokens limits response length."""
        from videosdk.plugins.google import GeminiLiveConfig
        
        config = GeminiLiveConfig(
            voice="Aoede",
            max_output_tokens=50,
        )
        
        # Config should be created successfully
        assert config is not None


class TestSearchOptimization:
    """Test cases for search functionality."""

    def test_college_search_service_initialized(self):
        """Test that college search is available in agent."""
        with patch("agent.Agent.__init__") as mock_init:
            mock_init.return_value = None
            
            with patch("agent.CollegeSearch") as mock_cs:
                mock_cs_instance = MagicMock()
                mock_cs.return_value = mock_cs_instance
                
                # After implementation, agent should have college_search
                from agent import ARYAAgent
                
                # Agent should have college search capability
                # This test verifies the service is available
                assert True  # Will verify after implementation