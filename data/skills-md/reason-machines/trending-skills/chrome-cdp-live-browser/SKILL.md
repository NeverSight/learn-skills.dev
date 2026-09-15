---
name: chrome-cdp-live-browser
description: Give AI agents access to your live Chrome session via CDP — interact with open tabs, logged-in accounts, and current page state
triggers:
  - "control my chrome browser"
  - "interact with open chrome tabs"
  - "automate my live browser session"
  - "take a screenshot of a webpage"
  - "click elements on a webpage"
  - "read content from a browser tab"
  - "navigate to a URL in chrome"
  - "use chrome devtools protocol"
---

# chrome-cdp: Live Chrome Session for AI Agents

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

`chrome-cdp` connects your AI agent directly to your running Chrome browser via the Chrome DevTools Protocol (CDP). Unlike browser automation tools that spin up fresh isolated browsers, this connects to tabs you already have open — with your logins, cookies, and current page state intact.

## What It Does

- **Live session access** — reads and interacts with tabs you're already logged into
- **Persistent daemon** — one WebSocket daemon per tab; the "Allow debugging" modal appears once, not on every command
- **No npm install** — only Node.js 22+ required
- **100+ tab support** — handles large numbers of open tabs reliably
- **Cross-origin iframe support** — `type` command works even inside cross-origin iframes

## Installation

### As a pi skill

```bash
pi install git:github.com/pasky/chrome-cdp-skill@v1.0.1
```

### Manual (for Amp, Claude Code, Cursor, Codex, etc.)

```bash
git clone https://github.com/pasky/chrome-cdp-skill
# Copy the skills/chrome-cdp/ directory to wherever your agent loads context from
```

### Enable Remote Debugging in Chrome

1. Open Chrome and navigate to: `chrome://inspect/#remote-debugging`
2. Toggle the **"Enable remote debugging"** switch

That's all. No flags, no relaunching Chrome.

The script auto-detects Chrome, Chromium, Brave, Edge, and Vivaldi on macOS, Linux, and Windows. For non-standard installs:

```bash
export CDP_PORT_FILE=/path/to/DevToolsActivePort
```

## Key Commands

All commands use `scripts/cdp.mjs` as the entry point. `<target>` is a unique prefix of the targetId shown by `list`.

### List Open Tabs

```bash
node scripts/cdp.mjs list
# Output:
# A1B2C3  https://github.com/pasky/chrome-cdp-skill  chrome-cdp-skill
# D4E5F6  https://mail.google.com/mail/u/0/           Gmail
```

### Screenshot a Tab

```bash
node scripts/cdp.mjs shot A1B2
# Saves screenshot to runtime dir, prints the file path
```

### Accessibility Tree (Semantic Snapshot)

```bash
node scripts/cdp.mjs snap A1B2
# Returns compact, semantic accessibility tree — best for understanding page structure
```

### Full HTML or Scoped HTML

```bash
node scripts/cdp.mjs html A1B2                    # full page HTML
node scripts/cdp.mjs html A1B2 ".main-content"    # scoped to CSS selector
node scripts/cdp.mjs html A1B2 "#article-body"    # scoped to ID
```

### Evaluate JavaScript

```bash
node scripts/cdp.mjs eval A1B2 "document.title"
node scripts/cdp.mjs eval A1B2 "window.location.href"
node scripts/cdp.mjs eval A1B2 "document.querySelectorAll('a').length"
```

### Navigate to URL

```bash
node scripts/cdp.mjs nav A1B2 https://example.com
# Navigates and waits for page load
```

### Network Resource Timing

```bash
node scripts/cdp.mjs net A1B2
# Shows network resource timing for the current page
```

### Click an Element

```bash
node scripts/cdp.mjs click A1B2 "button.submit"
node scripts/cdp.mjs click A1B2 "#login-btn"
node scripts/cdp.mjs click A1B2 "[data-testid='confirm']"
```

### Click at Coordinates

```bash
node scripts/cdp.mjs clickxy A1B2 320 480
# Clicks at CSS pixel coordinates (x=320, y=480)
```

### Type Text

```bash
node scripts/cdp.mjs type A1B2 "Hello, world!"
# Types at the currently focused element — works in cross-origin iframes
```

### Load More (Click Until Gone)

```bash
node scripts/cdp.mjs loadall A1B2 "button.load-more"
# Keeps clicking the selector until it disappears from the DOM
```

### Open a New Tab

```bash
node scripts/cdp.mjs open
node scripts/cdp.mjs open https://example.com
# Note: triggers Chrome's "Allow" prompt
```

### Stop Daemons

```bash
node scripts/cdp.mjs stop          # stop all daemons
node scripts/cdp.mjs stop A1B2     # stop daemon for specific tab
```

### Raw CDP Command Passthrough

```bash
node scripts/cdp.mjs evalraw A1B2 "Page.getFrameTree"
node scripts/cdp.mjs evalraw A1B2 "Runtime.evaluate" '{"expression":"1+1"}'
```

## Common Patterns

### Pattern: Read a Page You're Logged Into

```bash
# List tabs to find your target
node scripts/cdp.mjs list

# Grab the accessibility tree for a semantic view
node scripts/cdp.mjs snap D4E5

# Or get scoped HTML for a specific section
node scripts/cdp.mjs html D4E5 ".email-list"
```

### Pattern: Fill and Submit a Form

```bash
# Click the input field
node scripts/cdp.mjs click A1B2 "input[name='search']"

# Type into it
node scripts/cdp.mjs type A1B2 "my search query"

# Click submit
node scripts/cdp.mjs click A1B2 "button[type='submit']"

# Take a screenshot to verify result
node scripts/cdp.mjs shot A1B2
```

### Pattern: Extract Data with JavaScript

```bash
# Get all link hrefs on a page
node scripts/cdp.mjs eval A1B2 "Array.from(document.querySelectorAll('a')).map(a => a.href)"

# Get text content of a specific element
node scripts/cdp.mjs eval A1B2 "document.querySelector('.price').textContent.trim()"

# Get table data as JSON
node scripts/cdp.mjs eval A1B2 "
  Array.from(document.querySelectorAll('table tr')).map(row =>
    Array.from(row.querySelectorAll('td,th')).map(cell => cell.textContent.trim())
  )
"
```

### Pattern: Navigate and Wait

```bash
# Navigate and then immediately read the page
node scripts/cdp.mjs nav A1B2 https://news.ycombinator.com
node scripts/cdp.mjs snap A1B2
```

### Pattern: Paginated Content

```bash
# Keep loading content until "Load More" button disappears
node scripts/cdp.mjs loadall A1B2 "button[data-action='load-more']"

# Then extract all loaded content
node scripts/cdp.mjs eval A1B2 "document.querySelectorAll('.item').length"
```

### Pattern: Script Integration (Node.js)

```javascript
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

const exec = promisify(execFile);
const CDP = (...args) => exec('node', ['scripts/cdp.mjs', ...args]);

async function getPageTitle(tabPrefix) {
  const { stdout } = await CDP('eval', tabPrefix, 'document.title');
  return stdout.trim();
}

async function takeScreenshot(tabPrefix) {
  const { stdout } = await CDP('shot', tabPrefix);
  return stdout.trim(); // returns file path
}

async function navigateAndSnap(tabPrefix, url) {
  await CDP('nav', tabPrefix, url);
  const { stdout } = await CDP('snap', tabPrefix);
  return stdout;
}

// Usage
const tabs = (await CDP('list')).stdout;
console.log(tabs);
```

## Configuration

| Environment Variable | Purpose |
|----------------------|---------|
| `CDP_PORT_FILE` | Path to `DevToolsActivePort` file for non-standard browser installs |

Daemons auto-exit after **20 minutes of inactivity** — no manual cleanup needed in normal use.

## Troubleshooting

### "Allow debugging" modal keeps appearing
This happens if daemons aren't persisting. Make sure you're using the same `scripts/cdp.mjs` entry point — it manages daemon lifecycle automatically. If you switched tools mid-session, run `stop` and let daemons restart fresh.

### Browser not detected
If auto-detection fails, find your `DevToolsActivePort` file and set the env var:

```bash
# macOS Chrome example
export CDP_PORT_FILE="$HOME/Library/Application Support/Google/Chrome/Default/DevToolsActivePort"

# Linux Chrome example
export CDP_PORT_FILE="$HOME/.config/google-chrome/Default/DevToolsActivePort"
```

### Target not found / prefix ambiguous
Run `list` again — tab IDs change when tabs are closed/reopened. Use a longer prefix if multiple tabs share the same prefix characters.

### Remote debugging toggle not visible
Ensure you're on `chrome://inspect/#remote-debugging` (not just `chrome://inspect/`). The toggle is in the top-right of the page.

### Node.js version error
This project requires **Node.js 22+**. Check with `node --version` and upgrade if needed via [nvm](https://github.com/nvm-sh/nvm) or your package manager.

### Screenshots are blank or wrong size
The screenshot reflects the actual rendered viewport. If the tab is in a background window or the OS has display scaling, pixel coordinates for `clickxy` may need adjustment. Use `snap` or `eval` to inspect DOM state instead of relying solely on screenshots.

## Architecture Notes

- No Puppeteer, no Playwright, no intermediary — pure CDP WebSocket
- One persistent daemon process per tab (auto-spawned on first access)
- Daemon reuse is why 100+ tabs work reliably (no timeout on target enumeration)
- `type` uses CDP Input domain directly, bypassing iframe origin restrictions
