---
name: golden-and-snapshot-tests
description: Guards data and pixel goldens - *.golden.test.ts snapshots, append-only [contract] entries, Skia tolerance, jest -u rules. Use when adding a golden or snapshot test or a .snap diff appears. Not for device screenshots (e2e-maestro).
---

# Golden and snapshot tests

Goldens are the frozen answers of an app: the readable text a pure unit produces for fixed inputs,
the output every installed version must reproduce, the pixels a Skia surface draws. They change only
on purpose, after a real look, in a commit that says why, and contract entries never change at all.
This skill writes them in the Jest `golden` project and its two checkers prove that the tree and the
git history keep that policy.

## Rules that must hold

1. **A golden changes only by hand, one file at a time:** `npx jest <file> --selectProjects golden -u`,
   path first. Every script, hook and CI job runs `jest --ci`, which refuses to write a missing
   snapshot. No `-u`, `--updateSnapshot`, `--ci=false`, `CI=false` or baseline `--update` in
   `package.json`, git hooks (lefthook, husky, lint-staged), CI (GitHub Actions, EAS Workflows) or
   agent hooks. Why: an agent rubber-stamps whatever `-u` writes, and after `--selectProjects` a path
   is read as another project name, so every golden is rewritten (verified with `--listTests`).
2. **Look before accepting.** Read the `.snap.ios` diff line by line, open every new or changed PNG
   and its diff image, then `CI=1 npx jest --ci --selectProjects golden` passes. Why: an unread golden
   freezes a bug for every later run.
3. **Every commit that adds, changes or deletes a golden path carries
   `Gate-Change: <which goldens, why, what you looked at>`** (at least 10 characters). Golden paths:
   `**/*.golden.test.ts.snap(.ios|.android)`, `**/__image_snapshots__/**`, the pixel matcher
   `test/goldens/skia-golden.ts`, `.maestro/baselines/**`, plus `goldenPaths` in
   `contracts/goldens.json`. Why: one `git log --grep='^Gate-Change:'` lists every gate change later.
4. **`[contract]` entries are append-only.** Output that every installed version, every device or a
   file a user keeps must reproduce exactly (a backup or export format, a share code, a derived
   identifier such as a scheduled notification id, a date-keyed pick) is pinned in a describe titled
   `[contract] <unit> goldens`, registered in `contracts/goldens.json`, with at least three keys and,
   for date keys, a year-end/new-year pair. An existing entry is never edited, deleted or renamed, not
   even with a trailer; adding keys is fine. If the producing code must change, stop and ask: ship a
   versioned format next to the old one, or switch inputs from a future date. Why: users on the old
   and the new version would get different results from the same input; renaming a title deletes
   the entry (the key is the title).
5. **Data goldens are readable text from pure code.** `<unit>.golden.test.ts` next to the unit, one
   string per case (a header line with the inputs and headline numbers, then short lines or an ASCII
   grid), stored by jest-expo as `<file>.golden.test.ts.snap.ios` next to the test; at most 120 lines
   per entry (aim for 60); no clock, machine locale or unseeded randomness; no rendering. Why: a golden
   is reviewed by reading its diff, and a machine-dependent golden differs between runs.
6. **No component-tree snapshots and no inline snapshots, anywhere.** A `.snap` of a non-golden test
   is deleted and replaced by assertions on roles and text; `toMatchInlineSnapshot` is never used.
   Why: component trees churn on every style change and train `-u` reflexes; `-u` would rewrite the
   test file itself, and Jest 29 with Prettier 3 fails the suite outright (verified).
7. **Pixel goldens (apps that draw with Skia) render the production draw function** offscreen in the
   CanvasKit `golden` project, under `test/goldens/`, at three canvas sizes (narrow 320x400, phone
   390x560, tablet 1024x700; a fixed-size drawing says `// fixed-size: <why>`, and a pipeline smoke
   test that draws a function defined in the test is exempt) and, when it animates,
   at moments 0, 0.5 and 1, with fonts loaded explicitly, through the one matcher
   `test/goldens/skia-golden.ts` (`toMatchPixelGolden`), never a per-call threshold.
   `jest-image-snapshot` 6.5.2 and `@types/jest-image-snapshot` 6.4.2 are pinned exactly. Why: goldens
   catch what assertions forget only when they draw what users see, at the sizes they see it.
8. **Tolerances are gates:** 0.1% of pixels for Skia goldens (the matcher), 0.2% for simulator and
   emulator screenshots (e2e-maestro). Never raise one to hide a diff; a raise needs the reviewer's
   agreement first, then the matcher and `contracts/goldens.json` `maxPixelTolerance` change together
   in a commit with `Gate-Change: <name> <old> -> <new> approved by <reviewer>: <reason>`. Why: a
   raised tolerance silently accepts every future regression below it.
9. **Snapshots never outlive their tests and diffs never reach git.** An obsolete entry is removed with
   `-u` on that one file; an orphan `.snap` or baseline PNG is deleted with its test
   (`baseline-orphan`); `.gitignore` lists `reports/` and `**/__image_snapshots__/__diff_output__/`; `quality-gates.json` `gatedPaths` lists the golden paths.
   Why: an obsolete entry makes `jest --ci` exit 1 even when every test passed (verified), and a
   golden path missing from the gate is changed without a trailer.
10. **A failing golden is investigated, not re-accepted.** Decide: a bug (fix the code, keep the
    golden), intended (update that one file, rules 1 to 3) or a contract entry (always a bug). A
    golden that differs between two runs of the same commit means the code reads time or randomness.
    Why: the generators, formatters and CanvasKit are deterministic, so noise is a bug.

## Workflow

1. **Know the policy** once per session: read [references/golden-policy.md](references/golden-policy.md)
   (the kinds of golden, where each lives, the only way to change one, contract entries, failure
   triage, iOS and Android notes, "When multi-package").
2. **Pick the kind.** Readable output a reviewer checks: a data golden. Output installed versions
   must reproduce: a `[contract]` describe in a data golden. A Skia surface: a pixel golden. A whole
   screen on a device: a screenshot baseline (e2e-maestro). Seeded generator output: golden vectors
   (seeded-determinism-and-golden-vectors). Then read
   [references/data-goldens.md](references/data-goldens.md) or
   [references/pixel-goldens.md](references/pixel-goldens.md).
3. **A data golden:** if `test/goldens/golden-text.ts` is missing, copy it and its test from
   `templates/test/goldens/`. Imitate `templates/src/features/__FEATURE__/__FEATURE__-digest.golden.test.ts`
   (the digest unit and its reviewed `.snap.ios` show a complete, verified pair): a `describe<Unit>()`
   function that returns one string, fixed inputs, titles that start with a third-person verb.
4. **A contract:** put its cases in `describe('[contract] <unit> goldens', ...)`, pin at least three
   keys (a year-end/new-year pair for date keys, and a leap day), and register it in
   `contracts/goldens.json` (the first time, copy `templates/contracts/goldens.json` and its schema and
   replace the sample digest entry with yours; the checker fails a marked describe the register does
   not list, and an app with no contract needs no register). [examples/backup-envelope.golden.test.ts](examples/backup-envelope.golden.test.ts)
   shows a format contract.
5. **A pixel golden:** if `test/goldens/skia-golden.ts` is missing, copy
   [templates/test/goldens/skia-golden.ts](templates/test/goldens/skia-golden.ts) and run
   `npm install --save-dev --save-exact jest-image-snapshot@6.5.2 @types/jest-image-snapshot@6.4.2`
   (without the types, `npm run typecheck` fails with TS7016). The surface's golden test, draw code and
   layout come from skia-canvas-rendering's template.
6. **Create the goldens deliberately:** `npx jest <file> --selectProjects golden --listTests` (it must
   list only that file), then `npx jest <file> --selectProjects golden -u`. Read every new entry or
   open every new PNG with your file-reading tool, compare it with what users should get, then
   `CI=1 npx jest --ci --selectProjects golden`.
7. **Check the tree:** `node ${CLAUDE_SKILL_DIR}/scripts/check-goldens.mjs .` and fix every `FAIL`
   line (file, rule, fix); rerun until `RESULT: PASS`. Rules and options:
   [references/checkers.md](references/checkers.md).
8. **Commit with the trailer** ([examples/gate-change-commit.txt](examples/gate-change-commit.txt)):
   write the message to a file, stage, run
   `node ${CLAUDE_SKILL_DIR}/scripts/check-golden-changes.mjs . --staged --message <file>`, commit. At
   the end of the session run it with `--range <base>..HEAD` (base: the commit before the session's
   first); in CI, `--range origin/main..HEAD`.
9. **When a golden fails later:** follow "When a golden fails" in the policy reference. Bug: fix the
   code. Intended: step 6 for that one file, then step 8. A contract entry changed: revert, or stop and
   ask the reviewer. A wide re-acceptance (a Skia or font upgrade) follows run-goldens-rebaseline;
   after a Jest major (SDK 58 brings Jest 30) every file fails on its header: "Jest upgrades" in the policy.

## Definition of done

- [ ] Every data golden has its `.snap.ios`, every pixel golden its baselines, and
      `CI=1 npx jest --ci --selectProjects golden` passes with no obsolete snapshot.
- [ ] Every new or changed entry was read and every new or changed PNG opened; the report names them
      and why they changed.
- [ ] Every contract is registered in `contracts/goldens.json`, pins at least three keys (a
      year-boundary pair for date keys), and no existing `[contract]` entry changed.
- [ ] No script, hook or CI job writes goldens; no tolerance went up without an approval trailer.
- [ ] Every golden change sits in a commit with a `Gate-Change:` trailer, and
      `node ${CLAUDE_SKILL_DIR}/scripts/check-golden-changes.mjs . --range <base>..HEAD` prints
      `RESULT: PASS`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-goldens.mjs .` prints `RESULT: PASS` (allowed while
      adopting: `SKIP quality-gates.json [gated-path-missing] not yet created (quality-gates creates it)`,
      `SKIP .gitignore [diff-output-ignored] not yet created (typescript-and-lint-rules creates it)`)

## Anti-patterns

- **`npx jest -u` to make a red suite green.** It rewrites every golden that differs, bugs included.
  Read the failure, fix the code, and update only the one file you meant to change.
- **`npx jest --selectProjects golden <file> -u`.** The path becomes a second project name and every
  golden is rewritten. Put the path first and preview with `--listTests`.
- **Editing a `.snap.ios` by hand.** The next `-u` or a renamed test undoes it, and it hides what the
  code really produces. Change the code, then regenerate that file.
- **Re-accepting a `[contract]` entry "because the format improved".** Installed versions and files
  users kept still expect the old output. Version the format or ask the reviewer.
- **Renaming a contract describe "for consistency".** The snapshot key is the title, so the history
  check sees the old entry deleted. Keep the title; add a comment instead.
- **A 400-line JSON dump as a golden.** Nobody reviews it, so any change gets accepted. Describe the
  output as a header line and the fields that matter.
- **`expect(screen.toJSON()).toMatchSnapshot()` on a component.** It churns on every style tweak.
  Assert roles and text (unit-and-component-tests); screens are covered by screenshots.
- **`new Date()` or `toLocaleDateString()` in a golden.** It passes today on this machine only. Pass a
  date key or an instant literal and an explicit locale.
- **`failureThreshold: 0.01` in a test "because CanvasKit is noisy".** CanvasKit renders are
  byte-identical run to run; noise means the draw path reads time or randomness.
- **A pixel golden at one size or without the 0 and 1 moments.** Clipping at narrow sizes and wrong
  start or end states are the most common canvas bugs.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/golden-policy.md](references/golden-policy.md) | The kinds of golden and where they live, the only way to change one (verified Jest facts), gated paths and the trailer, contract entries, failure triage, obsolete and orphan snapshots, Jest upgrades (the snapshot header), iOS and Android, When multi-package | Workflow step 1, and whenever a golden fails |
| [references/data-goldens.md](references/data-goldens.md) | What deserves a data golden, readable text, the template pair, the snapshot file, reading a diff, writing and evolving contracts, formats worth pinning, the games appendix | Workflow steps 3 and 4 |
| [references/pixel-goldens.md](references/pixel-goldens.md) | The golden project and matcher, sizes and moments, fonts, accepting baselines, reading a failure, Skia upgrades, screenshot baselines on iOS and Android, headless previews | Workflow step 5 |
| [references/checkers.md](references/checkers.md) | Both checkers: rules, options, rn-skills.config.json keys, the contract file, SKIP lines, the log capture, CI use, troubleshooting | Workflow steps 7 and 8 |
| `templates/test/goldens/golden-text.ts` | `headerLine`, `goldenText`, `renderGrid`: readable golden text | Workflow step 3, when missing |
| `templates/test/goldens/golden-text.test.ts` | Its unit test | Copied with it |
| [templates/test/goldens/skia-golden.ts](templates/test/goldens/skia-golden.ts) | `toMatchPixelGolden`: 0.1% of pixels, diffs to `reports/visual/diff/` (canonical, synced; this skill owns it) | Workflow step 5, when missing |
| `templates/src/features/__FEATURE__/__FEATURE__-digest.ts` | A pure Tasks unit to pin: the daily digest plan and its notification id | Workflow step 3, as the shape of a pinned unit |
| `templates/src/features/__FEATURE__/__FEATURE__-digest.golden.test.ts` | The data golden pattern: a describe function, fixed inputs, a `[contract]` describe | Workflow steps 3 and 4 |
| `templates/src/features/__FEATURE__/__FEATURE__-digest.golden.test.ts.snap.ios` | Its reviewed snapshot (what readable entries look like) | Workflow step 3 |
| `templates/contracts/goldens.json` | The contract register both checkers read; its digest entry is a sample to replace (canonical, synced; this skill owns it) | Workflow step 4 |
| `templates/contracts/goldens.schema.json` | Its JSON schema (keys and meaning; canonical, synced) | Workflow step 4 |
| [examples/backup-envelope.golden.test.ts](examples/backup-envelope.golden.test.ts) | A format contract: backup format 1 pinned for boundary inputs | Workflow step 4 |
| [examples/backup-envelope.golden.test.ts.snap.ios](examples/backup-envelope.golden.test.ts.snap.ios) | Its snapshot | Workflow step 4 |
| [examples/gate-change-commit.txt](examples/gate-change-commit.txt) | Commit messages with the Gate-Change trailer (created, re-accepted, contract key added, tolerance approved) | Workflow step 8 |
| `scripts/check-goldens.mjs` | Checks the tree: snapshots present, readable and owned, no component or inline snapshots, no ambient input or UI in goldens, contracts, pixel matcher, sizes, baselines, no automated `-u`, `jest --ci` everywhere, gated paths, ignored diffs | Workflow step 7 and the definition of done |
| `scripts/check-golden-changes.mjs` | Checks commits or the staged change: Gate-Change trailers, `[contract]` entries never edited or deleted, tolerances never raised without approval | Workflow step 8 and the definition of done |
| `scripts/lib/golden-config.mjs` | The checkers' shared reader of paths, rn-skills.config.json keys and `contracts/goldens.json` | When a checker changes |
| `scripts/selftest.mjs` | Proves both checkers pass the templates and catch every planted bug | After changing a checker or a template |
| `scripts/check-lib.mjs` | Shared script library (synced; do not edit here) | Never by hand |
| `assets/shared.json` | Declares the synced files (check-lib, the pixel matcher, the register and its schema) | When adding a shared file |
| `assets/template-placeholders.json` | The placeholder values the template verification and the self-test use | When adding a placeholder |
| `tests/bases/app/` | The minimal app the fixtures lay the templates on | When the fixture base changes |
| `tests/fixtures/` | Overlay suites: `good/`, one `bad-*` per rule, `pass-*` and `error-*` cases; real `git log` captures for the history checker | When adding a checker rule |

## Related skills

- `unit-and-component-tests` - the Jest projects (the golden project's config), component tests and their `component-snapshot` rule.
- `run-goldens-rebaseline` - the manual ritual for re-accepting many goldens at once.
- `skia-canvas-rendering` - the surface draw code, its golden test template and draw-call label tests.
- `seeded-determinism-and-golden-vectors` - seeded generators and their oracle-filled vectors.
- `e2e-maestro` - simulator and emulator screenshot baselines (same policy, 0.2% tolerance).
- `git-commits-and-reporting` - the commit format, the Gate-Change trailer and the change report.
- `quality-gates` - `quality-gates.json` gated paths and the commit-msg hook that asks for the trailer.
- `data-export-and-restore` - backup and export formats that contract goldens pin.
- `level-generation-and-solvers` - level and daily-level goldens in games.
