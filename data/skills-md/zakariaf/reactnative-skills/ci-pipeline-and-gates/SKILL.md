---
name: ci-pipeline-and-gates
description: Builds GitHub Actions CI for Expo apps - verify on every PR, SHA-pinned actions, pinned runners and Node, device lanes, manual EAS releases. Use when editing .github/workflows or CI fails. Not for local gates (quality-gates).
---

# CI pipeline and gates

CI repeats the local gate on GitHub's machines, adds the device lanes a laptop cannot run every
night, and starts store builds only when a person decides. Three workflows do it (`ci.yml`: `npm
run verify` on every pull request and push; `devices.yml`: Android emulator and iOS simulator lanes
nightly; `release.yml`: an EAS build by hand behind a protected environment), with every action
pinned to a commit SHA and every runner and tool pinned to a version. Two checkers prove it. Verified
on 2026-10-14 against the `ubuntu-24.04` and `macos-26` runner-image READMEs, actionlint 1.7.12, Expo
SDK 57, Node 26.4.0, Xcode 26.6 and eas-cli 24.10.0; the device jobs were not run on GitHub.

## Rules that must hold

1. **CI runs the local gate, byte for byte: `npm ci`, then `npm run verify`, on every pull request
   and every push to `main`** (no `paths`/`branches` filter on `pull_request`, no `if:` on the job
   or the two steps). No hand-written lint, test or build steps, no `npx jest` beside it,
   only npm scripts that exist; a job that sets `APP_VARIANT` sets `EXPO_PUBLIC_APP_VARIANT` to the
   same value. Why: the guardrail compares the scripts, not YAML copies; CI that checks something else
   passes what the pre-push hook would stop.
2. **Every runner and tool is pinned:** `runs-on: ubuntu-24.04` / `macos-26` (never `-latest`), Node
   from `.nvmrc` through `setup-node` `node-version-file`, JDK 17 where Gradle or Maestro runs, Xcode
   selected by version inside the repo's build script. Why: the Ubuntu image's npm 10.9 fails <!-- stack-pin-ignore: the runner image's npm, not the project's -->
   `engine-strict`, no image's Node is the one `.nvmrc` pins, and a moving label (`macos-latest`,
   `macos-latest-xlarge`) changes the build with no diff to review.
3. **Every action is pinned to a full 40-character commit SHA with a `# vX.Y.Z` comment, at least 7
   days old, and Dependabot proposes updates with `cooldown: default-days: 7`.** Why: a tag can be
   repointed to malicious code; the comment keeps the pin reviewable; the cooldown matches the npm
   release age.
4. **Least privilege, no untrusted code in privileged context:** top-level `permissions: contents:
   read`, `pull_request` (never `pull_request_target` or `workflow_run`), `actions/checkout` with
   `persist-credentials: false`, no `${{ }}` of contributor-controlled or secret context inside a
   `run:` script (pass it through `env:`). Why: these are the routes by which a pull request reaches
   a write token or runs as code.
5. **Secrets live only in jobs with a protected `environment:` (never in the workflow-level `env:`,
   never passed to a reusable workflow), and those jobs restore no cache.**
   Why: the environment's reviewers and branch rule protect the secret; a cache any branch can write
   would run next to it.
6. **Every workflow has a concurrency group and every job a `timeout-minutes` (at most 180); a
   release workflow never cancels in progress, and the merge gate cancels only pull request runs.**
   Why: stale runs waste minutes, a hung simulator burns six hours, a cancelled release leaves a
   half-made build, and a cancelled run on `main` leaves a merged commit unverified.
7. **A red step stays red:** no `continue-on-error`, `|| true`, `|| exit 0`, `set +e` or other `||`
   fallback after a gate command, no pipe after one (`| tee`) without pipefail, no `NPM_CONFIG_*` override, no weakening `npm ci` flag;
   `LEFTHOOK: '0'` is the one switch, set in every workflow that installs. Why: each turns a failing gate green or drops part of the `.npmrc`
   policy, silently.
8. **Caches are keyed on the file that pins their content and never hold `node_modules`.** npm
   downloads on `package-lock.json`, Gradle on `package-lock.json`, the Maestro zip on its installer.
   Why: a key without `hashFiles` never invalidates, and `npm ci` deletes `node_modules` anyway.
9. **Every device lane the app has a script for runs in CI on its own schedule:** Android
   (`build:android:emu`, `e2e:android`) on Linux with KVM, iOS (`build:ios:sim`, `e2e:ios`) on macOS,
   nightly and on demand; a lane not run is a decision with its reason in `contracts/ci.json`. Why:
   macOS arm64 runners cannot nest virtualization, and a lane nobody runs proves nothing.
10. **Workflows never touch a device or a licence directly:** no `maestro`, `adb`, `emulator`,
    `avdmanager`, `xcrun simctl`, `xcode-select` lines or device actions, no `sdkmanager --licenses`.
    Why: the repo's scripts create `<project>-<purpose>` devices and address them by id; accepting a
    licence is the developer's legal decision.
11. **Every gate and device job uploads its reports with `if: ${{ always() }}`** (or `!cancelled()`). Why: screenshots,
    junit files and coverage are the evidence, and they die with the runner.
12. **Release lanes start by hand:** `workflow_dispatch` (or a pushed tag) only, a protected
    environment, the EAS CLI installed as one exact version with `--min-release-age=7
    --ignore-scripts` (never `npx eas-cli`, never `eas-version: latest`), `--non-interactive`, and
    eas-build-and-submit's preflight first; no `eas submit` or `eas update` on a push, also not behind
    an npm script (`npm run release:eas`, `release:ios`, `release:android`). Why: a store build, a
    submission or an OTA update reaches people, so a person decides.
13. **A workflow is a gate.** `quality-gates.json` `gatedPaths` covers `.github/workflows/**` and
    `.github/dependabot.yml`, so a change carries a `Gate-Change:` trailer; pushing a workflow and
    starting a release run are the developer's calls. Why: weakening CI is the quietest way to weaken
    every gate at once.

## Workflow

1. **Know what the repo has:** `ls .github/workflows .github/dependabot.yml .nvmrc`, the
   `package.json` scripts, and whether quality-gates is adopted (`quality-gates.json`, `npm run
   verify`). Without `verify`, adopt quality-gates first: CI repeats a gate, it never invents one.
   Read [references/workflow-anatomy.md](references/workflow-anatomy.md) for what each workflow does
   and why there are three.
2. **Copy the templates** (line 1 of each names its repo path):

   | Template | Goes to | When |
   |---|---|---|
   | `templates/workflows/ci.yml` | `.github/workflows/ci.yml` | always |
   | `templates/dependabot.yml` | `.github/dependabot.yml` | always |
   | `templates/workflows/devices.yml` | `.github/workflows/devices.yml` | the app has a device script; delete a job whose lane the app does not have |
   | `templates/workflows/release.yml` | `.github/workflows/release.yml` | the app releases through EAS (eas-build-and-submit) |
   | `templates/contracts/ci.json` + `ci.schema.json` | `contracts/` | always (`laneOptOuts: {}` until the developer decides otherwise) |

   In an existing workflow, replace ad-hoc steps with the npm scripts instead of adding a fourth file.
   Another skill's checker reaches CI as an npm script in quality-gates' `verifyExtraSteps`, never as
   a step of its own; one that compares with the target branch needs `fetch-depth: 0`
   ([workflow-anatomy.md](references/workflow-anatomy.md), "Adding a skill's checker to CI").
3. **Pin and harden:** read [references/security-hardening.md](references/security-hardening.md);
   resolve any new action to a commit SHA of a release at least 7 days old
   (`git ls-remote --tags <repo> '<tag>' '<tag>^{}'`) and add the `# vX.Y.Z` comment.
4. **Device lanes:** read [references/device-lanes.md](references/device-lanes.md) before changing a
   runner, the Android packages, the JDK step or the cadence. A lane the app will not run in CI gets a
   `laneOptOuts` entry only after the developer agrees, with their reason.
5. **Release lane:** read [references/release-lane.md](references/release-lane.md); list the human
   setup (EAS token, the `production` environment with reviewers and branch rule) in the report. The
   agent never creates tokens, environments or branch rules.
6. **Gate the files:** check that `quality-gates.json` `gatedPaths` holds `.github/workflows/**` and
   `.github/dependabot.yml`; adding them is a quality-gates gate change (`Gate-Change:` trailer).
7. **Run the checks:** `node ${CLAUDE_SKILL_DIR}/scripts/check-workflows.mjs .` and
   `node ${CLAUDE_SKILL_DIR}/scripts/check-ci-lanes.mjs .` (repo root positional, never `--root`).
   Fix every `FAIL` line (each names the file, line, rule and fix; [references/checks.md](references/checks.md)
   explains every rule), rerun until both print `RESULT: PASS`. Then run actionlint from a pinned,
   checksum-verified binary (checks.md, "actionlint").
8. **Ask before pushing:** a workflow runs on GitHub's machines under the repository's name. When CI
   later fails, triage as in [examples/red-run-triage.md](examples/red-run-triage.md): same command,
   same Node, same files, then the uploaded reports; fix the cause, never the workflow's strictness.

**When multi-package:** the workflows stay at the repository root; `npm ci` and `npm run verify` run
there; device scripts run with `--workspace apps/<app>` (either side of the script name); pass
`--app-dir apps/<app>` to `check-ci-lanes.mjs` (a workspace command is looked up in that package, any
other in the root `package.json`); one device job per shipping app.

## Definition of done

- [ ] `ci.yml` runs `npm ci` then `npm run verify` on `pull_request` and on push to `main`, with no
      other gate commands; `dependabot.yml` updates `github-actions` with a 7-day cooldown.
- [ ] Every `uses:` is a 40-character SHA with a `# vX.Y.Z` comment; no `-latest` runner; Node from
      `.nvmrc`; JDK 17 in every Gradle or Maestro job.
- [ ] Each device script in `package.json` has a scheduled job on the right runner, or a
      `laneOptOuts` entry the developer agreed to.
- [ ] `release.yml` (if present) starts only by hand, in a protected environment, with the pinned EAS
      CLI and the preflight first.
- [ ] actionlint (pinned release) prints nothing; the human settings (environment, branch protection,
      required `verify` check) are listed in the report for the developer.
- [ ] Expected SKIP lines only, each until its owner skill is adopted: `SKIP ... [script-missing] npm
      script "<build:android:emu|e2e:android|e2e:ios|build:ios:sim>" not yet created (<owner> creates
      it)` and `SKIP .github/workflows/release.yml [script-missing] scripts/eas/release-preflight.ts not
      yet created (eas-build-and-submit creates it)`, and `SKIP quality-gates.json [workflows-gated]
      not yet created (quality-gates creates it)` until quality-gates is adopted. Once the templates are copied both checkers count
      what they read (`check-workflows: N files checked`, `check-ci-lanes: N workflows checked`);
      `NOT APPLICABLE` means `.github/workflows/` was never created, so the skill is not applied yet.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-workflows.mjs .` prints `RESULT: PASS`
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-ci-lanes.mjs .` prints `RESULT: PASS`

## Anti-patterns

- **`run: npx eslint . && npx tsc && npx jest` in the workflow.** It drifts from `verify` the day a
  gate changes, and the guardrail never sees it. Run `npm run verify`.
- **`uses: actions/checkout@v7`.** Pin the commit SHA with the release as a comment; let Dependabot
  move it.
- **`runs-on: macos-latest` for the Android emulator.** No nested virtualization on Apple silicon
  runners; the emulator never boots. Linux with KVM.
- **`continue-on-error: true` on the E2E job "while it is flaky".** The lane is then decoration. Fix
  the flow or the app; read the uploaded screenshots.
- **`npm install` in CI.** It can rewrite the lockfile and install unreviewed versions; `npm ci`.
- **`NPM_CONFIG_MIN_RELEASE_AGE: '0'` to get a fresh package installed.** Wait for the release age or
  add a dated exclude block (dependency-management).
- **`echo "${{ github.event.pull_request.title }}"` in a script** (or `"${{ env.TITLE }}"` after
  moving it to `env:`). A crafted title runs as code; pass it through `env:` and read `"$TITLE"`.
- **`pull_request_target` "so forks get the token".** That is exactly the attack; use
  `pull_request`.
- **`yes | sdkmanager --licenses`.** Accepting a licence is the developer's decision; the hosted
  images ship with them accepted.
- **`expo/expo-github-action` with `eas-version: latest`, or `npx eas-cli build` on every push to
  `main`.** An unpinned CLI building and spending credits without a decision; start releases by hand
  with the pinned CLI.
- **Caching `node_modules` or restoring the npm cache in the release job.** Wasted or poisoned;
  lockfile-keyed download caches in unprivileged jobs only.
- **Raising `timeout-minutes` until a hanging lane "passes".** Read the logs; the hang is the bug.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/workflow-anatomy.md](references/workflow-anatomy.md) | The three workflows line by line, the runners and their images, the pinned toolchain, caches, reports, adopting, when multi-package, what CI cannot prove | Workflow step 1 |
| [references/security-hardening.md](references/security-hardening.md) | SHA pins (with the verified pins), finding a SHA, Dependabot cooldown, permissions, `pull_request_target`, checkout credentials, script injection, environments, cache poisoning, the repository settings a human sets | Workflow step 3 |
| [references/device-lanes.md](references/device-lanes.md) | Android on Linux with KVM, the SDK packages and licences, iOS on macOS with the pinned Xcode, JDK 17, named devices, flaky lanes, failures | Workflow step 4, and when a device job fails |
| [references/release-lane.md](references/release-lane.md) | The manual EAS release job, the human setup, what never runs from CI, Expo's EAS Workflows, apps without EAS | Workflow step 5 |
| [references/checks.md](references/checks.md) | Every rule of both checkers with its reason, `contracts/ci.json`, expected SKIP lines, the YAML subset, actionlint, when multi-package | Workflow step 7, and when a check fails |
| [examples/red-run-triage.md](examples/red-run-triage.md) | A red CI run on a Tasks app traced to a case-only rename git did not record on macOS, and what was not done | When CI fails and local passes |
| `templates/workflows/ci.yml` | The merge gate: `npm ci` + `npm run verify` on pull requests and pushes | Workflow step 2 |
| `templates/workflows/devices.yml` | Nightly Android (Linux + KVM) and iOS (macOS) build and E2E lanes | Workflow step 2 |
| `templates/workflows/release.yml` | The manual EAS build behind the `production` environment | Workflow step 2 |
| `templates/dependabot.yml` | Weekly SHA-pin updates for actions with a 7-day cooldown | Workflow step 2 |
| `templates/contracts/ci.json` | The CI contract: `laneOptOuts`, the device lanes the developer decided not to run, with reasons | Workflow steps 2 and 4 |
| `templates/contracts/ci.schema.json` | The contract's JSON schema (lane names, a reason of at least 20 characters) | When editing the contract |
| `scripts/check-workflows.mjs` | Pins, runners, permissions, triggers, credentials, injection, secrets, concurrency, timeouts, soft fails, npm config, LEFTHOOK, caches, Dependabot (16 rules) | Workflow step 7 and the definition of done |
| `scripts/check-ci-lanes.mjs` | The verify gate, installs, ad-hoc commands, Node pin, scripts, device lanes and runners, JDK, raw device commands, licences, reports, release trigger, environment and CLI, variant pairs, gated paths, opt-outs (19 rules) | Workflow step 7 and the definition of done |
| `scripts/lib/workflow-yaml.mjs` | The zero-dependency YAML reader (lines and comments kept) | Read only to change the parser |
| `scripts/lib/workflows.mjs` | The workflow model both checkers share (triggers, jobs, steps, shell commands, lanes, owners) | Read only to change a rule |
| `scripts/selftest.mjs` | Proves both checkers on the templates and every planted bug | After changing a checker, a template or a fixture |
| `scripts/check-lib.mjs` | Shared script helper, synced from the library (do not edit here) | Never by hand |
| `assets/shared.json` | Declares the synced files | When adding a shared file |
| `tests/bases/app/` | The minimal app the suites start from (scripts, `.nvmrc`, gated paths, a preflight stub) | When adding a case |
| `tests/fixtures/` | Overlay cases: `good/`, one `bad-*` per rule, `pass-*` for SKIP and NOT APPLICABLE, `error-*` | When adding a rule |

## Related skills

- `quality-gates` - what `npm run verify` runs, `gatedPaths`, `LEFTHOOK` outside workflows, the never list.
- `dependency-management` - `.npmrc`, release age, install scripts, `check:deps`, Node and npm pins.
- `ios-simulator-build`, `android-emulator-build` - the build scripts the device lanes call.
- `e2e-maestro` - the E2E scripts, the Maestro installer and flake rules.
- `eas-build-and-submit` - `eas.json`, the release preflight, submitting a build.
- `ota-updates` - EAS Update channels; never published from a push.
- `app-variants-and-environment` - `APP_VARIANT` and `EXPO_PUBLIC_*` values in build jobs.
- `git-commits-and-reporting` - the `Gate-Change:` trailer and the report that cites the run.
- `troubleshooting-playbook` - tool failures behind a red job.
