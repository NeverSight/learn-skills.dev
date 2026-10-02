---
name: review-code-publish
description: "Invoke review-code and publish one forge-native review of an existing pull request. Use when the caller wants a review posted to the pull request, not just reported back."
---

# Publish code review

## Boundaries

Invoking this skill authorizes publishing a review to the resolved pull request.
Retrospective review of a merged pull request is non-publishing unless separately authorized.
This does not authorize changing code, editing the pull request or issue, adding labels, or merging.
Use a gating event only when the user or repository workflow separately authorizes this identity to gate the merge.
A caller that resolved a reviewing app distinct from the pull request's author carries an explicit gating authorization in its packet, and that authorization is what permits a gating event here; a review published under a reviewing app is not a self-review.
A self-review always uses `COMMENT`.

This workflow is one-shot: finish without pausing for reviewer preferences.
If `review-code` is not among the installed skills, stop with `missing-dependency: review-code`.
`review-bot` is optional. Its absence falls back to the authenticated user, records the reason in the report, and withholds gating; it never produces a missing-dependency stop.

## Inspect

Invoke `review-code` with `mode: one-shot`, the explicit pull-request target (coordinate, URL, or current branch's open pull request), any user-supplied issues or spec, and the duplicate-review shortcut on.
Pass through supplied phase-1 packets, reviewer identity, focused-test policy, and check evidence under its Inputs table when provided.
A supplied review-token command stays here rather than travelling with them: `references/publication.md` spends it on the writes below, and `review-code` never publishes.
With no supplied reviewer identity, resolve it before the review runs as `references/publication.md` specifies. The tracker doc declares the reviewing app and client id, or a literal review-token command used as-is. For an app without a literal command, invoke `review-bot` when installed and take its returned login and command. Any `unavailable` result falls back to the authenticated user, records the reason in the report, and withholds gating. Resolution never stops the run; a token refused at publication still stops the write.
`review-code`'s one-shot mode, under its Modes section, asks nothing and reports every routed item in the record.
A named stop ends this run with its report.
Otherwise run `python3 <skill root>/scripts/render_review.py --check <private-dir>` under the skill root the record names; exit 0 means the returned artifacts supply everything below, and any other exit is an incomplete review: report its output and stop without publishing.
For a merged target without separate publication authorization, report the returned `report.md` as the complete would-be review and finish; this skill alone decides whether a merged target publishes.

## Publish

Read [`references/publication.md`](references/publication.md) now and follow its invariants, event table, batch shape, and thread operations.
Use the returned `batch.json` for the common `COMMENT` path.
An `issue-required` routed item appears as a `[Question]` in the review body; `Issue fit` states that the ledger came from the pull-request text. With otherwise complete coverage and no unsettled must-fix finding, the status is `Needs Information`, never `Incomplete` for this reason alone.
For authorized gating, regenerate it with `--emit-batch --event` through `<skill root>/scripts/render_review.py`, under the skill root `review-code` records; the script owns the suffix change.
Never locate scripts through a sibling-relative path.

Re-fetch the pull-request head, check it, and post the batch in one forge-native review call with the reference's freshness-and-submission block, one shell invocation.
Exit 3 means nothing was written on that block's `preflight failed` route and on the thread write loop's pre-write exits: report what it printed — a stale or unreadable head, a review-token command that yielded no usable token, or a refused `writes.jsonl` — and stop.
An exit 3 the block prints after its `write attempted` line is a failed review POST, not a preflight failure, and takes the repair, retry, and fallback rules below instead.
After the review posts, write `writes.jsonl` for every prior item and run the reference's thread write loop once for its replies and thread resolutions.

On a malformed-comment rejection, an ambiguous write, or a refused review, follow the reference's repair, retry, and fallback rules, using the scripts under the skill root `review-code` records; if compaction dropped the rendering instructions, re-read `references/output.md` from that root.

## Report

Read the published review back.
Report the posted status, reviewed head, coverage, review URL, finding URLs, open questions, disputed findings, and anything that failed to publish.
Use the posted form from `batch.json` after gating emission, not the advisory `payload.json` body.
Every file coordinate is the same script-rendered commit-pinned link the summary carries.
On a non-publishing retrospective run, report `report.md`'s complete would-be review in place of the review URL.
