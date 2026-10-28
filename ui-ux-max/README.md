# UI/UX Pro Max (Design Intelligence Engine)

> A production-grade design intelligence and reasoning skill for **Google Antigravity IDE**, providing searchable design systems, 79 UI styles, 192 product palettes, 74 font pairings, 119 UX guidelines, 25 chart types, and 22 technology stack profiles.

---

## Overview

`ui-ux-pro-max` is an AI-powered design system reasoning engine built on top of the BM25 retrieval algorithm. It analyzes project requirements across 5 parallel domains (product type, visual style, color palette, landing structure, typography) and synthesizes a complete, mathematically grounded design system tailored to your specific industry.

- **100% Zero-Dependency**: Runs entirely on the Python 3 standard library (`csv`, `json`, `math`, `pathlib`, `argparse`).
- **Offline & Deterministic**: Zero network requests, instant sub-50ms execution.
- **Hierarchical Persistence**: Generates `MASTER.md` design contracts and page-level overrides (`pages/<slug>.md`).
- **Multi-Platform Support**: Covers 22 modern web, mobile, and desktop stacks.

---

## Dataset Catalog

| Domain | Size | Key Coverage |
|:---|:---|:---|
| **Styles** | 79 searchable (50 active) | Glassmorphism, Brutalism, Neumorphism, Bento Grid, Claymorphism, Soft UI, Swiss Minimal |
| **Color Palettes** | 192 industry palettes | 1:1 mapped to 192 product types with semantic tokens (`--color-primary`, `--color-accent`) |
| **Typography** | 74 font pairings | Google Fonts imports, Tailwind font family configs, mood classification |
| **Reasoning Rules** | 192 decision profiles | Industry-specific style priorities, landing patterns, and anti-patterns |
| **UX Guidelines** | 119 best practices | WCAG accessibility, touch targets, performance budgets, resilient layout |
| **Technology Stacks**| 22 frameworks | React, Next.js, Vue, Nuxt, Svelte, Astro, Tailwind, SwiftUI, Flutter, Jetpack Compose, etc. |
| **Charts** | 25 data visualization types | Accessibility fallback, data volume thresholds, library recommendations |
| **Icons & Motion** | 105 curated icons / 17 GSAP | SVG Phosphor imports, GSAP scroll/stagger/reveal animation choreography |

---

## CLI Usage & Quick Start

All operations run via `scripts/search.py`:

```bash
# Workspace path:
python3 scripts/search.py "<query>" [options]

# Global Antigravity path:
python3 ~/.gemini/config/skills/ui-ux-pro-max/scripts/search.py "<query>" [options]
```

### 1. Generate Full Design System
```bash
# Terminal ASCII box format (default)
python3 scripts/search.py "fintech banking mobile" --design-system -p "NovaBank"

# Markdown format (ideal for documentation)
python3 scripts/search.py "developer tool ide dark" --design-system -f markdown -p "CodeCraft"

# Machine-readable JSON
python3 scripts/search.py "beauty spa wellness" --design-system --json
```

### 2. Tune with Design Dials (1–10)
```bash
# Adjust variance (asymmetry), motion (GSAP complexity), and density (spacing)
python3 scripts/search.py "analytics operations dashboard" \
  --design-system \
  --variance 8 \
  --motion 4 \
  --density 9 \
  -p "OpsConsole"
```

### 3. Persist Master + Page Overrides
```bash
# Creates design-system/opsconsole/MASTER.md
python3 scripts/search.py "internal ops dashboard" \
  --design-system \
  --persist \
  --output-dir "." \
  -p "OpsConsole"

# Creates design-system/opsconsole/pages/reports.md (inherits from Master)
python3 scripts/search.py "internal ops dashboard" \
  --design-system \
  --persist \
  --output-dir "." \
  -p "OpsConsole" \
  --page "reports"
```

### 4. Domain & Stack Inquiries
```bash
# Domain queries
python3 scripts/search.py "glassmorphism" --domain style
python3 scripts/search.py "contrast ratio focus" --domain ux
python3 scripts/search.py "serif editorial" --domain typography
python3 scripts/search.py "time-series trends" --domain chart

# Stack guidelines
python3 scripts/search.py "server components streaming" --stack nextjs
python3 scripts/search.py "lazy list state restoration" --stack swiftui
python3 scripts/search.py "responsive container queries" --stack html-tailwind
```

---

## Directory Architecture

```text
ui-ux-pro-max/
├── SKILL.md             # Antigravity agent instructions & priority matrix
├── README.md            # Human reference and documentation
├── LICENSE              # MIT License
├── .gitignore           # Excludes cache and generated files
├── data/                # 17 datasets & 22 stack CSV databases
│   ├── app-interface.csv
│   ├── charts.csv
│   ├── colors.csv
│   ├── google-fonts.csv
│   ├── icons.csv
│   ├── landing.csv
│   ├── motion.csv
│   ├── products.csv
│   ├── stacks/          # 22 stack guideline CSVs
│   ├── styles.csv
│   ├── typography.csv
│   ├── ui-reasoning.csv
│   └── ux-guidelines.csv
├── references/          # Progressive disclosure manuals
│   ├── pro-rules.md     # Native app & touch interaction checklists
│   └── quick-reference.md # Complete catalog of 119 UX guidelines
├── resources/           # Templates & auxiliary data assets
├── scripts/             # Python search & reasoning engine
│   ├── core.py          # BM25 algorithm, tokenizer, domain registry
│   ├── design_system.py # Reasoning aggregator & dial processor
│   ├── reasoning_contract.py # JSON condition evaluator
│   ├── search.py        # CLI frontend
│   └── validate_data.py # Offline data integrity validator
└── tests/               # Automated unit and regression test suite
    └── test_ui_ux_pro_max.py # Multi-domain, CLI, and dial verification
```

---

## Verification & Testing

To run the dedicated unit test suite:

```bash
python3 -B -m unittest discover -s tests
```

To run offline data integrity validation:

```bash
python3 -B scripts/validate_data.py
```
