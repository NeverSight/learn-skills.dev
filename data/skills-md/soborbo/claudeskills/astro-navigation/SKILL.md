---
name: astro-navigation
description: Navigation patterns for Astro sites. Header, footer, mobile menu, breadcrumbs, skip links. Use for all navigation implementation.
---

# Astro Navigation Skill

## Purpose

Provides navigation patterns for lead generation sites. Mobile-first, accessible, conversion-focused. Implements header, footer, mobile menu, breadcrumbs, and skip links with proper keyboard navigation and screen reader support.

## Core Rules

1. **Mobile-first** — Design for 375px, enhance for desktop
2. **Phone prominent** — Click-to-call in header on mobile
3. **CTA visible** — Primary CTA always accessible
4. **Accessible** — Keyboard navigable, screen reader friendly
5. **Fast** — No layout shift on menu toggle
6. **Sticky elements** — Header fixed top, mobile CTA bar fixed bottom
7. **Active states** — Indicate current page in navigation
8. **Skip link** — Allow keyboard users to skip to main content
9. **Escape key** — Close mobile menu with Escape
10. **Safe areas** — Account for iOS notch/safe areas

## Navigation Components

### Header
- Sticky header with logo, desktop nav, phone, and CTA
- Mobile menu button visible only on mobile
- Logo always links to homepage
- Phone number clickable with proper tel: link

### Mobile Menu
- Slide-in overlay from right
- Backdrop closes menu on click
- Escape key closes menu
- Prevents body scroll when open
- CTAs at bottom (Quote + Phone)

### Footer
- Four-column grid on desktop, stacked on mobile
- Company info, services, areas, quick links
- Bottom bar with copyright and legal links
- Extra padding on mobile to clear sticky CTA bar

### Breadcrumbs
- Schema.org structured data
- Current page indicated with aria-current
- Proper semantic markup with ol/li

### Skip Link
- Hidden by default, visible on focus
- Fixed position with high z-index
- Jumps to #main-content

### Active Link Styling
- Checks current pathname
- Applies aria-current="page"
- Visual indicator (color + font weight)

## Navigation Structure

```
Header (sticky top)
├── Logo (links to /)
├── Desktop Nav (hidden on mobile)
├── Desktop CTA (phone + button)
└── Mobile Menu Button (hidden on desktop)

Mobile Menu (overlay)
├── Close Button
├── Navigation Links
└── CTAs (Quote + Phone)

Footer (pb-24 on mobile, pb-12 on desktop)
├── Company Info
├── Services Links
├── Areas Links
├── Quick Links
└── Bottom Bar (copyright + legal)

Sticky Mobile CTA Bar (fixed bottom, mobile only)
├── Call Button
└── Quote Button
```

## References

Implementation details in references directory:

- [Header](./references/header.md) — Desktop header with nav and mobile menu button
- [Mobile Menu](./references/mobile-menu.md) — Slide-in menu with animation and script
- [Sticky CTA Bar](./references/sticky-cta-bar.md) — Fixed bottom bar for mobile
- [Footer](./references/footer.md) — Four-column footer with extra mobile padding
- [Breadcrumbs](./references/breadcrumbs.md) — Schema.org breadcrumb navigation
- [Skip Link](./references/skip-link.md) — Accessibility skip-to-content link
- [Active Link Styling](./references/active-link-styling.md) — Current page indication

## Key Patterns

**Mobile Menu Animation:**
- Hidden with `translate-x-full`, visible with `translate-x-0`
- Uses `requestAnimationFrame` for smooth transition
- 300ms duration matches CSS transition

**Sticky Elements:**
- Header: `sticky top-0 z-50`
- Mobile CTA: `fixed bottom-0 z-40`
- Footer: `pb-24` on mobile to clear CTA bar

**Accessibility:**
- `aria-expanded` on menu toggle
- `aria-current="page"` on active links
- `aria-label` on navigation landmarks
- Skip link for keyboard navigation

## Forbidden

- ❌ Hamburger menu on desktop
- ❌ Navigation without keyboard support
- ❌ Missing aria-expanded on toggles
- ❌ Logo without link to homepage
- ❌ Phone number not clickable on mobile
- ❌ Footer hidden by sticky mobile bar

## Definition of Done

- [ ] Mobile menu works (open/close/escape)
- [ ] Phone number clickable on mobile
- [ ] CTA visible on all viewports
- [ ] Skip link present
- [ ] Keyboard navigable
- [ ] Active page indicated
- [ ] Footer above mobile sticky bar
- [ ] Breadcrumbs on inner pages
