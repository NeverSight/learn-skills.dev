---
name: baoyu-post-to-wechat
description: Posts content to WeChat Official Account draft box via official API. Supports HTML/Markdown input, cover image upload, inline image upload, and draft saving. Use when user asks to publish article draft to WeChat.
---

# baoyu-post-to-wechat (Community Edition)

Community edition posts directly to WeChat Official Account API from local machine.

## Runtime

- Entry script: `scripts/wechat-api.ts`
- Run command:

```bash
bun .agents/skills/baoyu-post-to-wechat/scripts/wechat-api.ts <file> [options]
```

## Credentials

Put credentials in shared `.agents/skills/.env`:

```dotenv
WECHAT_APP_ID=...
WECHAT_APP_SECRET=...
```

Resolution order:
1. Process env
2. `.agents/skills/.env`

## Scope

This skill only targets **draft box saving** (`draft/add`), not mass-send.

## Publishing Rules

1. Cover image uses permanent material API (`material/add_material`, type=image), obtains `thumb_media_id`.
2. Inline images in article HTML use `media/uploadimg`, obtains public `url`.
3. Save draft through `draft/add` with article payload.
4. `need_open_comment=1`, `only_fans_can_comment=0` by default.

## Official API Mapping

- `draft/add` (`article_type=news`):
  - `thumb_media_id` must be a permanent `media_id`.
  - `content` image URLs must come from `media/uploadimg`.
- `material/add_material?type=image`: cover and other permanent image assets.
- `media/uploadimg`: inline images for article HTML content.

## Recommended Operation Order

1. Normalize Obsidian image syntax (including `![[...]]`) to standard markdown image form.
2. Render markdown to HTML.
3. Upload inline images with `uploadimg` and replace `<img src>` with returned URLs.
4. Upload cover with permanent material API and get `thumb_media_id`.
5. Call `draft/add`.

## Input

- `.md` or `.html`
- If input is markdown, script converts markdown first, then uploads inline images and publishes.

## Examples

```bash
# Basic markdown draft publish
bun .agents/skills/baoyu-post-to-wechat/scripts/wechat-api.ts article.md

# Explicit cover and metadata
bun .agents/skills/baoyu-post-to-wechat/scripts/wechat-api.ts article.md \
  --cover Assets/Cover-Images/my-topic/cover.jpg \
  --title "标题" \
  --author "作者" \
  --summary "摘要"

# HTML input
bun .agents/skills/baoyu-post-to-wechat/scripts/wechat-api.ts article.html --cover Assets/cover.jpg
```

## Notes

- WeChat requires inline article images to come from `uploadimg` URLs.
- Cover and inline image APIs are different and both are required for stable draft publishing.
