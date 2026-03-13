---
name: planning
description: Creates implementation-ready plans through discovery interviews, external research, and codebase analysis. Covers requirements, competitor research, architecture decisions, and change sequencing. Use when planning features, roadmaps, specs, or any work that needs discovery before coding
---

# Feature Planning

Create concrete, implementation-ready plans for features and complex changes.

DO NOT write code during planning. Only explore, research, analyze, and document. Be thorough.

## Reference Files

| File | Read When |
|------|-----------|
| `references/discovery-interview.md` | Starting the discovery phase or need guidance on what questions to ask |
| `references/research-strategy.md` | Planning external research or launching sub-agents for competitor/pattern research |
| `references/plan-templates.md` | Constructing the plan or reviewing plan quality — contains worked examples |

## Scope Check

Before deep planning, gauge the scope:

- **Full planning**: changes span 3+ files, cross system boundaries, have unclear requirements, or involve architectural tradeoffs
- **Light planning**: single-file changes with clear requirements — provide a brief execution outline instead of a full spec

For light planning, skip directly to a short outline: what file, what change, why.

## Workflow

### Phase 1: Discovery Interview

Conduct a thorough interview to surface requirements, constraints, and context the user may not have considered yet.

**How to interview:**

- Present questions with selectable options — don't ask open-ended questions when you can offer concrete choices
- **Batch related questions together.** Ask up to 4 independent questions at once, each displayed as its own tab with its own set of options. This reduces back-and-forth and respects the user's time
  - Each question should have a short label (the tab title) and 2-4 options with descriptions explaining tradeoffs
  - Allow multiple selections when choices aren't mutually exclusive
- **When to batch**: Group questions that are related but independent — answering one doesn't change the others. Example: "Auth method" + "Session storage" + "Token format" can be asked together
- **When to ask separately**: Ask one at a time when the answer to one question changes what you'd ask next
- Always include your recommendation as the first option (mark it as recommended)
- Skip questions the user has already answered
- Continue until there are no more meaningful questions or the user says they're done

**What makes a good question:**

- It surfaces a genuine ambiguity or tradeoff the user needs to decide
- It cannot be answered by reading the codebase or applying common sense
- It covers territory the user may not have considered

**What makes a bad question:**

- You could answer it yourself by reading `package.json`, the codebase, or the project's AGENTS/CLAUDE.md
- It asks for information the user already provided
- It's generic enough to apply to any project ("What framework are you using?")

If you can determine something from context, state your assumption and move on.
Don't ask — inform.

**Question domains** (not exhaustive — use judgment):

- Problem definition and success criteria
- User-facing behavior and interaction design
- Edge cases, error states, and failure modes
- Performance, scale, and data implications
- Accessibility and internationalization concerns
- Security and privacy considerations
- Tradeoffs between approaches (with your recommendation)
- Migration and backwards-compatibility concerns
- Whether the plan will be executed via an autonomous loop (determines output format)

Read `references/discovery-interview.md` for detailed question categories and examples of strong vs weak questions.

### Phase 2: Research

Go beyond the codebase. Not every plan needs this — skip when the feature is purely internal, the approach is well-established, or the user has provided sufficient context.

**When to research:**

- The feature involves user-facing patterns where conventions matter (forms, navigation, onboarding, dashboards, etc.)
- There are multiple viable technical approaches and the tradeoffs aren't obvious
- The user is building something they haven't built before
- Competitor or industry patterns would inform better decisions

**What to research:**

- **Competitors and similar products** — how do others solve this? What UX patterns are established?
- **Technical approaches** — what libraries, APIs, or architectural patterns apply? What are the tradeoffs?
- **Design patterns** — for UI features, what interaction patterns are standard? What accessibility requirements apply?

**How to research:**

- Launch sub-agents in parallel with focused research questions
- Each sub-agent gets one specific question, not a broad mandate
- Synthesize findings into actionable insights, not raw dumps

Read `references/research-strategy.md` for guidance on structuring research queries and synthesizing findings.

### Phase 3: Codebase Analysis

Explore the codebase systematically. Use sub-agents for parallel exploration when the codebase is large or the feature touches multiple systems.

**What to map:**

- **Relevant files** — document paths (not line numbers — code shifts in multi-agent environments)
- **Existing patterns** — architecture, naming conventions, data flow, component structure
- **Dependencies** — what systems, files, or modules will be affected by this change
- **Similar implementations** — existing features that solve analogous problems, to maintain consistency
- **Constraints** — technical limitations, conventions from AGENTS.md or CLAUDE.md, framework constraints
- **Operational context** — git history, decision logs, known issues, and "except when" rules — tribal knowledge that doesn't live in code but affects how changes should be made

**Document findings as:**

- **File**: `path/to/file.ext` — what it does, how it's relevant
- **Pattern**: existing approach used for similar features
- **Constraint**: technical limitation, convention, or requirement

### Phase 4: Plan Construction

Synthesize discovery, research, and analysis into an implementation-ready plan.

**Describe outcomes, not mechanical steps.** "Make the auth middleware reject expired tokens and return 401" beats "Add an if-statement checking token.exp against Date.now()." Specify what the change should achieve — let the implementer choose the approach.

**For each change, specify:**

- File path (not line numbers)
- What function, component, class, or section to modify
- What to achieve and how — be specific about the outcome
- Why this change serves the goal
- Dependencies — what must happen first
- Verification — how to confirm this specific change works (specific, observable behavior)

**Structuring the plan:**

- **Flat list** (default): Use for plans with ~4 or fewer changes concentrated in one area
- **Phased grouping**: Use when the plan has 5+ changes or spans multiple systems (data model, API, UI, etc.)
  - Each phase groups related changes that can be implemented and verified together
  - Phases are ordered by dependency — later phases build on earlier ones
  - Each phase should be safely re-runnable — if interrupted, the implementer can restart the current phase without corrupting previous work
  - Each phase ends with a brief validation checkpoint

**Plan output format (flat list):**

```markdown
## Goal
[One sentence: what we're building and why]

## Research Insights
[Key findings from external research that informed the plan]
[Skip this section if no external research was done]

## Changes

### 1. [Description]
- **File**: `path/to/file.ext`
- **Target**: `functionName()` / `ComponentName` / relevant section
- **Action**: What specifically to add, modify, or remove
- **Reasoning**: Why this change is needed
- **Depends on**: What must happen first, or "Nothing"
- **Verify**: How to confirm this change works — specific, observable behavior

### 2. [Description]
...

## Edge Cases & Risks
- [Specific scenario and how the plan addresses it]
- [Risk and mitigation strategy]

## Validation
- [ ] Specific, testable acceptance criterion
- [ ] Another criterion
- [ ] Edge case X is handled
```

**Plan output format (phased grouping):**

```markdown
## Goal
[One sentence: what we're building and why]

## Research Insights
[Key findings from external research that informed the plan]
[Skip this section if no external research was done]

## Phase 1: [Phase Name, e.g. "Data Model"]

### 1. [Description]
- **File**: `path/to/file.ext`
- **Target**: `functionName()` / `ComponentName` / relevant section
- **Action**: What specifically to add, modify, or remove
- **Reasoning**: Why this change is needed
- **Depends on**: What must happen first, or "Nothing"
- **Verify**: How to confirm this change works — specific, observable behavior

### 2. [Description]
...

**Checkpoint**: [How to verify this phase works before moving on]

## Phase 2: [Phase Name, e.g. "API Layer"]

### 3. [Description]
...

**Checkpoint**: [How to verify this phase works before moving on]

## Phase 3: [Phase Name, e.g. "UI"]

### 4. [Description]
...

**Checkpoint**: [How to verify this phase works before moving on]

## Edge Cases & Risks
- [Specific scenario and how the plan addresses it]
- [Risk and mitigation strategy]

## Validation
- [ ] Specific, testable acceptance criterion
- [ ] Another criterion
- [ ] Edge case X is handled
```

For complex features, include test descriptions in the Validation section: what test file, what test case name, and what it asserts.

**For multi-session features**, optionally add these sections to the plan:

- **Progress**: Checklist of phases/changes, marked as they're completed
- **Decision Log**: Implementation-time decisions that deviated from the original plan, with reasoning
- **Open Questions**: Anything discovered during implementation that needs revisiting

Keep the plan file updated as implementation proceeds — it becomes the source of truth.

#### Phase 4b: Loop-Ready Output (Optional)

If the user confirmed the plan will be executed via a loop (always ask about loop execution in Phase 1 — phrase it as an option: "Will you implement this via an autonomous loop?"):

1. Write a second file: `IMPLEMENTATION_PLAN.md` in the project root
2. Convert each change in the plan to a flat task:
   - `- [ ] [Description] — [file path] — [brief approach]`
3. Preserve phase ordering if the plan uses phased grouping
4. Each task must be completable in one loop iteration — split large changes if needed
5. Add a Goal section from the plan
6. Add empty Decision Log and Issues Found sections
7. Add a reference to the full plan: "See `docs/plans/<feature>.md` for full context"
8. Note: the loop script detects completion by checking for `ALL_TASKS_COMPLETE` at the start of the file. Include a comment at the top of the generated plan: `<!-- When all tasks are done, the loop agent prepends ALL_TASKS_COMPLETE above this line -->`

The rich plan stays as documentation.
The `IMPLEMENTATION_PLAN.md` is the executable task list for the loop.

**Agent capabilities**: Do not assume art or asset tasks are human-only. Agents may have skills for sprite creation, image generation, or other asset work. Plan these as normal tasks — the implementing agent will check its available skills and attempt them. Only mark a task as requiring human input when it genuinely cannot be automated (e.g., subjective creative direction, licensing decisions).

**Writing good Verify fields**: Use type-appropriate checks so the implementing agent knows what to confirm beyond "does it build?" Common patterns:

- **Asset tasks** (images, icons, sprites): Verify quality standards (correct dimensions, transparency, format), remove placeholder/generated code, confirm keys/paths match config/data files
- **Logic/data tasks**: Verify content is logically consistent (e.g., labels make sense, relationships are valid, new entries have all required references), events/hooks are emitted and cleaned up
- **UI tasks**: Verify layering/z-index doesn't obscure existing UI, visual effects are noticeable (not too subtle), cleanup on unmount/teardown

Tasks that produce temporary placeholders should be marked `Done (placeholder)` with a follow-up task created immediately.

#### Persist the Plan

Write the completed plan to a markdown file so it survives beyond this session.

- If the platform provides a designated plan location, use it
- Otherwise, write to the project directory (e.g., `docs/plans/<feature-name>.md`)
- The plan must be a standalone document — readable and actionable in a future session without conversation history

### Phase 5: Spec Stress-Test

After constructing the plan, stress-test it with fresh perspectives. This catches blind spots, underspecified areas, and risks that confirmation bias hides.

**Process (3 rounds):**

For each round, spawn a Task subagent (subagent_type: "general-purpose") with:
- ONLY the plan text (the subagent has no conversation history — this is the point)
- The prompt: "You are reviewing a feature implementation plan. Find 5-10 points that are underspecified, ambiguous, risky, or missing. Be specific — reference the exact section and explain what's unclear or could go wrong. Don't suggest rewrites — just identify the gaps."

After each round:
1. Present the subagent's findings to the user
2. Ask which findings to address (some may be intentional simplifications)
3. Incorporate accepted feedback into the plan before the next round

**When to skip:**
- Light planning (single-file, clear scope)
- User explicitly says to skip refinement
- A subagent review turns up no issues

**Key constraint:** Each subagent must receive ONLY the plan document, not the conversation history. The value comes from fresh eyes with zero context about the decisions that led to the plan.

### Phase 6: Plan Review

Before delivering the plan, verify:

- [ ] Someone could implement this without asking further questions
- [ ] Plan is self-contained — all context needed for implementation is in the plan, not just in conversation history
- [ ] Plan respects project conventions (from CLAUDE.md, AGENTS.md, or equivalent project config)
- [ ] File paths reference existing files or are plausible and consistent with the codebase structure
- [ ] Steps are ordered with clear dependency chains
- [ ] Acceptance criteria are specific and testable
- [ ] Every decision includes reasoning (the "why")
- [ ] No vague language — "update", "improve", "fix" always paired with specifics
- [ ] Research insights are incorporated where relevant
- [ ] Edge cases and risks are addressed

## Anti-Patterns

| Avoid | Do Instead |
|-------|------------|
| "Update the authentication system" | "Modify `auth/middleware.ts` — add `validateSession()` that checks token expiry" |
| "Add error handling" | "Wrap the API call in `auth/api.ts` with try/catch, show toast on error" |
| "Use the standard pattern" | "Follow the existing pattern from `user/dao.ts` (class-based with explicit types)" |
| "Make sure it works" | "Verify: (1) form submits on Enter, (2) inline errors display, (3) submit disabled during request" |
| Asking "What framework do you use?" | Read `package.json` and state: "I see you're using Next.js with App Router" |
| Specifying line numbers | Reference file path + function/component name |
| Skipping research for novel features | Launch sub-agents to research competitor patterns and technical approaches |
| Asking one question then moving on | Continue the interview until all meaningful questions are covered |
