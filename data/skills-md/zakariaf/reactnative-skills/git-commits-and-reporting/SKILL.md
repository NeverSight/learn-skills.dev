---
name: git-commits-and-reporting
description: Writes and checks Conventional Commits, Gate-Change trailers, release tags, evidence reports and stop-and-ask requests. Use when committing, tagging, reporting a slice or release, or blocked on a person. Not for gates (quality-gates).
---

# Git commits and reporting

Every change reaches the reviewer twice: as a commit history anyone can search, and as a short plain-language message they actually read before the code. This skill makes both exact: Conventional Commits with the right trailers, a commit-msg hook and a checker that share one rule set, monotonic release tags, an evidence report whose numbers come from named files, and one clear question when something needs a person. Three scripts check the messages, the tags and the reports before anything is committed or sent.

## Rules that must hold

1. **Headers are Conventional Commits: `<type>(<scope>): <subject>`**, at most 72 characters, imperative, lowercase start, no trailing period. The scope is a folder under `src/features/` or `src/` (`tasks`, `ui`, `data`), a fixed scope (`repo`, `deps`, `docs`, `ci`, `tooling`, `e2e`, `release`, `skills`) or an `extraScopes` entry of `contracts/commits.json`; when multi-package, a workspace folder. `!` only for a change that breaks persisted data or a public contract. The history is searched by scope, and the commit-msg hook rejects anything else.
2. **One behaviour per commit, its tests and code together**, with a body that says why. When `contracts/commits.json` sets `requirementRef`, a `feat` or `fix` outside the exempt scopes also names the requirement it serves (`TASK-12`, `#31`, `spec 4.2`). The history is the proof that each behaviour was built test-first.
3. **Trailers sit in the last paragraph, and `Gate-Change:` is exact.** `Gate-Change: <reason>` appears exactly when a changed file matches `gatedPaths` in `quality-gates.json` (gate configs only after the reviewer agreed; goldens, baselines, vectors and frozen fixtures only on purpose), and never otherwise. `Spec-Change: <requirement> <what changed>` only when a test expectation changed because the requirement changed, never for "the test was wrong". Reasons are at least 10 characters. Keep any `Co-Authored-By:` line the session asks for. Git reads trailers only there, and `git log --grep '^Gate-Change:'` must list every gate change and nothing else.
4. **Commit the checked file, with comments stripped:** `git commit --cleanup=strip -F reports/commit-message.txt` after `check-commits.mjs` passes. Plain `-F` stores the template's `#` hint lines in the history.
5. **The hook and the checker are one rule set.** `scripts/git/commit-message-rules.ts` (the commit-msg hook) and `check-commits.mjs` give the same 18 rule ids, and both test suites run `scripts/git/commit-message-samples.json`. A rule changes in both and in the sample list in one commit, so a message the hook accepts never fails the checker later.
6. **Never bypass or rewrite:** no `--no-verify`, no `LEFTHOOK=0`, no amend, rebase or force-push of pushed commits. A failing hook means the commit is not ready.
7. **Nothing outward-facing without the developer's word in this session:** no push, no tag push, no store upload (`eas submit`, Transporter, the Play API), no App Store Connect or Play Console change, no submission for review, no OTA update to a production channel. These cannot be taken back.
8. **Tags come only from the release step, after a successful upload, and are annotated** (`git tag -a v1.4.0+ios.14 -m "App Store build 14"`, so the tag check can read when each was made): `vX.Y.Z+ios.<n>` and `vX.Y.Z+android.<n>` on both lanes (EAS and local; an app that already tags a shared `vX.Y.Z+<build>` keeps it), then `vX.Y.Z` when the reviewer says "ship". Never move, delete or reuse a tag; build numbers only go up (Play refuses a lower `versionCode`, App Store Connect a reused build number). When multi-package, tags start with the app's folder: `<app>/vX.Y.Z+ios.<n>`.
9. **Every finished slice and release ends with the evidence report:** the outcome first in users' words (at most 240 characters and 2 sentences), an `Evidence:` line, numbers copied from named files (never from memory), at most one request with its default, at most five things to look at, an honest "Not tested or not verified" list, technical detail last. The reviewer reads this before any code.
10. **Changes that are easy to miss get their own block; human checks are listed, never waited for.** Goldens and baselines changed on purpose name the file and their Gate-Change commit; texts changed name every locale of the app and which drafts go to a native-language review. On-device checks and language reviews go under "Human checks (not blocking)". A rehearsal, a dry run or a placeholder FAIL is never cited as evidence.
11. **Stop and ask in the listed situations** ([references/stop-and-ask.md](references/stop-and-ask.md)): one message, one request answerable in a word, how long it takes, the default that applies meanwhile; then keep working on anything else. Release stops (signing, agreements, 401/403, a missing app record, a failed processing state) are never retried.
12. **Never read, print, copy or commit a secret:** store API keys (`.p8`, a Play service-account JSON), keystores and certificates, provisioning profiles, tokens, `.env` files, passwords. If a task seems to need one, ask.

## Workflow

1. **Install the hook's rules once** (the commit-msg job of `quality-gates` runs `node scripts/git/check-commit-message.ts {1}`): copy [templates/scripts/git/](templates/scripts/git/) to `scripts/git/` (it imports `scripts/quality/gated-paths.ts` from quality-gates) and run `npx jest scripts/git`. Copy [templates/contracts/commits.json](templates/contracts/commits.json) to `contracts/commits.json` only to change the scope folders, add scopes or switch the requirement rule on; the defaults need no file. Read [references/commit-format.md](references/commit-format.md) before the first commit of a session.
2. **Stage exactly one slice.** `git status` and `git diff --cached --stat`: one behaviour, its tests and code, and the docs it changes. Split unrelated changes into their own commits.
3. **Write the message into a file** from [templates/reports/commit-message.txt](templates/reports/commit-message.txt), for example `reports/commit-message.txt` (`reports/` is git-ignored). Replace every `__PLACEHOLDER__`; delete the trailer lines that do not apply. [examples/commit-messages.md](examples/commit-messages.md) shows good and bad messages.
4. **Check it against the staged files:** `node ${CLAUDE_SKILL_DIR}/scripts/check-commits.mjs . --message reports/commit-message.txt --staged`. Fix every `FAIL` line and rerun until `RESULT: PASS`, then `git commit --cleanup=strip -F reports/commit-message.txt`.
5. **Check the session's history** before reporting: `node ${CLAUDE_SKILL_DIR}/scripts/check-commits.mjs . --range <base>..HEAD` (`<base>` = `git rev-parse --short HEAD` noted at the start of the session). A bad unpushed commit of this session (the last one only) is reworded with `git reset --soft HEAD~1`, then steps 3-4 again (`git commit --cleanup=strip -F reports/commit-message.txt`), so the hook sees every file of the commit; a pushed one stays, and the report says so.
6. **Write the evidence report.** Read [references/evidence-messages.md](references/evidence-messages.md). Copy [templates/reports/evidence-slice.md](templates/reports/evidence-slice.md) or [templates/reports/evidence-release.md](templates/reports/evidence-release.md) to `reports/evidence-<YYYY-MM-DD>-<slug>.md` and fill it only from the evidence files and the Jest summary. When the work changed a golden, a baseline or a user-visible text, paste the matching block of [templates/reports/report-blocks.md](templates/reports/report-blocks.md) above "Human checks". Compare with [examples/slice-evidence.md](examples/slice-evidence.md), [examples/release-evidence.md](examples/release-evidence.md) and [examples/baseline-and-text-changes.md](examples/baseline-and-text-changes.md).
7. **Check the report:** `node ${CLAUDE_SKILL_DIR}/scripts/check-report.mjs . --report reports/evidence-<...>.md`. Fix and rerun until `RESULT: PASS`, then put the report in the final message (the red run and the commands stay under "Details"). An app with other release checks or human checks records them in `contracts/reporting.json` ([templates/contracts/reporting.json](templates/contracts/reporting.json)).
8. **When something needs a person,** read [references/stop-and-ask.md](references/stop-and-ask.md), fill [templates/reports/request.md](templates/reports/request.md) (a human step or a requirement question) or [templates/reports/release-stop.md](templates/reports/release-stop.md) (a release stopped), check it with `node ${CLAUDE_SKILL_DIR}/scripts/check-report.mjs . --report reports/request.md --kind request` ([examples/requests.md](examples/requests.md) has one of each), send it, and continue with work that does not depend on the answer.
9. **After a store upload or a "ship",** read [references/tags-and-releases.md](references/tags-and-releases.md), create the tag the release step names, and run `node ${CLAUDE_SKILL_DIR}/scripts/check-tags.mjs .` (add `--match 'v*'` only when the repo also tags other things on purpose). Push tags only when the developer has said so in this session.
10. **At the end of every session:** commit the finished slices (steps 2-5) and write the report (steps 6-7). If a gate still fails, report the failing gate and what was tried instead of working around it.

## Definition of done

- [ ] `scripts/git/` holds the seven files of [templates/scripts/git/](templates/scripts/git/) and `npx jest scripts/git` passes.
- [ ] Each new commit holds one behaviour with its tests; its body says why (and names the requirement when the contract asks).
- [ ] `Gate-Change:` appears exactly on the commits that touch a gated path; `Spec-Change:` only where the requirement changed.
- [ ] No hook was bypassed; nothing was pushed, tagged, uploaded, submitted or published without the developer's word in this session.
- [ ] The evidence report takes every number from a named file, lists what was not verified, names every golden or baseline changed on purpose (with its Gate-Change commit) and every changed text (every locale, which drafts go to review), lists the human checks without waiting for them, and cites no rehearsal or dry run as evidence.
- [ ] Every request carries one action, how long it takes and a default; tags (after a release) pass the tag check.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-commits.mjs . --range <base>..HEAD` prints `RESULT: PASS`
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-report.mjs . --report reports/<report>.md` prints `RESULT: PASS`
- [ ] After a release: `node ${CLAUDE_SKILL_DIR}/scripts/check-tags.mjs .` prints `RESULT: PASS`

The checkers print no SKIP lines. `check-commits.mjs` without a `quality-gates.json` uses the canonical gated paths it ships; `check-report.mjs` without `contracts/reporting.json` uses the defaults.

## Anti-patterns

- **`fix: stuff` or `Updated files.`** The history becomes unsearchable; say what changes for the user or the code, with a scope.
- **One commit for "drafts, repeats and the new list header".** Three behaviours, three commits; otherwise nobody can see that each was built test-first.
- **`Gate-Change: update` on a commit that also relaxed a lint rule.** A gate change needs the reviewer's agreement first and a reason that says why.
- **`Gate-Change:` on a commit that touched no gated file.** It pollutes the one list of gate changes; the checker fails it.
- **`Spec-Change: the test was wrong`.** That is editing a test to pass; fix the code or ask.
- **Rewording a commit with `git commit --amend` or a rebase reword.** The hook then compares against the commit being amended and cannot see its files, so a correct `Gate-Change:` fails as unneeded; use `git reset --soft HEAD~1` and a fresh commit.
- **`git commit -F msg.txt` with the template's hint lines still in it.** The `#` lines land in the history; use `--cleanup=strip`.
- **Changing the hook's rules without the checker (or the reverse).** The two drift and a commit passes one and fails the other; change both and the sample list together.
- **"All tests green, coverage great!"** Numbers come from files, with the file named: "Tests: 214/214 pass (unit 192, golden 22), random seed 48213".
- **Five questions in one message.** Ask the most blocking one with its default; the rest can wait.
- **"Waiting for the Arabic review before the release."** Language reviews and on-device checks are human checks: list them and keep going.
- **Citing a `--rehearsal` or `--dry-run` result under Checks.** It proves nothing about the release; it belongs under "Not tested or not verified".
- **Retrying the upload after a 401, a 403 or `errSecInternalComponent`.** It needs a person or a credential; retries can lock an account or burn build numbers.
- **Pushing "because the work is done".** Pushing is outward-facing until the developer says otherwise.
- **Tagging by hand, or reusing `v1.4.0+14` for a rebuilt binary.** A new build gets a new build number and a new upload tag.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/commit-format.md](references/commit-format.md) | Header, types, scopes, body, trailers, gated paths, slices, branches, the hook and the checker, good and bad headers, multi-package scopes | Workflow step 1, first commit of a session |
| [references/evidence-messages.md](references/evidence-messages.md) | The reporting rules, the evidence shape, slice and release form, the change blocks, human checks, where each number comes from, honest limits, plain words, `contracts/reporting.json` | Workflow steps 6-7 |
| [references/stop-and-ask.md](references/stop-and-ask.md) | When to stop, the human steps of an app's life (stores, credentials, reviews), release stops on iOS and Android, how to write the message | Workflow step 8, and whenever a step needs a person |
| [references/tags-and-releases.md](references/tags-and-releases.md) | Upload and release tags, build numbers (EAS remote and the local lane), release commits, OTA updates, pushing, multi-package prefixes | Workflow step 9 |
| [templates/scripts/git/check-commit-message.ts](templates/scripts/git/check-commit-message.ts) | `scripts/git/check-commit-message.ts`: the commit-msg hook entry (lefthook runs it) | Workflow step 1 |
| [templates/scripts/git/commit-message-rules.ts](templates/scripts/git/commit-message-rules.ts) | `scripts/git/commit-message-rules.ts`: the header, body and placeholder rules | Workflow step 1; when a rule changes |
| [templates/scripts/git/commit-trailer-rules.ts](templates/scripts/git/commit-trailer-rules.ts) | `scripts/git/commit-trailer-rules.ts`: trailer placement, reasons, Spec-Change, Gate-Change against the gated paths | Workflow step 1; when a rule changes |
| [templates/scripts/git/commit-config.ts](templates/scripts/git/commit-config.ts) | `scripts/git/commit-config.ts`: scopes, gated paths and the requirement rule from the repo | Workflow step 1 |
| [templates/scripts/git/requirement-ref.json](templates/scripts/git/requirement-ref.json) | `scripts/git/requirement-ref.json`: the default requirement reference, the one copy the hook, `check-commits.mjs` and tdd-workflow's history check read | When the default reference pattern is in question (change it only here) |
| [templates/scripts/git/commit-message-rules.test.ts](templates/scripts/git/commit-message-rules.test.ts) | `scripts/git/commit-message-rules.test.ts`: runs the shared samples and the config through Jest | Workflow step 1 |
| [templates/scripts/git/commit-message-samples.json](templates/scripts/git/commit-message-samples.json) | `scripts/git/commit-message-samples.json`: the sample list both rule sets must judge alike | When a rule changes (add its sample) |
| [templates/contracts/commits.json](templates/contracts/commits.json) | `contracts/commits.json`: scope folders, extra scopes, the requirement rule (optional) | Workflow step 1, to change a default |
| [templates/contracts/commits.schema.json](templates/contracts/commits.schema.json) | Its JSON schema | With the contract |
| [templates/contracts/reporting.json](templates/contracts/reporting.json) | `contracts/reporting.json`: locales, required checks, human checks, non-evidence markers (optional) | Workflow step 7, to change a default |
| [templates/contracts/reporting.schema.json](templates/contracts/reporting.schema.json) | Its JSON schema | With the contract |
| [templates/reports/commit-message.txt](templates/reports/commit-message.txt) | Commit message with placeholders and `#` hints | Workflow step 3 |
| [templates/reports/evidence-slice.md](templates/reports/evidence-slice.md) | Evidence report, slice form | Workflow step 6 |
| [templates/reports/evidence-release.md](templates/reports/evidence-release.md) | Evidence report, release form | Workflow step 6 |
| [templates/reports/report-blocks.md](templates/reports/report-blocks.md) | The two optional blocks: goldens and baselines changed on purpose, texts changed in every locale | Workflow step 6, when a golden, baseline or text changed |
| [templates/reports/request.md](templates/reports/request.md) | One request: a human step or a requirement question with options | Workflow step 8 |
| [templates/reports/release-stop.md](templates/reports/release-stop.md) | The message when a release step stops | Workflow step 8 |
| [examples/commit-messages.md](examples/commit-messages.md) | Good messages and bad ones with the rule each breaks | Workflow step 3 |
| [examples/slice-evidence.md](examples/slice-evidence.md) | A complete slice report | Workflow step 6 |
| [examples/release-evidence.md](examples/release-evidence.md) | A complete release report (iOS and Android) | Workflow step 6, for a release |
| [examples/baseline-and-text-changes.md](examples/baseline-and-text-changes.md) | A slice report with both change blocks | Workflow step 6, with the change blocks |
| [examples/requests.md](examples/requests.md) | A human-step request, a requirement question and a release stop | Workflow step 8 |
| `scripts/check-commits.mjs` | Checks a planned message (`--message` with `--staged` or `--files`), history (`--range`, `--log`) or the shared sample list (`--samples`): the 18 hook rules plus `comment-line` (history) and `sample-mismatch` | Workflow steps 4-5 and the definition of done |
| `scripts/check-report.mjs` | Checks an evidence report (`--kind slice` or `release`) or a request (`--kind request`) against the reporting rules | Workflow steps 7-8 and the definition of done |
| `scripts/check-tags.mjs` | Checks tag forms, the app prefix, an upload tag behind every release tag, one build-number scheme, build numbers that only go up (the repo's tags or `--list <file>`; `--match <glob>` limits it to release tags) | Workflow step 9 |
| `scripts/selftest.mjs` | Proves the three checkers pass good fixtures, catch every planted bug and judge the shared sample list as the hook's test does | After changing a checker, a template or an example |
| `scripts/check-lib.mjs` | Shared script helper, synced from the library (do not edit here) | Never by hand |
| `assets/quality-gates.json` | The canonical `quality-gates.json` (synced from quality-gates): the gated paths used when the repo has none | When a gated path is in question |
| `assets/shared.json` | Declares the synced files: `check-lib.mjs`, `templates/scripts/git/` (canonical here, owned by this skill), `assets/quality-gates.json` | When adding a shared file |
| `tests/fixtures/` | Overlay suites: commit logs captured from throwaway repos, message files, the sample list (base: the shipped template), tag lists, reports and requests | When adding a rule to a checker (add a sample for a commit rule too) |

## Related skills

- `quality-gates` - the commit-msg job, `quality-gates.json` and its gated paths, `check:fast` and `verify`.
- `tdd-workflow` - how each slice is built test-first before it is committed.
- `spec-traceability` - the requirement IDs that commit bodies, reports and questions quote.
- `golden-and-snapshot-tests` - when a golden may change, and the tolerance-raise trailer wording.
- `eas-build-and-submit` - the release step that uploads builds and reports their build numbers.
- `ios-release-testflight` and `android-release-play` - the local release lanes, signing and store stops.
- `ota-updates` - publishing updates, an outward-facing action.
- `i18n-strings-and-catalogs` - the app's locales and the review of translated drafts.
- `design-visual-parity` - design baselines and the "Design match" line.
