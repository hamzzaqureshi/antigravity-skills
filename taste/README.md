# Taste Skill: Anti-Slop Frontend Framework for AI Agents

> Flagship v2 anti-slop frontend framework by **Leonxlnx** (93.4k+ GitHub stars), adapted and fully operationalized for **Google Antigravity IDE**.

---

## Overview

`taste-skill` eliminates generic, boilerplate AI frontend output by:
1. **Reading the Room**: Performing brief inference and outputting a one-line "Design Read" before generating any code.
2. **Tuning The Three Dials**:
   - `DESIGN_VARIANCE (1-10)`: 1 = Symmetry, 10 = Artsy Chaos
   - `MOTION_INTENSITY (1-10)`: 1 = Static, 10 = Cinematic Physics
   - `VISUAL_DENSITY (1-10)`: 1 = Gallery, 10 = Packed Cockpit
3. **Mapping Real Design Systems**: Reaching for official packages (`@fluentui`, `@material/web`, `@carbon/react`, `polaris.js`, `govuk-frontend`, `shadcn/ui`, `Tailwind v4`) instead of reinventing them.
4. **Banning Generic AI Tells**: Hard ban on em-dashes (`—`), "Lila" AI purple glows, generic warm-craft beige/brass palettes, default serif fonts (`Fraunces`), and fake div screenshots.
5. **Enforcing Mechanical Pre-Flight Checks**: 12 strict rules that must pass before declaring work finished.

---

## Included Specialized Variants

| Variant | Aesthetic & Target | Reference File |
| :--- | :--- | :--- |
| **`design-taste-frontend`** | Flagship v2 master anti-slop framework | [SKILL.md](SKILL.md) |
| **`minimalist-ui`** | Editorial product UI (Notion / Linear / Raycast vibes) | [resources/variants/minimalist-ui.md](resources/variants/minimalist-ui.md) |
| **`industrial-brutalist-ui`** | Raw Swiss engineering, blueprint precision, 2px borders | [resources/variants/brutalist-ui.md](resources/variants/brutalist-ui.md) |
| **`high-end-visual-design`** | Calm luxury, generous whitespace, spring motion | [resources/variants/soft-ui.md](resources/variants/soft-ui.md) |
| **`gpt-taste`** | Hyper-strict anti-slop rules tailored to counter GPT/Codex | [resources/variants/gpt-taste.md](resources/variants/gpt-taste.md) |
| **`redesign-existing-projects`** | Audit-first methodology before refactoring existing codebases | [resources/variants/redesign-existing.md](resources/variants/redesign-existing.md) |
| **`stitch-design-taste`** | Google Stitch compatible rules with `DESIGN.md` export | [resources/variants/stitch-design.md](resources/variants/stitch-design.md) |
| **`full-output-enforcement`** | Bans placeholder comments (`// ...`) and incomplete code | [resources/variants/output-enforcement.md](resources/variants/output-enforcement.md) |

---

## Quick Start

### In Antigravity IDE (Chat Prompts):
```text
/taste Design a Linear-style minimalist developer landing page for distributed cache telemetry.
/taste style: brutalist Create an engineering portfolio with raw monospace typography and 2px borders.
/taste audit ./src/components/Hero.tsx
```

### Via CLI (`scripts/taste.py`):
```bash
# 1. Infer design read and dials from user brief
python3 scripts/taste.py infer --brief "B2B SaaS landing page for enterprise database monitoring"

# 2. Run the 12-point mechanical pre-flight audit
python3 scripts/taste.py audit ./src

# 3. Print configured dial values
python3 scripts/taste.py dials --variance 7 --motion 6 --density 4
```

---

## Directory Structure

```text
taste-skill/
├── SKILL.md                          # Flagship v2 design-taste-frontend contract
├── README.md                         # This guide
├── LICENSE                           # MIT License (Leonxlnx)
├── .gitignore                        # Clean exclusions
├── references/                       # Deep technical manuals
│   ├── BRIEF-INFERENCE-AND-DIALS.md  # 3 dials & one-line design read
│   ├── DESIGN-SYSTEM-MAP.md          # Official packages vs custom aesthetics
│   ├── GSAP-AND-MOTION-PATTERNS.md   # Canonical StickyStack, HorizontalPan, etc.
│   ├── ANTI-SLOP-RULES-AND-PREFLIGHT.md # 12-point check & hard bans
│   ├── SPECIALIZED-VARIANTS.md       # Minimalist, Brutalist, Soft, GPT-Taste
│   └── RESEARCH-LLM-LAZINESS.md      # Root causes & fixes for output truncation
├── resources/                        # Sub-skills & Image workflows
│   ├── variants/                     # 7 specialized design styles
│   └── image-skills/                 # image-to-code, brandkit, imagegen
├── scripts/
│   └── taste.py                      # Pre-flight auditor & dial inference engine
└── tests/
    └── test_taste.py                 # Automated unit test suite
```

---

## Verification

Run the automated test suite:

```bash
python3 -B -m unittest discover -s tests
```
