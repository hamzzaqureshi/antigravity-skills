---
name: anti-vcode
description: >-
  Static code scanner and diagnostic auditor that detects 40 patterns of AI slop ("vibecoding") in existing HTML/CSS/React code and enforces Swiss/Editorial typographic and grid discipline. Use when scanning or linting codebases for generic AI aesthetics, evaluating frontend code against the 40-sign anti-slop scorecard, applying Fibonacci/golden ratio hierarchy, or running "/anti-vcode". Not for generating initial design specs or searching token registries.
argument-hint: "[--audit | --design | --refactor] <target file, directory, or design prompt>"
license: MIT
metadata:
  author: "Google Antigravity Taste Engineering"
  version: "1.0.1"
---

# Anti-Vibecoding: Frontend Taste & Intentional Design

Eliminate the generic visual grammar of AI-generated websites. A vibecoded interface is technically competent but betrays an unmistakable **lack of authorship**:
> *Gradient hero ──► floating cards ──► unearned bento ──► fake testimonials ──► 3 pricing tiers ──► CTA.*

### The Litmus Test
> **Remove the logo and name. Could someone still identify the company or product?**
> If the answer is no, the interface is generic AI slop.

---

## Operating Modes

### 1. Audit Mode (Diagnostic)
When asked to evaluate or review existing frontend code:
```bash
python3 <skill-dir>/scripts/audit.py <path-to-file-or-directory> [--json]
```
The auditor checks the 40 anti-patterns, scores the code from 0 to 100 ("Authorship Score"), and outputs line-by-line remediation advice.

### 2. Design & Build Mode (Generative)
When creating or refactoring interfaces, reject the generic AI defaults and apply the 5-layer intentional design hierarchy:

```text
Fibonacci    ──►  Structure & Proportion (1.618 : 1 workspace split)
Swiss        ──►  Discipline & Alignment (Grid precision, architectural dividers)
Editorial    ──►  Hierarchy & Typography (Curated type pairings, authentic voice)
Surrealism   ──►  Occasional Disruption (One element breaks the grid with intent)
Animation    ──►  Behavior & State (Motion for UI, GSAP for choreography)
```

---

## The Pre-Flight Anti-Slop Ban List

Before outputting any code, verify against the **[40-Point Anti-Slop Checklist](references/ANTI-SLOP-CHECKLIST.md)**:

1. **NO Purple-to-Blue Gradients**: Banned. Use solid tonal surfaces, crisp architectural hairlines, or single signal accents.
2. **NO Radial Gradient Blurs / Orbs**: Do not float blurred color spheres (`blur-3xl`) behind cards to fill space.
3. **NO Dot-Grid Backgrounds**: Do not use repeated 1px dot patterns as faux "tech atmosphere".
4. **NO Excessive Glassmorphism**: Avoid stacking `backdrop-blur` and translucent cards. Use crisp, opaque surfaces.
5. **NO Soft Corner Radius Spam**: Ban `rounded-2xl` / `rounded-3xl` on everything. Use restrained radii (`4px - 8px`).
6. **NO Sparkle Icons (/ )**: Never use sparkle icons to fake "intelligence". Show actual product workflows.
7. **NO Unearned Bento Grids**: Do not force mismatched stats into bento boxes without informational necessity.
8. **NO Undifferentiated Inter Defaults**: Pair distinct display letterforms with disciplined body/mono fonts (see [PALETTES-AND-TYPOGRAPHY.md](references/PALETTES-AND-TYPOGRAPHY.md)).
9. **NO Buzzword Copy**: Ban *"Transform your workflow with the future of..."* Write concrete product facts.
10. **NO Unjustified 3D / Particles**: Never add spinning chrome cubes or canvas particle fields.

---

## Structural Implementation Rules

### 1. Fibonacci Proportion & Layout
- **Main : Secondary Content Split**: `1.618 : 1` (roughly 62% primary workspace / 38% auxiliary panel).
- **Hero / Content Split**: 60–62% primary visualization/interactive preview, 38–40% controls/copy.
- **Mathematical Type Scale**:
  `12px` (metadata) ──► `14px` (sub-ui) ──► `16px` (base) ──► `26px` (title) ──► `42px` (section) ──► `68px` (hero).
- **Asymmetric Balance**: Center the global container in the viewport, but balance internal elements asymmetrically.

### 2. Layered Motion Hierarchy
Consult **[MOTION-HIERARCHY.md](references/MOTION-HIERARCHY.md)**:
- **Motion (Framer Motion)**: Owns UI states and component micro-interactions (fast deceleration, `< 200ms`).
- **GSAP**: Owns multi-step timeline sequences and pinned scroll choreography.
- **Three.js**: Used **strictly** when 3D is a core product feature (data topology, spatial map).
- **Lenis**: Used only when full page relies on scroll-scrubbed timeline orchestration.
- **BAN**: Aimless floating particles, glowing cursor beams, and universal viewport fade-ins on every section.

### 3. Grounding in Product & Cognitive Laws
Consult **[DESIGN-PRINCIPLES.md](references/DESIGN-PRINCIPLES.md)**:
- **Hick's Law**: One clear primary action instead of 10 concurrent choices.
- **Pareto Principle**: Surface the vital 20% of controls; push edge cases deeper.
- **Occam's Razor**: One intuitive control beats 3 buttons, a dropdown, and a modal.
- **Dunning-Kruger Safeguards**: Reversible actions, consequence warnings, undo states.
