---
name: html-accessibility
description: Web accessibility (WCAG 2.1 AA) best practices for static HTML/CSS websites
license: Apache-2.0
---

# HTML Accessibility Skill

## Purpose

Ensure websites meet WCAG 2.1 Level AA accessibility standards for inclusive user experience.

## Core Principles (POUR)

### Perceivable
- Text alternatives for images
- Captions for audio/video
- Sufficient color contrast
- Text resizable without loss

### Operable
- Keyboard accessible
- Enough time to interact
- No seizure-inducing content
- Easy navigation

### Understandable
- Readable text
- Predictable behavior
- Input assistance
- Error prevention

### Robust
- Compatible with assistive tech
- Valid HTML
- Proper ARIA usage

## Best Practices

### Semantic HTML
```html
<!-- ✅ Good: Semantic -->
<header>
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/">Home</a></li>
    </ul>
  </nav>
</header>

<!-- ❌ Bad: Non-semantic -->
<div class="header">
  <div class="nav">...</div>
</div>
```

### Alt Text
```html
<!-- ✅ Good: Descriptive alt -->
<img src="chart.png" alt="Bar chart showing 60% increase in usage">

<!-- ❌ Bad: Missing or useless alt -->
<img src="chart.png" alt="chart">
```

### Color Contrast
```css
/* ✅ Good: WCAG AA compliant */
.text {
  color: #333;  /* Contrast ratio: 12.6:1 */
  background: #fff;
}

/* ❌ Bad: Insufficient contrast */
.text {
  color: #777;  /* Contrast ratio: 4.4:1 - fails for small text */
  background: #fff;
}
```

### Keyboard Navigation
```css
/* ✅ Good: Visible focus */
a:focus, button:focus {
  outline: 2px solid #007bff;
  outline-offset: 2px;
}

/* ❌ Bad: Removed focus */
*:focus {
  outline: none;  /* NEVER DO THIS */
}
```

## Testing

- Keyboard-only navigation
- Screen reader testing
- Color contrast checking
- HTML validation
- Automated tools (axe, WAVE)

## References

- [WCAG 2.1](https://www.w3.org/WAI/WCAG21/quickref/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
