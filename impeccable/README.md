# Impeccable: Design Intelligence for AI Coding Agents

> **Stop Your Site Looking AI-Made.**
> 1 skill, 24 commands, live browser iteration, and 60+ deterministic detector rules for AI-generated frontend design. Adapted with first-class support for **Google Antigravity IDE**.

Created by [Paul Bakaus](https://www.paulbakaus.com), augmented with the **Creative Stack** (*ShaderGradient, Liquid Glass, Liquid Logo, React Three Fiber*).

---

## Why Impeccable?

Every AI model trained on the same SaaS templates. Without design guidance, agents reach for the exact same tells on every project:
- Inter for every font
- Purple-to-blue linear gradients
- Cards nested inside cards inside cards
- Faux-tech dot grids and glowing background orbs
- Rounded-square icon tiles above every heading

### What Impeccable Adds:
1. **Durable Product Truth (`PRODUCT.md`)**: `/impeccable init` learns your audience, operating context, voice, and real constraints once, so subsequent commands design for your actual product rather than generic templates.
2. **24 Professional Commands**: A complete design vocabulary covering layout, typography, color, motion, polish, critique, and audit.
3. **60+ Deterministic Detector Rules**: Pure Rust engine binary that catches 60+ classic AI design tells locally in **0ms** without consuming API tokens.
4. **The Creative Stack**: First-class patterns for 3D mesh gradients (**ShaderGradient**), real optical dispersion (**Liquid Glass**), fluid brand marks (**Liquid Logo**), and declarative 3D (**React Three Fiber**).

---

## The 24 Commands

| Command | Category | Description |
| :--- | :--- | :--- |
| `/impeccable init` | Setup | One-time setup: capture durable product context in `PRODUCT.md` |
| `/impeccable shape` | Build | Plan UX/UI before writing code |
| `/impeccable document` | Build | Generate root `DESIGN.md` design system from existing code |
| `/impeccable extract` | Build | Pull reusable tokens and components into your design system |
| `/impeccable critique` | Evaluate | UX design review with heuristic scoring |
| `/impeccable audit` | Evaluate | Technical quality checks (a11y, performance, responsive) |
| `/impeccable polish` | Refine | Final quality pass before shipping |
| `/impeccable bolder` | Refine | Amplify safe, timid, or bland designs |
| `/impeccable quieter` | Refine | Tone down aggressive, loud, or overstimulating designs |
| `/impeccable distill` | Refine | Strip to essence, remove unnecessary visual clutter |
| `/impeccable harden` | Refine | Production-ready: error states, i18n, text overflow, edge cases |
| `/impeccable onboard` | Refine | Design first-run flows, empty states, and activation paths |
| `/impeccable animate` | Enhance | Add purposeful motion and spring micro-interactions |
| `/impeccable colorize` | Enhance | Add strategic color to monochromatic or washed-out UIs |
| `/impeccable typeset` | Enhance | Fix font choices, typographic hierarchy, and proportions |
| `/impeccable layout` | Enhance | Fix spacing, rhythm, and visual alignment |
| `/impeccable delight` | Enhance | Add memorable touches and tactile personality |
| `/impeccable overdrive` | Enhance | Push past conventional limits (**ShaderGradient**, **Liquid Glass**, **R3F**) |
| `/impeccable clarify` | Fix | Improve UX copy, button labels, and error messages |
| `/impeccable adapt` | Fix | Adapt for mobile, tablet, and responsive breakpoints |
| `/impeccable optimize` | Fix | Diagnose and fix rendering performance |
| `/impeccable live` | Iterate | Pick elements in the browser and iterate on live alternatives |
| `/impeccable generate` | Iterate | Generate automated variants of a named element in the browser |
| `/impeccable craft` | Build | Full shape-then-build workflow |

---

## The Creative Stack Reference

Located in [`reference/creative-stack.md`](reference/creative-stack.md):
- **[ShaderGradient](https://github.com/ruucm/shadergradient)**: GPU-accelerated 3D fluid mesh gradients replacing flat CSS purple-blue gradients.
- **[Liquid Glass](https://github.com/dashersw/liquid-glass-js)**: Physical optical refraction, dispersion, and chromatic aberration replacing generic `backdrop-blur-md`.
- **[Liquid Logo](https://github.com/paper-design/liquid-logo)**: Interactive WebGL fluid distortion shaders for brand marks.
- **[React Three Fiber](https://github.com/pmndrs/react-three-fiber)**: Declarative, component-based 3D scenes without imperative Three.js lifecycle bugs.

---

## Standalone Detector CLI

Scan any directory, file, or URL with the zero-dependency bundled engine binary:

```bash
# Scan a directory
./scripts/impeccable detect src/

# Scan an HTML file
./scripts/impeccable detect index.html

# Output JSON
./scripts/impeccable detect --json src/
```

Catches 60+ anti-patterns:
- Purple-to-blue linear gradients
- Cards inside cards inside cards
- Blurred background radial orbs
- Gray text on colored buttons
- Overused fonts (Inter, Arial, system defaults without hierarchy)
- Cramped padding and small touch targets

---

## Installation in Antigravity IDE

### Global (All Projects)
```bash
mkdir -p ~/.gemini/config/skills
cp -r impeccable ~/.gemini/config/skills/
```

### Workspace Project-Specific
```bash
mkdir -p .agents/skills
cp -r impeccable .agents/skills/
```

---

## License

Apache-2.0 License. Created by [Paul Bakaus](https://www.paulbakaus.com).
