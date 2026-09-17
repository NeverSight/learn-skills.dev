---
name: coderabbit
description: >-
  CodeRabbit CLI local code reviews and .coderabbit.yaml configuration.
  Run AI reviews on uncommitted/committed changes before pushing or opening
  a PR, parse --agent findings, iterate fix-and-verify loops within hourly
  rate limits, and tune repo config for low-noise high-signal reviews.
  Use when reviewing local changes pre-push/pre-PR, installing or driving
  the coderabbit/cr CLI, creating or tuning .coderabbit.yaml, or reducing
  CodeRabbit review noise. Not for PR-side review loops and thread
  handling (git-pr), commits (git-commit), or CI status (git-ci)
---

# CodeRabbit CLI and Configuration

**Local-first AI code review: catch issues before they reach the PR.** The CodeRabbit CLI (`coderabbit`, alias `cr`) reviews working-tree or branch changes locally, so the PR-side review becomes confirmation instead of iteration -- this saves billable PR review rounds (both CodeRabbit's own quota and any Copilot credits). Covers the CLI surface and `.coderabbit.yaml` tuning. PR-side mechanics (threads, re-requests, the bot loop) live in the `git-pr` skill.

## When to Use

- **Reviewing local changes** -- "review my changes", "run coderabbit", pre-commit/pre-push/pre-PR checks
- **Driving a review-fix loop** -- run review, fix valid findings, re-run to verify
- **Configuring CodeRabbit** -- create or tune `.coderabbit.yaml`, reduce review noise, disable redundant linters
- **Checking limits** -- rate limits per plan, review budgeting
- **Setting up the CLI** -- install, auth, headless/CI usage

## Critical Rules

1. **Reviews upload code to CodeRabbit's service.** A review sends the diff (and context) to CodeRabbit. On a repo with sensitive/unpublished code, confirm the user is OK with that before the first run.
2. **Reviews consume a per-hour quota** (Free: 3/hour CLI reviews). Scope deliberately (`--committed`/`--uncommitted`, `--base`) and use `coderabbit review findings` to replay the last result without spending a review.
3. **Use `--agent` output when driving fixes programmatically**; the default plain-text mode is for humans.
4. **Validate findings before fixing** -- same rule as PR reviews: judge each finding on its merits; never blind-fix to silence the tool.
5. **CodeRabbit is optional -- check the Code Review Policy first** (repo AGENTS.md/CLAUDE.md, falling back to the user's global agent instructions; see `git-pr` skill) for the preferred reviewer and checkpoints. Never install, authenticate, or run it on a project whose policy or user hasn't opted in.

---

## Setup

```bash
curl -fsSL https://cli.coderabbit.ai/install.sh | sh   # or: brew install coderabbit
coderabbit auth login        # browser OAuth; --agent emits JSON for agent-driven login
coderabbit auth status       # verify
coderabbit doctor            # diagnose runtime/auth/connectivity issues
```

`auth login` also accepts `--api-key <key>` (store a key instead of OAuth), `--region us|eu`, and `--self-hosted`; `auth org` switches the active organization.

**No paid plan required**: the Free plan includes CLI reviews (3/hour) after `coderabbit auth login` with a free account -- paid plans add org context, learnings, and higher limits. Headless/CI: `CODERABBIT_API_KEY` env var with an **Agentic API key** (requires the usage-based add-on on paid plans), or `--api-key` per call. `coderabbit update` self-updates.

The CLI must run inside a git repository. `cr` is a shorthand alias for `coderabbit`.

## Review Scopes and Checkpoints

| Checkpoint | Command | Reviews |
|------------|---------|---------|
| Before commit | `coderabbit review --uncommitted` | Staged + unstaged tracked changes |
| Before push | `coderabbit review --committed` | Local commits not in the base branch |
| Before PR (full branch) | `coderabbit review --base main` | Working tree + branch commits vs base |
| Subdirectory only | `coderabbit review --dir packages/api` | Changes under a path |
| Vs specific commit | `coderabbit review --committed --base-commit {sha}` | Changes since a commit |
| Include untracked files | `coderabbit review --include-untracked` | Also files not yet added to git |

Defaults (CLI v0.7): all tracked changes, base = repository default branch, plain-text output. v0.7 **removed** the older `--type <scope>` and `--plain` flags (`error: unknown option`) -- scope with `--committed`/`--uncommitted`, and plain is simply the default. `--light` runs a faster, lighter review policy for quick local iteration.

## Output Modes

- Default (no mode flag) -- detailed plain-text feedback with fix suggestions, non-interactive.
- `--agent` -- JSON-lines: one object per line. Finding objects carry `type: "finding"`, `severity` (`critical|major|minor|trivial|info`), `fileName`, `suggestions`, and `codegenInstructions` (written for coding agents -- follow them when fixing); a `comment` field appears when `codegenInstructions` is empty. Heartbeat events appear during long reviews; a final `complete` event carries `status` (`"review_skipped"` with `findings: 0` when the scope has no changes). A depleted bucket ends the run at exit code `1` with `{"type":"error","errorType":"rate_limit","recoverable":true,"metadata":{"waitTime":"7 minutes"}}` and no findings -- the exit status alone cannot tell a bounce from a real failure, so branch on `errorType`, take the retry window from `metadata.waitTime` (wait it out plus a minute, then re-run), and never read the empty result as a clean review.
- `coderabbit review findings` -- replay cached findings from the most recent local review **that produced findings** (clean sessions are skipped), with no new analysis and **no quota cost** (`--dir <path>` reads a scoped review's cache). Use between fix iterations; only re-run a real review to verify at the end.
- `coderabbit review --show-prompts` -- print the AI prompts from the most recent local review, no new review.
- `coderabbit stats` -- review statistics (`--rebuild` rescans review history).
- `coderabbit usage` -- the current billing period: organization, whether usage billing (overage) is active, your review count, the usage-based spend so far, and the period reset date. **Billing totals only** -- it does not report the hourly bucket, and no CLI command reveals a PR-side retry window. That question is answered on the PR instead, by `@coderabbitai rate limit` (below). Present in CLI v0.7 (`coderabbit --help`) even though the online command reference omits it: **the installed binary is the source of truth, not the docs page** -- verify with `--help` before "removing an unsupported command".
- `@coderabbitai rate limit` -- **not a CLI command: a PR comment**, and the only on-demand read of the PR-side bucket. Reports the remaining allowance and when the next review becomes available, and [does not consume a review](https://docs.coderabbit.ai/reference/review-commands) (aliases `rate-limit`, `limits`, `quota`). Answers within seconds, even while rate-limited: "Your next review will be available in N minutes" -- the only durable read of that window, since the notice edited into the summary comment can vanish. Post it before opening a loop, and after a bounce instead of probing with triggers. It spends no review, but it is still a PR comment -- a write, subject to the usual approval.

## The Local Review-Fix Loop

1. Run `coderabbit review --committed --base {base} --agent` (or `--uncommitted` pre-commit; background it -- reviews take minutes).
2. Parse findings; triage by `severity`. Address `critical` and `major` first.
3. **Validate each finding** against the codebase (conventions, actual behavior, project docs). Fix valid ones per `codegenInstructions`; note invalid ones with a one-line rationale for the user.
4. Re-run the same review command to verify fixes. Stop when no valid `critical`/`major` findings remain, or the hourly bucket is exhausted (the CLI reports the limit -- wait or stop, never hammer).
5. Then push / create the PR -- **once the change is completely finished**, not once the findings are fixed. Where PR-side auto-review and `auto_incremental_review` are on (both default), the push *is* the review request and it reviews whatever the branch holds at that moment: remaining tasks, tests, docs and config belong in the same push, or each leftover costs another PR-side window. The PR-side review (if any) should then come back clean or near-clean.

Commit fixes by what they change, never by what prompted them -- `fix: validate empty page cursor`, not `fix: coderabbit fixes` or `fix: review round 2` (see the `git-commit` skill). Fixes must not add code comments that restate what the code already reads.

Two passes (review, fix, verify) is the normal shape. More than three passes means findings are being treated as noise -- re-evaluate validity or tune config (see `references/configuration.md`).

## Rate Limits (Per Developer, Per Hour)

| Plan | CLI reviews | PR reviews | Files/review |
|------|-------------|------------|--------------|
| Free | 3 | 1 (summary only) | 150 |
| OSS (public repos) | 3 | 1--10, by repo popularity | 100--300, by popularity |
| Pro | 5 | 5 | 150 |
| Pro+ | 10 | 10 | 300 |
| Enterprise | 12 | 12 | 300 |

The Lite plan was retired (June 2026); Free / Pro / Pro+ / Enterprise are current. Beyond the hourly allowance, the usage-based add-on bills $0.25 per reviewed file (Pro and up). Open-source public repos get free reviews with popularity-based limits.

**The table is a CEILING, not the rate you get -- [fair-usage throttling](https://docs.coderabbit.ai/management/plans) sets the effective PR-side allowance below it.** It engages once a developer identity reaches the 95th percentile of recent PR review usage, and derives the refill rate from that developer's review count over a **rolling window that is either the past 24 hours or the past 7 days**, whichever the activity pattern selects; the plan allowance itself is not changed. Documented Pro ladder by reviews in the window: 0--29 -> 5/hr, 30--39 -> 4/hr, 40--49 -> 3/hr, 50--59 -> 2/hr, 60+ -> 1/hr one at a time. Pro+ starts at 10/hr and steps down to 1/hr at 90+. Observed live on a paid Pro plan, crossing a tier mid-loop: 4/hr at round 1, 3/hr two rounds later, then a bounce.

Two consequences. **A heavy review week throttles the next one** -- the binding window is days, not the hour, and capacity trickles back as old reviews age out instead of resetting on the hour. And **a bounce is free but pointless**: "a blocked push does not consume a review or delay when your next review becomes available", since capacity is set by earlier *completed* reviews -- yet a refused round is never queued, so extra triggers inside a closed window buy nothing. Probe with `@coderabbitai rate limit` (no review consumed) rather than with triggers -- verified live: after two bounces it still quoted a window closing 54 minutes after the last *completed* review, so the bounces moved nothing. (The run-configuration footer says "review **attempts** over the past 7 days", but the documented ladders count reviews; treat the footer's number, not its noun, as the fact.)

Past the included limit, the [usage-based add-on](https://docs.coderabbit.ai/management/usage-based-addon) decides what happens, and its admin-set mode decides which: `Automatic` keeps reviewing and bills the overage, `On demand` pauses until a seat-holder authorizes each review, `Off` stops until the included allowance resets. Only `Automatic` is a release valve -- and fair-usage spacing is a separate mechanism layered on top.

**Which plan row applies is something you must be told -- but the LIVE allowance is readable in two places:** the "Run configuration" block inside each posted review names the plan and the current reviews-per-hour figure (read it off the most recent review before planning a loop), and `@coderabbitai rate limit` reports the remaining allowance plus next availability on demand, without spending one. The rest is silent: `coderabbit usage` reports the billing period (org, overage on/off, review count, reset date) and the PR-side API never mentions a plan. Declare it in the **Code Review Policy** (`git-pr` skill) -- `CodeRabbit plan: pro+ until 2026-08-20, then pro` -- in the repo's AGENTS.md/CLAUDE.md, or globally for every repo. It decides real behaviour: how many PRs can be non-draft at once, how many rounds to budget, and how much iteration belongs in the CLI lane instead. Re-plan when a trial lapses; a queue tuned for 10 reviews/hour stalls at 5. Undeclared, take the floor from observed behaviour (`bot_bucket`) rather than assuming the best case.

### Where a Bounce Shows Up

**A depleted bucket passes for a clean result in every lane that ignores the lane's own signal.** Each lane does report it -- but never as a failed run, and never in the field most checks look at. Know the tell for the lane you are in:

| Lane | What a bounce looks like | The tell |
|------|--------------------------|----------|
| CLI (`--agent`) | Exit `1` with zero findings -- identical to a failure by exit status, and "no findings" reads as clean | `{"type":"error","errorType":"rate_limit",...,"metadata":{"waitTime":"7 minutes"}}` -- branch on `errorType`, never on the findings count |
| CLI (default output) | The run ends with a limit message and no findings | Read the message; do not treat the empty result as a passing review |
| PR-side | Often **nothing at all** -- no review, no threads, no comment -- plus a green `CodeRabbit` check in the PR's checks list | That check's `description` reads `Review rate limited` (state is `SUCCESS` for every finished outcome): `gh pr checks --json name,state,description`. `Review completed` is the reviewed case, and `Review in progress` (state `PENDING`) means it is still running -- wait rather than trigger |

The PR-side row is the one that misleads most: the checks list shows a tick next to CodeRabbit between passing CI jobs, so the PR reads as reviewed-and-green when the code was never looked at. PR-side handling (windows, re-triggers, the loop) lives in the `git-pr` skill.

**Only the PR itself can tell you when a PR-side round may retry -- ask it with `@coderabbitai rate limit`.** Three dead ends around it, so no one spends the time again:

| Where you might look | What you actually get |
|----------------------|-----------------------|
| `coderabbit usage` | Billing period only -- org, overage on/off, review count, reset date. No hourly bucket |
| CI logs behind the check | Nothing: CodeRabbit posts a **commit status**, not an Actions run (`check-runs` is empty, `target_url` is `null`). Log-diagnosable hard limits are a Copilot thing |
| The quota notice on the PR | A per-PR **estimate** that the next summary-comment edit can delete -- two PRs of one developer quoted 48 and 10 minutes 104 seconds apart, while a third PR's review completed 8 minutes later |

What *does* answer it: a `@coderabbitai rate limit` comment (remaining allowance + next availability, no review consumed), and the newest `Review completed` across **all** your open PRs, since the bucket is per developer (`bot_bucket` in `git-pr`'s `references/bot-review-loop.md`). If a sibling PR was reviewed after your bounce, the bucket is open now.

## Configuration

`.coderabbit.yaml` at the repo root governs both PR-side and CLI reviews (the CLI also accepts `-c <file>` for extra instruction files, e.g. `CLAUDE.md`). For typed, well-linted projects the goal is high-level findings only: `profile`, `tone_instructions`, disabled CI-redundant linters, `path_filters` for generated files. Validate edits with `coderabbit config validate [file]` (checks against the current official schema) before committing.

> **Reference**: See `references/configuration.md` for the full schema highlights, config precedence, the low-noise template for typed/linted projects, and PR-side commands (`@coderabbitai review` vs `full review`, pause/resume, config dump).

## Key Gotchas

1. **`--committed` needs commits, `--uncommitted` needs a dirty tree** -- reviewing the wrong scope silently reviews nothing (`review_skipped`); match the scope to the checkpoint.
2. **`coderabbit review findings` replays, it does not re-review** -- after fixing, cached findings still show; only a fresh review verifies fixes. It also skips clean sessions: even after a clean verify run, it replays the older findings, which is not a regression.
3. **The quota is per-hour, not per-day** -- a "limit reached" message means wait for the window, not stop for the day. Plan verify runs so the final pass fits the bucket. In `--agent` mode the bounce is a `rate_limit` error line at exit `1` -- indistinguishable from a real failure by exit status alone, and a findings-count check reads it as clean. Branch on `errorType` and take the window from `metadata.waitTime`.
4. **CLI reviews and PR reviews draw from separate buckets** -- burning CLI reviews locally does not reduce the PR-side allowance, which is the point of the local-first flow.
5. **Org context needs matching access** -- on a repo not linked to your CodeRabbit org, reviews run in limited free mode (no learnings/org context); results differ from PR-side reviews on the same code.
6. **`--agent` emits JSON lines, not a JSON document** -- parse line-by-line; do not `JSON.parse` the whole output.
7. **`--type <scope>` and `--plain` no longer exist** (removed in v0.7; `error: unknown option`) -- older docs and allowlists reference them; use `--committed`/`--uncommitted` and rely on the plain default.
8. **A PR-side rate limit is silent and green** -- no review, no threads, usually no comment, and a passing `CodeRabbit` check whose `description` reads `Review rate limited`. Nothing about the PR looks wrong, so an unreviewed PR gets reported as reviewed. Read that description before concluding anything from a quiet PR-side round (Where a Bounce Shows Up).
9. **A quoted retry window is an estimate, and it is not durable** -- it is edited into the summary comment and a later edit can remove it, while different PRs quote wildly different numbers at the same moment. Capture it when you see it, take the smallest one visible across your PRs, and treat a sibling PR's `Review completed` as the real all-clear (Where a Bounce Shows Up). Don't wait out the largest number you can find.
10. **The push is the PR-side review request** -- with auto-review plus `auto_incremental_review`, every push spends a PR-side review of whatever is on the branch, from a bucket that is **per developer, not per PR**. Finish the whole change locally, then push once; the local lane (separate bucket) is where iteration belongs.
11. **A rate-limited attempt can leave its commits looking reviewed** -- once the window reopens, a plain `@coderabbitai review` over unchanged commits answers "does not re-review already reviewed commits" and the round silently never happens, so the recovery trigger after a bounce is **`@coderabbitai full review`**. It does not always stick, though: observed on this repo, the *next push* after a bounce resumed its incremental range from the last **completed** review and did re-cover the two skipped commits unprompted. Read the review's own "Commits" block to see which range it actually took, rather than assuming either way. The same forcing form is the fix for a wedged **"Review queued"** (observed stuck 2+ hours): nudge after ~1 hour instead of waiting it out.

> **Reference**: See `references/configuration.md` for `.coderabbit.yaml` tuning and PR commands
> **Reference**: See `references/allowlist.md` for auto-approval patterns
> **Reference**: PR-side review loops, thread handling: `git-pr` skill (`references/bot-review-loop.md`)
