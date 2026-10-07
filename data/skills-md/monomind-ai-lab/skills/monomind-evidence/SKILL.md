---
name: monomind-evidence
description: "Capture safe, revision-bound proof for user-visible behavior, bug fixes, APIs, migrations, performance, or operational claims. Use when automated checks alone cannot demonstrate what changed or when a review needs reproducible before/after or runtime evidence."
---

# Monomind Evidence

Turn each acceptance claim into a reproducible artifact tied to the exact code and environment tested. Evidence complements repository checks; it never replaces them.

## Plan claims before captures

List the claims a reviewer must be able to verify. Choose the cheapest trustworthy medium for each:

| Claim | Useful evidence |
| --- | --- |
| Pure behavior or bug fix | Focused red/green test output and regression command |
| Static visual change | Matched before/after captures at the same state and viewport |
| Interactive UI flow | Ordered screenshots or an annotated recording of the live test |
| API or integration | Repeatable probe with redacted request, response, and exit status |
| Performance | Before/after benchmark with workload, sample count, and environment |
| Migration or data change | Dry-run output, counts, invariants, and rollback rehearsal |
| Production operation | Queryable logs, metrics, traces, and health checks |

For a bug fix, capture the old failure before changing the code whenever feasible. A single "after" image does not prove that the reported failure existed or that the tested path changed.

For a PR-ready visible comparison, use `monomind-before-after` when it is installed. It adds matched-source capture and Markdown packaging through the external `@vercel/before-and-after` CLI; this skill remains the authority for the claim/evidence plan and privacy boundary.

## Bind and capture

1. Record the exact revision or deployment identifier, branch when useful, environment, test data class, and executable command or interaction sequence.
2. Establish preconditions before the meaningful action. For visual pairs, match viewport, data, account state, and capture boundary.
3. Capture one assertion per meaningful state change. Mark it passed, failed, or untested with a reason; timestamps do not validate truth, so inspect the state before labeling it.
4. Store local artifacts in the project's gitignored evidence location, or `.artifacts/<task>/` when none exists. Keep the reproducer beside the output when practical.
5. Open or replay every artifact and confirm that it shows the stated claim, is legible, and belongs to the recorded revision.

## Protect data and authority

- Exclude tokens, credentials, personal data, payment data, private customer content, and unrelated windows or notifications.
- Use synthetic or approved test data. If safe proof is impossible, mark the claim untested and explain the constraint.
- Do not upload, post to a pull request, modify an issue, or use a public image host without explicit authority for that destination.
- Do not present synthetic playback, edited footage, or a different deployment as a live test of the target revision.

## Evidence report

Summarize:

```markdown
| Claim | Result | Artifact or command | Revision/environment | Caveat |
| --- | --- | --- | --- | --- |
```

Include repository checks separately from runtime proof so reviewers can see which claim each kind of evidence supports.

## Completion criteria

- Every material acceptance claim is proven, failed, or explicitly untested.
- Artifacts are reproducible, readable, and bound to the tested revision and environment.
- Before/after comparisons control for state and viewport.
- No sensitive or unrelated data is exposed.
- External publication occurred only within explicit authority.
