---
name: product-prd
description: Write product requirements documents from feature ideas or brainstorm output. Use when the user says "write a PRD", "product requirements", "feature spec", or needs to formalize a product concept into a structured document.
allowed-tools: ["Read", "Glob", "Grep", "AskUserQuestion", "Write"]
argument-hint: "[topic or brainstorm-path]"
---

# /product-prd — Product Requirements Document

Write structured PRDs that define what to build and why. PRDs are product-focused — they describe the problem, users, and requirements without prescribing technical implementation.

## When to Use

- User says "write a PRD", "product requirements", "feature spec"
- After a brainstorm session, to formalize requirements
- When a feature idea needs to be documented before building

## Process

### Step 1: Gather Context

Check for existing artifacts:
1. `docs/brainstorms/` — Use brainstorm output as starting point
2. User-provided description or `$ARGUMENTS`
3. If neither exists, ask clarifying questions

### Step 2: Clarify Requirements

Ask focused questions about gaps in the input:
- **Scope**: What's in v1 vs. later? What's explicitly out of scope?
- **Users**: Who are the primary and secondary users?
- **Success**: How will you measure if this works?
- **Priority**: Which requirements are must-have vs. nice-to-have?

Use AskUserQuestion — don't assume. Better to ask than to guess wrong.

### Step 3: Write PRD

Write to `docs/prds/YYYY-MM-DD-<name>.md` using the template in [references/prd-template.md](references/prd-template.md).

Key sections:
1. **Problem Statement** — What problem exists and why it matters
2. **Target Users** — Specific user personas, not "all users"
3. **User Stories** — "As a [user], I want to [action] so that [benefit]"
4. **Requirements** — Categorized as Must/Should/Could (MoSCoW)
5. **Success Metrics** — Measurable outcomes
6. **Out of Scope** — Explicit boundaries

### Step 4: Review with User

Present the PRD and use AskUserQuestion to confirm:
- Are the requirements complete?
- Is the priority (Must/Should/Could) correct?
- Anything missing or misunderstood?

## Output

Save to: `docs/prds/YYYY-MM-DD-<name>.md`

## Next Steps

- Ready for technical design? → `/product-tech-spec`
- Need to plan implementation? → `/engineer-plan`
