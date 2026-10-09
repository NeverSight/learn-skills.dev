---
name: start-flutter-craft
description: Use when starting any conversation - establishes how to find and use Flutter development skills, requiring Skill tool invocation before ANY response including clarifying questions
---

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST read the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. This is not optional. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

# Using Flutter-Craft Skills

You have access to Flutter-specific development skills that follow **Feature-Driven Development** with **Clean Architecture** principles.

## The Rule

**Check for skills BEFORE ANY RESPONSE.** This includes clarifying questions. Even 1% chance means invoke the Skill tool first.

```
User message received
    ↓
Might any skill apply? (even 1%?)
    ├─ YES → Invoke Skill tool: flutter-craft:<skill-name>
    │        → Announce: "Using [skill] to [purpose]"
    │        → Has checklist? → Create a todo entry per item (task tracking tool)
    │        → Follow skill exactly
    └─ NO  → Respond (including clarifications)
```

## Available Skills

### Project Setup Skills

| Skill | When to Use |
|-------|-------------|
| **flutter-project-init** | Creating a NEW Flutter project from scratch |

### Core Workflow Skills

| Skill | When to Use |
|-------|-------------|
| **flutter-brainstorming** | Before ANY new feature, component, or creative work |
| **flutter-planning** | After brainstorming, to create detailed implementation plan |
| **flutter-executing** | When you have a plan file to execute (batch of 3 tasks) |
| **flutter-verification** | Before claiming ANY work is complete |
| **flutter-debugging** | Before fixing ANY bug or error |

### Testing & Review Skills

| Skill | When to Use |
|-------|-------------|
| **flutter-testing** | When writing tests (priority: Repository → State → Widget) |
| **flutter-review-request** | After completing implementation, before merge |
| **flutter-review-receive** | When processing code review feedback |

### Utility Skills

| Skill | When to Use |
|-------|-------------|
| **flutter-subagent-dev** | For parallel task implementation with 2-stage review |
| **flutter-parallel-agents** | When 2+ independent tasks can run in parallel |
| **flutter-worktrees** | When isolated workspace needed for feature development |
| **flutter-finishing** | When all tasks complete, to decide merge/PR/keep/discard |
| **flutter-writing-skills** | When creating new skills for flutter-craft |

## Red Flags

These thoughts mean STOP—you're rationalizing:

| Thought | Reality |
|---------|---------|
| "This is just a simple widget" | Widgets need architecture. Check for skills. |
| "I'll just add a quick feature" | Features need brainstorming. Check first. |
| "Let me fix this bug quickly" | Bugs need systematic debugging. Check first. |
| "The code is done, it should work" | Verify before claiming done. Check for skills. |
| "This doesn't need Clean Architecture" | All Flutter code benefits from structure. |
| "I'll write tests later" | Testing priority exists for a reason. Check first. |
| "This is obvious, no planning needed" | Simple things become complex. Use planning. |
| "Let me just check the code first" | Skills tell you HOW to explore. Check first. |

## Flutter-Specific Triggers

| Context | Required Skill |
|---------|---------------|
| User says "new project", "create project", "start project" | flutter-project-init |
| User says "add feature", "create", "build" | flutter-brainstorming → flutter-planning |
| User says "fix bug", "error", "not working" | flutter-debugging |
| Plan file (`*-plan.md`) exists in docs/plans/ | flutter-executing |
| About to say "done", "complete", "fixed" | flutter-verification FIRST |
| User says "review", "check my code" | flutter-review-request |
| Multiple independent tasks identified | flutter-parallel-agents |

## Lightweight Path (small changes)

The full brainstorm → plan → execute chain is for **new features and behavior
changes**. It is NOT required for trivial work. If ALL of these hold:

- Single file (or a comment/typo/rename across files)
- No new behavior, no state management change, no new dependency
- No architecture decision to make

then make the change directly and invoke **flutter-verification** only.
When in doubt whether a change is trivial, it isn't — use the full chain.

## Skill Priority

When multiple skills could apply, use this order:

1. **Process skills first** (brainstorming, debugging) - these determine HOW to approach
2. **Implementation skills second** (executing, testing) - these guide execution
3. **Completion skills last** (verification, finishing) - these ensure quality

Example flows:
- "Add login feature" → flutter-brainstorming → flutter-planning → flutter-executing
- "Fix auth bug" → flutter-debugging → flutter-verification
- "Fix typo in a label" → direct edit → flutter-verification (lightweight path)
- "Review my code" → flutter-review-request

## Clean Architecture Reminder

All Flutter code should follow Clean Architecture layers:

```
lib/
└── features/
    └── <feature_name>/
        ├── domain/          # Entities, UseCases, Repository interfaces
        ├── data/            # Models, DataSources, Repository implementations
        └── presentation/    # Widgets, State Management (BLoC/Provider/Riverpod)
```

## REQUIRED SUB-SKILL Chaining

Some skills REQUIRE invoking another skill after completion:

- **flutter-brainstorming** → MUST invoke → **flutter-planning**
- **flutter-executing** → MUST invoke → **flutter-verification** (each batch)
- **flutter-executing** (all done) → MUST invoke → **flutter-finishing**
- **flutter-debugging** → MUST invoke → **flutter-verification**

## User Instructions

Instructions say WHAT, not HOW. "Add X" or "Fix Y" doesn't mean skip workflows.

**REMEMBER: If in doubt, invoke the skill. It's better to check and not need it than to skip and miss important steps.**
