---
name: translate-article
description: Translate MDX articles between English and Japanese for global engineers. Use when the user says "translate this article", "convert to Japanese/English", or asks to localize content in `src/content/docs/`. Auto-detects source language and outputs to the correct i18n path.
---

# Translate Article

Translate MDX articles in `src/content/docs/` between English and Japanese, targeting global engineering audiences.

## Workflow

1. **Detect source language** from the article content
2. **Translate** using guidelines below
3. **Write** to the correct output path

## Path Rules

| Source | Target | Example |
|--------|--------|---------|
| English (root) | Japanese | `tech/foo.mdx` → `ja/tech/foo.mdx` |
| Japanese (`ja/`) | English (root) | `ja/tech/foo.mdx` → `tech/foo.mdx` |

## Translation Guidelines

### Preserve (Do NOT translate)

- Code blocks and inline code
- Technical terms: API, JSON, REST, HTTP, OAuth, JWT, SDK, CLI, etc.
- Product/service names: Firebase, Vercel, GitHub, etc.
- URLs and file paths
- Frontmatter fields: `slug`, `sidebar`, `draft`, `editUrl`

### Translate

- Frontmatter: `title`, `description`
- Prose paragraphs
- Comments explaining code (translate the explanation, not the code)
- Alt text for images

### Style for Global Engineers

**English output:**
- Use simple, direct sentences
- Prefer active voice
- Avoid idioms and cultural references
- Use standard technical terminology

**Japanese output:**
- Use です/ます form
- Keep sentences concise
- Preserve English technical terms in katakana only when commonly used (e.g., クラウド, サーバー)
- Keep original English for terms engineers use as-is (e.g., API, JSON, Firebase)

## Example

**English source** (`tech/auth.mdx`):
```mdx
---
title: Authentication Guide
description: Learn how to implement OAuth 2.0 authentication.
---

# Authentication Guide

This guide explains how to set up OAuth 2.0 in your app.

\`\`\`typescript
const token = await getAccessToken();
\`\`\`
```

**Japanese output** (`ja/tech/auth.mdx`):
```mdx
---
title: 認証ガイド
description: OAuth 2.0 認証の実装方法を解説します。
---

# 認証ガイド

このガイドでは、アプリに OAuth 2.0 を設定する方法を説明します。

\`\`\`typescript
const token = await getAccessToken();
\`\`\`
```
