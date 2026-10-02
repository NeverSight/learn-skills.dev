---
name: implement-publish
description: Implement work from a spec, issue, or set of tickets and open a pull request for it. Use when the caller wants the implementation published as a pull request, not just written.
---

# Implement and publish

Implement the work, review it locally with a fresh-context subagent, then open one pull request linked to its spec. This skill stops at the pull request; `review-code-publish` handles the published review.

## Process

### 1. Resolve the targets

Read `docs/agents/issue-tracker.md` when present. Resolve the spec, forge, source and target repositories, and base branch from repository configuration, Git remotes, and the user's request. Record every issue, ticket, or written specification supplied by the user or inferred from the request, branch name, or commits for the pull request to address. Ask before any external write if the spec or publication target is ambiguous.

### 2. Prepare the branch

Follow the repository's branch and commit conventions. If the current branch is unsuitable as a pull-request head under them, branch from the base before any work starts. Implement on a branch, never on the base.

### 3. Implement

Use the implementation skill the user names, otherwise the best-matching model-invoked implementation skill. Implement directly if none applies.

Read the Supplied checks section of `review-code`'s `references/rubric.md` for the verification format and reuse criteria. Save a compact summary:

- Shared full commit SHA, clean/dirty input state and relevant environment.
- One line per check: command or check-run identity, result and readable output reference. Include relevant exceptions and coverage limits; link to logs instead of copying them.
- For required acceptance exercises that checks do not settle: criterion, method and observation under the same shared context, without correctness claims.

For initial implementation and review fixes, report missing required evidence and why it is missing. Do not add verification solely to populate the summary.

Apply these **verification rules** to implementation and review fixes:

- Run the repository's documented focused checks for changed behavior and its dependents. Documentation-only changes need tests only when documented checks cover them.
- Batch related changes before running shared checks once; group review fixes sharing a check into one continuation.
- Rerun checks when changes may affect their inputs, environment or covered behavior. Run the affected broader suite for shared dependency or configuration changes, cross-module changes, or uncertain impact, even if it passed earlier.
- Reuse success only for the same check at the exact head, with unchanged relevant inputs and environment and sufficient coverage. Uncommitted runs count only for the commit made from exactly that tree.
- Repeat required acceptance exercises when changes affect their criterion, method or inputs.
- Retain unaffected results at their original head and input state without rerunning solely because the head changed. They cannot satisfy checks explicitly required at the new head.

Finish with committed changes and recorded verification results. Keep implementation and review local until step 5.

### 4. Review before publishing

Before dispatching any review or continuation, choose an **awaited** route that returns its completed result while this step stays active, without changing global runtime settings. An acknowledgment is not completion; never hand back with a phase pending. If no route exists, stop before dispatch with `review-wait-unavailable`, naming the phase, missing operation and pending work. Failed or partial reviews instead follow the coverage gate below.

Spawn one resumable **general-purpose** reviewer capable of dispatching a verifier, with a fresh context excluding the implementation conversation (`fork_turns="none"` or equivalent). Brief it to:

- Invoke `review-code` with `mode: one-shot`, reviewing the base-to-committed-head range with explicit refs and every spec source from step 1 as user-supplied specs.
- Use step 3's saved verification results and missing required evidence, passing checks as caller-supplied check evidence. Supply observations and artifact references without implementation rationale or correctness claims.
- Return the output of `review-code`'s `scripts/render_review.py --check` on the record's private directory: status, coverage, and the `record.json`, `payload.json`, `batch.json` and `report.md` paths. Keep the verification results' path with the review record.

Read `report.md`; a missing report, or a record `--check` refuses, is an incomplete review, and its record is discarded. Otherwise accept the record as the current result and keep the absolute path of every `record.json` you accepted, the latest last. Evaluate findings against the code and spec. Treat `must-fix` as blocking and `consider` as optional. Report coverage gaps and unresolved questions. Fix warranted defects, verify under step 3 and commit. Give evidence-based reasons for declining findings; disputed blockers remain unresolved.

After committing fixes, read and follow [the continuation procedure](references/continuation.md) before choosing or dispatching the next phase, and include it in the continuation brief.

Require review of the final committed head with no blocking defects or material coverage gaps; any later commit requires review. That review is the record `python3 <skill root>/scripts/render_review.py --check --head <final head> --lineage <record> … <private-dir>` accepts with exit 0, with one `--lineage` for the final record and each record accepted before it; `<skill root>` is the record's `record.paths.skill_root`. If isolated review is unavailable or this gate remains unmet, report why and stop before publishing. Otherwise proceed through step 5 before returning.

### 5. Open the pull request

Using the resolved forge's tools, push the reviewed head and find an open pull request matching both source and target repositories and branches. Update its body if found; otherwise create one with a title and body. Finish with exactly one pull request at the reviewed head.

Write its body as a briefing that a reviewer with the diff can read in under a minute. Use these sections in order, in place of `## Summary` and `## Test plan`:

- `## Why`: the intent and approach in one or two short paragraphs. Link every issue from step 1 as **closes**, **partially implements** with remaining work, or **affects** with its impact, and link any other related ticket as context. For closure, use supported automatic closure on merge or note its unavailability. Name and link external specs.
- `## Scope`: bullets naming real symbols and paths.
- `## Tradeoffs`: rejected alternatives a reviewer would ask about.
- `## Blast Radius`: what the change touches and why it is safe or risky, in one to three sentences.
- `## Verification`: step 3's verification results and gaps, identifying acceptance criteria and preserving each result's head and input state, shared where they match. Report a performance change as one `before → after` number.

Drop `## Scope`, `## Tradeoffs`, or `## Blast Radius` when it has nothing to say. Link logs, metric tables, and other bulky evidence. Attach screenshots or video only when they prove a claim.

Leave issue status, labels and assignees alone.

Attempt each write once; on an ambiguous result read the target before a single retry, then report unresolved failure rather than writing again.

Finish with the pull request link, head SHA, branch, spec source, review outcome, remaining optional findings and anything that failed.
