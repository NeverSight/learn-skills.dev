---
name: multi-agent-review
description: Coordinate independent review agents and validation agents into one evidence-based review. Use when a code, document, design, or other bounded artifact needs several review dimensions or specialist perspectives; do not use for a simple single-perspective review.
---

# Multi-Agent Review

Orchestrate the review; do not perform every specialist review yourself. Produce a single result that preserves useful disagreement and makes its evidence and confidence clear.

## Frame the review

Establish the following before dispatching agents. Use the user's wording when it provides the answer, and state any material assumption.

- **Context:** the change's purpose, relevant constraints, and any policy or acceptance criteria.
- **Scope:** an exact boundary: files and changed lines, a component, a document section, or another inspectable target. Exclude adjacent work unless it is needed to demonstrate an impact within scope.
- **Review dimensions:** the quality or risk lenses to apply, such as correctness, security, performance, maintainability, accessibility, or operational safety.
- **Review policy:** the allowed severity values and the standard for `require_action`. When absent, use `critical`, `important`, and `suggestion`; reserve required action for a concrete change needed to prevent a material problem.

If the requested scope or dimensions cannot be determined safely, ask a focused question rather than silently widening the review.

## Dispatch independent reviewers

Assign each reviewer an explicit subset of the scope and one or more review dimensions. Use independent agents in parallel when available. Give every reviewer the same context, its own scope and dimensions, the review policy, and the reviewer-result schema in [references/reviewer-result-schema.json](references/reviewer-result-schema.json).

Tell reviewers to:

- inspect only their assigned scope;
- return an empty array when no actionable finding exists;
- give a precise in-scope location and concrete supporting evidence for every finding;
- return JSON conforming to the supplied schema, with no speculative or out-of-scope findings.

Keep an attribution record for each finding: reviewer, assigned scope, and dimensions. Reject malformed results and discard findings that are outside that reviewer's assigned scope.

## Triage and consolidate

1. Drop reviewer findings whose `confidence_level` is below 80.
2. Group the remainder by the underlying problem, not by matching wording. Preserve each contributing reviewer's attribution.
3. Merge findings only when their locations, evidence, and proposed action describe the same issue. Combine the evidence; do not let the highest severity automatically win.
4. When conclusions conflict, retain the alternatives as a conflict set. Identify the point of disagreement and the evidence for each position; do not resolve it by majority vote.

Do not synthesize missing evidence while consolidating. A weakly supported finding belongs in the discarded or attention-needed set, not in the verified findings.

## Validate consolidated findings

Send every remaining individual, merged, and conflicting finding to a validation agent that did not author the finding when possible. Give it the original evidence, attribution, applicable context, assigned scope, review policy, and the artifact itself. Ask it to independently confirm:

- the location is within scope and is accurate;
- the claimed behavior or quality concern is supported by the artifact and context;
- the severity and required action follow the supplied policy; and
- the revised `confidence_level` and location for a merged finding.

For a conflict set, the validator must evaluate each alternative and explicitly say whether the conflict remains unresolved. A validator may mark a finding `verified`, `needs_attention`, or `rejected`; it must give a reason for the latter two. Do not present rejected findings as review results.

## Present the result

Start with the reviewed scope, dimensions, and a concise outcome. Then show findings in review-policy priority order, with verified items first. Each finding must include its ID, location, severity, finding, required action, confidence, validation status, and supporting reviewer dimensions.

Assign user-facing IDs after consolidation and validation in presentation order: `R-01`, `R-02`, and so on. Use one unique sequence across verified findings, needs-attention items, and unresolved conflict sets. Retain original reviewer IDs internally for attribution and traceability.

Follow with a separate **Needs attention** section for non-rejected items the validator could not confirm, including the reason. Follow that with an **Unresolved conflicts** section when applicable, showing the competing claims and what evidence would resolve them. Report that no actionable findings were verified when that is the outcome.

Keep raw agent transcripts out of the user-facing result unless the user asks for them.
