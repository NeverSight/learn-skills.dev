---
name: 3dsvg-interactive-react
description: Turn SVGs into interactive React 3D components using the 3dsvg library and visual editor
triggers:
  - turn my SVG into a 3D component
  - add 3D effect to SVG in React
  - use 3dsvg library
  - make SVG spin in 3D
  - embed 3D SVG in my app
  - install 3dsvg npm package
  - SVG3D component props
  - export 3D model from SVG
---

# 3dsvg — Interactive React 3D Components from SVGs

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

`3dsvg` extrudes SVG paths, text, and shapes into fully interactive 3D React components powered by Three.js and React Three Fiber. It ships as an embeddable `<SVG3D>` component (npm) plus a visual editor at [3dsvg.design](https://3dsvg.design).

## Installation

```bash
npm install 3dsvg
# or
yarn add 3dsvg
# or
pnpm add 3dsvg
```

**Peer dependencies** (install if not already present):

```bash
npm install three @react-three/fiber @react-three/drei
```

## Quick Start

```tsx
import { SVG3D } from "3dsvg";

// Spin text in 3D
<SVG3D text="Hello" animate="spin" />

// 3D logo from SVG file
<SVG3D svg="/logo.svg" material="gold" />

// Pixel editor input
<SVG3D svg="<svg>...</svg>" material="chrome" animate="float" />
```

## SVG3DProps — Full API

```tsx
import { SVG3D } from "3dsvg";

<SVG3D
  // Input (choose one)
  text="Hello World"          // Text string (uses Google Fonts)
  svg="/path/to/file.svg"     // URL to SVG file
  // svg="<svg>...</svg>"     // Raw SVG markup string

  // Font (when using text=)
  font="Inter"                // Google Font name (10 presets available)

  // Material preset
  material="default"          // "default" | "plastic" | "metal" | "glass"
                              // "rubber" | "chrome" | "gold" | "clay"
                              // "emissive" | "holographic"

  // Animation
  animate="spin"              // "spin" | "float" | "pulse" | "wobble"
                              // "swing" | "spin+float" | undefined (static)

  // Geometry
  depth={0.2}                 // Extrusion depth (default: 0.2)
  bevelEnabled={true}         // Enable bevel on edges
  bevelThickness={0.02}       // Bevel thickness
  bevelSize={0.02}            // Bevel size
  bevelSegments={3}           // Bevel smoothness

  // Lighting
  ambientIntensity={0.5}      // Ambient light (0–1)
  keyLightIntensity={1.0}     // Key light brightness
  keyLightX={5}               // Key light X position
  keyLightY={5}               // Key light Y position
  keyLightZ={5}               // Key light Z position
  shadows={true}              // Enable shadow casting

  // Camera
  zoom={1}                    // Initial zoom level
  autoRotate={false}          // Auto-rotate camera (overrides animate)

  // Texture
  texture="none"              // "none" or procedural preset name, or URL
/>
```

## Common Patterns

### Basic Logo Viewer

```tsx
import { SVG3D } from "3dsvg";

export function LogoViewer() {
  return (
    <div style={{ width: 400, height: 400 }}>
      <SVG3D
        svg="/logo.svg"
        material="metal"
        animate="float"
        depth={0.3}
        bevelEnabled={true}
        bevelThickness={0.03}
      />
    </div>
  );
}
```

### Interactive 3D Text Badge

```tsx
import { SVG3D } from "3dsvg";

export function HeroBadge() {
  return (
    <SVG3D
      text="LAUNCH"
      font="Inter"
      material="chrome"
      animate="spin"
      depth={0.4}
      keyLightIntensity={1.5}
      ambientIntensity={0.3}
    />
  );
}
```

### Static Product Icon (No Animation)

```tsx
import { SVG3D } from "3dsvg";

export function ProductIcon({ svgUrl }: { svgUrl: string }) {
  return (
    <SVG3D
      svg={svgUrl}
      material="gold"
      depth={0.15}
      bevelEnabled={true}
      shadows={true}
      ambientIntensity={0.6}
      keyLightX={3}
      keyLightY={8}
      keyLightZ={3}
    />
  );
}
```

### Holographic Animated Logo

```tsx
import { SVG3D } from "3dsvg";

export function HolographicLogo() {
  return (
    <SVG3D
      svg="/brand.svg"
      material="holographic"
      animate="spin+float"
      depth={0.1}
      ambientIntensity={0.8}
    />
  );
}
```

### Inline SVG String

```tsx
import { SVG3D } from "3dsvg";

const starSvg = `
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <polygon points="50,5 61,35 95,35 68,57 79,91 50,70 21,91 32,57 5,35 39,35"
    fill="#FFD700"/>
</svg>
`;

export function Star3D() {
  return (
    <SVG3D
      svg={starSvg}
      material="gold"
      animate="pulse"
      depth={0.25}
    />
  );
}
```

## Material Presets Reference

| Value | Description |
|-------|-------------|
| `"default"` | Standard PBR material |
| `"plastic"` | Smooth, slightly shiny plastic |
| `"metal"` | Matte metallic surface |
| `"glass"` | Transparent glass look |
| `"rubber"` | Soft matte rubber |
| `"chrome"` | High-gloss mirror chrome |
| `"gold"` | Warm gold PBR |
| `"clay"` | Soft diffuse clay (great for screenshots) |
| `"emissive"` | Glowing emission effect |
| `"holographic"` | Iridescent rainbow foil |

## Animation Presets Reference

| Value | Description |
|-------|-------------|
| `"spin"` | Continuous Y-axis rotation |
| `"float"` | Gentle up/down bob |
| `"pulse"` | Breathing scale animation |
| `"wobble"` | Side-to-side wobble |
| `"swing"` | Pendulum swing |
| `"spin+float"` | Spin combined with float |
| `undefined` | Static, user-draggable only |

## Monorepo Development Setup

```bash
git clone https://github.com/renatoworks/3dsvg.git
cd 3dsvg
npm install
npm run build:engine   # Build the npm package
npm run dev:web        # Start the visual editor at localhost:3000
```

### Engine package only

```bash
cd packages/engine
npm run build          # Outputs to dist/
npm run dev            # Watch mode
```

### Project Structure

```
packages/
├── engine/src/
│   ├── index.tsx      # SVG3D public component
│   ├── scene.tsx      # Three.js scene, ExtrudedSVG mesh
│   ├── controls.tsx   # Animation logic, orbit controls
│   ├── materials.ts   # PBR material preset definitions
│   ├── types.ts       # SVG3DProps TypeScript types
│   └── use-font.ts    # Google Font → vector path loader
└── web/src/
    ├── app/           # Next.js pages
    ├── components/    # Editor UI panels, export bar
    └── lib/           # Texture generators, FFmpeg utils
```

## TypeScript Types

```tsx
import type { SVG3DProps } from "3dsvg";

const config: SVG3DProps = {
  svg: "/logo.svg",
  material: "chrome",
  animate: "float",
  depth: 0.3,
};

export function MyComponent() {
  return <SVG3D {...config} />;
}
```

## Next.js Integration

Because `SVG3D` uses Three.js (browser-only), use dynamic import with `ssr: false`:

```tsx
// components/Logo3D.tsx
"use client";
import dynamic from "next/dynamic";

const SVG3D = dynamic(
  () => import("3dsvg").then((m) => m.SVG3D),
  { ssr: false, loading: () => <div>Loading 3D...</div> }
);

export function Logo3D() {
  return (
    <SVG3D
      svg="/logo.svg"
      material="gold"
      animate="spin"
    />
  );
}
```

## Vite / React Integration

```tsx
// No special config needed — just import and use
import { SVG3D } from "3dsvg";

function App() {
  return (
    <div style={{ height: "100vh" }}>
      <SVG3D text="Vite + 3D" material="plastic" animate="float" />
    </div>
  );
}
```

## Visual Editor Workflow

1. Go to [3dsvg.design](https://3dsvg.design)
2. Choose an input method: **Text**, **Pixel Editor**, **SVG Code**, or **File Upload**
3. Pick a material, animation, and lighting configuration
4. Use the **Embed** export to copy a ready-to-paste `<SVG3D>` JSX snippet
5. Export as **PNG** (up to 4K), **Video** (MP4/WebM), or **3D Model** (GLB/STL/OBJ/PLY)

Drag and drop an SVG file anywhere on the editor to load it instantly.

## Troubleshooting

**Component renders blank / white screen**
- Ensure `three`, `@react-three/fiber`, and `@react-three/drei` are installed
- In Next.js, confirm you're using `dynamic` with `ssr: false`
- Wrap in a container with explicit `width` and `height`

**SVG not extruding correctly**
- Use simple, closed SVG paths; complex compound paths may not extrude
- Inline `fill` attributes on paths are respected — avoid CSS-only fills
- Try increasing `bevelSegments` for smoother curves

**Text not loading**
- The `font` prop loads from Google Fonts — ensure network access or host fonts locally
- Supported fonts are the 10 presets defined in `use-font.ts`

**Performance issues**
- Reduce `bevelSegments` (try `1` or `2`)
- Disable `shadows` for lower-end devices
- Use `animate={undefined}` for static display

**FFmpeg/video export fails in dev**
- Video export uses FFmpeg WASM and requires `SharedArrayBuffer`
- Add these headers to your dev server: `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp`

## License

MIT — [Renato Costa](https://renato.works) / [Blueberry](https://meetblueberry.com)
