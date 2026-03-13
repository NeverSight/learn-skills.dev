---
name: x-post
description: Post to X (Twitter) from the command line. Text, images, and video.
argument-hint: "post \"Your tweet text\" [--media /path/to/file]"
allowed-tools: Bash, Read
model: claude-haiku-4-5-20251001
---

Post to X using the CLI tool at `~/.claude/skills/x-post/x-post.py`.

## Setup

Requires Python packages: `pip install xdk requests_oauthlib`

Credentials file at `~/.claude/skills/x-post/x.key` (JSON):
```json
{
  "api_key": "...",
  "api_secret": "...",
  "access_token": "...",
  "access_token_secret": "..."
}
```

## Commands

**Post text:**
```bash
python ~/.claude/skills/x-post/x-post.py post "Your tweet text"
```

**Post with image:**
```bash
python ~/.claude/skills/x-post/x-post.py post "Your tweet text" --media /path/to/image.jpg
```

**Post with video:**
```bash
python ~/.claude/skills/x-post/x-post.py post "Your tweet text" --media /path/to/video.mp4
```

**Check profile:**
```bash
python ~/.claude/skills/x-post/x-post.py me
```

## Rules

- Always show the user the exact tweet text before posting and get confirmation
- Never post without explicit user approval
- Video uploads use chunked upload (INIT/APPEND/FINALIZE) and may take a minute for processing
- The script auto-detects media type from file extension
