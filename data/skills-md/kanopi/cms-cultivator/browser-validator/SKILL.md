---
name: browser-validator
description: Automatically validate implementations in real browsers after code is written or when user says "test this". Uses Chrome DevTools MCP to test responsive breakpoints (320px, 768px, 1024px), check accessibility compliance (WCAG AA contrast, keyboard navigation, ARIA), validate interactions, and generate detailed technical reports with file paths and specific fixes.
---

# Browser Validator Skill

## Purpose
Validate design implementations in real browsers using Chrome DevTools MCP to ensure quality, accessibility, and responsiveness.

## Philosophy

Real browser testing catches issues that code review cannot.

### Core Beliefs

1. **Test in Real Environments**: Browsers behave differently than localhost
2. **Multiple Breakpoints Required**: Mobile, tablet, desktop have different challenges
3. **Accessibility Requires Manual Verification**: Automated tools miss context-dependent issues
4. **Visual QA Prevents Surprises**: Screenshots catch layout breaks before users see them

### Why Browser Validation Matters

- **Cross-Browser Consistency**: Ensure components work everywhere
- **Responsive Behavior**: Verify breakpoints function correctly
- **Accessibility Compliance**: Check keyboard navigation and screen reader compatibility
- **Professional Quality**: Catch visual regressions before deployment

## When This Skill Activates

This skill automatically activates when:
- User says "test this", "validate", "check if it works"
- After component implementation is complete
- User asks "does it look right?"
- User mentions "browser", "Chrome", or "DevTools"
- Component is ready for QA
- Before submitting for review

## Decision Framework

Before validating in browser, determine:

### What Needs Validation?

1. **Responsive behavior** → Test layout at 320px, 768px, 1024px breakpoints
2. **Accessibility** → Check contrast, keyboard nav, ARIA, focus indicators
3. **Interactions** → Test hover, click, focus states
4. **Visual accuracy** → Compare with design reference (if provided)
5. **Functionality** → Verify buttons, forms, links work correctly

### What Are the Test URLs?

**Local development**:
- `http://localhost:8000/component`
- `http://site.ddev.site/test-page`
- `http://site.test/node/123`

**Staging/production**:
- `https://staging.example.com/feature`
- `https://production.com/public-page`

**URL must be**:
- Accessible from your machine
- Fully loaded (not 404, not auth-protected)
- Stable (not constantly changing)

### What Breakpoints to Test?

**Standard breakpoints** (always test):
- ✅ **Mobile**: 320px x 568px (minimum, iPhone SE)
- ✅ **Tablet**: 768px x 1024px (iPad)
- ✅ **Desktop**: 1024px x 768px (laptop)
- ⚠️ **Large desktop**: 1920px x 1080px (optional)

**What to check at each breakpoint**:
- Layout doesn't break
- No horizontal scrolling
- Text is readable (no overflow)
- Touch targets ≥ 44px (mobile), ≥ 40px (desktop)
- Images don't extend beyond viewport

### What Accessibility Checks?

**WCAG 2.1 Level AA (always check)**:
- ✅ **Color contrast**: Calculate exact ratios (4.5:1 normal, 3:1 large)
- ✅ **Keyboard navigation**: Tab through all interactive elements
- ✅ **Focus indicators**: Visible 2px minimum
- ✅ **Semantic HTML**: Proper headings, landmarks, ARIA
- ✅ **Alt text**: Content images have descriptive alt, decorative have alt=""

**How to test**:
- Use `mcp__chrome-devtools__press_key` to Tab through page
- Use `mcp__chrome-devtools__take_snapshot` to check DOM structure
- Calculate contrast ratios from screenshots

### What Interactions to Test?

**Interactive states**:
- `:hover` - Use `mcp__chrome-devtools__hover` on elements
- `:focus` - Tab to elements with keyboard
- `:active` - Click elements with `mcp__chrome-devtools__click`

**Capture screenshots**:
- Initial state
- Each breakpoint
- Hover/focus states
- Any dynamic behavior

### What Errors to Check?

**Console errors**:
- Use `mcp__chrome-devtools__list_console_messages`
- Check for JavaScript errors
- Report with stack traces

**Network issues**:
- Use `mcp__chrome-devtools__list_network_requests`
- Check for 404s, failed requests
- Note slow-loading resources

### Decision Tree

```
User requests browser validation
    ↓
Check: Chrome DevTools MCP available?
    ↓ Yes
Navigate to test URL
    ↓
Test each breakpoint (320/768/1024px)
    ↓
Capture screenshots at each breakpoint
    ↓
Check accessibility (contrast/keyboard/ARIA)
    ↓
Test interactions (hover/focus/click)
    ↓
Check console & network errors
    ↓
Generate detailed technical report
```

## Required MCP Integration

This skill requires **Chrome DevTools MCP** integration. Correct tool names to use:

**Navigation & Pages**:
- `mcp__chrome-devtools__navigate_page` - Navigate to URL
- `mcp__chrome-devtools__list_pages` - Get available pages
- `mcp__chrome-devtools__new_page` - Create new tab

**Viewport & Screenshots**:
- `mcp__chrome-devtools__resize_page` - Change viewport size
- `mcp__chrome-devtools__take_screenshot` - Capture screenshot
- `mcp__chrome-devtools__take_snapshot` - Get DOM structure

**Interaction**:
- `mcp__chrome-devtools__click` - Click element by UID
- `mcp__chrome-devtools__hover` - Hover over element
- `mcp__chrome-devtools__fill` - Fill form field
- `mcp__chrome-devtools__press_key` - Press keyboard key

**Debugging**:
- `mcp__chrome-devtools__list_console_messages` - Get JavaScript errors
- `mcp__chrome-devtools__list_network_requests` - Check network activity

## Validation Process

### Phase 1: Initial Setup

```javascript
// Navigate to test page
await mcp__chrome-devtools__navigate_page({
  url: testUrl,
  type: "url"
});

// Wait for page load (built-in)

// Take initial full-page screenshot
await mcp__chrome-devtools__take_screenshot({
  filePath: "screenshots/component/initial-fullpage.png",
  fullPage: true
});

// Get page structure
const pageSnapshot = await mcp__chrome-devtools__take_snapshot({
  verbose: true
});
```

### Phase 2: DOM Structure Validation

```javascript
// Get detailed page structure
const pageStructure = await mcp__chrome-devtools__take_snapshot({
  verbose: true
});

// Check for:
// - Proper semantic HTML
// - Heading hierarchy
// - Form labels
// - Image alt attributes
// - ARIA attributes
// - No empty elements
```

**Semantic HTML Checklist:**
- [ ] `<header>` for site/section header
- [ ] `<nav>` for navigation
- [ ] `<main>` for main content (only one per page)
- [ ] `<article>` for self-contained content
- [ ] `<section>` for thematic grouping
- [ ] `<aside>` for tangentially related content
- [ ] `<footer>` for site/section footer

**Heading Hierarchy Check:**
```
✅ GOOD:
<h1>Page Title</h1>
  <h2>Section 1</h2>
    <h3>Subsection 1.1</h3>
  <h2>Section 2</h2>

❌ BAD:
<h1>Page Title</h1>
  <h3>Section 1</h3>  ← Skipped h2
  <h2>Section 2</h2>
```

**Image Alt Text Check:**
```
✅ Content images: <img src="chart.png" alt="Q3 sales chart showing 25% growth">
✅ Decorative images: <img src="divider.png" alt="">
❌ Missing alt: <img src="photo.png">
```

### Phase 3: Responsive Testing

Test at all standard breakpoints:

```javascript
// Mobile (320px)
await mcp__chrome-devtools__resize_page({
  width: 320,
  height: 568
});
await mcp__chrome-devtools__take_screenshot({
  filePath: "screenshots/component/mobile-320px.png"
});

// Tablet (768px)
await mcp__chrome-devtools__resize_page({
  width: 768,
  height: 1024
});
await mcp__chrome-devtools__take_screenshot({
  filePath: "screenshots/component/tablet-768px.png"
});

// Desktop (1024px)
await mcp__chrome-devtools__resize_page({
  width: 1024,
  height: 768
});
await mcp__chrome-devtools__take_screenshot({
  filePath: "screenshots/component/desktop-1024px.png"
});

// Large Desktop (1920px) - optional
await mcp__chrome-devtools__resize_page({
  width: 1920,
  height: 1080
});
await mcp__chrome-devtools__take_screenshot({
  filePath: "screenshots/component/large-1920px.png"
});
```

**Mobile Validation (320px-767px):**
- [ ] No horizontal scrolling
- [ ] Text is readable (minimum 16px)
- [ ] Touch targets are 44px minimum
- [ ] Images scale properly
- [ ] Content stacks vertically
- [ ] Navigation is accessible
- [ ] Forms are usable

**Tablet Validation (768px-1023px):**
- [ ] Layout transitions smoothly
- [ ] Multi-column layouts work
- [ ] Navigation adapts appropriately
- [ ] Images maintain aspect ratio
- [ ] Spacing increases appropriately

**Desktop Validation (1024px+):**
- [ ] Full layout displays correctly
- [ ] Hover states function
- [ ] Maximum width constraints work
- [ ] Multi-column content aligns
- [ ] No excessive white space

### Phase 4: Interactive Elements Testing

Test all interactive elements:

```javascript
// Get page snapshot with element UIDs
const snapshot = await mcp__chrome-devtools__take_snapshot({
  verbose: false
});

// Find buttons by UID from snapshot
const buttons = snapshot.elements.filter(el => el.role === 'button');

// Test each button
for (const button of buttons) {
  // Hover test
  await mcp__chrome-devtools__hover({
    uid: button.uid
  });

  await mcp__chrome-devtools__take_screenshot({
    filePath: `screenshots/component/button-${button.uid}-hover.png`
  });

  // Click test
  await mcp__chrome-devtools__click({
    uid: button.uid
  });

  // Check result (wait for any changes)
  // Take screenshot if needed
}

// Test form interactions
const formInputs = snapshot.elements.filter(el => el.role === 'textbox');

for (const input of formInputs) {
  // Fill input
  await mcp__chrome-devtools__fill({
    uid: input.uid,
    value: "Test Value"
  });

  // Verify input accepted
}

// Test keyboard navigation
await mcp__chrome-devtools__press_key({
  key: "Tab"
});

// Check focus moved to next element
```

**Button/Link Checklist:**
- [ ] All buttons are clickable
- [ ] Links navigate to correct URLs
- [ ] Hover states appear
- [ ] Focus states are visible
- [ ] Disabled states are clear
- [ ] Loading states work (if applicable)

### Phase 5: Keyboard Navigation Testing

Test complete keyboard navigation flow:

```javascript
// Start from top of page
await mcp__chrome-devtools__navigate_page({
  url: testUrl,
  type: "reload"
});

// Tab through interactive elements
for (let i = 0; i < 10; i++) {
  await mcp__chrome-devtools__press_key({
    key: "Tab"
  });

  // Take snapshot to see what's focused
  const snapshot = await mcp__chrome-devtools__take_snapshot({
    verbose: false
  });

  // Check that focus indicator is visible
  // Check focus order is logical
}

// Test other keyboard interactions
await mcp__chrome-devtools__press_key({
  key: "Enter"  // Activate button
});

await mcp__chrome-devtools__press_key({
  key: "Escape"  // Close modal
});

await mcp__chrome-devtools__press_key({
  key: "Space"  // Activate button/checkbox
});
```

**Keyboard Navigation Checklist:**
- [ ] All interactive elements are focusable
- [ ] Focus order is logical (top→bottom, left→right)
- [ ] Focus indicators are visible (2px outline minimum)
- [ ] Enter/Space activates buttons
- [ ] Escape closes modals/dialogs
- [ ] Arrow keys work for custom components
- [ ] No keyboard traps

### Phase 6: Color Contrast Analysis

Check all text meets WCAG AA requirements:

```javascript
// Get all text elements from snapshot
const textElements = snapshot.elements.filter(el => el.text);

// For each text element:
// 1. Get computed foreground color
// 2. Get computed background color
// 3. Calculate contrast ratio
// 4. Compare against WCAG requirements

// WCAG AA Requirements:
// - Normal text (< 18pt or < 14pt bold): 4.5:1
// - Large text (≥ 18pt or ≥ 14pt bold): 3:1
// - UI components: 3:1
```

**Contrast Ratio Calculation:**
```
Relative Luminance (L) = 0.2126 * R + 0.7152 * G + 0.0722 * B
(where R, G, B are gamma corrected)

Contrast Ratio = (L1 + 0.05) / (L2 + 0.05)
(where L1 is lighter, L2 is darker)
```

**Example:**
```
Text: #666666 (rgb(102, 102, 102))
Background: #ffffff (rgb(255, 255, 255))

L1 = 1.0 (white)
L2 = 0.132 (gray)

Ratio = (1.0 + 0.05) / (0.132 + 0.05) = 3.8:1
Result: ❌ Fails WCAG AA (need 4.5:1)

Fix: Use #595959 instead
New ratio = 4.54:1 ✅ Passes
```

### Phase 7: Console and Network Analysis

Check for JavaScript errors and network issues:

```javascript
// Get console messages
const consoleMessages = await mcp__chrome-devtools__list_console_messages({
  types: ["error", "warn"],
  pageSize: 100
});

// Analyze errors
const errors = consoleMessages.filter(msg => msg.type === "error");
const warnings = consoleMessages.filter(msg => msg.type === "warn");

// Get network requests
const networkRequests = await mcp__chrome-devtools__list_network_requests({
  resourceTypes: ["document", "script", "stylesheet", "image"],
  pageSize: 100
});

// Find failed requests
const failedRequests = networkRequests.filter(req => req.status >= 400);
```

**Console Issues to Report:**
- ❌ JavaScript errors (with stack traces)
- ⚠️  Console warnings
- ❌ 404 errors (missing resources)
- ❌ CORS errors
- ⚠️  Deprecated API usage
- ❌ Network failures

### Phase 8: Accessibility Audit

Comprehensive accessibility checks:

**Focus Indicators:**
```javascript
// Check all focusable elements have visible indicators
// Minimum 2px outline
// High contrast color
// Non-hidden
```

**ARIA Usage:**
```javascript
// Check proper ARIA attributes:
// - aria-label on icon-only buttons
// - aria-describedby for complex widgets
// - aria-live for dynamic content
// - aria-hidden for decorative elements
// - role attributes where needed
```

**Touch Targets:**
```javascript
// Measure all interactive elements
// Must be ≥ 44x44px on mobile viewports
// Spacing between targets ≥ 8px
```

## Report Format

Generate detailed technical report:

```markdown
# Validation Report: Component Name
**URL**: {test-url}
**Date**: {timestamp}

## 📊 Summary
✅ Passed: {N} checks
⚠️  Warnings: {N} checks
❌ Failed: {N} checks

## 📱 Responsive Behavior

### Mobile (320px)
Screenshot: screenshots/component/mobile-320px.png
**Issues:**
❌ Text overflow in heading
   File: components/hero.scss:45
   Current: font-size: 2rem;
   Fix: font-size: clamp(1.5rem, 5vw, 2rem);

### Tablet (768px)
✅ Layout optimal

### Desktop (1024px)
✅ Layout optimal

## ♿ Accessibility

### Color Contrast
❌ Body text: 3.8:1 (need 4.5:1)
   File: components/hero.scss:23
   Current: color: #666
   Fix: color: #595959
   Calculation: (255+0.05)/(89+0.05) = 4.54:1 ✅

### Keyboard Navigation
✅ All elements focusable
⚠️  Focus indicator weak (1px)
   File: base/buttons.scss:15
   Fix: outline: 2px solid; outline-offset: 2px;

### ARIA
⚠️  Icon button missing label
   File: patterns/hero.php:42
   Fix: Add aria-label="Close banner"

## 🖱️  Interactions
✅ Hover states working
✅ Click handlers functioning

## 🐛 Console & Network
✅ No JavaScript errors
✅ All resources loaded

## 📝 Recommendations (Priority Order)

🔴 CRITICAL
1. Fix body text contrast (hero.scss:23)
2. Add aria-label to icon button (hero.php:42)

🟡 IMPORTANT
3. Fix mobile text overflow (hero.scss:45)
4. Strengthen focus indicators (buttons.scss:15)

🟢 NICE TO HAVE
5. Increase touch target size (hero.scss:67)
```

## Error Handling

### Chrome DevTools MCP Not Available

If Chrome DevTools MCP is not connected, provide manual checklist:

```markdown
❌ Chrome DevTools MCP not connected

Browser validation requires Chrome DevTools MCP.

**To enable:**
1. Install: https://github.com/anthropics/claude-chrome-mcp
2. Configure in Claude Code settings
3. Restart Claude Code
4. Retry validation

**Alternative: Manual Validation Checklist**

Test URL: {test-url}

📋 Responsive Testing:
□ View at 320px width (mobile)
□ View at 768px width (tablet)
□ View at 1024px+ width (desktop)
□ No horizontal scrolling on mobile
□ Touch targets ≥ 44px on mobile

📋 Accessibility:
□ Check contrast: https://webaim.org/resources/contrastchecker/
□ Test Tab key navigation
□ Verify focus indicators visible
□ Check heading hierarchy
□ Verify alt text on images

📋 Interactions:
□ Test all hover states
□ Test all click actions
□ Check console for errors
□ Verify network requests successful
```

### Test URL Not Accessible

```markdown
❌ Cannot access test URL: {url}

**Possible issues:**
- Local dev server not running
- URL typo
- Network/firewall restrictions
- HTTPS certificate issues

**Solutions:**
1. Verify URL in browser first
2. Check dev server is running
3. Try alternate URL
4. Check /etc/hosts for local domains
```

## Best Practices

1. **Test Early**: Don't wait until implementation is complete
2. **Test Often**: Validate after each significant change
3. **Fix Critical First**: Address WCAG failures before UX issues
4. **Re-validate**: Always re-run after applying fixes
5. **Real Devices**: Follow up automated tests with real device testing
6. **Document Issues**: Save reports for reference and tracking

## Integration with Commands

This skill is used by:

### `/design-to-block` Command
- Validates WordPress block patterns after creation
- Checks responsive behavior
- Ensures accessibility compliance

### `/design-to-paragraph` Command
- Validates Drupal paragraph types after creation
- Tests responsive layouts
- Verifies accessibility

### `/design-validate` Command
- Standalone validation of any implementation
- Can compare against design reference
- Generates detailed technical report

## Common Validation Failures

### Text Overflow on Mobile
**Symptom**: Heading text wraps awkwardly or extends beyond container
**Fix**: Use fluid typography with `clamp()`

### Low Contrast
**Symptom**: Text difficult to read, fails WCAG AA
**Fix**: Darken text color or lighten background

### Weak Focus Indicators
**Symptom**: Hard to see which element has keyboard focus
**Fix**: Increase outline to 2px, add offset

### Small Touch Targets
**Symptom**: Buttons/links difficult to tap on mobile
**Fix**: Increase padding to ensure 44px minimum

### Missing ARIA Labels
**Symptom**: Screen readers can't identify icon-only buttons
**Fix**: Add `aria-label` with descriptive text

### JavaScript Errors
**Symptom**: Console shows errors, functionality broken
**Fix**: Debug and fix JavaScript, verify asset paths

## Testing Scope

**What this validates:**
- ✅ Responsive layouts at multiple breakpoints
- ✅ WCAG AA accessibility (contrast, keyboard nav, ARIA)
- ✅ Interactive element functionality
- ✅ JavaScript console errors
- ✅ Network request failures
- ✅ Visual accuracy (if design reference provided)

**What this does NOT validate:**
- ❌ Cross-browser compatibility (Chrome only)
- ❌ Performance metrics (use performance tools)
- ❌ Security vulnerabilities
- ❌ Code quality
- ❌ SEO
