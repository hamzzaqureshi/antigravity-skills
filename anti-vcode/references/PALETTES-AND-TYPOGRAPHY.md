# Intentional Palettes & Typography Pairings

Replace the generic AI default (*purple-blue gradient + Inter + dark mode with low contrast*) with curated palettes and intentional typographic voices.

---

## 1. Distinctive Color Systems

### Palette A: Swiss Precision & International Signal
*Best for: Developer tools, productivity platforms, data systems, hardware interfaces.*
- **Background**: Warm Ivory (`#FBF9F5`) or Stark Architectural White (`#F5F5F7`)
- **Text & Structure**: Deep Carbon / Asphalt (`#121316`)
- **Borders & Dividers**: Crisp Neutral Hairline (`#E2E0D8`)
- **Single Focal Accent**: Signal Vermilion (`#FF3B00`) or International Klein Blue (`#002FA7`)
- **Philosophy**: 90% monochrome discipline; 10% razor-sharp intentional accent.

### Palette B: Warm Editorial & Archival
*Best for: Content platforms, research tools, analytics, long-form publishing.*
- **Background**: Archival Cream (`#F4EFEA`)
- **Text & Structure**: Warm Charcoal (`#1C1B1A`)
- **Card Fill**: Soft Stone (`#EAE4DC`)
- **Accent**: Burnt Terracotta (`#C2572B`) or Pine Forest (`#1C3D2F`)
- **Philosophy**: Organic, tactile paper aesthetic that completely rejects digital synthetic neon.

### Palette C: High-Contrast Technical Night
*Best for: Dashboards, terminal-adjacent tools, monitoring, audio/creative software.*
- **Background**: Deep Obsidian (`#0B0C0E`, never washed-out gray)
- **Panel Surface**: Elevated Slate (`#14161A`, with 1px border `#23272F`)
- **Text**: Razor Crisp Off-White (`#F0F2F5`) and Subordinate Muted (`#8C92A0`)
- **High-Affordance Accent**: Electric Acid Lime (`#CCFF00`) or Hyper Cyan (`#00E5FF`)
- **Philosophy**: Pure contrast compliance, zero muddy low-contrast grays, zero random purple radial blobs.

---

## 2. Intentional Typographic Pairings

| Aesthetic | Heading Display | Body / Interface | Monospace / Metadata |
| :--- | :--- | :--- | :--- |
| **Swiss Architectural** | **General Sans** or **Cabinet Grotesk** | **Satoshi** or **Chivo** | **IBM Plex Mono** |
| **Technical Editorial** | **Newsreader** or **Instrument Serif** (restrained) | **Plus Jakarta Sans** | **JetBrains Mono** |
| **Utilitarian Systems** | **Archivo Black** or **Clash Display** | **Inter** (strictly body) | **Geist Mono** |
| **Modern Humanities** | **Fraunces** or **Besley** | **DM Sans** | **Space Mono** |

---

## 3. Typographic Discipline Rules

1. **Adhere to a Mathematical Scale**:
   ```css
   --font-xs: 12px;   /* Metadata, badges, fine print */
   --font-sm: 14px;   /* Secondary UI, helper text */
   --font-base: 16px; /* Primary body copy, inputs */
   --font-lg: 20px;   /* Section subheadings */
   --font-xl: 26px;   /* Primary card/block titles */
   --font-2xl: 42px;  /* Section headings */
   --font-3xl: 68px;  /* Hero display */
   ```
2. **No Italic Clichés**: Do not italicize random buzzwords in headers (*effortless*, *intelligent*). Italicize only formal titles, foreign terms, or genuine editorial citations.
3. **Line Height Ratios**:
   - Display headings: `leading-none` or `line-height: 1.05 - 1.15` (tight, architectural).
   - Body copy: `line-height: 1.5 - 1.65` (breathable, legible).
