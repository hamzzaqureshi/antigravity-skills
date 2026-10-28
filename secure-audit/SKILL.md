---
name: secure-audit
description: >-
  Perform comprehensive security guidance and vulnerability reviews for codebases, APIs, services, CLI tools, libraries, and microservices. Use when the user asks for a security audit, vulnerability review, pen test, code security check, or asks security questions about their codebase. Operates in Guidance mode (focused advice) or Full Audit mode (6-phase coverage-led audit with verified machine-readable findings and reports).
argument-hint: "[--quick | --deep] [--scope <paths>] [<target-path>]"
license: MIT
metadata:
  author: "Cloudflare (original design), adapted for Google Antigravity"
  source: "https://github.com/cloudflare/security-audit-skill"
  version: "2.0.0"
---

# Security Audit: Coverage-Led Vulnerability Review

A defensive, source-grounded security audit workflow adapted for **Google Antigravity IDE**. It orchestrates isolated review perspectives through reconnaissance, coverage-led hunting, adversarial candidate validation, structured machine-readable findings, independent verification, and target-neutral reporting.

A candidate without a concrete lower-trust principal, crossed boundary, and affected resource is not a confirmed finding.

---

## Operating Modes

This skill is guidance by default. Loading it does not authorize the full multi-phase audit workflow or bulk file creation.

- **Guidance Mode** *(Default for questions and focused reviews)*:
  Use for security questions, specific file reviews, triage, or investigating particular vulnerability classes. Answer directly, inspect relevant source, explain mechanics, and recommend the smallest effective fix. Do not write full audit artifacts.
- **Full Audit Mode** *(Explicit requests: "audit this codebase", "full security review", "pen-test")*:
  Execute the complete 6-phase audit lifecycle and generate the full report suite (`REPORT.md`, `FINDINGS-DETAIL.md`, `NEEDS-VALIDATION.md`, and machine-validated `findings.json`).

*If the user's intent is ambiguous between guidance and a full audit, ask one focused clarification question before initializing files.*

---

## Safety & Execution Boundaries

1. **Source Inspection is Read-Only**: The audit investigates and reports; it never modifies target source code.
2. **Strict Sandboxing for Local Tests**: If running bounded local checks, harnesses, or unit tests:
   - No external network access.
   - Use dummy credentials and non-production fixtures.
   - Write only into isolated `scratch/` directories outside repository source.
   - Never generate or persist functional exploit payloads or weaponized exploit chains.
3. **Evidence Over Assumptions**: If a decisive security control is outside the repository (e.g. cloud IAM, reverse proxy, external WAF), record it as `needs_validation` with the exact unverified fact rather than guessing.

---

## Full Audit Workflow (6 Phases)

In Full Audit mode, resolve the target path and output directory (default: `~/security-audits/<repo-name>/run-<N>/`), then execute the phases in order:

### Phase 1: Reconnaissance
Map architecture, trust boundaries, entry points, and deterministic coverage units.
- **Guide**: [RECONNAISSANCE.md](references/RECONNAISSANCE.md)
- **Artifacts**: Produce `architecture.md` and initial `coverage-ledger.json`.
- **Validation**:
  ```bash
  node scripts/validate-coverage-ledger.cjs coverage-ledger.json
  ```

### Phase 2: Coverage-Led Hunting Waves
Assign focused hunting tasks across the ledger units. Hunters inspect source and identify candidate boundary failures.
- **Guides**: [HUNTING.md](references/HUNTING.md) and [ATTACK-CLASSES.md](references/ATTACK-CLASSES.md)
- **Domain Companions** (consult on-demand based on target architecture):
  - Web & Auth: [WEB-PROTOCOL-AND-AUTH.md](references/WEB-PROTOCOL-AND-AUTH.md)
  - Cloud & Infra: [CLOUD-AND-DEPLOYMENT.md](references/CLOUD-AND-DEPLOYMENT.md)
  - AI & LLM Systems: [AI-AND-LLM.md](references/AI-AND-LLM.md)
  - Client-Side & DOM: [CLIENT-SIDE.md](references/CLIENT-SIDE.md)
  - Supply Chain & CI: [SUPPLY-CHAIN-AND-RELEASE.md](references/SUPPLY-CHAIN-AND-RELEASE.md)
  - Protocols & Messaging: [PROTOCOLS-RPC-AND-MESSAGING.md](references/PROTOCOLS-RPC-AND-MESSAGING.md)
  - Data Isolation & Lifecycle: [DATA-ISOLATION-AND-LIFECYCLE.md](references/DATA-ISOLATION-AND-LIFECYCLE.md)
  - Binary & Memory Safety: [MEMORY-SAFETY-AND-BINARY.md](references/MEMORY-SAFETY-AND-BINARY.md)
  - Resource & Availability: [RESOURCE-EXHAUSTION-AND-AVAILABILITY.md](references/RESOURCE-EXHAUSTION-AND-AVAILABILITY.md)
  - Native & Local IPC: [DESKTOP-MOBILE-AND-LOCAL-IPC.md](references/DESKTOP-MOBILE-AND-LOCAL-IPC.md)

### Phase 3: Candidate Validation
Every unique candidate must be verified by a fresh, independent perspective whose goal is to attempt to disprove or boundedly confirm the boundary failure.
- **Guide**: [VALIDATION-AND-REPORTING.md](references/VALIDATION-AND-REPORTING.md)
- Candidates that fail verification are marked `rejected`.
- Blocked hypotheses with missing environment facts are marked `needs_validation`.

### Phase 4: Structured Output
Compile verified candidates into `findings.json`.
- **Schema**: [report-schema.json](resources/report-schema.json)
- **Validation** (mandatory before reporting):
  ```bash
  node scripts/validate-findings.cjs findings.json
  node scripts/validate-coverage-ledger.cjs coverage-ledger.json
  ```

### Phase 5: Independent Record Verification
A fresh verifier performs a final source-trace confirmation on all `confirmed` records. Any material updates require re-validation.

### Phase 6: Reporting
Synthesize findings into clean, target-neutral markdown reports:
- `REPORT.md`: Executive summary, coverage statistics, risk breakdown.
- `FINDINGS-DETAIL.md`: Comprehensive technical details for confirmed vulnerabilities with root causes and smallest effective source fixes.
- `NEEDS-VALIDATION.md`: Items requiring runtime or environmental verification by repo owners.

---

## Severity Calibration

- **Critical**: Unauthenticated arbitrary code execution, full database takeover, or arbitrary tenant compromise.
- **High**: Defeats explicit security controls (e.g. auth bypass, cross-tenant read/write, stored XSS on sensitive origins).
- **Medium**: Real boundary violation with limited blast radius or uncommon preconditions.
- **Low**: Information disclosure of non-secret internals or low-gain logic anomalies.
- **Informational**: Minimal-impact hygiene observation.
- *(Note: `needs_validation` items carry NO severity until verified).*

---

## Anti-Patterns to Avoid
1. Do NOT report generic style deviations or missing defense-in-depth as vulnerabilities without a reachable boundary failure.
2. Do NOT guess external deployment configurations that are absent from the source.
3. Do NOT generate weaponized exploit code or attack payloads. Provide clear, minimal reproduction descriptions and defensive patches.
4. Do NOT deliver reports before both schema validators pass cleanly.
