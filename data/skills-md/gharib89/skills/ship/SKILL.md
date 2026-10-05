---
name: ship
description: Drive one tracker issue to a merge-ready PR in a single run, stopping only at the human merge gate. Use when the user wants to ship an issue, or to run the unattended lane.
argument-hint: "[issue-number] [--unattended]"
metadata:
  version: 0.16.4
  profile-schema: 3
  composes: mattpocock/skills#d81f3a183412e71a5b1e84ca21bc1a35eea03a60:tdd mattpocock/skills#c55ee46073ed923f86ce59a5eb3b6d895095d1b7:writing-for-agents mattpocock/skills#c55ee46073ed923f86ce59a5eb3b6d895095d1b7:code-review upstash/context7#e275a848a420e0d11c2822f61201ee005bfd1133:find-docs humanlayer/skills#ca7c8088db69e315a8b2deea43820270457f8f3c:show-me
---

# ship

Drive one issue from nothing to a **merge-ready PR**, hands-off, stopping only
at the merge gate, so the human runs `/ship <issue>`, walks away, and comes back
to a PR implemented test-first, verified against the real thing the repo
integrates with, self-reviewed, reviewed by every reviewer the repo names,
CI-green, and summarized for a ten-second approve. This skill is **generic**: it
knows how to ship and nothing about the repo, and every repo fact comes from the
**ship profile**, `docs/agents/ship.md`. The copy under `.claude/skills/ship` is
a **derived copy**, changed in its source repo `Gharib89/skills` and refreshed
through the command the repo's `### Ship` block in CLAUDE.md carries.

**Version.** The harness strips this file's frontmatter on load, so read the
version once, at the start of the run, with
`sed -n 's/^  version: //p' <base directory>/SKILL.md`, then print
`ship <version>` in the run header, the first line of the first reply, and again
in the merge summary, so every PR records which ship produced it.

## Argument and flags

`$ARGUMENTS`:

- `<issue>`: the issue number (work item id on Azure DevOps); `prepare` alone
  takes none. Omitted with no flag: ask which issue.
- Free text instead of a number: the task spec itself. No issue fetch, claim,
  `Closes` or reflect, nor the `Done when:` clauses naming them; `none` is the
  issue argument to `preflight`, `isolate`, `open-pr`, `merge` and `cleanup`.
- `--unattended`: the **unattended run**, detailed in
  [reference/unattended.md](reference/unattended.md). No human is present: a
  blocked stop hands back instead of asking, the sandbox clone is the isolation,
  and the merge gate posts the summary as a PR comment and returns. With no
  `<issue>` it first runs the unattended lane: prepare, PR cap, select.

Without `--unattended` the run is **attended**: any needed human action stops
and asks, and the claim holds while it waits. **Preparation**, before `run-file
init` in every run but the no-issue lane's inner one: `prepare` (`--unattended`
in that lane). In a **cloud sandbox** (`CLAUDE_CODE_REMOTE=true`), or with that
flag, it runs `tooling --install` then the profile's `## Cloud lane`
`Bootstrap:`, elsewhere a no-op. A `failed` step stops the run, no claim, with
its tail: `tooling` as `host-unreachable`, `bootstrap` as `bootstrap-failed`.

## Compose, don't reinline

Load `tdd` (phase 2), `writing-for-agents` (phase 4, agent-facing docs),
`code-review` (phase 4) and `find-docs` (any API claim) through the Skill tool
when their moment comes, taking each one's logic from the skill itself, and tell
any composed skill with an unattended mode that the run is unattended,
explicitly, because it has no other way to know. **Read** `show-me` (phase 6,
the Change outline) instead; [pr-body.md](reference/pr-body.md) says why. The
frontmatter's `composes` line names all five, each pinned at the upstream commit
ship was tested against (`<owner>/<repo>#<sha>:<skill>`), and is what phase 0
checks: a skill added here is added there too.

## The pipeline

Work the phases in order, keeping the main thread on orchestration and
decisions. **First**, read
[reference/context-discipline.md](reference/context-discipline.md): the
delegation rule, the levers that keep a long run from bloating the window, and
your **required first action, the Run file** holding the ten-item checklist.
Each phase below flips it with `run-file open`, `close` or `skip`, and closes
once its `Done when:` holds, not before.

**A phase runs the mechanic it names**, rather than re-deriving what that
mechanic wraps. **Every host write, and every gating read, goes through a
mechanic**: one no mechanic performs is a **Ship defect** for the merge
summary's `Ship defects:` row, never a hand-rolled call; merge-gate.md says
where its draft goes. [reference/mechanics.md](reference/mechanics.md) carries
the rule in full, the informational reads it admits, the mechanic each phase
runs and the contract they share, `--help` included.

**0 · Isolate.** [reference/isolate.md](reference/isolate.md) carries what
preflight proves and refuses, the profile it loads and why the worktree is made
the way it is. Run `preflight <issue>` (`--unattended` in an unattended run):
every `reasons` entry is a row of the stop table below, and a push-permission
`unknown` on stderr is carried to the merge summary rather than a stop. Then
`read-issue <issue>`, phase 1's input, from which the branch `<type>` (`feat`,
`fix`, `docs`, ...) and `<slug>` are derived. Then `isolate <issue> <type>
<slug>` with the profile's `Carry:` files, or `isolate ... --in-place`
unattended. Every edit, commit and the PR happen from the path `isolate`
printed, and you **commit as you go**, because the PR needs real commits. A
`Bootstrap:` under `## Worktree` runs once here, after isolate.
**Done when:** `preflight` answered `ok: true`, `isolate` printed its path, and
any `## Worktree` `Bootstrap:` ran green.

**1 · Understand.** Too vague to plan from the `read-issue` result: stop
`ambiguous`, with no claim taken. Otherwise **claim before any work**:
`manage-issue <issue> take`, held until merge; later stops follow the stop
table. Then **grep each anchor** the issue cites, rewriting one the tree
contradicts ([implement.md](reference/implement.md)), and only then write what
success looks like into the Run file as criteria a later phase can check; a
later authoritative comment supersedes the body (**spec precedence**).
**Done when:** `claim: taken`, anchors grepped, the Run file holds the criteria.

**2 · Implement.** [reference/implement.md](reference/implement.md) carries the
classes, the TDD override, external-claim probes, the judgment/execution split
and the adjacent-find dispositions. Classify `docs` / `code` / `infra`;
**announce the class, the skip path it implies, whether the three lane keys
hold**, and the applicable verifications from `## Verification` (their `Applies
when:` lines are prose you judge here). Then implement test-first per class;
`Tripwires:` and `In-PR requirement:` land in this change whatever the class.
Keep a **deviations log** from the first edit: whenever the territory forces a
departure from the issue, brief or plan, take the conservative option, log what
and why, keep going; it lands verbatim in the merge summary. If the diff
outgrows one PR, or the fix demands a redesign the issue did not scope, stop
`needs-split` with a split proposal.
**Done when:** the applicable tests are green (red first, per class), the
tripwires and in-PR requirement have landed, a small-lane diff is counted under
the cap, and every departure and adjacent find so far is in the Run file with
its disposition.

**3 · Verify.** [reference/verify.md](reference/verify.md) carries the result
words, the `Without it:` dispositions and what `unexercised` is. Run each
applicable verification's `Run:` line **scoped to what you touched**, on the
environment the issue was reported against: green elsewhere is not fixed. Noisy
runs go to a cheap-tier subagent in the `verify` scratch directory. `docs` class
and the small lane skip this phase.
**Done when:** every applicable verification carries one result word, or
`run-file skip 3` recorded what skipped it.

**4 · Sync docs, then self-review.** Docs first, so the review reads the docs
edits as part of the diff. **Docs-sync fires only when the public surface or
observable behavior changed**: bring the profile's `Targets:` in line, folding
the edits into this change, a tracker issue's as a
[drafted section](reference/merge-gate.md#a-tracker-issue-on-targets). Skip it
for internal refactors, a bugfix restoring documented behavior, test-only or
tooling changes, and comments, and say so in one line at the merge gate.
**The `writing-for-agents` pass has a trigger of its own**, firing even where
docs-sync is skipped: whenever the diff touches a target on the profile's
`Agent-facing:` line, at the judgment tier, in the `writing` scratch directory,
over every agent-facing file in the diff. Human prose takes the mechanical pass.
With docs-sync's edits landed, load `code-review`, then dispatch this pass and
its two axes in one turn and end it, each naming its Report file. Small lane:
dispatch the axes, then run this pass inline.

**Self-review**, unconditional in every lane: invoke `code-review` against the
diff since `origin/HEAD`, its Standards axis reading the profile's
`## Coding standards` path, its Spec axis reading the issue, each axis prompt
carrying its own scratch directory (`standards`, `spec`) and saying the Local
gate runs later in the run, so the axis reads the gate's JSON and never runs
`check.sh full` or the suite itself. **Triage waits for every Report file**; one
that fails to arrive after the bounded retry is `red-after-retry: <axis>`, never
a disposition written from memory.
**Auto-triage** every finding: harden rather than rip out capability, verify
nits against the pinned versions, reject known non-issues, fix the valid ones,
and record a one-line disposition per finding. Two rails on rejecting: a claim
about **what exists in the repo** is checked against `origin/HEAD` rather than
the worktree, which may predate a merge; and a finding's **evidence and its
claim are separate**, so a reviewer citing the wrong commit for a real primitive
is still right. A valid finding outside the issue is an adjacent find. Then read
the diff yourself against the depth checks in the coding-standards file the
Standards axis reads, by their leading words: a vocabulary the change extends, a
rule-shaped prose change, new pattern-matching code, a new test run with its fix
reverted, a fix landed after review, and any the repo adds beside them. Reviewer
rounds find these otherwise, serially, at the cost of most of a run's wall time,
and the reverted-fix one escapes them entirely. This self-review plus green CI
is the review gate.
**Done when:** every report that fired has its Report file on disk and its path
in the Run file, every finding carries a disposition, and docs-sync landed or is
skipped in one line.

**5 · Local gate.** *Precondition:* every applicable verification is `pass`,
`deferred-to-ci` or `unexercised`, or the class is `docs`, **and** every phase-4
finding carries a disposition; otherwise go back. A gate run while `code-review`
is still out is paid twice when a finding lands. Run `base-fresh` first: CI
tests the merge ref, so a branch that predates a merge still goes green while
every "does this exist?" answer taken from the worktree was pre-merge; behind:
follow its advice, re-run, continue. Confirm every `Carry:` file still matches
the main checkout's copy; a difference is `carried file modified`, because ship
has no business editing untracked secrets. Then run the gate at the profile's
`Location:` from the worktree, inline (small lane: small-lane.md). Its verdict
is one JSON object: `verdict` `pass|fail|unavailable`, per-gate statuses
`pass|fail|deferred-to-ci|unavailable`, and `gates.secrets` in every lane;
unparseable output or a missing `secrets` key reads as `unavailable`. `fail`:
fix loop. `deferred-to-ci`: proceed, the merge summary naming each deferred
gate. `unavailable`: stop `local gate unavailable`, the PR unopened.
**Done when:** `base-fresh` answered `fresh: true`, the `Carry:` files match,
and the gate reads `verdict: pass` with `gates.secrets` present.

**6 · Open PR.** [reference/pr-body.md](reference/pr-body.md) carries what the
body holds and how it is written and read back. `open-pr <issue> --title
--body-file`, **non-draft** (drafts may not trigger a reviewer). Title: a
Conventional-Commit subject derived from the issue, honouring `Subject
constraints:`; it becomes the squash subject release tooling reads, and one that
later proves wrong is fixed with `update-pr-title`. **Every title or body write
to an open PR ends with `read-pr <pr>`**, its `## ` headings checked against the
ones the body owes. Then `reflect <issue> <pr>`.
**Done when:** `read-pr` shows an open, non-draft PR carrying the headings the
body owes, and `reflect` posted.

**7 · Reviewers.** [reference/review-loop.md](reference/review-loop.md) carries
the round per trigger, the cap as a budget, reading a round, the exit lines and
fallbacks. Best-effort: for each reviewer under `## Reviewers`, per round, start
it by its `Trigger:`, wait out one `poll-pr --brief` window, triage whatever
landed, push the fixes once, answer each thread with `reply-thread`, then the
block's `Resolve:`; `Cap:` bounds the rounds. **Every reviewer whose
`Fallback-for:` reads `None.` first, then the fallbacks.** Exits: `reviewed`,
`not reviewed: <reason>`, or `not invoked: <primary> reviewed`; `not reviewed`
proceeds to the merge gate on green CI and is reported there. At exit,
`update-pr-body --section` writes the sections the rounds grew, `Review` last,
then the phase-6 read-back.
**Done when:** every reviewer carries an exit word, every thread `poll-pr`
returned is replied to and resolved per `Resolve:`, every section the rounds
grew is rewritten, and `read-pr` shows a `## Review` line per reviewer.

**8 · CI.** CI runs from PR-open and overlaps phase 7; `ci-wait <pr>` covers it,
reading the profile's `Legs:`. `ci-wait` and `poll-pr` wait for the expected
head, `--sha <sha>` else the worktree's `HEAD` when it is on the PR's branch, so
a read straight after a push never grades the previous head. A `timeout` whose
`head_sha` is not that head means the host never showed the push: confirm it
landed, then re-run. On `conflict`, its stderr carries the recovery.
`no-checks` is fine only where `No-checks legal:` says so. A red leg named on a
verification's `Also proven by CI:` line is that verification failing: back to
phase 2. Red after the reviewers exited: fix, push, proceed on green. Honour
`Push policy:`: a push spends CI minutes and review quota, so push when the tree
changed.
**Done when:** `ci-wait` answered `green` with every leg on `Legs:` among its
`checks`, or `no-checks` where `No-checks legal:` admits it.

**9 · Merge gate.** [reference/merge-gate.md](reference/merge-gate.md) carries
the summary's shape, what `merge` does, its two refusals and the tracker drafts.
**Hard stop.** Write the summary per that file, uncompressed. Attended: post it
in the conversation and wait for an explicit "merge": the word is exact, and a
near miss is asked back. On approval run `merge <pr> <issue|none> [--worktree
<path>]`, `update-issue-body` per tracker draft, then `cleanup <issue|none>`,
and a Ship defect draft is filed only on a word of its own; a nonzero
exit, or a `false` in `merge`'s or `cleanup`'s JSON, re-runs the mechanic that
owns the step, and a step no mechanic re-does is a Ship defect for the summary.
Unattended: `comment-pr <pr> --body-file` with the summary. Either lane then
closes the phase, `run-file close 9` and its task to the `mirror`, and returns.
**Done when:** attended, `merge`, every `update-issue-body` and `cleanup` exited
0 with no `false`, and every Ship defect draft is filed, answered with
candidates, carries its `command` on the row, or was declined; unattended,
`comment-pr` posted.

## The stops

One guaranteed stop, the **merge gate**: merging is effectively irreversible, so
a human says merge and ship merges on that word alone, never on its own or
through an auto-merge flag. Two conditional pauses in an attended run: the
`ambiguous` stop (phase 1) and a **hand-off** (phase 3). Everything else,
triaging your own findings, fixing, re-running, is autonomous. Two guardrails
hold around that:

- **Red is fixed or reported.** Any failure before the merge gate gets at most
  two fix-and-retry attempts; still red after the second is `red-after-retry:
  <what>`, and a failure saying the approach is wrong stops sooner. Either way
  **stop and report** with the concrete evidence and, if cheap, a
  verified-working alternative, so the report is a fast yes.
- **Every stop has a name**, reported verbatim, with the claim action below. A
  sibling maps the name, a human reads it.

| Stop | Reason | Claim |
|---|---|---|
| Profile missing or invalid, host unreachable | `profile missing`, `profile invalid: <detail>`, `host-unreachable` | no claim |
| A skill ship composes is not installed at its pin, or its pin is malformed | `skill missing: <skill>; run <install line>`, `skill off pin: <skill> at <ref>, pinned <sha>; run <install line>`, `skills lock unreadable: skills-lock.json; repair it, then re-run preflight`, `composes pin invalid: <entry>; want <form>` | no claim |
| Preflight not actionable | `closed`, `is a pull request`, `already claimed`, `existing PR`, `existing branch`, `worktree exists`, `not triaged: run /triage first`, `ready-for-human: attended only` | no claim |
| Issue too vague to plan | `ambiguous` | no claim |
| Change outgrows one PR, or needs a redesign the issue did not scope | `needs-split` | attended: ask; unattended: hand back |
| A find shows the issue is mis-specified | `mis-specified` | attended: ask; unattended: hand back |
| Verification prerequisite missing | `hand-off` (attended waits, claim holds) / `blocked-verification` | attended: hold; unattended: hand back |
| Local gate verdict `unavailable` | `local gate unavailable: <gates>` | attended: ask; unattended: hand back |
| Carried file changed | `carried file modified: <file>` | attended: ask; unattended: hand back |
| Red after retries | `red-after-retry: <what>` | attended: ask; unattended: hand back |
| The branch fell behind its base before the merge | `stale-base: behind <n> on <base>` | attended: holds while you merge the base in; unattended: hand back |
| The PR is closed at the merge gate | `pr-closed: <state>` | attended: ask; unattended: hand back |
| `prepare` failed its Cloud lane `Bootstrap:` | `bootstrap-failed` | no claim |
| Open PRs at or above the profile's `PR cap:` | `pr-queue-full` | no claim |
| No issue passes selection | `nothing-ready` | no claim |
| The host's blocker query exists and failed | `blockers-unavailable` | no claim |
| Merge gate reached | none: the run's success | holds until merge |

Hand-back is `manage-issue <issue> handback "<reason>"`: unassign, drop
`ready-for-agent`, add `ready-for-human`, comment the reason; one that exits 1
says on its own output what the claim is left as. In an attended run you stop
and ask, and hand back only if the human says stop, to the human queue: never to
the agent queue, which loops forever.

## The lanes

Every run is **full lane** until the change proves it **small**: all three keys
hold, asserted by you at phase 2 and announced with the class. When unsure, it
is not small.

1. **No public-surface change.** The public surface is the profile's
   `## Public surface`; `Default.` means the exported or published API, CLI
   flags and exit codes, config schema, file formats and documented behavior.
2. **Provable without the real thing.** A unit or regression test fully proves
   it, or the class is `docs` and there is no behavior to test; either way no
   verification in the profile's `## Verification` applies.
3. **Contained.** No new dependency, none of the profile's `Tripwires:`
   fired, and the diff inside the size cap small-lane.md counts.

Behavior change is allowed: a bugfix is one. Small: read
[reference/small-lane.md](reference/small-lane.md) before continuing. Its floor
is the same in every repo, and the lane revokes one way only.

## Model tiers

Use the cheapest model that fits; reserve the strong tier for judgment. Tag
every subagent with a model explicitly and with its scratch directory
([reference/context-discipline.md](reference/context-discipline.md)); neither is
inherited.

| Work | Model |
|---|---|
| Investigation and mapping | haiku |
| Phase-2 **execution** from a settled plan; mechanical edits and fixes; the docs-sync pass on human prose; the `code-review` skill's **Spec** axis | sonnet |
| Phase-2 **judgment** (classification, plan, design, the implementation brief); triage of every finding; the `writing-for-agents` pass; the `code-review` skill's **Standards** axis | opus |

When you invoke `code-review`, tier its two axes yourself. Fall back to the
nearest available tier rather than running everything on one model.

## Working standards

These bind every edit a run makes, in every repo, regardless of a personal
`~/.claude/CLAUDE.md`, `~/.claude/rules/` or personal skills:

- **Simplest shape that solves the problem.** No speculative features,
  configurability or abstraction for single-use code; if the diff could be a
  third the size, rewrite it.
- **Surgical.** Touch only what the issue needs, every changed line tracing to
  it or to a logged deviation, matching existing style, leaving adjacent code,
  comments and formatting alone.
- **Root cause, not symptom.** No temporary patches, no swallowed errors, no
  `TODO` standing in for the fix; if the real fix is out of scope, say so and
  file it.
- **Comments record the why.** Document public APIs and non-obvious
  constraints, invariants and workarounds; skip narrative comments on internals.
- **Concise PR body, always the why.** State what changed and why; the reader
  has the diff for the how. The merge summary is exempt: write it uncompressed.

## Consult current docs

While implementing (phase 2) or triaging findings (phases 4 and 7), verify API
claims against **current** docs through the `find-docs` skill and the extra
`Sources:` the profile names. For every library on the profile's `Pinned:`
line, read the installed version from the repo's manifest and confirm the claim
against that version before acting on it; a remembered API the installed
version lacks is a regression.
