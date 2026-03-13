---
name: agent-browser
description: Browser automation CLI for AI agents. Use this skill to navigate websites, interact with elements, take screenshots, and extract data using a headless browser.
triggers:
  - "browse the web"
  - "open website"
  - "check url"
  - "take screenshot"
  - "agent-browser"
  - "use browser"
---

# Agent Browser Skill

This skill provides access to the `agent-browser` CLI, a powerful tool for headless browser automation designed for AI agents.

## 🚀 Usage

The core workflow relies on **snapshots** and **refs**. Instead of guessing CSS selectors, you get a snapshot of the page with unique references (like `@e1`, `@e2`) for every interactive element.

### Basic Workflow

1.  **Navigate**: `agent-browser open <url>`
2.  **Analyze**: `agent-browser snapshot -i` (Get interactive elements with refs)
3.  **Interact**: `agent-browser click @e1` or `agent-browser fill @e2 "text"`
4.  **Repeat**: Take a new snapshot after interactions to see the updated state.

### Common Commands

-   **Open URL**: `agent-browser open google.com`
-   **Get Snapshot**: `agent-browser snapshot -i` (Interactive only, recommended)
-   **Click**: `agent-browser click @e1`
-   **Type/Fill**: `agent-browser fill @e2 "search term"`
-   **Press Key**: `agent-browser press Enter`
-   **Go Back**: `agent-browser back`
-   **Screenshot**: `agent-browser screenshot page.png`
-   **Read Text**: `agent-browser get text @e1`

### Advanced

-   **Sessions**: `agent-browser --session my-session open ...` (Keep cookies/state separate)
-   **Wait**: `agent-browser wait --text "Success"`
-   **Help**: `agent-browser --help`

## 💡 Tips for Claude

-   **Always snapshot first**: Before clicking or typing, get a fresh snapshot to ensure you have valid refs.
-   **Use `-i` flag**: `agent-browser snapshot -i` filters for interactive elements, reducing noise.
-   **Check output**: The CLI returns JSON or text. Read it to confirm actions succeeded.
