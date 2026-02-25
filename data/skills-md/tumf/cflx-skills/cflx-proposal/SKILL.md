---
name: cflx-proposal
description: Create structured Conflux change proposals through interactive conversation with users. Use when users request "create a proposal", "draft a change", "propose a feature", or similar proposal creation tasks. This skill asks clarifying questions and guides users through the proposal process.
---

# Conflux Proposal Creator

Create structured change proposals for Conflux (OpenSpec-based) projects through interactive conversation with users.

## Scope Restrictions (Proposal-Only)

- This skill is for proposal creation only. Do NOT implement or modify product/source code.
- You may READ any files for context gathering.
- You may WRITE only under `openspec/changes/<change-id>/`.
- After strict validation passes, stop and present the proposal for review.

## Guardrails (Match Command Behavior)

- Favor straightforward, minimal implementations first and add complexity only when it is requested or clearly required.
- Keep changes tightly scoped to the requested outcome.
- Default to proposal splitting: when requirements can be decomposed into independent scopes, create separate change proposals.
- If uncertain whether to split, prefer splitting unless the scopes are tightly coupled and must ship together to preserve correctness.
- For each split proposal, use a distinct verb-led `change-id` and keep `proposal.md`, `tasks.md`, and `design.md` (when needed) scoped to that proposal only.
- When multiple proposals are created, explicitly document dependency/sequence relationships and parallelizability in the final user-facing summary.

## When to Use This Skill

Trigger this skill when users request:
- "Create a proposal for..."
- "Draft a change proposal"
- "Propose a new feature"
- "Document this change as a proposal"
- Any request to create structured change documentation

## Key Characteristics

**Human-Interactive Mode**:
- Ask clarifying questions to understand requirements
- Guide users through proposal structure
- Discuss design decisions and trade-offs
- Iterate on requirements based on feedback
- Present proposals for user review and approval

**Not for Orchestration**: This skill is designed for direct human interaction, not automated orchestration.

## Proposal Structure

A Conflux proposal consists of:

```
openspec/changes/<change-id>/
├── proposal.md          # Change description and context
├── tasks.md             # Implementation task checklist
├── design.md            # Architecture and design (optional)
└── specs/               # Spec deltas
    └── <capability>/
        └── spec.md      # Requirement specifications
```

## Interactive Workflow

### 1. Understand the Change

**Ask questions to clarify**:
- What problem does this solve?
- What are the acceptance criteria?
- Are there any constraints or dependencies?
- What is the scope (minimal vs. comprehensive)?

**Research existing code**:
```bash
# Review existing specs
 python3 "$SKILL_ROOT/scripts/cflx.py" list --specs

# Check related code
rg "<keyword>"
ls <relevant-directory>
```

**Strict validation note (common gotcha)**:
- In strict mode, include at least one spec delta under `openspec/changes/<id>/specs/<capability>/spec.md`.
- For bugfix-only proposals (no intended new behavior), add a minimal `## MODIFIED Requirements` delta with at least one `### Requirement:` and one `#### Scenario:`.

### 2. Evaluate Split Boundaries (Default: Split)

Before writing anything, evaluate whether the request should be split into multiple independent change proposals.

**Default rule**: if scopes are independent or weakly coupled, split into separate `openspec/changes/<change-id>/` proposals.

**Keep as a single proposal only when**:
- The scopes are tightly coupled and must ship atomically to preserve correctness.
- The acceptance criteria cannot be verified independently.

When keeping a single proposal despite multiple scopes, explicitly record the rationale in `proposal.md` or `design.md`.

### 3. Generate Change ID

**Rules**:
- Verb-led (e.g., `add-auth`, `fix-validation`, `refactor-api`)
- Kebab-case (lowercase with hyphens)
- Must NOT include date prefixes or suffixes (forbidden: `2026-02-07-add-auth`, `add-auth-2026-02-07`)
- Concise but descriptive
- Unique within the project

**Present to user**: "I suggest using the change ID `<id>`. Does this work for you?"

### 4. Draft Proposal Content

Create `openspec/changes/<id>/proposal.md`:

**Required sections**:
- Title (H1)
- Problem/Context
- Proposed Solution
- Acceptance Criteria
- Out of Scope (if applicable)

**Ask for feedback**: "Here's the draft proposal. Would you like to adjust anything?"

### 5. Create Task Breakdown

Create `openspec/changes/<id>/tasks.md`:

**Task format**:
```markdown
## Implementation Tasks

- [ ] Task 1: Description (verification: how to verify completion)
- [ ] Task 2: Description (verification: ...)

## Future Work

- Items that require human action
- Items requiring external systems
- Long-wait verification tasks
```

**Guidelines**:
- Break into small, verifiable steps
- Include verification methods
- Specify integration/wiring tasks
- Mark non-AI-executable tasks for Future Work

**External dependency policy (mock-first / verification-first)**:
- If a requirement cannot be verified locally without credentials or external systems, design mock/stub/fixture-based verification.
- Do not change production/runtime behavior to "use mocks"; mocks/stubs/fixtures are for tests and local verification.
- Only truly non-mockable dependencies (human decisions, real external systems, long-wait checks) go to Out of Scope / Future Work.

**Present to user**: "I've broken this down into X tasks. Do these cover everything?"

### 6. Design Documentation (Optional)

Create `openspec/changes/<id>/design.md` when:
- Change spans multiple systems
- Architectural decisions need documentation
- Trade-offs require explanation
- Complex implementation patterns

**Ask**: "Should we document the design decisions in detail?"

### 7. Write Spec Deltas

Create `openspec/changes/<id>/specs/<capability>/spec.md`:

**Format**:
```markdown
## ADDED Requirements

### Requirement: <requirement-name>

<Description>

#### Scenario: <scenario-name>

**Given**: <preconditions>
**When**: <action>
**Then**: <expected-outcome>

## MODIFIED Requirements

### Requirement: <existing-requirement-name>

<Updated description>

#### Scenario: <scenario-name>

...

## REMOVED Requirements

### Requirement: <deprecated-requirement-name>

<Reason for removal>
```

**Critical rules**:
- Each requirement must have at least one scenario
- Use ADDED/MODIFIED/REMOVED sections
- Be specific and testable

**Discuss with user**: "Should we add these requirements to the spec?"

### 8. Validate Proposal

Run validation:
```bash
 python3 "$SKILL_ROOT/scripts/cflx.py" validate <id> --strict
```

**If validation fails**:
- Show errors to user
- Discuss fixes
- Apply corrections
- Re-validate

**Present results**: "Validation passed! The proposal is ready for review."

### 9. Final Review

Present complete proposal to user:
- Show directory structure
- Summarize key points
- Highlight task count
- Confirm readiness

When the proposal was split into multiple independent change proposals, always present a proposal index:

```
- change-id
  - one-line objective
  - dependency/sequence (if any)
  - whether it can be implemented in parallel
```

**Ask**: "The proposal is complete. Would you like to proceed with implementation, or make any final adjustments?"

## Mock-First External Dependencies

When designing tasks, follow mock-first approach:

**Prefer**:
- Mock/stub/fixture implementations
- Test doubles for external APIs
- Local verification without credentials

**Avoid**:
- Blocking on missing API keys
- Requiring real external services
- Deferring mockable dependencies

**Discuss with user**: "For the external API integration, should we use mocks for testing, or do you have test credentials available?"

## Task Classification

**AI-Executable Tasks** (include with checkbox):
- Code implementation
- Unit/integration tests
- Documentation updates
- Linting/formatting
- Local verification

**Future Work Tasks** (no checkbox):
- Manual approval required
- Human decision-making
- External system deployment
- Long-wait verification (>1 day)

**Ask user**: "Are there any tasks that require manual review or external approvals?"

## Question Examples

### Understanding Requirements
- "What's the primary user need this addresses?"
- "Are there any security or performance requirements?"
- "What's the expected timeline for this change?"

### Clarifying Scope
- "Should this include error handling for edge cases?"
- "Do we need backward compatibility?"
- "Are there related features we should consider?"

### Design Decisions
- "Would you prefer approach A (simpler) or B (more flexible)?"
- "Should we optimize for performance or maintainability?"
- "Where should this integrate with the existing system?"

### Verification
- "How should we verify this is working correctly?"
- "What would constitute a successful implementation?"
- "Are there specific test scenarios we should cover?"

## Built-in Tools

Use `python3 "$SKILL_ROOT/scripts/cflx.py"` for all Conflux operations:

```bash
# List existing changes
python3 "$SKILL_ROOT/scripts/cflx.py" list

# List specs
python3 "$SKILL_ROOT/scripts/cflx.py" list --specs

# Show change details
python3 "$SKILL_ROOT/scripts/cflx.py" show <id>

# Validate proposal
python3 "$SKILL_ROOT/scripts/cflx.py" validate <id> --strict
```

## Best Practices

### Communication
- Ask one question at a time (avoid overwhelming)
- Summarize understanding before proceeding
- Present options with recommendations
- Confirm major decisions

### Proposal Quality
- Keep scope focused and minimal
- Break large changes into multiple proposals
- Include clear acceptance criteria
- Specify verification for each task

### User Experience
- Be responsive to feedback
- Iterate on content based on input
- Present information clearly
- Provide helpful suggestions

## Common Patterns

### Feature Addition
1. Understand user need
2. Review existing architecture
3. Propose minimal viable solution
4. Break into implementation tasks
5. Add spec requirements

### Bug Fix
1. Understand the bug behavior
2. Identify root cause area
3. Propose fix approach
4. Include regression tests
5. Add MODIFIED spec if behavior changes

### Refactoring
1. Clarify refactoring goals
2. Identify affected components
3. Plan incremental steps
4. Ensure test coverage
5. Document design decisions

## Troubleshooting

### User Unclear About Requirements
- Ask more specific questions
- Provide examples or options
- Start with minimal scope
- Plan for iteration

### Complex Dependencies
- Discuss mock-first approach
- Identify what's truly non-mockable
- Plan integration points
- Document assumptions

### Large Scope
- Suggest breaking into multiple proposals
- Identify core vs. nice-to-have
- Prioritize with user
- Plan phased approach

## Reference Files

No additional reference files.

## Example Interaction

```
User: "I want to add user authentication"

Agent: "I'd like to understand the authentication requirements better:
1. What type of authentication? (JWT, session-based, OAuth?)
2. What user actions need to be protected?
3. Do you have an existing user database or need to create one?"

User: "JWT-based, protect API endpoints, we have a users table"

Agent: "Got it. I suggest the change ID `add-jwt-auth`. I'll create a proposal with:
- JWT token generation and validation
- Middleware for protected routes
- Login/logout endpoints

Does this scope look correct?"

User: "Yes, please proceed"

Agent: [Creates proposal.md, tasks.md, specs/]
"Here's the task breakdown:
1. Implement JWT utility functions
2. Create auth middleware
3. Add login endpoint
4. Add logout endpoint
5. Protect existing API routes
6. Add unit tests
7. Add integration tests

Total: 7 tasks. Does this cover everything?"

User: "Add password reset too"

Agent: "I'll add password reset. This requires email sending - should we:
A) Mock email for testing (recommended)
B) Use a real email service (needs credentials)
?"

User: "Mock for now"

Agent: [Updates proposal]
"Added 2 more tasks for password reset with mocked email.
Running validation... ✓ Validation passed!

The proposal is ready. Would you like to start implementation?"
```
