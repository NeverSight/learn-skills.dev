---
name: playwright-visual-testing
description: Browser automation, visual testing, and screenshot validation using Playwright MCP server for accelerated web development. Master visual regression testing, automated UI testing, and cross-browser validation.
---

# Playwright Visual Testing & Browser Automation

A comprehensive skill for browser automation and visual testing using Playwright MCP server integration. This skill enables rapid UI testing, visual regression detection, automated browser interactions, and cross-browser validation for modern web applications.

## When to Use This Skill

Use this skill when:

- Testing web applications across multiple browsers (Chromium, Firefox, WebKit)
- Implementing visual regression testing for UI changes
- Automating user interactions for QA and testing
- Validating responsive designs across different viewports
- Taking screenshots for documentation or bug reports
- Testing form submissions and user workflows
- Verifying accessibility of web interfaces
- Debugging browser-specific issues
- Creating automated E2E test suites
- Validating web applications before deployment
- Testing PWAs and single-page applications
- Capturing visual states for design reviews

## Core Concepts

### Playwright Browser Automation Philosophy

Playwright provides reliable end-to-end testing for modern web apps:

- **Auto-wait**: Automatically waits for elements to be actionable before interacting
- **Web-first assertions**: Retry assertions until they pass or timeout
- **Cross-browser**: Test on Chromium, Firefox, and WebKit with single API
- **Accessibility snapshots**: Navigate pages using semantic structure, not visual rendering
- **Visual testing**: Compare screenshots to detect visual regressions
- **Network control**: Intercept and mock network requests
- **Multi-context**: Test multiple scenarios in isolated browser contexts

### Key Playwright Entities

1. **Browser**: The browser instance (Chromium, Firefox, WebKit)
2. **Page**: A single page/tab in the browser
3. **Locator**: Element selector using accessibility tree
4. **Snapshot**: Accessibility tree representation of page state
5. **Screenshot**: Visual capture of page or element
6. **Network Request**: HTTP requests made by the page
7. **Console Messages**: Browser console output
8. **Dialog**: Browser prompts, alerts, confirms

### Visual Testing Workflow

1. **Navigate** to the target page
2. **Wait** for page to stabilize (animations, loading)
3. **Capture** accessibility snapshot for context
4. **Take screenshot** of page or specific elements
5. **Compare** against baseline (optional)
6. **Validate** visual appearance and functionality
7. **Document** results and issues

## Playwright MCP Server Tools Reference

### Browser Lifecycle Management

#### browser_navigate
Navigate to a URL in the current page.

**Parameters:**
```
url: The URL to navigate to (required)
```

**Example:**
```javascript
url: "https://example.com"
```

**Best Practices:**
- Use full URLs including protocol (https://)
- Wait for navigation to complete before taking actions
- Handle redirects and page transitions

#### browser_navigate_back
Navigate back to the previous page in history.

**Parameters:** None

**Example:**
```javascript
// Navigate back after clicking a link
```

**Use Cases:**
- Testing navigation flows
- Verifying back button behavior
- Multi-step form navigation

#### browser_close
Close the current browser page.

**Parameters:** None

**When to Use:**
- Clean up after testing
- Free system resources
- Reset browser state

#### browser_resize
Resize the browser viewport.

**Parameters:**
```
width: Width in pixels (required)
height: Height in pixels (required)
```

**Common Viewports:**
```javascript
// Mobile
width: 375, height: 667  // iPhone SE
width: 414, height: 896  // iPhone XR

// Tablet
width: 768, height: 1024  // iPad

// Desktop
width: 1280, height: 720  // HD
width: 1920, height: 1080 // Full HD
```

**Example:**
```javascript
width: 375
height: 667
```

### Page Inspection & Snapshots

#### browser_snapshot
Capture accessibility snapshot of the current page.

**Parameters:** None

**Returns:**
- Accessibility tree with semantic structure
- Element references (ref) for interactions
- Text content and roles
- Interactive elements and states

**Why Use Snapshots:**
- Better than screenshots for automation
- Semantic understanding of page structure
- Element references for precise interactions
- Faster than visual parsing
- Works without visual rendering

**Example Snapshot Structure:**
```
heading "Welcome" [ref=123]
  text "to our site"
button "Sign In" [ref=456]
textbox "Email" [ref=789]
  value: ""
```

#### browser_take_screenshot
Take a screenshot of the current page or element.

**Parameters:**
```
filename: Output filename (optional, defaults to page-{timestamp}.png)
type: Image format - "png" or "jpeg" (default: png)
fullPage: Capture full scrollable page (default: false)
element: Human-readable element description (optional)
ref: Element reference from snapshot (optional, requires element)
```

**Screenshot Types:**

1. **Viewport Screenshot** (default):
```javascript
filename: "homepage-viewport.png"
```

2. **Full Page Screenshot**:
```javascript
filename: "homepage-full.png"
fullPage: true
```

3. **Element Screenshot**:
```javascript
filename: "header.png"
element: "main header navigation"
ref: "123"
```

**Best Practices:**
- Use descriptive filenames with context
- PNG for UI elements (lossless)
- JPEG for photos/images (smaller size)
- Full page for documentation
- Element screenshots for focused testing

### Browser Interaction

#### browser_click
Perform click on an element.

**Parameters:**
```
element: Human-readable element description (required)
ref: Element reference from snapshot (required)
button: "left", "right", or "middle" (default: left)
doubleClick: true for double-click (default: false)
modifiers: Array of modifier keys ["Alt", "Control", "ControlOrMeta", "Meta", "Shift"]
```

**Examples:**

1. **Basic Click**:
```javascript
element: "Submit button"
ref: "456"
```

2. **Right Click**:
```javascript
element: "Context menu trigger"
ref: "789"
button: "right"
```

3. **Click with Modifier**:
```javascript
element: "Link to open in new tab"
ref: "123"
modifiers: ["ControlOrMeta"]
```

4. **Double Click**:
```javascript
element: "Word to select"
ref: "321"
doubleClick: true
```

#### browser_type
Type text into an editable element.

**Parameters:**
```
element: Human-readable element description (required)
ref: Element reference from snapshot (required)
text: Text to type (required)
slowly: Type one character at a time (default: false)
submit: Press Enter after typing (default: false)
```

**Examples:**

1. **Form Input**:
```javascript
element: "Email textbox"
ref: "123"
text: "user@example.com"
```

2. **Search with Submit**:
```javascript
element: "Search field"
ref: "456"
text: "playwright testing"
submit: true
```

3. **Character-by-Character** (triggers key handlers):
```javascript
element: "Auto-complete input"
ref: "789"
text: "New York"
slowly: true
```

#### browser_press_key
Press a keyboard key.

**Parameters:**
```
key: Key name or character (required)
```

**Common Keys:**
```
ArrowLeft, ArrowRight, ArrowUp, ArrowDown
Enter, Escape, Tab, Backspace, Delete
Home, End, PageUp, PageDown
F1-F12
Control, Alt, Shift, Meta
```

**Examples:**
```javascript
// Navigation
key: "ArrowDown"

// Submit form
key: "Enter"

// Close dialog
key: "Escape"

// Tab through fields
key: "Tab"
```

#### browser_fill_form
Fill multiple form fields at once.

**Parameters:**
```
fields: Array of field objects (required)
  - name: Human-readable field name
  - type: "textbox", "checkbox", "radio", "combobox", "slider"
  - ref: Element reference from snapshot
  - value: Value to set (string, "true"/"false" for checkboxes)
```

**Example:**
```javascript
fields: [
  {
    name: "Username",
    type: "textbox",
    ref: "123",
    value: "john_doe"
  },
  {
    name: "Password",
    type: "textbox",
    ref: "456",
    value: "secretpass123"
  },
  {
    name: "Remember me",
    type: "checkbox",
    ref: "789",
    value: "true"
  }
]
```

#### browser_select_option
Select option from dropdown.

**Parameters:**
```
element: Human-readable element description (required)
ref: Element reference from snapshot (required)
values: Array of values to select (required)
```

**Example:**
```javascript
element: "Country dropdown"
ref: "123"
values: ["United States"]
```

**Multi-select:**
```javascript
element: "Programming languages"
ref: "456"
values: ["JavaScript", "Python", "Go"]
```

#### browser_hover
Hover over an element.

**Parameters:**
```
element: Human-readable element description (required)
ref: Element reference from snapshot (required)
```

**Use Cases:**
- Trigger tooltips
- Show dropdown menus
- Test hover states
- Reveal hidden elements

**Example:**
```javascript
element: "Help icon"
ref: "123"
```

#### browser_drag
Drag and drop between elements.

**Parameters:**
```
startElement: Source element description (required)
startRef: Source element reference (required)
endElement: Target element description (required)
endRef: Target element reference (required)
```

**Example:**
```javascript
startElement: "Task card"
startRef: "123"
endElement: "Done column"
endRef: "456"
```

**Use Cases:**
- Drag-and-drop interfaces
- Reordering lists
- File uploads
- Kanban boards

### Advanced Interactions

#### browser_evaluate
Execute JavaScript in page context.

**Parameters:**
```
function: JavaScript function as string (required)
element: Element description (optional)
ref: Element reference (optional, requires element)
```

**Examples:**

1. **Page-level Script**:
```javascript
function: "() => { return document.title; }"
```

2. **Element-level Script**:
```javascript
element: "Custom widget"
ref: "123"
function: "(element) => { return element.getAttribute('data-value'); }"
```

**Common Use Cases:**
```javascript
// Get page title
function: "() => document.title"

// Scroll to bottom
function: "() => window.scrollTo(0, document.body.scrollHeight)"

// Get element dimensions
function: "(element) => { const rect = element.getBoundingClientRect(); return { width: rect.width, height: rect.height }; }"

// Set local storage
function: "() => localStorage.setItem('theme', 'dark')"

// Get computed style
function: "(element) => getComputedStyle(element).backgroundColor"
```

#### browser_file_upload
Upload files to file input.

**Parameters:**
```
paths: Array of absolute file paths (required)
  - Omit or pass empty array to cancel file chooser
```

**Example:**
```javascript
paths: [
  "/Users/user/Documents/resume.pdf",
  "/Users/user/Photos/headshot.jpg"
]
```

**Single File:**
```javascript
paths: ["/Users/user/Downloads/report.csv"]
```

**Cancel Upload:**
```javascript
paths: []
```

### Browser State & Debugging

#### browser_console_messages
Get console messages from the browser.

**Parameters:**
```
onlyErrors: Return only error messages (default: false)
```

**Returns:**
- All console.log, console.error, console.warn messages
- Timestamps and message types
- JavaScript errors and stack traces

**Examples:**

1. **All Messages**:
```javascript
onlyErrors: false
```

2. **Errors Only**:
```javascript
onlyErrors: true
```

**Use Cases:**
- Debug JavaScript errors
- Monitor API failures
- Track console warnings
- Verify logging behavior

#### browser_network_requests
Get all network requests since page load.

**Parameters:** None

**Returns:**
- URL, method, status code
- Request/response headers
- Timing information
- Request/response bodies

**Use Cases:**
- Verify API calls
- Check resource loading
- Debug failed requests
- Monitor performance
- Validate analytics tracking

#### browser_handle_dialog
Respond to browser dialogs.

**Parameters:**
```
accept: Accept or dismiss dialog (required)
promptText: Text for prompt dialogs (optional)
```

**Dialog Types:**
- alert: Information message
- confirm: Yes/No choice
- prompt: Text input request
- beforeunload: Page navigation warning

**Examples:**

1. **Accept Alert**:
```javascript
accept: true
```

2. **Dismiss Confirm**:
```javascript
accept: false
```

3. **Answer Prompt**:
```javascript
accept: true
promptText: "John Doe"
```

#### browser_wait_for
Wait for conditions before proceeding.

**Parameters:**
```
text: Wait for text to appear (optional)
textGone: Wait for text to disappear (optional)
time: Wait for specified seconds (optional)
```

**Examples:**

1. **Wait for Text**:
```javascript
text: "Loading complete"
```

2. **Wait for Removal**:
```javascript
textGone: "Loading..."
```

3. **Fixed Wait**:
```javascript
time: 2
```

**Best Practices:**
- Prefer waiting for specific conditions over fixed time
- Use for dynamic content loading
- Wait for animations to complete
- Ensure page stability before screenshots

### Tab Management

#### browser_tabs
Manage browser tabs.

**Parameters:**
```
action: "list", "new", "close", "select" (required)
index: Tab index for close/select (optional)
```

**Actions:**

1. **List Tabs**:
```javascript
action: "list"
```

2. **New Tab**:
```javascript
action: "new"
```

3. **Close Tab**:
```javascript
action: "close"
index: 1  // Optional, closes current if omitted
```

4. **Switch Tab**:
```javascript
action: "select"
index: 0
```

**Use Cases:**
- Multi-tab workflows
- Testing tab-specific features
- Opening links in new tabs
- Managing multiple sessions

### Browser Installation

#### browser_install
Install the browser specified in config.

**Parameters:** None

**When to Use:**
- First-time setup
- "Browser not installed" errors
- Updating browser version
- CI/CD environment setup

## Visual Testing Workflow Patterns

### Pattern 1: Basic Visual Regression Test

**Scenario:** Verify homepage hasn't changed visually

```workflow
1. Navigate to page
   - Use browser_navigate with target URL
   - Wait for page to load completely

2. Capture baseline
   - Take full-page screenshot
   - Use browser_snapshot for context
   - Document visible elements

3. Make changes (if testing changes)
   - Update code, deploy
   - Clear cache

4. Capture new state
   - Navigate to same URL
   - Take identical screenshot
   - Compare manually or with tools

5. Validate differences
   - Expected changes present
   - No unexpected regressions
   - Document findings
```

### Pattern 2: Responsive Design Testing

**Scenario:** Test layout across devices

```workflow
1. Define viewports
   - Mobile: 375x667 (iPhone SE)
   - Tablet: 768x1024 (iPad)
   - Desktop: 1920x1080 (Full HD)

2. For each viewport:
   a. Resize browser
      - browser_resize with dimensions

   b. Navigate to page
      - browser_navigate to URL

   c. Wait for layout
      - browser_wait_for with condition

   d. Capture snapshot
      - browser_snapshot for structure

   e. Take screenshot
      - browser_take_screenshot with descriptive name
      - Include viewport in filename

3. Compare layouts
   - Verify responsive breakpoints
   - Check element reflow
   - Validate mobile navigation
   - Ensure content accessibility

4. Document issues
   - Screenshot any problems
   - Note viewport where issue occurs
   - Record expected vs actual behavior
```

### Pattern 3: Form Testing Workflow

**Scenario:** Test multi-step form submission

```workflow
1. Navigate to form
   - browser_navigate to form URL
   - browser_snapshot to get field refs

2. Fill form fields
   - Use browser_fill_form for batch entry
   - Or individual browser_type for each field
   - Include validation triggers

3. Test validation
   - Submit with invalid data
   - browser_snapshot to see errors
   - Screenshot error states
   - Verify error messages appear

4. Complete valid submission
   - Fill all required fields
   - browser_click submit button
   - Wait for success message
   - browser_wait_for confirmation text

5. Verify results
   - Check success page
   - Verify data submission
   - Screenshot confirmation
   - Check network requests
```

### Pattern 4: Element-Specific Visual Testing

**Scenario:** Test individual component changes

```workflow
1. Navigate to component page
   - browser_navigate to page
   - browser_snapshot for structure

2. Locate component
   - Find element ref from snapshot
   - Verify component is visible

3. Test states
   a. Default state
      - Take element screenshot
      - Document initial appearance

   b. Hover state
      - browser_hover on element
      - Take element screenshot
      - Compare with default

   c. Active/focused state
      - browser_click on element
      - Take element screenshot
      - Verify visual feedback

   d. Error state (if applicable)
      - Trigger validation error
      - Take element screenshot
      - Verify error styling

4. Document state changes
   - Compare screenshots
   - Note expected behaviors
   - Report any issues
```

### Pattern 5: Cross-Browser Testing

**Scenario:** Verify consistency across browsers

```workflow
1. Define browser matrix
   - Chromium (Chrome/Edge)
   - Firefox
   - WebKit (Safari)

2. For each browser:
   a. Configure browser
      - Set in MCP server config

   b. Run test suite
      - Navigate to pages
      - Capture snapshots
      - Take screenshots
      - Test interactions

   c. Document results
      - Save browser-specific screenshots
      - Note rendering differences
      - Log browser-specific bugs

3. Compare results
   - Side-by-side screenshots
   - Functionality differences
   - Performance variations
   - CSS rendering issues

4. Address discrepancies
   - Fix critical cross-browser bugs
   - Document acceptable differences
   - Add browser-specific styles if needed
```

### Pattern 6: E2E User Journey Testing

**Scenario:** Complete user workflow validation

```workflow
1. Start journey
   - browser_navigate to landing page
   - browser_snapshot initial state
   - Screenshot starting point

2. Authentication
   - Navigate to login
   - Fill credentials with browser_fill_form
   - Submit form
   - Wait for redirect
   - Screenshot logged-in state

3. Main workflow steps
   For each step:
   - Take snapshot before action
   - Perform user action
   - Wait for completion
   - Take screenshot after action
   - Verify expected state

4. Complete transaction
   - Submit final action
   - Wait for confirmation
   - Screenshot success state
   - Verify completion message

5. Cleanup
   - Logout if needed
   - Screenshot final state
   - Document journey results
```

### Pattern 7: Accessibility Snapshot Testing

**Scenario:** Verify semantic structure and accessibility

```workflow
1. Navigate to page
   - browser_navigate to URL

2. Capture accessibility snapshot
   - browser_snapshot for semantic tree
   - Review element roles
   - Check heading hierarchy
   - Verify labels and descriptions

3. Validate structure
   - Proper heading levels (h1 → h2 → h3)
   - Form inputs have labels
   - Buttons have accessible names
   - Interactive elements have roles
   - ARIA attributes present

4. Test keyboard navigation
   - browser_press_key "Tab"
   - Snapshot after each tab
   - Verify focus indicators
   - Ensure logical tab order
   - Test skip links

5. Test screen reader experience
   - Review snapshot text content
   - Verify alt text present
   - Check ARIA live regions
   - Validate semantic landmarks
   - Ensure meaningful structure

6. Document findings
   - Screenshot accessibility tree
   - Note missing labels
   - Report hierarchy issues
   - Suggest improvements
```

## Browser Automation Best Practices

### Screenshot Best Practices

1. **Consistent Naming Convention**
```
{page}-{viewport}-{state}-{timestamp}.png

Examples:
homepage-desktop-default-1634567890.png
login-mobile-error-1634567891.png
checkout-tablet-success-1634567892.png
```

2. **Filename Organization**
```
screenshots/
  ├── baselines/
  │   ├── homepage-desktop.png
  │   ├── homepage-mobile.png
  │   └── homepage-tablet.png
  ├── current/
  │   └── homepage-desktop-20251017.png
  └── diffs/
      └── homepage-desktop-diff-20251017.png
```

3. **Full Page vs Viewport**
- Use full page for documentation
- Use viewport for regression testing
- Element screenshots for components
- Consider page length for full-page captures

4. **Image Format Selection**
- PNG: UI elements, text, sharp edges (lossless)
- JPEG: Photos, backgrounds, large images (smaller size)
- Use PNG by default for testing

### Snapshot vs Screenshot Strategy

**Use Snapshots When:**
- Automating interactions
- Testing functionality
- Verifying structure
- Checking accessibility
- Need element references
- Testing dynamic content

**Use Screenshots When:**
- Visual regression testing
- Documentation
- Bug reports
- Design reviews
- Stakeholder presentations
- Visual comparisons

**Use Both When:**
- Comprehensive testing
- Debugging visual issues
- Creating test reports
- Documenting complex flows

### Waiting Strategies

1. **Wait for Specific Elements**
```javascript
// Good
browser_wait_for with text: "Data loaded"

// Avoid
browser_wait_for with time: 5
```

2. **Wait for Animations**
```javascript
// Wait for loading spinner to disappear
browser_wait_for with textGone: "Loading..."
```

3. **Wait for Network Idle**
```javascript
// Check network requests after waiting
browser_network_requests to verify completion
```

4. **Dynamic Content**
```javascript
// Wait for specific text before screenshot
browser_wait_for with text: "Results: 42 items"
```

### Interaction Reliability

1. **Always Use Snapshots First**
```workflow
1. browser_snapshot
2. Find element ref in snapshot
3. Use ref for interaction
4. Never guess element references
```

2. **Verify Element State**
```javascript
// Take snapshot to verify element exists
// Check element is visible and actionable
// Then perform interaction
```

3. **Handle Dynamic Elements**
```javascript
// Wait for element to appear
browser_wait_for with text: "Submit"
// Then take fresh snapshot
browser_snapshot
// Get updated ref and interact
```

4. **Error Recovery**
```javascript
// If interaction fails:
1. Take screenshot of current state
2. Capture console messages (browser_console_messages)
3. Check network requests (browser_network_requests)
4. Take new snapshot to see current state
```

### Form Testing Strategy

1. **Batch vs Individual Entry**
```javascript
// Batch for simple forms (faster)
browser_fill_form with all fields

// Individual for complex forms (better control)
browser_type for each field
browser_wait_for after each entry
Verify validation triggers
```

2. **Validation Testing**
```javascript
// Test each validation rule
1. Enter invalid data
2. Attempt submission
3. Snapshot to see errors
4. Screenshot error messages
5. Correct data
6. Verify error clears
```

3. **Multi-Step Forms**
```javascript
// Document each step
1. Fill step 1
2. Screenshot before submit
3. Click next
4. Wait for step 2
5. Snapshot new state
6. Repeat for each step
```

### Network Monitoring

1. **Track API Calls**
```javascript
// After user action
browser_network_requests
// Verify expected endpoints called
// Check status codes
// Validate request/response data
```

2. **Performance Testing**
```javascript
// Capture network timing
browser_network_requests
// Analyze:
- Request count
- Total transfer size
- Response times
- Failed requests
```

3. **Debug Failed Requests**
```javascript
browser_network_requests
// Find failed requests
// Check error messages
// Screenshot current state
// Console messages for errors
```

## Development Acceleration Strategies

### Strategy 1: Test Template Creation

Create reusable test patterns:

```template
Visual Regression Test Template:
1. Navigate: browser_navigate to {URL}
2. Wait: browser_wait_for for {condition}
3. Baseline: browser_take_screenshot "baseline-{name}.png", fullPage: true
4. [Make changes]
5. Capture: browser_take_screenshot "current-{name}.png", fullPage: true
6. Compare: [Manual or automated comparison]
7. Document: Screenshot any differences

Responsive Test Template:
For viewport in [mobile, tablet, desktop]:
  1. Resize: browser_resize to {viewport dimensions}
  2. Navigate: browser_navigate to {URL}
  3. Wait: browser_wait_for for stability
  4. Snapshot: browser_snapshot
  5. Screenshot: browser_take_screenshot "{page}-{viewport}.png"
  6. Validate: Check layout integrity

Form Test Template:
1. Navigate: browser_navigate to {form URL}
2. Snapshot: browser_snapshot for refs
3. Fill: browser_fill_form with test data
4. Screenshot: "form-filled.png"
5. Submit: browser_click submit button
6. Wait: browser_wait_for for result
7. Verify: Snapshot and screenshot result
8. Check: browser_network_requests for submission
```

### Strategy 2: Automated Screenshot Organization

Organize screenshots systematically:

```organization
Project Structure:
tests/
  visual/
    baselines/        # Reference screenshots
    results/          # Current test screenshots
    diffs/            # Difference images
    reports/          # HTML reports with comparisons

Naming Convention:
{test-name}_{viewport}_{state}_{date}.png

Examples:
login_desktop_default_20251017.png
cart_mobile_empty_20251017.png
checkout_tablet_error_20251017.png

Metadata File:
screenshot-metadata.json:
{
  "screenshot": "login_desktop_default_20251017.png",
  "timestamp": "2025-10-17T10:30:00Z",
  "url": "https://example.com/login",
  "viewport": {"width": 1920, "height": 1080},
  "browser": "chromium",
  "test": "login_flow",
  "passed": true
}
```

### Strategy 3: Parallel Multi-Browser Testing

Test across browsers efficiently:

```strategy
Browser Matrix:
- Chromium (latest)
- Firefox (latest)
- WebKit (latest)

Parallel Execution:
1. Define test suite
2. Configure each browser
3. Run tests in parallel
4. Collect results
5. Compare across browsers
6. Generate cross-browser report

Result Organization:
screenshots/
  chromium/
    homepage.png
    login.png
  firefox/
    homepage.png
    login.png
  webkit/
    homepage.png
    login.png
  comparison/
    homepage-browsers.html
    login-browsers.html
```

### Strategy 4: Visual Regression Automation

Automate visual comparison workflow:

```automation
1. Capture Baselines (one-time):
   - Navigate to each page
   - Take reference screenshots
   - Store in baselines/

2. Run Visual Tests:
   - Navigate to each page
   - Take current screenshots
   - Store in results/

3. Compare Images:
   - Pixel-by-pixel comparison
   - Highlight differences
   - Generate diff images
   - Calculate similarity score

4. Generate Report:
   - List all comparisons
   - Show side-by-side views
   - Highlight failures
   - Include metrics

5. Review and Update:
   - Review failures
   - Accept intentional changes
   - Update baselines
   - Fix regressions
```

### Strategy 5: Component Library Testing

Test design system components:

```strategy
Component Test Suite:
For each component:
  1. Navigate to component page
  2. Snapshot for structure
  3. Test each variant:
     - Default
     - Hover
     - Active
     - Disabled
     - Error
  4. Screenshot each state
  5. Verify accessibility
  6. Check responsive behavior

Documentation Generation:
1. Capture all component states
2. Organize by component
3. Generate visual catalog
4. Include code examples
5. Document usage guidelines

Example:
components/
  Button/
    button-default.png
    button-hover.png
    button-active.png
    button-disabled.png
    button-error.png
  Input/
    input-default.png
    input-focus.png
    input-error.png
    input-disabled.png
```

## Troubleshooting

### Common Issues

**Screenshot appears blank**
- Wait for page to load: browser_wait_for
- Check if element is visible: browser_snapshot
- Ensure page has rendered: Add delay
- Verify URL is correct

**Element not found for interaction**
- Take fresh snapshot: browser_snapshot
- Check element ref is current
- Wait for element to appear: browser_wait_for
- Verify element exists in snapshot

**Browser not launching**
- Run browser_install
- Check MCP server configuration
- Verify browser binary path
- Check system permissions

**Screenshot differs from expected**
- Check viewport size: browser_resize
- Wait for animations: browser_wait_for
- Ensure font loading complete
- Disable dynamic content (timestamps, ads)

**Form submission fails**
- Verify all required fields filled
- Check validation errors: browser_snapshot
- Wait for submit button to be enabled
- Check console for JavaScript errors: browser_console_messages

**Network requests not captured**
- Call browser_network_requests after action
- Ensure page has completed requests
- Check for request failures
- Verify request timing

**Dialog not handled**
- Set up browser_handle_dialog before triggering
- Accept or dismiss appropriately
- Provide promptText for prompt dialogs
- Test dialog in advance

### Debugging Workflow

1. **Capture Current State**
```workflow
1. browser_snapshot - See page structure
2. browser_take_screenshot - See visual state
3. browser_console_messages onlyErrors: true - Check errors
4. browser_network_requests - See network activity
```

2. **Isolate Issue**
```workflow
1. Simplify test to minimum reproduction
2. Test in single browser
3. Disable dynamic content
4. Remove variable elements
5. Test step-by-step
```

3. **Document Problem**
```workflow
1. Screenshot before issue
2. Screenshot at failure point
3. Capture console messages
4. Save network requests
5. Note expected vs actual
6. Include reproduction steps
```

## Practical Examples

### Example 1: Homepage Visual Regression

**Test homepage hasn't visually changed:**

```test
1. Navigate
   browser_navigate
   url: "https://example.com"

2. Wait for page load
   browser_wait_for
   textGone: "Loading..."

3. Capture baseline
   browser_take_screenshot
   filename: "homepage-baseline.png"
   fullPage: true

4. [After code changes, repeat]

5. Capture current
   browser_take_screenshot
   filename: "homepage-current.png"
   fullPage: true

6. Compare images manually or with tools
7. Document differences
```

### Example 2: Login Form Testing

**Test login form functionality:**

```test
1. Navigate to login
   browser_navigate
   url: "https://example.com/login"

2. Get form structure
   browser_snapshot

3. Fill form
   browser_fill_form
   fields: [
     {
       name: "Email",
       type: "textbox",
       ref: "123",
       value: "test@example.com"
     },
     {
       name: "Password",
       type: "textbox",
       ref: "456",
       value: "password123"
     }
   ]

4. Screenshot filled form
   browser_take_screenshot
   filename: "login-filled.png"

5. Submit
   browser_click
   element: "Sign In button"
   ref: "789"

6. Wait for redirect
   browser_wait_for
   text: "Welcome back"

7. Screenshot success
   browser_take_screenshot
   filename: "login-success.png"

8. Verify network request
   browser_network_requests
```

### Example 3: Responsive Design Check

**Test responsive layout:**

```test
Mobile:
1. Resize to mobile
   browser_resize
   width: 375
   height: 667

2. Navigate
   browser_navigate
   url: "https://example.com"

3. Wait
   browser_wait_for
   time: 2

4. Screenshot
   browser_take_screenshot
   filename: "homepage-mobile.png"
   fullPage: true

Tablet:
5. Resize to tablet
   browser_resize
   width: 768
   height: 1024

6. Navigate
   browser_navigate
   url: "https://example.com"

7. Screenshot
   browser_take_screenshot
   filename: "homepage-tablet.png"
   fullPage: true

Desktop:
8. Resize to desktop
   browser_resize
   width: 1920
   height: 1080

9. Navigate
   browser_navigate
   url: "https://example.com"

10. Screenshot
    browser_take_screenshot
    filename: "homepage-desktop.png"
    fullPage: true
```

### Example 4: Component State Testing

**Test button states:**

```test
1. Navigate to component library
   browser_navigate
   url: "https://example.com/components/button"

2. Get page structure
   browser_snapshot

3. Default state
   browser_take_screenshot
   filename: "button-default.png"
   element: "Primary button"
   ref: "123"

4. Hover state
   browser_hover
   element: "Primary button"
   ref: "123"

   browser_take_screenshot
   filename: "button-hover.png"
   element: "Primary button"
   ref: "123"

5. Active state
   browser_click
   element: "Primary button"
   ref: "123"

   browser_take_screenshot
   filename: "button-active.png"
   element: "Primary button"
   ref: "123"

6. Snapshot for verification
   browser_snapshot
```

### Example 5: E2E Checkout Flow

**Test complete checkout process:**

```test
1. Navigate to product
   browser_navigate
   url: "https://example.com/products/item-123"

2. Add to cart
   browser_snapshot

   browser_click
   element: "Add to Cart button"
   ref: "456"

   browser_wait_for
   text: "Added to cart"

3. Go to cart
   browser_click
   element: "Cart icon"
   ref: "789"

   browser_take_screenshot
   filename: "cart-with-item.png"

4. Proceed to checkout
   browser_click
   element: "Checkout button"
   ref: "101"

5. Fill shipping info
   browser_snapshot

   browser_fill_form
   fields: [
     {name: "Name", type: "textbox", ref: "111", value: "John Doe"},
     {name: "Address", type: "textbox", ref: "222", value: "123 Main St"},
     {name: "City", type: "textbox", ref: "333", value: "New York"},
     {name: "Zip", type: "textbox", ref: "444", value: "10001"}
   ]

6. Screenshot checkout
   browser_take_screenshot
   filename: "checkout-filled.png"
   fullPage: true

7. Complete order
   browser_click
   element: "Place Order button"
   ref: "555"

   browser_wait_for
   text: "Order confirmed"

8. Screenshot confirmation
   browser_take_screenshot
   filename: "order-confirmed.png"
   fullPage: true

9. Verify network requests
   browser_network_requests
```

### Example 6: Accessibility Testing

**Test keyboard navigation and structure:**

```test
1. Navigate to page
   browser_navigate
   url: "https://example.com/form"

2. Capture semantic structure
   browser_snapshot

3. Verify heading hierarchy
   - Check h1 → h2 → h3 order
   - Ensure single h1
   - Verify logical structure

4. Test keyboard navigation
   browser_press_key
   key: "Tab"

   browser_snapshot

   browser_take_screenshot
   filename: "focus-field-1.png"

5. Continue tabbing
   browser_press_key
   key: "Tab"

   browser_snapshot

   browser_take_screenshot
   filename: "focus-field-2.png"

6. Verify all interactive elements reachable
   - Buttons
   - Links
   - Form fields
   - Custom widgets

7. Check ARIA labels
   - Form labels present
   - Button labels descriptive
   - Error messages announced
   - Status updates live

8. Screenshot accessibility tree
   browser_take_screenshot
   filename: "accessibility-structure.png"
```

### Example 7: Network Debugging

**Debug failed API calls:**

```test
1. Navigate to page
   browser_navigate
   url: "https://example.com/dashboard"

2. Wait for page
   browser_wait_for
   time: 3

3. Check console errors
   browser_console_messages
   onlyErrors: true

4. Check network requests
   browser_network_requests

5. Find failed requests
   - Status: 4xx or 5xx
   - Timeout errors
   - CORS issues

6. Screenshot error state
   browser_take_screenshot
   filename: "api-error-state.png"

7. Retry action
   browser_click
   element: "Refresh button"
   ref: "123"

8. Monitor new requests
   browser_network_requests

9. Document findings
   - Failed endpoint
   - Error message
   - Request/response data
   - Screenshot
```

### Example 8: Dialog Handling

**Test confirmation dialogs:**

```test
1. Navigate to page
   browser_navigate
   url: "https://example.com/settings"

2. Trigger delete action
   browser_snapshot

   browser_click
   element: "Delete Account button"
   ref: "123"

3. Handle confirmation
   browser_handle_dialog
   accept: false  # Cancel first time

4. Verify still on page
   browser_snapshot

5. Try again
   browser_click
   element: "Delete Account button"
   ref: "123"

6. Accept this time
   browser_handle_dialog
   accept: true

7. Wait for result
   browser_wait_for
   text: "Account deleted"

8. Screenshot confirmation
   browser_take_screenshot
   filename: "account-deleted.png"
```

### Example 9: Tab Management

**Test multi-tab workflow:**

```test
1. List current tabs
   browser_tabs
   action: "list"

2. Open link in new tab
   browser_click
   element: "Privacy Policy link"
   ref: "123"
   modifiers: ["ControlOrMeta"]

3. Switch to new tab
   browser_tabs
   action: "select"
   index: 1

4. Screenshot new tab
   browser_take_screenshot
   filename: "privacy-policy.png"

5. Switch back
   browser_tabs
   action: "select"
   index: 0

6. Close extra tab
   browser_tabs
   action: "close"
   index: 1

7. Verify single tab
   browser_tabs
   action: "list"
```

### Example 10: Animation Testing

**Test loading animations:**

```test
1. Navigate to page
   browser_navigate
   url: "https://example.com/data-heavy"

2. Screenshot loading state
   browser_take_screenshot
   filename: "loading-spinner.png"

3. Wait for loading to complete
   browser_wait_for
   textGone: "Loading..."

4. Wait for animations
   browser_wait_for
   time: 1

5. Screenshot final state
   browser_take_screenshot
   filename: "content-loaded.png"
   fullPage: true

6. Verify stability
   browser_wait_for
   time: 2

   browser_take_screenshot
   filename: "stable-state.png"
   fullPage: true

7. Compare screenshots
   - loading-spinner.png
   - content-loaded.png
   - stable-state.png
```

## Quick Reference

### Essential Commands

```
Navigate:
  browser_navigate url: "{URL}"

Snapshot:
  browser_snapshot

Screenshot:
  browser_take_screenshot filename: "{name}.png"

Full Page Screenshot:
  browser_take_screenshot filename: "{name}.png", fullPage: true

Element Screenshot:
  browser_take_screenshot filename: "{name}.png", element: "{description}", ref: "{ref}"

Click:
  browser_click element: "{description}", ref: "{ref}"

Type:
  browser_type element: "{description}", ref: "{ref}", text: "{text}"

Fill Form:
  browser_fill_form fields: [{name, type, ref, value}, ...]

Wait:
  browser_wait_for text: "{text}"
  browser_wait_for textGone: "{text}"
  browser_wait_for time: {seconds}

Resize:
  browser_resize width: {width}, height: {height}

Console:
  browser_console_messages onlyErrors: true

Network:
  browser_network_requests
```

### Common Viewport Sizes

```
Mobile:
  375 x 667   (iPhone SE)
  390 x 844   (iPhone 12/13/14)
  414 x 896   (iPhone 11 Pro Max)
  360 x 640   (Android Small)
  412 x 915   (Android Large)

Tablet:
  768 x 1024  (iPad Portrait)
  1024 x 768  (iPad Landscape)
  810 x 1080  (Android Tablet)

Desktop:
  1280 x 720  (HD)
  1366 x 768  (Laptop)
  1920 x 1080 (Full HD)
  2560 x 1440 (2K)
  3840 x 2160 (4K)
```

### Test Organization Template

```
tests/
  ├── visual/
  │   ├── baselines/
  │   ├── results/
  │   └── diffs/
  ├── e2e/
  │   ├── auth/
  │   ├── checkout/
  │   └── navigation/
  ├── responsive/
  │   ├── mobile/
  │   ├── tablet/
  │   └── desktop/
  └── components/
      ├── buttons/
      ├── forms/
      └── navigation/

reports/
  ├── visual-regression.html
  ├── cross-browser.html
  └── accessibility.html
```

## Resources

- [Playwright Documentation](https://playwright.dev)
- [Playwright API Reference](https://playwright.dev/docs/api/class-playwright)
- [Playwright MCP Server](https://github.com/microsoft/playwright-mcp)
- [Visual Testing Guide](https://playwright.dev/docs/test-snapshots)
- [Best Practices](https://playwright.dev/docs/best-practices)
- [Accessibility Testing](https://playwright.dev/docs/accessibility-testing)

---

**Skill Version**: 1.0.0
**Last Updated**: October 2025
**Skill Category**: Browser Automation, Visual Testing, Quality Assurance
**Compatible With**: Playwright MCP Server, Chromium, Firefox, WebKit
