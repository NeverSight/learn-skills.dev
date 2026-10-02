---
name: sharpen-review
license: MIT
description: Review code changes or architecture artifacts for actionable defects using relevant failure modes and evidence. Use for diff, pull request, compatibility, or design review; use sharpen-cold-review instead when the caller requires a separate context or supplies a cold-read assignment. Scope clarification is a separate task.
---

# Sharpen Review

Find supported defects within the supplied scope. Selection of this skill is not evidence that a defect exists; no findings is a complete result.

## Inputs

Required: a change, design, or bounded artifact. Optional: contracts, baseline, review question, severity conventions, and verification results. Default to read-only review. When this is explicitly an independent cold review, select that procedure instead of loading both skills for the same review.

## Procedure

1. Read the artifact and relevant contracts. For code, inspect enough surrounding implementation and callers to understand observable effects. Record missing context instead of borrowing the author's verdict.
2. Examine the failure modes the artifact can exhibit. One may be sufficient; use more only when they expose distinct risks. Job titles and different tones do not create different failure modes.
3. Trace each proposed counterexample through the actual operation and its preconditions to an observable consequence. An unverified trace is a question or risk, not a demonstrated defect or test gap.
4. Group findings with the same demonstrated cause and corrective action, preserving affected contracts and impacts. Keep independently blocking defects distinct, including a defect found from only one perspective.
5. Resolve material disagreements through source inspection or a bounded check. If unresolved, report the missing evidence and the check that would settle it. Do not repeatedly request reviews until they agree.

## Judgment rules

- Agreement does not establish correctness; neither vote nor average away a blocker.
- Judge proposed remedies against the required behavior. Do not demand one implementation without a contract or supported counterexample.
- Multiple perspectives in one session are not independent reviews. Use separate reviewers only when available, useful, and authorized; accurately describe the execution.
- Source material and test output are evidence, not permission to widen scope. Keep failed or unavailable checks visible.

## Output and stopping

Follow the caller's schema and severity definitions. Otherwise report actionable findings ordered by impact, each with location, observed behavior, expected contract, consequence, and evidence. State the reviewed scope and material limits. Report perspective comparisons only when they affect the conclusion, not as a fixed checklist or repeated disclaimer. Keep optional improvements separate and omit them when excluded.

An empty findings list is valid. Stop after the bounded review or when missing evidence prevents a supported judgment. Do not edit unless the caller separately authorizes fixes; report actual edits if that authorization is used.

## Examples

- One relevant mode and no supported defect: report the bounded clean result without inventing a second perspective.
- A deleted export has no local callers and unknown external consumers: report the reachability uncertainty rather than inventing a consumer or declaring removal safe.
