---
name: dev-browser
description: Browser automation. This skill enables agents to research, test web UIs, and interact with web applications using a headless browser.
---

# Dev Browser Integration

## Overview

`dev-browser` uses `agent-browser` to provide browser automation capabilities. It allows the agent to control a web browser to navigate pages, interact with elements, take screenshots, and extract information. This is essential for:
- Web research beyond simple text fetching
- Testing web applications (e.g., verifying UI changes)
- Interacting with dynamic web pages (SPA, JavaScript-heavy sites)
- Automating browser-based workflows

## Usage Guide

Use `agent-browser` for web automation. Run `agent-browser --help` for all commands.

### Common Prompts

**Navigation & Research:**
- "Go to https://example.com and summarize the pricing model."
- "Search Google for 'latest React patterns' and list the top 3 results."
- "Navigate to the local server at http://localhost:3000 and tell me what you see."

**Interaction:**
- "Click on the 'Sign Up' button."
- "Type 'hello world' into the search box and press Enter."
- "Take a screenshot of the homepage."

**Testing/Verification:**
- "Verify that the login form shows an error when I submit an empty password."
- "Check if the navigation bar is responsive on mobile view."

## Best Practices

### For Agents
1.  **Be Specific with Selectors**: When asking to click or type, describe the element clearly (e.g., "the blue 'Submit' button", "the input field labeled 'Email'").
2.  **Wait for Content**: Dynamic pages may load slowly. If an element isn't found, ask the agent to wait or check for a loading state.
3.  **Use Screenshots**: Visual verification is often better than text descriptions for UI layout issues.
4.  **Local Development**: Use `http://localhost:PORT` to test local applications. Ensure the server is running before asking the browser to visit.

### Troubleshooting

**"Element not found"**
- The page might not be fully loaded. Ask to wait or use a more robust selector description.
- The element might be inside an iframe or shadow DOM (mention this if known).

**Connection Refused (Localhost)**
- Ensure your local dev server is running (`npm start`, etc.).
- Check if the port is correct.
