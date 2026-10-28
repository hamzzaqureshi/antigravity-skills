# Contributing to Antigravity Skills Suite

Thank you for your interest in contributing to the **Antigravity Skills Suite**! This project provides a production-grade, model-agnostic library of AI coding skills designed for Google Antigravity, Claude Code, Codex, and other LLM agent harnesses.

---

## Guiding Principles

1. **Model-Agnostic & Zero External Dependencies**:
   - Helper scripts and engines MUST use the standard library only (pure Python standard library or native Node.js).
   - Avoid external `pip` or `npm` runtime dependencies to ensure instant installation across any environment.
2. **Progressive Disclosure**:
   - Keep `SKILL.md` entrypoints concise and dense with YAML frontmatter.
   - Place specialized references, token dictionaries, and deep technical specs in `references/` so the agent reads them strictly on-demand.
3. **Empirical Verification (100% Pass Rate)**:
   - Every skill must have an automated test suite discoverable via standard `unittest` (`python3 -B -m unittest discover -s tests`).
   - Run `python3 -B test_all.py` before submitting any changes.

---

## Directory Structure for New Skills

Every skill must conform to the following directory layout:

```text
<skill-name>/
├── SKILL.md             # [Required] Concise agent entrypoint with YAML frontmatter
├── README.md            # [Required] Quickstart, commands, and usage documentation
├── LICENSE              # [Required] Open-source license (MIT / Apache-2.0)
├── .gitignore           # [Required] Clean exclusion of local cache/logs
├── references/          # [Required/Optional] In-depth guides and progressive disclosure
├── scripts/             # [Required/Optional] Zero-dependency Python CLI or engine
├── resources/           # [Optional] Offline data, templates, or schemas
└── tests/               # [Required] Automated unit tests
```

---

## Step-by-Step: Adding a New Skill

1. **Create the Skill Directory**:
   ```bash
   mkdir -p <skill-name>/{scripts,references,tests}
   ```

2. **Author `SKILL.md`**:
   Ensure it includes valid YAML frontmatter:
   ```markdown
   ---
   name: <skill-name>
   description: "Concise summary of what the skill does and when the agent should invoke it."
   ---
   ```

3. **Author Automated Tests**:
   Create `tests/test_<skill_name>.py` using standard Python `unittest`.

4. **Register the Skill**:
   Add the skill to:
   - `install.py` (`SKILLS` array)
   - `install.sh` (`SKILLS` array)
   - `package.py` (`SKILLS` array)
   - `test_all.py` (`SUITES` array)
   - `README.md` (Skills Matrix & Cheat Sheet)

5. **Verify Zero Defects & Zero Drift**:
   ```bash
   # Run all test suites in parallel
   python3 -B test_all.py

   # Sync to global environment
   python3 -B install.py

   # Rebuild release archives
   python3 -B package.py
   ```

---

## Hygiene & Cleanliness Rules

- **Zero Bytecode Debris**: Always run Python with `-B` (`python3 -B`) or `PYTHONDONTWRITEBYTECODE=1` to prevent `.pyc` and `__pycache__` clutter.
- **Zero Hardcoded Paths**: Never hardcode developer home paths (like `/home/username/`). Always resolve relative to `Path(__file__).resolve().parent`.
- **Formatting**: Format code with standard Python conventions and Markdown with GitHub-flavored Markdown.

