---
name: x-composer
version: 1.1.0
description: Compose and post to X.com using Chrome CDP automation. Use when user asks to "post to X", "tweet", "draft a tweet", "share on X", or "write a thread". Handles Chrome launch, text input with emoji/unicode support, and multi-paragraph formatting via real browser automation (no API costs, bypasses anti-bot detection).
---

# X Composer

Post to X.com via Chrome DevTools Protocol (CDP). Uses real Chrome to bypass anti-bot detection.

## Prerequisites

- Google Chrome installed
- `chrome-remote-interface` npm package

Install if missing:

```bash
npm install -g chrome-remote-interface
```

## Workflow

Posting to X involves these steps:

1. Launch Chrome with CDP (run `scripts/cdp-launch.js`)
2. Wait for X.com compose page to load (~3s)
3. Type draft text (run `scripts/cdp-type.js`)
4. User reviews and clicks Post manually

## Step 1: Launch Chrome

Run `scripts/cdp-launch.js` with optional URL argument:

```bash
NODE_PATH=$(npm root -g) node scripts/cdp-launch.js
```

| URL | Purpose |
|-----|---------|
| *(default)* | `https://x.com/compose/post` |
| `https://x.com/home` | Open home feed |
| `https://x.com/search?q=QUERY&f=live` | Search posts |

Reuses existing Chrome CDP instance if running. First run requires manual X.com login — session persists in `~/.chrome-cdp-profile`.

Wait ~3 seconds after launch before typing.

## Step 2: Type Draft

Pipe JSON segments to `scripts/cdp-type.js` via stdin:

```bash
echo '[{"text":"Hello world!"}]' | NODE_PATH=$(npm root -g) node scripts/cdp-type.js
```

### Segment Format

| Segment | Effect |
|---------|--------|
| `{"text": "string"}` | Insert text (emoji/unicode safe) |
| `{"enter": true}` | Single line break |
| `{"enter": 2}` | Multiple line breaks |

### Example: Multi-paragraph post

```bash
cat << 'EOF' | NODE_PATH=$(npm root -g) node scripts/cdp-type.js
[
  {"text": "Hook line with emoji"},
  {"enter": 2},
  {"text": "Main content paragraph."},
  {"enter": 2},
  {"text": "- Point one"},
  {"enter": true},
  {"text": "- Point two"},
  {"enter": 2},
  {"text": "https://example.com"},
  {"enter": true},
  {"text": "#hashtag #tags"}
]
EOF
```

## Step 3: User Posts

Draft is entered in browser. User reviews and clicks "Post" manually. Never auto-post.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Chrome not connecting | `pkill -f "Chrome.*remote-debugging"` then relaunch |
| No X.com tab found | Launch Chrome first, wait 3s |
| Text not typing | Click compose box in browser first |
| Module not found | `npm install -g chrome-remote-interface` |
| Login required | Use default profile path (`~/.chrome-cdp-profile`), login once |

## Notes

- `NODE_PATH=$(npm root -g)` resolves globally installed `chrome-remote-interface`
- `Input.insertText()` handles emoji/unicode reliably (not character-by-character)
- Fixed `--user-data-dir` preserves login across Chrome restarts
- If text appears scrambled, restart Chrome and retry
