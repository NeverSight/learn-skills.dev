---
name: webcli
description: Browse the web, read page content, click buttons, fill forms, take screenshots, and get accessibility snapshots using the webcli headless browser. Use when the user asks to visit a website, gather information from a web page, or interact with a web app.
allowed-tools: Bash(webcli *)
---

# webcli — Headless Browser CLI

You have access to a headless browser via the `webcli` command. Use it to navigate websites, read content, interact with elements, take screenshots, and get accessibility snapshots.

## Prerequisites

```bash
npm install -g @erdinccurebal/webcli
npx playwright install chromium
```

Homepage: https://webcli.erdinc.curebal.dev/
Repository: https://github.com/erdinccurebal/webcli

## Commands Reference

### Navigation
```bash
webcli go <url>                    # Navigate to URL (auto-starts daemon)
webcli go <url> -w networkidle     # Wait for network to settle
webcli go <url> -t mytab           # Open in named tab
webcli back                        # Go back in history
webcli forward                     # Go forward
webcli reload                      # Reload current page
```

### Reading Page Content
```bash
webcli source                      # Get full visible text of the page
webcli links                       # List all links (text + href)
webcli forms                       # List all forms with their inputs
webcli html <selector>             # Get innerHTML of element
webcli attr <selector> <attribute> # Get element attribute value
webcli eval "<js>"                 # Execute JavaScript and return result
webcli title                       # Get the page title
webcli url                         # Get the current URL
webcli value <selector>            # Get input/textarea value
webcli count <selector>            # Count matching elements
webcli box <selector>              # Get bounding box (x, y, w, h)
webcli styles <selector> [props..] # Get computed CSS styles
webcli visible <selector>          # Check if element is visible
webcli enabled <selector>          # Check if element is enabled
webcli checked <selector>          # Check if checkbox is checked
```

### Accessibility Snapshot (Recommended for AI agents)
```bash
webcli snapshot                    # Get accessibility tree with refs (@e1, @e2...)
webcli snapshot --all              # Include non-interactive elements
webcli snapshot --max-depth 5      # Limit tree depth
```

The snapshot assigns deterministic refs to interactive elements. Use these refs in other commands:
```bash
webcli snapshot                    # Get tree: [button @e1] "Submit", [textbox @e2] "Email"
webcli fill @e2 "user@example.com" # Fill using ref
webcli click @e1                   # Click using ref
```

### Interaction
```bash
webcli click "<visible text>"      # Click element by visible text
webcli click @e1                   # Click element by snapshot ref
webcli clicksel "<css selector>"   # Click element by CSS selector
webcli dblclick "<text>"           # Double-click element by visible text
webcli hover "<selector>"          # Hover over an element
webcli fill "<selector>" "<value>" # Fill an input field (preferred for forms)
webcli type "<text>"               # Type with keyboard (for focused element)
webcli select "<selector>" "<val>" # Select dropdown option
webcli press Enter                 # Press keyboard key (Enter, Tab, Escape...)
webcli focus "<selector>"          # Focus an element
webcli check "<selector>"         # Check a checkbox
webcli uncheck "<selector>"       # Uncheck a checkbox
webcli drag "<from>" "<to>"        # Drag and drop between selectors
webcli upload "<selector>" <file>  # Upload a file to input[type=file]
webcli scroll down 500             # Scroll page (up/down/left/right, px)
```

### Waiting
```bash
webcli wait "<selector>"           # Wait for CSS selector to be visible
webcli waitfor "<text>"            # Wait for text to appear on page
webcli sleep 2000                  # Sleep for N milliseconds
```

### Screenshots & PDF
```bash
webcli screenshot                  # Take full-page screenshot (returns path)
webcli screenshot -o page.png      # Save to specific file
webcli screenshot --no-full        # Viewport-only screenshot
webcli screenshot --annotate       # Screenshot with numbered interactive elements
webcli pdf                         # Save page as PDF
webcli pdf -o page.pdf             # Save PDF to specific file
```

### Console & Errors
```bash
webcli console on                  # Start capturing console messages
webcli console off                 # Stop capturing
webcli console                     # Show captured console messages
webcli errors                      # Show page errors
```

### Dialog Handling
```bash
webcli dialog accept               # Accept alert/confirm dialog
webcli dialog accept "input text"  # Accept prompt dialog with text
webcli dialog dismiss              # Dismiss dialog
```

### Frame (iframe) Switching
```bash
webcli frame "<selector>"          # Switch to an iframe
webcli frame main                  # Switch back to main frame
```

### Storage (localStorage)
```bash
webcli storage get                 # Get all localStorage
webcli storage get mykey           # Get specific key
webcli storage set mykey myvalue   # Set a value
webcli storage clear               # Clear all localStorage
```

### State Management
```bash
webcli state save session.json     # Save cookies + localStorage + sessionStorage
webcli state load session.json     # Restore full browser state
```

### Browser Settings
```bash
webcli viewport 1920 1080          # Change viewport size
webcli useragent "<string>"        # Change user agent
webcli device "iPhone 14"          # Emulate device (viewport + UA)
webcli network on                  # Start logging network requests
webcli network off                 # Stop logging
webcli network                     # Show network logs
```

### Cookie Management
```bash
webcli cookie export               # Export cookies as JSON
webcli cookie import <file>        # Import cookies from JSON file
```

### Tab & Daemon Management
```bash
webcli tabs                        # List open tabs
webcli quit                        # Close current tab
webcli quit -t mytab               # Close specific tab
webcli status                      # Show daemon info (PID, uptime, tabs)
webcli stop                        # Stop daemon and close browser
```

### Global Options
All commands support:
- `-t, --tab <name>` — target a specific tab (default: "default")
- `--json` — output as structured JSON
- `--timeout <ms>` — command timeout (default: 30000)

## Best Practices

### Recommended workflow for AI agents
1. `webcli go <url>` to navigate
2. `webcli snapshot` to get accessibility tree with refs
3. Use refs for interaction: `webcli click @e1`, `webcli fill @e2 "value"`
4. `webcli snapshot` again to see updated state
5. `webcli screenshot` if user wants visual confirmation

### Alternative workflow (text-based)
1. `webcli go <url>` to navigate
2. `webcli source` to read the page content
3. Use `webcli click`, `webcli fill`, `webcli press` to interact
4. `webcli source` again to see the result

### Form filling
- Always use `webcli fill` for input fields — it properly sets React/Vue controlled inputs
- Use `webcli click` or `webcli clicksel` for buttons
- Use `webcli press Enter` to submit forms
- After submitting, use `webcli sleep 1000` then `webcli source` to check the result

### Multi-tab browsing
```bash
webcli go https://site-a.com -t research
webcli go https://site-b.com -t reference
webcli source -t research          # Read from specific tab
webcli source -t reference
```

### Error recovery
- If a command times out, try `webcli sleep 2000` then retry
- If an element is not found, use `webcli source` to check what's on the page
- If the daemon seems stuck, use `webcli stop` then retry the command
- Use `webcli wait "<selector>"` before interacting with dynamically loaded content

## Important Notes
- Always read the page with `webcli source` or `webcli snapshot` before trying to interact
- Prefer `webcli snapshot` + refs for the most reliable element targeting
- Prefer `webcli fill` over `webcli type` for form inputs
- Prefer `webcli click` (by text) over `webcli clicksel` (by selector) when possible
- Use `webcli sleep` between rapid interactions to let pages update
- The daemon persists between commands — no need to re-navigate unless the page changes
