---
name: review-pr
description: Review a GitHub PR, then automatically request changes for any findings or approve a clean review. Use on a PR URL when the ask is to produce and submit findings; when findings already exist and the ask is to act on them, use /fix-pr-review. Batch mode covers 2+ PRs or "review all open PRs". For local uncommitted changes, use /parallel-review.
---

# /review-pr: Deep GitHub PR Review

Reviews a remote GitHub PR with anti-slop filtering. It takes a PR URL and nothing else.

Goal: produce an accurate, critical, actionable PR review, filter out noise (style nitpicks, hallucinated references, duplicates, generic advice), and submit the result to GitHub. Reviews of another author's PR use `REQUEST_CHANGES` or `APPROVE`; self-reviews use `COMMENT` because GitHub forbids authors from approving their own PRs.

**Cascade** is the failure this review is built to prevent: a fix shipped for round N's finding becomes round N+1's finding. Two things feed it: the suggested fix carries a defect of its own, and the fix lands on the cited site while identical sibling sites go untouched. So every finding proposing a code change carries an `Inverse risk:` and a `Class-sites:` count, one field per feeder. Phase 3 measures the result as `cascade_share` at step 7.5, the verdict at step 8 reads it to say whether the PR is converging, and Phase 4 prints it.

This skill expects CodeRabbit on the repo via `.coderabbit.yaml`. CodeRabbit handles style and convention findings first. `/review-pr` handles the deep semantic and codebase-wide review only it can do.

**Use AskUserQuestion for user-facing decisions that still require judgment**: stop-and-ask and post-failure recovery. Posting is not a decision point. Invoking `/review-pr` authorizes submission of the complete review. Large PRs always proceed with chunked review without asking. Any sentence that offers the user 2+ labeled paths is an AskUserQuestion call. Options are cursor-selectable, concrete, and considered. Put the strongest first and mark it "(Recommended)".

## Reference files

Main or a subagent loads each file only on the branch that reaches it. Loader and firing condition:

- `references/batch-mode.md`: orchestration rules, "don't stop" semantics, consolidated-report template, and automatic posting sequence. Loaded by **main** at Phase 1 when the user gives 2+ PR URLs or asks for all open PRs.
- `references/reviewer-prompt.md`: the whole Subagent 1 prompt, the anti-slop rules it works under, and the note on why the finding shape is not restated inside it. Loaded by **main** at the Phase 2 dispatch on every `SIZE_MODE` branch.
- `references/cross-cutting-prompt.md`: the whole Subagent 3 prompt. Loaded by **main** at the Phase 2 dispatch when `SIZE_MODE` is `parallel-chunked`; the unchunked modes never dispatch Subagent 3.
- `references/security-prompt.md`: the whole Subagent 4 prompt. Loaded by **main** at the Phase 2 dispatch when `INCLUDE_SECURITY_REVIEWER = true`, in every `SIZE_MODE`.
- `references/q5-type-coercion.md`: the Q5 type-coercion scan: coercion methods, how to decide a field is numeric, severity. Loaded by **Subagent 1** while answering Q5, and by **Subagent 4**, when the diff contains a DB insert/update or an API payload construction.
- `references/class-sweep-and-inverse-risk.md`: reviewer-prompt steps 5 and 6: blast-radius search order, the `class_completeness:` and `Inverse risk:` field rules, the worked inverse-risk examples. Loaded by **Subagent 1** as soon as any finding proposes a code change.
- `references/repo-map.md`: the `repo_map_files` / `repo_map_exports` shell, local and cross-repo modes. The one copy in the repo; `/fix-pr-review` loads it from here too. Loaded by **main** in Phase 1 when `packages/` or `apps/` exists.
- `references/q6-reusability-search.md`: STEP A enumeration + STEP B search algorithm + Q6 control-flow gap. Loaded by **Subagent 1** when the diff has 1+ new definitions of any STEP A kind (not top-level only). The cross-repo search block lives in `references/q6-cross-repo.md`, loaded only when `repo_map_exports` is the cross-repo `N/A` marker.
- `references/finding-output-format.md`: the per-finding field block, the `class_completeness:` audit shape, and the run-level closing block. The one copy of the finding shape. Loaded by **Subagent 1**, **Subagent 3**, **Subagent 4** and **V3** before they write any finding.
- `references/schema-design-checks.md`: Q7 (overlap), Q8 (1:1 consolidation), Q9 (cross-table FK) checks. Loaded by **Subagent 1** when `INCLUDE_SCHEMA_CHECKS = true`, and by **V3** when the gap check covers Q7-Q9.
- `references/verification-subagents.md`: V1/V2/V3 dispatch conditions + the exact prompt each is given. Loaded by **main** in Phase 3 at the first of steps 4.55 / 4.9 / 6 that fires.
- `references/false-positive-rules.md`: the four-rule YAML table (`wrapped-coercion`, `intent-alignment`, `library-behavior-citation`, `default-fallback`) each surviving finding is run through. Loaded by **main** at Phase 3 step 4.6 when any finding survives step 4.5.
- `references/finding-state-schema.md`: both persistence files: `.claude/review-state/<pr>.yml` (schema, finding-ID strategy, state machine, Phase 1 read path) and the run-over-run cache (schema + the three replay branches). Loaded by **main** in Phase 1 before the review-state read and the cache check, and held through Phase 3. The Phase 4 write-back and sweep live in `${CLAUDE_SKILL_DIR}/references/finding-state-phase4.md`, loaded in Phase 4 after posting, plus on Phase 1 startup when the state directory is non-empty.
- `references/github-posting.md`: fresh-review REST/GraphQL posting flow: summary body, per-finding comments, hunk validation, Phases A through C, and the write-back. Loaded by **main** in Phase 4 for every completed review. Re-runs with a prior review or cache entry also load `${CLAUDE_SKILL_DIR}/references/github-posting-rerun.md` (Steps 0, 0b, 0c, 4-rolling, 8d); a posting failure also loads `${CLAUDE_SKILL_DIR}/references/github-posting-recovery.md` (Step 7).
- `references/phase1-timeline-state.md`: prior-review thread query plus shaping, the review-state read plus round seeding, and the run-over-run cache branches. Loaded by **main** in Phase 1 at the timeline, state, and cache steps.
- `references/dispatch-prompts.md`: the `<SKILL_DIR>` derivation, the `<PROMPT_PREAMBLE>` and `<GROUND_TRUTH>` blocks, and the silent-failure hunter context packet. Loaded by **main** at the Phase 2 dispatch.
- `references/critic-verify.md`: critic steps 1 through 4.57, dedupe through origin attribution. Loaded by **main** at Phase 3 step 1, kept through step 4.57, reloaded at step 6 for routed findings.
- `references/critic-round2.md`: critic steps 4.9, 4.95 and 4.96, regression sweep plus suppression plus lineage. Loaded by **main** at Phase 3 step 4.9, only from round 2 on.

Four closures, so the accounting is deterministic. Main never loads `finding-output-format.md`: only Subagent 1, Subagent 3, Subagent 4, and V3 load it, before writing findings. V1 and V2 load no references: they report compact verdicts from finding text. Main never loads `schema-design-checks.md` or `q5-type-coercion.md`: Subagent 1 loads each under its own condition, Subagent 4 loads the coercion scan under the same condition, and V3 loads the schema checks only when the gap check covers Q7-Q9. The anti-slop rules live in `reviewer-prompt.md` alone: no dispatch pastes a second copy into any prompt.

## Planning-doc grounding (optional pre-review context)

If `docs/superpowers/specs/` or `~/.claude/plans/*.md` reference this PR, check the diff against those documented design decisions and flag undocumented deviations under Q1 Intent. If no such files exist, skip this check.

## Usage

```
/review-pr https://github.com/owner/repo/pull/123
```

If no URL is provided, ask the user for one. Bare `gh` commands infer a PR from the current branch. This skill reviews the URL it was given.

## Batch mode (multiple PRs)

Fires when the user provides **2+ PR URLs** or asks to review **all open PRs**. A single-PR run skips this entirely and drops straight into Phase 1. On that branch, load `${CLAUDE_SKILL_DIR}/references/batch-mode.md` before doing anything else: it holds the PR enumeration, the orchestration rules (one subagent per PR, main never reviews inline, subagents never post or ask), the "don't stop" semantics for review-only checkpoints, the consolidated-report template, and the automatic posting sequence.

---

## Phase 1: Gather context (main)

Run these as **two separate Bash tool calls in a single assistant message**. True parallelism needs separate tool_use blocks, not `&&` chained.

```bash
gh pr view <url> --json number,title,body,author,baseRefName,headRefName,headRefOid,baseRefOid,additions,deletions,changedFiles,files,closingIssuesReferences,reviews,comments,state,isDraft
gh pr diff <url>
```

Record `CURRENT_HEAD` from `headRefOid`, `PINNED_BASE_OID` from `baseRefOid`, and `BASE_REF_NAME` from `baseRefName`. A push landing between the two calls mixes revisions, so after the diff lands, re-read both OIDs and require equality with the recorded pair. On either mismatch, discard both results and restart Phase 1 once. A second mismatch proceeds with a note that the PR moved mid-review.

Issue the independent reads below as parallel Bash tool calls in a single assistant message: viewer login, linked-issue bodies, review threads, cwd repo, CodeRabbit config, and suppressions. They depend on nothing but the PR URL and owner/repo, so sequencing them is pure wall time.

Phase 1 fetches the **full diff**. Stash it in main context. The error-handling content scan and the Phase 3 critic reference check both need it.

### Empty-diff short-circuit

If `changedFiles == 0` OR `additions + deletions == 0`:

> **Nothing to review.** This PR contains no reviewable file changes.

Stop immediately.

### Private-repo / access-error handling

If `gh pr view` returns a GraphQL resolution error or HTTP 404:

> **Couldn't access PR.** Check repo access. Try `gh auth refresh -s repo` and retry.

Fail fast.

### Detect self-review posting

After the metadata request succeeds, compare the authenticated viewer with the PR author already recorded in that response:

```bash
VIEWER=$(gh api user -q .login)
AUTHOR=<.author.login from the Phase 1 metadata>
```

GitHub documents that [pull request authors cannot approve their own pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews). Set `IS_SELF_REVIEW=true` when the accounts match and continue through the complete review. Phase 3 still decides the semantic verdict as `approve` or `request-changes`; Phase 4 submits the review with `COMMENT`, preserving its summary and per-finding threads without claiming an approval GitHub cannot record. Set `IS_SELF_REVIEW=false` otherwise.

### Extract linked issues

1. Prefer `closingIssuesReferences` (each carries its own `repository.nameWithOwner`; use that, not the PR's repo).
2. Fall back to body regex: `(?i)(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)` (same-repo only).
3. For each linked issue: `gh issue view <num> --repo <owner>/<repo> --json title,body,state`.
4. If ≥ 2 linked issues, note `multiple linked issues, so intent may be ambiguous`. If their goals plainly contradict, route to stop-and-ask fallback.

### Build the intent model

```
Goal: <one sentence from issue + PR description>
Expected touches: <what files/areas should be changed>
Out of scope: <anything the issue explicitly excludes, or "none">
Size: <additions>/<deletions> lines across <N> files
Draft: <yes|no>
```

### Build the prior-review timeline

Pull every review thread and read the saved state per `${CLAUDE_SKILL_DIR}/references/phase1-timeline-state.md`. Load it now. It holds the thread query, the prior-findings shape, the state-file read plus round seeding, and the cache branches. What it builds feeds Phase 3 dedupe and the round-2 regression sweep.

### Load review-state (multi-round dedup)

Covered by the reference loaded above.


### Stop-and-ask fallback

Trigger if **no linked issue** AND the PR description **lacks all** of these:

- A file path or directory reference
- A function / class / symbol name
- An error message or stack trace
- A reproduction command
- A linked issue URL in body (even outside `closingIssuesReferences`)

Thin descriptions like "update X", "fix bug", or "wip" fail. Terse but grounded descriptions like "Fix race in `auth/cache.ts` eviction; repros with `make stress-test-auth`" pass.

On trigger, AskUserQuestion:

```
header: "Intent"
text: "Intent is unclear. No linked issue and the description lacks grounding signals. How should I proceed?"
options:
  - "Proceed anyway": Review with just the diff; findings will be generic without grounding
  - "Skip this PR": Abort the review
  - "I'll provide intent": Wait for user to type intent text
```

On "I'll provide intent", wait for follow-up text, then build the intent model from it.

### Size warning

If `additions + deletions > 2000`:

> This PR touches **X lines across Y files**. Review may be noisy and slow. Proceeding.

### Wall-time instrumentation (start)

Capture `PHASE_START_TIME=$(date +%s)` at the top of Phase 1 and similar at each later phase. Print elapsed total in Phase 4.

### Detect cwd-vs-PR-repo mismatch (cross-repo mode)

```bash
CWD_REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "")
PR_REPO="<owner>/<repo>"
[ -z "$CWD_REPO" ] || [ "$CWD_REPO" != "$PR_REPO" ] && CROSS_REPO_MODE=true || CROSS_REPO_MODE=false
```

Cross-repo mode changes:
1. Repo map computation falls back to remote `gh api` tree fetch.
2. Phase 3 already-fixed check uses `gh api` instead of local `git log`.

Note it in the Phase 4 output header.

### CodeRabbit config check (one-time hint)

Once per `(owner, repo)` per session, check whether `.coderabbit.yaml` exists in the PR repo:

```bash
gh api "repos/<owner>/<repo>/contents/.coderabbit.yaml" >/dev/null 2>&1 \
  && CR_CONFIG_PRESENT=true \
  || CR_CONFIG_PRESENT=false
```

If `CR_CONFIG_PRESENT=false` AND this is the first run of `/review-pr` against this repo in the current session, hint once after Phase 4 output:

> No `.coderabbit.yaml` in `<owner>/<repo>`. Adding one pushes style + convention checks into CodeRabbit. Copy the template at `https://raw.githubusercontent.com/bhagyamudgal/skills/main/coderabbit-config/coderabbit.yaml.template` to `<repo>/.coderabbit.yaml` (bootstrap steps in that repo's `coderabbit-config/README.md`). Future `/review-pr` runs in this repo will be tighter.

The hint is informational. It never gates posting.

### Size-based routing (determine SIZE_MODE)

```
SIZE = additions + deletions

if SIZE <= 500:     SIZE_MODE = "parallel-standard"     # Subagent 1 reviewer + conditional silent-failure hunter
else:               SIZE_MODE = "parallel-chunked"      # Per-chunk reviewers + hunter + cross-cutting reviewer, always proceed without asking
```

Subagent 1 always dispatches; tiny PRs pay one subagent round trip.

### Run-over-run cache check

Check the run-over-run cache per `${CLAUDE_SKILL_DIR}/references/phase1-timeline-state.md`, loaded above.


If `PRIOR_STATE.convergence` exists, invoke `converge-reviews` with the current request, base/head, diff hash, paths, and planned roster/lenses before Phase 2. Reuse a matching result without dispatch. When it returns `closure_check: available`, dispatch the one targeted check over only the named blocker IDs and changed sites. Keep the recorded round unchanged and reject any new finding or widened coverage from that check. Feed its evidence and updated blocker dispositions back through `converge-reviews`, persist the new result plus `closure_check: passed | failed`, then apply that result: a passing check may return `converged`; a failed check remains `blocked-at-cap` at the current round. When the initial result is `continue`, review only the invalidated coverage it names; apply any other result without starting another round.

### Compute shared-package repo map (for Q6)

If `CROSS_REPO_MODE=true`, load `${CLAUDE_SKILL_DIR}/references/repo-map.md` and run the cross-repo block unconditionally: the target repository's layout decides, not the local cwd's. Otherwise, if `packages/` or `apps/` exists, load `${CLAUDE_SKILL_DIR}/references/repo-map.md` and run the block for the mode you are in: it holds both shell blocks (the cross-repo `gh api` tree fetch and the local `bash -c` find/grep pair, each truncating at 500 lines) and writes `repo_map_files` + `repo_map_exports` to the staged `repo-map.md` for the subagent prompts. It is the one copy of that shell, shared with `/fix-pr-review`.

If neither directory exists in local mode, skip the shell. Set both to `N/A (not a monorepo)` and flag `IS_MONOREPO=false`. Subagent 1 reroutes greps to the changed files' directories, or the repository root when those reveal nothing. Never assume `src/`.

### Check for error-handling touches (flag for Phase 2)

Grep the diff content for error-handling patterns in **added or modified lines**:

```
try \{ | catch \( | catch \{ | throw new | throw \s | \.catch\( | Result< | rescue | err := | raise
```

If any pattern appears or the user mentions error handling, set `INCLUDE_SILENT_FAILURE_HUNTER = true`.

### Check for new database tables (flag for Phase 2)

Grep the diff content in **added lines**:

```
pgTable\( | createTable\( | CREATE TABLE | knex\.schema\.createTable | Schema\.create\(
```

If any pattern appears, set `INCLUDE_SCHEMA_CHECKS = true`. Also extract `SCHEMA_DIR`. Typical values are `db/schema/`, `drizzle/schema/`, `src/schema/`, or `migrations/`. If unidentifiable, set `SCHEMA_DIR = "."` and limit Q7-Q9 grepping to files matching the table-definition pattern, for example `Grep("pgTable", ".", glob: "**/*.ts")`.

In cross-repo mode, use `gh api git/trees/<head-sha>?recursive=1` for file listing. Q7-Q9 reads use `gh api repos/<owner>/<repo>/contents/<path>?ref=<head-sha>`.

### Check for sensitive code (flag for Phase 2)

Split each changed file path into segments on `/`, `.`, `_`, `-` and camelCase boundaries, then compare every segment, case-insensitively, against this list. Whole segments only, so `author` and `design-tokens` never match:

```
auth | login | logout | session | sessions | token | jwt | oauth | oidc | permission | permissions | authorization | authorize | authz | access | policy | policies | rbac | role | roles | guard | guards | acl | tenant | tenants | billing | payment | payments | stripe | checkout | invoice | invoices | crypto | secret | secrets | password | passwords | webhook | webhooks | hl7 | fhir
```

Match the diff's **added and removed lines**, case-sensitively, against the pattern below. Removed lines count because deleting a guard or a tenant filter is the most common security regression. Bare `accountId` triggers on purpose: in a multi-tenant repo it marks every tenant-scoped query.

```
accountId | account_id | tenantId | tenant_id | organizationId | orgId | @UseGuards | @Roles | @Public | req\.user | hasAccess | canAccess | isAuthorized | authorize\( | Forbidden | createHmac | timingSafeEqual | bcrypt | jsonwebtoken | jwt\. | dangerouslySetInnerHTML | innerHTML | queryRawUnsafe | executeRawUnsafe | sql\.raw | child_process
```

If either matches, set `INCLUDE_SECURITY_REVIEWER = true` and keep the matched paths and patterns as `SENSITIVE_HITS` for the Subagent 4 prompt.

### Load project-level review suppressions

Read it at the base revision, never the worktree: a checked-out PR must not suppress its own review.

```bash
SUPPRESSIONS_FILE=".claude/review-suppressions.yml"
SUPPRESSIONS=$(git show "$PINNED_BASE_OID:$SUPPRESSIONS_FILE" 2>/dev/null || { git fetch --no-tags origin "$BASE_REF_NAME" 2>/dev/null; git show "$PINNED_BASE_OID:$SUPPRESSIONS_FILE" 2>/dev/null; } || true)
```

When the base has no such file, set `SUPPRESSIONS = ""` and log that a PR-added suppressions file was ignored. A PR may propose suppressions for future reviews after merge, never for its own.

Schema:

```yaml
suppressions:
  - pattern: "factory pattern"
    category: Architecture
    reason: "YAGNI - single provider by design"
    added: 2026-04-13
  - pattern: "missing timeout"
    file: "claude-code.ts"
    reason: "Timeout handled at caller level"
```

`pattern` is required. It matches case-insensitively against the finding `Issue` text. `category` and `file` are optional and scope the suppression. `reason` is required and appears in Filtered Out for auditability.

If file exists, pass into Subagent 1 prompt as "Review suppressions: patterns this project has already accepted; skip them". Phase 3 step 5.5 also applies as safety net.

In cross-repo mode, fetch via `gh api repos/<owner>/<repo>/contents/.claude/review-suppressions.yml?ref=$PINNED_BASE_OID`. Skip on 404. The pinned base OID is trusted; the PR head is not, so a PR can never suppress its own review.

### Stage the handoff files

Subagents never fetch the diff or receive pasted context. At the end of Phase 1, write these into a per-PR subdirectory next to `$STATE_FILE`, named for the state file without `.yml` (batch mode shares the directory across concurrent flows): `diff.full.patch` (full diff, for the hunter, cross-cutting reviewer, security reviewer, and V3), `diff.chunk-N.patch` (per-chunk diffs split by file, chunked mode only), `repo-map.md` (repo map from the step above), `timeline.md` (intent model plus prior timeline and closed findings). No prompt tells a subagent to run `gh pr diff`. Prompts carry file paths plus the small inline intent.

---

## Phase 2: Reviewer subagents

Launch in a **single message with multiple Agent tool calls** based on `SIZE_MODE`. The reviewer subagents go out once here and the Phase 3 verifiers go out once there. That is the whole review. If the PR needs a second look, start a fresh `/review-pr` run. Never re-dispatch inside this one.

### Dispatch strategy

**`SIZE_MODE == "parallel-standard"`** (500 lines or fewer, default):
- Dispatch Subagent 1 (Claude reviewer) + conditional Subagent 2 (silent-failure hunter) in parallel. Subagent 1 reads `diff.full.patch`; both read `repo-map.md` and `timeline.md`.

**`SIZE_MODE == "parallel-chunked"`** (> 500 lines):
- Dispatch ONE Subagent 1 PER CHUNK with the small inline intent plus its chunk file, `repo-map.md`, and `timeline.md`. Prompt: "Your scope is the files listed above. Read only <chunk-file>. Do not report findings in other files."
- Dispatch one silent-failure hunter and one **cross-cutting reviewer** at full PR scope, both reading `diff.full.patch`. Chunk reviewers report within their own chunk only, so Subagent 3 is the one reviewer that can see a defect class spanning two chunks. Without it, that class feeds the cascade directly.
- Always proceed with chunked parallel review. Never ask for confirmation, regardless of size.

**Either mode**, when `INCLUDE_SECURITY_REVIEWER = true`: also dispatch Subagent 4 (security reviewer) at full PR scope, reading `diff.full.patch` and `timeline.md`.

### Degraded-mode rule

If any subagent errors out or returns empty, continue with the remaining ones and note `<reviewer> unavailable` in the Phase 4 output header. Abort only if all fail.

**Note on CodeRabbit.** CodeRabbit findings arrive through the prior-review timeline in Phase 1, pulled from the PR existing comments when the repo has `.coderabbit.yaml`. See the one-time hint above. No CodeRabbit subagent goes out. If the PR latest commit has no CodeRabbit comment yet, Subagent 1 carries the load and the next round picks up the CodeRabbit input.

### Subagent 1: Claude reviewer (`general-purpose`)

Substitute `<SKILL_DIR>`, the shared preamble, and the ground-truth block per `${CLAUDE_SKILL_DIR}/references/dispatch-prompts.md`, then load `${CLAUDE_SKILL_DIR}/references/reviewer-prompt.md` at this dispatch. Every dispatch names the staged file paths from the end of Phase 1.


### Subagent 2 (conditional): Silent-failure hunter

Only dispatch if `INCLUDE_SILENT_FAILURE_HUNTER = true`.

- `subagent_type`: `pr-review-toolkit:silent-failure-hunter`

The context packet is PART OF THE PROMPT, not commentary around it. Dispatch the `### Subagent 2 (conditional)` packet in `${CLAUDE_SKILL_DIR}/references/dispatch-prompts.md` verbatim, with `<GROUND_TRUTH>` substituted. Handed only a URL, this subagent has no idea what the PR is for or what earlier rounds closed, so it re-finds settled issues and misses the rest.


### Subagent 3 (conditional): Cross-cutting reviewer

Dispatch when `SIZE_MODE` is `parallel-chunked`. Skip otherwise.
In unchunked modes Subagent 1 already sees every file.

- `subagent_type`: `general-purpose`
- Scope: the WHOLE PR. It is the only reviewer permitted to report across file boundaries.

The prompt lives in `${CLAUDE_SKILL_DIR}/references/cross-cutting-prompt.md`. Load it at
this dispatch.

### Subagent 4 (conditional): Security reviewer

Dispatch when `INCLUDE_SECURITY_REVIEWER = true`, in either `SIZE_MODE`. Subagent 1 still answers Q5; this is the independent second pass on the code where one missed security bug costs the most.

- `subagent_type`: `general-purpose`
- Scope: the WHOLE PR, security only. Each finding cites the line that introduces it.

The prompt lives in `${CLAUDE_SKILL_DIR}/references/security-prompt.md`. Load it at this dispatch.

---

## Phase 3: Critic pass (main context)

The critic pass always runs. It catches slop the reviewer prompt misses. No branch prints, posts, or persists findings that skipped it.

After all subagents return, main Claude runs the critic pass, splitting the work on one line:

- **Judgment stays in main.** Dedupe, the 3-prong test, false-positive rules, suppressions,
  ranking, verdict. These need the intent model and the prior-review timeline, which main
  already holds. Shipping them to a subagent would mean re-sending all of it.
- **Evidence-gathering goes to subagents.** Anything that means grepping the repo,
  enumerating callers, or re-reading files at HEAD. These burn context proportional to the
  codebase and return a few lines of verdict. Main should hold the verdict, not the search.

Steps 4.55, 4.9 and 6 dispatch subagents per `${CLAUDE_SKILL_DIR}/references/verification-subagents.md`. Load it when you reach the first of those steps whose condition holds, and keep it for the others. The three dispatch in one message. If none holds, the file is never needed.
Everything else runs inline. A verification subagent reports evidence in a compact
structured verdict; main rules on severity, on drops, and on the state file.

Execute in order:
Steps 1 through 4.56 run per `${CLAUDE_SKILL_DIR}/references/critic-verify.md`. Load it at step 1 and keep it through step 4.56, then reload it at step 6 for findings routed back through 4.55 and 4.56. Steps 4.9, 4.95 and 4.96 run per `${CLAUDE_SKILL_DIR}/references/critic-round2.md`, loaded only from round 2 on.

### 1. Dedupe

Merge findings that describe the same issue, across reviewers and within one output, per the reference. Same file, line, and symbol means duplicate whatever the category says.

### 1.5. Cheap line-count sanity

Drop cited lines that cannot exist before spending verdict effort, per the reference.

### 2. Verify `file:line`

Check every reference against the stashed diff, per the reference. Post-image side only.

### 3. Drop already-known

Drop anything Phase 1 already reported unless it carries `Category: Prior-finding-correction`, per the reference. A finding whose thread the author answered stays dropped even when the new commits left its code unchanged.

### 4. Challenge with the 3-prong test

Drop a finding only when all three hold: cosmetic, behavior-neutral, refactor-free. Any one failing keeps it. Log drops as `noise / 3-prong test`.

### 4.5. Reusability audit verification

Count new definitions, parse the `reusability_searches:` audit (missing, sentinel, or entries), and log all drops, per the reference.

### 4.55. Class-completeness verification

Sweep every code-change finding for sibling sites through V1, per the reference. Everything entering leaves widened, carrying a non-empty `Class-sites`.

### 4.56. Inverse-risk verification

Derive or vet the `Inverse risk:` on every `Suggested fix:`, per the reference. `/fix-pr-review` implements these verbatim, so an unvetted remedy becomes production code.

### 4.57. Attribute origin

Mark every surviving finding `Origin: introduced` or `Origin: pre-existing` by blaming its cited line against the pinned base, per the reference. Runs every round, round 1 included. Only `introduced` findings decide the verdict. A `pre-existing` finding still posts as a thread, then Phase 4 tracks it in its own issue so it never blocks this PR.


### 4.6. Apply false-positive rules table

A unified iterator over a rules table. Each rule has: `id`, `trigger` (regex matched against `Issue` or `Why`), `evidence_check` (a callable that returns `evidence_present | evidence_absent | inapplicable`), `action` (`drop` / `downgrade-1` / `downgrade-1-and-note`).

Apply each rule in order. Log each fire to Filtered Out with the rule `id` + reason.

The rules themselves, the four-rule YAML table with every `trigger` regex and `evidence_check` body, live in `references/false-positive-rules.md`. Load it here whenever at least one finding survives step 4.5; skip it when the finding list is empty. That table is the single source of truth for false-positive filtering: adding a new false-positive class is a one-row YAML edit there, not a new prose section here.

### 4.9. Proactive regression sweep (runs before prior-state suppression, 4.95)

Skip entirely when `CURRENT_ROUND == 1`. From round 2, sweep every prior-state entry per `${CLAUDE_SKILL_DIR}/references/critic-round2.md`. Load it here. A missing verdict gets re-checked inline, never read as still-closed.

### 4.95. Apply prior-state suppression (multi-round dedup)

From round 2, suppress already-handled findings per the reference loaded at step 4.9. Every finding leaves with exactly one of `active`, `resolved`, `dismissed`, `wontfix`, `regression`.

### 4.96. Attribute lineage on this round's findings

Skip entirely when `CURRENT_ROUND == 1`. There is no earlier fix to attribute to, and every finding gets `caused_by: null`. From round 2, attribute fresh findings per the reference loaded at step 4.9, one hop, same bound as step 4.9. Step 7.5 counts only the resolvable links; dangling ids are excluded per `references/finding-state-schema.md` (`caused_by` cardinality).


### 5. Confidence-based drop

Drop all `Confidence: low` findings at Moderate or Minor. Log as `low-confidence filler`. **Keep** low-confidence Critical/Serious. Humans want risky-but-uncertain flags.

### 5.5. Apply project-level suppressions

If `SUPPRESSIONS` was loaded in Phase 1, match each remaining finding:

1. Check if `Issue` text contains `pattern` (case-insensitive substring).
2. If `category` set, also check finding's `Category` matches exactly.
3. If `file` set, also check finding's `File` path contains the string.

If ALL specified conditions match: DROP, log `suppressed by .claude/review-suppressions.yml: "<reason>" (pattern: "<pattern>")`.

**Critical/Serious override**: suppressions drop findings at any severity. A team that explicitly decided a pattern is acceptable outranks the review, and `reason` keeps the drop auditable.

### 6. Gap check (Q1-Q6, Q7-Q9 if schema PR)

For any question category where Subagent 1 said nothing, briefly think about whether the diff has anything in that category. Add findings if you spot misses. Include Q7-Q9 only if `INCLUDE_SCHEMA_CHECKS = true`.

**Large-PR routing.** If `additions + deletions >= 500` and main lacks the full diff,
route this check to **V3: Deep gap check** and fold its findings in here. V3 has the
context budget to answer from the diff itself, where main would be guessing from a
file list. Pass V3 `INCLUDE_SCHEMA_CHECKS` and `SCHEMA_DIR`. It is dispatched precisely
on the large PRs where schema changes live, so dropping the flag drops Q7-Q9 exactly
where they are most likely to fire.

**Re-run the cascade gates on everything this step adds.** Reload `${CLAUDE_SKILL_DIR}/references/critic-verify.md` for this routing. Findings created here, main's
own and V3's alike, arrive after steps 4.55, 4.56, 4.57 and 4.96 have already run, so they
carry an empty `Class-sites`, an empty `Inverse risk`, no `Origin`, and no `caused_by` unless
routed back. Route every finding this step adds back through:

1. **3**: drop already-known, including answered threads.
2. **4.55**: class-completeness sweep, so `Class-sites: <A>/<N>` is non-empty. Where V1
   has already returned, run the sweep inline in main rather than dispatching a second V1;
   the 4-subagent cap still holds.
3. **4.56**: inverse-risk derivation, so every `Suggested fix:` carries an `Inverse risk:`.
4. **4.57**: origin attribution, so `Origin` is `introduced` or `pre-existing`.
5. **4.96**: lineage attribution, so `caused_by` is set or explicitly null.

`Inverse risk` and `Class-sites` are mandatory on any finding proposing a code change no
matter which step raised it; a gap-check finding that skips these writes nulls straight
into the state file and blinds the next round's regression sweep.

### 7. Rank by severity

Critical > Serious > Moderate > Minor.

### 7.5. Compute `cascade_share`

The ONE place this ratio is computed. Ranking is done, the finding set is final, and every
finding carries a `caused_by` from step 4.9 or 4.96, so this is the first point where the
number is both computable and stable.

At `CURRENT_ROUND == 1` there is no prior round to attribute to: set `cascade_share = 0`,
skip the trend sentence, and move on.

From round 2:

```
cascade_share: <count of active introduced findings with a resolvable caused_by> / <count of active introduced findings>
```

Pre-existing findings stay out of both counts. No fix in this PR wrote their lines.

A `caused_by` counts only when its target finding is still present. Dangling ids are excluded, per `references/finding-state-schema.md` (`caused_by` cardinality), which owns that rule.

Zero active introduced findings → `cascade_share = 0`, not a division by zero.

Step 8 below reads this value for the verdict prefix, and Phase 4's **Cascade check**
prints it. Neither recomputes it: one number, one definition, one round.

### 8. Decide verdict

Count only `Origin: introduced` findings here. Pre-existing findings still post, but never set the verdict.

- One or more surviving introduced findings → `request-changes`
- No surviving introduced findings AND no open blockers → `approve`
- No surviving introduced findings BUT one or more open blockers (`OPEN_BLOCKERS` from Phase 1) → `request-changes` on the blocked-by-open-threads path. Dedupe was right to drop the re-reported findings, so no new threads go up. The review posts body-only with the event, and its body lists every blocker as `path:line` (`path` alone for file-level threads with no line), author, and one-line issue. A self-review posts the same body with `COMMENT`, keeping the semantic `request-changes` verdict in the body and terminal output. Pre-existing findings on this path go in that body under `### Pre-existing` without threads, and Phase 4 still tracks each in its own issue. Thread coverage prints `0/<P>`, where `<P>` is that pre-existing count, with the reason pointing at the blocking-threads list.

At any round, if `cascade_share > 0.5`, prepend to the verdict reason:

> Over half of this round's findings were introduced by the previous round's fixes.
> Patching site-by-site is not converging. This module needs a design pass.

### 9. Decide Senior-engineer approval

A binary assessment:

- **No**: one or more introduced findings survived the critic pass, OR one or more open blockers exist, OR Q1 identified an intent gap
- **Yes**: otherwise

Write a one-sentence approval reason grounded in the most important finding or the absence of findings. Composed text carries no em or en dash. Text quoted from the issue or the diff stays as you found it.

---

## Phase 4: Output

Every Phase 4 path reaches **Convergence handoff** after main submits the GitHub review and writes back local state.

### Print this block to terminal, always

```
# PR Review: <title> (#<number>)

**Senior engineer approval**: <emoji> <Yes | No>, <one-sentence reason>
**Verdict**: <emoji> <approve | request-changes>
**GitHub event**: <APPROVE | REQUEST_CHANGES | COMMENT; use COMMENT when IS_SELF_REVIEW=true>
**Goal**: <intent goal>
**Size**: <additions>/<deletions> across <N> files
**Reviewers**: <list, with "(unavailable)" marker for any failed subagent>
**Round**: <CURRENT_ROUND> (<active>/<resolved>/<dismissed> findings carried across rounds)
**Convergence**: <N> new · <C> caused by earlier fixes · <R> regressions reopened · <F> carried
**Thread coverage**: <threaded>/<surviving> findings as review threads<; reason when below full>
<trend line, omit at round 1>
**Review URL**: <https://github.com/<owner>/<repo>/pull/<number>#pullrequestreview-<REVIEW_DB_ID> | <same URL> (pending draft) | not posted (<reason>)>

## Summary
<2-3 sentence summary>

## Findings (<introduced count>)

### Critical
<entries>

### Serious
<entries>

### Moderate
<entries>

### Minor
<entries>

## Pre-existing (<count>)
<entries in severity order, each with its blame commit and its tracking issue URL, or `not tracked (<reason>)` when Phase 4 could not file it>

## Filtered out (<count>)
<dropped findings with reasons, for auditability>

## Multi-round status
<for each finding in PRIOR_STATE: id, file, status, round_resolved/dismissed, dismissal_reason. Useful for "did I really ship M3 in round 5?" scanning.>
```

### Verdict and approval emoji mapping

**Senior engineer approval**: Yes → ✅ · No → ❌
**Verdict**: approve → ✅ · request-changes → ❌
**Severity headers**: Critical → 🔴 · Serious → 🟠 · Moderate → 🟡 · Minor → 🔵

Terminal output must include Filtered out. It shows when the critic over-filters. Include Pre-existing when any finding carries that origin. Include multi-round status when `PRIOR_STATE.findings` is non-empty.

### Review URL

Always print the **Review URL** line last in the header block, after posting/recovery settles, so the user can open the submitted review in one click. Build it from the reconciled review database ID:

```
REVIEW_URL="https://github.com/<owner>/<repo>/pull/<number>#pullrequestreview-<REVIEW_DB_ID>"
```

Use the fresh review's `REVIEW_DB_ID` from Phase C, the reused review's `PRIOR_REVIEW_DB_ID` on the rolling path, or the reconciled ID from the monolithic recovery write-back. When the user keeps a pending draft ("Show payload & keep draft"), print the pending review's URL with a `(pending draft)` suffix instead. When nothing was posted (abort, block, keep-local), print `not posted (<reason>)` instead of a URL. A run that blocks or aborts before posting still prints the block with the reason.

### Thread coverage

Threaded findings over surviving findings, printed after the posting/recovery outcome is known: the line reports that outcome, not the planned payload. Line-level and file-level threads both count; body-fallback findings count as surviving, not threaded. Name the reason whenever threaded < surviving: body fallback, recovery fallback, a blocked or aborted phase, or no threaded posting at all (batch subagent; the orchestrator posts). A run that blocks or aborts before posting still prints the block with the reason. Zero surviving findings prints `0/0`.

### Cascade check

Mandatory from round 2. PRINT the step 7.5 value. Do not recompute it here: Step 8 already read that same number for the verdict prefix, and a second computation on a different finding set is how the two disagree.

Emit exactly one trend sentence, picked from what the numbers say:
- `cascade_share > 0.5` → `Not converging, because the fixes are generating the findings.`
- New findings falling round over round and `cascade_share == 0` → `Converging, with the tail shrinking.`
- New count flat across 3+ rounds → `Stalled at the same volume each round; scope may be growing.`

```
Convergence: 4 new · 3 caused by earlier fixes · 1 regression reopened · 2 carried
Trend: cascade_share 0.75. Not converging, because the fixes are generating the findings.
```

If a verdict reverses an earlier `approve` assessment, say so explicitly in the Summary
with the reason and the two SHAs. For another author's PR, write *"I approved this at `dd142e0`.
I'm reversing that, because `e4f7432` made one thing worse than it was."* For a self-review,
write *"I assessed this as approve at `dd142e0`. I'm reversing that, because `e4f7432`
made one thing worse than it was."*

### Wall-time instrumentation (end)

Compute total elapsed + per-phase from `PHASE_START_*` timestamps. Append before Filtered Out:

```
## Timing
Phase 1: <s> (metadata + diff + intent + repo map + state load)
Phase 2: <s> wall / <sum> CPU (parallel: <N> subagents)
Phase 3: <s> (dedupe + verify + 3-prong + reusability audit + FP rules + prior-state + suppressions + gap + verdict)
Phase 4: <s>
Total:   <s>
```

### Post to GitHub

An explicit `/review-pr <PR URL>` invocation is fresh authorization to submit the complete review to that exact PR. The authorization remains valid only while the target PR, head SHA, semantic verdict, GitHub event, and frozen payload match the later mutation card. Apply `preflight-mutations` normally and block on any non-ready verdict; do not bypass it or ask the user to select findings, confirm posting, keep the review local, edit the body, or choose a next action.

- When `IS_SELF_REVIEW=false`, submit every surviving finding as an individual review comment with `REQUEST_CHANGES`; submit a clean review with no open blockers with `APPROVE` and no review comments; submit a clean review with open blockers on the blocked-by-open-threads path (Phase 3 step 8). A review whose only surviving findings are pre-existing counts as clean, and its `APPROVE` carries those findings as threads.
- When `IS_SELF_REVIEW=true`, submit the same complete finding set or clean summary with `COMMENT`. Keep the semantic verdict in the body and terminal output.
- Preserve every item in `Filtered out` as terminal-only audit output. Filtered items never enter the GitHub payload.
- Every surviving finding ships as a review thread, or the Thread coverage line states plainly that it did not ship and why. The terminal report is never pasted as an issue comment.

Load `${CLAUDE_SKILL_DIR}/references/github-posting.md` now: summary body, per-finding comments, hunk validation, Phases A through C, and the write-back. Also load `${CLAUDE_SKILL_DIR}/references/github-posting-rerun.md` when a prior `/review-pr` review or cache entry exists for this PR, and `${CLAUDE_SKILL_DIR}/references/github-posting-recovery.md` if any posting phase fails.

Pass into the reference: `<owner>`, `<repo>`, `<pr-num>`, `<head_sha>`, `CURRENT_ROUND`, `IS_SELF_REVIEW`, summary body content, the complete surviving finding list (line-level + file-level), `PRIOR_STATE` (Step 0c in the rerun file compares against it), `$CACHE_FILE` path, `$STATE_FILE` path, and the `/review-pr` invocation as the posting authorization source.

### Convergence handoff

After authoritative posting and write-back, invoke `converge-reviews` with the PR request, base/current head and diff hash, reviewed paths, reviewer roster and lenses, current findings and dispositions, and `$STATE_FILE`. Store the resulting `convergence` block in that existing state file without replacing `review-pr`'s finding state. Apply its result contract before recommending another review round or declaring the review converged.

---

## Error handling

- **`gh` not installed/authed** → fail fast: `Run 'gh auth login' and retry.`
- **Invalid PR URL** → `Couldn't parse PR URL. Expected: https://github.com/owner/repo/pull/NUMBER`.
- **PR not accessible (404 / GraphQL error)** → `Couldn't access PR. Check repo access; try 'gh auth refresh -s repo'.`
- **PR is closed/merged** → warn but proceed (post-mortem review).
- **PR is a draft** → note in output header, proceed.
- **PR has no changes** → short-circuit (Phase 1).
- **Phase 2 subagent failure** → continue with remaining; abort only if ALL fail.
- **Network errors on `gh`** → surface, don't silently fall back.
- **Review event permission denied** → surface the GitHub error and stop. Use `COMMENT` only when Phase 1 established `IS_SELF_REVIEW=true`; never downgrade another author's review after a permission failure.
- **Failed state-file write** → log warning, do not block posting. State file is best-effort persistence.
