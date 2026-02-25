---
name: agent-team-builder
description: >
  Designs and executes multi-agent teams to accomplish complex tasks through iterative collaboration,
  quality gates, and refinement loops. Use when a user wants to accomplish any non-trivial task
  that would benefit from specialised agents working in sequence or parallel - e.g. writing an
  article, building a software feature, conducting research, producing a marketing campaign,
  designing a system, creating educational content, or any task that naturally decomposes into
  research → planning → execution → review → refinement stages. Triggers on phrases like "build
  me a team to...", "use agents to...", "orchestrate agents for...", or when a task is complex
  enough that a single agent would benefit from decomposition into specialists.
---

# Agent Team Builder

Design and execute a bespoke multi-agent team for any complex task. Always follow these four phases in order.

## Phase 1: Task Intake

Ask the user the following (combine into one message, avoid multiple rounds of questioning):

**Required:**
- What is the task goal and any key constraints?
- What does "done well" look like? (success criteria)
- Tone, style, or audience if relevant

**Quality gate preferences** (for each major stage):
- Human approval: user reviews output and decides pass/loop
- Automated review: a dedicated critic agent decides pass/loop, user only sees final output
- Offer to configure per-stage during blueprint review

Use `AskUserQuestion` for structured intake where choices are discrete. Use free-text follow-up for open-ended requirements.

## Phase 2: Team Design

After intake, design the agent team:

1. **Decompose** the task into 4–8 specialist roles. See `references/team-patterns.md` for role libraries by task category.
2. **Define the workflow**: sequential pipeline, parallel branches, or hybrid. Most tasks follow: `Research → Plan → Execute → Review → Refine → Finalise`.
3. **Assign quality gates**: at each handoff point, decide (based on user preferences) whether the gate is human or automated (critic agent).
4. **Define loop conditions**: what triggers a revision loop vs. passing the gate? Be explicit.
5. **Name the team**: short kebab-case slug (e.g. `article-team`, `feature-team`).

## Phase 3: Blueprint Presentation

Present the team design for approval before spawning anything. Format:

```
## Team: [team-name]
**Goal:** [one sentence]

### Agents
| # | Role | Responsibility | Agent Type |
|---|------|---------------|------------|
| 1 | Researcher | ... | general-purpose |
| 2 | Planner | ... | general-purpose |
...

### Workflow
[Stage 1: Role → Role] → [GATE: human/automated] → [Stage 2: Role → Role] → ...

### Quality Gates
- Gate 1 (after [stage]): [human/automated] — passes when: [criterion]
- Gate 2 (after [stage]): [human/automated] — passes when: [criterion]

### Loop Conditions
- If Gate 1 fails: [specific revision instruction to agent N]
- Max iterations: [N] before escalating to user
```

Wait for explicit user approval. Offer to adjust roles, gates, or workflow before proceeding.

## Phase 4: Execution

After approval, execute the team. See `references/execution-guide.md` for full tool syntax and patterns.

**Execution sequence:**
1. Create the team with `TeamCreate`
2. Create all tasks with `TaskCreate` (establish dependencies with `addBlockedBy`)
3. Spawn the orchestrator agent via the `Task` tool — this agent manages all other agents
4. The orchestrator: spawns worker agents, monitors task completion, enforces quality gates, routes revision loops, and shuts down the team when done

**Orchestrator responsibilities (communicate clearly in its prompt):**
- Spawn each worker agent in sequence/parallel per the approved workflow
- At each quality gate: run the gate (human via `AskUserQuestion` or automated via a critic `Task`)
- On gate failure: send revision instructions back to the relevant agent, increment loop counter
- On max iterations exceeded: surface the issue to the user and ask how to proceed
- On all gates passed: compile final output and deliver to user, then shut down team

**Keep the user informed:** After spawning, tell the user what's running and where to watch for gate approvals (if any are human-gated).

## Key Principles

- **Iterative by default**: every pipeline should have at least one refinement loop
- **Explicit gate criteria**: vague gates (e.g. "good quality") cause infinite loops — make criteria specific and measurable
- **Max iterations**: always set a maximum (default: 3) to prevent runaway loops
- **Fail loudly**: if an agent produces unusable output, escalate to the user rather than silently looping
- **Right-size the team**: 4–6 agents is the sweet spot; more adds coordination overhead without quality gains
