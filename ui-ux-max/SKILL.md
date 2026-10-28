---
name: ui-ux-max
description: "Searchable BM25 design intelligence database and stack-specific guideline engine for 22 frameworks (React, Next.js, Vue, Svelte, Tailwind, SwiftUI, React Native, etc.). Features 79 styles, 192 product palettes, 74 font pairings, 119 UX guidelines, 105 icons, and 25 chart types. Use when searching for industry-specific color palettes, font pairings, UX guidelines, or running `search.py --design-system` to generate persistent design specs across 22 frameworks. Not for static code scanning or creative dial tuning."
---

# UI/UX Pro Max - Design Intelligence

Searchable local UI/UX guidance: 79 searchable styles (50 active), 192 product palettes and exact reasoning profiles, 74 font pairings, 119 UX guidelines, 105 curated icons, 17 GSAP presets, 25 chart types, and 22 technology stacks.

## When to Apply

Use this skill when the task involves **UI structure, visual design decisions, interaction patterns, or user experience quality control**:
- Designing new pages, dashboards, landing pages, or mobile views
- Creating or refactoring UI components, forms, navigation, or data tables
- Choosing color palettes, typography scales, spacing tokens, or layout systems
- Reviewing UI for UX, accessibility (WCAG), performance, and visual hierarchy
- Implementing animations, micro-interactions, or GSAP choreographies
- Implementing stack-specific best practices across 22 supported frameworks

Skip it for pure backend logic, API/database design, non-visual performance work, or infrastructure/DevOps — unless the task changes how something **looks, feels, moves, or is interacted with**.

---

## Rule Categories by Priority

*Follow priority 1→10 to decide which category to focus on first; use `--domain <Domain>` to query full details. The full rule text for every category lives in `references/quick-reference.md` — read it on demand rather than loading it every time.*

| Priority | Category | Impact | Domain | Key Checks (Must Have) | Anti-Patterns (Avoid) |
|:---|:---|:---|:---|:---|:---|
| 1 | Accessibility | CRITICAL | `ux` | Contrast 4.5:1, Alt text, Keyboard nav, Aria-labels | Removing focus rings, Icon-only buttons without labels |
| 2 | Touch & Interaction | CRITICAL | `ux` | Min size 44×44px, 8px+ spacing, Loading feedback | Reliance on hover only, Instant state changes (0ms) |
| 3 | Performance | HIGH | `ux` | WebP/AVIF, Lazy loading, Reserve space (CLS < 0.1) | Layout thrashing, Cumulative Layout Shift |
| 4 | Style Selection | HIGH | `style`, `product` | Match product type, Consistency, SVG icons (no emoji) | Mixing flat & skeuomorphic randomly, Emoji as icons |
| 5 | Layout & Responsive | HIGH | `ux` | Mobile-first breakpoints, Viewport meta, No horizontal scroll | Horizontal scroll, Fixed px container widths, Disable zoom |
| 6 | Typography & Color | MEDIUM | `typography`, `color` | Base 16px, Line-height 1.5, Semantic color tokens | Text < 12px body, Gray-on-gray, Raw hex in components |
| 7 | Animation | MEDIUM | `ux`, `gsap` | Context-aware timing, Motion conveys meaning, Spatial continuity | One duration for every transition, Animating width/height, No reduced-motion |
| 8 | Forms & Feedback | MEDIUM | `ux` | Visible labels, Error near field, Helper text, Progressive disclosure | Placeholder-only label, Errors only at top, Overwhelm upfront |
| 9 | Navigation Patterns | HIGH | `ux` | Predictable back, Bottom nav ≤5, Deep linking | Overloaded nav, Broken back behavior, No deep links |
| 10 | Charts & Data | LOW | `chart` | Legends, Tooltips, Accessible colors | Relying on color alone to convey meaning |

For the full rule list per category (all 119 UX guidelines with rationale), read [quick-reference.md](./references/quick-reference.md). For app-specific polish rules (icons, touch feedback, dark mode contrast, safe areas) and the canonical pre-delivery checklist, read [pro-rules.md](./references/pro-rules.md).

---

## Prerequisites & Execution

The bundled scripts require Python 3 (standard library only — zero third-party dependencies, zero network requests).

Invoke the CLI script using its full path or relative to the skill location:

```bash
# Global installation path:
python3 ~/.gemini/config/skills/ui-ux-pro-max/scripts/search.py "<query>" [options]

# Or from workspace / skill directory:
python3 scripts/search.py "<query>" [options]
```

---

## Query Contract

Choose the smallest search mode that matches the request:

1. **New project/page or system-wide visual direction** → use `--design-system`.
2. **Targeted concern or component bug** → use one explicit `--domain`.
3. **Known implementation stack** → use `--stack`; add a separate domain search only for a distinct design concern.

Write each query around **one dominant intent**, using **2–5 meaningful terms** plus one useful constraint such as product, platform, or interaction. Do not combine unrelated checklist topics into one query.

- **Accessibility**: Query semantic outcome first (`"error summary validation" --domain ux`), then component domain if needed (`"decorative icon aria hidden" --domain icons`), then stack.
- **Text Layout & Compact UI**: Query semantic UX outcome first (`"orphan heading line balance" --domain ux`, `"badge chip label wraps" --domain ux`), then the detected stack (`"chip badge overflow nowrap" --stack html-tailwind`).

Before using a result, verify the returned domain/category, top result identity, and fit for the user's product and platform. **Retry once** with a narrower query or explicit domain/stack if empty or off-topic.

---

## Core Workflows

### Step 1: Analyze User Requirements
Extract:
- **Product type**: SaaS, e-commerce, portfolio, dashboard, entertainment, developer tool, healthcare, fintech, etc.
- **Target audience & context**: age group, usage context (desktop productivity, mobile on-the-go).
- **Style keywords**: playful, vibrant, minimal, dark mode, high contrast, immersive, Swiss.
- **Stack**: detect from project files (`package.json`, `pubspec.yaml`, `*.xcodeproj`, `composer.json`, etc.) or ask. **Never assume a stack**.

### Step 2: Generate Design System (Required for new projects & pages)

```bash
python3 scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

This aggregates product, style, color, landing, and typography matches, evaluates rules from `ui-reasoning.csv`, and outputs pattern, style, colors, typography, effects, and anti-patterns to avoid.

**Example:**
```bash
python3 scripts/search.py "beauty spa wellness service" --design-system -p "Serenity Spa"
```

### Step 2b: Persist Design System (Master + Overrides Pattern)
Save the design system for hierarchical retrieval across sessions with `--persist` and an explicit `--output-dir`:

```bash
python3 scripts/search.py "<query>" --design-system --persist -p "Project Name" --output-dir "<project-root>" [--page "dashboard"]
```

This creates:
- `design-system/<project-slug>/MASTER.md` — Global Source of Truth (colors, typography, spacing, components)
- `design-system/<project-slug>/pages/<page-name>.md` — Page-specific overrides (if `--page` is provided)

**Hierarchical Retrieval Rules:**
1. Check `design-system/<project-slug>/pages/<page-name>.md` first.
2. If the page file exists, prioritize its rules over Master.
3. If not, use `design-system/<project-slug>/MASTER.md` exclusively.
4. If Master already exists, `--persist` skips writing and leaves it untouched unless `--force` is explicitly passed. Never overwrite without user consent.

### Step 2c: Design Dials (1–10 Sliders)
Tune the design system without rewriting the query:

```bash
python3 scripts/search.py "<query>" --design-system --variance <1-10> --motion <1-10> --density <1-10>
```

| Dial | Low (1-3) | Mid (4-7) | High (8-10) |
|:---|:---|:---|:---|
| `--variance` | Centered / minimal (Minimalism, Soft UI) | Balanced / modern | Bold / asymmetric (Brutalism, Bento Grid, Kinetic) |
| `--motion` | Subtle micro-interactions | Standard scroll/stagger motion | Complex choreography (pin, Flip, SplitText GSAP) |
| `--density` | Spacious (24-96px spacing scale) | Standard (16-64px default) | Dense/dashboard (8-32px compact spacing) |

- `--motion` attaches a matching GSAP preset from `motion.csv`.
- `--density` overrides the `--space-*` CSS variable scale.

### Step 3: Domain-Specific Detailed Searches

```bash
python3 scripts/search.py "<query>" --domain <domain> [-n <max_results>]
```

| Need | Domain | Example Query |
|:---|:---|:---|
| Product type patterns | `product` | `"developer tool ide" --domain product` |
| UI visual styles | `style` | `"glassmorphism dark mode" --domain style` |
| Color palettes | `color` | `"fintech banking trust" --domain color` |
| Font pairings | `typography` | `"editorial serif modern" --domain typography` |
| Individual Google Fonts | `google-fonts` | `"sans serif geometric variable" --domain google-fonts` |
| Chart recommendations | `chart` | `"time-series analytics" --domain chart` |
| UX best practices & A11y | `ux` | `"error summary validation" --domain ux` |
| Landing page patterns | `landing` | `"hero social-proof cta" --domain landing` |
| Curated SVG icons | `icons` | `"security lock shield" --domain icons` |
| GSAP animation presets | `gsap` | `"stagger cards reveal" --domain gsap` |
| React/Next performance | `react` | `"rerender memo virtualization" --domain react` |
| Native/Mobile UI rules | `web` | `"safe-area haptics dynamic-type" --domain web` |

### Step 4: Tech Stack Guidelines

```bash
python3 scripts/search.py "<query>" --stack <stack>
```

**22 Supported Stacks:**
- **Web / Frontend**: `react`, `nextjs`, `vue`, `nuxtjs`, `nuxt-ui`, `svelte`, `astro`, `angular`, `laravel`, `html-tailwind`, `shadcn`, `threejs`
- **Mobile**: `swiftui`, `jetpack-compose`, `react-native`, `flutter`
- **Desktop**: `javafx`, `wpf`, `winui`, `avalonia`, `uno`, `uwp`

---

## Output Formats

- `-f ascii` (default): Boxed terminal display, human-readable.
- `-f markdown`: Formatted markdown tables and blocks, ideal for documentation.
- `--json`: Complete un-truncated JSON object with raw metadata and persistence statuses.

---

## Pre-Delivery Quality Checklist

Before finalizing any UI implementation, verify against this checklist:

- [ ] **Icons**: SVG only (Lucide, Heroicons, Phosphor). Never emojis as interface icons.
- [ ] **Clickables**: `cursor-pointer` on all interactive elements. Visible focus states (`:focus-visible`).
- [ ] **Contrast**: Text contrast ratio 4.5:1 minimum (WCAG AA).
- [ ] **Motion**: Respect `prefers-reduced-motion`. Micro-interactions between 150ms–300ms.
- [ ] **Typography**: Modular type scale; balanced wrapping; no orphan headings.
- [ ] **Touch Targets**: Minimum 44×44px with 8px+ spacing on touch devices.
- [ ] **Responsive**: Verified at 375px, 768px, 1024px, and 1440px. No horizontal scroll.
- [ ] **Resilient Text**: Long tokens, chips, and badges reflow or wrap without clipping.
- [ ] **No Generic Slop**: Banned purple/pink AI gradients unless specifically requested.
