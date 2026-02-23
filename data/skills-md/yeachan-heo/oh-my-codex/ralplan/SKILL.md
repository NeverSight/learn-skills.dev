---
name: ralplan
description: Alias for /plan --consensus
---

# Ralplan (Consensus Planning Alias)

Ralplan is a shorthand alias for `/plan --consensus`. It triggers iterative planning with Planner, Architect, and Critic agents until consensus is reached.

## Usage

```
/ralplan "task description"
```

## Behavior

This skill invokes the Plan skill in consensus mode:

```
/plan --consensus <arguments>
```

The consensus workflow:
1. **Planner** creates initial plan
2. **User feedback**: **MUST** use `AskUserQuestion` to present the draft plan before review (Proceed to review / Request changes / Skip review)
3. **Architect** reviews for architectural soundness
4. **Critic** evaluates against quality criteria
5. If Critic rejects: iterate with feedback (max 5 iterations)
6. On Critic approval: **MUST** use `AskUserQuestion` to present the plan with approval options
7. User chooses: Approve, Request changes, or Reject
8. On approval: **MUST** invoke `/ralph` for execution -- never implement directly

Follow the Plan skill's full documentation for consensus mode details.
