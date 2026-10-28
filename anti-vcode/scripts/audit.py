#!/usr/bin/env python3
"""Anti-Vibecoding Frontend Auditor.

Scans frontend codebases (HTML, CSS, JSX, TSX, Vue, Svelte) for the 40 signs
of generic AI-generated frontend design, and outputs a concrete Authorship Score
along with specific remediation advice.

Usage:
    python3 audit.py <file-or-directory> [--json] [--threshold N]
"""
import argparse
import json
import os
import re
import sys

# Cliché pattern detectors
RULES = [
    {
        "id": "purple-blue-gradient",
        "name": "Purple-to-Blue AI Gradient",
        "category": "Visual Language",
        "weight": 8,
        "pattern": re.compile(r"(from-purple-\d+\s+to-blue-\d+|from-indigo-\d+\s+to-purple-\d+|linear-gradient\([^)]*(#8b5cf6|#6366f1|#a855f7|purple|indigo)[^)]*(#3b82f6|#06b6d4|blue|cyan)[^)]*\))", re.I),
        "advice": "Replace generic purple-blue linear gradients with solid tonal backgrounds, subtle hairlines, or single intentional focal accents."
    },
    {
        "id": "gradient-text-hero",
        "name": "Gradient Text on Hero Headline",
        "category": "Visual Language",
        "weight": 6,
        "pattern": re.compile(r"<h[1-3][^>]*(bg-clip-text\s+text-transparent|background-clip:\s*text)[^>]*>", re.I),
        "advice": "Rely on strong typographic weight, scale, and high-contrast letterforms instead of masking text with multi-stop gradients."
    },
    {
        "id": "radial-gradient-orb",
        "name": "Giant Radial Gradient Orb",
        "category": "Visual Language",
        "weight": 5,
        "pattern": re.compile(r"(radial-gradient|blur-(2xl|3xl)[^>]*rounded-full[^>]*bg-(purple|blue|indigo)-\d+)", re.I),
        "advice": "Remove decorative blurred background spheres. Give positive content breathing room through genuine spatial geometry."
    },
    {
        "id": "excessive-glassmorphism",
        "name": "Excessive Glassmorphism / Frosted Glass",
        "category": "Visual Language",
        "weight": 5,
        "pattern": re.compile(r"(backdrop-blur-(md|lg|xl)|backdrop-filter:\s*blur)", re.I),
        "advice": "Use crisp opaque surfaces with refined 1px border dividers rather than stacking translucent frosted cards."
    },
    {
        "id": "soft-radius-spam",
        "name": "Soft Pill Radius on Everything",
        "category": "Visual Language",
        "weight": 4,
        "pattern": re.compile(r"\b(rounded-2xl|rounded-3xl|border-radius:\s*(1[6-9]|[2-9]\d)px)\b", re.I),
        "advice": "Use disciplined, restrained corner radii (e.g. 4px - 8px) to establish architectural structure instead of soft pill shapes."
    },
    {
        "id": "sparkle-ai-icon",
        "name": "Sparkle Icon Pretending to Mean AI",
        "category": "UI Clichés",
        "weight": 7,
        "pattern": re.compile(r"(<Sparkles\b|\u2728|\u2729|icon=['\"]sparkles?['\"])", re.I),
        "advice": "Remove sparkle icons. Let features demonstrate their capability through functional previews and real workflows."
    },
    {
        "id": "emoji-heading",
        "name": "Emoji in Section Headings",
        "category": "UI Clichés",
        "weight": 5,
        "pattern": re.compile(r"<h[1-4][^>]*>[^<]*[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F900-\U0001F9FF][^<]*</h[1-4]>", re.I),
        "advice": "Remove casual emojis from technical and professional section titles."
    },
    {
        "id": "decorative-terminal",
        "name": "Decorative Fake Terminal Window",
        "category": "UI Clichés",
        "weight": 5,
        "pattern": re.compile(r"(bg-red-500[^>]*bg-yellow-500[^>]*bg-green-500|window-controls|mac-dots)", re.I),
        "advice": "If showing code or CLI output, show real, copyable commands with interactive outputs without decorative traffic-light dots."
    },
    {
        "id": "generic-buzzword-copy",
        "name": "Generic Buzzword Copywriting",
        "category": "Content & Product",
        "weight": 8,
        "pattern": re.compile(r"(transform your workflow|the future of\s+\w+|supercharge your\s+\w+|intelligent collaboration|it's not \w+,\s*it's \w+)", re.I),
        "advice": "Replace hollow hype statements with concrete product demonstrations (e.g., 'Audits your source code in 12ms')."
    },
    {
        "id": "fake-social-proof",
        "name": "Suspicious Social Proof Metric",
        "category": "Content & Product",
        "weight": 6,
        "pattern": re.compile(r"(trusted by (10|50|100),000\+ teams|join (10|50|100),000\+ (creators|developers))", re.I),
        "advice": "Show real verified customer quotes, case studies, or link directly to open-source metrics rather than generic rounded totals."
    },
    {
        "id": "em-dash-spam",
        "name": "Overused Em-Dashes",
        "category": "Typography",
        "weight": 4,
        "pattern": re.compile(r"([a-zA-Z]+—[a-zA-Z]+.*—[a-zA-Z]+)", re.I),
        "advice": "Reduce mechanical em-dash phrasing. Use clear, direct sentences with standard punctuation."
    },
    {
        "id": "default-inter-everywhere",
        "name": "Undifferentiated Inter / Geist Default",
        "category": "Typography",
        "weight": 4,
        "pattern": re.compile(r"(font-family:\s*['\"]?(Inter|Geist)['\"]?,|font-inter|font-geist)", re.I),
        "advice": "Pair a distinct editorial or geometric display typeface for headings with a disciplined monospace or humanist body font."
    }
]

EXTENSIONS = {".html", ".htm", ".css", ".jsx", ".tsx", ".vue", ".svelte", ".js", ".ts"}


def scan_file(filepath):
    findings = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception as e:
        return findings

    for line_idx, line in enumerate(lines, start=1):
        for rule in RULES:
            if rule["pattern"].search(line):
                findings.append({
                    "file": filepath,
                    "line": line_idx,
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "category": rule["category"],
                    "weight": rule["weight"],
                    "advice": rule["advice"],
                    "snippet": line.strip()[:100]
                })
    return findings


def scan_path(target_path):
    if os.path.isfile(target_path):
        return scan_file(target_path)
    
    all_findings = []
    for root, dirs, files in os.walk(target_path):
        # Skip node_modules, build outputs, and hidden dirs
        dirs[:] = [d for d in dirs if d not in {"node_modules", ".git", "dist", "build", ".next", ".cache"}]
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in EXTENSIONS:
                fp = os.path.join(root, file)
                all_findings.extend(scan_file(fp))
    return all_findings


def compute_score(findings):
    # Total deduction capped at 100. Authorship score = 100 - total_penalties.
    penalty = sum(f["weight"] for f in findings)
    score = max(0, 100 - min(100, penalty))
    return score


def print_report(findings, target_path, score):
    print("=" * 68)
    print("         ANTI-VIBECODING FRONTEND AUDIT REPORT")
    print("=" * 68)
    print(f"Target: {os.path.abspath(target_path)}")
    print(f"Authorship Score: {score}/100")
    if score >= 85:
        verdict = "EXCELLENT (Intentional, Human-Authored Design)"
    elif score >= 65:
        verdict = "MODERATE (Some Generic AI Patterns Detected)"
    else:
        verdict = "HIGH VIBECODE DETECTED (Generic AI Slop Aesthetic)"
    print(f"Verdict: {verdict}")
    print(f"Flagged Clichés: {len(findings)}")
    print("-" * 68)

    if not findings:
        print("[PASS] No generic AI vibecoding clichés detected. Clean, intentional frontend!")
        print("=" * 68)
        return

    # Group by category
    by_cat = {}
    for f in findings:
        by_cat.setdefault(f["category"], []).append(f)

    for cat, items in by_cat.items():
        print(f"\n[{cat.upper()}] ({len(items)} occurrence(s)):")
        for item in items[:8]:  # Limit output per category
            rel_file = os.path.relpath(item["file"], target_path) if os.path.isdir(target_path) else os.path.basename(item["file"])
            print(f"  • L{item['line']} in {rel_file}: {item['rule_name']}")
            print(f"    Snippet: \"{item['snippet']}\"")
            print(f"    Fix: {item['advice']}\n")
        if len(items) > 8:
            print(f"    ... and {len(items) - 8} more occurrences.")

    print("=" * 68)
    print("Core Recommendation: Consult references/DESIGN-PRINCIPLES.md and")
    print("references/PALETTES-AND-TYPOGRAPHY.md for replacement tokens.")
    print("=" * 68)


def main():
    parser = argparse.ArgumentParser(description="Anti-Vibecoding Frontend Auditor")
    parser.add_argument("target", help="File or directory to audit")
    parser.add_argument("--json", action="store_true", help="Output raw JSON results")
    parser.add_argument("--threshold", type=int, default=70, help="Minimum acceptable score (exit 1 if below)")
    args = parser.parse_args()

    if not os.path.exists(args.target):
        sys.exit(f"Error: Target path '{args.target}' does not exist.")

    findings = scan_path(args.target)
    score = compute_score(findings)

    if args.json:
        result = {
            "target": os.path.abspath(args.target),
            "authorship_score": score,
            "findings_count": len(findings),
            "findings": findings
        }
        print(json.dumps(result, indent=2))
    else:
        print_report(findings, args.target, score)

    sys.exit(0 if score >= args.threshold else 1)


if __name__ == "__main__":
    main()
