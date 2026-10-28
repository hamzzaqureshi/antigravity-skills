# Design Token Architecture & Quality Gates

> How TypeUI / Awesome Design Skills structures tokens, accessibility compliance, component families, and quality gates.

---

## 1. Dual-File Anatomy

Each of the 67 design systems in this registry provides two synchronized files:

1. **`SKILL.md` (Agent Directive)**:
   - **Mission**: Defines the role and objective of the AI agent for that visual language.
   - **Style Foundations**: Typography scale, weights, colors, density modes, and metaphors.
   - **Accessibility Mandates**: WCAG 2.2 AA compliance, keyboard navigation, focus rings.
   - **Writing Tone & Voice**: Content guidance matching the aesthetic personality.
   - **Do / Don't Rules**: Concrete anti-patterns to avoid.
   - **Quality Gates**: Testable acceptance criteria for code review.

2. **`DESIGN.md` (Human & Machine Token Spec)**:
   - Frontmatter containing structured YAML tokens:
     - `colors`: `primary`, `secondary`, `success`, `warning`, `danger`, `surface`, `text`, `neutral`.
     - `typography`: `h1`, `body-md`, `label-caps`, `fontFamily`, `fontSize`, `weights`.
     - `rounded`: `sm`, `md`, `lg`, `full`.
     - `spacing`: `sm`, `md`, `lg`, density scale.
   - Human-readable design rationale and token explanations.

---

## 2. Using Tokens in Web Applications

Use `scripts/design_system.py export-css <slug>` to generate native CSS custom properties:

```css
/* Generated from Design System: Glassmorphism */
:root {
  /* Colors */
  --color-primary: #1856FF;
  --color-secondary: #3A344E;
  --color-success: #07CA6B;
  --color-warning: #E89558;
  --color-danger: #EA2143;
  --color-surface: #FFFFFF;
  --color-text: #141414;

  /* Typography */
  --font-primary: "Plus Jakarta Sans", sans-serif;
  --font-mono: "JetBrains Mono", monospace;

  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;

  /* Spacing */
  --space-sm: 8px;
  --space-md: 16px;
}
```

---

## 3. WCAG 2.2 AA Quality Gates

Every theme in the registry enforces:
- **Contrast Ratio**: 4.5:1 minimum for body text against surface; 3:1 for large display text and interactive controls.
- **Keyboard-First Focus**: Focus rings must be high-contrast and never disabled (`outline: none` without replacement is banned).
- **Reduced Motion**: All animations must degrade gracefully when `prefers-reduced-motion: reduce` is active.
