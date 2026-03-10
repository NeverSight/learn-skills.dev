---
name: helpmetest-visual-check
description: "Instant visual verification via screenshots. For quick checks like 'does button look blue', 'is layout centered', 'header look right on mobile'. Fast alternative to formal testing - just look and confirm. Use when user wants visual inspection without creating test files."
argument-hint: [url-or-description]
allowed-tools: mcp__helpmetest-*
---

# Visual Check

Quick visual verification using screenshots. Tests how things look without creating formal test files.

## When to Use This Skill

Use when user asks casual verification questions like:
- "Check if the login button is blue"
- "Does the header look right on mobile?"
- "See if the pricing table is centered"
- "Is the footer visible?"
- "Verify the hero image loaded"
- "Check that modal is showing correctly"

**NOT for:**
- Creating formal tests (use `/helpmetest-test-generator`)
- Comprehensive site testing (use `/helpmetest`)
- Debugging failing tests (use `/helpmetest-debugger`)

## Process

### Step 1: Understand What to Check

Extract from user's request:
- **URL** - Where to look (if not provided, ask)
- **Element/Feature** - What to verify ("login button", "header", "pricing table")
- **Expected state** - What should it look like? ("blue", "centered", "visible")

### Step 2: Navigate and Capture

Use `helpmetest_run_interactive_command` with navigation + screenshot:

```robot
Go To  <url>
```

**Tool returns:**
- Screenshot (automatically included)
- Page state
- Any console errors

### Step 3: Describe What You See

Based on screenshot, describe:
1. **Is the element there?** - Present or missing
2. **How does it look?** - Color, size, position, styling
3. **Matches expectation?** - Yes/No with specifics

**Example response:**
```
✓ Login button found in top-right navigation
✓ Color: Blue (#0066FF) - matches expected blue
✓ Size: Standard button size (~120px wide)
✓ Position: Aligned right, 20px from edge
```

### Step 4: Test Interactions (If Needed)

If user wants to verify behavior (hover, click, etc):

```robot
# Hover to check hover state
Hover  button:has-text("Login")

# Click to check if it works
Click  button:has-text("Login")
```

Each command returns a new screenshot showing the result.

### Step 5: Responsive Checks (If Needed)

If user mentions "mobile" or "tablet":

```robot
# Set mobile viewport
Set Viewport Size  375  667  # iPhone SE

# Capture mobile view
Go To  <url>
```

Common viewports:
- Mobile: 375x667 (iPhone SE), 390x844 (iPhone 12)
- Tablet: 768x1024 (iPad)
- Desktop: 1920x1080

## Guidelines

**Be Specific:**
- ❌ "Button looks fine"
- ✅ "Button is blue (#2563EB), 140px wide, centered in navbar"

**Compare to Expectation:**
- User said: "check if button is blue"
- You say: "Button is blue (#0066FF) ✓" or "Button is red (#DC2626) ✗ - Expected blue"

**Mention Issues:**
- Overlapping elements
- Cut-off text
- Misaligned items
- Wrong colors
- Missing elements
- Console errors

**Keep It Casual:**
- This is quick verification, not formal QA
- No need to create artifacts or tests
- Just answer: "Does it look right? Yes/No, here's why"

## Interactive Commands Available

```robot
# Navigation
Go To  <url>

# Element inspection
Get Element  <selector>  # Check if exists
Get Style  <selector>  <property>  # Get CSS value

# Viewport changes
Set Viewport Size  <width>  <height>

# Interactions (to check behavior)
Click  <selector>
Hover  <selector>
Fill Text  <selector>  <text>
Press Keys  <selector>  <key>

# Scrolling
Scroll To Element  <selector>
Scroll By  <x>  <y>

# Waiting (if page loads slowly)
Wait For Elements State  <selector>  visible  timeout=5000
```

Every command automatically returns a screenshot.

## Example Workflows

### Example 1: Quick Button Check
```
User: "Check if the Sign Up button is green"

1. Go To  https://example.com
2. Look at screenshot
3. Find "Sign Up" button in nav
4. Respond: "Sign Up button is green (#10B981) ✓"
```

### Example 2: Layout Verification
```
User: "Is the pricing table centered?"

1. Go To  https://example.com/pricing
2. Look at screenshot
3. Check table position
4. Respond: "Pricing table is centered ✓ - Equal margins on both sides (~200px)"
```

### Example 3: Responsive Check
```
User: "Does the header look good on mobile?"

1. Set Viewport Size  375  667
2. Go To  https://example.com
3. Look at screenshot
4. Respond: "Header stacks vertically ✓ - Logo on top, menu items below. Hamburger icon visible."
```

### Example 4: Hover State
```
User: "Check if the button changes color on hover"

1. Go To  https://example.com
2. Look at initial screenshot (button default state)
3. Hover  button:has-text("Submit")
4. Look at new screenshot (button hover state)
5. Respond: "Button changes from blue (#0066FF) to dark blue (#0047B3) on hover ✓"
```

### Example 5: Modal Appearance
```
User: "See if the modal shows up when clicking Contact"

1. Go To  https://example.com
2. Click  button:has-text("Contact")
3. Look at screenshot
4. Respond: "Modal appears ✓ - Dark overlay with white form centered on screen"
```

## Output Format

Always structure your response:

```
[Element/Feature Name]

Status: ✓ Matches expectation / ✗ Issue found / ⚠️ Partial match

Details:
- [Specific observation 1]
- [Specific observation 2]
- [Specific observation 3]

[If issue found:]
Issue: [What's wrong]
Expected: [What it should be]
Actual: [What it is]
```

## When to Stop

This skill is for QUICK checks. If user asks:
- "Test this thoroughly" → Use `/helpmetest`
- "Create a test for this" → Use `/helpmetest-test-generator`
- "Why is this test failing?" → Use `/helpmetest-debugger`

Keep it simple: Look, describe, confirm.
