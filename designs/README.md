# Design Systems Registry: 67 Themed Design Systems

> A curated collection of 67 complete design systems with AI agent rules (`SKILL.md`) and token foundations (`DESIGN.md`) for **Google Antigravity IDE**.

---

## Overview

When creating frontend interfaces, reaching for the right design language shouldn't require guessing hex codes and border radii.

This skill packages all 67 themes from the **TypeUI / Awesome Design Skills** registry into an offline, zero-dependency Antigravity engine. Each theme includes:
- **`SKILL.md`**: Strict AI guidelines covering brand mission, style foundations, component anatomy, WCAG 2.2 AA rules, and quality gates.
- **`DESIGN.md`**: Machine-readable token declarations (`colors`, `typography`, `rounded`, `spacing`) and human design rationales.

---

## Quick Start

### In Antigravity IDE:
```text
/design-system apply glassmorphism
/design-system search brutalist
/design-system tokens neobrutalism
```

### Via CLI (`scripts/design_system.py`):
```bash
# 1. List all 67 available design systems
python3 scripts/design_system.py list

# 2. Search for themes matching a keyword
python3 scripts/design_system.py search "neon"

# 3. View exact tokens (colors, fonts, radius) for a theme
python3 scripts/design_system.py tokens bento

# 4. Export CSS custom properties directly to a file
python3 scripts/design_system.py export-css glassmorphism --output styles/tokens.css

# 5. Inspect the complete agent guidance
python3 scripts/design_system.py inspect neobrutalism
```

---

## Catalog of 67 Themes

| Category | Available Themes |
| :--- | :--- |
| **Product & Modern** | `clean`, `bento`, `sleek`, `spacious`, `shadcn`, `modern`, `basic`, `refined` |
| **Tactile & Physical** | `glassmorphism`, `claymorphism`, `neumorphism`, `paper`, `skeumorphism`, `perspective` |
| **Brutalist & Raw** | `brutalism`, `neobrutalism`, `mono`, `neon`, `dithered`, `matrix` |
| **Retro & Gaming** | `retro`, `riso`, `sega`, `pacman`, `tetris`, `sketch`, `doodle` |
| **Warm & Cultural** | `terracotta`, `cafe`, `vintage`, `storytelling`, `artistic`, `craft` |
| **Enterprise & System** | `enterprise`, `corporate`, `professional`, `ant`, `material`, `square`, `roku`, `levels` |
| **Vibrant & Expressive**| `colorful`, `gradient`, `vibrant`, `cosmic`, `expressive`, `fantasy`, `fiction`, `immersive` |

*For the complete catalog of all 67 themes with primary fonts and hex palettes, see [references/THEME-REGISTRY.md](references/THEME-REGISTRY.md).*

---

## Directory Structure

```text
design-systems/
├── SKILL.md                          # Main agent contract & CLI instructions
├── README.md                         # This guide
├── LICENSE                           # MIT License
├── .gitignore                        # Clean exclusions
├── references/                       # Deep manuals
│   ├── THEME-REGISTRY.md             # Full 67-theme comparison table
│   └── TOKEN-ARCHITECTURE.md         # Tokens, typography scales, WCAG 2.2 AA
├── resources/                        # Registry data
│   ├── index.json                    # Slug lookup index
│   └── skills/                       # 67 individual theme directories
│       ├── glassmorphism/ (SKILL.md, DESIGN.md)
│       ├── brutalism/     (SKILL.md, DESIGN.md)
│       └── ... (65 more)
├── scripts/
│   └── design_system.py              # CLI tool for tokens, search, export-css
└── tests/
    └── test_design_systems.py        # Automated test suite
```

---

## Verification

Run the automated test suite:

```bash
python3 -B -m unittest discover -s tests
```
