---
name: chrome-automation
description: Automate Chrome browser tasks using agent-browser CLI. Navigate pages, fill forms, click buttons, take screenshots, extract data, and replay recorded workflows — all inside the user's real Chrome session.
---

# Skill: Chrome Automation (agent-browser)

Automate browser tasks in the user's real Chrome session via the [agent-browser](https://github.com/vercel-labs/agent-browser) CLI.

> **Prerequisite**: agent-browser must be installed and Chrome must have remote debugging enabled. See `references/agent-browser-setup.md` if unsure.

---

## Core Principle: Reuse the User's Existing Chrome

This skill operates on a **single Chrome process** — the user's real browser. There is no session management, no separate profiles, no launching a fresh Playwright browser.

### Always Start by Listing Tabs

Before opening any new page, **always list existing tabs first**:

```bash
agent-browser --auto-connect tab list
```

This returns all open tabs with their index numbers, titles, and URLs. Check if the page you need is already open:

- **If the target page is already open** → switch to that tab directly instead of opening a new one. The user likely has it open because they are already logged in and the page is in the right state.
  ```bash
  agent-browser --auto-connect tab <index>
  ```
- **If the target page is NOT open** → open it in the current tab or a new tab.
  ```bash
  agent-browser --auto-connect open <url>
  ```

### Why This Matters

- The user's Chrome has their cookies, login sessions, and browser state
- Opening a new page when one is already available wastes time and may lose login state
- Many marketing platforms (social media dashboards, ad managers, CMS tools) require login — reusing an existing logged-in tab avoids re-authentication

---

## Connection

Always use `--auto-connect` to connect to the user's running Chrome instance:

```bash
agent-browser --auto-connect <command>
```

This auto-discovers Chrome with remote debugging enabled. If connection fails, guide the user through enabling remote debugging (see `references/agent-browser-setup.md`).

---

## Common Workflows

### 1. Navigate and Interact

```bash
# List tabs to find existing pages
agent-browser --auto-connect tab list

# Switch to an existing tab (if found)
agent-browser --auto-connect tab <index>

# Or open a new page
agent-browser --auto-connect open https://example.com
agent-browser --auto-connect wait --load networkidle

# Take a snapshot to see interactive elements
agent-browser --auto-connect snapshot -i

# Click, fill, etc.
agent-browser --auto-connect click @e3
agent-browser --auto-connect fill @e5 "some text"
```

### 2. Extract Data from a Page

```bash
# Get all text content
agent-browser --auto-connect get text body

# Take a screenshot for visual inspection
agent-browser --auto-connect screenshot

# Execute JavaScript for structured data
agent-browser --auto-connect eval "JSON.stringify(document.querySelectorAll('table tr').length)"
```

### 3. Replay a Chrome DevTools Recording

The user may provide a recording exported from Chrome DevTools Recorder (JSON, Puppeteer JS, or @puppeteer/replay JS format). See [Replaying Recordings](#replaying-recordings) below.

---

## Step-by-Step Interaction Guide

### Taking Snapshots

Use `snapshot -i` to see all interactive elements with refs (`@e1`, `@e2`, ...):

```bash
agent-browser --auto-connect snapshot -i
```

The output lists each interactive element with its role, text, and ref. Use these refs for subsequent actions.

### Step Type Mapping

| Action | Command |
|--------|---------|
| Navigate | `agent-browser --auto-connect open <url>` (optionally `wait --load networkidle`, but some sites like Reddit never reach networkidle — skip if `open` already shows the page title) |
| Click | `snapshot -i` → find ref → `click @eN` |
| Fill standard input | `click @eN` → `fill @eN "text"` |
| Fill rich text editor | `click @eN` → `keyboard inserttext "text"` |
| Press key | `press <key>` (Enter, Tab, Escape, etc.) |
| Scroll | `scroll down <amount>` or `scroll up <amount>` |
| Wait for element | `wait @eN` or `wait "<css-selector>"` |
| Screenshot | `screenshot` or `screenshot --annotate` |
| Get page text | `get text body` |
| Get current URL | `get url` |
| Run JavaScript | `eval <js>` |

### How to Distinguish Input Types

- **Standard input/textarea** → use `fill`
- **Contenteditable div / rich text editor** (LinkedIn message box, Gmail compose, Slack, CMS editors) → click/focus first, then use `keyboard inserttext`

### Ref Lifecycle

Refs (`@e1`, `@e2`, ...) are **invalidated when the page changes**. Always re-snapshot after:
- Clicking links or buttons that trigger navigation
- Submitting forms
- Triggering dynamic content loads (AJAX, SPA navigation)

### Verification

After each significant action, verify the result:
```bash
agent-browser --auto-connect snapshot -i   # check interactive state
agent-browser --auto-connect screenshot     # visual verification
```

---

## Replaying Recordings

### Accepted Formats

1. **JSON** (recommended) — structured, can be read progressively:
   ```bash
   # Count steps
   jq '.steps | length' recording.json

   # Read first 5 steps
   jq '.steps[0:5]' recording.json
   ```

2. **@puppeteer/replay JS** (`import { createRunner }`)
3. **Puppeteer JS** (`require('puppeteer')`, `page.goto`, `Locator.race`)

### How to Replay

1. **Parse the recording** — understand the full intent before acting. Summarize what the recording does.
2. **List tabs first** — check if the target page is already open.
3. **Navigate** — execute `navigate` steps, reusing existing tabs when possible.
4. **For each interaction step**:
   - Take a snapshot (`snapshot -i`) to see current interactive elements
   - Match the recording's `aria/...` selectors against the snapshot
   - Fall back to `text/...`, then CSS class hints, then screenshot
   - **Do not rely on ember IDs, numeric IDs, or exact XPaths** — these change every page load
5. **Verify after each step** — snapshot or screenshot to confirm

---

## Iframe-Heavy Sites

`snapshot -i` operates on the main frame only and **cannot penetrate iframes**. Sites like LinkedIn, Gmail, and embedded editors render content inside iframes.

### Detecting Iframe Issues

- `snapshot -i` returns unexpectedly short or empty results
- Recording references elements not appearing in snapshot output
- `get text body` content doesn't match what a screenshot shows

### Workarounds

1. **Use `eval` to access iframe content**:
   ```bash
   agent-browser --auto-connect eval --stdin <<'EVALEOF'
   const frame = document.querySelector('iframe[data-testid="interop-iframe"]');
   const doc = frame.contentDocument;
   const btn = doc.querySelector('button[aria-label="Send"]');
   btn.click();
   EVALEOF
   ```
   Note: Only works for same-origin iframes.

2. **Use `keyboard` for blind input**: If the iframe element has focus, `keyboard inserttext "..."` sends text regardless of frame boundaries.

3. **Use `get text body`** to read full page content including iframes.

4. **Use `screenshot`** for visual verification when snapshot is unreliable.

### When to Ask the User

If workarounds fail after 2 attempts on the same step, pause and explain:
- The page uses iframes that cannot be accessed via snapshot
- Which element you need and what you expected
- Ask the user to perform that step manually, then continue

---

## Handling Unexpected Situations

### Handle Automatically (do not stop):
- Popups or banners → dismiss them (`find text "Dismiss" click` or `find text "Close" click`)
- Cookie consent dialogs → accept or dismiss
- Tooltip overlays → close them first
- Element not in snapshot → try `find text "..." click`, or scroll to reveal with `scroll down 300`

### Pause and Ask the User:
- Login / authentication is required
- A CAPTCHA appears
- Page structure is completely different from expected
- A destructive action is about to happen (deleting data, sending real content) — confirm first
- Stuck for more than 2 attempts on the same step
- All iframe workarounds have failed

When pausing, explain clearly: what step you are on, what you expected, and what you see.

---

## Key Commands Reference

| Command | Description |
|---------|-------------|
| `tab list` | List all open tabs with index, title, and URL |
| `tab <index>` | Switch to an existing tab by index |
| `tab new` | Open a new empty tab |
| `tab close` | Close the current tab |
| `open <url>` | Navigate to URL |
| `snapshot -i` | List interactive elements with refs |
| `click @eN` | Click element by ref |
| `fill @eN "text"` | Clear and fill standard input/textarea |
| `type @eN "text"` | Type without clearing |
| `keyboard inserttext "text"` | Insert text (best for contenteditable) |
| `press <key>` | Press keyboard key |
| `scroll down/up <amount>` | Scroll page in pixels |
| `wait @eN` | Wait for element to appear |
| `wait --load networkidle` | Wait for network to settle |
| `wait <ms>` | Wait for a duration |
| `screenshot [path]` | Take screenshot |
| `screenshot --annotate` | Screenshot with numbered labels |
| `eval <js>` | Execute JavaScript in page |
| `get text body` | Get all text content |
| `get url` | Get current URL |
| `set viewport <w> <h>` | Set viewport size |
| `find text "..." click` | Semantic find and click |
| `close` | Close browser session |

---

## Known Limitations

1. **Iframe blindness**: `snapshot -i` cannot see inside iframes. See [Iframe-Heavy Sites](#iframe-heavy-sites).
2. **`find text` strict mode**: Fails when multiple elements match. Use `snapshot -i` to locate the specific ref instead.
3. **`fill` vs contenteditable**: `fill` only works on `<input>` and `<textarea>`. For rich text editors, use `keyboard inserttext`.
4. **`eval` is main-frame only**: To interact with iframe content, traverse via `document.querySelector('iframe').contentDocument...`

---

## Multi-Platform Operations

When the user requests an action across **multiple platforms** (e.g., "publish this article to Dev.to, LinkedIn, and X"), do NOT attempt all platforms in a single conversation. Instead, launch **sequential Agent subagents**, one per platform.

### Why Subagents

Each platform operation consumes ~25-40K tokens (reference file + snapshots + interactions). Running 3-5 platforms in one context risks hitting the 200K token limit and degrading late-platform accuracy. Each subagent gets its own fresh 200K context window.

### How to Execute

1. **Prepare the content** — confirm the post text, title, tags, and any platform-specific adaptations with the user.
2. **For each platform**, launch a `general-purpose` Agent subagent with a prompt that includes:
   - The full content to publish
   - Instructions to read the relevant reference file (e.g., `Read /path/to/skills/chrome-automation/references/x.md`)
   - Instructions to read the agent-browser skill file for command reference
   - The specific task (post, comment, reply, etc.)
   - Any platform-specific instructions (e.g., "use these hashtags on LinkedIn")
3. **Run subagents sequentially** (one at a time), because they all share the same Chrome browser via `--auto-connect`. Parallel subagents would cause tab conflicts.
4. **After each subagent completes**, report the result to the user before launching the next one.

### Prompt Template for Subagents

```
You are automating a browser task on [PLATFORM].

First, read these files for context:
- /absolute/path/to/skills/chrome-automation/references/[platform].md
- /absolute/path/to/.claude/skills/agent-browser/SKILL.md (agent-browser command reference)

Then connect to the user's Chrome browser using `agent-browser --auto-connect` and perform the following task:

[TASK DESCRIPTION]

Content to publish:
[CONTENT]

Important:
- Always list tabs first (`tab list`) and reuse existing logged-in tabs
- Re-snapshot after every navigation or action
- Confirm with the user before submitting/publishing (destructive action)
- If login is required or a CAPTCHA appears, stop and explain
```

### When NOT to Use Subagents

- **Single platform** — just do it directly in the current conversation.
- **Read-only tasks** (browsing, searching, extracting data) — context usage is lighter; a single conversation can handle 2-3 platforms.

---

## Platform References

When automating tasks on specific platforms, consult the relevant reference document for page structure details, common operations, and known quirks:

| Platform | Reference | Key Notes |
|----------|-----------|-----------|
| Reddit | [`references/reddit.md`](./references/reddit.md) | Custom `faceplate-*` components; `networkidle` never reached; unlabeled comment textbox; `find text` fails due to duplicate elements |
| X (Twitter) | [`references/x.md`](./references/x.md) | `open` often times out (use `tab list` to reuse existing tabs); click **timestamp** for post detail (not username); DraftJS contenteditable input (`data-testid="tweetTextarea_0"`); avoid `networkidle` |
| LinkedIn | [`references/linkedin.md`](./references/linkedin.md) | Ember.js SPA; Enter submits comments (use Shift+Enter for newlines); comment box and compose box share the same label; avoid `networkidle`; messaging overlay may block content |
| Dev.to | [`references/devto.md`](./references/devto.md) | Fast server-rendered HTML (Forem/Rails); standard `<textarea>` for comments/posts (Markdown); 5 reaction types; Algolia-powered search; `networkidle` works normally |
| Hacker News | [`references/hackernews.md`](./references/hackernews.md) | Minimal plain HTML; all form fields are unlabeled; `link "reply"` navigates to separate page; `networkidle` works instantly; rate limiting on posts/comments |

---

> For installation and Chrome setup instructions, see [`references/agent-browser-setup.md`](./references/agent-browser-setup.md).
