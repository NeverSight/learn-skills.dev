---
name: agents-generator
description: Generate product-focused AGENTS.md documentation for AI agents. Use when creating documentation that explains the WHY behind code.
---

# AGENTS.md Generator Skill

Specialized knowledge for generating documentation that helps AI agents understand code in product context.

## When to Use

- Creating AGENTS.md for a component or feature
- Documenting user flows and trust factors
- Helping AI understand the "why" not just "what"

## Core Principle

**Product context > Technical details**

AI agents need to understand:
- What problem this solves
- Who uses it and why
- What success looks like
- What breaks trust
- How errors are recovered

## Template Structure

```markdown
# [Component/Feature Name]

## Product Context

### Problem Solved
[Specific user pain this addresses]

### Users Served
[Personas from personas.md]

### Cognitive Load Eliminated
[What mental burden this removes]

## User Personas

### [Primary Persona]
- **Needs:** [From this feature]
- **Fears:** [What worries them]
- **Success:** [What success looks like]

## Key User Flows

### Flow: [Name]
- **Trigger:** [What starts this]
- **Steps:** 1 → 2 → 3
- **Success Outcome:** [End state]
- **Failure Recovery:** [How to recover]
- **Metrics:** [How measured]

## Trust & Experience

### What Builds Trust
- [Trust builder]

### What Breaks Trust
- [Trust breaker]

### Error Recovery
- [Recovery pattern]

## Technical Context

### Setup
[How to run/test]

### Key Files
- `file` - purpose

### Conventions
- [Convention]

### Related Components
- `component` - relationship

## AI Agent Guidelines

When working on this:
- [Guideline]
- [What to avoid]
```

## Information Sources

To populate AGENTS.md, check:

| Source | What to Extract |
|--------|-----------------|
| `pm-workspace-docs/initiatives/active/[name]/prd.md` | Problem, personas, flows |
| `pm-workspace-docs/initiatives/active/[name]/research.md` | User quotes, pain points |
| `pm-workspace-docs/company-context/personas.md` | Persona details |
| Component stories (`.stories.tsx`) | States, interactions |
| Tests | Expected behavior |
| Existing code | Technical patterns |

## Quality Criteria

Good AGENTS.md documentation:

| Criteria | Check |
|----------|-------|
| Product-first | Problem stated before code |
| Persona-aware | Specific personas named |
| Flow-complete | Entry → success → failure paths |
| Trust-conscious | Build/break factors explicit |
| Actionable tech | Setup instructions work |

## Save Location Pattern

Mirror source structure:

```
Source: elephant-ai/web/src/components/integrations/hubspot/
Docs:   pm-workspace-docs/agents-docs/web/components/integrations/hubspot/AGENTS.md
```

## Anti-Patterns

🚩 **Code-first documentation** - Always lead with user problem
🚩 **Generic personas** - Use specific names from personas.md
🚩 **Happy path only** - Document failure and recovery
🚩 **Missing trust factors** - AI features especially need trust context
🚩 **Stale documentation** - Update when features change
