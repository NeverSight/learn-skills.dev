---
name: playwright-mcp
description: "Live browser interaction via Playwright MCP — navigate pages, click buttons, fill forms, take screenshots."
metadata:
  version: 1.0.0
  mcp-server: playwright
---

# Playwright MCP Browser Automation

You are an expert at using the Playwright MCP server for live browser interaction. This skill teaches you to navigate pages, inspect elements, fill forms, and debug web UIs through direct browser control.

## Critical: These Are Direct Tool Calls

MCP tools are **direct tool calls** — exactly like `Read`, `Grep`, or `Bash`. They are NOT CLI commands.

**CORRECT** — call the tool directly:
```
Tool: mcp__playwright__browser_navigate
Parameters: { "url": "http://localhost:3010" }
```

**WRONG** — do NOT shell out:
```
Bash: claude mcp call playwright browser_navigate ...  # This does not work
```

All Playwright MCP tools use the `mcp__playwright__` prefix.

## Critical: Always Snapshot Before Interacting

`browser_snapshot` returns an accessibility tree with `ref` values for every interactive element. You **must** snapshot before clicking, typing, or hovering — the `ref` values are required for all interaction tools.

## Critical: Output Size Awareness

| Tool | Output Size | Notes |
|------|------------|-------|
| `browser_snapshot` | Medium-Large | Full accessibility tree — scales with page complexity |
| `browser_take_screenshot` | Large | Base64 image — use sparingly |
| `browser_console_messages` | Variable | Can be very large on noisy apps |
| `browser_network_requests` | Variable | Can be very large on API-heavy pages |
| `browser_navigate` | Small | Returns page title only |
| `browser_click` | Small | Returns snapshot after click |
| `browser_type` | Small | Returns snapshot after typing |

Prefer `browser_snapshot` over `browser_take_screenshot` for understanding page structure. Screenshots are for visual verification only.

## Workflow 1: Navigate & Inspect

**Trigger:** User says "open this page", "what's on the page?", "inspect the UI", "check the layout"

### Steps

1. **Navigate to the page:**
   ```
   browser_navigate({ url: "http://localhost:3010/home/team-slug/settings" })
   ```

2. **Get page structure** (always do this before interacting):
   ```
   browser_snapshot → accessibility tree with ref values for all elements
   ```

3. **Analyze the snapshot:** Identify interactive elements (buttons, links, inputs) by their `ref` values. Report page structure to user.

### Decision: Snapshot vs Screenshot

| Need | Use |
|------|-----|
| Understand page structure, find elements | `browser_snapshot` (structured, has `ref` values) |
| Visual appearance, layout bugs, CSS issues | `browser_take_screenshot` (visual image) |
| Both structure and appearance | Snapshot first, then screenshot if visual check needed |

## Workflow 2: Form Interaction

**Trigger:** User says "fill out the form", "submit the login", "type in the field", "select an option"

### Steps

1. **Snapshot to find form fields:**
   ```
   browser_snapshot → identify input refs and their labels
   ```

2. **Fill fields** (choose based on complexity):
   - **Single field:** `browser_type({ ref: "input-ref", text: "value" })`
   - **Multiple fields:** `browser_fill_form({ fields: [{ ref: "ref1", value: "val1" }, { ref: "ref2", value: "val2" }] })`
   - **Dropdown:** `browser_select_option({ ref: "select-ref", values: ["option-value"] })`

3. **Submit the form:**
   ```
   browser_click({ ref: "submit-button-ref" })
   ```

4. **Verify result:**
   ```
   browser_snapshot → check for success message, error states, or navigation
   ```

### Key Patterns

- `browser_fill_form` is faster than multiple `browser_type` calls for multi-field forms
- Use `browser_press_key({ key: "Enter" })` as alternative to clicking submit
- After submission, wait if needed: `browser_wait_for({ text: "Success" })` then snapshot

## Workflow 3: Debug Investigation

**Trigger:** User says "debug the page", "check for errors", "what API calls are happening?", "why isn't it working?"

### Steps

1. **Navigate to the problematic page:**
   ```
   browser_navigate({ url: "..." })
   ```

2. **Run these in parallel** (they are independent):
   ```
   browser_console_messages → JavaScript errors, warnings, logs
   browser_network_requests → API calls, failed requests, status codes
   ```

3. **Snapshot the page:**
   ```
   browser_snapshot → current UI state, error messages, loading states
   ```

4. **Investigate further:**
   ```
   browser_evaluate({ expression: "document.querySelectorAll('.error').length" }) → run custom JS
   ```

## Workflow 4: Multi-Step Navigation

**Trigger:** User says "go through the flow", "test the signup process", "walk through the wizard"

### Steps

1. **Navigate to starting page:**
   ```
   browser_navigate({ url: "..." })
   ```

2. **For each step:**
   ```
   browser_snapshot → find the next action
   browser_click({ ref: "..." }) or browser_type({ ref: "...", text: "..." })
   browser_wait_for({ text: "expected content" }) → if page loads async
   ```

3. **Handle dialogs if they appear:**
   ```
   browser_handle_dialog({ accept: true }) → confirm/alert/prompt
   ```

4. **Go back if needed:**
   ```
   browser_navigate_back
   ```

## Tool Reference

### Navigation
| Tool | Purpose | Parameters |
|------|---------|------------|
| `browser_navigate` | Go to URL | `url` (required) |
| `browser_navigate_back` | Go back | None |
| `browser_wait_for` | Wait for text or time | `text` or `timeout` (ms) |
| `browser_tabs` | List/switch tabs | None or `index` to switch |

### Inspection
| Tool | Purpose | Parameters |
|------|---------|------------|
| `browser_snapshot` | Accessibility tree with refs | None |
| `browser_take_screenshot` | Visual screenshot | None |
| `browser_console_messages` | JS console output | None |
| `browser_network_requests` | Network activity | None |

### Interaction
| Tool | Purpose | Parameters |
|------|---------|------------|
| `browser_click` | Click element | `ref` (from snapshot) |
| `browser_type` | Type text | `ref`, `text` |
| `browser_fill_form` | Fill multiple fields | `fields` array of `{ ref, value }` |
| `browser_select_option` | Select dropdown | `ref`, `values` array |
| `browser_hover` | Hover element | `ref` |
| `browser_drag` | Drag and drop | `startRef`, `endRef` |
| `browser_press_key` | Keyboard input | `key` (e.g., "Enter", "Tab") |
| `browser_file_upload` | Upload file | `ref`, `paths` array |
| `browser_handle_dialog` | Confirm/dismiss dialog | `accept` boolean |

### Advanced
| Tool | Purpose | Parameters |
|------|---------|------------|
| `browser_evaluate` | Run JavaScript | `expression` |
| `browser_resize` | Resize viewport | `width`, `height` |
| `browser_close` | Close page | None |
| `browser_install` | Install browser | None |
| `browser_run_code` | Run Playwright code | `code` string |

## Troubleshooting

### "No browser running" or Connection Errors

The Playwright MCP server manages its own browser instance. If tools fail:
1. Try `browser_install` to ensure the browser binary is available
2. Try `browser_navigate` to a simple URL — this may initialize the browser

### Elements Not Found After Navigation

Pages with async content may not have rendered yet:
1. Use `browser_wait_for({ text: "expected content" })` before snapshot
2. Use `browser_wait_for({ timeout: 2000 })` for time-based waiting

### Proxied or Internal Domains

The MCP browser cannot reach proxied or internal domains that require network tunnels. Use `http://127.0.0.1:54321` directly for local Supabase.

### Snapshot Returns Very Large Output

Complex pages produce large accessibility trees. If output is too large:
1. Navigate to a specific sub-page rather than the full app
2. Use `browser_evaluate` to query specific elements instead
