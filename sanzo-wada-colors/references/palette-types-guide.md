# Sanzo Wada Palette Types: Duos, Trios, & Quads

Sanzo Wada's *A Dictionary of Color Combinations* (published in Japan in the 1930s) was among the first systematic explorations of multi-color harmony combining traditional Japanese seasonal aesthetics with Western color printing.

---

## 1. The Three Palette Structures

The collection is categorized into three harmonic arrangements:

| Arrangement | Count | Combination IDs | Typical Role in Software & UI |
|---|:---:|:---:|---|
| **Duos (2-Color)** | 120 | `#1` – `#120` | Minimalist interfaces, editorial covers, high-contrast brand marks, primary & accent pairings. |
| **Trios (3-Color)** | 120 | `#121` – `#240` | Full product shells: Surface/Background, Content/Text, and Interactive Accent/Focus. |
| **Quads (4-Color)** | 108 | `#241` – `#348` | Multi-state systems, data visualization categorical scales, illustration, complex dashboard widgets. |

---

## 2. When to Use Which Palette

### Duos (1 to 120)
- **Best For**:
  - Swiss / Editorial layouts with restrained typography.
  - Dark mode / Light mode polarity.
  - Monograms, logo marks, and business stationery.
- **Example**: Combination `#6` (Deep Indigo `#051230` + Cameo Pink `#e0b3b6`). High contrast, sophisticated editorial elegance.

### Trios (121 to 240)
- **Best For**:
  - Standard SaaS or consumer web applications.
  - Establishing clear visual hierarchy:
    - Dominant (60%): Surface / Background
    - Secondary (30%): Structure / Cards / Borders
    - Accent (10%): Call-to-action buttons / Active badges
- **Example**: Combination `#198` (Burnt Sienna `#ae5224` + Apricot Yellow `#ffdd00` + Green `#489b6e`). Warm, organic, vibrant.

### Quads (241 to 348)
- **Best For**:
  - Data visualization charts (pie charts, line graphs, bar charts).
  - Multi-tier badge systems (e.g. Success, Warning, Neutral, Info).
  - Editorial illustration and complex card components.
- **Example**: Combination `#285` (Burnt Sienna `#ae5224` + Raw Umber `#8c6633` + Calamine Blue `#78cdd0` + Pale Gray `#e6e6e6`).

---

## 3. WCAG Accessibility Rules for Wada Palettes

Because Sanzo Wada designed these for print in the 1930s rather than digital displays, not every adjacent pair meets WCAG 2.1 AA (4.5:1 for body text).

When applying these in Web/UI:
1. Always run `wada contrast <ID>` to check contrast ratios.
2. Use the highest-contrast pair for text on background ($>4.5:1$).
3. Use low-contrast pairs ($<3.0:1$) strictly for decorative borders, background tint fills, or subtle card accents.

