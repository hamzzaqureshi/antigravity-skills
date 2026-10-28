#!/usr/bin/env python3
"""Cross-Platform Installer for Google Antigravity Skills Suite.

Works on Linux, macOS, and Windows.
Supports:
  - Antigravity IDE Global (~/.gemini/config/skills) [Default]
  - Antigravity IDE Project (.agents/skills)
  - Claude Code Global (~/.claude/skills)
  - Claude Code Project (.claude/skills)
  - Custom target paths
"""

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

SKILLS = [
    ("court", "Adversarial idea & architecture trials"),
    ("secure-audit", "Coverage-led vulnerability hunting & AST validators"),
    ("anti-vcode", "40-point anti-slop code scanner & Swiss design"),
    ("impeccable", "24-command design framework & offline detector"),
    ("steal", "Austin Kleon creative operating system"),
    ("taste", "Leonxlnx v2 anti-slop frontend dials & preflight"),
    ("designs", "Curated 67 design themes & token registry"),
    ("ui-ux-max", "BM25 design intelligence (79 styles, 192 palettes)"),
    ("threeui", "104 production 3D & WebGL Three.js components"),
    ("rev-engineer", "REA: Decompilation, Electron/JS & binary reconstruction"),
    ("logo-design", "Disciplined SVG brand identity & 1,400+ reference library"),
    ("writing-readme", "The Art of Writing Excellent GitHub READMEs (50-point rubric & 5 archetypes)"),
    ("arena", "100 sub-agents tournament bracket to eliminate bad answers"),
    ("ponytail", "The lazy senior dev: minimal diffs, zero YAGNI bloat, and shortcut debt tracking"),
    ("last30days", "Real-time temporal intelligence (Reddit, X, YouTube, HN, Polymarket) + CrowdPulse fast-lane"),
    ("scrapling", "Adaptive web scraping, stealth browsing, Cloudflare bypass & concurrent spiders"),
    ("humanizer", "Wikipedia-backed 26-pattern anti-AI-writing polish & prose humanizer"),
    ("diagram-design", "Editorial HTML+SVG diagrams (45 types, no shadows, zero Mermaid slop, Antigravity IDE helper)"),
    ("socratic", "Senior engineering self-interrogation (15 domains, 10 decision packs, MVP/Prod/Enterprise gates)"),
    ("rigor", "Empirical engineering discipline (grounding, task ledger, cross-model review & completion gates)"),
    ("sanzo-wada-colors", "Sanzo Wada 1930s color dictionary (348 palettes, 159 pigments, WCAG contrast & CSS tokens)"),
]

BUNDLES = {
    "design": [
        "anti-vcode", "designs", "ui-ux-max", "threeui", "taste",
        "sanzo-wada-colors", "diagram-design", "logo-design", "impeccable"
    ],
    "engineering": [
        "rigor", "secure-audit", "socratic", "court",
        "rev-engineer", "scrapling", "ponytail", "arena"
    ],
    "prose": [
        "writing-readme", "humanizer", "steal", "last30days"
    ],
}

SCRIPT_DIR = Path(__file__).resolve().parent

IGNORE_PATTERNS = shutil.ignore_patterns(
    "__pycache__", "*.pyc", "*.pyo", ".DS_Store", "node_modules",
    ".court", ".impeccable", ".rigor", ".artist", "dist"
)


def list_skills():
    print(f"\nAvailable Skills ({len(SKILLS)} total):")
    print("─" * 70)
    for idx, (name, desc) in enumerate(SKILLS, 1):
        print(f"  {idx:>2}. {name:<22} - {desc}")
    print("\nCurated Bundles:")
    print("  • design       (9 skills: anti-vcode, designs, ui-ux-max, threeui, taste, ...)")
    print("  • engineering  (8 skills: rigor, secure-audit, socratic, court, rev-engineer, ...)")
    print("  • prose        (4 skills: writing-readme, humanizer, steal, last30days)")
    print("─" * 70)
    sys.exit(0)


def copy_skill(src: Path, dest: Path, dry_run: bool = False):
    if dry_run:
        return
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest, ignore=IGNORE_PATTERNS)
    # Set execution permissions on scripts if on POSIX
    if os.name == "posix":
        for folder in ["scripts", "bin"]:
            target_dir = dest / folder
            if target_dir.is_dir():
                for p in target_dir.rglob("*"):
                    if p.is_file() and p.suffix in (".py", ".sh", ".cjs", ".js", ""):
                        try:
                            p.chmod(p.stat().st_mode | 0o755)
                        except OSError:
                            pass


def prompt_selection(all_names):
    """Interactive selector for target directory and skills."""
    print("=" * 72)
    print("       Google Antigravity Skills Suite — Guided Installer")
    print("=" * 72)

    # 1. Target Directory
    print("\nStep 1: Choose destination:")
    print("  1) Antigravity Global        (~/.gemini/config/skills) [Recommended]")
    print("  2) Current Project Workspace (./.agents/skills)        [Project-scoped]")
    print("  3) Claude Code Global        (~/.claude/skills)        [Claude CLI]")
    print("  4) Claude Code Project       (./.claude/skills)")
    print("  5) Custom Directory\n")

    t_choice = input("Select destination [1-5] (default: 1): ").strip() or "1"
    home = Path.home()

    if t_choice == "1":
        target_dir = home / ".gemini" / "config" / "skills"
    elif t_choice == "2":
        target_dir = Path(".").resolve() / ".agents" / "skills"
    elif t_choice == "3":
        target_dir = home / ".claude" / "skills"
    elif t_choice == "4":
        target_dir = Path(".").resolve() / ".claude" / "skills"
    elif t_choice == "5":
        custom_input = input("Enter custom path: ").strip()
        if not custom_input:
            print("Error: Target path cannot be empty.", file=sys.stderr)
            sys.exit(1)
        target_dir = Path(custom_input).resolve()
    else:
        target_dir = home / ".gemini" / "config" / "skills"

    # 2. Scope Selection
    print("\nStep 2: Choose skills to install:")
    print("  1) Install All 21 Skills [Recommended - Complete Toolkit]")
    print("  2) Frontend & Design Bundle (9 skills: anti-vcode, designs, ui-ux-max, threeui...)")
    print("  3) Engineering & Security Bundle (8 skills: rigor, secure-audit, socratic, court...)")
    print("  4) Writing & Research Bundle (4 skills: writing-readme, humanizer, steal...)")
    print("  5) Custom Pick (select by numbers e.g. 1, 8, 20)\n")

    s_choice = input("Select skills [1-5] (default: 1): ").strip() or "1"

    if s_choice == "1":
        selected = all_names
    elif s_choice == "2":
        selected = BUNDLES["design"]
    elif s_choice == "3":
        selected = BUNDLES["engineering"]
    elif s_choice == "4":
        selected = BUNDLES["prose"]
    elif s_choice == "5":
        print("\nAvailable skills:")
        for idx, (name, _) in enumerate(SKILLS, 1):
            print(f"  {idx:>2}) {name}")
        raw_picks = input("\nEnter numbers or names separated by commas: ").strip()
        selected = []
        for token in raw_picks.split(","):
            token = token.strip()
            if not token:
                continue
            if token.isdigit():
                num = int(token)
                if 1 <= num <= len(SKILLS):
                    selected.append(SKILLS[num - 1][0])
            elif token in all_names:
                selected.append(token)
            else:
                print(f"Warning: Ignoring unknown token '{token}'")
        if not selected:
            print("No valid skills selected. Defaulting to all.")
            selected = all_names
    else:
        selected = all_names

    return target_dir, selected


def main():
    parser = argparse.ArgumentParser(
        description="Install Antigravity Skills Suite locally or globally."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-g", "--global", dest="is_global", action="store_true",
        help="Install globally for Antigravity IDE (~/.gemini/config/skills)"
    )
    group.add_argument(
        "-p", "--project", nargs="?", const=".", metavar="DIR",
        help="Install locally into project repository (.agents/skills)"
    )
    group.add_argument(
        "-c", "--claude", action="store_true",
        help="Install globally for Claude Code (~/.claude/skills)"
    )
    group.add_argument(
        "--claude-project", nargs="?", const=".", metavar="DIR",
        help="Install locally for Claude Code project (.claude/skills)"
    )
    group.add_argument(
        "--custom", metavar="DIR",
        help="Install into custom destination path"
    )

    parser.add_argument(
        "-a", "--all", action="store_true",
        help="Install all 21 skills without prompting"
    )
    parser.add_argument(
        "-b", "--bundle", choices=["design", "engineering", "prose"],
        help="Install a curated bundle of skills"
    )
    parser.add_argument(
        "-s", "--skills", metavar="LIST",
        help="Comma-separated subset of skills to install"
    )
    parser.add_argument(
        "-l", "--list", action="store_true",
        help="List available skills and bundles"
    )
    parser.add_argument(
        "-t", "--test", action="store_true",
        help="Run verification test runner after install"
    )
    parser.add_argument(
        "-d", "--dry-run", action="store_true",
        help="Simulate installation without writing files"
    )

    args = parser.parse_args()

    if args.list:
        list_skills()

    all_names = [s[0] for s in SKILLS]

    # Resolve selected skills from CLI
    if args.skills:
        selected = [s.strip() for s in args.skills.split(",") if s.strip()]
        for s in selected:
            if s not in all_names:
                print(f"Error: Unknown skill '{s}'. Available: {', '.join(all_names)}", file=sys.stderr)
                sys.exit(1)
    elif args.bundle:
        selected = BUNDLES[args.bundle]
    elif args.all:
        selected = all_names
    else:
        selected = None

    home = Path.home()
    target_dir = None

    if args.is_global:
        target_dir = home / ".gemini" / "config" / "skills"
    elif args.project:
        target_dir = Path(args.project).resolve() / ".agents" / "skills"
    elif args.claude:
        target_dir = home / ".claude" / "skills"
    elif args.claude_project:
        target_dir = Path(args.claude_project).resolve() / ".claude" / "skills"
    elif args.custom:
        target_dir = Path(args.custom).resolve()

    # If neither target nor skills were fully specified, run interactive mode
    if target_dir is None or selected is None:
        if sys.stdin.isatty():
            t_prompt, s_prompt = prompt_selection(all_names)
            if target_dir is None:
                target_dir = t_prompt
            if selected is None:
                selected = s_prompt
        else:
            if target_dir is None:
                target_dir = home / ".gemini" / "config" / "skills"
            if selected is None:
                selected = all_names

    print(f"\nTarget Directory: {target_dir}")
    print(f"Selected ({len(selected)}/{len(SKILLS)}): {', '.join(selected)}")

    if args.dry_run:
        print("\n[Dry Run] No files written.")
        sys.exit(0)

    target_dir.mkdir(parents=True, exist_ok=True)

    installed_count = 0
    for name in selected:
        src = SCRIPT_DIR / name
        dest = target_dir / name
        if not src.is_dir():
            print(f"  Warning: Skipping missing skill: {name}")
            continue
        print(f"  Installing {name}...")
        copy_skill(src, dest, dry_run=args.dry_run)
        installed_count += 1

    print(f"\nSuccessfully installed {installed_count} skill(s) into {target_dir}\n")

    if args.test:
        print("Running test suite verification...")
        test_script = SCRIPT_DIR / "test_all.py"
        if test_script.is_file():
            subprocess.run([sys.executable, "-B", str(test_script)])


if __name__ == "__main__":
    main()
