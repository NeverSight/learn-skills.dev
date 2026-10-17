---
name: release-notes
description: >-
  Use when writing changelog entries, release notes, or customer-facing "what's
  new" from features, commits, or a feature list. Not for internal code review
  or marketing landing page copy from scratch.
---

# Release notes

## Audience

Ask or infer: **end users** (simple, benefit-led) vs **developers** (technical).

Default: end users unless stated otherwise.

## Structure

```markdown
# v1.4.0 — May 22, 2026

## Highlights
- One sentence theme of the release.

## New
- Feature — why it matters.

## Improved
- Change — user-visible benefit.

## Fixed
- Bug — what was broken.

## Breaking (if any)
- What changed + migration step.
```

## Style

- Past tense or imperative: "Added", "Fixed".
- No internal ticket jargon unless developer audience.
- Group by category; max 5–7 bullets per section; link docs if helpful.

## Input handling

From vague prompts, extract discrete shippable items. Do not invent features not described.

## Avoid

- Wall of commit SHAs for user-facing notes.
- "Various bug fixes" without at least one concrete example when fixes were provided.
