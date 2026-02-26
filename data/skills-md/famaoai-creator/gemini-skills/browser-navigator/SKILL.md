---
name: browser-navigator
description: Automates browser actions using Playwright CLI. Can record, replay, and generate browser automation scenarios stored in the knowledge base. Useful for UI testing, data extraction, and visual auditing.
status: implemented
arguments:
  - name: url
    short: u
    type: string
    description: URL to navigate to
  - name: scenario
    short: s
    type: string
    description: Path to Playwright spec file
  - name: screenshot
    type: boolean
    description: Take a screenshot
  - name: extract
    type: string
    description: CSS selector to extract text from
  - name: out
    short: o
    type: string
    description: Output file path
category: Integration & API
last_updated: '2026-02-13'
tags:
  - automation
  - compliance
  - data-engineering
  - gemini-skill
  - qa
---

# Browser Navigator (Playwright-based)

This skill automates web browser interactions using the Playwright CLI. It focuses on executing scenarios stored in `knowledge/browser-scenarios/` and generating new ones as needed.

## Capabilities

### 1. Scenario Execution

Run existing Playwright test scripts to perform complex multi-step actions.

- **Command**: `npx playwright test <path_to_spec>`
- **Results**: Check output logs and screenshots saved in `work/screenshots/`.

### 2. Scenario Generation

Create new automation scripts (`.spec.js`) based on user requirements.

- **Workflow**:
  1.  Define the goal (e.g., "Log in and export the table").
  2.  Draft the Playwright script using `@playwright/test` syntax.
  3.  Save the script to `knowledge/browser-scenarios/` for future use.
  4.  Verify by running it.

### 3. Visual & Content Auditing

- Capture full-page screenshots for UI review.
- Extract text content or specific DOM elements for analysis.

## Knowledge Base

- **Scenarios**: `knowledge/browser-scenarios/`
  - Always check this directory first for reusable scripts before creating new ones.
  - New scripts should be named descriptively (e.g., `github-login.spec.js`).

## Usage Examples

- "Run the example scenario and show me the screenshot."
- "Create a new scenario to visit 'https://news.ycombinator.com', capture the top 10 titles, and save it as `hacker-news.spec.js`."
- "Debug the UI of my local dev server at localhost:3000."

## Safety & Best Practices

- **Privacy**: Never hardcode credentials. Use environment variables if necessary.
- **Paths**: Always save screenshots to `work/screenshots/`.
- **Cleanup**: Close browser contexts properly (Playwright handles this in `test` blocks).
- **Environment**: If Playwright is not installed, prompt the user to run `npm install -D @playwright/test`.

## Troubleshooting

| Error                                             | Cause                                | Fix                                            |
| ------------------------------------------------- | ------------------------------------ | ---------------------------------------------- |
| `Cannot find module '@playwright/test'`           | Playwright not installed             | Run `npm install -D @playwright/test`          |
| `browserType.launch: Executable doesn't exist`    | Browser binaries missing             | Run `npx playwright install chromium`          |
| `Target page, context or browser has been closed` | Navigation timeout                   | Increase timeout or check URL validity         |
| `net::ERR_CONNECTION_REFUSED`                     | Target server not running            | Start the local dev server first               |
| `EPERM: operation not permitted`                  | File permission issue on screenshots | Check write permissions on `work/screenshots/` |

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
