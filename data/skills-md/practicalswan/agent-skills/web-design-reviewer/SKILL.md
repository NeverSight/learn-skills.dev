---
name: web-design-reviewer
description: Visual inspection of live websites to find and fix design issues. Use when reviewing UI layout/design, checking responsive design visually, detecting visual inconsistencies, or diagnosing CSS/accessibility problems at the source code level. Not for automated E2E testing.
---

# Web Design Reviewer

Use this skill for visual QA and source-level fixes after a page is already running. This is not the right skill for functional automation or regression suites.

## Activation Conditions

- Reviewing a live page for layout or spacing defects
- Checking responsive behavior at a few critical widths
- Comparing a page to a design system or visual target
- Tracing a visible issue back to CSS, Tailwind classes, or component structure

## Recommended Workflow

1. Open the page with a browser-capable MCP client such as Playwright MCP.
2. Capture the current state before editing.
3. Test desktop and mobile widths.
4. Fix the source code, then re-check the same viewports.

## Playwright MCP Mapping

These tool names are current in the Playwright MCP server used by Codex:

- `browser_navigate` to open the page
- `browser_snapshot` to inspect accessible structure
- `browser_take_screenshot` for before and after captures
- `browser_resize` for responsive review
- `browser_console_messages` and `browser_network_requests` to catch front-end breakage

## Review Checklist

- [ ] No overflow or clipped content at target widths
- [ ] Interactive controls remain visible and reachable
- [ ] Text contrast and focus states are acceptable
- [ ] Repeated components use consistent spacing, typography, and color
- [ ] Fixes were verified visually after the code change

## References & Resources

### Documentation
- [Visual Checklist](./references/visual-checklist.md) - High-signal items for layout, contrast, spacing, and responsive review
- [Framework Fixes](./references/framework-fixes.md) - Typical fix locations for CSS, Tailwind, CSS modules, and component styles

### Scripts
- [CSS Risk Audit](./scripts/css-risk-audit.py) - Scan CSS and front-end source for risky fixed widths, viewport traps, and overflow patterns

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [web-testing](../web-testing/SKILL.md) | Functional and automated browser testing after design fixes |
| [frontend-design](../frontend-design/SKILL.md) | Design principles to review against |
| [react-development](../react-development/SKILL.md) | Fix design issues in React source code |
