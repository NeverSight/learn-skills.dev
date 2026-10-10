---
name: p5-brush
description: "Generate generative art sketches using p5.js + p5.brush. Describe what you want to draw and get a standalone HTML file with natural, hand-drawn-style artwork."
argument-hint: "a stormy ocean in watercolor with heavy bleed"
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# p5.brush — AI Generative Art Skill

You generate standalone HTML files that produce generative art using **p5.js 2.x** and **p5.brush v2**.

**Library by [@acamposuribe](https://github.com/acamposuribe/p5.brush)**. Design custom brushes visually with the [Brush Maker](https://acamposuribe.github.io/p5.brush/tools/brush-maker.html).

## Workflow

1. User describes what they want (e.g. "a field of wildflowers in charcoal", "abstract watercolor circles")
2. You write a complete HTML file with an embedded p5.js sketch using the p5.brush API
3. Save to a sensible location (e.g. `./output/<descriptive-name>.html` in the current project, or wherever the user specifies)
4. Open in browser: `open <path>`

## Output Template

Every generated file follows this structure:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>p5.brush — [title]</title>
  <script src="https://cdn.jsdelivr.net/npm/p5@2/lib/p5.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/p5.brush@2.0.0-beta"></script>
  <style>
    html, body { margin: 0; padding: 0; overflow: hidden; background: #1a1a1a; display: flex; justify-content: center; align-items: center; height: 100vh; }
    canvas { display: block; }
  </style>
</head>
<body>
<script>
function setup() {
  createCanvas(800, 800, WEBGL);
  brush.load();
  // Shift WEBGL origin to top-left:
  translate(-width / 2, -height / 2);

  // Set background
  background(245, 240, 235); // warm paper

  // Set a random seed for reproducibility
  randomSeed(42);

  // --- Your generative art code here ---
}
</script>
</body>
</html>
```

## CRITICAL RULES

1. **Always use `WEBGL` mode**: `createCanvas(w, h, WEBGL)` — p5.brush v2 requires it
2. **Always call `brush.load()`** in setup, after `createCanvas(w,h,WEBGL)`. Use `brush.load(buffer)` to target a `p5.Graphics` or `p5.Framebuffer`, and `brush.load()` to switch back
3. **Shift origin**: `translate(-width/2, -height/2)` right after background to work in top-left coordinates
4. **Angles follow `angleMode()`** — radians by default (matching p5). `brush.addField()` angles default to degrees unless you pass `{ angleMode: "radians" }`
5. **`brush.arc()` is stroke-only** — it does NOT fill. `brush.circle()` and `brush.rect()` support stroke + fill + hatch
6. **Use `randomSeed()`** for reproducible outputs — p5.brush syncs automatically (both `randomSeed()` and `noiseSeed()`)
7. **Static sketches only need `setup()`** — no `draw()` loop needed. Use `draw()` only for animations with `brush.refreshField(frameCount/10)`
8. **All drawing in one frame** — put everything in `setup()` for static art
9. **Text labels: use HTML overlay, NOT p5 `text()`** — WEBGL mode requires TTF/OTF fonts loaded via `loadFont()` which is fragile with CDN fonts. For labeled artwork, use absolutely positioned HTML `<div>` elements over the canvas instead
10. **Image brushes require `await`** — `brush.add()` returns a Promise for `type: "image"`. You must `await` it and declare `async function setup()`
11. **Fill budget** — watercolor fills are expensive. Keep filled shape count reasonable (under ~50 for complex fills with high bleed) or the sketch will lag

## API REFERENCE

### Setup & Config

```js
brush.load()              // Initialize. Call in setup() after createCanvas(w,h,WEBGL)
brush.load(buffer)        // Target a p5.Graphics or p5.Framebuffer
brush.load()              // Switch back to main canvas
brush.scaleBrushes(scale) // Scale all default brush params (weight, scatter, spacing)
brush.instance(p)         // For p5 instance mode — call before setup/draw
```

### Vector Fields

Fields guide brush strokes along organic paths. Activate before drawing.

```js
brush.field("waves")       // Activate: "hand", "curved", "zigzag", "waves", "seabed", "spiral", "columns"
brush.noField()            // Deactivate
brush.wiggle(5)            // Shorthand: activate "hand" field with intensity (1-10)
brush.refreshField(t)      // Update field for animation (use frameCount/10 in draw())
brush.listFields()         // Returns array of available field names
```

Custom field:
```js
brush.addField("myField", function(t, field) {
  for (let col = 0; col < field.length; col++)
    for (let row = 0; row < field[0].length; row++)
      field[col][row] = 45 + noise(col * 0.1, row * 0.1) * 180;
  return field;
}, { angleMode: "degrees" }); // default is degrees
brush.field("myField");
```

### Brush Management

```js
brush.box()               // Returns array of all brush names
brush.pick("2B")           // Select brush without changing color/weight
```

**Built-in brushes:**

| Name | Type | Character |
|------|------|-----------|
| `2B` | pencil | Soft, dark, textured |
| `HB` | pencil | Medium, balanced |
| `2H` | pencil | Hard, light, precise |
| `cpencil` | pencil | Colored pencil, softer opacity |
| `pen` | pen | Ink pen, clean lines |
| `rotring` | pen | Technical pen, very precise |
| `charcoal` | pencil | Heavy texture, wide scatter |
| `spray` | spray | Scattered dots |
| `marker` | marker | Flat, solid strokes |
| `marker2` | marker | Marker variant |
| `hatch_brush` | hatch | Clean lines for hatching |

**Custom brush types:**

```js
// Standard custom brush
brush.add("myBrush", {
  type: "default",     // "default", "spray", "marker", "custom", "image"
  weight: 0.5,         // thickness (canvas units)
  scatter: 0.8,        // sideways wobble (canvas units)
  sharpness: 0.5,      // 0-1, edge softness (default type only)
  grain: 10,           // texture density (default type only)
  opacity: 150,        // 0-255
  spacing: 0.1,        // gap between stamps (1 = no overlap)
  pressure: [1, 0.5],  // [start,end] or [start,mid,end] or (t)=>value
  rotate: "natural",   // "none", "natural", "random"
});

// Custom tip brush — draw your own tip shape
brush.add("diamond", {
  type: "custom",
  weight: 5,
  opacity: 23,
  spacing: 0.6,
  pressure: [0.5, 1.5, 0.5],
  tip: (_m) => { _m.rotate(45); _m.rect(-1.5, -1.5, 3, 3); },
  rotate: "natural",
});

// Image brush — MUST use await + async setup()
await brush.add("watercolor", {
  type: "image",
  weight: 10,
  scatter: 2,
  opacity: 30,
  spacing: 1.5,
  pressure: [1, 0.5],
  image: { src: "./brush_tips/brush.jpg" },
  rotate: "random",
});
```

### Stroke

```js
brush.set("2B", "#333", 1)     // Set brush, color, weight — activates stroke
brush.stroke("#ff0000")         // Set color, activate stroke
brush.strokeWeight(2)           // Weight multiplier
brush.noStroke()                // Disable stroke
```

### Fill (Watercolor)

```js
brush.fill("#4a90d9", 150)           // Color + opacity (0-255), activate fill
brush.fill(244, 15, 24, 75)          // RGB + opacity
brush.fillBleed(0.5, "out")          // Edge bleed: strength 0-1, direction "out"/"in"
brush.fillTexture(0.5, 0.3)          // Texture: strength 0-1, border intensity 0-1
brush.noFill()                       // Disable fill
```

### Hatch

```js
brush.hatch(8, 45, { rand: 0.2, continuous: false, gradient: false })
// dist: line spacing, angle: follows angleMode(), options: { rand, continuous, gradient }
brush.hatchStyle("rotring", "#555", 0.5)  // Brush for hatch lines
brush.noHatch()
brush.hatchArray(polygons)                // Hatch across multiple Polygon objects at once
```

### Drawing Primitives

**Lines & curves** (stroke only):
```js
brush.line(x1, y1, x2, y2)
brush.flowLine(x, y, length, direction)    // Follows active vector field
brush.spline([[x1,y1], [x2,y2,pressure], ...], curvature)  // 0-1 curvature
brush.arc(x, y, radius, startAngle, endAngle)  // STROKE ONLY, follows angleMode()
```

**Shapes** (support stroke + fill + hatch):
```js
brush.rect(x, y, w, h)                     // Default: top-left corner mode
brush.rect(x, y, w, h, "center")           // Center mode
brush.circle(x, y, radius)                 // Supports stroke + fill + hatch
brush.circle(x, y, radius, true)           // With hand-drawn irregularity
brush.polygon([[x1,y1], [x2,y2], ...])     // Not affected by vector fields
```

**Custom shapes** (support stroke + fill + hatch, affected by fields):
```js
brush.beginShape(0.5)        // curvature 0-1
brush.vertex(x, y)           // or brush.vertex(x, y, pressure)
brush.vertex(x2, y2)
brush.endShape(true)          // true = close shape
```

**Manual stroke paths:**
```js
brush.beginStroke("curve", x, y)   // or "segments"
brush.move(angle, length, pressure)
brush.endStroke(angle, pressure)
```

### Clipping

```js
brush.clip([x1, y1, x2, y2])   // Clip strokes/hatches to rectangle (not fills)
brush.noClip()
```

### Classes

**Polygon:**
```js
let poly = new brush.Polygon([[x1,y1], [x2,y2], ...]);
poly.draw()                    // Draw outline with current stroke
poly.fill()                    // Fill with current fill settings
poly.hatch()                   // Hatch with current hatch settings
```

**Plot (reusable stroke paths):**
```js
let plot = new brush.Plot("curve");
plot.addSegment(angle, length, pressure);
plot.endPlot(finalAngle, finalPressure);
plot.draw(x, y);               // Draw at position
plot.fill(x, y);               // Fill at position
plot.hatch(x, y);              // Hatch at position
```

**Position (flow field walker):**
```js
let pos = new brush.Position(x, y);
pos.moveTo(direction, length, stepLength);  // Move along flow field
pos.angle();                   // Get field angle at current position
pos.reset();                   // Reset plotted distance
```

## RECIPES

### Hand-drawn look
```js
brush.wiggle(3);
brush.set("2B", "#333", 1);
brush.line(100, 100, 400, 300);
```

### Watercolor blobs
```js
brush.noStroke();
brush.fill("#4a90d9", 100);
brush.fillBleed(0.6, "out");
brush.fillTexture(0.5, 0.3);
brush.rect(200, 200, 300, 300);
```

### Cross-hatched shapes
```js
brush.noFill();
brush.hatch(5, 45, { rand: 0.1 });
brush.hatchStyle("rotring", "#444", 0.5);
brush.set("pen", "#222", 0.8);
brush.rect(100, 100, 300, 300);
// Layer second direction:
brush.hatch(5, -45, { rand: 0.1 });
brush.rect(100, 100, 300, 300);
```

### Flow field lines
```js
brush.field("curved");
brush.set("cpencil", "#8B4513", 0.8);
for (let i = 0; i < 200; i++) {
  brush.flowLine(random(width), random(height), random(100, 400), random(TWO_PI));
}
```

### Filled circle with watercolor
```js
brush.noStroke();
brush.fill("#e85d75", 120);
brush.fillBleed(0.4);
brush.circle(400, 400, 100);
```

### Mixed media grid (from author's examples)
```js
let palette = ["#7b4800", "#002185", "#003c32", "#fcd300", "#ff2702", "#6b9404"];
let cols = 12, rows = 6, border = 300;
let cw = (width - border) / cols, rh = (height - border) / rows;

brush.field("curved");
for (let i = 0; i < rows; i++) {
  for (let j = 0; j < cols; j++) {
    if (random() < 0.1) {
      brush.fill(random(palette), random(80, 140));
      brush.fillBleed(random(0.05, 0.4));
      brush.fillTexture(0.55, 0.5);
    } else {
      brush.set(random(["2H", "HB", "charcoal"]), random(palette));
      brush.hatchStyle(random(["marker", "marker2"]), random(palette));
      brush.hatch(random(10, 60), random(0, 180));
    }
    brush.rect(border/2 + cw * j, border/2 + rh * i, cw, rh);
    brush.noStroke(); brush.noFill(); brush.noHatch();
  }
}
```

## Design Tips

- **Paper colors**: warm `(245, 240, 235)`, cream `(252, 248, 240)`, cool white `(248, 248, 252)`, dark `(30, 30, 35)`
- **Layering**: Draw background elements first (light opacity), then foreground (higher opacity). Multiple passes build depth.
- **Organic variation**: Use `random()` and `noise()` for position, size, color shifts. Avoid exact repetition.
- **Color palettes**: Pick 3-5 colors. Vary saturation/brightness with `random()` for natural feel.
- **Composition**: Use golden ratio, rule of thirds, or radial layouts. Leave breathing room.
- **Texture stacking**: Combine hatching + watercolor fill + pencil outlines for rich mixed-media effects.
- **Scale**: `brush.scaleBrushes(2)` for larger canvases (1200+px) so strokes stay visible.
- **p5 transforms work**: `push()`, `pop()`, `translate()`, `rotate()`, `scale()` — brush state is saved/restored automatically alongside p5's state.
