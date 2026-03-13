---
name: web-browser
description: Browser automation for AI agents. Use when the user needs to interact with websites, navigate pages, fill forms, click buttons, take screenshots, extract data, test web apps, or automate any browser task. Triggers include "open a website", "fill out a form", "click a button", "take a screenshot", "scrape data", "test this web app", "login to a site", or any task requiring programmatic web interaction.
allowed-tools: Bash(npx agent-browser:*), Bash(npx playwright:*), Bash(node *)
---

# browser-automation

## Overview

Browser automation skill with two approaches:

**agent-browser** - Snapshot-based interaction model optimized for AI agents
- Compact element refs (`@e1`, `@e2`) reduce token usage dramatically
- Workflow: `open` → `snapshot -i` → interact with refs → re-snapshot
- Best for: dynamic exploration, form filling, scraping with unknown structure

**playwright** - Direct Playwright CLI and Node.js scripts
- Full Playwright API access via scripts
- Codegen for recording interactions
- Best for: scripted automation, testing, batch operations, complex workflows

## Sub-skills

CRITICAL: You MUST load the appropriate sub-skill from the `sub-skills/` directory based on user intent.

### When to use each

| Sub-skill | When to use | Triggers |
|-----------|-------------|----------|
| **agent-browser.md** | Interactive exploration, AI-driven navigation, unknown page structure | "navigate to", "fill this form", "click the button", "scrape this page", "explore the site" |
| **playwright.md** | Scripted automation, testing, batch screenshots, codegen | "write a script", "generate test", "batch screenshot", "record my actions", "create automation script" |

### Default behavior

- If user intent is unclear, prefer **agent-browser** for interactive tasks
- If user asks for "a script" or "automation code", use **playwright**
- If user mentions "codegen" or "record", use **playwright**


## Process

1. Determine user intent from their request
2. Load the appropriate sub-skill from `sub-skills/`
3. Execute the sub-skill process
4. Verify expected outcome was achieved


## Resources

- **sub-skills/**: Approach-specific instructions
  - `agent-browser.md`: Snapshot/refs workflow with npx agent-browser
  - `playwright.md`: Playwright CLI and Node.js scripts
- **references/agent-browser/**: Deep-dive documentation for agent-browser
- **templates/agent-browser/**: Ready-to-use shell scripts for agent-browser


## Quick reference

### agent-browser (default for interactive tasks)

```bash
# Session isolation (generate random slug like bright-falcon)
npx agent-browser --session <slug> open https://example.com
npx agent-browser --session <slug> snapshot -i
npx agent-browser --session <slug> click @e1
npx agent-browser --session <slug> fill @e2 "text"
```

### playwright (for scripts and codegen)

```bash
# Quick screenshot
npx playwright screenshot https://example.com output.png

# Record interactions as code
npx playwright codegen https://example.com

# PDF generation
npx playwright pdf https://example.com output.pdf
```
