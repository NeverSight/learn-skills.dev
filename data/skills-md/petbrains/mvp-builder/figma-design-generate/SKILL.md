---
name: figma-design-generate
description: >
  Capture UI and send it to Figma as editable design layers using generate_figma_design.
  Use when someone says "push to Figma", "send to Figma", "capture UI", "code to canvas",
  "sync with Figma", "update Figma file", or wants to send implemented UI to Figma for
  designer review. Also trigger after completing a feature build when the workflow includes
  Figma roundtrip (Figma → code → Figma). Covers only the code-to-Figma direction —
  for reading from Figma, use get_metadata or get_screenshot tools directly.
allowed-tools: Read, Write, Bash(*), mcp__figma__generate_figma_design
---

# Figma Design Generate

Capture UI and send it to Figma as fully editable design layers — real frames, components, auto-layout, and text layers, not flat screenshots.

The tool is remote only, exempt from standard Figma MCP rate limits, and works with Figma Design files.

## When to Use

- User says "push to Figma", "send to Figma", "capture UI", "code to canvas", "sync Figma"
- After building or implementing a feature — send result to designers for review
- Syncing a Figma file with the current implementation state
- Roundtrip workflow: Figma → code → Figma → designer refines → code again

## Process

### 1. Determine the target

Three destination options:

**New Figma file** — default when no file specified. Created in the user's team or organization drafts. The tool will ask the user which Figma organization or team to use.

**Existing Figma Design file** — user provides a Figma file URL. Requires edit permissions. If the URL doesn't point to a Figma Design file, a new file is created instead.

**Clipboard** — user wants to paste layers into a Figma file manually.

### 2. Call generate_figma_design

Prompt the tool with a clear description of what to capture and where to send it.

**Example prompts to the tool:**
- New file: `"Start a local server for my app and capture the UI in a new Figma file."`
- Existing file: `"Start a local server for my app and capture the UI in <Figma file URL>."`
- Clipboard: `"Start a local server for my app and use the Figma MCP server to capture the UI to my clipboard."`

If a local server is already running, omit the "Start a local server" part — the tool can infer it, but being specific the first time helps.

The tool handles everything: starts the server if needed, injects the capture script, and opens a browser window. An initial capture happens automatically when the browser window opens.

### 3. User interacts with the capture toolbar

In the opened browser window, a toolbar appears with two options:
- **Entire screen** — captures the full current state of the interface
- **Select element** — lets the user pick a specific element to capture

The user controls this toolbar. Wait for them to complete.

### 4. Finish the capture

- If capturing to a Figma Design file — user clicks **Open file** to view the result
- If capturing to clipboard — user pastes the design layers into any Figma file
- The agent can also complete the process via a follow-up prompt

## Decision Rules

| Situation | Action |
|-----------|--------|
| User provides Figma URL | Use as existing file target |
| No target specified | Default to new file — tool asks user for org/team |
| Multiple pages or states needed | Call tool again for each — it reuses the same file within the conversation |
| User says "also capture checkout" after first capture | No need to re-specify the file — tool infers same target |
| Capturing from a live web app or production site | Prompt the tool to use Playwright to inject the required script |
| Capturing from local dev server | No extra steps — tool handles injection directly |
| User wants to capture responsive variants | Resize the viewport in the browser between captures |

## Tips for Best Results

**Be descriptive about what to capture.** "Capture the checkout flow" works better than "Capture this" — helps organize frames in Figma.

**Capture strategically.** Focus on key screens and important states (empty, error, filled) rather than every page. Responsive breakpoints are valuable for designer review.

**Sequential captures reuse the target.** After the first capture to a file, subsequent prompts like "Also capture the account screen" automatically go to the same file. The tool infers this, or asks for confirmation.

**Existing file suggestions.** When capturing to an existing file, the tool can suggest recent files the user has created or edited.

**Design tokens alignment.** If the project uses design tokens aligned with Figma variables, the captured layers will reference correct tokens — makes designer review faster.