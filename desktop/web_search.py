"""No-key web search using DuckDuckGo's HTML results page."""
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36"}


def search_web(query: str, limit: int = 5) -> list[dict[str, str]]:
    query = " ".join((query or "").split()).strip()
    if not query:
        return []
    response = requests.get(
        "https://html.duckduckgo.com/html/?q=" + quote_plus(query),
        headers=HEADERS, timeout=12
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for item in soup.select(".result"):
        link = item.select_one(".result__a")
        snippet = item.select_one(".result__snippet")
        if not link:
            continue
        href = link.get("href", "").strip()
        title = link.get_text(" ", strip=True)
        description = snippet.get_text(" ", strip=True) if snippet else ""
        if href and title:
            results.append({"title": title, "url": href, "snippet": description})
        if len(results) >= max(1, min(limit, 8)):
            break
    return results
