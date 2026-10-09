---
name: wechat-miniprogram-ui-ux
description: Use when the user wants to design, implement, refine, or review a WeChat Mini Program page, flow, or design system in WXML/WXSS/JS. Combines WeChat Mini Program design constraints with a design-system workflow, anti-pattern filtering, and delivery checklist tailored for mobile-first mini program interfaces.
---

# WeChat Mini Program UI/UX

Use this skill for WeChat Mini Program UI work. It is specific to mini program constraints, not generic web UI.

## Goals

- Keep the interface native to WeChat usage habits.
- Preserve a clear page focus and one dominant action.
- Optimize for mobile reading, tap comfort, and short task completion.
- Always handle loading, empty, error, and permission-denied states.
- Produce intentional visuals, but never fight the platform chrome or interaction model.

## Workflow

1. Identify the target:
   - Page type: list, detail, form, dashboard, feed, account, checkout, approval, settings.
   - User goal: browse, decide, submit, manage, confirm, recover.
   - State complexity: guest/logged-in, empty/contentful, success/failure, role-based actions.
2. Read the relevant references:
   - WeChat principles and mini program constraints: `references/wechat-design-principles.md`
   - Design-system workflow and anti-pattern framing: `references/design-system-pattern.md`
3. Generate a compact page design system before editing code:
   - Page focus
   - Information hierarchy
   - Key components
   - Color direction
   - Typography scale
   - Spacing rhythm
   - Motion and feedback rules
   - States to support
4. Implement in mini program primitives first:
   - Prefer WXML + WXSS + built-in components
   - Use `rpx` for layout sizing
   - Respect safe areas and fixed bottom actions
   - Keep JS logic state-driven and explicit
5. Run a pre-delivery review against the checklist in `references/wechat-design-principles.md`.

## Output Shape

When designing or implementing, structure thinking in this order:

1. Page intent
2. Primary action
3. Content hierarchy
4. State coverage
5. Visual system
6. Interaction details

Keep this short unless the user asks for a full spec.

## Platform Rules

- Design for narrow mobile viewports first.
- Avoid desktop-like dense tables, tiny controls, and hover-dependent interactions.
- Do not place critical actions where the WeChat top-right capsule area creates conflict.
- Keep navigation obvious. Users should know where they are, what they can do next, and how to go back.
- Prefer one primary CTA per screen section; secondary actions should be visually quieter.
- If a page can fail to load, never leave a blank screen. Show a visible recovery path.
- If data may be absent, design an intentional empty state with next action.
- If permissions or login are required, explain the reason before prompting.

## Visual Direction

- Favor clean, high-contrast, mobile-readable layouts over decorative complexity.
- Use bold visual direction only when it still supports fast comprehension.
- Build around 1 strong accent color plus stable neutrals.
- Use cards, spacing, and typography to create hierarchy before adding extra decoration.
- Keep imagery purposeful. Hero images must not bury the core action.
- Motion should explain state changes, not decorate idle elements.

## Common Mini Program Patterns

- Lists: sticky filters only if they materially help scanning; preserve scroll performance.
- Detail pages: title, summary, trust/context, primary CTA, then secondary content.
- Forms: short sections, explicit labels, inline validation, submit-state feedback.
- Bottom bars: reserve for the most important action only; support safe-area padding.
- Management screens: show role, status, and allowed actions clearly to reduce permission confusion.

## Anti-Patterns

- Web landing-page aesthetics copied directly into mini program task pages.
- Multiple competing CTAs in the first viewport.
- Light text on busy image backgrounds without a reliable contrast layer.
- Long ungrouped forms with placeholder-only labels.
- Blank screens on request failure.
- Destructive actions styled too similarly to primary confirm actions.
- Overuse of gradients, glass effects, or shadow stacks that hurt readability on small screens.
- Dense information blocks without section headers or spacing rhythm.

## Implementation Notes

- Prefer page-level tokens or CSS variables when establishing a new visual direction.
- Reuse existing project patterns if the codebase already has a design language.
- If the existing screen is inconsistent, align it to WeChat principles first, then improve aesthetics.
- When reviewing code, prioritize usability regressions over purely visual opinions.

## References

- `references/wechat-design-principles.md`
- `references/design-system-pattern.md`
