---
name: navigation-patterns
description: Navigation patterns, breadcrumbs, tabs, sidebars, and user flows. Use when building navigation, menus, or site architecture.
version: 1.0.0
---

# Navigation Patterns

This skill covers navigation design — site architecture, breadcrumbs, tabs, sidebars, and user flow patterns that help users find content.

## Use-When

This skill activates when:
- Agent builds navigation components
- Agent creates page hierarchies or breadcrumbs
- Agent designs tabs or tabbed interfaces
- Agent builds sidebars or menus
- Agent structures site or app navigation

## Core Rules

- ALWAYS use semantic nav elements (nav, ul, li)
- ALWAYS indicate current page in navigation
- ALWAYS provide consistent navigation across pages
- ALWAYS include skip links for keyboard users
- PREFER breadcrumbs for deep hierarchies (3+ levels)

## Common Agent Mistakes

- Using divs instead of semantic nav elements
- Not marking active/current page
- Inconsistent navigation between pages
- Missing mobile navigation patterns
- No way to navigate back (broken back button)

## Examples

### ✅ Correct

```tsx
<nav aria-label="Main">
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/products" aria-current="page">Products</a></li>
  </ul>
</nav>

// Breadcrumbs
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li aria-current="page">Widget</li>
  </ol>
</nav>
```

### ❌ Wrong

```tsx
// Non-semantic
<div className="nav">
  <div>Home</div>
  <div>Products</div>
</div>

// No current indicator
<ul>
  <li><a href="/">Home</a></li>
  <li><a href="/products">Products</a></li>
</ul>
```

## References

- [Nielsen Norman Group - Navigation](https://www.nngroup.com/articles/usability-heuristics-applied/)
- [MDN - Navigation](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/nav)
