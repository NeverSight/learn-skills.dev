---
name: sdd-implementation
description: Execute planned implementations following todo-lists systematically. Use for code generation, building features, and executing SDD plans.
---

# SDD Implementation Skill

Build what has been planned, following specs and todo-lists precisely.

## When to Use

- Executing planned implementations
- Code generation from specifications
- Building features according to plan

## Protocol

### Step 1: Load the Plan
Read: `plan.md` → `spec.md` → `tasks.md` → `todo-list.md`

### Step 2: Execute Systematically
1. **Read entire list** before starting
2. **Execute in order** — respect dependency chains
3. **Mark completion** — `- [ ]` → `- [x]` immediately
4. **Document blockers** — never skip silently, use `[BLOCKED: reason]`

### Step 3: Follow Patterns
Reference `references/patterns.md` for project conventions and implementation patterns.

### Step 4: Track Progress
Use `scripts/progress.sh` to visualize completion status.

### Step 5: Report

```markdown
## Implementation Summary

### Completed
- [x] Task 1: description

### Files Created/Modified
- `path/to/file.ts`: [purpose]

### Blockers Encountered
- [blocker and resolution]

### Discoveries
- [anything that should update specs]
```

## Anti-Patterns

- Skipping tasks without explanation
- Marking items done without completing them
- Implementing differently than planned without noting why
- Ignoring blockers instead of documenting them

## Integration

- After completion, `sdd-verifier` subagent validates work (spawned as child subagent in 2.5+)
- Discoveries trigger `sdd-evolve` skill for spec updates
- Use the ask question tool for ambiguous requirements
