---
name: playwright
description: Browser automation for web testing and interaction. Use for navigating pages, filling forms, clicking elements, taking screenshots, and inspecting page content. Maintains stateful browser session across commands.
allowed-tools: Bash, Read
---

# Playwright Browser Automation Skill

Use **playwright-server** for browser automation via curl commands. The server maintains a stateful browser session.

## Prerequisites

The server is installed at `~/.claude/bin/playwright-server.js`. If not present:

```bash
cd ~/.claude/bin
npm init -y
npm install playwright
npx playwright install chromium
```

## Server Lifecycle

```bash
# Start server (if not running)
curl -sf localhost:3210/health || (node ~/.claude/bin/playwright-server.js &>/dev/null & sleep 1)

# Check health
curl -sf localhost:3210/health

# Stop server
pkill -f playwright-server
```

## Quick Reference

| Task | Command |
|------|---------|
| Start browser | `curl -s localhost:3210 -d '{"cmd":"start"}'` |
| Navigate | `curl -s localhost:3210 -d '{"cmd":"navigate","url":"URL"}'` |
| Get snapshot | `curl -s localhost:3210 -d '{"cmd":"snapshot"}'` |
| Click | `curl -s localhost:3210 -d '{"cmd":"click","selector":"SEL"}'` |
| Fill input | `curl -s localhost:3210 -d '{"cmd":"fill","selector":"SEL","value":"VAL"}'` |
| Screenshot | `curl -s localhost:3210 -d '{"cmd":"screenshot"}'` |
| Stop browser | `curl -s localhost:3210 -d '{"cmd":"stop"}'` |

## Core Commands

### Browser Lifecycle

```bash
curl -s localhost:3210 -d '{"cmd":"start"}'              # Headless
curl -s localhost:3210 -d '{"cmd":"start","headless":false}'  # Headed
curl -s localhost:3210 -d '{"cmd":"stop"}'
curl -s localhost:3210 -d '{"cmd":"status"}'
```

### Navigation

```bash
curl -s localhost:3210 -d '{"cmd":"navigate","url":"http://localhost:3000"}'
curl -s localhost:3210 -d '{"cmd":"back"}'
curl -s localhost:3210 -d '{"cmd":"reload"}'
```

### Page Inspection

**snapshot** - Get accessibility tree (use to understand page structure):

```bash
curl -s localhost:3210 -d '{"cmd":"snapshot"}'
```

Example output:
```
- heading "Page Title" [level=1]
- navigation:
  - link "Home"
  - link "About"
- main:
  - textbox "Email"
  - textbox "Password"
  - button "Sign In"
```

**screenshot** - Capture page:

```bash
curl -s localhost:3210 -d '{"cmd":"screenshot"}'
curl -s localhost:3210 -d '{"cmd":"screenshot","path":"/tmp/shot.png"}'
curl -s localhost:3210 -d '{"cmd":"screenshot","fullPage":true}'
```

### Basic Interactions

```bash
curl -s localhost:3210 -d '{"cmd":"click","selector":"button[type=submit]"}'
curl -s localhost:3210 -d '{"cmd":"fill","selector":"input[name=email]","value":"test@example.com"}'
curl -s localhost:3210 -d '{"cmd":"type","selector":"input","text":"query"}'
curl -s localhost:3210 -d '{"cmd":"press","key":"Enter"}'
```

### Waiting

```bash
curl -s localhost:3210 -d '{"cmd":"wait","selector":".loaded"}'
curl -s localhost:3210 -d '{"cmd":"wait","selector":".spinner","state":"hidden"}'
curl -s localhost:3210 -d '{"cmd":"waitUrl","pattern":"**/dashboard"}'
curl -s localhost:3210 -d '{"cmd":"waitLoad","state":"networkidle"}'
```

## Selector Basics

```bash
# CSS selectors
"button[type=submit]"
"#login-form input[name=email]"

# Text selectors
"text=Sign In"

# Role selectors
"role=button[name='Sign In']"

# Combining
"#form >> input[name=email]"
```

**For complete selector strategies**: See [references/selectors.md](references/selectors.md)

## Additional References

- **All commands**: See [references/commands.md](references/commands.md) for interaction, inspection, wait, tab, and dialog commands
- **Selectors**: See [references/selectors.md](references/selectors.md) for selector strategies
- **Workflows**: See [references/workflows.md](references/workflows.md) for common workflows and troubleshooting
