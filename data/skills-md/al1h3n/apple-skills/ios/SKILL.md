---
name: ios
description: >
  iOS Human Interface Guidelines (HIG) and native interface design: Dynamic Type ramp,
  iOS layout and spacing (8 pt grid, 44 pt minimum touch targets, concentric squircle
  corners, sheets, navigation stacks, inset grouped lists), Apple system colors and materials,
  dark/light mode pairs, responsive layouts across iPhone, iPad, and desktop panels,
  interactive springs and motion, accessibility compliance, and production UI checklists.
  Use for "design an iOS app / screen", "iOS Human Interface Guidelines", "HIG typography",
  "iOS touch targets / layout", "SwiftUI / UIKit layout conventions", or "review iOS UI".
  Pairs with liquid-glass for Apple Liquid Glass materials.
---

# iOS Design & Human Interface Guidelines

Apple-grade iOS interfaces come from **clarity**, **deference**, and **depth**: one clear job
per screen, content-first layout where controls recede, Dynamic Type scaling, concentric squircle
radii, and fluid spring physics.

## Pick the path

| You are doing | Read first |
|---|---|
| Deciding screen hierarchy, primary action, progressive disclosure | `references/focus-and-hierarchy.md` |
| iOS fonts, Dynamic Type ramps, SF font alternatives, weights | `references/typography.md` |
| Spacing rhythm (8 pt), touch targets (≥ 44 pt), squircle corners, sheets | `references/layout-and-spacing.md` |
| System colours, dark/light modes, accents, glass vs solid | `references/color-and-materials.md` (+ liquid-glass) |
| iOS springs (smooth / snappy / bouncy), gesture interactions | `references/motion.md` |
| Button labels, action verbs, alert microcopy, error states | `references/copywriting.md` |
| AI assistant sheets, voice interfaces, floating cards | `references/ai-assistant-ui.md` |
| Production readiness, contrast (≥ 4.5:1), HIG checklist | `references/review-checklist.md` |
| Translating designs from or to Figma | `references/figma-workflow.md` |

## Core iOS Numbers

- **Touch targets:** Minimum 44 × 44 pt for touch; 28 pt minimum for pointer devices.
- **Rhythm & Grid:** 8 pt base grid (spacing steps: 4, 8, 12, 16, 24, 32 pt).
- **Margins:** iPhone: 16–20 pt; iPad: 20–24 pt; split view & desktop panels: 24 pt.
- **Typography Ramp:** Large Title 34/41, Title 1 28/34, Title 2 22/28, Title 3 20/25, Headline 17/22 semibold, Body 17/22 regular, Callout 16/21, Subheadline 15/20, Footnote 13/18, Caption 1 12/16, Caption 2 11/13.
- **Corner Radii:** Squircles with continuous curvature (smoothing 60%). Outer radius = inner radius + padding.
- **Contrast:** ≥ 4.5:1 for standard text (< 18 pt); ≥ 3:1 for large titles and glyphs.
- **Springs:** Smooth 0.5 s / bounce 0; Snappy 0.5 s / bounce 0.15; Bouncy 0.5 s / bounce 0.3.

## The HIG Rules

1. **One job per screen:** Never overload a view; use navigation stacks or sheets for secondary flows.
2. **One primary action:** Emphasize the single next step with a tinted background; keep secondary buttons quiet.
3. **Deference:** The interface should defer to the user's content. Chrome recedes; content is the hero.
4. **Continuous squircles:** Always use Apple continuous rounded corners (`RoundedRectangle(cornerRadius: r, style: .continuous)`).
5. **Dynamic Type compliance:** Text elements must scale gracefully without truncation.
6. **Every state designed:** Provide clear rest, pressed, disabled, loading (skeleton pills), and empty states.
