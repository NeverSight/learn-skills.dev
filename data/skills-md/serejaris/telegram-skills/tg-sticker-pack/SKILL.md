---
name: tg-sticker-pack
description: "Use when making static Telegram stickers or a sticker pack from a meme frame, photo or video: cut the person out, put a caption on top (WordArt, Impact, label tags), check the 512 px PNG/WEBP format offline, and publish the set from a user account through @Stickers or from a bot through createNewStickerSet / addStickerToSet."
license: MIT
---

# tg-sticker-pack

Checked against the official docs on 2026-11-11: [Stickers](https://core.telegram.org/stickers) and Bot API 10.4 (`uploadStickerFile`, `createNewStickerSet`, `addStickerToSet`, `InputSticker`). The @Stickers dialog was run end to end the same day from a user account with Telethon 1.45.

## Format

| What | Rule |
|---|---|
| File | `.PNG` or `.WEBP` |
| Size | one side exactly 512 px, the other 512 px or less |
| Background | transparent; Telegram's tip is a white stroke and a black shadow |
| Bytes | keep under 512 KB: the long-standing static limit (the current Stickers page states no byte limit) |
| Set | up to 120 stickers; `createNewStickerSet` takes 1–50 initial ones |
| Emoji | 1–20 per sticker (`emoji_list`) |

`scripts/check_sticker.py files a.webp b.png` checks size, format, alpha and bytes offline (stdlib only); `scripts/check_sticker.py name <short_name> [--bot <bot_username>]` checks a set name. Exit code 1 means an error.

## Make

Scripts need Pillow, `cut.py` also rembg: `uv run --with pillow --with 'rembg[cpu]' python scripts/cut.py …`.

1. **Frame.** Download the video into an empty folder, pick the frame from a contact sheet: `ffmpeg -i v.webm -vf "fps=1,scale=320:-1,tile=7x10" -frames:v 1 contact.jpg` (the frame at second `7·row + column`), then `ffmpeg -ss <t> -i v.webm -frames:v 1 frame.png`.
2. **Cutout.** `cut.py frame.png cut.webp --box x0,y0,x1,y1`. The default `birefnet-portrait` model keeps dark clothes and a hand-held microphone; `isnet-general-use` and `u2net_human_seg` dropped a black top on the same frame. Check the `-green.jpg` preview it writes.
3. **Sticker.** `sticker.py make --cut cut.webp --top "it depends on" --word REASONING --style wordart-chrome --out out --name reasoning`. Styles: `wordart-chrome` (gradient chrome, wave, perspective, 3D extrusion), `wordart-rainbow` (rainbow, arch), `pink`, `impact` (white with black stroke), `tags` (white and yellow label tags). The caption sits above the head; `--outline N` adds a white stroke of N px around the figure. `--font` takes any heavy font that covers your alphabet.
4. **Review.** Open `<name>-dark.png`: the sticker on a dark chat background. Caption readable, letters clear of each other, face uncovered. Compare variants with `sticker.py sheet a.png b.png --out sheet.png`.

## Publish

### From a user account: @Stickers

The owner is the account that talks to @Stickers; the short name needs no bot suffix. Read the bot's reply after every message and follow its text.

| New set | Add to a set |
|---|---|
| `/newpack` → title | `/addsticker` → choose the set |
| sticker file → emoji | sticker file → emoji |
| next file → emoji … | `/done` |
| `/publish` → `/skip` (icon) → short name | |

Send the sticker as a file. With Telethon, a `.webp` path goes out as a document, which is what the bot asks for; a `.png` path goes out as a compressed photo unless you pass `force_document=True`. The reply with `t.me/addstickers/<short_name>` means the set is live.

### From a bot: Bot API

The set belongs to a user (`user_id`), the bot can edit it later.

```json
POST /bot<TOKEN>/createNewStickerSet
{
  "user_id": 123456789,
  "name": "memes_by_mybot",
  "title": "memes",
  "stickers": [
    {"sticker": "attach://s1", "format": "static", "emoji_list": ["🤔"]}
  ]
}
```

- `name`: English letters, digits and underscores, starts with a letter, no `__`, ends in `_by_<bot_username>` (case-insensitive), 1–64 characters. `title`: 1–64 characters.
- Upload with multipart (`attach://s1`), a URL, or a `file_id` from `uploadStickerFile(user_id, sticker, sticker_format="static")`.
- More stickers: `addStickerToSet(user_id, name, sticker)`; the same sticker twice leaves the set unchanged.

## Done

The set link `https://t.me/addstickers/<short_name>` returns a page whose `og:title` names the set, and every file passed `check_sticker.py files`.
