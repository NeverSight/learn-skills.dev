---
name: playwright-mcp
description: Microsoft Playwright Model Context Protocol (MCP) server for local browser automation, accessibility snapshot navigation, E2E testing, and live web interaction (microsoft/playwright-mcp). Use when the agent needs to navigate websites, click elements, fill forms, execute tests, or inspect live DOM structures.
---

# Playwright MCP (Microsoft Browser Automation & Live DOM Interaction)

Based on [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp): official Microsoft Playwright Model Context Protocol (MCP) server providing structured browser automation through accessibility snapshots, bypassing the need for heavy screenshot parsing or vision-only models.

---

## 🎯 When to Use
- **Interactive Browser Automation:** Navigating web pages, clicking buttons, selecting options, typing into inputs, and submitting forms.
- **Accessibility Snapshot Navigation:** Inspecting web interfaces via structured ARIA/accessibility trees, drastically saving token context compared to full HTML dumps.
- **End-to-End (E2E) Test Execution:** Validating authentication flows, checkout flows, and user journey funnels.
- **Screenshot & Console Capture:** Taking targeted viewport screenshots and intercepting browser console logs for live debugging.

---

## 🚀 Setup & Registration

### MCP Configuration
Register Microsoft Playwright MCP in your agent's configuration (`.mcp.json` or IDE settings):

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```

---

## 🛠️ Key Capabilities & Tools
- `browser_navigate`: Navigates to any target URL and returns the parsed accessibility tree.
- `browser_click`: Clicks an element identified by its accessibility reference ID.
- `browser_type`: Types text into specified form inputs or content-editable elements.
- `browser_screenshot`: Captures full-page or element-specific screenshots.
- `browser_evaluate`: Evaluates custom JavaScript in the browser execution context.

---

## ⚡ Integration with REA & Security Workflows
- **Dynamic XSS & CSP Verification:** Navigate to test endpoints with live attack payloads to verify if CSP actively blocks script execution or if DOM-based XSS triggers alert dialogs.
- **Automated Login & Auth Flow Testing:** Automate the multi-step login flow for web applications (Clerk, Supabase, OAuth) to test authenticated routes and cookie security flags.
- **E2E Post-Fix Validation:** After implementing a security patch or header reconfiguration, run Playwright MCP to verify that the website continues to function seamlessly for real users.
