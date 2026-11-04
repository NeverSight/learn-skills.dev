---
name: product-mockup
description: >
  Product mockups and showcases: photoreal product/packaging scenes via Gemini 3.1 Flash
  image editing, and pixel-exact device frames (phone, laptop, browser) around real
  screenshots via HTML/CSS. Covers 3D CSS transforms, lifestyle staging, feature callouts,
  before/after, and e-commerce product shots. Use when the goal is presenting a product or
  UI itself; for a marketing graphic that merely includes a product use graphic-design,
  social-media-graphic, or ad-creative-design.
  Trigger phrases: "create a product mockup", "device mockup", "phone mockup",
  "laptop mockup", "product showcase", "screenshot mockup", "app preview",
  "product presentation", "mockup design".
license: MIT
---

# Product Mockup Design

Create professional product mockups and showcases. Two paths:

- **Gemini (default for physical products):** product photo + prompt -> photoreal staged scene, packaging, lifestyle shot
- **HTML/CSS (default for app/web screenshots):** Gemini redraws UI and will alter text, icons, and layout, so wrap real screenshots in CSS device frames (Steps 3-9) and render to PNG. For a photoreal device scene, generate the scene with a blank screen, then composite the screenshot in code

---

## Step 1: Load Design Context

1. Read `.agents/design-context.md` first -- brand colors (hex), fonts, style archetype
2. If missing, use the `design-context` Default Fallbacks and tell the user defaults were used
3. Product mockups should match the brand's design style (minimal, bold, luxurious, etc.)

---

## Gemini Image Generation Path

Pipeline/CLI: `image-generation`. Prompt craft, cropping, and text-overlay fallback: `graphic-design` Step 3.

1. Pass the product photo with `--image product.png` and say "keep the product's shape, colors, label text, and logo exactly as in the reference"
2. Ratio: 1:1 or 4:5 for e-commerce and social, 16:9 or 3:2 for web heroes; crop to exact pixels with `--resize WxH`
3. Read the output PNG and compare it with the source photo: label text, logo, proportions, color, and part count must match. AI "improvements" to the product are defects. Fix one issue per follow-up turn
4. Marketplace main images (e.g. Amazon) usually require a pure white #FFFFFF background, the product filling ~85% of the frame, and >=1000px on the longest side (1600+ for zoom) -- check the marketplace's current rules

### Example Prompts

- **Product Photo:** "Place this [product] on a [background description]. Professional product photography style. [lighting]. [additional elements]."
- **Device Mockup:** "Create a [device type] mockup showing [app/website screenshot]. [angle/perspective] view on a [surface/background]. Soft shadows, [lighting style]. Clean, realistic presentation."
- **Packaging Mockup:** "Create a product packaging mockup for [brand]. [box/bottle/bag] with [label design description] on a [background]. Studio lighting, [additional props]. Premium, shelf-ready look."

---

## Step 2: Identify Mockup Type

| Type | Best For | Key Technique |
|------|----------|---------------|
| **Device Frame** | App/web screenshots | CSS device shells |
| **Lifestyle/Context** | Product in environment | Background + shadows |
| **3D Perspective** | Dynamic presentation | CSS perspective/transform |
| **Before/After** | Transformations | Split view comparison |
| **Feature Callout** | Highlighting features | Lines + labels |
| **Packaging** | Physical product boxes | 3D box with CSS |
| **Multi-Device** | Responsive showcase | Multiple frames |
| **Screenshot Frame** | Clean screenshot display | Window chrome + shadow |

---

## Step 3: Device Mockup Frames

### iPhone / Smartphone Frame

```css
.phone-mockup {
  position: relative; width: 280px; height: 572px; background: #1a1a1a;
  border-radius: 40px; padding: 12px;
  box-shadow: 0 0 0 2px #333, 0 0 0 4px #1a1a1a, 0 20px 60px rgba(0,0,0,0.4);
}
.phone-mockup .screen { width: 100%; height: 100%; border-radius: 30px; overflow: hidden; background: #fff; position: relative; }
.phone-mockup .dynamic-island {
  position: absolute; top: 10px; left: 50%; transform: translateX(-50%);
  width: 100px; height: 28px; background: #000; border-radius: 20px; z-index: 10;
}
.phone-mockup .screen img { width: 100%; height: 100%; object-fit: cover; border-radius: 30px; }
```

### Laptop / MacBook Frame

```css
.laptop-mockup { position: relative; width: 680px; }
.laptop-screen { background: #222; border-radius: 12px 12px 0 0; padding: 16px 16px 0; position: relative; }
.laptop-screen .screen { width: 100%; aspect-ratio: 16/10; background: #fff; border-radius: 4px 4px 0 0; overflow: hidden; }
.laptop-screen::before { content: ''; position: absolute; top: 6px; left: 50%; transform: translateX(-50%); width: 6px; height: 6px; background: #444; border-radius: 50%; }
.laptop-base { height: 14px; background: linear-gradient(180deg, #ccc 0%, #aaa 100%); border-radius: 0 0 8px 8px; }
```

### Browser Window Frame

```css
.browser-mockup { width: 800px; border-radius: 8px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
.browser-chrome { background: #E5E7EB; padding: 10px 16px; display: flex; align-items: center; gap: 8px; }
.browser-dots { display: flex; gap: 6px; }
.browser-dots span { width: 10px; height: 10px; border-radius: 50%; }
.browser-dots span:nth-child(1) { background: #EF4444; }
.browser-dots span:nth-child(2) { background: #F59E0B; }
.browser-dots span:nth-child(3) { background: #22C55E; }
.browser-url { flex: 1; background: #fff; border-radius: 4px; padding: 4px 12px; font-size: 12px; color: #666; }
.browser-content { background: #fff; width: 100%; aspect-ratio: 16/10; overflow: hidden; }
```

---

## Step 4: 3D Perspective Transforms

### Isometric View

```css
.isometric-container { perspective: 1200px; display: flex; justify-content: center; align-items: center; padding: 80px; }
.isometric-device { transform: rotateX(12deg) rotateY(-8deg) rotateZ(2deg); transform-style: preserve-3d; transition: transform 0.4s ease; }
.isometric-device:hover { transform: rotateX(5deg) rotateY(-3deg) rotateZ(0deg); }
```

### Floating Perspective

```css
.float-device {
  transform: rotateY(-15deg) rotateX(5deg) translateZ(20px);
  transform-style: preserve-3d; animation: gentleFloat 6s ease-in-out infinite;
}
@keyframes gentleFloat {
  0%, 100% { transform: rotateY(-15deg) rotateX(5deg) translateZ(20px) translateY(0); }
  50% { transform: rotateY(-15deg) rotateX(5deg) translateZ(20px) translateY(-12px); }
}
```

### Stacked Multi-Device

```css
.device-stack { position: relative; perspective: 1200px; width: 800px; height: 600px; }
.device-stack .phone  { position: absolute; right: 10%; bottom: 5%; z-index: 3; transform: rotateY(-5deg) translateZ(40px); }
.device-stack .laptop { position: absolute; left: 5%; top: 10%; z-index: 1; transform: rotateY(5deg); }
.device-stack .tablet { position: absolute; right: 25%; top: 5%; z-index: 2; transform: rotateY(-3deg) translateZ(20px) scale(0.8); }
```

### Fan Layout

```css
.fan-layout { display: flex; align-items: flex-end; justify-content: center; perspective: 1500px; }
.fan-layout .screen:nth-child(1) { transform: rotateY(25deg) translateX(-30px); }
.fan-layout .screen:nth-child(2) { transform: rotateY(0deg) translateZ(30px); z-index: 2; }
.fan-layout .screen:nth-child(3) { transform: rotateY(-25deg) translateX(30px); }
```

---

## Step 5: Lifestyle Background Presentation

### Gradient Stage

```css
.product-stage {
  display: flex; align-items: center; justify-content: center; min-height: 600px; padding: 80px;
  background: radial-gradient(ellipse at 50% 120%, rgba(var(--primary-rgb), 0.15) 0%, transparent 60%),
              linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
}
```

### Desk/Surface Scene

```css
.desk-scene {
  position: relative; background: linear-gradient(180deg, #F8FAFC 0%, #E2E8F0 100%);
  min-height: 600px; display: flex; align-items: flex-end; justify-content: center; padding-bottom: 40px;
}
.desk-scene::before {
  content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 40%;
  background: linear-gradient(180deg, #E2E8F0, #CBD5E1);
}
.desk-scene .device { position: relative; z-index: 2; filter: drop-shadow(0 20px 40px rgba(0,0,0,0.15)); }
```

---

## Step 6: Before/After Comparisons

### Slider-Style

```css
.comparison { position: relative; width: 800px; aspect-ratio: 16/9; overflow: hidden; border-radius: 12px; box-shadow: 0 20px 60px rgba(0,0,0,0.2); }
.comparison .before, .comparison .after { position: absolute; inset: 0; }
.comparison .before { z-index: 1; filter: grayscale(50%) brightness(0.9); }
.comparison .after  { z-index: 2; clip-path: inset(0 50% 0 0); }
.comparison .divider { position: absolute; left: 50%; top: 0; bottom: 0; width: 3px; background: #fff; z-index: 3; }
```

### Side-by-Side

```css
.side-by-side { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: start; }
.side-by-side .label { font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px; }
```

---

## Step 7: Feature Highlight Callouts

### Line-Connected Callouts

```css
.feature-showcase { position: relative; display: flex; align-items: center; justify-content: center; padding: 80px; }
.callout { position: absolute; display: flex; align-items: center; gap: 8px; }
.callout .dot { width: 12px; height: 12px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 0 4px rgba(var(--accent-rgb), 0.2); flex-shrink: 0; }
.callout .line { width: 60px; height: 1px; background: rgba(255,255,255,0.3); flex-shrink: 0; }
.callout .text { font-size: 13px; font-weight: 500; background: rgba(0,0,0,0.4); backdrop-filter: blur(8px); padding: 6px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.1); white-space: nowrap; }
```

### Numbered Feature List

```css
.feature-list { display: flex; flex-direction: column; gap: 20px; }
.feature-item { display: flex; align-items: flex-start; gap: 16px; }
.feature-number { width: 32px; height: 32px; border-radius: 50%; background: var(--primary); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 700; flex-shrink: 0; }
```

---

## Step 8: Packaging Visualization (3D Box)

```css
.product-box { width: 200px; height: 280px; position: relative; transform-style: preserve-3d; transform: rotateX(-12deg) rotateY(-25deg); /* negative X tilt shows the top face */ }
.box-front { position: absolute; width: 200px; height: 280px; background: var(--primary); transform: translateZ(30px); display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 24px; border-radius: 4px; }
/* Box is 200w x 280h x 60d, centered on z=0: front at +30, side at x=200, top at y=0 */
.box-side { position: absolute; left: 0; top: 0; width: 60px; height: 280px; background: color-mix(in srgb, var(--primary) 80%, black); transform: rotateY(90deg) translateZ(170px); /* 170 = width - depth/2 */ }
.box-top { position: absolute; left: 0; top: 0; width: 200px; height: 60px; background: color-mix(in srgb, var(--primary) 90%, white); transform: rotateX(90deg) translateZ(30px); /* 30 = depth/2 */ }
/* Wrap .product-box in a parent with `perspective: 1000px` */
```

---

## Step 9: Screenshot Presentation

### Clean Window Frame

```css
.screenshot-frame { border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05), 0 20px 60px rgba(0,0,0,0.15); background: #fff; }
.screenshot-frame .chrome { height: 36px; background: linear-gradient(180deg, #F9FAFB, #F3F4F6); display: flex; align-items: center; padding: 0 12px; gap: 6px; border-bottom: 1px solid #E5E7EB; }
.screenshot-frame .chrome .dot { width: 10px; height: 10px; border-radius: 50%; background: #D1D5DB; }
.screenshot-frame img { width: 100%; display: block; }
```

### Rotated Screenshot Collage

```css
.screenshot-collage { display: flex; padding: 40px; justify-content: center; }
.screenshot-collage .shot:nth-child(1) { transform: rotate(-5deg); z-index: 1; }
.screenshot-collage .shot:nth-child(2) { transform: rotate(0deg) translateY(-10px); z-index: 2; }
.screenshot-collage .shot:nth-child(3) { transform: rotate(5deg); z-index: 1; }
.screenshot-collage .shot { border-radius: 8px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.2); border: 4px solid #fff; }
```

---

## Quality Checklist

- Device frames look realistic (proper proportions, shadows, details)
- Shadows are natural (soft, directional, not uniform)
- 3D transforms have appropriate perspective depth
- Screenshot content is visible and not distorted
- Brand colors from design-context used for stage/background
- Multiple devices are properly scaled relative to each other
- The overall composition draws attention to the product
- Gemini output was Read and compared against the source product photo (label, logo, shape unchanged)
- Screenshots in device frames are the real, unaltered UI and are not stretched (match the screen's aspect ratio)
- Code output rendered to PNG (`node <graphic-design>/scripts/render.mjs mockup.html --size WxH --out mockup.png`) and the PNG Read before delivery
- Code is self-contained HTML/CSS
