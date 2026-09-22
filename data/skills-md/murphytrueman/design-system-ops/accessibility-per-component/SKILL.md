---
name: accessibility-per-component
description: "Run an accessibility audit on a specific design system component. Trigger when someone says: accessibility check, a11y audit, WCAG compliance, is this accessible, check accessibility, does this meet WCAG, screen reader support, keyboard navigation check, or anything about auditing the accessibility of a specific component."
references:
  - ../../knowledge-notes/output-discipline.md
---

# Accessibility per component

A skill for running a structured accessibility audit on a design system component, covering five dimensions: keyboard navigation, screen reader experience, colour and contrast, focus management, and ARIA implementation. Produces a PASS/FAIL/WARN per criterion with specific remediation guidance.

## Context

Accessibility audits at the component level are more valuable than page-level or system-level assessments because they fix the problem at its source. A component with a correct accessibility implementation propagates that correctness to every product that uses it. A component with an accessibility bug propagates that bug at the same scale.

This skill audits against WCAG 2.1 AA as the baseline. Where a criterion is more stringent at AAA and the difference matters practically (particularly around colour contrast and keyboard accessibility), this is noted. The output is not a compliance report — it is a practical guide to what needs to change and why.

## Boundaries

This skill audits a single component at a time. If the request is for a page-level or full-product accessibility audit, escalate to a dedicated accessibility review process — this skill is not designed for that scope. If no specific component is identified, ask which component to audit before proceeding. If the component has no implementation yet (design only, no code), note that the audit covers design intent only and flag code-level checks as pending.

---

## Step 1: Gather component information

Ask for or confirm:
- Component name and its design system context
- Access to the component for testing: Storybook, a live implementation, or a design file
- The component's interactive states (default, hover, focus, active, disabled, error, etc.)
- Any existing accessibility documentation for the component
- Whether the component is used in any assistive technology-sensitive contexts (financial, medical, government — these warrant extra rigour)

If the component can only be assessed from a design file rather than a live implementation, note that the keyboard and screen reader dimensions are being assessed against the specification rather than the built behaviour. These findings should be verified against the implementation before being marked as passing.

## Step 2: Run the five-dimension audit

### Dimension 1: Keyboard navigation

Every interactive component must be fully operable by keyboard alone. Assess:

**Tab order**
- Does the component receive keyboard focus in a logical order relative to surrounding content?
- If the component is a composite widget (e.g. a modal, a menu, a tab panel), is the internal tab order logical?

**Activation**
- Can the component's primary action be triggered with Enter?
- If the component behaves like a button (not a link), can it also be triggered with Space?
- For components with multiple actions (e.g. a dropdown with options), are all actions keyboard accessible?

**Arrow key navigation**
- For composite widgets (menus, tab panels, radio groups, listboxes), is arrow key navigation implemented correctly per the ARIA Authoring Practices Guide (APG) pattern for this widget type?

**Escape key**
- For components that open a layer (modal, popover, tooltip, dropdown), does Escape close it and return focus correctly?

**Skip/bypass mechanisms**
- If the component contains a large block of content (e.g. a data table), is there a mechanism to skip past it?

Result per criterion: PASS / FAIL / WARN (warn = partially implemented or needs verification in a specific context)

### Dimension 2: Screen reader experience

Assess the experience for a screen reader user navigating with keyboard focus:

**Role announcement**
- Does the component announce the correct ARIA role? Is the role appropriate for how the component behaves?
- FAIL example: a custom dropdown built from a `<div>` with no role — announces as nothing
- PASS example: `role="combobox"` on an autocomplete input

**State announcement**
- Are interactive states announced correctly? Expanded/collapsed, checked/unchecked, selected, disabled, required, invalid
- FAIL example: a toggle switch with no `aria-checked` — the state is not communicated
- PASS example: `aria-checked="true"` toggling to `aria-checked="false"` with a live region or label change

**Name computation**
- Does the component have an accessible name? Is it descriptive enough to be meaningful out of context?
- For form elements: is the label correctly associated (via `for`/`id`, `aria-labelledby`, or `aria-label`)?
- For icon-only buttons: is there an accessible name via `aria-label` or visually hidden text?
- FAIL example: an icon button with no accessible name — announces only as "button"

**Group labelling**
- If the component is part of a group (radio group, checkbox group, fieldset), is the group correctly labelled?

**Live regions**
- If the component produces dynamic content changes (error messages appearing, status updates), are these communicated via `aria-live` or an appropriate role?

**Instructions and descriptions**
- If the component requires usage instructions to be usable (e.g. a date picker, a password field with requirements), are these instructions programmatically associated via `aria-describedby`?

Result per criterion: PASS / FAIL / WARN

### Dimension 3: Colour and contrast

**Text contrast**
- All text within the component must meet a minimum 4.5:1 contrast ratio against its background at WCAG AA (3:1 for large text — 18pt regular or 14pt bold).
- Check all text at all states: default, hover, disabled, error, success.
- Note: disabled state text is exempt from WCAG AA contrast requirements, but low-contrast disabled text should still be flagged as a WARN if it is likely to be read by users with low vision.

**Non-text contrast (UI components)**
- Active UI component boundaries (input borders, checkbox borders, button outlines where the shape communicates the control) must meet a 3:1 minimum contrast ratio against adjacent colours. (WCAG 1.4.11)

**Focus indicator contrast**
- The focus indicator must meet 3:1 contrast against adjacent colours. (WCAG 2.4.11 AA)

**Colour as the only means of conveying information**
- If the component uses colour to convey state or meaning (e.g. a red border for an error, a green icon for success), is colour supplemented by another indicator (icon, text label, pattern)?

Result per criterion: PASS / FAIL / WARN with specific contrast ratio figures where assessable

### Dimension 4: Focus management

Focus management is a component-level concern whenever a component opens, closes, moves, or otherwise changes the focus context.

Assess:

**Focus on open**
- When the component opens a layer (modal, dialog, drawer, dropdown), where does focus move?
- Correct: focus moves to the first focusable element within the layer, or to the layer container if it has a defined ARIA role that accepts focus
- Incorrect: focus stays on the trigger, leaving keyboard users unable to interact with the new content

**Focus trap**
- For modal dialogs: is focus trapped within the modal while it is open? Can a keyboard user accidentally tab out of the modal into the obscured page content behind it?

**Focus on close**
- When the component closes, where does focus return?
- Correct: focus returns to the trigger element that opened the layer
- Incorrect: focus moves to the top of the page, loses position, or becomes undefined

**Focus visibility**
- Is the focus indicator visible at all focusable elements within the component?
- Is the focus indicator styled in a way that clearly distinguishes it from the hover state?

Result per criterion: PASS / FAIL / WARN

## Step 2b: Screen reader testing guide

For teams new to screen reader testing, provide this practical guide alongside the audit findings. Screen reader testing is the dimension most often skipped because teams do not know how to do it.

**Quick-start screen reader testing (macOS — VoiceOver):**
1. Enable VoiceOver: Cmd + F5 (or System Settings → Accessibility → VoiceOver)
2. Navigate with Tab to move through interactive elements
3. Listen for: role announcement (button, link, checkbox), name (the accessible label), and state (expanded, checked, disabled)
4. Use VO + Right Arrow to read non-interactive content
5. Test: Can you complete the component's primary task using only keyboard + screen reader?

**Quick-start screen reader testing (Windows — NVDA):**
1. Download NVDA (free): nvaccess.org
2. Navigate with Tab for interactive elements, Arrow keys for content
3. Listen for the same: role, name, state
4. Press NVDA + T to read the window title (confirms you are in the right context)
5. Test: Can you complete the component's primary task?

**What to listen for per component type:**
- **Buttons:** Should announce "[label], button". If icon-only, should announce the action, not the icon name.
- **Form inputs:** Should announce "[label], [type] edit". Required fields should announce "required".
- **Modals/dialogs:** Should announce the dialog title on open. Tab should be trapped inside.
- **Toggles/checkboxes:** Should announce current state ("checked" / "not checked") and change on toggle.
- **Dropdowns/selects:** Should announce "[label], combo box, [current value]". Arrow keys should navigate options.

Include this guide in the audit output when Dimension 2 (Screen reader experience) has any FAIL or WARN findings, so teams can verify the fix.

### Dimension 5: ARIA implementation

Assess the correctness of ARIA usage:

**Role appropriateness**
- Are the ARIA roles used appropriate for the component's function? (Reference the APG for the correct role pattern for each widget type)
- Are any roles being used in ways that conflict with their defined semantics?

**Required ARIA attributes**
- Are all required attributes for the component's ARIA role present? (e.g. `aria-expanded` for a disclosure, `aria-selected` for a tab, `aria-controls` linking a trigger to its content)

**Prohibited ARIA patterns**
- Is ARIA being used to fix an inaccessible native implementation when a semantic HTML element would be more appropriate? (First rule of ARIA: do not use ARIA if a native HTML element provides the correct semantics)
- Are there redundant or conflicting ARIA attributes?

**Landmark regions**
- If the component occupies a significant section of a page (a navigation, a main content area, a complementary region), is it correctly wrapped in the appropriate landmark element or role?

Result per criterion: PASS / FAIL / WARN

## Step 3: Produce the audit report

---

### Accessibility audit: [component name]

Open with a headline sentence that tells the reader the overall state and where to focus.

**Audit date:** [date]
**WCAG level:** 2.1 AA
**Assessment method:** [live component / design specification / Storybook]
**Additional context:** [e.g. tested with VoiceOver/macOS, NVDA/Windows — if applicable]

---

#### Overall status

✅ PASS / ⚠️ WARN / ❌ FAIL

---

#### Results by dimension

| Dimension | Criterion | Result | Finding | Remediation |
|---|---|---|---|---|
| Keyboard | Tab order | ✅ PASS / ⚠️ WARN / ❌ FAIL | [specific finding] | [specific fix] |
| ... | | | | |

**Status key:** ✅ PASS / ⚠️ WARN / ❌ FAIL

---

#### Critical findings

Pull out any FAIL results that create significant barriers — particularly any that prevent a user from completing a task using only a keyboard or screen reader. These need to be fixed before the component ships or remains in the system.

---

#### WCAG criterion references

For each FAIL or WARN finding, include the relevant WCAG criterion (e.g. 1.4.3 Contrast Minimum, 2.1.1 Keyboard). This makes it easier to prioritise against compliance requirements and to communicate findings to stakeholders.

---

## Step 3b: Remediation code examples

For every FAIL or WARN finding, include a concrete code example showing the fix. Remediation guidance without code is advice; remediation guidance with code is a pull request waiting to happen.

**Format for each code example:**

```
Finding: [finding ID and short description]
Before (violation):
  [The exact code pattern that causes the failure]

After (fixed):
  [The corrected code with the specific change highlighted]

Why this fixes it:
  [One sentence explaining what changed and which WCAG criterion it satisfies]
```

**Examples by dimension:**

Keyboard navigation — missing Enter/Space activation:
```
Before:
  <div className="button" onClick={handleClick}>Submit</div>

After:
  <button type="button" onClick={handleClick}>Submit</button>

Why: Native <button> provides Enter and Space activation, focus management,
and correct role announcement without additional ARIA. (WCAG 2.1.1)
```

Screen reader — missing accessible name on icon button:
```
Before:
  <button><Icon name="close" /></button>

After:
  <button aria-label="Close dialog"><Icon name="close" aria-hidden="true" /></button>

Why: aria-label provides the accessible name. aria-hidden on the icon prevents
the icon name from being announced alongside the label. (WCAG 4.1.2)
```

Focus management — focus not returned on close:
```
Before:
  const handleClose = () => {
    setIsOpen(false);
  };

After:
  const triggerRef = useRef(null);
  const handleClose = () => {
    setIsOpen(false);
    triggerRef.current?.focus();
  };
  // On the trigger: ref={triggerRef}

Why: Focus returns to the element that opened the overlay, maintaining
the user's position in the page. (WCAG 2.4.3)
```

ARIA — missing required attributes on disclosure:
```
Before:
  <button onClick={toggle}>FAQ Item</button>
  <div className={isOpen ? 'visible' : 'hidden'}>Answer text</div>

After:
  <button
    onClick={toggle}
    aria-expanded={isOpen}
    aria-controls="faq-answer-1"
  >FAQ Item</button>
  <div id="faq-answer-1" role="region" aria-labelledby="faq-trigger-1">
    Answer text
  </div>

Why: aria-expanded communicates state. aria-controls links trigger to content.
role="region" with aria-labelledby makes the content a labelled landmark. (WCAG 4.1.2)
```

Colour contrast — insufficient text contrast:
```
Before:
  .label { color: #999999; background: #FFFFFF; }
  /* Contrast ratio: 2.85:1 — fails WCAG AA (4.5:1 required) */

After:
  .label { color: #595959; background: #FFFFFF; }
  /* Contrast ratio: 7.0:1 — passes WCAG AA and AAA */

Why: Darkening the text colour from #999 to #595959 exceeds the 4.5:1 minimum. (WCAG 1.4.3)
```

Include the appropriate code example pattern for every FAIL finding. For WARN findings, include the example if the fix is clear; omit it if the finding requires contextual judgment that code alone cannot resolve.

---

## Step 3c: Complex component deep-dive protocol

Simple components (buttons, badges, basic inputs) tend to pass most checks. The real value of this skill is exposed on complex, high-CR components where accessibility failures are subtle and compound. When the target component is one of the following types, apply the extended protocol:

### Combobox / Autocomplete
Additional checks beyond the standard five dimensions:
- Does the listbox open on focus, on typing, or on a specific trigger? Is this consistent with the APG combobox pattern?
- Are results announced to screen readers as they filter? (aria-live region or aria-activedescendant)
- Can the user select with Enter without the form submitting prematurely?
- What happens when no results match? Is this announced?
- Is the selected value persistent after closing and reopening?
- Can the user clear the selection with keyboard alone?

### DatePicker / Calendar
Additional checks:
- Is the calendar grid navigable with arrow keys (day-by-day horizontally, week-by-week vertically)?
- Does the month/year navigation wrap correctly at boundaries?
- Are disabled dates announced as disabled, not just visually greyed?
- Can the user type a date directly into the input field as an alternative to the calendar?
- Does the date format match the aria-label pattern (e.g., "March 9, 2026" not "03/09/2026")?
- Is the calendar grid marked with `role="grid"` with correct row/cell roles?

### Data table
Additional checks:
- Are column headers marked with `scope="col"` or equivalent ARIA?
- Is sort state announced (aria-sort)?
- Can the user navigate cell-by-cell with arrow keys?
- Are action buttons within cells reachable without tabbing through every cell?
- Does pagination announce the new page content?
- Are row selection checkboxes grouped correctly?

### Modal / Dialog
Additional checks:
- Is `aria-modal="true"` set on the dialog element?
- Is the inert attribute or aria-hidden applied to background content?
- Can the user reach the close button without tabbing through all dialog content?
- Does the dialog have a visible, announced title?
- Are nested modals (dialog within dialog) handled correctly?

### Tabs
Additional checks:
- Does the implementation use `role="tablist"`, `role="tab"`, `role="tabpanel"` correctly?
- Are tabs navigable with arrow keys (not Tab)?
- Does activating a tab move focus to the panel or keep it on the tab?
- Is the `aria-selected` state correctly toggled between tabs?
- Are disabled tabs announced as disabled but still focusable?

For any component matching these types, run both the standard five-dimension audit AND the extended protocol. The extended protocol findings should be interleaved into the main report by dimension, not presented as a separate section.

---

## Quality checks

- All five dimensions are covered, not just contrast and keyboard navigation
- Focus management is assessed for every interactive state, not just the default state
- ARIA findings reference the APG pattern for the component type where relevant
- Contrast findings include actual contrast ratio figures, not just pass/fail
- Every FAIL finding has a specific, actionable remediation with a code example
- The distinction between specification-level and implementation-level findings is clear
- Complex components (Combobox, DatePicker, DataTable, Modal, Tabs) receive the extended protocol in addition to the standard audit
- Code examples show both before (violation) and after (fix) with the specific WCAG criterion referenced
