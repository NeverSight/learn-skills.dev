---
name: spline-3d
description: Integrate free 3D assets from Spline.design into React projects
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Spline 3D

Integrate interactive 3D scenes from Spline.design into React applications. Spline is a collaborative 3D design tool with a generous free tier and a large community library of remixable assets.

## What is Spline

Spline (spline.design) is a browser-based 3D design tool that lets you create, animate, and export interactive 3D scenes. Key facts:

- **Free tier** includes unlimited projects, community assets, and code export
- **No 3D modeling skills required** — remix community assets or use the visual editor
- **Built-in interactions** — hover, click, scroll, and drag events on 3D objects
- **Code export** — generates a `.splinecode` bundle you embed via `<iframe>` or React component

## When to Use

- Hero section backgrounds with depth and interactivity
- Interactive product displays (rotate, zoom, explode views)
- Floating 3D decorative elements (orbs, shapes, abstract art)
- Portfolio/agency sites where visual impact matters
- Onboarding sequences with 3D illustrations

## When NOT to Use

- Small icons or UI elements (overkill, use SVG)
- Pages with multiple heavy sections (one Spline scene per page max)
- Content-heavy pages where 3D distracts from readability
- Mobile-first projects where performance is paramount (Spline is GPU-intensive)

## Finding Assets

### Browse the Community Library

1. Go to **spline.design**
2. Click **Discover** in the top nav
3. Browse **Community** tab
4. Use filters:
   - **Website** — assets designed for web integration
   - **3D** — general 3D objects and scenes
   - **Animation** — pre-animated assets
5. Search by keyword: "abstract", "gradient", "product", "geometric", "blob"

### Top Categories for Web Projects

| Search Term | What You Get |
|-------------|-------------|
| "gradient blob" | Organic animated shapes for backgrounds |
| "product mockup" | Phone/laptop/device frames |
| "abstract background" | Geometric compositions for hero sections |
| "floating shapes" | Decorative 3D elements |
| "interactive" | Scenes with hover/click events built in |

## Remixing Assets

1. Find an asset you like
2. Click **Remix** (fork icon) — this copies it to your workspace
3. In the Spline editor:
   - Change colors: select object → Material panel → adjust Color/Gradient
   - Remove objects: select → Delete
   - Adjust camera: drag viewport, set default camera angle
   - Remove background: Scene panel → Background → set to transparent or match your site color
   - Adjust lighting: select lights in the scene tree → tweak intensity/color
4. Preview with **Play** button

### Background Removal

Critical for web integration — you almost always want a transparent or color-matched background:

1. Open Scene panel (left sidebar)
2. Click **Background**
3. Set to **Transparent** for overlay use
4. Or set to your exact site background hex for seamless blending

## Exporting for Web

### Code Export (Recommended)

1. Click **Export** (top-right)
2. Select **Code Export**
3. Choose **vanilla.js**
4. Copy the scene URL — it looks like:
   ```
   https://prod.spline.design/aBcDeFgHiJkLmNoP/scene.splinecode
   ```

### Direct Embed (Quick and Dirty)

Spline also provides an `<iframe>` embed code. This works but gives you less control:

```html
<iframe
  src="https://my.spline.design/[ID]"
  frameborder="0"
  width="100%"
  height="100%"
/>
```

Use the React component approach instead for production sites.

## React Integration

### Install

```bash
npm install @splinetool/react-spline
```

### Basic Usage

```tsx
import Spline from "@splinetool/react-spline";

export function Hero3D() {
  return (
    <div className="relative h-screen w-full overflow-hidden">
      <Spline scene="https://prod.spline.design/aBcDeFgHiJkLmNoP/scene.splinecode" />
    </div>
  );
}
```

### With Loading State

```tsx
import Spline from "@splinetool/react-spline";
import { useState } from "react";

export function Hero3D() {
  const [isLoaded, setIsLoaded] = useState(false);

  return (
    <div className="relative h-screen w-full overflow-hidden">
      {!isLoaded && (
        <div className="absolute inset-0 flex items-center justify-center bg-neutral-950">
          <div className="h-8 w-8 animate-spin rounded-full border-2 border-white/20 border-t-white" />
        </div>
      )}
      <Spline
        scene="https://prod.spline.design/aBcDeFgHiJkLmNoP/scene.splinecode"
        onLoad={() => setIsLoaded(true)}
        style={{ opacity: isLoaded ? 1 : 0, transition: "opacity 0.5s ease" }}
      />
    </div>
  );
}
```

## Interactive Spline (Code API)

Spline scenes can be controlled programmatically. This is how you trigger animations, respond to user events, or sync 3D state with React state.

### Access the Spline Runtime

```tsx
import Spline from "@splinetool/react-spline";
import type { Application } from "@splinetool/runtime";
import { useRef } from "react";

export function InteractiveScene() {
  const splineRef = useRef<Application | null>(null);

  function onLoad(spline: Application) {
    splineRef.current = spline;
  }

  function handleClick() {
    // Find a named object in the scene and trigger its event
    const cube = splineRef.current?.findObjectByName("Cube");
    if (cube) {
      // Trigger the mouseDown event on the object
      splineRef.current?.emitEvent("mouseDown", cube);
    }
  }

  return (
    <>
      <Spline
        scene="https://prod.spline.design/[ID]/scene.splinecode"
        onLoad={onLoad}
      />
      <button onClick={handleClick} className="absolute bottom-8 left-1/2 -translate-x-1/2">
        Interact
      </button>
    </>
  );
}
```

### Common Runtime Methods

```ts
// Find objects by name (set in Spline editor)
const obj = spline.findObjectByName("ProductModel");

// Trigger events
spline.emitEvent("mouseDown", obj);
spline.emitEvent("mouseHover", obj);

// Set variables (if defined in Spline)
spline.setVariable("color", "#ff0000");
spline.setVariable("progress", 0.5);
```

### Naming Convention

In the Spline editor, give objects descriptive names (not "Object 1"). Use PascalCase:
- `HeroOrb`
- `ProductPhone`
- `BackgroundMesh`

These names are what `findObjectByName` searches for.

## Self-Hosting .splinecode Files

By default, Spline serves the `.splinecode` bundle from `prod.spline.design`. For production, self-host to avoid:
- CORS issues
- Dependency on Spline CDN availability
- Potential rate limits

### Steps

1. Export from Spline as **Binary (.splinecode file)**
   - Export → Download → `.splinecode`
2. Place in your `public/` directory:
   ```
   public/
     spline/
       hero-scene.splinecode
   ```
3. Reference locally:
   ```tsx
   <Spline scene="/spline/hero-scene.splinecode" />
   ```

**File size warning**: `.splinecode` files range from 500KB to 10MB+ depending on scene complexity. Check your bundle budget.

## Performance Optimization

### Lazy Load with IntersectionObserver

Don't load the Spline scene until it's near the viewport:

```tsx
import { useEffect, useRef, useState } from "react";

export function LazySpline({ scene }: { scene: string }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [shouldLoad, setShouldLoad] = useState(false);

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setShouldLoad(true);
          observer.disconnect();
        }
      },
      { rootMargin: "200px" } // start loading 200px before visible
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return (
    <div ref={containerRef} className="h-screen w-full">
      {shouldLoad && (
        <SplineComponent scene={scene} />
      )}
    </div>
  );
}

// Dynamic import to code-split the Spline runtime
import { lazy, Suspense } from "react";
const SplineComponent = lazy(() => import("@splinetool/react-spline"));
```

### Mobile Considerations

Spline scenes are GPU-intensive. On mobile:

```tsx
import { useEffect, useState } from "react";

function useIsMobile(breakpoint = 768) {
  const [isMobile, setIsMobile] = useState(false);
  useEffect(() => {
    const mq = window.matchMedia(`(max-width: ${breakpoint}px)`);
    setIsMobile(mq.matches);
    const handler = (e: MediaQueryListEvent) => setIsMobile(e.matches);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, [breakpoint]);
  return isMobile;
}

export function AdaptiveHero() {
  const isMobile = useIsMobile();

  return (
    <div className="h-screen w-full">
      {isMobile ? (
        // Static image fallback on mobile
        <img src="/hero-fallback.webp" alt="" className="h-full w-full object-cover" />
      ) : (
        <Spline scene="/spline/hero-scene.splinecode" />
      )}
    </div>
  );
}
```

### Performance Checklist

- [ ] Only one Spline scene per page
- [ ] Lazy loaded (not in initial bundle)
- [ ] Mobile fallback to static image
- [ ] `.splinecode` file is under 5MB
- [ ] Scene uses low-poly meshes where possible
- [ ] Unused objects removed from scene before export
- [ ] Background set to transparent or color-matched

## Spline + Scroll Integration

Combine with scroll progress for parallax-like 3D effects:

```tsx
function onLoad(spline: Application) {
  splineRef.current = spline;

  window.addEventListener("scroll", () => {
    const progress = window.scrollY / (document.body.scrollHeight - window.innerHeight);
    spline.setVariable("scrollProgress", progress);
  }, { passive: true });
}
```

In the Spline editor, create a variable called `scrollProgress` (0 to 1) and bind it to object rotation, position, or material opacity.

## Best Use Cases

| Use Case | Approach |
|----------|----------|
| Hero background | Full-bleed scene, transparent BG, lazy loaded |
| Product showcase | Interactive scene with hover/click events |
| Floating accent | Small scene positioned absolutely, low poly |
| Scroll storytelling | Variable-driven scene synced to scroll position |
| Loading screen | Animated scene displayed during app initialization |

## Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| @splinetool/react-spline | npm | React wrapper component |
| @splinetool/runtime | npm (peer) | Runtime API for interactivity |
| Spline.design account | Web service | Create/remix/export scenes |
