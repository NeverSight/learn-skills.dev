---
name: symbol-tools
description: Encode any symbol or character into 11 formats (Unicode, HTML, CSS, JavaScript, Python, Java, UTF-8, UTF-16, URL), look up Unicode properties, and resolve 47 HTML entities. Use when working with special characters, symbol encoding, or Unicode lookups.
license: MIT
metadata:
  author: fyipedia
  version: "0.2.1"
  homepage: "https://symbolfyi.com/"
---

# SymbolFYI — Symbol Tools for AI Agents

Pure Python symbol encoder. Compute 11 encoding representations and full Unicode properties for any character. Includes 47 HTML entity mappings — all with zero dependencies (optional `fonttools` for block/script info).

**Install**: `pip install symbolfyi` · **Web**: [symbolfyi.com](https://symbolfyi.com/) · **API**: [REST API](https://symbolfyi.com/developers/) · **npm**: `npm install symbolfyi`

## When to Use

- User asks to encode a symbol or special character into Unicode, HTML, CSS, or programming language format
- User needs Unicode properties for a character (name, category, block, script)
- User wants to look up or reverse-lookup an HTML entity (`&rarr;`, `&hearts;`, etc.)
- User needs UTF-8 or UTF-16 byte representation of a character
- User asks about Unicode general categories or bidirectional properties

## Tools

### `get_encodings(char) -> EncodingInfo`

Compute 11 encoding representations for any single character.

```python
from symbolfyi import get_encodings

enc = get_encodings("→")
enc.unicode        # 'U+2192'
enc.html_decimal   # '&#8594;'
enc.html_hex       # '&#x2192;'
enc.html_entity    # '&rarr;'
enc.css            # '\2192'
enc.javascript     # '\u{2192}'
enc.python         # '\u2192'
enc.java           # '\u2192'
enc.utf8_bytes     # 'e2 86 92'
enc.utf16_bytes    # '21 92'
enc.url_encoded    # '%E2%86%92'
```

### `get_info(char) -> SymbolInfo | None`

Get full Unicode properties and all encodings for a character.

```python
from symbolfyi import get_info

info = get_info("♠")
info.name           # 'BLACK SPADE SUIT'
info.codepoint      # 9824
info.character      # '♠'
info.category       # 'So'
info.category_name  # 'Other Symbol'
info.block          # 'Miscellaneous Symbols'  (requires fonttools)
info.script         # 'Zyyy'  (requires fonttools)
info.bidirectional  # 'ON'
info.mirrored       # False
info.encodings      # EncodingInfo (all 11 formats)
```

### `lookup_html_entity(entity) -> str | None`

Resolve an HTML entity string to its character.

```python
from symbolfyi import lookup_html_entity

lookup_html_entity("&amp;")     # '&'
lookup_html_entity("&hearts;")  # '♥'
lookup_html_entity("&rarr;")    # '→'
lookup_html_entity("&euro;")    # '€'
```

### `get_category_name(category_code) -> str`

Get the full name for a Unicode general category code.

```python
from symbolfyi import get_category_name

get_category_name("Sm")  # 'Math Symbol'
get_category_name("Sc")  # 'Currency Symbol'
get_category_name("Lu")  # 'Uppercase Letter'
```

## REST API (No Auth Required)

```bash
curl https://symbolfyi.com/api/symbol/2192/
curl https://symbolfyi.com/api/encode/→/
curl https://symbolfyi.com/api/search/?q=arrow
curl https://symbolfyi.com/api/collection/arrows/
curl https://symbolfyi.com/api/random/
```

Full spec: [OpenAPI 3.1.0](https://symbolfyi.com/api/openapi.json)

## Encoding Formats Reference

| Format | Example (`→`) | Use Case |
|--------|--------------|----------|
| Unicode | `U+2192` | Standard reference |
| HTML Decimal | `&#8594;` | HTML pages |
| HTML Hex | `&#x2192;` | HTML pages |
| HTML Entity | `&rarr;` | Named HTML entity |
| CSS | `\2192` | `content` property |
| JavaScript | `\u{2192}` | ES6+ string literals |
| Python | `\u2192` | String literals |
| Java | `\u2192` | String literals |
| UTF-8 | `e2 86 92` | Byte-level encoding |
| UTF-16 | `21 92` | Windows/Java internals |
| URL | `%E2%86%92` | URLs, query strings |

## Common HTML Entities

| Entity | Character | Name |
|--------|-----------|------|
| `&amp;` | & | Ampersand |
| `&lt;` `&gt;` | < > | Angle brackets |
| `&copy;` | © | Copyright |
| `&reg;` | ® | Registered |
| `&trade;` | ™ | Trademark |
| `&euro;` | € | Euro sign |
| `&pound;` | £ | Pound sign |
| `&rarr;` | → | Right arrow |
| `&hearts;` | ♥ | Heart suit |
| `&infin;` | ∞ | Infinity |
| `&ne;` | ≠ | Not equal |
| `&le;` `&ge;` | ≤ ≥ | Less/greater or equal |

## Unicode General Categories

| Code | Name | Examples |
|------|------|---------|
| Lu | Uppercase Letter | A, B, C |
| Ll | Lowercase Letter | a, b, c |
| Nd | Decimal Number | 0, 1, 2 |
| Sm | Math Symbol | +, =, ∞ |
| Sc | Currency Symbol | $, €, £ |
| So | Other Symbol | ♠, ♥, ☆ |
| Po | Other Punctuation | !, ?, . |
| Ps/Pe | Open/Close Punctuation | (, ), [, ] |

## Demo

![SymbolFYI demo](https://raw.githubusercontent.com/fyipedia/symbolfyi/main/demo.gif)

## Creative FYI Family

Part of the [FYIPedia](https://fyipedia.com) ecosystem: [ColorFYI](https://colorfyi.com), [EmojiFYI](https://emojifyi.com), [UnicodeFYI](https://unicodefyi.com), [FontFYI](https://fontfyi.com).
