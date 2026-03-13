---
name: color-tools
description: Convert colors between 7 color spaces, check WCAG contrast, generate harmonies, Tailwind shades, and simulate color blindness. Use when working with hex colors, accessibility checks, palette generation, or design systems.
license: MIT
metadata:
  author: fyipedia
  version: "0.2.1"
  homepage: "https://colorfyi.com"
---

# ColorFYI — Color Tools for AI Agents

Pure Python color engine. Convert hex to RGB/HSL/CMYK/OKLCH, check WCAG contrast ratios, generate color harmonies, create Tailwind shade palettes, and simulate color blindness — all with zero dependencies.

**Install**: `pip install colorfyi` · **Web**: [colorfyi.com](https://colorfyi.com/) · **API**: [REST API](https://colorfyi.com/developers/) · **npm**: `npm install @fyipedia/colorfyi`

## When to Use

- User asks to convert a color between formats (hex, RGB, HSL, CMYK, Lab, OKLCH)
- User needs WCAG contrast ratio check for accessibility compliance
- User wants to generate a color palette, harmonies, or Tailwind shades
- User asks about color blindness simulation or accessible color choices
- User needs to pick text color (black/white) for a given background

## Tools

### `get_color_info(hex) -> ColorInfo`

Convert any hex color to all 7 color spaces in one call.

```python
from colorfyi import get_color_info

info = get_color_info("FF6B35")
info.rgb    # RGB(r=255, g=107, b=53)
info.hsl    # HSL(h=16.0, s=100.0, l=60.4)
info.cmyk   # CMYK(c=0.0, m=58.0, y=79.2, k=0.0)
info.oklch  # OKLCH(l=0.685, c=0.179, h=42.9)
info.lab    # Lab(l=65.4, a=42.1, b=47.8)
info.hsv    # HSV(h=16.0, s=79.2, v=100.0)
info.warmth # "warm"
```

### `contrast_ratio(hex1, hex2) -> ContrastResult`

WCAG 2.1 contrast check with AA/AAA pass/fail for normal and large text.

```python
from colorfyi import contrast_ratio

cr = contrast_ratio("1E40AF", "FFFFFF")
cr.ratio       # 8.55
cr.aa_normal   # True  (≥ 4.5:1)
cr.aa_large    # True  (≥ 3:1)
cr.aaa_normal  # True  (≥ 7:1)
```

### `text_color_for_bg(hex) -> str`

Pick black or white text for optimal readability on a background color.

```python
from colorfyi import text_color_for_bg

text_color_for_bg("FF6B35")  # "000000" (black)
text_color_for_bg("1E3A5F")  # "FFFFFF" (white)
```

### `harmonies(hex) -> Harmonies`

Generate 5 harmony types from the color wheel.

```python
from colorfyi import harmonies

h = harmonies("FF6B35")
h.complementary        # ['35C0FF']
h.analogous            # ['FF3535', 'FFA135']
h.triadic              # ['6B35FF', '35FF6B']
h.split_complementary  # ['3565FF', '35FFA1']
h.tetradic             # ['C035FF', '35FF6B', '35C0FF']
```

### `generate_shades(hex) -> list[Shade]`

Tailwind-style 50-950 shade palette from any base color.

```python
from colorfyi import generate_shades

shades = generate_shades("3B82F6")
for s in shades:
    print(f"{s.level}: #{s.hex}")
# 50: #EFF6FF, 100: #DBEAFE, ..., 950: #172554
```

### `simulate_color_blindness(hex, type) -> str`

Simulate how a color appears under 4 types of color vision deficiency.

```python
from colorfyi import simulate_color_blindness

simulate_color_blindness("FF0000", "deuteranopia")  # Green-blind
simulate_color_blindness("FF0000", "protanopia")    # Red-blind
simulate_color_blindness("FF0000", "tritanopia")    # Blue-blind
simulate_color_blindness("FF0000", "achromatopsia") # Total color blindness
```

### `delta_e(hex1, hex2) -> float`

Perceptual color difference (CIE76). < 2.3 = imperceptible to humans.

```python
from colorfyi import delta_e

delta_e("FF6B35", "FF6B36")  # 0.4 (imperceptible)
delta_e("FF0000", "00FF00")  # 170.6 (very different)
```

## REST API (No Auth Required)

```bash
curl https://colorfyi.com/api/color/FF6B35/
curl https://colorfyi.com/api/contrast/FF6B35/FFFFFF/
curl https://colorfyi.com/api/harmonies/FF6B35/
curl https://colorfyi.com/api/shades/FF6B35/
curl https://colorfyi.com/api/blindness/FF6B35/
```

Full spec: [OpenAPI 3.1.0](https://colorfyi.com/api/openapi.json)

## Color Spaces Reference

| Space | Format | Best For |
|-------|--------|----------|
| Hex | `#FF6B35` | Web/CSS |
| RGB | `rgb(255, 107, 53)` | Screen display |
| HSL | `hsl(16°, 100%, 60%)` | Hue adjustments |
| HSV | `hsv(16°, 79%, 100%)` | Color pickers |
| CMYK | `cmyk(0%, 58%, 79%, 0%)` | Print design |
| CIE Lab | `Lab(65.4, 42.1, 47.8)` | Perceptual comparison |
| OKLCH | `oklch(0.685, 0.179, 42.9)` | Modern CSS |

## WCAG Thresholds

| Level | Ratio | Use |
|-------|-------|-----|
| AA Normal | ≥ 4.5:1 | Body text |
| AA Large | ≥ 3:1 | 18px+ or 14px bold |
| AAA Normal | ≥ 7:1 | Enhanced accessibility |
| AAA Large | ≥ 4.5:1 | Enhanced, large text |

## Demo

![ColorFYI demo](https://raw.githubusercontent.com/fyipedia/colorfyi/main/demo.gif)

## Creative FYI Family

Part of the [FYIPedia](https://fyipedia.com) ecosystem: [EmojiFYI](https://emojifyi.com), [SymbolFYI](https://symbolfyi.com), [UnicodeFYI](https://unicodefyi.com), [FontFYI](https://fontfyi.com).
