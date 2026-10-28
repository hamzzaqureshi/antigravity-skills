# Scrapling — Adaptive Web Scraping & Stealth Crawling Framework

> High-performance Python web scraping framework (90.2k+ stars) with HTTP/3, TLS browser fingerprint impersonation, Cloudflare Turnstile/Interstitial bypass, concurrent spiders, adaptive element parsing, and clean RAG markdown conversion.

---

## Quickstart

### 1. Installation

```bash
# Core parser + fetchers + browser stealth automation
pip install "scrapling[all]>=0.5"

# Install Chromium/Chrome stealth dependencies once
scrapling install --force
```

Check environment readiness at any time:
```bash
python3 scripts/scrapling_helper.py readiness
```

---

## Common Usage Patterns

### A. Fast Static Request with Browser Impersonation
```python
from scrapling.fetchers import FetcherSession

with FetcherSession(impersonate="chrome") as session:
    page = session.get("https://quotes.toscrape.com/", stealthy_headers=True)
    quotes = page.css(".quote .text::text").getall()
    print(quotes)
```

### B. Stealth Browser with Cloudflare Turnstile Bypass
```python
from scrapling.fetchers import StealthySession

with StealthySession(headless=True, solve_cloudflare=True) as session:
    page = session.fetch("https://nopecha.com/demo/cloudflare")
    links = page.css("#padded_content a").getall()
```

### C. Clean Markdown for LLMs & RAG (One-Liner)
```python
from scrapling.fetchers import Fetcher

page = Fetcher.get("https://en.wikipedia.org/wiki/Web_scraping")
# Generates clean, sanitized Markdown without an LLM in the loop
markdown_corpus = page.markdown()
```

### D. Concurrent Spider with AutoThrottle & Pause/Resume
```python
from scrapling.spiders import Spider, Response

class QuotesSpider(Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]
    concurrent_requests = 10

    async def parse(self, response: Response):
        for quote in response.css(".quote"):
            yield {
                "text": quote.css(".text::text").get(),
                "author": quote.css(".author::text").get(),
            }
        next_page = response.css(".next a")
        if next_page:
            yield response.follow(next_page[0].attrib["href"])

result = QuotesSpider(crawldir="./crawl_data").start()
result.items.to_json("quotes.json")
```

---

## CLI Commands

Extract clean Markdown or text without writing code:
```bash
# Convert page to Markdown for AI consumption (with prompt-injection protection)
scrapling extract get "https://example.com" article.md --ai-targeted

# Use stealth browser for Cloudflare-protected sites
scrapling extract fetch "https://nopecha.com/demo/cloudflare" captchas.html --solve-cloudflare
```

---

## References & Guides

- **Fetching Strategies**: [references/fetching/choosing.md](references/fetching/choosing.md)
- **Stealth & Cloudflare**: [references/fetching/stealthy.md](references/fetching/stealthy.md)
- **Adaptive Selectors**: [references/parsing/adaptive.md](references/parsing/adaptive.md)
- **Spiders & Architecture**: [references/spiders/architecture.md](references/spiders/architecture.md)
- **Building RAG Systems**: [references/building-rag-systems.md](references/building-rag-systems.md)
- **MCP Server Protocol**: [references/mcp-server.md](references/mcp-server.md)

