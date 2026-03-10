---
name: publish-md-to-wechat
description: Automatically format and publish Markdown documents to WeChat Official Account Drafts with professional styles. It handles authentication, style-driven HTML conversion (WeChat native compatible), image uploading, and draft creation.
---

# publish-md-to-wechat

Automatically format and publish Markdown documents to WeChat Official Account Drafts with professional styles.

## Description

Use this skill when you need to publish a Markdown file to a WeChat Official Account. It handles authentication, style-driven HTML conversion (WeChat native compatible), image uploading, and draft creation.

**When to use:**
1. Publishing articles, tutorials, or newsletters from MD to WeChat.
2. Applying professional design styles (Swiss Modern, Terminal) to raw Markdown.
3. Automating the "Copy-Paste-Format" workflow for WeChat.

## Prerequisites

- WeChat **AppID** and **AppSecret** (from mp.weixin.qq.com -> Basic Configuration).
- Server IP must be added to the **IP Whitelist** in WeChat console.
- **Setup Environment**: Run `./install.sh` to initialize the virtual environment and dependencies (`mistune`).

## Usage

### 1. Simple Publish (Swiss Modern Style)

Invoke the publisher using the virtual environment:

```bash
source .venv/bin/activate && python3 scripts/wechat_publisher.py \
  --id YOUR_APP_ID \
  --secret YOUR_APP_SECRET \
  --md path/to/article.md \
  --style swiss
```

### 2. Advanced Features

- **Obsidian Support**: Automatically handles `![[WikiLink]]` image syntax.
- **Image Auto-Upload**: Searches for local images recursively in the project and uploads them to WeChat servers automatically.
- **Robust Rendering**: Powered by `mistune` AST parser for perfect nested lists, tables, and code blocks.

### 2. Available Styles (Adapted from Frontend Slides)

| Style | Vibe | Best For |
| :--- | :--- | :--- |
| `swiss` | Clean, high-contrast, professional | Technical guides, reports |
| `terminal` | Green text on dark, hacker aesthetic | Dev tools, coding tips |
| `bold` | Vibrant cards on dark, high impact | Product launches, announcements |
| `botanical` | Elegant, sophisticated, premium | Artistic pieces, luxury brands |
| `notebook` | Cream paper with mint accents, tactile | Study notes, diaries |
| `cyber` | Futuristic navy with cyan glow | AI, tech, web3 topics |
| `voltage` | Electric blue with neon yellow | Energetic, creative pitches |
| `geometry` | Soft pastels with rounded cards | Friendly, approachable content |
| `editorial` | Witty, personality-driven, serif | Opinions, blogs, personal brands |
| `ink` | Warm cream with crimson, literary | Storytelling, deep dives |
### 3. Automatic Cover Generation

If no cover image is provided, the Agent can use one of these two strategies:

#### Strategy A: Built-in Design Card (Deterministic)
Use the `generate_cover.py` script to create a professional SVG cover:
```bash
python3 scripts/generate_cover.py \
  --title "Your Article Title" \
  --subtitle "Secondary Description" \
  --style swiss
```
*Output: `assets/cover.svg`. Convert to PNG before publishing.*

#### Strategy B: Generative AI (Creative)
The Agent can generate a prompt based on the article's theme and call an external image generation API (like DALL-E 3) to create a custom illustration.

### 4. Strategy for Agents

1. **Check Credentials**: Ensure `WECHAT_APP_ID` and `WECHAT_APP_SECRET` are available.
2. **Cover Handling**: 
   - If a PNG/JPG exists, use it.
   - If not, use **Strategy A** to generate a branded card.
3. **Convert & Upload**:
...
   - The script automatically converts MD to WeChat-compatible HTML using `section` tags and inline CSS.
   - It uploads the provided `--thumb` image to get a `thumb_media_id`.
3. **Draft Creation**: It calls the WeChat Draft Box API and returns the `media_id` on success.

## Troubleshooting

- **IP Whitelist Error**: If you see `errcode: 40164`, copy the IP from the error message and add it to the WeChat Whitelist.
- **Image Size**: Ensure the cover image is under 2MB.
- **SSL Errors**: The script bypasses SSL verification by default to handle environment-specific cert issues.

---
*Created via Skill Creator*
