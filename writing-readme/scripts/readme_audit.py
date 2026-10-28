#!/usr/bin/env python3
"""README Quality Auditor & 50-Point Scorecard Diagnostic Engine.

Zero-dependency Python tool to:
  1. Evaluate a GitHub README against the 10-dimension 50-point quality scorecard
  2. Detect anti-patterns (unreplaced placeholders, untagged code blocks, broken relative links)
  3. Validate structural hierarchy and heading levels
  4. Generate prioritized improvement recommendations
  5. Return machine-readable JSON or human-friendly colorized terminal reports
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

PLACEHOLDER_PATTERNS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"<your[-_]username>",
    r"<your[-_]repo>",
    r"<your[-_]api[-_]key>",
    r"\bYOUR_API_KEY\b",
    r"\bYOUR_SECRET\b",
    r"\[owner\]",
    r"\[repo\]",
    r"\[Project Name\]",
    r"lorem ipsum",
    r"replace this",
    r"\bfoo/bar\b",
]

CRITICAL_SECTIONS = [
    ("Installation", r"^#{1,3}\s+.*(install|setup|getting started)", "Installation instructions"),
    ("Usage", r"^#{1,3}\s+.*(usage|quickstart|example|getting started)", "Usage or quickstart guide"),
    ("Prerequisites", r"^#{1,3}\s+.*(prerequisite|requirement|system requirement)", "Prerequisites or requirements"),
    ("License", r"^#{1,3}\s+.*license", "License section or badge"),
]


def audit_readme(readme_path: Path, check_links: bool = True) -> dict:
    if not readme_path.is_file():
        return {
            "error": f"README file not found: {readme_path}",
            "passed": False,
            "total_score": 0,
        }

    text = readme_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    line_count = len(lines)
    word_count = len(re.findall(r"\b\w+\b", text))
    root_dir = readme_path.parent

    scores = {}
    feedback = {}
    critical_defects = []

    # Parse clean lines outside of code blocks, and check opening code blocks
    clean_lines = []
    untagged_code_blocks = 0
    in_code = False
    for l in lines:
        if l.strip().startswith("```"):
            if not in_code:
                # Opening code fence: check language tag
                tag = l.strip()[3:].strip()
                if not tag:
                    untagged_code_blocks += 1
            in_code = not in_code
            continue
        if not in_code:
            clean_lines.append(l)

    # 1. Purpose & Audience (0-5)
    # Check title, elevator pitch blockquote, problem/solution wording
    s1 = 0
    f1 = []
    has_h1 = any(re.match(r"^#\s+[^#]", l) for l in clean_lines)
    has_hook = any(l.startswith("> ") for l in clean_lines[:15])
    has_value_words = bool(re.search(r"\b(solve|why|problem|designed for|built for|solution|benefit)\b", text, re.I))

    if has_h1:
        s1 += 2
    else:
        f1.append("Missing primary H1 project title.")

    if has_hook:
        s1 += 2
    else:
        f1.append("Missing elevator pitch / one-sentence blockquote near the top.")

    if has_value_words:
        s1 += 1
    else:
        f1.append("Explain the core problem, user, or value proposition more explicitly.")

    scores["purpose_and_audience"] = min(5, s1)
    feedback["purpose_and_audience"] = f1

    # 2. Structure & Navigation (0-5)
    # Check heading levels, TOC if long, reasonable heading count
    s2 = 3
    f2 = []
    headings = [l for l in clean_lines if l.startswith("#")]
    heading_levels = [len(re.match(r"^(#+)", h).group(1)) for h in headings]

    # Check for heading level jumps (e.g. h1 -> h3)
    level_jumps = False
    for i in range(len(heading_levels) - 1):
        if heading_levels[i+1] > heading_levels[i] + 1:
            level_jumps = True
            break
    if level_jumps:
        s2 -= 1
        f2.append("Heading levels jump incorrectly (e.g. # to ###).")

    has_toc = any("table of contents" in l.lower() for l in headings) or any("[#overview]" in text.lower() or "[#installation]" in text.lower() for _ in [1])
    if line_count > 150 and not has_toc:
        s2 -= 1
        f2.append("README is > 150 lines but lacks a Table of Contents.")
    elif line_count <= 150 or has_toc:
        s2 += 1

    if len(headings) >= 4:
        s2 += 1

    scores["structure_and_navigation"] = max(0, min(5, s2))
    feedback["structure_and_navigation"] = f2

    # 3. Accuracy & Cleanliness (0-5)
    # Check for placeholder strings and suspicious tokens
    s3 = 5
    f3 = []
    found_placeholders = []
    for pat in PLACEHOLDER_PATTERNS:
        matches = re.findall(pat, text, re.IGNORECASE)
        if matches:
            found_placeholders.append(f"'{matches[0]}'")

    if found_placeholders:
        s3 = max(0, 5 - len(found_placeholders) * 2)
        f3.append(f"Detected unreplaced placeholders: {', '.join(found_placeholders)}.")
        if s3 == 0:
            critical_defects.append("Unreplaced template placeholders detected.")

    scores["accuracy"] = s3
    feedback["accuracy"] = f3

    # 4. Installation (0-5)
    s4 = 0
    f4 = []
    has_install = False
    has_code_block = False
    in_install_section = False
    in_code_state = False

    for l in lines:
        if l.strip().startswith("```"):
            in_code_state = not in_code_state
            if in_install_section and in_code_state:
                has_code_block = True
            continue
        if not in_code_state:
            if re.search(r"^#{1,3}\s+.*(install|setup|getting started)", l, re.I):
                has_install = True
                in_install_section = True
            elif in_install_section and l.startswith("#"):
                in_install_section = False

    if has_install:
        s4 += 3
        if has_code_block:
            s4 += 2
        else:
            f4.append("Installation section lacks copy-pasteable code blocks.")
    else:
        f4.append("Missing dedicated Installation or Setup section.")
        critical_defects.append("No installation section found.")

    scores["installation"] = min(5, s4)
    feedback["installation"] = f4

    # 5. Usage (0-5)
    s5 = 0
    f5 = []
    has_usage = any(re.search(r"^#{1,3}\s+.*(usage|quickstart|example|getting started)", l, re.I) for l in clean_lines)
    has_expected_output = bool(re.search(r"(expected output|output:|console\.log|print\(|stdout|result:)", text, re.I))

    if has_usage:
        s5 += 3
        if has_expected_output:
            s5 += 2
        else:
            f5.append("Include expected output logs so users can verify success.")
    else:
        f5.append("Missing dedicated Usage or Quickstart section.")

    scores["usage"] = min(5, s5)
    feedback["usage"] = f5

    # 6. Technical Explanation (0-5)
    s6 = 2
    f6 = []
    has_arch = bool(re.search(r"^#{1,3}\s+.*(architecture|system design|data flow|components)", text, re.I | re.M))
    has_diagram = "```mermaid" in text or "┌──" in text or "├──" in text or "──▶" in text

    if has_arch:
        s6 += 2
    if has_diagram:
        s6 += 1
    else:
        f6.append("Add a visual architecture diagram (Mermaid or ASCII box flow).")

    scores["technical_explanation"] = min(5, s6)
    feedback["technical_explanation"] = f6

    # 7. Readability (0-5)
    s7 = 5
    f7 = []
    if untagged_code_blocks > 0:
        s7 -= min(3, untagged_code_blocks * 2)
        f7.append(f"Found {untagged_code_blocks} code block(s) without syntax highlighting tags (e.g. ```bash, ```python).")

    # Check for long unbroken walls of text (> 120 words without bullet, table, or code)
    paragraphs = text.split("\n\n")
    long_paras = [
        p for p in paragraphs
        if len(p.split()) > 100
        and not p.startswith("```")
        and not p.startswith("#")
        and not p.startswith("|")
        and "```" not in p
    ]
    if long_paras:
        s7 -= 1
        f7.append("Found dense paragraphs > 100 words. Break up with bullet points or tables.")

    scores["readability"] = max(0, min(5, s7))
    feedback["readability"] = f7

    # 8. Visual Communication (0-5)
    s8 = 1
    f8 = []
    has_badges = bool(re.search(r"\[!\[.*\]\(.*\)\]\(.*\)", text)) or "img.shields.io" in text
    has_images = bool(re.search(r"!\[.*\]\(.*\)", text))
    has_tables = bool(re.search(r"\|.*\|.*\|", text))

    if has_badges:
        s8 += 1
    if has_images or has_diagram:
        s8 += 2
    else:
        f8.append("Consider adding UI screenshots, demo GIFs, or diagrams.")
    if has_tables:
        s8 += 1

    scores["visual_communication"] = min(5, s8)
    feedback["visual_communication"] = f8

    # 9. Trust & Completeness (0-5)
    s9 = 1
    f9 = []
    has_license = bool(re.search(r"(license|mit|apache|gpl)", text, re.I))
    has_tests = bool(re.search(r"(pytest|npm test|cargo test|make test|unittest|testing)", text, re.I))
    has_contrib = bool(re.search(r"(contributing|pull request|issue)", text, re.I))

    if has_license:
        s9 += 2
    else:
        f9.append("Missing explicit License reference.")
        critical_defects.append("Missing license reference.")

    if has_tests:
        s9 += 1
    else:
        f9.append("Document how to run the test suite to build confidence.")

    if has_contrib:
        s9 += 1

    scores["trust_and_completeness"] = min(5, s9)
    feedback["trust_and_completeness"] = f9

    # 10. Maintainability & Links (0-5)
    s10 = 5
    f10 = []
    broken_links = []
    if check_links:
        # Find relative markdown links: [text](path)
        for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text):
            target = m.group(2).split("#")[0]  # strip anchor
            if not target or target.startswith("http://") or target.startswith("https://") or target.startswith("mailto:"):
                continue
            target_path = (root_dir / target).resolve()
            if not target_path.exists():
                broken_links.append(target)

        if broken_links:
            s10 = max(0, 5 - len(broken_links) * 2)
            f10.append(f"Broken relative links detected: {', '.join(broken_links[:3])}.")
            if len(broken_links) > 2:
                critical_defects.append(f"{len(broken_links)} broken relative file links.")

    scores["maintainability"] = s10
    feedback["maintainability"] = f10

    # Calculate Total Score
    total_score = sum(scores.values())

    if total_score >= 45 and not critical_defects:
        grade = "A (Exemplary Production Grade)"
        passed = True
    elif total_score >= 38 and not critical_defects:
        grade = "B (High Quality)"
        passed = True
    elif total_score >= 30:
        grade = "C (Needs Polish)"
        passed = False
    else:
        grade = "F (Defective / Incomplete)"
        passed = False

    return {
        "file": str(readme_path),
        "total_score": total_score,
        "max_score": 50,
        "percentage": round((total_score / 50) * 100, 1),
        "grade": grade,
        "passed": passed,
        "line_count": line_count,
        "word_count": word_count,
        "scores": scores,
        "feedback": {k: v for k, v in feedback.items() if v},
        "critical_defects": critical_defects,
    }


def format_report(audit: dict, use_color: bool = True) -> str:
    if "error" in audit:
        return f"Error: {audit['error']}"

    bold = "\033[1m" if use_color else ""
    green = "\033[0;32m" if use_color else ""
    cyan = "\033[0;36m" if use_color else ""
    yellow = "\033[1;33m" if use_color else ""
    red = "\033[0;31m" if use_color else ""
    reset = "\033[0m" if use_color else ""

    lines = []
    lines.append("=" * 72)
    lines.append(f"        {bold}README 50-POINT QUALITY SCORECARD AUDIT{reset}")
    lines.append("=" * 72)
    lines.append(f"Target:      {cyan}{audit['file']}{reset}")
    lines.append(f"Metrics:     {audit['line_count']} lines · {audit['word_count']} words")

    score_color = green if audit["passed"] else (yellow if audit["total_score"] >= 30 else red)
    lines.append(f"Score:       {bold}{score_color}{audit['total_score']} / {audit['max_score']} ({audit['percentage']}%){reset} · Grade: {bold}{audit['grade']}{reset}")
    lines.append("-" * 72)
    lines.append(f"{'Dimension':<32} | {'Score':<8} | {'Status'}")
    lines.append("-" * 72)

    categories = [
        ("purpose_and_audience", "1. Purpose & Audience"),
        ("structure_and_navigation", "2. Structure & Navigation"),
        ("accuracy", "3. Accuracy & Cleanliness"),
        ("installation", "4. Installation Instructions"),
        ("usage", "5. Usage & Examples"),
        ("technical_explanation", "6. Technical & Architecture"),
        ("readability", "7. Readability & Code Tags"),
        ("visual_communication", "8. Visual Communication"),
        ("trust_and_completeness", "9. Trust & Completeness"),
        ("maintainability", "10. Maintainability & Links"),
    ]

    for key, label in categories:
        s = audit["scores"].get(key, 0)
        c = green if s >= 4 else (yellow if s >= 3 else red)
        status = "EXCELLENT" if s == 5 else ("GOOD" if s >= 4 else ("ADEQUATE" if s >= 3 else "POOR"))
        lines.append(f"{label:<32} | {c}{s}/5{reset}     | {c}{status}{reset}")

    lines.append("=" * 72)

    if audit["critical_defects"]:
        lines.append(f"\n{bold}{red}⛔ CRITICAL DEFECTS (Fix Immediately):{reset}")
        for cd in audit["critical_defects"]:
            lines.append(f"  • {red}{cd}{reset}")

    if audit["feedback"]:
        lines.append(f"\n{bold}{cyan}Prioritized Action Items:{reset}")
        idx = 1
        for cat, items in audit["feedback"].items():
            for item in items:
                lines.append(f"  {idx}. {item}")
                idx += 1

    lines.append("\n" + ("=" * 72))
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Audit GitHub README files against 50-point quality scorecard.")
    parser.add_argument("readme", nargs="?", default="README.md", help="Path to README.md (default: ./README.md)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON format")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI color codes")
    parser.add_argument("--no-link-check", action="store_true", help="Skip checking relative file links")
    parser.add_argument("--min-score", type=int, default=35, help="Minimum score to pass (default: 35)")

    args = parser.parse_args()

    readme_path = Path(args.readme).resolve()
    result = audit_readme(readme_path, check_links=not args.no_link_check)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        use_color = not args.no_color and sys.stdout.isatty()
        print(format_report(result, use_color=use_color))

    if "error" in result:
        sys.exit(1)

    sys.exit(0 if result["passed"] and result["total_score"] >= args.min_score else 1)


if __name__ == "__main__":
    main()
