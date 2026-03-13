---
name: font-tools
description: Access 50 popular Google Fonts metadata, generate CSS import URLs and font-family declarations, browse 10 web-safe font stacks, and get 15 curated font pairings with mood and use-case recommendations. Use when working with web fonts, typography, or CSS font configuration.
license: MIT
metadata:
  author: fyipedia
  version: "0.2.1"
  homepage: "https://fontfyi.com/"
---

# FontFYI — Font Tools for AI Agents

Pure Python Google Fonts toolkit. Access 50 popular fonts metadata, generate CSS import URLs, browse 10 web-safe font stacks, and get 15 curated heading + body pairings — all with zero dependencies.

**Install**: `pip install fontfyi` · **Web**: [fontfyi.com](https://fontfyi.com/) · **API**: [REST API](https://fontfyi.com/developers/) · **npm**: `npm install fontfyi`

## When to Use

- User asks to look up a Google Font's metadata (category, variants, subsets, designer)
- User needs a CSS `font-family` declaration or Google Fonts import URL
- User wants font pairing suggestions for heading + body combinations
- User asks about web-safe font stacks for system fonts, monospace, serif, etc.
- User needs to generate `<link>` tags or Homebrew install commands for fonts

## Tools

### `get_font(slug) -> dict | None`

Look up font metadata by slug.

```python
from fontfyi import get_font

font = get_font("inter")
font["family"]           # 'Inter'
font["category"]         # 'sans-serif'
font["variants"]         # ['100', '200', '300', 'regular', '500', '600', '700', '800', '900']
font["subsets"]          # ['cyrillic', 'greek', 'latin', 'latin-ext', 'vietnamese']
font["designer"]         # 'Rasmus Andersson'
font["popularity_rank"]  # 6
```

### `search(query, limit=20) -> list[dict]`

Search fonts by family name (case-insensitive).

```python
from fontfyi import search

results = search("rob")
for font in results:
    print(f"{font['family']} ({font['category']})")
# Roboto (sans-serif)
# Roboto Condensed (sans-serif)
# Roboto Mono (monospace)
# Roboto Slab (serif)
```

### `css_family(family, category) -> str`

Generate a CSS `font-family` declaration with proper fallback.

```python
from fontfyi import css_family

css_family("Inter", "sans-serif")       # "'Inter', sans-serif"
css_family("Roboto Mono", "monospace")  # "'Roboto Mono', monospace"
css_family("Playfair Display", "serif") # "'Playfair Display', serif"
```

### `google_fonts_url(family, weights=None) -> str`

Generate a Google Fonts CSS2 import URL.

```python
from fontfyi import google_fonts_url

google_fonts_url("Inter", [400, 700])
# 'https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap'

google_fonts_url("Roboto")
# 'https://fonts.googleapis.com/css2?family=Roboto&display=swap'
```

### `google_fonts_link(family, weights=None) -> str`

Generate a complete HTML `<link>` tag for Google Fonts.

```python
from fontfyi import google_fonts_link

google_fonts_link("Inter", [400, 700])
# '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap">'
```

### `get_pairings_for(font_slug) -> list[FontPairing]`

Get all curated pairings that include a given font.

```python
from fontfyi import get_pairings_for

for p in get_pairings_for("inter"):
    print(f"{p.heading} + {p.body} ({p.mood}, score: {p.score})")
# inter + merriweather (professional-modern, score: 9)
# poppins + inter (modern-friendly, score: 9)
# space-grotesk + inter (tech-modern, score: 8)
# plus-jakarta-sans + inter (modern-clean, score: 8)
# inter + source-serif-4 (modern-readable, score: 8)
```

### `get_stack(slug) -> FontStack | None`

Get a web-safe CSS font stack preset.

```python
from fontfyi import get_stack

stack = get_stack("system-ui")
stack.name   # 'System UI'
stack.stack  # "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"

stack = get_stack("monospace-code")
stack.stack  # "ui-monospace, 'Cascadia Code', 'Source Code Pro', Menlo, Consolas, 'DejaVu Sans Mono', monospace"
```

### `parse_variants(variants) -> tuple[list[int], bool]`

Parse Google Fonts variant strings into numeric weights and italic flag.

```python
from fontfyi import parse_variants

weights, has_italic = parse_variants(["100", "regular", "700", "italic", "700italic"])
weights      # [100, 400, 700]
has_italic   # True
```

### `weight_name(weight) -> str`

Get the CSS weight name for a numeric weight value.

```python
from fontfyi import weight_name

weight_name(400)  # 'Regular'
weight_name(700)  # 'Bold'
weight_name(300)  # 'Light'
```

### `homebrew_install_cmd(family) -> str`

Generate a Homebrew cask install command for a font.

```python
from fontfyi import homebrew_install_cmd

homebrew_install_cmd("JetBrains Mono")  # 'brew install --cask font-jetbrains-mono'
homebrew_install_cmd("Inter")           # 'brew install --cask font-inter'
```

## REST API (No Auth Required)

```bash
curl https://fontfyi.com/api/font/inter/
curl https://fontfyi.com/api/search/?q=roboto
curl https://fontfyi.com/api/pairings/inter/
curl https://fontfyi.com/api/stack/system-ui/
curl https://fontfyi.com/api/random/
```

Full spec: [OpenAPI 3.1.0](https://fontfyi.com/api/openapi.json)

## Font Stacks Reference

| Stack | CSS Value |
|-------|-----------|
| System UI | `system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, ...` |
| Neo-grotesque | `Inter, Roboto, 'Helvetica Neue', 'Arial Nova', ...` |
| Transitional | `Charter, 'Bitstream Charter', 'Sitka Text', Cambria, serif` |
| Old Style | `'Iowan Old Style', 'Palatino Linotype', ...` |
| Humanist Sans | `Seravek, 'Gill Sans Nova', Ubuntu, Calibri, ...` |
| Geometric Humanist | `Avenir, Montserrat, Corbel, ...` |
| Monospace Code | `ui-monospace, 'Cascadia Code', 'Source Code Pro', Menlo, ...` |
| Monospace Slab | `'Nimbus Mono PS', 'Courier New', monospace` |
| Industrial | `Bahnschrift, 'DIN Alternate', 'Franklin Gothic Medium', ...` |
| Rounded Sans | `ui-rounded, 'Hiragino Maru Gothic ProN', Quicksand, ...` |

## CSS Weight Names

| Weight | Name |
|--------|------|
| 100 | Thin |
| 200 | Extra Light |
| 300 | Light |
| 400 | Regular |
| 500 | Medium |
| 600 | Semi Bold |
| 700 | Bold |
| 800 | Extra Bold |
| 900 | Black |

## Demo

![FontFYI demo](https://raw.githubusercontent.com/fyipedia/fontfyi/main/demo.gif)

## Creative FYI Family

Part of the [FYIPedia](https://fyipedia.com) ecosystem: [ColorFYI](https://colorfyi.com), [EmojiFYI](https://emojifyi.com), [SymbolFYI](https://symbolfyi.com), [UnicodeFYI](https://unicodefyi.com).
