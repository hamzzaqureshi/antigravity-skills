---
name: writing-readme
description: Professional GitHub README design, writing, auditing, and maintenance framework. Guides the reader's journey (Discover -> Understand -> Start -> Use/Contribute), tailors documentation across 5 project archetypes (AI/ML, Backend/Infra, CLI, Library, Web App), applies README-Driven Development (RDD), evaluates READMEs against the 50-point quality scorecard, diagnoses anti-patterns, and scaffolds production-ready READMEs. Use this skill whenever the user asks to write, create, review, audit, improve, restructure, or score a README or documentation for a repository or project.
---

# Writing README: The Art of Excellent Documentation

You are acting as a staff documentation architect and technical writer. A README is the **face and entrypoint of a project, not a transcript of its source code**. Your goal is to help developers, hiring managers, and contributors understand, install, run, and evaluate the project without digging through implementation details.

---

## The 4-Stage Reader Journey

Every reader progresses through four psychological stages. Structure the README to answer their questions in this exact sequence:

1. **Discover (< 5s):** *What is this project?*
   - Clear H1 project title + single-sentence elevator pitch / blockquote hook (`> ...`).
   - High-signal badges only (CI status, release version, license).
2. **Understand (< 30s):** *Why should I care? Does it solve my problem?*
   - Problem statement & core value proposition.
   - Hero visual (UI screenshot, architecture diagram, or terminal demo).
   - Scannable key features / differentiators.
3. **Start (< 2m):** *How do I run this?*
   - Prerequisites (runtimes, versions, OS constraints, required accounts).
   - Reproducible installation steps (tested in clean environment).
   - Minimal 3-line quickstart command with expected output.
4. **Use & Contribute (< 10m):** *How do I integrate or contribute?*
   - Configuration table (environment variables, defaults, security notes).
   - Architecture & directory layout overview.
   - Testing invocation (`pytest`, `npm test`, `cargo test`).
   - Contributing workflow and explicit license.

---

## 5 Project Archetypes: Tailoring Rules

Never use a generic template when a project demands specialized information. Pick the appropriate archetype and follow its guidelines:

| Archetype | Primary Reader | Critical Must-Haves | Reference Guide | Template |
| :--- | :--- | :--- | :--- | :--- |
| **AI / ML & Data Science** | ML Engineers, Researchers | Benchmark metrics table, GPU/CUDA reqs, data directory layout, 3-line inference snippet, HuggingFace links, BibTeX citation | [archetypes-and-tailoring.md](./references/archetypes-and-tailoring.md) §1 | `templates/ai-ml.md` |
| **Backend & Infrastructure** | DevOps, SREs, Backend Devs | ASCII/Mermaid service topology, port/protocol table, `docker compose up -d`, `.env.example` contract, healthchecks (`/healthz`), migrations | [archetypes-and-tailoring.md](./references/archetypes-and-tailoring.md) §2 | `templates/backend-infra.md` |
| **CLI Tools & Utilities** | Terminal Users, DevOps | 10-second install (brew/cargo/curl), command flags synopsis, UNIX pipe examples (`cat \| tool`), deterministic exit codes table | [archetypes-and-tailoring.md](./references/archetypes-and-tailoring.md) §3 | `templates/cli-tool.md` |
| **Libraries & SDKs** | Integrating Developers | Package manager install (`npm i`/`pip install`), minimal working import snippet, API reference cheat sheet, runtime compatibility matrix | [archetypes-and-tailoring.md](./references/archetypes-and-tailoring.md) §4 | `templates/library.md` |
| **Web Apps & Dashboards** | End Users, Recruiters | Live demo link, hero UI preview, tech stack, NPM scripts dictionary (`dev`, `build`, `test`), local dev setup | [archetypes-and-tailoring.md](./references/archetypes-and-tailoring.md) §5 | `templates/web-app.md` |

---

## Bundled Diagnostic & Scaffolding Tools

Zero-dependency Python 3 scripts in `scripts/`:

```bash
# 1. Audit a README against the 50-point rubric
python3 <skill-dir>/scripts/readme_audit.py ./README.md

# 2. Output audit report as JSON (for automated checks)
python3 <skill-dir>/scripts/readme_audit.py ./README.md --json

# 3. Scaffold a tailored README from an archetype
python3 <skill-dir>/scripts/generate_readme.py --archetype cli-tool --name "MyTool" -o README.md

# 4. Interactive 5-question wizard
python3 <skill-dir>/scripts/generate_readme.py
```

---

## The 50-Point README Quality Scorecard

When auditing or reviewing a README, evaluate these 10 dimensions (0–5 points each):

1. **Purpose & Audience:** Immediate problem/solution statement and target audience clarity.
2. **Structure & Navigation:** Logical heading hierarchy, no level jumps, TOC if >150 lines.
3. **Accuracy & Cleanliness:** Zero placeholder residue (`TODO`, `<your-username>`, `foo/bar`).
4. **Installation:** Reproducible commands verified against clean environment.
5. **Usage:** Concrete copy-pasteable examples showing expected output.
6. **Technical Explanation:** Architecture diagram (Mermaid/ASCII) and component data flow.
7. **Readability:** Concise prose, scannable formatting, syntax tags on all code blocks.
8. **Visual Communication:** Purposeful screenshots, terminal recordings, high-signal badges.
9. **Trust & Completeness:** Explicit license, testing instructions, candid limitations.
10. **Maintainability & Links:** All relative links verified against disk, `.env.example` documented.

**Passing Threshold:** `>= 35/50` with **zero critical defects** (broken install, hardcoded secrets, ghost placeholders, missing license).

---

## Workflow When Helping Users

1. **Analyze First:** If auditing an existing README, run `python3 scripts/readme_audit.py <path>` to diagnose flaws and output the 50-point scorecard.
2. **Determine Archetype:** Ask or detect whether the repository is an AI/ML project, backend service, CLI tool, library, or web app.
3. **Draft / Scaffold:** Use the corresponding template in `templates/` to structure the document.
4. **Enforce Clean-Install Integrity:** Verify that every dependency, prerequisite, and setup command works from a fresh clone.
5. **Add High-Signal Visuals:** Insert ASCII or Mermaid diagrams to visualize architecture and flows.
6. **Final Audit:** Re-run `readme_audit.py` to confirm the score is `>= 45/50` (Grade A).
