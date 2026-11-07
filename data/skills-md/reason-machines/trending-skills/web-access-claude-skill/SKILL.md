---
name: web-access-claude-skill
description: Give Claude Code full internet access with three-layer channel dispatch, CDP browser automation, and parallel sub-agent task splitting
triggers:
  - give claude code internet access
  - install web access skill for claude
  - browse the web with claude code
  - automate chrome browser with claude
  - parallel web research with claude agents
  - fetch and scrape web pages in claude code
  - use CDP browser automation in claude
  - help me search and browse websites with claude
---

# Web Access Skill for Claude Code

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A skill that gives Claude Code complete internet access using three-layer channel dispatch (WebSearch / WebFetch / CDP), Chrome DevTools Protocol browser automation via a local proxy, parallel sub-agent task splitting, and cross-session site experience accumulation.

## What This Project Does

Claude Code ships with `WebSearch` and `WebFetch` but lacks:
- **Dispatch strategy** — knowing *when* to use which tool
- **Browser automation** — clicking, scrolling, file upload, dynamic pages
- **Accumulated site knowledge** — domain-specific patterns reused across sessions

Web Access fills all three gaps with:

| Capability | Detail |
|---|---|
| Auto tool selection | WebSearch / WebFetch / curl / Jina / CDP chosen per scenario |
| CDP Proxy | Connects directly to your running Chrome, inherits login state |
| Three click modes | `/click` (JS), `/clickAt` (real mouse events), `/setFiles` (upload) |
| Parallel dispatch | Multiple targets → sub-agents share one Proxy, tab-isolated |
| Site experience store | Per-domain URL patterns, quirks, traps — persisted across sessions |
| Media extraction | Pull image/video URLs from DOM, screenshot any video frame |

## Installation

**Option A — Let Claude install it:**
```
帮我安装这个 skill：https://github.com/eze-is/web-access
```
or in English:
```
Install this skill for me: https://github.com/eze-is/web-access
```

**Option B — Manual:**
```bash
git clone https://github.com/eze-is/web-access ~/.claude/skills/web-access
```

The skill file is `~/.claude/skills/web-access/SKILL.md`. Claude Code loads all `SKILL.md` files under `~/.claude/skills/` automatically.

## Prerequisites

### Node.js 22+
```bash
node --version   # must be >= 22
```

### Enable Chrome Remote Debugging
1. Open `chrome://inspect/#remote-debugging` in your Chrome
2. Check **Allow remote debugging for this browser instance**
3. Restart Chrome if prompted

### Verify Dependencies
```bash
bash ~/.claude/skills/web-access/scripts/check-deps.sh
```

Expected output:
```
✅ Node.js 22.x found
✅ Chrome DevTools reachable at localhost:9222
✅ curl available
```

## CDP Proxy — Core Component

The proxy is a lightweight Node.js WebSocket bridge between Claude and your Chrome instance.

### Start the Proxy
```bash
# Start in background (auto-exits after 20 min idle)
node ~/.claude/skills/web-access/scripts/cdp-proxy.mjs &

# Confirm it's running
curl -s http://localhost:3456/ping
# → {"status":"ok"}
```

### Full HTTP API Reference

```bash
# ── Tab management ──────────────────────────────────────────
# Open new tab, returns tab ID
curl -s "http://localhost:3456/new?url=https://example.com"
# → {"targetId":"ABC123","url":"https://example.com"}

# Close a tab
curl -s "http://localhost:3456/close?target=ABC123"
# → {"closed":true}

# ── Page content ────────────────────────────────────────────
# Execute JavaScript, returns result
curl -s -X POST "http://localhost:3456/eval?target=ABC123" \
  -d 'document.title'
# → {"result":"Example Domain"}

# Get full page HTML
curl -s -X POST "http://localhost:3456/eval?target=ABC123" \
  -d 'document.documentElement.outerHTML'

# ── Interaction ─────────────────────────────────────────────
# JS click (fast, works for most buttons)
curl -s -X POST "http://localhost:3456/click?target=ABC123" \
  -d 'button.submit'

# Real mouse click via CDP (use for upload triggers, canvas elements)
curl -s -X POST "http://localhost:3456/clickAt?target=ABC123" \
  -d '.upload-btn'

# File upload via input element
curl -s -X POST "http://localhost:3456/setFiles?target=ABC123" \
  -H "Content-Type: application/json" \
  -d '{"selector":"input[type=file]","files":["/tmp/photo.png"]}'

# ── Navigation ──────────────────────────────────────────────
# Scroll to bottom
curl -s "http://localhost:3456/scroll?target=ABC123&direction=bottom"

# Scroll to top
curl -s "http://localhost:3456/scroll?target=ABC123&direction=top"

# ── Visual ──────────────────────────────────────────────────
# Screenshot to file
curl -s "http://localhost:3456/screenshot?target=ABC123&file=/tmp/shot.png"

# Screenshot returned as base64
curl -s "http://localhost:3456/screenshot?target=ABC123"
# → {"base64":"iVBORw0KGgo..."}
```

## Three-Layer Channel Dispatch

The skill teaches Claude to pick the right tool automatically:

```
Task type                  → Tool choice
─────────────────────────────────────────
General search query       → WebSearch
Static page / docs / API   → WebFetch or Jina
Login-gated / dynamic page → CDP Proxy
Heavy JS / SPA             → CDP Proxy
Video / canvas interaction → CDP Proxy (clickAt)
Bulk text extraction       → Jina (token-efficient)
Raw HTTP / custom headers  → curl
```

### Jina Usage (Token-Efficient Reads)
```bash
# Jina converts any URL to clean markdown — great for docs/articles
curl -s "https://r.jina.ai/https://docs.example.com/api"
```

## Code Examples

### Example 1: Open a Page and Extract Data

```javascript
// Claude runs this flow via CDP Proxy

// 1. Open tab
const tabRes = await fetch('http://localhost:3456/new?url=https://news.ycombinator.com');
const { targetId } = await tabRes.json();

// 2. Wait for load, then extract top story titles
const evalRes = await fetch(`http://localhost:3456/eval?target=${targetId}`, {
  method: 'POST',
  body: `
    Array.from(document.querySelectorAll('.titleline > a'))
      .slice(0, 10)
      .map(a => ({ title: a.textContent, href: a.href }))
  `
});
const { result } = await evalRes.json();
console.log(JSON.parse(result));

// 3. Clean up
await fetch(`http://localhost:3456/close?target=${targetId}`);
```

### Example 2: Login-Gated Page (Uses Existing Chrome Session)

```javascript
// Chrome already has the user logged in — CDP inherits cookies automatically

async function scrapeAuthenticatedPage(url) {
  // Open tab in the user's real Chrome — no login needed
  const { targetId } = await fetch(`http://localhost:3456/new?url=${url}`)
    .then(r => r.json());

  // Wait for dynamic content
  await fetch(`http://localhost:3456/eval?target=${targetId}`, {
    method: 'POST',
    body: `new Promise(r => setTimeout(r, 2000))`
  });

  // Extract content
  const { result } = await fetch(`http://localhost:3456/eval?target=${targetId}`, {
    method: 'POST',
    body: `document.querySelector('.main-content')?.innerText`
  }).then(r => r.json());

  await fetch(`http://localhost:3456/close?target=${targetId}`);
  return result;
}
```

### Example 3: File Upload Automation

```javascript
async function uploadFile(pageUrl, filePath) {
  const { targetId } = await fetch(`http://localhost:3456/new?url=${pageUrl}`)
    .then(r => r.json());

  // Wait for page
  await new Promise(r => setTimeout(r, 1500));

  // Click the upload trigger button (real mouse event — required for some SPAs)
  await fetch(`http://localhost:3456/clickAt?target=${targetId}`, {
    method: 'POST',
    body: '.upload-trigger-button'
  });

  await new Promise(r => setTimeout(r, 500));

  // Set file on the (possibly hidden) input
  await fetch(`http://localhost:3456/setFiles?target=${targetId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      selector: 'input[type=file]',
      files: [filePath]
    })
  });

  // Submit
  await fetch(`http://localhost:3456/click?target=${targetId}`, {
    method: 'POST',
    body: 'button[type=submit]'
  });

  // Screenshot to verify
  await fetch(`http://localhost:3456/screenshot?target=${targetId}&file=/tmp/upload-result.png`);

  await fetch(`http://localhost:3456/close?target=${targetId}`);
}
```

### Example 4: Parallel Research with Sub-Agents

```javascript
// Instruct Claude to dispatch parallel sub-agents like this:

const targets = [
  'https://product-a.com',
  'https://product-b.com',
  'https://product-c.com',
  'https://product-d.com',
  'https://product-e.com'
];

// Each sub-agent opens its own tab (tab-isolated, same Proxy)
const results = await Promise.all(
  targets.map(async (url) => {
    const { targetId } = await fetch(`http://localhost:3456/new?url=${url}`)
      .then(r => r.json());

    await new Promise(r => setTimeout(r, 2000));

    const { result } = await fetch(`http://localhost:3456/eval?target=${targetId}`, {
      method: 'POST',
      body: `({
        title: document.title,
        description: document.querySelector('meta[name=description]')?.content,
        h1: document.querySelector('h1')?.textContent,
        pricing: document.querySelector('[class*="pric"]')?.innerText?.slice(0,200)
      })`
    }).then(r => r.json());

    await fetch(`http://localhost:3456/close?target=${targetId}`);
    return { url, data: JSON.parse(result) };
  })
);

console.table(results);
```

### Example 5: Video Frame Screenshot

```javascript
async function screenshotVideoAt(pageUrl, timestampSeconds) {
  const { targetId } = await fetch(`http://localhost:3456/new?url=${pageUrl}`)
    .then(r => r.json());

  await new Promise(r => setTimeout(r, 3000));

  // Seek video to timestamp
  await fetch(`http://localhost:3456/eval?target=${targetId}`, {
    method: 'POST',
    body: `
      const v = document.querySelector('video');
      v.currentTime = ${timestampSeconds};
      v.pause();
    `
  });

  await new Promise(r => setTimeout(r, 500));

  // Capture the frame
  await fetch(`http://localhost:3456/screenshot?target=${targetId}&file=/tmp/frame-${timestampSeconds}s.png`);

  await fetch(`http://localhost:3456/close?target=${targetId}`);
}
```

## Common Patterns

### Pattern: Check Proxy Before CDP Tasks
```bash
# Always verify proxy is up before a CDP workflow
curl -s http://localhost:3456/ping || \
  node ~/.claude/skills/web-access/scripts/cdp-proxy.mjs &
```

### Pattern: Use Jina for Documentation
```bash
# Cheaper and cleaner than WebFetch for text-heavy pages
curl -s "https://r.jina.ai/https://api.anthropic.com/docs"
```

### Pattern: Prefer WebSearch for Discovery, CDP for Execution
```
1. WebSearch  → find the right URLs
2. WebFetch   → read static/public content
3. CDP        → interact, authenticate, dynamic content
```

### Pattern: Extract All Media URLs
```javascript
// Get all images and videos on current page
const media = await fetch(`http://localhost:3456/eval?target=${targetId}`, {
  method: 'POST',
  body: `({
    images: Array.from(document.images).map(i => i.src),
    videos: Array.from(document.querySelectorAll('video source, video[src]'))
               .map(v => v.src || v.getAttribute('src'))
  })`
}).then(r => r.json());
```

## Troubleshooting

### Proxy won't start
```bash
# Check if port 3456 is already in use
lsof -i :3456

# Kill existing proxy
kill $(lsof -ti :3456)

# Restart
node ~/.claude/skills/web-access/scripts/cdp-proxy.mjs &
```

### Chrome not reachable
```bash
# Verify Chrome remote debugging is on
curl -s http://localhost:9222/json/version
# Should return Chrome version JSON

# If empty — go to chrome://inspect/#remote-debugging and enable it
```

### `/clickAt` has no effect
- The element may need scrolling into view first:
```bash
curl -s -X POST "http://localhost:3456/eval?target=ID" \
  -d 'document.querySelector(".btn").scrollIntoView()'
```
- Then retry `/clickAt`

### Page content is empty / JS not rendered
```bash
# Add a wait after /new before /eval
curl -s -X POST "http://localhost:3456/eval?target=ID" \
  -d 'new Promise(r => setTimeout(r, 3000))'
# Then fetch content
```

### File upload input not found
Some SPAs render `<input type=file>` only after the trigger click. Always:
1. `/clickAt` the visible upload button first
2. Wait 500ms
3. Then `/setFiles`

### Sub-agent tabs interfering
Each sub-agent should store its own `targetId` and never share it. The Proxy is stateless per-tab.

## Proxy Auto-Shutdown

The proxy exits automatically after **20 minutes of no requests**. For long-running tasks:
```bash
# Keep-alive ping in background
while true; do curl -s http://localhost:3456/ping > /dev/null; sleep 300; done &
```

## Site Experience Store

The skill accumulates domain knowledge in a local JSON store. When Claude visits `twitter.com`, it reads any saved notes about:
- Known working URL patterns
- Login flow quirks  
- Selectors that are stable vs dynamic
- Rate limiting behavior

This persists across Claude sessions. The store lives at:
```
~/.claude/skills/web-access/data/site-experience.json
```

You can inspect or edit it manually to add your own domain knowledge.

## Project Structure

```
~/.claude/skills/web-access/
├── SKILL.md                    ← This skill file (loaded by Claude)
├── scripts/
│   ├── cdp-proxy.mjs          ← CDP Proxy server (Node.js 22+)
│   └── check-deps.sh          ← Dependency checker
└── data/
    └── site-experience.json   ← Accumulated domain knowledge
```

## Capability Summary for Task Routing

| User says | Claude should use |
|---|---|
| "Search for X" | WebSearch |
| "Read this URL" | WebFetch or Jina |
| "Go to my dashboard on X" | CDP (login state) |
| "Click the submit button on X" | CDP `/click` or `/clickAt` |
| "Upload this file to X" | CDP `/setFiles` |
| "Research these 5 products" | Parallel sub-agents via CDP |
| "Extract images from X" | CDP `/eval` + DOM query |
| "Screenshot X at 1:23 in the video" | CDP `/eval` seek + `/screenshot` |
