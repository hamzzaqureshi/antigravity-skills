# Three.js & WebGL Production Architecture

> Core guidelines for building high-performance, robust 3D WebGL interfaces in web applications without memory leaks or frame drops.

---

## 1. Canvas Mounting & WebGL Lifecycle

When mounting Three.js into a modern web application (React, Vue, Svelte, or vanilla JS):

```typescript
// Standard production canvas initialization
const canvas = canvasRef.current;
const renderer = new THREE.WebGLRenderer({
  canvas,
  alpha: true,              // Transparent background for layering over UI
  antialias: true,          // Smooth edges (disable on low-end mobile if heavy)
  powerPreference: "high-performance",
});

// Clamp Device Pixel Ratio to prevent GPU overload on Retina/4K displays
const pixelRatio = Math.min(window.devicePixelRatio || 1, 2);
renderer.setPixelRatio(pixelRatio);
renderer.setSize(width, height, false);
```

### DPR Clamping (Crucial for 60 FPS)
Never allow raw `window.devicePixelRatio` on high-DPI devices (3x or 4x screens). A 4K phone rendering at 3x DPR pushes 9x more pixels per frame, instantly dropping frame rates:
```javascript
const dpr = Math.min(window.devicePixelRatio || 1, 1.5); // 1.5 for complex shaders, 2.0 max
renderer.setPixelRatio(dpr);
```

---

## 2. Strict Memory Management & Garbage Collection

WebGL resources (buffers, textures, render targets, shader programs) are allocated in GPU memory and **are NOT automatically collected by JavaScript garbage collection**. Failing to dispose them causes browser crashes and tab reloads.

### The Disposal Contract:
When unmounting or replacing a component:

```typescript
useEffect(() => {
  // Setup scene, camera, renderer...
  return () => {
    // 1. Cancel active animation frame
    if (animationFrameId) {
      cancelAnimationFrame(animationFrameId);
    }

    // 2. Remove resize and pointer listeners
    window.removeEventListener("resize", handleResize);

    // 3. Traverse and dispose every mesh, geometry, and material
    scene.traverse((object) => {
      if (object instanceof THREE.Mesh) {
        if (object.geometry) {
          object.geometry.dispose();
        }
        if (object.material) {
          if (Array.isArray(object.material)) {
            object.material.forEach((mat) => disposeMaterial(mat));
          } else {
            disposeMaterial(object.material);
          }
        }
      }
    });

    // 4. Dispose renderer and force context loss
    renderer.dispose();
    renderer.forceContextLoss();
  };
}, []);

function disposeMaterial(material: THREE.Material) {
  // Dispose all attached textures
  for (const key of Object.keys(material)) {
    const value = (material as any)[key];
    if (value && typeof value.dispose === "function" && value instanceof THREE.Texture) {
      value.dispose();
    }
  }
  material.dispose();
}
```

---

## 3. Responsive Resizing with ResizeObserver

Avoid listening only to `window.resize`. UI containers (such as cards, heroes, or modals) can resize independently due to CSS layout shifts, grid adjustments, or sidebar toggles.

```typescript
const container = containerRef.current;
const resizeObserver = new ResizeObserver((entries) => {
  for (const entry of entries) {
    const { width, height } = entry.contentRect;
    if (width === 0 || height === 0) return;

    camera.aspect = width / height;
    camera.updateProjectionMatrix();

    renderer.setSize(width, height, false);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  }
});

resizeObserver.observe(container);
// Cleanup: resizeObserver.disconnect();
```

---

## 4. The Render Loop: On-Demand vs Continuous

1. **Continuous Rendering (`requestAnimationFrame`)**:
   - Required for physics simulations, continuous waves, particle drift, fluid noise, and animated shaders.
   - Use `clock.getDelta()` or `performance.now()` rather than fixed frame increments for frame-rate independent motion.
   - **Pause when off-screen**: Use an `IntersectionObserver` to halt `requestAnimationFrame` when the canvas is scrolled out of the viewport.

2. **On-Demand Rendering**:
   - For static 3D models or scenes that only change on mouse move or orbit controls.
   - Only call `renderer.render(scene, camera)` when uniforms change or controls emit a `change` event. Saves significant battery on mobile.

---

## 5. WebGL Context Loss Recovery

Mobile browsers or systems under heavy GPU load can lose the WebGL context at any time. Handle it gracefully:

```typescript
canvas.addEventListener("webglcontextlost", (event) => {
  event.preventDefault();
  console.warn("WebGL Context Lost. Halting render loop.");
  cancelAnimationFrame(animationFrameId);
}, false);

canvas.addEventListener("webglcontextrestored", () => {
  console.info("WebGL Context Restored. Re-initializing scene.");
  reinitializeScene();
}, false);
```

---

## 6. Performance Budget Guidelines

| Metric | Target | Rationale |
|:---|:---|:---|
| **Frame Rate** | 60 FPS (120 FPS on ProMotion) | Never drop below 30 FPS under active interaction |
| **Draw Calls** | < 50 calls per frame | Batch geometries with `InstancedMesh` or merge buffers |
| **Poly Count** | < 100k triangles for mobile | Keep models optimized; use normal maps for micro-details |
| **Texture Size**| Max 2048×2048 (1024 preferred) | 4K textures cause mobile GPU memory pressure |
| **DPR** | Clamped to `1.5` or `2.0` | Prevents rendering 8M+ pixels on Retina screens |
| **Offscreen** | Pause render loop | Free CPU/GPU when user scrolls away |
