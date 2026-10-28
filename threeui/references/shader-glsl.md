# GLSL Shader & WebGL Effect Architecture

> In-depth reference for authoring custom GLSL shaders (Vertex & Fragment) for Three.js and raw WebGL effects in ThreeUI.

---

## 1. Shader Pipeline Overview

Shaders execute directly on the GPU in two distinct stages:

```text
3D Geometry (Vertices)
        ↓
[Vertex Shader]      → Transforms 3D object coordinates into 2D clip space (gl_Position)
        ↓
Rasterization & Interpolation
        ↓
[Fragment Shader]    → Calculates the final RGBA color for every pixel/fragment (gl_FragColor)
```

---

## 2. Standard ThreeUI Uniforms Contract

Most ThreeUI background and surface shaders communicate with JavaScript via these canonical uniforms:

```glsl
precision highp float;

uniform vec2  u_res;          // Canvas width & height in physical pixels (canvas.width, canvas.height)
uniform float u_time;         // Elapsed time in seconds (progresses animation)
uniform vec2  u_mouse;        // Normalized or pixel mouse coordinates
uniform float u_speed;        // Time scale multiplier
uniform float u_noise_scale;  // Spatial frequency of noise patterns
uniform vec3  u_color;        // Base color tint in RGB (0.0 to 1.0)
```

### Fullscreen Quad Vertex Shader:
For post-processing or 2D canvas background shaders that cover the full screen:

```glsl
// Minimal full-screen quad vertex shader
attribute vec2 a_pos;

void main() {
    gl_Position = vec4(a_pos, 0.0, 1.0);
}
```
JavaScript sets up two triangles with clip coordinates: `[-1, -1, 1, -1, -1, 1, 1, 1]`.

---

## 3. Simplex & Perlin Noise Patterns

Procedural organic effects (liquid flow, clouds, topography, ember storms) rely on noise.

### 2D / 3D Simplex Noise Formulation:
```glsl
vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec4 mod289(vec4 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec4 permute(vec4 x) { return mod289(((x * 34.0) + 1.0) * x); }
vec4 taylorInvSqrt(vec4 r) { return 1.79284291400159 - 0.85373472095314 * r; }

float snoise(vec3 v) {
  const vec2 C = vec2(1.0/6.0, 1.0/3.0);
  const vec4 D = vec4(0.0, 0.5, 1.0, 2.0);
  vec3 i  = floor(v + dot(v, C.yyy));
  vec3 x0 = v - i + dot(i, C.xxx);
  vec3 g = step(x0.yzx, x0.xyz);
  vec3 l = 1.0 - g;
  vec3 i1 = min(g.xyz, l.zxy);
  vec3 i2 = max(g.xyz, l.zxy);
  vec3 x1 = x0 - i1 + C.xxx;
  vec3 x2 = x0 - i2 + C.yyy;
  vec3 x3 = x0 - D.yyy;
  i = mod289(i);
  vec4 p = permute(permute(permute(
             i.z + vec4(0.0, i1.z, i2.z, 1.0))
           + i.y + vec4(0.0, i1.y, i2.y, 1.0))
           + i.x + vec4(0.0, i1.x, i2.x, 1.0));
  float n_ = 0.142857142857;
  vec3 ns = n_ * D.wyz - D.xzx;
  vec4 j = p - 49.0 * floor(p * ns.z * ns.z);
  vec4 x_ = floor(j * ns.z);
  vec4 y_ = floor(j - 7.0 * x_);
  vec4 x = x_ * ns.x + ns.yyyy;
  vec4 y = y_ * ns.x + ns.yyyy;
  vec4 h = 1.0 - abs(x) - abs(y);
  vec4 b0 = vec4(x.xy, y.xy);
  vec4 b1 = vec4(x.zw, y.zw);
  vec4 s0 = floor(b0) * 2.0 + 1.0;
  vec4 s1 = floor(b1) * 2.0 + 1.0;
  vec4 sh = -step(h, vec4(0.0));
  vec4 a0 = b0.xzyw + s0.xzyw * sh.xxyy;
  vec4 a1 = b1.xzyw + s1.xzyw * sh.zzww;
  vec3 p0 = vec3(a0.xy, h.x);
  vec3 p1 = vec3(a0.zw, h.y);
  vec3 p2 = vec3(a1.xy, h.z);
  vec3 p3 = vec3(a1.zw, h.w);
  vec4 norm = taylorInvSqrt(vec4(dot(p0,p0), dot(p1,p1), dot(p2,p2), dot(p3,p3)));
  p0 *= norm.x; p1 *= norm.y; p2 *= norm.z; p3 *= norm.w;
  vec4 m = max(0.6 - vec4(dot(x0,x0), dot(x1,x1), dot(x2,x2), dot(x3,x3)), 0.0);
  m = m * m;
  return 42.0 * dot(m * m, vec4(dot(p0,x0), dot(p1,x1), dot(p2,x2), dot(p3,x3)));
}
```

### Fractal Brownian Motion (FBM) for Multi-Octave Texture:
Layering multiple frequencies of noise generates terrain, clouds, and complex liquid folds:

```glsl
float fbm(vec3 p) {
    float total = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;
    for (int i = 0; i < 4; i++) {
        total += amplitude * snoise(p * frequency);
        frequency *= 2.0;
        amplitude *= 0.5;
    }
    return total;
}
```

---

## 4. Raymarching & Signed Distance Functions (SDF)

Used in ThreeUI's flagship 3D shaders like `liquid-form` (Velox) and `liquid-metal-button` to render mathematical 3D surfaces entirely in the fragment shader without polygon meshes.

### Raymarching Core Loop:
```glsl
#define MAX_STEPS 64
#define MAX_DIST 20.0
#define SURF_DIST 0.002

float sphereSDF(vec3 p, float radius) {
    return length(p) - radius;
}

// Scene Distance Evaluator
float getDist(vec3 p) {
    // Add simplex noise displacement to create organic morphing
    float displacement = snoise(p * u_noise_scale + u_time * u_speed) * 0.25;
    return sphereSDF(p, 1.2) + displacement;
}

// Raymarcher
float rayMarch(vec3 ro, vec3 rd) {
    float dO = 0.0;
    for (int i = 0; i < MAX_STEPS; i++) {
        vec3 p = ro + rd * dO;
        float dS = getDist(p);
        dO += dS;
        if (dO > MAX_DIST || abs(dS) < SURF_DIST) break;
    }
    return dO;
}

// Surface Normal Calculation (Gradient of SDF)
vec3 getNormal(vec3 p) {
    float d = getDist(p);
    vec2 e = vec2(0.001, 0.0);
    vec3 n = d - vec3(
        getDist(p - e.xyy),
        getDist(p - e.yxy),
        getDist(p - e.yyx)
    );
    return normalize(n);
}
```

---

## 5. Lighting & Reflection Model (Fresnel & Metalness)

```glsl
vec3 calculateLighting(vec3 p, vec3 n, vec3 ro) {
    vec3 lightPos = vec3(2.0, 4.0, 3.0);
    vec3 l = normalize(lightPos - p);
    vec3 v = normalize(ro - p);
    vec3 r = reflect(-l, n);

    // Diffuse component
    float diff = max(dot(n, l), 0.0);

    // Specular highlight
    float spec = pow(max(dot(r, v), 0.0), 32.0);

    // Fresnel reflection (bright rim light at glancing angles)
    float fresnel = pow(1.0 - max(dot(n, v), 0.0), 3.0);

    vec3 baseColor = vec3(0.85, 0.88, 0.95); // Silver/Liquid metallic
    return baseColor * (diff * 0.5 + 0.3) + vec3(1.0) * spec + vec3(0.5, 0.7, 1.0) * fresnel;
}
```
