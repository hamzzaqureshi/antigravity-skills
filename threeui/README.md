# ThreeUI: 3D, WebGL & Three.js Component Intelligence

> A production-grade design and engineering skill for **Google Antigravity IDE**, containing 104 interactive Three.js components, GLSL shaders, raymarched surfaces, WebGL buttons, and 3D scenes from DesignCode's ThreeUI.

---

## Overview

`threeui` packages the open-source Community catalog from **DesignCode / Meng To (`MengTo/threeui`)** into an offline, zero-dependency Antigravity skill.

Modern web design increasingly demands immersive 3D, WebGL, and dynamic shader effects to stand out. `threeui` provides agents and developers with:
- **104 Production-Tested Components**: Spanning 9 distinct categories (Backgrounds, Buttons, Three.js Scenes, Kinetic Typography, UI Elements, and Landing Pages).
- **Exact TSX & GLSL Source Code**: Self-contained React implementations with mathematical raymarching, simplex noise, and shader uniforms.
- **Instant Local CLI Search**: Fast search engine (`scripts/threeui.py`) to query, inspect, and export components into any project.
- **Production Performance Guardrails**: Built-in rules for DPR clamping, memory disposal, 60 FPS budgets, and Next.js App Router SSR boundaries.

---

## Component Catalog Summary

| Category | Count | Notable Components |
|:---|:---|:---|
| **Backgrounds** | 29 | `liquid-form` (Velox silver raymarching), `bell-field`, `flow-field`, `crt`, `elements` (water, fire, lightning), `constellation-field`, `stream-convergence`, `topo-field` |
| **Buttons & CTAs** | 20 | `liquid-metal-button` (WebGL 2 prismatic liquid), `plasma-button`, `ignition-button`, `induction-button`, `dot-border-button`, `gradient-pill-button`, `lumen-cta` |
| **Three.js Scenes** | 20 | `energy-orb` (FBM energy globe), `laser`, `japanese-tower`, `temple-night`, `landscape`, `bookshelf`, `structure-flow`, `generative-tree` |
| **Text Animation** | 14 | `typography-vortex`, `semantic-bloom`, `particle-wordmark`, `audio-wordmark`, `morphing-glyph-cloud`, `neon-typography`, `outline-typeflow` |
| **UI Elements** | 9 | `animated-top-dock`, `spark-badge`, `performance-gauges`, `connectivity-graph`, `uplink-loader`, `diagnostics-panel`, `skeuomorphic-toggle` |
| **CSS Effects** | 5 | `circle-buttons`, `glassmorphism-cta`, `spinning-border-button`, `sliding-text-cta`, `rectangle-buttons` |
| **Hero Sections** | 3 | `sylva-hero`, `complete-shelf-landing-page`, `bestsellers-book-showcase` |
| **Landing Pages** | 2 | `kage-landing-page`, `meng-to-sketchbook-landing-page` |
| **Sections** | 2 | `editorial-intro-section`, `newsletter-footer-section` |

---

## CLI Usage & Quick Start

All operations run via `scripts/threeui.py` (Python 3 standard library only):

```bash
# Workspace path:
python3 scripts/threeui.py <command> [options]

# Global Antigravity path:
python3 ~/.gemini/config/skills/threeui/scripts/threeui.py <command> [options]
```

### 1. Search Components
```bash
# Search by keyword across all categories
python3 scripts/threeui.py search "liquid"

# Filter search by category
python3 scripts/threeui.py search "wave" --category Backgrounds

# Get results in JSON format
python3 scripts/threeui.py search "button" --json
```

### 2. Inspect Uniforms & Controls
```bash
python3 scripts/threeui.py info liquid-form
python3 scripts/threeui.py info spark-badge
```

### 3. Retrieve or Dump Source Code
```bash
# Outputs the complete TSX component and companion GLSL shaders
python3 scripts/threeui.py code liquid-form
```

### 4. Export Component Directly into Your Project
```bash
# Exports component files directly into target directory
python3 scripts/threeui.py export liquid-form --output-dir ./src/components/threeui
```

### 5. Browse Categories & Counts
```bash
python3 scripts/threeui.py categories
python3 scripts/threeui.py list --category Backgrounds
```

---

## Directory Architecture

```text
threeui/
├── SKILL.md             # Antigravity agent instructions & priority matrix
├── README.md            # Human reference and documentation
├── LICENSE              # MIT License
├── .gitignore           # Version control exclusions
├── references/          # Progressive disclosure manuals
│   ├── threejs-core.md        # Three.js lifecycle, render loop, DPR clamping & disposal
│   ├── shader-glsl.md         # GLSL vertex/fragment shaders, uniforms & raymarching
│   ├── react-integration.md   # React & Next.js App Router boundaries ("use client", SSR)
│   └── component-catalog.md   # Full tabular catalog of all 104 components & props
├── resources/           # Component data & implementations
│   ├── catalog.json           # Clean structured JSON catalog (104 components)
│   └── components/            # TypeScript/TSX & GLSL source files for all 47 component families
├── scripts/             # Zero-dependency Python CLI tool
│   └── threeui.py             # Search, inspect, code retrieval & export tool
└── tests/               # Automated unit test suite
    └── test_threeui.py        # Catalog integrity, search, and export tests
```

---

## Verification & Testing

To run the unit test suite:

```bash
python3 -B -m unittest discover -s tests
```
