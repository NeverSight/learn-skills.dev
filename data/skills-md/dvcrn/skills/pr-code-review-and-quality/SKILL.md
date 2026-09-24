---
name: pr-code-review-and-quality
description: Review GitHub pull requests for code quality and deliver inline findings when posting is authorized.
---

# PR Code Review and Quality

Review the requested change for correctness, readability, architecture, security, and performance. Judge improvements against repository conventions and concrete risks; perfection or personal preference is not a merge requirement.


**PR target:** Require a PR number, `owner/repo#number`, or URL supplied by the user, including an unambiguous prior mention. Do not infer it from the current branch or choose an open PR. If no target was provided, ask.

**Output rule:** When the user explicitly invokes this skill's GitHub posting workflow, that request authorizes one `COMMENT` review. Do not ask again. Post it, then report the review URL and a one-paragraph summary. Automatic skill selection or a general request to inspect a PR does not authorize posting; honor explicit local-only or read-only requests. Pass the established delivery choice to any delegate.

## Target and authority

Resolve owner, repository, PR number, and head SHA from the user's input, established conversation context, or an explicit PR named earlier in the conversation. Ask only if the target remains unclear.

Use the delivery choice established by the output rule above. Do not modify implementation code during a review.

## Evidence and coverage

Inspect the PR intent, diff, and relevant CI results. Read changed files, callers, and tests as needed to assess the behavior. Choose the reading order and depth appropriate to the risk. Review large changes in coherent groups and disclose any incomplete coverage.

Use [criteria.md](references/criteria.md) for the five axes and team standards. Load [security-checklist.md](references/security-checklist.md) for security-sensitive changes and [performance-checklist.md](references/performance-checklist.md) when performance is in scope.

Assess whether the author's checks establish the changed behavior. Add targeted verification when evidence is missing; do not repeat passing checks without a new change, failure, or unresolved concern.

## Findings

Use these severity labels consistently:

| Prefix | Meaning |
| --- | --- |
| No prefix | Required change |
| Critical: | Security vulnerability, data loss, or broken functionality that blocks merge |
| Nit: | Optional minor style preference |
| Optional: / Consider: | Suggested improvement |
| FYI: | Relevant information the author lacks |

Every finding needs concrete evidence, a useful file/line reference, and an explanation of impact. Omit praise, restated code, and speculative issues. State a clean result concisely when no findings remain.

## Delivery

For authorized posting, use [github-delivery.md](references/github-delivery.md). Submit one review with event `COMMENT`; never `APPROVE` or `REQUEST_CHANGES`. Inline comments must anchor to the reviewed diff; other findings belong in the summary. Preserve user/repository attribution policy.

Completion means the requested scope was reviewed and findings delivered on the authorized surface, with verification limits disclosed. For GitHub delivery, verify the submitted review and report its URL. After new commits, use [re-review.md](references/re-review.md) to assess the delta without duplicating prior findings.
