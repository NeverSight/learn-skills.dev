---
name: agent-browser
description: Automate headless browser interactions using agent-browser CLI. Use when scraping web pages, automating form submissions, testing web apps, or performing browser automation tasks. Works with element refs (@e1, @e2) optimized for AI agent reasoning.
---

# agent-browser CLI

A headless browser automation CLI designed for AI agents, with fast Rust-based execution and element refs optimized for LLM reasoning.

## Overview

agent-browser provides programmatic browser control through a CLI that's purpose-built for AI agent workflows. It uses deterministic element references (`@e1`, `@e2`, etc.) from accessibility trees, making it ideal for LLM-based automation where consistent element targeting is critical.

**Key Features:**
- Fast Rust-based CLI with Node.js fallback
- Element refs (`@e1`, `@e2`) for stable LLM reasoning
- Session isolation for parallel browser instances
- JSON output for programmatic parsing
- Accessibility tree snapshots for element discovery
- CDP connection support for existing browser instances

## When to Use

- Automating web interactions (form filling, clicking, navigation)
- Scraping web content with accessibility tree parsing
- Testing web applications programmatically
- Multi-agent scenarios requiring isolated browser sessions
- Screenshot capture and PDF generation
- Monitoring web page state changes

## Prerequisites

- Node.js >= 18 or Bun runtime
- Chromium (installed via `agent-browser install`)

## Installation

```bash
# Install globally
bun install -g agent-browser

# Download Chromium
agent-browser install

# Linux with system dependencies
agent-browser install --with-deps
```

Verify installation:
```bash
agent-browser --version
```

## Quick Start

```bash
# Navigate to a page
agent-browser open https://example.com

# Get accessibility snapshot with element refs
agent-browser snapshot -i  # -i = interactive elements only

# Click an element by ref
agent-browser click @e2

# Fill a form field
agent-browser fill @e3 "test@example.com"

# Take a screenshot
agent-browser screenshot output.png
```

## Core Workflow

### 1. Open Page and Snapshot

```bash
# Open URL
agent-browser open https://example.com

# Get interactive elements with refs
agent-browser snapshot -i --json
```

The snapshot returns elements like:
```
@e1 link "Home"
@e2 textbox "Email"
@e3 button "Submit"
```

### 2. Interact Using Refs

```bash
# Click by ref
agent-browser click @e2

# Type into focused element
agent-browser type @e2 "hello@example.com"

# Fill (clears first, then types)
agent-browser fill @e2 "hello@example.com"

# Press keyboard key
agent-browser press Enter
```

### 3. Verify State

```bash
# Check element visibility
agent-browser is visible @e3

# Get element text
agent-browser get text @e1

# Get page URL
agent-browser get url
```

## Command Reference

### Navigation

| Command | Description |
|---------|-------------|
| `open <url>` | Navigate to URL |
| `back` | Go back in history |
| `forward` | Go forward in history |
| `reload` | Reload current page |
| `close` | Close browser |

### Interactions

| Command | Description |
|---------|-------------|
| `click <ref>` | Click element |
| `dblclick <ref>` | Double-click element |
| `type <ref> <text>` | Type text into element |
| `fill <ref> <text>` | Clear and fill element |
| `press <key>` | Press keyboard key (Enter, Tab, Control+a) |
| `hover <ref>` | Hover over element |
| `focus <ref>` | Focus element |
| `check <ref>` | Check checkbox |
| `uncheck <ref>` | Uncheck checkbox |
| `select <ref> <val>` | Select dropdown option |
| `scroll <dir> [px]` | Scroll (up/down/left/right) |
| `wait <ref\|ms>` | Wait for element or milliseconds |

### Information

| Command | Description |
|---------|-------------|
| `snapshot` | Get accessibility tree with refs |
| `snapshot -i` | Interactive elements only |
| `snapshot -c` | Compact (remove empty elements) |
| `snapshot -d <n>` | Limit tree depth |
| `get text <ref>` | Get element text content |
| `get html <ref>` | Get element HTML |
| `get value <ref>` | Get input value |
| `get url` | Get current page URL |
| `get title` | Get page title |
| `screenshot [path]` | Take screenshot |
| `screenshot --full` | Full page screenshot |
| `pdf <path>` | Save page as PDF |

### State Checks

| Command | Description |
|---------|-------------|
| `is visible <ref>` | Check if element is visible |
| `is enabled <ref>` | Check if element is enabled |
| `is checked <ref>` | Check if checkbox is checked |

### Find Elements

```bash
# Find by role and click
agent-browser find role button click --name Submit

# Find by text
agent-browser find text "Sign In" click

# Find by label
agent-browser find label "Email" fill "test@example.com"

# Find by placeholder
agent-browser find placeholder "Search..." type "query"
```

## Session Management

Sessions provide isolated browser instances for parallel execution:

```bash
# Use named session
agent-browser --session login-flow open https://app.com

# Different session for another task
agent-browser --session checkout open https://app.com/cart

# List active sessions
agent-browser session list

# Environment variable (persistent across commands)
export AGENT_BROWSER_SESSION=my-session
agent-browser open https://example.com
```

## JSON Output

Use `--json` for machine-readable output:

```bash
# Snapshot as JSON
agent-browser snapshot -i --json

# Get element info as JSON
agent-browser get text @e1 --json

# Parse in scripts
agent-browser get url --json | jq -r '.url'
```

## Advanced Features

### CDP Connection

Connect to an existing Chrome instance:

```bash
# Start Chrome with debugging
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

# Connect agent-browser
agent-browser --cdp 9222 snapshot
```

### Video Recording

```bash
# Start recording
agent-browser record start recording.webm https://example.com

# Perform actions...
agent-browser click @e1
agent-browser fill @e2 "test"

# Stop and save
agent-browser record stop
```

### Network Interception

```bash
# Block requests to URL pattern
agent-browser network route "**/analytics/*" --abort

# Mock API response
agent-browser network route "**/api/user" --body '{"name": "Test"}'

# View captured requests
agent-browser network requests
```

### Custom Headers

```bash
# Set auth headers
agent-browser --headers '{"Authorization": "Bearer token123"}' open https://api.example.com
```

### Browser Extensions

```bash
# Load extension
agent-browser --extension /path/to/extension open https://example.com
```

## AI Agent Patterns

### Form Automation

```bash
#!/bin/bash
# Login automation script

agent-browser open https://app.com/login

# Get form elements
agent-browser snapshot -i --json > elements.json

# Fill credentials
agent-browser fill @e2 "user@example.com"
agent-browser fill @e3 "password123"

# Submit
agent-browser click @e4

# Wait for navigation
agent-browser wait 2000

# Verify login
agent-browser get url --json | jq -r '.url'
```

### Data Extraction

```bash
#!/bin/bash
# Scrape product data

agent-browser open https://shop.com/products

# Get page content
agent-browser snapshot --json > snapshot.json

# Extract specific element text
agent-browser get text '[data-testid="price"]' --json

# Screenshot for verification
agent-browser screenshot products.png
```

### Multi-Page Workflow

```bash
#!/bin/bash
SESSION="checkout-flow"

# Step 1: Add to cart
agent-browser --session $SESSION open https://shop.com/product/123
agent-browser --session $SESSION click @add-to-cart-button
agent-browser --session $SESSION wait 1000

# Step 2: Go to checkout
agent-browser --session $SESSION open https://shop.com/checkout
agent-browser --session $SESSION snapshot -i

# Step 3: Fill shipping
agent-browser --session $SESSION fill @shipping-name "John Doe"
agent-browser --session $SESSION fill @shipping-address "123 Main St"

# Cleanup
agent-browser --session $SESSION close
```

## Options Reference

| Option | Description |
|--------|-------------|
| `--session <name>` | Isolated browser session |
| `--json` | JSON output format |
| `--headed` | Show browser window (not headless) |
| `--cdp <port>` | Connect via Chrome DevTools Protocol |
| `--headers <json>` | HTTP headers for requests |
| `--proxy <url>` | Proxy server |
| `--executable-path <path>` | Custom browser executable |
| `--extension <path>` | Load browser extension |
| `--full, -f` | Full page screenshot |
| `--debug` | Debug output |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `AGENT_BROWSER_SESSION` | Default session name |
| `AGENT_BROWSER_EXECUTABLE_PATH` | Custom browser path |
| `AGENT_BROWSER_STREAM_PORT` | WebSocket streaming port |

## Troubleshooting

### "Browser not found"
```bash
# Install Chromium
agent-browser install
```

### Element ref not found
```bash
# Refresh snapshot after page changes
agent-browser snapshot -i

# Check if element is visible
agent-browser is visible @e1
```

### Session conflicts
```bash
# List active sessions
agent-browser session list

# Use unique session names
agent-browser --session unique-$(date +%s) open https://example.com
```

### Headless issues
```bash
# Run with visible browser for debugging
agent-browser --headed open https://example.com
```

### Timeout waiting for element
```bash
# Explicit wait before interaction
agent-browser wait 2000
agent-browser wait @e1  # Wait for element to appear
```

## Best Practices

- **Always snapshot first**: Get element refs before interacting
- **Use `--json` for parsing**: Machine-readable output for scripts
- **Session isolation**: Use `--session` for parallel workflows
- **Explicit waits**: Add `wait` commands after navigation/clicks
- **Interactive snapshots**: Use `-i` flag to reduce noise
- **Verify state**: Check element visibility before clicking
- **Screenshot on failure**: Capture state when automation fails
