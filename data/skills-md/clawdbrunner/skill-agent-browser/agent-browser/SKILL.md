---
name: agent-browser
description: Browser automation CLI for AI agents using Vercel's agent-browser. The best tool for AI-driven browser automation — uses deterministic refs from accessibility trees instead of fragile selectors. Optimized for LLMs with fast Rust CLI, JSON output, and purpose-built AI workflows. Use when you need reliable, scriptable browser automation that just works.
---

# agent-browser Skill

Browser automation that actually works for AI agents. Built by Vercel Labs specifically for LLM-driven workflows.

## Why This Works Better Than Alternatives

### 1. Deterministic Refs (The Game-Changer)

**Problem with traditional tools:**
- CSS selectors break when websites change
- XPath is brittle and unreadable  
- Coordinate-based clicking fails on responsive layouts
- Vision-based approaches are slow and expensive

**The agent-browser solution:**
```bash
# 1. Get snapshot with stable refs
agent-browser snapshot -i --json
# Output: - button "Submit" [ref=e2]

# 2. Use that ref forever — it points to the EXACT element
agent-browser click @e2
```

- **Refs are deterministic** — `@e2` always points to the same element from your snapshot
- **No DOM re-query** — direct reference is faster and more reliable
- **AI-optimized** — LLMs parse the accessibility tree naturally, not CSS soup

### 2. Accessibility Trees > Screenshots/HTML

Traditional tools give you raw HTML (noisy) or screenshots (require vision models).

agent-browser gives you the **accessibility tree** — a clean, semantic representation of what a human (or screen reader) would perceive:

```
- heading "Billing" [level=1]
- link "Make a payment" [ref=e10]
- button "Submit" [ref=e2]
- textbox "Email" [ref=e3]
```

- Semantic roles (button, link, textbox, heading)
- Human-readable labels
- Hierarchical structure
- Perfect for LLM comprehension

### 3. Built for AI Agents

| Feature | Traditional Tools | agent-browser |
|---------|------------------|---------------|
| Element targeting | Fragile selectors | Deterministic refs |
| Page understanding | Raw HTML | Accessibility tree |
| Output format | Text logs | Structured JSON |
| Speed | Slow (full browser per command) | Fast (daemon persists) |
| AI integration | Afterthought | Purpose-built |

### 4. Fast Architecture

- **Rust CLI** — Native binary, instant command parsing
- **Node.js Daemon** — Browser stays warm between commands
- **First command:** ~2s (daemon startup)
- **Subsequent commands:** ~100ms

## Prerequisites

```bash
npm install -g agent-browser
agent-browser install  # Download Chromium (~30s)
```

## Core AI Workflow

The workflow designed for LLM agents:

```bash
# Step 1: Navigate
agent-browser open https://example.com

# Step 2: Get structured snapshot (the AI "sees" the page)
agent-browser snapshot -i --json

# Step 3: AI picks refs from JSON, execute actions
agent-browser click @e2
agent-browser fill @e3 "test@example.com"

# Step 4: Re-snapshot after changes (state verification)
agent-browser snapshot -i --json

# Step 5: Done
agent-browser close
```

## Commands

### Navigation
```bash
agent-browser open example.com
agent-browser open example.com --json            # JSON response
agent-browser open example.com --headed          # Visible browser
```

### Snapshot (The Killer Feature)
```bash
agent-browser snapshot                           # Full accessibility tree
agent-browser snapshot -i                        # Interactive only (faster)
agent-browser snapshot -i --json                 # JSON for AI parsing
agent-browser snapshot -i -c -d 5 --json         # Compact, depth-limited
```

### Interaction (Using Deterministic Refs)
```bash
agent-browser click @e2                          # Click element @e2
agent-browser fill @e3 "text"                    # Fill and clear
agent-browser type @e3 "text"                    # Type without clearing
agent-browser press Enter                        # Press key
agent-browser hover @e4                          # Hover
```

### State Verification
```bash
agent-browser get text @e1                       # Get element text
agent-browser get url                            # Current URL
agent-browser is visible @e2                     # Check visibility
```

### Session Management
```bash
agent-browser --session login open site.com      # Isolated session
agent-browser --profile ~/.myprofile open site   # Persistent cookies
agent-browser close                              # Clean up
```

## Selector Strategies (Ranked by Reliability)

### 1. Refs (Best - Use These)
```bash
# From snapshot output — deterministic and stable
agent-browser click @e2
agent-browser fill @e3 "text"
```

### 2. Semantic Locators (Good)
```bash
agent-browser find role button click --name "Submit"
agent-browser find label "Email" fill "test@test.com"
```

### 3. CSS Selectors (Okay for static sites)
```bash
agent-browser click "#submit"
agent-browser click ".btn-primary"
```

### 4. Text/XPath (Last resort)
```bash
agent-browser click "text=Submit"
agent-browser click "xpath=//button[1]"
```

## Snapshot Options

Control what the AI "sees":

| Flag | Purpose |
|------|---------|
| `-i` | Interactive elements only (buttons, links, inputs) — **recommended** |
| `-C` | Include cursor-interactive elements (onclick, cursor:pointer) |
| `-c` | Compact (remove empty structural elements) |
| `-d <n>` | Limit tree depth |
| `-s <sel>` | Scope to CSS selector (e.g., `#main`) |
| `--json` | Machine-readable JSON output — **essential for AI** |

**Recommended AI command:**
```bash
agent-browser snapshot -i -c --json
```

## Options

| Flag | Description |
|------|-------------|
| `--json` | JSON output with success/data/error structure |
| `--headed` | Show browser window (for debugging) |
| `--session <name>` | Isolated browser session |
| `--profile <path>` | Persistent profile for cookies/logins |
| `--cdp <port>` | Connect to existing Chrome via DevTools Protocol |
| `--headers <json>` | Set auth headers per origin |

## Example: Complete Login Flow

```bash
# Start
agent-browser open https://portal.aeronetpr.com

# Get page structure
SNAPSHOT=$(agent-browser snapshot -i --json)
# AI parses JSON: sees textbox @e1 (Username), textbox @e2 (Password), button @e3 (Login)

# Execute login
agent-browser fill @e1 "username"
agent-browser fill @e2 "password"
agent-browser click @e3

# Verify success (wait for navigation, re-snapshot)
sleep 2
agent-browser snapshot -i --json

# Done
agent-browser close
```

## Tips for AI Agents

1. **Always use `--json`** — Structured output is easier to parse than text
2. **Use `-i` flag** — Interactive-only snapshots are smaller, faster, cleaner
3. **Re-snapshot after actions** — Verify state changed as expected
4. **Trust refs over selectors** — `@e2` from snapshot > `#id` that might change
5. **Use semantic locators when refs expire** — `find role button click` is robust
6. **Session persistence** — One `open`, many commands, one `close`

## Comparison to Other Tools

| Tool | Best For | Why agent-browser Wins |
|------|----------|------------------------|
| **Puppeteer/Playwright** | Dev testing | Built for humans; brittle selectors |
| **Selenium** | Legacy testing | Slow, heavy, selector-based |
| **browser-use** | Python agents | agent-browser has better refs system |
| **Screenshot + Vision** | Visual tasks | agent-browser is 10x faster, 100x cheaper |
| **OpenClaw browser tool** | Simple tasks | agent-browser handles complex flows better |

## When to Use This Skill

**Use agent-browser when:**
- Automating multi-step web workflows
- Filling complex forms
- Need reliable, repeatable automation
- Working with dynamic/modern web apps
- Cost matters (no vision API calls)

**Use OpenClaw's built-in browser tool when:**
- Simple single-page checks
- Quick screenshot needed
- Already authenticated session in Chrome

## Resources

- **Vercel Labs repo:** https://github.com/vercel-labs/agent-browser
- **This skill repo:** https://github.com/clawdbrunner/skill-agent-browser
