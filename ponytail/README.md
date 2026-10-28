# Ponytail: The Lazy Senior Dev

> The best code is the code you never wrote. Makes your AI agent think like the laziest senior dev in the room.

Ponytail enforces ruthless engineering restraint: the smallest complete diff that solves the whole task, reusing existing helpers, standard libraries, and native platform features while eliminating speculative abstractions and YAGNI bloat.

---

## Quick Reference

| Level | Trigger | Behavior |
| :--- | :--- | :--- |
| **lite** | `/ponytail lite` | Build what was asked, but name the smaller option in one line and let the user choose. |
| **full** | `/ponytail` | (Default) Minimal complete diff, zero over-engineering, test risky logic, name skipped work and risks. |
| **ultra** | `/ponytail ultra` | Questions the request aggressively; pushes back before building anything not strictly justified. |

---

## Workflows & Commands

### 1. Code Review (`/ponytail-review`)
Reviews the current diff or recent change like the senior dev who gets paged when it breaks:
- Order: Correct -> Safe -> Holds under load -> Tested -> Fast -> Lean.
- Categorizes findings into `Must fix`, `Should fix`, and `Nice to have`.

### 2. Repo Audit (`/ponytail-audit`)
One-shot quality audit of the entire repository for bugs, security holes, scalability limits, missing tests, and dead code to delete or merge.

### 3. Debt Ledger (`/ponytail-debt`)
Scans the codebase for all `shortcut:` comments naming ceiling limits and upgrade paths:
```bash
python3 scripts/debt.py
```

### 4. Gain Scoreboard (`/ponytail-gain`)
Displays the measured benchmark impact scoreboard:
```bash
python3 scripts/gain.py
```

---

## License
MIT License.

