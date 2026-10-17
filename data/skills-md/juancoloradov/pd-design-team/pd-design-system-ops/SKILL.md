---
name: pd-design-system-ops
description: >-
  Use when the design system itself needs to grow or be reviewed: a gap was flagged during product work,
  a token or component is proposed or changed, no system exists yet and one should be established, or the
  system needs an audit or changelog entry. To apply the system in product work, use pd-design-system.
metadata:
  team: product-design
  role: design-system-steward
  version: "2.0.0"
---

# pd-design-system-ops — grow and guard the living system

## Overview

The system evolves. This skill lets it grow from real needs surfaced in product work while keeping it
coherent, accessible, and versioned. `pd-design-system` consumes the system; this skill stewards it.
Changing a live system is consequential and hard to reverse, so explain the plan and get confirmation
first, prefer additive changes, deprecate rather than delete, and always give a migration path.

## Before you start

- Load `pd-foundations`: `design-system.md`, `handoff-protocol.md` (system growth loop), `accessibility.md`,
  `compliance.md`, `working-agreement.md`, and the adapter for the project's design tool (`tools/README.md`).
- Read `docs/design/PROJECT.md`. `design_tool` and `design_system` say how updates reach the live system
  (the tool's write path, or edits to token and component code). With `design_system.source: none`,
  start with Mode 0. Paths below are relative to `artifacts_dir` (default `docs/design/`).
- Never edit the skill files for project data; project facts live in `PROJECT.md` and the artifacts.

## Versioning

The system carries `MAJOR.MINOR.PATCH`, tracked at the top of `<artifacts_dir>/design-system/CHANGELOG.md`.

- **PATCH:** a token value tweak with no renamed or removed name; doc fixes.
- **MINOR:** additive: new component, variant, or token.
- **MAJOR:** breaking: any rename, removal, or prop-shape change to something in use.

Bump on every shipped change and cite the new version in the migration note.

**Deprecation:** mark deprecated parts (example: a `_deprecated/` prefix) with a migration note; they
stay for one MAJOR cycle. At the next MAJOR, remove those with zero remaining references (per the
usage scan) and log the removal.

## When to use

- A gap was flagged (`<artifacts_dir>/design-system/SYSTEM-BACKLOG.md`).
- A token or component change is proposed, or the system needs an audit or a health check.
- No design system exists yet (`design_system.source: none`) and design work is about to start.

**Not for:** applying existing parts to a design (`pd-design-system`).

## Mode 0 — no system yet
Run this before any visual work: visual needs tokens to bind to, and `pd-design-system` needs the visual
artifact, so neither can create the first system. Follow "No system yet" in `design-system.md`: propose a
minimal provisional system, get the user's agreement, name an owner who approves later changes, and write
`<artifacts_dir>/<date>-components-provisional-system.md` (`discipline: components`, `status: draft`).
Point `design_system.locations` and `conventions` in `PROJECT.md` at it (`source` stays `none` until a
real system exists), then report it to `pd-design-lead`, which runs the normal pipeline against it.
Later gaps go through Mode A.

## Mode A — gap-driven growth

1. **Read** the backlog, then **triage** each entry: reuse (an existing part covers it; explain),
   extend (variant or token on an existing part), add (new), or reject (say why). The entry's severity
   and blocking flag set the order. Before approving a rename, removal, or reshape, scan current usage:
   search `<artifacts_dir>/**` for the name and check other files or packages that consume the system.
   List the blast radius and decide: additive (MINOR) or breaking (MAJOR plus migration plan).
2. **Design the change:** name (follow the project's conventions), variants and states, tokens,
   accessibility. Check for duplicates. If a shared color token changes value, re-run contrast for every
   component and state that consumes it.
3. **Confirm, then build:** state the plan; on approval apply it via the declared tool (adapter
   recipes), then audit new components with the adapter's checks.
4. **Record:** append to `CHANGELOG.md` (date · version bump · change · migration). Write newly
   discovered conventions (prefixes, property names, token layers) into `conventions` in `PROJECT.md`
   so the next agent starts from current truth.
5. **Propagate:** move artifacts that used a substitute to the new part. Draft or in-review artifacts
   may be edited in place; an approved artifact is superseded by a new dated file, never edited. For a
   MAJOR change, use `<artifacts_dir>/INDEX.md` to find every artifact referencing the old name, list
   them in the migration note as "requiring review", and notify `pd-handoff` if a code mapping or
   shipped token is affected.

## Mode B — review the system

Re-sync the live system, then audit the areas in `references/review-checklist.md` (naming, variants,
tokens, deprecation, accessibility, docs, drift). Report as a table: item · issue · severity
(Critical/High/Medium/Low) · recommendation.

## Output
- `<artifacts_dir>/design-system/CHANGELOG.md` with every shipped change; conventions in `PROJECT.md`.
- Mode 0: `<artifacts_dir>/<date>-components-provisional-system.md`.
- Mode B: `<artifacts_dir>/<date>-components-<topic>.md` (artifact header, `discipline: components`,
  topic such as `system-review`).

## Honesty and domain packs
Check every claim against the live system before asserting a part exists. Scope claims to what was
audited; never call the system "complete" or "fully accessible" (see `compliance.md`). If `PROJECT.md`
lists domain packs, read each pack's design-system section and apply it on top of this skill.

## Common mistakes

- Editing the live system before explaining the plan and getting confirmation.
- Deleting or renaming parts in use instead of deprecating and migrating.
- Shipping a rename, removal, or prop-shape change without a usage scan and MAJOR bump.
- Near-duplicate tokens, variant growth with no plan to collapse it, or naming drift between tokens and
  component properties.
- Adding components without all states, accessibility notes, or docs, or without recording new
  conventions in `PROJECT.md`.
- Letting deprecated parts accumulate with no sunset review.
