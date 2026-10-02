---
name: finish-it
description: "Take a spec, issue, branch, or pull request through implement-publish, review-code-publish, and rounds of resolve-review, each step in a fresh subagent, resuming from wherever the pull request already is. Invoke only when the caller asks for finish-it by name."
disable-model-invocation: true
---

# Finish it

Run one **delivery**: take a spec source to a pull request whose latest published review reflects its current head after at least one round, or after the delivery's own first review when that review approves with nothing to address. Every step runs in its own fresh-context subagent; the forge is the only shared memory, so nothing is persisted on disk and re-invoking this skill on the pull request resumes the delivery from wherever the forge says it is.

Three terms carry the skill:

- **Spec source**: the issue, tickets, or written specification the pull request implements.
- **Round**: one `resolve-review` pass over the pull request's feedback, skipped when there is nothing to address, followed by a `review-code-publish` re-review.
- **Delivery**: the whole run, entered at any step of the chain.

## Boundaries

Invoking this skill authorizes every write the underlying skills make on its behalf: creating an issue from a prose spec, opening the pull request, publishing reviews, replies, thread resolutions, and addressing summaries. It never merges, never closes an issue, and leaves labels and assignees alone.

The delivery runs unattended. Questions the underlying skills would put to a user land on the pull request instead; a stop names the step and its reason.

If `implement-publish`, `review-code-publish`, `resolve-review`, or `review-code` is not among the installed skills, stop with `missing-dependency: <name>` before any write. Check all four first. `review-bot` is optional; its absence is a recorded fallback to the authenticated user with gating withheld, never a missing-dependency stop.

## Process

### 1. Settle the inputs

Read `docs/agents/issue-tracker.md` when present. Record:

- **N**, the requested round total: the integer in the invocation text (`rounds: 5`, "with 2 rounds"), otherwise 3. `0` is allowed.
- The **base branch**: the one the caller names, otherwise the repository's default branch.
- The **author identity**: the forge login this session writes code, pull requests, replies, and addressing summaries as (`gh api user --jq .login`).
- The **reviewer identity**: resolve once here from `docs/agents/issue-tracker.md`, which declares **Reviewing app** and **Client id**, or an optional literal **Review-token command**. Use a literal command as-is without consulting `review-bot`, reading the login with `GH_TOKEN=$(sh -c '<review-token command>') gh api graphql -f query='{viewer{login}}' --jq .data.viewer.login`; `gh api user` is refused for an app token. A command that is absent, that fails, or whose token cannot authenticate is not an error. For an app without a literal command, invoke `review-bot`'s Resolve entry point when installed with the client id and the delivery's target repository as `<owner>/<repo>`: the repository that owns the base branch, and the pull request's base repository once one exists, never the checkout's remote. Retain its returned login and command verbatim. If the skill is absent or returns any `unavailable` result, or the literal command fails, use the author identity, record the reason in the report and packet, and withhold gating. Resolution never stops the delivery. With no app or command declared, use the author identity. A token refused at publication still stops that write.
- **Gating authorization**: authorized exactly when the reviewer identity is a reviewing app distinct from the pull request's author, which is what lets the review carry `APPROVE` or `REQUEST_CHANGES`. Withheld on the author-identity fallback, where the review publishes `COMMENT` under the self-review rules. Record the decision here; a subagent never infers it.
- The **nested reviewer tier**: the name in `reviewer tier: <name>` when the invocation supplies one, otherwise unset. An unset tier lets each underlying skill's dispatch select its own tier. A named tier overrides that selection and each step passes it through to its reviewer dispatch. Every dispatch states the tier it selected explicitly.

A base or spec source the caller left ambiguous is settled here, never inside a subagent, which has no user to ask. If it cannot be settled, stop before any write.

### 2. Locate the delivery

Read the forge and pick the first step from the entry table. A bare number is a pull request first and an issue second, as the issue-tracker doc says.

| Observed state | First step |
|---|---|
| prose spec | create the issue, then the issue row |
| issue with no open pull request closing it | implement |
| issue already closed-by an open pull request | that pull request's row |
| current branch with commits, no pull request, no issue | implement, letting `implement-publish` infer the spec from branch and commits |
| pull request with no review at any head | review, then rounds |
| pull request whose latest review is not `Approved` at the current head | rounds |
| pull request whose head moved since the latest review, or with an addressing summary newer than the latest review | review, which finishes the pending round uncounted, then rounds |

Notes for reading a pull request:

- "Latest" is by forge timestamp, a comment's last edit when it has one, across reviews from any identity and addressing summaries. A human review is a review.
- A pull request with no linked issue is reviewed from its own text; `review-code` handles that.
- An issue's open pull request is found by `gh pr list --state open --search "<number>"` and confirmed by a closing reference in the body.

**Creating the issue** from a prose spec: `gh issue create` with a one-line title you write and a body that is the prose verbatim under a `## Spec` heading, no labels or assignees. Read the issue back; its number is the spec source for every later step.

**Counting completed rounds.** D is the number of general pull-request comments carrying an `<!-- addressed head=... -->` trailer or opening with `**Addressed** at`, any identity. Rounds remaining = `max(1, N − D)`. Record D and the remaining count.

### 3. The handoff packet

Every subagent receives the same packet and nothing from earlier steps: the repository path, base branch, head branch, pull request URL, issue URL or spec source, round number and rounds remaining, author identity, reviewer identity and the resolution result from step 1, including any fallback reason, the returned or literal review-token command when one applies, the gating authorization from step 1, and the named nested reviewer tier or its unset state. The review subagent never sees the resolver's report; the resolve subagent never sees the review as text. Both read the forge.

Dispatch each step as one **general-purpose** subagent in a fresh context that inherits none of this conversation; use `fork_turns="none"` or the host's equivalent. General-purpose because each underlying skill dispatches its own reviewer or verifier; types without the `Agent` tool are unsuitable. State the tier the dispatch selected, and run it on an awaited route, a foreground dispatch or supported join whose tool call returns the completed report while this session stays active; an acknowledgment or agent id is not a return. The forge is read for the step's artifact only after the subagent returns. Brief it to invoke the named skill by name with the packet, to pass through a named nested reviewer tier or let the underlying skill select one when the field is unset, to wait for every subagent it dispatches to return on an awaited route chosen before each dispatch or continuation — a report that leaves its own reviewer or verifier running has not finished the step — and to return its final report.

A subagent's report is a claim. After each step, read the forge for the step's **artifact** before continuing. A missing artifact, a report that leaves the step's own subagent pending (`early-handback: <step>`), an underlying skill's named stop that the step's artifact rule does not accept, or an unresolvable spec source or base branch is a failed step, and a failed step ends the delivery with a report naming the step and its reason, plus the affected phase, the pending agent id when available, and the missing artifact: no step is retried, and none is skipped. The orchestrator's own forge writes are attempted once; on an ambiguous result read the target before a single retry, then report the failure rather than writing again.

### 4. Implement

Brief the subagent to invoke `implement-publish` with the spec source, base branch, and current branch from the packet.

Artifact: exactly one open pull request whose head is the branch. Record its URL and head SHA into the packet.

### 5. Review

Brief the subagent to invoke `review-code-publish` on the pull request with the spec source.

Artifact: a review by the reviewer identity whose reviewed head is the pull request's current head. Compare logins with a trailing `[bot]` ignored on both sides: GitHub's REST records carry the suffix its GraphQL `author.login` omits, so an unnormalized compare never matches an app's own review. `review-code-publish`'s `duplicate-review` stop names such a review already there, so it is a successful review step; read that review from the forge. Record the status, open questions, and disputed findings.

### 6. Rounds

When this delivery ran step 5 and its review is `Approved` at the current head with the empty ledger check below holding, run no rounds and report: a re-review of an unchanged head with nothing to address can only repeat it. Otherwise, repeat for each remaining round, in order:

1. **Empty ledger check.** At the current head, the latest review is `Approved`, lists no open question and no disputed finding, and no review thread is unresolved or holds feedback without a reply from the pull-request author. When all hold, skip the resolve and go to the review; the round still counts.
2. **Prepare the checkout.** Fetch, confirm the working tree is clean, and check out the pull request's head branch at its live head. A dirty tree is a stop, not something to clean up.
3. **Resolve.** Brief the subagent to invoke `resolve-review` on the pull request. Artifact: an addressing summary this pass posted, or the existing same-head summary it updated, its last edit later than the review this round addressed, carrying an `addressed head=` equal to the pushed head, which equals the local head. Record whether the round added commits.
4. **Review** as in step 5, on the new head.
5. **Count the round**, then, from the second round of this delivery on, stop early when the review reached `Approved`, or when the round made no progress: no commits added and the review's only unsettled items are disputed findings or questions waiting on a person. Once rounds start, the first round of a delivery always runs, a pull request that entered already `Approved` included.

### 7. Report

Finish with the pull request URL and head SHA, the final review status, rounds run this delivery and D found at entry, disputed findings, open questions, and any step that stopped with its reason. Every file coordinate is the forge's immutable link at the reported head.
