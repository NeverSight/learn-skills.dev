---
name: ysl-design-system
description: "Brand standards: primary color #129748, CSS conventions, component structure patterns for admin and seller apps."
color: "#129748"
---

# Design System Skill

You are working on the **E-commerce Design System** — brand standards and CSS conventions shared across the admin panel (Bootstrap-Vue) and seller portal (CoreUI).

## Brand Identity

- **Primary color**: `#129748` (green)
- **Secondary**: `#9da5b1` (gray)
- **Success/Info**: `#00c0ef` (cyan)
- **Danger**: `#ff4136` (red)
- **Confirm button**: `#129748` (brand green)
- **Cancel button**: `#9da5b1` (gray)

## Font Stack

```scss
$font-family-sans-serif: "Lato", "Kantumruy Pro", sans-serif;
```

- **Lato** — Primary Latin font
- **Kantumruy Pro** — Khmer script support

## Platform-Specific UI Libraries

| Platform | UI Framework | CSS Approach |
|----------|-------------|-------------|
| Admin (Vue 2) | Bootstrap Vue 2.15 | Global CSS, scoped optional |
| Seller (Vue 3) | CoreUI Vue 4.5 / Pro 5.2 | Global SCSS, `<style lang="scss" scoped>` empty |

## References

- @references/styling.md — CSS standards, SCSS architecture, no-scoped-style rule
- @references/component-structure.md — Section separation, naming conventions
