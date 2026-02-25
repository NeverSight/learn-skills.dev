---
name: sdd-evolve
description: Update specifications with discoveries made during development. Use when implementation reveals new requirements, constraints, or design changes.
---

# SDD Evolve Skill

Keep specifications in sync with implementation discoveries.

## When to Use

- Implementation reveals new requirements
- Technical constraints discovered during development
- Design changes needed based on learnings
- Edge cases found not in original spec

## Protocol

### Step 1: Categorize the Discovery
- **Discovery**: New information that was unknown
- **Refinement**: Clarification of existing requirement
- **Addition**: New requirement not in original scope
- **Modification**: Change to existing requirement
- **Removal**: Requirement no longer needed

### Step 2: Assess Impact
1. Which spec files are affected?
2. Does this change the plan?
3. Are there downstream impacts?
4. Should implementation pause for review?

### Step 3: Document the Change

```markdown
## Changelog

### [Date] - [Category]: [Brief Description]
**Context**: [Why this change is needed]
**Change**: [What specifically changed]
**Impact**: [How this affects existing work]
**Decision**: [What was decided]
```

### Step 4: Update Specs
Modify the appropriate files: `spec.md`, `plan.md`, `tasks.md`, `todo-list.md`.

## Best Practices

1. **Document immediately** — don't wait until end of implementation
2. **Be specific** — include enough detail to understand later
3. **Link to context** — reference related tasks
4. **Assess impact** — flag if review is needed
5. **Preserve history** — never delete, always add changelog

## Integration

- Called during `sdd-implementer` subagent work
- Triggered by `/evolve` command
- Feeds into future `/audit` runs
- Use the ask question tool if change requires stakeholder input
