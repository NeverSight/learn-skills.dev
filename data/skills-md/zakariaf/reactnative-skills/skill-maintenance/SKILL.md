---
name: skill-maintenance
description: Builds and repairs agent skills (SKILL.md) - scaffold, descriptions, self-tested checkers, routing evals. Use when creating, editing or checking a skill, or one does not load or trigger. Not for app errors (troubleshooting-playbook).
---

# Skill maintenance

Makes every change to an agent skill land finished: built to the skill standard, self-contained, routed by a sharp description, and proven by its own checkers and their planted-bug self-test. The usual reader of a skill is an agent working with no human review, so a skill is correct only when the checks here say so.

## Rules that must hold

1. **A skill is done only when its checks pass.** `validate-skill.mjs`, the skill's own `scripts/selftest.mjs` and `check-skill.mjs` all print `RESULT: PASS`; nobody reads skill files closely, so nothing else counts as review.
2. **Copy knowledge in; never point at it.** No repo docs, design files, research notes, other skills' files, maintainer tooling paths, absolute, scratch or `../` paths, and no runtime variable that only some agents set (`${CLAUDE_SKILL_DIR}` in markdown is the one allowed); a skill is installed alone (a plugin cache, `.agents/skills/`, `.claude/skills/`) and every pointer dangles there.
3. **The description decides whether the skill is ever used.** At most 300 characters (aim for 250), a third-person verb first, "Use when" with the words tasks contain, and "Not for <work> (<neighbour-skill>)"; the agent sees only names and descriptions before it loads a skill, and that listing is budgeted.
4. **Rules and the definition of done sit at the top, in the six-section order, and SKILL.md stays at 300 lines or fewer.** After context compaction only the first 5,000 tokens of a skill survive, so whatever sits lower is lost in long sessions.
5. **Frontmatter is `name` and `description`, plus the few allowed keys.** `disable-model-invocation: true` belongs only on a side-effecting `run-*` runbook whose workflow stops and asks; `allowed-tools` and `hooks` make the agent's own invocation need approval (denied in headless runs), and `paths` or `user-invocable` hide the skill.
6. **Every checker proves itself against planted bugs.** A good case and one `bad-*` case per rule listed in its `--help`, each EXPECT naming the rule id, written as overlay cases (a `mutation.json` on a shared base); a check that has only ever passed proves nothing, and an EXPECT that says only "FAIL" passes on a crash.
7. **Checkers keep the output contract and never pass on nothing.** Positional repo root, `--help`, exit 0/1/2, a `RESULT:` last line; a missing target exits 2; SKIP only through `notYetCreated()` for a file another skill creates, NOT APPLICABLE only for a repo fact, and ship gates never skip; a silent pass turns a gate green on a typo.
8. **Checkers read the app through its layout and contracts, never through hard-coded paths.** `resolveLayout()` for folders, `walkRepo()` for scans (it prunes installed skills, whose fixtures plant bugs on purpose), app facts in a repo-owned `contracts/<name>.json` whose template the skill ships, and every device named (`maestro --device`, a simctl UDID, `adb -s`, an AVD name); otherwise the checker works in one repo only or reaches another session's simulator.
9. **Templates are real files that name their repo path on line 1 and pass a real app's gates.** `tsc`, ESLint and Jest in a reference app; a template that does not compile teaches the bug it was meant to prevent.
10. **Edit the canonical copy, never a synced or generated file.** Shared files change in the library's shared folder and arrive through its sync; generated files change through their generator; the next sync or render erases a hand edit, and the validator fails on drift first.
11. **Every version-sensitive fact carries a "verified on" date and a re-verify command.** Expo, React Native and agent tooling move faster than memory; a dated fact with its command is refreshed in minutes, an undated one rots silently.
12. **Touch only the skill you were asked to change.** Other people and agents work on other skills in parallel, writes under `.claude/` need the developer, and shared or generated files have owners; put every other needed change in the report.

## Workflow

1. **Decide: a new skill or a change to an existing one.** Run `node ${CLAUDE_SKILL_DIR}/scripts/check-routing.mjs . --prompt "<the task>"` from the repo root to see which skill already wins the task: it prints the top three as `rank #1 <skill> (score ...)` and judges nothing (add `--expect <skill>` to make it an eval); in a repo whose only skills are installed ones the root prints NOT APPLICABLE, so pass `.agents/skills` instead of `.`. Read [references/descriptions-and-routing.md](references/descriptions-and-routing.md) when the boundary is unclear; extend a skill rather than adding a near-duplicate.
2. **New skill:** `node ${CLAUDE_SKILL_DIR}/scripts/new-skill.mjs <name> --skills-root skills` (add `--runbook` for a side-effecting `run-*` runbook; a repo without `skills/` yet gets it created). The scaffold holds the six sections, a reference, a working pattern checker with its overlay self-test, and `__FILL_...__` placeholders wherever a person must write. Read [references/authoring-standard.md](references/authoring-standard.md) before filling it; [examples/new-skill-walkthrough.md](examples/new-skill-walkthrough.md) shows a complete run.
3. **Knowledge:** copy it into `references/` (a Contents list when over 100 lines), `templates/` (line 1 names the repo path; prove each in a real app with `tsc`, ESLint and Jest), `examples/` (shapes only) and `assets/`. Date every version fact and give its re-verify command.
4. **Scripts:** read [references/writing-scripts.md](references/writing-scripts.md) for the contract and the check-lib API, then [references/self-tests-and-fixtures.md](references/self-tests-and-fixtures.md) for the overlay cases. Write one `bad-*` case per rule, then run each checker on a real app repo and read every finding: a rule that fires on correct code gets ignored.
5. **Description:** write it with the descriptions reference, then add two realistic prompts for the skill and one near miss for its closest neighbour to the repo's routing evals (`contracts/routing-evals.json`): copy both [templates/contracts/routing-evals.json](templates/contracts/routing-evals.json) and `templates/contracts/routing-evals.schema.json` into `contracts/` (the evals file names the schema beside it), then replace its `__PLACEHOLDER__` seeds with the new skill, its neighbour and their prompts; `check-routing.mjs` fails on a seed left in (`eval-placeholder`).
6. **Check the skill:** `node ${CLAUDE_SKILL_DIR}/scripts/validate-skill.mjs skills/<name>`, then `node skills/<name>/scripts/selftest.mjs` when it has scripts, then `node ${CLAUDE_SKILL_DIR}/scripts/check-skill.mjs skills/<name>`. Fix every `FAIL` line and rerun until all three pass. In a skill library with a canonical shared folder, add `--shared <that folder>` to the validator so it also proves the synced copies.
7. **Check the set:** `node ${CLAUDE_SKILL_DIR}/scripts/check-skill-set.mjs .` (the repo root, so skills installed under `.agents/skills` count for collisions and the listing) and `node ${CLAUDE_SKILL_DIR}/scripts/check-routing.mjs .`. A problem your change caused is yours; one in a skill someone else is building goes in the report (`--skip-missing` turns evals for unbuilt skills into notes). After a description rewrite, confirm with the agent itself: `check-routing.mjs . --live --only <name> --runs 3 --plugin-dir .` (a few short model calls; `--plugin-dir .` loads skills authored in `skills/`, which the agent otherwise never sees, and the run stops with exit 2 when an expected skill is not loaded).
8. **Library round,** when the repo is a skill library with its own tools (shared-file sync, a catalogue, all self-tests): follow [references/library-round.md](references/library-round.md), which also covers the development loop and the settings that keep skill scripts from prompting.
9. **When a skill does not load, trigger or run,** match the symptom in the pitfalls table of [references/how-skills-load.md](references/how-skills-load.md).
10. **Report:** the skill, its description, what each script checks, the `RESULT` lines, and everything left for someone else (another skill's files, a shared file's owner, settings, a human step). Name the review items no checker can see (the heuristic limits in the authoring-standard reference): a prose pointer to a repo document, a reference copied without its source and date, a skip whose rule id is not a literal.

## Definition of done

- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/validate-skill.mjs skills/<name>` prints `RESULT: PASS`, and `node skills/<name>/scripts/selftest.mjs` prints `RESULT: PASS` when the skill has scripts, with every `bad-*` case failing for its own rule.
- [ ] Every template names its repo path on line 1 and passed `tsc`, ESLint and Jest in a real app; every version fact is dated with a re-verify command.
- [ ] The repo's routing evals hold two prompts for the skill; `node ${CLAUDE_SKILL_DIR}/scripts/check-skill-set.mjs .` shows no problem caused by this change and `node ${CLAUDE_SKILL_DIR}/scripts/check-routing.mjs .` passes (`--skip-missing` only while other skills are still being built).
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-skill.mjs skills/<name>` prints `RESULT: PASS`

These scripts print no SKIP lines. In a repo with no project skills (none in `skills/`, `.claude/skills/` or `.agents/skills/`) each prints `NOT APPLICABLE: no project skills ...` and passes; in a repo whose only skills are installed ones it prints `NOT APPLICABLE: only installed skills (...)` (pass `.agents/skills` to check those).

## Anti-patterns

- **"See the handbook, chapter 14, for the details."** The chapter is not there when the skill runs elsewhere; copy the rows you need into a reference.
- **Fixing a routing miss by pasting the eval's words into the description.** Name the category of work, or add a "Not for" to the skill that won.
- **Editing `scripts/check-lib.mjs` (or any synced file) inside a skill.** The next sync reverts it, and the validator fails first; change the canonical copy.
- **A checker that exits 0 when its folder is missing, or SKIPs its own target.** A typo then turns the gate green; exit 2, and SKIP only a file another skill creates.
- **`walk(root, { ignore: REPO_SCAN_IGNORES })`, a constant built from it, or a hand-rolled `readdir` loop for a repo scan.** It descends into installed skills and fails on their planted fixtures; use `walkRepo()`, and mark a deliberately wider scan `// repo-scan-walk: deliberate (<why>)`.
- **App facts (screen ids, budgets, folder names) written into a checker.** The checker then fits one app; read them from `contracts/<name>.json` and ship its template.
- **`xcrun simctl boot booted`, `adb shell` without `-s`, `maestro test` without `--device`.** Several sessions share one machine; name the device every time.
- **A full-copy fixture per case.** Hundreds of near-identical trees blow the fixture budget and hide what each case plants; write a `mutation.json` on one base.
- **An undated "works with SDK 57".** Nobody can tell when it stopped being true; date it and give the command that re-checks it.
- **Writing the skill straight into `.claude/skills/`.** Every write there asks the developer; author in `skills/` and load it as a plugin or link it.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/authoring-standard.md](references/authoring-standard.md) | The whole standard: placement, self-containment, anatomy, frontmatter, section order, templates, quality bar, every validator and check-skill rule | Workflow step 2, before writing any skill file |
| [references/descriptions-and-routing.md](references/descriptions-and-routing.md) | The description formula, good and bad examples, keeping a set apart, routing evals offline and live | Workflow steps 1, 5 and 7 |
| [references/writing-scripts.md](references/writing-scripts.md) | The script contract, a complete checker, the check-lib API, layout, contracts, repo scans, devices, packages | Workflow step 4 |
| [references/self-tests-and-fixtures.md](references/self-tests-and-fixtures.md) | runSelftest, case kinds, the overlay format (SUITE.json, mutation.json ops, DELETE.txt), hygiene and budget | Workflow step 4, and when a fixture goes stale |
| [references/library-round.md](references/library-round.md) | This skill's commands in order, a skill library's own round (sync, all self-tests, catalogue), the development loop, settings | Workflow step 8 |
| [references/how-skills-load.md](references/how-skills-load.md) | Discovery, parsing, listing budget, invocation, compaction, permissions, diagnostics, pitfalls by symptom | Workflow step 9, and when a rule needs its reason |
| [examples/new-skill-walkthrough.md](examples/new-skill-walkthrough.md) | A new skill from scaffold to PASS, and a rule added to an existing checker | Workflow step 2 |
| `templates/contracts/routing-evals.json` | The repo's routing evals: prompts and the skill each should load, seeded with placeholders to replace | Workflow step 5 |
| `templates/contracts/routing-evals.schema.json` | JSON Schema of the routing evals contract | Workflow step 5, when editing the evals |
| `assets/scaffold/` | What new-skill.mjs copies: `SKILL.md.tmpl`, a reference, `check-rules.mjs`, its self-test, overlay fixtures, `assets/shared.json` | Workflow step 2 (through the script) |
| `assets/standard.json` | The standard's constants (description cap, sections, allowed keys, reserved names, ban lists, budgets, device rules) | When a project tightens the standard (`--standard <file>`) |
| `scripts/new-skill.mjs` | Creates a skill from the scaffold; refuses bad, reserved or taken names | Workflow step 2 |
| `scripts/validate-skill.mjs` | The standard's checker for one skill, a skills folder or a repo | Workflow step 6 and the definition of done |
| `scripts/check-skill.mjs` | Checks one skill is finished (boundaries, reasons, used files, placeholders, template headers, self-test coverage, a bad case per rule, EXPECT ids, SKIP lines, contracts, deprecated helpers, repo scans) | Workflow step 6 and the definition of done |
| `scripts/check-skill-set.mjs` | Checks the set: overlapping or duplicate descriptions, hand-offs, listing budget (scaled by the repo's `skillListingBudgetFraction`), average length, index coverage | Workflow step 7 |
| `scripts/check-routing.mjs` | Routing evals, offline ranking or live with Claude Code; `--prompt` alone prints the ranking | Workflow steps 1 and 7 |
| `scripts/lib/skill-standard.mjs` | The validator's rule engine | When changing a validator rule |
| `scripts/lib/frontmatter.mjs` | The strict one-line YAML subset parser | Never by hand |
| `scripts/lib/skill-md.mjs` | SKILL.md reader and path resolution used by the checkers | Never by hand |
| `scripts/lib/router.mjs` | The offline ranking used by check-routing | When tuning the offline router |
| `scripts/lib/live-route.mjs` | Runs `claude -p`, reads the session's skill list and the first tool call | Never by hand |
| `scripts/selftest.mjs` | Proves every script passes its good case and catches every planted bug | After changing a script, the scaffold or a fixture |
| `scripts/check-lib.mjs` | Shared script helper, synced (do not edit here) | Never by hand |
| `assets/shared.json` | Declares the shared files this skill copies in | When adding a shared file |
| `tests/fixtures/` | Overlay cases: sample skills, skill sets, eval files, scaffold runs | When adding a rule |

## Related skills

- `troubleshooting-playbook` - failures in the app or its tooling rather than in a skill.
- `quality-gates` - the repo's own gates and hooks, which may run this skill's checkers.
- `git-commits-and-reporting` - committing a skill change and reporting it.
- `react-native-conventions-index` - the index skill whose table must name every skill.
