---
name: trae-rules-writer
description: "Create Trae IDE rules (.trae/rules/*.md) for AI behavior constraints. Use when user wants to: create a project rule, set up code style guidelines, enforce naming conventions, make AI always do X, or customize AI behavior for specific files. Triggers on: '创建 rule', 'project rule', '.trae/rules/', 'AGENTS.md', 'CLAUDE.md', 'make AI always use PascalCase'. Do NOT use for skills (use trae-skill-writer) or agents (use trae-agent-writer)."
---

# Trae Rules Writer

Create Trae IDE rules by analyzing project conventions first, then designing rules that match existing patterns.

## Workflow

```
1. ANALYZE  → Scan project structure, code style (ls .trae/rules/, cat AGENTS.md)
2. IDENTIFY → What conventions exist? What needs guidance?
3. DESIGN   → Choose rule type and application mode
4. CREATE   → Write rules in Trae's official format
```

## Rule Format

```markdown
---
description: When to apply this rule (for intelligent mode)
globs: "*.ts,*.tsx"
alwaysApply: false
---

# Rule Title

Concise guidance for AI.
```

## Application Modes

| Mode                | Frontmatter                      | Use Case                      |
| ------------------- | -------------------------------- | ----------------------------- |
| Always Apply        | `alwaysApply: true`              | Global conventions (naming)   |
| File-Specific       | `globs: "*.tsx,*.jsx"`           | Language-specific rules       |
| Apply Intelligently | `description: "When doing X..."` | Context-dependent guidance    |
| Manual Only         | (no frontmatter)                 | Invoke with `#RuleName`       |

## Rule Types

| Type          | Location                  | Scope           |
| ------------- | ------------------------- | --------------- |
| User Rules    | Settings > Rules & Skills | All projects    |
| Project Rules | `.trae/rules/*.md`        | Current project |

## Compatible Files

| File              | Description                |
| ----------------- | -------------------------- |
| `AGENTS.md`       | Reusable across IDEs       |
| `CLAUDE.md`       | Compatible with Claude Code|
| `CLAUDE.local.md` | Local-only, gitignored     |

## Example

```
User: "Create rules for this TypeScript React project"

Analysis:
- Structure: src/components/, src/hooks/
- Naming: PascalCase components, camelCase functions
- No existing .trae/rules/

Creating: .trae/rules/

📄 code-style.md
---
alwaysApply: true
---
# Code Style
- PascalCase for components and types
- camelCase for functions and variables

📄 react-patterns.md
---
globs: "*.tsx,*.jsx"
---
# React Patterns
- Use functional components with hooks
- Custom hooks go in src/hooks/
```

## References

- [Application Mode Examples](examples/application-modes.md) - Complete examples
- [Rule Template](assets/rule.md.template) - Starter template
