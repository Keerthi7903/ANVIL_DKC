import httpx
from typing import List, Dict, Any

from config import settings


TAVILY_URL = "https://api.tavily.com/search"


class TavilySearchError(Exception):
    pass


async def tavily_search(
    query: str,
    max_results: int = 5
) -> List[Dict[str, Any]]:
    """
    Perform Tavily web search.
    """

    payload = {
        "api_key": settings.TAVILY_API_KEY,
        "query": query,
        "max_results": max_results
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            TAVILY_URL,
            json=payload
        )

    if response.status_code != 200:
        raise TavilySearchError(
            f"Tavily search failed: {response.text}"
        )

    data = response.json()

    return data.get("results", [])