# Anti-Vibecoding Skill for Google Antigravity IDE

> **The Anti-Slop Frontend Framework for AI Coding Agents.**
> Enforces intentional authorship, Fibonacci proportions, Swiss discipline, curated typography, and layered motion over generic AI-generated templates.

---

## The Problem: The Visual Grammar of AI Slop

A vibecoded website is technically functional, but betrays an unmistakable **lack of authorship**:
- Harsh purple-to-blue gradients
- Giant blurred radial orbs behind cards
- Dot-grid backgrounds as generic "tech atmosphere"
- Excessive glassmorphism and soft `rounded-3xl` corners on everything
- Sparkle icons pretending to mean intelligence
- Inter / Geist used without a typographic concept
- Bento grids with no content reason
- Identical 3-feature cards and fake testimonials
- Zero real product demonstrations

### The Litmus Test:
> **Remove the logo and name. Could someone still identify the product?**

---

## The 5-Layer Design Hierarchy

```text
Fibonacci    ──►  Structure & Proportion (1.618 : 1 workspace split)
Swiss        ──►  Discipline & Alignment (Grid precision, architectural dividers)
Editorial    ──►  Hierarchy & Typography (Curated type pairings, authentic voice)
Surrealism   ──►  Occasional Disruption (One element breaks the grid with intent)
Animation    ──►  Behavior & State (Motion for UI, GSAP for choreography)
```

---

## Features

1. **Automated Auditor (`audit.py`)**:
   Scan any HTML, CSS, JSX, TSX, Vue, or Svelte file for the 40 vibecoded signs and receive a 0–100 **Authorship Score** with exact line numbers and fixes:
   ```bash
   python3 scripts/audit.py src/
   ```

2. **The 40-Sign Anti-Slop Checklist**:
   Full reference cataloging visual, typographic, UI, animation, and content clichés in [`references/ANTI-SLOP-CHECKLIST.md`](references/ANTI-SLOP-CHECKLIST.md).

3. **Cognitive & Product Laws**:
   Translates 11 core laws (Hick's, Pareto, Occam's, Hanlon's, Parkinson's, etc.) directly into UI constraints in [`references/DESIGN-PRINCIPLES.md`](references/DESIGN-PRINCIPLES.md).

4. **Layered Motion System**:
   Clear boundaries between UI micro-interactions (Motion) and timeline choreography (GSAP) in [`references/MOTION-HIERARCHY.md`](references/MOTION-HIERARCHY.md).

5. **Curated Palettes & Typography**:
   Tested Swiss, Editorial, and Technical Night themes that ban default purple gradients in [`references/PALETTES-AND-TYPOGRAPHY.md`](references/PALETTES-AND-TYPOGRAPHY.md).

---

## Installation

### Global Installation (Available across all projects)
```bash
mkdir -p ~/.gemini/config/skills
cp -r anti-vibecoding ~/.gemini/config/skills/
```

### Project Installation
```bash
mkdir -p .agents/skills
cp -r anti-vibecoding .agents/skills/
```

---

## How to Trigger

In any Antigravity conversation:

- **Review existing UI**:
  ```text
  Audit my landing page in ./src/pages/index.tsx against the anti-vibecoding checklist.
  ```

- **Generate new UI**:
  ```text
  Design a dashboard for a network monitoring tool using Swiss x Editorial aesthetics and Fibonacci proportions. Avoid any generic AI vibecoding tropes.
  ```

- **Refactor generic UI**:
  ```text
  Refactor this hero section to make it look intentionally human-authored and remove all slop clichés.
  ```

---

## Running Scanner Tests

```bash
python3 -m unittest discover -s tests
```

---

## License

MIT License
