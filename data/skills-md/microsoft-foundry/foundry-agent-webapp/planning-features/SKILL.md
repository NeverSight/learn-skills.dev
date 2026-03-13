---
name: planning-features
description: >
  Provides structured plan template for feature implementation.
  Use when planning new features, multi-file changes, or
  creating implementation roadmaps before coding.
---

# Feature Planning

> **Tip:** For read-only planning mode, press **Shift+Tab** in VS Code or Copilot CLI to enter built-in plan mode.

## Research-First Workflow

1. **Understand the request** — clarify scope and success criteria
2. **Search the codebase** for existing patterns and relevant files
3. **Load relevant skills** from `.github/skills/` for project conventions
4. **Generate a structured plan** using the template below

### Research Guidelines

- Search existing patterns before proposing new ones — reuse what the codebase already does
- Read relevant skills (e.g., `writing-csharp-code`, `writing-typescript-code`, `writing-bicep-templates`) to follow project conventions
- Check current implementations in files you plan to modify so the plan reflects actual code structure

## Required Plan Structure

Every plan must include these sections:

### 1. Overview
2-3 sentence description of the feature or change.

### 2. Requirements
```markdown
- [ ] Requirement one
- [ ] Requirement two
```

### 3. Files to Modify

| File Path | Changes |
|-----------|---------|
| `path/to/file` | Description of modifications |

### 4. Files to Create

| File Path | Purpose |
|-----------|---------|
| `path/to/new/file` | What this file does |

### 5. Implementation Steps
Numbered steps with sub-steps. Reference skill patterns where applicable.

```markdown
1. Step one
   - Sub-step referencing `writing-csharp-code` skill patterns
   - Sub-step with specific code location
2. Step two
   - Sub-step referencing `writing-typescript-code` skill patterns
```

### 6. Testing Checklist
```markdown
- [ ] Manual verification step one
- [ ] Manual verification step two
```

### 7. Edge Cases
Document each edge case and how the implementation should handle it.

### 8. Documentation Updates
If the plan affects state machines, SSE events, or API endpoints, include updates to `ARCHITECTURE-FLOW.md`. Load the `understanding-architecture` skill for validation rules.
