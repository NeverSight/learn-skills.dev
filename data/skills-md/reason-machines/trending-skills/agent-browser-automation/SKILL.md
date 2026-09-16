---
name: agent-browser-automation
description: Headless browser automation CLI for AI agents using native Rust binary with Chrome DevTools Protocol
triggers:
  - automate browser with agent-browser
  - use agent-browser for web scraping
  - browser automation CLI for AI
  - take screenshot with agent-browser
  - click and fill forms with agent-browser
  - agent-browser snapshot accessibility tree
  - batch browser commands with agent-browser
  - install agent-browser for automation
---

# agent-browser

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

`agent-browser` is a headless browser automation CLI built in Rust, designed for AI agents. It wraps Chrome via the Chrome DevTools Protocol (CDP) and exposes a fast, ergonomic command-line interface for navigation, interaction, accessibility snapshots, screenshots, network interception, and more — with no Node.js or Playwright runtime required.

## Installation

### Recommended (npm global)
```bash
npm install -g agent-browser
agent-browser install  # Download Chrome for Testing (first time only)
```

### macOS (Homebrew)
```bash
brew install agent-browser
agent-browser install
```

### Rust / Cargo
```bash
cargo install agent-browser
agent-browser install
```

### Local project dependency
```bash
npm install agent-browser
# Add to package.json scripts or invoke via npx
```

### Linux (with system dependencies)
```bash
agent-browser install --with-deps
```

## Quick Start

```bash
agent-browser open https://example.com
agent-browser snapshot                        # Accessibility tree with @refs (best for AI)
agent-browser click @e2                       # Click by ref from snapshot
agent-browser fill @e3 "hello@example.com"   # Fill by ref
agent-browser get text @e1                    # Get text content
agent-browser screenshot page.png
agent-browser close
```

## Core Commands

### Navigation
```bash
agent-browser open <url>           # Navigate (aliases: goto, navigate)
agent-browser get url              # Get current URL
agent-browser get title            # Get page title
agent-browser close                # Close browser (aliases: quit, exit)
```

### Accessibility Snapshot (recommended for AI agents)
```bash
agent-browser snapshot             # Returns accessibility tree with @ref IDs
agent-browser snapshot -i          # Interactive / compact mode
```

Snapshot output includes `@eN` refs you can use directly:
```
@e1 [button] "Submit"
@e2 [textbox] "Email" value=""
@e3 [link] "Sign in"
```

Then act on them:
```bash
agent-browser fill @e2 "user@example.com"
agent-browser click @e1
```

### Interaction
```bash
agent-browser click <sel>                     # Click element
agent-browser dblclick <sel>                  # Double-click
agent-browser fill <sel> <text>               # Clear and fill input
agent-browser type <sel> <text>               # Type into element
agent-browser press <key>                     # Press key (Enter, Tab, Control+a)
agent-browser keyboard type <text>            # Type at current focus (real keystrokes)
agent-browser keyboard inserttext <text>      # Insert text without key events
agent-browser hover <sel>                     # Hover element
agent-browser select <sel> <value>            # Select dropdown option
agent-browser check <sel>                     # Check checkbox
agent-browser uncheck <sel>                   # Uncheck checkbox
agent-browser scroll down 500                 # Scroll (up/down/left/right, optional px)
agent-browser scroll down --selector "#feed"  # Scroll within element
agent-browser scrollintoview <sel>            # Scroll element into view
agent-browser drag <src> <target>             # Drag and drop
agent-browser upload <sel> /path/file.pdf     # Upload file
```

### Screenshots & PDF
```bash
agent-browser screenshot                          # Save to temp dir, print path
agent-browser screenshot page.png                 # Save to path
agent-browser screenshot --full page.png          # Full-page screenshot
agent-browser screenshot --annotate               # Numbered element labels overlay
agent-browser screenshot --screenshot-dir ./shots # Custom output directory
agent-browser screenshot --screenshot-format jpeg --screenshot-quality 80
agent-browser pdf output.pdf                      # Save page as PDF
```

### Getting Element Info
```bash
agent-browser get text <sel>           # Text content
agent-browser get html <sel>           # innerHTML
agent-browser get value <sel>          # Input value
agent-browser get attr <sel> <attr>    # Attribute value
agent-browser get count <sel>          # Count matching elements
agent-browser get box <sel>            # Bounding box
agent-browser get styles <sel>         # Computed styles
agent-browser get cdp-url              # CDP WebSocket URL
```

### State Checks
```bash
agent-browser is visible <sel>
agent-browser is enabled <sel>
agent-browser is checked <sel>
```

### Semantic Locators (find)
```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "test@example.com"
agent-browser find placeholder "Search..." fill "rust"
agent-browser find testid "login-btn" click
agent-browser find first ".item" click
agent-browser find nth 2 "a" text
agent-browser find role textbox fill "hello" --name "Username"
```

**Actions:** `click`, `fill`, `type`, `hover`, `focus`, `check`, `uncheck`, `text`

### Waiting
```bash
agent-browser wait "#modal"                          # Wait for element visible
agent-browser wait 2000                              # Wait N milliseconds
agent-browser wait --text "Welcome back"             # Wait for text
agent-browser wait --url "**/dashboard"              # Wait for URL pattern
agent-browser wait --load networkidle                # Wait for load state
agent-browser wait --fn "window.appReady === true"   # Wait for JS condition
agent-browser wait "#spinner" --state hidden         # Wait for element to disappear
```

**Load states:** `load`, `domcontentloaded`, `networkidle`

### JavaScript Eval
```bash
agent-browser eval "document.title"
agent-browser eval "JSON.stringify(window.__STATE__)"
agent-browser eval -b "BASE64_ENCODED_JS"
echo "return document.body.innerHTML" | agent-browser eval --stdin
```

### Batch Execution (efficient multi-step)
```bash
echo '[
  ["open", "https://example.com"],
  ["snapshot", "-i"],
  ["fill", "@e2", "user@example.com"],
  ["click", "@e1"],
  ["screenshot", "result.png"]
]' | agent-browser batch --json

# Stop on first failure
agent-browser batch --bail < commands.json
```

### Tabs & Frames
```bash
agent-browser tab                    # List tabs
agent-browser tab new https://...    # New tab with URL
agent-browser tab 2                  # Switch to tab 2
agent-browser tab close              # Close current tab
agent-browser frame "#my-iframe"     # Switch into iframe
agent-browser frame main             # Return to main frame
```

### Cookies & Storage
```bash
agent-browser cookies
agent-browser cookies set session_id "abc123"
agent-browser cookies clear

agent-browser storage local
agent-browser storage local set theme dark
agent-browser storage local clear
agent-browser storage session set cart '{"items":[]}'
```

### Network
```bash
agent-browser network route "**/api/users" --body '{"users":[]}'  # Mock response
agent-browser network route "**/ads/**" --abort                    # Block requests
agent-browser network unroute                                       # Remove all routes
agent-browser network requests --filter api                        # View requests
agent-browser network har start
agent-browser network har stop recording.har
```

### Browser Settings
```bash
agent-browser set viewport 1280 800
agent-browser set viewport 375 812 2        # With device pixel ratio (retina)
agent-browser set device "iPhone 14"
agent-browser set geo 37.7749 -122.4194
agent-browser set offline on
agent-browser set headers '{"X-Custom":"value"}'
agent-browser set credentials admin secret
agent-browser set media dark
```

### Auth State
```bash
agent-browser state save ./auth.json    # Save cookies + localStorage
agent-browser state load ./auth.json    # Restore auth state
agent-browser state list                # List saved states
agent-browser state show auth.json      # Summary of saved state
```

### Dialogs
```bash
agent-browser dialog accept             # Accept alert/confirm/prompt
agent-browser dialog accept "My input"  # Accept prompt with text
agent-browser dialog dismiss
```

### Clipboard
```bash
agent-browser clipboard read
agent-browser clipboard write "Hello, World!"
agent-browser clipboard copy           # Ctrl+C current selection
agent-browser clipboard paste          # Ctrl+V
```

### Diff & Visual Testing
```bash
agent-browser diff snapshot                                  # vs last snapshot
agent-browser diff snapshot --baseline before.txt            # vs saved file
agent-browser diff snapshot --selector "#main" --compact
agent-browser diff screenshot --baseline before.png
agent-browser diff screenshot --baseline b.png -o diff.png
agent-browser diff url https://v1.example.com https://v2.example.com
agent-browser diff url https://v1.example.com https://v2.example.com --screenshot
agent-browser diff url https://v1.example.com https://v2.example.com --selector "#content"
```

### Debug & Profiling
```bash
agent-browser trace start trace.zip
agent-browser trace stop
agent-browser profiler start
agent-browser profiler stop profile.json
agent-browser console                  # View console messages
agent-browser errors                   # View uncaught JS exceptions
agent-browser highlight "#button"      # Visually highlight element
agent-browser inspect                  # Open Chrome DevTools
agent-browser connect 9222             # Connect to existing browser via CDP port
```

## Common Patterns

### Login flow and save session
```bash
#!/bin/bash
agent-browser open https://app.example.com/login
agent-browser fill "#email" "$LOGIN_EMAIL"
agent-browser fill "#password" "$LOGIN_PASSWORD"
agent-browser click "[type=submit]"
agent-browser wait --url "**/dashboard"
agent-browser state save ./session.json
```

### AI agent loop with snapshot-driven interaction
```bash
#!/bin/bash
agent-browser open https://app.example.com
agent-browser state load ./session.json

# Get snapshot, parse @refs, act
SNAPSHOT=$(agent-browser snapshot)
echo "$SNAPSHOT"

# Agent determines @e5 is the search box
agent-browser fill @e5 "quarterly report"
agent-browser press Enter
agent-browser wait --load networkidle
agent-browser snapshot
agent-browser screenshot results.png
```

### Batch commands from a script (JSON)
```bash
cat > commands.json << 'EOF'
[
  ["open", "https://news.ycombinator.com"],
  ["wait", "--load", "networkidle"],
  ["get", "title"],
  ["snapshot"],
  ["screenshot", "hn.png"]
]
EOF

agent-browser batch --json < commands.json
```

### Scrape with mocked network
```bash
agent-browser open https://api-heavy-app.example.com
agent-browser network route "**/api/slow-endpoint" --body '{"data":"mocked"}'
agent-browser snapshot
agent-browser network unroute
```

### Full-page screenshot with annotations
```bash
agent-browser open https://example.com
agent-browser wait --load networkidle
agent-browser screenshot --full --annotate annotated.png
```

### Connect to already-running Chrome
```bash
# Start Chrome with remote debugging
google-chrome --remote-debugging-port=9222 &

agent-browser connect 9222
agent-browser open https://example.com
agent-browser snapshot
```

### Emulate mobile device
```bash
agent-browser set device "iPhone 14"
agent-browser open https://example.com
agent-browser screenshot mobile.png
```

### HAR recording for network analysis
```bash
agent-browser open https://example.com
agent-browser network har start
agent-browser click "#load-data"
agent-browser wait --load networkidle
agent-browser network har stop session.har
```

## Selector Reference

| Format | Example | Notes |
|--------|---------|-------|
| `@ref` | `@e1`, `@e12` | From `snapshot` output — preferred for AI |
| CSS | `#id`, `.class`, `[attr=val]` | Standard CSS selectors |
| Text | `"Sign In"` | Exact text match |
| XPath | `//button[@type='submit']` | Full XPath |

## Troubleshooting

### Chrome not found
```bash
agent-browser install              # Downloads Chrome for Testing
agent-browser install --with-deps  # Linux: also installs system libs
```

### Element not found / timing issues
```bash
agent-browser wait "#my-element"              # Wait for visibility first
agent-browser wait --load networkidle         # Wait for page to settle
agent-browser wait --fn "!!document.querySelector('#app')"
```

### Selector issues — use snapshot refs instead
```bash
# Instead of fragile CSS:
agent-browser click ".btn.btn-primary.submit-form"

# Use snapshot refs:
agent-browser snapshot  # Find @e7 = [button] "Submit"
agent-browser click @e7
```

### Debug what's on the page
```bash
agent-browser screenshot debug.png        # Visual check
agent-browser snapshot                    # Accessibility tree
agent-browser console                     # JS console output
agent-browser errors                      # Uncaught exceptions
agent-browser eval "document.readyState"
```

### Auth issues between sessions
```bash
agent-browser state save ./auth.json   # After successful login
agent-browser state load ./auth.json   # At start of next session
```

### Handling alerts/dialogs
```bash
# Set up handler BEFORE the action that triggers dialog
agent-browser dialog accept
agent-browser click "#delete-button"
```

### Performance — use batch for multi-step workflows
```bash
# Slow: one process per command
agent-browser open https://example.com
agent-browser fill "#q" "search"
agent-browser click "#submit"

# Fast: single process, multiple commands
echo '[["open","https://example.com"],["fill","#q","search"],["click","#submit"]]' \
  | agent-browser batch --json
```
