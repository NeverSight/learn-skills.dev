---
name: preflight
description: Reads the diff between the current branch and main and produces a production pre-flight checklist of everything that must be done or configured once the change merges. Use before merging or deploying a branch.
---

# Preflight

Produce a production pre-flight checklist for the current branch.

## Steps

1. Get the diff against the base branch: `git diff main...HEAD`.
2. Read every changed hunk. Look for things that need action in production once
   this merges — for example:
   - new environment variables / config keys
   - new or changed database migrations
   - work pushed onto a queue (needs a worker running)
   - new external services, mail, storage, or credentials
3. Build a checklist of those items. Group them primarily by **type** — a
   freeform category that fits the work, choosing whatever labels suit the diff.
   Common ones (not a fixed list):
   - **Database** — migrations, schema, seed data.
   - **Infrastructure** — queue workers, schedulers, services that must run.
   - **Configuration** — env vars, config keys, credentials.
   - **Operational** — things to confirm or watch in production.
4. Within each type, sub-group the items by confidence. Use whatever confidence
   label fits — for example **Required** (broken without it), **Verify** /
   **Likely** (almost certainly needed, depends on setup), **Recommended** /
   **Nice to confirm** (worth a glance, may already be handled).
5. For every item, cite the file in the diff that implies it (no line numbers).

## Rules

- Only include items the diff actually supports. Do not guess or pad the list.
- If a type or confidence group has no items, omit it.
- Order types so the most action-required ones come first.
- Render each type as a real heading: the name on its own line with an
  underline rule of box-drawing dashes (`────`) directly beneath it, matching
  the width of the name. Confidence labels stay as plain sub-headings.
- Keep the output short: type heading, confidence sub-heading, one line per item.
  No preamble, no summary.
