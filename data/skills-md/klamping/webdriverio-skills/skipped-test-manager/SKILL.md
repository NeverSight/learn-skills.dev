---
name: skipped-test-manager
description: Use when temporarily skipping failing WebdriverIO tests for app bugs or unimplemented functionality, while tracking ownership, ticket linkage, and re-enable status.
---

# Skipped Test Manager

Manage temporary test skips as controlled technical debt.

This skill standardizes how tests are skipped, documented, tracked, reported, and re-enabled.

## When to Use

- A test fails due to confirmed app-level bug.
- A test targets not-yet-implemented product functionality.
- A skip already exists and needs tracking, reporting, or re-enable review.

## When Not to Use

- The issue is a test bug that should be fixed directly.
- The failure can be resolved with a small, safe test update.
- You cannot provide reason/ownership metadata for the skip.

## Project Context Files

Read these files first when available:

- `.webdriverio-skills/project-context.md`
- `.webdriverio-skills/project-context.json`
- `.webdriverio-skills/custom-rules.md`

If context is stale or missing, run `managing-project-customizations` first.

## Skip Workflow

1. Confirm the root cause is app bug or unimplemented functionality.
2. Apply `.skip` at the narrowest scope possible (`it.skip` over `describe.skip` when feasible).
3. Add required metadata comment directly above skipped test.
4. Link ticket when provided.
5. Update skip report entries.

## Required Metadata Comment

Add a structured comment immediately above each skipped test:

```js
// TEMP_SKIP reason: <app-bug|unimplemented>
// root_cause: <short explanation>
// since: <YYYY-MM-DD>
// owner: <team-or-person>
// ticket: <optional ticket id/url>
```

If your team has an override format in `.webdriverio-skills/custom-rules.md`, follow it.

## Ticket Linking

- If ticket details are provided, include them in metadata.
- Prefer stable IDs and URLs (e.g. `PROJ-123`, ticket link).
- If ticket integration exists, use ticket status to drive re-enable checks.

## Re-enable Workflow

- Re-check skipped tests when linked tickets are marked resolved.
- Remove `.skip`, keep test intent, and run targeted validation.
- If re-enable fails, update metadata with latest root cause and reopen/extend ticket tracking.

## Reporting

Maintain/update a report at:

- `.webdriverio-skills/skipped-tests-report.md`

Use this skill's report template as the default structure:

- `skills/skipped-test-manager/skipped-tests-report.template.md`

Each entry should include:

- test identifier (spec + test title)
- reason + root cause summary
- since date + age in days
- owner
- ticket reference (if provided)
- current status (`skipped`, `ready-to-reenable`, `re-enabled`)

## Aging Policy

- Compute skip age from `since` date.
- Highlight oldest skips first.
- Mark skips with resolved tickets as `ready-to-reenable`.

## Quick Reference

| Action | Standard |
|---|---|
| Temporary skip | Use `it.skip` / `describe.skip` with metadata comment |
| App bug tracking | Add ticket id/url when provided |
| Re-enable trigger | Linked ticket resolved or explicit user request |
| Reporting | Update `skipped-tests-report.md` with age and status |

## Common Mistakes

- Skipping tests without root-cause metadata.
- Using broad `describe.skip` when only one test should be skipped.
- Leaving skipped tests untracked and unreported.
- Never re-checking skipped tests after ticket resolution.
