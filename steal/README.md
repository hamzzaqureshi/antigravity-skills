# Steal Like an Artist: Reusable Creative Operating System

> An operationalization of Austin Kleon's bestselling philosophy into a disciplined, automated creative operating system for software architecture, product design, engineering, and writing.

---

## Overview

Originality is not invention from an empty vacuum. It is an **emergent property of informed transformation**.

This skill equips AI agents, designers, and software engineers with a rigorous behavioral engine to:
- **Trace Creative Lineages**: Map direct, cross-domain, and negative precedents.
- **Synthesize Multi-Source Influences**: Combine mechanisms across 3+ orthogonal domains (e.g. game loops + Unix pipes + Swiss typography).
- **Enforce Safe Boundaries**: Separate **Plagiarism** (unacceptable) from **Imitation** (private practice) from **Transformation** (novel synthesis).
- **Audit Originality**: Run automated Section 29 audits evaluating source awareness, transformation depth, attribution, and independent value.
- **Break Creative Blocks**: Apply ruthless subtraction, tight constraints, and low-cost 60-minute prototyping.

---

## Quick Start

### 1. In Google Antigravity IDE (Chat Commands)
```text
/steal "Design an unobtrusive terminal status bar inspired by Bloomberg terminals and Quake HUDs"
/artist recommend "Fast local vector store"
/artist audit ./proposals/architecture.md
```

### 2. Via Command Line (`scripts/artist.py`)
The skill bundles a zero-dependency, pure Python 3 standard-library CLI:

```bash
# 1. Initialize project creative context (.artist/ directory)
python3 scripts/artist.py init

# 2. Capture a high-signal idea theft into .artist/ideas.json
python3 scripts/artist.py capture \
  --title "Monospace Telemetry HUD" \
  --source "Bloomberg Terminal & Quake 3 Arena" \
  --source-type "ui" \
  --mechanism "Fixed-width high-contrast text overlay" \
  --adaptation "Render terminal process latency and memory state" \
  --tags "ui,terminal,telemetry"

# 3. Add to the creative lineage tree
python3 scripts/artist.py lineage \
  --add "Unix Stream Pipes" \
  --category "direct" \
  --mechanism "Composable stdout/stdin streams"

# 4. View lineage tree
python3 scripts/artist.py lineage

# 5. Audit an idea or document for originality
python3 scripts/artist.py audit --file proposals/architecture.md --threshold 70

# 6. Log daily creative progress into .artist/logbook.md
python3 scripts/artist.py log \
  --worked "Zero-copy streaming parser" \
  --learned "Buffer pools eliminate GC pauses" \
  --built "CLI benchmark tool" \
  --next-step "Profile memory under 50k events"
```

---

## Directory Structure

```text
steal-like-an-artist/
├── SKILL.md                          # Main agent contract & 6-phase loop
├── README.md                         # This comprehensive guide
├── LICENSE                           # MIT License
├── .gitignore                        # Clean version control exclusions
├── references/                       # In-depth technical guides
│   ├── OPERATING-SYSTEM.md           # Complete unabridged 37-section ARTIST.md
│   ├── CREATIVE-LINEAGE-AND-INFLUENCE.md # Lineage mapping, cross-domain catalog
│   ├── ORIGINALITY-AUDIT-AND-ATTRIBUTION.md # 6-dimension rubric, 10 anti-patterns
│   ├── PROTOTYPING-AND-CONSTRAINTS.md # Subtraction engine & gap-finding heuristics
│   └── IDEA-BANK-AND-CAPTURE.md      # Idea card protocols & daily logbooks
├── resources/                        # Schemas and markdown templates
│   ├── idea-card-schema.json         # Strict Section 33 schema
│   └── templates/
│       ├── recommendation-template.md# Section 32 recommendation block
│       ├── review-template.md        # Section 34 creative review
│       └── logbook-template.md       # Section 25 daily log format
├── scripts/
│   └── artist.py                     # Zero-dependency Python CLI engine
└── tests/
    └── test_artist.py                # Automated unit tests
```

---

## Verification

Run the automated test suite:

```bash
python3 -B -m unittest discover -s tests
```

---

## License

MIT License. Inspired by Austin Kleon's *Steal Like an Artist*. Built for the Antigravity community.
