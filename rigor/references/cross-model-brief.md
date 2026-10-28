# Rigor: Cross-Model Review Brief Template

> **Prime Directive: Models from one family share identical blindspots.**  
> Before critical changes land on the main branch, a secondary model family or independent subagent reviews the diff with focused, checkable questions.

---

## 1. Review Brief Template

When dispatching a review, generate a brief file using this structure:

```markdown
# Cross-Model Review Brief

## Target Change
- **Base Commit**: `<base_sha>`
- **Head Commit**: `<head_sha>`
- **Diff Package**: `<path_to_review_diff>`
- **Scope**: `<list of 2-5 core modified files>`

## Focus Questions (Checkable & Falsifiable)
1. Can function `X` fail silently or raise an unhandled exception when argument `Y` is nil/empty?
2. Does the database migration lock tables during standard transaction execution?
3. Which newly added branch in `Z` has no corresponding unit test?
4. Are any credentials, secrets, or unbounded input vectors left unvalidated?

## Constraints
- **Role**: Read-only reviewer.
- **Tools**: No file editing; no tool calls unless verifying specific documentation.
- **Output**: Single report file containing:
  - Confirmed Issues (with line references and reproduction steps)
  - Rejected Hypotheses (findings verified to be safe)
  - Questions for the Human Author
```

---

## 2. Strong vs Weak Review Questions

| Weak Question (Vague, Subjective) | Strong Question (Falsifiable, Checkable) |
|---|---|
| "Is this code clean?" | "Does `calculateDiscount()` handle negative prices without throwing?" |
| "Check for security issues." | "Can an unauthenticated request access `GET /api/v1/users/:id/export`?" |
| "Are there tests?" | "Which branch of `validateToken()` has no assertion in `test_auth.py`?" |

