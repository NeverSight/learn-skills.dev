---
name: tooyoung:ink-reader
description: "Intelligently read any URL content with auto platform detection and fallback strategies. Supports WeChat, Zhihu, Bilibili, Toutiao, Weibo, Xiaohongshu, Douyin, X/Twitter, and generic websites. Trigger words: read url, read link, read this, fetch url, grab content, ink-reader"
metadata:
  version: "1.0.0"
---

# Ink Reader

Intelligently read any URL content. Auto-detect platform, pick the best fetch strategy, output clean Markdown.

## When to Activate

Activate this skill when the user:

- Shares a URL and asks to read / fetch / view / grab its content
- Says "read this link", "what does this say", "fetch this article"
- Uses `/ink-reader <url>`

## Fetch Strategy Overview

Three-layer fallback, zero configuration required:

```
Layer 1: Jina Reader    → Free, no API key, covers most public content
Layer 2: WebFetch        → Claude Code built-in, direct URL reading
Layer 3: Playwright MCP  → Browser automation, handles login-required sites
```

## Platform Detection

Match the URL domain to determine platform and strategy routing:

| Platform    | Domain Contains           | Needs Login | Strategy Order     |
| ----------- | ------------------------- | ----------- | ------------------ |
| WeChat      | `mp.weixin.qq.com`        | Yes         | Jina → Playwright  |
| Zhihu       | `zhihu.com`               | No          | Jina → WebFetch    |
| Bilibili    | `bilibili.com`, `b23.tv`  | No          | Jina → WebFetch    |
| Toutiao     | `toutiao.com`             | No          | Jina → WebFetch    |
| Weibo       | `weibo.com`, `m.weibo.cn` | Yes         | Jina → Playwright  |
| Xiaohongshu | `xiaohongshu.com`         | Yes         | Jina → Playwright  |
| Douyin      | `douyin.com`              | No          | Jina → WebFetch    |
| X/Twitter   | `x.com`, `twitter.com`    | Partial     | See X/Twitter Flow |
| Generic     | anything else             | No          | Jina → WebFetch    |

### Routing Rules

- **No login required**: Jina → WebFetch → Playwright MCP (if available)
- **Login required** (WeChat, Weibo, Xiaohongshu): Jina → Playwright MCP (skip WebFetch, it won't help)
- **X/Twitter**: Dedicated flow below

## Execution Steps

### Step 1: Identify Platform

Parse the URL domain and match against the platform table above.

### Step 2: Fetch Content

#### For normal platforms (no login needed)

1. **Try Jina Reader**:
   - Use WebFetch with URL: `https://r.jina.ai/{original_url}`
   - Prompt: "Extract the article title, author, publish time, and full body content. Return as-is in Markdown."
   - If result is meaningful (> 100 chars, no verification page), use it.

2. **Try WebFetch direct**:
   - Use WebFetch with the original URL directly.
   - Prompt: "Extract the article title, author, publish time, and full body content."
   - If result is meaningful, use it.

3. **Try Playwright MCP** (if available):
   - Navigate to the original URL.
   - Wait for content to load.
   - Take a snapshot and extract content.
   - If Playwright MCP is not available, skip this step.

#### For login-required platforms (WeChat, Weibo, Xiaohongshu)

1. **Try Jina Reader** (same as above, sometimes works even for login-required sites).

2. **Try Playwright MCP** (if available):
   - Navigate to the original URL.
   - If a verification/login page is detected, inform the user.
   - If Playwright MCP is not available, inform the user:
     > "This platform requires login. Install Playwright MCP to enable browser-based reading."

#### For X/Twitter

1. **Extract status ID** from URL:
   - Pattern: `x.com/{user}/status/{id}` or `twitter.com/{user}/status/{id}`
   - Strip query parameters.

2. **Try Thread Reader App via Jina**:
   - Use WebFetch with URL: `https://r.jina.ai/https://threadreaderapp.com/thread/{status_id}.html`
   - Prompt: "Extract the full thread content including all tweets. Return in Markdown."
   - If result is meaningful (> 100 chars, contains actual thread content), output as thread.

3. **Try Jina on original X URL**:
   - Use WebFetch with URL: `https://r.jina.ai/{original_url}`
   - Prompt: "Extract the tweet content, author, and timestamp."
   - If result is meaningful, output as single post.

4. **Try Playwright MCP** (if available):
   - Navigate to `https://threadreaderapp.com/thread/{status_id}.html`
   - Extract content from the page.

### Step 3: Validate Content

Content is **valid** when ALL of these are true:

- Length > 100 characters after trimming
- Does NOT contain these verification markers: "环境异常", "完成验证", "请完成验证", "access denied", "please verify", "subscribe to continue", "sign in to read", "create a free account"
- Is NOT a login wall or CAPTCHA page

If content fails validation, treat it as a failure and try the next strategy.

### Step 4: Output

Use the output format specified below.

## Output Format

### Success

```markdown
# {Title}

**Source**: {Platform Name}
**Author**: {Author name, omit if unavailable}
**Published**: {Time, omit if unavailable}
**URL**: {Original URL}
**Strategy**: {Jina Reader / WebFetch / Playwright MCP}

---

{Body content in Markdown}
```

Rules:

- Only include Author and Published lines if the information is actually available.
- Do NOT fabricate metadata. If it's not in the fetched content, omit it.
- Keep images as remote URLs. Do NOT attempt to download images.
- Clean up excessive whitespace, navigation elements, ads, and cookie banners from the content.

### Failure

```markdown
# Failed to read URL

**URL**: {url}
**Platform**: {detected platform}
**Attempted strategies**:

- {strategy 1}: {error reason}
- {strategy 2}: {error reason}

**Suggestions**:

- {contextual suggestions}
```

Contextual suggestions by scenario:

- Login-required platform + no Playwright → "Install Playwright MCP to enable browser-based reading for this platform."
- WeChat verification → "WeChat has strict anti-scraping. Try opening the link in a browser and copying the content manually."
- All strategies returned empty → "The page may require JavaScript rendering. Try using Playwright MCP."
- X/Twitter thread failed → "Try opening <https://threadreaderapp.com/thread/{id}.html> in your browser."

## Save Mode

When the user says "save", "save it", "keep this", or "save to file" AFTER a successful read:

1. Create directory `./ink-reader-clips/` in current working directory (if not exists).
2. Write file: `./ink-reader-clips/{YYYY-MM-DD}_{sanitized_title}.md`
3. File content:

```markdown
---
title: "{Title}"
source: "{Platform Name}"
url: "{Original URL}"
saved_at: "{YYYY-MM-DD HH:MM:SS}"
---

{Body content}
```

- Sanitize title for filename: remove `<>:"/\|?*`, replace whitespace with `-`, truncate to 50 chars.
- Report: "Saved to `./ink-reader-clips/{filename}`"

Do NOT auto-save. Only save when explicitly asked.

## Important Notes

- **No Python scripts**: Everything is done through Claude Code's built-in tools.
- **No API keys needed**: Jina Reader is free and keyless.
- **Playwright MCP is optional**: The skill works without it, just with reduced capability for login-required platforms.
- **Images stay remote**: Never download images. Keep original URLs in the Markdown output.
- **Respect content**: Output the content faithfully. Do not summarize or modify unless the user explicitly asks.
