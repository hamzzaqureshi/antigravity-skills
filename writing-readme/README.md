# Writing README Skill

> The Art of Writing Excellent GitHub READMEs: A battle-tested 4-week framework, 50-point diagnostic scorecard, and zero-dependency scaffolding engine designed to write, review, and maintain documentation for AI/ML, backend, CLI, and web projects.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)
[![Scorecard](https://img.shields.io/badge/scorecard-50--point%20rubric-orange.svg)](#-50-point-quality-scorecard)
[![Dependencies](https://img.shields.io/badge/dependencies-zero%20(stdlib)-success.svg)](#-prerequisites--installation)

---

## Table of Contents

- [What Problem This Solves](#-what-problem-this-solves)
- [Prerequisites & Installation](#-prerequisites--installation)
- [Quickstart & Usage](#-quickstart--usage)
- [Architecture & Workflow](#-architecture--workflow)
- [Project Archetypes & Templates](#-project-archetypes--templates)
- [50-Point Quality Scorecard](#-50-point-quality-scorecard)
- [Deep-Dive References](#-deep-dive-references)
- [How to Trigger in Antigravity IDE](#-how-to-trigger-in-antigravity-ide)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)

---

## What Problem This Solves

A README is often the very first thing an engineer, client, or recruiter sees when opening your repository. Weak documentation forces readers to dig through source code, guess prerequisites, or struggle with broken install steps.

This skill operationalizes a comprehensive **28-day README course curriculum** into an automated AI assistant and zero-dependency CLI toolkit to:
- Guide the reader through the 4-stage psychological journey: *Discover (<5s) ➔ Understand (<30s) ➔ Start (<2m) ➔ Use & Contribute (<10m)*.
- Eliminate guess-work using 6 tailored blueprints for **AI/ML**, **Backend & Infrastructure**, **CLI Tools**, **Libraries & SDKs**, and **Web Apps**.
- Enforce strict reproducibility via automated 50-point diagnostics, catching unreplaced placeholders, missing expected outputs, untagged code blocks, and broken links.
- Enable **README-Driven Development (RDD)** to clarify product requirements and API ergonomics before writing code.

---

## Prerequisites & Installation

### Prerequisites
- **Python:** `>= 3.10` (Standard library only; zero external dependencies required)
- **Git & Shell:** Bash, Zsh, or any standard terminal

### Setup
Clone or place this skill in your Antigravity skills repository:

```bash
# Clone or navigate to the skill directory
cd /path/to/skills/writing-readme

# Verify installation by running the test suite
python3 -B -m unittest discover -s tests
# Expected output: Ran 9 tests in 0.08s ... OK
```

---

## Quickstart & Usage

The skill provides two high-speed command-line tools in `scripts/`:

### 1. 50-Point Quality Diagnostic (`readme_audit.py`)
Audit any existing README against the 10 core dimensions:

```bash
# Audit a markdown document with colorized terminal output
python3 scripts/readme_audit.py ./README.md

# Audit and export structured JSON for CI/CD checks
python3 scripts/readme_audit.py ./README.md --json
```

**Expected terminal output:**
```text
========================================================================
  README Quality Scorecard: README.md
========================================================================
  Overall Score:  48 / 50 (96.0%)
  Quality Grade:  A (Exemplary Production Grade)
  Audit Result:   PASSED
------------------------------------------------------------------------
  • Purpose & Audience:       [ 5 / 5 ]
  • Structure & Navigation:   [ 5 / 5 ]
  • Accuracy & Cleanliness:   [ 5 / 5 ]
  • Installation:             [ 5 / 5 ]
  • Usage & Verification:     [ 5 / 5 ]
  • Technical Explanation:    [ 4 / 5 ]
  • Readability & Syntax:     [ 5 / 5 ]
  • Visual Communication:     [ 5 / 5 ]
  • Trust & Completeness:     [ 5 / 5 ]
  • Maintainability & Links:  [ 4 / 5 ]
========================================================================
```

### 2. Tailored Archetype Scaffolder (`generate_readme.py`)
Scaffold a complete, tailored README draft in seconds:

```bash
# Interactive 5-question wizard
python3 scripts/generate_readme.py

# One-shot CLI generation for an AI/ML project
python3 scripts/generate_readme.py --archetype ai-ml --name "VisionFlow" --output README.md
# Expected output: Successfully generated ai-ml README at: README.md
```

---

## Architecture & Workflow

The skill organizes documentation design around an intentional 5-stage pipeline:

```text
[Raw Project / Idea]
         │
         ▼
[5 Foundational Questions] ──▶ (Archetype, Audience, Distribution, Complexity, Goal)
         │
         ▼
[Tailored Blueprint Engine] ──▶ (ai-ml / backend-infra / cli-tool / library / web-app)
         │
         ▼
[50-Point Scorecard Audit] ──▶ (Detects missing outputs, broken links, syntax errors)
         │
         ▼
[Production-Ready README]
```

---

## Project Archetypes & Templates

Each archetype in `templates/` enforces a tailored structure suited to its reader:

| Archetype | Primary Reader | Key Differentiating Sections |
| :--- | :--- | :--- |
| **`ai-ml`** | ML Engineers, Researchers | Benchmark tables, GPU/CUDA VRAM specs, 3-line inference, dataset schema |
| **`backend-infra`** | DevOps, SREs, Backend Devs | Service topology diagram, port/protocol table, Docker Compose, `.env.example` |
| **`cli-tool`** | Terminal Users, Sysadmins | 10-second install, flag synopsis, UNIX pipe examples, exit codes |
| **`library`** | Software Engineers | Multi-package install, minimal import snippet, API cheat sheet, runtime matrix |
| **`web-app`** | Users, Frontend Developers | Live demo URL, feature highlights, npm script dictionary, dev server setup |
| **`standard`** | General Open-Source | Baseline adhering strictly to the Standard Readme specification |

---

## 50-Point Quality Scorecard

The auditor evaluates repositories across 10 critical dimensions (0 to 5 points each):

| # | Dimension | Passing Standard |
| :---: | :--- | :--- |
| **1** | **Purpose & Audience** | Clear H1 title, elevator pitch blockquote, explicit problem/solution statement |
| **2** | **Structure & Navigation** | Logical hierarchy, no skipped heading levels, TOC if length exceeds 150 lines |
| **3** | **Accuracy & Cleanliness** | Zero unreplaced placeholder tags, template markers, or broken references |
| **4** | **Installation** | Dedicated setup section with copy-pasteable, reproducible code blocks |
| **5** | **Usage & Verification** | Working quickstart with expected outputs or console logs |
| **6** | **Technical Explanation** | Architecture overview with Mermaid or ASCII box flow diagrams |
| **7** | **Readability & Syntax** | Tagged code blocks (`bash`, `python`), no text walls > 100 words |
| **8** | **Visual Communication** | Relevant status badges, architecture diagram, formatted markdown tables |
| **9** | **Trust & Completeness** | Valid license declared, test execution documented, contributing guide linked |
| **10** | **Maintainability & Links** | All internal relative markdown links resolve to existing files |

---

## Deep-Dive References

Curated craft guides are available in `references/`:
- [`principles-and-journey.md`](./references/principles-and-journey.md) — 4-stage reader journey, RDD, and mental models.
- [`archetypes-and-tailoring.md`](./references/archetypes-and-tailoring.md) — Tailoring blueprints across the 5 project archetypes.
- [`reproducibility-and-setup.md`](./references/reproducibility-and-setup.md) — Clean-install testing, prerequisites, and secrets management.
- [`architecture-and-visuals.md`](./references/architecture-and-visuals.md) — Mermaid vs ASCII, badge signal-to-noise, and visual communication.
- [`quality-scorecard.md`](./references/quality-scorecard.md) — Comprehensive 50-point rubric breakdown and critical defect gates.
- [`maintenance-and-evolution.md`](./references/maintenance-and-evolution.md) — Automated doc testing in CI, link validation, and monorepos.

---

## How to Trigger in Antigravity IDE

Invoke the skill naturally in chat:
- **Audit:** *"Audit our current README.md using the 50-point scorecard and tell me what needs improvement."*
- **Scaffold:** *"Draft a production-grade README for an AI/ML fine-tuning pipeline for diffusion models."*
- **RDD:** *"Before we implement this CLI tool, let's do README-Driven Development and draft the user manual and commands."*
- **Rewrite:** *"Rewrite this weak README to make it compelling, reproducible, and easy to scan."*

---

## Testing

Run the automated test suite:

```bash
python3 -B -m unittest discover -s tests
```

---

## Contributing

Contributions, template additions, and rubric improvements are welcome! Please ensure all tests pass and `readme_audit.py` awards Grade A to any new templates before submitting a PR.

---

## ⚖License

[MIT License](LICENSE) © 2026 Antigravity IDE Team.
