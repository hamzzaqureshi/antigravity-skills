# The 50-Point README Quality Scorecard

Use this diagnostic rubric to evaluate any README. Score each of the 10 dimensions from `0` (missing / broken) to `5` (flawless / exemplary) for a total score out of **50 points**.

---

## Scorecard Dimensions

| Category | Description | 0 Points | 3 Points | 5 Points |
| :--- | :--- | :--- | :--- | :--- |
| **1. Purpose & Audience** | Clear problem statement, target audience, and value proposition. | Unclear what project does or who it is for. | Basic description present, but lacks positioning. | Immediate, compelling hook explaining problem and unique solution. |
| **2. Structure & Navigation** | Logical heading hierarchy, scannable layout, Table of Contents if long. | Random wall of text; skipped heading levels. | Standard sections present; minor scanability gaps. | Pristine information architecture, quick-jump links, clear visual hierarchy. |
| **3. Accuracy** | Real paths, valid commands, current version references. | Obvious copy-paste errors or outdated versions. | Mostly correct; minor syntax or version lag. | 100% verified against current active repository. |
| **4. Installation** | Reproducible setup instructions from a clean environment. | Missing commands, assumed global tools, fails in clean VM. | Works but requires guessing an unstated dependency. | Deterministic, multi-platform, verified clean-install protocol. |
| **5. Usage** | Actionable, copy-pasteable examples with expected outputs. | No examples or incomplete snippets that cannot run. | Basic example present without expected output. | Minimal working snippet (<10 lines) + real command and expected stdout. |
| **6. Technical Explanation** | Architecture diagrams, component relationships, data flow. | Black box with zero explanation of internals. | Text description of files or components. | Visual diagram (Mermaid/ASCII) + port mappings + data pipeline flow. |
| **7. Readability** | Concise prose, code block language tags, scannable formatting. | Bloated prose, untagged code blocks, poor grammar. | Readable but verbose; occasional walls of text. | Tight, punchy prose; code blocks tagged; scannable tables & bullet points. |
| **8. Visual Communication** | Screenshots, terminal recordings, purposeful badges. | No visuals or broken image links. | Decorative screenshots without annotation. | High-resolution cropped UI demo or terminal recording; high-signal badges. |
| **9. Trust & Completeness** | Testing commands, license, known limitations, contributing guide. | Missing license; zero tests; claims 100% perfection. | License present; basic test command documented. | Explicit license; test commands; candid disclosure of limitations. |
| **10. Maintainability** | Verified relative links, .env templates, no dead placeholders. | Broken links; unedited `TODO` or `YOUR_KEY` markers. | Links work; some manual maintenance required. | All relative links verified; clean `.env.example`; zero placeholder residue. |

---

## Grading Scale

- **45 – 50 (Grade A - Production Masterpiece):** Ready for viral open-source release, executive presentation, or flagship portfolio.
- **38 – 44 (Grade B - High Quality):** Solid, dependable documentation. Minor polish needed on visual hierarchy or edge cases.
- **30 – 37 (Grade C - Needs Work):** Usable by experienced developers, but full of friction for newcomers. Missing expected outputs or diagrams.
- **Below 30 (Grade F - Defective):** Broken commands, missing setup steps, or unmaintained placeholders.

---

## Critical Defect Gates

Regardless of the total numerical score, any of the following triggers an **immediate rejection**:
1. **Broken Installation Command:** A new user running the commands in a clean shell hits a syntax error or missing package.
2. **Hardcoded Secrets:** Committing real API keys, tokens, or credentials in configuration examples.
3. **Ghost Placeholders:** Leaving `TODO`, `<your-username>`, or `foo/bar` unreplaced in instructions.
4. **Missing License:** Ambiguity over open-source usage rights.
