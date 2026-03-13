---
name: content-rewrite
description: Adapt and rewrite content for different platforms (LinkedIn, X, Reddit, English blog, WeChat). Each platform has its own tone, format, and length requirements.
---

# Content Rewrite

Adapt a piece of source content (article, blog post, announcement, etc.) into platform-specific versions for distribution across social media and content platforms.

## When to Use

Use this skill when the user provides source content and wants it rewritten or adapted for one or more target platforms.

## Confirm Before Writing

Before starting, **always ask the user**:

1. **Perspective / voice** — Should the content use first person ("I", telling a personal story) or third person (stating facts objectively)? This significantly affects tone and credibility on every platform.
2. **Target platforms** — Which platforms to write for? (LinkedIn, X, Reddit, English blog, WeChat, or all)

## Platform References

Each platform has a dedicated style guide under `references/`:

| Platform | Reference | Key Characteristics |
|----------|-----------|-------------------|
| LinkedIn | `references/linkedin.md` | Professional tone, include an image or link, concise |
| X (Twitter) | `references/x.md` | 280-char limit (free users), conversational, punchy |
| Reddit | `references/reddit.md` | Casual and human-like, community-aware, anti-marketing |
| English Blog | `references/blog-en.md` | Slightly professional, structured, SEO-friendly |
| WeChat (公众号) | `references/wechat.md` | Storytelling, emotional hooks, twists and engagement |

## General Guidelines

- **No AI smell** — All platforms require natural, human-sounding writing. Avoid robotic patterns, excessive structure, and formulaic transitions. See the `remove-ai-style` skill for detailed rules.
- **Conversational tone** — Even on professional platforms like LinkedIn, keep the writing approachable. Nobody likes reading corporate speak.
- **Platform-native** — Each version should feel like it was written by someone who actually uses that platform, not cross-posted from a press release.
- **Adapt, don't translate** — Rewriting for a platform means rethinking the content for that audience, not just reformatting the same text.
