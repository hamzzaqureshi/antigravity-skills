# Specialized Style Variants & Sub-Skills

> Guidelines and directives for the 6 specialized aesthetic modes included in the Taste Skill suite.

---

## 1. Minimalist UI (`minimalist-ui`)
- **Aesthetic**: Editorial product UI (Linear, Notion, Raycast vibes).
- **Palette**: Deep charcoal, pure white, cool slate, single quiet accent.
- **Typography**: `Geist` or `Inter Tight`, generous line heights, small crisp badges.
- **Layout**: Crisp 1px borders, subtle negative space, zero flashy gradients.
- **Motion**: Instant snappy micro-transitions (`duration: 0.15s`), zero bouncy physics.

---

## 2. Industrial Brutalist UI (`industrial-brutalist-ui`)
- **Aesthetic**: Raw Swiss engineering, architectural drafts, blueprint precision.
- **Palette**: Stark black and white, caution yellow or safety orange single accent.
- **Typography**: Heavy grotesque headings (`PP Neue Montreal`, `Cabinet Grotesk`), IBM Plex Mono data.
- **Layout**: Hard 2px solid black borders, exposed grid lines, raw tables, zero rounded corners (`rounded-none`).
- **Motion**: Mechanical stepped keyframes, hard toggles, zero spring bounce.

---

## 3. High-End Visual Design / Soft UI (`high-end-visual-design`)
- **Aesthetic**: Calm, expensive, luxury product interface (Bang & Olufsen, Apple, Leica).
- **Palette**: Muted smoke, soft cream, warm charcoal, brushed aluminum accents.
- **Typography**: Elegant display sans (`Söhne`, `GT Walsheim`), loose tracking.
- **Layout**: Expansive breathing room (`py-32`), tactile cards with diffused inner shadows.
- **Motion**: Silky smooth spring physics (`stiffness: 80, damping: 25`), soft parallax.

---

## 4. GPT-Taste (`gpt-taste`)
- **Aesthetic**: Hyper-strict anti-slop rules tailored specifically to counter OpenAI GPT/Codex tendencies.
- **Directives**: Aggressively bans repetitive bento boxes, enforces high layout variance (`DESIGN_VARIANCE: 9`), and mandates custom GSAP timelines over generic CSS transitions.

---

## 5. Google Stitch Compatibility (`stitch-design-taste`)
- **Aesthetic**: Compatible with Google Stitch design systems.
- **Output**: Generates both production frontend code and exportable `DESIGN.md` design-token specifications.

---

## 6. Full Output Enforcement (`full-output-enforcement`)
- **Directives**: Enforces that the agent never emits lazy placeholder comments such as:
  - `// ... rest of the code remains the same`
  - `/* TODO: implement handlers here */`
  - `<div className="...">...</div>`
- Mandates 100% complete, fully compilable code in every response.
