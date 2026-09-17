---
name: release-pipeline
description: Merge an all-clear PR and ship it — rebase, merge preserving attribution, tag, deploy, verify it's actually live, close PR/issues with credit, update the trust ledger. Stages 5-6 of the PR lifecycle. Runs only after pr-deep-review's gate is all-clear.
---

# release-pipeline

**When to load:** a PR has passed the [authoritative gate](../../docs/lifecycle/quality-gates.md) and
is cleared to ship. Runs [PR lifecycle](../../docs/lifecycle/pr-lifecycle.md) stages [5]–[6]. Band B
— a human owns the final irreversible merge call on anything substantial; the narrowest mechanical
merges can be Band A only with the [watchdog](../../docs/playbooks/watchdog-pattern.md).

> Precondition: **do not enter this skill on a self-report.** The gate must have been run fresh by
> [`pr-deep-review`](../pr-deep-review/SKILL.md) and come back all-clear. A cached "looks clean" is
> not a ship signal.

## Steps

1. **Rebase onto the current trunk.** If staleness is the only blocker, the Builder rebases it
   directly. Re-confirm the gate is still green on the rebased code if the trunk moved under it.
2. **Verify the credit before merging** (see the attribution gate below) — the contributor you're
   about to thank must actually be the author of the work you're shipping.
3. **Merge preserving attribution.** The original author's authorship must survive: fix on their
   branch where possible, or a non-squash merge with co-author trailers when not. Never let a rebase
   or "absorb" erase who wrote it. See [contributor recognition](../../docs/lifecycle/contributor-recognition.md).
4. **Stamp the release.** Changelog entry naming the contributor; bump any in-product version marker
   so it matches the tag. Tag the release.
5. **Deploy and verify it's actually live.** "Shipped" means the tag exists **and** the merge is
   real **and** (if you deploy) the running version serves the change. Re-derive the live version;
   never claim shipped from a passed gate alone.
6. **Close + credit [6].** Close the PR and every issue it resolves with a comment naming the
   version and **thanking the author by handle.** Update the [trust ledger](../../docs/lifecycle/contributor-recognition.md)
   with one terminal outcome for the PR, in the [event schema](../contributor-trust/SKILL.md#the-ledger).
   Clean up the branch/worktree.

## The attribution-verification gate

Crediting the *wrong* contributor is its own failure — it's easy when you ship several changes
back-to-back and carry a handle over from the previous one. A present co-author trailer proves a
trailer exists; it does **not** prove the *name* is right.

- **Re-derive the credit from the work being shipped**, every time. Look up the actual author of
  *this* change from the source — never reuse the previous release's handle from memory.
- **All credit surfaces must name the same, correct handle**: the changelog, the release notes, and
  the closing thank-you comment. They have to agree.
- If you can, make it a check: confirm each credited handle matches an author/co-author of the
  commits being shipped, and fail the release if a credited name matches nobody in the change.

## Pitfalls
- **A rebased/absorbed PR may not auto-close.** Confirm the source PR and its issues actually closed;
  a "released" claim is wrong if a constituent PR quietly stayed open (the rebased-PR-close gotcha).
- **Squash-merging away authorship.** The default squash can drop co-authors — preserve them
  explicitly.
- **Claiming shipped from the gate.** The gate authorizes the merge; it is not the merge. Verify the
  tag, the merge, and the running version.
- **Same-day collisions.** When several releases land close together, the changelog and version
  marker can conflict — resolve deliberately, and don't let one release's credit bleed onto another.

## Verification
- The change is merged, tagged, and (if deployed) the live version serves it — all three re-derived,
  not assumed.
- The author is credited identically on every surface, and the handle is the real author of the work.
- The PR and its issues are closed with version + thanks; the trust ledger has one terminal event.
- No branch/worktree left dangling.
