#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ThreeUI Component & Shader Engine.

CLI tool for searching, inspecting, and extracting Three.js, WebGL, and shader
components from the ThreeUI catalog (DesignCode / Meng To).

Usage:
    python3 threeui.py search "liquid"
    python3 threeui.py list [--category backgrounds]
    python3 threeui.py categories
    python3 threeui.py info liquid-form
    python3 threeui.py code liquid-form
    python3 threeui.py export liquid-form --output-dir ./src/components
"""

import argparse
import io
import json
import os
import re
import shutil
import sys
from pathlib import Path

# Force UTF-8 encoding
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
RESOURCES_DIR = ROOT_DIR / "resources"
CATALOG_FILE = RESOURCES_DIR / "catalog.json"
COMPONENTS_DIR = RESOURCES_DIR / "components"


def load_catalog():
    """Load the full ThreeUI component catalog."""
    if not CATALOG_FILE.exists():
        print(f"Error: Catalog file not found at {CATALOG_FILE}", file=sys.stderr)
        sys.exit(1)
    with CATALOG_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def tokenize(text):
    """Normalize and tokenize text into unique words."""
    if not text:
        return []
    return re.findall(r"\b[a-z0-9_-]+\b", str(text).lower())


def score_component(comp, query_tokens):
    """Calculate matching score for a component against query tokens."""
    if not query_tokens:
        return 1.0

    score = 0.0
    id_tokens = tokenize(comp.get("id", ""))
    label_tokens = tokenize(comp.get("label", ""))
    cat_tokens = tokenize(comp.get("category", ""))
    desc_tokens = tokenize(comp.get("description", ""))
    tags = [t.lower() for t in comp.get("tags", [])]
    tag_tokens = []
    for t in tags:
        tag_tokens.extend(tokenize(t))

    for token in query_tokens:
        # Exact ID match
        if token == comp.get("id", "").lower():
            score += 15.0
        elif token in comp.get("id", "").lower():
            score += 8.0

        # Exact label match
        if token in label_tokens:
            score += 10.0
        elif any(token in t for t in label_tokens):
            score += 5.0

        # Tag matches
        if token in tags:
            score += 7.0
        elif token in tag_tokens:
            score += 4.0

        # Category match
        if token in cat_tokens:
            score += 5.0

        # Description matches
        if token in desc_tokens:
            score += 2.0

    return score


def search_components(query, category=None, limit=10):
    """Search components with keyword scoring."""
    catalog = load_catalog()
    query_tokens = tokenize(query)

    scored = []
    for comp in catalog:
        if category:
            cat_norm = category.lower().replace("-", " ")
            comp_cat = comp.get("category", "").lower()
            if cat_norm not in comp_cat and comp_cat not in cat_norm:
                continue

        score = score_component(comp, query_tokens)
        if score > 0:
            scored.append((score, comp))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [comp for _, comp in scored[:limit]]


def list_categories():
    """List all categories and counts."""
    catalog = load_catalog()
    counts = {}
    for comp in catalog:
        cat = comp.get("category", "Uncategorized")
        counts[cat] = counts.get(cat, 0) + 1
    return counts


def find_component(comp_id):
    """Find a single component by ID or slug."""
    catalog = load_catalog()
    norm_id = comp_id.lower().strip()
    for comp in catalog:
        if comp.get("id", "").lower() == norm_id:
            return comp
    # Try fuzzy or partial match
    for comp in catalog:
        if norm_id in comp.get("id", "").lower():
            return comp
    return None


def get_component_files(comp):
    """Find all source files associated with a component."""
    comp_path = comp.get("componentPath", "")
    if not comp_path:
        return []

    target_base = COMPONENTS_DIR / comp_path
    parent_dir = target_base.parent

    files = []
    if target_base.is_file():
        files.append(target_base)
    elif target_base.with_suffix(".tsx").is_file():
        files.append(target_base.with_suffix(".tsx"))
    elif target_base.with_suffix(".ts").is_file():
        files.append(target_base.with_suffix(".ts"))

    # Also grab sister shader/css/glsl files in the same directory
    if parent_dir.is_dir() and parent_dir != COMPONENTS_DIR:
        for item in sorted(parent_dir.glob("*")):
            if item.is_file() and item.suffix.lower() in (".ts", ".tsx", ".js", ".jsx", ".glsl", ".css", ".html"):
                if item not in files:
                    files.append(item)

    return files


def cmd_search(args):
    """Handle 'search' command."""
    results = search_components(args.query, category=args.category, limit=args.limit)
    if args.json:
        print(json.dumps(results, indent=2))
        return

    if not results:
        print(f"No ThreeUI components found matching '{args.query}'.")
        return

    print(f"\n[SEARCH] ThreeUI Search Results for '{args.query}':\n")
    print(f"{'ID':<30} | {'Category':<16} | {'Label':<24} | {'Runtime'}")
    print("-" * 88)
    for c in results:
        cid = c.get("id", "")
        cat = c.get("category", "")
        lbl = c.get("label", "")
        rt = c.get("runtime", "")[:24]
        print(f"{cid:<30} | {cat:<16} | {lbl:<24} | {rt}")

    print("\n[TIP] Tip: Run `python3 scripts/threeui.py info <id>` for controls and props.")
    print("        Run `python3 scripts/threeui.py code <id>` to retrieve source code.")


def cmd_list(args):
    """Handle 'list' command."""
    catalog = load_catalog()
    if args.category:
        cat_norm = args.category.lower().replace("-", " ")
        filtered = [c for c in catalog if cat_norm in c.get("category", "").lower()]
    else:
        filtered = catalog

    if args.json:
        print(json.dumps(filtered, indent=2))
        return

    by_category = {}
    for c in filtered:
        cat = c.get("category", "General")
        by_category.setdefault(cat, []).append(c)

    for cat, items in sorted(by_category.items()):
        print(f"\n[DIR] {cat} ({len(items)} components):")
        print("-" * 72)
        for c in sorted(items, key=lambda x: x.get("id", "")):
            desc = c.get("description", "")
            if len(desc) > 60:
                desc = desc[:57] + "..."
            print(f"  • {c.get('id', ''):<28} - {c.get('label', ''):<20} | {desc}")


def cmd_categories(args):
    """Handle 'categories' command."""
    cats = list_categories()
    if args.json:
        print(json.dumps(cats, indent=2))
        return

    total = sum(cats.values())
    print("\n[EXPORT] ThreeUI Component Categories:")
    print("=" * 48)
    for cat, count in sorted(cats.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {cat:<24} : {count:>3} components")
    print("-" * 48)
    print(f"  Total Components: {total}\n")


def cmd_info(args):
    """Handle 'info' command."""
    comp = find_component(args.id)
    if not comp:
        print(f"Error: Component '{args.id}' not found in catalog.", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(comp, indent=2))
        return

    print("=" * 72)
    print(f"  {comp.get('label', '')} ({comp.get('id', '')})")
    print("=" * 72)
    print(f"  Category:    {comp.get('category', '')}")
    print(f"  Runtime:     {comp.get('runtime', '')}")
    print(f"  Export Name: {comp.get('exportName', '')}")
    print(f"  Path:        {comp.get('componentPath', '')}")
    print(f"  Description: {comp.get('description', '')}")

    tags = comp.get("tags", [])
    if tags:
        print(f"  Tags:        {', '.join(tags)}")

    controls = comp.get("controls", [])
    if controls:
        print("\n[DIALS]  Controls & Uniforms:")
        print("  " + "-" * 68)
        for ctrl in controls:
            kind = ctrl.get("kind", "range")
            key = ctrl.get("key", "")
            lbl = ctrl.get("label", key)
            dflt = ctrl.get("default", "")
            if kind == "range":
                cmin = ctrl.get("min", 0)
                cmax = ctrl.get("max", 1)
                cstep = ctrl.get("step", 0.1)
                print(f"  • {key:<20} ({kind:<6}) : Default: {dflt} (Min: {cmin}, Max: {cmax}, Step: {cstep})")
            elif kind in ("checkpoint", "choice"):
                opts = [o.get("value", "") for o in ctrl.get("options", [])]
                print(f"  • {key:<20} ({kind:<10}) : Default: {dflt} | Options: {', '.join(opts[:6])}")
            else:
                print(f"  • {key:<20} ({kind:<6}) : Default: {dflt}")

    variants = comp.get("variants", [])
    if variants:
        print(f"\n[STYLE] Predefined Variants ({len(variants)}):")
        print("  " + "-" * 68)
        for v in variants:
            print(f"  • {v.get('id', ''):<20} : {v.get('label', '')} - {v.get('description', '')[:50]}")

    files = get_component_files(comp)
    if files:
        print("\n[FILE] Source Files:")
        print("  " + "-" * 68)
        for f in files:
            rel = f.relative_to(ROOT_DIR)
            print(f"  • {rel}")

    print("\n[TIP] Run `python3 scripts/threeui.py code " + comp.get("id", "") + "` to view full source code.")


def cmd_code(args):
    """Handle 'code' command."""
    comp = find_component(args.id)
    if not comp:
        print(f"Error: Component '{args.id}' not found.", file=sys.stderr)
        sys.exit(1)

    files = get_component_files(comp)
    if not files:
        print(f"Error: No source files located for component '{args.id}'.", file=sys.stderr)
        sys.exit(1)

    if args.json:
        payload = {}
        for f in files:
            payload[f.name] = f.read_text(encoding="utf-8", errors="replace")
        print(json.dumps(payload, indent=2))
        return

    for f in files:
        print("=" * 80)
        print(f"FILE: {f.name} ({f.stat().st_size} bytes)")
        print("=" * 80)
        print(f.read_text(encoding="utf-8", errors="replace"))
        print("\n")


def cmd_export(args):
    """Handle 'export' command."""
    comp = find_component(args.id)
    if not comp:
        print(f"Error: Component '{args.id}' not found.", file=sys.stderr)
        sys.exit(1)

    files = get_component_files(comp)
    if not files:
        print(f"Error: No source files found for '{args.id}'.", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    copied = []
    for f in files:
        dest = out_dir / f.name
        shutil.copy2(f, dest)
        copied.append(str(dest))

    if args.json:
        print(json.dumps({"status": "success", "component": comp.get("id"), "files": copied}, indent=2))
    else:
        print(f"[PASS] Successfully exported {len(copied)} files for '{comp.get('label')}' to {out_dir}:")
        for p in copied:
            print(f"  • {p}")


def main():
    parser = argparse.ArgumentParser(description="ThreeUI 3D & WebGL Component Engine")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # search
    p_search = subparsers.add_parser("search", help="Search 3D components and shaders")
    p_search.add_argument("query", help="Keyword query (e.g. liquid, wave, button, galaxy)")
    p_search.add_argument("-c", "--category", help="Filter by category")
    p_search.add_argument("-n", "--limit", type=int, default=10, help="Max results (default: 10)")
    p_search.add_argument("--json", action="store_true", help="Output JSON")
    p_search.set_defaults(func=cmd_search)

    # list
    p_list = subparsers.add_parser("list", help="List components")
    p_list.add_argument("-c", "--category", help="Filter by category")
    p_list.add_argument("--json", action="store_true", help="Output JSON")
    p_list.set_defaults(func=cmd_list)

    # categories
    p_cats = subparsers.add_parser("categories", help="List all categories and counts")
    p_cats.add_argument("--json", action="store_true", help="Output JSON")
    p_cats.set_defaults(func=cmd_categories)

    # info
    p_info = subparsers.add_parser("info", help="Get component details, controls, and uniforms")
    p_info.add_argument("id", help="Component ID (e.g. liquid-form, spark-badge)")
    p_info.add_argument("--json", action="store_true", help="Output JSON")
    p_info.set_defaults(func=cmd_info)

    # code
    p_code = subparsers.add_parser("code", help="Dump component implementation source and shaders")
    p_code.add_argument("id", help="Component ID")
    p_code.add_argument("--json", action="store_true", help="Output JSON with filenames as keys")
    p_code.set_defaults(func=cmd_code)

    # export
    p_export = subparsers.add_parser("export", help="Export component source files to a directory")
    p_export.add_argument("id", help="Component ID")
    p_export.add_argument("-o", "--output-dir", required=True, help="Target directory")
    p_export.add_argument("--json", action="store_true", help="Output JSON")
    p_export.set_defaults(func=cmd_export)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
