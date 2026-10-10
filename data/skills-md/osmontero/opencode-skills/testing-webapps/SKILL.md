---
name: testing-webapps
description: Use when testing local web applications using Playwright. Triggers include requests to verify frontend functionality, debug UI behavior, capture browser screenshots, view browser logs, or test any web application interactively. Write native Python Playwright scripts for all web application testing tasks.
license: Complete terms in LICENSE.txt
---
------

# Testing Web Applications

To test local web applications, write native Python Playwright scripts.

## Prerequisites

Before running any Python scripts, **activate the opencode virtual environment**:

```bash
source ~/.local/opencode-venv/bin/activate
```

Then use `python3 scripts/...` normally. If Playwright browser binaries aren't installed yet:

```bash
playwright install chromium
```

**Helper Scripts Available**:
- `scripts/with_server.py` - Manages server lifecycle (supports multiple servers)

**Always run scripts with `--help` first** to see usage. DO NOT read the source until you try running the script first and find that a customized solution is abslutely necessary. These scripts can be very large and thus pollute your context window. They exist to be called directly as black-box scripts rather than ingested into your context window.

## Decision Tree: Choosing Your Approach

```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using selectors
    │         └─ Fails/Incomplete → Treat as dynamic (below)
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Run: python scripts/with_server.py --help
        │        Then use the helper + write simplified Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

## Example: Using with_server.py

To start a server, run `--help` first, then use the helper:

**Single server:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**Multiple servers (e.g., backend + frontend):**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

To create an automation script, include only Playwright logic (servers are managed automatically):
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # Always launch chromium in headless mode
    page = browser.new_page()
    page.goto('http://localhost:5173') # Server already running and ready
    page.wait_for_load_state('networkidle') # CRITICAL: Wait for JS to execute
    # ... your automation logic
    browser.close()
```

## Reconnaissance-Then-Action Pattern

1. **Inspect rendered DOM**:
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **Identify selectors** from inspection results

3. **Execute actions** using discovered selectors

## Common Pitfall

❌ **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps
✅ **Do** wait for `page.wait_for_load_state('networkidle')` before inspection

## Best Practices

- **Use bundled scripts as black boxes** - To accomplish a task, consider whether one of the scripts available in `scripts/` can help. These scripts handle common, complex workflows reliably without cluttering the context window. Use `--help` to see usage, then invoke directly. 
- Use `sync_playwright()` for synchronous scripts
- Always close the browser when done
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`

## Waiting Correctly

`networkidle` is the right default for first load, but it is the wrong tool for asserting that a specific thing happened. Prefer waiting on the condition you actually care about.

```python
page.wait_for_selector("[data-testid=results]", state="visible")
page.wait_for_function("() => document.querySelectorAll('.row').length > 0")
page.get_by_role("button", name="Save").click()
expect(page.get_by_text("Saved")).to_be_visible()      # auto-retries
```

**Never `wait_for_timeout()` as a substitute for a condition.** A fixed sleep is either too short (flaky) or too long (slow), and it always hides the real race. The one legitimate use is waiting out a known animation duration before a screenshot.

Prefer role-based locators over CSS — they survive restyling and they double as an accessibility assertion:

```python
page.get_by_role("button", name="Delete account")
page.get_by_label("Email address")
page.get_by_role("heading", level=1)
```

If `get_by_role` cannot find a control, that is usually a genuine accessibility defect, not a test problem. See `building-accessible-interfaces`.

## Asserting Console Cleanliness

A page that renders correctly while throwing errors is broken. Capture and assert.

```python
errors, warnings = [], []
page.on("console", lambda m: (errors if m.type == "error" else warnings).append(m.text)
        if m.type in ("error", "warning") else None)
page.on("pageerror", lambda e: errors.append(f"uncaught: {e}"))
page.on("requestfailed", lambda r: errors.append(f"{r.method} {r.url} — {r.failure}"))

page.goto(URL); page.wait_for_load_state("networkidle")
assert not errors, errors
```

## Accessibility Auditing

Run axe against the live page. This is the automated third of the accessibility check — the keyboard walk and screen-reader pass in `building-accessible-interfaces` are still required.

```python
page.add_script_tag(url="https://cdn.jsdelivr.net/npm/axe-core@4/axe.min.js")
result = page.evaluate("async () => await axe.run()")
violations = [(v["id"], v["impact"], len(v["nodes"])) for v in result["violations"]]
assert not violations, violations
```

Keyboard traversal — catches missing focus styles and unreachable controls:

```python
seq = []
for _ in range(40):
    page.keyboard.press("Tab")
    seq.append(page.evaluate("""() => {
        const el = document.activeElement;
        if (!el || el === document.body) return null;
        const s = getComputedStyle(el);
        return {tag: el.tagName, name: el.ariaLabel || el.innerText?.slice(0,30),
                outline: s.outlineStyle, ring: s.boxShadow !== 'none'};
    }"""))
invisible = [s for s in seq if s and s["outline"] == "none" and not s["ring"]]
assert not invisible, f"focusable elements with no visible focus: {invisible}"
```

## Responsive and Visual Checks

```python
for name, w, h in [("mobile", 390, 844), ("tablet", 768, 1024), ("desktop", 1440, 900)]:
    page.set_viewport_size({"width": w, "height": h})
    page.wait_for_timeout(200)                       # settle layout/animation
    overflow = page.evaluate("""() => [...document.querySelectorAll('*')]
        .filter(e => e.getBoundingClientRect().right > document.documentElement.clientWidth + 1)
        .slice(0,5).map(e => e.tagName + '.' + e.className)""")
    assert not overflow, f"{name}: horizontal overflow from {overflow}"
    page.screenshot(path=f"/tmp/{name}.png", full_page=True)
```

**Then read the screenshots.** A passing assertion says the DOM is not overflowing; it says nothing about whether the page looks right. For a full visual audit use the `reviewing-interface-quality` skill.

Deterministic screenshots — disable animation and caret so repeat runs match:

```python
page.screenshot(path="x.png", animations="disabled", caret="hide", full_page=True)
```

## Controlling the Network

Testing error and empty states requires forcing them. This is how you exercise the state matrix from `designing-user-experience`.

```python
page.route("**/api/items", lambda r: r.fulfill(status=200, json=[]))        # empty state
page.route("**/api/items", lambda r: r.fulfill(status=500))                 # error state
page.route("**/api/items", lambda r: r.abort())                             # network failure
page.context.set_offline(True)                                              # offline state

# Slow response — verifies the loading state actually appears
page.route("**/api/**", lambda r: (page.wait_for_timeout(3000), r.continue_())[1])
```

Emulate constrained conditions:

```python
ctx = browser.new_context(color_scheme="dark", reduced_motion="reduce",
                          locale="ar-EG", viewport={"width": 390, "height": 844})
```

`reduced_motion="reduce"` verifies the `prefers-reduced-motion` block exists. `color_scheme="dark"` catches contrast that only fails in dark mode.

## Debugging a Failing Script

```python
browser = p.chromium.launch(headless=False, slow_mo=400)   # watch it run
page.pause()                                               # opens Playwright Inspector
```

```bash
PWDEBUG=1 python3 your_script.py            # step through
python3 -m playwright codegen localhost:5173  # record interactions into code
```

Capture a trace when a failure is intermittent:

```python
context.tracing.start(screenshots=True, snapshots=True)
# ...
context.tracing.stop(path="/tmp/trace.zip")   # then: playwright show-trace /tmp/trace.zip
```

## Common Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Element found but click does nothing | Overlay intercepting the event | `page.get_by_role(...).click()` reports the interceptor — dismiss it first |
| Passes headed, fails headless | Timing, or a font/layout difference | Wait on conditions, not timeouts; set an explicit viewport |
| `strict mode violation` | Locator matched multiple elements | Narrow with `.first`, a role, or a more specific name |
| Screenshot is blank | Captured before paint | `wait_for_load_state("networkidle")` plus a settle timeout |
| Works once, fails on rerun | Test mutated state and did not reset | Use a fresh `browser.new_context()` per run |
| Selector breaks after a restyle | CSS-class-based locator | Use `get_by_role` / `get_by_label` / `data-testid` |

## Reference Files

- **examples/** - Examples showing common patterns:
  - `element_discovery.py` - Discovering buttons, links, and inputs on a page
  - `static_html_automation.py` - Using file:// URLs for local HTML
  - `console_logging.py` - Capturing console logs during automation

## Related Skills

- **reviewing-interface-quality** — full visual/UX/a11y audit of a rendered UI
- **building-accessible-interfaces** — what the axe results mean and how to fix them
- **designing-user-experience** — the state matrix these network mocks exist to exercise
- **systematic-debugging** — when a test failure is a real bug, not a test bug