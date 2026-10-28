#!/usr/bin/env python3
"""Sanzo Wada Color Engine: 348 historical palettes and 159 colors from A Dictionary of Color Combinations (1930s)."""

import argparse
import json
import math
import os
from pathlib import Path
import random
import sys

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
COLORS_JSON = DATA_DIR / "colors.json"

_DATA_CACHE = None


def load_data():
    """Load and index the 159 colors and 348 combinations."""
    global _DATA_CACHE
    if _DATA_CACHE is not None:
        return _DATA_CACHE

    if not COLORS_JSON.is_file():
        raise FileNotFoundError(f"Colors dataset not found: {COLORS_JSON}")

    with open(COLORS_JSON, "r", encoding="utf-8") as f:
        colors = json.load(f)

    # Build combination map (1 to 348)
    combinations = {}
    for i in range(1, 349):
        combinations[i] = []

    for c in colors:
        for combo_id in c.get("combinations", []):
            if combo_id in combinations:
                combinations[combo_id].append(c)

    _DATA_CACHE = {
        "colors": colors,
        "combinations": combinations,
    }
    return _DATA_CACHE


def get_combination(combo_id: int):
    """Retrieve color palette by combination ID (1 to 348)."""
    data = load_data()
    if combo_id not in data["combinations"] or not data["combinations"][combo_id]:
        raise ValueError(f"Combination #{combo_id} not found (valid range: 1 to 348)")
    return data["combinations"][combo_id]


def search_colors(query: str):
    """Search colors by name or hex code."""
    data = load_data()
    q = query.strip().lower()
    results = []
    for c in data["colors"]:
        if q in c["name"].lower() or q in c["hex"].lower():
            results.append(c)
    return results


def list_combinations(size: int = None, limit: int = 50, offset: int = 0):
    """List combinations filtered by size (2 = Duo, 3 = Trio, 4 = Quad)."""
    data = load_data()
    results = []
    for cid in range(1, 349):
        combo = data["combinations"][cid]
        if size is None or len(combo) == size:
            results.append({"id": cid, "size": len(combo), "colors": combo})

    return results[offset : offset + limit]


def get_random_combination(size: int = None):
    """Pick a random combination, optionally filtered by size."""
    data = load_data()
    valid_ids = []
    for cid in range(1, 349):
        combo = data["combinations"][cid]
        if size is None or len(combo) == size:
            valid_ids.append(cid)

    if not valid_ids:
        raise ValueError(f"No combinations found for size {size}")
    chosen_id = random.choice(valid_ids)
    return chosen_id, data["combinations"][chosen_id]


def relative_luminance(rgb):
    """Calculate WCAG 2.1 relative luminance for an [R, G, B] tuple."""
    r, g, b = [x / 255.0 for x in rgb]
    r_lin = r / 12.92 if r <= 0.04045 else math.pow((r + 0.055) / 1.055, 2.4)
    g_lin = g / 12.92 if g <= 0.04045 else math.pow((g + 0.055) / 1.055, 2.4)
    b_lin = b / 12.92 if b <= 0.04045 else math.pow((b + 0.055) / 1.055, 2.4)
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


def wcag_contrast_ratio(rgb1, rgb2):
    """Calculate WCAG contrast ratio between two [R, G, B] colors."""
    l1 = relative_luminance(rgb1)
    l2 = relative_luminance(rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def ansi_color_block(rgb, width=4):
    """Render a 24-bit TrueColor ANSI background block."""
    r, g, b = rgb
    return f"\033[48;2;{r};{g};{b}m{' ' * width}\033[0m"


def format_palette_card(combo_id: int):
    """Format an informative CLI card with TrueColor swatches and color values."""
    colors = get_combination(combo_id)
    size_label = {2: "Duo", 3: "Trio", 4: "Quad"}.get(len(colors), f"{len(colors)}-color")

    lines = [
        f"\033[1mSanzo Wada Combination #{combo_id}\033[0m ({size_label})",
        "─" * 58,
    ]

    # Visual swatch strip
    swatches = "".join(ansi_color_block(c["rgb"], width=8) for c in colors)
    lines.append(f"Palette: {swatches}")
    lines.append("")

    for i, c in enumerate(colors, 1):
        block = ansi_color_block(c["rgb"], width=3)
        cmyk_str = f"C:{c['cmyk'][0]} M:{c['cmyk'][1]} Y:{c['cmyk'][2]} K:{c['cmyk'][3]}"
        rgb_str = f"rgb({c['rgb'][0]}, {c['rgb'][1]}, {c['rgb'][2]})"
        lines.append(f"  {block}  \033[1m{c['hex']}\033[0m  {c['name']:<20}  {rgb_str:<18}  {cmyk_str}")

    lines.append("")
    lines.append("WCAG Contrast Matrix:")
    for i in range(len(colors)):
        for j in range(i + 1, len(colors)):
            ratio = wcag_contrast_ratio(colors[i]["rgb"], colors[j]["rgb"])
            rating = "AAA" if ratio >= 7.0 else ("AA" if ratio >= 4.5 else ("AA Large" if ratio >= 3.0 else "Fail"))
            block1 = ansi_color_block(colors[i]["rgb"], width=2)
            block2 = ansi_color_block(colors[j]["rgb"], width=2)
            lines.append(f"  {block1} vs {block2}  {colors[i]['name']} / {colors[j]['name']}: \033[1m{ratio:.2f}:1\033[0m ({rating})")

    lines.append("─" * 58)
    return "\n".join(lines)


def export_palette(combo_id: int, fmt: str = "css") -> str:
    """Export palette in CSS, Tailwind, SCSS, JSON, or SVG format."""
    colors = get_combination(combo_id)
    size_label = {2: "Duo", 3: "Trio", 4: "Quad"}.get(len(colors), "Palette")

    if fmt == "css":
        out = [
            f"/* Sanzo Wada #{combo_id} ({size_label}) */",
            ":root {",
        ]
        for i, c in enumerate(colors, 1):
            var_name = f"--wada-{combo_id}-color-{i}"
            slug = c["name"].lower().replace(" ", "-")
            out.append(f"  {var_name}: {c['hex']}; /* {c['name']} */")
            out.append(f"  --color-{slug}: {c['hex']};")
        out.append("}")
        return "\n".join(out)

    elif fmt == "tailwind":
        palette_obj = {}
        for i, c in enumerate(colors, 1):
            slug = c["name"].lower().replace(" ", "-")
            palette_obj[slug] = c["hex"]
        data = {f"wada-{combo_id}": palette_obj}
        return json.dumps(data, indent=2)

    elif fmt == "scss":
        out = [f"// Sanzo Wada #{combo_id} ({size_label})"]
        for i, c in enumerate(colors, 1):
            slug = c["name"].lower().replace(" ", "-")
            out.append(f"${slug}: {c['hex']};")
        return "\n".join(out)

    elif fmt == "json":
        data = {
            "combination": combo_id,
            "type": size_label,
            "colors": colors,
        }
        return json.dumps(data, indent=2)

    elif fmt == "svg":
        width = len(colors) * 120
        height = 140
        rects = []
        texts = []
        for i, c in enumerate(colors):
            x = i * 120
            rects.append(f'  <rect x="{x}" y="0" width="120" height="90" fill="{c["hex"]}"/>')
            texts.append(f'  <text x="{x + 60}" y="110" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="#333">{c["hex"]}</text>')
            texts.append(f'  <text x="{x + 60}" y="128" font-family="sans-serif" font-size="10" text-anchor="middle" fill="#666">{c["name"]}</text>')

        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            f'  <!-- Sanzo Wada Combination #{combo_id} -->',
            "\n".join(rects),
            "\n".join(texts),
            "</svg>",
        ]
        return "\n".join(svg)

    else:
        raise ValueError(f"Unknown format: {fmt} (valid: css, tailwind, scss, json, svg)")


def main():
    parser = argparse.ArgumentParser(description="Sanzo Wada Color Engine: 348 historical palettes from A Dictionary of Color Combinations.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # combo
    sp_combo = subparsers.add_parser("combo", help="Display palette by ID (1-348)")
    sp_combo.add_argument("id", type=int, help="Combination ID (1 to 348)")

    # search
    sp_search = subparsers.add_parser("search", help="Search colors by name or hex")
    sp_search.add_argument("query", help="Color name substring or hex code")

    # list
    sp_list = subparsers.add_parser("list", help="List combinations filtered by size")
    sp_list.add_argument("--size", type=int, choices=[2, 3, 4], help="Filter by size (2=Duo, 3=Trio, 4=Quad)")
    sp_list.add_argument("--limit", type=int, default=20, help="Max results")
    sp_list.add_argument("--offset", type=int, default=0, help="Offset")

    # random
    sp_rand = subparsers.add_parser("random", help="Pick a random combination")
    sp_rand.add_argument("--size", type=int, choices=[2, 3, 4], help="Filter by size")

    # export
    sp_exp = subparsers.add_parser("export", help="Export combination tokens")
    sp_exp.add_argument("id", type=int, help="Combination ID (1 to 348)")
    sp_exp.add_argument("--format", choices=["css", "tailwind", "scss", "json", "svg"], default="css", help="Export format")

    # contrast
    sp_con = subparsers.add_parser("contrast", help="Compute WCAG contrast ratios")
    sp_con.add_argument("id", type=int, help="Combination ID (1 to 348)")

    args = parser.parse_args()

    try:
        if args.command == "combo":
            print(format_palette_card(args.id))

        elif args.command == "search":
            results = search_colors(args.query)
            if not results:
                print(f"No colors found matching '{args.query}'")
            else:
                print(f"Found {len(results)} color(s) matching '{args.query}':\n")
                for c in results:
                    block = ansi_color_block(c["rgb"], width=3)
                    combos_str = ", ".join(f"#{cid}" for cid in c.get("combinations", [])[:6])
                    if len(c.get("combinations", [])) > 6:
                        combos_str += f" (+{len(c['combinations']) - 6} more)"
                    print(f"  {block}  \033[1m{c['hex']}\033[0m  {c['name']:<22}  rgb{tuple(c['rgb'])}  Used in: {combos_str}")

        elif args.command == "list":
            combos = list_combinations(size=args.size, limit=args.limit, offset=args.offset)
            title = f"Sanzo Wada Palettes (Size: {args.size or 'All'}, Showing {len(combos)})"
            print(f"\033[1m{title}\033[0m\n" + "─" * 60)
            for item in combos:
                cid = item["id"]
                colors = item["colors"]
                swatches = "".join(ansi_color_block(c["rgb"], width=4) for c in colors)
                names = ", ".join(c["name"] for c in colors)
                print(f"  #{cid:<3}  {swatches}  {names}")

        elif args.command == "random":
            cid, colors = get_random_combination(size=args.size)
            print(format_palette_card(cid))

        elif args.command == "export":
            print(export_palette(args.id, fmt=args.format))

        elif args.command == "contrast":
            colors = get_combination(args.id)
            print(f"\033[1mWCAG Contrast Matrix for Combination #{args.id}\033[0m\n" + "─" * 50)
            for i in range(len(colors)):
                for j in range(i + 1, len(colors)):
                    r = wcag_contrast_ratio(colors[i]["rgb"], colors[j]["rgb"])
                    rating = "AAA (7.0+)" if r >= 7.0 else ("AA (4.5+)" if r >= 4.5 else ("AA Large (3.0+)" if r >= 3.0 else "Fail (<3.0)"))
                    b1 = ansi_color_block(colors[i]["rgb"], width=2)
                    b2 = ansi_color_block(colors[j]["rgb"], width=2)
                    print(f"  {b1} vs {b2}  {colors[i]['name']} vs {colors[j]['name']}: {r:.2f}:1  [{rating}]")

    except Exception as exc:
        print(f"wada error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

