#!/usr/bin/env python3
"""Design Systems Registry CLI - Curated 67 Design System Skills & Tokens.

Zero-dependency Python tool for:
  1. Listing and searching all 67 design system themes.
  2. Extracting design tokens (colors, typography, spacing, radius).
  3. Exporting tokens directly to CSS custom properties.
  4. Inspecting AI agent guidelines and accessibility constraints.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.join(HERE, "..")
RESOURCES_DIR = os.path.join(SKILL_ROOT, "resources")
INDEX_PATH = os.path.join(RESOURCES_DIR, "index.json")
SKILLS_DIR = os.path.join(RESOURCES_DIR, "skills")


def load_index():
    if not os.path.isfile(INDEX_PATH):
        print(f"Error: Registry index not found at {INDEX_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_frontmatter(content):
    if not content.startswith("---\n"):
        return {}, content
    end_idx = content.find("\n---\n", 4)
    if end_idx == -1:
        return {}, content
    fm_text = content[4:end_idx]
    body = content[end_idx + 5:]
    
    # Simple line-based YAML parser for flat/nested keys
    data = {}
    current_section = None
    sub_data = {}

    for line in fm_text.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()

        if indent == 0 and ":" in stripped:
            if current_section and sub_data:
                data[current_section] = sub_data
                sub_data = {}
            k, v = stripped.split(":", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if v:
                data[k] = v
                current_section = None
            else:
                current_section = k
        elif indent > 0 and current_section and ":" in stripped:
            k, v = stripped.split(":", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            sub_data[k] = v

    if current_section and sub_data:
        data[current_section] = sub_data

    return data, body


def get_skill_files(slug):
    index = load_index()
    if slug not in index:
        # Try case-insensitive lookup
        matches = [k for k in index if k.lower() == slug.lower()]
        if matches:
            slug = matches[0]
        else:
            return None, None

    skill_md = os.path.join(SKILLS_DIR, slug, "SKILL.md")
    design_md = os.path.join(SKILLS_DIR, slug, "DESIGN.md")

    if not os.path.isfile(skill_md):
        skill_md = None
    if not os.path.isfile(design_md):
        design_md = None

    return skill_md, design_md


# --- COMMAND: list ---
def cmd_list(args):
    index = load_index()
    items = []

    for slug, info in sorted(index.items()):
        skill_file = os.path.join(SKILLS_DIR, slug, "SKILL.md")
        desc = ""
        if os.path.isfile(skill_file):
            with open(skill_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            fm, _ = parse_frontmatter(content)
            desc = fm.get("description", "")
            if not desc:
                # Look for summary in text
                match = re.search(r"##\s+Overview\s*\n+([^\n#]+)", content)
                if match:
                    desc = match.group(1).strip()
        items.append({
            "slug": slug,
            "name": info.get("name", slug.title()),
            "description": desc
        })

    if args.json:
        print(json.dumps(items, indent=2))
    else:
        print("=" * 76)
        print("           AWESOME DESIGN SYSTEMS REGISTRY (67 THEMES)")
        print("=" * 76)
        print(f"{'Slug':<18} | {'Name':<18} | {'Description'}")
        print("-" * 76)
        for it in items:
            desc_short = (it["description"][:36] + "...") if len(it["description"]) > 36 else it["description"]
            print(f"{it['slug']:<18} | {it['name']:<18} | {desc_short}")
        print("-" * 76)
        print(f"Total Design Systems: {len(items)}")
        print("=" * 76)


# --- COMMAND: search ---
def cmd_search(args):
    index = load_index()
    query = args.query.lower()
    results = []

    for slug, info in index.items():
        score = 0
        match_reasons = []

        if query in slug.lower():
            score += 10
            match_reasons.append("slug")
        if query in info.get("name", "").lower():
            score += 10
            match_reasons.append("name")

        skill_file = os.path.join(SKILLS_DIR, slug, "SKILL.md")
        design_file = os.path.join(SKILLS_DIR, slug, "DESIGN.md")

        content = ""
        if os.path.isfile(skill_file):
            with open(skill_file, "r", encoding="utf-8", errors="ignore") as f:
                content += f.read()
        if os.path.isfile(design_file):
            with open(design_file, "r", encoding="utf-8", errors="ignore") as f:
                content += f.read()

        if query in content.lower():
            score += 5
            match_reasons.append("content")

        if score > 0:
            fm, _ = parse_frontmatter(content)
            results.append({
                "slug": slug,
                "name": info.get("name", slug.title()),
                "score": score,
                "reasons": match_reasons,
                "description": fm.get("description", "")
            })

    results.sort(key=lambda x: x["score"], reverse=True)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print("=" * 72)
        print(f"       SEARCH RESULTS FOR: '{args.query}' ({len(results)} found)")
        print("=" * 72)
        if not results:
            print("  No matching design systems found.")
        for r in results:
            print(f"• {r['name']} [{r['slug']}]: {r['description']}")
        print("=" * 72)


# --- COMMAND: tokens ---
def cmd_tokens(args):
    skill_file, design_file = get_skill_files(args.slug)
    if not design_file:
        print(f"Error: Design system '{args.slug}' not found.", file=sys.stderr)
        sys.exit(1)

    with open(design_file, "r", encoding="utf-8") as f:
        content = f.read()

    fm, body = parse_frontmatter(content)

    if args.json:
        print(json.dumps(fm, indent=2))
    else:
        print("=" * 64)
        print(f"         DESIGN TOKENS: {fm.get('name', args.slug.title())}")
        print("=" * 64)
        for section, values in fm.items():
            if isinstance(values, dict):
                print(f"\n[{section.upper()}]")
                for k, v in values.items():
                    print(f"  {k:<16}: {v}")
            else:
                print(f"{section:<16}: {values}")
        print("=" * 64)


# --- COMMAND: export-css ---
def cmd_export_css(args):
    skill_file, design_file = get_skill_files(args.slug)
    if not design_file:
        print(f"Error: Design system '{args.slug}' not found.", file=sys.stderr)
        sys.exit(1)

    with open(design_file, "r", encoding="utf-8") as f:
        content = f.read()

    fm, _ = parse_frontmatter(content)
    css_lines = [
        f"/* Generated from Design System: {fm.get('name', args.slug.title())} */",
        ":root {"
    ]

    # Colors
    colors = fm.get("colors", {})
    if isinstance(colors, dict):
        css_lines.append("  /* Colors */")
        for k, v in colors.items():
            css_lines.append(f"  --color-{k}: {v};")

    # Typography
    typo = fm.get("typography", {})
    if isinstance(typo, dict):
        css_lines.append("\n  /* Typography */")
        for k, v in typo.items():
            css_lines.append(f"  --font-{k}: {v};")

    # Rounded
    rounded = fm.get("rounded", {})
    if isinstance(rounded, dict):
        css_lines.append("\n  /* Border Radius */")
        for k, v in rounded.items():
            css_lines.append(f"  --radius-{k}: {v};")

    # Spacing
    spacing = fm.get("spacing", {})
    if isinstance(spacing, dict):
        css_lines.append("\n  /* Spacing */")
        for k, v in spacing.items():
            css_lines.append(f"  --space-{k}: {v};")

    css_lines.append("}\n")
    css_out = "\n".join(css_lines)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(css_out)
        print(f"[OK] Exported CSS tokens for '{args.slug}' to {args.output}")
    else:
        print(css_out)


# --- COMMAND: inspect ---
def cmd_inspect(args):
    skill_file, design_file = get_skill_files(args.slug)
    if not skill_file:
        print(f"Error: Design system '{args.slug}' not found.", file=sys.stderr)
        sys.exit(1)

    with open(skill_file, "r", encoding="utf-8") as f:
        content = f.read()

    print(content)


def main():
    parser = argparse.ArgumentParser(description="Awesome Design Systems Registry CLI")
    sub = parser.add_subparsers(dest="subcommand", help="Available subcommands")

    # list
    p_list = sub.add_parser("list", help="List all 67 design systems")
    p_list.add_argument("--json", action="store_true", help="Output JSON")

    # search
    p_search = sub.add_parser("search", help="Search design systems by keyword")
    p_search.add_argument("query", help="Keyword or style search")
    p_search.add_argument("--json", action="store_true", help="Output JSON")

    # tokens
    p_tokens = sub.add_parser("tokens", help="View tokens for a specific design system")
    p_tokens.add_argument("slug", help="Theme slug (e.g. glassmorphism, bento, brutalism)")
    p_tokens.add_argument("--json", action="store_true", help="Output JSON")

    # export-css
    p_css = sub.add_parser("export-css", help="Export tokens to CSS custom properties")
    p_css.add_argument("slug", help="Theme slug")
    p_css.add_argument("--output", help="Output CSS file path")

    # inspect
    p_inspect = sub.add_parser("inspect", help="Inspect SKILL.md guidelines for a theme")
    p_inspect.add_argument("slug", help="Theme slug")

    args = parser.parse_args()
    if not args.subcommand:
        parser.print_help()
        sys.exit(0)

    handlers = {
        "list": cmd_list,
        "search": cmd_search,
        "tokens": cmd_tokens,
        "export-css": cmd_export_css,
        "inspect": cmd_inspect
    }
    handlers[args.subcommand](args)


if __name__ == "__main__":
    main()
