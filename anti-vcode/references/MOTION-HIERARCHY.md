# Layered Motion & Animation Hierarchy

Avoid the classic vibecoded animation anti-pattern:
> *"Every section fades in on scroll, every button shifts 2px on hover, a glowing cursor follows the mouse, and 5 animation libraries fight for 800KB of bundle weight."*

Instead, motion must have a strict single-owner hierarchy:

```text
                 EXPERIENCE
                     │
             ┌───────┴───────┐
             │               │
         STRUCTURE        DETAILS
             │               │
           GSAP            Motion
      (Choreography)     (UI States)
             │               │
          SCROLL          PHYSICS
             │               │
           Lenis        React Spring
      (Foundation)       (Gestures)
             │
          SPATIAL
             │
         Three.js
      (Conceptual 3D)
```

---

## 1. The Core Motion Stack

| Layer | Primary Library | Role | When to Use |
| :--- | :--- | :--- | :--- |
| **Component UI** | **Motion** (Framer Motion) | State transitions | Menus, expanding cards, modals, layout morphs, hover states, list additions. |
| **Choreography** | **GSAP** | Multi-step timelines | Coordinated page entrance, pinned scroll narratives, synchronized typography reveals. |
| **Spatial / 3D** | **Three.js / WebGL** | Conceptual 3D scenes | **Only** when 3D is a core product feature (data topology, spatial map, physical product CAD). |
| **Scroll Foundation**| **Lenis** | Smooth scroll coordination | When entire page relies on synchronized, scrubbed timeline animation. |

---

## 2. Motion Rules & Anti-Patterns

### What to Do
1. **Assign One Tool Per Job**: Do not animate buttons with GSAP and modals with Motion. Motion owns the UI; GSAP owns cinematic timelines.
2. **Fast & Snappy UI**: Interface interactions (dropdowns, tabs, clicks) must finish under **180ms - 240ms** using cubic-bezier deceleration curves (`ease-out`).
3. **Tactile Feedback Over Floating**: Instead of moving 2px up on hover, provide active `:active` press scale (e.g., `scale(0.98)`), clear focus rings, and tonal shifts.
4. **Coordinated Hero Moment**: If orchestrating a page entrance:
   ```text
   Page Load ──► Headline unmasks ──► Product visual settles ──► Interface controls arm
   ```

### What to Ban
1. **No Universal Viewport Fade-Ins**: Do NOT attach scroll triggers to every single card and text block. It makes users wait for basic content to appear.
2. **No Faux "Premium" 3D Props**: Ban spinning metallic chrome cubes, floating spheres, and decorative 3D doughnuts that convey zero information.
3. **No Mouse-Following Glow Beams**: Radial gradients tracking mouse coordinates add CPU overhead and visually obscure text.
4. **No Aimless Particle Canvases**: Banned unless developing a literal astronomy or physics simulation.
