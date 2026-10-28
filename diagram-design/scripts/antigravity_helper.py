#!/usr/bin/env python3
"""Google Antigravity IDE Helper for Diagram Design.

Provides unified CLI utilities for diagram generation, validation, conversion,
standalone SVG export, and Antigravity artifact integration.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
ASSETS_DIR = SKILL_ROOT / "assets"
SCRIPTS_DIR = SKILL_ROOT / "scripts"

THEMES = {
    "default-light": {
        "paper": "#f5f5f5",
        "paper-2": "#ffffff",
        "ink": "#2d3142",
        "muted": "#4f5d75",
        "accent": "#bf4520",
        "line": "#bfc0c0",
    },
    "default-dark": {
        "paper": "#1a1b26",
        "paper-2": "#24283b",
        "ink": "#c0caf5",
        "muted": "#7982a9",
        "accent": "#ff9e64",
        "line": "#414868",
    },
    "antigravity-dark": {
        "paper": "#13141a",
        "paper-2": "#1e1f29",
        "ink": "#f1f3f5",
        "muted": "#9aa0a6",
        "accent": "#ff7e33",
        "line": "#2e303d",
    },
    "antigravity-light": {
        "paper": "#ffffff",
        "paper-2": "#f8f9fa",
        "ink": "#202124",
        "muted": "#5f6368",
        "accent": "#bf4520",
        "line": "#dadce0",
    },
}


def run_self_check(file_path: Path, offline: bool = False) -> tuple[bool, str]:
    """Runs self_check.py against the specified HTML diagram."""
    cmd = [sys.executable, "-B", str(SCRIPTS_DIR / "self_check.py")]
    if offline:
        cmd.append("--offline")
    cmd.append(str(file_path))

    proc = subprocess.run(cmd, capture_output=True, text=True)
    success = proc.returncode == 0
    output = proc.stdout.strip() if success else (proc.stderr.strip() or proc.stdout.strip())
    return success, output


def extract_ir(input_path: Path) -> tuple[str, str]:
    """Extracts structured IR from .drawio, .mmd/.mermaid, or .excalidraw files."""
    suffix = input_path.suffix.lower()
    if suffix in (".mmd", ".mermaid"):
        script = SCRIPTS_DIR / "mermaid_extract.py"
        fmt = "mermaid"
    elif suffix in (".drawio", ".xml") or (suffix == ".png" and "drawio" in input_path.name.lower()):
        script = SCRIPTS_DIR / "drawio_extract.py"
        fmt = "drawio"
    elif suffix in (".excalidraw",) or (suffix == ".json" and "excalidraw" in input_path.name.lower()):
        script = SCRIPTS_DIR / "excalidraw_extract.py"
        fmt = "excalidraw"
    else:
        # Default try mermaid if text
        script = SCRIPTS_DIR / "mermaid_extract.py"
        fmt = "auto-mermaid"

    proc = subprocess.run([sys.executable, "-B", str(script), str(input_path)], capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"Extractor failed ({fmt}): {proc.stderr or proc.stdout}")
    return fmt, proc.stdout


def export_svg_file(html_path: Path, svg_path: Path | None = None) -> Path:
    """Exports standalone SVG from diagram HTML file."""
    if svg_path is None:
        svg_path = html_path.with_suffix(".svg")
    cmd = [sys.executable, "-B", str(SCRIPTS_DIR / "export_svg.py"), str(html_path), str(svg_path)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"SVG export failed: {proc.stderr or proc.stdout}")
    return svg_path


def apply_theme_tokens(content: str, theme_name: str) -> str:
    """Replaces CSS custom properties with theme tokens."""
    if theme_name not in THEMES:
        return content
    tokens = THEMES[theme_name]
    for key, val in tokens.items():
        pattern = rf"(--color-{key}\s*:\s*)([^;]+);"
        content = re.sub(pattern, rf"\g<1>{val};", content)
    return content


def scaffold_diagram(
    diagram_type: str,
    output_path: Path,
    theme: str = "default-light",
    title: str = "Architecture Diagram",
) -> Path:
    """Scaffolds a new diagram HTML file based on template or type example."""
    # Look for example file
    example_file = ASSETS_DIR / f"example-{diagram_type}.html"
    template_file = ASSETS_DIR / "template.html"

    if example_file.exists():
        content = example_file.read_text(encoding="utf-8")
    elif template_file.exists():
        content = template_file.read_text(encoding="utf-8")
    else:
        raise FileNotFoundError(f"Neither {example_file} nor {template_file} exists.")

    if title:
        content = re.sub(r"<title[^>]*>.*?</title>", f"<title id=\"[diagram-slug]-title\">{title}</title>", content, count=1)
        content = re.sub(r"<h1[^>]*>.*?</h1>", f"<h1>{title}</h1>", content, count=1)

    content = apply_theme_tokens(content, theme)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Antigravity IDE Diagram Design Helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # validate
    val_p = subparsers.add_parser("validate", help="Validate a diagram HTML file using self_check.py")
    val_p.add_argument("file", type=Path, help="Path to diagram HTML file")
    val_p.add_argument("--offline", action="store_true", help="Reject Google Fonts links for pure offline mode")

    # scaffold
    scaf_p = subparsers.add_parser("scaffold", help="Scaffold a new diagram HTML file")
    scaf_p.add_argument("type", type=str, help="Diagram type (architecture, flowchart, sequence, etc.)")
    scaf_p.add_argument("out", type=Path, help="Output HTML file path")
    scaf_p.add_argument("--theme", choices=list(THEMES.keys()), default="default-light", help="Theme palette")
    scaf_p.add_argument("--title", type=str, default="Antigravity Diagram", help="Diagram title")

    # convert
    conv_p = subparsers.add_parser("convert", help="Extract structured IR from .drawio, .mmd, or .excalidraw")
    conv_p.add_argument("input", type=Path, help="Input source file (.drawio, .mmd, .excalidraw)")
    conv_p.add_argument("--out", type=Path, default=None, help="Optional output markdown file path")

    # export-svg
    svg_p = subparsers.add_parser("export-svg", help="Export standalone SVG from diagram HTML")
    svg_p.add_argument("html", type=Path, help="Input diagram HTML file")
    svg_p.add_argument("--out", type=Path, default=None, help="Output SVG file path")

    args = parser.parse_args()

    if args.command == "validate":
        ok, msg = run_self_check(args.file, offline=args.offline)
        if ok:
            print(f"[PASS] VALID: {args.file}")
            return 0
        else:
            print(f"[FAIL] INVALID: {args.file}\n{msg}", file=sys.stderr)
            return 1

    elif args.command == "scaffold":
        out = scaffold_diagram(args.type, args.out, theme=args.theme, title=args.title)
        print(f"[PASS] Scaffolded {args.type} diagram at {out}")
        ok, msg = run_self_check(out)
        if ok:
            print("[PASS] Self-check passed")
        else:
            print(f"[WARN] Self-check warning: {msg}", file=sys.stderr)
        return 0

    elif args.command == "convert":
        fmt, ir = extract_ir(args.input)
        if args.out:
            args.out.write_text(ir, encoding="utf-8")
            print(f"[PASS] Extracted {fmt} IR to {args.out}")
        else:
            print(ir)
        return 0

    elif args.command == "export-svg":
        out = export_svg_file(args.html, args.out)
        print(f"[PASS] Standalone SVG exported to {out}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())

