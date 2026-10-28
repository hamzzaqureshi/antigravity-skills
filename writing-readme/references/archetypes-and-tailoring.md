# Project Archetypes & Tailoring Guide

Different software archetypes serve completely different audiences with radically different information needs. Never force a one-size-fits-all structure onto diverse repositories.

---

## 1. AI, Machine Learning & Data Science Repositories

### Primary Readers
Researchers, ML engineers, data scientists, recruiters evaluating modeling skills.

### Critical Sections & Must-Haves
1. **Benchmark Scorecard / Results Table:** State Top-1 Accuracy, F1, BLEU, or inference latency alongside evaluation dataset names and SOTA baselines.
2. **Hardware & Accelerator Requirements:** Explicitly state minimum GPU VRAM, CUDA versions, CPU fallback behavior, and MPS support (Apple Silicon).
3. **Data Schema & Directory Layout:** Show the exact expected layout of input datasets (`train/`, `val/`, `annotations.json`).
4. **3-Line Inference Snippet:** Show how to run inference with the model in Python immediately without training from scratch.
5. **Pretrained Checkpoint Access:** Provide direct HuggingFace, S3, or GCS links to download model weights.
6. **Citation (BibTeX):** If accompanying research, include a clean BibTeX citation block.

---

## 2. Backend Services & Cloud Infrastructure

### Primary Readers
DevOps/SREs, backend developers, platform engineers, sysadmins.

### Critical Sections & Must-Haves
1. **ASCII / Mermaid Architecture Diagram:** Show entry ingress, API gateways, database dependencies, caches, and message brokers.
2. **Port & Protocol Inventory:** A clean markdown table listing internal ports, external ports, protocols, and endpoint descriptions.
3. **One-Command Docker Compose:** A turnkey `docker compose up -d` snippet with verified clean startup.
4. **Environment Variables & Secrets Contract:** Document every config variable with its default, description, and security sensitivity. Never commit `.env` with real credentials.
5. **Health Checks & Observability:** Document `/healthz`, `/metrics` (Prometheus), log format, and tracing endpoints.
6. **Disaster Recovery & Migrations:** Instructions for running schema migrations (`make migrate`) and backup procedures.

---

## 3. Command Line Interfaces (CLI Tools)

### Primary Readers
Terminal power users, systems engineers, automated CI/CD runners.

### Critical Sections & Must-Haves
1. **10-Second Install:** Single curl script, Homebrew tap, `cargo install`, or precompiled binary release downloads.
2. **Help Flag Output / Synopsis:** Clean ASCII usage block showing `tool [OPTIONS] <COMMAND>`.
3. **UNIX Pipe Demonstration:** Show how the CLI interacts with stdin/stdout, pipes (`cat file | tool | jq .`), and standard streams.
4. **Deterministic Exit Codes:** Table specifying what exit codes `0`, `1`, `2`, `127` represent for shell scripting.
5. **Terminal Visual:** VHS GIF or asciinema demo showing instant execution.

---

## 4. Reusable Libraries & SDKs (npm, PyPI, Crates, Go)

### Primary Readers
Developers integrating your code as an external dependency.

### Critical Sections & Must-Haves
1. **Package Manager Command:** `npm i`, `pip install`, `cargo add`, `go get`.
2. **Minimal Working Import:** A self-contained code snippet (< 10 lines) demonstrating the primary export.
3. **API Reference Table:** List functions/classes, argument types, return types, and exceptions thrown.
4. **Compatibility Matrix:** Document supported language runtimes (e.g. Node 18/20/22, Python 3.9-3.12, ESM vs CJS).
5. **Bundle Size / Zero-Dependency Badge:** State bundlephobia gzipped footprint and external dependency count.

---

## 5. Web Applications & Dashboards

### Primary Readers
End users, product managers, frontend engineers, recruiters.

### Critical Sections & Must-Haves
1. **Live Demo Link:** Prominent clickable link to the deployed application on Vercel, Netlify, or custom domain.
2. **Hero UI Screenshot:** Clean visual showing the active user interface.
3. **Tech Stack Badges:** Framework, CSS system, state management, backend provider.
4. **NPM Scripts Dictionary:** Table explaining `dev`, `build`, `test`, `lint`, `preview`.
5. **Environment Configuration:** Explicit instructions for `.env.local` setup.
