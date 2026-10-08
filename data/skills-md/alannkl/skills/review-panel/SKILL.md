---
name: review-panel
description: "Panel review of any chosen scope: a review brief, parallel reviewer model voices (presets standard/max/ultra), merged findings, triage, and optionally fixes and verification. Fixes are user-gated by default; an upfront auto-fix option approves them. Spawns several fresh agent sessions, so cost scales with the preset; strongest with multiple harnesses installed (claude, codex, cursor), falls back to one."
disable-model-invocation: true
---

# Review panel

Run the pipeline: scope → brief → panel → merge → triage → findings report → approval gate → fix → verify → final report.

Set the **approval mode** when the run starts. The default is **gated**. `/review-panel auto-fix` sets **auto-fix**, which grants standing approval for findings triaged with a **fix** disposition. Auto-fix never selects an **escalate** fork; escalations always require a later user decision.

## 1. Scope

Resolve one review scope for the whole panel with `code-review`'s bundled resolver, run by absolute path from inside the repository, with `<code-review-dir>` for that skill's installed directory: `python3 <code-review-dir>/scripts/resolve-scope.py [--scope <spec>]`. Use a user-named scope exactly, without adjacent changes: pass a commit, a range, `staged`, or `worktree` (unstaged and untracked) as `--scope`; a branch as `<base>...<branch>`, since a bare branch name is its tip commit only; and a pull request as `<base>...<head>` after fetching both refs. A supplied diff file or named files are the scope as given. Without `--scope`, the resolver takes the first non-empty of staged changes; unstaged and untracked changes; commits ahead of the upstream; or the current branch against its merge base with the default branch. Exit 1 means nothing to review: stop and say so. Exit 2 means a bad ref, multiple merge bases, an unreadable file, or an unwritable output directory: fix the cause or resolve the scope by hand. Give every voice the printed `scope` and `diff` path, and put the printed `excluded` files in the brief so no voice flags code that is mid-edit.

## 2. Brief

Collect the acceptance criteria from the conversation, ticket, or commit messages. Write the **review brief** to the scratchpad. Include the intent, requirements satisfied, deliberate trade-offs, known limitations, and declared non-goals, stating trade-offs and non-goals as claims with their basis. Keep it to one page. Scope exclusions belong in the brief; verdicts do not: never tell a voice what not to flag or cap a severity — triage decides. The brief is done when a stranger could reject an out-of-scope finding by citing it.

## 3. Panel

Assemble the reviewer **voices** from the preset the user named (`/review-panel max`), the exact composition they specified, or the default `standard`. A composition the user spells out overrides every preset. Fresh eyes come from the context, not the model. A fresh context using the parent's model is still a fresh reviewer.

Roster, ranked by capability:

| Rank | Member        | Harness | Sibling |
| ---- | ------------- | ------- | ------- |
| 1    | fable 5       | claude  | opus 5  |
| 2    | codex 5.6 sol | codex   | terra   |
| 3    | opus 5        | claude  | fable 5 |
| 4    | grok 4.6      | cursor  | kimi k3 |

Ranks 3–4 are reserves. They enter as siblings, as fallback rivals, or as `ultra`'s second rival.

Resolve three roles relative to the **parent**, meaning this session's harness and model:

- **rivals**: the highest-ranked members on harnesses other than the parent's, in rank order. `standard` and `max` use the first rival; `ultra` uses the first two. With no other harness installed, the sibling stands in as rival; with a single-model harness, the twin stands in.
- **sibling**: the strongest model on the parent's harness other than the parent's own; the roster lists each member's. With a single-model harness, the twin stands in.
- **twin**: the parent's own model in a fresh context.

The parent always runs `code-review` inline on the resolved scope (the **parent voice**), plus the preset's fresh voices:

| Preset               | Fresh voices                                                                |
| -------------------- | --------------------------------------------------------------------------- |
| `standard` (default) | code-review: rival · adversarial: rival                                     |
| `max`                | code-review: rival, sibling · adversarial: rival, sibling, twin             |
| `ultra`              | code-review: both rivals, sibling · adversarial: both rivals, sibling, twin |

Step 7 verification always goes to the first rival. With a fable parent in a full environment, the rivals are sol, then grok, and the sibling is opus. `standard` reviews with sol in both roles; `max` adds opus in both roles plus adversarial fable; `ultra` adds grok in both roles.

Rules:

- Every panel includes at least one `adversarial-review` voice in a fresh context; `adversarial-review` never runs in the parent context. A member named twice runs as two separate fresh contexts.
- **Effort.** Under `standard`, fresh voices run at high reasoning effort. Under `max` and `ultra`, they default to xhigh; fable and kimi k3 stay at high. Terra always runs at max. The parent voice keeps the session's own effort. The user can override any voice's effort.
- **Missing member.** When a preset or user-named member is unavailable, stop and recommend a composition built from the available members. Proceed only after the user chooses. The prescribed rival fallback chain needs no confirmation.
- Route a voice whose model runs on the parent's own harness through the harness's builtin subagent tool if it has one; route every other voice through `spawn-agent`. Either way, pass the reviewing skill's `SKILL.md` path in the prompt as its charter. Tell the voice to perform the review itself, without spawning agents or invoking `review-panel`.
- The user may name members beyond the roster: any harness or model the environment can run. For a harness `spawn-agent` has no reference for, run a headless CLI session by that harness's own conventions (its `--help` is the source of truth); if it cannot be run, treat it as a missing member.
- Before launching, report the resolved scope, the intent from the brief, and the panel composition to the user. Report and continue; do not wait for approval.
- Send every voice the same scope and brief verbatim. Launch the fresh voices in parallel and run the parent pass while they work. Collect every report unedited; do not soften or pre-judge findings. On a re-run over the same scope, pass the previous run's final report to every voice as prior findings.

## 4. Merge

Merge the reports into one findings list. Collapse findings with the same root cause and remedy into one, listing every affected location; keep independently actionable defects separate. Keep the highest severity, the most concrete failure scenario, and a **concurrence** tag (`flagged by 2/3 voices`). Origin carries no weight. The parent voice's findings count like any other, while concurrence signals credibility and feeds triage's confidence. Merging is done when no two findings share a root cause and remedy.

## 5. Triage

Invoke `review-triage` on the merged findings inline in this session. Keeping triage here preserves the conversation, review brief, and any author context recovered during the review.

Present the complete triage report, including every disposition, proposed fix, and escalation fork.

In gated mode, follow the report with a **decision round** over every **fix** and **escalate** finding — the findings that need a user decision. Deferred and rejected dispositions stand as reported; the user can override one through the same round. Collect the decisions through the harness's multiple-choice question tool, one question per finding, batched up to the tool's limit; with no such tool, ask in prose. Each question carries the finding's case in its own text, so the user decides without scrolling back to the report:

- the problem, in one or two lines
- the proposed fix
- the fix's estimated cost: files and functions touched, rough lines changed, and any risk the fix itself introduces

A **fix** finding offers **approve fix** (marked recommended), **defer**, and **reject**; an **escalate** finding offers its A/B/C fork with triage's recommendation marked. A rejection needs the user's reason — take it from the free-text option or ask — and it travels with the finding into the final report.

In auto-fix mode, proceed with every **fix** disposition after presenting the report; if the report contains an **escalate** disposition, stop before any fix work and put its fork to the user through the same decision-round format. A `/review-panel` invocation without `auto-fix` authorizes review, triage, and the decision round; only the round's answers authorize fixes.

**Record durable decisions in the artifact native to each kind.** A rejection whose reason is local and non-obvious gets a comment at the finding's site stating the code's rationale — the confusion that produced the finding is itself a defect, and the comment is its fix. For a deferral, follow triage's planned comment or ticket; evidence-pending deferrals stay in the report only. A decided escalation gets an ADR when the repo keeps an ADR log. Scope rejections live in the final report only. Write each comment as the code's own voice ("validated at the parse boundary"), not as review history. Report the proposed recording edits and continue. Apply them only when the user's authorization covers those specific edits; approval of an unrelated fix does not authorize them. Otherwise leave them proposed in the report. They need no step 7 ruling.

If no finding has a **fix** or **escalate** disposition, the triage report and any recording edits the user approved complete the pipeline.

## 6. Fix

In gated mode, the decision round's answers define the approved set. In auto-fix mode, all **fix** dispositions are already approved. Apply the approved fixes as one batch, honoring triage's scope: nothing beyond the approved findings and escalation options. Unapproved findings remain pending.

Parallel fixers need isolation chosen by file overlap. Partition the batch into disjoint file-ownership lists before launching; only a clean partition may share the working tree, and each fixer edits only the files it owns. Overlapping files, or a fixer that needs destructive git operations (a mutation check that reverts a file), get sequential waves or per-fixer worktrees instead. On a shared tree, treat mid-flight full-suite results as noise — neighbors' half-edited files fail tests that are not failures; the gate that counts is one full-suite run on the assembled tree after every fixer lands.

## 7. Verify the fixes

Verification is a closed check, not a re-review. Send it to one fresh first-rival context, not the whole panel, and never to the parent: by this step the parent authored the fix batch, and an author's own `resolved` ruling is the one check that always passes.

Assemble the evidence in the parent so the verifier reads instead of re-derives:

- the approved findings, each mapped to the diff hunks that claim to fix it
- the fix diff
- the full-suite result on the assembled tree, which the parent runs before handing off

For each finding, require `resolved` or `unresolved` with concrete evidence, plus any blocking issues introduced by the fixes. Send unresolved and fix-introduced blocking findings through `review-triage`, present its report, and return to step 5's approval gate: gated mode runs another decision round, while auto-fix mode may take one further **fix** batch automatically. **Two post-fix verification passes is the cap.** Report findings still open at the cap instead of fixing them.

## 8. Report

Report:

- final verdict and fixes applied
- panel composition, with any substitutions
- findings left unapproved
- deferred and rejected findings, each with its evidence
- escalations and how they were decided
- anything left open at the cycle cap

The pipeline is complete when every approved finding is verified resolved or explicitly reported open. Recommend a fresh `/review-panel` run on the new state only when the fix batch resolved several high-or-critical findings or reworked a large share of the scope. The user re-invoking is the outer loop.
