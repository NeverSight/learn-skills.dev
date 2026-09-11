---
name: registry-workflow
description: Maintain component registries through taxonomy and sync discipline. Use when changing a shadcn registry or design system, syncing components, or analyzing consumer drift.
---

[REFERENCE.md](REFERENCE.md) owns examples, commands, filters, and governance.

## Classify

Use highest matching level to choose test depth:

| Level | Signals | Tests |
|---|---|---|
| Atom | one primitive, 0-1 state, no custom keyboard/portal | 3-4 |
| Molecule | 2-3 atoms, <=2 state, small handler, optional portal | 5-8 |
| Organism | 3+ state, 3+ imports, custom keyboard/portal | 8-15 |

Radix keyboard behavior is not custom code.

## Consumer drift

1. Match registry/consumer files; run `git diff --no-index --ignore-all-space`.
2. Filter import aliases, client directives, comments, whitespace.
3. Classify each component: `Upstream` reusable fix; `Skip-Import-Only`; `Skip-Outdated` (sync down); `Skip-Business-Logic` (routes/endpoints/analytics/flags/domain).
4. Report one status each; reimplement mixed reusable fixes cleanly upstream.

## Maintain

Ship sync separately. Keep consumer behavior outside managed files. Breaking changes need codemod, changelog, migration example, consumer smoke tests. Stay router/framework agnostic; fix repeated misuse in component API. Changesets state affected components, before/after, rationale.

## Hooks

Copy executable `scripts/ui-registry-warn.sh` and `scripts/registry-check.sh` to `.claude/hooks/`; register PostToolUse `Edit|Write` warning and Stop check. Keep the split-file convention: route pages use `*.page.tsx`; reusable pieces live in `components/`.

Done: both hooks run; component edits warn; `redpanda-ui/` changes without `registry.json` block; registry changes without changeset block.
