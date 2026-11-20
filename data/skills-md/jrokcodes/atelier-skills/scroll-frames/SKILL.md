---
name: scroll-frames
description: Apple-style scroll-driven frame animation — video to flipbook scroll experience
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Scroll Frames

Convert video into scroll-driven flipbook animations. The user scrolls, the video "plays" frame by frame — the signature Apple product page effect.

## When to Use

- Product reveal pages (hardware, SaaS, physical goods)
- Premium landing page hero sections
- Storytelling sequences where scroll = narrative progression
- Any "wow factor" moment that justifies the asset weight

Do NOT use for: background ambiance (use actual video), short UI transitions (use Framer Motion), content-heavy pages where scroll hijacking frustrates users.

## Pipeline Overview

```
Video (MP4) → ffmpeg (extract frames) → sharp (PNG → WebP) → Canvas API (render on scroll)
```

## Step 1: Source the Video

### Option A — Real footage
Record or obtain an MP4. Trim to the exact segment needed. Shorter = fewer frames = better performance.

### Option B — AI-generated transitions
Use this workflow for product/concept animations without real footage:

1. **Generate start and end keyframes** with Nano Banana 2 (or any image model)
2. **Generate transition video** with Kling 3.0 (image-to-video, 5s mode)
3. Export as MP4

**Background matching warning**: The generated video background MUST match your website's background color exactly. A white product on #0a0a0a video against a #000000 page creates a visible mismatch. Either:
- Specify the exact hex in your image generation prompt
- Post-process the video to replace the background
- Use a transparent/alpha channel workflow if the tool supports it

## Step 2: Extract Frames with ffmpeg

```bash
# Create output directory
mkdir -p frames

# Extract at 24 fps (standard — adjust for scroll feel)
ffmpeg -i input.mp4 -vf fps=24 "frames/frame_%04d.png"

# For a smoother scroll: 30 fps (more frames, larger payload)
ffmpeg -i input.mp4 -vf fps=30 "frames/frame_%04d.png"

# For a snappier scroll: 12 fps (fewer frames, lighter)
ffmpeg -i input.mp4 -vf fps=12 "frames/frame_%04d.png"
```

**Frame count math**: A 5-second video at 24fps = 120 frames. At ~50KB each (WebP) = ~6MB total. Budget accordingly.

### Resize during extraction (optional)

```bash
# Cap width at 1920px, maintain aspect ratio
ffmpeg -i input.mp4 -vf "fps=24,scale=1920:-1" "frames/frame_%04d.png"
```

## Step 3: Convert to WebP with Sharp

WebP is 25-35% smaller than JPEG at equivalent quality, with better transparency support.

### Batch conversion script

```js
// convert-frames.js
import sharp from "sharp";
import { readdir } from "fs/promises";
import { join } from "path";

const INPUT_DIR = "./frames";
const OUTPUT_DIR = "./frames-webp";

async function convert() {
  const files = (await readdir(INPUT_DIR))
    .filter((f) => f.endsWith(".png"))
    .sort();

  await import("fs").then((fs) =>
    fs.mkdirSync(OUTPUT_DIR, { recursive: true })
  );

  console.log(`Converting ${files.length} frames...`);

  const BATCH_SIZE = 20;
  for (let i = 0; i < files.length; i += BATCH_SIZE) {
    const batch = files.slice(i, i + BATCH_SIZE);
    await Promise.all(
      batch.map((file) =>
        sharp(join(INPUT_DIR, file))
          .webp({ quality: 80 })
          .toFile(join(OUTPUT_DIR, file.replace(".png", ".webp")))
      )
    );
    console.log(`  ${Math.min(i + BATCH_SIZE, files.length)}/${files.length}`);
  }

  console.log("Done.");
}

convert();
```

```bash
npm install sharp
node convert-frames.js
```

**Quality tuning**: `quality: 80` is the sweet spot. Below 70 you get visible artifacts on gradients. Above 85 the file size gains diminish.

## Step 4: React Scroll-Frame Component

```tsx
// ScrollFrames.tsx
import { useEffect, useRef, useState, useCallback } from "react";

interface ScrollFramesProps {
  /** Array of frame URLs in order */
  frames: string[];
  /** Width of the canvas */
  width: number;
  /** Height of the canvas */
  height: number;
  /** Scroll distance in vh units that maps to full animation (default: 300) */
  scrollSpan?: number;
  /** CSS class for the outer wrapper */
  className?: string;
}

export function ScrollFrames({
  frames,
  width,
  height,
  scrollSpan = 300,
  className,
}: ScrollFramesProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const imagesRef = useRef<HTMLImageElement[]>([]);
  const currentFrameRef = useRef(0);
  const rafRef = useRef<number>(0);
  const [loaded, setLoaded] = useState(false);

  // Preload all frames
  useEffect(() => {
    let cancelled = false;

    async function preload() {
      const images = await Promise.all(
        frames.map(
          (src) =>
            new Promise<HTMLImageElement>((resolve) => {
              const img = new Image();
              img.src = src;
              img.onload = () => resolve(img);
              img.onerror = () => resolve(img); // graceful degradation
            })
        )
      );

      if (!cancelled) {
        imagesRef.current = images;
        setLoaded(true);
        drawFrame(0);
      }
    }

    preload();
    return () => { cancelled = true; };
  }, [frames]);

  const drawFrame = useCallback(
    (index: number) => {
      const canvas = canvasRef.current;
      const ctx = canvas?.getContext("2d");
      const img = imagesRef.current[index];
      if (!ctx || !img || !img.complete) return;

      if (currentFrameRef.current === index) return; // skip if same frame
      currentFrameRef.current = index;
      ctx.clearRect(0, 0, width, height);
      ctx.drawImage(img, 0, 0, width, height);
    },
    [width, height]
  );

  // Scroll handler with IntersectionObserver gating
  useEffect(() => {
    const container = containerRef.current;
    if (!container || !loaded) return;

    let isVisible = false;

    const observer = new IntersectionObserver(
      ([entry]) => { isVisible = entry.isIntersecting; },
      { threshold: 0 }
    );
    observer.observe(container);

    function onScroll() {
      if (!isVisible) return;

      cancelAnimationFrame(rafRef.current);
      rafRef.current = requestAnimationFrame(() => {
        const rect = container!.getBoundingClientRect();
        const scrollHeight = container!.offsetHeight - window.innerHeight;
        const progress = Math.min(
          Math.max(-rect.top / scrollHeight, 0),
          1
        );
        const frameIndex = Math.min(
          Math.floor(progress * imagesRef.current.length),
          imagesRef.current.length - 1
        );
        drawFrame(frameIndex);
      });
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    return () => {
      window.removeEventListener("scroll", onScroll);
      observer.disconnect();
      cancelAnimationFrame(rafRef.current);
    };
  }, [loaded, drawFrame]);

  return (
    <div
      ref={containerRef}
      className={className}
      style={{ height: `${scrollSpan}vh`, position: "relative" }}
    >
      <canvas
        ref={canvasRef}
        width={width}
        height={height}
        style={{
          position: "sticky",
          top: "50%",
          transform: "translateY(-50%)",
          maxWidth: "100%",
          height: "auto",
        }}
      />
    </div>
  );
}
```

### Usage

```tsx
// Generate frame URLs
const frames = Array.from(
  { length: 120 },
  (_, i) => `/frames/frame_${String(i + 1).padStart(4, "0")}.webp`
);

<ScrollFrames
  frames={frames}
  width={1920}
  height={1080}
  scrollSpan={400}
  className="mx-auto max-w-7xl"
/>
```

## Step 5: Place Frames in Public Directory

```
public/
  frames/
    frame_0001.webp
    frame_0002.webp
    ...
    frame_0120.webp
```

For production, consider a CDN or image hosting service to reduce bundle size.

## Performance Best Practices

1. **WebP over JPEG** — 25-35% smaller at same quality, decode performance is equivalent
2. **Preload frames eagerly** — start loading as soon as the component mounts, not when visible
3. **Passive scroll listeners** — always `{ passive: true }` on scroll events
4. **Skip redundant draws** — track `currentFrameRef` and skip `drawImage` if frame index unchanged
5. **IntersectionObserver gating** — stop processing scroll events when the canvas is off-screen
6. **requestAnimationFrame throttling** — never draw more than once per frame
7. **Batch preloading** — for 200+ frames, load in chunks of 20-30 to avoid network congestion
8. **Resize canvas for mobile** — serve 960px-wide frames on mobile, 1920px on desktop
9. **Total payload budget** — aim for under 8MB for the full frame set; under 4MB is ideal

## Scroll Speed Tuning

The `scrollSpan` prop controls how much vertical scroll maps to the full animation.

| scrollSpan | Feel | Best for |
|------------|------|----------|
| 200vh | Fast, punchy | Short sequences (30-60 frames) |
| 300vh | Balanced | Standard product reveals |
| 500vh | Slow, cinematic | Detailed storytelling, many frames |

Test by scrolling at a natural pace. If it feels rushed, increase `scrollSpan`. If it feels draggy, decrease it.

## Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| ffmpeg | CLI tool | Frame extraction from video |
| sharp | npm package | PNG to WebP batch conversion |
| Canvas API | Browser built-in | Frame rendering |
| IntersectionObserver | Browser built-in | Visibility gating |

## Checklist Before Shipping

- [ ] Frame background matches page background color
- [ ] WebP quality tested at target size (no banding on gradients)
- [ ] Mobile frame set is smaller resolution than desktop
- [ ] Total frame payload is under budget
- [ ] First frame renders immediately on load (no blank canvas)
- [ ] Scroll feels natural at chosen `scrollSpan`
- [ ] No layout shift when canvas enters viewport
- [ ] Tested on throttled network (3G simulation)
