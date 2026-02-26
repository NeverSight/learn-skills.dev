---
name: workflow-designer
description: Design detailed, implementation-ready engineering workflows as checklists. Use when the user asks for a workflow, process, or step-by-step implementation plan related to coding, refactors, or technical tasks.
---

# Workflow Designer

This skill helps the agent design **clear, detailed, implementation-ready workflows** for engineering tasks, with an emphasis on **code-focused work** (features, refactors, debugging, reviews, etc.).

The primary output is a **checklist-style workflow** that someone could follow end-to-end.

## When to Use This Skill

The agent should apply this skill whenever:

- The user explicitly asks to **“design a workflow”**, “workflow designer”, or similar.
- The user asks for a **step-by-step implementation plan** (e.g. “give me a plan to implement X”).
- The user asks for a **process** around technical work (e.g. “design a deployment process”, “review process”, “incident workflow”).
- The task involves **non-trivial multi-step engineering work** where a structured process will help.

This skill is primarily for:

- **Code-centric workflows**: implementing features, refactors, migrations, debugging, testing.
- **Engineering processes**: deployment, release, code review, incident handling, onboarding technical tasks.

## Output Format

Always produce a **checklist-first workflow**, optimized for someone to execute step by step.

### Required Structure

Follow this structure unless the user specifies another:

```markdown
## Context
- **Goal**: [...]
- **Scope**: [...]
- **Assumptions**: [...]

## High-Level Phases
- **Phase 1**: [...]
- **Phase 2**: [...]
- **Phase 3**: [...]

## Detailed Workflow Checklist
- [ ] **Phase 1: ...**
  - [ ] Step 1: ...
  - [ ] Step 2: ...
- [ ] **Phase 2: ...**
  - [ ] Step 1: ...
  - [ ] Step 2: ...

## Risks and Validation
- **Risks / pitfalls**:
  - ...
- **Validation / completion criteria**:
  - ...
```

### Level of Detail

- Default to **detailed and exhaustive** within reason:
  - Break work into **small, actionable steps** that could be checked off.
  - Make implicit steps explicit when they are easy to forget (e.g. “run tests”, “update docs”).
- Avoid unnecessary prose; prefer **concise, actionable bullets**.

If the scope is huge (e.g. “design complete architecture for a bank”), first:

- Briefly note that the scope is broad.
- Propose a **phased workflow** (e.g. discovery → design → implementation → rollout).
- Optionally ask the user what phase to detail first, but **still provide an initial high-level workflow**.

## Workflow Design Process (How the Agent Should Think)

When invoked, the agent should follow this internal process before writing the final workflow:

1. **Clarify the goal (mentally or briefly in text)**  
   - What is the primary outcome? (e.g. “Feature X shipped to production”, “Refactor Y complete with no regressions”).  
   - Is this mainly about **implementation**, **refactor**, **migration**, **debugging**, **process**, or **other**?

2. **Identify constraints and context**  
   - Check for any constraints mentioned by the user: deadlines, tech stack, environments, approvals, testing requirements.  
   - If constraints are missing but critical, either:
     - Infer sensible defaults, and
     - Optionally call them out in the **Assumptions** section.

3. **Define 3–6 high-level phases**  
   Examples:
   - For a feature: *Discovery → Design → Implementation → Testing → Review → Release*  
   - For a refactor: *Analysis → Design → Incremental changes → Testing → Cleanup & docs*  
   - For a process: *Intake → Triage → Execution → Validation → Closure*

4. **Expand phases into checklists**  
   - For each phase, create 3–10 **concrete steps**.  
   - Prefer verbs at the start: “Analyze…”, “Implement…”, “Write…”, “Run…”, “Verify…”.
   - Include critical cross-cutting steps: testing, observability, documentation, communication.

5. **Add risks and validation**  
   - List key pitfalls (e.g. data loss, downtime, regressions).  
   - Provide explicit **done criteria** and validation checks (tests, monitoring, reviews).

6. **Tailor to the user’s context**  
   - If the user’s stack, tools, or conventions are known from the conversation, reference them (e.g. “update `README.md`”, “add Jest tests”, “update CI pipeline”).

## Patterns and Examples

### Example: Implementing a New Feature

**User request:** “Design a workflow to implement a new user profile page in our web app.”

The agent should respond in this style (shortened here for brevity):

```markdown
## Context
- **Goal**: Implement a new user profile page in the web app and release it safely to production.
- **Scope**: Backend API, frontend UI, tests, and deployment.
- **Assumptions**: Existing auth system; CI/CD pipeline in place.

## High-Level Phases
- **Phase 1**: Clarify requirements and UX
- **Phase 2**: Design API and data model changes
- **Phase 3**: Implement backend + frontend
- **Phase 4**: Testing and QA
- **Phase 5**: Launch and follow-up

## Detailed Workflow Checklist
- [ ] **Phase 1: Clarify requirements and UX**
  - [ ] Capture required fields and interactions for the profile page.
  - [ ] Identify permissions (who can view/edit which fields).
  - [ ] Agree on UX wireframes or rough layout.

- [ ] **Phase 2: Design API and data model changes**
  - [ ] Review existing user model and endpoints.
  - [ ] Design any new fields and validation rules.
  - [ ] Define API contract (request/response shapes).

... (and so on for other phases)

## Risks and Validation
- **Risks / pitfalls**:
  - Inconsistent data between old and new profile fields.
  - Leaking sensitive information on the profile page.
- **Validation / completion criteria**:
  - All acceptance criteria are met and covered by automated tests.
  - No P0 errors in logs after release window.
```

### Example: Refactor Workflow

For refactors, emphasize safety and incremental change:

- Phases like: *Baseline & safety nets → Refactor in small steps → Keep behavior identical → Clean up → Monitor*.
- Checklist items for:
  - Capturing current behavior, adding missing tests.
  - Refactoring in thin slices.
  - Running tests and static analysis after each logical change.

### Example: Debugging Workflow

For debugging requests:

- Phases like: *Reproduce → Narrow scope → Form hypotheses → Test systematically → Fix → Prevent regression*.
- Checklist items for:
  - Capturing failing cases and logs.
  - Binary search / isolation strategies.
  - Adding regression tests once fixed.

## Adapting to User Requests

- If the user specifies a preferred structure (e.g. “only numbered steps”, “no risks section”), **respect their format** while keeping the spirit of this skill (clear, actionable steps).
- If the user wants a **lighter** or **heavier** workflow, adjust detail accordingly but keep the **Context → Phases → Checklist → Validation** pattern unless explicitly told otherwise.

## Summary of Key Behaviors

When this skill is active, the agent should:

- **Think like a senior engineer designing a process**: prioritize safety, clarity, and maintainability.
- **Produce detailed checklists** that someone else can follow without extra context.
- **Call out assumptions, risks, and validation steps** explicitly.
- **Adapt** the workflow to the specific task, stack, and constraints the user mentions.

