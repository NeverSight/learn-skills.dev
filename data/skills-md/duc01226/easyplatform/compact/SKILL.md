---
name: compact
description: '[Tooling & Meta] Compress conversation context to optimize tokens'
---

# Compact Context

Proactively compress the current conversation context to optimize token usage.

## When to Use

- Before starting a new task in a long session
- When working on multiple unrelated features
- At natural workflow checkpoints (after commits, PR creation)
- When context indicator shows high usage

## Actions

1. **Summarize completed work** - What was done, key decisions made
2. **Preserve essential context** - Active file paths, current task, blockers
3. **Clear redundant history** - Old exploration, superseded plans
4. **Update memory** - Save important patterns to `.claude/memory/`

## Best Practices

- Use `/compact` at natural breakpoints, not mid-task
- After compacting, briefly restate the current objective
- Check that critical file paths are still accessible
- If working on a bug, preserve error messages and stack traces

## Context Preservation Checklist

Before compacting, ensure you've saved:

- [ ] Current branch and uncommitted changes status
- [ ] Active file paths being modified
- [ ] Any error messages or stack traces
- [ ] Key decisions and their rationale
- [ ] Pending items from todo list

## Example Usage

```
User: /compact
Claude: Compacting context...

## Session Summary
- Implemented employee export feature
- Fixed validation bug in SaveEmployeeCommand
- Created unit tests for EmployeeHelper

## Active Context
- Branch: feature/employee-export
- Files: Employee.Application/Commands/ExportEmployees/
- Current task: Add pagination to export

## Cleared
- Exploration of unrelated notification code
- Superseded implementation approaches

Ready to continue with pagination implementation.
```

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
