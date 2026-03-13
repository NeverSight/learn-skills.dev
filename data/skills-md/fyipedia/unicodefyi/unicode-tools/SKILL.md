---
name: unicode-tools
description: Encode any Unicode character into 17 formats (Unicode, HTML, CSS, JavaScript, Python, Java, Go, Ruby, Rust, C/C++, URL, UTF-8/16/32), look up full Unicode properties, resolve 92 HTML entities, and search characters by name. Use when working with character encoding, Unicode lookup, or HTML entities.
license: MIT
metadata:
  author: fyipedia
  version: "0.2.1"
  homepage: "https://unicodefyi.com/"
---

# UnicodeFYI — Unicode Tools for AI Agents

Pure Python Unicode character toolkit. Compute 17 encoding representations, look up full Unicode properties (name, category, block, script), resolve 92 HTML entities, and search characters by name — all with zero dependencies (optional `fonttools` for block/script info).

**Install**: `pip install unicodefyi` · **Web**: [unicodefyi.com](https://unicodefyi.com/) · **API**: [REST API](https://unicodefyi.com/developers/) · **npm**: `npm install unicodefyi`

## When to Use

- User asks to encode a character in multiple programming languages (Python, JavaScript, Java, Go, Ruby, Rust, C/C++)
- User needs Unicode properties for a character (name, block, script, category, bidirectionality)
- User wants to look up or reverse-lookup an HTML entity
- User needs UTF-8, UTF-16, or UTF-32 byte representation
- User asks to search for Unicode characters by name (arrows, check marks, math symbols)
- User needs to convert between codepoint and character

## Tools

### `get_encodings(char) -> EncodingInfo`

Compute 17 encoding representations for any single character.

```python
from unicodefyi import get_encodings

enc = get_encodings("✓")
enc.unicode        # 'U+2713'
enc.decimal        # '10003'
enc.html_decimal   # '&#10003;'
enc.html_hex       # '&#x2713;'
enc.html_entity    # '&check;'
enc.css            # '\2713'
enc.javascript     # '\u{2713}'
enc.python         # '\u2713'
enc.java           # '\u2713'
enc.go             # '\u2713'
enc.ruby           # '\u{2713}'
enc.rust           # '\u{2713}'
enc.c_cpp          # '\u2713'
enc.url_encoded    # '%E2%9C%93'
enc.utf8_bytes     # 'e2 9c 93'
enc.utf16be_bytes  # '27 13'
enc.utf32be_bytes  # '00 00 27 13'
```

### `get_char_info(codepoint) -> CharInfo | None`

Get full Unicode properties and all encodings from a codepoint integer.

```python
from unicodefyi import get_char_info

info = get_char_info(0x2713)
info.name           # 'CHECK MARK'
info.character      # '✓'
info.codepoint      # 10003
info.category       # 'So'
info.category_name  # 'Other Symbol'
info.block          # 'Dingbats'  (requires fonttools)
info.block_slug     # 'dingbats'
info.script         # 'Zyyy'  (requires fonttools)
info.script_slug    # 'common'
info.bidirectional  # 'ON'
info.mirrored       # False
info.encodings      # EncodingInfo (all 17 formats)
```

### `search(query, limit=50) -> list[CharInfo]`

Search Unicode characters by name (case-insensitive substring match).

```python
from unicodefyi import search

results = search("arrow")
for r in results[:5]:
    print(f"{r.character} U+{r.codepoint:04X} {r.name}")
# ← U+2190 LEFTWARDS ARROW
# ↑ U+2191 UPWARDS ARROW
# → U+2192 RIGHTWARDS ARROW
# ↓ U+2193 DOWNWARDS ARROW
# ↔ U+2194 LEFT RIGHT ARROW
```

### `lookup_html_entity(entity) -> str | None`

Resolve an HTML entity string to its character. Supports 92 named entities.

```python
from unicodefyi import lookup_html_entity

lookup_html_entity("&check;")   # '✓'
lookup_html_entity("&cross;")   # '✗'
lookup_html_entity("&mdash;")   # '—'
lookup_html_entity("&hellip;")  # '…'
lookup_html_entity("&bull;")    # '•'
```

### `get_category_name(category_code) -> str`

Get the full name for a Unicode general category code.

```python
from unicodefyi import get_category_name

get_category_name("Sm")  # 'Math Symbol'
get_category_name("Cc")  # 'Control'
get_category_name("Cn")  # 'Unassigned'
```

## REST API (No Auth Required)

```bash
curl https://unicodefyi.com/api/character/2713/
curl https://unicodefyi.com/api/encode/✓/
curl https://unicodefyi.com/api/search/?q=check+mark
curl https://unicodefyi.com/api/block/dingbats/
curl https://unicodefyi.com/api/random/
```

Full spec: [OpenAPI 3.1.0](https://unicodefyi.com/api/openapi.json)

## 17 Encoding Formats

| Format | Example (`✓`) | Use Case |
|--------|--------------|----------|
| Unicode | `U+2713` | Standard reference |
| Decimal | `10003` | Numeric codepoint |
| HTML Decimal | `&#10003;` | HTML pages |
| HTML Hex | `&#x2713;` | HTML pages |
| HTML Entity | `&check;` | Named HTML entity |
| CSS | `\2713` | `content` property |
| JavaScript | `\u{2713}` | ES6+ string literals |
| Python | `\u2713` | String literals |
| Java | `\u2713` | String literals |
| Go | `\u2713` | String literals |
| Ruby | `\u{2713}` | String literals |
| Rust | `\u{2713}` | String/char literals |
| C/C++ | `\u2713` | String literals |
| URL | `%E2%9C%93` | URLs, query strings |
| UTF-8 | `e2 9c 93` | Byte-level encoding |
| UTF-16 BE | `27 13` | Windows/Java internals |
| UTF-32 BE | `00 00 27 13` | Fixed-width encoding |

## Common Unicode Blocks

| Block | Range | Examples |
|-------|-------|---------|
| Basic Latin | U+0020–U+007F | A, z, @, ~ |
| General Punctuation | U+2000–U+206F | —, …, ‰ |
| Currency Symbols | U+20A0–U+20CF | €, £, ¥, ₹ |
| Arrows | U+2190–U+21FF | ←, →, ↑, ↓ |
| Mathematical Operators | U+2200–U+22FF | ∀, ∃, ∞, ≠ |
| Geometric Shapes | U+25A0–U+25FF | ■, ●, ▲, ◆ |
| Miscellaneous Symbols | U+2600–U+26FF | ☀, ★, ♠, ♥ |
| Dingbats | U+2700–U+27BF | ✓, ✗, ✂, ✈ |

## Demo

![UnicodeFYI demo](https://raw.githubusercontent.com/fyipedia/unicodefyi/main/demo.gif)

## Creative FYI Family

Part of the [FYIPedia](https://fyipedia.com) ecosystem: [ColorFYI](https://colorfyi.com), [EmojiFYI](https://emojifyi.com), [SymbolFYI](https://symbolfyi.com), [FontFYI](https://fontfyi.com).
