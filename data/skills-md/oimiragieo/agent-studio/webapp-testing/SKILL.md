---
name: webapp-testing
description: Test local web applications using Playwright with Python. Verify frontend functionality, debug UI behavior, capture screenshots, and view browser console logs. Supports static HTML files, dynamic webapps with running servers, and automated test generation.
version: 1.1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Bash, Glob, Grep]
args: '<target-url|html-file> [--screenshot] [--headless] [--test-plan <path>]'
agents: [qa, frontend-pro, developer]
category: 'Testing'
tags: [testing, playwright, browser, e2e, webapp, frontend, ui, screenshots]
best_practices:
  - Always run helper scripts with --help first before reading source code
  - Wait for networkidle state before inspecting dynamic content
  - Use CSS selectors over XPath for element discovery
  - Capture screenshots at key interaction points for visual verification
  - Check browser console logs for JavaScript errors alongside visual checks
error_handling: graceful
streaming: supported
verified: true
lastVerifiedAt: '2026-03-01'
---

# Web Application Testing Skill

<!-- Agent: evolution-orchestrator | Task: #2 | Session: 2026-02-21 -->
<!-- Source: Anthropic (github.com/anthropics/skills) -->
<!-- Attribution: Adapted from Anthropic webapp-testing skill -->

<identity>
Web application testing toolkit adapted from Anthropic's official skills repository. Provides systematic methodology for testing local web applications using Playwright with Python. Covers frontend verification, UI debugging, screenshot capture, and browser console log analysis.
</identity>

<capabilities>
- Local web application testing with Playwright (Python)
- Frontend functionality verification
- UI behavior debugging and inspection
- Browser screenshot capture at key interaction points
- Browser console log viewing and error detection
- Static HTML file testing (direct read + selector identification)
- Dynamic webapp testing with server lifecycle management
- Automated test script generation
- Element discovery and CSS selector identification
- Page load state management (networkidle, domcontentloaded, load)
</capabilities>

## Overview

This skill adapts Anthropic's webapp-testing skill for the agent-studio framework. It provides a systematic approach to testing web applications locally using Playwright, choosing the right strategy based on the type of web content being tested.

**Source repository**: `https://github.com/anthropics/skills`
**License**: MIT
**Tool**: Playwright (Python API)

## When to Use

- When verifying frontend functionality of a web application
- When debugging UI behavior or visual rendering issues
- When capturing screenshots for visual regression testing
- When checking browser console for JavaScript errors
- When testing form submissions, navigation flows, and interactive elements
- When generating automated test scripts for web applications

## Iron Law

```
NEVER INSPECT DOM BEFORE WAITING FOR NETWORKIDLE ON DYNAMIC APPS
```

Dynamic web applications load content asynchronously. Inspecting the DOM before the page has stabilized will produce incorrect or incomplete results. Always call `page.wait_for_load_state('networkidle')` before inspecting rendered content on dynamic apps.

## Decision Tree: Choose Your Approach

```
Is the target a static HTML file?
  YES → Approach A: Direct Read
  NO → Is there a running dev server?
    YES → Approach B: Reconnaissance-then-Action
    NO → Approach C: Helper Script First
```

### Approach A: Static HTML Files

For static HTML files that do not require a server:

1. Read the HTML file directly
2. Identify CSS selectors for elements of interest
3. Write a Playwright script to open the file and verify content

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(f"file://{abs_path_to_html}")

    # Verify content
    title = page.title()
    assert title == "Expected Title"

    # Check element exists
    element = page.query_selector("h1.main-heading")
    assert element is not None

    # Capture screenshot
    page.screenshot(path="screenshot.png")
    browser.close()
```

### Approach B: Running Server (Reconnaissance-then-Action)

When a dev server is already running:

1. **Reconnaissance**: Navigate to the app and discover the page structure
2. **Wait for stability**: `page.wait_for_load_state('networkidle')`
3. **Inspect**: Query elements, read content, check console logs
4. **Act**: Interact with forms, buttons, navigation
5. **Verify**: Assert expected outcomes

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Capture console messages
    console_messages = []
    page.on("console", lambda msg: console_messages.append(
        f"[{msg.type}] {msg.text}"
    ))

    # Navigate and wait for stability
    page.goto("http://localhost:3000")
    page.wait_for_load_state("networkidle")

    # Discover page structure
    headings = page.query_selector_all("h1, h2, h3")
    buttons = page.query_selector_all("button")
    forms = page.query_selector_all("form")
    links = page.query_selector_all("a[href]")

    # Print discovered elements
    for h in headings:
        print(f"Heading: {h.text_content()}")
    for btn in buttons:
        print(f"Button: {btn.text_content()}")

    # Screenshot before interaction
    page.screenshot(path="before-interaction.png")

    # Interact with form
    page.fill("input[name='email']", "test@example.com")
    page.fill("input[name='password']", "testpass123")
    page.click("button[type='submit']")
    page.wait_for_load_state("networkidle")

    # Screenshot after interaction
    page.screenshot(path="after-interaction.png")

    # Check for console errors
    errors = [m for m in console_messages if "[error]" in m.lower()]
    if errors:
        print(f"Console errors found: {errors}")

    browser.close()
```

### Approach C: No Running Server (Helper Script)

When the web app needs a server started:

```python
import subprocess
import time
from playwright.sync_api import sync_playwright

# Start the server
server_proc = subprocess.Popen(
    ["npm", "run", "dev"],
    cwd="/path/to/project",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=False  # Security: always shell=False
)

# Wait for server to be ready
time.sleep(5)  # Or use a health check loop

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")

        # Run tests...
        page.screenshot(path="test-result.png")
        browser.close()
finally:
    server_proc.terminate()
    server_proc.wait()
```

## Common Test Patterns

### Pattern 1: Visual Regression Check

```python
# Take baseline screenshot
page.screenshot(path="baseline.png", full_page=True)

# After changes, take comparison screenshot
page.screenshot(path="current.png", full_page=True)

# Compare (use image diff library)
```

### Pattern 2: Form Validation Testing

```python
# Test empty submission
page.click("button[type='submit']")
error_msgs = page.query_selector_all(".error-message")
assert len(error_msgs) > 0, "Expected validation errors for empty form"

# Test invalid email
page.fill("input[type='email']", "not-an-email")
page.click("button[type='submit']")
email_error = page.query_selector("input[type='email']:invalid")
assert email_error is not None
```

### Pattern 3: Navigation Flow Testing

```python
# Test navigation links
nav_links = page.query_selector_all("nav a")
for link in nav_links:
    href = link.get_attribute("href")
    link.click()
    page.wait_for_load_state("networkidle")
    assert page.url.endswith(href), f"Expected URL to end with {href}"
    page.go_back()
    page.wait_for_load_state("networkidle")
```

### Pattern 4: Responsive Design Testing

```python
viewports = [
    {"width": 375, "height": 812, "name": "mobile"},
    {"width": 768, "height": 1024, "name": "tablet"},
    {"width": 1920, "height": 1080, "name": "desktop"},
]

for vp in viewports:
    page.set_viewport_size({"width": vp["width"], "height": vp["height"]})
    page.wait_for_load_state("networkidle")
    page.screenshot(path=f"responsive-{vp['name']}.png")
```

## Critical Pitfalls

1. **Do NOT inspect DOM before networkidle**: Dynamic apps load content asynchronously. Early inspection gives incomplete results.
2. **Do NOT use shell=True**: When spawning server processes, always use `shell=False` with array arguments for security.
3. **Do NOT hardcode waits**: Use `page.wait_for_selector()` or `page.wait_for_load_state()` instead of `time.sleep()`.
4. **Do NOT ignore console errors**: Always capture and report browser console errors -- they indicate real issues.
5. **Do NOT forget cleanup**: Always terminate server processes in a `finally` block.

## Prerequisites

Ensure Playwright is installed:

```bash
pip install playwright
playwright install chromium
```

## Integration with Agent-Studio

### Recommended Workflow

1. Use `webapp-testing` to verify frontend behavior
2. Feed screenshot evidence to `code-reviewer` for visual review
3. Use `tdd` skill to generate test suites from discovered patterns
4. Use `accessibility` skill to verify WCAG compliance

### Complementary Skills

| Skill             | Relationship                                          |
| ----------------- | ----------------------------------------------------- |
| `tdd`             | Generate test suites from webapp-testing discoveries  |
| `accessibility`   | WCAG compliance verification after functional testing |
| `frontend-expert` | UI/UX pattern guidance for test design                |
| `chrome-browser`  | Alternative browser automation approach               |
| `test-generator`  | Generate test code from testing patterns              |

## Iron Laws

1. **NEVER INSPECT DOM BEFORE NETWORKIDLE** — Dynamic web applications load content asynchronously. Inspecting the DOM before the page has stabilized produces incorrect or incomplete results.
2. **NEVER use shell=True** when spawning server processes — always use `shell=False` with array arguments (SE-01 security requirement).
3. **ALWAYS capture console errors** — browser console errors indicate real issues; never ignore them in test reports.
4. **ALWAYS terminate server processes in finally blocks** — leaked server processes corrupt future test runs and consume resources.
5. **NEVER hardcode waits** — use `page.wait_for_selector()` or `page.wait_for_load_state()` instead of `time.sleep()`.

## Anti-Patterns

| Anti-Pattern                            | Why It Fails                                                       | Correct Approach                                                   |
| --------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| Inspecting DOM before networkidle       | Dynamic content not yet loaded; assertions produce false negatives | Always `page.wait_for_load_state('networkidle')` before inspection |
| Using `time.sleep()` for waits          | Flaky — too short on slow machines, too long on fast ones          | Use explicit waits: `wait_for_selector`, `wait_for_load_state`     |
| Ignoring browser console errors         | Real JS errors go undetected; test passes but app is broken        | Always capture and report console errors in every test run         |
| Using `shell=True` for server processes | Command injection vulnerability                                    | Always `shell=False` with list arguments                           |
| Not cleaning up server processes        | Port conflicts, resource leaks on subsequent runs                  | Use `try/finally` to guarantee `server_proc.terminate()`           |

## Memory Protocol (MANDATORY)

**Before starting:**

Read `.claude/context/memory/learnings.md`

Check for:

- Existing test scripts or Playwright configurations in the project
- Known page selectors from previous sessions
- Previously discovered console errors or flaky test patterns

**After completing:**

- Testing pattern found -> `.claude/context/memory/learnings.md`
- Test flakiness or browser issue -> `.claude/context/memory/issues.md`
- Decision about test strategy -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
