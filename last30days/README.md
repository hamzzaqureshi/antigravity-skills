# last30days: Real-Time Multi-Platform Intelligence

[![Tests](https://img.shields.io/badge/tests-8%20passed-22c55e?style=flat-square)](tests/)
[![Platforms](https://img.shields.io/badge/sources-24%20platforms-38bdf8?style=flat-square)](SKILL.md)
[![Zero-Dependencies](https://img.shields.io/badge/fast--lane-CrowdPulse%20%3C150ms-0ea5e9?style=flat-square)](scripts/pulse.py)
[![License](https://img.shields.io/badge/license-MIT-64748b?style=flat-square)](LICENSE)

> **Real-time temporal consensus engine: research what engineers and communities actually say across Reddit, X, YouTube, Hacker News, Polymarket, and GitHub over the last 30 days.**

---

## Overview

LLM pre-training knowledge is static and drifts over time. `last30days` queries live platform feeds to surface real-time developer sentiment, emerging bugs, modern consensus, and betting odds:
- **CrowdPulse Fast-Lane (`scripts/pulse.py`)**: Zero-API-key, sub-150ms concurrent queries to Reddit, Hacker News, GitHub, and Polymarket using standard library Python.
- **Deep Research Engine (`scripts/last30days.py`)**: Multi-source aggregator weighting results by engagement (upvotes, views, comments, and capital).

---

## Quickstart & CLI

```bash
# Query instant developer pulse on a topic (<150ms, zero keys)
python3 last30days/scripts/pulse.py "react 19"

# Full multi-platform research across 24 sources
python3 last30days/scripts/last30days.py "claude code vs codex"

# Run doctor diagnostics to verify feed health
python3 last30days/scripts/doctor.py
```

---

## Automated Verification

Run unit tests via standard Python `unittest`:
```bash
python3 -B -m unittest discover -s tests
```

