---
name: accessibility-expert
description: Build inclusive interfaces with WCAG compliance and best practices.
---

# Accessibility Expert

Create inclusive digital experiences that work for everyone.

## WCAG 2.1 Quick Reference

### Level A (Minimum)
- All images have alt text
- Videos have captions
- Content is keyboard accessible
- No seizure-triggering content
- Pages have titles

### Level AA (Target for most)
- 4.5:1 contrast for text
- 3:1 contrast for UI components
- Text resizable to 200%
- Focus visible on all elements
- Error suggestions provided

### Level AAA (Enhanced)
- 7:1 contrast ratio
- Sign language for video
- Extended audio descriptions
- No timing-based interactions

## Semantic HTML First

```html
<!-- Use semantic elements -->
<nav> instead of <div class="nav">
<button> instead of <div onclick>
<main> instead of <div id="main">
<article> instead of <div class="article">

<!-- Proper heading hierarchy -->
<h1>Page Title</h1>
  <h2>Section</h2>
    <h3>Subsection</h3>
```

## ARIA When Needed

```html
<!-- Only when HTML semantics aren't enough -->
<div role="tablist">
  <button role="tab" aria-selected="true">Tab 1</button>
  <button role="tab" aria-selected="false">Tab 2</button>
</div>

<!-- Live regions for dynamic content -->
<div aria-live="polite">Status: Saved</div>
<div aria-live="assertive">Error: Form invalid</div>

<!-- Descriptions and labels -->
<input aria-describedby="hint">
<span id="hint">Password must be 8 characters</span>
```

## Keyboard Navigation

### Focus Management
- Visible focus indicator on all interactive elements
- Logical tab order (follows visual order)
- Skip links for main content
- Focus trap in modals

### Key Patterns
| Key | Action |
|-----|--------|
| Tab | Move to next element |
| Shift+Tab | Move to previous |
| Enter/Space | Activate button |
| Arrow keys | Navigate within component |
| Escape | Close modal/menu |

## Screen Reader Support

### Content Structure
- Use landmarks: main, nav, aside, footer
- Descriptive link text (not "click here")
- Announce dynamic changes
- Provide text alternatives

### Testing Checklist
- [ ] Can navigate with keyboard only
- [ ] Screen reader announces all content
- [ ] Focus order makes sense
- [ ] Dynamic content is announced
- [ ] Forms have proper labels
- [ ] Errors are clearly communicated

## Color & Contrast

### Don't Rely on Color Alone
- Add icons or patterns
- Use text labels
- Provide multiple indicators

### Contrast Requirements
- Normal text: 4.5:1 minimum
- Large text (18px+): 3:1 minimum
- UI components: 3:1 minimum
- Focus indicators: 3:1 minimum

## Forms

```html
<!-- Always associate labels -->
<label for="email">Email</label>
<input id="email" type="email" required>

<!-- Group related fields -->
<fieldset>
  <legend>Shipping Address</legend>
  <!-- address fields -->
</fieldset>

<!-- Clear error messages -->
<input aria-invalid="true" aria-describedby="error">
<span id="error" role="alert">Please enter valid email</span>
```

## Testing Tools

- **axe DevTools**: Browser extension
- **WAVE**: Web accessibility evaluation
- **Lighthouse**: Built into Chrome
- **NVDA/VoiceOver**: Screen readers
- **Colour Contrast Analyser**: Check contrast
