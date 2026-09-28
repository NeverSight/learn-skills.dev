---
name: postlake-media
description: Upload an image or video to PostLake and attach it to a post. Use when a post needs media, or for platforms that require it (Instagram, TikTok, YouTube, Pinterest).
---

# PostLake: upload media

Upload the file first to get a `med_…` id, then pass it as `media` in a publish or
schedule call. Some platforms require media (Instagram, TikTok, YouTube, Pinterest).

## Auth

```
Authorization: Bearer $POSTLAKE_API_KEY
```

Base URL `https://api.postlake.dev`.

## Upload

POST the raw bytes with the file's `Content-Type`. Limits: images ≤20MB
(jpeg/png/webp/gif); videos ≤200MB (mp4/mov/webm).

From a local file:

```bash
curl -X POST https://api.postlake.dev/v1/media \
 -H "Authorization: Bearer $POSTLAKE_API_KEY" \
 -H "Content-Type: image/jpeg" \
 --data-binary @photo.jpg
```

From a URL (download it first, then upload the bytes):

```bash
curl -sL "https://example.com/photo.jpg" -o /tmp/m.jpg
curl -X POST https://api.postlake.dev/v1/media \
 -H "Authorization: Bearer $POSTLAKE_API_KEY" \
 -H "Content-Type: image/jpeg" \
 --data-binary @/tmp/m.jpg
```

Response:

```json
{ "id": "med_47214a…", "url": "https://media.postlake.dev/med_47214a…", "contentType": "image/jpeg", "size": 86487 }
```

## Attach it to a post

Pass the id(s) as `media`, with optional alt text for accessibility:

```bash
curl -X POST https://api.postlake.dev/v1/posts \
 -H "Authorization: Bearer $POSTLAKE_API_KEY" \
 -H "Content-Type: application/json" \
 -H "Idempotency-Key: $(uuidgen)" \
 -d '{
  "text": "New drop 👟",
  "accounts": ["acc_54d8…"],
  "media": ["med_47214a…"],
  "mediaAlt": ["A pair of orange running shoes"]
 }'
```

## Tips

- Set the `Content-Type` to the real file type. It's how PostLake validates the
 upload.
- For video platforms (YouTube/TikTok) upload an mp4 and set a title via
 `platformOptions.youtube.title`.
- Reuse a `med_…` id across multiple posts; you don't need to re-upload.
