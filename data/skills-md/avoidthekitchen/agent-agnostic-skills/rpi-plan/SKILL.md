---
name: rpi-plan
description: Create detailed, implementation-ready technical plans through an interactive and skeptical process grounded in codebase research. Use this whenever the user asks to plan, scope, design, spec, or phase implementation work (including "make a plan", "how should we build this", "break this into phases", and "write a technical spec"), even if they do not explicitly ask for a "plan."
---

# RPI Plan

Use this skill to turn requirements into a concrete implementation plan with clear phases, file-level changes, and verification criteria.

## Initial Response

When this skill is invoked, respond with:

```text
I'll help you create a detailed implementation plan. Let me start by understanding what we're building.

Please provide:
1. The task description or requirements
2. Any relevant context, constraints, or specific requirements
3. Links to related research or previous implementations

I'll analyze this information and work with you to create a comprehensive plan.
```

Then wait for the user's input.

## Workflow

### Step 1: Context Gathering and Initial Analysis

1. Read all user-mentioned files fully before planning.
2. Research the current codebase state:
- Locate related files and entry points.
- Understand existing implementation details and constraints.
- Find nearby patterns/features to mirror.
3. Present your understanding and ask focused questions only where human judgment is required.

### Step 2: Research and Discovery

1. Create a task list to track exploration and prevent blind spots.
2. Run parallel research tracks when available; otherwise execute tracks sequentially.
3. Wait for all research tracks to finish before drawing conclusions.
4. Present design options with tradeoffs and recommend one approach.

### Step 3: Plan Structure Alignment

After alignment on direction, propose phasing before full detail:

```markdown
Here's my proposed plan structure:

## Overview
[1-2 sentence summary]

## Implementation Phases:
1. [Phase name] - [what it accomplishes]
2. [Phase name] - [what it accomplishes]
3. [Phase name] - [what it accomplishes]

Does this phasing make sense?
```

### Step 4: Detailed Plan Authoring

Write the plan to `rpi/plans/TIMESTAMP_plan_descriptive_name.md`.

- Use a Windows-safe timestamp for `TIMESTAMP`: `YYYY-MM-DD-HH-MM` (for example `2026-03-05-22-10`).
- Use a short snake_case suffix for `descriptive_name`.
- For every planned implementation change, add an explicit unchecked task item using `- [ ]`.
- Do not leave changes as prose-only summaries; each actionable change must be trackable as a checkbox.

Use this structure:

```markdown
# [Feature/Task Name] Implementation Plan

## Overview
[Brief description of what we're implementing and why]

## Current State Analysis
[What exists now, what's missing, key constraints discovered]

## Desired End State
[Specific target behavior and how to verify it]

## What We're NOT Doing
[Explicit out-of-scope items]

## Implementation Approach
[High-level strategy and rationale]

## Phase 1: [Descriptive Name]

### Overview
[What this phase accomplishes]

### Changes Required
#### 1. [Component/File Group]
**File**: `path/to/file.ext`
**Changes**:
- [ ] [Concrete change 1]
- [ ] [Concrete change 2]

    ```[language]
    // Specific code to add or modify
    ```

### Success Criteria
#### Automated Verification
- [ ] Tests pass: `npm test`
- [ ] Type checks pass: `npm run typecheck`
- [ ] Lint passes: `npm run lint`

#### Manual Verification
- [ ] Feature works as expected
- [ ] No regressions in related flows
- [ ] Performance remains acceptable

---

## Phase 2: [Descriptive Name]
[Repeat the same structure]

## Testing Strategy
### Unit Tests
- [What to test]
- [Key edge cases]

### Integration Tests
- [Critical end-to-end scenarios]

### Manual Testing Steps
1. [Specific step]
2. [Specific step]

## Performance Considerations
[Perf implications and mitigations]

## Migration Notes
[Data/system migration details if applicable]
```

### Step 5: Review and Iterate

1. Save the plan and share the path with the user.
2. Refine based on feedback.
3. Continue until the plan is implementation-ready.

## Quality Bar

- Be skeptical of vague requirements and identify ambiguities early.
- Keep the process interactive; get explicit buy-in at major checkpoints.
- Include concrete file paths and measurable success criteria.
- Prefer incremental, testable phases over big-bang changes.
- Resolve open questions before finalizing a plan.
