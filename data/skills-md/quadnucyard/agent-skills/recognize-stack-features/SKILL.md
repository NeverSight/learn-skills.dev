---
name: recognize-stack-features
description: >
  Infer vertical features and their dependencies from actual changes across a
  commit stack, regardless of original commit boundaries. Use for feature
  inventories, stack reviews, splitting, and restack planning, including as a
  shared analysis step referenced by other skills.
license: MIT
---

# Recognize Stack Features

Recover the capabilities a stack actually delivers, the changes each needs, and
how they combine to address the larger problem.
Produce an evidence-backed feature map for a calling workflow. Recognition alone
does not authorize code edits, history changes, or implementation of missing work.

## What counts as a feature

A feature is a coherent, independently meaningful capability delivered vertically
through the necessary layers: implementation, integration, and actual downstream
use, with the proven-independence exception below for complete standalone
contracts. It can add behavior, repair existing behavior, or change how an existing
production path works. Vertical does not require touching every architectural
layer; it requires completing the path relevant to the claimed outcome.

- **Require a real consumer.** Trace a changed producer, API, representation, or
  mechanism to downstream production code and an observable result. The consumer
  may already exist at the base; show how the change reaches it. Tests, mocks,
  benchmarks, examples, exports, and declarations alone do not establish adoption.
  A consumer is downstream in the execution or dependency path; it need not be in
  a later commit or another package.
- **Allow proven independence.** A change can stand alone if it delivers a useful
  contract without later in-stack adoption, such as a supported library API for
  external consumers, a complete CLI operation, or a refactor of an already used
  path. State the contract, intended consumer or existing entry point, and why
  later changes can be removed without losing its purpose. A public keyword,
  passing unit tests, or hypothetical future reuse is insufficient evidence.
- **Do not promote preparation to a feature.** If an addition has no real
  consumer and no demonstrated independent purpose, attach it to the feature
  that first needs it. If no such feature exists in scope, report unused,
  incomplete, or unverified work. Never invent a consumer to complete the map.
- **Separate verification from delivery.** Tests validate an identified contract;
  they cannot supply its missing production consumer. Associate test-only work
  with the behavior it verifies, or report it as independent verification work
  without claiming a new production feature.

## Establish the evidence

Resolve an explicit excluded base, included tip, and source graph. Pin immutable
revision identities before reading; include relevant ancestors and merge parents.
For nonadjacent selections, identify intervening changes and prerequisites outside
scope rather than silently treating the selection as a contiguous stack.

Read every parent diff, the base-to-tip result, relevant intermediate trees, and
the surrounding implementations and callers. Commit messages and existing slices
are search hints only: both may describe bad grouping. Infer what changed from
code and actual use; supplied requirements establish intended outcomes, while
inferred intent remains provisional. Trust descriptions only when their behavior,
scope, and rationale are substantive, then verify against code and consumers.
A `refactor` label may hide a new feature; classify actual effects and flag gaps.
Do not spend recognition time on formatting or linter checks.

For repeatable evidence collection in Git or colocated jj repositories, use the
bundled Python 3.11+ helper with Git supporting `--attr-source`, from this skill's
installed directory:

```sh
python scripts/stack_evidence.py --repo REPOSITORY --base BASE --tip TIP --output NEW_DIRECTORY
```

Add repeated `--term IDENTIFIER` arguments to find literal candidate references
in the base and every selected tree. For jj, resolve revisions to Git commit IDs
using read-only `jj --no-pager --ignore-working-copy` commands at a fixed operation
first. The script accepts Git revisions, not jj change IDs; it never snapshots jj
or reads uncommitted source files. Inherited Git repository selectors are ignored;
attributes come from the inspected revision instead of the working tree.
For a backend without Git access, collect equivalent
evidence with the repository's native read commands.

The helper writes `manifest.json`, `net.patch`, and per-revision tree indexes,
per-parent patches, and optional candidate matches. Merge parents remain separate;
parents outside the selected range are identified as context. Use the pinned IDs
to read full source with `git show COMMIT:path`. The script does not recognize
features or classify consumers. Matches include tests and dead code; absence of a
literal match cannot exclude indirect calls, registration, generated code, or
external consumers. Binary blobs and submodule contents need separate inspection.
Only use a successful run with a complete manifest; failures leave partial output.

## Infer boundaries from behavior

1. **Describe actual outcomes.** For each changed behavior, name its entry point,
   before/after contract, producer, downstream consumer, and effect. Trace data,
   control flow, registration, configuration, and relevant failure paths. Inspect
   existing callers as well as changed ones. Enumerate distinct production effects
   before grouping their code. Mark broken or missing wiring.
2. **Build a many-to-many source map.** Assign meaningful hunks, symbols, wiring,
   removals, and coverage to candidate outcomes. One commit may contain multiple
   features; one feature may span several commits, including early commits with
   no consumers. Neither shared files nor separate commits settle ownership.
3. **Close each vertical path.** Combine implementation with the downstream
   adoption needed for its outcome. Follow later corrections, moves, and renames
   to their semantic owner. A correction to a feature introduced within the stack
   belongs to that feature; a fix to preexisting behavior may be independent.
   Record when the outcome first works and any later revision to its contract.
4. **Challenge separation and merging.** Ask whether removing the other candidate
   leaves a useful, complete capability on its declared prerequisites. Split when
   both capabilities have distinct outcomes and valid paths; combine when the
   proposed units only provide horizontal fragments of the same outcome. A
   dependency between two complete capabilities does not make them one feature.
   A later optional capability is its own candidate when the earlier behavior
   already works and the extension has a distinct usable contract. Do not absorb
   it just because it extends the same path. Co-location in a commit is never
   evidence that an unrelated production effect supports another feature; require
   a demonstrated causal or contract dependency for that ownership.
5. **Resolve shared support explicitly.** A helper serving several features is
   not automatically a standalone feature. Give its necessary introduction to a
   complete first adopter, with later adopters depending on that contract, unless
   independence is demonstrated. Record shared ownership and incremental changes
   without counting the same implementation twice. Do not merge all consumers
   simply because they share a helper or form a connected dependency graph.
6. **Reconcile the timeline and scope.** Preserve meaningful migrations, removals,
   compatibility stages, and capabilities introduced then removed before the tip.
   Distinguish durable outcomes from abandoned scaffolding or rewrites. A net
   diff alone cannot make this distinction. Include merge-resolution behavior;
   do not attribute it automatically to either branch.

Apply the same reasoning to internal refactors and maintenance: show the existing
production behavior they preserve or repair. Keep genuinely independent support,
verification, documentation, and noise visible without forcing every source hunk
to be a new feature. Uncertainty is a reported gap, not evidence of independence.

When complexity or coupling affects inferred boundaries, distinguish interactions
required by the feature's contract from dependencies imposed by the existing
architecture. Cite requirements and producer/consumer paths, allowing mixed or
uncertain causes. Do not treat architectural entanglement as proof that outcomes
are one feature. Record the actual dependency and any bounded separation proposal
without assuming that the architecture can be changed within this task.

## Tell the big picture

Identify whether the stack's features combine into a solution to a larger
problem. State that problem, the intended outcome, and the observable conditions
that would establish success. Use supplied requirements when available; label
inferred goals and success conditions as provisional. Do not invent a unifying
goal for unrelated work or treat the stack's implemented subset as the full goal.

Keep the big-picture narrative focused on the primary goal. Omit internal fixes,
refactors, and migrations from that narrative unless they are themselves the
primary goal; retain their ownership, dependencies, and evidence in the detailed
feature map and commit inventory. Assess their effect on goal completion without
turning supporting implementation work into additional headline goals.

Explain how the features cooperate to produce the overall outcome, including
base-provided capabilities and prerequisites outside the stack. Connect each
required success condition to feature labels and concrete end-to-end evidence.
Check the composition itself: individually complete features may still leave
missing integration, incompatible contracts, or uncovered paths between them.
Serving one larger goal does not erase independently meaningful feature boundaries.

Assess whether the selected tip meets the overall goal: met, partially met,
unmet, or unverified, with reasons grounded in the evidence. Distinguish known
delivery gaps from missing validation or uncertain intent; passing component
tests alone does not prove the combined solution works. Keep intermediate
achievements separate from what remains usable at the tip. Identify required
remaining work separately from optional future extensions, naming the existing
owners and contracts those extensions would build on without counting them as
present delivery.

## Record each commit's role and later fate

Include a source-commit inventory alongside the feature map. For every commit,
give its revision, actual behavior or state change, and these explicit fields;
split the evidence by hunk or symbol when a commit mixes work:

- **Later code fate:** whether code introduced or changed here is later
  refactored, moved, replaced, corrected, or removed within the inspected scope.
  Name the affected code and later revisions, distinguish structural changes
  from contract changes, and identify any meaningful intermediate state. Report
  no later change found or unverified when appropriate; a later edit to the same
  file alone does not establish that this code was refactored.
- **Consumer status:** whether each changed producer or mechanism has a real
  production consumer at this commit and at the selected tip. Identify existing
  consumers, the first later adopting revision, and any subsequent loss of use.
  Explicitly list code still lacking consumers, or justify its independent
  contract under the rules above. Distinguish verified absence from incomplete
  tracing; tests and hypothetical future adoption do not close the gap.
- **Development line:** stable label(s) for the coherent thread of work advanced
  by this commit, such as a capability, migration, or structural refactor. Define
  each line's purpose and connect its commits, feature owners, and dependencies.
  A line may span several features or commits; it is neither a Git branch nor
  proof of a single feature boundary. Assign mixed commits to multiple lines
  with their respective hunks; identify shared support and uncertain membership
  rather than forcing one classification from chronology or shared files.

Carry these fields into any per-commit summary handed to a calling workflow.
Use the code timeline and adoption evidence to classify development lines, not
commit titles alone. Later refactoring or delayed adoption informs ownership;
it does not by itself make a meaningful source milestone disposable.

## Hand off a reusable feature map

Lead with the big picture: the larger problem and primary goal(s), how
the features form the solution, and the goal assessment with supporting evidence
and remaining gaps. Preserve this assessment when handing the map to a calling
workflow so it can judge overall completion as well as individual features.

Use stable feature labels independent of source commit numbers. Scale the detail
to the stack, but retain these facts for each candidate:

- **Outcome and status:** the concrete contract and whether it is delivered,
  incomplete, removed later, or unverified; classify independent nonfeature work.
- **Vertical evidence:** entry point → changed mechanism → downstream production
  consumer → effect, with revision and source locations. For independence,
  provide the explicit justification instead of a fabricated downstream caller.
- **Source ownership:** source commits and relevant hunks or symbols, including
  scattered adoption and fixes; show where a mixed commit splits among features.
- **Dependencies and milestones:** base-provided contracts, other feature labels,
  shared support owners, and the state where adoption becomes complete. Distinguish
  semantic dependencies from chronological order or textual overlap.
- **Validation and gaps:** checks supporting the contract, inspection versus
  execution, missing consumers, unresolved intent, and confidence with reasons.

Reconcile all meaningful source changes with this map, including nonfeature work
and omissions with reasons. Explain where inferred boundaries disagree with the
original slices. Reserve justified extension seams by naming the existing owner
and contract that future work would extend; future consumers do not establish
present adoption or complete an unfinished feature.

Keep feature recognition separate from commit scheduling: a feature can have
meaningful incremental milestones, and shared prerequisites need explicit order.
The calling review, split, or restack skill decides target commits, fixes, and
mutations within its own authorization. Other skills can invoke this skill by
name and consume this map; this skill requires no companion skill.

## Boundary examples

| Actual changes | Recognition |
| --- | --- |
| One commit adds CSV export and repairs login expiry. | Two outcomes with their own production paths; split the mixed source ownership. |
| Early commits add an encoder and tests; a later commit wires it into export. | One export feature spanning the commits; encoder tests are not its consumer. |
| A helper changes; unchanged production callers already reach it. | Adoption can be complete without editing a caller; trace the changed effect through those callers. |
| A complete export path is followed by optional compression and its wiring. | Two vertical capabilities if export works without compression; compression depends on export. |
| Export and upload share a new encoder. | Distinct outcomes can share support; assign its introduction to a complete adopter or justify independent value. |
| Export and upload are complete, but the stated goal is automatic off-site backup and nothing connects them. | Preserve the two feature boundaries; the larger goal is only partially met because the automatic end-to-end path is missing. |
| A new API has only tests and an unused export. | Incomplete or unused support unless an independently useful external contract is established. |
| A migration enables a real compatibility path and a later commit removes it. | Preserve the meaningful intermediate outcome even if the tip no longer contains it. |
