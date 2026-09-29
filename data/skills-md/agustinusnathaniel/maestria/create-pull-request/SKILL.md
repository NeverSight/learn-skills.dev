---
description: Draft or revise a pull request title and body. Use when preparing a PR, reviewing its text, or refreshing it after a push.
name: create-pull-request
---

# Create Pull Request

You are the agent preparing the PR draft. Work in order: gather inputs, check the project template, write the title and body, then complete the draft or publish it when requested.

## When to use

Use when preparing, revising, or reviewing a PR title and body draft, updating a PR after a push that changed diff or verification, or checking PR text when publication is requested. Read-only drafting or revision counts as in scope even when no capture, upload, or publication tool is available; a draft-only request completes with a usable title and body while outstanding publication or evidence is reported as the remaining step.

Do not use for code or diff investigation where no PR preparation is requested, merge/release/production decisions, or protected-branch commits. Those stay under the host, user, and project authorization and review rules.

If the project forbids PR creation, stop only that operation and report it as the blocker for the PR step; continue other requested work. A ban on installing tools forbids neither drafting nor using a tool that is already available; stop only the forbidden operation and report the blocker on the affected step.

## Multiple PRs

For a multi-PR outcome, state each PR's scope, acceptance evidence, base branch, prerequisites, and review status in its draft. Check that the description covers only its own diff.

## Title

Write an explicit Conventional Commits title. Do not infer it from commit message format. Keep it human-readable and scoped to the user-visible outcome or maintainer benefit.

## Body structure

Use literal `##` headings in this order:

1. `## Summary`
2. `## Changes`
3. `## Verification`
4. `## Visual evidence` (only when the change has a rendered surface)
5. `## Breaking changes` (only when applicable)

Project template precedence: when the project defines an explicit PR template, follow that template while preserving the required information above. Do not impose these literal headings on a replacement template. Map content across, then confirm nothing required was dropped.

Default body template (use when no project template applies):

```markdown
## Summary

[User-visible outcome or maintainer benefit, one short paragraph or concise bullets. No session IDs or internal execution metadata.]

## Changes

| File           | What changed                        | Why           |
| -------------- | ----------------------------------- | ------------- |
| `path/to/file` | Actual change and practical purpose | Review reason |

## Verification

[Checks run, results, unresolved gaps. Note review outcome briefly, no pasted identifiers.]

## Visual evidence

[Only for rendered surfaces: published artifacts, captions, current coverage; or `Not applicable: <concrete reason>`.]

## Breaking changes

[Only when applicable: migration guidance.]
```

Rules for `## Changes`: describe the actual change and practical purpose, not the editing action. Group related files with one rationale. List only symbols that help review. Omit session IDs and internal metadata.

Rules for `## Verification`: list checks and results honestly. Carry unresolved acceptance gaps. Never claim unverified results.

## Completion

Complete the request in one of two ways:

1. Draft-only request: the draft is complete when the title and body are usable and every outstanding item (publication, missing evidence, unchecked variants) is reported with its checked limitation. A draft-only result never presents itself as published.
2. Actual PR creation or update, when requested and the tooling is available: publish with the existing host tooling, checking the tool current help when needed instead of relying on cached syntax, then read back the published body yourself and confirm it matches the current diff before reporting delivery. When publication or a required publishing step is unavailable or forbidden, report the outcome incomplete with the exact blocker instead of claiming delivery.

## Visual evidence where required

When the change has a rendered surface, visual evidence is required; otherwise write `Not applicable: <concrete reason>` in the body and skip this section, including draft-only requests.

For rendered surfaces, capture, handoff, publication in the PR body, and readback are distinct stages. A local path alone does not satisfy PR-body publication.

Capture the affected screen or interaction, including relevant responsive or state variants, with an available browser or capture tool; a missing desktop display alone does not rule out headless capture. For text-only CLI output, a representative terminal transcript can be sufficient. If vision is available, inspect the capture; otherwise label it visually unverified. Preserve the local artifact at any workable path, including /tmp; do not auto-commit screenshots unless project policy requires it. Keep capture effort proportionate to the changed surface.

Record evidence as paths plus captions plus coverage gaps: each artifact states what it shows and which variants remain unchecked. When project review rules require an independent check, a reviewer checks that coverage against the changed surface before delivery.

Present evidence concisely by changed screen or behavior: label each artifact with its state and relevant viewport or theme. Use a before/after table when comparison helps and a short captioned list for a single state or when tables would shrink images. Pair comparable captures with matching viewports and states, name the intended difference, and disclose missing baselines or unchecked variants without fabricating them. Keep representative captures in the main section with supplemental captures in a collapsible section when supported.

For applicable changes, report evidence captured, unavailable with the checked limitation, or unnecessary with a concrete reason. Source-only documentation edits and mechanical moves preserving rendering can use existing evidence; a refactor label or passing build alone does not establish unchanged visuals.

Publish required evidence in the PR body as an attachment or accessible artifact link with a descriptive caption, using supported authorized tooling; check the tool current help for upload support instead of relying on cached syntax. Capture and upload are separate capabilities. If upload is unavailable, preserve the local artifact, give its path in the handoff, and state the PR attachment limitation.

If required visual evidence is missing, the published result is incomplete: state the checked limitation. Do not report delivery as complete until the evidence is published in the PR body and you have read back the published body to verify its inclusion; local paths, session-log references, and comments alone do not satisfy this requirement. Do not waive an explicit user or project evidence requirement because tooling is missing: provide it or report the outcome incomplete with the exact blocker. Optional PR illustration may be omitted with a reason; required evidence cannot silently become a follow-up.

Read back the actual PR body yourself; confirm attachments render or links resolve and evidence matches the current relevant diff.

When a later change affects captured appearance or behavior, replace affected captures, update captions and comparisons, and remove obsolete or redundant PR body references; keep intentional clearly labeled before baselines and never present a historical before as current. Refresh only affected evidence, not every commit or unrelated file.

## Freshness

After any push that changes the cumulative diff or verification evidence, update the title and body to match, then read back the published body for a published PR to confirm it matches before reporting delivery. For a draft-only request, present the updated draft with outstanding items reported. Refresh only affected content, not every commit or unrelated file.
