# Brief Inference and The Three Dials

> How to read the room before touching code, infer the design language, and configure the three dials: `DESIGN_VARIANCE`, `MOTION_INTENSITY`, and `VISUAL_DENSITY`.

---

## 1. Brief Inference Protocol

Before generating code or selecting components, infer what the user actually needs. LLM design fails when the model jumps to a generic default aesthetic instead of reading the room.

### 1.A The 6 Diagnostic Signals

1. **Page Kind**:
   - Landing page: SaaS, consumer product, agency, event, developer tool.
   - Portfolio: Software engineer, product designer, creative technologist, agency studio.
   - Redesign: Preserve existing brand tokens vs. radical overhaul.
   - Editorial / Content: Publication, blog, manifesto, documentation.
2. **Vibe Vocabulary**:
   - Notice user keywords: *"minimalist"*, *"Linear-style"*, *"Apple-y"*, *"calm"*, *"Awwwards"*, *"brutalist"*, *"serious B2B"*, *"editorial"*, *"glassy"*, *"dark tech"*.
3. **Reference Signals**:
   - URLs provided, screenshots attached, named competitors, referenced brands.
4. **Target Audience**:
   - B2B procurement committee vs. design-conscious consumer vs. engineering hiring manager. The audience determines the aesthetic, not personal agent taste.
5. **Existing Brand Assets**:
   - Existing logos, palette hex codes, typography, photography. On redesigns, these are mandatory starting materials.
6. **Quiet Constraints**:
   - Public-sector compliance (WCAG AAA), regulated financial/medical interfaces, trust-first commerce. These constraints strictly override decorative aesthetics.

---

## 2. The One-Line Design Read

Before emitting any code, state in one clear line:

> **"Reading this as: `<page kind>` for `<audience>`, with a `<vibe>` language, leaning toward `<design system or aesthetic family>`."**

### Examples:
- *"Reading this as: B2B SaaS landing for technical buyers, with a Linear-style minimalist language, leaning toward Tailwind utilities + Geist + restrained motion."*
- *"Reading this as: solo designer portfolio for hiring managers, with an editorial / kinetic-type language, leaning toward native CSS + scroll-driven animation + custom typography."*
- *"Reading this as: redesign of a public-sector service site, with a trust-first language, leaning toward GOV.UK Frontend or USWDS."*

---

## 3. The Three Dials Configuration

| Dial | Scale | Definition |
| :--- | :---: | :--- |
| **`DESIGN_VARIANCE`** | `1 - 10` | `1` = Strict Symmetrical Grid, `10` = Asymmetric Experimental Artistry |
| **`MOTION_INTENSITY`** | `1 - 10` | `1` = Completely Static, `10` = Cinematic Scroll-Hijacking & Physics |
| **`VISUAL_DENSITY`** | `1 - 10` | `1` = Art Gallery / Airy Breathing Space, `10` = Cockpit / Compact Metrics |

### Baseline Configuration: `8 / 6 / 4`

### Dial Inference Mapping:

| Signal / Use Case | `DESIGN_VARIANCE` | `MOTION_INTENSITY` | `VISUAL_DENSITY` |
| :--- | :---: | :---: | :---: |
| **Minimalist / Clean / Linear-style** | `5 - 6` | `3 - 4` | `2 - 3` |
| **Premium Consumer / Luxury / Brand** | `7 - 8` | `5 - 7` | `3 - 4` |
| **Playful / Agency / Awwwards / Wild** | `9 - 10`| `8 - 10`| `3 - 4` |
| **Standard SaaS Landing (Default)** | `7 - 9` | `6 - 8` | `3 - 5` |
| **Trust-First / Public Sector / Gov** | `3 - 4` | `2 - 3` | `4 - 5` |
| **Designer / Creative Portfolio** | `8` | `7` | `3` |
| **Software Engineer Portfolio** | `6` | `5` | `4` |
| **Editorial / Magazine / Blog** | `6` | `4` | `3` |
| **Redesign (Preserve Tokens)** | `Match existing` | `Match + 1` | `Match existing` |
| **Redesign (Full Overhaul)** | `+2` | `+2` | `Match existing` |

---

## 4. How Dials Mechanically Govern Output

- **`DESIGN_VARIANCE > 4`**: Centered heroes are strictly avoided. Force 50/50 split screens or asymmetric column locks.
- **`DESIGN_VARIANCE 8 - 10`**: Masonry layouts, fractional CSS grid (`2fr 1fr 1fr`), wide empty gutters (`padding-left: 20vw`). *Mandatory mobile override: Viewports `< 768px` must collapse to strict single-column `w-full`.*
- **`MOTION_INTENSITY 1 - 3`**: No automatic entrance loops. CSS `:hover` and `:active` states only.
- **`MOTION_INTENSITY 4 - 7`**: Fluid spring transitions (`stiffness: 100, damping: 20`), scroll-reveal stagger.
- **`MOTION_INTENSITY 8 - 10`**: ScrollTrigger pinned sticky-stacks, horizontal scrub pans, custom pointer physics.
- **`VISUAL_DENSITY > 7`**: Card containers banned. Borders and 1px dividers separate data rows. All numbers rendered in `font-mono`.
