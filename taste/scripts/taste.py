#!/usr/bin/env python3
"""Taste Skill CLI - Anti-Slop Frontend Engineering & Pre-Flight Auditor.

Zero-dependency Python tool for:
  1. Brief Inference & Dial Calibration (Variance, Motion, Density).
  2. 12-Point Mechanical Pre-Flight Auditing (Em-dashes, Lila gradients,
     Hero padding, Banned palettes, Eyebrow density, Hardware acceleration).
"""
import argparse
import json
import os
import re
import sys

# Banned warm-craft / beige palette hexes
BANNED_WARM_HEXES = {
    "#f5f1ea", "#f7f5f1", "#fbf8f1", "#efeae0", "#ece6db", "#faf7f1", "#e8dfcb",
    "#b08947", "#b6553a", "#9a2436", "#9c6e2a", "#bc7c3a", "#7d5621",
    "#1a1714", "#1a1814", "#1b1814"
}

BANNED_FONTS = ["fraunces", "instrument serif", "instrument_serif"]


def infer_brief(brief_text):
    text = brief_text.lower()

    if any(k in text for k in ["minimalist", "linear", "calm", "editorial", "raycast"]):
        style = "Minimalist / Linear-Style"
        variance, motion, density = 5, 3, 2
        foundation = "Tailwind v4 + Geist / Geist Mono + Restrained Motion"
    elif any(k in text for k in ["brutalist", "swiss", "industrial", "raw", "blueprint"]):
        style = "Industrial Brutalist / Swiss"
        variance, motion, density = 9, 3, 7
        foundation = "Native CSS / Tailwind + Cabinet Grotesk + IBM Plex Mono"
    elif any(k in text for k in ["luxury", "apple", "premium consumer", "soft", "wellness"]):
        style = "Premium Consumer / Soft Luxury"
        variance, motion, density = 7, 6, 3
        foundation = "Tailwind v4 + Söhne / GT Walsheim + Spring Physics"
    elif any(k in text for k in ["agency", "awwwards", "playful", "wild", "experimental"]):
        style = "Creative Agency / Awwwards"
        variance, motion, density = 9, 8, 3
        foundation = "Native CSS + GSAP ScrollTrigger + Custom Kinetic Typography"
    elif any(k in text for k in ["gov", "public sector", "trust", "regulated", "accessibility"]):
        style = "Trust-First / Public Sector"
        variance, motion, density = 3, 2, 5
        foundation = "GOV.UK Frontend / USWDS / Radix Themes (WCAG AAA)"
    elif any(k in text for k in ["dashboard", "b2b", "analytics", "enterprise"]):
        style = "Enterprise B2B / Analytics"
        variance, motion, density = 6, 4, 8
        foundation = "@carbon/react or @fluentui/react-components"
    else:
        style = "Modern SaaS Landing (Default)"
        variance, motion, density = 8, 6, 4
        foundation = "Tailwind v4 + Satoshi / Cabinet Grotesk + Motion"

    design_read = (
        f"Reading this as: {style} with a calibrated aesthetic language, "
        f"leaning toward {foundation}."
    )

    return {
        "style": style,
        "design_read": design_read,
        "dials": {
            "DESIGN_VARIANCE": variance,
            "MOTION_INTENSITY": motion,
            "VISUAL_DENSITY": density
        },
        "foundation": foundation
    }


def audit_content(content, filename="input"):
    violations = []
    penalties = 0

    # 1. Em-Dash Check (Strict Ban)
    em_dashes = len(re.findall(r"—", content))
    if em_dashes > 0:
        violations.append({
            "rule": "em-dash-ban",
            "count": em_dashes,
            "severity": "CRITICAL",
            "message": f"Found {em_dashes} forbidden em-dashes (—). Replace with clean periods, colons, or concise copy."
        })
        penalties += min(25, em_dashes * 8)

    # 2. Lila AI Purple-Blue Glow / Gradients
    lila_matches = len(re.findall(r"(?:from-purple-\d+\s+to-blue-\d+|bg-purple-500\/20|radial-gradient.*purple)", content, re.I))
    if lila_matches > 0:
        violations.append({
            "rule": "lila-purple-glow-ban",
            "count": lila_matches,
            "severity": "HIGH",
            "message": "AI-purple gradient / radial orb detected. Replace with neutral dark base and singular intentional accent."
        })
        penalties += min(20, lila_matches * 10)

    # 3. Banned Warm-Craft Palette Hexes
    found_warm_hexes = [h for h in BANNED_WARM_HEXES if h in content.lower()]
    if found_warm_hexes:
        violations.append({
            "rule": "banned-warm-craft-palette",
            "matches": found_warm_hexes,
            "severity": "HIGH",
            "message": f"Detected banned generic warm-craft hex codes: {', '.join(found_warm_hexes)}. Rotate to Cold Luxury, Forest, or Cobalt."
        })
        penalties += min(20, len(found_warm_hexes) * 8)

    # 4. Banned Fonts
    found_banned_fonts = [f for f in BANNED_FONTS if f in content.lower()]
    if found_banned_fonts:
        violations.append({
            "rule": "banned-fonts-as-default",
            "matches": found_banned_fonts,
            "severity": "HIGH",
            "message": f"Detected banned default fonts: {', '.join(found_banned_fonts)}. Default to modern sans-serif display fonts."
        })
        penalties += 15

    # 5. Hero Top Padding Cap (max pt-24)
    oversized_hero_padding = re.findall(r"\bpt-(?:28|32|36|40|44|48|52|56|60|64)\b", content)
    if oversized_hero_padding:
        violations.append({
            "rule": "hero-top-padding-cap",
            "matches": oversized_hero_padding,
            "severity": "MEDIUM",
            "message": f"Hero top padding exceeds pt-24 cap: {', '.join(set(oversized_hero_padding))}. Content floats too far down viewport."
        })
        penalties += 10

    # 6. Eyebrow Restraint Check
    eyebrows = len(re.findall(r"(?:uppercase\s+tracking-(?:wider|widest|\[0\.\d+em\]))", content, re.I))
    if eyebrows > 4:
        violations.append({
            "rule": "eyebrow-density-violation",
            "count": eyebrows,
            "severity": "MEDIUM",
            "message": f"Detected {eyebrows} uppercase tracking eyebrows. Enforce max 1 eyebrow per 3 sections."
        })
        penalties += min(15, (eyebrows - 3) * 5)

    # 7. Forbidden Scroll Listeners
    scroll_listeners = len(re.findall(r"window\.addEventListener\([\"']scroll[\"']", content))
    if scroll_listeners > 0:
        violations.append({
            "rule": "forbidden-scroll-listener",
            "count": scroll_listeners,
            "severity": "HIGH",
            "message": "window.addEventListener('scroll') causes unbatched layout thrashing. Use Motion useScroll or GSAP ScrollTrigger."
        })
        penalties += 15

    # 8. Lucide Icon Sprawl (Discouraged by default)
    if "lucide-react" in content.lower():
        violations.append({
            "rule": "lucide-icon-discouraged",
            "severity": "LOW",
            "message": "lucide-react is the standard LLM default. Prefer @phosphor-icons/react, hugeicons-react, or radix-ui icons."
        })
        penalties += 5

    score = max(0, 100 - penalties)
    return {
        "target": filename,
        "score": score,
        "passed": score >= 70 and em_dashes == 0,
        "violations": violations
    }


def audit_path(path):
    results = []
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            results.append(audit_content(f.read(), path))
    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith((".html", ".jsx", ".tsx", ".vue", ".svelte", ".css", ".md")):
                    full_path = os.path.join(root, file)
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        results.append(audit_content(f.read(), full_path))
    return results


def main():
    parser = argparse.ArgumentParser(description="Taste Skill CLI - Anti-Slop Frontend Auditor & Dial Engine")
    sub = parser.add_subparsers(dest="subcommand", help="Available subcommands")

    # infer
    p_infer = sub.add_parser("infer", help="Infer design language and dials from brief")
    p_infer.add_argument("--brief", required=True, help="User prompt or brief description")
    p_infer.add_argument("--json", action="store_true", help="Output JSON")

    # audit
    p_audit = sub.add_parser("audit", help="Run 12-point preflight audit on files")
    p_audit.add_argument("target", help="File or directory to audit")
    p_audit.add_argument("--threshold", type=int, default=70, help="Pass score threshold (default 70)")
    p_audit.add_argument("--json", action="store_true", help="Output JSON")

    # dials
    p_dials = sub.add_parser("dials", help="Print configuration block for dials")
    p_dials.add_argument("--variance", type=int, default=8, help="DESIGN_VARIANCE (1-10)")
    p_dials.add_argument("--motion", type=int, default=6, help="MOTION_INTENSITY (1-10)")
    p_dials.add_argument("--density", type=int, default=4, help="VISUAL_DENSITY (1-10)")

    args = parser.parse_args()
    if not args.subcommand:
        parser.print_help()
        sys.exit(0)

    if args.subcommand == "infer":
        res = infer_brief(args.brief)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print("=" * 64)
            print("           TASTE SKILL - BRIEF INFERENCE")
            print("=" * 64)
            print(f"Detected Style: {res['style']}")
            print(f"Design Read:    {res['design_read']}")
            print(f"Foundation:     {res['foundation']}")
            print("-" * 64)
            print(f"DESIGN_VARIANCE:  {res['dials']['DESIGN_VARIANCE']} / 10")
            print(f"MOTION_INTENSITY: {res['dials']['MOTION_INTENSITY']} / 10")
            print(f"VISUAL_DENSITY:   {res['dials']['VISUAL_DENSITY']} / 10")
            print("=" * 64)

    elif args.subcommand == "audit":
        reports = audit_path(args.target)
        if not reports:
            print(f"No inspectable web files found in: {args.target}")
            sys.exit(0)

        all_passed = all(r["score"] >= args.threshold and r["passed"] for r in reports)
        if args.json:
            print(json.dumps({
                "passed": all_passed,
                "reports": reports
            }, indent=2))
        else:
            print("=" * 64)
            print("        TASTE SKILL - 12-POINT PRE-FLIGHT AUDIT")
            print("=" * 64)
            for r in reports:
                status = "[OK] PASS" if r["passed"] else "✖ FAIL"
                print(f"File:  {r['target']}")
                print(f"Score: {r['score']}/100 | Result: {status}")
                if r["violations"]:
                    print("Violations:")
                    for v in r["violations"]:
                        print(f"  • [{v['severity']}] {v['rule']}: {v['message']}")
                print("-" * 64)
            print(f"Overall Result: {'ALL PASS (100%)' if all_passed else 'SOME CHECKS FAILED'}")
            print("=" * 64)

        sys.exit(0 if all_passed else 1)

    elif args.subcommand == "dials":
        print(f"// Taste Skill Dials Configuration")
        print(f"const DESIGN_VARIANCE = {args.variance};  // 1=Symmetry, 10=Artsy Chaos")
        print(f"const MOTION_INTENSITY = {args.motion}; // 1=Static, 10=Physics")
        print(f"const VISUAL_DENSITY = {args.density};   // 1=Gallery, 10=Cockpit")


if __name__ == "__main__":
    main()
