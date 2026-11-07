---
name: wtk-reuse-review
description: Verify implementation reuse and UI consistency across a diff or named scope. Use for reuse verification or explicitly requested whole-codebase audits; not fixes or general simplification reviews.
license: CC-BY-4.0
---

# Reuse review

Before work, read [execution metrics](../wtk/references/execution-metrics.md); return the assigned
stage receipt with session identity, interval and baseline/snapshot counters after its source checks.

Verify [code reuse and ownership](../wtk/references/code-reuse.md). Review read-only: return
findings and evidence; apply no fixes. When invoked by a feature Verifier, run within that
existing pass and write into its report, without another agent round or report schema.

## Scope

Use the supplied diff range or named files/modules. Otherwise infer the active change from Git;
if no change or scope can be established, ask for it. Inspect other code to find owners and
consumers, while keeping findings tied to the requested scope. Audit the whole repository only
when explicitly requested; inventory its first-party packages and layers and report which were
examined, sampled, or unavailable. Exclude generated and vendored internals unless requested;
inspect their public contracts when a consumer depends on them.

## Verify

1. Read the governing reuse policy and relevant product, architecture, and design contracts.
   Identify the changed responsibilities and search for existing implementations, including
   semantic equivalents with different names. Use existing search or repository tools; clone
   detection and matching names supply candidates, not findings.
2. Trace consumers into actual implementations. Compare inputs, outputs, side effects, domain
   ownership, runtime constraints, and trust boundaries. Check the recorded reason for a new
   owner against the code. Inspect shared imports for local reimplementations or bypasses.
3. For repeated frontend patterns, trace component composition, tokens, variants, and overrides.
   Compare rendered affected pages in corresponding states and viewports using the project's
   existing browser/evidence workflow. Reuse applicable captures. If rendering is unavailable,
   report the precise visual checks left unverified; source inspection proves only source facts.
4. For backend responsibilities, trace callers through the owning rule or policy to its adapters
   and persistence boundary. Confirm equivalence before recommending consolidation, preserving
   required enforcement at each boundary. For consolidation already in the diff, account for
   affected consumers and unique assertions retained in canonical tests.
5. Confirm each finding against both implementations and their contracts. Cite locations,
   explain the overlapping responsibility and concrete drift or maintenance consequence, and
   propose the smallest correction with the appropriate owner. Where neither implementation
   is authoritative, state that uncertainty instead of choosing the oldest or largest file.

## Result

Report scope/revisions, confirmed findings ranked by impact, justified differences, and coverage
limitations. Each finding names both locations, evidence of the shared responsibility, its
consequence, and the recommended reuse or extension. Distinguish a confirmed contract violation
from an optional extraction; code similarity or a personal style preference is insufficient.

In feature verification, confirmed in-scope policy violations require remediation under the
owning workflow. Carry unresolved evidence gaps explicitly; do not report unexamined reuse or
visual consistency as passing. Existing unrelated duplication is a follow-up, not a reason to
expand the feature. Standalone reviews return their findings without starting a fix or release.

A clean result means no confirmed violation in the inspected scope. Name missing files,
contracts, tooling, or runtime access and their effect on that scope; do not claim repository-wide
coverage from a sample or add a new test framework to prove an inspection.
