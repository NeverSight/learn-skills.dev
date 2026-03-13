---
name: svg-logo-maker
description: Design and generate production-quality SVG logos in modern minimalist style. Use this skill PROACTIVELY whenever the user asks to create a logo, design a brand mark, generate an SVG icon, make a logomark, create a wordmark, build a brand identity symbol, or needs any kind of vector logo. Also triggers for requests like "make me a logo", "design an icon for my app", "create a brand symbol", "I need a logo for...", "generate SVG logo", or any task involving logo/icon/brand mark creation — even if they don't specifically mention "SVG" or "minimalist".
---

# SVG Logo Maker

Generate world-class minimalist SVG logos using **svg.js** for programmatic construction, **browser-based visual verification**, and automated SVG export.

**Why svg.js?** Writing raw SVG path data is extremely error-prone for AI. svg.js provides high-level shape methods (`rect()`, `circle()`, `polygon()`, `group()`, `gradient()`, `mask()`, `transform()`) that map naturally to function calls — which AI excels at. The browser renders the result, enabling visual iteration.

## Five Principles of Effective Logo Design

These principles guide every decision throughout the workflow. Evaluate all designs against them.

| Principle | What it means | Test |
|---|---|---|
| **Simplicity** | Express the message through clean, essential elements. Every line must earn its place. | Can you describe the logo in one sentence? |
| **Timelessness** | Root the design in enduring brand values, not trends. | Would this look dated in 10 years? |
| **Uniqueness** | Stand apart with original choices. Avoid clichéd symbols (lightbulbs for ideas, globes for "global"). | Could a competitor use the same concept? |
| **Relevance** | Match the audience, industry, and brand personality. A children's app needs different energy than a law firm. | Does it feel right for the target audience? |
| **Readability** | Text must be crisp at any size. Shapes must be recognizable at 32×32px. | Mentally shrink it to a favicon — does it survive? |

## Reference Library

This skill bundles `assets/` containing logos from leading global brands in **two formats**:

| Format | Files | Purpose |
|---|---|---|
| **PNG** (`*.png`) | Visual reference images | **Read these first** — AI can visually parse PNG images to understand shape, proportion, color, negative space, and overall design quality. Use PNG files as the primary design inspiration source. |
| **SVG** (`*.svg`) | Source vector code | Read these to study real-world SVG structure, path construction, optimization techniques, and how professional logos are built in code. |

**Brands included**: Apple, OpenAI, Anthropic, Claude, Claude Code, Cursor, Google, Figma, Meta, Midjourney, Grok, DeepSeek, Doubao, Moonshot, Ollama, Cloudflare, Microsoft, AWS, IBM, Gemini, Antigravity.

The reference logos are located at: `{SKILL_DIR}/assets/`

### How to Use the Reference Library

1. **Visual study (PNG)**: Before designing, read 3–5 PNG files relevant to the target industry/style using the Read tool. The AI can see the rendered logo, analyze its visual structure, and internalize design patterns that are impossible to learn from SVG code alone.
2. **Technical study (SVG)**: After visual study, read the corresponding SVG files to understand how the visual result was achieved in code — path construction, use of groups, transforms, gradients, and masks.
3. **Cross-reference**: Always study both formats for the same logo. The PNG shows *what* to achieve; the SVG shows *how* to build it.

---

## Workflow

### Phase 1 — Brand Identity & Requirement Gathering

A logo translates an entire brand identity into a single mark. **Invest heavily in this phase** — a logo built on shallow understanding will look generic.

#### 1a. Brand Identity Deep-Dive

Extract or infer the following from the user's request. For minimal input, infer reasonable defaults and state assumptions explicitly.

| Dimension | What to capture | Why it matters |
|---|---|---|
| **Brand name** | Exact text (for wordmark/lettermark/monogram) | Determines letterform needs |
| **Target audience** | Demographics, shared interests, sophistication level | Shapes visual tone (playful vs. authoritative) |
| **Core mission** | One sentence describing the brand's purpose | Anchors the visual metaphor |
| **Brand adjectives** | 3–5 words describing the brand's personality (e.g. "bold, trustworthy, innovative") | Drives form language and color |
| **Core values** | 2–3 keywords the brand represents (e.g. "trust", "speed", "innovation") | Informs symbolism and shape choices |
| **Industry / domain** | Tech, finance, health, food, education, creative, etc. | Provides stylistic starting points |

#### 1b. Logo Requirements

| Dimension | What to capture |
|---|---|
| **Logo type** | Logomark, Letterform, Monogram, Wordmark, Abstract, Combination, or Emblem (see Logo Type Guide below) |
| **Color preference** | Specific hex values, or mood-based ("warm", "corporate blue", "monochrome") |
| **Style cues** | Geometric / organic / angular / rounded / abstract / figurative |
| **Usage context** | App icon, website header, favicon, print, all-purpose |
| **Negative space** | Any clever use of negative space requested |

#### Logo Type Guide

Choose the type that best serves the brand's needs:

| Type | Description | Best for | Examples |
|---|---|---|---|
| **Wordmark** | Full company name, typography-driven | Short, unique names | Coca-Cola, Google, FedEx |
| **Letterform** | Single letter | Well-known companies wanting a strong, compact identity | Facebook (F), Pinterest (P) |
| **Monogram** | Initials of the brand name | Established brands with long names | CNN, H&M, IBM |
| **Abstract** | Abstract shapes and symbols, no text | Brands wanting a modern, universal mark | Pepsi, Audi, Nike swoosh |
| **Logomark** | Figurative symbol representing the brand | Brands with a clear visual metaphor | Apple, Twitter bird |
| **Combination** | Text + symbol together | Brands wanting to leverage both | Airbnb, Dropbox, Doritos |
| **Emblem** | Text/symbol contained within a shape (badge, crest, seal) | Traditional, authoritative brands | Starbucks, BMW, Harley-Davidson |

### Phase 2 — Visual Study of Reference Logos

**MANDATORY before designing.** Read PNG reference logos to build visual intuition.

1. **Select 3–5 reference logos** from `{SKILL_DIR}/assets/` that are most relevant to the target brand's industry, style, or logo type. Use the Read tool to view the PNG files — AI can visually parse these images.
2. **Read the corresponding SVG files** for the selected logos to understand their construction technique.
3. **Document observations** — For each reference logo studied, note:
   - What makes the design effective (shape language, negative space, balance)
   - What construction technique was used (geometric primitives, paths, masks)
   - What can be borrowed or adapted for the current project

This visual study directly informs the design plan. Reference specific logos when justifying design decisions.

### Phase 3 — Design Plan

Before writing any code, produce a structured design plan. Present it to the user for confirmation before proceeding.

#### Design Plan Template

```
## Logo Design Plan: [Brand Name]

### 1. Design Concept
- **Core metaphor**: [What real-world object/shape/idea the logo abstracts]
- **Visual narrative**: [One sentence describing what the viewer should "read" from the logo]
- **Inspiration sources**: [Which reference logos (from Phase 2 visual study) inform this direction and why — cite specific PNG files studied]
- **Uniqueness check**: [How this design avoids clichéd symbols and stands apart from competitors]

### 2. Form Language
- **Geometry**: [Geometric primitives used — circles, rectangles, triangles, curves]
- **Shape semantics**: [Why these shapes were chosen — see Shape Psychology reference]
- **Proportions**: [Grid system, golden ratio, modular scale, or freeform]
- **Negative space**: [How white space participates in the design — any hidden forms or clever reveals]
- **Optical balance**: [Weight distribution and visual center of gravity]
- **Visual hierarchy**: [Which element draws the eye first, second, third]

### 3. Typography (if applicable)
- **Font personality**: [Display / Serif / Sans-serif / Monospace / Slab serif / Script — see Typography Guide]
- **Letterform treatment**: [Custom geometric construction, modified typeface, or hand-drawn feel]
- **Weight and spacing**: [Stroke width rationale, letter-spacing logic]
- **Readability at scale**: [How it reads at favicon size vs. billboard]

### 4. Color Strategy
- **Design approach**: Monochrome first, color second
- **Monochrome version**: [How the logo works in pure black on white]
- **Primary palette**: [Hex values with rationale — see Color Psychology reference]
- **Color scheme type**: [Complementary / Analogous / Triadic / Monochromatic — see Color Theory reference]
- **Color meaning**: [Psychological and cultural associations of chosen colors]
- **Contrast check**: [Sufficient contrast between elements for readability]

### 5. Construction Plan
- **svg.js strategy**: [Which shapes, groups, transforms, masks to use]
- **viewBox**: [Dimensions, typically 0 0 512 512]
- **Scalability target**: [Favicon to billboard]
- **Variants planned**: [Primary logo, compact/icon variant, monochrome variant]
```

### Phase 4 — SVG Construction with svg.js

**Do NOT write raw SVG markup. Use svg.js to construct the logo programmatically.**

#### Critical Rule: Monochrome First

**Always build the logo in monochrome (black on white) first.** This ensures the design works through form alone, without relying on color as a crutch. Only add color after the monochrome version passes visual review.

#### Step 1: Create the HTML Workspace

Write a file named `_logo-workspace.html` in the output directory with this scaffold:

```html
<!DOCTYPE html>
<html>
<head>
  <title>Logo Workspace</title>
  <script src="https://cdn.jsdelivr.net/npm/@svgdotjs/svg.js@3.0/dist/svg.min.js"></script>
  <style>
    body {
      margin: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 32px;
      padding: 48px 24px;
      min-height: 100vh;
      background: #e8e8e8;
      font-family: system-ui, sans-serif;
    }
    .preview {
      background: white;
      box-shadow: 0 4px 24px rgba(0,0,0,0.12);
    }
    .label {
      font-size: 13px;
      color: #666;
      margin-bottom: 8px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .size-row {
      display: flex;
      gap: 24px;
      align-items: end;
    }
    .size-item { text-align: center; }
    textarea#svg-output {
      position: fixed;
      bottom: 0; left: 0;
      width: 1px; height: 1px;
      opacity: 0;
      pointer-events: none;
    }
  </style>
</head>
<body>
  <div>
    <div class="label">Primary — 512×512</div>
    <div id="canvas" class="preview"></div>
  </div>
  <div>
    <div class="label">Scale test</div>
    <div class="size-row">
      <div class="size-item">
        <div class="label">128px</div>
        <div id="preview-128" class="preview"></div>
      </div>
      <div class="size-item">
        <div class="label">64px</div>
        <div id="preview-64" class="preview"></div>
      </div>
      <div class="size-item">
        <div class="label">32px</div>
        <div id="preview-32" class="preview"></div>
      </div>
    </div>
  </div>
  <textarea id="svg-output"></textarea>
  <script>
    var draw = SVG().addTo('#canvas').size(512, 512).viewbox(0, 0, 512, 512);

    // ========== LOGO DRAWING CODE (MONOCHROME FIRST) ==========

    // [AI writes svg.js code here — BLACK ON WHITE ONLY in first pass]

    // ========== END LOGO CODE ==========

    // --- Scale previews ---
    var svgMarkup = draw.node.outerHTML;
    [128, 64, 32].forEach(function(s) {
      var el = document.getElementById('preview-' + s);
      el.innerHTML = svgMarkup;
      var svg = el.querySelector('svg');
      svg.setAttribute('width', s);
      svg.setAttribute('height', s);
    });

    // --- Export ---
    var svgEl = draw.node;
    svgEl.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    var output = svgEl.outerHTML;
    output = output.replace(/\s*svgjs:data="[^"]*"/g, '');
    output = output.replace(/\s*class="[^"]*"/g, '');
    document.getElementById('svg-output').value = output;
  </script>
</body>
</html>
```

**Key improvement over a single canvas**: The workspace now shows **scale previews** at 128px, 64px, and 32px alongside the primary 512px canvas. This directly tests the Readability principle — if the logo is illegible at 32px, simplify before adding color.

**Critical**: The `<textarea id="svg-output">` stores the exported SVG for extraction. Do not remove it.

#### Step 2: Write the Drawing Code (Monochrome)

Place svg.js code between the `LOGO DRAWING CODE` markers. **Use only black (`#000` or `#1a1a1a`) fills in the first pass.** Prefer high-level shape methods over raw path data.

##### svg.js API Reference (Logo-Relevant Subset)

**Shapes:**
```javascript
draw.rect(width, height)              // Rectangle
draw.rect(w, h).radius(r)             // Rounded rectangle
draw.circle(diameter)                  // Circle
draw.ellipse(width, height)           // Ellipse
draw.line(x1, y1, x2, y2)            // Line
draw.polygon('x1,y1 x2,y2 x3,y3')   // Polygon (auto-closed)
draw.polyline('x1,y1 x2,y2 x3,y3')  // Polyline (open)
draw.path('M0 0 L100 50 ...')         // SVG path (complex curves only)
```

**Positioning & Sizing:**
```javascript
.move(x, y)          // Absolute position (top-left corner)
.center(x, y)        // Center element at position
.size(w, h)          // Resize element
.dx(offset)          // Relative horizontal shift
.dy(offset)          // Relative vertical shift
```

**Styling:**
```javascript
.fill(color)                                    // '#f06', 'none', 'currentColor'
.fill({ color: '#f06', opacity: 0.8 })          // With opacity
.stroke({ width: 2, color: '#333' })            // Stroke
.stroke({ width: 2, color: '#333', linecap: 'round', linejoin: 'round' })
.opacity(0.5)                                    // Element-level opacity
```

**Transforms:**
```javascript
.transform({ rotate: 45 })                          // Rotate degrees
.transform({ rotate: 45, origin: [256, 256] })      // Rotate around point
.transform({ scale: 2 })                            // Uniform scale
.transform({ translateX: 10, translateY: 20 })       // Translate
.transform({ rotate: 30 }, true)                     // Additive transform
```

**Groups (essential for complex logos):**
```javascript
var g = draw.group()
g.rect(100, 100).fill('#f06')
g.circle(80).fill('#0f9').center(50, 50)
g.move(100, 100)              // Move entire group
g.transform({ rotate: 45 })   // Transform entire group
```

**Gradients:**
```javascript
var grad = draw.gradient('linear', function(add) {
  add.stop(0, '#f06')
  add.stop(0.5, '#ff0')
  add.stop(1, '#0f9')
})
grad.from(0, 0).to(1, 1)  // Diagonal direction
draw.rect(100, 100).fill(grad)

var radial = draw.gradient('radial', function(add) {
  add.stop(0, '#fff')
  add.stop(1, '#000')
})
draw.circle(100).fill(radial)
```

**Text (wordmarks/lettermarks):**
```javascript
draw.text('BRAND').font({
  family: 'Helvetica, Arial, sans-serif',
  size: 72,
  anchor: 'middle',
  weight: 'bold'
}).center(256, 256).fill('#333')
```

**Masks (negative space effects):**
```javascript
var mask = draw.mask()
mask.rect(512, 512).fill('#fff')                    // White = fully visible
mask.circle(100).center(256, 256).fill('#000')      // Black = hidden

draw.rect(512, 512).fill('#f06').maskWith(mask)     // Circle punched out
```

**Clipping:**
```javascript
var clip = draw.clip()
clip.circle(200).center(256, 256)

draw.rect(512, 512).fill('#f06').clipWith(clip)     // Only circle area visible
```

#### Construction Strategies

**Geometric logos**: Build from `rect()`, `circle()`, `polygon()`. Use groups with transforms for symmetry — draw one segment, clone and rotate:
```javascript
for (var i = 0; i < 6; i++) {
  draw.rect(20, 80).center(256, 200).fill('#333')
    .transform({ rotate: i * 60, origin: [256, 256] })
}
```

**Lettermark / Monogram logos**: Construct from `rect()` for straight strokes, `path()` for curves. Alternatively, use `text()` with web-safe geometric fonts for prototyping, then verify in browser.

**Abstract marks**: Layer shapes with different fills. Use `mask()` for boolean-like operations (subtract, intersect). Group related shapes for unified transforms.

**Negative space logos**: Use `mask()` — white areas reveal, black areas hide. Draw the positive shape first, then cut out the negative form.

**Emblem logos**: Create an outer boundary shape (circle, shield, badge), then place text/symbol inside. Use `clip()` to contain elements within the boundary.

**Symmetry patterns**: Draw one unit in a group, then loop with rotational transforms:
```javascript
var unit = draw.group()
unit.ellipse(40, 120).center(256, 190).fill('#f06')

for (var i = 1; i < 8; i++) {
  unit.clone().transform({ rotate: i * 45, origin: [256, 256] }).addTo(draw)
}
```

### Phase 5 — Browser Preview & Iteration

This is the critical advantage: **visual feedback loop with structured critique**.

#### Step 1: Preview

1. **Open the workspace** in the browser:
   ```
   browser_navigate → file:///absolute/path/to/_logo-workspace.html
   ```
2. **Lock the browser** for interaction:
   ```
   browser_lock
   ```
3. **Take a screenshot** to capture the rendered logo:
   ```
   browser_take_screenshot
   ```

#### Step 2: Structured Critique (Monochrome Pass)

Evaluate the monochrome version against this rubric:

| Criterion | Question | Action if fails |
|---|---|---|
| **Simplicity** | Can I describe this in one sentence? Are there elements I can remove without losing meaning? | Strip unnecessary shapes. |
| **Readability** | Does the 32px preview still read clearly? | Simplify or thicken elements. |
| **Uniqueness** | Could a competitor use the same basic concept? Is it a cliché symbol? | Rethink the metaphor. |
| **Relevance** | Does the form language match the brand personality and audience? | Revisit brand adjectives. |
| **Optical balance** | Does it feel centered? Is visual weight evenly distributed? | Adjust positioning; don't trust coordinates alone. |
| **Negative space** | Is white space purposeful? Any unintended trapped space? | Clean up gaps between shapes. |
| **Proportions** | Are stroke weights consistent? Do elements relate harmoniously? | Normalize widths and spacing. |

#### Step 3: Iterate (Monochrome)

If the monochrome design doesn't pass critique:
- Unlock the browser: `browser_unlock`
- Edit the JavaScript in `_logo-workspace.html`
- Re-lock and navigate to the same URL to reload
- Take another screenshot
- Repeat until the **monochrome design is solid**

#### Step 4: Add Color

Once the monochrome version is approved:
- Update the drawing code to replace black fills with the planned color palette
- Take a new screenshot
- Verify that color enhances (not replaces) the design's effectiveness
- Check that the color version still passes all critique criteria

#### Step 5: Final Critique (Color Pass)

| Criterion | Question |
|---|---|
| **Color harmony** | Do colors work together? Is the scheme (complementary/analogous/triadic) coherent? |
| **Color meaning** | Do the chosen colors reinforce brand personality and values? |
| **Contrast** | Is there sufficient contrast between adjacent elements? |
| **Monochrome resilience** | If I desaturate, does the logo still work? (It should — you designed it monochrome first.) |
| **Timelessness** | Is the color palette classic or trendy? Avoid neon gradients that will date quickly. |

**Target 2–4 iteration cycles total** (monochrome + color). If more are needed, reconsider the design approach.

### Phase 6 — SVG Export & Variants

Once the logo looks correct in the browser:

1. **Take a snapshot** to find the textarea:
   ```
   browser_snapshot → find ref for textarea#svg-output
   ```

2. **Extract the SVG string**:
   ```
   browser_get_input_value → ref of textarea#svg-output
   ```

3. **Post-process the SVG**:
   - Ensure `xmlns="http://www.w3.org/2000/svg"` is present on root `<svg>`
   - Add `<title>[Brand Name]</title>` as first child if not present
   - Remove any remaining svg.js artifacts (`svgjs:data`, generated `id` attributes, `class` attributes)
   - Ensure `viewBox="0 0 512 512"` and `width="512" height="512"` are set
   - For monochrome logos, consider replacing color fills with `currentColor`

4. **Unlock the browser**:
   ```
   browser_unlock
   ```

5. **Save logo variants**:
   - **Primary**: `{brand-name}-logo.svg` — Full color version
   - **Monochrome**: `{brand-name}-logo-mono.svg` — Black-only version (replace all fills with `#000` or `currentColor`)
   - **Compact/icon** (if applicable): `{brand-name}-icon.svg` — Symbol only, no text, optimized for small sizes

6. **Delete the workspace** — Remove `_logo-workspace.html` using the Delete tool.

7. **Confirm** — "Logos saved to `{path}`. Open them in a browser or SVG editor to preview."

---

## Design Reference Guides

### Shape Psychology

Shapes carry emotional weight. Choose shapes that reinforce brand personality.

| Shape | Emotional associations | Best for |
|---|---|---|
| **Circle** | Unity, community, completeness, harmony, protection | Social platforms, global brands, inclusive brands |
| **Square / Rectangle** | Stability, reliability, order, professionalism, security | Finance, enterprise, construction, logistics |
| **Triangle** | Direction, energy, power, innovation, aspiration | Tech, fitness, leadership brands |
| **Organic / Curves** | Movement, fluidity, friendliness, natural growth | Health, wellness, food, creative agencies |
| **Angular / Sharp** | Precision, cutting-edge, boldness, disruption | Tech startups, gaming, engineering |
| **Hexagon** | Balance, efficiency, interconnection (beehive metaphor) | Tech, science, networks |

### Color Theory

Use established color relationships for harmonious palettes:

| Scheme | How it works | Effect |
|---|---|---|
| **Monochromatic** | Shades/tints of one hue | Clean, sophisticated, unified |
| **Complementary** | Opposite hues on the color wheel | High contrast, energetic |
| **Analogous** | Adjacent hues on the color wheel | Harmonious, natural, calming |
| **Triadic** | Three evenly-spaced hues | Vibrant, balanced, dynamic |
| **Split-complementary** | One hue + two neighbors of its complement | Contrast with less tension |

### Color Psychology

| Color | Associations | Industries that use it |
|---|---|---|
| **Blue** | Trust, reliability, calm, professionalism | Finance, tech, healthcare, corporate |
| **Red** | Energy, urgency, passion, excitement | Food, entertainment, retail, sports |
| **Green** | Growth, health, nature, freshness, wealth | Wellness, sustainability, finance |
| **Yellow / Gold** | Optimism, warmth, clarity, prestige | Food, luxury, children's brands |
| **Orange** | Creativity, enthusiasm, friendliness | E-commerce, entertainment, youth brands |
| **Purple** | Luxury, creativity, wisdom, spirituality | Beauty, premium brands, education |
| **Black** | Sophistication, power, elegance, authority | Luxury, fashion, tech |
| **White** | Purity, simplicity, minimalism, space | Tech, healthcare, modern brands |
| **Brown** | Reliability, earthiness, warmth, security | Logistics (UPS), organic, outdoor brands |
| **Teal / Cyan** | Innovation, clarity, balance | AI/tech, wellness, modern enterprise |

### Typography Guide (for Wordmarks, Lettermarks, Monograms)

| Font Type | Personality | Use when |
|---|---|---|
| **Display** | Decorative, unique, attention-grabbing | The brand is bold and distinctive |
| **Serif** | Timeless, professional, authoritative | Traditional, luxury, editorial brands |
| **Sans-serif** | Modern, minimal, readable | Tech, startups, clean brand identities |
| **Monospace** | Technical, retro, developer-oriented | Dev tools, tech brands, gaming |
| **Slab serif** | Powerful, authoritative, impactful | Brands wanting to command attention |
| **Script** | Elegant, creative, personal | Beauty, wedding, artisan brands |

When constructing letterforms programmatically with svg.js, prefer geometric construction (building letters from `rect()`, `circle()`, `path()`) over `text()` for the final logo — this avoids font-dependency issues in the exported SVG.

---

## Design Principles — Learn from the Best

Study the reference logos in `assets/` before generating. **Read the PNG files to visually see each logo; read the SVG files to understand construction.** Key patterns:

**Apple** — Single iconic silhouette. One path, one shape, universally recognized. The bite creates asymmetry and memorability.

**OpenAI** — Mathematical precision through geometric symmetry. Hexagonal knot with interlocking paths.

**Anthropic** — Lettermark reduced to pure geometry. Bold, structural, unmistakable at any size.

**Cursor** — 3D prism rendered flat. Light/shadow division creates depth illusion from a single shape.

**Figma** — Modular building blocks. Rounded rectangles in a grid, each a different color. Simple parts, complex whole.

**Google** — Letter "G" from four simple arcs. Color segmentation creates recognition from pure geometry.

**FedEx** — Hidden arrow in negative space between "E" and "x" — a discovery moment that reinforces the brand promise.

**Nike** — Abstract swoosh suggests motion and energy. No text needed. Ultimate simplicity.

**Starbucks** — Emblem containing a detailed illustration within a circular boundary. Shows that emblems can carry complexity inside a clean frame.

## Quality Checklist

Before finalizing, verify against all five principles:

**Simplicity:**
- [ ] Can describe the logo in one sentence
- [ ] No unnecessary elements — every shape carries meaning
- [ ] 5 or fewer shape groups in the final design
- [ ] File size under 5KB (ideally under 2KB)

**Timelessness:**
- [ ] Avoids trendy gradients, textures, or effects
- [ ] Would look appropriate 10 years from now
- [ ] Design rooted in brand values, not aesthetics of the moment

**Uniqueness:**
- [ ] No clichéd symbols (lightbulb, globe, generic swoosh)
- [ ] Distinct from competitors in the same industry
- [ ] Contains a memorable detail or hidden meaning

**Relevance:**
- [ ] Form language matches brand personality (adjectives from Phase 1)
- [ ] Color choices align with industry and audience expectations
- [ ] Appropriate tone (playful vs. professional vs. luxurious)

**Readability:**
- [ ] Browser screenshot shows a clean, professional logo
- [ ] 32px preview is still legible and recognizable
- [ ] Text elements (if any) are crisp at all sizes
- [ ] Sufficient contrast between elements
- [ ] Optically centered with 8–12% padding within viewBox

**Technical quality:**
- [ ] Monochrome version works independently
- [ ] No overlapping shapes creating unintended artifacts
- [ ] Final `.svg` file is clean — no svg.js artifacts, no unnecessary IDs/classes
- [ ] Valid SVG parseable by any browser
- [ ] Logo variants delivered (primary, monochrome, compact/icon if applicable)

## Common Pitfalls

- **Skipping the brand identity deep-dive**: A logo built on "make something cool" will be generic. Invest in Phase 1.
- **Jumping to color**: Design monochrome first. Color should enhance, never rescue, a weak form.
- **Over-complexity**: 5+ shape groups in a minimalist logo = too complex. Simplify.
- **Tiny vanishing details**: If invisible at 32×32, remove it. The scale test in the workspace catches this.
- **Generic shapes**: Every shape must carry brand-specific meaning. Avoid "abstract blob" designs.
- **Clichéd symbols**: Lightbulbs for ideas, globes for global, gears for engineering — find a fresher metaphor.
- **Poor optical centering**: Use screenshots to visually verify — don't trust coordinates alone.
- **Inconsistent stroke weights**: Maintain visual weight consistency across elements.
- **Raw path data**: Only use `draw.path()` for curves impossible to build from primitives. Prefer `rect()`, `circle()`, `polygon()`, `group()` + transforms.
- **Skipping iteration**: ALWAYS preview in browser. Never ship a logo without visual verification.
- **Single variant delivery**: Always deliver at minimum a color and monochrome version.

## Style Direction by Industry

| Industry | Typical Form Language | Color Direction | Shape Tendency |
|---|---|---|---|
| Tech / AI | Geometric, angular, interconnected nodes | Blues, gradients, monochrome | Hexagons, triangles, sharp angles |
| Finance | Stable, symmetrical, strong horizontals | Navy, gold, dark green | Squares, rectangles, shields |
| Health | Organic curves, rounded, flowing | Greens, teals, warm whites | Circles, curves, organic forms |
| Food & Beverage | Warm, hand-crafted feel, circular | Earthy tones, reds, oranges | Circles, organic shapes |
| Education | Open, ascending, book/light metaphors | Blues, greens, warm yellows | Upward triangles, open books |
| Creative / Design | Asymmetric, bold, unconventional | Vibrant, multi-color, black | Mixed, rule-breaking |
| E-commerce | Dynamic, forward-moving, arrow motifs | Oranges, blues, clean whites | Arrows, dynamic angles |
| Gaming | Sharp, angular, energetic | Neons, dark backgrounds, high contrast | Sharp angles, bold geometry |
| Luxury | Refined, minimal, high contrast | Black, gold, deep jewel tones | Thin lines, serif letterforms |
| Children / Education | Rounded, playful, friendly | Bright primaries, pastels | Circles, soft rounded shapes |

These are starting points, not rules. Break conventions when the brand demands it.
