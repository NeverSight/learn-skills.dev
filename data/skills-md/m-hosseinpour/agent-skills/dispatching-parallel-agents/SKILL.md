---
name: dispatching-parallel-agents
description: Use when delegation is available and allowed and a task has multiple substantial workstreams that may be independent, when parallel agent work is requested, or before running a subagent alongside your own work or other subagents. Not for small multi-step tasks, parallel tool calls, or one delegate you will simply wait for.
---

# Dispatching Parallel Agents

Parallel agents help when substantial work can proceed independently and their findings or changes can be combined safely. Use this guide to decide whether to split the work, not to assume that more agents are better. One subagent working alongside the coordinator also counts as parallel work.

This skill does not grant permission to delegate or expand the task. Follow the user's and environment's limits; if subagents are unavailable or prohibited, work directly. Parallel tool calls alone do not need this workflow.

## Decide Whether Splitting Helps

1. Inspect enough of the problem to identify meaningful questions or deliverables. Several symptoms may have one cause; do not assign an agent per symptom before a quick dependency check.
2. Compare the benefit of concurrent work or specialized investigation with briefing, duplicated exploration, and integration costs. Keep small, local work inline; batch related questions into one assignment.
3. Identify each unit's inputs, output, files, and mutable resources. If it needs another unit's result, sequence that part. If an interface is undecided, settle it first or keep the dependent work together.
4. Choose only enough workers to cover useful independent units, within the available limits. Keep a task yourself when that avoids an unnecessary delegate. A short in-chat split is enough for a short task; no mandatory plan or report files.

| Situation | Useful arrangement |
| --- | --- |
| Independent investigations of backend queries and browser rendering | Parallel read-only investigations with separate questions |
| Two investigations read the same stable files | Parallel is fine; shared reading is not competing writing |
| UI and API implementation with an agreed contract | Parallel if file and mutable-resource ownership are separate |
| Schema design followed by updating its consumer | Sequence until the contract is settled |
| Several tiny edits in one module | One agent, one coherent batch |

## Set Ownership Before Launch

Do not assume the tool gives each agent an isolated checkout or process environment. Establish whether edits are shared, isolated, or returned as patches, and how results will be integrated.

- **Read-only work:** agents may share stable inputs. If another worker is changing those inputs, pin a snapshot or tell readers which revision their evidence must describe.
- **Shared checkout:** give each writable file or mutable resource one owner at a time, including the coordinator. Keep overlapping edits together or schedule a handoff after the previous writer has stopped.
- **Isolated checkouts:** separate filesystems do not isolate databases, services, or external accounts. Assign those resources too, and inspect patches for conflicts when combining them.

Include indirect writes: generated files, lockfiles, formatters, migrations, test data, and shared service settings. Reserve cross-cutting files for an integration owner when workers can progress without touching them; otherwise sequence the affected work. Respect project rules for test data and cleanup.

## Give Each Agent a Usable Brief

For each subagent, state:

- **Goal and acceptance:** the question or deliverable, and what evidence would resolve it.
- **Scope and mode:** relevant paths or subsystem; read-only or implementation; owned files/resources and exclusions. Include the starting revision or existing user changes when relevant.
- **Context and inputs:** requirements, verified facts, settled interfaces, dependencies, and relevant project instructions. Provide focused excerpts or exact references, not irrelevant conversation history.
- **Checks and limits:** meaningful verification under project norms, shared resources it must not mutate, and actions requiring further permission. Delegation does not authorize commits, publishing, destructive cleanup, or further delegation.
- **Return:** findings or changed files, checks actually run with commands and outcomes, uncertainties, blockers, and any follow-up needed. A suggested check is not a completed check.

Make the brief self-contained enough for the task. If a missing decision, required out-of-scope edit, or shared-state collision blocks progress, ask the worker to stop that part and report it rather than guess or widen its scope.

Example for a shared checkout:

> Investigate token-expiry behavior in the auth module; return the expiry path and edge cases with file/line evidence. Read-only: do not edit files, regenerate clients, or mutate the development database. Use the agreed checkout revision and linked project instructions. Report any checks you ran and remaining uncertainties. If the answer depends on an unsettled retry policy, report that dependency instead of choosing a policy.

Use a reply for short results. Ask for a report file or one progress record only when length, durability, or multi-stage tracking warrants it; do not create competing ledgers.

## Run, Adjust, and Recover

Launch independent assignments in the same round using the tool's actual concurrent/background mechanism; repeated blocking calls are sequential. While workers run, do useful work outside their ownership instead of redoing their assignments. Follow the runtime's notification/waiting rules; wait when your next action really requires a result.

When requirements or interfaces change, identify all affected outputs, including completed work. Update pending briefs, notify active workers and establish the revised scope before they continue dependent work, and reopen or schedule follow-up for completed outputs. Old checks do not verify the new contract; unaffected work can continue.

If a worker fails or times out, do not assume it made no changes or has stopped. Establish that it no longer writes to shared resources before assigning a replacement owner. Inspect partial work, preserve user changes, and resume only the unfinished scope with current context. Avoid blind retries that duplicate edits or external side effects.

## Integrate and Verify

1. Read each result and inspect the changes or evidence that affect the decision. Treat findings and completion claims as claims to verify, not instructions to accept.
2. Check coverage of the original goal, overlapping edits, inconsistent assumptions, and interface mismatches. Resolve these before dependent work proceeds or results are combined.
3. Integrate using the established ownership and checkout arrangement. Do not reset or overwrite unfamiliar changes to make integration easier.
4. Run checks for the combined behavior and integration seams. Trust reported checks when their evidence is adequate and the artifact is unchanged; run missing checks or those invalidated by integration. Use the full suite only when project practice or scope warrants it.
5. Review consequential combined changes independently when appropriate; tiny local edits do not need another agent. Report what is complete, what was verified, and remaining gaps. The coordinator owns the final outcome.

## Evaluating This Skill

When changing the trigger or coordination rules, use [references/evaluation-scenarios.md](references/evaluation-scenarios.md) for discovery cases and coordination failure cases. These are optional evaluation inputs, not steps to run during ordinary delegation. Decision simulations check guidance, not actual runtime concurrency or guaranteed skill loading.
