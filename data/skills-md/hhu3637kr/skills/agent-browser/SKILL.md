---
name: agent-browser
description: Headless browser automation for AI agents using agent-browser CLI. Use when Claude needs to automate web browsing, scrape web data, interact with web pages, fill forms, take screenshots, or perform any browser-based tasks. Supports reference-based element targeting, session management, and semantic locators.
---

# Agent Browser Automation

Guide for using agent-browser CLI to automate web browsing tasks in Claude Code.

## Quick Start

### Installation Check

Before using agent-browser, verify installation:

```bash
# Check if installed
agent-browser --version

# If not installed, install globally
npm install -g agent-browser
agent-browser install  # Download Chromium
```

**Windows Note**: If you encounter `/bin/sh` errors on Windows, use:
```bash
npx agent-browser <command>
```

See [troubleshooting.md](references/troubleshooting.md) for platform-specific issues.

## Core Workflow

agent-browser uses a **refs-based system** where page elements get unique identifiers (like `@e1`, `@e2`) that you can use for interactions.

### Basic Pattern

1. **Open a page**
2. **Get snapshot** with refs
3. **Interact** using refs
4. **Repeat** as needed

```bash
# 1. Navigate to page
agent-browser open example.com

# 2. Get page snapshot with interactive elements
agent-browser snapshot -i --json

# 3. Use refs from snapshot to interact
agent-browser click @e5
agent-browser fill @e3 "search query"

# 4. Take screenshot or get results
agent-browser screenshot result.png
```

## Essential Commands

### Navigation
```bash
agent-browser open <url>           # Open URL
agent-browser goto <url>           # Navigate to URL
agent-browser back                 # Go back
agent-browser forward              # Go forward
agent-browser reload               # Reload page
```

### Getting Page Information
```bash
agent-browser snapshot             # Get accessibility tree
agent-browser snapshot -i          # Interactive elements only
agent-browser snapshot -i --json   # JSON format (best for AI)
agent-browser screenshot <file>    # Take screenshot
agent-browser get text @e1         # Get element text
agent-browser get html             # Get page HTML
agent-browser get url              # Get current URL
```

### Interacting with Elements
```bash
agent-browser click @e2            # Click element by ref
agent-browser dblclick @e2         # Double click
agent-browser fill @e3 "text"      # Fill input field
agent-browser type @e3 "text"      # Type text (slower, more realistic)
agent-browser press Enter          # Press keyboard key
agent-browser check @e4            # Check checkbox
agent-browser select @e5 "option"  # Select dropdown option
agent-browser upload @e6 file.pdf  # Upload file
```

### Semantic Locators (Find Commands)
When you don't have refs, use semantic locators:

```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "user@example.com"
agent-browser find placeholder "Search..." type "query"
```

### Waiting
```bash
agent-browser wait @e1             # Wait for element
agent-browser wait --text "Done"   # Wait for text
agent-browser wait --url /success  # Wait for URL change
agent-browser wait --load          # Wait for page load
```

## Session Management

Use sessions to run multiple isolated browser instances:

```bash
# Start different sessions
agent-browser --session task1 open site-a.com
agent-browser --session task2 open site-b.com

# Each session has separate:
# - Cookies and storage
# - Authentication state
# - Navigation history

# List active sessions
agent-browser session list

# Close specific session
agent-browser --session task1 close
```

## AI Agent Workflow

For AI-driven automation, follow this pattern:

1. **Navigate and snapshot**
```bash
agent-browser open https://example.com
agent-browser snapshot -i --json > page.json
```

2. **Parse JSON to understand page structure**
   - Identify interactive elements and their refs
   - Understand page layout and available actions

3. **Execute actions using refs**
```bash
agent-browser click @e2
agent-browser fill @e5 "input data"
```

4. **Get new snapshot after page changes**
```bash
agent-browser snapshot -i --json > updated.json
```

5. **Repeat until task complete**

See [workflows.md](references/workflows.md) for detailed AI workflow patterns.

## Advanced Features

### Network Interception
```bash
# Block requests
agent-browser route --block "*.ads.com/*"

# Mock responses
agent-browser route --mock "/api/data" response.json
```

### State Persistence
```bash
# Save authentication state
agent-browser save-state auth.json

# Load state in new session
agent-browser load-state auth.json
```

### Debugging
```bash
# Enable console logs
agent-browser --console open example.com

# Highlight elements
agent-browser highlight @e3

# Enable tracing
agent-browser --trace trace.zip open example.com
```

## Best Practices

1. **Use `-i --json` for snapshots** - Reduces noise, easier for AI to parse
2. **Prefer refs over selectors** - More reliable than CSS/XPath
3. **Use sessions for parallel tasks** - Isolate different workflows
4. **Wait for elements** - Use `wait` commands to handle dynamic content
5. **Take screenshots** - Visual confirmation of state
6. **Use semantic locators as fallback** - When refs aren't available

## Common Patterns

### Form Filling
```bash
agent-browser open https://form.example.com
agent-browser snapshot -i --json
agent-browser fill @e1 "John Doe"
agent-browser fill @e2 "john@example.com"
agent-browser click @e3  # Submit button
agent-browser wait --url /success
```

### Data Extraction
```bash
agent-browser open https://data.example.com
agent-browser snapshot -i --json > structure.json
agent-browser get text @e5 > data.txt
agent-browser screenshot evidence.png
```

### Multi-Step Workflow
```bash
# Login
agent-browser open https://app.example.com/login
agent-browser fill @e1 "username"
agent-browser fill @e2 "password"
agent-browser click @e3

# Navigate to target
agent-browser wait --url /dashboard
agent-browser goto https://app.example.com/data

# Extract data
agent-browser snapshot -i --json > results.json
```

## Platform-Specific Notes

### Windows
- Use `npx agent-browser` if global command fails
- PowerShell may require quotes around URLs with special characters
- See [troubleshooting.md](references/troubleshooting.md) for `/bin/sh` errors

### Linux
- Install with dependencies: `agent-browser install --with-deps`
- May need to install Playwright system dependencies manually

### macOS
- Works out of the box after `npm install -g agent-browser`

## Reference Documentation

- **[commands.md](references/commands.md)** - Complete command reference
- **[workflows.md](references/workflows.md)** - AI workflow patterns and examples
- **[troubleshooting.md](references/troubleshooting.md)** - Common issues and solutions

## Architecture

agent-browser is built on **Playwright** with:
- Fast Rust CLI implementation (with Node.js fallback)
- Accessibility tree parsing for AI-friendly page representation
- Reference system (`@e1`, `@e2`) for stable element targeting
- Chrome DevTools Protocol (CDP) for persistent sessions

## When to Use agent-browser

✅ **Use agent-browser when:**
- Automating web browsing tasks
- Scraping data from websites
- Filling and submitting forms
- Testing web applications
- Interacting with dynamic web pages
- Need AI-friendly element targeting

❌ **Don't use agent-browser when:**
- Simple HTTP requests suffice (use curl/fetch instead)
- API endpoints are available (use API directly)
- Task doesn't require browser rendering
