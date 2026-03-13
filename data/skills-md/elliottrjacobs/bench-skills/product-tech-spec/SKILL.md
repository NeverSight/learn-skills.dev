---
name: product-tech-spec
description: Write technical specifications bridging product requirements and implementation. Use when the user says "tech spec", "technical spec", "architecture doc", "system design", or after writing a PRD and before planning implementation.
allowed-tools: ["Read", "Glob", "Grep", "Task", "AskUserQuestion", "Write"]
argument-hint: "[topic or prd-path]"
---

# /product-tech-spec — Technical Specification

Write technical specs that bridge product requirements and implementation plans. Covers architecture, APIs, data models, and component hierarchy.

## When to Use

- User says "tech spec", "technical spec", "architecture doc"
- After writing a PRD and before planning implementation
- When architecture decisions need to be documented

## Process

### Step 1: Gather Context

Check for existing artifacts:
1. `docs/prds/` — Read the PRD this spec implements
2. `docs/brainstorms/` — Additional context if available
3. User-provided description or `$ARGUMENTS`

### Step 2: Research (Parallel Agents)

Spawn 2 agents IN PARALLEL using the Task tool:

#### Agent 1 — Codebase Analyst
```
Task(subagent_type: "general-purpose", description: "Analyze codebase for tech spec")
prompt: Analyze this project's architecture to inform a tech spec for [FEATURE].
  Focus on: tech stack and versions, existing data models, API patterns,
  component structure, auth patterns, state management approach.
  Return findings relevant to architectural decisions.
```

#### Agent 2 — Practices Researcher
```
Task(subagent_type: "general-purpose", description: "Research architecture patterns")
prompt: Research architecture best practices for [FEATURE TYPE] given [TECH STACK].
  Focus on: recommended patterns, data model design, API design,
  component architecture, security considerations.
  Return practical architectural guidance.
```

### Step 3: Write Tech Spec

Write to `docs/tech-specs/YYYY-MM-DD-<name>.md` using the template in [references/tech-spec-template.md](references/tech-spec-template.md).

Key sections:
1. **Overview** — What this spec covers and its relationship to the PRD
2. **Architecture** — System design, component hierarchy, data flow
3. **Data Models** — Database tables, types, relationships
4. **API Design** — Endpoints, server actions, or edge functions
5. **Component Hierarchy** — UI structure and state ownership
6. **Security** — Auth, RLS policies, input validation
7. **Migration Plan** — How to get from current state to target state

**Writing rules:**
- Reference specific existing patterns from the codebase analysis
- Make decisions, don't list options (that's what the brainstorm was for)
- Include concrete examples (schema SQL, TypeScript types, component trees)
- Call out risks and unknowns

### Step 4: Review with User

Present key architectural decisions and use AskUserQuestion to confirm approach before finalizing.

## Output

Save to: `docs/tech-specs/YYYY-MM-DD-<name>.md`

## Next Steps

- Ready to plan tasks? → `/engineer-plan`
- Need to start building? → `/engineer-work`
