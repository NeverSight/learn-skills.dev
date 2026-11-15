---
license: MIT
name: jj-execute-restack
description: >
  Execute a supplied Jujutsu restack plan, implementing authorized fixes and
  rebuilding a separate verified stack, including selective feature extraction,
  while preserving source history and existing refs. Use when an actionable
  plan is ready for reconstruction.
---

# Execute a Jujutsu Restack

Own mutations and execution evidence. Consume a plan from `jj-plan-restack` or
an equivalent supplied plan; the planner need not be installed. If no actionable
plan exists, use the planner when available rather than inventing boundaries
during execution. Do not publish or replace the user's branch implicitly.

## Admit the plan

- Verify the intended `.jj` repository with `jj root`; use noninteractive
  `jj --no-pager` commands with explicit descriptions. In colocated repositories,
  mutate with jj and use Git only for read-only verification. Preserve unrelated
  work and record the operation before mutation.
- Require a source snapshot record, explicit base/tip and retained prefix,
  original inventory and semantic timeline, complete redistribution map,
  ordered target commits, authorized fixes, per-boundary checks, final-tree
  target, and unresolved decisions. Missing decisions block affected work.
- Require the selection mode: partial feature picking, or a full rebuild with
  focused work first and other features last. Follow the
  [scope and suffix contract](references/scope-and-safety.md#partial-porting-and-presence-only-suffixes).
  An explicit presence-only suffix waiver overrides the validation gates below
  for that suffix; preserve and report its contributions without claiming it
  verified. Out-of-focus work alone does not imply a waiver.
- For another destination branch, require its pinned `DESTINATION_BASE`, the
  fully/partially ported and superseded mapping, remaining dependency closure,
  and an integration-target contract. Follow
  [destination preparation](references/scope-and-safety.md#another-destination-base);
  old-source-tip equality does not apply to this mode.
- Compare exact source commit identities, trees, relevant refs, and working-copy
  state to the plan. Short change IDs alone cannot detect rewritten versions.
  Drift blocks affected mutations until an updated plan is available; use the
  planner if installed, otherwise report the evidence and request an updated
  plan. Unrelated operation-log advancement alone does not invalidate a plan.
  Do not change intended behavior or boundaries silently.
- Trust only substantive descriptions, checked against code and consumers.
  A `refactor` may add a feature; correct misclassified plans before mutation.
- Check conflicts already present in the original stack for intentional feature
  removal; a conflict alone is not evidence of a missing feature or dependency.
  Do not add removed features back to resolve it. If the plan and source evidence
  leave intent unclear, ask the user before resolving the affected conflict.
- Read [scope and safety](references/scope-and-safety.md) before mutations.
  Preserve original commits and the retained prefix. Never bypass immutability,
  arrange history with `jj rebase`, or duplicate the whole stack or suffix.
  Correct completed rebuilt commits through verified children, never direct
  content edits. Description-only updates may use explicit `jj describe` on
  workflow-owned rebuilt revisions, with evidence handled as described below.
  Scope squash/absorb to their mapped owners; revision checkouts for
  validation remain allowed without modifying those commits.
- For a behavior-preserving mainline, require an explicit behavior baseline and
  residual mapping. No feature or fix that changes that baseline may enter the
  mainline, even if present in the source or separately authorized. Preserve
  requested residuals on side branches from dependency-appropriate milestones;
  the source-fix phase below must not promote them into the mainline target.

## Fix, reconstruct, verify

1. **Protect and fix.** Pin the pre-fix source with a fresh tag. Implement only
   planned, authorized fixes as verified new top commits; never edit originals.
   Record their source mapping and inspect the complete intentional delta.
   Pin the corrected source with a fresh immutable tag when fixes exist; it is
   now `OLD_TIP`, the corrected full source. Without fixes, reuse the source tag.
   For same-base extraction, prepare the separate retained-feature target described in
   [scope and safety](references/scope-and-safety.md#prepare-an-extraction-target).
   For another destination base, prepare and pin the integration target using
   the destination-preparation contract, composing extraction when requested.
   Set `EXPECTED_TIP` to the applicable pinned target; only a same-base rebuild
   without extraction uses `OLD_TIP` directly.
2. **Build one milestone.** Follow [reconstruction](references/reconstruction.md)
   from the recorded `REBUILD_BASE`. Use original diffs and milestone trees,
   duplication only for a small manually confirmed reusable slice, and final-state
   partitioning only with the plan's semantic audit. Do not apply content twice.
   Record actual source-to-new mappings and final descriptions.
3. **Validate before advancing.** Read each complete parent diff and follow the
   [per-commit protocol](references/validation-and-recovery.md#per-commit-check-protocol).
   No broken intermediate commit may depend on a later repair. Advance only the
   dedicated clean bookmark after validation. For structural conflicts use
   [correction children](references/conflict-resolution.md); revalidate rewritten
   owners and affected descendants oldest first.
4. **Finish.** Prove clean-tip tree equality with `EXPECTED_TIP`, and that
   the pre-fix-to-clean delta contains precisely the authorized fixes and
   extraction changes, plus the accounted destination integration delta when
   changing bases. Audit the target delta independently of the rebuilt tip.
   Verify
   preserved source IDs/refs, retained-prefix identity, separate suffix, semantic
   milestones, and per-commit evidence. Apply the
   [completion and recovery rules](references/validation-and-recovery.md).

## Deviations and reporting

When unexpected complexity affects execution, distinguish inherent feature
requirements from difficulty imposed by the existing architecture and from
reconstruction mechanics. Cite source evidence and mark mixed or uncertain causes.
Return changed structural needs to planning within the existing authorization;
do not turn integration difficulty into an implicit refactoring mandate.

Repair reconstruction mistakes within the existing plan through verified
correction children. New source defects, changed dependencies, ambiguous
ownership, or different commit purposes return to planning. Do not smuggle
behavior changes into conflict resolution. If replanning adds an authorized
source fix, append it to the preserved source, pin a fresh corrected target,
and rebuild from the first affected boundary; never move an existing safety tag.
If extraction is active, regenerate and validate its target against the updated
corrected source before resuming; the earlier target cannot silently omit a fix.

Keep execution progress separate from intended design: record exact validated
revisions, checks, outcomes, last validated milestone, and pending corrections.
On resume, compare source identities and protected refs to the original snapshot,
and workflow-owned refs and working-copy state to the execution checkpoint.
Recorded fixes and bookmark advances are expected progress, not external drift.
Changed content or parent trees invalidate affected behavior evidence. For
description-only rewrites, prove those trees unchanged, record old-to-new exact
identities, and recheck descriptions, graph, refs, and metadata-sensitive checks;
applicable behavior evidence may carry forward. See the
[validation protocol](references/validation-and-recovery.md) for details. A no-op
needs no clean bookmark; extraction or destination integration with no rebuilt suffix follows the explicit
empty-result rules there.

Report findings addressed, final order and source mapping, safety tags, clean
bookmark, tree comparisons, and verification limits. Use short jj change IDs
with role/description context; keep commit hashes in internal records.
For a separate post-restack review, use `jj-plan-restack` when available or
perform an equivalent read-only audit of target content, behavior/design
adoption, every commit's actual parent boundary, and source/ref preservation.
Review focuses on behavior and design, not format or lint. Review-only requests
do not authorize reconstruction or fixes.
