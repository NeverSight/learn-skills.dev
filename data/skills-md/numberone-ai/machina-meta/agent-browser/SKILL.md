---
name: agent-browser
description: CLI-based browser automation via agent-browser. Use for advanced browser workflows including multi-session, state persistence, page diffing, annotated screenshots, and network interception. Invoked via Bash commands (npx agent-browser).
---

# agent-browser Skill

CLI-based browser automation using [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser). Provides browser control via Bash commands as an alternative to playwright-mcp.

## When to Use agent-browser vs playwright-mcp

| Feature | playwright-mcp | agent-browser |
|---------|---------------|---------------|
| Invocation | MCP tool calls (`mcp__playwright__*`) | Bash commands (`npx agent-browser`) |
| Session persistence | No (fresh context each time) | Yes (`--session`, `--session-name`) |
| State save/load | No | Yes (`state save/load`) |
| Page diffing | No | Yes (`diff snapshot`, `diff screenshot`) |
| Annotated screenshots | No | Yes (`screenshot --annotate`) |
| Network interception | No | Yes (`network route`) |
| Cookie management | Via `browser_run_code` JS | Native (`cookies set`) |
| Multi-tab | `browser_tabs` tool | `tab new`, `tab <n>` |
| Element refs | `@ref` from snapshot | `@ref` from snapshot (same concept) |
| Best for | Quick interactions, MCP-native workflows | Advanced workflows, sessions, diffing, state persistence |

**Default**: Use **playwright-mcp** for standard browser interactions (it's already loaded as an MCP server).

**Use agent-browser** when you need:
- Session persistence across commands
- Page diffing (snapshot or visual)
- Annotated screenshots with element labels
- Network interception / mocking
- Saved authentication state
- Cookie/storage manipulation
- CDP connection to existing browser

## Nix Environment Setup

This workspace uses Nix for reproducible tooling. The Nix-managed Playwright has Chromium at a different revision than agent-browser's bundled Playwright expects. The project-level `agent-browser.json` config file at the workspace root handles this automatically by setting `executablePath` to the Nix store Chromium.

**No extra flags needed** — just run `npx agent-browser` commands from the workspace root.

If the Chromium path changes (e.g., after `niv update`), update `agent-browser.json`:
```json
{
  "executablePath": "/nix/store/<hash>-playwright-chromium/chrome-linux64/chrome"
}
```

Find the current path: `ls -la /nix/store/*-playwright-browsers/chromium-*`

## Core Workflow

The basic agent-browser interaction loop:

```bash
# 1. Open a page
npx agent-browser open https://example.com

# 2. Get interactive elements (snapshot with refs)
npx agent-browser snapshot -i

# 3. Interact using @refs from snapshot
npx agent-browser click @e3
npx agent-browser fill @e5 "search term"

# 4. Re-snapshot to see updated state
npx agent-browser snapshot -i

# 5. Take screenshot for visual verification
npx agent-browser screenshot

# 6. Close when done
npx agent-browser close
```

### Snapshot Options

```bash
npx agent-browser snapshot              # Full accessibility tree
npx agent-browser snapshot -i           # Interactive elements only (recommended)
npx agent-browser snapshot -c           # Compact (remove empty elements)
npx agent-browser snapshot -d 3         # Limit depth to 3 levels
npx agent-browser snapshot -s "#main"   # Scope to CSS selector
```

### Screenshots

```bash
npx agent-browser screenshot                        # Viewport screenshot
npx agent-browser screenshot --full                  # Full page
npx agent-browser screenshot --annotate              # With numbered element labels
npx agent-browser screenshot path/to/save.png        # Save to specific path
```

## MachinaMed Authentication

MachinaMed uses Google SSO. You must set JWT cookies before navigating to authenticated pages.

### Method 1: State File (Recommended for agent-browser)

```bash
# 1. Generate auth cookies
(cd repos/dem2 && ./scripts/user_manager.py user token dbeal@numberone.ai --export-cookie)
# Output: export AUTH_HEADER="Cookie: access_token=eyJhbG...; refresh_token=eyJhbG..."

# 2. Open browser and set cookies before navigating
npx agent-browser open about:blank
npx agent-browser cookies set access_token "eyJhbG..." --domain localhost --path /
npx agent-browser cookies set refresh_token "eyJhbG..." --domain localhost --path /

# 3. Now navigate to authenticated page
npx agent-browser open http://localhost:3000/markers
```

### Method 2: Session Persistence

```bash
# First time: set up auth in a named session
npx agent-browser --session-name machina open about:blank
npx agent-browser --session-name machina cookies set access_token "eyJhbG..." --domain localhost --path /
npx agent-browser --session-name machina cookies set refresh_token "eyJhbG..." --domain localhost --path /
npx agent-browser --session-name machina open http://localhost:3000/markers

# Later: reuse the session (cookies persist)
npx agent-browser --session-name machina open http://localhost:3000/markers
```

### Method 3: State Save/Load

```bash
# Save authenticated state for reuse
npx agent-browser state save machina-auth.json

# Load it in a new session
npx agent-browser --state machina-auth.json open http://localhost:3000/markers
```

### For Preview/Staging Environments

Replace `localhost` domain with the target:

```bash
npx agent-browser cookies set access_token "eyJhbG..." --domain preview-99.n1-machina.dev --path /
npx agent-browser cookies set refresh_token "eyJhbG..." --domain preview-99.n1-machina.dev --path /
npx agent-browser open https://preview-99.n1-machina.dev/markers
```

## Session Management

```bash
# Isolated sessions (separate browser contexts)
npx agent-browser --session my-test open https://example.com
npx agent-browser --session my-test snapshot -i

# List active sessions
npx agent-browser session list

# Auto-persisting sessions (state saved/restored automatically)
npx agent-browser --session-name my-persistent open https://example.com
```

## Page Diffing

Compare page states before and after changes:

### Snapshot Diff (DOM/Accessibility Tree)

```bash
# Take baseline snapshot, make changes, then diff
npx agent-browser snapshot > baseline.txt
# ... make changes ...
npx agent-browser diff snapshot --baseline baseline.txt

# Scoped diff (only specific section)
npx agent-browser diff snapshot --selector "#main-content" --compact
```

### Visual Diff (Pixel Comparison)

```bash
# Save baseline screenshot
npx agent-browser screenshot baseline.png

# After changes, compare
npx agent-browser diff screenshot --baseline baseline.png -o diff-result.png

# With threshold (0-1, default 0.2)
npx agent-browser diff screenshot --baseline baseline.png -t 0.1
```

### URL Comparison

```bash
# Compare two URLs side by side
npx agent-browser diff url http://localhost:3000/markers https://preview-99.n1-machina.dev/markers

# Visual comparison
npx agent-browser diff url http://localhost:3000 https://preview-99.n1-machina.dev --screenshot

# Scoped comparison
npx agent-browser diff url <url1> <url2> --selector "#biomarker-list"
```

## Network Interception

```bash
# Block requests (e.g., analytics)
npx agent-browser network route "**/analytics/**" --abort

# Mock API responses
npx agent-browser network route "**/api/v1/observations/**" --body '{"items": []}'

# View tracked requests
npx agent-browser network requests
npx agent-browser network requests --filter api

# Remove routes
npx agent-browser network unroute
```

## Common Commands Reference

### Navigation

```bash
npx agent-browser open <url>           # Navigate to URL
npx agent-browser back                 # Go back
npx agent-browser forward              # Go forward
npx agent-browser reload               # Reload page
npx agent-browser close                # Close browser
```

### Interaction

```bash
npx agent-browser click @e1            # Click element by ref
npx agent-browser fill @e2 "text"      # Clear and fill input
npx agent-browser type @e2 "text"      # Type into element
npx agent-browser press Enter          # Press key
npx agent-browser select @e3 "option"  # Select dropdown option
npx agent-browser check @e4            # Check checkbox
npx agent-browser scroll down 500      # Scroll down 500px
```

### Element Inspection

```bash
npx agent-browser get text @e1         # Get text content
npx agent-browser get html @e1         # Get innerHTML
npx agent-browser get value @e1        # Get input value
npx agent-browser get title            # Get page title
npx agent-browser get url              # Get current URL
npx agent-browser is visible @e1       # Check visibility
```

### Semantic Locators

```bash
npx agent-browser find role button click           # Click first button
npx agent-browser find text "Submit" click         # Click by text
npx agent-browser find label "Email" fill "a@b.c"  # Fill by label
npx agent-browser find testid "login-btn" click    # Click by data-testid
```

### Waiting

```bash
npx agent-browser wait "#element"                  # Wait for element
npx agent-browser wait 2000                        # Wait 2 seconds
npx agent-browser wait --text "Loading complete"   # Wait for text
npx agent-browser wait --load networkidle          # Wait for network idle
```

### JavaScript Execution

```bash
npx agent-browser eval "document.title"
npx agent-browser eval "window.scrollTo(0, document.body.scrollHeight)"
```

### Tabs

```bash
npx agent-browser tab                  # List tabs
npx agent-browser tab new <url>        # Open new tab
npx agent-browser tab 2                # Switch to tab 2
npx agent-browser tab close            # Close current tab
```

### Cookies & Storage

```bash
npx agent-browser cookies                          # Get all cookies
npx agent-browser cookies set <name> <value>       # Set cookie
npx agent-browser cookies clear                    # Clear cookies
npx agent-browser storage local                    # Get localStorage
npx agent-browser storage local set <key> <value>  # Set localStorage
```

### State Management

```bash
npx agent-browser state save <path>    # Save auth/session state
npx agent-browser state load <path>    # Load saved state
npx agent-browser state list           # List saved states
npx agent-browser state clear --all    # Clear all states
```

### Debugging

```bash
npx agent-browser console              # View console messages
npx agent-browser errors               # View page errors
npx agent-browser highlight @e1        # Highlight element
npx agent-browser trace start          # Start recording trace
npx agent-browser trace stop           # Stop and save trace
```

## Global Flags

```bash
--session <name>          # Isolated browser session
--session-name <name>     # Auto-persisting session
--state <path>            # Load storage state JSON
--headed                  # Show browser window (visible)
--json                    # JSON output format
--full, -f                # Full page screenshot
--annotate                # Annotated screenshot
--debug                   # Debug output
--config <path>           # Config file path
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `AGENT_BROWSER_SESSION` | Session name |
| `AGENT_BROWSER_SESSION_NAME` | Auto-save/restore session |
| `AGENT_BROWSER_STATE` | Storage state JSON file |
| `AGENT_BROWSER_PROFILE` | Persistent profile path |
| `AGENT_BROWSER_DEFAULT_TIMEOUT` | Operation timeout (ms) |

## Related Skills

- **machina-ui**: Required authentication setup for MachinaMed pages. Load machina-ui first to get JWT cookies, then use agent-browser for browser automation.
- **playwright-mcp**: Default MCP-based browser automation. Use for standard interactions.
- **machina-docker**: Development stack management (start/stop services before browser testing).
