---
name: tg-rich-messages
description: "Use when sending structured or richly formatted messages from a Telegram bot — tables, section headings, collapsible blocks, photo galleries, maps, math formulas, audio, native styled buttons, bot UI cards, or streaming AI responses. Also use for understanding rich message types and limits when plain sendMessage with parse_mode HTML/Markdown is not sufficient."
license: MIT
---

# tg-rich-messages

Sending requires network access to `api.telegram.org` and a Telegram bot token.

## Overview

Bot API 10.1 introduced **Rich Messages**. Bot API 10.2 (July 14, 2026) added direct
outgoing block JSON and explicit media bindings. Rich messages are document-grade content
delivered directly in chat. Think Instant View articles — headings, tables, collage,
slideshow, map, math, collapsible blocks — but sent by a bot via `sendRichMessage`.

**Use `sendRichMessage` instead of `sendMessage` when you need:**

| Need | Mechanism |
|---|---|
| Section headings (h1–h6) | `RichBlockSectionHeading` |
| Tables with header rows / spanning cells | `RichBlockTable` |
| Collapsible sections | `RichBlockDetails` |
| Photo grid or slide deck | `RichBlockCollage` / `RichBlockSlideshow` |
| Embedded map | `RichBlockMap` |
| LaTeX math (inline or block) | `RichTextMathematicalExpression` / `RichBlockMathematicalExpression` |
| Streaming AI reply with "Thinking…" block | `sendRichMessageDraft` + `RichBlockThinking` |
| Footnotes / anchor links | `RichTextReference` / `RichTextAnchorLink` |

Plain `sendMessage` with `parse_mode: HTML` still covers bold/italic/code/spoiler/links
for simple formatting. Move to `sendRichMessage` only when you need structural blocks.

---

## Bot UI composition (10.3)

Use the network-free [Python helper](scripts/rich_ui.py) for deterministic heading, paragraph, pre, compact table, details and photo blocks with literal strings. It validates a narrow subset, not the complete Bot API. Photo uploads stay in the consumer's authorized transport. See [consumer integration](consumer-integration.md) for the exact API, illustrated previews, provenance, send/edit lifecycle and local tests.

Inline keyboard styles: `primary`, `success`, `danger`; omit for app default. Product composition: at most one primary CTA per screen; neutral secondary navigation. Green is reserved for confirmed success or a desirable commit, red for genuinely destructive actions. Ordinary Back/Cancel, bonus offers and verification actions remain neutral. Start with heading → brief value → next action; move provider plumbing and limits to contextual About/limits views. Review actual mobile outcomes and user feedback before adding emphasis. RichMessageButton additionally accepts `link` only for callback buttons. Never put `link` on InlineKeyboardButton. Native rich button rows use `type: "buttons"`, 1–8 buttons and optional `align: left|center|right`; these are documented in the reference and intentionally outside the helper subset.

For decision/inference bots, explain what the product does and why it helps with a concrete **input → criteria → result** sequence. Offer a free catalogue and case preview before an explicit paid/quota-consuming run; cached navigation should not silently repeat inference. Attribute source-backed cases as your observed experiment, an external project, or a synthetic teaching adaptation. Keep source links available and longer provenance in a closed details block. Show actual outputs and disclose missing values honestly. See the onboarding section in [consumer integration](consumer-integration.md).

Direct block text is literal RichText. Keep dynamic strings unescaped; HTML escaping belongs only to an HTML renderer. A native JSON code block is `{"type":"pre","text":json_string,"language":"json"}`. Table cells require `align` and `valign`; compact tables use `is_compact: true`.

Update an acknowledged screen with `editMessageText.rich_message`, exactly one of `text` and `rich_message`. Keep returned Bot API message IDs and check callback ownership/current-screen binding. There is no `editRichMessage`. Do not silently duplicate a message after an unknown delivery outcome.

## Sending: InputRichMessage

`sendRichMessage` takes an `InputRichMessage` object in its `rich_message` field.
Choose exactly one content field:

| Field | When to use |
|---|---|
| `html` | Rich HTML with Telegram-specific tags |
| `markdown` | GitHub-Flavored Markdown + Telegram extensions |
| `blocks` | Direct `InputRichBlock[]` JSON for deterministic programmatic composition |

Do not pass multiple content fields. With `html` or `markdown`, add optional `media` bindings
for uploaded files, Telegram `file_id` values, or HTTP URLs.

Optional fields on `InputRichMessage`:

| Field | Type | Purpose |
|---|---|---|
| `is_rtl` | Boolean | Render message right-to-left |
| `skip_entity_detection` | Boolean | Disable auto-detection of URLs, emails, mentions, etc. |
| `media` | InputRichMessageMedia[] | Resolve `tg://photo`, `tg://video`, and `tg://audio` references in markup |

### Media bindings for HTML and Markdown

Reference media in markup:

```markdown
![](tg://photo?id=cover)
![](tg://video?id=demo)
![](tg://audio?id=voice)
```

Then bind each ID:

```json
{
  "markdown": "## Launch\n\n![](tg://photo?id=cover)",
  "media": [
    {
      "id": "cover",
      "media": {"type": "photo", "media": "AgAC...file_id"}
    }
  ]
}
```

Media IDs are 1–64 characters using only letters, digits, `_`, and `-`. The nested
`InputMedia*.media` accepts a Telegram `file_id`, an HTTP/HTTPS URL, or
`attach://<part_name>`. Use JSON for `file_id` and URLs. Use multipart/form-data for
`attach://` uploads and provide a file part with the same name.

`InputRichMessageMedia.media` may be `InputMediaAnimation`, `InputMediaAudio`,
`InputMediaPhoto`, `InputMediaVideo`, or `InputMediaVoiceNote`. Markup exposes three
reference schemes: `photo`, `video`, and `audio`; animation travels through `video`, and
voice note through `audio`.

#### Captions and player metadata

The caption comes from the **markup**, not from the binding — the title argument of the
Markdown image syntax (or `<figcaption>` in HTML):

```markdown
![](tg://photo?id=cover "Release notes: the model shipped on July 29")
```

`InputMedia*.caption` inside the binding is ignored. What the binding *does* carry is
player metadata, and for audio it is what turns a raw file into a labelled track in the
message:

```json
{
  "id": "live_answer",
  "media": {
    "type": "audio",
    "media": "attach://live_answer_file",
    "duration": 4,
    "performer": "Grok Voice 2.0",
    "title": "Answer: 323"
  }
}
```

| Type | Metadata worth setting |
|---|---|
| `audio` | `duration`, `performer`, `title` — shown in the inline player |
| `video` | `duration`, `width`, `height`, `thumbnail`, `supports_streaming`, `has_spoiler` |
| `photo` | `has_spoiler` |

Set `duration` even when Telegram can infer it: several short clips in one message render
as a consistent list only when every one of them reports its length.

### Preflight: validate bindings before sending

Telegram reports a bad binding as one opaque `Bad Request`. Validate locally first and the
failure names the offending id. Four checks, all cheap:

1. **Every `tg://…?id=X` in markup has a binding.** Missing → the media silently never
   renders or the call fails.
2. **Every binding is referenced by the markup.** An unused binding means an editing slip —
   a renamed id, a dropped paragraph. Telegram's behaviour here is unspecified; treat it as
   a build error of your own.
3. **The reference scheme matches the bound type.** `tg://audio?id=X` accepts `audio` or
   `voice_note`; `tg://video?id=X` accepts `video` or `animation`; `tg://photo?id=X` accepts
   `photo`. A mismatch is a definite error.
4. **Every `attach://<name>` has a matching file part**, and the file exists on disk.

```python
import re

REF = re.compile(r"tg://(photo|video|audio)\?id=([A-Za-z0-9_-]+)")
ACCEPTS = {"photo": {"photo"}, "video": {"video", "animation"}, "audio": {"audio", "voice_note"}}

def check(markup: str, media: list[dict]) -> None:
    bound = {item["id"]: item["media"]["type"] for item in media}
    refs = set(REF.findall(markup))
    referenced = {media_id for _, media_id in refs}
    if missing := referenced - bound.keys():
        raise ValueError(f"missing bindings: {sorted(missing)}")
    if unused := bound.keys() - referenced:
        raise ValueError(f"unused bindings: {sorted(unused)}")
    for scheme, media_id in refs:
        if bound[media_id] not in ACCEPTS[scheme]:
            raise ValueError(f"{media_id}: tg://{scheme} cannot carry {bound[media_id]}")
```

Keep the file paths in a small manifest next to the payload — attachment name, path, MIME
type — so the multipart step is a lookup rather than a second source of truth:

```json
[
  {"id": "cover", "attachment_name": "cover_file", "path": "cover.png", "mime_type": "image/png"}
]
```

### Direct block JSON

Use `blocks` when code already has a structured document tree:

```json
{
  "blocks": [
    {"type": "heading", "size": 2, "text": "Daily AI Brief"},
    {"type": "paragraph", "text": ["One release matters today: ", {"type": "bold", "text": "Opus 5"}]},
    {
      "type": "photo",
      "photo": {"type": "photo", "media": "AgAC...file_id"},
      "caption": {"text": "Official launch image"}
    }
  ]
}
```

Nested blocks use `InputRichBlock`. Media blocks embed `InputMedia*` directly. Put captions
in the outer block; captions inside nested `InputMedia*` are ignored.

---

## Sending: HTTP calls

### curl (HTML mode)

```bash
curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendRichMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": '"$CHAT_ID"',
    "rich_message": {
      "html": "<h2>Weekly Report</h2><p>Highlights from the past week.</p><table bordered><tr><th>Item</th><th>Value</th></tr><tr><td>Sales</td><td><b>142</b></td></tr></table>"
    }
  }'
```

### Python (stdlib, HTML mode)

```python
import json
import os
import urllib.request

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = int(os.environ["CHAT_ID"])

payload = {
    "chat_id": CHAT_ID,
    "rich_message": {
        "html": (
            "<h2>Weekly Report</h2>"
            "<p>Highlights from the past week.</p>"
            "<table bordered>"
            "<tr><th>Item</th><th>Value</th></tr>"
            "<tr><td>Sales</td><td><b>142</b></td></tr>"
            "</table>"
        )
    },
}

req = urllib.request.Request(
    f"https://api.telegram.org/bot{TOKEN}/sendRichMessage",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"},
    method="POST",
)
with urllib.request.urlopen(req) as resp:
    result = json.load(resp)
```

### Python (stdlib, Markdown mode)

```python
payload = {
    "chat_id": CHAT_ID,
    "rich_message": {
        "markdown": (
            "## Weekly Report\n\n"
            "Highlights from the past week.\n\n"
            "| Item | Value |\n"
            "|------|-------|\n"
            "| Sales | **142** |\n"
        )
    },
}
```

See [`examples.md`](examples.md) for more complete examples including streaming drafts,
collages, details blocks, and a full multipart upload.

### Delivery outcomes: what a failed call actually means

A rich message with uploads is a large multipart request, so the interesting failures are
not validation errors — they are the ones where you do not know whether the message went
out. Split the response three ways:

| Response | Meaning | Correct reaction |
|---|---|---|
| `ok: true` | Delivered | Store `message_id` — it is the handle for later `editMessageText` |
| HTTP 4xx with `ok: false` | Definite failure, nothing was posted | Fix the payload and resend |
| HTTP 429 or 5xx, or a transport timeout | **Unknown** — the message may already be in the channel | Do not blind-retry |

The third row is the one that bites. Retrying a timed-out `sendRichMessage` is how a channel
gets the same article twice, and there is no dedup on Telegram's side. Mark the send as
*unresolved* instead, and require a human (or a lookup of the channel's last message) to
decide before anything is sent again. If you retry automatically anywhere, retry only calls
that failed with a definite 4xx.

---

## Block types — quick reference

### Structural blocks

| Type string | HTML tag | Purpose | Key fields |
|---|---|---|---|
| `paragraph` | `<p>` | Text paragraph | `text: RichText` |
| `heading` | `<h1>`–`<h6>` | Section heading | `text`, `size: 1–6` (1 = largest) |
| `pre` | `<pre>` | Preformatted / code block | `text`, `language?: string` |
| `footer` | `<footer>` | Footer text | `text: RichText` |
| `divider` | `<hr/>` | Horizontal rule | _(no content fields)_ |
| `anchor` | `<a name="...">` | Named anchor point | `name: string` |
| `mathematical_expression` | `<tg-math-block>` | Block LaTeX formula | `expression: string` |
| `list` | `<ul>` / `<ol>` | Ordered or unordered list | `items: RichBlockListItem[]` |
| `blockquote` | `<blockquote>` | Block quotation | `blocks: RichBlock[]`, `credit?: RichText` |
| `pullquote` | `<aside>` | Centered pull quote | `text`, `credit?: RichText` |
| `details` | `<details>` | Collapsible section | `summary: RichText`, `blocks: RichBlock[]`, `is_open?: true` |
| `table` | `<table>` | Data table | `cells: RichBlockTableCell[][]`, `is_bordered?`, `is_striped?`, `caption?: RichText` |
| `map` | `<tg-map>` | Static embedded map | `location: Location`, `zoom: 0–24`, `width`, `height`, `caption?` |
| `collage` | `<tg-collage>` | Photo/video grid | `blocks: RichBlock[]`, `caption?: RichBlockCaption` |
| `slideshow` | `<tg-slideshow>` | Swipeable photo/video deck | `blocks: RichBlock[]`, `caption?: RichBlockCaption` |
| `photo` | `<img>` | Photo block | `photo: PhotoSize[]`, `has_spoiler?: true`, `caption?` |
| `video` | `<video>` | Video block | `video: Video`, `has_spoiler?: true`, `caption?` |
| `animation` | `<video>` (gif) | Animation / GIF block | `animation: Animation`, `has_spoiler?: true`, `caption?` |
| `audio` | `<audio>` (mp3) | Audio / music block | `audio: Audio`, `caption?` |
| `voice_note` | `<audio>` (ogg) | Voice message block | `voice_note: Voice`, `caption?` |
| `thinking` | `<tg-thinking>` | "Thinking…" placeholder **(draft only)** | `text: RichText` |

> **`thinking` is only valid in `sendRichMessageDraft`.** It cannot appear in `sendRichMessage` and is never stored in a Message.

### Inline text types (RichText)

| Type string | HTML tag | Purpose | Extra fields |
|---|---|---|---|
| `bold` | `<b>` | Bold | `text` |
| `italic` | `<i>` | Italic | `text` |
| `underline` | `<u>` | Underline | `text` |
| `strikethrough` | `<s>` | Strikethrough | `text` |
| `spoiler` | `<tg-spoiler>` | Hidden spoiler text | `text` |
| `marked` | `<mark>` | Highlight | `text` |
| `code` | `<code>` | Inline monospace | `text` |
| `subscript` | `<sub>` | Subscript | `text` |
| `superscript` | `<sup>` | Superscript | `text` |
| `custom_emoji` | `<tg-emoji>` | Custom emoji | `custom_emoji_id`, `alternative_text` |
| `mathematical_expression` | `<tg-math>` | Inline LaTeX | `expression: string` |
| `date_time` | `<tg-time>` | Formatted timestamp | `text`, `unix_time: int`, `date_time_format: string` |
| `text_mention` | `<a href="tg://user?id=...">` | User mention by ID | `text`, `user: User` |
| `mention` | auto-detected | Username mention | `text`, `username: string` |
| `url` | `<a href="https://...">` | URL link | `text`, `url: string` |
| `email_address` | `<a href="mailto:...">` | Email link | `text`, `email_address: string` |
| `phone_number` | `<a href="tel:...">` | Phone link | `text`, `phone_number: string` |
| `bank_card_number` | auto-detected | Bank card highlight | `text`, `bank_card_number: string` |
| `hashtag` | auto-detected | Hashtag | `text`, `hashtag: string` |
| `cashtag` | auto-detected | Cashtag | `text`, `cashtag: string` |
| `bot_command` | auto-detected | Bot command | `text`, `bot_command: string` |
| `anchor` | `<a name="...">` (inline) | Inline anchor point | `name: string` |
| `anchor_link` | `<a href="#...">` | Link to anchor | `text`, `anchor_name: string` (empty = top) |
| `reference` | `<tg-reference name="...">` | Footnote definition | `text`, `name: string` |
| `reference_link` | `<a href="#...">` (ref) | Link to footnote | `text`, `reference_name: string` |

---

## Markdown quick syntax

```
**bold**   *italic*   __bold__   _italic_
~~strikethrough~~   `code`   ==marked==   ||spoiler||

[Link text](https://example.com)
[Email](mailto:user@example.com)
[Phone](tel:+1234567890)
[Mention user](tg://user?id=123456789)
![custom emoji](tg://emoji?id=5368324170671202286)
![timestamp label](tg://time?unix=1647531900&format=wDT)
$inline LaTeX formula$
$$block LaTeX formula$$

# H1  ## H2  ...  ###### H6

```python
code block with language
```

---   (divider)

- unordered item        1. ordered item
- [ ] task              - [x] done task

> blockquote line

![](https://example.com/photo.jpg)           # photo block
![](https://example.com/photo.jpg "Caption") # with caption
![](https://example.com/video.mp4)           # video block
![](https://example.com/track.mp3)           # audio block
![](https://example.com/note.ogg)            # voice note
![](https://example.com/anim.gif)            # animation

| Col 1 | Col 2 |
|:------|------:|
| left  | right |

Text[^fn1].   [^fn1]: Footnote text.

<details open><summary>**Bold title**</summary>
Content here.
</details>

<tg-collage>
![](https://example.com/a.jpg)
![](https://example.com/b.jpg)
</tg-collage>

<tg-map lat="48.8566" long="2.3522" zoom="14"/>
```

---

## Limits & traps

| Limit | Value |
|---|---|
| Max UTF-8 characters (text, alt-text, formulas) | **32 768** |
| Max blocks (including nested: list items, table rows, blockquote/details blocks) | **500** |
| Max nesting levels | **16** |
| Max media attachments (photos, videos, audio) | **50** |
| Max table columns | **20** |
| Map zoom range | **0–24** |

### Critical constraints

**Choose exactly one content representation.** Use `html`, `markdown`, or `blocks`.

**Markup media has two source paths.**
- Media must be specified as separate blocks, not inline in text.
- Direct HTTP/HTTPS media URLs work without `media`.
- `tg://photo?id=`, `tg://video?id=`, and `tg://audio?id=` require a matching entry in `media`.
- Each bound `InputMedia*.media` accepts `file_id`, HTTP/HTTPS URL, or multipart `attach://`.
- Direct URL media type is inferred from MIME type and URL extension. Bound media type comes
  from the nested `InputMedia*` object.

**Table cells: inline formatting only.**
No blocks (`<p>`, `<ul>`, `<img>`, etc.) inside `<td>` / `<th>`. Only inline tags.

**`RichBlockThinking` is draft-only.**
Can only appear in `sendRichMessageDraft`. Never in `sendRichMessage`. Never stored in a
Message object.

**`sendRichMessageDraft` is private-chat only.**
`chat_id` must be an Integer. `@username` strings are not accepted.

**`editMessageText`: `text` and `rich_message` are mutually exclusive.**
Pass exactly one. Sending both (or neither) is an error.

**Map is static, no markers.**
`RichBlockMap` renders a static tile at the given location and zoom level. No pins,
no interactivity.

**Block count includes nesting.**
The 500-block limit counts every `RichBlockListItem`, every table row, every block inside
`blockquote` / `details`. Deep nesting exhausts the budget fast.

**Collage and slideshow accept both photos and videos.**
`blocks` can mix `photo` and `video` blocks. Both may also be placed inside a `details`
block as collapsible media.

---

## Common mistakes

| Mistake | Fix |
|---|---|
| Passing an array directly as `rich_message` | Wrap it as `{"blocks":[...]}` |
| Using `tg://...id=cover` without `media` | Add an `InputRichMessageMedia` with `id: "cover"` |
| Leaving a bound id that markup no longer references | Drop the binding — an unused one is an editing slip, not a no-op |
| Binding `voice_note` behind `tg://video?id=` | Match the scheme: `photo`→photo, `video`→video/animation, `audio`→audio/voice_note |
| Sending `attach://cover` in JSON only | Switch the request to multipart/form-data and add the `cover` file part |
| Nesting the multipart form fields as JSON objects | Every non-file field is a string: `json.dumps(rich_message)` in one form field |
| Putting the caption in `InputMedia*.caption` of a binding | Captions come from markup — the image title argument or `<figcaption>` |
| Shipping audio bindings without `duration`/`title` | The inline player shows an unlabelled blob; set the metadata on the binding |
| Retrying a `sendRichMessage` that timed out | Outcome is unknown — retrying duplicates the post; resolve it before resending |
| Putting an `InputMedia*` caption inside a direct media block | Put the caption on `InputRichBlockPhoto` / `Video` / `Audio` |
| Putting `<img>` or `<video>` inline in `<p>` | Move media to its own block, outside `<p>` |
| Adding block elements inside `<td>` | Only inline tags inside table cells |
| Using `RichBlockThinking` in `sendRichMessage` | `thinking` is valid only in `sendRichMessageDraft` |
| Calling `sendRichMessageDraft` with `@username` | Use numeric `chat_id` (Integer) |
| Sending `text` and `rich_message` together in `editMessageText` | Pass exactly one |
| Forgetting to call `sendRichMessage` after streaming | Draft expires after 30 s — always finalize with full message |
| Assuming a narrower fixed map zoom range | Outgoing InputRichBlockMap.zoom is optional and ranges **0–24** |
| Using `skip_entity_detection` for manual link formatting | Set it to `true` to prevent double-detection when you already mark up URLs manually |

---

## Full spec

All types, all fields, all format details: [`../../reference/rich-messages-spec.md`](../../reference/rich-messages-spec.md)
