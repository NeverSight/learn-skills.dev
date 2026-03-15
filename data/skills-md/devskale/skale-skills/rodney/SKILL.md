---
name: rodney
description: Chrome automation from CLI using rodney tool. Drive headless Chrome for web scraping, testing, screenshots, form filling, navigation, and accessibility checks. Use when user wants to automate browser interactions, scrape websites, take screenshots, test web pages, fill forms, or check accessibility. Supports persistent Chrome sessions, multi-step workflows, and shell scripting integration.
---

# Rodney - Chrome Automation

Rodney drives a persistent headless Chrome instance from the command line. Each command connects to the same long-running Chrome process, enabling multi-step browser interactions from shell scripts.

## Quick Start

```bash
rodney start                    # Launch headless Chrome
rodney open https://example.com # Navigate to URL
rodney title                    # Print page title
rodney text "h1"                # Extract text from element
rodney screenshot page.png      # Take screenshot
rodney stop                     # Shut down Chrome
```

## Installation

**Before using this skill, ensure rodney is installed and in PATH.**

Verify installation:
```bash
which rodney && rodney --version
```

If not found, install using one of these methods:

### Option 1: uv (recommended)
```bash
uv tool install rodney
```

Update to latest:
```bash
uv tool upgrade rodney
```

Or with pipx:
```bash
pipx install rodney
pipx upgrade rodney
```

### Option 2: Build from source (requires Go 1.21+)
```bash
git clone https://github.com/simonw/rodney
cd rodney
go build -o rodney .
sudo mv rodney /usr/local/bin/
```

Update to latest:
```bash
cd rodney
git pull
go build -o rodney .
sudo mv rodney /usr/local/bin/
```

### Option 3: pip in virtual environment
```bash
uv pip install rodney
# Ensure venv is activated before using rodney
source .venv/bin/activate
```

Update to latest:
```bash
source .venv/bin/activate
uv pip install --upgrade rodney
```

### Chrome/Chromium Requirement

Rodney requires Chrome or Chromium. Set path if not at default:

```bash
# macOS
export ROD_CHROME_BIN="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Linux (usually auto-detected)
export ROD_CHROME_BIN="/usr/bin/google-chrome"
```

## Core Workflows

### Web Scraping

```bash
rodney start
rodney open https://example.com
rodney waitstable
title=$(rodney title)
content=$(rodney text "article")
links=$(rodney js 'Array.from(document.querySelectorAll("a")).map(a => a.href)')
rodney stop
```

### Form Interaction

```bash
rodney start
rodney open https://example.com/login
rodney input "#email" "user@example.com"
rodney input "#password" "secret"
rodney click "button[type=submit]"
rodney waitload
rodney stop
```

### Screenshots & PDFs

```bash
rodney start
rodney open https://example.com
rodney screenshot -w 1920 -h 1080 full-page.png
rodney screenshot-el ".chart" chart.png
rodney pdf output.pdf
rodney stop
```

### Accessibility Testing

```bash
rodney start
rodney open https://example.com
rodney ax-tree --depth 3           # Dump accessibility tree
rodney ax-find --role button       # Find all buttons
rodney ax-find --role button --json | python3 -c "
import json, sys
buttons = json.load(sys.stdin)
unnamed = [b for b in buttons if not b.get('name', {}).get('value')]
if unnamed:
    print(f'FAIL: {len(unnamed)} buttons missing accessible names')
    sys.exit(1)
print(f'PASS: all {len(buttons)} buttons have accessible names')
"
rodney stop
```

### CI/CD Assertions

Rodney uses exit codes: 0=success, 1=check failed, 2=error.

```bash
#!/bin/bash
set -euo pipefail

rodney start
rodney open "https://myapp.com"
rodney waitstable

# These exit 1 if condition fails, 0 if passes
rodney exists "h1"
rodney visible "#main-content"
rodney assert 'document.title' 'My App'
rodney assert 'document.querySelector(".logged-in") !== null'

rodney stop
```

## Session Types

**Global session** (default): State in `~/.rodney/`
```bash
rodney start
rodney open https://example.com
```

**Local session**: State in `./.rodney/` (per-project isolation)
```bash
rodney start --local
rodney open https://example.com
```

Auto-detection: If `./.rodney/state.json` exists, local session is used.

## Waiting Strategies

| Command | Use Case |
|---------|----------|
| `wait <selector>` | Wait for element to appear |
| `waitload` | Wait for page load event |
| `waitstable` | Wait for DOM to stop changing |
| `waitidle` | Wait for network idle |
| `sleep <seconds>` | Fixed delay |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `RODNEY_HOME` | `~/.rodney` | Data directory |
| `ROD_CHROME_BIN` | `/usr/bin/google-chrome` | Chrome binary path |
| `ROD_TIMEOUT` | `30` | Element query timeout (seconds) |

## Full Command Reference

See [references/commands.md](references/commands.md) for complete command list with all options.
