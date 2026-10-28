# The 40 Signs of Vibecoded Frontend (Anti-Slop Master Checklist)

A diagnostic checklist exposing the visual grammar of generic AI-generated interfaces. Individually, some of these patterns are benign; together, they signal an unmistakable **lack of human authorship**.

---

## 1. Visual Language Clichés

1. **Purple-to-Blue Gradients**: The default AI palette (`#6366f1` to `#a855f7`). Banned unless the brand literally makes blacklights.
2. **Gradient Text in the Hero**: Slapping a 3-stop linear gradient on an `h1` as a substitute for typographic hierarchy.
3. **Neon Accents on Pitch-Black**: Cyan/magenta neon glow on `#000000` to evoke faux "cyberpunk" or "future tech".
4. **Giant Radial Gradient Orbs**: Blurred colored spheres (`blur-3xl`) floating behind cards solely to fill negative space.
5. **Grain Texture Over Gradients**: A 5% noise PNG overlay slapped on top of a purple gradient to pretend it is "textured editorial".
6. **Dot-Grid Backgrounds**: Repeated 1px dot patterns used as generic "tech atmosphere".
7. **Excessive Glassmorphism**: `backdrop-blur-md` and `bg-white/5 border-white/10` on every single container and card.
8. **Soft Corner Radius on Everything**: `rounded-2xl` and `rounded-3xl` applied uniformly to badges, inputs, cards, and modals.
9. **Colored Left Borders on Cards**: A 3px purple or cyan vertical border on cards trying to signal "feature status".
10. **Low-Contrast Dark Mode**: Gray-on-gray (`#71717a` text on `#18181b` backgrounds) that violates WCAG AA readability.
11. **Generic Pastel Palette**: Washed-out mint, lavender, and peach palettes with zero relationship to the product domain.
12. **Bento Grids Without Content Logic**: Forcing arbitrary stats and buttons into asymmetrical grids just because Apple did it once.
13. **Three Identical Feature Cards**: Three equal-width cards in a row with identical icon + title + 2-line description.
14. **Floating Blobs & Filler Shapes**: Floating 3D shapes, abstract cubes, and geometric particles that convey zero product value.

---

## 2. Typography Clichés

15. **Inter for Absolutely Everything**: Defaulting to Inter with standard weights, ignoring editorial or monospace pairings.
16. **Space Grotesk + Instrument Serif by Template Default**: The standard indie-hacker pairing applied without concept.
17. **Italic Serif as the "Premium" Accent**: Arbitrarily italicizing single buzzwords in the headline (*intelligent*, *seamless*, *effortless*).
18. **Oversized Hero Typography With No Concept**: Giant 84px headlines that say nothing specific.
19. **Em Dashes Everywhere**: Sprinkle—em dashes—into every—sentence to fake conversational sophistication.
20. **Random Typography Scale**: Jumping arbitrarily between `14px`, `18px`, `22px`, and `36px` instead of adhering to a disciplined ratio.

---

## 3. UI Clichés

21. **Lucide Icons for Everything**: Defaulting to outline Lucide icons with 1.5px stroke on every list item and button.
22. **Sparkle Icons (/ ) Meaning "AI"**: Using four-pointed stars to pretend a generic feature is magically intelligent.
23. **Emojis in Serious Headings**: Using , , or next to enterprise software headers.
24. **Checkmark Bullets for Every Benefit**: Green or purple checkmarks in front of generic marketing copy.
25. **Three Floating Icon Boxes in a Row**: Stacking three cards with centered icons above the fold.
26. **Floating Pill Badge Above Every Headline**: `[ Introducing v2.0 -> ]` placed mechanically over the title.
27. **Untouched UI Library Defaults**: Raw, uncustomized Shadcn / Radix / Tailwind defaults that look like every GitHub starter repo.
28. **Indistinguishable Buttons**: Primary, secondary, and tertiary buttons with no clear visual hierarchy or affordance.
29. **Cards Inside Cards Inside Cards**: Deeply nested bordered containers with no informational necessity.
30. **Decorative Terminal Windows**: Faux macOS window dots (red, yellow, green) framing fake code or CLI commands purely for decoration.

---

## 4. Animation Clichés

31. **Viewport Fade-In on Every Section**: Mechanical `opacity: 0 -> 1; translateY(20px)` triggered on scroll on every single element.
32. **Trivial 2px Button Hovers**: Buttons that only shift `translateY(-2px)` on hover with no tactile press feedback.
33. **Cursor-Following Glowing Beams**: Radial gradient following mouse coordinates across dark backgrounds.
34. **Animated Arrows Pointing Nowhere**: Pulsing or bouncing `->` SVG icons urging the user to click.
35. **Random Floating Particle Fields**: Canvas particles floating aimlessly across the hero.
36. **Parallax on Everything**: Layered elements scrolling at slightly mismatched speeds with no spatial concept.
37. **Smooth Scrolling as a Crutch**: Adding Lenis or smooth-scroll solely to make a hollow layout feel "buttery".

---

## 5. Content & Product Clichés

38. **Generic Buzzword Copy**: *"Transform your workflow with the future of intelligent collaboration."*
39. **Fake Metrics & Social Proof**: *"Trusted by 10,000+ teams across 40 countries"* with no verified logos or case studies.
40. **No Real Product Demonstration**: Providing the cookie-cutter sequence:
    `gradient hero -> 3 feature cards -> fake testimonials -> 3 pricing tiers -> FAQ -> CTA`
    with zero actual interface screenshots, live workflows, or interactive demos.

---

## 6. The Non-Negotiable Technical Floor (Zero-Slop CSS Mechanics)

41. **`overflow-x: clip` Over `overflow-x: hidden`**: Never use `overflow-x: hidden` or `100vw` on `html, body`—it breaks `position: sticky` and causes mobile layout shifts. Use `overflow-x: clip`.
42. **Never `transition: all`**: Animate only GPU-composited properties (`transform`, `opacity`) or explicit colors. Never animate layout properties (`width`, `height`, `top`, `left`, `margin`, `padding`).
43. **Grid Blow-Out Defense**: Always use `minmax(0, 1fr)` for image-bearing grid tracks, and `overflow-wrap: break-word; min-width: 0` on headings to prevent mobile horizontal blowouts.
44. **No Tracked-Uppercase Eyebrows**: Avoid tiny letterspaced uppercase pills (`FEATURE SPOTLIGHT`) floating above every heading. Use a disciplined body or subhead font in sentence case.
45. **No Universal Email Footer Band**: Do not end every page with a generic "Subscribe to our newsletter" form. Ground the closing section in the visitor's actual job (book, buy, install, try).

---

## The Litmus Test: The Logo Test

> **Remove the logo and name from the site. Could an informed user still identify the company or product?**

If not, the site is vibecoded slop. Replace generic decoration with product-specific visual metaphors, disciplined typography, intentional proportions, and demonstrable workflows.
