# Security Audit Skill for Google Antigravity IDE

> **Source-First, Coverage-Led Vulnerability Auditing.** Turns your Antigravity agent into an adversarial, evidence-grounded security auditor.

Adapted for **Google Antigravity IDE** from [Cloudflare's security-audit-skill](https://github.com/cloudflare/security-audit-skill).

---

## Highlights

- **Model Agnostic**: Compatible with any model in Antigravity IDE (Gemini 3/2.5 Pro/Flash, Claude, GPT-4o, etc.).
- **Dual Operating Modes**:
  - **Guidance Mode**: Fast, focused answers to security questions and targeted file reviews without creating files.
  - **Full Audit Mode**: Systematic 6-phase audit lifecycle generating machine-validated findings and comprehensive remediation reports.
- **Evidence-Grounded**:
  - Distinguishes **Confirmed** (fully demonstrated boundary violation), **Needs Validation** (blocked by unverified environmental facts), and **Rejected** (disproven leads).
  - Adversarial validation: Candidate findings are cross-verified by independent review perspectives.
  - No checklist spam: Missing defense-in-depth is treated as hardening advice, not vulnerabilities.
- **Zero-Dependency Validators**:
  - Validates `coverage-ledger.json` and `findings.json` using pure Node.js scripts and `report-schema.json`.
- **Safe & Non-Destructive**: Target source code is strictly read-only. Isolated scratch testing.

---

## 6-Phase Audit Lifecycle

1. **Reconnaissance**: Map system architecture, entry points, and deterministic coverage units into `architecture.md` and `coverage-ledger.json`.
2. **Coverage-Led Hunting**: Assign focused review passes across ledger units using the attack class companions (`WEB-PROTOCOL-AND-AUTH.md`, `CLOUD-AND-DEPLOYMENT.md`, `AI-AND-LLM.md`, etc.).
3. **Candidate Validation**: Independent verification perspectives attempt to disprove or boundedly confirm each candidate.
4. **Structured Output**: Compile verified findings into `findings.json` and validate against `report-schema.json`.
5. **Independent Record Verification**: Final confirmation of source traces and evidence.
6. **Target-Neutral Reporting**: Generate executive summaries and remediation blueprints (`REPORT.md`, `FINDINGS-DETAIL.md`, `NEEDS-VALIDATION.md`).

---

## Installation

### Global Installation (Recommended)
Available in **every project** across Antigravity IDE:

```bash
mkdir -p ~/.gemini/config/skills
cp -r security-audit ~/.gemini/config/skills/
```

### Project-Specific Installation
Committed into a single project repository:

```bash
mkdir -p .agents/skills
cp -r security-audit .agents/skills/
```

---

## How to Trigger

In any Antigravity conversation:

- **Quick Review**:
  ```text
  Check if this authentication middleware has any security flaws or timing issues.
  ```

- **Full Codebase Audit**:
  ```text
  Run a security audit on this codebase and generate the audit report.
  ```

- **Scoped Review**:
  ```text
  Audit our cloud deployment and API routes in ./src/api for security vulnerabilities.
  ```

---

## Running Validator Tests

```bash
node tests/run-tests.cjs
```

---

## Credits & License

- Original research and architecture: **Cloudflare Security AI Research** ([cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill)).
- Adapted for Google Antigravity Customization Architecture.
- Licensed under the **MIT License**.
