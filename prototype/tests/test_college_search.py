"""Tests for College Search Module"""

import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path


class TestCollegeSearch:
    """Test cases for CollegeSearch class."""

    @patch("src.college_search.TavilyClient")
    def test_initialization_with_api_key(self, mock_tavily):
        """Test that CollegeSearch initializes with API key."""
        mock_client = MagicMock()
        mock_tavily.return_value = mock_client
        
        from src.college_search import CollegeSearch
        search = CollegeSearch(api_key="test_key")
        
        assert search.api_key == "test_key"

    @patch("src.college_search.TavilyClient")
    def test_initialization_with_env_var(self, mock_tavily, monkeypatch):
        """Test that CollegeSearch uses env var if no key provided."""
        monkeypatch.setenv("TAVILY_API_KEY", "env_key")
        mock_client = MagicMock()
        mock_tavily.return_value = mock_client
        
        from src.college_search import CollegeSearch
        search = CollegeSearch()
        
        assert search.api_key == "env_key"

    @patch("src.college_search.TavilyClient")
    def test_search_colleges_basic(self, mock_tavily):
        """Test basic college search."""
        mock_client = MagicMock()
        mock_tavily.return_value = mock_client
        
        mock_response = {
            "results": [
                {
                    "title": "IIT Bombay - Indian Institute of Technology",
                    "url": "https://www.careers360.com/colleges/iit-bombay",
                    "content": "IIT Bombay is one of the top engineering colleges in India...",
                },
                {
                    "title": "IIT Delhi - Indian Institute of Technology",
                    "url": "https://www.careers360.com/colleges/iit-delhi",
                    "content": "IIT Delhi is a premier engineering institution...",
                },
            ]
        }
        mock_client.search.return_value = mock_response
        
        from src.college_search import CollegeSearch
        search = CollegeSearch(api_key="test_key")
        
        results = search.search_colleges("best engineering colleges India")
        
        assert len(results) == 2
        assert "IIT Bombay" in results[0]["title"]
        mock_client.search.assert_called_once()

    @patch("src.college_search.TavilyClient")
    def test_search_colleges_with_domain_filter(self, mock_tavily):
        """Test that search is limited to Careers360 domain."""
        mock_client = MagicMock()
        mock_tavily.return_value = mock_client
        
        mock_response = {"results": []}
        mock_client.search.return_value = mock_response
        
        from src.college_search import CollegeSearch
        search = CollegeSearch(api_key="test_key")
        
        search.search_colleges("IIT colleges")
        
        call_args = mock_client.search.call_args
        kwargs = call_args.kwargs if hasattr(call_args, 'kwargs') else call_args[1]
        
        assert "careers360.com" in str(kwargs.get("include_domains", []))

    @patch("src.college_search.TavilyClient")
    def test_search_courses(self, mock_tavily):
        """Test course search."""
        mock_client = MagicMock()
        mock_tavily.return_value = mock_client
        
        mock_response = {
            "results": [
                {
                    "title": "B.Tech in Computer Science",
                    "url": "https://www.careers360.com/courses/btech-cs",
                    "content": "B.Tech CS is a 4-year undergraduate program...",
                },
            ]
        }
        mock_client.search.return_value = mock_response
        
        from src.college_search import CollegeSearch
        search = CollegeSearch(api_key="test_key")
        
        results = search.search_courses("B.Tech Computer Science")
        
        assert len(results) == 1
        assert "B.Tech" in results[0]["title"]

    @patch("src.college_search.TavilyClient")
    def test_search_fees(self, mock_tavily):
        """Test college fees search."""
        mock_client = MagicMock()
        mock_tavily.return_value = mock_client
        
        mock_response = {
            "results": [
                {
                    "title": "IIT Bombay Fees",
                    "url": "https://www.careers360.com/colleges/iit-bombay/fees",
                    "content": "Total fees for B.Tech is approximately Rs 8-10 lakhs...",
                },
            ]
        }
        mock_client.search.return_value = mock_response
        
        from src.college_search import CollegeSearch
        search = CollegeSearch(api_key="test_key")
        
        results = search.search_fees("IIT Bombay B.Tech fees")
        
        assert len(results) == 1
        assert "fees" in results[0]["title"].lower() or "fees" in results[0]["content"].lower()

    @patch("src.college_search.TavilyClient")
    def test_search_admissions(self, mock_tavily):
        """Test admission information search."""
        mock_client = MagicMock()
        mock_tavily.return_value = mock_client
        
        mock_response = {
            "results": [
                {
                    "title": "IIT JEE Admission Process",
                    "url": "https://www.careers360.com/exams/jee-main",
                    "content": "JEE Main is the entrance exam for IITs...",
                },
            ]
        }
        mock_client.search.return_value = mock_response
        
        from src.college_search import CollegeSearch
        search = CollegeSearch(api_key="test_key")
        
        results = search.search_admissions("IIT admission process")
        
        assert len(results) == 1
        assert "admission" in results[0]["title"].lower() or "JEE" in results[0]["content"]

    @patch("src.college_search.TavilyClient")
    def test_format_results_for_voice(self, mock_tavily):
        """Test formatting results for voice response."""
        mock_client = MagicMock()
        mock_tavily.return_value = mock_client
        
        mock_response = {
            "results": [
                {
                    "title": "IIT Bombay",
                    "url": "https://careers360.com/college/iit-bombay",
                    "content": "Top ranked engineering college with excellent placements.",
                },
                {
                    "title": "IIT Delhi",
                    "url": "https://careers360.com/college/iit-delhi",
                    "content": "Premier institute for technical education.",
                },
            ]
        }
        mock_client.search.return_value = mock_response
        
        from src.college_search import CollegeSearch
        search = CollegeSearch(api_key="test_key")
        
        results = search.search_colleges("IIT colleges")
        formatted = search.format_for_voice(results)
        
        assert "IIT Bombay" in formatted
        assert "IIT Delhi" in formatted

    @patch("src.college_search.TavilyClient")
    def test_search_with_max_results(self, mock_tavily):
        """Test search with custom max results."""
        mock_client = MagicMock()
        mock_tavily.return_value = mock_client
        
        mock_response = {"results": []}
        mock_client.search.return_value = mock_response
        
        from src.college_search import CollegeSearch
        search = CollegeSearch(api_key="test_key")
        
        search.search_colleges("test query", max_results=10)
        
        call_args = mock_client.search.call_args
        kwargs = call_args.kwargs if hasattr(call_args, 'kwargs') else call_args[1]
        
        assert kwargs.get("max_results") == 10

    @patch("src.college_search.TavilyClient")
    def test_error_handling_empty_query(self, mock_tavily):
        """Test error handling for empty query."""
        from src.college_search import CollegeSearch
        search = CollegeSearch(api_key="test_key")
        
        with pytest.raises(ValueError, match="Query is required"):
            search.search_colleges("")

    @patch("src.college_search.TavilyClient")
    def test_error_handling_api_error(self, mock_tavily):
        """Test error handling when API returns error."""
        mock_client = MagicMock()
        mock_tavily.return_value = mock_client
        
        mock_client.search.side_effect = Exception("API Error")
        
        from src.college_search import CollegeSearch
        search = CollegeSearch(api_key="test_key")
        
        with pytest.raises(Exception, match="API Error"):
            search.search_colleges("test query")


class TestCollegeSearchIntegration:
    """Integration tests for CollegeSearch."""

    @patch("src.college_search.TavilyClient")
    def test_full_college_search_flow(self, mock_tavily):
        """Test complete college search flow."""
        mock_client = MagicMock()
        mock_tavily.return_value = mock_client
        
        mock_response = {
            "results": [
                {
                    "title": "IIT Bombay - Best Engineering College",
                    "url": "https://www.careers360.com/colleges/iit-bombay",
                    "content": "IIT Bombay ranks #1 among engineering colleges in India...",
                },
                {
                    "title": "BITS Pilani - Top Private Engineering",
                    "url": "https://www.careers360.com/colleges/bits-pilani",
                    "content": "BITS Pilani is a leading private engineering institute...",
                },
            ]
        }
        mock_client.search.return_value = mock_response
        
        from src.college_search import CollegeSearch
        search = CollegeSearch(api_key="test_key")
        
        query = "best engineering colleges India"
        results = search.search_colleges(query)
        formatted = search.format_for_voice(results)
        
        assert len(results) == 2
        assert "IIT Bombay" in formatted

    @patch("src.college_search.TavilyClient")
    def test_careers360_domain_exclusivity(self, mock_tavily):
        """Test that all searches are limited to Careers360 domain."""
        mock_client = MagicMock()
        mock_tavily.return_value = mock_client
        
        test_queries = [
            ("engineering colleges", "colleges"),
            ("MBA courses", "courses"),
            ("college fees", "fees"),
            ("admission process", "admissions"),
        ]
        
        from src.college_search import CollegeSearch
        search = CollegeSearch(api_key="test_key")
        
        for query, _ in test_queries:
            mock_client.search.return_value = {"results": []}
            search.search_colleges(query)
            
            call_args = mock_client.search.call_args
            kwargs = call_args.kwargs if hasattr(call_args, 'kwargs') else call_args[1]
            domains = kwargs.get("include_domains", [])
            
            assert any("careers360.com" in d for d in domains)