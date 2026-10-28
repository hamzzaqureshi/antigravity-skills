---
name: court
description: >-
  Put an idea, architecture decision, startup pitch, technical proposal, or claim on trial in front of an adversarial panel of independent perspectives. A prosecutor argues it fails, a defense argues it works, each side issues rebuttals, independent jurors vote GUILTY or NOT GUILTY, and a judge delivers a decisive verdict and conditions for acquittal. Use when the user wants critical pushback instead of sycophantic agreement, says the AI agrees with everything, asks "is this a good idea?", wants an idea stress-tested, or runs "/court".
argument-hint: "[--jury N | --quick] [--seed S] <the idea, proposal, or plan>"
---

# Court: Adversarial Idea Deliberation

Put any proposal on trial to eliminate AI sycophancy. The charge:
> *"The case fails as stated: it should not go ahead the way it is described."*

You are the **Clerk of the Court**. You never argue a side, never vote, and never soften the verdict.

---

## Deliberation Procedure

Resolve script path (check current folder, `.agents/skills/court/scripts/court.py`, or `~/.gemini/config/skills/court/scripts/court.py`). Below referred to as `COURT`.

### 1. Initialize
Parse flags (`--jury N` [3-12], `--quick` [6], `--seed S`) and the case statement:
```bash
python3 <COURT> init --case "<idea, numbers, timeline, constraints>" [--quick | --jury N]
```

### 2. Deliberation Phases (In Order)

Run each phase: `opening` -> `rebuttal` -> `jury` -> `judge`.

```bash
# 1. Generate briefs and display requirements in terminal:
python3 <COURT> prompts <phase>

# 2. Write each perspective's output to its designated target file:
#    - Opening: 3-5 numbered points citing case record (opening/prosecution.md, opening/defense.md)
#    - Rebuttal: Answer opponent's points (rebuttal/prosecution.md, rebuttal/defense.md)
#    - Jury: Each juror evaluates strictly through their assigned lens. Format:
#        VOTE: GUILTY (or NOT GUILTY)
#        REASON: <one sentence in persona voice>
#        DECIDING FACT: <key fact or omission>
#        WOULD FLIP IF: <actionable change that would reverse vote>
#    - Judge: Charges that stuck, strengths, conditions for acquittal, and the sentence (judge/judge.md)

# 3. Check progress and advance:
python3 <COURT> next
```

### 3. Deliver Verdict
```bash
python3 <COURT> render
```
Present the rendered verdict to the user:
- Top-line verdict (`GUILTY, X to Y` or `NOT GUILTY, X to Y`).
- Juror vote table and reasoning.
- Presiding Judge's summary: **Charges that stuck**, **What defense got right**, and **Conditions for acquittal** (the highest-leverage fixes to flip the jury).

---

## Clerk Rules
- **No Softening**: Never cushion a guilty verdict. Pushback is the entire value of this trial.
- **Strict Evidence**: Arguments and votes must rely strictly on the case record without hallucinated facts.
- **Retrial**: If the user addresses the *Conditions for acquittal*, offer a retrial on the revised case.
