---
name: ship-it
description: "Conducts a feature through the full build loop, plan, spec, tickets, implement, review, end to end across as many sessions as it takes, in any GitHub repository. Looks at what already exists for the feature (a map, a spec, tickets, a diff awaiting review) and states the one next step to take. Manual-only workflow: do NOT invoke automatically or unprompted; only activate when explicitly requested by the user via ship-it or /ship-it."
compatibility: Git repository, GitHub issue access (gh CLI), and a cross-platform shell.
metadata:
  disable-model-invocation: "true"
---

# Ship It

Conduct a feature through the full build loop, one phase at a time, across
however many sessions it takes: **Plan → Spec → Tickets → Implement → Review**

This skill is self-contained and tracks work as GitHub issues: everything it
needs lives in this folder and in the files it writes into the repo you run it
in. It doesn't call out to any other skill.

## Invocation & Harness Configuration

`ship-it` is designed as a manual-only workflow and should not be invoked automatically by models without explicit user request.

## Why a conductor, not one pass

A feature big enough to need all five phases requires rigorous separation of
concerns to prevent confirmation bias and enforce objective verification gates.
When a single session authors, implements, and reviews its own work in one
unbroken pass, it naturally suffers from authoring bias: rationalizing its own
assumptions, skipping verification, and confirming its own design choices.

Dividing the build loop into discrete phases—Plan, Spec, Tickets, Implement,
Review—establishes explicit verification gates at each handoff:

- Specs are verified against user requirements and adversarially audited before breaking into tickets.
- Ticket breakdowns require explicit user validation before creation.
- Implementation incorporates pragmatic, domain-aligned verification (recommending test-first Red-Green where automated test suites exist, or direct acceptance verification where they do not).
- Review evaluates diffs independently without the author's internal rationalizations.

This skill does not try to run the whole loop in a single reply. Each time you
run it, it works out where the feature currently stands and does **one** phase's
worth of work, then stops and tells you the next command. Run it again,
whenever, to keep going.

## Preflight, only when needed

`ship-it` assumes the repo is already set up: `gh` installed and
authenticated, a `github.com` remote, Issues enabled with write access, and
the `ready-for-agent` label and the `ship-it:*` type labels present (see
[references/preflight.md](references/preflight.md)). Normal runs don't check
any of this — skip straight to "Every run" below.

Run the checklist in [references/preflight.md](references/preflight.md) only
when the user explicitly asks (`ship-it preflight`, `/ship-it preflight`, or the equivalent in
conversation), or when an issue tool call during Orient or a phase fails in a way that
checklist covers (auth, rate limits, 403/500 errors, network errors, permissions, missing label, disabled Issues). Fix what's fixable, report the rest.

## Every run

### 1. Orient: which feature, which phase

If it isn't obvious from the conversation which feature is in play (the repo
may have several going at once), ask, and settle on that feature's **slug**: a
short, consistent identifier every issue for it carries in its title (e.g.
`auth-rewrite`, giving titles like `[auth-rewrite] Spec: ...`). A fresh
session with no conversation history just asks for the slug directly.

Once you have the slug, run one query per artifact type, in this order, and
take whichever comes back furthest along:

1. **Map**, not fully resolved:
   `gh issue list --label "ship-it:map" --search "<slug> in:title" --state open --json number,title,labels,state`
   (see [references/plan.md](references/plan.md))
2. **Published spec**:
   `gh issue list --label "ship-it:spec" --search "<slug> in:title" --state open --json number,title,labels,state`
   (see [references/spec.md](references/spec.md))
3. **Tickets** generated from that spec:
   Query tickets for the feature:
   `gh issue list --label "ship-it:ticket" --search "<slug> in:title" --json number,title,labels,assignees,state`
   and find the earliest unblocked, unclaimed ticket per the [Orient Discovery Algorithm](#orient-discovery-algorithm).
4. **An implementation in progress**, or a diff that hasn't been reviewed yet:
   check for an open PR referencing the slug or a matching branch, and for a
   ticket from step 3 that's assigned but still open (see
   [references/implement.md](references/implement.md) and
   [references/review.md](references/review.md))

#### Orient Discovery Algorithm

Find the earliest unblocked, unclaimed ticket:

- Filter out claimed (`assignees` non-empty) and closed (`state: "CLOSED"`) tickets.
- For open, unclaimed tickets, inspect each ticket's `## Blocked by` tasklist via `gh issue view <number> --json body` (and native dependency edges if present per the [Markdown Relationship Contract](references/tickets.md#markdown-relationship-contract)).
- Check blocker issue states via `gh issue view <blocker-id> --json state`. A ticket is **unblocked** if it has no blockers (or "None") or every blocker referenced in its `## Blocked by` tasklist has `state: "CLOSED"`.
- Take whichever unblocked, unclaimed ticket is earliest in sequence.

Each query above already asks for `labels`, so read them off the same
response rather than issuing a follow-up call: `ship-it:validated` on a map,
spec, or ticket set means it already passed the adversarial audit in
[references/validate.md](references/validate.md); `ship-it:reviewed` on a
ticket means its diff already passed independent review. Its **absence** on a
spec or ticket set that spans more than one session is the signal to validate
next — don't read a published artifact with no `ship-it:validated` label as
license to route straight past the audit into tickets or implementation.

Whichever of these is furthest along tells you the phase. Nothing existing at
all means the feature hasn't started.

**Orient error-recovery**: If any `gh` query fails during Orient (e.g. rate limit, 403, 500, network or authentication error), do **not** assume "nothing exists" or restart the feature from scratch—falsely assuming absence risks duplicating specs or tickets. Instead, treat the failure as an error and route to preflight ([references/preflight.md](references/preflight.md)) to diagnose and fix the environment before re-running Orient.

### 2. Route to the one next step

| Current state                                                                        | Next step                                                                                                             |
| ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| Nothing exists; the feature is well-scoped enough to hold in one session             | Read `references/spec.md`, write the spec directly. No map needed.                                                    |
| Nothing exists; the effort is genuinely too big or too foggy to scope in one sitting | Read `references/plan.md`, chart the map. Use the test in that file, not a guess, to decide "foggy" vs "well-scoped." |
| A map exists and isn't resolved                                                      | Read `references/plan.md`, resolve the next ticket on the map. One ticket per session.                                |
| The map is resolved (or planning was skipped) and no spec exists                     | Read `references/spec.md`.                                                                                            |
| A spec exists, lacks `ship-it:validated`, and the build spans more than one session  | Read `references/validate.md` and audit the spec before splitting it into tickets. This is the recommended default here, not a parallel option to skip in favor of speed; skip only for a genuinely small, well-scoped spec. |
| A spec exists, no tickets yet, and the build needs more than one session             | Read `references/tickets.md`.                                                                                         |
| A spec exists and the whole build fits in one sitting                                | Read `references/implement.md` directly against the spec; skip ticket-splitting. Validation (`references/validate.md`) is recommended even here unless the spec is trivially small. |
| Tickets exist, lack `ship-it:validated`, and haven't started                         | Read `references/validate.md` and audit the ticket set before anyone starts building. Recommended default whenever the set is big enough that a bad slice would surface mid-implementation; skip only for a small, obviously-right set. |
| Tickets exist and at least one is unblocked and unclaimed                            | Read `references/implement.md`, claim and build that ticket. Start a **fresh session** for it (see Context hygiene).  |
| A ticket is implemented (assigned, still open) and lacks `ship-it:reviewed`          | Read `references/review.md` in a **fresh session**, separate from whatever session implemented it.                    |
| A ticket carries `ship-it:reviewed`                                                  | Close out: comment resolution, close the ticket, open the PR or merge, per how the user works. If this is the final ticket of the spec, execute the [Feature Close-Out Protocol](#feature-close-out-protocol).     |
| Review found issues                                                                  | Route back to `references/implement.md`, in a fresh session, to address them, then back to `references/review.md`.    |
| Tickets exist but none are unblocked and unclaimed                                  | Report status (blocked or in-flight tickets) and stop.                                                                |

### 3. Report and stop

End every run with one line: which phase you worked, what you did, and, if
the feature isn't finished, the exact next thing to run. Don't silently chain
into the next phase in the same reply unless the user explicitly asked for the
whole loop at once.

### Feature Close-Out Protocol

When the final ticket of a spec is closed and reviewed:

1. Close the parent spec issue (and map, if one exists) with a resolution comment summarizing what was shipped (`gh issue close <spec-id> --comment "<text>"`).
2. Reference `Closes #<spec-id>` in the pull request description so merging the PR auto-closes the spec issue.

## Context hygiene

- **Plan → Spec → Tickets** benefit from staying in one unbroken conversation
  once planning has produced a clear destination: the thinking compounds. Not
  a hard rule, just worth naming if you're about to lose the thread.
- **Implement** should start in a **fresh session per ticket**. A ticket is
  self-contained by construction (see `references/tickets.md`), ensuring each
  slice is built strictly to its self-contained acceptance criteria and
  preventing context pollution and confirmation bias from earlier tickets.
- **Validate and review** strictly mandate the [2-Tier Context Isolation Protocol](references/validate.md#2-tier-context-isolation-protocol) rather than the authoring context; in-context persona simulation within an authoring session is strictly prohibited.
- If a session's context is growing large before a natural stopping point,
  that's the signal to wrap up and hand off, not to push through with degraded
  reasoning.

## Reference index

| File                                               | Read it when                                                               |
| -------------------------------------------------- | -------------------------------------------------------------------------- |
| [references/preflight.md](references/preflight.md) | A `gh` call fails, or the user asks to preflight the repo                  |
| [references/plan.md](references/plan.md)           | The effort is too big or foggy for one session                             |
| [references/spec.md](references/spec.md)           | Turning a settled idea into a spec                                         |
| [references/validate.md](references/validate.md)   | Adversarially auditing a published spec, ticket set, or map before build   |
| [references/tickets.md](references/tickets.md)     | Splitting a spec into buildable, session-sized slices                      |
| [references/implement.md](references/implement.md) | Building a ticket or a small spec with domain-aligned verification        |
| [references/review.md](references/review.md)       | A diff exists and needs checking against standards and spec, fresh session |
