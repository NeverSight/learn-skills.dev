---
name: agent-reach
description: Read-only access to internet platforms (Twitter/X, Reddit, YouTube subtitles, GitHub, LinkedIn, Bilibili, web). Use when the agent needs to search, read web links, retrieve social discussions, CVE/vulnerability intel, or when standard web search/fetch is blocked or insufficient.
---

# Agent Reach

Give your AI agent eyes to see the entire internet. Read & search Twitter/X, Reddit, YouTube, GitHub, LinkedIn, Bilibili, and login-walled web platforms with one CLI and zero API fees.

## Overview
One command for every platform: `agent-reach`. Read-only; returns structured JSON output.

```bash
agent-reach channels                  # List available channels, actions, and parameters
agent-reach <channel> <action> [args] # e.g. agent-reach github search "vulnerability scanner"
agent-reach read <url>                # Automatically select channel and read any URL
```

---

## 🔌 Supported Channels

| Tier | Channel | Capabilities | Source / Upstream Tools |
| :--- | :--- | :--- | :--- |
| **Default** | `web` | General webpage reading, content extraction, search fallback | Jina Reader, Exa |
| **Default** | `youtube` | Video transcripts, subtitles, audio speech-to-text | yt-dlp, whisper |
| **Default** | `github` | Repositories, files, issues, commit logs, pull requests | GitHub public APIs |
| **Default** | `bilibili` | Video details, subtitles, Danmaku comments | bili-cli, public endpoints |
| **Default** | `v2ex` | Topic reading, community discussions | V2EX public feeds |
| **Optional** | `reddit` | Subreddit search, threads, comment trees | Reddit json/RSS |
| **Optional** | `linkedin` | Posts, company profiles, job postings | OpenCLI / CloakBrowser |
| **Optional** | `twitter` / `x` | Tweets, search, user profiles | OpenCLI / CloakBrowser |
| **Optional** | `xiaohongshu`| Note descriptions, tags, comments | CloakBrowser session |
| **Optional** | `boss` | Developer job listings, skill demands | boss-agent-cli |
| **Optional** | `xueqiu` | Stock quotes, financial sentiment | Xueqiu public endpoints |
| **Optional** | `xiaoyuzhou` | Podcast transcripts, summaries | Groq Whisper API |

---

## ⚡ Integration with REA (Reverse Engineer Anything)

When combined with the REA suite:
1. **Threat & Vulnerability Research:** When auditing a website or binary with REA, use Agent Reach to instantly look up CVEs, GitHub discussions, and security advisories without leaving your terminal:
   ```bash
   agent-reach github search "package-name vulnerability CVE"
   agent-reach reddit search "framework-name security breach"
   ```
2. **Deep Web Reading:** When a website or API blocks standard curl/fetch with Cloudflare or bot protection, use:
   ```bash
   agent-reach read https://target-app.com/docs
   ```
3. **Tutorial & Exploit Video Transcripts:** Extract technical explanations directly from YouTube or Bilibili video transcripts without watching the video:
   ```bash
   agent-reach youtube read "https://www.youtube.com/watch?v=..."
   ```

---

## 🚀 Setup & Installation

Install Agent Reach with `uv` (recommended):
```bash
uv tool install https://github.com/Panniantong/Agent-Reach/archive/refs/tags/v1.6.0.zip
agent-reach setup
```

To manage channels and dependencies:
```bash
agent-reach add <channel>      # Install dependencies for an optional channel
agent-reach remove <channel>   # Remove an unused channel
agent-reach doctor --text      # Check system dependencies and browser status
agent-reach check <channel>    # Verify connectivity for a specific channel
agent-reach update             # Upgrade Agent Reach and installed channel tools
```

---

## 📊 Result Structure & Error Handling

Outputs are standard JSON with `{ ok, channel, action, backend, items, meta, error }`:
- **`ok: true`:** Results found in `items` (`title`, `url`, `author`, `published_at`, `text`, `raw`).
- **`ok: false`:** Examine `error.code`:

| error.code | Meaning | Action to Take |
| :--- | :--- | :--- |
| `NEED_SETUP` | Dependency missing | Run `agent-reach add <channel>`. If key is needed, user runs `agent-reach configure <key>` |
| `NEED_LOGIN` | Site requires login | User runs `agent-reach login <channel>` in their own window. (Never log in for them) |
| `UPSTREAM_BROKEN` | Platform changed layout | Inform user; run `agent-reach update` if agreed |
| `TIMEOUT` | Request timed out | Run `agent-reach doctor --text`; do not retry in an aggressive loop |
| `RATE_LIMITED` | Platform rate limit | Wait `retry_after_seconds` specified in meta |
| `PLATFORM_BLOCKED`| Captcha / Cloudflare wall | User opens official page to solve captcha |
| `NOT_FOUND` | Content nonexistent | Check target URL or keyword |

---

## 🛡️ Security & Red Lines

- **Read-Only:** Agent Reach never posts, comments, likes, or sends messages.
- **Credential Safety:** Never logs in for the user; never asks for, captures, or logs passwords.
- **Dedicated Profile:** Browser sessions run inside an isolated profile under `~/.agent-reach/browser/profile` and shut down after 10 idle minutes.
