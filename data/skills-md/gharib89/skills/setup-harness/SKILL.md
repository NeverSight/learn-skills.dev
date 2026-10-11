---
name: setup-harness
description: "Set up this repo's agent harness for Claude Code: one check entry point (scripts/check.sh), a pre-commit runner, the linters, formatters, typecheckers and tests it runs, hooks that run them after every edit and at every turn end, vendored language servers proven by a real LSP hover, and a cloud setup that installs them in every Claude Code on the web session, proven in a real one; each third-party tool pinned and passed through an install check. Independent of Ship; run it before /setup-skills. Re-run any time for a gap report that proposes only what is missing, broken or behind, keeping the repo's own additions and standing choices."
disable-model-invocation: true
metadata:
  version: 0.10.3
  harness-schema: 3
---

# Setup harness

Give every Claude Code session in this repo a fast, measured way to check its own work: `scripts/check.sh` answers "is this change good" at three rungs, Claude Code hooks run the fast rungs on every edit and every stop, and the pre-commit runner holds the commit. The run is explore, present, confirm, write, prove. Nothing is written before the human confirms it as a diff, and nothing third-party is installed before it passes the install check.

**Paths are contracts.** `scripts/check.sh`, `.claude/hooks/check-hook.sh`, `.claude/hooks/cloud-setup.sh` and `docs/agents/harness.md` are read by hooks and by a re-run, and `setup-skills` is to read the profile; write them at exactly those paths. Configuration is committed at project scope (`.claude/settings.json`, `.claude/hooks/`, the runner config); anything machine-specific goes to `.claude/settings.local.json`, and the report names it as such.

## Process

### 1. Preconditions: instruct and stop

On any failure print the exact command, then "then rerun `/setup-harness`", and stop.

1. **A git repo with tracked files**, on GitHub or Azure DevOps (`git remote get-url origin`). `curl` and `python3` on `PATH`: this skill's `scripts/pick-version.sh` needs both.
2. **A clean working tree** (`git status --porcelain` empty; else `git stash -u`).
3. **Claude Code floor.** Skip this item entirely when `CLAUDE_CODE_REMOTE=true`. Read `claude --version`. Below the `Floor:` of [templates/harness-profile.md](templates/harness-profile.md), write nothing under `.claude/` in this run, print the upgrade command for the install method (`claude update`; Homebrew `brew upgrade claude-code`; npm `npm install -g @anthropic-ai/claude-code@latest`), and stop.
4. **Warn, do not stop**, in the report's header:
   - `claude doctor </dev/null` reports `Auto-updates:` other than `enabled`: name the switch doctor names (`DISABLE_AUTOUPDATER`, `DISABLE_UPDATES`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`) and the install method's own update command, since Homebrew, WinGet and apt installs do not self-update.
   - The installed version trails its channel's latest: `npm view @anthropic-ai/claude-code dist-tags --json` (`latest` and `stable`); name the channel, both versions and the update command.

### 2. The profile

Read `docs/agents/harness.md` if it exists; a repo without one is a first run, and a repo with one is a **re-run**, whose report is the gap report of [reference/gap-report.md](reference/gap-report.md): read it now.

- `Schema:` equal to this skill's `metadata.harness-schema`: read its choices (`## Budgets` overrides, the `## Cloud` verdict and `Allowlist:`, `Excluded:`, `Root:`, `Local-only:` and `Declined:` lines) and honour them without re-asking; removed or stale lines re-open per gap-report.md `## Deleted pieces and standing choices`. A `Proof: <sha>` stands or is stale per [reference/cloud.md](reference/cloud.md) `## Recording the proof`.
- `Schema:` behind: read and honour its choices as on an equal schema; the migration is the first, undroppable row of the confirm step, applied entry by entry from [harness-schema.md](harness-schema.md), `Schema:` rewritten last.
- `Schema:` ahead: stop. That repo was set up by a newer setup-harness; print `npx skills add Gharib89/skills --skill setup-harness --agent claude-code -y` and "then rerun `/setup-harness`".

### 3. Explore

Read-only. Collect, then present everything at once in step 4.

1. **Stacks, members and file kinds** per [reference/detection.md](reference/detection.md): read every `catalog/*.md` `## Signals` block first, then scan tracked files only. Read [catalog/README.md](catalog/README.md) once, then each detected entry's file.
2. **Tools per member and role** from the evidence, applying the catalog's yielding rules: the repo's tools are kept and only their gaps filled; a default fills only a role with no evidence.
3. **Surfaces** per [reference/surfaces.md](reference/surfaces.md): each with its member and evidence paths, the behaviour tools it proposes, and whether the repo has a `.claude/skills/run-*/`.
4. **The pre-commit runner** git invokes, per [reference/runner.md](reference/runner.md), and any config that is present but not wired.
5. **Existing harness pieces**: `scripts/check.sh`, `.claude/hooks/`, the `hooks` in `.claude/settings.json` and `.claude/settings.local.json`, and a `### Harness` block in `CLAUDE.md`. An existing harness file is the repo's own evidence: compare it with its current template by what it says, keep what it adds and propose only what it lacks ([reference/gap-report.md](reference/gap-report.md) `## Files the skill wrote`).
6. **The install-check rows**: every package, hook repo, binary or vendored plugin the plan adds or re-pins, per [reference/install-check.md](reference/install-check.md), with its version picked by this skill's `scripts/pick-version.sh` and its tier, publisher, provenance and glue read now; a language server's per [reference/language-servers.md](reference/language-servers.md) `## Vendoring` step 1, at the SHA it records. On every run, first or re-run, also every pin already in the repo for a tool the harness runs, per gap-report.md `## Pins`.
7. **On a re-run, time the rungs** now, per gap-report.md `## Timing on a re-run`, so the report carries the budgets and any over-budget Offer.
8. **The cloud** per [reference/cloud.md](reference/cloud.md): the verdict's evidence, need by need; an existing cloud `SessionStart` script; the cloud setup's steps, each rung's cloud label, and the static host check over those steps. `origin` on `dev.azure.com` or `visualstudio.com` makes the proof's route Azure DevOps and changes nothing else.

### 4. Present

On a re-run, the gap report in the layout gap-report.md `## The report` gives, each gap under its one disposition. Otherwise one message, in this order:

1. **Header**: skill version, the profile's `Schema:` (and what it migrates to), the Claude Code floor against the installed version (or `skipped: cloud session`), the step-1 warnings, and the surfaces with their evidence paths.
2. **Detection** as detection.md's report lists it.
3. **Questions**, numbered, each with a recommendation: every new fixture tree and every new candidate root ([reference/detection.md](reference/detection.md)), asking excluded or read, and root or ignored, each with the human's reason, every role with two tools and no caller, a runner choice where more than one config has no shim, the cloud verdict with its evidence, each blocked host a step needs (does the environment's Custom allowlist admit it?), the run recipe Offer where surfaces.md makes one, and each question a catalog `Traps:` line asks (js-ts Playwright Test's `webServer.command`).
4. **The install-check table**, glue in full after it, then **Found, not installed** with each refusal's reason.
5. **The writes, as diffs**: runner config additions, the manifest line of each pinned dev dependency, each vendored language server plugin with its `enabledPlugins` line, config files a catalog `Constraints:` or `Traps:` line writes, the `scripts/check.sh` configuration block, `.claude/hooks/check-hook.sh`, the cloud setup's `STEPS` block (or the diff to the repo's own cloud script), the `.claude/settings.json` hook entries, `docs/agents/harness.md` and the `CLAUDE.md` block.

### 5. Confirm

One approval covers the batch: the human answers the questions and may drop rows or writes by number. A candidate root's answer is recorded with the human's reason, a root as `Root: <manifest>: <reason>` and an ignore as `Declined: <manifest> as a root: <reason>`, the form a root with a lockfile takes too when the human drops its `TURN_ROWS` row with a reason; a fixture tree's as `Excluded: <path prefix>: <reason>` or `Declined: <path prefix> as excluded: <reason>`. An answer given without a reason is asked once more before the writes, and one still without a reason acts in this run but is not recorded, so its question is new next run. A row dropped with a reason and an answer keeping a unit off the version the install check picks are each recorded in the profile in the same batch, as `Declined: <what>: <reason>` (`Declined: <unit> <picked version>: <reason>` for the last); a row dropped without a reason is proposed again next run. Re-present only what an answer changed. On a re-run the questions are the gap report's Offers, steps 6 to 8 act on the approved rows and the profile lines the answers record, and step 6's timing is the re-timing of gap-report.md `## Timing on a re-run`.

### 6. Write

In this order, each step's failure stopping the run with its output:

1. **Installs**: each approved unit at its exact pin (a language server whose pin rides in its launch installs nothing here, [reference/language-servers.md](reference/language-servers.md) `## Vendoring` step 4), then the repo's own deps from its lockfile (`uv sync --frozen`, `pnpm install --frozen-lockfile`).
2. **The runner**: its config additions, its install command when git does not yet invoke it (`prek install --allow-missing-config`, [reference/runner.md](reference/runner.md)), then `prek run --all-files` (or the runner's equivalent). A failure here is the repo's code on a tool new to it: report the findings and ask whether to fix them in this run, leave them for the human, or drop the tool; on leave or drop, `git restore` the files its fixes rewrote. Never weaken the tool's config to pass.
3. **`scripts/check.sh`** from [templates/check.sh](templates/check.sh), configuration block filled per [reference/check-ladder.md](reference/check-ladder.md).
4. **Time the rungs** before any hook exists, per check-ladder.md's timing section: each twice, cold reported, warm judged against its budget. A warm `edit` or `turn` over budget gets the narrow / demote / override offer now, and its hook waits until one is applied.
5. **Vendored language servers** per [reference/language-servers.md](reference/language-servers.md) `## Vendoring` steps 2 to 4, at the SHA Explore read.
6. **`.claude/hooks/check-hook.sh`** from [templates/check-hook.sh](templates/check-hook.sh) and the hook entries from [templates/settings-hooks.json](templates/settings-hooks.json), merged beside the repo's own, each `timeout` derived from its budget.
7. **The cloud setup**, cloud-first only, per [reference/cloud.md](reference/cloud.md) `## Writing the cloud setup`: `.claude/hooks/cloud-setup.sh` from [templates/cloud-setup.sh](templates/cloud-setup.sh) (chained after Ship's cloud bootstrap where an entry runs one), or the repo's own cloud script, when it is not that bootstrap, extended in place, and the `SessionStart` entry from [templates/settings-cloud.json](templates/settings-cloud.json).
8. **`docs/agents/harness.md`** from [templates/harness-profile.md](templates/harness-profile.md): `Floor:` and `Location:` as written, every budget `default` unless the human gave an override with a reason, `## Cloud` with the confirmed `Verdict:`, `Setup:` (the cloud setup's path, `None.` when local-only), the human's `Allowlist:`, and `Proof:` kept where step 2 found it standing, else `unproven`, `Local-only:` lines (never a language server's), one for each partial need the cloud verdict found, each MCR no, and each catalog `Local-only:` line a wired `FULL_ROWS` tool carries on a cloud-first repo, so every `LOCAL_ONLY` name has the line whose `<part>` is that name; then the `Excluded:`, `Root:` and `Declined:` lines from the confirm step. Then run `scripts/harness-profile-check.sh docs/agents/harness.md` from this skill's directory; a violation is fixed before continuing.
9. **The `CLAUDE.md` block** from [templates/harness-block.md](templates/harness-block.md), replacing an existing `### Harness` block rather than adding a second.

### 7. Prove

1. `git add --intent-to-add :/`, then `scripts/check.sh full` prints one JSON line and exits 0, or its failures are reported, each `<rung>: fail (<check>)`, as the repo's code or, where the failing content is what this run wrote, as this run's; then, pass or fail, `git reset --quiet`. The runner's `--all-files` checks only files git lists, so without the intent-to-add the files this run created (a new `CLAUDE.md`, `scripts/check.sh`, the hooks, the profile) go unchecked until the human's first commit.
2. **The language server proof**, local sessions only, per [reference/language-servers.md](reference/language-servers.md) `## The proof`: `/reload-plugins` asked for when this run wrote a plugin, then an `LSP` hover per wired language.
3. **The cloud proof**, cloud-first only, per [reference/cloud.md](reference/cloud.md) `## The proof`: the local double run, the static host check, then the commit, on GitHub the push the human approves, the printed `claude --cloud` command (on Azure DevOps the `git status` gate over the whole tree first, then `CCR_FORCE_BUNDLE=1`, nothing pushed), and the human's pasted answer, recorded as `Proof: <sha>` in a commit of the profile alone.

### 8. Report

1. The header from step 4.
2. What was written, one line per file, `.claude/settings.local.json` entries named machine-specific.
3. **Language servers**: one line per wired language from the proof, each `local-only`.
4. **Budgets**: one row per rung, cold, warm, budget, verdict (`within`, `over: narrowed`, `over: demoted to <rung>`, `over: override <N>s`, `not judged: fail (<check>)`, `not judged: unavailable (<check>)`, `not judged: contract` on a re-run). Then the **cloud** table: per rung its cloud label and cloud times, and the cloud setup's local double run.
5. **Not acted on**: unclaimed extensions and stacks, unwired tools, Found-not-installed units, `public API: no baseline (<member>)`, `<tool>: <root> not served`, anything "present, not wired".
6. **Standing choices**: every `Excluded:`, `Root:`, `Declined:`, `Local-only:` and override, `Allowlist:`, and the cloud state: `Proof: <sha>`, `cloud: unproven` with what is missing, or `cloud: n/a (local-only: <reason>)`.
7. **Next**: commit the harness files if the proof did not; hooks in `.claude/settings.json` load in new sessions, so start one (or review them in `/hooks`) before relying on them; then `/setup-skills` if the repo uses Ship.
