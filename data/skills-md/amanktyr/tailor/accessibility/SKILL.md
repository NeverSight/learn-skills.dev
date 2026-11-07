---
name: accessibility
description: Enforces web accessibility (a11y), WCAG 2.1 AA guidelines, keyboard navigation, focus management, semantic HTML, and ARIA patterns.
---

# Accessibility (a11y) Skill

Activate this skill when creating or modifying user interfaces, form inputs, modal dialogs, menus, navigation bars, interactive widgets, or visual styling.

> **Accessibility Law:** *Accessible software is usable software for everyone. Use semantic HTML first and manage focus and motion rigorously.*

---

## 1. Semantic HTML First (First Line of Defense)

* Always prefer native HTML5 elements (`<button>`, `<nav>`, `<main>`, `<dialog>`, `<header>`, `<article>`, `<section>`, `<aside>`) over generic `<div>` or `<span>` elements with click handlers.
* **Do NOT add redundant ARIA attributes** when native elements already provide implicit roles (e.g. avoid `<button role="button">` or `<nav role="navigation">`).

---

## 2. Keyboard Navigation & Focus Management

* **Full Keyboard Operability:** Every interactive element must be reachable and actionable via keyboard (`Tab`, `Shift+Tab`, `Enter`, `Space`, `Escape`, and arrow keys).
* **Visible Focus Indicators:** Never remove focus outlines (`outline: none` without providing an accessible `:focus-visible` replacement).
* **Focus Trapping in Modal Dialogs:**
  - When a modal opens, trap keyboard focus within the dialog container.
  - Pressing `Escape` must close the dialog.
  - When closed, restore focus back to the triggering element.

---

## 3. Forms & Labeling

* Every form control (`<input>`, `<select>`, `<textarea>`) must have an associated `<label for="inputId">` or `aria-labelledby`.
* Provide clear, inline error messages linked to inputs via `aria-describedby="errorId"` and marked with `aria-invalid="true"`.

---

## 4. Visual Contrast & Media

* **Color Contrast (WCAG 2.1 AA):**
  - Normal text: Minimum contrast ratio of **4.5:1** against its background.
  - Large text (18pt+ or 14pt bold): Minimum contrast ratio of **3.0:1**.
  - Interactive UI components & graphical objects: Minimum **3.0:1**.
* **Informative vs Decorative Images:**
  - Informative images: Descriptive `alt="User profile photo of Jane Doe"`.
  - Purely decorative images: Explicit empty `alt=""` and `aria-hidden="true"`.

---

## 5. Dynamic Announcements (Live Regions)

* For dynamic asynchronous updates, notifications, toast messages, and shopping cart counters:
  - Use `aria-live="polite"` for non-disruptive announcements (e.g. "Item added to cart", "Save completed").
  - Use `aria-live="assertive"` or `role="alert"` strictly for critical errors requiring immediate user intervention.
  - Ensure live region containers exist in the DOM *before* dynamic content is injected into them.

---

## 6. Motion Sensitivity (Vestibular Safety)

* Respect user motion preferences by wrapping non-essential animations, transitions, and parallax scrolling with the `prefers-reduced-motion` media query:
  ```css
  @media (prefers-reduced-motion: reduce) {
    *, ::before, ::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
      scroll-behavior: auto !important;
    }
  }
  ```
