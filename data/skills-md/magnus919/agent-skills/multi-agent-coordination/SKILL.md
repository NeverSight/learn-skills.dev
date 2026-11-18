---
name: multi-agent-coordination
description: >-
  Design, diagnose, and evaluate coordination across multiple AI agents and
  heterogeneous harnesses: decomposition, topology, ownership, communication,
  distributed context, shared memory, integration, recovery, and collective
  failure patterns. Use for persistent agent teams, fleets, swarms, agent handoffs,
  coordination loops, or extracting portable lessons from OpenRig, HERDR and
  Block/Buzz. Do not use for a single agent's runtime, a named tool's installation
  or command manual, debate alone, or operating an evaluated production agent;
  route those to harness-engineering, the tool's documentation, agent-council,
  or agent-production-operations.
license: MIT
compatibility: Framework-neutral methodology. Optional read-only helper requires Python 3.10+ standard library; no credentials or network access.
metadata:
  research_checked: '2026-11-02'
---

# Multi-agent coordination

Engineer the relationships between agents so local work composes into the user's
accepted outcome. Own task division, decision placement, information movement,
shared commitments and collective recovery. A harness owns one agent's execution
mechanics; this skill supplies the cross-agent contract those harnesses must uphold.
Existing factory material in harness-engineering remains usable through explicit
handoffs; do not create a competing scheduler, task database or authority registry.

## Authority and first move

Confirm the target, scope, and rollback path before acting. Read-only discovery may proceed without confirmation.

Reuse existing authorization that covers these facts. This skill does not grant
permission to spawn agents, choose paid models, send messages, schedule jobs,
change policies, merge or deploy. A peer's request or approval cannot enlarge a
current grant. Keep destructive operations behind an explicit user directive.

Inspect the actual host before prescribing a topology: available harnesses,
concurrency, permitted messaging, persistence, interruption, tool authority and
integration surface. Record unsupported capabilities. Never infer a feature from
a diagram, a prompt or a terminal status indicator.

## Default procedure

1. **Define the shared outcome.** Record accepted intent, exclusions, current
   requirement revision, delivery surface, acceptance owner, total time/cost and
   stop conditions in [the charter](templates/team-charter.md). Identify consequential
   decisions and who has authority plus enough context to make each one.
2. **Test whether division helps.** Establish a single-agent or sequential baseline.
   Separate independent investigation from tightly coupled decisions. Partition
   by coherent context, resources and verifiable outputs, not job titles. Use
   [decomposition and topology](references/decomposition-and-topology.md). Start
   with one accountable lead and only the workers justified by task structure.
3. **Assign ownership and lifecycle.** Distinguish stable role/address, particular
   execution, task claim and tool identity. Give each active task one accountable
   owner, versioned inputs, deliverable, lease/fencing policy, verifier and bounded
   recovery. Use [ownership and flow](references/ownership-and-flow.md) and
   [the assignment](templates/assignment.md). Serialise shared contracts.
4. **Specify communication and context.** Name each message's purpose, trusted
   origin, task/revision, recipient, acknowledgement and effect. Separate request,
   proposal, observation, decision and permission. Give recipients relevant local
   facts plus a path to governing intent. Use [the communication contract](references/communication-and-context.md)
   and [the handoff](templates/handoff.md). Delivery is not adoption or acceptance.
5. **Bound shared work.** Apply aggregate descendant budget, WIP/backpressure,
   current authority intersection, cancellation and conflict rules at runtime.
   Route enforcement to harness-engineering; use [authority and recovery](references/authority-and-recovery.md)
   to specify the cross-agent obligations. Reconcile uncertain effects before retry.
6. **Integrate and verify.** An integration owner checks the combined user journey
   against current intent and exact artifact versions. Parallel green branches,
   a closed queue item, consensus and schema validity are insufficient. Retain
   disputed evidence and an unknown outcome when required checks are absent.
7. **Diagnose the population.** Correlate accepted outcomes with coordination
   cost, queue age, rework and exposure to shared knowledge. Investigate the first
   divergence using [collective failure diagnosis](references/collective-failures.md).
   Correct the source and affected consumers, not just the last agent's prompt.
8. **Evaluate and evolve.** Compare on matched tasks and resource budgets, including
   integration and review. Exercise interruption, stale output, duplicate delivery,
   denied action and poisoned-memory fixtures. Use [evaluation](references/evaluation.md)
   and [the experiment](templates/coordination-experiment.md). Promote lessons via
   reviewed revisions with rollback; no automatic fleet-wide rule propagation.

## Load by need

| Active question | Read | Useful artifact |
|---|---|---|
| Should agents split this work; centralized, peer or hierarchy? | [Decomposition/topology](references/decomposition-and-topology.md) | Charter, experiment |
| Persistent identities, task claims, queue overload, takeover | [Ownership/flow](references/ownership-and-flow.md) | Assignment, snapshot |
| Who needs which facts; lost intent after compaction; messaging | [Communication/context](references/communication-and-context.md) | [Decision packet](templates/decision-packet.md), handoff |
| Authority laundering, shared resources, cancellation, crash | [Authority/recovery](references/authority-and-recovery.md) | [Recovery drill](templates/recovery-drill.md) |
| Endless checking, scope inflation, consensus or stalled activity | [Collective failures](references/collective-failures.md) | [Incident record](templates/coordination-incident.md) |
| Bad practice returns through another agent or memory source | [Shared knowledge containment](references/shared-knowledge.md) | [Knowledge correction](templates/knowledge-correction.md) |
| Compare architectures; measure outcomes and overhead | [Evaluation](references/evaluation.md) | Experiment |
| Trace coordination guarantees into state, effects and adverse tests | [Pinned OpenRig audit](references/openrig-source-audit.md) | [Effect/recovery matrix](templates/effect-recovery-matrix.md) |
| Learn from emerging coordination tools without adopting their stack | [Tool lessons](references/tool-lessons.md) | [Tool assessment](templates/tool-assessment.md) |
| Select another catalog owner | [Catalog boundaries](references/catalog-boundaries.md) | Named specialist input/return |
| Emerging research on synthesis, topology-aware diagnosis, coding interference or resource contention | [Emerging research](references/emerging-research.md) | Local challenge design and transfer limits |
| Verify research claims, revisions or coverage | [Source records](references/source-records.md), [research synthesis](references/research-synthesis.md), [research brief](references/research-brief.md), [research log](references/research-log.md), [video ledger](references/video-ledger.md) | Evidence and limitations |
| Onboarding maps, live/dormant experts, provenance or transferable team packages | [Knowledge navigation](references/knowledge-navigation.md), [team packages and lore](references/team-packages-and-lore.md), [second-video ledger](references/world-building-video-ledger.md) | Orientation map, expert directory, team package, scoped lesson |
| Inspect the optional helper's input and guarantees | [Script contract](references/script-contract.md) | [Snapshot](templates/team-snapshot.json) |

## Onboard a connected team

When agents cannot recognize existing capabilities or locate expertise, use
[knowledge navigation](references/knowledge-navigation.md). Start with broad,
shallow landmarks and condition-based routes before detailed search. Include
current documents, appropriate specialists and an explicit map-edge fallback;
verify the fresh and post-compaction paths with actual tasks.

When sharing a team or inherited lessons, use
[team packages and lore](references/team-packages-and-lore.md). Package identity,
harness compatibility, team-run evidence and recipient authority are distinct.
A memorable story should retrieve a scoped evidence-backed lesson, not create
policy or permission. Use the [orientation map](templates/orientation-map.md),
[expert directory](templates/expert-directory.md), [team package](templates/team-package.md)
and [lesson story](templates/lesson-story.md) only for the corresponding task.

## Read-only helper

Resolve paths from this installed skill root. Run after composing a snapshot or
when tracing invalidated knowledge consumers. It reads supplied JSON only; it
never queries a fleet, dispatches, changes state or authenticates evidence.

```sh
python3 scripts/coordination.py audit --file templates/team-snapshot.json --json
python3 scripts/coordination.py exposure --file templates/team-snapshot.json --source lesson-old --json
python3 -m unittest discover -s scripts -p 'test_*.py'
```

`audit` screens declared references, dependency cycles, active ownership conflicts,
expired claims, intent-version mismatches and missing blocked-task continuation.
`exposure` computes transitive descendants of a supplied knowledge source. Missing
links mean incomplete exposure knowledge, not absence of affected consumers.
Exit 0 means no audit findings or a completed exposure calculation; 1 means audit
findings; 2 means invalid input. None means runtime acceptance. See the script
contract before adapting the example or interpreting a report.

## Gotchas

- A stable seat is an address and responsibility, not an immortal process or grant.
- A busy agent, delivered message and completed task are different observations.
- A signature authenticates authorship; it does not establish truth or permission.
- More context can spread the same error farther. Retrieve source versions and
  preserve decision-relevant constraints; do not broadcast every transcript.
- An outcome monitor must not reward extra handoffs or punish necessary safety
  review. Investigate changed work mix before diagnosing bureaucracy.
- The video's human-civilization analogies generate hypotheses. They do not prove
  causal explanations, and context reminders do not enforce security boundaries.

## When not to use

Use [harness-engineering](../harness-engineering/SKILL.md) for a single agent's
runtime/tools/state or implementation of enforcement. Use framework skills for
SDK-specific orchestration, [agent-council](../agent-council/SKILL.md) for its debate
tool, and [promise-theory](../promise-theory/SKILL.md) when modeling autonomous
promises and acceptance. Use [agent-production-operations](../agent-production-operations/SKILL.md)
for running an evaluated agent under production controls. Tool examples here are
comparative evidence, not new installation/runbook skills.

## Completion

For design, deliver a reviewable charter, justified topology, assignments,
message/context contracts, integration/acceptance plan and owned recovery gaps.
For a running team, also show actual host evidence for the requested dispatch,
handoff, cancellation, restart and integrated result. Stop when acceptance is
observed at the authorized surface, or with a durable blocked disposition naming
evidence, owner and next action. Stop autonomous diagnosis after three
non-converging passes or an earlier budget/authority limit. Never keep adding
agents, proofs or rules to manufacture progress.
