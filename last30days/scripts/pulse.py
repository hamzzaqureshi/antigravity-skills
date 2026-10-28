#!/usr/bin/env python3
"""CrowdPulse: Zero-Dependency Real-Time Intelligence Fast-Lane.

Queries public keyless social and market APIs concurrently using Python standard library:
  - Reddit (Public search JSON)
  - Hacker News (Algolia Search API)
  - GitHub (Public Repository Search)
  - Polymarket (Public Gamma Events API)

Usable via CLI or as an importable Python module:
    from pulse import fetch_pulse
    data = fetch_pulse("react 19")
"""

import argparse
import concurrent.futures
import json
import sys
import time
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

USER_AGENT = "Mozilla/5.0 (compatible; Antigravity-CrowdPulse/1.0; +https://antigravity.dev)"


def _fetch_url(url: str, timeout: float = 3.5, headers: Optional[Dict[str, str]] = None) -> Any:
    req_headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, headers=req_headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        if resp.status == 200:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    return None


def fetch_reddit(query: str, limit: int = 5, timeout: float = 3.5) -> List[Dict[str, Any]]:
    """Fetch top Reddit posts from the last month."""
    encoded = urllib.parse.quote(query)
    url = f"https://www.reddit.com/search.json?q={encoded}&sort=top&t=month&limit={limit}"
    data = _fetch_url(url, timeout=timeout)
    items = []
    if data and "data" in data and "children" in data["data"]:
        for child in data["data"]["children"]:
            post = child.get("data", {})
            items.append({
                "source": "Reddit",
                "title": post.get("title", ""),
                "community": f"r/{post.get('subreddit', '')}",
                "score": post.get("score", 0),
                "comments": post.get("num_comments", 0),
                "url": f"https://reddit.com{post.get('permalink', '')}",
                "created_utc": post.get("created_utc", 0),
            })
    return items


def fetch_hackernews(query: str, limit: int = 5, timeout: float = 3.5) -> List[Dict[str, Any]]:
    """Fetch top Hacker News stories matching query."""
    encoded = urllib.parse.quote(query)
    url = f"https://hn.algolia.com/api/v1/search?query={encoded}&tags=story&hitsPerPage={limit}"
    data = _fetch_url(url, timeout=timeout)
    items = []
    if data and "hits" in data:
        for hit in data["hits"]:
            object_id = hit.get("objectID", "")
            items.append({
                "source": "HackerNews",
                "title": hit.get("title", ""),
                "community": "news.ycombinator.com",
                "score": hit.get("points", 0) or 0,
                "comments": hit.get("num_comments", 0) or 0,
                "url": hit.get("url") or f"https://news.ycombinator.com/item?id={object_id}",
                "discussion_url": f"https://news.ycombinator.com/item?id={object_id}",
                "created_at": hit.get("created_at", ""),
            })
    return items


def fetch_github(query: str, limit: int = 5, timeout: float = 3.5) -> List[Dict[str, Any]]:
    """Fetch top GitHub repositories matching query."""
    encoded = urllib.parse.quote(query)
    url = f"https://api.github.com/search/repositories?q={encoded}&sort=stars&order=desc&per_page={limit}"
    data = _fetch_url(url, timeout=timeout)
    items = []
    if data and "items" in data:
        for repo in data["items"]:
            items.append({
                "source": "GitHub",
                "title": repo.get("full_name", ""),
                "description": repo.get("description", "") or "",
                "score": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
                "url": repo.get("html_url", ""),
                "language": repo.get("language", ""),
                "updated_at": repo.get("updated_at", ""),
            })
    return items


def fetch_polymarket(query: str, limit: int = 5, timeout: float = 3.5) -> List[Dict[str, Any]]:
    """Fetch active Polymarket prediction markets matching query."""
    encoded = urllib.parse.quote(query)
    url = f"https://gamma-api.polymarket.com/events?closed=false&limit={limit}&q={encoded}"
    data = _fetch_url(url, timeout=timeout)
    items = []
    if data and isinstance(data, list):
        for event in data:
            slug = event.get("slug", "")
            markets = event.get("markets", [])
            odds_str = "N/A"
            if markets and isinstance(markets, list):
                prices = markets[0].get("outcomePrices")
                if prices:
                    try:
                        p_list = json.loads(prices) if isinstance(prices, str) else prices
                        if p_list and len(p_list) > 0:
                            yes_val = float(p_list[0]) * 100
                            odds_str = f"{yes_val:.1f}% Yes"
                    except Exception:
                        pass
            items.append({
                "source": "Polymarket",
                "title": event.get("title", ""),
                "odds": odds_str,
                "volume": event.get("volume", 0) or 0,
                "url": f"https://polymarket.com/event/{slug}" if slug else "",
            })
    return items


def mock_pulse(query: str) -> Dict[str, Any]:
    """Instant offline mock for tests and isolated sandboxes."""
    return {
        "query": query,
        "elapsed_seconds": 0.002,
        "mode": "mock",
        "reddit": [
            {
                "source": "Reddit",
                "title": f"The community consensus on {query}",
                "community": "r/technology",
                "score": 1420,
                "comments": 284,
                "url": f"https://reddit.com/r/technology/comments/mock_{query}",
                "created_utc": time.time() - 86400,
            }
        ],
        "hackernews": [
            {
                "source": "HackerNews",
                "title": f"Show HN: Fast implementation of {query}",
                "community": "news.ycombinator.com",
                "score": 450,
                "comments": 190,
                "url": f"https://news.ycombinator.com/item?id=mock_{query}",
                "discussion_url": f"https://news.ycombinator.com/item?id=mock_{query}",
                "created_at": "2026-10-28T12:00:00Z",
            }
        ],
        "github": [
            {
                "source": "GitHub",
                "title": f"antigravity/{query}-core",
                "description": f"High performance {query} runtime engine",
                "score": 8920,
                "forks": 612,
                "url": f"https://github.com/antigravity/{query}-core",
                "language": "Python",
                "updated_at": "2026-10-28T15:00:00Z",
            }
        ],
        "polymarket": [
            {
                "source": "Polymarket",
                "title": f"Will {query} release production milestone in 2026?",
                "odds": "84.5% Yes",
                "volume": 245000,
                "url": f"https://polymarket.com/event/mock-{query}",
            }
        ],
    }


def fetch_pulse(query: str, limit: int = 5, timeout: float = 3.5, mock: bool = False) -> Dict[str, Any]:
    """Concurrently query Reddit, Hacker News, GitHub, and Polymarket."""
    if mock:
        return mock_pulse(query)

    t0 = time.perf_counter()
    results: Dict[str, Any] = {
        "query": query,
        "reddit": [],
        "hackernews": [],
        "github": [],
        "polymarket": [],
    }

    def safe_run(fn, name):
        try:
            return fn(query, limit=limit, timeout=timeout)
        except Exception:
            return []

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        f_reddit = executor.submit(safe_run, fetch_reddit, "reddit")
        f_hn = executor.submit(safe_run, fetch_hackernews, "hackernews")
        f_gh = executor.submit(safe_run, fetch_github, "github")
        f_poly = executor.submit(safe_run, fetch_polymarket, "polymarket")

        results["reddit"] = f_reddit.result()
        results["hackernews"] = f_hn.result()
        results["github"] = f_gh.result()
        results["polymarket"] = f_poly.result()

    results["elapsed_seconds"] = round(time.perf_counter() - t0, 3)
    results["mode"] = "live"
    return results


def format_pulse_markdown(pulse: Dict[str, Any]) -> str:
    """Format pulse data into a dense, readable Markdown brief."""
    lines = [
        f"### CrowdPulse: {pulse.get('query', '')} ({pulse.get('elapsed_seconds', 0)}s)",
        "",
    ]

    # Reddit
    reddit = pulse.get("reddit", [])
    if reddit:
        lines.append("####  Reddit Community Consensus")
        for item in reddit[:3]:
            lines.append(f"- **[{item['title']}]({item['url']})**")
            lines.append(f"  *{item['community']}* · **{item['score']} upvotes** · {item['comments']} comments")
        lines.append("")

    # Hacker News
    hn = pulse.get("hackernews", [])
    if hn:
        lines.append("####  Hacker News Developer Takes")
        for item in hn[:3]:
            lines.append(f"- **[{item['title']}]({item['url']})**")
            lines.append(f"  **{item['score']} points** · [{item['comments']} comments]({item['discussion_url']})")
        lines.append("")

    # GitHub
    gh = pulse.get("github", [])
    if gh:
        lines.append("####  GitHub Open Source Activity")
        for item in gh[:3]:
            lines.append(f"- **[{item['title']}]({item['url']})** ( {item['score']:,} stars)")
            if item.get("description"):
                lines.append(f"  _{item['description']}_")
        lines.append("")

    # Polymarket
    poly = pulse.get("polymarket", [])
    if poly:
        lines.append("####  Polymarket Real-Money Odds")
        for item in poly[:3]:
            vol = f"${item['volume']:,.0f}" if isinstance(item['volume'], (int, float)) else str(item['volume'])
            lines.append(f"- **[{item['title']}]({item['url']})**")
            lines.append(f"  Odds: **{item['odds']}** · Volume: {vol}")
        lines.append("")

    total_items = len(reddit) + len(hn) + len(gh) + len(poly)
    lines.append(f"_Retrieved {total_items} high-signal community items via Keyless Public APIs._")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="CrowdPulse: Zero-Dependency Community Intelligence Fast-Lane")
    parser.add_argument("query", nargs="*", help="Topic or query to search")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    parser.add_argument("--mock", action="store_true", help="Use mock data (offline mode)")
    parser.add_argument("--limit", type=int, default=5, help="Max results per platform (default: 5)")
    parser.add_argument("--timeout", type=float, default=3.5, help="Request timeout per source in seconds")

    args = parser.parse_args()
    q = " ".join(args.query).strip() if args.query else "ai coding agents"

    pulse = fetch_pulse(q, limit=args.limit, timeout=args.timeout, mock=args.mock)

    if args.json:
        print(json.dumps(pulse, indent=2))
    else:
        print(format_pulse_markdown(pulse))


if __name__ == "__main__":
    main()

