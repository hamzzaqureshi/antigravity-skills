#!/usr/bin/env python3
"""Socratic Reasoning & Gate Engine for Antigravity.

Analyzes engineering tasks, maps relevant domains and packs,
calculates token budgets, and formats the Socratic contract and readiness gates.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
QUESTIONS_DIR = SKILL_ROOT / "questions"
PACKS_DIR = SKILL_ROOT / "packs"
GRADES_DIR = SKILL_ROOT / "grades"

DOMAINS = {
    "00": {"id": "00-requirements", "name": "Requirements & Scope", "always": True},
    "01": {
        "id": "01-frontend",
        "name": "Frontend & UI",
        "signals": [
            "frontend", "ui", "react", "vue", "svelte", "component",
            "css", "html", "tailwind", "layout", "button", "modal", "page"
        ],
    },
    "02": {
        "id": "02-backend",
        "name": "Backend & Services",
        "signals": [
            "backend", "service", "endpoint", "job", "queue", "worker",
            "express", "fastapi", "django", "server", "controller", "daemon"
        ],
    },
    "03": {
        "id": "03-data",
        "name": "Data & Storage",
        "signals": [
            "database", "schema", "postgres", "mysql", "sqlite", "redis",
            "sql", "storage", "migration", "cache", "orm", "table", "persistence"
        ],
    },
    "04": {
        "id": "04-api",
        "name": "API Design",
        "signals": [
            "api", "sdk", "webhook", "connector", "integration", "oauth",
            "rest", "graphql", "grpc", "endpoint", "payload", "json"
        ],
    },
    "05": {
        "id": "05-security",
        "name": "Security",
        "signals": [
            "auth", "authentication", "jwt", "authorization", "secret",
            "token", "password", "crypto", "encryption", "permission", "cors", "public", "payment"
        ],
    },
    "06": {
        "id": "06-infra",
        "name": "Infrastructure & DevOps",
        "signals": [
            "deploy", "docker", "k8s", "kubernetes", "ci/cd", "cloud",
            "aws", "gcp", "azure", "terraform", "container", "pipeline"
        ],
    },
    "07": {"id": "07-testing", "name": "Testing & Quality", "always": True},
    "08": {
        "id": "08-observability",
        "name": "Observability & Ops",
        "signals": [
            "monitoring", "metrics", "log", "logging", "alert", "sentry",
            "datadog", "prometheus", "tracing", "otel", "telemetry", "cron"
        ],
    },
    "09": {
        "id": "09-ai-llm",
        "name": "AI / LLM / Agents",
        "signals": [
            "ai", "llm", "agent", "prompt", "model", "rag", "embedding",
            "vector", "openai", "claude", "gemini", "fine-tuning", "tokens"
        ],
    },
    "10": {
        "id": "10-mobile",
        "name": "Mobile & Offline",
        "signals": [
            "mobile", "ios", "android", "offline", "pwa", "flutter",
            "react-native", "swift", "kotlin", "app"
        ],
    },
    "11": {
        "id": "11-product-ux",
        "name": "Product & UX",
        "signals": [
            "user", "onboarding", "ux", "workflow", "error-message",
            "notification", "analytics", "funnel", "cli"
        ],
    },
    "12": {
        "id": "12-cost-performance",
        "name": "Cost & Performance",
        "signals": [
            "scale", "latency", "performance", "throughput", "concurrency",
            "benchmark", "spend", "cost", "high traffic", "p95", "p99"
        ],
    },
    "13": {
        "id": "13-compliance",
        "name": "Compliance & Legal",
        "signals": [
            "gdpr", "hipaa", "privacy", "personal data", "pii", "audit",
            "legal", "license", "copyright", "retention"
        ],
    },
    "14": {
        "id": "14-team-maintenance",
        "name": "Team & Maintenance",
        "signals": [
            "refactor", "legacy", "documentation", "cleanup", "technical debt",
            "deprecation", "on-call", "runbook", "team"
        ],
    },
}

PACK_TRIGGERS = {
    "software-design": ["complexity", "abstraction", "interface", "class", "module", "coupling"],
    "domain-modeling": ["aggregate", "bounded context", "domain", "entity", "value object", "ubiquitous language"],
    "data-systems": ["source of truth", "consistency", "idempotency", "eventual", "partition", "distributed", "replication"],
    "operations": ["timeout", "retry", "circuit breaker", "load shedding", "rollback", "3am", "runbook", "outage"],
    "threat-modeling": ["attacker", "threat", "trust boundary", "elevation", "tampering", "spoofing"],
    "ai-engineering": ["evals", "rag", "hallucination", "retrieval", "prompt injection", "token budget"],
    "agent-design": ["subagent", "multi-agent", "tool permissions", "delegation", "dispatcher", "verifier"],
    "legacy-change": ["legacy code", "seam", "characterization test", "untested", "sprout method", "strangler"],
    "testing-design": ["mock", "unit test", "brittle test", "test pyramid", "test suite", "regression"],
    "product-discovery": ["problem-solution", "mom test", "discovery", "interview", "willingness to pay"],
}


def detect_domains(text: str) -> list[str]:
    """Scans text and returns matching domain IDs."""
    text_lower = text.lower()
    matched = []

    for num, meta in DOMAINS.items():
        if meta.get("always"):
            matched.append(meta["id"])
            continue

        signals = meta.get("signals", [])
        for sig in signals:
            pattern = rf"\b{re.escape(sig)}s?\b"
            if re.search(pattern, text_lower):
                matched.append(meta["id"])
                break

    return sorted(list(set(matched)))


def detect_packs(text: str) -> list[str]:
    """Scans text and returns recommended specialized packs."""
    text_lower = text.lower()
    matched = []

    for pack, triggers in PACK_TRIGGERS.items():
        for trig in triggers:
            pattern = rf"\b{re.escape(trig)}s?\b"
            if re.search(pattern, text_lower):
                matched.append(pack)
                break

    return sorted(list(set(matched)))


def estimate_tokens(domain_ids: list[str], pack_names: list[str], depth: str = "core") -> int:
    """Estimates tokens consumed by loading the selected domain and pack files."""
    # Approximate ~1 token per 4 characters / 0.75 words
    total_words = 0
    # Base SKILL.md ~ 1,800 words (~2,300 tokens)
    skill_md = SKILL_ROOT / "SKILL.md"
    if skill_md.exists():
        total_words += len(skill_md.read_text(encoding="utf-8").split())

    sub_dir = "core" if depth == "core" else ""
    for d in domain_ids:
        path = QUESTIONS_DIR / sub_dir / f"{d}.md" if sub_dir else QUESTIONS_DIR / f"{d}.md"
        if path.exists():
            total_words += len(path.read_text(encoding="utf-8").split())

    for p in pack_names:
        p_path = PACKS_DIR / p / "core.md"
        if p_path.exists():
            total_words += len(p_path.read_text(encoding="utf-8").split())

    # Return estimated tokens (~1.33 tokens per word)
    return int(total_words * 1.33)


def format_contract(
    domains: list[str],
    highlights: list[str] | None = None,
    assumed: list[str] | None = None,
    open_questions: list[str] | None = None,
    risks: list[str] | None = None,
    plan: list[str] | None = None,
) -> str:
    """Renders the standard Socratic Contract markdown."""
    hl = highlights or ["Read existing patterns from codebase", "Applied standard engineering defaults"]
    asm = assumed or ["Single-process concurrency safe", "Default timeouts sufficient for initial tier"]
    oq = open_questions or ["(None - all engineering decisions resolved internally)"]
    rk = risks or ["Downstream network stalls without circuit breakers"]
    pln = plan or ["Implement minimum complete design", "Run test suite and domain verification"]

    lines = [
        "### Socratic Engineering Contract",
        f"- **Domains considered:** {', '.join(domains)}",
        "- **Self-answered highlights:**",
    ]
    lines.extend([f"  • {h}" for h in hl])
    lines.append("- **Assumed (flag if wrong):**")
    lines.extend([f"  • {a}" for a in asm])
    lines.append("- **Open questions for you:**")
    lines.extend([f"  • {q}" for q in oq])
    lines.append("- **Top risks & mitigations:**")
    lines.extend([f"  • {r}" for r in rk])
    lines.append("- **Execution Plan:**")
    lines.extend([f"  {idx}. {p}" for idx, p in enumerate(pln, 1)])

    return "\n".join(lines)


def get_gate(grade: str) -> str:
    """Fetches the readiness gate checklist for mvp, production, or enterprise."""
    grade_path = GRADES_DIR / f"{grade}.md"
    if not grade_path.exists():
        raise FileNotFoundError(f"Unknown grade: {grade}. Available: mvp, production, enterprise")
    return grade_path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Socratic Engineering Assistant CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # scan
    scan_p = subparsers.add_parser("scan", help="Scan prompt or task description for domains & packs")
    scan_p.add_argument("text", type=str, help="Prompt or task text to analyze")
    scan_p.add_argument("--depth", choices=["core", "full"], default="core", help="Question depth")

    # gate
    gate_p = subparsers.add_parser("gate", help="Show readiness gate for a grade")
    gate_p.add_argument("grade", choices=["mvp", "production", "enterprise"], help="Target grade")

    # contract
    contract_p = subparsers.add_parser("contract", help="Generate Socratic contract scaffold")
    contract_p.add_argument("text", type=str, help="Task description")

    args = parser.parse_args()

    if args.command == "scan":
        domains = detect_domains(args.text)
        packs = detect_packs(args.text)
        tokens = estimate_tokens(domains, packs, depth=args.depth)
        print(f"[PASS] Domains ({len(domains)}): {', '.join(domains)}")
        if packs:
            print(f"[PASS] Suggested Packs ({len(packs)}): {', '.join(packs)}")
        else:
            print("[PASS] Suggested Packs: None (generic domain questions sufficient)")
        print(f"[METRICS] Estimated Token Budget ({args.depth}): ~{tokens:,} tokens")
        return 0

    elif args.command == "gate":
        content = get_gate(args.grade)
        print(content)
        return 0

    elif args.command == "contract":
        domains = detect_domains(args.text)
        print(format_contract(domains))
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
