---
name: ui-ux-design-principles
description: Comprehensive UI and UX design principles for software development. This skill should be used when designing interfaces, implementing user interactions, ensuring accessibility, optimizing performance, and creating responsive layouts. Triggers on tasks involving UI components, user experience flows, accessibility requirements, responsive design, or design system implementation.
license: MIT
metadata:
  author: design-system
  version: "1.0.0"
---

# UI/UX Design Principles

Comprehensive guide for UI and UX design principles in software development, covering visual design, interaction patterns, accessibility, performance, and responsive design.

## When to Apply

Reference these guidelines when:
- Designing new UI components or interfaces
- Implementing user interactions and navigation
- Ensuring accessibility compliance (WCAG 2.1 AA)
- Creating responsive and mobile-first layouts
- Optimizing user feedback and error handling
- Building design systems and maintaining consistency
- Testing and iterating on user experience

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Visual Design | HIGH | `visual-` |
| 2 | Accessibility | CRITICAL | `accessibility-` |
| 3 | Interaction Design | HIGH | `interaction-` |
| 4 | Responsive Design | HIGH | `responsive-` |
| 5 | User Feedback | MEDIUM-HIGH | `feedback-` |
| 6 | Information Architecture | MEDIUM | `ia-` |
| 7 | Performance Optimization | MEDIUM | `performance-` |
| 8 | Consistency | MEDIUM | `consistency-` |
| 9 | Mobile-First Design | HIGH | `mobile-` |
| 10 | Testing and Iteration | MEDIUM | `testing-` |

## Quick Reference

### 1. Visual Design (HIGH)
- `visual-hierarchy` - Establish clear visual hierarchy
- `visual-color-palette` - Use cohesive color palette
- `visual-typography` - Effective typography for readability
- `visual-contrast` - Maintain WCAG 2.1 AA contrast
- `visual-style-consistency` - Consistent style across application

### 2. Accessibility (CRITICAL)
- `accessibility-wcag` - Follow WCAG guidelines
- `accessibility-semantic-html` - Use semantic HTML
- `accessibility-alt-text` - Provide alt text for images
- `accessibility-keyboard-navigation` - Ensure keyboard navigability
- `accessibility-assistive-tech` - Test with assistive technologies

### 3. Interaction Design (HIGH)
- `interaction-navigation` - Intuitive navigation patterns
- `interaction-familiar-components` - Use familiar UI components
- `interaction-cta` - Clear calls-to-action
- `interaction-animations` - Judicious use of animations
- `interaction-responsive` - Cross-device compatibility

### 4. Responsive Design (HIGH)
- `responsive-fluid-layouts` - Use relative units and flexible layouts
- `responsive-media-queries` - Breakpoints for different screen sizes
- `responsive-images` - Responsive images with srcset
- `responsive-typography` - Relative units for typography
- `responsive-content-priority` - Prioritize content for mobile

### 5. User Feedback (MEDIUM-HIGH)
- `feedback-mechanisms` - Clear feedback for user actions
- `feedback-loading` - Loading indicators for async operations
- `feedback-errors` - Clear error messages and recovery
- `feedback-analytics` - Track user behavior

### 6. Information Architecture (MEDIUM)
- `ia-organization` - Logical content organization
- `ia-labeling` - Clear labeling and categorization
- `ia-search` - Effective search functionality
- `ia-sitemap` - Visualize structure with sitemap

### 7. Performance Optimization (MEDIUM)
- `performance-images` - Optimize images and assets
- `performance-lazy-loading` - Lazy load non-critical resources
- `performance-code-splitting` - Code splitting for initial load
- `performance-core-web-vitals` - Monitor Core Web Vitals

### 8. Consistency (MEDIUM)
- `consistency-design-system` - Develop and adhere to design system
- `consistency-terminology` - Consistent terminology
- `consistency-positioning` - Consistent element positioning
- `consistency-visual` - Visual consistency across sections

### 9. Mobile-First Design (HIGH)
- `mobile-first-approach` - Design mobile first, scale up
- `mobile-touch-targets` - Touch-friendly interface elements
- `mobile-gestures` - Implement common gestures
- `mobile-thumb-zones` - Consider thumb zones

### 10. Testing and Iteration (MEDIUM)
- `testing-ab` - A/B testing for critical decisions
- `testing-heatmaps` - Use heatmaps and session recordings
- `testing-user-feedback` - Gather and incorporate feedback
- `testing-iteration` - Iterate based on data

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/visual-hierarchy.md
rules/accessibility-wcag.md
rules/responsive-fluid-layouts.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
