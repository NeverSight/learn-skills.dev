---
name: sb-ship
description: "Graduate ONE Explore experiment to a production component — preserve the experiment (cp, never git mv), pick new-vs-update, close the decision loop. Use for 'ship this', 'promote this experiment', 'graduate to production'."
compatibility: "Requires bash and git; ast-grep optional for rewriting callsites on graduation; Node.js optional (validate-stories --strict runs tsc/eslint via npx)."
allowed-tools: Bash Read Glob Grep Write Edit
license: MIT
metadata:
  author: strongeron
  version: '2.3.0'
  bundle: storybook-workbench
  vendor:
    # Skill-local files live in scripts/; references/ + templates/ here are resolved from
    # shared/ ($CORE) in dev and copied into dist/ by build.sh on export.
    scripts: [validate-stories.sh, find-stories-by-tag.sh]
    wrappers: false
    references: [propagate-workflow.md]
    templates: [design-decisions.md]   # templates/ — propagate-workflow.md points readers to it; vendored on export
---

# sb-ship — graduate, preserving history

Event-triggered when an Explore iteration meets the graduation gate. **The one rule that matters:
preserve the experiment — `cp`, never `git mv`.** The Explore story stays as design history;
`git mv` here is the destructive bug `propagate-workflow.md` exists to prevent. **Load
`references/propagate-workflow.md` before any Ship action** — it's the *only* reference
this skill needs; **Do NOT load** the sb-wrappers/sb-audit refs (lifecycle, galleries, composition) for
a Ship.

## Decide the path (ask yourself)

- **Did the Explore define its own component file, or iterate on an existing one?** → Path A vs Path B.
- **Path B: evolve in place (B1) or keep V1 in `_legacy/` (B2)?** B2 only when V1 still has live
  callsites needing a migration window.
- **Did the import path change?** If yes → `ast-grep` callsites. If not → skip it.
- **Other tagged stories that should flip?** (a Compare `decision:pending` → `decision:chosen` + winner.)

## Execute

- **Path A — NEW component.** `cp` the component explore→components, write a *fresh* production
  stories file **to the recorded `storiesLocation`** (`.storybook/audit/status.md`; the rule lives in
  `CONTEXT.md` §STORIES LOCATION — never scatter) — don't `cp` the Explore stories (production has
  different concerns: autodocs, no decision metadata), validate, then `ast-grep` callsites only if a path changed.
- **Path B — UPDATE existing.** Apply the Explore's diffs into the production component + stories
  in place; `ast-grep` only if the import path changed.
- **Both — close the loop IN PLACE** (no `git mv`):
  `tags: ['explore','decision:chosen','archived','!autodocs','!test']` +
  `parameters.decision = { status, winner, date, shippedTo }`. Confirm with
  `find-stories-by-tag.sh decision:chosen`.

## Gate + next

Run the bundled `scripts/validate-stories.sh` on the new production story (in the bundle:
`${CLAUDE_PLUGIN_ROOT}/scripts/validate-stories.sh`, or
`${CLAUDE_PLUGIN_ROOT}/scripts/`). Confirm the flip with `scripts/find-stories-by-tag.sh
decision:chosen`. Append the decision to the ledger (`templates/design-decisions.md`); the graduated experiment stays put.

**Re-enter the usage flow.** A graduated component is new to `src/` — it isn't in the rendered JSONs
yet, so its Docs "Real usage" band and `storyCoverage` are blank. Trigger the one-command usage refresh
(`refresh-usage.sh`, owned by `sb-audit`/`sb-inventory`) so the new component enters `component-usage.json`
/ `project-inventory.json`; a Storybook rebuild then shows its real usage. Then `/sb-hub`.
