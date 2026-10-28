#!/usr/bin/env python3
"""Ponytail Debt Ledger Scanner.

Scans the codebase for `shortcut:` (or legacy `ponytail:`) comments
that record deliberate shortcuts, ceilings, and upgrade paths.
"""
import argparse
import json
import os
import re
import sys

DEFAULT_IGNORE_DIRS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache",
    "dist", "build", ".court", ".arena", ".next", ".astro", ".turbo"
}

MARKER_PATTERN = re.compile(
    r'(?:#|//|/\*|--|<!--)\s*(?:shortcut|ponytail):\s*(.*?)(?:\*/|-->)?$',
    re.IGNORECASE
)


def parse_shortcut_text(text):
    text = text.strip()
    parts = [p.strip() for p in text.split(",") if p.strip()]
    if not parts:
        return {"summary": text, "ceiling": "unspecified", "upgrade": "unspecified", "no_trigger": True}

    summary = parts[0]
    ceiling = "unspecified"
    upgrade = "unspecified"
    no_trigger = True

    for p in parts[1:]:
        p_lower = p.lower()
        if p_lower.startswith("ceiling:"):
            ceiling = p[8:].strip()
        elif p_lower.startswith("upgrade:"):
            upgrade = p[8:].strip()
            no_trigger = False
        elif p_lower.startswith("when:"):
            upgrade = p[5:].strip()
            no_trigger = False
        else:
            if upgrade == "unspecified":
                upgrade = p
                no_trigger = False
            elif ceiling == "unspecified":
                ceiling = p

    return {
        "summary": summary,
        "ceiling": ceiling,
        "upgrade": upgrade,
        "no_trigger": no_trigger
    }


def scan_directory(root_dir, marker="shortcut|ponytail"):
    pattern = re.compile(
        rf'(?:#|//|/\*|--|<!--)\s*(?:{marker}):\s*(.*?)(?:\*/|-->)?$',
        re.IGNORECASE
    )
    results = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in DEFAULT_IGNORE_DIRS and not d.startswith(".")]
        for fname in filenames:
            if fname.endswith((".pyc", ".png", ".jpg", ".zip", ".tar.gz", ".wasm", ".bin")):
                continue
            fpath = os.path.join(dirpath, fname)
            rel_path = os.path.relpath(fpath, root_dir)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
                    for line_no, line in enumerate(fh, start=1):
                        m = pattern.search(line)
                        if m:
                            parsed = parse_shortcut_text(m.group(1))
                            results.append({
                                "file": rel_path,
                                "line": line_no,
                                "raw": m.group(1).strip(),
                                **parsed
                            })
            except Exception:
                continue

    return results


def format_ledger(hits):
    if not hits:
        return "No shortcut debt. Clean ledger."

    lines = ["## Ponytail Debt Ledger", ""]
    grouped = {}
    for h in hits:
        grouped.setdefault(h["file"], []).append(h)

    no_trigger_count = 0
    for file_path, items in grouped.items():
        lines.append(f"### `{file_path}`")
        for it in items:
            rot_flag = " [NO-TRIGGER - Rot Risk]" if it["no_trigger"] else ""
            if it["no_trigger"]:
                no_trigger_count += 1
            lines.append(
                f"- **L{it['line']}**: {it['summary']}. "
                f"Ceiling: *{it['ceiling']}*. Upgrade: *{it['upgrade']}*.{rot_flag}"
            )
        lines.append("")

    lines.append(f"**Total:** {len(hits)} markers ({no_trigger_count} with no upgrade trigger).")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Scan codebase for shortcut debt.")
    parser.add_argument("--path", "-p", default=".", help="Root directory to scan (default: .)")
    parser.add_argument("--marker", "-m", default="shortcut|ponytail", help="Custom marker keyword")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--out", "-o", help="Optional output markdown file path")

    args = parser.parse_args()
    hits = scan_directory(args.path, marker=args.marker)

    if args.json:
        output = json.dumps(hits, indent=2)
    else:
        output = format_ledger(hits)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(output + "\n")
        print(f"Ledger written to {args.out}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())

