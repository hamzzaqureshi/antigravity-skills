# Court Skill for Google Antigravity IDE

> **Stop AI Sycophancy.** Put your idea, technical proposal, architecture decision, or startup plan on trial in front of an adversarial panel of independent perspectives.

Adapted for **Google Antigravity IDE** from the original [court-skill](https://github.com/alexyc9381/court-skill) created by Alex Chen ([@nocodealex](https://instagram.com/nocodealex)).

---

## Highlights

- **Model Agnostic**: Works with **any model of choice** (Gemini 3/2.5 Flash/Pro, Claude, GPT-4o, etc.) configured in Antigravity IDE.
- **Universal Reusability**: Works for any project, domain, or context—software architecture, business decisions, refactoring proposals, marketing plans, or creative concepts.
- **Adversarial Deliberation**:
  - **Prosecutor**: Builds the strongest honest case that the proposal fails.
  - **Defense**: Builds the strongest honest case that the proposal works.
  - **Rebuttals**: Cross-examination of the opponent's strongest points.
  - **Jury of 12 Personas**: Independent evaluations from 12 distinct lenses (Accountant, Engineer, Competitor, First-Time Customer, Retired Judge, Investor, Lawyer, etc.).
  - **Presiding Judge**: Delivers a structured `VERDICT.md` containing charges that stuck, strengths, and **conditions for acquittal** (the highest-leverage actionable fixes to save the proposal).
- **Non-Invasive**: State is saved strictly inside `.court/` in your workspace. Your existing project source files are never modified.

---

## Installation

### Option 1: Global Installation (Recommended)
Make the skill automatically available in **every project and workspace** across your machine:

```bash
mkdir -p ~/.gemini/config/skills
cp -r court ~/.gemini/config/skills/
```

### Option 2: Project-Specific Installation
Include the skill directly inside a specific project repository to share with your team:

```bash
mkdir -p .agents/skills
cp -r court .agents/skills/
```

---

## How to Use

In any Antigravity conversation or prompt, trigger the court skill naturally:

```text
/court Rewrite our backend services in Go. We have a team of 3 Python developers and 6 months to deadline.
```

or simply:

```text
Put this architecture plan on trial: we are migrating our database from PostgreSQL to DynamoDB.
```

or:

```text
Don't just agree with me. Stress test my startup idea with a full jury trial.
```

### Flags Supported:
- `--jury N`: Run with 3 to 12 jurors (default: 12).
- `--quick`: Fast run with 6 jurors.
- `--seed S`: Fixes deterministic juror selection.

---

## Running the Unit Tests

```bash
python3 -m unittest discover -s tests
```

---

## Credits & License

- Original concept and implementation: **Alex Chen** ([@nocodealex](https://instagram.com/nocodealex), [chen.media](https://chen.media)).
- Adapted for Google Antigravity Customization Architecture.
- Licensed under the **MIT License**.
