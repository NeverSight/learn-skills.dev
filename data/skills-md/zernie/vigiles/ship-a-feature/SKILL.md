---
name: ship-a-feature
description: Ship a NEW capability to vigiles so it actually reaches a user — a new export, public function, subpath, CLI flag, or hook-vocabulary word. Use when about to add, or having just added, a feature / export / public API to this repo. Runs the executable checks a green `npm run check` does NOT make — reachable from a public door, API-surface diff READ, a public doc home, the experimental_ decision, a gate on a frozen tree. NOT for bug fixes, refactors, doc-only or test-only edits.
argument-hint: <the exported symbol, e.g. "alternateSpellings">
---

# Ship a feature (so it ships, not half-ships)

The nine-row definition-of-done already exists — `cohesive-feature-delivery` in
`CLAUDE.md`. On 2026-09-02 `equivalentDisasters` went out tested, gated and
committed, and failed **four** of those rows unnoticed: unreachable from every
public door, a neighbour's JSDoc silently stolen, no doc, no stability mark.
Prose in a 2000-line file does not fire. This does. **Every check below names
the failure it was written for; nothing here is theory.**

## 1. Before writing — three decisions only you can make

| Decision                                                   | Criterion                                                                                                                                                                                                                |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Which door?** (`package.json` `exports` subpath)         | Free + deterministic → `.` (`src/test.ts`). Bills a model → `./eval` (`paid_` prefix). Hook vocabulary → `./hook`. A symbol not re-exported from a door's barrel **does not exist** to `require("vigiles")` (failure 1). |
| **Stable or `experimental_`?**                             | STABILITY.md: exported + not stable ⇒ `@experimental` tag AND `experimental_` name. One day old with one consumer is not stable. ESLint `local/experimental-name` holds tag→name; it cannot write the tag (failure 4).   |
| **Where does the WHY live publicly?** (`document-the-why`) | A `docs/*.md` section beside the claim it changes — for `equivalentDisasters`, next to "blocks 7/7" in `docs/compiled-hooks.md`. Not the README (brevity), not this file (contributor tier).                             |

Write the answers into the PR body. The script below refuses to pass the
stability row until you state it.

## 2. After writing — one command, five checks

```sh
npm run build
node .claude/skills/ship-a-feature/scripts/ship-check.mjs <symbol> [--stable "<why it is stable>"]
```

| Check          | What it executes                                                                                   | Measured failure it exists for                                                                       |
| -------------- | -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **REACHABLE**  | `import()`s every `exports` subpath from the built `dist/`; the symbol must be a key on ≥ 1        | `equivalentDisasters` in `src/guardrail-check.ts`, never in `src/test.ts` → `undefined` (1)          |
| **SURFACE**    | regenerates `api-surface/` (`api:report`), then READS `git diff`: any `+… (undocumented)` fails    | inserted between `verifyGuardrail`'s JSDoc and its declaration; the diff said so, nobody read it (2) |
| **DOCUMENTED** | `\b<symbol>\b` must occur in `docs/**/*.md` or `README.md`                                         | no public home until asked (3)                                                                       |
| **FINDABLE**   | two pages must name it — or one names it and another LINKS to that section's anchor                | documented once, inside a guide about a DIFFERENT feature, with no inbound link (5)                  |
| **MARKED**     | declaration's JSDoc has `@experimental`, or the name is prefixed, or you passed `--stable "<why>"` | exported one day old, no tag, no prefix; the lint rule had nothing to hold (4)                       |

**DOCUMENTED and FINDABLE are different questions.** The first asks whether the
capability is written down anywhere. The second asks whether a reader who does
not already know which file to open can get to it. `experimental_equivalentDisasters`
(since renamed `experimental_alternateSpellings`) passed the first and failed the second: it was explained once, under its own
heading, inside the guide for a different feature, and nothing linked there — so
the testing guide, where someone asking "does my guard actually block?" looks,
named it zero times. A pointer satisfies FINDABLE; you do not have to repeat the
explanation.

`✗` means fix and re-run; the script prints the fix beside each finding. A `✓ MARKED
stable` line carries your reason — paste it into the PR body.

## 3. The gate — on a FROZEN tree, in the foreground, with its real exit code

```sh
node .claude/skills/ship-a-feature/scripts/ship-check.mjs --gate     # = npm run check, frozen
```

It hashes the tree before and after and fails if anything changed while the
gate ran. Three measured ways a gate lies, all closed by running it this way:

- **Editing during the run** (5): `npm run check` linted a half-written file and
  failed on errors that belonged to no state. Do not touch the tree until it exits.
- **Waiting with `until ! pgrep -f 'check.mjs'`** (6): the waiting shell's own
  command line matches the pattern, so it never ends. Twenty minutes reported as
  "still running". Run gates in the foreground; if you must background one, `wait`
  the PID you spawned. Never `pgrep -f` a string that appears in your own command.
- **`npx vitest run … | tail -8`** (7): the pipeline's status is `tail`'s. Exit 0
  with three tests failing. No pipe after a gate — redirect to a file and read it.

## Already mechanized — call it, do not restate it

| Property                                   | Owner (do not duplicate)                                    |
| ------------------------------------------ | ----------------------------------------------------------- |
| tag `@experimental` ⇒ `experimental_` name | ESLint `local/experimental-name` (in `npm run lint`)        |
| `./eval` symbols carry `paid_`             | `npm run exports:check` (in `npm run check`)                |
| surface drift vs committed snapshot        | `npm run api:check` (in `npm run check`)                    |
| docs' `ts` blocks import real exports      | `npm run docs:check` — only once a doc EXISTS (3)           |
| every CLI verb mentioned in `docs/`        | `src/doc-command-coverage.ts` — verbs only, not API symbols |
| the whole command list                     | `npm run check` (`node scripts/check.mjs --list` prints it) |

## 4. Done means

The five ✓ lines, a `✓ GATE` line, and the PR body naming door · stability
decision · doc section. A feature nobody can `import` is not a feature, and one
nobody can navigate to is not documented.
