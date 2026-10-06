---
name: seenry-review
description: "Review a web interface, a UI diff or a single component and return ranked, fixable findings. Use for design critique, UI audits, accessibility checks, reviewing a branch or PR for interface impact, stress-testing one component across states and sizes, or explaining how an observed interface or animation is built."
license: Apache-2.0
metadata:
  author: Seenry
  version: "0.1.0"
---

# Seenry Review

Judge what renders, not what the code intends. Every finding is visible, specific, ranked and comes with the smallest fix. Use the rules in the [Seenry system](../seenry/SKILL.md) as the standard: grid and spacing, per-component type limits, concentric radii, one accent, consistent page shell, and the [anti-slop list](../seenry/references/anti-slop.md).

If you built the surface yourself, say so and treat the verdict as self-review. A fresh agent context is better.

## Evidence, not taste

Report what you can show: a measurement, a screenshot, a failing check, a rule with a number. A density, radius or voice you would have chosen differently is not a finding when the project chose it deliberately and applies it consistently. Press hard on the triggers below; stay quiet on preference. A short review from a real inspection beats a long one padded to look thorough, and "no actionable findings" is a valid result.

**High on sight** (never averaged down because the surface is minor):
- an interactive control with no accessible name, no visible focus, or no keyboard path
- content or a control clipped, overlapped or unreachable at 320px, at 200% zoom or behind the keyboard
- text or control contrast below its required ratio on the surface it actually renders on
- state or meaning carried by color alone, or by motion alone
- motion that ignores `prefers-reduced-motion`, or animation on a 100+/day or keyboard-driven action
- a destructive action with no confirmation, undo or distinct treatment
- truncated content with no way to reach the full value; an error with no way to recover
- a semantic color used against its meaning (danger color on a safe action)
- placeholder material shipped as final (gradient standing in for an image, lorem ipsum, fake testimonials)

**Prefer the cheaper fix.** Propose the earliest that works: delete (a line space already carries, an animation that shouldn't exist), use the platform (native element, native focus ring), reuse a project token or component, correct a value, and only then add something new.

**Consolidate.** One root cause is one row with every location. Report at most 15 findings; triggers first. If the cap cuts findings, say how many.

## Choose the mode

| The user asks | Mode |
| --- | --- |
| "Review / critique / audit this page, screen or site" | **Screen review** |
| "Review this branch / PR / commit / my changes" | **Change review**: run `git diff` against the base, list changed UI surfaces, render them before and after, review only those |
| "Stress test / break this component" | **Stress test** |
| "Is this accessible / WCAG" | **Screen review**, accessibility pass only, with [the checklist](../seenry/references/accessibility.md) |
| "Review / improve the animations", "where should this animate" | **Motion review** |
| "How was this built / explain this interaction" | **Explain** |

## Screen review

1. **Render.** Open the page at 1440 and 390 (plus 320 for overflow). Screenshot each. Exercise the main action with pointer and keyboard.
   - **Review the complete flow before its motion.** State the component's purpose, how people enter, each meaningful action and its visible outcome. Check discoverability, appropriate Back/Cancel/dismissal behavior, focus return, relevant empty/error/disabled states, repeated or interrupted actions, and phone fit. Mark a state not applicable only with a reason; untested states remain unverified.
   - **Use flow-appropriate dismissal.** A confirmation dialog can use Cancel and Escape with native modal behavior; a navigation flow can use Back. Do not require an extra Close or X button on every dialog. A source-point return control is a spatial criterion for a directly expanding card or toggle flow, not a universal dialog requirement. Existing controls still need clear names, usable targets, visible focus and correct outcomes.
2. **Measure.** Run `node ../seenry/scripts/audit_page.mjs <url or file> --widths 1440,390,320 --shots <dir>` ([page audit](../seenry/scripts/audit_page.mjs)); it combines the [system audit](../seenry/scripts/system_audit.mjs) and the [optical audit](../seenry/scripts/optical_audit.mjs) and works on any project. Record totals: font sizes, weights, families, radii, shadows, off-grid values, nested radius violations, components over limit, horizontal overflow, and per component the alignment anchors, near-miss edges and optical insets ([alignment](../seenry/references/alignment.md)). Toggle the [grid overlay](../seenry/assets/layout-guides/README.md) to check shared edges.
3. **Look in this order**, because earlier failures make later ones moot:
   - **Job and hierarchy.** Within 5 seconds, is it clear what this is, for whom, and what to do next? Is the primary action the most prominent control?
   - **Material and anchors.** Real images, icons and data, or placeholders? Does every element align to an edge or center line of another, or do some float? Is there one dominant element and one detail layer? Use the studio critique in [exploration](../seenry/references/exploration.md#4-critique-like-a-studio).
   - **Layout.** Shared content edges, section rhythm, grouping (2x rule), reading order, phone reflow.
   - **Type.** Family count, sizes and weights per component and page, display weight and tracking, line length, wrapping.
   - **Color and surface.** Accent area and roles, contrast, elevation choices, radius family and concentricity.
   - **Components and states.** Hover, focus, active, disabled, loading, empty, error, overflow.
   - **Content.** Specific or generic copy, realistic data, claims with proof.
   - **Accessibility.** Keyboard path, focus visibility, names, contrast, targets, zoom, reduced motion.
4. **Compare** against a reference when useful: with Seenry MCP, pull the same page type from 2–3 strong sites (`search_references` with `page_type`, or `list_sites` + `get_design`) and name the specific relationship that differs. See [benchmarks](../seenry/references/benchmarks.md).

## Report format

One table, ranked by severity, one row per root cause, every location listed:

| Sev | Where | Now | Change to | Why |
| --- | --- | --- | --- | --- |
| High | `Hero.tsx:14` | h1 72px / 800 / 0 tracking / 1.2 | 56px / 500 / −0.03em / 1.05 | Heavy default display reads as template; see benchmarks |
| High | pricing, 390px | tiers overflow, horizontal scroll | stack tiers, CTA full-width | content hidden at supported width |
| Med | `Card.tsx:8` | radius 16 with 12 inset, image radius 16 | image radius 4 | non-concentric corners |

- **High**: blocks the task or hides content/actions at a supported size, fails contrast or keyboard, or reads immediately as generated.
- **Med**: harms hierarchy, consistency or clarity.
- **Low**: polish.

Then: system audit totals at both widths, what was verified, what was not verified (motion, screen reader, device), and a one-line verdict: **Ship**, **Fix then ship** (Med only) or **Block** (any High). Do not rewrite the page unasked; offer to apply the fixes.

## Change review

The question is "did this change make the interface worse?", not "what is wrong with this codebase?".

1. **Resolve the scope.** With a named PR, branch or commit range, use it. Otherwise: commits ahead of the merge base with the default branch plus uncommitted changes; else uncommitted changes only; else stop and ask what to review.
2. **Expand files to surfaces.** A changed token, shared component or stylesheet affects every screen that uses it; list those screens. Render the affected states at both widths before (a worktree or `git stash`) and after, and run the page audit on both.
3. **Read the removed lines.** Deleted focus styles, `aria-*` attributes, `alt` text, reduced-motion blocks, `min-width: 0`, labels and error handling are regressions even when the added code looks fine.
4. **Hold the change to its stated intent** (PR description, commit message): a half-finished rollout is a finding.
5. **Classify every finding:** **Introduced** (new problem), **Regression** (something that worked now doesn't; a regression against a high-on-sight trigger is High), **Pre-existing** (report at most three, in their own section, outside the verdict).
6. Flag hard-coded values that bypass tokens, by file and line. Leave correctness, security and performance to the regular code review.

## Motion review

Inventory every transition, animation and gesture in scope. For each: frequency tier, purpose, tool, properties, duration, easing or spring, interruption, reduced-motion and hover gating, measured against the build sequence and **Never ship** table in `seenry-motion`. Watch each at normal speed and at 10% in the DevTools Animations panel. Also list **missed opportunities** (a jarring jump that needs continuity, a press with no feedback) and **rejected candidates** (what should stay instant, and why). Report in the table format.

## Stress test

Render the component alone on a scratch page and put every realistic variant on screen at once:

- Content: empty, 1 character, typical, 2x long, 5x long, unbroken string (URL, email), emoji and CJK, RTL if supported, missing image, 0 / 1 / 99+ / 1,000,000 counts, negative numbers.
- States: default, hover, focus-visible, active, disabled, loading, error, success, selected, expanded.
- Containers: 240, 320, 390, 768, 1200 wide; 200% zoom; increased text spacing.
- Input: mouse, keyboard only, touch emulation, rapid repeated clicks, reversal mid-transition.

Screenshot the grid of variants, run the system audit and [text collisions](../seenry/scripts/text_collisions.mjs), and report failures in the table format. Delete the scratch page afterwards unless asked to keep it.

## Explain

Describe what is observed, then how it is likely built, then why it works for the task. Separate observed from inferred. For a live site, read the DOM and computed styles; for motion, record or step through frames at normal speed (a screenshot never proves timing). With Seenry MCP, `get_page_motion` and `get_design` give recordings and measured styles. End with how to adapt the mechanism to the user's product without copying brand assets.
