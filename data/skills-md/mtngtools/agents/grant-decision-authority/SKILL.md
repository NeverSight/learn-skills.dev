---
name: grant-decision-authority
description: Let the agent settle any call a human would normally make, within safe bounds — each one marked in the tree, tabled on the PR, and approved by a human before it merges.
disable-model-invocation: true
metadata:
  type: command
  invocation: human-only
  applies-to: [decisions, approvals, specs, tickets, commits, prs, sessions]
---

# grant-decision-authority

> **human-only.** Start this only when a human asks for it by name. Granting yourself decision authority is exactly the thing this skill is careful about — if you arrived here from another skill, stop.

The human is stepping away, and the work is going to hit calls that are theirs to make. This lends you their answer on the ones that are safe to lend, so the work continues instead of parking on the first ambiguity.

**The wider grant.** `grant-naming-authority` lends you gated names; this lends you gated names *and* the ordinary judgment calls around them. The scope is wider, so the bounds below are the substance of this skill — they are what keep a grant of "decide it yourself" from meaning "decide anything".

The loan buys motion, never a decision. **A call made under it is still open.**

**How a loan is held** — the markers, the grep, the PR table, the reviewer note, the merge gate, and the settle-up — is the [borrowed-authority ledger](./ledger.md). Read it; this skill only says what may be borrowed.

## 1. Read the room

Run the ledger's grep first:

```
grep -rn "TEMPORARY AGENT" .
```

Hits mean a previous window left loans standing: settle those before opening new ones.

Then find what the repo has already decided, because **a loan cannot overrule a decision that already exists**. Read its `AGENTS.md`/`CLAUDE.md`, the specs and ADRs covering the work, and the ticket's own text. A call the repo has already settled is not open, and picking differently is not borrowing — it is overriding, which no grant covers.

**Done when:** the tree is clean of markers, and you can say what the repo has already settled about this work.

## 2. What may be borrowed

**In bounds — borrow it, mark it, keep going:**

- **Gated names**, on the terms in `grant-naming-authority` — its "gate generously" and "adoption is not a loan" limits apply here unchanged.
- **Implementation calls inside a settled spec** — structure, seams, internal types, which pattern, where a boundary goes.
- **A choice between approaches that both satisfy the spec** — pick one, record the other as the alternative.
- **Error and edge handling the spec left unstated** — retry counts, timeouts, what a nullable case does, which of two failure modes wins.
- **Test strategy** — what to cover, at which level, with which fixtures.
- **Ambiguity in an acceptance criterion** that has a reading consistent with the spec. Take that reading, mark it, and say in the row what the other reading was.
- **Ordering and slicing of your own work** — what to build first, whether to split a commit, how to word a message.

**Out of bounds — stop, do everything else, and hand it back:**

- **Anything irreversible.** Deleting data, rewriting shared history, force-pushing, dropping a migration, removing a file whose content exists nowhere else. A loan is undone by a rename; these are not undone at all.
- **Anything that leaves the repo.** Publishing, releasing, tagging, sending anything to a third party, touching another org's tracker. Opening a PR on this repo is fine and is the point; everything past it is not.
- **Security and access.** Credentials, auth, permissions, relaxing or disabling a gate, a check, or a lint that is failing. "The gate is wrong" is a claim for the human, not a call for you.
- **Dependencies and licences.** Adding a runtime dependency, changing a version pin with a behaviour change behind it, anything touching a licence.
- **Contracts with anyone outside this change.** Wire schemas, public API shape, database schema in use, a config key another system reads. These are the same class as a gated name, but a rename does not fix them after the fact.
- **Scope.** Dropping an acceptance criterion, calling a ticket done that isn't, closing a ticket, splitting work into a new one, merging a PR.
- **Contradicting a settled spec, ADR, or ticket.** Deviating from a written decision is an override, not a loan. If the written decision looks wrong, that is a finding to hand back — with the evidence — not a call to make.
- **A ticket whose premise turns out to be false.** An acceptance criterion resting on a factual claim you can disprove does not become yours to reinterpret. Disprove it, stop, and hand it back to whoever wrote it. Building the substitute you think they meant and footnoting it in the PR is the failure this bullet exists to prevent.
- **Anything the ticket, the spec, or the human reserved to them**, however small.

**When you are unsure which side a call falls on, it is out of bounds.** The cost of parking one call is a line in the handback; the cost of borrowing one you should not have is a merged PR nobody meant to approve.

**Out of bounds does not mean stop working.** Park that one call, do everything in the ticket that does not depend on it, and list it in the handback with what you would have chosen and why you did not.

**Done when:** every call the work reached is borrowed-and-marked, or parked-and-listed. None is silently taken.

## 3. Borrowing a call

**Do the whole proposal anyway** — what you chose, a real alternative you actually weighed, and why this one. That is the row the human answers; without it the settle-up is a fresh design session rather than a review.

Then write the marker at the site of the act, per the ledger, and continue.

## 4. PR, gate, settle

All three are the ledger's: generate the table from the grep, carry the reviewer note, open the PR normally, and settle one case at a time. Record each approval per the `approval-policy` skill.

**Parked calls go on the PR too**, under the table, as their own short list — they are the other half of what the human came back to decide, and they are invisible to the grep because nothing was written for them.

**Done when:** the ledger's own done-when is met, and every parked call has been answered or explicitly deferred.

## Where this sits in the flow

`/implement` builds the ticket; this skill is what lets it keep building past calls it cannot approve. `/create-pr-for-branch` opens the PR, `/review-pr-in-worktree` judges it, `/respond-to-pr-review` is usually where the answers arrive and the markers come out.

`/grant-naming-authority` is the narrow version — names only — and is the right grant when that is all the work needs. `/implement-unattended` turns this on together with parallel build and review.
