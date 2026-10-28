---
name: designs
description: >-
  Curated registry of 67 design system themes and token foundations (TypeUI / Awesome Design Skills). Features instant token lookup, component rules, typography scales, color palettes, and accessibility constraints across 67 aesthetic families (Bento, Glassmorphism, Brutalism, Claymorphism, Dithered, Editorial, Neobrutalism, Riso, Terracotta, Neon, Retro, etc.). Use when styling components, picking design system tokens, or running "/designs", "/design-system", or "/design-systems".
argument-hint: "[list | search | tokens | export-css | inspect] <theme-slug>"
---

# Design Systems Registry: 67 Themed Design Systems

> A curated catalog of 67 complete design systems for AI-powered agents, providing strict `SKILL.md` agent rules and `DESIGN.md` token foundations across every major visual aesthetic.

You are the **Design System Architect**. When asked to style a web application, landing page, or UI component with a distinct visual language, you reach into this registry to extract exact tokens, typography pairings, color harmonies, and accessibility constraints.

---

## 1. Quick CLI Integration

The offline standard-library CLI is located at:
`scripts/design_system.py` (or `~/.gemini/config/skills/design-systems/scripts/design_system.py`).
Referred to below as `DS`.

```bash
# List all 67 themes
python3 <DS> list

# Search for a specific aesthetic (e.g. brutalism, glass, cyber, retro)
python3 <DS> search <query>

# View tokens for a specific theme
python3 <DS> tokens <slug>

# Export CSS variables directly
python3 <DS> export-css <slug> [--output style.css]

# Inspect full AI guidance and component rules
python3 <DS> inspect <slug>
```

---

## 2. Core Aesthetic Categories

The registry provides 67 distinct themes grouped into major visual families:

### A. Modern Product & Clean
- **`clean`**: Ultra-minimal, high-contrast, product-focused.
- **`bento`**: Apple-style modular card grids with asymmetric rhythm.
- **`sleek`**: Polished modern dark-mode interface with subtle borders.
- **`spacious`**: Airy layout with generous whitespace and breathable hierarchy.
- **`shadcn`**: Accessible component primitives with neutral palettes.
- **`modern`**: Balanced contemporary SaaS design.

### B. Tactile & Physical Metaphors
- **`glassmorphism`**: Translucent frosted glass layers with luminous borders.
- **`claymorphism`**: Soft 3D inflated pillowy buttons and playful shadows.
- **`neumorphism`**: Soft extruded surface shadows and debossed insets.
- **`paper`**: Textured stationery aesthetic with warm deckle-edge accents.
- **`skeumorphism`**: Realistic physical materials, leather, and metal textures.

### C. Bold, Raw & Subversive
- **`brutalism`**: Hard mechanical Swiss typography, raw black borders, 0px radius.
- **`neobrutalism`**: High-contrast black outlines with saturated pop colors and hard drop shadows.
- **`mono`**: Monospace terminal aesthetics and technical telemetry.
- **`neon`**: Cyberpunk glowing accents against deep obsidian surfaces.
- **`dithered`**: Retro bitmap dithering and vintage computer graphics.

### D. Cultural, Vintage & Nostalgic
- **`retro`**: Warm 80s/90s computing aesthetics and CRT scanline nostalgia.
- **`riso`**: Risograph spot-color printing, grain textures, and paper overlap.
- **`terracotta`**: Earthy Mediterranean ceramic tones and warm artisanal craft.
- **`cafe`**: Warm inviting coffee-house tones and comfortable serif typography.
- **`sega` / `pacman` / `tetris`**: Arcade gaming visual languages and 8-bit accents.

### E. Corporate & Enterprise
- **`enterprise`**: High-density analytics, structured tables, and subdued tokens.
- **`corporate`**: Polished blue-chip credibility with conservative hierarchies.
- **`professional`**: Clean executive presentation and clear data displays.
- **`ant`**: Enterprise financial table layout following Ant Design principles.
- **`material`**: Google Material Design 3 tokens and reactive state.

---

## 3. Workflow for Styling Applications

1. **Select or Infer Theme**:
   - Match the user's brief against the 67 themes using `python3 <DS> search "<vibe>"`.
2. **Extract Tokens**:
   - Run `python3 <DS> export-css <slug>` to generate the CSS custom properties.
   - Insert `:root { ... }` into the project stylesheet (`index.css` or `globals.css`).
3. **Review Guidelines & Quality Gates**:
   - Check `python3 <DS> inspect <slug>` for the theme's specific Do/Don't rules, typography hierarchy, and WCAG AA requirements.
4. **Build Components**:
   - Style buttons, cards, navigation, and hero sections strictly adhering to the theme's token palette and corner radius scales.

---

## 4. References & Catalog

- **Complete Theme Table (67 Themes)**: [references/THEME-REGISTRY.md](references/THEME-REGISTRY.md)
- **Token Architecture & WCAG Gates**: [references/TOKEN-ARCHITECTURE.md](references/TOKEN-ARCHITECTURE.md)
- **Theme Index Map**: [resources/index.json](resources/index.json)
