---
name: accessibility-auditor
description: Audit websites for accessibility issues and WCAG compliance. Use when checking accessibility, fixing a11y issues, or ensuring WCAG compliance.
---

# Accessibility Auditor

## Instructions

When auditing accessibility:

1. **Run automated checks** (axe, Lighthouse)
2. **Manual keyboard testing**
3. **Screen reader testing**
4. **Check WCAG criteria**
5. **Provide fixes**

## Automated Testing

```bash
# Lighthouse accessibility audit
npx lighthouse https://yoursite.com --only-categories=accessibility --view

# axe-core CLI
npx @axe-core/cli https://yoursite.com

# Pa11y
npx pa11y https://yoursite.com
```

### React Testing Library + jest-axe

```typescript
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

test('Button has no accessibility violations', async () => {
  const { container } = render(<Button>Click me</Button>);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Playwright Accessibility Testing

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('page has no accessibility violations', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});
```

## WCAG Checklist

### Level A (Minimum)

#### Perceivable
- [ ] **1.1.1** Non-text content has alt text
- [ ] **1.3.1** Info and relationships are programmatically determined
- [ ] **1.3.2** Meaningful reading sequence
- [ ] **1.4.1** Color is not the only way to convey info

#### Operable
- [ ] **2.1.1** All functionality available via keyboard
- [ ] **2.1.2** No keyboard traps
- [ ] **2.4.1** Skip navigation link provided
- [ ] **2.4.2** Pages have descriptive titles
- [ ] **2.4.3** Focus order is logical
- [ ] **2.4.4** Link purpose is clear

#### Understandable
- [ ] **3.1.1** Page language is specified
- [ ] **3.2.1** Focus doesn't cause unexpected changes
- [ ] **3.3.1** Errors are identified and described
- [ ] **3.3.2** Labels or instructions provided

#### Robust
- [ ] **4.1.1** Valid HTML (no duplicate IDs, proper nesting)
- [ ] **4.1.2** Name, role, value for all UI components

### Level AA (Standard Target)

- [ ] **1.4.3** Contrast ratio 4.5:1 for text
- [ ] **1.4.4** Text resizable to 200%
- [ ] **1.4.10** Content reflows at 320px width
- [ ] **2.4.6** Headings and labels are descriptive
- [ ] **2.4.7** Focus indicator is visible
- [ ] **3.2.3** Navigation is consistent
- [ ] **3.2.4** Components identified consistently

## Common Issues & Fixes

### 1. Missing Alt Text

```tsx
// Bad
<img src="/hero.jpg" />

// Good - Informative image
<img src="/hero.jpg" alt="Team collaborating in modern office" />

// Good - Decorative image
<img src="/decoration.jpg" alt="" role="presentation" />

// Good - Icon button
<button aria-label="Close dialog">
  <XIcon aria-hidden="true" />
</button>
```

### 2. Missing Form Labels

```tsx
// Bad
<input type="email" placeholder="Email" />

// Good - Visible label
<div>
  <label htmlFor="email">Email</label>
  <input id="email" type="email" />
</div>

// Good - Visually hidden label
<div>
  <label htmlFor="search" className="sr-only">Search</label>
  <input id="search" type="search" placeholder="Search..." />
</div>
```

### 3. Poor Color Contrast

```tsx
// Bad - 2.5:1 ratio
<p className="text-gray-400 bg-white">Low contrast text</p>

// Good - 4.5:1+ ratio
<p className="text-gray-700 bg-white">Accessible text</p>

// Check contrast: https://webaim.org/resources/contrastchecker/
```

### 4. Missing Focus Styles

```css
/* Bad - Removes focus */
*:focus { outline: none; }

/* Good - Custom focus style */
*:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* Tailwind */
.btn {
  @apply focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2;
}
```

### 5. Non-semantic HTML

```tsx
// Bad
<div onClick={handleClick}>Click me</div>

// Good
<button onClick={handleClick}>Click me</button>

// Bad
<div className="header">...</div>

// Good
<header>...</header>
```

### 6. Missing ARIA for Dynamic Content

```tsx
// Loading state
<button disabled aria-busy="true">
  <span className="sr-only">Loading</span>
  <Spinner aria-hidden="true" />
</button>

// Live region for updates
<div aria-live="polite" aria-atomic="true">
  {message && <p>{message}</p>}
</div>

// Modal
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
>
  <h2 id="modal-title">Dialog Title</h2>
</div>
```

### 7. Skip Link

```tsx
// Add as first focusable element
<a
  href="#main-content"
  className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-white"
>
  Skip to main content
</a>

<main id="main-content">
  ...
</main>
```

## Screen Reader Only Class

```css
/* Visually hidden but accessible */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Show on focus (for skip links) */
.sr-only-focusable:focus {
  position: static;
  width: auto;
  height: auto;
  padding: inherit;
  margin: inherit;
  overflow: visible;
  clip: auto;
  white-space: normal;
}
```

## Keyboard Testing Checklist

1. **Tab through page** - Logical order?
2. **Enter/Space on buttons** - Activates?
3. **Arrow keys in menus** - Navigates?
4. **Escape** - Closes modals/dropdowns?
5. **Focus visible** - Always visible?
6. **No traps** - Can tab out of all components?

## Common ARIA Patterns

```tsx
// Tabs
<div role="tablist">
  <button role="tab" aria-selected="true" aria-controls="panel-1">Tab 1</button>
  <button role="tab" aria-selected="false" aria-controls="panel-2">Tab 2</button>
</div>
<div role="tabpanel" id="panel-1">Content 1</div>
<div role="tabpanel" id="panel-2" hidden>Content 2</div>

// Accordion
<button aria-expanded="true" aria-controls="content-1">Section 1</button>
<div id="content-1">Content</div>

// Menu
<button aria-haspopup="menu" aria-expanded="false">Options</button>
<ul role="menu" hidden>
  <li role="menuitem">Option 1</li>
  <li role="menuitem">Option 2</li>
</ul>

// Alert
<div role="alert">Error: Please fix the form</div>

// Progress
<div role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100">
  50%
</div>
```

## Tools

- **axe DevTools** - Browser extension
- **WAVE** - Browser extension
- **Lighthouse** - Built into Chrome
- **NVDA** - Free Windows screen reader
- **VoiceOver** - Built into macOS (Cmd+F5)
- **Color Contrast Analyzer** - Desktop app
