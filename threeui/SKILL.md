---
name: threeui
description: "3D, WebGL, and Three.js interactive UI component intelligence. 104 production-grade Three.js components, shaders, interactive backgrounds, 3D buttons, hero scenes, kinetic typography, and landing pages from DesignCode / ThreeUI. Provides instant search, shader code retrieval, WebGL lifecycle management, 60fps performance optimization, and React/Next.js integration."
---

# ThreeUI - 3D & WebGL Component Intelligence

Production-grade 3D, WebGL, and Three.js design intelligence derived from DesignCode's ThreeUI library. Contains 104 production-tested Three.js components, custom GLSL shaders, raymarched surfaces, interactive buttons, kinetic typography, and full 3D landing experiences across 9 categories.

---

## When to Apply

Use this skill whenever the task involves **3D, WebGL, Three.js, Canvas, or Shader engineering**:
- Adding interactive 3D hero scenes, animated backgrounds, or particle systems
- Building raymarched liquid metal buttons, glowing glass CTAs, or tactile toggles
- Implementing kinetic typography, morphing glyphs, or audio/particle wordmarks
- Integrating Three.js / WebGL into React or Next.js App Router applications
- Auditing and fixing WebGL memory leaks, context loss, layout thrashing, or low FPS

Skip this skill for standard flat CSS layouts, generic 2D forms, or non-visual backend services.

---

## Catalog Categories (104 Components)

| Category | Count | Highlights |
|:---|:---|:---|
| **Backgrounds** | 29 | `liquid-form` (Velox silver raymarching), `bell-field`, `flow-field`, `crt`, `halo`, `elements`, `constellation-field`, `stream-convergence` |
| **Buttons & CTAs** | 20 | `liquid-metal-button` (Prismatic WebGL 2), `plasma-button`, `ignition-button`, `induction-button`, `dot-border-button`, `lumen-cta` |
| **Three.js Scenes** | 20 | `globe` (layered FBM energy orb), `laser`, `japanese-tower`, `temple-night`, `landscape`, `bookshelf`, `structure-flow` |
| **Text Animation** | 14 | `typography-vortex`, `semantic-bloom`, `particle-wordmark`, `audio-wordmark`, `morphing-glyph-cloud`, `neon-typography` |
| **UI Elements** | 9 | `animated-top-dock`, `spark-badge`, `performance-gauges`, `connectivity-graph`, `uplink-loader`, `diagnostics-panel` |
| **CSS Effects** | 5 | `dark-glass`, `glassmorphism-cta`, `spinning-border-button`, `sliding-text-cta` |
| **Hero Sections** | 3 | `sylva-hero`, `complete-shelf-landing-page`, `bestsellers-book-showcase` |
| **Landing Pages** | 2 | `kage-landing-page`, `meng-to-sketchbook-landing-page` |
| **Sections** | 2 | `editorial-intro-section`, `newsletter-footer-section` |

For the complete catalog of all 104 components with descriptions, props, and runtimes, read [component-catalog.md](./references/component-catalog.md).

---

## CLI Search & Extraction Engine

The bundled tool `scripts/threeui.py` is zero-dependency (Python 3 stdlib only) and provides instant local search, inspection, and code extraction:

```bash
# 1. Search components by keyword or effect
python3 scripts/threeui.py search "liquid"
python3 scripts/threeui.py search "wave" --category Backgrounds
python3 scripts/threeui.py search "button" --limit 5

# 2. View component details, uniforms, and controls
python3 scripts/threeui.py info liquid-form
python3 scripts/threeui.py info spark-badge

# 3. View/dump complete source code (TSX + GLSL shaders)
python3 scripts/threeui.py code liquid-form

# 4. Export component files directly into user's project
python3 scripts/threeui.py export liquid-form --output-dir ./src/components/threeui

# 5. List categories and component counts
python3 scripts/threeui.py categories
```

---

## Core Operational Workflow

### Step 1: Identify the Visual Intent
Determine what 3D effect best fits the project:
- **Atmospheric Background**: Raymarched liquid (`liquid-form`), floating simplex noise (`flow-field`), matrix CRT (`crt`), or celestial particles (`constellation-field`).
- **High-Impact CTA**: Liquid metal button (`liquid-metal-button`), plasma button (`plasma-button`), or glassmorphism glow pill.
- **Hero Centerpiece**: 3D globe / energy orb (`energy-orb`), laser grid (`laser`), or living world scene (`sylva-hero`).
- **Kinetic Wordmark**: Audio/Particle responsive typography (`particle-wordmark`).

### Step 2: Query the Catalog
Run `scripts/threeui.py search "<keyword>"` to find verified, authored implementations rather than hallucinating Three.js scenes from scratch.

### Step 3: Inspect Uniforms & Controls
Run `scripts/threeui.py info <id>` to understand the available configuration knobs (`speed`, `noiseScale`, `mouseAmount`, `camera`, `color`).

### Step 4: Implement with Strict Production Guardrails
When delivering code, ALWAYS adhere to the following Three.js / WebGL rules:

1. **DPR Clamping (Crucial for 60 FPS)**:
   ```typescript
   const dpr = Math.min(window.devicePixelRatio || 1, 1.5); // 1.5 for heavy shaders, 2.0 max
   renderer.setPixelRatio(dpr);
   ```
2. **Next.js SSR Boundary**:
   Add `"use client";` to WebGL components. In Server Components, import dynamically with `{ ssr: false }`:
   ```tsx
   import dynamic from "next/dynamic";
   const LiquidForm = dynamic(() => import("./LiquidFormBackground").then(m => m.LiquidFormBackground), { ssr: false });
   ```
3. **Strict Resource Disposal**:
   Always dispose geometries, materials, textures, and cancel `requestAnimationFrame` on unmount to prevent GPU memory leaks:
   ```typescript
   return () => {
     cancelAnimationFrame(animId);
     geometry.dispose();
     material.dispose();
     renderer.dispose();
     renderer.forceContextLoss();
   };
   ```
4. **Pause When Offscreen**:
   Use an `IntersectionObserver` to stop the render loop when the canvas is outside the viewport.

---

## Detailed Architectural Guides

- [threejs-core.md](./references/threejs-core.md) — Three.js lifecycle, render loops, responsive ResizeObserver, context loss recovery, and disposal contracts.
- [shader-glsl.md](./references/shader-glsl.md) — GLSL vertex/fragment shaders, uniforms, 2D/3D simplex noise, raymarching SDFs, and Fresnel lighting.
- [react-integration.md](./references/react-integration.md) — React & Next.js App Router integration, Canvas refs, R3F patterns, and dynamic SSR imports.
- [component-catalog.md](./references/component-catalog.md) — Full directory of all 104 components with descriptions and props.
