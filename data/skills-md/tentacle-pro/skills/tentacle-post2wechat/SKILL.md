---
name: tentacle-post2wechat
description: Enterprise WeChat draft publisher via api.tentacle.pro. Uses API_KEY, server-side credential mapping, token caching/refresh, cover upload, inline image upload, and draft/add.
---

# tentacle-post2wechat (Enterprise Edition)

## Purpose

Enterprise publisher that sends requests to `api.tentacle.pro`.
Server resolves `API_KEY -> AppID/AppSecret`, caches/refreshes WeChat tokens, then forwards to WeChat APIs.

## Runtime

```bash
bun .agents/skills/tentacle-post2wechat/scripts/main.ts <html_file> [options]
```

## Shared .env (`.agents/skills/.env`)

```dotenv
API_KEY=tpk_...
```

## Behavior

1. Force-compress local images before upload (`jpeg`, quality `65`).
2. Upload inline images using enterprise endpoint and replace `<img src>` URLs.
3. Upload cover image as permanent material and obtain `thumb_media_id`.
4. Save to draft box only (`draft/add`).

## Official WeChat API Role Mapping

- Inline article images map to WeChat `media/uploadimg` semantics and return URL for HTML replacement.
- Cover image maps to WeChat permanent material (`material/add_material?type=image`) and returns `media_id`.
- Draft save maps to WeChat `draft/add` (`article_type=news`) with `thumb_media_id` + replaced HTML content.

## Recommended Pipeline

1. **If input is `.md`**: proactively invoke the `tentacle-markdown2html` skill first to convert it to HTML, then continue with the steps below. Do not ask the user to do this manually.
2. Receive normalized HTML (or convert markdown in previous step).
3. Upload inline images and rewrite `<img src>` to returned URLs.
4. Upload cover image and get `thumb_media_id`.
5. Submit `draft/add` payload.

## Required Inputs

- HTML file (auto-generated from `.md` via `tentacle-markdown2html` if needed)
- Cover image (`--cover`) or first inline image fallback

## Example

```bash
bun .agents/skills/tentacle-post2wechat/scripts/main.ts article.html \
  --cover Assets/Cover-Images/topic/cover.jpg \
  --title "标题" \
  --author "作者" \
  --summary "摘要（不超过120字）"
```

## API Contract

See `references/api-contract.md`.
