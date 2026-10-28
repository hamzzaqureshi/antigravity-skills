# Anti-Slop Rules & 12-Point Pre-Flight Check

> Concrete, non-negotiable rules for eliminating generic AI tells from frontend interfaces.

---

## 1. Hard Bans (Zero Tolerance)

1. **The Em-Dash Ban**: Em-dashes (`—`) in headlines, body copy, quotes, and badges are **STRICTLY BANNED**. They are the #1 tell of LLM-generated prose. Use periods, colons, or clean separate sentences.
2. **The "Lila" AI-Purple Glow**: Never use harsh purple-to-blue gradients (`from-purple-500 to-blue-500`), blurred radial background orbs, or glowing neon drop shadows.
3. **The Premium-Consumer Warm-Craft Cliché**:
   - Banned backgrounds: `#f5f1ea`, `#f7f5f1`, `#fbf8f1`, `#efeae0`, `#ece6db` (warm paper/bone).
   - Banned accents: `#b08947`, `#b6553a`, `#9a2436`, `#9c6e2a`, `#bc7c3a` (brass/clay/oxblood).
   - Banned dark text: `#1a1714`, `#1a1814` (espresso).
   - *Rotate to authentic alternatives: Cold Luxury (silver/smoke), Forest (deep green/amber), Cobalt + Cream, Terracotta + Slate, or Monochrome + saturated pop.*
4. **Banned Fonts as Defaults**: `Fraunces` and `Instrument_Serif` are banned as default reach. Default to modern sans-serif display fonts (`Geist`, `Cabinet Grotesk`, `Satoshi`, `Outfit`).
5. **Div-Based Fake Screenshots**: Do not render fake product dashboards with empty colored `<div>` rectangles. Use real images, live component previews, or omit them entirely.

---

## 2. Layout & Typography Discipline

- **Hero Initial Viewport Rule**: Hero MUST fit in initial viewport without scrolling. Headline max 2 lines; subtext max 20 words; CTAs visible immediately.
- **Hero Top Padding Cap**: Maximum `pt-24` (≈6rem) on desktop.
- **Hero Text Elements Cap**: Maximum 4 elements (Eyebrow or brand strip, Headline, Subtext, CTAs). No secondary trust badges or pricing teasers inside the hero.
- **Eyebrow Restraint**: Maximum **1 eyebrow per 3 sections**. Never place an uppercase tracking label above every section.
- **Navigation Height & Single Line**: Navigation must fit on a single line at desktop. Height capped at 64px - 72px (max 80px).
- **CTA Button Text Wrap Ban**: Button text must fit on one line at desktop. Shorten label (1-3 words) or widen button.
- **No Duplicate CTA Intent**: Do not mix "Get Started", "Start a Project", and "Reach out" on the same page. Pick ONE label per intent.

---

## 3. The 12-Point Pre-Flight Audit Checklist

Before declaring any frontend task complete, execute this mechanical audit:

| # | Check | Verification Rule |
| :---: | :--- | :--- |
| **1** | **Em-Dash Scan** | Search for `—` across all files. Count must be **0**. |
| **2** | **Hero Viewport** | Hero content fits in `min-h-[100dvh]`; CTA visible without scroll. |
| **3** | **Hero Top Padding** | Top padding is $\le$ `pt-24`. |
| **4** | **Eyebrow Density** | Count of `uppercase tracking` labels $\le \lceil \text{sectionCount} / 3 \rceil$. |
| **5** | **CTA Single Line** | No desktop button labels wrap to multiple lines. |
| **6** | **Single Intent CTAs** | Only 1 consistent CTA label used per user action. |
| **7** | **Contrast Check** | WCAG AA minimum (4.5:1 for body, 3:1 for headers) verified in both light & dark modes. |
| **8** | **Theme Consistency** | Entire page shares one consistent theme mode (no random dark/light inverted sections). |
| **9** | **Mobile Collapse** | Every multi-column grid has explicit mobile fallback (`col-span-12` or `grid-cols-1`). |
| **10**| **Reduced Motion** | All animations wrapped in `useReducedMotion()` or `@media (prefers-reduced-motion: reduce)`. |
| **11**| **Icon Consistency** | Exactly 1 icon family used across the entire tree with uniform `strokeWidth`. |
| **12**| **Copy Hallucination** | No cute fake-craftsman wordplay or unverified fake-precise metrics (`4.1x`, `99.4%`). |
