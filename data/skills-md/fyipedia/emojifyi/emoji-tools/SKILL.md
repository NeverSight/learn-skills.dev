---
name: emoji-tools
description: Encode emojis into 8 formats (UTF-8, UTF-16, HTML, CSS, Python, JavaScript, Java), look up emoji metadata, and search 3,781 emojis from Unicode Emoji 16.0. Use when working with emoji encoding, lookup, or browsing by category.
license: MIT
metadata:
  author: fyipedia
  version: "0.2.1"
  homepage: "https://emojifyi.com/"
---

# EmojiFYI — Emoji Tools for AI Agents

Pure Python emoji toolkit. Encode any emoji into 8 representations, look up metadata for 3,781 emojis from Unicode Emoji 16.0, search by name, and browse by category — all with zero dependencies.

**Install**: `pip install emojifyi` · **Web**: [emojifyi.com](https://emojifyi.com/) · **API**: [REST API](https://emojifyi.com/developers/) · **npm**: `npm install emojifyi`

## When to Use

- User asks to encode an emoji into UTF-8, UTF-16, HTML entity, CSS, Python, JavaScript, or Java format
- User needs to look up emoji metadata (category, Unicode version, ZWJ status, skin tone support)
- User wants to search emojis by name or keyword
- User needs to browse emojis by category or Unicode version
- User asks about emoji codepoints, surrogate pairs, or encoding details

## Tools

### `encode(character) -> EncodingResult`

Compute all 8 encoding representations for any emoji or Unicode character.

```python
from emojifyi import encode

result = encode("😀")
result.codepoint              # 'U+1F600'
result.utf8_bytes             # '0xF0 0x9F 0x98 0x80'
result.utf16_surrogates       # '0xD83D 0xDE00'
result.html_entity            # '&#x1F600;'
result.css_content            # '\1F600'
result.python_literal         # '\U0001F600'
result.javascript_literal     # '\u{1F600}'
result.java_literal           # '\uD83D\uDE00'
```

### `get_emoji(slug) -> EmojiInfo | None`

Look up emoji metadata by slug.

```python
from emojifyi import get_emoji

info = get_emoji("grinning-face")
info.character       # 😀
info.codepoint       # U+1F600
info.cldr_name       # grinning face
info.category        # smileys-and-emotion
info.subcategory     # face-smiling
info.emoji_version   # 1.0
info.is_zwj          # False
info.has_skin_tones  # False
```

### `get_emoji_by_char(character) -> EmojiInfo | None`

Look up emoji metadata by its character.

```python
from emojifyi import get_emoji_by_char

info = get_emoji_by_char("❤️")
info.slug            # red-heart
info.category        # smileys-and-emotion
```

### `search(query, limit=20) -> list[EmojiInfo]`

Search emojis by name (case-insensitive substring match).

```python
from emojifyi import search

results = search("heart")
for emoji in results[:5]:
    print(f"{emoji.character} {emoji.cldr_name}")
# ❤️ red heart
# 🧡 orange heart
# 💛 yellow heart
# ...
```

### `by_category(category_slug) -> list[EmojiInfo]`

Get all emojis in a category.

```python
from emojifyi import by_category

faces = by_category("smileys-and-emotion")
print(len(faces))  # 184
```

### `by_version(version) -> list[EmojiInfo]`

Get all emojis added in a specific Emoji version.

```python
from emojifyi import by_version

new = by_version("16.0")
for e in new[:3]:
    print(f"{e.character} {e.cldr_name}")
```

### `categories() -> list[Category]`

List all 10 emoji categories.

```python
from emojifyi import categories

for cat in categories():
    print(f"{cat.icon} {cat.name} ({cat.slug})")
```

### `emoji_count() -> int`

Total number of emojis in the dataset.

```python
from emojifyi import emoji_count

print(emoji_count())  # 3781
```

## REST API (No Auth Required)

```bash
curl https://emojifyi.com/api/emoji/grinning-face/
curl https://emojifyi.com/api/encode/😀/
curl https://emojifyi.com/api/search/?q=heart
curl https://emojifyi.com/api/category/smileys-and-emotion/
curl https://emojifyi.com/api/random/
```

Full spec: [OpenAPI 3.1.0](https://emojifyi.com/api/openapi.json)

## Emoji Encoding Formats

| Format | Example (`😀`) | Use Case |
|--------|---------------|----------|
| Codepoint | `U+1F600` | Unicode standard reference |
| UTF-8 | `0xF0 0x9F 0x98 0x80` | Web, files, databases |
| UTF-16 | `0xD83D 0xDE00` | Windows, Java, JavaScript internals |
| HTML | `&#x1F600;` | Web pages, emails |
| CSS | `\1F600` | `content` property |
| Python | `\U0001F600` | String literals |
| JavaScript | `\u{1F600}` | ES6+ string literals |
| Java | `\uD83D\uDE00` | Surrogate pair literals |

## Emoji Categories

| Category | Examples |
|----------|---------|
| Smileys & Emotion | 😀 😂 ❤️ 💋 |
| People & Body | 👋 🤝 👨‍💻 |
| Animals & Nature | 🐶 🌸 🌍 |
| Food & Drink | 🍕 🍺 ☕ |
| Travel & Places | ✈️ 🏠 🗽 |
| Activities | ⚽ 🎮 🎨 |
| Objects | 💡 📱 🔑 |
| Symbols | ✅ ❌ ♻️ |
| Flags | 🇺🇸 🇯🇵 🇰🇷 |
| Component | 🏻 🏼 🏽 (skin tones) |

## Demo

![EmojiFYI demo](https://raw.githubusercontent.com/fyipedia/emojifyi/main/demo.gif)

## Creative FYI Family

Part of the [FYIPedia](https://fyipedia.com) ecosystem: [ColorFYI](https://colorfyi.com), [SymbolFYI](https://symbolfyi.com), [UnicodeFYI](https://unicodefyi.com), [FontFYI](https://fontfyi.com).
