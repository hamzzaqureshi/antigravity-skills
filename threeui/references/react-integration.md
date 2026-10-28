# React & Next.js Integration Guide for Three.js & WebGL

> Best practices for integrating ThreeUI WebGL components into React and Next.js (App Router / Pages Router) without SSR hydration mismatches or memory leaks.

---

## 1. Next.js App Router: The SSR Boundary

WebGL relies directly on `window`, `document`, `HTMLCanvasElement`, and the browser GPU context (`canvas.getContext("webgl")`). These APIs **do not exist on the server**.

### The Golden Rule:
Any component rendering a WebGL canvas must:
1. Include `"use client";` at the top of the file.
2. Be dynamically imported with `ssr: false` if rendered from a Server Component.

```tsx
// app/page.tsx (Server Component)
import dynamic from "next/dynamic";

// Disable server-side rendering for the 3D scene
const LiquidFormBackground = dynamic(
  () => import("@/components/threeui/LiquidFormBackground").then((mod) => mod.LiquidFormBackground),
  { ssr: false }
);

export default function Page() {
  return (
    <main className="relative min-h-screen bg-black">
      {/* Background canvas sits behind page content */}
      <div className="absolute inset-0 pointer-events-none z-0">
        <LiquidFormBackground speed={1.2} noiseScale={1.5} />
      </div>

      <div className="relative z-10 max-w-5xl mx-auto pt-24 px-6">
        <h1 className="text-5xl font-bold text-white">Next Generation Visuals</h1>
      </div>
    </main>
  );
}
```

---

## 2. Robust React Canvas Pattern (Ref + Cleanup)

Here is the canonical React wrapper pattern used across ThreeUI components:

```tsx
"use client";

import { useEffect, useRef } from "react";
import * as THREE from "three";

export interface SceneProps {
  speed?: number;
  className?: string;
}

export function ThreeScene({ speed = 1.0, className = "" }: SceneProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const propsRef = useRef({ speed });
  propsRef.current = { speed }; // Keep mutable reference for render loop

  useEffect(() => {
    const container = containerRef.current;
    const canvas = canvasRef.current;
    if (!container || !canvas) return;

    // 1. Initialize Renderer
    const renderer = new THREE.WebGLRenderer({
      canvas,
      alpha: true,
      antialias: true,
      powerPreference: "high-performance",
    });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));

    // 2. Setup Scene & Camera
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
    camera.position.z = 5;

    // 3. Create Mesh / Shaders
    const geometry = new THREE.IcosahedronGeometry(1.5, 4);
    const material = new THREE.MeshStandardMaterial({
      color: 0x4f46e5,
      roughness: 0.2,
      metalness: 0.8,
    });
    const mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);

    // 4. Lighting
    const dirLight = new THREE.DirectionalLight(0xffffff, 2);
    dirLight.position.set(5, 5, 5);
    scene.add(dirLight);
    scene.add(new THREE.AmbientLight(0xffffff, 0.5));

    // 5. Responsive ResizeObserver
    const handleResize = () => {
      const { width, height } = container.getBoundingClientRect();
      if (width === 0 || height === 0) return;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height, false);
    };
    handleResize();

    const resizeObserver = new ResizeObserver(handleResize);
    resizeObserver.observe(container);

    // 6. Animation Loop
    let animId: number;
    let clock = new THREE.Clock();

    const animate = () => {
      const delta = clock.getDelta();
      const currentSpeed = propsRef.current.speed;

      mesh.rotation.x += 0.5 * delta * currentSpeed;
      mesh.rotation.y += 0.7 * delta * currentSpeed;

      renderer.render(scene, camera);
      animId = requestAnimationFrame(animate);
    };
    animate();

    // 7. Strict Cleanup
    return () => {
      cancelAnimationFrame(animId);
      resizeObserver.disconnect();
      geometry.dispose();
      material.dispose();
      renderer.dispose();
      renderer.forceContextLoss();
    };
  }, []);

  return (
    <div ref={containerRef} className={`relative w-full h-full overflow-hidden ${className}`}>
      <canvas ref={canvasRef} className="block w-full h-full pointer-events-auto" />
    </div>
  );
}
```

---

## 3. Integrating with React Three Fiber (`@react-three/fiber`)

When your project uses `@react-three/fiber` (R3F) and `@react-three/drei`:

```tsx
"use client";

import { Canvas, useFrame } from "@react-three/fiber";
import { Float, MeshDistortMaterial } from "@react-three/drei";
import { useRef } from "react";
import * as THREE from "three";

function FloatingOrb() {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += delta * 0.2;
    }
  });

  return (
    <Float speed={2} rotationIntensity={0.5} floatIntensity={1}>
      <mesh ref={meshRef}>
        <sphereGeometry args={[1.2, 64, 64]} />
        <MeshDistortMaterial
          color="#6366f1"
          roughness={0.1}
          metalness={0.9}
          distort={0.4}
          speed={2}
        />
      </mesh>
    </Float>
  );
}

export function HeroScene() {
  return (
    <div className="w-full h-[500px]">
      <Canvas
        camera={{ position: [0, 0, 4], fov: 45 }}
        dpr={[1, 1.5]}
        gl={{ antialias: true, alpha: true }}
      >
        <ambientLight intensity={0.5} />
        <directionalLight position={[10, 10, 5]} intensity={1.5} />
        <FloatingOrb />
      </Canvas>
    </div>
  );
}
```
