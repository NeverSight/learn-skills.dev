---
name: web-motion-auditor
description: Use when reviewing web animations, UI transitions, scroll effects, hover states, loading states, GIF/video captures, reduced-motion support, animation performance, or motion polish in HTML, React, Next.js, or Vercel apps.
---

# Web Motion Auditor

## Workflow

1. Run or open the app.
2. Inspect the animated states: load, hover, focus, click, route transition, scroll, empty/loading/success/error.
3. Check accessibility:
   - `prefers-reduced-motion`
   - focus visibility
   - no motion that blocks reading or interaction
4. Check performance on desktop and mobile widths.
5. Capture screenshots/video when possible.
6. Score with the motion quality rubric.
7. Return concrete fixes with file references.

## Common Fixes

- Shorten transitions.
- Use transforms/opacity instead of layout-heavy properties.
- Reduce stagger count.
- Add reduced-motion branch.
- Replace decorative motion with state-explaining motion.
- Move complex narrative motion to Remotion or a controlled hero scene.

