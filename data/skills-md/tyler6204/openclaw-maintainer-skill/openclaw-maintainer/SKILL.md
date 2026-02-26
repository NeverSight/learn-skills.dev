---
name: openclaw-maintainer
description: PR review and merge automation for OpenClaw maintainers. Parallelized sub-steps using sub-subagents. Uses gpt (codex) for reasoning tasks and gpt-fast (codex-spark) for lightweight API/search tasks.
---

# OpenClaw Maintainer

PR review + prep + merge automation with parallelized sub-steps.
Uses two model tiers for cost/speed optimization:
- **gpt** (openai-codex/gpt-5.3-codex, 60 TPS): code analysis, fixes, anything requiring judgment
- **gpt-fast** (openai-codex/gpt-5.3-codex-spark, 2000 TPS): GitHub searches, CI checks, post-merge cleanup, API calls + string matching

## maxSpawnDepth Requirement

This skill requires `maxSpawnDepth >= 2` in the OpenClaw session configuration. The parallelism works like this:

1. **Main agent** spawns a top-level subagent (depth 1) for review/prep/merge
2. **Top-level subagent** spawns sub-subagents (depth 2) for parallel work (scanning, cleanup)

If maxSpawnDepth is less than 2, sub-subagents will fail to spawn and the parallel phases will break. The skill will still work at depth 1 but will run everything serially in the parent subagent, which is slower.

## SAFETY: NEVER PUSH TO MAIN

Subagents have full disk access. The one inviolable rule:
- NEVER force-push, push, or directly commit to `main` or `origin/main`.
- All pushes go to PR head branches only.
- The only way code reaches main is through `gh pr merge --squash`.
- If gates (lint/build/test) have not passed, do NOT merge.

## LOCAL-ONLY FILES RULE

Non-source files (testing checklists, notes, TODOs, temp files, debug outputs, scratch plans) must NEVER be committed to PR branches. They go in `.local/` which is gitignored. The preparepr command enforces this automatically, but all commands should be aware of it.

## Token Optimization

Build, test, and lint commands are run as background processes to avoid burning tokens watching real-time output. Only read output on failure.

- **Tests:** `sleep 60` then poll every 10s. Average runtime ~60s.
- **Build:** `sleep 40` then poll every 10s. Average runtime ~30-40s.
- **Lint:** fast enough to run inline.

This pattern is enforced in preparepr.md. See the "Token-Optimized Command Execution" section in preparepr.md for the exact commands.

## Changelog Awareness

Before committing prep fixes, the workflow checks the project changelog:
- Determines the latest release version via `gh release list --limit 1 --exclude-drafts --exclude-pre-releases`
- Reads CHANGELOG.md and adds entries under an "Unreleased" section
- Never puts entries into already-released version sections
- Summarizes what the PR does concisely

## Docs Awareness

After applying code fixes, the workflow scans for user-facing changes (new parameters, changed behavior, new config options, removed features). If found, relevant docs are updated. Internal-only changes skip this step.

## Test Quality Enforcement

During review (/reviewpr), test code is specifically analyzed for:
- `sleep`, `setTimeout`, artificial delays, or polling patterns in tests (should use fake timers)
- Missing test coverage for new functionality
- Tests reimplementing the function they test
- Test isolation issues (reading/writing real user directories)

## GitHub Identity Awareness

Before commenting on any issue or PR, the workflow checks `gh api user` to determine the logged-in GitHub username. If the current user is also the PR/issue author, comments use self-referential language ("Closing this out, superseded by #X") instead of thanking yourself. For other people's contributions, polite acknowledgment is used. This applies across mergepr and any cleanup sub-subagents that comment on issues or close PRs.

## .local/ Artifacts (Cross-Step Coordination)

The `.local/` folder inside the worktree is the thread that connects parallel work across steps:

| File | Written by | Read by | Purpose |
|------|-----------|---------|---------|
| `.local/review.md` | /reviewpr | /preparepr, /mergepr | Full structured review (sections A-K) |
| `.local/related.md` | /reviewpr | /preparepr, /mergepr | Related issues/PRs to close after merge |
| `.local/prep.md` | /preparepr | /mergepr | Prep summary with push verification shas |

- `/reviewpr` saves both `review.md` and `related.md`
- `/preparepr` reads `review.md` and `related.md`, writes `prep.md`
- `/mergepr` reads all three to verify state and drive post-merge cleanup

## Command Files

The actual command files live in this skill's `commands/` folder. Subagents read these directly (they do NOT read this SKILL.md file).
- `commands/reviewpr.md` - review only (parallelized: code analysis, CI/related scan, test coverage)
- `commands/preparepr.md` - rebase, fix, run gates, push fixes, but do NOT merge (parallel scan, serial fix, gates, push)
- `commands/mergepr.md` - merge only (serial merge, then single cleanup sub-subagent)

## Workflow Overview (3 step)

1. **User:** "review PR #2403"
2. **Main agent:** spawns gpt subagent (xhigh thinking) via `sessions_spawn`. Subagent reads `commands/reviewpr.md` and executes.
3. **GPT subagent:** sets up worktree, spawns 3 parallel sub-subagents (code analysis, CI/related scan, test coverage), combines results into structured review, saves `.local/review.md` and `.local/related.md`, pings back findings.
4. **Main agent:** summarizes for user (ready for prep, needs work, concerns)
5. **User:** "ok prep it" / "fix X first" / "don't merge"
6. **Main agent:** if approved, spawns gpt subagent (xhigh thinking) via `sessions_spawn`. Subagent reads `commands/preparepr.md`.
7. **GPT subagent:** installs dependencies, spawns 2 parallel read-only scanners (lint, fix identification), then serially applies fixes following the recommended fix order, rebases, updates changelog and docs if needed, runs gates (token-optimized including tests), pushes, verifies push. Saves `.local/prep.md`.
8. **User:** "merge it"
9. **Main agent:** spawns gpt subagent (xhigh thinking) via `sessions_spawn`. Subagent reads `commands/mergepr.md`.
10. **GPT subagent:** verifies state, checks GitHub identity, merges via `gh pr merge --squash`, then spawns a single cleanup sub-subagent (close superseded PRs, close related issues, clean worktree). Pings back merge SHA.
11. **Main agent:** confirms to user with merge SHA

## ALWAYS USE SUBAGENT

Review, prep, and merge are long running tasks. NEVER run in the main thread. Always use `sessions_spawn` to create a subagent.

## Model Tiers

Two model tiers, used by both top-level subagents and their sub-subagents:

| Alias | Model ID | TPS | Use for |
|-------|----------|-----|---------|
| `gpt` | openai-codex/gpt-5.3-codex | 60 | Code analysis, fixes, judgment calls |
| `gpt-fast` | openai-codex/gpt-5.3-codex-spark | 2000 | GitHub searches, CI checks, post-merge cleanup, API calls |

Top-level subagents always use `gpt` with `thinking:xhigh`. They spawn sub-subagents with the appropriate tier based on task type. The command files specify which model each sub-subagent should use.

If a model is not available, fall back to session default model.

## Review Workflow (/reviewpr)

```
sessions_spawn task:"Review PR #<number> in openclaw repo. Read commands/reviewpr.md and follow its instructions exactly." model:gpt thinking:xhigh runTimeoutSeconds:0 label:"pr-<number>-review"
```

Default model is `gpt` which is good for most reviews. For PRs requiring deeper nuance (complex architecture decisions, subtle correctness issues, security-sensitive changes), you can override with opus:

```
sessions_spawn task:"Review PR #<number> in openclaw repo. Read commands/reviewpr.md and follow its instructions exactly." model:opus thinking:high runTimeoutSeconds:0 label:"pr-<number>-review"
```

## Prep Workflow (/preparepr)

```
sessions_spawn task:"Prepare PR #<number> in openclaw repo. Read commands/preparepr.md and follow its instructions exactly." model:gpt thinking:xhigh runTimeoutSeconds:0 label:"pr-<number>-prep"
```

## Merge Workflow (/mergepr)

```
sessions_spawn task:"Merge PR #<number> in openclaw repo. Read commands/mergepr.md and follow its instructions exactly." model:gpt thinking:xhigh runTimeoutSeconds:0 label:"pr-<number>-merge"
```

## Parallelism Design

Each command file documents when and how to spawn sub-subagents, including which model tier to use. All command files include the EXACT `sessions_spawn` call syntax so sub-subagents know precisely what to invoke.

### /reviewpr parallelism
Three parallel read-only sub-subagents after worktree setup:
- **Subagent A (Code Analysis)** `model:gpt thinking:xhigh`: reads diff, analyzes quality, correctness, edge cases, security
- **Subagent B (CI & Related Scan)** `model:gpt-fast`: checks CI status, searches for related issues/PRs, scans for duplicates
- **Subagent C (Test Coverage)** `model:gpt thinking:xhigh`: checks test coverage gaps, test quality (flags sleep/setTimeout/polling), docs, changelog
- Then the parent (gpt) combines all results into one structured review

### /preparepr parallelism
Parallel read-only scanning phase (2 sub-subagents), then serial fix/gates phases:
- **Parallel Scan Phase:** lint scanner `model:gpt-fast` and fix identifier `model:gpt thinking:xhigh` run concurrently
- **Serial Fix Phase:** parent (gpt) applies code fixes following the recommended fix order from the Fix Identifier, rebases, commits, updates changelog and docs
- **Gates Phase:** run lint (inline), build (background, sleep 40 + poll), test (background, sleep 60 + poll). Tests run here AFTER fixes are applied. Only read output on failure.
- **Push Phase:** push and verify (parent, gpt)

Note: tests are intentionally NOT run during the parallel scan phase. Running tests before fixes are applied produces misleading results. Tests run in the gates phase after all fixes are committed.

### /mergepr parallelism
Serial merge (parent, gpt) with identity-aware commenting, then single cleanup sub-subagent:
- **Serial Phase:** verify state, check GitHub identity, merge via gh pr merge --squash, post identity-aware comment
- **Single Cleanup Sub-subagent** `model:gpt-fast`: close superseded PRs (identity-aware), close related issues (identity-aware), clean worktree and branches. All done serially in one agent since it's ~5 API calls total.

## Important Notes

- Subagents read the command file directly, they do NOT read this SKILL.md
- Each command file is self-contained with all setup, steps, and safety rules
- Sub-subagents spawned by command subagents are always read-only or cleanup-only
- If checks or gates fail, report failure and stop, do not force merge
- If merge fails, report and do NOT retry in a loop
- PR must end in MERGED state, never CLOSED
- Code only reaches main through `gh pr merge --squash`, never through direct push
- Token optimization: build/test run in background, only read output on failure
- Changelog is updated during prep if the PR has user-facing changes
- GitHub identity is checked before any PR/issue comments to avoid self-thanking
- maxSpawnDepth must be >= 2 for parallel sub-subagents to work
