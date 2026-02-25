---
name: team-driven
description: Use when executing implementation plans with Agent Teams for parallel task execution and context resilience. Preferred over subagent-driven when tasks are heavy or parallelizable.
---

# Team-Driven Development

Execute plan by creating an Agent Team with persistent implementer teammates and a dedicated reviewer. Teammates work in parallel on independent tasks, with the reviewer providing continuous quality gates.

**Core principle:** Persistent teammates + parallel execution + dedicated reviewer = high throughput, context resilience, quality assurance

**Announce at start:** "I'm using the team-driven skill to execute this plan with an Agent Team."

## NON-NEGOTIABLE: Reviewer Must Review Every Task

<EXTREMELY-IMPORTANT>
The reviewer teammate MUST perform BOTH spec compliance and code quality review for every task before it can be marked complete.

**A task is NOT complete until the reviewer DMs the lead with APPROVED.**

You MUST NOT:
- Skip the reviewer for ANY reason ("task was simple", "just a config change")
- Mark a task complete without reviewer approval
- Proceed to the next parallelism group while any task has open review issues

The Task Status Dashboard in `.planning/progress.md` has `Spec Review` and `Quality Review` columns.
A task row MUST show `PASS` in BOTH columns before you can set its status to `complete`.
</EXTREMELY-IMPORTANT>

## When to Use

```dot
digraph when_to_use {
    "Have implementation plan?" [shape=diamond];
    "Tasks heavy OR parallelizable?" [shape=diamond];
    "Stay in this session?" [shape=diamond];
    "team-driven" [shape=box style=filled fillcolor=lightgreen];
    "subagent-driven" [shape=box];
    "executing-plans" [shape=box];

    "Have implementation plan?" -> "Tasks heavy OR parallelizable?" [label="yes"];
    "Have implementation plan?" -> "brainstorm first" [label="no"];
    "Tasks heavy OR parallelizable?" -> "Stay in this session?" [label="yes"];
    "Tasks heavy OR parallelizable?" -> "subagent-driven (lighter tasks, serial)" [label="no - light & serial"];
    "Stay in this session?" -> "team-driven" [label="yes"];
    "Stay in this session?" -> "executing-plans" [label="no - separate session"];
}
```

**Two independent advantages over subagent-driven:**

1. **Parallelism** — Independent tasks execute simultaneously across multiple implementers
2. **Context resilience** — Each teammate has its own full context window. Subagents share the parent's context limit and can crash on heavy tasks. Teammates don't have this problem.

**Even without parallelism, team-driven is preferred for heavy tasks** where a single subagent might hit context limits.

## Team Structure

```
Team Lead (you, current session)
├── implementer-1 (teammate)  ──→ Task A ─┐
├── implementer-2 (teammate)  ──→ Task B ──┤── parallel
├── implementer-N (teammate)  ──→ Task C ─┘
└── reviewer (teammate)       ──→ reviews completed tasks
```

- **Team lead:** Reads plan, creates tasks, assigns work, aggregates findings, updates progress.md
- **Implementers:** Persistent teammates, each works on assigned tasks, DMs reviewer when done
- **Reviewer:** Dedicated teammate for spec compliance + code quality review. DMs implementer for fixes, DMs lead when approved.

## The Process

```dot
digraph process {
    rankdir=TB;

    "Read plan, identify parallelism groups" [shape=box];
    "TeamCreate + spawn implementers + reviewer" [shape=box];
    "Create tasks via TaskCreate with dependencies" [shape=box];
    "Assign Group N tasks to available implementers" [shape=box];

    subgraph cluster_per_task {
        label="Per Task (parallel within group)";
        "Implementer works on task" [shape=box];
        "Implementer DMs reviewer" [shape=box];
        "Reviewer reviews (spec + quality)" [shape=box];
        "Issues found?" [shape=diamond];
        "Reviewer DMs implementer to fix" [shape=box];
        "Reviewer DMs lead: approved" [shape=box];
    }

    "Lead: aggregate findings, update progress.md" [shape=box style=filled fillcolor=lightyellow];
    "More groups?" [shape=diamond];
    "Shutdown team, use finishing-branch" [shape=box style=filled fillcolor=lightgreen];

    "Read plan, identify parallelism groups" -> "TeamCreate + spawn implementers + reviewer";
    "TeamCreate + spawn implementers + reviewer" -> "Create tasks via TaskCreate with dependencies";
    "Create tasks via TaskCreate with dependencies" -> "Assign Group N tasks to available implementers";
    "Assign Group N tasks to available implementers" -> "Implementer works on task";
    "Implementer works on task" -> "Implementer DMs reviewer";
    "Implementer DMs reviewer" -> "Reviewer reviews (spec + quality)";
    "Reviewer reviews (spec + quality)" -> "Issues found?";
    "Issues found?" -> "Reviewer DMs implementer to fix" [label="yes"];
    "Reviewer DMs implementer to fix" -> "Reviewer reviews (spec + quality)" [label="re-review"];
    "Issues found?" -> "Reviewer DMs lead: approved" [label="no"];
    "Reviewer DMs lead: approved" -> "Lead: aggregate findings, update progress.md";
    "Lead: aggregate findings, update progress.md" -> "More groups?";
    "More groups?" -> "Assign Group N tasks to available implementers" [label="yes - next group"];
    "More groups?" -> "Shutdown team, use finishing-branch" [label="no"];
}
```

## Step-by-Step

### Step 1: Read Plan and Identify Parallelism

Read the plan file. Look for the `### Parallelism Groups` section:

```markdown
### Parallelism Groups
- **Group A** (parallel): Task 1, Task 2, Task 3
- **Group B** (after Group A): Task 4, Task 5
- **Group C** (after Group B): Task 6
```

If no parallelism groups are defined, treat each task as its own group (serial execution — still benefits from context resilience).

Determine `MAX_PARALLEL` = largest group size. This is the number of implementer teammates to spawn.

### Step 2: Create Team and Spawn Teammates

```
TeamCreate: team_name="plan-execution"

# Spawn implementers (one per max parallel slot)
Task(team_name="plan-execution", name="implementer-1", subagent_type="general-purpose")
Task(team_name="plan-execution", name="implementer-2", subagent_type="general-purpose")
...

# Spawn reviewer
Task(team_name="plan-execution", name="reviewer", subagent_type="general-purpose")
```

**Implementer teammate prompt:** Use `./implementer-teammate-prompt.md` template.

**Reviewer teammate prompt:** Use `./reviewer-teammate-prompt.md` template.

<EXTREMELY-IMPORTANT>
**FIXED POOL — No New Implementers After Setup**

The implementers spawned in this step are the ONLY implementers for the entire plan execution. You MUST NOT create additional implementers later, regardless of the reason.

- If all implementers are busy → **wait** for one to finish, then assign the next task
- If a new parallelism group has more tasks than implementers → **run in waves** (assign to implementers as they become free)
- NEVER create an implementer named after a task (e.g., `implementer-task6`, `implementer-task-N`) — implementers are named `implementer-1`, `implementer-2`, etc. and are reused across all tasks

Creating new implementers mid-execution wastes resources, fragments context, and violates the persistent-teammate design.
</EXTREMELY-IMPORTANT>

### Step 3: Create Tasks and Set Dependencies

Create all tasks via TaskCreate. Set `addBlockedBy` for tasks in later groups:

```
TaskCreate: "Task 1: ..." (Group A)
TaskCreate: "Task 2: ..." (Group A)
TaskCreate: "Task 3: ..." (Group A)
TaskCreate: "Task 4: ..." (Group B) → addBlockedBy: [1, 2, 3]
TaskCreate: "Task 5: ..." (Group B) → addBlockedBy: [1, 2, 3]
TaskCreate: "Task 6: ..." (Group C) → addBlockedBy: [4, 5]
```

### Step 4: Assign Tasks

For the current group, assign tasks to implementers:

```
TaskUpdate: taskId="1", owner="implementer-1"
TaskUpdate: taskId="2", owner="implementer-2"
TaskUpdate: taskId="3", owner="implementer-3"

SendMessage: type="message", recipient="implementer-1", content="Please work on Task 1: [full task text from plan]"
SendMessage: type="message", recipient="implementer-2", content="Please work on Task 2: [full task text from plan]"
...
```

**IMPORTANT:** Include the full task text in the message. Don't make teammates read the plan file.

### Step 5: Monitor and Aggregate

As teammates complete tasks:

1. **Reviewer approves** → lead receives DM notification
2. **Lead updates progress.md Dashboard** — mark task complete, note key outcome
3. **Lead reads agent planning dirs** — aggregate findings to top-level `.planning/findings.md`
4. **Lead assigns next tasks** to the **same teammate that just finished** if unblocked tasks exist — reuse the existing implementer pool, NEVER spawn new ones

### Step 6: Shutdown

After all tasks complete:

1. Update `.planning/progress.md` with final status
2. Send shutdown requests to all teammates
3. **REQUIRED SUB-SKILL:** Use superpower-planning:finishing-branch

## Per-Agent Planning Directories

Each **persistent teammate** maintains a single planning directory across all tasks:

```bash
mkdir -p .planning/agents/implementer-1/
mkdir -p .planning/agents/implementer-2/
mkdir -p .planning/agents/reviewer/
```

Implementers update the same `findings.md` and `progress.md` as they work on successive tasks. This keeps context continuous rather than fragmented across per-task folders.

**Note:** Subagent-driven follows the same convention — one directory per role (e.g., `implementer/`), reused across tasks. Do NOT create per-task directories like `implementer-task-N/`.

## Prompt Templates

- `./implementer-teammate-prompt.md` — Initial prompt for spawning implementer teammates
- `./reviewer-teammate-prompt.md` — Initial prompt for spawning the reviewer teammate

## Example Workflow

```
You: I'm using Team-Driven Development to execute this plan.

[Read plan: docs/plans/feature-plan.md]
[Identify groups: Group A (Tasks 1,2,3), Group B (Tasks 4,5), Group C (Task 6)]
[MAX_PARALLEL = 3]

[TeamCreate: "plan-execution"]
[Spawn: implementer-1, implementer-2, implementer-3, reviewer]
[Create all 6 tasks via TaskCreate with group dependencies]

=== Group A (parallel) ===

[Assign Task 1 → implementer-1, Task 2 → implementer-2, Task 3 → implementer-3]
[Send full task text to each implementer]

[implementer-1 working on Task 1...]
[implementer-2 working on Task 2...]
[implementer-3 working on Task 3...]

implementer-2 → reviewer: "Task 2 done. [report]"
reviewer → implementer-2: "Missing error handling for edge case X"
implementer-2: fixes issue
implementer-2 → reviewer: "Fixed. [updated report]"
reviewer → lead: "Task 2 approved"

implementer-1 → reviewer: "Task 1 done. [report]"
reviewer → lead: "Task 1 approved"

implementer-3 → reviewer: "Task 3 done. [report]"
reviewer → lead: "Task 3 approved"

[Lead: aggregate findings, update progress.md, unblock Group B]

=== Group B (parallel, after A) ===

[Assign Task 4 → implementer-1, Task 5 → implementer-2]
[implementer-3 is idle — can be shut down or held for Group C]

... same pattern ...

=== Group C ===

[Assign Task 6 → implementer-1]
... reviewer approves ...

[All tasks complete]
[Shutdown team]
[Use finishing-branch skill]
```

## vs Subagent-Driven

| Dimension | Subagent-Driven | Team-Driven |
|-----------|----------------|-------------|
| Parallelism | Serial only | Parallel within groups |
| Context lifetime | One-shot (dies after task) | Persistent (survives across tasks) |
| Context limit | Shares parent's limit | Own full context window |
| Review | New reviewer subagent per task | Persistent reviewer teammate |
| Communication | Through lead only | Peer DM (implementer ↔ reviewer) |
| Cost | Lower (serial execution) | Higher (parallel agents) |
| Best for | Light serial tasks | Heavy tasks, parallelizable work |

## Red Flags

**Never:**
- **Skip the reviewer for any task — this is the #1 rule. NO EXCEPTIONS. Every task MUST be reviewed (spec + quality) before it can be marked complete.**
- **Create new implementers after initial setup** — the implementer pool is fixed at Step 2. If all are busy, WAIT. Never spawn `implementer-task6`, `implementer-taskN`, or any ad-hoc implementer.
- Assign two implementers to tasks that edit the same files
- Let implementers communicate directly with each other (use lead as coordinator for cross-task concerns)
- Proceed to next group before current group is fully reviewed and approved
- Forget to aggregate findings from agent planning dirs

**If teammate goes idle:**
- Idle is normal — it means they're waiting for input
- Send them a message to wake them up with new work
- Don't treat idle as an error

**If teammate hits a blocker:**
- Teammate should DM lead describing the blocker
- Lead resolves (provide info, reassign, or escalate to user)
- Don't let blocked teammates spin

## Integration

**Required workflow skills:**
- **superpower-planning:git-worktrees** — RECOMMENDED: Set up isolated workspace unless already on a feature branch
- **superpower-planning:writing-plans** — Creates the plan with parallelism groups
- **superpower-planning:finishing-branch** — Complete development after all tasks

**Complementary skills:**
- **superpower-planning:verification** — Final verification before declaring done
