---
name: accessibility-a11y
description: WCAG 2.2 compliance, ARIA patterns, keyboard navigation, screen readers, automated testing
---

# Accessibility (a11y)

## Overview

This skill covers building accessible web applications that work for everyone, including people using screen readers, keyboard-only navigation, switch devices, and other assistive technologies. It addresses WCAG 2.2 compliance at AA and AAA levels, correct ARIA usage, focus management, color contrast, reduced motion support, and automated testing integration.

Use this skill when building new UI components, reviewing existing interfaces for accessibility compliance, fixing a11y audit findings, or integrating automated accessibility testing into CI/CD pipelines.

---

## Core Principles

1. **Semantic HTML first** - Native HTML elements (`<button>`, `<nav>`, `<dialog>`) provide accessibility for free. ARIA is a repair tool for when semantics are insufficient, not a replacement for proper HTML.
2. **Keyboard is the baseline** - If it doesn't work with a keyboard alone, it doesn't work. Every interactive element must be focusable, operable, and have visible focus indicators.
3. **Test with real assistive technology** - Automated tools catch ~30% of accessibility issues. The rest require manual testing with screen readers (VoiceOver, NVDA) and keyboard-only navigation.
4. **Progressive enhancement** - Build the accessible version first, then layer on visual enhancements. Never hide content from assistive technology that sighted users can see.
5. **No information by color alone** - Color can reinforce meaning but never be the sole indicator. Use icons, text labels, and patterns alongside color.

---

## Key Patterns

### Pattern 1: Accessible Modal Dialog

**When to use:** Any overlay that requires user interaction before returning to the main content.

**Implementation:**

```tsx
import { useRef, useEffect, useCallback } from "react";

interface DialogProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export function Dialog({ isOpen, onClose, title, children }: DialogProps) {
  const dialogRef = useRef<HTMLDialogElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;

    if (isOpen) {
      // Store the element that had focus before opening
      previousFocusRef.current = document.activeElement as HTMLElement;
      dialog.showModal();
    } else {
      dialog.close();
      // Restore focus to the triggering element
      previousFocusRef.current?.focus();
    }
  }, [isOpen]);

  // Handle Escape key (native dialog handles this, but we need cleanup)
  const handleClose = useCallback(() => {
    onClose();
  }, [onClose]);

  // Handle backdrop click
  const handleBackdropClick = useCallback(
    (e: React.MouseEvent<HTMLDialogElement>) => {
      if (e.target === dialogRef.current) {
        onClose();
      }
    },
    [onClose]
  );

  if (!isOpen) return null;

  return (
    <dialog
      ref={dialogRef}
      onClose={handleClose}
      onClick={handleBackdropClick}
      aria-labelledby="dialog-title"
      aria-describedby="dialog-description"
      className="dialog"
    >
      <div className="dialog-content" role="document">
        <header className="dialog-header">
          <h2 id="dialog-title">{title}</h2>
          <button
            onClick={onClose}
            aria-label="Close dialog"
            className="dialog-close"
          >
            <span aria-hidden="true">&times;</span>
          </button>
        </header>
        <div id="dialog-description">{children}</div>
      </div>
    </dialog>
  );
}
```

```css
/* Focus trap is handled natively by <dialog> showModal() */
dialog::backdrop {
  background: rgba(0, 0, 0, 0.5);
}

dialog .dialog-close:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}
```

**Why:** The native `<dialog>` element with `showModal()` provides focus trapping, Escape key handling, and proper `role="dialog"` semantics automatically. Custom modal implementations almost always have focus trap bugs. Using the native element gives you correct behavior for free.

---

### Pattern 2: Accessible Form with Error Handling

**When to use:** Any form that collects user input and validates it.

**Implementation:**

```tsx
interface FormFieldProps {
  id: string;
  label: string;
  type?: string;
  required?: boolean;
  error?: string;
  description?: string;
  value: string;
  onChange: (value: string) => void;
}

function FormField({
  id,
  label,
  type = "text",
  required = false,
  error,
  description,
  value,
  onChange,
}: FormFieldProps) {
  const descriptionId = description ? `${id}-description` : undefined;
  const errorId = error ? `${id}-error` : undefined;

  // Build aria-describedby from available descriptions
  const describedBy = [descriptionId, errorId].filter(Boolean).join(" ") || undefined;

  return (
    <div className="form-field">
      <label htmlFor={id}>
        {label}
        {required && <span aria-hidden="true"> *</span>}
        {required && <span className="sr-only"> (required)</span>}
      </label>

      {description && (
        <p id={descriptionId} className="field-description">
          {description}
        </p>
      )}

      <input
        id={id}
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        required={required}
        aria-invalid={error ? "true" : undefined}
        aria-describedby={describedBy}
        aria-required={required}
      />

      {error && (
        <p id={errorId} className="field-error" role="alert">
          <span aria-hidden="true">!</span> {error}
        </p>
      )}
    </div>
  );
}

// Form-level error summary for screen readers
function ErrorSummary({ errors }: { errors: Record<string, string> }) {
  const errorEntries = Object.entries(errors);
  if (errorEntries.length === 0) return null;

  return (
    <div role="alert" aria-labelledby="error-summary-title" className="error-summary">
      <h3 id="error-summary-title">
        {errorEntries.length} error{errorEntries.length > 1 ? "s" : ""} found
      </h3>
      <ul>
        {errorEntries.map(([field, message]) => (
          <li key={field}>
            <a href={`#${field}`}>{message}</a>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

```css
/* Screen-reader only class */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

.field-error {
  color: var(--color-error);
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

/* Never rely on color alone for errors - include icon */
.field-error::before {
  content: "";
  /* Error icon via background-image */
}

input[aria-invalid="true"] {
  border-color: var(--color-error);
  /* Also use a thicker border or icon, not just color */
  border-width: 2px;
}
```

**Why:** Forms are the most common source of accessibility failures. This pattern ensures every field has a programmatic label, errors are announced via `role="alert"`, error messages are linked to inputs via `aria-describedby`, and the error summary lets keyboard users jump directly to problematic fields.

---

### Pattern 3: Keyboard Navigation for Custom Widgets

**When to use:** Building custom interactive components (tabs, menus, listboxes, comboboxes) that don't map to native HTML elements.

**Implementation:**

```tsx
// Accessible tabs following WAI-ARIA Authoring Practices
interface Tab {
  id: string;
  label: string;
  content: React.ReactNode;
}

function Tabs({ tabs }: { tabs: Tab[] }) {
  const [activeIndex, setActiveIndex] = useState(0);

  const handleKeyDown = (e: React.KeyboardEvent, index: number) => {
    let newIndex = index;

    switch (e.key) {
      case "ArrowRight":
        newIndex = (index + 1) % tabs.length;
        break;
      case "ArrowLeft":
        newIndex = (index - 1 + tabs.length) % tabs.length;
        break;
      case "Home":
        newIndex = 0;
        break;
      case "End":
        newIndex = tabs.length - 1;
        break;
      default:
        return; // Don't prevent default for other keys
    }

    e.preventDefault();
    setActiveIndex(newIndex);

    // Move focus to the newly active tab
    const tabElement = document.getElementById(`tab-${tabs[newIndex].id}`);
    tabElement?.focus();
  };

  return (
    <div>
      <div role="tablist" aria-label="Content sections">
        {tabs.map((tab, index) => (
          <button
            key={tab.id}
            id={`tab-${tab.id}`}
            role="tab"
            aria-selected={index === activeIndex}
            aria-controls={`panel-${tab.id}`}
            tabIndex={index === activeIndex ? 0 : -1}
            onClick={() => setActiveIndex(index)}
            onKeyDown={(e) => handleKeyDown(e, index)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {tabs.map((tab, index) => (
        <div
          key={tab.id}
          id={`panel-${tab.id}`}
          role="tabpanel"
          aria-labelledby={`tab-${tab.id}`}
          hidden={index !== activeIndex}
          tabIndex={0}
        >
          {tab.content}
        </div>
      ))}
    </div>
  );
}
```

**Why:** Custom widgets must implement the expected keyboard interaction pattern from WAI-ARIA Authoring Practices. Tabs use Arrow keys to move between tabs (not Tab key), with `tabIndex={-1}` on inactive tabs so only the active tab is in the tab order. This matches the mental model of screen reader users.

---

### Pattern 4: Live Regions for Dynamic Content

**When to use:** When content updates without a page reload and screen reader users need to be informed (notifications, search results, loading states).

**Implementation:**

```tsx
// Toast notification system with live regions
function ToastContainer({ toasts }: { toasts: Toast[] }) {
  return (
    <div
      aria-live="polite"
      aria-atomic="false"
      aria-relevant="additions"
      className="toast-container"
    >
      {toasts.map((toast) => (
        <div
          key={toast.id}
          role="status"
          className={`toast toast-${toast.type}`}
        >
          <span className="toast-icon" aria-hidden="true">
            {toast.type === "success" ? "check" : "warning"}
          </span>
          <span>{toast.message}</span>
          <button
            onClick={() => dismissToast(toast.id)}
            aria-label={`Dismiss: ${toast.message}`}
          >
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
      ))}
    </div>
  );
}

// For urgent errors, use role="alert" (assertive)
function CriticalError({ message }: { message: string }) {
  return (
    <div role="alert" className="critical-error">
      {message}
    </div>
  );
}

// Search results count announcement
function SearchResults({ query, count }: { query: string; count: number }) {
  return (
    <>
      <div aria-live="polite" className="sr-only">
        {count} results found for "{query}"
      </div>
      {/* Visual results list */}
    </>
  );
}
```

**Why:** Screen readers don't monitor the DOM for visual changes. Live regions explicitly tell assistive technology to announce new content. Use `aria-live="polite"` for non-urgent updates (search results, toasts) and `role="alert"` for urgent messages (errors, session expiry).

---

### Pattern 5: Automated Accessibility Testing

**When to use:** Every project, integrated into CI/CD and development workflow.

**Implementation:**

```typescript
// Jest + axe-core for component testing
import { render } from "@testing-library/react";
import { axe, toHaveNoViolations } from "jest-axe";

expect.extend(toHaveNoViolations);

describe("LoginForm", () => {
  it("should have no accessibility violations", async () => {
    const { container } = render(<LoginForm />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it("should have no violations in error state", async () => {
    const { container } = render(<LoginForm />);

    // Trigger validation errors
    fireEvent.click(screen.getByRole("button", { name: /submit/i }));

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

```typescript
// Playwright + axe for E2E accessibility testing
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test.describe("accessibility", () => {
  test("home page passes axe audit", async ({ page }) => {
    await page.goto("/");

    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag22aa"])
      .analyze();

    expect(results.violations).toEqual([]);
  });

  test("modal dialog passes axe audit when open", async ({ page }) => {
    await page.goto("/dashboard");
    await page.getByRole("button", { name: "Create project" }).click();

    const results = await new AxeBuilder({ page })
      .include(".dialog")
      .analyze();

    expect(results.violations).toEqual([]);
  });
});
```

```yaml
# GitHub Actions CI integration
name: Accessibility Audit
on: [pull_request]
jobs:
  a11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run build
      - name: Run axe accessibility tests
        run: npx playwright test --grep "accessibility"
      - name: Run pa11y on built pages
        run: |
          npx serve -s build -l 3000 &
          sleep 3
          npx pa11y-ci --config .pa11yci.json
```

**Why:** Automated testing catches structural issues (missing labels, invalid ARIA, contrast failures) consistently and early. Catching 30% of issues automatically in CI is better than catching 0% and discovering problems after launch. Combine with manual testing for full coverage.

---

## Color Contrast Quick Reference

| Text Size | WCAG AA | WCAG AAA |
|---|---|---|
| Normal text (< 18px / 14px bold) | 4.5:1 | 7:1 |
| Large text (>= 18px / 14px bold) | 3:1 | 4.5:1 |
| UI components & graphical objects | 3:1 | 3:1 |
| Decorative / disabled elements | No requirement | No requirement |

---

## ARIA Quick Reference

| Need | Use This | Not This |
|---|---|---|
| Label for input | `<label for="x">` or `aria-labelledby` | `placeholder` as only label |
| Describe input requirements | `aria-describedby` pointing to hint text | Title attribute |
| Hide decorative content | `aria-hidden="true"` | `display: none` (hides from everyone) |
| Mark required field | `aria-required="true"` + `required` | Only visual asterisk |
| Announce error | `role="alert"` or `aria-live="assertive"` | Just changing text color |
| Expandable section | `aria-expanded="true/false"` | Custom `data-open` attribute |

---

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Better Approach |
|---|---|---|
| `<div onclick>` instead of `<button>` | No keyboard access, no role, no focus | Use `<button>` for clickable elements |
| Using ARIA where native HTML works | More complex, more bugs | `<nav>` not `<div role="navigation">` |
| `tabindex="5"` (positive values) | Breaks natural tab order | Use `tabindex="0"` or `tabindex="-1"` only |
| `aria-label` that duplicates visible text | Screen reader hears it twice | Use `aria-label` only for non-visible labels |
| Hiding focus outlines (`outline: none`) | Keyboard users lose their place | Style `:focus-visible` instead of removing |
| `autofocus` on page load | Disorients screen reader users | Let users navigate naturally |
| Images of text | Cannot be resized, not translatable | Use real text with CSS styling |

---

## Checklist

- [ ] All interactive elements are keyboard accessible (Tab, Enter, Space, Escape, Arrow keys)
- [ ] Focus indicators are visible on all focusable elements (`:focus-visible`)
- [ ] All images have descriptive `alt` text (or `alt=""` for decorative)
- [ ] Form inputs have associated `<label>` elements
- [ ] Error messages are programmatically associated with inputs (`aria-describedby`)
- [ ] Color contrast meets WCAG AA (4.5:1 normal text, 3:1 large text)
- [ ] No information conveyed by color alone
- [ ] `prefers-reduced-motion` media query respected for animations
- [ ] Page has correct heading hierarchy (h1 > h2 > h3, no skips)
- [ ] Language is declared (`<html lang="en">`)
- [ ] axe-core tests passing in CI
- [ ] Manual testing done with VoiceOver (macOS) or NVDA (Windows)

---

## Related Resources

- **Skills:** `performance-engineering` (intersection of performance and a11y), `growth-engineering` (accessible onboarding)
- **Rules:** `rules/checklists/ui-visual-changes.md` (visual change accessibility checks)
- **Rules:** `rules/stacks/react-typescript.md` (React component patterns)
