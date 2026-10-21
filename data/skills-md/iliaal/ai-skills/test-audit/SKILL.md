---
name: test-audit
class: workflow
description: >-
  Audit whether tests detect regressions in the behavior they claim to protect.
  Find mocked-away subjects, weak or circular assertions, undiscriminating fixtures,
  swallowed failures, and tests missing from gates. Use for test-quality audits,
  suspected false confidence in generated tests, and reviewing new tests. Use
  ia-writing-tests for writing tests.
---

# Test audit

Find tests that remain green when their claimed behavior breaks. Assess behavior,
not apparent authorship, mock count, assertion count, or a target finding percentage.
Default to a read-only audit. Change tests or production code only when requested.

Adapted from the OpenClaw test-audit skill (MIT).

## What counts as a finding

Evaluate each claimed behavior separately. A test can protect one obligation and miss
another. Use these dispositions:

- **Ineffective for the claim:** the named behavior is replaced, never reached, or
  disconnected from a verdict that can fail.
- **Partially effective:** real behavior is tested, but a specific promised distinction
  is absent from the input or assertions. Preserve the protection that exists.
- **Not enforced:** the test is uncollected, skipped, or absent from a blocking gate.
  Report local collection and CI enforcement separately from assertion quality.
- **Redundant:** another test protects the same behavior at the same boundary under
  equivalent inputs and setup. This requires separate evidence; weakness alone is
  not redundancy.
- **Adequate for its scope:** the test detects a credible failure of its actual contract.
- **Unresolved:** missing context or execution prevents a defensible decision.

A missing additional edge case is not automatically a defective existing test. Tie
each quality finding to an existing claim, documented contract, or misleading assertion.
Distinguish an individual test's weakness from a suite-wide coverage gap.

## 1. Establish scope and execution

Read repository instructions, runner configuration, shared fixtures, test helpers, and
CI commands. Record the exact focused command and applicable completion gates.
Determine which tests are collected, execute, and block a merge. An advisory job is
not a blocking gate. A local green result does not establish CI enforcement.

Build an inventory from the runner's collection output when practical. Otherwise label
the source inventory approximate. Count files, test definitions, and parameter cases
separately. Do not treat helpers as tests or silently omit unrecognized syntax.

For a bounded request, inspect every in-scope test. For a large suite, declare the
review budget and selection method before discovery. Cover distinct layers, major
fixtures, and mocking styles. Combine risk-directed selection with a reproducible
sample independent of detector hits. Keep those two sample results separate. Record
the seed and sample unit if claiming random sampling. Expand recurring patterns into
their owner family when practical; report anything left unreviewed.

Do not infer suite prevalence from targeted examples. If a prevalence estimate is
requested, use a representative sample with an explicit denominator and uncertainty.
Do not tune findings to an expected rate such as 10–20%.

## 2. Discover through behavior

Read [behavioral-review.md](./references/behavioral-review.md) before auditing test bodies.
For each reviewed test, trace:

1. **Claim:** what observable behavior does the name, fixture, or requirement promise?
2. **Real subject:** which production operation actually runs, including setup, imported
   helpers, autouse fixtures, module mocks, and dependency injection?
3. **Input:** does the fixture create the distinction the claim depends on?
4. **Oracle:** where does the expected answer come from, and which assertion checks it?
5. **Verdict:** will an incorrect result reach the runner as a failure?
6. **Counterexample:** what plausible wrong implementation would still pass this test?

Construct a concrete counterexample before declaring an assertion sufficient. Examples
include ignoring one filter, selecting the first item instead of the minimum, dropping
a forwarded prop, or returning an empty result where only the type is asserted.
Prefer a changed observable result over a crash or syntax error.

Inspect both positive and negative tests. Trace assertion helpers to their actual
checks. Read the relevant implementation and neighboring tests before reporting a gap.
For mocks, identify whether the replaced operation owns the claimed behavior or is a
collaborator of a real subject. Check arguments, call requirements, returned data, and
observable effects at that boundary.

When delegation is available, split semantic discovery by owner or directory. Each
reviewer discovers independently of detector output. Require exact locations, real
subject, surviving regression, retained value, and evidence status. Independently
verify the strongest findings before reporting them.

## 3. Use detectors as additional leads

Run each script by its path in this skill's directory, not the audited repository's
`scripts/`, with the audited repository root as the working directory. Write output
to a temporary directory.
Use the repository's pinned tooling for runner commands. The scripts require Python
3.11+ and the standard library.

| Script | What its results mean |
|---|---|
| [weak_negatives.py](./scripts/weak_negatives.py) `<test globs>` | Heuristic candidates for ambiguous refusal assertions. Does not assess positive behavior or assertion data flow. |
| [duplicate_tests.py](./scripts/duplicate_tests.py) `<test globs> --json` | Structural duplicate/consolidation candidates, not an effectiveness score. |
| [junit_census.py](./scripts/junit_census.py) `<report.xml> --test-files <glob>` | Reported skips, possible collection gaps, and PHPUnit zero-assertion leads (adequate when not throwing is the documented contract). |
| [guard_pins.py](./scripts/guard_pins.py) `--src <glob> --tests <glob>` | Refusal strings without textual matches; not proof of guard coverage. |
| [pytest_reach_probe.py](./scripts/pytest_reach_probe.py) | Runs the target suite with a recording plugin; use a scratch copy. See [stacks.md](./references/stacks.md). |

Before trusting any output, read [detectors.md](./references/detectors.md): for the
four static detectors, status 2 means known incomplete input, and each detector has
blind spots that require source review. Read [stacks.md](./references/stacks.md) for
runner/probe commands and duplicate parser limits. Confirm tool flags locally before
use. No detector hits means only no matches to that detector's rules; continue the
semantic sample.

## 4. Confirm regression sensitivity

Static evidence can establish a finding when the data flow is explicit, such as a
test asserting a value it assigned itself. Label it **source-confirmed**. Otherwise
state the counterexample as **inferred** until executed. Use **execution-confirmed**
only when the exact test ran against a verified behavioral change.

For high-impact or uncertain findings, use a focused mutation in an isolated scratch
copy. Do not mutate the user's checkout for an audit. Keep network calls, paid APIs, and
shared databases outside the probe unless separately authorized and isolated. Before
running a mutation, read [mutation-and-repair.md](./references/mutation-and-repair.md)
for the procedure and how to read a surviving mutant.

## 5. Report actionable evidence

For each finding, give:

- Exact test name and `file:line`, plus the relevant production location.
- Claimed behavior, actual real subject, and input/assertion/verdict defect.
- Concrete surviving regression and retained useful protection.
- Evidence status, command/results when executed, and unresolved limitations.
- Individual-test versus suite scope, neighboring coverage checked, and repair direction.

Report reviewed scope and selection method alongside findings. Separate confirmed
findings, unresolved candidates, and retained counterexamples. Do not count every
missing obligation as a separate bad test. State commands not run and reasons.

Before proposing deletion of a production seam or a test, or when changes are authorized, or when
authoring a new test, read [mutation-and-repair.md](./references/mutation-and-repair.md).
