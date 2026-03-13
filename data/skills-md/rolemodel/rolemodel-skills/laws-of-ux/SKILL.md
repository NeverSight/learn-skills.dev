---
name: laws-of-ux
description: Review and guide UI implementations using the 21 Laws of UX. Identifies usability issues in HTML, CSS, and JavaScript by applying established cognitive, visual, and behavioral principles. Use when reviewing UI code, building new interfaces, or auditing user experience.
metadata:
  triggers:
    - ux review
    - ui review
    - usability
    - laws of ux
    - ux best practices
    - user experience
    - ux audit
    - ui patterns
---

## Overview

This skill guides AI in reviewing and building user interfaces using the 21 Laws of UX. It serves two purposes:

1. **Review mode**: Analyze existing UI code for violations of UX principles and suggest improvements.
2. **Guidance mode**: Apply UX laws when building new features to ensure usable, intuitive interfaces from the start.

The laws are organized into three categories based on what aspect of the user experience they address:
- **Cognitive & Decision-Making** — How users think and process information
- **Visual & Perceptual** — How users see and interpret visual layouts
- **Behavioral & Interaction** — How users act and respond to interfaces

When reviewing code, check the Review Checklist first to identify which laws are most relevant, then refer to the detailed sections for guidance and examples.

Keywords: UX review, UI review, usability, Laws of UX, UX best practices, user experience, UX audit, UI patterns

## Review Checklist

Use this table for quick scanning. Each check maps to one or more laws and tells you what to look for in code.

| Check | Law(s) | What to Look For |
|-------|--------|------------------|
| Navigation has 7 or fewer top-level items | Miller's Law | `nav`, menu, sidebar — count direct children |
| Choices are minimized per step | Hick's Law | `<select>` option counts, radio groups, button arrays |
| Click targets are at least 44x44px | Fitts's Law | Button/link `min-height`, `min-width`, `padding` |
| Important actions are large and easy to reach | Fitts's Law | CTA sizing and placement in layout |
| Loading feedback appears within 400ms | Doherty Threshold | Spinners, skeleton screens, `disabled` states |
| Forms accept flexible input formats | Postel's Law | Input validation, masking, format requirements |
| One primary CTA is visually distinct | Von Restorff Effect | Button variant classes, color emphasis |
| Related items are visually grouped | Proximity, Common Region | Spacing, borders, background grouping |
| Progress indicators on multi-step flows | Zeigarnik Effect, Goal-Gradient | Step indicators, progress bars |
| Key actions at start/end of lists | Serial Position Effect | Nav ordering, list structure |
| Interface follows platform conventions | Jakob's Law | Standard patterns vs custom widgets |
| UI is visually polished and consistent | Aesthetic-Usability Effect | Design token usage, consistent styling |
| Complexity is handled by the system, not the user | Tesler's Law | Smart defaults, auto-detection, pre-filled values |
| Most-used features are prioritized | Pareto Principle | Layout hierarchy, feature prominence |
| Forms and flows are appropriately scoped | Parkinson's Law | Step count, field count, time constraints |
| Final interactions leave a positive impression | Peak-End Rule | Success states, confirmation pages, error recovery |
| Visual hierarchy is clean and simple | Law of Prägnanz | Layout clarity, minimal visual noise |
| Consistent visual styling signals relatedness | Law of Similarity | Consistent classes for related elements |
| Connected elements share visual indicators | Uniform Connectedness | Lines, borders, shared backgrounds |
| Simplest explanation wins | Occam's Razor | UI complexity vs task requirements |
| Multi-step tasks show progress and momentum | Goal-Gradient Effect | Progress bars, step completion feedback |

---

## Cognitive & Decision-Making Laws

These laws address how users process information, make decisions, and manage mental effort.

### Miller's Law

**Definition**: The average person can hold approximately 7 (plus or minus 2) items in working memory at one time.

**Key Takeaway**: Chunk content into groups of 5-9 items. When more items are needed, use hierarchy and grouping to reduce cognitive load.

**What to look for in code:**
- Count direct children in navigation menus, tab bars, and sidebars
- Count form fields visible at one time (without scrolling)
- Count options in dropdown selects and radio button groups
- Check whether long lists are chunked into logical groups

**Examples:**

✅ GOOD
```html
<nav class="main-nav">
  <a href="/dashboard">Dashboard</a>
  <a href="/projects">Projects</a>
  <a href="/team">Team</a>
  <a href="/reports">Reports</a>
  <a href="/settings">Settings</a>
</nav>
```

🚫 BAD
```html
<nav class="main-nav">
  <a href="/dashboard">Dashboard</a>
  <a href="/projects">Projects</a>
  <a href="/team">Team</a>
  <a href="/reports">Reports</a>
  <a href="/analytics">Analytics</a>
  <a href="/settings">Settings</a>
  <a href="/billing">Billing</a>
  <a href="/integrations">Integrations</a>
  <a href="/support">Support</a>
  <a href="/docs">Documentation</a>
  <a href="/profile">Profile</a>
  <a href="/admin">Admin</a>
</nav>
```
12 flat navigation items overwhelm working memory. Group under dropdowns or consolidate.

**Review flags:**
- Flag navigation with more than 7 top-level items
- Flag forms with more than 7 fields visible simultaneously without grouping
- Flag `<select>` elements with more than 10 ungrouped options (suggest `<optgroup>`)

---

### Hick's Law

**Definition**: The time it takes to make a decision increases with the number and complexity of choices available.

**Key Takeaway**: Reduce the number of choices presented at any given time. Break complex decisions into smaller, sequential steps.

**What to look for in code:**
- Count the number of action buttons visible simultaneously
- Check if multi-step wizards are used for complex forms instead of one long page
- Look for progressive disclosure patterns (show more options only when needed)
- Check whether default/recommended options are highlighted

**Examples:**

✅ GOOD
```html
<div class="pricing-options">
  <div class="pricing-card">
    <h3>Basic</h3>
    <button class="btn btn--outline">Select</button>
  </div>
  <div class="pricing-card pricing-card--recommended">
    <span class="badge">Recommended</span>
    <h3>Pro</h3>
    <button class="btn btn--primary">Select</button>
  </div>
  <div class="pricing-card">
    <h3>Enterprise</h3>
    <button class="btn btn--outline">Contact Us</button>
  </div>
</div>
```

🚫 BAD
```html
<div class="pricing-options">
  <div class="pricing-card"><h3>Free</h3><button class="btn">Select</button></div>
  <div class="pricing-card"><h3>Starter</h3><button class="btn">Select</button></div>
  <div class="pricing-card"><h3>Basic</h3><button class="btn">Select</button></div>
  <div class="pricing-card"><h3>Pro</h3><button class="btn">Select</button></div>
  <div class="pricing-card"><h3>Business</h3><button class="btn">Select</button></div>
  <div class="pricing-card"><h3>Enterprise</h3><button class="btn">Select</button></div>
  <div class="pricing-card"><h3>Custom</h3><button class="btn">Select</button></div>
</div>
```
Seven visually identical options with no recommended choice. Reduce options and highlight the best default.

**Review flags:**
- Flag more than 4-5 equally weighted action buttons in a single view
- Flag multi-step processes that present all steps at once instead of progressively
- Flag choice sets without a highlighted default or recommended option

---

### Tesler's Law (Law of Conservation of Complexity)

**Definition**: Every application has an inherent amount of complexity that cannot be removed or hidden. It must be dealt with by either the system or the user.

**Key Takeaway**: Absorb complexity into the system so users don't have to deal with it. Use smart defaults, auto-detection, and pre-filled values.

**What to look for in code:**
- Check for smart defaults on form fields
- Look for auto-detection (e.g., timezone, locale, address auto-complete)
- Check if the system pre-fills values it already knows
- Look for conditional logic that simplifies the user's path

**Examples:**

✅ GOOD
```html
<form>
  <label for="phone">Phone Number</label>
  <input type="tel" id="phone" placeholder="(555) 123-4567"
         data-controller="phone-format"
         data-action="input->phone-format#format">
  <!-- System handles formatting — user types digits freely -->
</form>
```

🚫 BAD
```html
<form>
  <label for="phone">Phone Number (format: +1-XXX-XXX-XXXX)</label>
  <input type="text" id="phone" pattern="\+1-\d{3}-\d{3}-\d{4}">
  <span class="help-text">Must include country code and dashes</span>
</form>
```
The burden of formatting is placed on the user instead of the system.

**Review flags:**
- Flag forms that require specific formatting from users when the system could auto-format
- Flag fields that ask for information the system already has (e.g., re-entering email when logged in)
- Flag missing smart defaults where reasonable values exist

---

### Occam's Razor

**Definition**: Among competing hypotheses that explain the same observations, the one with the fewest assumptions should be selected.

**Key Takeaway**: Prefer the simplest UI that accomplishes the task. Remove unnecessary elements, steps, and visual complexity.

**What to look for in code:**
- Check for unused or redundant UI elements (decorative elements that serve no purpose)
- Look for overly complex component hierarchies when simpler structures would work
- Check if the number of distinct styles and visual treatments is justified

**Examples:**

✅ GOOD
```html
<div class="empty-state">
  <p>No projects yet.</p>
  <a href="/projects/new" class="btn btn--primary">Create your first project</a>
</div>
```

🚫 BAD
```html
<div class="empty-state">
  <img src="/images/empty-illustration.svg" alt="">
  <h2>Welcome to Your Dashboard!</h2>
  <p>It looks like you haven't created any projects yet. Projects help you organize your work and collaborate with your team members efficiently.</p>
  <p>Getting started is easy — just click the button below to create your first project and begin your journey!</p>
  <a href="/projects/new" class="btn btn--primary btn--large">Create Project</a>
  <a href="/help/getting-started" class="btn btn--outline">Learn More</a>
  <p class="text-muted">You can also import projects from other tools.</p>
</div>
```
Excessive content for a simple empty state. The user's goal is clear — help them act on it quickly.

**Review flags:**
- Flag UI with multiple competing calls-to-action where one would suffice
- Flag overly verbose copy in action-oriented contexts
- Flag deeply nested component trees that could be simplified

---

### Parkinson's Law

**Definition**: Any task will inflate until all of the available time is spent.

**Key Takeaway**: Constrain task scope by setting reasonable boundaries. Reduce form fields to only what is necessary and break large tasks into focused steps.

**What to look for in code:**
- Count form fields — are all of them truly required for the current step?
- Check for optional fields that could be deferred to a later step
- Look for multi-step flows that appropriately scope each step

**Review flags:**
- Flag forms with more than 5-7 fields when fewer would accomplish the goal
- Flag "optional" fields in critical-path forms (move them to a secondary step)
- Flag single-page forms that could benefit from a stepped approach

---

### Pareto Principle (80/20 Rule)

**Definition**: Roughly 80% of effects come from 20% of causes.

**Key Takeaway**: Identify the 20% of features and actions that users rely on most, and make those prominent and effortless to access.

**What to look for in code:**
- Check that the most common actions are immediately accessible (not buried in menus)
- Look at layout hierarchy — primary features should have visual prominence
- Check that less common actions are accessible but do not compete for attention

**Review flags:**
- Flag primary actions buried in dropdown menus or secondary navigation
- Flag dashboards where all elements have equal visual weight
- Flag settings or options that mix frequently-used controls with rarely-used ones at the same level

---

## Visual & Perceptual Laws

These laws address how users perceive and interpret visual information on screen.

### Law of Proximity

**Definition**: Objects that are near each other tend to be perceived as a group.

**Key Takeaway**: Use spacing to communicate relationships. Related items should be closer together; unrelated items should have more space between them.

**What to look for in code:**
- Check `gap`, `margin`, and `padding` values — related items should have tighter spacing than between groups
- Look for form field groupings using `<fieldset>` or wrapper divs with spacing
- Check that spacing tokens create visual hierarchy (e.g., `--op-space-small` within groups, `--op-space-large` between groups)

**Examples:**

✅ GOOD
```css
.form__group {
  display: flex;
  flex-direction: column;
  gap: var(--op-space-x-small);  /* Tight spacing within group */
}

.form__section + .form__section {
  margin-top: var(--op-space-x-large);  /* Larger spacing between sections */
}
```

🚫 BAD
```css
.form label,
.form input,
.form select,
.form textarea {
  margin-bottom: 16px;  /* Uniform spacing everywhere — no grouping */
}
```
Uniform spacing fails to communicate which fields are related.

**Review flags:**
- Flag uniform spacing between all items in a layout where logical groups exist
- Flag form fields without visual grouping (no `<fieldset>`, section dividers, or spacing variation)
- Flag hard-coded spacing values instead of design tokens (see `optics-context` skill)

---

### Law of Similarity

**Definition**: Elements that share visual characteristics (color, shape, size) are perceived as related and part of a group.

**Key Takeaway**: Apply consistent styling to elements that serve the same function. Vary styling deliberately to signal different purposes.

**What to look for in code:**
- Check that elements with the same function use the same CSS classes
- Verify that navigation items, card components, and list items are styled consistently
- Check that intentional differences in styling reflect genuine differences in function

**Examples:**

✅ GOOD
```html
<div class="action-bar">
  <button class="btn btn--primary">Save</button>
  <button class="btn btn--outline">Cancel</button>
  <button class="btn btn--danger">Delete</button>
</div>
```
Three distinct button styles signal three distinct intents.

🚫 BAD
```html
<div class="action-bar">
  <button class="btn btn--primary">Save</button>
  <button class="btn btn--primary">Cancel</button>
  <button class="btn btn--primary">Delete</button>
</div>
```
All buttons look identical despite serving very different purposes.

**Review flags:**
- Flag elements with the same function but different styling (inconsistent)
- Flag elements with different functions but identical styling (ambiguous)
- Flag custom one-off styles on elements that should match their siblings

---

### Law of Common Region

**Definition**: Elements within a shared boundary (border, background, or container) are perceived as a group.

**Key Takeaway**: Use visual containers — backgrounds, borders, cards — to group related content. This reinforces grouping beyond just proximity.

**What to look for in code:**
- Check for `<fieldset>`, cards, panels, or sections with visible boundaries
- Look for `background-color`, `border`, or `border-radius` used to create container regions
- Verify that grouped items share a common container element

**Examples:**

✅ GOOD
```html
<fieldset class="form__section">
  <legend>Shipping Address</legend>
  <input type="text" placeholder="Street">
  <input type="text" placeholder="City">
  <input type="text" placeholder="Zip">
</fieldset>

<fieldset class="form__section">
  <legend>Billing Address</legend>
  <input type="text" placeholder="Street">
  <input type="text" placeholder="City">
  <input type="text" placeholder="Zip">
</fieldset>
```

🚫 BAD
```html
<label>Shipping Street</label>
<input type="text">
<label>Shipping City</label>
<input type="text">
<label>Shipping Zip</label>
<input type="text">
<label>Billing Street</label>
<input type="text">
<label>Billing City</label>
<input type="text">
<label>Billing Zip</label>
<input type="text">
```
Flat list of fields with no grouping. Users cannot quickly identify where shipping ends and billing begins.

**Review flags:**
- Flag long flat lists of form fields with no visual grouping
- Flag distinct content sections without container boundaries
- Flag `<fieldset>` usage without `<legend>` (boundary exists but label is missing)

---

### Law of Uniform Connectedness

**Definition**: Elements that are visually connected (by lines, colors, frames, or other shapes) are perceived as more related than elements with no connection.

**Key Takeaway**: Use visual connectors — lines, shared colors, enclosures — to indicate relationships between elements.

**What to look for in code:**
- Check for visual connectors in step indicators (lines between steps)
- Look for shared background colors or borders linking related items
- Verify that timelines, breadcrumbs, or wizards use connecting visual elements

**Examples:**

✅ GOOD
```css
.stepper__step {
  display: flex;
  align-items: center;
}

.stepper__connector {
  flex: 1;
  height: 2px;
  background-color: var(--op-color-border);
}

.stepper__step--completed .stepper__connector {
  background-color: var(--op-color-primary-base);
}
```

**Review flags:**
- Flag multi-step wizards without visual connectors between steps
- Flag related elements that lack any shared visual treatment
- Flag breadcrumb or timeline components without connecting lines or arrows

---

### Law of Prägnanz (Law of Simplicity)

**Definition**: People tend to interpret ambiguous or complex images in the simplest form possible.

**Key Takeaway**: Keep layouts clean and simple. Use clear visual hierarchy, ample whitespace, and avoid unnecessary visual complexity.

**What to look for in code:**
- Check for excessive borders, shadows, and decorative elements
- Look for layouts with too many competing visual weights
- Verify whitespace is used effectively to let content breathe

**Examples:**

✅ GOOD
```css
.card {
  background: var(--op-color-surface-base);
  border-radius: var(--op-radius-medium);
  padding: var(--op-space-large);
}
```

🚫 BAD
```css
.card {
  background: linear-gradient(135deg, #f5f5f5, #e0e0e0);
  border: 2px solid #ccc;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06);
  padding: 24px;
  outline: 1px solid rgba(255, 255, 255, 0.5);
}
```
Excessive styling competes for attention and adds visual noise.

**Review flags:**
- Flag elements with more than 2 decorative treatments (shadow + border + gradient)
- Flag layouts with no whitespace between major sections
- Flag hard-coded visual values instead of design tokens (see `optics-context` skill)

---

### Von Restorff Effect (Isolation Effect)

**Definition**: When multiple similar objects are present, the one that differs most from the rest is most likely to be remembered.

**Key Takeaway**: Make the most important element visually distinct. Use a single primary CTA style to draw attention to the key action.

**What to look for in code:**
- Check that only one primary action button exists per view or section
- Look for visual emphasis on the most important element (color, size, weight)
- Verify that secondary actions use subdued styling

**Examples:**

✅ GOOD
```html
<div class="dialog__actions">
  <button class="btn btn--outline">Cancel</button>
  <button class="btn btn--primary">Confirm Purchase</button>
</div>
```

🚫 BAD
```html
<div class="dialog__actions">
  <button class="btn btn--primary">Cancel</button>
  <button class="btn btn--primary">Confirm Purchase</button>
</div>
```
Both actions have equal visual weight — the user cannot quickly identify the primary action.

**Review flags:**
- Flag views with multiple `btn--primary` (or equivalent) elements competing for attention
- Flag CTAs that blend in with surrounding elements (no visual distinction)
- Flag pages with no clear visual focal point

---

### Serial Position Effect

**Definition**: Users tend to best remember the first and last items in a series.

**Key Takeaway**: Place the most important items at the beginning and end of lists, navigation, and content sequences.

**What to look for in code:**
- Check navigation ordering — key items should be first and last
- Look at list and tab ordering for priority placement
- Check footer/bottom-of-page content for important actions

**Examples:**

✅ GOOD
```html
<nav class="main-nav">
  <a href="/dashboard">Dashboard</a>     <!-- First: most-used page -->
  <a href="/projects">Projects</a>
  <a href="/team">Team</a>
  <a href="/reports">Reports</a>
  <a href="/settings">Settings</a>       <!-- Last: memorable position -->
</nav>
```

**Review flags:**
- Flag navigation where the least important item is in the first position
- Flag long lists without any strategic ordering of key items
- Flag footers that contain only boilerplate without useful actions

---

## Behavioral & Interaction Laws

These laws address how users interact with interfaces and what drives their behavior.

### Fitts's Law

**Definition**: The time to acquire a target is a function of the distance to and size of the target.

**Key Takeaway**: Make important interactive elements large and easy to reach. Increase click/tap target sizes, especially on touch devices.

**What to look for in code:**
- Check button and link sizing — minimum 44x44px for touch targets
- Look for adequate padding on interactive elements
- Check placement of important actions — they should be near where the user's attention/cursor already is
- Verify mobile-specific sizing with media queries

**Examples:**

✅ GOOD
```css
.btn {
  min-height: 44px;
  min-width: 44px;
  padding: var(--op-space-small) var(--op-space-medium);
}

.icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  min-width: 44px;
}
```

🚫 BAD
```css
.action-link {
  font-size: 12px;
  padding: 2px 4px;
}

.icon-btn {
  width: 20px;
  height: 20px;
}
```
Tiny click targets are difficult to tap on touch devices and hard to click precisely on desktop.

**Review flags:**
- Flag interactive elements smaller than 44x44px (especially on touch interfaces)
- Flag text links with no padding (rely on text size alone for target area)
- Flag important actions positioned far from the user's likely focus area
- Flag close/dismiss buttons that are very small or in hard-to-reach corners

---

### Doherty Threshold

**Definition**: Productivity soars when a computer and its users interact at a pace (<400ms) that ensures neither has to wait on the other.

**Key Takeaway**: Provide immediate visual feedback for all user actions. Use loading states, optimistic updates, and skeleton screens to keep perceived response time under 400ms.

**What to look for in code:**
- Check for loading indicators on async actions (spinners, skeleton screens)
- Look for `disabled` states on buttons during form submission
- Check for optimistic UI patterns (updating the UI before the server responds)
- Look for Turbo Frame/Stream usage for partial page updates

**Examples:**

✅ GOOD
```html
<button type="submit" class="btn btn--primary"
        data-disable-with="Saving..."
        data-controller="submit-button">
  Save Changes
</button>
```

```html
<!-- Skeleton screen while loading -->
<div class="card card--skeleton">
  <div class="skeleton-line skeleton-line--title"></div>
  <div class="skeleton-line"></div>
  <div class="skeleton-line"></div>
</div>
```

🚫 BAD
```html
<button type="submit" class="btn btn--primary">Save Changes</button>
<!-- No loading state, no disabled state, no visual feedback -->
```

**Review flags:**
- Flag form submit buttons without `data-disable-with` or equivalent loading state
- Flag async data loading without skeleton screens or spinners
- Flag actions that navigate to a new page when a partial update (Turbo Frame) would be faster
- Flag lack of transition/animation on state changes

---

### Goal-Gradient Effect

**Definition**: The tendency to approach a goal increases with proximity to the goal.

**Key Takeaway**: Show progress in multi-step tasks. As users get closer to completion, make progress visually apparent to motivate them to finish.

**What to look for in code:**
- Check multi-step forms for progress indicators
- Look for completion percentage or step counts (e.g., "Step 3 of 5")
- Check onboarding flows for progress feedback
- Look for visual progress (progress bars, checkmarks on completed steps)

**Examples:**

✅ GOOD
```html
<div class="stepper">
  <div class="stepper__step stepper__step--completed">
    <span class="stepper__icon">&#10003;</span>
    <span>Account</span>
  </div>
  <div class="stepper__connector stepper__connector--completed"></div>
  <div class="stepper__step stepper__step--active">
    <span class="stepper__icon">2</span>
    <span>Profile</span>
  </div>
  <div class="stepper__connector"></div>
  <div class="stepper__step">
    <span class="stepper__icon">3</span>
    <span>Preferences</span>
  </div>
</div>
```

🚫 BAD
```html
<h2>Profile Information</h2>
<form>
  <!-- Multi-step form with no indication of progress or remaining steps -->
  <input type="text" placeholder="Name">
  <button type="submit">Next</button>
</form>
```

**Review flags:**
- Flag multi-step forms or wizards without a progress indicator
- Flag onboarding flows without step counts or progress bars
- Flag checkout processes without clear step visualization

---

### Jakob's Law

**Definition**: Users spend most of their time on other sites. They prefer your site to work the same way as all the other sites they already know.

**Key Takeaway**: Follow established UI conventions. Use standard patterns for navigation, forms, and common interactions. Innovate cautiously.

**What to look for in code:**
- Check that navigation follows platform conventions (top bar or sidebar, logo links to home)
- Look for standard form patterns (labels above inputs, submit at bottom-right)
- Check that links look like links and buttons look like buttons
- Verify standard keyboard interactions (Escape to close modals, Tab to navigate)

**Examples:**

✅ GOOD
```html
<header class="header">
  <a href="/" class="header__logo">
    <img src="/logo.svg" alt="AppName">
  </a>
  <nav class="header__nav"><!-- standard nav items --></nav>
  <div class="header__actions">
    <a href="/account" class="header__avatar"><!-- user menu --></a>
  </div>
</header>
```

🚫 BAD
```html
<footer>
  <a href="/">
    <img src="/logo.svg" alt="AppName">
  </a>
  <nav><!-- main navigation in the footer --></nav>
</footer>
```
Placing primary navigation in the footer breaks user expectations.

**Review flags:**
- Flag custom widgets that replicate native browser controls (custom select, custom checkbox) without keyboard accessibility
- Flag non-standard placement of navigation, search, or user account links
- Flag links styled as plain text or buttons styled as links (role confusion)
- Flag modals that cannot be closed with Escape key

---

### Aesthetic-Usability Effect

**Definition**: Users often perceive aesthetically pleasing design as design that is more usable.

**Key Takeaway**: Invest in visual polish. A well-designed interface builds user trust, increases tolerance for minor usability issues, and encourages engagement.

**What to look for in code:**
- Check for consistent use of design tokens (colors, spacing, typography)
- Look for visual alignment and consistent spacing
- Verify that the interface uses a cohesive color palette
- Check for attention to detail in micro-interactions (hover states, focus states, transitions)

**Examples:**

✅ GOOD
```css
.btn {
  background-color: var(--op-color-primary-base);
  color: var(--op-color-primary-base-on);
  border-radius: var(--op-radius-medium);
  padding: var(--op-space-small) var(--op-space-medium);
  transition: background-color 150ms ease;
}

.btn:hover {
  background-color: var(--op-color-primary-plus-one);
}

.btn:focus-visible {
  outline: 2px solid var(--op-color-primary-base);
  outline-offset: 2px;
}
```

🚫 BAD
```css
.btn {
  background: blue;
  color: white;
  padding: 8px 12px;
}
/* No hover state, no focus state, no transitions */
```
Missing interaction states and hard-coded colors feel unpolished and reduce perceived quality.

**Review flags:**
- Flag interactive elements without hover and focus states
- Flag inconsistent spacing or typography (mixing tokens with hard-coded values)
- Flag missing transitions on state changes
- Flag hard-coded colors instead of design tokens (see `optics-context` skill)

---

### Peak-End Rule

**Definition**: People judge an experience largely based on how they felt at its most intense point (peak) and at its end, rather than the sum of every moment.

**Key Takeaway**: Design positive peak moments and strong endings. Success states, confirmation messages, and completion celebrations matter disproportionately.

**What to look for in code:**
- Check success/confirmation pages for positive feedback
- Look for completion celebrations (checkmarks, success messages, animations)
- Verify that error states provide helpful recovery paths (not dead ends)
- Check that the last step of any flow feels satisfying

**Examples:**

✅ GOOD
```html
<div class="success-state">
  <div class="success-state__icon">&#10003;</div>
  <h2>Payment Successful!</h2>
  <p>Your order #1234 has been confirmed. You'll receive a confirmation email shortly.</p>
  <a href="/orders/1234" class="btn btn--primary">View Order</a>
</div>
```

🚫 BAD
```html
<div class="alert alert--success">
  <p>Done.</p>
</div>
<!-- Redirects to homepage after 3 seconds -->
```
An abrupt, minimal success message after a complex flow (like checkout) leaves a weak final impression.

**Review flags:**
- Flag completion states that are generic or dismissive ("Done", "Success")
- Flag error pages without clear next steps or recovery options
- Flag auto-redirects away from success/confirmation pages
- Flag checkout or onboarding flows that end without a positive confirmation moment

---

### Postel's Law (Robustness Principle)

**Definition**: Be liberal in what you accept, and conservative in what you send.

**Key Takeaway**: Accept a wide range of user input formats and be forgiving of minor mistakes. Auto-format, auto-correct, and provide helpful suggestions rather than strict validation errors.

**What to look for in code:**
- Check input validation — does it reject valid input due to strict formatting?
- Look for auto-formatting (phone numbers, dates, credit cards)
- Check error messages — are they helpful and specific?
- Verify that search is forgiving (handles typos, partial matches)

**Examples:**

✅ GOOD
```html
<input type="tel" placeholder="Phone number"
       data-controller="phone-input"
       data-action="input->phone-input#format">
<!-- Accepts: 5551234567, 555-123-4567, (555) 123-4567, +1 555 123 4567 -->
```

🚫 BAD
```html
<input type="text" placeholder="XXX-XXX-XXXX" pattern="\d{3}-\d{3}-\d{4}">
<span class="error">Phone number must be in format XXX-XXX-XXXX</span>
```
Rejecting valid phone numbers because of formatting differences.

**Review flags:**
- Flag strict input patterns that reject common alternative formats
- Flag validation messages that don't explain what's expected
- Flag search inputs without fuzzy matching or autocomplete
- Flag date inputs that require a specific format instead of using a date picker

---

### Zeigarnik Effect

**Definition**: People remember uncompleted or interrupted tasks better than completed tasks.

**Key Takeaway**: Use visual indicators for incomplete tasks to motivate completion. Show what's started but not finished — profile completion bars, incomplete form drafts, saved progress.

**What to look for in code:**
- Check for profile or setup completion indicators
- Look for "draft" or "in progress" states in list views
- Verify that partially completed forms save progress
- Check for "resume where you left off" patterns

**Examples:**

✅ GOOD
```html
<div class="profile-completion">
  <div class="progress-bar">
    <div class="progress-bar__fill" style="width: 60%"></div>
  </div>
  <p>Your profile is 60% complete. <a href="/profile/edit">Complete your profile</a></p>
</div>
```

🚫 BAD
```html
<!-- No indication that the user's profile is incomplete -->
<div class="profile-header">
  <h2>Welcome, Alex</h2>
</div>
```
Missing the opportunity to motivate profile completion.

**Review flags:**
- Flag multi-step flows that don't save partial progress
- Flag onboarding flows without completion indicators
- Flag forms that lose data on navigation away (no auto-save or draft state)
- Flag missing "incomplete" or "draft" badges on list items that need attention

---

## Cross-Cutting Concerns

Several laws reinforce each other. When reviewing code, group related findings rather than flagging the same issue under multiple law names.

### Grouping Laws: Proximity + Common Region + Similarity + Uniform Connectedness
These four laws all relate to how users perceive which elements belong together. When reviewing layouts:
- Check for spatial grouping (Proximity)
- Check for visual containers (Common Region)
- Check for consistent styling of related elements (Similarity)
- Check for visual connectors (Uniform Connectedness)

If a layout violates all four, report it as a single grouping issue and reference the most relevant law for the fix.

### Complexity Laws: Miller's + Hick's + Tesler's + Occam's Razor + Parkinson's
These laws all address how to manage complexity in the interface:
- Too many items → Miller's Law
- Too many choices → Hick's Law
- Complexity pushed to user → Tesler's Law
- Unnecessary complexity → Occam's Razor
- Scope creep in forms → Parkinson's Law

When a form has too many fields with too many options per field, cite the most impactful law for each specific issue.

### Feedback Laws: Doherty Threshold + Peak-End Rule + Goal-Gradient + Zeigarnik
These laws all relate to feedback and perceived progress:
- Immediate response to actions → Doherty Threshold
- Quality of key moments → Peak-End Rule
- Progress visualization → Goal-Gradient Effect
- Incomplete task awareness → Zeigarnik Effect

In multi-step flows, check all four, but report findings grouped by the specific interaction point rather than by law name.

### Companion Skills
- **`bem-structure`**: Use for CSS class naming conventions when creating components that implement these UX laws.
- **`optics-context`**: Use for design token usage (colors, spacing, typography) when implementing visual aspects of these laws.
