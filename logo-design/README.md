# Logo Design Skill

> A comprehensive, disciplined logo design engine for **Google Antigravity IDE** and AI agents. Guides brand identity from initial discovery and word mapping to precision geometric SVG construction, optical corrections, optical testing, client presentation boards, and export asset kits.

---

## Core Principles & Checkpoint Workflow

1. **Identifier, Not Explanation:** A logo is a simple, distinctive, relevant mark that works at 16 px and on a billboard, in one colour, for decades.
2. **Concept Checkpoint:** The skill always pauses after generating initial concepts. It builds a combined overview image (`concept_sheet.py`) with honest recommendations and size ladders (64/32/16 px). The full production kit is only built after you approve a direction.
3. **Black First:** Every logo is built in solid black on white first to ensure the silhouette and negative space hold up before colour is applied.

---

## 1,400+ Real-World SVG Reference Library

Bundled in `assets/library/` is a visual reference library of 1,400+ SVGs across ~1,200 brands:
- Classified by **mark type** (abstract, combination, pictorial, letterform, wordmark, emblem, mascot, monogram)
- Searchable by **technique**, **geometry**, **subject**, **industry**, **mood**, and **colour**
- Used to study construction geometry and avoid category clichés (never to copy)

---

## Zero-Dependency Python Toolset

All scripts use the Python 3 standard library:

| Script | Purpose & Usage |
| :--- | :--- |
| **`search_library.py`** | Search 1,400+ reference logos: `python3 scripts/search_library.py --technique negative-space --summary` |
| **`svg_audit.py`** | Audit SVG craft, anchors, near-miss angles, and tiny details: `python3 scripts/svg_audit.py my_logo.svg` |
| **`concept_sheet.py`** | Generate the checkpoint sheet (true 64/32/16 px sizes): `python3 scripts/concept_sheet.py a.svg b.svg -o concepts.png` |
| **`preview_sheet.py`** | Build HTML test sheet (pixel tests, squint blur, shelf test): `python3 scripts/preview_sheet.py logo.svg -o preview.html` |
| **`presentation_board.py`**| Client presentation boards with industry mockups: `python3 scripts/presentation_board.py spec.json -o board.html` |
| **`export_variants.py`** | Export black, white, mono, square, favicon, and full web-icon set: `python3 scripts/export_variants.py logo.svg --web-icons` |
| **`render_png.py`** | Render SVG to transparent PNG at exact dimensions: `python3 scripts/render_png.py logo.svg --size 512` |

---

## How to Trigger in Antigravity IDE

Trigger the skill naturally in chat:

- **New Brand Identity:**
  > *"Design a logo for Harbor, a savings app for first-time savers. It should feel calm and safe."*
- **Wordmark Directions:**
  > *"Give me three wordmark directions for a specialty coffee roaster called Kiln. Warm and modern, no coffee cup clichés."*
- **Logo Critique & Audit:**
  > *"Here is our current logo (`logo.svg`). Audit it against logo principles and suggest a refresh."*
- **Asset Kit Generation:**
  > *"Turn this symbol into favicon, app icon, one-colour versions, and a web manifest set."*
- **Category Convention Check:**
  > *"What are the standard logo conventions and clichés in payments and fintech?"*

---

## In-Depth Reference Guides

Progressive disclosure guides loaded on demand in `references/`:
- [`principles.md`](./references/principles.md) — 12 core design principles and mnemonic models
- [`discovery-brief.md`](./references/discovery-brief.md) — Discovery questions, brief templates, and word mapping
- [`mark-types.md`](./references/mark-types.md) — Wordmark, monogram, symbol, emblem, mascot decision guide
- [`visual-techniques.md`](./references/visual-techniques.md) — Grids, optical overshoot, bone effect, irradiation, negative space
- [`svg-construction.md`](./references/svg-construction.md) — Clean SVG math, viewBox rules, arc commands, path simplification
- [`color.md`](./references/color.md) & [`typography.md`](./references/typography.md) — Palette contrast, pairings, optical weights
- [`testing-checklist.md`](./references/testing-checklist.md) — 16 px squint test, one-colour test, competitor shelf test
- [`presentation-delivery.md`](./references/presentation-delivery.md) — Presentation decks and mockups
- [`identity-system.md`](./references/identity-system.md) — Sub-brands, patterns, and motion guidelines
- [`redesign.md`](./references/redesign.md) & [`critique.md`](./references/critique.md) — Preserving brand equity in rebrands

---

## ⚖License & Trademarks

- Skill text, scripts, templates, and catalog data: **MIT License**
- Reference SVGs in `assets/library/svg/` are trademarks of their respective owners, included strictly for educational reference.
