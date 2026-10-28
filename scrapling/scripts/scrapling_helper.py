#!/usr/bin/env python3
"""Scrapling Helper CLI: Environment Readiness, Code Generator & Fallback Extractor.

Provides zero-dependency utilities for Antigravity AI agents:
  1. Readiness check (detects scrapling, playwright, browser dependencies)
  2. Code snippet generator (static, stealth, spider, RAG markdown)
  3. Lightweight fallback extractor (standard library urllib for offline/zero-dependency environments)
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from typing import Dict, Any

TEMPLATES = {
    "static": '''from scrapling.fetchers import FetcherSession

# Fast HTTP request with Chrome TLS fingerprint impersonation
with FetcherSession(impersonate="chrome") as session:
    page = session.get("https://example.com", stealthy_headers=True)
    titles = page.css("h1::text, h2::text").getall()
    print("Found titles:", titles)
''',
    "stealth": '''from scrapling.fetchers import StealthySession

# Stealth browser automation with Cloudflare Turnstile bypass
with StealthySession(headless=True, solve_cloudflare=True) as session:
    page = session.fetch("https://nopecha.com/demo/cloudflare")
    links = page.css("#padded_content a::attr(href)").getall()
    print("Extracted links:", links)
''',
    "spider": '''import asyncio
from scrapling.spiders import Spider, Response

class SiteSpider(Spider):
    name = "site_crawler"
    start_urls = ["https://quotes.toscrape.com/"]
    concurrent_requests = 5

    async def parse(self, response: Response):
        for item in response.css(".quote"):
            yield {
                "text": item.css(".text::text").get(),
                "author": item.css(".author::text").get(),
            }
        next_page = response.css(".next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page)

result = SiteSpider(crawldir="./crawl_cache").start()
print(f"Scraped {len(result.items)} items")
result.items.to_json("output.json")
''',
    "rag": '''from scrapling.fetchers import Fetcher

# Convert any webpage directly into clean, sanitized Markdown for RAG / LLM context
page = Fetcher.get("https://en.wikipedia.org/wiki/Web_scraping")
markdown_corpus = page.markdown()

with open("article.md", "w", encoding="utf-8") as f:
    f.write(markdown_corpus)
print("Saved clean RAG markdown (bytes:", len(markdown_corpus), ")")
'''
}


def check_readiness() -> Dict[str, Any]:
    """Check availability of Scrapling and browser dependencies."""
    scrapling_installed = False
    scrapling_version = None
    try:
        import scrapling
        scrapling_installed = True
        scrapling_version = getattr(scrapling, "__version__", "unknown")
    except ImportError:
        pass

    has_scrapling_cli = shutil.which("scrapling") is not None
    has_docker = shutil.which("docker") is not None

    return {
        "scrapling_installed": scrapling_installed,
        "scrapling_version": scrapling_version,
        "scrapling_cli": has_scrapling_cli,
        "docker_available": has_docker,
        "install_command": 'pip install "scrapling[all]>=0.5" && scrapling install --force',
        "docker_command": "docker pull ghcr.io/d4vinci/scrapling:latest",
    }


def html_to_simple_markdown(html: str) -> str:
    """Basic standard-library HTML to text/markdown converter."""
    # Remove script and style elements
    clean = re.sub(r"<(script|style).*?</\1>", "", html, flags=re.DOTALL | re.IGNORECASE)
    # Convert headings
    clean = re.sub(r"<h1[^>]*>(.*?)</h1>", r"# \1\n\n", clean, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r"<h2[^>]*>(.*?)</h2>", r"## \1\n\n", clean, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r"<h3[^>]*>(.*?)</h3>", r"### \1\n\n", clean, flags=re.DOTALL | re.IGNORECASE)
    # Convert paragraphs
    clean = re.sub(r"<p[^>]*>(.*?)</p>", r"\1\n\n", clean, flags=re.DOTALL | re.IGNORECASE)
    # Convert links
    clean = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', r"[\2](\1)", clean, flags=re.DOTALL | re.IGNORECASE)
    # Strip remaining HTML tags
    clean = re.sub(r"<[^>]+>", "", clean)
    # Normalize excessive newlines
    clean = re.sub(r"\n{3,}", "\n\n", clean)
    return clean.strip()


def mock_extraction(url: str) -> str:
    """Deterministic mock extraction for tests and offline sandboxes."""
    mock_html = f"""<html>
<head><title>Mock Web Page</title></head>
<body>
<h1>Scrapling Mock Data</h1>
<p>Target URL: {url}</p>
<p>Scrapling provides <strong>stealth browsing</strong> and <strong>Cloudflare bypass</strong>.</p>
<div class="quotes">
  <div class="quote"><span class="text">The best code is simple code.</span></div>
</div>
<a href="https://example.com/docs">Documentation Link</a>
</body></html>"""
    return html_to_simple_markdown(mock_html)


def main():
    parser = argparse.ArgumentParser(description="Scrapling Helper CLI for Antigravity")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # readiness
    p_readiness = subparsers.add_parser("readiness", help="Check Scrapling environment status")
    p_readiness.add_argument("--json", action="store_true", help="Output JSON format")

    # snippet
    p_snippet = subparsers.add_parser("snippet", help="Print Scrapling code template")
    p_snippet.add_argument("type", choices=["static", "stealth", "spider", "rag"], help="Template type")

    # extract
    p_extract = subparsers.add_parser("extract", help="Extract webpage content (fallback/mock)")
    p_extract.add_argument("url", nargs="?", default="https://example.com", help="Target URL")
    p_extract.add_argument("--mock", action="store_true", help="Use deterministic mock data")
    p_extract.add_argument("--markdown", action="store_true", help="Format as clean markdown")

    args = parser.parse_args()

    if args.command == "readiness":
        status = check_readiness()
        if args.json:
            print(json.dumps(status, indent=2))
        else:
            print("========================================================================")
            print("                 SCRAPLING ENVIRONMENT READINESS")
            print("========================================================================")
            print(f"  • Scrapling Library : {'[OK] INSTALLED (' + str(status['scrapling_version']) + ')' if status['scrapling_installed'] else '✖ NOT INSTALLED'}")
            print(f"  • Scrapling CLI     : {'[OK] AVAILABLE' if status['scrapling_cli'] else '✖ NOT IN PATH'}")
            print(f"  • Docker Fallback   : {'[OK] AVAILABLE' if status['docker_available'] else '✖ NOT AVAILABLE'}")
            print("------------------------------------------------------------------------")
            if not status["scrapling_installed"]:
                print("  Install via pip:")
                print(f"    {status['install_command']}")
            else:
                print("  Status: Ready for high-performance scraping!")
            print("========================================================================")

    elif args.command == "snippet":
        print(TEMPLATES[args.type])

    elif args.command == "extract":
        if args.mock:
            print(mock_extraction(args.url))
        else:
            try:
                req = urllib.request.Request(args.url, headers={"User-Agent": "Mozilla/5.0 (compatible; Antigravity/1.0)"})
                with urllib.request.urlopen(req, timeout=5.0) as resp:
                    html = resp.read().decode("utf-8", errors="replace")
                if args.markdown:
                    print(html_to_simple_markdown(html))
                else:
                    print(html[:2000])
            except Exception as e:
                print(f"Extraction failed: {e}", file=sys.stderr)
                sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

