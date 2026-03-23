"""College Search Module - Tavily MCP for Careers360"""

import os
import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

try:
    from tavily import TavilyClient
except ImportError:
    TavilyClient = None

CARERS360_DOMAINS = [
    "careers360.com",
    "www.careers360.com",
]


class CollegeSearch:
    """Tavily-based college search service limited to Careers360."""

    def __init__(self, api_key: Optional[str] = None):
        if TavilyClient is None:
            raise ImportError("tavily-python package not installed. Run: pip install tavily-python")
        
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY is required")
        
        self.client = TavilyClient(api_key=self.api_key)
        logger.info("College search service initialized")

    def search_colleges(
        self,
        query: str,
        max_results: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Search for colleges on Careers360.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of search results with title, url, content
        """
        if not query or not query.strip():
            raise ValueError("Query is required for search")
        
        logger.info(f"Searching colleges: {query[:50]}...")
        
        response = self.client.search(
            query=f"{query} site:careers360.com",
            include_domains=CARERS360_DOMAINS,
            max_results=max_results,
        )
        
        results = response.get("results", [])
        logger.info(f"Found {len(results)} college results")
        
        return results

    def search_courses(
        self,
        query: str,
        max_results: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Search for courses on Careers360.
        
        Args:
            query: Course search query
            max_results: Maximum number of results
            
        Returns:
            List of course results
        """
        if not query or not query.strip():
            raise ValueError("Query is required for search")
        
        logger.info(f"Searching courses: {query[:50]}...")
        
        response = self.client.search(
            query=f"{query} courses site:careers360.com",
            include_domains=CARERS360_DOMAINS,
            max_results=max_results,
        )
        
        results = response.get("results", [])
        logger.info(f"Found {len(results)} course results")
        
        return results

    def search_fees(
        self,
        query: str,
        max_results: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Search for college fee information on Careers360.
        
        Args:
            query: Fee search query
            max_results: Maximum number of results
            
        Returns:
            List of fee results
        """
        if not query or not query.strip():
            raise ValueError("Query is required for search")
        
        logger.info(f"Searching fees: {query[:50]}...")
        
        response = self.client.search(
            query=f"{query} fees structure site:careers360.com",
            include_domains=CARERS360_DOMAINS,
            max_results=max_results,
        )
        
        results = response.get("results", [])
        logger.info(f"Found {len(results)} fee results")
        
        return results

    def search_admissions(
        self,
        query: str,
        max_results: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Search for admission information on Careers360.
        
        Args:
            query: Admission search query
            max_results: Maximum number of results
            
        Returns:
            List of admission results
        """
        if not query or not query.strip():
            raise ValueError("Query is required for search")
        
        logger.info(f"Searching admissions: {query[:50]}...")
        
        response = self.client.search(
            query=f"{query} admission process site:careers360.com",
            include_domains=CARERS360_DOMAINS,
            max_results=max_results,
        )
        
        results = response.get("results", [])
        logger.info(f"Found {len(results)} admission results")
        
        return results

    def format_for_voice(self, results: List[Dict[str, Any]]) -> str:
        """
        Format search results for voice response.
        
        Args:
            results: List of search results
            
        Returns:
            Formatted text for voice output
        """
        if not results:
            return "I couldn't find any relevant information. Please try a different query."
        
        formatted_parts = []
        
        for i, result in enumerate(results[:3], 1):
            title = result.get("title", "")
            content = result.get("content", "")[:200]
            
            formatted_parts.append(f"{i}. {title}. {content}")
        
        return " ".join(formatted_parts)

    def search_general(
        self,
        query: str,
        search_type: str = "colleges",
        max_results: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        General search method that delegates to specific search methods.
        
        Args:
            query: Search query
            search_type: Type of search (colleges, courses, fees, admissions)
            max_results: Maximum number of results
            
        Returns:
            List of search results
        """
        if search_type == "courses":
            return self.search_courses(query, max_results)
        elif search_type == "fees":
            return self.search_fees(query, max_results)
        elif search_type == "admissions":
            return self.search_admissions(query, max_results)
        else:
            return self.search_colleges(query, max_results)


def get_college_search(api_key: Optional[str] = None) -> CollegeSearch:
    """Factory function to get CollegeSearch instance."""
    return CollegeSearch(api_key=api_key)