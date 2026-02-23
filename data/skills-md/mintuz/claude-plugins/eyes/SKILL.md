---
name: eyes
description: WHEN users express dissatisfaction with visual appearance or behavior; use Playwright MCP to capture screenshots and collaborate on UI fixes with a structured feedback loop.
---

# Eyes - Visual Feedback Loop

Use Playwright MCP to capture screenshots and collaborate with users on visual refinements. Always confirm before making changes.

## Workflow

1. **Capture current state** — Use Playwright MCP `browser_take_screenshot` to capture the current page or element to better understand the users questions or requirements.

2. **Gather specific feedback** — Ask what needs adjustment: "Looking at this screenshot, what specifically would you like changed?"

3. **Propose changes clearly** — Describe intended modifications with specifics:
   - Bad: "I'll fix the spacing"
   - Good: "I'll increase the gap between cards from 16px to 24px and add 32px padding to the container"

4. **Confirm before implementing** — Use AskUserQuestion to get explicit approval. Never modify code without confirmation.

5. **Verify with comparison** — After changes, capture a new screenshot to confirm the fix has been made.

## Playwright MCP Tools

Use these Playwright MCP tools for the visual feedback loop:

- `browser_navigate` — Navigate to a URL
- `browser_take_screenshot` — Take a screenshot of the current page
- `browser_snapshot` — Capture accessibility snapshot of the current page (useful for understanding structure)
- `browser_click` — Perform click on a web page
- `browser_hover` — Hover over element on page
- `browser_wait_for` — Wait for text appearance/disappearance or specified duration
- `browser_console_messages` — Returns all console messages (useful for debugging)
- `browser_resize` — Resize the browser window (useful for responsive testing)
- `browser_install` — Install the browser specified in the config

## Related Skills

When implementing visual changes, load these skills for guidance:

- **`web:css`** — CSS architecture, spacing, units, and selector patterns
- **`web:web-design`** — Visual hierarchy, typography, color, and component polish

## Before/After Comparison

After implementing changes:

1. Take a new screenshot of the same element/page
2. Present both screenshots side by side
3. Ask: "Does this match what you were looking for?"
4. If not, repeat the feedback loop
