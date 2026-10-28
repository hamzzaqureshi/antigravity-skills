# Maintenance, Evolution & Documentation Lifecycle

> "A README is not a one-time launch artifact. It is a living, maintained component of your codebase."

---

## The Documentation Lifecycle

As projects grow from solo prototypes into multi-contributor systems, documentation needs evolve:

```text
Phase 1: Prototype ──────▶ Phase 2: Open Source / MVP ──────▶ Phase 3: Mature Ecosystem
(Single-file README)      (README + Architecture + Tests)    (README Entrypoint + Docs Site)
```

### When to Split into a Dedicated Documentation Site
A README should remain the **entrypoint**, not an encyclopedia. Move content to a documentation site (Docusaurus, VitePress, MkDocs, Read the Docs) when:
- API references exceed 300 lines of markdown.
- You have multiple distinct user personas (e.g., end-user tutorials vs plugin developer specs).
- You need multi-version documentation (v1 vs v2).
- The README exceeds 800 lines or takes more than 3 scroll screens to reach installation.

Keep the README as the front door: summary, quickstart, and direct links to the deep-dive docs site.

---

## Automated Documentation Testing in CI

Documentation rots unless verified by automated pipelines.

### 1. Markdown Linting
Enforce formatting standards using `markdownlint` or `oxlint`:
- No trailing whitespace.
- Heading levels increment by one level at a time (`#` -> `##` -> `###`).
- Fenced code blocks must declare a language.

### 2. Relative Link Verification
Ensure every markdown link (`[Guide](./docs/guide.md)`) points to a file that actually exists in Git:

```bash
# Automated check using Python or markdown-link-check
python3 scripts/readme_audit.py README.md --check-links
```

### 3. Example Command Smoke Testing
For critical projects, execute the README quickstart command inside GitHub Actions:

```yaml
name: Test README Quickstart
on: [push, pull_request]
jobs:
  smoke-test-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run README quickstart command
        run: |
          pip install -e .
          python main.py --help
```

---

## Monorepo README Hierarchies

In monorepos (`packages/`, `apps/`, `crates/`):
- **Root README:** Explains the overall project vision, repository organization, monorepo tooling (`turbo`, `pnpm`, `nx`, `cargo`), workspace build steps, and contributing guide.
- **Package README:** Self-contained guide for that specific package (installation, package-specific API, minimal usage). Someone viewing that package on npm or PyPI will see its dedicated README.

---

## Deprecations & Project Status

Be candid about project health. If a project is archived or looking for maintainers, add a prominent status notice at the very top:

```markdown
> [!WARNING]
> **Project Status: Archived / Inactive**
> This repository is no longer actively maintained. For active forks, see [Project Alternative](https://github.com/...).
```
