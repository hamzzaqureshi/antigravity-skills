# Design Principles & Mental Models

How to ground frontend interfaces in rigorous structural principles and product laws instead of aesthetic imitation.

---

## The Structural Hierarchy

To build interfaces that feel human-authored and intentional, structure the design system through five distinct layers:

```text
Fibonacci    ──►  Structure & Proportion (Geometry)
Swiss        ──►  Discipline & Alignment (Grid)
Editorial    ──►  Hierarchy & Typography (Voice)
Surrealism   ──►  Occasional Disruption (Identity)
Animation    ──►  Behavior & State (Motion)
```

### 1. Fibonacci: Structural Proportion
Use the **Golden Ratio (1.618)** and Fibonacci sequences for spatial relationships, not decorative spiral graphics.
- **Main : Secondary Content**: `1.618 : 1` (roughly 62% primary workspace / 38% auxiliary panel).
- **Hero Split**: Primary visual/action occupies ~62%, controls/details occupy ~38%.
- **Typographic Scale**: Adhere to deliberate ratios (e.g., `16px -> 26px -> 42px -> 68px`) rather than arbitrary steps.
- **Asymmetric Balance**: Center the global container in the viewport, but balance internal elements asymmetrically according to visual weight.

### 2. Swiss: Discipline & Precision
- **Strict Grid Alignment**: Every element snaps to a predictable column or baseline grid.
- **Restraint Over Decoration**: Negative space serves comprehension, not decoration.
- **Neutral Framing**: Allow content to be the hero, framed by quiet, functional borders and dividers.

### 3. Editorial: Distinctive Voice & Hierarchy
- **Typography-Led Identity**: Pair typefaces with intention (e.g., high-contrast serif with refined geometric grotesque, or humanist sans with utilitarian mono).
- **Content Density**: Important data gets generous spatial breathing room; supporting metadata is tight, legible, and subordinate.

### 4. Surrealism: Controlled Disruption
- **Breaking the Grid**: Allow exactly one key element (e.g., an architectural diagram, a focal interactive preview) to break the container boundary or cross a section seam.
- **Unconventional Metaphors**: Replace generic cards with metaphors true to the domain (ledger sheets, blueprint layers, physical cards, command palettes).

---

## The 11 Product & Cognitive Laws for UI

### Cognitive Laws
1. **Hick's Law** (*Decision time increases logarithmically with options*):
   - Never feature-dump. Replace 10 concurrent buttons with a single primary entrypoint that progressively discloses options.
2. **Occam's Razor** (*Prefer the simplest sufficient solution*):
   - If one intuitive control solves the user's intent, do not build three buttons, a dropdown, and a modal.
3. **Dunning-Kruger Safeguards** (*Limited knowledge causes overconfidence*):
   - Implement reversible actions, safety previews, undo states, and explicit consequence warnings on destructive operations.
4. **Hanlon's Razor** (*Never attribute to user error what can be explained by poor affordance*):
   - When users fail a task, fix the confusing affordance, label, or missing feedback before blaming user error.

### Product Laws
5. **Pareto Principle** (*80% of value comes from 20% of controls*):
   - Surface the vital 20% prominently in the top-level interface. Subordinate rarely used edge-case settings into secondary views.
6. **Goodhart's Law** (*When a measure becomes a target, it ceases to be a good measure*):
   - Design metrics displays around verified outcomes, not easily gamed vanity stats (e.g., "completed workflows" vs. "raw clicks").
7. **Parkinson's Law** (*Work expands to fill available space*):
   - Constrain task boundaries. Design time-boxed, focused workflows rather than infinite scrollable configuration sheets.
8. **Peter Principle** (*Complexity grows beyond competence*):
   - Implement progressive complexity: Clean defaults for beginners -> advanced filters and bulk actions -> API/CLI for power users.

### Engineering & Architecture Laws
9. **Hofstadter's Law** (*Tasks take longer than expected*):
   - Design for failure modes: skeleton states, network retries, optimistic UI updates, and clear recovery paths.
10. **Chesterton's Fence** (*Understand why something exists before removing it*):
    - When refactoring legacy UI, understand what edge-case or compliance need a control served before deleting it.
11. **Brooks's Law** (*Adding complexity makes late projects later*):
    - In design systems: add only components that earn their weight. Every new variant adds maintenance and visual debt.
