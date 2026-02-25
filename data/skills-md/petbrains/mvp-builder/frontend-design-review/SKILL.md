---
name: frontend-design-review
description: Design principles and review methodology for UI/UX work. Use when building new interfaces, reviewing visual changes, or validating design quality. Contains best practices for visual polish, accessibility (WCAG 2.1 AA), responsive design, component standards, and interaction patterns. Works both as a development guide and a review checklist. Produces structured reports with prioritized findings.
---

# Design Review

Design principles and quality standards for building and reviewing user interfaces.

## When to Use

**During Development:**
- Building new UI components or pages
- Implementing design system elements
- Adding interactive features
- Working on responsive layouts

**During Review:**
- Evaluating PRs with visual changes
- Validating accessibility compliance
- Checking design system consistency
- Final QA before release

## Core Principles

### Users First
Every design decision should serve user needs. Prioritize clarity over cleverness, and optimize for the most common workflows. When in doubt, choose the option that reduces user effort.

### Meticulous Craft
Small details compound into overall quality. Consistent spacing, aligned elements, and polished interactions signal care and build trust. Sweat the details that users feel but may not consciously notice.

### Simplicity & Clarity
Remove everything that doesn't serve a purpose. Each element should earn its place on screen. Labels and instructions should be unambiguous — if users need to think about what something means, simplify it.

### Speed & Performance
Perceived performance is part of design. Optimize for fast initial load, instant feedback on interactions, and smooth animations. Slow UI feels broken regardless of visual quality.

### Consistency
Maintain uniform patterns across the entire product. Same actions should look and behave the same way everywhere. Consistency reduces cognitive load and makes interfaces predictable.

### Accessibility
Design for the full spectrum of users. This includes sufficient color contrast, keyboard navigation, screen reader support, and respecting motion preferences. Accessibility is not optional polish — it's core quality.

## Design Foundations

### Color
Build a systematic palette rather than picking colors ad-hoc. Include a neutral scale for text and backgrounds, a primary brand color used strategically, and semantic colors for feedback states (success, error, warning, info). Every color combination should meet WCAG AA contrast requirements. Plan for dark mode from the start.

### Typography
Choose a clean, legible typeface and establish a clear hierarchy. Define distinct sizes for headings, body text, and captions using a consistent scale. Limit font weights to maintain visual coherence. Generous line height improves readability, especially for body text.

### Spacing
Use a consistent spacing scale based on a base unit. Apply the same spacing values throughout the interface for padding, margins, and gaps. Consistent spacing creates rhythm and makes layouts feel intentional rather than arbitrary.

### Shape
Define a small set of border radius values and apply them consistently. Sharper corners typically feel more professional; rounder corners feel friendlier. Match the radius to the element's size and purpose.

## Component Standards

### Interactive States
Every interactive element needs clear visual states: default, hover, active, focus, and disabled. Focus states are critical for keyboard users — they must be clearly visible. Disabled states should look inactive but remain readable.

### Buttons
Establish a clear hierarchy: primary for main actions, secondary for alternatives, tertiary/ghost for less prominent options. Destructive actions deserve distinct styling. Include consistent icon placement and sizing. Button text should describe the action ("Save Changes" not "Submit").

### Form Elements
Labels should be visible and associated with inputs — don't rely on placeholders alone. Provide helper text for complex fields and clear error messages that explain how to fix problems. Group related fields logically and indicate required vs optional clearly.

### Cards & Containers
Use cards to group related content and create visual separation. Maintain consistent internal padding and spacing. Cards can have subtle shadows or borders to establish hierarchy, but avoid over-decorating.

### Data Display
Tables need clear headers, consistent alignment (left for text, right for numbers), and adequate row spacing. Consider how tables will handle empty states, loading, and many rows. Provide sorting and filtering for large datasets.

### Feedback & Status
Use badges, tags, and indicators consistently. Color-code status information (but don't rely on color alone). Loading states should appear quickly — use skeleton screens for page loads and spinners for discrete actions. Success and error feedback should be immediate and clear.

## Layout & Hierarchy

### Visual Hierarchy
Guide attention through size, weight, color, and position. The most important content should be immediately obvious. Use typography scale and spacing to create clear relationships between elements.

### White Space
Generous negative space improves comprehension and reduces cognitive load. Cramped interfaces feel overwhelming. White space is not wasted space — it's a tool for creating focus and breathing room.

### Grid & Alignment
Use a consistent grid system for layout structure. Align elements deliberately — misalignment is visually jarring even when subtle. Responsive grids should adapt gracefully across breakpoints.

### Responsive Behavior
Design for multiple viewport sizes. Establish breakpoints (typically mobile, tablet, desktop) and define how layouts adapt at each. Touch targets should be adequately sized on mobile. Avoid horizontal scrolling.

## Accessibility Standards

### Keyboard Navigation
All interactive elements must be reachable and operable via keyboard. Tab order should follow logical reading order. Focus must never become trapped. Provide skip links for navigation-heavy pages.

### Focus Indicators
Focus states must be clearly visible — the default browser outline is often insufficient. Design custom focus styles that are obvious against all backgrounds. Never remove focus indicators without replacement.

### Color & Contrast
Text must meet minimum contrast ratios against backgrounds (4.5:1 for normal text, 3:1 for large text). Don't convey information through color alone — pair with icons, text, or patterns. Test with color blindness simulators.

### Semantic Structure
Use proper heading hierarchy (h1 → h2 → h3). Choose semantic HTML elements over generic divs. Form inputs need associated labels. Images need meaningful alt text (or empty alt for decorative images).

### Motion
Respect `prefers-reduced-motion` for users who are sensitive to animation. Provide alternatives for motion-dependent interactions. Avoid flashing or rapidly changing content.

## Common Patterns

### Content Moderation Interfaces
When displaying items for review, make status immediately visible through consistent indicators. Group primary actions together and make them easy to reach. Support efficient workflows with bulk operations and keyboard shortcuts. For high-volume work, minimize visual noise to reduce fatigue.

### Data-Heavy Interfaces
Prioritize scannability with clear alignment, adequate spacing, and visual groupings. Provide filtering and search for large collections. Support different view modes if useful (table vs cards). Loading and empty states need thoughtful design, not just afterthought placeholders.

### Settings & Configuration
Group related options logically and label everything clearly. Progressive disclosure keeps simple cases simple while allowing access to advanced options. Provide sensible defaults. Confirm destructive changes. Give feedback when settings are saved.

## Review Process

### Live Environment First
Always assess the actual interface before reviewing code. Experience the user flow, test interactions, and feel the performance. Static code review misses issues that are obvious in use.

### Systematic Evaluation
Work through the interface methodically rather than spot-checking. Cover the primary user flow, then edge cases. Test at multiple viewport sizes. Check keyboard navigation end-to-end.

### Evidence-Based Feedback
Capture screenshots for visual issues. Be specific about what's wrong and where. Describe problems in terms of user impact, not just aesthetic preference.

## Issue Prioritization

### Blocker
Prevents core functionality or causes significant accessibility barriers. Must fix before release. Examples: broken interactions, keyboard traps, missing form labels, illegible text contrast.

### High Priority
Significant quality issues that affect user experience but don't block functionality. Should fix before merge. Examples: confusing layouts, missing loading states, inconsistent patterns, poor mobile experience.

### Medium Priority
Improvements that would enhance quality but aren't urgent. Good for follow-up. Examples: animation polish, minor spacing inconsistencies, suboptimal information hierarchy.

### Nitpick
Minor aesthetic preferences or edge cases. Optional to address. Examples: subjective color tweaks, rare edge case handling, micro-copy improvements.

## Report Structure

When documenting review findings, organize by priority:

```
## Summary
Brief overall assessment — what works well and key concerns.

## Blockers
Critical issues requiring immediate attention.

## High Priority
Significant issues to address before merge.

## Suggestions
Medium priority improvements for consideration.

## Nitpicks
Minor observations, prefix with "Nit:" to signal low priority.
```

Lead with what's working well. Frame issues as problems to solve, not mistakes made. Focus on user impact rather than prescribing specific technical solutions — the implementer often knows the codebase better.

## Integration Notes

This skill focuses on design principles and review methodology. For automated browser testing (screenshots, viewport testing, interaction verification), use the **frontend-playwright** skill which provides Playwright MCP tooling.

Adapt specific implementation details (CSS approach, component library, token values) to match the project's existing stack and conventions.
