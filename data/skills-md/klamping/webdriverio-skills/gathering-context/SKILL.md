---
name: gathering-context
description: Use when investigating a failing WebdriverIO test and you need to understand what the test was doing and where it broke.
---

# Context Gatherer

Reads all available artifacts for a failing WebdriverIO test and returns a structured markdown summary. Called by the Investigator agent — does not diagnose or fix, only gathers and organizes evidence.

## Inputs

The Investigator passes a structured failure object:

```
- testName: string        # The it() / describe() title
- specFile: string        # Relative path to the spec file
- errorMessage: string    # The assertion or exception message
- stackTrace: string      # Full stack trace
- logFile?: string        # Optional: path to wdio log file
- snapshotDir?: string    # Optional: dir where HTML/screenshots/video are saved
```

## Project Context Files

Before scanning from scratch, read project cache files when available:

- `.webdriverio-skills/project-context.md`
- `.webdriverio-skills/project-context.json`
- `.webdriverio-skills/custom-rules.md`
- `references/website-analysis/<target>/website-analysis.md`
- `references/website-analysis/<target>/website-analysis.json`

Use cached reporter, service, artifact, and environment details to narrow discovery work.

If files are missing or stale, run `managing-project-customizations` first.

### Target Resolution Rule

When reading `references/website-analysis/<target>/...`, resolve `<target>` as:

- lowercase site host from the test URL/baseUrl (e.g. `demo.learnwebdriverio.com`)
- if host is unknown, use `unknown-target` and continue without blocking

## Workflow

### Step 1 — Locate Artifacts

Use cached context first, then read `wdio.conf.js` (or discovered WDIO config files) to resolve:

- **Reporters** — which are configured (e.g. `allure`, `junit`, `spec`) and their output directories. Note artifact paths; do not parse report formats.
- **Log paths** — where WDIO writes its log output.
- **Snapshot directories** — where screenshots and HTML snapshots are saved on failure (often configured in `afterTest` hook via `browser.saveScreenshot()` and `browser.savePDF()` / page source capture).
- **Video** — if a video service (e.g. `wdio-video-reporter`) is configured, note the output path.
- **Services** — list all configured services. Flag any in these categories as a potential failure dimension for the Investigator:

| Service type | Why it matters |
|---|---|
| Visual regression (e.g. `wdio-image-comparison-service`) | Failure may be a visual diff, not a selector or logic issue |
| Mobile / Appium | Element interaction differs from browser; gestures, native contexts |
| Cloud providers (BrowserStack, Sauce, LambdaTest) | Session timeouts, capability mismatches, remote-specific failures |
| `selenium-standalone` / `chromedriver` | Driver version mismatch can cause unexpected command failures |

If `snapshotDir` or `logFile` were provided in the failure object, use those directly and skip discovery for those paths.

### Step 2 — Read the Spec File

Open `specFile` and:

1. Extract the full body of the `it()` block matching `testName`
2. Identify all enclosing `describe()` blocks (tests can be nested — outer describe hooks apply)
3. Identify all Mocha hooks in scope: `before`, `beforeEach`, `after`, `afterEach` at every nesting level — these run around the failing test and may be relevant
4. Note all `import` / `require` statements — these reveal page object dependencies to traverse in Step 3

If website analysis references exist, use them to quickly map the failing test to:
- likely section/component ownership
- expected critical states for the area
- known auth-gated routes or dependencies

**Mocha structure to understand:**
- `describe()` blocks scope hooks and can be nested arbitrarily deep
- `before` / `after` run once per describe block
- `beforeEach` / `afterEach` run around every `it()` in their scope
- All hooks from all enclosing describe levels apply to any given `it()`

### Step 3 — Traverse Page Object Dependencies

Starting from the imports found in Step 2, recursively follow all `import` / `require` statements.

For each page object class found:

- Extract method names and their implementations
- Note every WebdriverIO command used (see Command Reference below)
- Extract every selector passed to `$()` or `$$()` — these are CSS or XPath strings that map directly to DOM elements

**Page Object pattern:**
Page objects are JavaScript classes that encapsulate selectors and interactions. A method like `async clickSubmit()` wraps `await this.submitBtn.click()` where `submitBtn` is defined as `get submitBtn() { return $('#submit-btn') }`. Understanding this chain — method → command → selector → DOM element — is essential for correlating failures with HTML snapshots.

Continue recursing until all transitive imports are read. Cross-reference selectors from page objects with the HTML snapshots in Step 5.

### Step 4 — Search for Custom Commands

Search the codebase for `addCommand` to find all custom command definitions.

For each custom command found:
- Note whether it's registered on `browser` or `element`
- Read its full implementation
- If a custom command appears in the failing test or any page object method, treat it as a first-class suspect — read it completely

Custom commands do not appear as named entries in WDIO logs. You will see only the underlying native commands they delegate to. To understand what a custom command was doing at failure time, cross-reference the native command sequence in the logs with the custom command's implementation.

If a custom command calls another custom command, follow the chain completely.

### Step 5 — Read Logs

Open the log file (from `logFile` input or discovered in Step 1).

Filter to lines associated with the failing test. WDIO logs include:

- `COMMAND <method> <endpoint>` — a native browser command being sent
- `DATA <payload>` — the command's parameters
- `RESULT <value>` — the response from the driver

Match the log's command sequence against the WebdriverIO commands in the spec and page objects to reconstruct what actually executed at runtime. Look for the last successful command before the error appears.

### Step 6 — Collect HTML Snapshots

If HTML snapshots exist in the snapshot directory:

1. Load them in filename / timestamp order — earlier snapshots show DOM state before the failure
2. For the failure-time snapshot: check whether selectors from page objects are present in the HTML, have the expected attributes, text, and state
3. CSS selectors can be matched structurally against the HTML. XPath requires understanding document hierarchy.
4. Note any elements that are absent, hidden (`display:none`, `visibility:hidden`, `aria-hidden`), disabled, or have unexpected attribute values

### Step 7 — Collect Visual Artifacts

Locate screenshots and video files associated with the test run. Do not attempt to analyze their content — record file paths and timestamps only. The Investigator decides whether to pass them to a vision-capable model.

Include in the summary:
- Screenshot file paths (in timestamp order)
- Video file path (if present)

---

## Command Reference

Use this reference to understand what a failing test was executing. If a command is unfamiliar or you need full parameter details, look it up:

- Element commands: `https://webdriver.io/docs/api/element/<commandName>`
- Browser commands: `https://webdriver.io/docs/api/browser/<commandName>`
- Expect / assertions: `https://webdriver.io/docs/api/expect-webdriverio`
- Full API index: `https://webdriver.io/docs/api`

### Element Commands

Called on an element object returned by `$()` or `$$()`. Operate on a specific DOM node. **Failures here relate to that element's state, visibility, or interactability — look at the selector and the DOM snapshot.**

| Command | What it does | Common failure modes |
|---|---|---|
| `$('selector')` | Find first matching element | Element not in DOM, wrong selector, not yet rendered |
| `$$('selector')` | Find all matching elements | Returns empty array if none match |
| `click()` | Click the element | Element obscured, not interactable, wrong element matched |
| `setValue(val)` | Clear and type into input | Element not an input, not focused, readonly |
| `addValue(val)` | Append to input value | Same as setValue |
| `getText()` | Get visible text content | Element not rendered, text in shadow DOM |
| `getValue()` | Get input value | Element not an input type |
| `getAttribute(name)` | Get DOM attribute | Attribute doesn't exist → returns null |
| `getCSSProperty(prop)` | Get computed CSS value | Useful for checking visibility, color, dimensions |
| `isDisplayed()` | Is element visible? | Returns false if hidden via CSS |
| `isExisting()` | Is element in DOM? | Returns false if not yet rendered |
| `isClickable()` | Is element clickable? | Checks displayed + enabled + in viewport |
| `isEnabled()` | Is form element enabled? | Returns false for disabled inputs/buttons |
| `isSelected()` | Is checkbox/radio selected? | Only for checkboxes and radio buttons |
| `waitForDisplayed(opts)` | Wait until visible | Timeout if element never becomes visible |
| `waitForExist(opts)` | Wait until in DOM | Timeout if element never appears |
| `waitForClickable(opts)` | Wait until clickable | Timeout if never interactable |
| `selectByVisibleText(text)` | Select `<option>` by label | Text mismatch, not a `<select>` element |
| `selectByAttribute(attr, val)` | Select `<option>` by attribute | Attribute value mismatch |
| `scrollIntoView()` | Scroll element into viewport | Needed before click on off-screen elements |
| `moveTo()` | Hover over element | Used for hover-triggered UI |

### Browser Commands

Called on the global `browser` object. Operate at the session or page level. **Failures here relate to navigation, page state, or browser context — not element-level issues.**

| Command | What it does | Common failure modes |
|---|---|---|
| `browser.url(path)` | Navigate to URL or path | Wrong base URL, page load failure |
| `browser.getUrl()` | Get current URL | Useful for asserting navigation succeeded |
| `browser.getTitle()` | Get page title | Page not loaded, wrong page |
| `browser.refresh()` | Reload current page | — |
| `browser.back()` / `forward()` | Browser history navigation | — |
| `browser.waitUntil(fn, opts)` | Wait for arbitrary condition | Timeout if condition never true; check fn logic |
| `browser.execute(fn)` | Run JS in browser context | JS error in fn, wrong return type |
| `browser.executeAsync(fn)` | Run async JS in browser | Callback never called → timeout |
| `browser.pause(ms)` | Hard wait (avoid if possible) | Masks timing issues rather than fixing them |
| `browser.keys(keys)` | Send keyboard input | Focus not on expected element |
| `browser.switchToFrame(id)` | Switch context to iframe | Wrong frame ID, frame not loaded |
| `browser.switchToParentFrame()` | Return to main frame | Already in main frame |
| `browser.newWindow(url)` | Open new window/tab | — |
| `browser.switchWindow(handle)` | Switch to window by handle/title | Wrong handle, window closed |
| `browser.acceptAlert()` | Accept a browser dialog | No dialog present |
| `browser.dismissAlert()` | Dismiss a browser dialog | No dialog present |
| `browser.getAlertText()` | Get dialog message text | No dialog present |
| `browser.setCookies(cookies)` | Set browser cookies | Wrong domain, malformed cookie |
| `browser.getCookies()` | Get all cookies | — |
| `browser.deleteCookies()` | Delete cookies | — |
| `browser.saveScreenshot(path)` | Save screenshot to file | — |
| `browser.getPageSource()` | Get full page HTML | Useful for snapshot comparison |

### Expect / Assertions

Assertions use `expect-webdriverio`. A failing assertion means the element or browser was in the wrong state at that moment.

| Assertion | What it checks |
|---|---|
| `expect(el).toBeDisplayed()` | Element is visible |
| `expect(el).toExist()` | Element is in DOM |
| `expect(el).toBeClickable()` | Element is interactable |
| `expect(el).toBeEnabled()` | Form element is not disabled |
| `expect(el).toBeSelected()` | Checkbox/radio is checked |
| `expect(el).toHaveText(str)` | Element text matches |
| `expect(el).toHaveValue(str)` | Input value matches |
| `expect(el).toHaveAttribute(attr, val)` | Attribute has expected value |
| `expect(el).toHaveClass(name)` | Element has CSS class |
| `expect(el).toHaveURL(str)` | Current URL matches (on browser) |
| `expect(el).toHaveTitle(str)` | Page title matches (on browser) |
| `expect(arr).toHaveLength(n)` | Array/collection length |

When an assertion fails, the error message includes the actual vs. expected value. Cross-reference the actual value with the HTML snapshot and logs to understand why the state was wrong.

---

## Output

Return a structured markdown summary to the Investigator:

```markdown
## Context: <testName>

### Test Flow
Step-by-step reconstruction of what the test was doing,
derived from the spec file, hooks in scope, and page object methods.

### Last Known Good State
What the test had successfully completed just before the failure,
based on log command sequence and intermediate HTML snapshots (if present).

### Point of Failure
- **Error:** <errorMessage>
- **Stack trace:** excerpt pointing to the exact file and line
- **Command:** the WebdriverIO command that failed or produced wrong state
- **Selector involved:** the CSS/XPath selector (if applicable)
- **Page object method:** which method contained the failing command

### DOM State at Failure
Key observations from the HTML snapshot at failure time:
- Was the selector present? Hidden? Disabled?
- Were expected elements missing or in unexpected state?
- Any relevant attribute values or form state?

### Visual Artifacts
- Screenshots: [list of file paths with timestamps, in order]
- Video: [file path if present, otherwise "none"]
- HTML snapshots: [list of file paths in sequence, oldest first]

### Active Services
[List configured services and flag any that may be relevant to the failure]

### Custom Commands Involved
[List any custom commands called in the test flow, with their source location]

### Hypothesis
One or two sentences: the most likely cause of the failure based on the
evidence gathered. Do not speculate beyond what the artifacts support.
```
