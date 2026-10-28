# Rigor: The Grounding Ladder

> **Prime Directive: Treat every fact that can change as a hypothesis.**  
> Pre-training knowledge degrades. External library interfaces, CLI flags, pricing, limits, and runtime versions must be grounded against primary sources.

---

## 1. The 5-Rung Verification Ladder

Climb the ladder until a primary source settles the fact:

| Rung | Target | Verification Method | Cost | Trust Level |
|:---:|---|---|:---:|:---:|
| **1** | **The Installed Tool** | `tool --version`, `tool --help`, one-line probe | Seconds | Highest |
| **2** | **Project Dependencies** | `package.json`, `poetry.lock`, local `.d.ts` / source code | Seconds | Very High |
| **3** | **Official Documentation** | Official developer docs, API reference, GitHub repo README | 1 min | High |
| **4** | **Maintainer Release Notes** | GitHub Releases, `CHANGELOG.md`, migration guides | 1 min | High |
| **5** | **Secondary Sources** | StackOverflow, blog posts, community tutorials | Variable | Low (Verify first) |

---

## 2. Facts That Require Grounding

Before generating code or stating facts, check if the statement falls into one of these classes:

1. **API Signatures**: Function arguments, return shapes, configuration keys.
2. **CLI Flags**: Option names, default values, subcommands.
3. **Version Compatibility**: Minimum Node/Python/Go version, deprecation warnings.
4. **Limits & Quotas**: Rate limits, max token context windows, file size caps.
5. **Pricing & Plans**: API costs, subscription tiers, free allowance boundaries.

---

## 3. Grounding Cache Rule

- **Within Session**: A verified source recorded in the current session may be reused without re-checking.
- **Across Sessions**: Assumed unverified; check again before building.

