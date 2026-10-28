#!/usr/bin/env python3
"""Unified Test Suite for Google Antigravity Skills.

Executes all unit, smoke, and validator tests across:
  1. court (Adversarial Idea Deliberation)
  2. security-audit (Coverage-Led Vulnerability Hunter)
  3. anti-vibecoding (Frontend Taste & 40-Point Anti-Slop Scanner)
  4. impeccable (24-Command Design Engine & Creative Stack)
  5. steal-like-an-artist (Austin Kleon Creative Operating System)
  6. taste-skill (Flagship v2 Anti-Slop Frontend Framework)
  7. design-systems (TypeUI / Awesome Design Skills 67-Theme Registry)
  8. ui-ux-pro-max (UI/UX Pro Max BM25 Design Intelligence Engine)
  9. threeui (DesignCode / ThreeUI 104 3D & WebGL Component Engine)
  10. reverse-engineer-anything (REA Target Router & MCP Helper)
  11. logo-design (Disciplined SVG Brand Identity & 1,400+ Library)
  12. writing-readme (The Art of Writing Excellent GitHub READMEs)
  13. arena (The Arena: 100-Agent Tournament Bracket & Elimination Engine)
  14. ponytail (The Lazy Senior Dev: Minimal Diffs & Anti-Bloat Engine)
  15. last30days (CrowdPulse & Real-Time Multi-Platform Research Engine)
  16. scrapling (Adaptive Web Scraping, Stealth Browsing & Anti-Bot Bypass)
  17. humanizer (26-Pattern Anti-AI-Writing Prose Polish & Slop Eliminator)
  18. diagram-design (45-Type Editorial HTML+SVG Diagramming & Antigravity IDE Engine)
  19. socratic (Silent Senior Engineering Self-Interrogation & Readiness Gates)
"""
import os
import subprocess
import sys
import time

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
ROOT = os.path.dirname(os.path.abspath(__file__))
PY_BIN = sys.executable

SUITES = [
    {
        "name": "court",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": os.path.join(ROOT, "court"),
        "description": "Adversarial Idea Deliberation Engine"
    },
    {
        "name": "secure-audit",
        "cmd": ["node", "tests/run-tests.cjs"],
        "cwd": os.path.join(ROOT, "secure-audit"),
        "description": "Coverage Ledger & Findings Validators (65 tests)"
    },
    {
        "name": "anti-vcode",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": os.path.join(ROOT, "anti-vcode"),
        "description": "40-Sign Anti-Slop Code Scanner"
    },
    {
        "name": "impeccable",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": os.path.join(ROOT, "impeccable"),
        "description": "24-Command Design Framework & Detector Smoke Tests"
    },
    {
        "name": "steal",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": os.path.join(ROOT, "steal"),
        "description": "Creative Lineage & Originality Audit Engine"
    },
    {
        "name": "taste",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": os.path.join(ROOT, "taste"),
        "description": "Anti-Slop Frontend Dials & 12-Point Preflight Auditor"
    },
    {
        "name": "designs",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": os.path.join(ROOT, "designs"),
        "description": "Curated 67 Design System Themes & Token Registry"
    },
    {
        "name": "ui-ux-max",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": os.path.join(ROOT, "ui-ux-max"),
        "description": "UI/UX Pro Max BM25 Design Intelligence Engine"
    },
    {
        "name": "threeui",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": os.path.join(ROOT, "threeui"),
        "description": "ThreeUI 3D & WebGL 104-Component Engine"
    },
    {
        "name": "rev-engineer",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": os.path.join(ROOT, "rev-engineer"),
        "description": "REA Reverse Engineer Anything (MCP Binary & Runtime Engine)"
    },
    {
        "name": "logo-design",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": os.path.join(ROOT, "logo-design"),
        "description": "Logo Design & SVG Identity Engine (1,400+ Reference Library)"
    },
    {
        "name": "writing-readme",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": os.path.join(ROOT, "writing-readme"),
        "description": "The Art of Writing Excellent GitHub READMEs (50-Point Auditor & Scaffolder)"
    },
    {
        "name": "arena",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": os.path.join(ROOT, "arena"),
        "description": "The Arena (100 Sub-Agents Single-Elimination Bracket Tournament)"
    },
    {
        "name": "ponytail",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": os.path.join(ROOT, "ponytail"),
        "description": "Ponytail (Lazy Senior Dev: Minimal Diff & Zero Over-Engineering Engine)"
    },
    {
        "name": "last30days",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": os.path.join(ROOT, "last30days"),
        "description": "last30days & CrowdPulse Fast-Lane (Real-Time Temporal Intelligence Engine)"
    },
    {
        "name": "scrapling",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": os.path.join(ROOT, "scrapling"),
        "description": "Scrapling (Adaptive Web Scraping, Stealth Browsing & Anti-Bot Bypass)"
    },
    {
        "name": "humanizer",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": os.path.join(ROOT, "humanizer"),
        "description": "Humanizer (26-Pattern Anti-AI-Writing Prose Polish & Slop Eliminator)"
    },
    {
        "name": "diagram-design",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": os.path.join(ROOT, "diagram-design"),
        "description": "Diagram Design (45-Type Editorial HTML+SVG Diagrams & Antigravity IDE Engine)"
    },
    {
        "name": "socratic",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": os.path.join(ROOT, "socratic"),
        "description": "Socratic (Silent Self-Interrogation & 3am Readiness Gates)"
    },
    {
        "name": "rigor",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": os.path.join(ROOT, "rigor"),
        "description": "Rigor (Empirical Engineering Discipline: Grounding, Task Ledger & Completion Gates)"
    },
    {
        "name": "sanzo-wada-colors",
        "cmd": [PY_BIN, "-B", "-m", "unittest", "discover", "-s", "tests"],
        "cwd": os.path.join(ROOT, "sanzo-wada-colors"),
        "description": "Sanzo Wada Colors (348 Palettes, 159 Pigments, WCAG Matrix & Token Engine)"
    }
]


def _run_single_suite(s):
    t0 = time.time()
    res = subprocess.run(s["cmd"], cwd=s["cwd"], capture_output=True, text=True)
    elapsed = time.time() - t0
    return {
        "name": s["name"],
        "description": s["description"],
        "passed": (res.returncode == 0),
        "elapsed": elapsed,
        "stdout": res.stdout,
        "stderr": res.stderr,
    }


def run_all():
    print("=" * 72)
    print("          GOOGLE ANTIGRAVITY SKILLS SUITE - TEST RUNNER")
    print("=" * 72)

    sequential = "--sequential" in sys.argv or "-s" in sys.argv
    mode = "Sequential" if sequential else "High-Performance Parallel"
    print(f"Mode: {mode} ({len(SUITES)} suites across isolated sandboxes)\n")

    total_start = time.time()
    results = []
    all_ok = True

    if sequential:
        for s in SUITES:
            print(f"▶ Testing [{s['name']}] ({s['description']})...")
            r = _run_single_suite(s)
            results.append(r)
            if r["passed"]:
                print(f"  PASS in {r['elapsed']:.3f}s")
            else:
                all_ok = False
                print(f"  FAIL in {r['elapsed']:.3f}s")
                print(r["stderr"] or r["stdout"])
    else:
        from concurrent.futures import ThreadPoolExecutor
        max_workers = min(len(SUITES), max(4, os.cpu_count() or 4))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            ordered_futures = [executor.submit(_run_single_suite, s) for s in SUITES]
            for f in ordered_futures:
                r = f.result()
                results.append(r)
                if r["passed"]:
                    print(f"  [{r['name']:<20}] PASS in {r['elapsed']:.3f}s ({r['description']})")
                else:
                    all_ok = False
                    print(f"  [{r['name']:<20}] FAIL in {r['elapsed']:.3f}s ({r['description']})")
                    print(r["stderr"] or r["stdout"])

    total_time = time.time() - total_start
    print("\n" + "=" * 72)
    print("                         SUMMARY REPORT")
    print("=" * 72)
    print(f"{'Skill':<20} | {'Status':<10} | {'Runtime':<10}")
    print("-" * 72)
    for r in results:
        status_str = "PASSED" if r["passed"] else "FAILED"
        print(f"{r['name']:<20} | {status_str:<10} | {r['elapsed']:.3f}s")
    print("=" * 72)
    print(f"Total Suite Runtime: {total_time:.3f}s | Result: {'ALL PASS (100%)' if all_ok else 'SOME FAILED'}")
    print("=" * 72)

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(run_all())
