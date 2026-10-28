# Court Skill Architecture & Extension Guide

The **Court Skill** is an adversarial multi-perspective deliberation framework adapted for Google Antigravity IDE. It combats LLM sycophancy (the tendency for AI models to agree with whatever the user proposes) by forcing an adversarial trial before an independent panel of jurors.

## Core Principles

1. **Model Independence**: Works identically regardless of what LLM powers Antigravity IDE (Gemini Flash/Pro, Claude Sonnet/Opus, GPT-4o, DeepSeek, or local models).
2. **Deterministic Bookkeeping**: State, briefs, phases, vote parsing, and tallying are driven by `scripts/court.py` using standard Python 3 with zero external dependencies.
3. **Strict Separation of Concerns**:
   - Case details live in `.court/case.md`.
   - Each role is isolated: Prosecution, Defense, Jurors, and Judge receive only the evidence in the record.
   - Jurors vote blindly and independently through distinct cognitive lenses.
4. **Safety & Non-Invasiveness**:
   - All trial state is saved inside `.court/` in the project root.
   - Project source files are never altered.

## Customizing Jurors

The standard jury panel lives in `resources/jurors.json`. You can create specialized jury panels for specific domains by passing `--jurors-file <path>` to `court.py init`.

### Example: Software Architecture Jury Panel
```json
[
  {"name": "The SRE / On-Call Engineer", "lens": "You are paged at 3 AM when things break. What makes this fragile in production, how will it be monitored, and what is the recovery path?"},
  {"name": "The Security Auditor", "lens": "You look for attack vectors, privilege escalation, dependency risks, and compliance exposures."},
  {"name": "The Junior Developer", "lens": "How steep is the learning curve? Can someone contribute safely in their first week without breaking things?"},
  {"name": "The Product Manager", "lens": "How does this delay customer-facing features? Does the user experience improve, or is this engineering vanity?"},
  {"name": "The Cost Optimizer", "lens": "What does this do to cloud infrastructure bills, licensing fees, and continuous integration runtime?"},
  {"name": "The Tech Lead", "lens": "Will the team still maintain this in two years, or will this become abandoned tech debt?"}
]
```

## CLI Reference

```bash
# Preview trial steps
python3 court.py plan [--jury N | --quick]

# Start a trial
python3 court.py init --case-file .court/case.md [--jury N] [--seed S] [--jurors-file PATH]

# Phase management
python3 court.py prompts <phase>    # Write briefs for current phase
python3 court.py check <phase>      # Check missing outputs
python3 court.py next               # Inspect current phase & print next step
python3 court.py status             # Summary table of all 4 phases

# Deliberation outcome
python3 court.py tally              # Output current vote count
python3 court.py render             # Generate and print final VERDICT.md
```
