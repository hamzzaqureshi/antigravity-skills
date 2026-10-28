# Rigor: Completion Gate & Evidence Table Reference

The Completion Gate enforces a strict rule:
> **NO CLAIM OF DONE, FIXED, OR PASSING WITHOUT FRESH VERIFICATION OUTPUT IN THIS MESSAGE.**

---

## 1. The Evidence Table Format

Whenever asserting that work is complete, fixed, tested, or ready, include an Evidence Table in your response:

| Claim | Command or Check | Result (Observed in This Message) | Status |
|---|---|---|---|
| All unit tests pass | `pytest tests/` | `24 passed, 0 failed in 0.42s, exit 0` | Verified |
| Linter / style clean | `flake8 .` | `0 errors, 0 warnings, exit 0` | Verified |
| Issue #42 reproduced & fixed | `python test_repro.py` | `AssertionError before; exits 0 after fix` | Verified |
| Documentation up to date | `git diff docs/` | `Updated API signatures and flags` | Verified |

---

## 2. What Counts as Proof vs What Does NOT

| Category | Real Proof (Passes Gate) | Fake Claim (Fails Gate) |
|---|---|---|
| **Test Suite** | Full test command executed in this step, exit 0, test count displayed | "Tests should pass now", "I ran them earlier" |
| **Bug Fix** | Reproduction script fails without fix and passes with fix | "The logic looks correct now", "Fixed the typo" |
| **Types & Lint** | Clean output from `tsc --noEmit`, `mypy`, `eslint` in current turn | "No red squiggly lines in the editor" |
| **Build** | Compiler output: `Built in 1.2s, 0 errors` | "The syntax is valid", "No syntax errors found" |
| **Subagent Output**| Parent agent executes independent verification check | Blindly forwarding "Subagent reported done" |

---

## 3. The 7-Step Protocol

1. **Name the claim**: State what you intend to assert ("Bug #12 fixed", "Auth module ready").
2. **Name the proof**: Identify the exact command that proves or disproves the claim.
3. **Run the check**: Execute the check via tool execution now.
4. **Read the raw output**: Inspect exit code, passed/failed counts, and log tail.
5. **Compare**: If the output contradicts the claim, state the failure and fix it.
6. **Populate the Evidence Table**: Insert the raw facts into the table.
7. **Make the claim**: Only now emit the completion assertion.

