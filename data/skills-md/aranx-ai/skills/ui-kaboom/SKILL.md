---
name: ui-kaboom
description: "Design beautiful and functional user interfaces for web applications. Use this skill when the user asks to design, build, review, or improve the visual design of web UI — including layout, typography, color, hierarchy, spacing, depth, images, and finishing touches. Applies practical, systematic design principles with Tailwind CSS."
---

# UI Kaboom

Systematic, practical design principles for building beautiful and functional web interfaces. Apply these rules when designing or reviewing any web UI.

---

## Design Workflow

1. **Start with a feature** — Design actual functionality first, not the shell (nav, sidebar, footer). The layout emerges from the features.
2. **Design in low fidelity** — Grayscale first. Use spacing, contrast, and size to create hierarchy before introducing color.
3. **Work in cycles** — Design a simple version, build it, discover edge cases, fix them, repeat. Don't design everything upfront.
4. **Choose a personality** — Decide on tone through font, color, border-radius, and language. Stay consistent.
5. **Systematize choices** — Define spacing, type scale, colors, shadows, and radii upfront. Constrained choices create consistency and speed.

---

## 1. Visual Hierarchy

**The most important design tool.** Every interface has primary, secondary, and tertiary content. Make the hierarchy obvious.

### Don't Rely on Size Alone
Use font weight and color — not just font size — to create hierarchy:
- **Dark color** (slate-900) for primary content
- **Medium grey** (slate-500) for secondary content
- **Light grey** (slate-400) for tertiary content
- **Two font weights**: 400/500 for normal, 600/700 for emphasis
- Never use font weights under 400 for UI work

### Emphasize by De-emphasizing
When something won't stand out, make the *competition* quieter instead of making the target louder.

### Labels Are a Last Resort
- Self-evident formats don't need labels: emails, phone numbers, prices
- Combine label + value: "12 left in stock" instead of "In stock: 12"
- When needed, make labels secondary (smaller, lighter, uppercase tracking-wide)

### Semantic vs Visual Hierarchy
An `<h1>` doesn't have to be huge. Style for visual hierarchy, not HTML semantics.

### Balance Weight and Contrast
- Icons feel heavy — soften them with lighter color (slate-400)
- Thin borders too subtle — make them thicker, not darker (border-2)

### Button Hierarchy
Style by importance, not semantics:
- **Primary**: solid, high contrast (`bg-blue-600 text-white`)
- **Secondary**: outline or muted (`border border-slate-300 text-slate-700`)
- **Tertiary**: link-style (`text-slate-500 underline`)
- Destructive actions aren't always red — reserve bold red for confirmation dialogs

---

## 2. Layout and Spacing

### Start with Too Much White Space
Remove space instead of adding it. What seems like "too much" in isolation is "just right" in context.

### Use a Spacing Scale
Ensure ~25% minimum jump between adjacent values:
```
p-1=4px  p-2=8px  p-3=12px  p-4=16px  p-6=24px
p-8=32px  p-12=48px  p-16=64px  p-24=96px  p-32=128px
```

### Don't Fill the Whole Screen
If content needs 600px, use `max-w-2xl mx-auto`. Extra width makes interfaces harder to interpret.

### Grids Are Overrated
Fixed widths often beat fluid percentages. Sidebars should be fixed (`w-64 shrink-0`), main content flexes.

### Relative Sizing Doesn't Scale
Large elements shrink faster than small ones on mobile. Define sizes independently per breakpoint — don't rely on ratios.

### Avoid Ambiguous Spacing
More space *between* groups, less space *within* groups. Labels should be closer to their inputs than to the next field.

---

## 3. Typography

### Type Scale
```
text-xs=12px   text-sm=14px   text-base=16px   text-lg=18px
text-xl=20px   text-2xl=24px  text-3xl=30px    text-4xl=36px
```
Use px or rem — never em (they compound when nested).

### Font Selection
- 5+ weights = better crafted typeface
- Don't use headline fonts for body text (tight spacing, short x-height)
- Sort by popularity in font directories to find quality options

### Line Length: 45-75 Characters
`max-w-prose` (65ch) is optimal. Different elements can have different widths — narrow text with wide images is fine.

### Line-Height Is Inversely Proportional to Font Size
- Small text (14-16px): `leading-relaxed` (1.625)
- Large headings (36px+): `leading-tight` (1.25)
- Longer lines need more line-height

### Alignment
- `items-baseline` for mixed font sizes — not `items-center`
- Left-align by default; center only headlines and short blocks
- Right-align numbers in tables
- Tighten headlines: `tracking-tight`; loosen all-caps: `tracking-wide`

### Links
Not every link needs color. In nav/list-heavy interfaces, use weight or hover-only styling. Reserve blue/underline for links in prose.

---

## 4. Color

### Use HSL (or oklch)
HSL makes color relationships intuitive — hue (0-360°), saturation (0-100%), lightness (0-100%). Tailwind 4 uses oklch for wider gamut. Don't confuse HSL with HSB (design tools use HSB where 100% brightness ≠ white).

### Build a Complete Palette (You Need More Colors Than You Think)
You can't build anything real with 5 hex codes. You need three categories:
- **Greys**: 8-10 shades (text, backgrounds, panels, borders, form controls)
- **Primary**: 5-10 shades (brand, CTAs, active nav — the color that defines your site's "look")
- **Accents**: 5-10 shades each for semantic and feature colors:
  - **Red** — errors, destructive actions, negative trends
  - **Yellow** — warnings, caution states
  - **Green** — success, positive trends
  - **Teal/Pink/etc.** — highlight new features, categorize items
- **Total**: Up to **10 different colors with 5-10 shades each** for complex UIs

### Define 9 Shades per Color (100-900)
Don't use CSS `lighten()`/`darken()` — you'll get 35 nearly identical shades. Define a fixed set:
1. **Pick base (500)** — should work as a button background
2. **Pick edges** — 900 for darkest text, 100 for tinted backgrounds (test with an alert component)
3. **Fill gaps**: 700 and 300 first (midpoints), then 800, 600, 400, 200

### Perceived Brightness and Hue Rotation
Not all hues are equally bright. At the same HSL lightness, yellow appears much lighter than blue. Perceived brightness has three local maximums (yellow 60°, cyan 180°, magenta 300°) and three minimums (red 0°, green 120°, blue 240°).

**Use this to create richer shade palettes:**
- **To lighten**: rotate hue toward nearest bright hue (60°, 180°, 300°)
- **To darken**: rotate hue toward nearest dark hue (0°, 120°, 240°)
- **Example**: For a yellow palette, rotate toward orange as you darken — shades feel warm and rich instead of dull brown
- **Combine approaches**: adjust both hue and lightness for natural-feeling shade scales
- **Keep rotations under 20-30°** or it looks like a different color entirely

### Saturation Rules
- **Increase saturation as lightness moves away from 50%** — without this, edge shades look washed out
- The same saturation value at 50% lightness looks more colorful than at 90% lightness
- If your base color is already at 100% saturation, use hue rotation instead to adjust brightness

### Saturate Your Greys
Pure grey (0% saturation) feels lifeless. Real-world "greys" are saturated:
- **Cool greys**: Saturate with blue (H~207-210, S~12-21%) → Tailwind's `slate`
- **Neutral greys**: Minimal saturation → Tailwind's `gray`, `zinc`
- **Warm greys**: Saturate with yellow/orange (H~39-41, S~12-21%) → Tailwind's `stone`
- **Increase saturation for edge shades** to maintain consistent color temperature across the scale

### On Colored Backgrounds
Don't use grey text — hand-pick a color with the same hue but adjusted saturation/lightness:
```html
<!-- Bad --> <div class="bg-blue-600 text-gray-400">...</div>
<!-- Good --> <div class="bg-blue-600 text-blue-200">...</div>
```

### Accessibility
- **Normal text** (under ~18px): **4.5:1** contrast minimum (hsl(0,0%,42%) ≈ 5.41:1 AA; hsl(0,0%,33%) ≈ 7.57:1 AAA)
- **Large text** (18px+ or 14px+ bold): **3:1** minimum
- **Flip the contrast** when colored backgrounds are too dark and dominate hierarchy: use dark text on light background (`bg-green-100 text-green-800`) instead of white text on dark background
- **Rotate hue for colored-on-colored**: When picking secondary text color on a dark colored panel, rotate hue toward a brighter color (cyan, magenta, yellow) to gain contrast without approaching pure white
- **Never rely on color alone** — add icons (arrows for trends), labels, or contrast differences for colorblind users
- Use **contrast** (light vs dark shades of one color) instead of multiple distinct colors in graphs/charts

---

## 5. Depth and Shadows

### Light Comes from Above
- Top edges: lighter (catch light)
- Bottom edges: darker (in shadow)
- Below elements: cast shadow

### Shadow Elevation System
```
shadow-sm  — buttons, subtle lift
shadow     — cards, default
shadow-md  — dropdowns, popovers
shadow-lg  — hover cards, sticky headers
shadow-xl  — modals, dialogs
shadow-2xl — full-screen overlays
```

### Two-Part Shadows
Professional shadows combine:
1. **Large, soft** — direct light (big offset, large blur)
2. **Small, tight** — ambient occlusion (small offset, tight blur)

At higher elevations, the ambient shadow fades.

### Interactive Shadows
- Drag: add shadow (`shadow-sm` to `shadow-lg`) to "lift" element
- Press: reduce shadow (`shadow-md` to `shadow-sm`) to "push" element

### Flat Design Depth
- Lighter than background = raised; darker = inset
- Solid shadows (no blur) maintain flat aesthetic

### Overlapping Creates Layers
Offset elements across background transitions. Use `ring-2 ring-white` as invisible borders when images overlap.

---

## 6. Images

### Use Quality Photography
Bad photos ruin good designs. Use professional photos or high-quality stock (Unsplash). Never design with placeholders.

### Text Over Images
Images have competing light/dark areas. Solutions:
- **Overlay**: `bg-black/40` over image
- **Lower contrast**: reduce image dynamics
- **Colorize**: desaturate + multiply blend with brand color
- **Text shadow**: large blur, no offset (glow effect)

### Respect Intended Sizes
- Don't scale 16-24px icons to 64px — wrap in a shape instead
- Don't shrink full screenshots — crop or simplify
- Redraw logos at favicon size instead of scaling down

### User-Uploaded Content
- Force aspect ratio: `aspect-square object-cover`
- Prevent background bleed: `ring-1 ring-black/5`

---

## 7. Finishing Touches

### Supercharge Defaults
- Replace bullets with icons (checkmarks, arrows)
- Style testimonial quotes as decorative elements
- Custom checkboxes/radios with brand colors

### Add Accent Borders
```html
<div class="border-t-4 border-blue-500">Card</div>
<div class="border-l-4 border-amber-500">Alert</div>
<a class="border-b-2 border-blue-500">Active nav</a>
```

### Decorate Backgrounds
- Alternate background colors between sections
- Subtle gradients (hues within 30 degrees)
- Faint patterns, simple geometric shapes
- Keep contrast low — nothing competes with content

### Design Empty States First
Empty states are first impressions. Include illustration, clear CTA, and hide UI that doesn't work yet.

### Use Fewer Borders
Before adding a border, try: box shadow, different background colors, or more spacing.

### Think Outside the Box
- Dropdowns with sections, columns, icons
- Tables with combined columns and hierarchy
- Radio buttons as selectable cards

---

## Reference Files

For detailed principles, edge cases, and extended guidance:
- **[references/starting-from-scratch.md](references/starting-from-scratch.md)** — Design process, low-fidelity, personality, systematization
- **[references/hierarchy.md](references/hierarchy.md)** — Emphasis, de-emphasis, labels, weight/contrast, button hierarchy
- **[references/layout-and-spacing.md](references/layout-and-spacing.md)** — White space, spacing systems, grids, responsive sizing
- **[references/typography.md](references/typography.md)** — Type scale, font selection, line length/height, alignment
- **[references/color.md](references/color.md)** — HSL/oklch, palette building, shade definition, accessibility
- **[references/depth-and-shadows.md](references/depth-and-shadows.md)** — Light source, elevation system, two-part shadows, overlapping
- **[references/images.md](references/images.md)** — Photography, text over images, scaling, user content
- **[references/finishing-touches.md](references/finishing-touches.md)** — Accent borders, backgrounds, empty states, creative components
