---
name: ui-ux-polish
description: 'Iterative UI/UX polishing workflow for web applications. Use when improving visual polish, refining desktop and mobile UX separately, running iterative enhancement cycles, applying design patterns like glassmorphism or bento grids, or auditing accessibility and WCAG compliance. Use for Stripe-level visual quality, responsive optimization, and design system alignment.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
---

# UI/UX Polish

Iterative enhancement workflow that elevates working web applications from decent to world-class. Covers desktop and mobile optimization as separate modalities, visual design patterns, and accessibility standards.

**When to use**: The app works correctly with basic styling in place and you want to elevate visual quality through iterative refinement. Also use for applying specific design patterns (glassmorphism, neumorphism, bento grids) or auditing accessibility.

**When NOT to use**: The app is broken or buggy (fix bugs first), styling is fundamentally wrong (needs complete overhaul), or no basic design system exists yet.

## Quick Reference

| Pattern               | Technique                                       | Key Point                                     |
| --------------------- | ----------------------------------------------- | --------------------------------------------- |
| Iterative polish      | Run the same polish prompt 10+ times            | Small improvements compound dramatically      |
| Desktop/mobile split  | Optimize each modality independently            | Prevents compromises that hurt both           |
| Glassmorphism         | `backdrop-blur-xl` + `bg-white/70` + border     | Functional depth with legibility              |
| Neumorphism           | Dual-direction box shadows                      | Best in light mode; use borders for a11y      |
| Bento grid            | CSS Grid with `rounded-3xl` cells               | Hero cell spans multiple columns/rows         |
| WCAG 2.2 AA           | Contrast ratios + target sizes + focus visible  | 4.5:1 text, 3:1 UI, 24x24px targets           |
| Reduced motion        | `prefers-reduced-motion: reduce`                | Disable animations for motion-sensitive users |
| Semantic HTML         | Landmarks + heading hierarchy + native elements | Use `<button>` not `<div role="button">`      |
| Inclusive design      | Multiple input methods + error forgiveness      | Support keyboard, voice, and touch equally    |
| Typography hierarchy  | Consistent scale with clear levels              | Font size, weight, and spacing rhythm         |
| Spacing rhythm        | Consistent padding and margin scale             | Use design token multiples (4px, 8px, 16px)   |
| Hover/focus states    | Visible feedback on all interactive elements    | Keyboard users need visible focus indicators  |
| Animation/transitions | `ease-out` enter, `ease-in` exit, 100-300ms     | Prefer transform/opacity for GPU compositing  |
| Micro-interactions    | Button press, toggle, focus, success/error      | Always respect `prefers-reduced-motion`       |

## Common Mistakes

| Mistake                                                 | Correct Pattern                                              |
| ------------------------------------------------------- | ------------------------------------------------------------ |
| Running polish on a broken app                          | Fix all functional bugs first, then apply iterative polish   |
| Making one large pass instead of many small ones        | Run 10+ iterations; incremental improvements compound        |
| Optimizing desktop and mobile simultaneously            | Treat each as a separate modality and optimize independently |
| Stopping after changes appear minimal                   | Keep iterating; subtle spacing and typography tweaks add up  |
| Applying glassmorphism to all elements                  | Use glass effects strategically on cards and modals only     |
| Neumorphism without accessibility borders               | Add a 1px border for low-vision users (contrast requirement) |
| Ignoring `prefers-reduced-motion`                       | Always respect system motion preferences in CSS              |
| Using `<div>` with click handlers instead of `<button>` | Use native semantic HTML elements for built-in accessibility |

## Delegation

- **Desktop and mobile polish in parallel**: Use `Task` agent to run separate polish passes for each modality
- **Visual regression verification**: Use `Explore` agent to check that polish iterations have not broken layout or accessibility
- **Design system alignment planning**: Use `Plan` agent to establish spacing, typography, and color patterns before polishing
- **Comprehensive accessibility audits**: Delegate to `accessibility` skill for in-depth WCAG compliance, ARIA patterns, focus management, and screen reader testing

## References

- [Polish Workflow](references/polish-workflow.md) -- The iterative polish prompt, why it works, iteration protocol, and multi-agent strategies
- [Design Patterns](references/design-patterns.md) -- Glassmorphism, neumorphism, bento grids with Tailwind implementations
- [Accessibility](references/accessibility.md) -- WCAG 2.2 AA standards, semantic HTML, ARIA, inclusive design, and reduced motion
- [Animation and Micro-interactions](references/animation-and-microinteractions.md) -- CSS transitions, loading states, spring animations, page transitions, and Tailwind animation utilities
