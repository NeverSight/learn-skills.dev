---
name: ux-designer
description: 'Designs user experiences and interfaces grounded in research. Use when creating user journeys, wireframes, prototypes, or improving usability. Use for information architecture, interaction design, accessibility audits, design system creation, and developer handoff.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
---

# UX Designer

## Overview

Designs intuitive, accessible user experiences grounded in research rather than personal preference. Covers a 5-phase design process from information architecture through developer handoff, including user flows, wireframing, prototyping, usability testing, and accessibility compliance.

**When to use:** Creating user journeys and flows, designing wireframes and prototypes, improving usability, building design systems, conducting accessibility audits, preparing developer handoff documentation.

**When NOT to use:** Backend architecture without UI, database schema design, DevOps configuration.

## Quick Reference

| Phase                    | Goal                                   | Key Deliverables                                    |
| ------------------------ | -------------------------------------- | --------------------------------------------------- |
| Information Architecture | Organize content and functionality     | Site map, navigation design, labeling taxonomy      |
| User Flows               | Map paths users take to complete tasks | Flow diagrams, happy path, error states, edge cases |
| Wireframing              | Create low-fidelity layouts            | Lo-fi/mid-fi/hi-fi wireframes, layout patterns      |
| Prototyping and Testing  | Create interactive prototypes and test | Clickable prototype, usability test results         |
| UI Design and Handoff    | Production-ready designs               | Design specs, component states, responsive layouts  |

## Key UX Principles

1. **Consistency** -- use familiar patterns; do not reinvent standard UI elements
2. **Feedback** -- confirm user actions with success messages and loading states
3. **Error Prevention** -- design to prevent errors, not just handle them
4. **Recognition Over Recall** -- show options rather than requiring memory
5. **Flexibility** -- support both novice and expert users with shortcuts and defaults

## Design Patterns Summary

| Pattern        | Key Rules                                                              |
| -------------- | ---------------------------------------------------------------------- |
| Forms          | Label above field, inline validation, one column, group related fields |
| Navigation     | Current page highlighted, breadcrumbs for depth, max 7 top nav items   |
| Empty States   | Explain why empty, provide clear next action, use illustration or icon |
| Loading States | Skeleton screens over spinners, progress indicators, optimistic UI     |

## Common Mistakes

| Mistake                                                         | Correct Pattern                                                                        |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Designing based on personal preference instead of user research | Ground every design decision in user research, card sorting, or usability test data    |
| Skipping empty, loading, and error state designs                | Design all states for every screen: default, loading, empty, error, and success        |
| Using placeholder text as form labels                           | Place labels above fields; placeholders disappear on input and fail accessibility      |
| Ignoring keyboard navigation and focus states                   | Test Tab order, visible focus indicators, and ARIA labels for all interactive elements |
| Designing a single layout for all screen sizes                  | Create separate responsive layouts for mobile, tablet, and desktop breakpoints         |
| Not testing with real users before development                  | Conduct usability testing with 5+ participants on interactive prototypes               |

## Delegation

- **User research and testing**: Use `Task` agent to plan card sorting, tree testing, and usability test sessions
- **Accessibility audit**: Use `Explore` agent to verify WCAG 2.2 AA compliance across all screens using automated tools
- **Design system architecture**: Use `Plan` agent to define color scales, typography hierarchy, spacing grid, and component library structure

## References

- [Design Process](references/design-process.md) -- 5-phase UX process, information architecture, user flows, wireframing, prototyping, and handoff
- [Visual Design Fundamentals](references/visual-design.md) -- color theory, typography scales, spacing systems, visual hierarchy, dark mode, and responsive patterns
- [Accessibility Guide](references/accessibility-guide.md) -- WCAG 2.2 AA compliance, keyboard navigation, screen readers, color contrast, and audit checklists
- [Tools and Resources](references/tools-and-resources.md) -- design tools, prototyping platforms, testing services, and accessibility checkers
