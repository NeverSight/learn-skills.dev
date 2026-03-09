---
name: accessibility
description: >
  Audit, implement, and fix web accessibility with a screen-reader-first lens.
  Use when building or reviewing UI components, forms, dialogs, navigation,
  dynamic content, or any interactive element. Covers WCAG 2.2 AA compliance,
  ARIA patterns, keyboard navigation, focus management, and assistive technology
  compatibility (NVDA, JAWS, VoiceOver). Trigger on: "accessible", "a11y",
  "screen reader", "WCAG", "ARIA", or when adding any interactive UI.
---

# Accessibility

Web accessibility done right means your UI is navigable, understandable, and operable by people who cannot use a mouse — primarily those using screen readers (NVDA, JAWS, VoiceOver), keyboard-only users, and those with motor, cognitive, or visual impairments. The 2024 WebAIM Million report found 95.9% of home pages failing basic accessibility checks. Most failures are preventable with the right mental model.

## The Core Mental Model

Screen readers **linearise** a 2D page into a 1D audio stream. A blind user never sees the whole page at once — they navigate sequentially by **headings**, **landmarks**, **form fields**, **links**, and **interactive controls** using keyboard shortcuts. Every decision you make should answer: *"What will a screen reader announce, and does it make sense in isolation?"*

The three rules that flow from this:

1. **Semantics over style** — use native HTML elements (`<button>`, `<nav>`, `<h2>`) before reaching for ARIA. Native elements come with free keyboard support, accessible names, and correct roles.
2. **Context must travel with the element** — a screen reader user navigating by tab or by links list sees elements stripped of their visual neighbours. Labels, descriptions, and states must be programmatically attached, not implied by proximity.
3. **Dynamic changes must be announced** — screen readers only notice changes if focus moves to new content or a live region announces it. Silent DOM mutations are invisible to AT.

---

## When Auditing Existing UI

Review in this priority order — fix critical issues before polishing low-impact ones:

| Priority | Category | WCAG Level | See |
|----------|----------|------------|-----|
| 1 | Accessible names (buttons, inputs, links) | A | references/aria-patterns.md |
| 2 | Keyboard operability (all interactive elements) | A | references/focus-management.md |
| 3 | Focus management (dialogs, SPAs, live regions) | A/AA | references/focus-management.md |
| 4 | Semantic structure (headings, landmarks, lists) | A | references/wcag-checklist.md |
| 5 | Form errors and validation | A/AA | references/common-fixes.md |
| 6 | Colour contrast and visual states | AA | references/wcag-checklist.md |
| 7 | Dynamic content announcements | AA | references/aria-patterns.md |
| 8 | Images and media | A | references/wcag-checklist.md |

Quote the exact failing snippet, name the WCAG criterion, and propose the smallest viable fix. Do not refactor unrelated code.

---

## When Building New UI

### The quick decision tree

```
Need an interactive control?
  ↓
Does a native HTML element do this?  → YES → Use it. Done.
  ↓ NO
Use the correct ARIA role + required attributes + keyboard handler.

Adding dynamic content?
  ↓
Does focus move to the new content? → YES → No live region needed.
  ↓ NO
Is it a transient status (toast, cart count, form error)?
  → Use aria-live="polite" (or role="alert" for errors)

Opening a dialog/modal?
  → Trap focus inside. Restore focus to trigger on close.
  → See references/focus-management.md
```

### Mandatory checks before shipping any interactive component

- [ ] Every input, select, textarea has an associated `<label>` (not just placeholder)
- [ ] Every button has an accessible name (text content, `aria-label`, or `aria-labelledby`)
- [ ] Every icon-only control has `aria-label`; the icon has `aria-hidden="true"`
- [ ] Focus is visible on all interactive elements (never `outline: none` without a replacement)
- [ ] Tab order is logical and matches visual order
- [ ] All pointer interactions have a keyboard equivalent
- [ ] No `tabindex` greater than 0

---

## The Five Most Common Failures (and their fixes)

### 1. Icon-only button with no accessible name
```html
<!-- ❌ Screen reader announces: "button" -->
<button><svg>...</svg></button>

<!-- ✅ Screen reader announces: "Close, button" -->
<button aria-label="Close"><svg aria-hidden="true">...</svg></button>
```

### 2. Input with no label
```html
<!-- ❌ Screen reader announces: "edit text" -->
<input type="email" placeholder="Email" />

<!-- ✅ Screen reader announces: "Email address, edit text" -->
<label for="email">Email address</label>
<input id="email" type="email" />
```

### 3. div or span used as a button
```html
<!-- ❌ Not keyboard accessible, no role announced -->
<div onclick="save()">Save</div>

<!-- ✅ Free keyboard support, correct role -->
<button onclick="save()">Save</button>
```

### 4. Form error not linked to field
```html
<!-- ❌ Error visible but not associated with the field -->
<input id="email" type="email" />
<span>Please enter a valid email</span>

<!-- ✅ Screen reader announces error when field is focused -->
<input id="email" type="email"
       aria-describedby="email-err"
       aria-invalid="true" />
<span id="email-err" role="alert">Please enter a valid email</span>
```

### 5. Dynamic content updated silently
```html
<!-- ❌ Cart count updates, screen reader users never know -->
<span id="cart-count">3</span>

<!-- ✅ Announces "4 items in cart" when count changes -->
<span id="cart-count" aria-live="polite" aria-atomic="true">4 items in cart</span>
```

---

## Screen Reader Testing

Automated tools catch ~30–40% of accessibility issues. The rest require AT testing.

**Minimum viable test matrix:**
- NVDA + Chrome or Firefox (Windows) — covers ~66% of screen reader users
- VoiceOver + Safari (macOS/iOS) — covers Apple ecosystem
- Add JAWS + Chrome for enterprise contexts

**Core navigation patterns to test manually:**
1. Tab through all interactive elements — are names and roles announced correctly?
2. Press `H` to navigate by headings — is the page structure logical?
3. Press `D` to navigate by landmarks — are regions clearly labelled?
4. Open and close any dialogs — does focus trap, then restore?
5. Submit a form with errors — are error messages announced?
6. Trigger any dynamic content update — is the change announced?

See **references/screen-readers.md** for NVDA/JAWS/VoiceOver commands, browse vs. forms mode, and testing scripts.

---

## ARIA: The Rules

**Rule 0:** Don't use ARIA if native HTML solves it. Bad ARIA is worse than no ARIA.

**Rule 1:** `aria-label` and `aria-labelledby` provide the accessible name (what the element *is*).
**Rule 2:** `aria-describedby` provides supplementary description (what it *does* or *needs*).
**Rule 3:** `aria-live="polite"` for non-urgent updates; `role="alert"` (implicit `assertive`) for errors.
**Rule 4:** Live regions must exist in the DOM on page load — inject text into them, don't inject the region itself.
**Rule 5:** `aria-hidden="true"` removes from the AT tree completely. Never apply to focusable elements.

Full ARIA pattern library → **references/aria-patterns.md**

---

## Visually Hidden Content

To show content to screen readers but hide it visually:

```css
.visually-hidden:not(:focus):not(:active) {
  clip-path: inset(50%);
  height: 1px;
  overflow: hidden;
  position: absolute;
  white-space: nowrap;
  width: 1px;
}
```

Use for: skip links, supplementary link context ("Read more <span class="visually-hidden">about caching</span>"), icon button labels when `aria-label` is impractical for translation reasons.

Do **not** use for: content that sighted users need. Hiding meaningful content from one group creates disparity, not accessibility.

---

## Colour and Contrast (WCAG AA)

| Content type | Minimum ratio |
|---|---|
| Body text (<18pt / <14pt bold) | 4.5:1 |
| Large text (≥18pt or ≥14pt bold) | 3:1 |
| UI components (borders, icons, focus rings) | 3:1 |
| Placeholder text | 4.5:1 |
| Disabled elements | Exempt |

Never convey information by colour alone — always pair with a shape, pattern, or text label.

---

## Reference Files

| File | Contents |
|------|----------|
| **references/screen-readers.md** | NVDA/JAWS/VoiceOver commands, browse vs. forms mode, testing scripts per component type |
| **references/aria-patterns.md** | ARIA roles, labelling hierarchy, live region patterns, complex widget ARIA (combobox, tabs, tree) |
| **references/focus-management.md** | Modal focus trap, SPA route change focus, skip links, focus restoration patterns |
| **references/wcag-checklist.md** | WCAG 2.2 AA criterion-by-criterion checklist with pass/fail examples |
| **references/common-fixes.md** | Code-level fix templates for the 20 most common audit findings |
