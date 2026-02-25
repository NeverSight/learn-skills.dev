---
name: frontend-color-system
description: Color palette and theme generation from brand colors. Use when setting up project theming, creating shadcn/Tailwind color schemes, checking WCAG accessibility contrast, or building dark mode. Includes API tools for palette generation and contrast validation.
allowed-tools: Read, Edit, Write, Bash (*)
---

# Color System

Generate accessible color palettes. Check contrast. Create themes.

## When to Use

- Setting up project colors from brand color
- Checking accessibility (WCAG contrast)
- Creating dark mode variants
- Generating shadcn/Tailwind theme

## Process

**BRAND → GENERATE → VALIDATE → APPLY**

1. Get brand color (HEX)
2. Generate palette via API
3. Check contrast ratios
4. Apply to theme

## API Quick Reference

```bash
# Get color info
curl "https://www.thecolorapi.com/id?hex=6366F1"

# Generate scheme (analogic, complement, monochrome, triad)
curl "https://www.thecolorapi.com/scheme?hex=6366F1&mode=analogic&count=5"

# Check contrast (WCAG)
curl "https://webaim.org/resources/contrastchecker/?fcolor=FFFFFF&bcolor=6366F1&api"
```

## WCAG Requirements

| Level | Normal Text | Large Text |
|-------|-------------|------------|
| AA | 4.5:1 | 3:1 |
| AAA | 7:1 | 4.5:1 |

## Quick Theme from Brand

```bash
BRAND="6366F1"

# Get info
curl "https://www.thecolorapi.com/id?hex=$BRAND" | jq '.name.value, .hsl.value'

# Generate shades
curl "https://www.thecolorapi.com/scheme?hex=$BRAND&mode=monochrome&count=9"

# Check text contrast
curl "https://webaim.org/resources/contrastchecker/?fcolor=FFFFFF&bcolor=$BRAND&api"
```

## shadcn Theme Structure

```css
:root {
  /* Base */
  --background: 0 0% 100%;
  --foreground: 240 10% 3.9%;

  /* Components */
  --card: 0 0% 100%;
  --card-foreground: 240 10% 3.9%;
  --popover: 0 0% 100%;
  --popover-foreground: 240 10% 3.9%;

  /* Brand */
  --primary: 239 84% 67%;
  --primary-foreground: 0 0% 98%;

  /* Secondary/Muted/Accent */
  --secondary: 240 4.8% 95.9%;
  --secondary-foreground: 240 5.9% 10%;
  --muted: 240 4.8% 95.9%;
  --muted-foreground: 240 3.8% 46.1%;
  --accent: 240 4.8% 95.9%;
  --accent-foreground: 240 5.9% 10%;

  /* Destructive */
  --destructive: 0 84.2% 60.2%;
  --destructive-foreground: 0 0% 98%;

  /* UI */
  --border: 240 5.9% 90%;
  --input: 240 5.9% 90%;
  --ring: 239 84% 67%;
  --radius: 0.5rem;
}

.dark {
  --background: 240 10% 3.9%;
  --foreground: 0 0% 98%;
  --card: 240 10% 3.9%;
  --card-foreground: 0 0% 98%;
  --primary: 239 84% 67%;
  --primary-foreground: 240 10% 3.9%;
  --secondary: 240 3.7% 15.9%;
  --secondary-foreground: 0 0% 98%;
  --muted: 240 3.7% 15.9%;
  --muted-foreground: 240 5% 64.9%;
  --border: 240 3.7% 15.9%;
  --input: 240 3.7% 15.9%;
}
```

## Safe Primary Colors (AA on white)

| Color | HEX | Contrast |
|-------|-----|----------|
| Blue | #2563EB | 4.5:1 ✓ |
| Indigo | #4F46E5 | 4.9:1 ✓ |
| Purple | #7C3AED | 4.5:1 ✓ |
| Green | #16A34A | 4.5:1 ✓ |
| Red | #DC2626 | 4.5:1 ✓ |

## Semantic Colors

```yaml
success: "#22C55E"  # Green-500
warning: "#F59E0B"  # Amber-500
error:   "#EF4444"  # Red-500
info:    "#3B82F6"  # Blue-500
```

## Gray Scale Options

| Name | Character | Best For |
|------|-----------|----------|
| Slate | Cool blue | Tech, modern |
| Zinc | Cool neutral | Professional |
| Neutral | Pure gray | Minimal |
| Stone | Warm brown | Organic |

## Dark Mode Rules

```yaml
Light → Dark inversion:
  Background: L=100% → L=4%
  Foreground: L=4%   → L=98%
  Muted:      L=96%  → L=16%
  Border:     L=90%  → L=16%
  Primary:    Keep hue, adjust L for visibility
```

## Troubleshooting

```yaml
"Contrast too low":
  → Darken color (reduce L in HSL)
  → Use for accents only, not text

"Brand color not accessible":
  → Create darker variant for interactive
  → Use original for decorative only

"Colors look different in dark mode":
  → Increase L slightly for vibrant colors
  → Reduce chroma to avoid vibration on dark bg
```

## References

- **[palettes.md](references/palettes.md)** — Complete theme templates, Tailwind config, OKLCH
- **[workflows.md](references/workflows.md)** — Step-by-step guides from brand to theme

## External Tools

- https://ui.shadcn.com/themes — shadcn theme generator
- https://uicolors.app — Tailwind palette generator
- https://oklch.com — OKLCH color picker
- https://webaim.org/resources/contrastchecker — Contrast checker
