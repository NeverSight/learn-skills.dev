---
name: grant-naming-authority
description: Let the agent choose gated names and keep going — every borrowed name marked in the tree, tabled on the PR, and approved by a human before it merges.
disable-model-invocation: true
metadata:
  type: command
  invocation: human-only
  applies-to: [naming, specs, commits, prs, approvals, sessions]
---

# grant-naming-authority

> **human-only.** Start this only when a human asks for it by name. Granting yourself naming authority is exactly the thing this skill is careful about — if you arrived here from another skill, stop.

The human is stepping away, and work that needs a gated name would otherwise stop at the proposal and wait. This lends you their answer so the work continues: you pick the name you would have proposed, mark it, and carry it through to a PR where a human settles it before the merge.

The loan buys motion, never a decision. **A name used under it is still open.**

**How a loan is held** — the markers, the grep, the PR table, the reviewer note, the merge gate, and the settle-up — is the [borrowed-authority ledger](../grant-decision-authority/ledger.md), shared with `grant-decision-authority`. Read it; this skill only says what may be borrowed.

## 1. Find the repo's naming authority

**Before the ledger's grep, before anything.** The repo — not this skill — decides which names are even gated, what an acceptable proposal contains, and where an approval gets recorded. It is usually stated inline in `AGENTS.md` or `CLAUDE.md` with a pointer to a fuller page (`docs/`, an ADR). **Read the pointer target too:** the inline block is the summary, and the exemptions live in the page.

**Where the repo has no naming authority, there is nothing to borrow.** Say so and stop — an unbounded grant over every identifier in the tree is not what the human just handed you.

Then run the ledger's `grep -rn "TEMPORARY AGENT" .`: hits mean a previous window left loans standing, so settle those first.

Report what authority you found and that the window is open, then get on with the work.

**Done when:** you can name the repo's naming authority, say which names it gates, and the tree is either clean of markers or you have settled the ones you found.

## 2. What may be borrowed

**Gated names, and nothing else.** This grant does not reach scope, spec deviations, dependencies, or anything else a decision could be about — that is `grant-decision-authority`, and it is a separate act by the human.

Two limits on what a naming loan covers:

- **Gate generously.** A name you are unsure about is borrowed and marked. An unnecessary marker costs one question at settle-up; a missing one costs a rename after review.
- **Adoption is not a loan.** A name taken from a named upstream — another repo, the framework, a wire schema, a third-party API — needs no approval where the repo's authority says so. Cite the source in place, as that authority requires, and leave the marker off. Borrowing a name you should have adopted is how a wire contract quietly stops matching.

## 3. Borrowing a name

When the work reaches a gated name, **do the whole proposal anyway** — the repo's authority defines its shape, and it is typically the full set, a real alternative, and why. The proposal is the thing the human answers; skipping it turns the settle-up into a fresh naming session instead of a review, and leaves the PR table with a row it cannot fill.

Then pick the name you would have proposed, write the marker at its sites per the ledger, and continue.

**Done when:** every gated name in the work is either adopted with its source cited, or borrowed with a marker carrying the name, the alternative, and the reason.

## 4. PR, gate, settle

All three are the ledger's: generate the table from the grep, carry the reviewer note, open the PR normally, and settle one case at a time when the human answers. Record each approval per the `approval-policy` skill.

**Done when:** the ledger's own done-when is met — no markers, every row answered, the removal pushed.

## Where this sits in the flow

`/implement` builds the ticket; this skill is what lets it keep building past a name it cannot approve. `/create-pr-for-branch` opens the PR the table lands in, `/review-pr-in-worktree` judges it — its reviewers are the ones the note is written for — and `/respond-to-pr-review` is usually where the human's answers arrive and the markers come out.

`/grant-decision-authority` is the wider grant, of which this is the narrow, most common case. `/implement-unattended` turns on both at once, plus parallel build.
