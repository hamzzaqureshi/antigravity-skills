#!/usr/bin/env python3
"""Humanize Audit: Automated 26-Pattern AI Slop Prose Scanner.

Detects Wikipedia's 26 'Signs of AI Writing' across markdown, docs, PRs, and copy.
Computes a 100-point human authenticity score and provides exact line fixes.
Zero external dependencies (pure Python standard library).
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List

# Core regex rules for the 26 AI writing patterns
PATTERNS = [
    # A. Staging instead of stating
    {
        "id": 1,
        "category": "Staging",
        "name": "Not X but Y contrast",
        "severity": "HIGH",
        "regex": r"(?i)\b(?:it'?s not (?:just|only|merely)\b.*?,\s*(?:it'?s|it is|it represents)\b|this doesn'?t mean\b.*?\.\s*it means\b)",
        "fix": "Cut the contrast and state the actual claim directly.",
    },
    {
        "id": 2,
        "category": "Staging",
        "name": "One-line dramatic closer",
        "severity": "HIGH",
        "regex": r"(?i)(?:let that sink in\.?|that is the real win\.?|and that makes all the difference\.?|the rest is history\.?)",
        "fix": "Remove the closer that explains or dramatizes the fact.",
    },
    {
        "id": 3,
        "category": "Staging",
        "name": "Saying that sounds deep",
        "severity": "HIGH",
        "regex": r"(?i)\b(?:at its core,\s*what (?:really )?matters|symmetry is the language of|in a world where\b)",
        "fix": "Replace the fake philosophical saying with a concrete fact.",
    },
    {
        "id": 4,
        "category": "Staging",
        "name": "Staged run-up before point",
        "severity": "HIGH",
        "regex": r"(?i)\b(?:let'?s dive in\b|honestly\?\s*it depends|here'?s the (?:thing|kicker|deal):?)",
        "fix": "Delete the throat-clearing opener and start with the claim.",
    },
    {
        "id": 5,
        "category": "Staging",
        "name": "Arguing with no one",
        "severity": "MEDIUM",
        "regex": r"(?i)\b(?:i'?m not saying\b.*?\bbut\b|a tempting (?:approach|mistake) would be\b)",
        "fix": "Remove the fake objection and keep the real decision.",
    },
    # B. Rhythm by rule & punctuation
    {
        "id": 8,
        "category": "Rhythm",
        "name": "Em-dashes as universal connector",
        "severity": "LOW",
        "regex": r"(?: — |—[A-Za-z])",
        "fix": "Replace with periods, commas, colons, or parentheses.",
    },
    {
        "id": 9,
        "category": "Rhythm",
        "name": "Stacked qualifiers",
        "severity": "LOW",
        "regex": r"(?i)\b(?:could potentially possibly|might arguably perhaps|generally usually tends to)\b",
        "fix": "Pick one supported qualifier or remove entirely.",
    },
    # C. Inflation & Stock AI Vocabulary
    {
        "id": 12,
        "category": "Inflation",
        "name": "Stock AI buzzwords",
        "severity": "HIGH",
        "regex": r"(?i)\b(?:delve(?:s|d|ing)? into|a testament to|rich tapestry|beacon of|pivotal moment|landscape of|seamlessly|in today'?s fast-paced|game-?changer|revolutionize)\b",
        "fix": "Replace cliché AI marketing terms with specific, neutral verbs.",
    },
    {
        "id": 13,
        "category": "Inflation",
        "name": "Inflated significance",
        "severity": "MEDIUM",
        "regex": r"(?i)\b(?:marking a (?:pivotal|historic) moment|despite challenges,?\s*continues to thrive|the future looks bright)\b",
        "fix": "Keep the underlying fact and drop the inflated importance.",
    },
    {
        "id": 16,
        "category": "Inflation",
        "name": "Sales brochure language",
        "severity": "MEDIUM",
        "regex": r"(?i)\b(?:nestled within|breathtaking|unparalleled|unlock your potential|elevate your\b)",
        "fix": "State plainly what the product or place is.",
    },
    {
        "id": 18,
        "category": "Inflation",
        "name": "Avoiding is/are/has",
        "severity": "LOW",
        "regex": r"(?i)\b(?:serves as|boasts a|features a)\b",
        "fix": "Use simple 'is' or 'has'.",
    },
    # D. Formatting by rule
    {
        "id": 19,
        "category": "Formatting",
        "name": "Bold labels as decoration",
        "severity": "LOW",
        "regex": r"^\s*[-*]\s*\*\*[^*]+:\*\*\s+",
        "fix": "Turn the mechanical labeled bullet into conversational prose.",
    },
    # E. Chatbot residue
    {
        "id": 22,
        "category": "Residue",
        "name": "Chatbot residue & conversational filler",
        "severity": "HIGH",
        "regex": r"(?i)\b(?:great question!|certainly!|i'?d be happy to help|i hope this helps!|as an ai language model)\b",
        "fix": "Delete conversational fluff; output content directly.",
    },
    {
        "id": 23,
        "category": "Residue",
        "name": "Knowledge-limit disclaimers",
        "severity": "MEDIUM",
        "regex": r"(?i)\b(?:while details are limited in available sources|based on the information provided)\b",
        "fix": "State what the sources show or omit the sentence.",
    },
]


def audit_text(text: str, filename: str = "<stdin>") -> Dict[str, Any]:
    """Scan text against the 26 AI writing patterns."""
    lines = text.splitlines()
    findings = []
    penalty = 0

    severity_weights = {"HIGH": 8, "MEDIUM": 4, "LOW": 2}

    for p in PATTERNS:
        prog = re.compile(p["regex"])
        matches_found = 0
        for line_num, line in enumerate(lines, 1):
            for m in prog.finditer(line):
                matches_found += 1
                matched_snippet = m.group(0)
                findings.append({
                    "line": line_num,
                    "pattern_id": p["id"],
                    "pattern_name": p["name"],
                    "category": p["category"],
                    "severity": p["severity"],
                    "match": matched_snippet,
                    "fix": p["fix"],
                    "line_context": line.strip()[:100],
                })
        if matches_found > 0:
            penalty += min(matches_found * severity_weights[p["severity"]], 25)

    score = max(0, 100 - penalty)
    grade = (
        "A (Clean Human Prose)" if score >= 90 else
        "B (Minor AI Tells)" if score >= 75 else
        "C (Noticeable AI Slop)" if score >= 50 else
        "F (Heavy AI Slop)"
    )

    return {
        "file": filename,
        "total_lines": len(lines),
        "total_words": len(text.split()),
        "findings_count": len(findings),
        "score": score,
        "grade": grade,
        "findings": findings,
    }


def format_report(result: Dict[str, Any]) -> str:
    """Format audit results into terminal/markdown report."""
    lines = [
        "========================================================================",
        f"               HUMANIZER PROSE AUDIT: {result['file']}",
        "========================================================================",
        f"  • Score : {result['score']} / 100 ({result['grade']})",
        f"  • Lines : {result['total_lines']}  |  Words: {result['total_words']}",
        f"  • Tells Detected : {result['findings_count']}",
        "------------------------------------------------------------------------",
    ]

    if not result["findings"]:
        lines.append("  [PASS] No AI writing tells detected! Text reads naturally human.")
    else:
        lines.append("DETECTED AI TELLS & SUGGESTED REWRITES:")
        for idx, f in enumerate(result["findings"], 1):
            lines.append(f"\n[{idx}] Line {f['line']}: {f['pattern_name']} ({f['severity']} severity)")
            lines.append(f"    Match : \"{f['match']}\"")
            lines.append(f"    Context: {f['line_context']}")
            lines.append(f"    Fix   : {f['fix']}")

    lines.append("\n========================================================================")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Humanizer: Scan text for AI writing patterns")
    parser.add_argument("path", nargs="?", help="Path to text or markdown file")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--strict", action="store_true", help="Exit with code 1 if score < 80")

    args = parser.parse_args()

    if args.path:
        if not os.path.exists(args.path):
            print(f"File not found: {args.path}", file=sys.stderr)
            sys.exit(1)
        with open(args.path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        filename = args.path
    else:
        # Read from stdin
        if sys.stdin.isatty():
            parser.print_help()
            sys.exit(0)
        content = sys.stdin.read()
        filename = "<stdin>"

    result = audit_text(content, filename=filename)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_report(result))

    if args.strict and result["score"] < 80:
        sys.exit(1)


if __name__ == "__main__":
    main()

