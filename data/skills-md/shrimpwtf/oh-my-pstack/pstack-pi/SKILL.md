---
name: pstack-pi
description: "Pi runtime adapter for poteto-mode. Maps canonical pstack roles and lifecycle protocols to Pi-compatible task agents, batching, isolation, follow-ups, and durable result resources."
---

# pstack on Pi

`poteto-mode` is the sole router. It selects the playbook, canonical role, step order, and lifecycle protocol. This adapter translates those choices to Pi-compatible runtimes. It never selects a playbook, repeats the playbook index, or changes a playbook gate.

While this skill is active, its role map is the specific pstack execution contract. Generic host instructions remain valid outside pstack work.

## Canonical role map

Use the live host's configured names. This reference mapping targets OMP, a
Pi-based runtime; other hosts must substitute their own names through the runtime
contract.

| Canonical role | Pi/OMP agent | Contract |
|---|---|---|
| `explorer` | `scout` | Read-only repository reconnaissance, trace reduction, narrow audits. |
| `watcher` | `scout` | Observe one exact generation or external-state transition, then terminate. |
| `planner` | `designer` | Technical planning, architecture, decomposition, sequencing, and non-visual design candidates. |
| `designer` | `designer` | Visual, interaction, and product-design candidates. |
| `reviewer` | `reviewer` | Independent code, protocol, behavioral, or security review. |
| `researcher` | `librarian` | Source-verified external library, framework, API, protocol, or version research. |
| `synthesizer` | `reviewer` | Cross-report synthesis, adjudication, and advisory judgment over frozen evidence. |
| `implementer` | `task` | Bounded implementation or test changes with explicit write ownership. |
| `owner` | `task` | One coupled multi-step implementation session retained through IRC follow-ups. |
| `mechanical` | `sonic` | Fully specified low-judgment edits. Ambiguity returns to the root. |

The reference OMP roster is closed:

```text
scout
designer
reviewer
security-reviewer
librarian
task
sonic
```

A canonically routed task item's `agent` value must be one of those bundled names. Canonical role labels and model aliases are not agent names.

`poteto-agent` and `comment-sicko` are custom compatibility agents for direct named seams in imported skills. A direct compatibility call may use that custom agent name; ordinary canonical routing never does.

### Planning distinction

The imported warning about a built-in planning subagent describes a source-host mechanism that bypassed the skill contract. This Pi-compatible package has no bundled `plan` agent. Canonical `planner` work uses `designer` with a technical-planning brief and does not pass source-host subagent fields.

### Security review

Use `security-reviewer` for an independent security lane. Keep it read-only and separate from ordinary code review when both are required. A later `reviewer` session may synthesize frozen reports; it does not replace the primary security review.

## Task contract

The root coordinator performs every `task` call through the host task facility. A child never calls `task`, starts another child, or asks the user directly. Put `Do not call task or start subagents` under `FORBIDDEN` in every child brief.

Children start without the parent conversation. Every prompt must stand alone. They receive the configured workspace, context files, skills, and approved plan resources supplied by the host.

### One task

When the flat schema is active:

```json
{
  "name": "parser-overflow-worker",
  "agent": "task",
  "task": "GOAL\n...\n\nROLE\n...\n\nSCOPE\n...\n\nCONTEXT\n...\n\nACCEPTANCE\n...\n\nVERIFY\n...\n\nTIMEBOX\n...\n\nFORBIDDEN\n...\n\nREPORT\n...\n\nSTANDING\n...",
  "isolated": true
}
```

When batch mode is active, use a one-item `tasks[]` call instead of inventing a per-call batch switch.

Use `isolated: true` for a writer that needs a dedicated worktree. Read the returned isolation metadata and verify the patch, branch, or applied change the host reports. Use a non-isolated session for a long-lived owner that must accept follow-ups in the same workspace.

### Batched panel

Use one batch call for independent participants:

```json
{
  "context": "Shared immutable repository, base SHA, artifacts, constraints, and verification context.",
  "tasks": [
    {
      "name": "candidate-a",
      "agent": "designer",
      "task": "Standalone brief for architecture candidate A.",
      "isolated": false
    },
    {
      "name": "candidate-b",
      "agent": "designer",
      "task": "Standalone brief for architecture candidate B.",
      "isolated": false
    }
  ]
}
```

Each `name` is unique. `context` contains common immutable material. Each item still names its exact role, slice, acceptance criteria, verification, forbidden work, and report contract.

Start every participant in one batch before consuming any verdict. Separate writers with isolated workspaces or disjoint output paths. Freeze candidate artifacts before starting reviewers. Freeze reviewer reports before starting a separate synthesizer session.

### Background completion and follow-ups

Background task results arrive through the host's async result delivery. Record the returned job and agent identifiers. The preview may be truncated.

- Read the full result from `agent://<id>`.
- Read the session transcript from `history://<id>` when the report is incomplete, ambiguous, or suspicious.
- Use `hub` with `op: "jobs"` to inspect jobs and `op: "wait"` with `ids` to wait for specific job IDs.
- Use `hub` with `op: "list"` to inspect peers and `op: "send"` with `to` for one in-scope correction, answer, authorization, or next coupled phase.
- Use `hub` with `op: "cancel"` and exact job `ids` for stale, superseded, or scope-breaching work.
- A follow-up to a parked session revives the same session when the host reports that capability.
- Never steer a reviewer toward a preferred conclusion.
- Use only operations exposed by the live `hub` schema. Do not invent lifecycle operations.
- Ignore duplicate terminal deliveries and reject stale artifact generations.

A task result is evidence, not completion. The root inspects the artifact and runs verification.

## Brief shape

A dispatch is forbidden until its brief contains:

**GOAL**  
One-sentence outcome executable by a stranger.

**ROLE**  
The canonical role, mapped OMP agent, authority, and expected stance.

**SCOPE**  
Writable and non-writable paths, exact slice or race arm, worktree and branch where applicable, and every output path. State the one-writer assignment.

**CONTEXT**  
Repository root, relevant source paths, base SHA, frozen artifacts, active skill and playbook paths, settled assumptions, and known gotchas.

**ACCEPTANCE**  
Checkable observable outcomes, one per line.

**VERIFY**  
Exact commands, fixtures, runtime probes, comparison baselines, environment requirements, and known false-positive or false-negative risks.

**TIMEBOX**  
A rough cap. At the cap, return partial evidence and stop instead of broadening scope.

**FORBIDDEN**  
At minimum: no child task calls; no subagent spawning; no out-of-scope fixes; no unrequested migrations; no shared-path edits outside ownership; no merge; no direct user questions; no completion claim without executed verification.

**REPORT**  
Require `PASS | ISSUES | BLOCKED`, semantic session name, branch and exact SHAs where applicable, verdict and evidence, changed files or artifacts, actual verification commands and results, deviations, unresolved risks, and parent actions.

**STANDING**  
Copy the active playbook's standing policy text verbatim when it supplies one.

## Canonical protocols

### Bounded session

1. Author one standalone brief.
2. Start one task with the mapped agent.
3. Record its semantic name, agent ID, job ID, role, scope, isolation mode, base SHA, and expected artifact.
4. Consume the async result when delivered.
5. Read `agent://<id>`; inspect `history://<id>` when needed.
6. Send one IRC correction only within the same unit.
7. Inspect the artifact and independently run the promised verification.
8. Accept the unit only after the parent verifies the reported output.

A role or unit change requires a fresh task.

### Panel

1. Partition independent slices or race arms with one task per participant.
2. Start every participant in one batch before consuming any result.
3. Track participants by semantic name and identifiers, never arrival order.
4. Wait for every required result through `hub` `op: "wait"`, or cancel it explicitly through `hub` `op: "cancel"`.
5. Ignore duplicate terminal delivery.
6. Freeze implementation artifacts, branches, head SHAs, reports, and hashes.
7. Start every independent reviewer in a new batch only after the candidates are frozen.
8. Freeze verdicts before starting a separate `reviewer` when synthesis is needed.
9. Treat synthesis as advice. The root selects and verifies.

Do not mix implementers, reviewers, or synthesizers in one session. Do not let reviewers race a moving head.

### Long-lived owner

1. Start one non-isolated `task` session with the complete owner brief.
2. Record its agent ID and reuse it. Do not start a sibling owner for the same unit.
3. The owner works only in its assigned branch and paths and never starts children.
4. Send a `hub` `op: "send"` follow-up only for the next coupled phase, an in-scope correction, an answer resolved from evidence, or explicit authorization.
5. Require a terminal report at each verification boundary.
6. Independently verify the boundary before authorizing the next phase.
7. Stand down on ownership violation, stale generation, or terminal scope breach.

### One-shot watcher

1. Start one background `scout` task.
2. Put the exact branch, head SHA, generation, watched predicate, stop predicate, and timebox in the brief.
3. Require one meaningful event and a terminal report.
4. Discard a report whose generation no longer matches.
5. Start a fresh watcher for each new generation.
6. Stand down when the stop predicate is met or the work is superseded.

A watcher observes. It does not fix, merge, authorize, or silently follow a changed head.

## Interactions and decisions

Children resolve uncertainty from source, standing policy, frozen evidence, or the brief. Otherwise they use the safest reversible interpretation and report the assumption, or return `BLOCKED` with the exact missing decision and evidence gathered.

The root resolves a child question and sends the answer through `hub` `op: "send"` to the existing agent. Ask the user only for genuine product preference, unavailable authority, or an irreversible action not covered by standing orders.

## Ownership and verification

- One writer per branch, worktree, mutable state, and output path.
- Separate sessions own implementation, review, judgment, and synthesis.
- A task stays inside its assigned unit and role.
- Isolate concurrent writers unless their outputs are structurally disjoint.
- A worker's report never verifies its own work.
- Record branch, base SHA, and exact head SHA or artifact generation.
- Prefer behavioral proof over type-check-only evidence.
- A new commit, restack, conflict resolution, or applied patch creates a new generation that voids the prior verdict.
- Judges and synthesizers advise. The root owns selection, user interaction, external writes, merges, deletion, and final truth.
- Claim model independence only from returned resolved-model and fallback metadata.

## Model routing

OMP resolves a task agent through its current settings, including `modelRoles`, `task.agentModelOverrides`, the agent definition, and normal fallback. Agent selection and model selection are separate decisions.

Do not put a `model` field in a task item. Do not use a model alias as the `agent` value. Configure routing through the installed OMP settings and report the actual resolved model when independence matters.

Recommended role aliases:

| OMP agent | Recommendation |
|---|---|
| `scout` | `@smol` |
| `designer` | `@designer` |
| `reviewer` | `@advisor` |
| `security-reviewer` | `@advisor` |
| `librarian` | `@smol` |
| `task` | `@task` or a stronger implementation role |
| `sonic` | `@tiny` or `@smol` |

These are recommendations, not task payload fields.

## Writing

Apply `unslop` to every reply, brief, report, review, task dispatch, commit message, and agent-facing edit.
