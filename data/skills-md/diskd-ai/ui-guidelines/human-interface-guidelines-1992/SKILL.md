---
name: human-interface-guidelines-1992
description: Apply and review classic desktop UI designs against the 1992 Human Interface Guidelines. Use when designing or auditing menus, windows, dialog/alert boxes, controls, icons, color, mouse/keyboard behaviors, language/messages/help (including Balloon Help), localization/worldwide compatibility, accessibility (universal access), and collaborative-computing UX for desktop-style interfaces.
---

# Human Interface Guidelines (1992)

Use this skill to **apply** and **audit** user interfaces against the classic desktop conventions described in the 1992 guidelines.

## Workflow

### 1) Establish context (ask if missing)
- Target environment: classic desktop-style UI, color depth, screen sizes, multi-monitor expectations.
- Audience: novice vs expert mix, accessibility needs, localization targets.
- Artifacts: screenshots, mockups, flows, specs, or code; plus constraints (toolkit limits, timeline).

### 2) Classify what you’re reviewing
Identify the surface area and review by component:
- Menus and keyboard equivalents
- Windows (document vs utility), scrolling, zooming, positioning
- Dialog boxes and alerts (modeless vs movable modal vs modal)
- Controls (buttons, radio/checkbox, sliders/steppers, disclosure)
- Icons and icon families
- Color usage (black-and-white-first, selection/highlight behavior)
- Behaviors (mouse + keyboard conventions; selection/editing)
- Language (labels, messages, help systems, Balloon Help)
- Worldwide compatibility, universal access, collaborative computing UX

### 3) Evaluate with the checklist first, then go deep
- Start with `references/checklist.md` to catch the highest-impact issues quickly.
- Use `references/conspect.md` when you need rationale, design patterns, or component-specific rules.
- If needed, consult the source PDF at `Human_Interface_Guidelines_1992.pdf` (avoid long verbatim quotes; paraphrase and cite figure/section names instead).

### 4) Return findings in a review-friendly format
Provide:
1. **High-priority violations** (things that break core “look/feel”, consistency, safety, or accessibility)
2. **Recommended fixes** (what to change + why + any tradeoffs)
3. **Verification checklist** (what to re-check after changes)
4. **Open questions** (missing context that could change recommendations)

## Bundled references
- `references/conspect.md`: detailed paraphrased outline by chapter/topic.
- `references/checklist.md`: practical review checklist derived from Appendix C.
