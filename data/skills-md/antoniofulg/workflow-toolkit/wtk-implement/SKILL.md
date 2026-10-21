---
name: wtk-implement
description: 'Implement approved modular work from a `.tasks` source into a `.checks` checklist, prove each check, and leave independent verification to the coordinator. Use for modular work; not Lean feature artifacts or undecided work.'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club - github.com/tech-leads-club
  version: 0.1.0
---

# TLC Implement

Implement approved modular work: extract the checks, build, and leave independent verification to
the coordinator. The checklist fixes obligations; implementation decomposition is yours.

Before execution, read [execution metrics](../wtk/references/execution-metrics.md) and return the
assigned stage receipt with session identity, interval and baseline/snapshot counters after its
source checks, using the normal handoff format.

Before delegated work, follow [agent selection](../wtk/references/agent-selection.md); use the
accepted stage settings and selected skill in the current checkout, without mandatory native roles.

Before environment setup or handoff, apply [runtime lifecycle](../wtk/references/runtime-lifecycle.md)
to the checkout's application/test services.

When the source requires reuse, construction order or approval, apply
[construction constraints](../wtk/references/construction-constraints.md) during Extract, Build
and verification handoff. At phase boundaries or context recovery, use
[context handoff](../wtk/references/context-handoff.md).

## Profile and handoff

The project declares `profile: light|standard|ui` and optional `handoff: on|off` in `AGENTS.md` or
equivalent. Absent a declaration, use `light` and `handoff: on`; the resolver may set a stronger
profile. A project budget overrides the 150k-token default. Handoff affects build batching only,
never independent verification.

| Profile | Adds |
| --- | --- |
| `light` | proofs at `HEAD`, named tests exist and ran, one located assertion per check, level/sampling gaps, and `Swept existing` re-read |
| `standard` | light plus recomputed `Coverage`, `Test policy` verdicts, and one fault per assertion surface |
| `ui` | standard plus binding-source comparison and per-screen copy and arrangement enumeration; read [screens.md](references/screens.md) |

Use the `ui` profile for binding interface sources. The profile is a floor and the report names it. Empty inputs are recorded as such, not treated as
passes. Read `references/test-policy.md` only for `standard` or `ui` checklist rows.

## Critical rules

1. Every check names its **proof**: the test or command whose exit code settles it.
2. Tests assert checklist outcomes, never the implementation. Never weaken, skip, or delete one to
   pass a suite; a wrong check stops for user clarification.
3. The checklist and test-policy rows are fixed while building. `Landing` is additive: record a new
   door with its literal shape and rejected alternative before writing the closing code.
4. A build agent never spawns another agent at all. The coordinator dispatches one fresh sub-agent as Verifier after
   the last batch, never the author or a child of the builder. An approved checklist authorizes local edits and commits
   only; push, deploy, and production data changes require explicit authorization.

## Extract

Apply [project requirements](../wtk/references/project-requirements.md) before deriving checks:
read applicable rules and required driver guidance, carry source-backed landings from the task,
and reconcile missing or changed obligations. The coordinator obtains the shared criteria review
before dependent feature build, reusing an upstream review when it covers the complete contract.

Read the approved `.tasks/<name>.md` source completely, then ground its checks in the touched code
and existing conventions. Refuse a claim without a nameable proof, concrete value, or explicit
boundary; ask when the source leaves a real decision open rather than guessing.

Reuse the approved source's Swept dispositions and map them to checklist checks or existing proof.
Revisit only missing, contradictory, or changed inputs. When no upstream sweep exists, perform it
once across validation, failure modes, idempotency/retry, authorization, concurrency/ordering, data
lifecycle, external-dependency failure, state transitions, and observability. Record each landing
as a check, existing behaviour, `n/a - <reason>`, or unresolved question. Under `ui`, a
design marked binding supplies concrete screen values; read [screens.md](references/screens.md).
Under `light` or `standard`, skip that reference.

### Format

After Extract and its sweep, read [checklist-format.md](references/checklist-format.md) and write the
`.checks/<feature>.md` artifact. Do not load the format during the first source pass.

## Build

Apply [project requirements](../wtk/references/project-requirements.md#build-and-recover), including
the inherited guidance, criteria-review disposition and blocking prerequisites under every profile.

For a selected image or design, load [UI/UX](../wtk/references/ui-ux.md) before coding;
freeze its contract and complete the builder capture/compare/fix loop before handoff.


Write tests from the checklist, implement the minimum requested change, run each proof, and commit
coherent pieces with Conventional Commits. Do not add unrequested capability or unrelated refactors;
an edge test is useful when it asserts a named expected outcome.

Decide newly discovered doors without blocking on routine choices, then append their literal shape and
rejected alternative to `Landing` **before** writing the closing code and in that code's commit. Never
rewrite an approved row. A red proof triggers diagnosis, a code fix, and a rerun; only a wrong or
impossible check, or an approved unbuildable row, stops for renegotiation. A new non-contradictory door
is additive and does not stop the build.

### When one agent is not enough

Use one builder by default. Estimate context and record a split under `## Handoff` only when a
concrete context limit or planned transfer requires it. Pack **whole slices** under the declared
budget (150k tokens by default); never split a slice. Before handoff, record closed checks, user decisions, and
abandoned approaches. Handoff occurs only on green, with every proof in the batch passing; the next
builder reads the checklist and landed diff, not a narrative. If one slice exceeds the budget, report
that the upstream task cut it too coarsely. `handoff: off` keeps one builder in one session;
recover after compaction through the shared context handoff reference above.

## Verify

After the feature's last batch, the coordinator dispatches one fresh Verifier over the complete
feature range with every check. The builder reports and stops; it never dispatches verification or
writes the final verdict. See [verify.md](references/verify.md).

## Knowledge chain

Use existing code and conventions, project docs, library docs, then web search; mark anything still
uncertain. Never invent an API, flag, command, or behaviour.

## Output

Produce the checklist or implementation, lead with the verdict, and report closed checks, proof
results, deviations, and commit hashes. Do not write `verification.md` as builder.
