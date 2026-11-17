---
name: update-skill
description: Thorough on-demand refresh of one skill in a skills repo - researches usage, upstream, and docs in parallel, gates twice for approval, bumps version, updates CHANGELOG, validates, commits, watches CI. Use to check a skill's freshness.
argument-hint: "[skill-name]"
metadata:
  version: "0.10.0"
  categories: "agents, automation"
  topics: "skill-maintenance, versioning, changelog, research, agent-skills"
  openclaw:
    homepage: https://github.com/tenequm/skills/tree/main/skills/update-skill
    emoji: "🔄"
  upstream: "keep-a-changelog@2.0.0"
---

# Update Skill

Run a thorough on-demand refresh of one skill in a skills repository. Two hard human-approval gates ensure no edits or commits happen without explicit confirmation.

The target skill is: $ARGUMENTS

If no argument was provided, run `ls ${CLAUDE_PROJECT_DIR}/skills/` and ask the user which to update. Stop until confirmed. Then verify `${CLAUDE_PROJECT_DIR}/skills/$ARGUMENTS/SKILL.md` exists; if not, list skills and ask again. Throughout this run, `<name>` refers to the resolved skill name.

## Operating rules

These rules apply across all phases:

- **GATE 1 stops before any edit.** Do NOT call Edit or Write until the user replies affirmatively to the GATE 1 banner.
- **GATE 2 stops before any commit or push.** Do NOT run `git commit` or `git push` until the user replies affirmatively to the GATE 2 banner.
- **Privacy scan is a hard blocker.** Skills in a public repo can publish on merge, so the run does not reach a commit while a Phase 6 leak finding is unresolved.
- **Sticky posture.** Once GATE 1 has been emitted, "report findings first" persists across follow-up rounds in the same session. If the user replies `changes` or asks for revisions, re-emit the gate after revising; never silently apply.
- **Non-resume.** If the session is interrupted between GATE 1 and GATE 2, re-run `/update-skill <name>` from scratch. There is no checkpoint or resume mechanism.
- **Duplicate triggers.** If a scheduled task or a repeated invocation fires while a run is holding at a gate, hold at the emitted gate and answer from the existing report - never redo research or re-apply edits.
- **No `--no-verify`, no `--amend`, no force-push** unless the user explicitly authorizes it for this run. Per the repo's CLAUDE.md or AGENTS.md.
- **Working directory.** Every path, every `just check`, and every working git command (`status`/`diff`/`add`/`commit`/`push`) in the phases below runs against `<workdir>` - the Phase 0 worktree. Use absolute paths under `<workdir>`; do not mix in the main checkout.
- **Scratch directory for toolchains.** Pick one scratch directory outside every checkout (the session scratchpad if the harness provides one, else `mktemp -d`) and name it in every subagent brief. Every build or toolchain command - `swift`, `xcodebuild`, `npm`, `cargo`, `uv`, `go` and the like, including `--help` probes and scratch packages - runs with that directory as its working directory. Subagents start in the main checkout, so a bare `swift build --help` leaves a `.build/` there.
- **No backticks in shell arguments.** Single-quote search patterns (`rg -n 'pattern' path`). In zsh and bash a backtick inside a double-quoted argument is command substitution, and one such `rg` pattern has printed the whole environment, secrets included, into a transcript.

## Phase 0 - Separate worktree

Run the whole update in a separate worktree on a new branch `chore/update-<name>`, so several skills can be updated in parallel. `<workdir>` is that worktree's absolute path. Keep it until the PR merges, then remove it and delete the branch.

## Phase 1 - Pre-flight read

Read every file in `skills/<name>/` end-to-end, in parallel:
- `skills/<name>/SKILL.md`
- All files under `skills/<name>/references/` (use Glob first to enumerate)
- `skills/<name>/CHANGELOG.md` (if present)

Capture state for the rest of the run:
- `metadata.version` (current)
- `metadata.upstream` (current; parse to `{name: version}` map; empty if absent)
- Topmost CHANGELOG entry date (if `CHANGELOG.md` exists; this is the "last verified" signal)
- `git log -1 --format=%cs -- skills/<name>/` date (last touch)
- `git status --porcelain` snapshot of `<workdir>` and of `${CLAUDE_PROJECT_DIR}` - the baseline for the Phase 6 hygiene check, so pre-existing user files are never flagged or removed
- A per-skill license file, only if the repo's linter or publish pipeline requires one (ClawHub does not - it licenses every skill MIT-0); if required and missing, queue a fix row in the Phase 3 report
- `bootstrap_needed` flag = true if `metadata.upstream` is missing OR `CHANGELOG.md` is missing - **unless the skill is upstreamless by nature** (it wraps no package, spec, or living doc - e.g. a workflow or writing skill like `polish`). For those, omitting `metadata.upstream` is correct, not a gap: derive `bootstrap_needed` from the missing `CHANGELOG.md` alone and skip the upstream-candidate proposal.

## Phase 2 - Parallel research

Dispatch the research subagents in a single message: one each for upstream and docs, plus the usage lanes. Subagents run in the background by default (Claude Code v2.1.198+): collect every agent's completion before starting Phase 3. If the user supplied a seed finding (a bug they hit, a release they know about), pass it verbatim to the relevant agent - specific leads converge fastest. **Adapt each angle to the skill**: a skill wrapping a package researches that package's releases and source; a skill tracking living docs or a spec researches those docs and their source repos; a skill with no upstream at all still gets the usage angle.

- **Usage** (pond - optional): if the pond MCP is available, dispatch three usage lanes alongside the upstream and docs agents. Tell each to use the pond MCP tools and read their descriptions first, and paste in the interim notes below:
  - **Summaries** - the agent's own end-of-task conclusions about the tool: causes, fixes, workarounds, rules it settled on.
  - **Corrections** - moments the user corrected how the tool was used, including the user overriding the skill's own advice. These rarely carry an error string.
  - **Usage audit** - sessions where this skill was loaded, and what failed while it was followed: denied launches, masked exit codes, wrong commands, things the agent had to look up that the skill should have said.

  Each lane excludes this repo's own sessions (they are circular), prefers newer conclusions over older ones, checks whether a learning was later reversed, and rechecks coverage against the skill as it is on disk at report time. It never copies tool-result bodies into a finding. Findings are **advisory leads, not facts** - ground-checked in Phase 3. **If pond is not installed, skip this angle entirely** - dispatch only the upstream and docs agents, and note "Usage angle skipped: pond MCP not available (https://pond.locker/)" in the Phase 3 report.
- **Upstream**: releases, commits, and merged PRs since the last-verified date. Read real source - clone to a local scratch dir (e.g. `~/pjv/<owner>/<repo>`, lowercase) or use the GitHub MCP pinned to a concrete tag/SHA. For skills wrapping a CLI, also ground-truth against the live installed binary (`<cmd> --help`, real invocations, run from the scratch directory) - docs and clones lag shipped behavior.
- **Docs**: the current canonical docs, read from source (raw `.md` or cloned repo), not model-summarized. Two distinct jobs, **both required**:
  - **(a) Drift check** - compare the docs against the skill's current `SKILL.md` and `references/`, flagging API changes, deprecated or removed symbols, and patterns the skill should adopt. This is anchored to what the skill already says.
  - **(b) Coverage sweep** - enumerate upstream's *current* feature/concept surface from the docs nav / table of contents, the API index, and the "what's new" / changelog. List every major capability, primitive, or concept the skill has **zero mention of**. Do NOT anchor this to existing skill content - the whole point is to find net-new surface the skill is silent about (`ADD` findings). This is the step a "verify what's there" pass structurally misses.

Every finding is one bulleted line: `[KIND]` (`ADD`/`CHANGE`/`DEPRECATE`/`REMOVE`/`FIX`/`SECURITY`), a one-line summary, an exact quote from the source (no paraphrase), and a citation. Usage lanes return `L<n> | <rule as the skill would state it> | covered: partial/no/contradicts | <session_id> <date> <project> | <lane> | <confidence>` instead, deduped by `(rule, session_id)`. Merge all returns into one list, deduped by `(KIND, citation)`.

### pond interim notes (remove once [tenequm/pond#369](https://github.com/tenequm/pond/issues/369) lands)

Paste this block into every usage-lane brief. Subagents cannot read MCP resources, so `schema://pond-sql` and ndjson exports are out of their reach; use text output only.

- The store is word-indexed (BM25), not semantic, and may be remote. Query with the literal words expected in the text, scope by date, and set `timeout_seconds` to 300-600. Measured on a remote store: `fts()` boolean 35-45 s over 150 days, a narrow `"operator":"And"` match 5-8 s, `contains_tokens` as discovery 70-135 s (use it only for exact-string existence counts), parts scans 50-450 s (one per lane).
- `pond_search` cannot filter by role or exclude a project. Discover through `pond_sql` with `fts('messages', '{"boolean":{"must":[{"match":{"column":"search_text","terms":"<tool>"}}],"should":[{"match":{"column":"search_text","terms":"<cause and fix words>"}}]}}')` joined to `messages` on `message_id`. Filter with `role = 'assistant'` (summaries) or `role = 'user' AND length(search_text) < 1500` (corrections), plus `NOT (source_agent LIKE '%/%')` and `NOT (project LIKE '%<this repo dir>%')`.
- User-role text carries echoed files and injected instructions. Exclude rows containing `<bash-stdout>`, `<system-reminder>`, `<skill>`, `<task-notification>` or `The following is the Codex`. Correction words (`never`, `instead`, `wrong`) are useless as filters for the same reason; the length cap is the filter.
- The skill-load index is `parts` where `tool_name = 'Skill'` and `json_extract(variant_data, '$.params.skill')` names the skill. Never use the bare skill name: a global CLAUDE.md that names it echoes it into nearly every session. For failures, scan `tool_result` bodies for the tool's own error prefix, grouped by signature; `is_failure` catches gate denials only.
- Read candidates with `pond_get_message`, confirm wording with a narrow And match, and finish with `pond_search` `sort_by="recency"` as the reversal check. It also surfaces a concurrent update run on the same skill: dedupe against it.

## Phase 3 - Verify, report, GATE 1

### Ground-truth verification (before the report)

No row ships unverified. Before a finding becomes a row, confirm it against primary source read **today**:

- Verify the finding's claim **and the existing skill text it touches** - links, enumerated lists, pinned versions, version-coupled examples. Spot-check the skill's other upstream-coupled claims even where no finding landed; silent staleness is the common miss.
- A row asserting upstream state (a bug, API shape, version, behavior) cites the primary source checked - cloned `repo@SHA file:line`, a release, or a docs URL; a pond citation alone is insufficient, so re-ground it or drop it. A row that is purely experiential enrichment (a recurring gap or confusion) may keep its pond citation, but verify the wording you write is technically correct.
- Drop a pond-reported bug already fixed upstream; correct any finding whose pond framing the source contradicts.
- A usage row that re-grounds against upstream (a bug, a flag, a version) becomes an ordinary section 4 row with the primary citation; a purely experiential one stays in section 6. A row that conflicts with a recipe in the user's own CLAUDE.md or AGENTS.md stays, marked `conflicts with CLAUDE.md`: only the user can pick which side changes.
- **Coverage-gap rows** (net-new concepts from the Phase 2(b) sweep) are verified two ways: confirm the concept exists in today's source (cite it), **and** confirm the skill genuinely omits it - grep the skill for the concept and any synonyms before claiming it's absent, so a renamed-but-present feature isn't reported as missing.
- Scope-check every usage-derived row: a learning about private infrastructure (internal hosts, personal tooling, machine-specific setups) belongs in the user's own CLAUDE.md or memory, not a public skill. Route it there and drop the row - the Phase 6 leak scan cannot make this judgment call.

### Report

Print a structured report, sections in order:

1. **Tracked packages diff** - `package | pinned | latest | delta`, or "no upstream packages tracked."
2. **Proposed `metadata.upstream`** - the new flat string. No floating tags (`@latest`/`@next`/`@beta`/`@canary`); pin to a concrete tag or SHA.
3. **Proposed CHANGELOG entry** - a Keep a Changelog block ready to commit.
4. **Proposed edits** - one row per smallest atomic change, each with a stable ID (`A1`/`C1`/`D1`/`R1`/`F1`/`S1`...): `<ID> | target file | one-line summary | citation`. Batch trivially-related changes into one row; past ~20 rows, consider whether the skill needs a rewrite rather than a patch. When ADD rows are numerous, include the projected post-apply `SKILL.md` line count; if it would cross the repo's size cap (500 lines in this repo), plan the `references/` split as part of the proposal, not as a surprise after apply.
5. **New-concept coverage** (**always present, never omitted**) - the result of the Phase 2(b) coverage sweep. Either a table of net-new upstream concepts the skill omits (each becoming an `ADD` row above), or the explicit statement that there are none. End this section with the verbatim attestation below. Coverage need not be complete to pass - but any gap in what you could enumerate (JS-gated docs, rate limits, unreachable pages) must be named here, not silently dropped:
   ```
   Coverage sweep: enumerated upstream's current surface from <sources>. Net-new concepts the skill omits: <list> / none since <last-verified date>. Not reachable this run: <areas, or "none">.
   ```
6. **Operational learnings** (present whenever the usage angle ran) - one row per usage finding not already covered: `<ID> | rule | covered: partial/no/contradicts | session date project | lane`, with IDs `L1`, `L2`... Then one line listing findings already covered, so the reader sees the sweep ran. End with this attestation:
   ```
   Usage sweep: lanes <summaries, corrections, audit> over <window>; <N> sessions read; SQL <min>-<max> s, timeouts: <none|list>. Concurrent update run: <session|none>. Routed to CLAUDE.md: <items|none>.
   ```
7. **Bootstrap proposal** (only when `bootstrap_needed`): candidate upstream packages greppable from the skill's content, each as `<package> (mentioned <N>x, first cite: <file>:<line>)` for the user to confirm or prune; plus a seed `CHANGELOG.md`. Propose only upstreams whose releases would invalidate the skill's content - the package, spec, or living doc the skill teaches. A tool mentioned incidentally (a validator run once, a CLI in one example) is not an upstream candidate. If the skill is **upstreamless by nature**, say so explicitly, propose no candidates, and leave `metadata.upstream` omitted - only seed the `CHANGELOG.md`.

### No-op short-circuit

If sections 1-4 yield zero rows AND the Phase 2(b) coverage sweep found no omitted concepts (section 5 attestation says "none") AND section 6 has no uncovered rows AND `bootstrap_needed` is false, print this verbatim and exit cleanly - no file changes, no commit. Never short-circuit without the section 5 attestation present:

```
All current as of <today>. Last verified per CHANGELOG.md on <date> against <metadata.upstream value>.
```

### CHANGELOG format

[Keep a Changelog](https://keepachangelog.com/en/2.0.0/) format. The dated entry uses only the sections it has content for (Added / Changed / Deprecated / Removed / Fixed / Security), plus a `Verified against: <pkg@version list>` trailer **only if** a tracked package version actually changed this run. Mark breaking changes inside Changed/Removed with a leading `**Breaking:**` marker, and pin the KaC link in preambles to the version followed (both per KaC 2.0.0).

When `bootstrap_needed`, create the full file with this header:

```markdown
# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [<current-version>] - <YYYY-MM-DD>
- Initial CHANGELOG; tracking established.
```

### GATE 1 banner (verbatim)

```
GATE 1 - APPROVE TO EDIT? (yes / yes <IDs> / drop <IDs> / changes <free-form> / no)
```

Reply parsing:
- `yes` / `yes all` -> apply every row
- `yes A1-A4 C1 L2` -> apply only those rows (and the listed package version updates, if any)
- `drop D1,R2` -> apply everything except those
- `changes <text>` -> revise the report and re-emit GATE 1
- `no` -> abort, no changes

Do NOT call Edit or Write until you receive an affirmative. Every revision round re-emits GATE 1; never silently apply.

## Phase 4 - Apply

Apply each approved row with Edit/Write; batch independent edits in parallel. Then, in order:

1. Update `metadata.upstream` to the new comma-separated `<name>@<version>` list. Reject floating tags - stop with an error if one appears. Skip entirely if the skill is upstreamless by nature - leave `metadata.upstream` omitted.
2. Bump `metadata.version` (semver per the repo's CLAUDE.md or AGENTS.md: patch for fixes, minor for new content/sections, major for breaking removal).
3. Append the new dated entry to `CHANGELOG.md` directly under `[Unreleased]`, above the previous entry. Add the `Verified against:` trailer only if a tracked version changed this run.
4. If `bootstrap_needed`, write the full `CHANGELOG.md` from the bootstrap header plus the approved seed entry.
5. When pasting upstream doc examples into a `SKILL.md` body, never let a `!` at line start or after whitespace directly touch a backticked command - Claude Code executes it at skill load, even inside code fences, and repo linters may reject it. Keep such examples in `references/` or break the adjacency.
6. Check the post-apply `SKILL.md` line count against the repo's cap (500 here); if crossed, execute the `references/` split planned in Phase 3.

## Phase 5 - Repo validation gate

If the repo defines a validation command - check its CLAUDE.md/AGENTS.md or `Justfile`/`package.json` (e.g. `just check`, `npm run lint`, `make check`) - run it from `<workdir>`. In this repo that is `just check`, which also regenerates `README.md` - stage it with the skill changes, a stale `README.md` is the most common CI failure. On failure, surface the error verbatim, fix the root cause, and re-run until clean. If the failure looks unrelated to this run's edits, attribute before debugging: stash the changes (`git stash -u`) and re-run the gate on a clean tree. Failing identically means the breakage is pre-existing (an environment flake or repo issue) - unstash, report it to the user, and don't sink this run into debugging it. No `--no-verify`, no `--amend`, no hook-skipping. If the repo has no validation gate, skip this phase and note it.

## Phase 6 - Privacy scan + diff review + GATE 2

### Privacy / leak scan (hard blocker)

Skills in a public repo can publish on merge, and any research source can leak into the diff - especially pond, which draws on private cross-project conversations. This scan runs every time, whether or not pond was used. Before showing the diff, dispatch a dedicated agent (separate from the Phase 2 research agents) to scan the added/changed lines **and every new untracked file** under `skills/<name>/` and `README.md` (if the repo generates one). `git diff` alone misses brand-new files (e.g. a fresh `references/` doc) - enumerate them with `git status --porcelain` and give the agent their full content.

It flags anything unsafe for a public skill: secrets (keys, tokens, passwords, `.env` values, connection strings), personal data (real names, emails, handles), and the easy-to-miss ones - non-public project or repo names, internal hostnames or endpoints, ticket IDs, local machine paths, pond session IDs. Intentional public references are fine (the public repo owner, official upstream repos and docs, published package names, spec URLs). The agent returns `[LEAK] <file>:<line> - <what> - suggested redaction: <text>` per issue, or exactly `NO LEAKS FOUND`.

An unresolved `[LEAK]` is a hard blocker: redact each finding, re-run the scan, and repeat until clean before GATE 2. Hold the commit message to the same public-safe standard.

### Checkout hygiene (hard blocker)

Run `git status --porcelain` in `<workdir>` and in `${CLAUDE_PROJECT_DIR}` too - subagents can write into the main checkout even when the run edits a worktree. Any path missing from the Phase 1 snapshot and outside `skills/<name>/` and the generated `README.md` is a leftover from this run (a `.build/`, `node_modules/`, a scratch package): show it to the user, remove it, and re-check before GATE 2. Never gitignore it away - that hides the next leak from this check.

### Diff review

Print `git status`, `git diff --stat`, and per-file diffs for `SKILL.md`, every changed `references/` file, `CHANGELOG.md`, and `README.md`. Then print this recovery hint verbatim, immediately above the gate banner:

```
To discard everything: git restore . && git clean -fd skills/<name>/
```

```
GATE 2 - APPROVE COMMIT + PUSH? (yes / no)
```

Wait for explicit confirmation. Do not commit on ambiguous responses.

## Phase 7 - Commit, push, watch

**Branch guard first.** Run `git rev-parse --abbrev-ref HEAD`. If the result is not the repo's default branch, ask the user: push to the current branch and open a PR (recommended), push directly to the default branch (only on explicit instruction - if the repo auto-publishes on merge, this skips PR review and ships straight to the registry), or cancel.

Commit with a conventional-commit message (type per content, per the repo's CLAUDE.md or AGENTS.md) using the HEREDOC pattern:

```bash
git commit -m "$(cat <<'EOF'
<type>(<name>): <one-line summary>

<body if non-trivial>
EOF
)"
```

- **On the default branch**: `git push`, then, if the repo has CI, `gh run watch` the triggered run. On CI failure, surface logs verbatim; do not auto-retry.
- **On a feature branch**: `git push -u origin <branch>`, then `gh pr create` with a body summarizing the Phase 3 report. Skip `gh run watch` at this point - PR CI is typically non-publishing, and some publish-on-merge repos run no PR CI at all. The run is not done at PR creation: once the PR merges, watch the default-branch publish run (`gh run watch`), confirm the publish landed, then do the Phase 0 cleanup (worktree first, then branch).

Updating several skills in one session? Land them together: batch into one push, or merge the PRs back-to-back and watch only the final publish run - each push to the default branch typically triggers a full republish.

If the repo auto-publishes on merge (e.g. to a registry via CI), confirm the publish landed once CI is green. The published slug and release/tag naming follow the repo's own pipeline - check its CLAUDE.md/AGENTS.md (the published slug can differ from the folder name).

## Done

Report a one-line summary to the user: skill name, version delta, tracked packages updated, CI status. If the repo's skills are consumed through an installer (e.g. `npx skills`), remind the user to refresh installed copies (`npx skills update <name>`) once the publish lands.
