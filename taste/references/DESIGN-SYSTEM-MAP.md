# Brief to Design System Mapping

> When to install official design systems vs. when to build custom bespoke styling.

---

## 1. Official Design Systems Matrix

If the brief matches an established enterprise or ecosystem pattern, install and use the **official** package. Do not recreate its CSS by hand.

| Brief Archetype | Official Package to Install | Rationale & Capabilities |
| :--- | :--- | :--- |
| **Microsoft / Enterprise SaaS** | `@fluentui/react-components` | Official Fluent tokens, high enterprise data density, accessibility out of the box. |
| **Google / Material Product** | `@material/web` + M3 tokens | Official Material 3 tokens and reactive dynamic state. |
| **IBM / Enterprise Analytics** | `@carbon/react` + `@carbon/styles` | Mature data-density patterns and telemetry tables. |
| **Shopify Admin Surfaces** | `polaris.js` / Polaris React | Mandatory compliance for Shopify admin extensions. |
| **Atlassian / Jira-style Tooling** | `@atlaskit/*` + `@atlaskit/tokens` | Official Atlassian design system primitives. |
| **GitHub Devtools / Ecosystem** | `@primer/react-brand` or `@primer/css` | Official Primer Brand component library. |
| **UK Public-Sector Services** | `govuk-frontend` | Legally mandated accessibility compliance. |
| **US Public-Sector Services** | `uswds` | Federal accessibility standards and trust styling. |
| **Fast Local Business / SMB MVP** | `Bootstrap 5.3` | Mature, zero-overhead, highly stable responsive grid. |
| **Accessible React Foundation** | `@radix-ui/themes` | Polished headless accessible primitives. |
| **Modern Bespoke SaaS** | `shadcn/ui` (`npx shadcn@latest add`) | Own the code directly. *Never ship unmodified default state.* |
| **Modern AI Marketing / Indie** | `Tailwind v4` utilities + `dark:` | Maximum flexibility for indie landing pages and custom UI. |

### The Honesty Rule
- Never import a design system's tokens and proceed to override 90% of them with arbitrary inline styles.
- **One system per project.** Do not mix `@fluentui` with `@carbon/react` in the same React tree.

---

## 2. Aesthetic Directions (Bespoke Implementation)

When the brief represents an aesthetic trend rather than an official design system, there is no official npm package. Implement using native CSS, Tailwind v4, and modern primitives:

| Aesthetic Direction | Authentic Implementation Strategy |
| :--- | :--- |
| **Glassmorphism / Frosted** | `backdrop-filter: blur(16px)`, layered 1px inner border (`border-white/10`), inner highlight (`shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`). Provide solid-fill fallback under `prefers-reduced-transparency`. |
| **Apple-Style Bento Grids** | Native CSS Grid with mixed column/row spans. Ensure cells have visual diversity (not 6 empty text boxes). |
| **Industrial Brutalism** | Monospace typography, raw 1px/2px black borders, high contrast, zero border-radius (`rounded-none`). |
| **Editorial Magazine** | Elegant serif typography, asymmetric grid layouts, generous whitespace, drop caps, justified text columns. |
| **Dark Tech / Hacker** | Monospace numbers, single neon accent against deep charcoal/black, terminal aesthetics, minimal chrome. |
| **Aurora Mesh Gradients** | Layered SVG blur filters or WebGL shaders. Avoid harsh purple/blue generic AI gradients. |
| **Apple Liquid Glass** | Apple documents this for native visionOS/macOS only. *There is no official `liquid-glass.css`.* Web versions are approximations using `backdrop-filter` + refractive borders. Label honestly as approximation. |
