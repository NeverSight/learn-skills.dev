---
name: search.images
description: Search image results through the configured self-hosted SearXNG instance for visual references, source images, thumbnails, or image result URLs.
user-invocable: true
disable-model-invocation: false
metadata:
  hybridclaw:
    category: research
    short_description: "SearXNG image search."
    tags:
      - search
      - images
      - searxng
      - research
---
# Search Images

Use this skill when the user asks to search for images, visual references, pictures, thumbnails, screenshots, product photos, logos, diagrams, or image-source URLs.

## Workflow

1. Call `web_search` with:
   - `provider: "searxng"`
   - `categories: "images"`
   - the user's visual search query
   - `count`, `freshness`, `country`, or `language` only when the user asks for them or they are clearly implied.
2. Return the most relevant image results with title, URL, and thumbnail URL when available.
3. Use `web_fetch` only for a result page when the user asks to inspect the source page.

## Constraints

- Do not use hosted image search providers for this skill unless the user explicitly asks to leave the sovereign SearXNG path.
- Do not present thumbnails or result URLs as licensed assets unless licensing is verified from the source page.
- If SearXNG is not configured, say that the self-hosted image search provider is unavailable and include the tool error.
