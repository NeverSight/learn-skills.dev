---
name: orchestrator
description: >
  Build and deploy parallel execution via subagent waves, agent teams, and
  multi-wave pipelines. Use when the Decomposition Gate identifies 2+ independent
  actions or when spawning teams. NOT for single-action tasks or non-parallel work.
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# Orchestration: Subagents, Agent Teams & Parallel Execution

These rules govern ALL parallelization decisions. Apply them on every task.

Not for single-action requests, simple file edits, or sequential-only workflows.

## Dispatch

| $ARGUMENTS | Action |
|------------|--------|
| *(empty)* | Load full orchestration guide; apply Decomposition Gate to current request |
| `pattern <A-F>` | Show the named pattern from `references/patterns.md` |
| `tier` | Display Tier Selection table and model guidance |
| `recovery` | Show the Accounting Rule and Recovery Ladder |

## Canonical Vocabulary

| Canonical Term | Meaning |
|----------------|---------|
| **subagent** | A Task-tool-spawned agent running in parallel within a session |
| **wave** | A batch of parallel subagents dispatched in a single message |
| **team** | A TeamCreate-spawned group of teammates coordinated by a lead |
| **teammate** | A member of an agent team with assigned file ownership |
| **lead** | The orchestrating agent in a team; never implements directly |
| **dispatch** | Send one or more subagents/teammates to execute in parallel |
| **gate** | A mandatory checkpoint that must pass before proceeding |
| **accounting rule** | N dispatched = N resolved; no agent silently dropped |

## 0. Decomposition Gate (MANDATORY before any work)

Before executing any request that involves tool-mediated work:

1. **DECOMPOSE**: List the actions needed (file reads, edits, searches, commands, analyses).
2. **CLASSIFY**: Which actions are independent (no data dependency)? Which are dependent?
3. **DISPATCH**: 2+ independent → parallel Task calls in one message. Mix → parallel first, dependent after. All dependent → single session.
4. **CONFLICT CHECK**: Two independent actions editing the same file → make those sequential; all others remain parallel.
5. **TRACK**: For orchestrated work, create TaskCreate entries before dispatch (see Section 7).

**Fast path**: Single-action requests skip directly to single session.

**Explore-first path**: Cannot decompose without exploration → dispatch parallel exploration subagents first (Pattern F Wave 1), then re-enter this gate.

**User override**: Explicit user requests for a specific execution approach take precedence.

### Common rationalizations (all invalid)
- "It's faster to do it myself" — Parallel subagents complete N tasks in time of the slowest 1.
- "The task is too simple" — If it has 2+ independent actions, parallelize them.
- "I'll just do this one thing first" — Decompose BEFORE doing anything.

### Mode constraints
- **Plan mode**: Read-only subagents only. No teams, no write-capable agents.
- **Implementation mode**: All tiers available. Default to highest applicable tier.
- **Delegate mode**: Lead orchestrates only. All implementation via teammates/subagents.

### Skill integration
When a superpowers skill is active, the gate operates WITHIN the skill's execution structure:
- **Phase-gated skills**: Parallelize within each phase. Do not parallelize across phase boundaries.
- **Per-task review loop skills**: The skill's sequential structure takes precedence. Parallelize exploration within each task, not across tasks.
- **Dispatch-precondition skills**: The skill's "Don't use when" conditions remain valid. The gate does not override skill-level safety guards.

---

## 1. Tier Selection (mandatory — highest applicable tier wins)

| Tier | Mechanism | Use when | Model |
|------|-----------|----------|-------|
| **Team + waves** | TeamCreate | 3+ domain-crossing streams, coordination needed | opus (default) |
| **Subagent wave** | Task tool, parallel calls | 2+ independent actions, no inter-agent communication | opus (default), sonnet for routine/mechanical only |
| **Single session** | Direct execution | Only 1 action, OR all actions share file dependencies | N/A |

Select the highest tier whose criteria are met. Never select a lower tier to reduce cost.

---

## 2. Subagent Best Practices

### Spawning
- **One response, multiple Task calls.** All independent subagents MUST be dispatched in the same message.
- Use `run_in_background: true` for subagents whose results are not needed immediately.
- N independent actions = N parallel subagents. Merge only when they share file/directory scope.

### Prompt-tuning
- Give every subagent a detailed, self-contained prompt with exact file paths, expected output format, and domain context.
- Do NOT rely on the subagent inheriting conversation history — it does not.

### Model selection
- `opus` — default for ALL subagents. Use for implementation, analysis, reasoning, reviews.
- `sonnet` — ONLY for routine, mechanical tasks: straightforward file lookups, basic searches.
- `haiku` — ONLY for trivial, zero-risk tasks. Never for anything requiring judgment.

### Context management
- Delegate verbose operations (test suites, log parsing, doc fetching) to subagents.
- Use subagent resumption (agent ID) for multi-phase work rather than spawning fresh.
- After a wave completes, apply the Accounting Rule (Section 4) before synthesizing.

---

## 3. Agent Team Best Practices

- Start with 2-4 teammates. Scale up only when justified.
- Assign each teammate a distinct domain and non-overlapping file ownership.
- Aim for 5-6 tasks per teammate — productive yet manageable for check-ins.
- Include all task-specific context in spawn prompts: file paths, architecture decisions, acceptance criteria.
- Use delegate mode to prevent the lead from implementing work itself.
- Never assign two teammates overlapping file ownership.
- The lead must not proceed to synthesis until all teammate tasks are accounted for (Section 4).

---

## 4. Quality Gates & Failure Recovery

### The Accounting Rule (MANDATORY after every parallel dispatch)

When N agents are dispatched, all N must be accounted for before proceeding:

1. **COLLECT**: Wait for all N agents to return. Poll with `TaskOutput` block=false for timeout detection.
2. **TALLY**: Results received vs dispatched. Missing = unresolved.
3. **RESOLVE** all non-successes via the Recovery Ladder (see `references/patterns.md`).
4. **GATE**: Do NOT advance until every agent has SUCCESS or explicit SKIP.
5. **REPORT**: Summarize all agent outcomes via TaskUpdate before proceeding.

### Hooks for automated enforcement
- **TeammateIdle** hook: prevent teammates from idling before work is verified.
- **TaskCompleted** hook: prevent tasks from closing before tests pass.
- Both use exit code 2 to send feedback and keep the teammate/task active.

---

## 5. Orchestration Patterns

| Pattern | Name | Use When | Details |
|---------|------|----------|---------|
| A | Parallel subagent wave | 2-6 independent subtasks in a session | see `references/patterns.md` |
| B | Agent team with file ownership | Cross-domain features, large refactors | see `references/patterns.md` |
| C | Competing hypotheses | Debugging, architecture decisions | see `references/patterns.md` |
| D | Plan-then-swarm | Large tasks needing human approval | see `references/patterns.md` |
| E | Teams of subagent-using teammates | Very large tasks, nested parallelism | see `references/patterns.md` |
| F | Multi-wave pipeline | Explore → implement → verify phases | see `references/patterns.md` |

---

## 6. Limitations

- No session resumption for teammates (`/resume` and `/rewind` won't restore them).
- No nested teams (teammates can use subagents but cannot spawn teams).
- One team per session. Clean up before starting a new one.
- Lead is fixed — cannot transfer leadership.
- All teammates inherit the lead's permission mode at spawn.
- Subagent resumption may not recover from all failure modes (re-spawn instead).
- No built-in timeout detection — orchestrator must poll with `TaskOutput` manually.
- Recovery re-spawns count toward the session's agent budget.

---

## Critical Rules

1. Never dispatch independent actions sequentially — all independent Task calls MUST appear in one response.
2. Always run the Decomposition Gate before any tool-mediated work; skipping it is never acceptable.
3. Never reduce parallelism, tier, or model quality for any reason — cost is not a constraint; always use opus unless the task unambiguously qualifies for sonnet or haiku.
4. Never silently drop a failed subagent — N dispatched = N accounted for; apply the Accounting Rule after every wave.
5. Never advance to Wave N+1 with unresolved agents — resolve all agents in Wave N first.
6. Always create TaskCreate entries before dispatching subagent waves or agent teams — silent orchestration is forbidden.
7. Never assign two teammates overlapping file ownership — overlapping edits cause lost work.
8. Always include full context in subagent and teammate prompts — they do not inherit conversation history.

---

## Reference File Index

| File | Content | Read When |
|------|---------|-----------|
| `references/patterns.md` | Detailed patterns A-F with ASCII diagrams, key rules, recovery ladder | Designing parallel execution or selecting a pattern |

---

## 7. Progress Visibility (MANDATORY for orchestrated work)

All orchestrated work must produce structured progress indicators via TaskCreate/TaskUpdate.

| Tier | Requirement | Granularity |
|------|------------|-------------|
| **Subagent wave** | MUST | One task per subagent, created before dispatch |
| **Agent team** | MUST | One task per teammate assignment, created during setup |
| **Single session** (3+ steps) | SHOULD | One task per logical step |

### Rules
- Create tasks before execution begins, not retroactively.
- Each task MUST have a descriptive `activeForm` in present continuous tense naming the specific action and target.
- Update tasks to `in_progress` before starting, `completed` immediately after.
- After wave completion + accounting, summarize all agent outcomes before dispatching the next wave.
