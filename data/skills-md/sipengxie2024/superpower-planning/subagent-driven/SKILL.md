---
name: subagent-driven
description: Use when executing implementation plans with independent tasks in the current session
---

# Subagent-Driven Development

Execute plan by dispatching fresh subagent per task, with two-stage review after each: spec compliance review first, then code quality review. Each subagent gets its own planning directory for structured knowledge capture.

**Core principle:** Fresh subagent per task + per-agent planning dir + two-stage review (spec then quality) = high quality, fast iteration

## NON-NEGOTIABLE: Two-Stage Review Gate

<EXTREMELY-IMPORTANT>
Every task MUST pass TWO independent reviews before it can be marked complete:

1. **Spec Compliance Review** — Dispatch `./spec-reviewer-prompt.md` subagent
2. **Code Quality Review** — Dispatch `./quality-reviewer-prompt.md` subagent (only after spec review passes)

A task is NOT complete until BOTH reviews return APPROVED. No exceptions — not for "simple" tasks, config changes, or thorough self-reviews.

The Task Status Dashboard in `.planning/progress.md` has `Spec Review` and `Quality Review` columns. Both MUST show `PASS` before status can be `complete`.
</EXTREMELY-IMPORTANT>

## When to Use

```dot
digraph when_to_use {
    "Have implementation plan?" [shape=diamond];
    "Tasks mostly independent?" [shape=diamond];
    "Stay in this session?" [shape=diamond];
    "subagent-driven" [shape=box];
    "executing-plans" [shape=box];
    "Manual execution or brainstorm first" [shape=box];

    "Have implementation plan?" -> "Tasks mostly independent?" [label="yes"];
    "Have implementation plan?" -> "Manual execution or brainstorm first" [label="no"];
    "Tasks mostly independent?" -> "Stay in this session?" [label="yes"];
    "Tasks mostly independent?" -> "Manual execution or brainstorm first" [label="no - tightly coupled"];
    "Stay in this session?" -> "subagent-driven" [label="yes"];
    "Stay in this session?" -> "executing-plans" [label="no - parallel session"];
}
```

**vs. Executing Plans (parallel session):**
- Same session (no context switch)
- Fresh subagent per task (no context pollution)
- Per-agent planning directories (structured knowledge capture)
- Two-stage review after each task: spec compliance first, then code quality
- Faster iteration (no human-in-loop between tasks)

## The Process

```dot
digraph process {
    rankdir=TB;

    subgraph cluster_per_task {
        label="Per Task";
        "Create agent planning dir (if not exists)" [shape=box style=filled fillcolor=lightyellow];
        "Dispatch implementer subagent (./implementer-prompt.md)" [shape=box];
        "Implementer subagent asks questions?" [shape=diamond];
        "Answer questions, provide context" [shape=box];
        "Implementer subagent implements, tests, commits, self-reviews" [shape=box];
        "Dispatch spec reviewer subagent (./spec-reviewer-prompt.md)" [shape=box];
        "Spec reviewer subagent confirms code matches spec?" [shape=diamond];
        "Implementer subagent fixes spec gaps" [shape=box];
        "Dispatch code quality reviewer subagent (./quality-reviewer-prompt.md)" [shape=box];
        "Code quality reviewer subagent approves?" [shape=diamond];
        "Implementer subagent fixes quality issues" [shape=box];
        "Aggregate agent findings into top-level .planning/" [shape=box style=filled fillcolor=lightyellow];
        "Mark task complete via TaskUpdate" [shape=box];
    }

    "Read plan, extract all tasks with full text, note context, create tasks via TaskCreate" [shape=box];
    "More tasks remain?" [shape=diamond];
    "Dispatch final code reviewer subagent for entire implementation" [shape=box];
    "Use superpower-planning:finishing-branch" [shape=box style=filled fillcolor=lightgreen];

    "Read plan, extract all tasks with full text, note context, create tasks via TaskCreate" -> "Create agent planning dir (if not exists)";
    "Create agent planning dir (if not exists)" -> "Dispatch implementer subagent (./implementer-prompt.md)";
    "Dispatch implementer subagent (./implementer-prompt.md)" -> "Implementer subagent asks questions?";
    "Implementer subagent asks questions?" -> "Answer questions, provide context" [label="yes"];
    "Answer questions, provide context" -> "Dispatch implementer subagent (./implementer-prompt.md)";
    "Implementer subagent asks questions?" -> "Implementer subagent implements, tests, commits, self-reviews" [label="no"];
    "Implementer subagent implements, tests, commits, self-reviews" -> "Dispatch spec reviewer subagent (./spec-reviewer-prompt.md)";
    "Dispatch spec reviewer subagent (./spec-reviewer-prompt.md)" -> "Spec reviewer subagent confirms code matches spec?";
    "Spec reviewer subagent confirms code matches spec?" -> "Implementer subagent fixes spec gaps" [label="no"];
    "Implementer subagent fixes spec gaps" -> "Dispatch spec reviewer subagent (./spec-reviewer-prompt.md)" [label="re-review"];
    "Spec reviewer subagent confirms code matches spec?" -> "Dispatch code quality reviewer subagent (./quality-reviewer-prompt.md)" [label="yes"];
    "Dispatch code quality reviewer subagent (./quality-reviewer-prompt.md)" -> "Code quality reviewer subagent approves?";
    "Code quality reviewer subagent approves?" -> "Implementer subagent fixes quality issues" [label="no"];
    "Implementer subagent fixes quality issues" -> "Dispatch code quality reviewer subagent (./quality-reviewer-prompt.md)" [label="re-review"];
    "Code quality reviewer subagent approves?" -> "Aggregate agent findings into top-level .planning/" [label="yes"];
    "Aggregate agent findings into top-level .planning/" -> "Mark task complete via TaskUpdate";
    "Mark task complete via TaskUpdate" -> "More tasks remain?";
    "More tasks remain?" -> "Create agent planning dir (if not exists)" [label="yes - next task"];
    "More tasks remain?" -> "Dispatch final code reviewer subagent for entire implementation" [label="no"];
    "Dispatch final code reviewer subagent for entire implementation" -> "Use superpower-planning:finishing-branch";
}
```

## Per-Agent Planning Directories

Each agent role gets ONE directory, reused across all tasks:

```bash
mkdir -p .planning/agents/{role}/
```

Example:
```bash
mkdir -p .planning/agents/implementer/
mkdir -p .planning/agents/spec-reviewer/
mkdir -p .planning/agents/quality-reviewer/
```

Each agent planning dir contains:
- `findings.md` - Discoveries, decisions, critical items (appended across tasks)
- `progress.md` - Step-by-step progress log (appended across tasks)

**Do NOT create per-task directories** like `implementer-task-1/`, `implementer-task-2/`. One directory per role, updated continuously.

Include the planning dir path in the agent's prompt using `./implementer-prompt.md` template.

## Orchestrator Aggregation Flow

After each task completes (both reviews passed), aggregate the agent's findings:

1. **Read** the agent's `.planning/agents/{role}/findings.md` and `progress.md`
2. **Extract** items marked with `> **Critical for Orchestrator:**` plus any errors and test results
3. **Append** extracted items to top-level `.planning/findings.md` under a task heading
4. **Update** top-level `.planning/progress.md`:
   - **Update the Task Status Dashboard table** at the top (add/update the row for this task)
   - **Append** completion details to the session log section

Example aggregation:
```markdown
<!-- Append to .planning/findings.md -->
## Task 2: Recovery modes
- [From implementer] Database migration requires careful ordering
- [From spec-reviewer] All requirements met after fix pass
- [From quality-reviewer] Approved with no issues

<!-- Update Task Status Dashboard table in .planning/progress.md -->
| Task 1: Hook installation | ✅ complete | PASS | PASS | agents/implementer/ | 5 tests passing |
| Task 2: Recovery modes | ✅ complete | PASS (2nd pass) | PASS | agents/implementer/ | 8 tests passing |
| Task 3: Config parser | ⏳ pending | - | - | - | - |

<!-- Append to session log in .planning/progress.md -->
- [x] Task 2: Recovery modes - COMPLETED
  - Implementer: 8 tests passing, committed
  - Spec review: Passed (2nd pass after fix)
  - Quality review: Approved
```

## Prompt Templates

- `./implementer-prompt.md` - Dispatch implementer subagent (includes planning dir injection)
- `./spec-reviewer-prompt.md` - Dispatch spec compliance reviewer subagent
- `./quality-reviewer-prompt.md` - Dispatch code quality reviewer subagent

## Example Workflow

```
You: I'm using Subagent-Driven Development to execute this plan.

[Read plan file once: docs/plans/feature-plan.md]
[Extract all 5 tasks with full text and context]
[Create all tasks via TaskCreate]

Task 1: Hook installation script

[Create .planning/agents/implementer/ (if not exists)]
[Dispatch implementation subagent with full task text + context + planning dir]

Implementer: "Before I begin - should the hook be installed at user or system level?"

You: "User level (~/.config/superpowers/hooks/)"

Implementer: "Got it. Implementing now..."
[Later] Implementer:
  - Implemented install-hook command
  - Added tests, 5/5 passing
  - Self-review: Found I missed --force flag, added it
  - Committed
  - Logged findings to .planning/agents/implementer/findings.md

[Dispatch spec compliance reviewer with its own planning dir]
Spec reviewer: Spec compliant - all requirements met, nothing extra

[Get git SHAs, dispatch code quality reviewer]
Code reviewer: Strengths: Good test coverage, clean. Issues: None. Approved.

[Aggregate: read agent findings, append to .planning/findings.md and progress.md]
[Mark Task 1 complete]

Task 2: Recovery modes

[Reuse .planning/agents/implementer/ (already exists from Task 1)]
[Dispatch implementation subagent with full task text + context + planning dir]

Implementer: [No questions, proceeds]
Implementer:
  - Added verify/repair modes
  - 8/8 tests passing
  - Self-review: All good
  - Committed

[Dispatch spec compliance reviewer]
Spec reviewer: Issues:
  - Missing: Progress reporting (spec says "report every 100 items")
  - Extra: Added --json flag (not requested)

[Implementer fixes issues]
Implementer: Removed --json flag, added progress reporting

[Spec reviewer reviews again]
Spec reviewer: Spec compliant now

[Dispatch code quality reviewer]
Code reviewer: Strengths: Solid. Issues (Important): Magic number (100)

[Implementer fixes]
Implementer: Extracted PROGRESS_INTERVAL constant

[Code reviewer reviews again]
Code reviewer: Approved

[Aggregate agent findings into .planning/]
[Mark Task 2 complete]

...

[After all tasks]
[Dispatch final code-reviewer]
Final reviewer: All requirements met, ready to merge

Done!
```

## Advantages

**vs. Manual execution:**
- Subagents follow TDD naturally
- Fresh context per task (no confusion)
- Parallel-safe (subagents don't interfere)
- Subagent can ask questions (before AND during work)
- Per-agent planning dirs capture knowledge persistently

**vs. Executing Plans:**
- Same session (no handoff)
- Continuous progress (no waiting)
- Review checkpoints automatic

**Efficiency gains:**
- No file reading overhead (controller provides full text)
- Controller curates exactly what context is needed
- Subagent gets complete information upfront
- Questions surfaced before work begins (not after)
- Planning dirs prevent knowledge loss between subagents

**Quality gates:**
- Self-review catches issues before handoff
- Two-stage review: spec compliance, then code quality
- Review loops ensure fixes actually work
- Spec compliance prevents over/under-building
- Code quality ensures implementation is well-built
- Aggregation preserves findings for future tasks

**Cost:**
- More subagent invocations (implementer + 2 reviewers per task)
- Controller does more prep work (extracting all tasks upfront)
- Review loops add iterations
- But catches issues early (cheaper than debugging later)

## Red Flags

**Never:**
- **Skip reviews** — see Two-Stage Review Gate above. No exceptions.
- Start implementation on main/master branch without explicit user consent
- Dispatch multiple implementation subagents in parallel (conflicts)
- Make subagent read plan file (provide full text instead)
- Skip scene-setting context (subagent needs to understand where task fits)
- Ignore subagent questions (answer before letting them proceed)
- Accept "close enough" on spec compliance (reviewer found issues = not done)
- Start code quality review before spec compliance passes (wrong order)
- Skip planning dir creation or aggregation step (knowledge gets lost)

**If subagent asks questions:**
- Answer clearly and completely
- Provide additional context if needed
- Don't rush them into implementation

**If reviewer finds issues:**
- Implementer (same subagent) fixes them
- Reviewer reviews again
- Repeat until approved
- Don't skip the re-review

**If subagent fails task:**
- Dispatch fix subagent with specific instructions
- Don't try to fix manually (context pollution)

## Integration

**Required workflow skills:**
- **superpower-planning:git-worktrees** - RECOMMENDED: Set up isolated workspace unless already on a feature branch
- **superpower-planning:writing-plans** - Creates the plan this skill executes
- **superpower-planning:requesting-review** - Code review template for reviewer subagents
- **superpower-planning:finishing-branch** - Complete development after all tasks

**Subagents should use:**
- **superpower-planning:tdd** - Subagents follow TDD for each task

**Alternative workflow:**
- **superpower-planning:executing-plans** - Use for parallel session instead of same-session execution
