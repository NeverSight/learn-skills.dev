---
name: technical-svg-diagrams
description: Generate clean, minimal technical SVG diagrams in a consistent Cloudflare-inspired style. Use when creating architecture diagrams, flow diagrams, or component diagrams for blog posts and documentation.
---

<objective>
Generate technical SVG diagrams with consistent styling for blog posts and documentation. All diagrams use a unified visual language: grid backgrounds, monospace fonts, muted colors with semantic accents, and clean geometric shapes.
</objective>

<quick_start>
1. Identify diagram type needed (architecture, flow, or component)
2. Read `references/svg-patterns.md` for templates and color palette
3. Generate SVG using the established patterns
4. Save to target directory with descriptive filename
</quick_start>

<design_system>
## Color Palette

| Purpose | Color | Hex |
|---------|-------|-----|
| Background | Light gray | #fafafa |
| Grid lines | Subtle gray | #e5e5e5 |
| Primary text | Dark gray | #333 |
| Secondary text | Medium gray | #666 |
| Muted text | Light gray | #999 |
| Borders/arrows | Gray | #ccc |
| Success/positive | Green | #27ae60 |
| Error/negative | Red | #e74c3c |
| Primary accent | Blue | #3498db |
| Warning/sandbox | Orange | #f39c12 |
| Process step | Purple | #9b59b6 |

## Typography

- **Font family:** `monospace` for all text
- **Title:** 14px bold, #333
- **Subtitle/tag:** 12px, #888, in brackets `[ LIKE_THIS ]`
- **Labels:** 10-11px, color matches element
- **Notes:** 7-8px, #999

## Common Elements

**Grid background:**
```xml
<pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
  <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#e5e5e5" stroke-width="0.5"/>
</pattern>
```

**Arrow marker:**
```xml
<marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
  <path d="M0,0 L0,6 L9,3 z" fill="#ccc"/>
</marker>
```

**Node (circle with inner dot):**
```xml
<circle cx="X" cy="Y" r="35" fill="none" stroke="#ccc" stroke-width="2"/>
<circle cx="X" cy="Y" r="18" fill="#COLOR"/>
```

**Box container:**
```xml
<rect x="X" y="Y" width="W" height="H" fill="none" stroke="#ccc" stroke-width="2"/>
```

**Dashed container (sandbox/isolation):**
```xml
<rect x="X" y="Y" width="W" height="H" fill="none" stroke="#f39c12" stroke-width="2" stroke-dasharray="5,3"/>
```

**Label box:**
```xml
<rect x="X" y="Y" width="W" height="H" fill="none" stroke="#ccc" stroke-width="1"/>
<text x="CX" y="CY" font-family="monospace" font-size="11" fill="#666" text-anchor="middle">LABEL_NAME</text>
```
</design_system>

<diagram_types>
## Architecture Diagrams

Horizontal left-to-right flow showing system components.

**Use for:** Before/after comparisons, system overviews, data flow

**Structure:**
- Title + tag at top left
- Components flow left to right
- Arrows connect components
- Bottom note summarizes key point

**Dimensions:** 800x350 to 800x400

## Flow Diagrams

Vertical top-to-bottom showing process steps.

**Use for:** Execution flows, request lifecycles, step-by-step processes

**Structure:**
- Title + tag at top
- Dashed vertical guide line
- Steps connected by arrows with polygon heads
- Decision diamonds for branching
- Ellipses for start/end states

**Dimensions:** 600x700 (adjust height for steps)

## Component Diagrams

Focused view of a single component's internals.

**Use for:** Showing internal structure, nested elements, detailed breakdowns

**Structure:**
- Outer container box
- Inner elements with semantic colors
- Labels above or below containers
</diagram_types>

<process>
## Creating a Diagram

1. **Determine type and dimensions**
   - Architecture: 800x350-400, horizontal
   - Flow: 600x700+, vertical
   - Component: varies by content

2. **Set up SVG structure**
   ```xml
   <svg viewBox="0 0 WIDTH HEIGHT" xmlns="http://www.w3.org/2000/svg">
     <defs>
       <!-- Grid pattern -->
       <!-- Arrow markers as needed -->
     </defs>

     <!-- Background -->
     <rect width="WIDTH" height="HEIGHT" fill="#fafafa"/>
     <rect width="WIDTH" height="HEIGHT" fill="url(#grid)"/>

     <!-- Title -->
     <text x="40" y="40" font-family="monospace" font-size="14" fill="#333" font-weight="bold">TITLE</text>
     <text x="X" y="40" font-family="monospace" font-size="12" fill="#888">[ TAG ]</text>

     <!-- Content -->

     <!-- Bottom note -->
     <text x="CENTER" y="BOTTOM" font-family="monospace" font-size="10" fill="#999" text-anchor="middle">summary note</text>
   </svg>
   ```

3. **Add components using patterns from references/svg-patterns.md**

4. **Connect with arrows**
   - Solid lines for primary flow
   - Dashed lines for secondary/return flow
   - Use opacity="0.5" for response arrows

5. **Add labels**
   - Component names in SCREAMING_SNAKE_CASE
   - Action labels in lowercase_snake_case
   - Use text-anchor="middle" for centered text

6. **Save with descriptive filename**
   - `diagram-before.svg`, `diagram-after.svg`
   - `diagram-flow.svg`, `diagram-architecture.svg`
</process>

<success_criteria>
Diagram is complete when:
- [ ] Uses consistent color palette
- [ ] All text is monospace
- [ ] Grid background applied
- [ ] Title with bracketed tag present
- [ ] Components properly connected with arrows
- [ ] Labels are clear and properly positioned
- [ ] Bottom summary note included
- [ ] SVG is valid and renders correctly
</success_criteria>

<export_to_webp>
## Convert SVG to WebP

After creating the SVG, convert to WebP for universal compatibility.

**Using uv (cross-platform, recommended):**
```bash
uvx --from cairosvg cairosvg diagram.svg -o diagram.png --output-width 1600
uvx --with pillow python -c "from PIL import Image; Image.open('diagram.png').save('diagram.webp', 'WEBP', lossless=True)"
rm diagram.png
```
Note: `lossless=True` is best for diagrams - smaller than lossy AND perfect quality.

**Alternative tools (if available):**
```bash
# ImageMagick
convert -background none -density 150 diagram.svg diagram.webp

# librsvg + cwebp
rsvg-convert -w 1600 diagram.svg -o diagram.png && cwebp diagram.png -o diagram.webp
```

**Platform notes:**
- macOS: `brew install cairo` if cairosvg fails
- Linux: `apt install libcairo2-dev` if needed
- Windows: uv works natively; or use WSL for other tools
</export_to_webp>
