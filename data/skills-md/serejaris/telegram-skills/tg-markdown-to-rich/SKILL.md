---
name: tg-markdown-to-rich
description: "Use when converting Markdown documents, reports, or any text content into a Telegram Rich Message for delivery via a bot. Triggers: \"send markdown to Telegram\", \"convert doc to rich message\", \"publish report to bot\", \"format markdown for sendRichMessage\", \"telegram rich message from file\". Produces an InputRichMessage JSON object ready for Telegram Bot API 10.2 sendRichMessage, including file_id, URL, and multipart upload media bindings."
license: MIT
---

# tg-markdown-to-rich

The converter uses Python 3 standard library only. Direct sending requires network access to
`api.telegram.org` and `TELEGRAM_BOT_TOKEN`.

Converts a Markdown file (or stdin) into a Telegram `InputRichMessage` JSON
object. The output uses the `markdown` field of `InputRichMessage` and is ready
to pass directly to [`sendRichMessage`](../../reference/rich-messages-spec.md).

See also: [`../tg-rich-messages/SKILL.md`](../tg-rich-messages/SKILL.md) for
composing rich messages programmatically.

---

## Usage

```bash
# File input → stdout JSON
python3 scripts/md2rich.py document.md

# Pipe stdin
cat report.md | python3 scripts/md2rich.py

# Additional flags
python3 scripts/md2rich.py document.md --rtl
python3 scripts/md2rich.py document.md --skip-entity-detection
python3 scripts/md2rich.py document.md \
  --media cover=photo=AgAC...file_id \
  --media voice=voice_note=https://cdn.example.com/briefing.ogg

# Bindings with player metadata (duration, performer, title, has_spoiler)
python3 scripts/md2rich.py document.md --media-json bindings.json

# Upload local files: each attach://NAME needs a matching --attach NAME=PATH
python3 scripts/md2rich.py document.md \
  --media-json bindings.json \
  --attach cover_file=./cover.png \
  --attach answer_file=./answer.mp3

# Send directly via Telegram Bot API (multipart when --attach is used)
TELEGRAM_BOT_TOKEN=<token> python3 scripts/md2rich.py document.md \
  --send --chat-id <chat_id>
```

`--media` covers the common `ID=TYPE=SOURCE` case. Use `--media-json` when a binding needs
fields that syntax cannot express — an audio track's `duration`, `performer`, and `title`,
or `has_spoiler` on a photo:

```json
[
  {
    "id": "answer",
    "media": {
      "type": "audio",
      "media": "attach://answer_file",
      "duration": 4,
      "performer": "Voice 2.0",
      "title": "Answer: 323"
    }
  }
]
```

### Exit codes

| Code | Meaning |
|---|---|
| `0` | Converted, or sent and acknowledged |
| `1` | Definite failure — limit exceeded, bad binding, or a 4xx from Telegram |
| `2` | **Unknown outcome** — 429, 5xx, or a transport failure during `--send` |

Code `2` is not a retry signal. The message may already be in the chat; resending duplicates
it. Check the target chat before any second attempt.

Output is a JSON object:

```json
{
  "markdown": "# Title\n\n![](tg://photo?id=cover)",
  "media": [
    {"id": "cover", "media": {"type": "photo", "media": "AgAC...file_id"}}
  ]
}
```

Pass this as the `rich_message` parameter to `sendRichMessage`.

---

## Markdown → Rich block mapping

| Markdown syntax | Rich block / inline |
|---|---|
| `# H1` … `###### H6` | `heading` block (size 1–6) |
| Paragraph text | `paragraph` block |
| `**bold**` / `__bold__` | `bold` inline |
| `*italic*` / `_italic_` | `italic` inline |
| `` `code` `` | `code` inline |
| `~~strikethrough~~` | `strikethrough` inline |
| `==marked==` | `marked` inline |
| `\|\|spoiler\|\|` | `spoiler` inline |
| `` ```lang … ``` `` | `pre` block (with language) |
| `[text](url)` | `url` inline |
| `[text](mailto:…)` | `email_address` inline |
| `[text](tel:…)` | `phone_number` inline |
| `[text](tg://user?id=…)` | `text_mention` inline |
| `$LaTeX$` | `mathematical_expression` inline |
| `$$LaTeX$$` / ` ```math` | `mathematical_expression` block |
| `---` | `divider` block |
| `> text` | `blockquote` block |
| `- item` / `* item` | `list` block (unordered) |
| `1. item` | `list` block (ordered) |
| `- [ ] task` / `- [x] task` | `list` block with checkbox |
| GFM table `\| … \|` | `table` block |
| `![alt](https://…)` (block-level) | `photo` block (with optional caption from title) |
| `[^id]: …` footnote | `reference` inline + `reference_link` |
| `<u>` / `<ins>` | `underline` inline (HTML pass-through) |
| `<sub>` / `<sup>` | `subscript` / `superscript` inline |
| `<aside>…<cite>…</cite></aside>` | `pullquote` block |
| `<details [open]><summary>…</summary>…</details>` | `details` block |
| `<tg-collage>…</tg-collage>` | `collage` block |
| `<tg-slideshow>…</tg-slideshow>` | `slideshow` block |

---

## Limits enforced (exit 1 on violation)

| Limit | Value |
|---|---|
| Max characters (UTF-8) | 32 768 |
| Max blocks (incl. nested) | 500 |
| Max nesting depth | 16 |
| Max media blocks | 50 |
| Max table columns | 20 |

---

## Unsupported inputs and fallback behavior

| Input | Behavior |
|---|---|
| `tg://photo`, `tg://video`, `tg://audio` | Validated both ways against `--media` / `--media-json` bindings: a reference without a binding and a binding without a reference are both exit 1 |
| `file_id` or HTTP/HTTPS source | Sent in JSON through `InputRichMessage.media` |
| `attach://name` source | Uploaded via multipart when `--attach name=path` is supplied; without it, exit 1 before any request |
| Nested blocks inside table cells | GFM spec disallows this; content treated as inline text (Telegram cells accept only inline formatting) |
| Other non-HTTP media URI | Warning to stderr; passed through for Telegram validation |
| `<tg-map>` HTML tag | Passed through unchanged; not generatable from plain Markdown |
| `RichBlockThinking` | Not producible from Markdown (only valid in `sendRichMessageDraft`) |
| HTML tags not in Rich HTML spec | Passed through; Telegram will ignore unknown tags |

---

## References

- Canonical spec: [`../../reference/rich-messages-spec.md`](../../reference/rich-messages-spec.md)
- Related skill: [`../tg-rich-messages/SKILL.md`](../tg-rich-messages/SKILL.md)
