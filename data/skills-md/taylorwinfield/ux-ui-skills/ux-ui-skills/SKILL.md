---
name: ux-ui-skills
description: Use when producing, reviewing, or refactoring UI in any codebase — to avoid generic AI-slop output and to keep work grounded in the project's real design system rather than invented tokens, classes, and components.
---

# UX/UI Skills

Ten skills for AI coding agents that target the two failure modes of AI-generated UI:

- **Slop** — generic, template-default, framework-boilerplate UI that looks like every other AI-built screen.
- **Fiction** — UI ungrounded in the project's real design system: invented CSS classes, hallucinated tokens, components that don't exist.

Each skill carries the **method** for producing world-class UI (Linear / Notion / Vercel / Stripe tier) in any codebase, not the answers for any one project. The project-specific answers — your tokens, your components, your interaction vocabulary — are scaffolded by `bootstrapping-design-context` and filled in once, then cited by every other skill from that point forward.

## When to apply

Reference these skills when:

- A new screen, template, or component is being designed
- An existing UI is being audited or refactored
- A UI quality judgment needs to be defended against "looks fine to me"
- A flow doc, design brief, or interaction system is being authored
- A repo has no design-context docs yet and an agent is about to start UI work

## Skills by track

### Foundation (anti-fiction)

| Skill | Use when |
|---|---|
| [`bootstrapping-design-context`](skills/bootstrapping-design-context/SKILL.md) | The repo has no design brief, no design tokens, no interaction-system doc — and agents are about to start UI work anyway. |
| [`grounding-before-designing`](skills/grounding-before-designing/SKILL.md) | About to reference a component, design token, or data shape in a repo. Anti-fictitious core. |
| [`design-judgment-references`](skills/design-judgment-references/SKILL.md) | Making or defending a UI quality judgment that needs to be anchored to an established principle, not personal taste. |

### Feature design (create)

| Skill | Use when |
|---|---|
| [`flow-doc-first`](skills/flow-doc-first/SKILL.md) | Any user-facing UI is requested — a new screen, template, component, or non-trivial restyle. Process spine: artifact before production UI. |
| [`designing-states-not-screens`](skills/designing-states-not-screens/SKILL.md) | Designing any view, list, form, or data surface that can be empty, loading, partial, erroring, first-run, or offline. The #1 slop→craft differentiator. |
| [`visual-hierarchy-and-type`](skills/visual-hierarchy-and-type/SKILL.md) | Laying out a screen or composing typography and spacing, or when a screen reads flat with no clear focal order. |
| [`interaction-craft`](skills/interaction-craft/SKILL.md) | A UI has motion, transitions, async feedback, focus changes, or a perceived-latency surface. |
| [`precision-copy-and-formatting`](skills/precision-copy-and-formatting/SKILL.md) | A UI contains text, numbers, money, dates, quantities, or a destructive action. |

### Audit & refactor (grill)

| Skill | Use when |
|---|---|
| [`grilling-ui`](skills/grilling-ui/SKILL.md) | Auditing or reviewing existing UI, a flow doc, or templates for quality problems. |
| [`anti-slop-audit`](skills/anti-slop-audit/SKILL.md) | Checking UI for generic, templated, or AI-slop tells — as a fast pre-PR check or within a deeper audit. |

## Authoring conventions

Each skill follows a fixed structure enforced by the linter at `bin/lint_skills.py`:

- YAML frontmatter (`name`, `description` only) with `Use when/before/after` triggering conditions
- A `<!-- type: rigid|flexible -->` classifier
- Body sections in order: `## Doctrine` → `## Process` → `## Red flags`
- A red-flags table with header `| Rationalisation | Reality |`

Full rules in [`CONVENTIONS.md`](CONVENTIONS.md).
