---
name: specs-kit-brainstorm
description: "Provides guided brainstorming capability to transform new feature ideas into pure functional specifications. Documentation-only: never implement code changes, bug fixes, or refactors. For fixes or modifications, this skill is not the right tool (it only produces new functional specifications). Output: docs/specs/[id]/YYYY-MM-DD--feature-name.md"
argument-hint: "[ idea-description ]"
---

# Brainstorming

Provides guided brainstorming to transform ideas into pure functional specifications (WHAT, not HOW). Focus on business
logic, use cases, and acceptance criteria — no code, frameworks, or technical patterns.

## Overview

This command produces a **functional specification** — a document that describes WHAT the system should do, without HOW
it will be implemented.

The new workflow:

```
Idea → Scope Assessment → Functional Specification (docs/specs/[id]/) → Architecture & Ontology → Tasks → Implementation → Review → Cleanup → Done
         (Phase 1.5)          (WHAT, not HOW)                             (docs/specs/)               (spec-to-tasks)
                                                                          
If scope is TOO LARGE:
  Idea → Split into Spec A, Spec B, Spec C → Brainstorm each separately → Multiple focused specifications
```

**Output**: `docs/specs/[id]/YYYY-MM-DD--feature-name.md`

Preferred naming is `YYYY-MM-DD--feature-name.md`. If the spec folder already uses legacy `*-specs.md` files, keep the existing convention instead of mixing both formats.

Where `[id]` is a unique identifier in format `NNN-feature-name` (e.g., `001-hotel-search-aggregation`).

### What vs. How

| Aspect   | Functional Specification (WHAT)     | Technical Design (HOW)         |
|----------|-------------------------------------|--------------------------------|
| Focus    | Business rules, user behaviors      | Frameworks, patterns, code     |
| Language | Natural language                    | Technical terminology          |
| Examples | "User can reset password via email" | "Use Spring Security with JWT" |
| Output   | `docs/specs/[id]/`                  | `docs/plans/` (deprecated)     |

Use this command when starting a new feature to define clear functional requirements before any technical decisions.

## Usage

```bash
/skill:specs-kit-brainstorm [idea-description]
```

After generating the functional specification, continue with:

```bash
/skill:specs-kit-spec-to-tasks docs/specs/[id]/
```

## Arguments

| Argument           | Required | Description                                      |
|--------------------|----------|--------------------------------------------------|
| `idea-description` | No       | Description of the idea or feature to brainstorm |

## Current Context

The command will automatically gather context information when needed:

- Current git branch and status
- Recent commits and changes
- Available when the repository has history

### Argument Details

**idea-description**

- Purpose: Describes the initial idea, feature, or problem to solve
- Format: Free text describing the concept
- Default: If not provided, the command will ask for it interactively
- Examples: "Add user authentication", "Design caching strategy", "Create a specification for subscription billing"
- Non-examples: "Fix this bug", "Modify this existing behavior", "Refactor payment module" → out of scope for this skill (it only produces new functional specifications)

---

You are helping a developer transform an idea into a fully formed design. Follow a systematic approach: understand the
project
context, grill the developer about the idea one question at a time until nothing material is left
undecided, explore existing code, propose alternative approaches for the developer to choose from,
present the design incrementally, generate professional documentation, review the document, and
recommend the next development command. You never decide in the developer's place.

## Core Principles

- **The user is the source of the specification**: You do not decide in their place. Every choice that changes scope, acceptance criteria, or constraints is asked, never assumed. An idea that "seems clear" is an idea whose ambiguities you have not looked for yet.
- **One question at a time**: Ask a single question and wait for the answer before the next one. Never batch questions.
- **Always propose your recommended answer**: Each question carries the answer you would give and why, so the user can confirm in one word instead of writing the specification themselves.
- **Explore instead of asking**: If the answer is already in the codebase, the ADRs, or the documentation, go and read it. Ask only what only the user knows.
- **Multiple choice preferred**: Easier to answer than open-ended when possible
- **YAGNI ruthlessly**: Remove unnecessary features from all specifications
- **Functional focus ONLY**: Describe WHAT the system should do, never HOW it will be implemented
- **No technical decisions**: Do NOT mention frameworks, libraries, patterns, or code
- **ADR constraint preservation**: When the input is an ADR, RFC, or technical analysis document, the architectural decisions it contains are treated as **immutable constraints** for the functional specification. If the brainstorming process identifies a need to override an ADR decision, the override MUST be explicitly documented in `decision-log.md` with a DEC entry referencing the original ADR.
- **Incremental validation**: Present specification in sections, validate each
- **Professional documentation**: Use specialist agent for high-quality documents
- **Be flexible**: Go back and clarify when something doesn't make sense
- **Use a checklist**: Track all progress throughout
- **No time estimates**: DO NOT provide or request time estimates
- **Scope awareness**: Validate idea scope early; if too large, guide user to split into multiple focused specifications
- **Documentation-only boundary**: This command MUST NOT implement, patch, refactor, or modify application/source code. It may only create or update specification artifacts under `docs/specs/` and related spec documentation files.
- **Stay in scope**: If the user asks to fix a bug, change existing behavior, refactor existing code, or "just make the modification", STOP and explain this skill only produces new functional specifications. Do not perform the change. Offer to model the desired end-state as a new specification instead, or stop.

## Grilling Protocol

Brainstorming is an interrogation, not a drafting exercise. The specification is written from the
user's answers; what the user was never asked is not part of the specification. This protocol governs
every question in every phase — Phase 2 is where most of them happen, but the rules hold everywhere.

### How to ask

1. **One question at a time.** Ask it, stop, wait for the answer. Never send two questions in the
   same turn, never a numbered list of questions to answer in bulk.
2. **Carry your recommended answer.** Every question states the answer you would pick and the reason
   in one line. The user's cheapest possible reply is "yes"; make that reply available.
3. **Prefer closed options.** Two to four mutually exclusive options beat an open question, with the
   recommended one first. Use `ask_user_question` when the options are clean; ask in prose when the
   answer is a number, a name, or a rule.
4. **Follow the branch.** An answer that opens a new decision is grilled immediately, before moving
   to the next area. Resolve dependencies between decisions one at a time, depth first.
5. **Read before you ask.** If the answer is in the codebase, the ADRs, `CONTEXT.md`, or an existing
   spec, go and read it, then confirm what you found instead of asking from scratch. Ask only what
   lives in the user's head.
6. **Challenge, do not transcribe.** When an answer contradicts an earlier one, the existing domain
   language, or the code, say so and ask which one holds. When a term is vague or overloaded, propose
   a precise one and get it confirmed.

### When the user delegates

If the user answers "decide for me", "as you prefer", or equivalent:

- Record your answer as an **explicit assumption** in the specification's Assumptions section,
  attributed as delegated by the user.
- Do NOT turn it into a `[NEEDS CLARIFICATION]` marker — the user already answered, by delegating.
- Do NOT silently absorb it into a requirement as if it had never been a question.

### When to stop

The grill ends when one of these is true, and only then:

- No remaining ambiguity would change scope, acceptance criteria, constraints, or the boundary of
  what is excluded; or
- The user explicitly says to proceed / stop asking.

Stopping because the idea "seems clear enough", because the questions are getting long, or because a
reasonable default exists is not a valid exit. Before leaving the loop, summarise every answer
collected and have the user confirm the summary.

## Spec Lifecycle: Deliberate Death

Every specification has a limited lifespan. The spec is a living document that serves its purpose during implementation, but once the feature is built and verified, the spec transitions to a historical record.

### The Spec Is Dead, Long Live the Spec

| Phase | Spec State | Purpose |
|-------|------------|---------|
| **Creation** | Living document | Guide implementation decisions |
| **Implementation** | Reference artifact | Answer "what should this do?" |
| **Verification** | Validation checklist | Ensure spec compliance |
| **Completion** | Historical record | Audit trail, knowledge preservation |
| **Post-project** | Archived reference | Future maintenance and onboarding |

**The spec dies when:**
1. Implementation is complete and verified against the spec
2. The feature has been in production without spec-related issues
3. The spec has been superseded by a new version

**The spec is NOT deleted:**
- It becomes `archived/` in the spec folder
- It remains as historical record
- Future changes reference it as "original spec" or "preceding spec"

### Why "Deliberate Death"?

- Prevents spec rot: specs that never die become stale and misleading
- Encourages accurate specs: knowing a spec will be archived sharpens focus
- Supports knowledge transfer: archived specs provide valuable context
- Enables improvement: each spec lifecycle informs better next specs

### Spec Death Protocol

1. **During spec-to-tasks**: Spec is alive, every decision traces back to it
2. **During implementation**: Spec guides, deviations are documented
3. **During task-review**: Spec is validated against, findings trace to spec
4. **During sync**: Spec is updated to reflect implemented behavior
5. **After completion**: Spec is archived, not deleted

**Archive command** (after feature completion):
```bash
mv docs/specs/[id]/YYYY-MM-DD--feature-name.md \
   docs/specs/[id]/archived/YYYY-MM-DD--feature-name.md
```

Add to `archived/README.md`:
```markdown
## [Date] - [Feature Name] - COMPLETED
- Implementation: complete
- Status: verified against spec
- Superseded by: [link or N/A]
```

---

## Requirement Syntax: EARS Standard

All functional requirements in the generated specification MUST use **EARS syntax** (Easy Approach to Requirements Syntax).

### Syntax Forms

| Form | Pattern | Example |
|------|---------|---------|
| **Event-driven** | `WHEN <event> THEN the system SHALL <action>` | `WHEN the user clicks "Submit" THEN the system SHALL validate the form data` |
| **State-driven** | `WHEN <system state> THEN the system SHALL <action>` | `WHEN the session expires THEN the system SHALL clear user data` |
| **Generic** | `The system SHALL <action>` | `The system SHALL encrypt all stored passwords with bcrypt` |
| **Feature** | `IF <feature> THEN the system SHALL <action>` | `IF multi-factor auth is enabled THEN the system SHALL require second factor` |
| **Negative** | `IF <unwanted condition> THEN the system SHALL <response>` | `IF SQL input detected THEN the system SHALL reject with 400` |

### Mandatory Keywords

- **SHALL** — obligation (use for MUST requirements)
- **WILL** — intention (use for planned features)
- **MAY** — permission (use for optional behaviors)

### Forbidden Words (cause ambiguity)

- "robust", "intuitive", "fast", "scalable", "efficient", "user-friendly"
- Replace with measurable criteria

### Requirement ID Format

- Format: `REQ-XXX` (e.g., `REQ-001`, `REQ-002`)
- Numbering: Sequential per spec
- Placement: Before each requirement text

### Example Good vs Bad

```markdown
# BAD (vague)
"The system must be fast and secure."

# GOOD (EARS)
"The system SHALL encrypt all stored passwords with bcrypt and cost factor ≥12."

# BAD (missing trigger)
"The user receives a confirmation email."

# GOOD (EARS)
"WHEN a purchase is completed THEN the system SHALL send a confirmation email to the customer's registered address."
```

### Validation Checklist

Before Phase 5 generation, verify:
- [ ] Every requirement has REQ-ID prefix
- [ ] Every requirement uses SHALL/WILL/MAY
- [ ] Every requirement has a trigger (WHEN/IF) or is generic
- [ ] No forbidden words present
- [ ] Each requirement is testable (can verify pass/fail)

## Non-Goals Enforcement

Every specification MUST include an explicit **"Non-Goals"** section that lists what the feature does NOT do.

**Purpose**: Prevent AI agent from adding "helpful" features outside the intended scope.

**Rules**:
1. If the feature doesn't include social login → add "No social login providers"
2. If the feature doesn't support real-time → add "No real-time updates or WebSocket support"
3. If there's no admin panel → add "No administrative interface"
4. Always include at least 3 non-goals

**Format**:
```markdown
## Non-Goals

This feature does NOT include:

- **Feature X**: [Brief explanation why excluded]
- **Feature Y**: [Brief explanation why excluded]
- **Feature Z**: [Brief explanation why excluded]
```

**Trigger Pattern**: "The system will NOT do X" or "X is out of scope for this feature"

### Common Non-Goals Templates (use as starting point)

#### Web Application
- No social login (OAuth, Google, GitHub, etc.)
- No multi-language support (English only)
- No real-time updates (no WebSocket, SSE, or polling)
- No offline mode or PWA support
- No mobile app (web-only)

#### Backend/API
- No GraphQL (REST only)
- No async processing (synchronous only)
- No caching layer
- No message queue integration
- No third-party integrations

#### Database/Data
- No data export functionality
- No data import/migration tools
- No backup/restore utilities
- No data archiving

#### Security
- No two-factor authentication
- No role-based access control (RBAC)
- No API key management
- No audit logging

#### Operations
- No monitoring/observability setup
- No CI/CD pipeline setup
- No containerization
- No deployment automation

**Rule**: Start with project-specific exclusions, then add domain-specific ones.

---

## Negative Requirements

Every specification SHOULD include explicit **"Negative Requirements"** that describe behaviors the system must NOT exhibit. These are constraints that prevent common failures, security issues, or anti-patterns.

### Purpose

- **Prevent failures**: Define what the system MUST NOT do to avoid known failure modes
- **Block security issues**: Specify anti-patterns that must never appear (SQL injection, XSS, etc.)
- **Document constraints**: Make implicit exclusions explicit for future maintainers
- **Guide implementation**: Help developers avoid dangerous patterns during implementation

### Negative Requirements vs Non-Goals

| Aspect | Non-Goals | Negative Requirements |
|--------|-----------|----------------------|
| **Focus** | Features NOT included in this spec | Behaviors the system MUST NOT exhibit |
| **Type** | Scope exclusions (what we don't build) | Anti-patterns/prevention (how we don't build it) |
| **Example** | "No social login" | "The system SHALL NOT store passwords in plain text" |
| **Validation** | Is feature X built? | Does behavior Y occur in implementation? |

### Common Categories

**Security Constraints** (OWASP Top 10 based):
- No SQL string concatenation (use parameterized queries)
- No eval() or dynamic code execution
- No hardcoded credentials or secrets
- No user-generated content without sanitization
- No insecure direct object references

**Data Integrity Constraints**:
- No lost updates (optimistic locking or versioning)
- No data loss on concurrent operations
- No state corruption on failure

**Performance Constraints**:
- No N+1 query patterns
- No blocking operations in request handlers
- No unbounded data structures

**Reliability Constraints**:
- No silent failures (errors must be logged)
- No single points of failure without mitigation
- No data inconsistency across services

### Template Format

```markdown
## Negative Requirements

The system SHALL NOT:

### Security
- [Constraint 1 with REQ-ID]
- [Constraint 2 with REQ-ID]

### Data Integrity
- [Constraint 3 with REQ-ID]

### Reliability
- [Constraint 4 with REQ-ID]
```

### EARS Syntax for Negative Requirements

| Pattern | Example |
|---------|---------|
| **Negative** | `IF <unwanted condition> THEN the system SHALL NOT <action>` |
| **Prevention** | `The system SHALL NOT <unsafe behavior>` |

Example:
```markdown
## Negative Requirements

The system SHALL NOT:

### Security
- REQ-NR001: IF user input is used in SQL query THEN the system SHALL NOT concatenate directly; it SHALL use parameterized queries with placeholders
- REQ-NR002: The system SHALL NOT store passwords in plain text; it SHALL use bcrypt with cost factor ≥12

### Data Integrity
- REQ-NR003: The system SHALL NOT allow concurrent updates to overwrite each other without detection; it SHALL implement optimistic locking
```

### Generating Negative Requirements

During Phase 5, identify negative requirements by asking:
1. "What failures could occur if we don't specify this?"
2. "What security issues could happen with this feature?"
3. "What anti-patterns might developers use?"
4. "What race conditions or data corruption could happen?"

### Validation Checklist

- [ ] At least 3 Negative Requirements present
- [ ] Each has REQ-NR prefix and EARS syntax
- [ ] Categories are identified (Security, Data Integrity, Reliability)
- [ ] No contradictions with positive requirements
- [ ] Directly traceable to anti-patterns or known failure modes

---

## [NEEDS CLARIFICATION] Marker Rules

A `[NEEDS CLARIFICATION]` marker records a question the **user chose to defer**, not a question you decided not to ask. Everything else is grilled (see the Grilling Protocol) and answered before the specification is written.

### Why a marker is an exception

- The grill is the normal way to resolve an unknown. A marker is what remains when the user says "not now" or "I have to check".
- A marker is therefore always traceable to a question that was actually asked and explicitly deferred.
- More than 3 markers in a finished specification is a **symptom**: the grill was cut short. Do not compress the excess into silent assumptions — go back and ask.

### Marker Requirements

| Requirement | Description |
|-------------|-------------|
| **Asked first** | A marker may only exist for a question that was put to the user and that the user deferred |
| **Specific questions** | Each marker must contain a specific, answerable question |
| **Inline placement** | Markers appear inline within requirement text, not as a separate section |
| **Impact prioritization** | Markers are prioritized: scope > security/privacy > user experience > technical |
| **More than 3 is a symptom** | Not a hard cap: it means the grill stopped too early. Resume it rather than trimming the list |

### When to Use a Marker

Mark with `[NEEDS CLARIFICATION: specific question]` ONLY when ALL of these are true:
1. The question was **actually asked** during the grill
2. The user **explicitly deferred** it (not "decide for me" — that is a delegated assumption, see the Grilling Protocol)
3. The choice **significantly impacts feature scope**, security, or user experience

### Areas the Grill MUST Cover (never guessed)

Each row below is a question to put to the user, with your recommended answer already proposed. None
of them is a default you may adopt on your own.

| Area | Ask | Your recommendation is the starting point |
|------|-----|-------------------------------------------|
| Data retention | How long is this data kept, and what happens at the end? | Propose the industry standard for the domain |
| Performance targets | What response time / volume must this hold up to? | Propose standard web/mobile expectations |
| Error handling | What does the user see and what does the system do when this fails? | Propose user-facing message + fallback |
| Authentication / authorization | Who may do this, and how are they identified? | Propose the mechanism already used in the project |
| Integration patterns | What capability must the other system expose? | Propose the shape used by existing integrations |
| UI/UX behaviour | What does the user see and in what order? | Propose the pattern already in the product |
| Input validation | What is a valid value, and what is rejected? | Propose type/range/boundary checks |

If the user answers, the answer becomes a requirement. If the user delegates, your recommendation
becomes a documented assumption. If the user defers, it becomes a marker. There is no fourth branch
in which you decide quietly.

### Marker Syntax

```markdown
The system must support [NEEDS CLARIFICATION: which payment providers should be supported at launch?] for processing transactions.
```

The marker is placed **INLINE** within the requirement text. It does not replace the requirement — the requirement still stands with a best-guess default.

### Marker Validation Checklist

Before Phase 5 generation, verify:
- [ ] Every marker corresponds to a question the user was asked and deferred
- [ ] Each marker has a specific question (not vague "needs clarification")
- [ ] Markers are inline within requirement text
- [ ] Markers are prioritized by impact (scope > security > UX > technical)
- [ ] No marker stands in for a question that was never asked
- [ ] More than 3 markers: the grill is resumed, not trimmed

### Marker Enforcement Examples

```markdown
# GOOD: Specific question, high impact
The system SHALL process payments via [NEEDS CLARIFICATION: which payment providers should be supported at launch?] (Stripe, PayPal, or both?)

# BAD: Vague question
The system SHALL support payments via [NEEDS CLARIFICATION: what should we support?] (unspecified)

# BAD: technical detail, and out of scope for a functional specification
The database should use [NEEDS CLARIFICATION: PostgreSQL or MySQL?] for storage.
→ Not a functional question at all. It belongs to the technical plan.

# BAD: never asked, silently defaulted
The system retains audit records for 90 days.
→ Retention was never put to the user. Ask, then record the answer.
```

### Marker Count Validation in Phase 5

After generating the specification:
1. Count all `[NEEDS CLARIFICATION:` occurrences
2. For each one, confirm the user was asked and chose to defer. A marker with no question behind it is a missing grill round: go and ask it now
3. If count > 3: tell the user the grill looks incomplete and offer to resume it. Never convert the excess into best-guess assumptions on your own
4. Report final marker count in the completion summary

---

## Hard Boundary: No Implementation During Brainstorming

This command is a **specification authoring workflow only**.

### Allowed File Changes

The command may create or edit only specification artifacts, such as:

- `docs/specs/[id]/YYYY-MM-DD--feature-name.md`
- `docs/specs/[id]/user-request.md`
- `docs/specs/[id]/brainstorming-notes.md`
- `docs/specs/[id]/decision-log.md`
- `docs/specs/ontology.md`

### Forbidden Actions

The command MUST NOT:

- Edit source code, tests, configuration, migrations, build files, or runtime assets
- Apply bug fixes, refactors, patches, or behavior changes
- Run code-formatting or code-modifying commands
- Create commits or branches for implementation work
- Treat a user request for "fix", "modify", "change", "patch", "refactor", "correggi", "modifica", "risolvi", or "sistema" as permission to change code

### Required Response for Fix/Modification Requests

If the user request is primarily a bug fix or modification of existing behavior, respond with a message instead of implementing:

```markdown
This request is a bug fix or change to existing behavior, so this skill is not the right tool: it only produces new functional specifications, and I will not modify code from here.

I can instead model the desired end-state as a new functional specification, if that helps. Otherwise, stop here.
```

After showing the message, always ask the user whether they want to create a **new functional specification** instead.

Use ask_user_question with these options:
- "Create a new functional spec" (continue only with documentation)
- "Exit without changes"

Only continue with brainstorming if the user explicitly confirms they want a **new functional specification** and not a direct code change.

---

## Phase 0: Input Mode Detection & ADR Discovery

**Goal**: Determine whether the input is a free-form idea, an ADR/RFC, or a structured analysis document. If the input is a structured document, extract architectural decisions as constraints before proceeding.

**Context**: The the skill arguments parameter may contain:
- A free-text idea (e.g., "Add user authentication with JWT tokens")
- A path to an existing document (e.g., `@docs/adr/039-git-worktree-management.md`)
- A reference to a file containing architectural decisions, RFC, or analysis

**Actions**:

1. **Detect input mode**:
   - If the skill arguments contains a file path pattern (starts with `/`, `./`, `docs/`, or `@docs/`): **Structured Document Mode**
   - If the skill arguments is free text describing a feature: **Free-Form Idea Mode**
   - If the skill arguments is empty: Ask user for input and detect mode from their response

2. **If Structured Document Mode**:
   - Read the referenced document
   - Extract all **architectural decisions** documented in the file:
     - Configuration values, defaults, and file paths
     - CLI flags and command structures proposed
     - Integration patterns with existing systems
     - Error handling and edge-case strategies
     - Directory structures and documentation conventions
   - Create a `constraints` list in memory with the extracted decisions
   - **Do NOT re-evaluate these decisions** — they are the architectural foundation. The functional specification must work within them.
   - If a decision in the ADR contradicts project conventions (e.g., architecture.md, ontology.md), flag it as a conflict, not as a candidate for change

3. **If Free-Form Idea Mode**:
   - Proceed directly to Phase 1 — no constraints to extract
   - The brainstorming will discover all decisions collaboratively

4. **Decision override protocol**:
   - If during brainstorming you identify that an ADR decision should be overridden:
     - Create a DEC entry in `decision-log.md` with:
       - Reference to the original ADR (e.g., "Overrides ADR-039, Section 3: Configuration")
       - Justification for the override
       - Impact on the specification
     - Only then modify the constraint
   - Without a DEC entry, ADR constraints remain immutable

5. **Summarize constraints** (Structured Document Mode only):
   - After extraction, produce a brief summary:
   ```
   Input Mode: Structured Document (ADR-039)
   Constraints extracted:
   - Config: worktreeBasePath (default: ../<repo-name>-worktrees)
   - CLI: No explicit flags mentioned
   - Integration: ADR-038 branch creation
   - Behavior: Worktree creation + manual cleanup command
   Override DEC entries: None / DEC-XXX
   ```

---

## Phase 1: Context Discovery

**Goal**: Understand the current project state and the initial idea, within the bounds of any extracted constraints

**Initial idea**: the skill arguments

**Actions**:

1. Create todo list with all phases (including Phase 0 if Structured Document Mode)
2. **Determine workflow tier before codebase exploration, document generation, or any action that could become implementation**:
    - **Bug fix** (defect in existing system):
        - STOP the brainstorming workflow by default
        - Do NOT inspect files with the intent to patch them
        - Do NOT edit source code, tests, configuration, migrations, or build files
        - Explain that bug fixes are out of scope for this skill (it produces new specifications only)
        - Ask via ask_user_question only to confirm routing:
            - Options:
                - "Create a new functional spec" (only if the user wants a new specification instead of a bug fix)
                - "Exit without changes"
    - **Modify existing behavior / refactor / delta change**:
        - STOP the brainstorming workflow by default
        - Do NOT apply the requested change
        - Explain that modifications to existing behavior are out of scope for this skill (it produces new specifications only)
        - Ask via ask_user_question only to confirm routing:
            - Options:
                - "Create a new functional spec" (only if the user wants a new specification instead of a delta/change)
                - "Exit without changes"
    - **Direct implementation request** (e.g., "fix it", "make the change", "implement this now"):
        - Refuse to implement inside brainstorming
        - Explain that brainstorming only writes specs
        - Recommend the appropriate implementation/debugging workflow after a spec/task exists
    - **New feature** (any scope): Continue with brainstorm
3. Only after the request is confirmed as a new feature specification, explore the current project state (for context only - do NOT include in specification):
    - Read recent commits to understand what's being worked on
    - Check for existing documentation (README, docs/, existing specs)
    - Look for related features or similar implementations
4. Ask the opening questions, one at a time (the full grill happens in Phase 2):
    - What problem are they trying to solve?
    - What is the high-level goal?
    - Any initial thoughts or constraints?

---

## Phase 1.5: Complexity Assessment & Scope Validation

**Goal**: Assess idea complexity early and guide user to split if scope is too large for a single specification

**Actions**:

1. **Estimate implementation scope** based on the idea description and context from Phase 1:
   - Count distinct user stories / use cases mentioned
   - Identify separate functional domains or bounded contexts
   - Note integration points with external systems
   - Assess data model complexity (entities, relationships)
   - Evaluate user interaction complexity (flows, edge cases)

2. **Classify scope size** using these indicators:

   **Small Scope** (proceed normally - will generate 3-8 tasks):
   - Single user story or use case
   - One functional domain
   - 0-2 integration points
   - Simple data model (1-3 entities)
   - Straightforward user flow
   - Examples: "Add password reset", "Implement search filter", "Add user profile photo upload"

   **Medium Scope** (proceed normally - will generate 8-15 tasks):
   - 2-4 user stories
   - One focused functional domain
   - 2-4 integration points
   - Moderate data model (4-8 entities)
   - Multiple user flows but related
   - Examples: "User authentication with roles", "Product catalog with categories"

   **Large Scope** (WARNING - will likely generate >15 tasks - see step 3):
   - 5+ user stories
   - Multiple functional domains or bounded contexts
   - 5+ integration points
   - Complex data model (9+ entities)
   - Multiple independent user flows
   - Examples: "Full E-commerce system", "Multi-provider travel aggregator", "Complete CRM system"

3. **If scope is classified as LARGE**:
   - **Inform the user**: "This idea has a very large scope. To ensure high-quality implementation and maintainable code, I recommend splitting it into smaller, focused specifications."
   - **Propose a split strategy**: Suggest 2-3 smaller specifications that cover the original idea incrementally.
     - Example split:
       - Spec 1: Core domain and data model
       - Spec 2: Primary user flows and API
       - Spec 3: Advanced features and integrations
   - **Use ask_user_question** to offer options:
     - Options:
       - "Split the idea into the suggested specifications" (recommended)
       - "Focus only on one part of the idea" (ask which one)
       - "Continue with a single large specification" (not recommended - warn about task count limit)
   - If user chooses to split: Focus the current brainstorming session on the FIRST part of the split.
   - If user chooses to focus on one part: Focus the current session on that part.
   - If user chooses to continue: Proceed with a warning that `spec-to-tasks` will reject the spec if it exceeds 15 tasks, and that even within the limit any single task declaring more than 8 files or more than 6 acceptance criteria will trigger a split proposal: oversized tasks are what measurably need repeated implementation attempts in the loop.

---

## Phase 2: Grilling the Idea

**Goal**: Extract the specification from the user through sustained interrogation, one question at a
time, until nothing material is left undecided

This is the heart of the skill. Apply the **Grilling Protocol**: a single question per turn, each
carrying your recommended answer, waiting for the reply before the next one. There is **no limit** on
the number of questions — the loop ends on the protocol's exit condition, never on a quota.

**Actions**:

1. Open the loop by telling the user what is about to happen: you will ask a series of questions, one
   at a time, each with a proposed answer they can simply confirm, and they can say "proceed" at any
   point to stop.
2. Before asking anything, read what is already written: Phase 0 constraints, existing specs, ADRs,
   `CONTEXT.md`, the codebase. Anything answered there is confirmed, not asked.
3. Grill each area below in order, depth first — when an answer opens a new decision, follow it
   immediately rather than queueing it. An area is done when its answers are precise enough to write
   testable acceptance criteria from them.

   **Area 1 — Problem and actors**: what breaks today, who feels it, what "solved" looks like.

   **Area 2 — Scope and boundary**: what is in this specification and what is deliberately left out.
   Every boundary answer is a candidate Non-Goal.

   **Area 3 — Business rules**: the rules that govern the behaviour, including the ones that hold
   only in some states. Push for the rule, not the example.

   **Area 4 — Data**: what information exists, what makes it valid, who may see it, how long it is
   kept.

   **Area 5 — Flows and edge cases**: the nominal path, then the alternatives, then what happens when
   each step fails. Invent concrete scenarios and force a precise answer on each one.

   **Area 6 — Integrations**: which existing systems are touched, and what capability each must
   provide.

   **Area 7 — Exclusions and negative requirements**: what the system must never do. Ask explicitly:
   - "Are there security constraints or anti-patterns we must avoid?"
   - "Are there known failure modes or race conditions to prevent?"
   - "Are there data integrity constraints beyond normal validation?"

   **Area 8 — The never-guessed list**: every row of *Areas the Grill MUST Cover* in the
   [NEEDS CLARIFICATION] Marker Rules section that this feature touches — retention, performance,
   error behaviour, authorization, integration shape, UI behaviour, validation. One question each,
   with your recommendation.

4. Sharpen the language as you go: when the user uses a vague or overloaded term, propose the precise
   one and get it confirmed. When an answer contradicts an earlier one, the project's documented
   language, or the code, surface the contradiction and ask which holds.
5. Record each answer as you receive it. Delegated answers ("decide for me") become documented
   assumptions; deferred answers become `[NEEDS CLARIFICATION]` markers. Nothing is left implicit.
6. If the user changes the idea significantly mid-grill, restart from the affected area.
7. Close the loop with a summary of every answer collected, and ask the user to confirm it before
   moving to Phase 3.

---

## Phase 3: Functional Approach Exploration

**Goal**: Present 2-3 different functional approaches with trade-offs (WHAT, not HOW)

**Actions**:

1. Based on the refined idea, develop 2-3 distinct approaches focusing on BEHAVIOR:
    - **Approach A**: Simple/MVP (fastest to implement, may lack some features)
    - **Approach B**: Balanced (good feature set, reasonable complexity) - **typically your recommendation**
    - **Approach C**: Comprehensive (full-featured, more complex)

2. For each approach, describe ONLY functional aspects:
    - User behaviors supported
    - Business rules and constraints
    - Data requirements (what, not how)
    - Integration points (capabilities needed, not technical implementation)
    - Pros (benefits for users/business)
    - Cons (limitations, complexity for users)

3. **CRITICAL**: Do NOT mention any technical details:
    - NO frameworks (Spring, NestJS, React, etc.)
    - NO patterns (Repository, Service, Controller, etc.)
    - NO libraries or dependencies
    - NO code or pseudo-code

4. Present the approaches with ask_user_question and let the **user** choose:
    - Lead with your recommended option and say why it is your recommendation
    - Present the alternatives fairly, with what each one costs and gives up
    - Never select on your own, not even when one approach clearly dominates: state that it dominates
      and have the user confirm it
5. Grill the chosen approach before leaving the phase: whatever it leaves ambiguous goes back through
   the Phase 2 loop, one question at a time

6. **After approach selection, log the decision**:
    - Create an in-memory note of DEC-001: Approach Selection
    - Record: date, approach chosen, alternatives presented, rationale
    - This will be written to `decision-log.md` in Phase 6

---

## Phase 4: Contextual Codebase Exploration (Optional)

**Goal**: Understand existing codebase for context only — do NOT influence the specification with technical decisions

**NOTE**: This phase is OPTIONAL. Skip if not needed. The functional specification should be technology-agnostic.

**Actions**:

1. Only if the feature needs to integrate with existing systems, explore the codebase directly (there is no subagent dispatch; do it in this session):

   **Explore codebase for integration context** — understand what existing systems, APIs, or data structures the new feature must integrate with.

   Focus on:
   1. Existing APIs or interfaces the feature must use
   2. Shared data structures or models
   3. Existing business rules that apply

   Return:
   - List of integration requirements (capabilities needed, not implementation)
   - Do NOT suggest frameworks, patterns, or technical solutions

2. Incorporate findings as integration requirements in the specification
3. Do NOT let this influence technical decisions — keep the specification functional

---

## Phase 5: Functional Specification Presentation

**Goal**: Present the functional specification in validated sections

**DO NOT START WITHOUT APPROACH APPROVAL**

**Template**: Read the functional specification template at `templates/functional-specification.md` (in this skill directory) to understand the target structure. The specification MUST follow this template.

**Actions**:

1. Once the approach is selected, present the functional specification in sections of 200-300 words each
2. Incorporate any integration requirements from Phase 4
3. Cover the following areas in separate sections (matching the template structure):

   **Section 1: Business Context** (→ template: `## Business Context`)
    - What problem does this feature solve?
    - Who are the users and what are their goals?
    - How does this fit into the overall system purpose?

   **Section 2: Functional Requirements** (→ template: `## Functional Requirements`)
    - User stories and use cases
    - Business rules and constraints
    - Data requirements (what data, not how to store)
    - External system capabilities needed

   **Section 3: User Interactions** (→ template: `## User Interactions`)
    - User flows and journeys
    - Alternative paths and edge cases
    - Error scenarios and how users are informed

   **Section 4: Acceptance Criteria** (→ template: `## Acceptance Criteria`)
    - Clear, testable criteria for each user story
    - Success conditions in natural language
    - Edge case handling
    - **MANDATORY: Acceptance Criteria Taxonomy** — Every criterion MUST be classified with one of:
      - **`[IMP]` Implementable**: Requires new code, configuration, or explicit system behavior. **Only these generate implementation tasks.**
      - **`[SEF]` Side-Effect**: A natural, automatic consequence of an `[IMP]` criterion being satisfied. These do NOT generate standalone tasks but should be verifiable in e2e tests.
      - **`[EXT]` External Verification**: Verified by external tools, user observation, or existing system behavior. These do NOT generate tasks but should appear as e2e checkpoints.
    - **60% Rule**: At least 60% of acceptance criteria should be `[IMP]`. If fewer than 60% are `[IMP]`, the specification is too descriptive and not prescriptive enough — return to Section 2 and refine.
    - **Why this matters**: `spec-to-tasks` uses `[IMP]` criteria to generate atomic tasks. `[SEF]` and `[EXT]` criteria that are misclassified as `[IMP]` produce "false work" — tasks that verify natural behavior rather than implement functionality.

   **Section 5: Integration Requirements** (→ template: `## Integration Requirements`)
    - What existing systems must integrate with (capabilities, not implementation)
    - Data exchange requirements (not technical protocols)

4. **CRITICAL**: Throughout all sections, NEVER mention:
    - Frameworks, libraries, or tools
    - Technical patterns or architectural styles
    - Code or pseudo-code

5. Validate section by section: present a section, collect the user's feedback or approval, then move
   to the next one. Do not draft the whole specification and present it once
    - Whatever a section leaves ambiguous goes back through the Phase 2 grill loop before the section
      is approved
    - The user may explicitly ask for the full draft in one go ("show me everything, no stops"): only
      then present all sections together

6. Move to Phase 5.3 when every section has been approved

---

## Phase 5.3: Non-Goals Definition

**Goal**: Explicitly define what this feature does NOT include

**Actions**:

1. **Review the idea description** and identify:
   - What was explicitly mentioned as out of scope
   - What was mentioned as in scope
   - Common related features that could be assumed

2. **Brainstorm potential Non-Goals** by asking:
   - "What would a developer naturally assume but is NOT in scope?"
   - "What related features could be 'helpful' but are excluded?"
   - "What technical capabilities are related but not required?"

3. **Generate Non-Goals list** (minimum 3):
   - Platform limitations (e.g., "No mobile app", "No offline mode")
   - Feature exclusions (e.g., "No social login", "No real-time sync")
   - Scope boundaries (e.g., "No multi-tenancy", "No plugin system")
   - Technical exclusions (e.g., "No WebSocket", "No GraphQL")

4. **Format each Non-Goal**:
   - Bold the excluded feature name
   - One sentence explaining why it's excluded
   - Connects to business logic when possible

**Output**:
```markdown
## Non-Goals

This feature does NOT include:

- **Social Login**: Only email/password authentication is supported
- **Multi-language Support**: Interface is English only
- **Real-time Updates**: No WebSocket or SSE support
- **Admin Panel**: User management done via database directly
- **Export/Import**: No data migration utilities
```

**Validation**:
- [ ] Minimum 3 Non-Goals present
- [ ] Each Non-Goal has explanation
- [ ] No contradictions with functional requirements
- [ ] Non-Goals are mutually exclusive with requirements

---

## Phase 6: Specification Generation

**Goal**: Generate professional functional specification document

**Actions**:

1. Compile all validated specification sections

2. Generate unique spec ID:
    - Count existing folders in `docs/specs/` to determine next sequence number
    - Create slug from feature name (lowercase, hyphenated)
    - Format: `NNN-feature-slug` (e.g., `001-hotel-search-aggregation`)
    - Example: If 5 specs exist, next ID is `006-feature-name`

3. Create spec folder: `docs/specs/[id]/`

4. **CRITICAL: Save the original user request**:
    - Create a file `user-request.md` in `docs/specs/[id]/` containing:
        - The original user input/idea description
        - Any constraints or requirements mentioned
        - This file will be used by `spec-to-tasks` to verify all requirements are captured
    - Example content:
      ```markdown
      # User Request

      **Original Input**: [what the user asked for]

      **Key Requirements Mentioned**:
      - [requirement 1]
      - [requirement 2]

      **Constraints**: [any constraints mentioned]
      ```

5. Generate a professional functional specification document directly (there is no subagent dispatch; do it in this session), based on the following validated specification:

    **Feature Title**: [title]
    **Date**: [current date]
    **Spec ID**: [id] (e.g., 001-hotel-search-aggregation)

    **Business Context**:
    - Problem solved: [from Section 1]
    - Target users: [from Section 1]
    - System fit: [from Section 1]

    **Functional Requirements**:
    - User stories: [from Section 2]
    - Business rules: [from Section 2]
    - Data requirements: [from Section 2]
    - External capabilities: [from Section 2]

    **User Interactions**:
    - User flows: [from Section 3]
    - Alternative paths: [from Section 3]
    - Error scenarios: [from Section 3]

    **Acceptance Criteria**:
    - Testable criteria: [from Section 4 — each MUST be tagged with [IMP], [SEF], or [EXT]]
    - Success conditions: [from Section 4]
    - Edge cases: [from Section 4]
    - **60% Rule Check**: Ensure at least 60% of criteria are [IMP]; if not, flag for refinement

    **Integration Requirements**:
    - Systems to integrate: [from Section 5]
    - Data exchange: [from Section 5]

    **Non-Goals**: [from Phase 5.3]
    **Negative Requirements**: [security, data integrity, reliability constraints]
    **Open Questions**: [list]

    Read the functional specification template at `templates/functional-specification.md` (in this skill directory) and use it as the document structure.
    Fill in the gathered information into the template sections.
    Save the result to: docs/specs/[id]/YYYY-MM-DD--feature-name.md

    IMPORTANT:
    - Read and follow the template at `templates/functional-specification.md`
    - This is a FUNCTIONAL specification, NOT a technical design
    - Do NOT mention any frameworks, libraries, or tools
    - Do NOT include code or pseudo-code
    - Focus on WHAT the system should do, not HOW
    - Use EARS syntax (SHALL/WILL/MAY) for all requirements
    - Include REQ-XXX prefix for each requirement
    - Every acceptance criterion MUST include its taxonomy tag: [IMP], [SEF], or [EXT]
    - Include Non-Goals section (minimum 3 items)
    - Include Negative Requirements section (minimum 3 items with REQ-NR prefix)

6. Verify the document was created successfully in `docs/specs/[id]/`
    - If the file was not created or is incomplete:
        - Regenerate it with additional guidance
        - Use ask_user_question to decide: "Retry generation", "Continue with manual creation", or "Abort"

8. **CRITICAL: Save brainstorming context files for later use by spec-to-tasks**:
    - If you have conversation context or notes about the feature (from the dialogue with user), save them to the spec
      folder
    - Create a file named `brainstorming-notes.md` in `docs/specs/[id]/` with:
        - Key technical decisions discussed
        - Architecture patterns mentioned
        - Any specific technologies or integrations requested
        - Notes about implementation approach
    - This file will be read by `/skill:specs-kit-spec-to-tasks` to ensure technical details are NOT lost

8.5. **Create decision-log.md for decision audit trail**:

- Create a file `decision-log.md` in `docs/specs/[id]/` with the following format:
  ```markdown
  # Decision Log: [Feature Name]

  | ID | Date | Task | Decision | Alternatives | Impact | Decided By |
  |----|------|------|----------|--------------|--------|------------|

  ## DEC-001: Approach Selection
  - **Date**: [current date YYYY-MM-DD]
  - **Task**: Brainstorming
  - **Phase**: Approach Selection
  - **Context**: Selection of functional approach for feature specification
  - **Decision**: [Approach chosen - A/B/C]
  - **Alternatives Considered**: [Brief description of approaches presented]
  - **Impact**: Specification structure, scope boundaries, acceptance criteria
  - **Decided By**: user selection
  ```
- This file will track all non-trivial decisions made during implementation
- Future phases (task-implementation, task-review) will append entries to this file

8.6. **Initialize or enrich the project ontology (`docs/specs/ontology.md`)**:

   Domain terms identified during brainstorming are part of the functional understanding (Ubiquitous Language). This step captures them in a shared, project-level ontology file.

   - **Check if `docs/specs/ontology.md` exists**:

   - **If the file does NOT exist**:
     1. Collect domain terms that emerged during the brainstorming dialogue (from Phases 2-5)
     2. Use **ask_user_question** to present the identified terms and ask the user to confirm, add, or remove terms:
        ```
        During brainstorming, the following domain terms emerged:
        - [Term 1]: [proposed definition]
        - [Term 2]: [proposed definition]
        - ...

        Should I create the project ontology (docs/specs/ontology.md) with these terms?
        ```
        - Options:
          - "Yes, create with these terms" (recommended)
          - "Yes, but let me adjust the terms first"
          - "Skip ontology creation for now"
     3. If the user confirms, create `docs/specs/ontology.md` using this template:
        ```markdown
        # Project Ontology — Ubiquitous Language

        **Created**: [current date YYYY-MM-DD]
        **Last Updated**: [current date YYYY-MM-DD]

        ## Domain Glossary

        | Term | Definition | Bounded Context |
        |------|-----------|-----------------|
        | [Term 1] | [Definition] | [Context where this term applies] |
        | [Term 2] | [Definition] | [Context where this term applies] |

        ## Bounded Contexts

        | Context | Description | Key Terms |
        |---------|-------------|-----------|
        | [Context 1] | [Description] | [Terms specific to this context] |

        ## Conceptual Mapping

        [Relationships between key domain entities — to be refined during task generation]
        ```

   - **If the file ALREADY exists**:
     1. Read the existing `docs/specs/ontology.md`
     2. Compare domain terms from the brainstorming session against existing glossary entries
     3. If NEW terms were identified that are not in the glossary:
        - Use **ask_user_question** to present the new terms and ask if they should be added
        - If confirmed, append the new terms to the Domain Glossary table
        - Update the `Last Updated` date
     4. If no new terms: skip silently

   - **Note**: The ontology is a living document. It will be further refined by `/skill:specs-kit-spec-to-tasks` when technical decisions are made.

9. Update todos

---

## Phase 6.5: EARS Validation

**Goal**: Ensure all requirements follow EARS syntax before finalizing the spec

**Actions**:

1. **Parse all requirements** in the generated spec:
   - Extract requirements with `REQ-XXX` pattern
   - Identify requirements that lack REQ-ID

2. **Validate each requirement**:
   - Has REQ-ID prefix?
   - Uses SHALL/WILL/MAY keyword?
   - Has trigger (WHEN/IF) or is generic (no trigger)?
   - Contains forbidden words?

3. **Fix violations**:
   - Add missing REQ-IDs
   - Restructure requirements missing triggers
   - Replace forbidden words with measurable alternatives

4. **Document non-requirements**:
   - Explanatory text (not requirements) should NOT have REQ-ID
   - Notes and rationale are exempt from EARS syntax

5. **Update requirement count**:
   - Report final REQ count in summary
   - Flag if >50% of requirements are generic (may indicate missing triggers)

**Output**: EARS-compliant requirements section with validation report

Example output snippet:

```markdown
## Functional Requirements

### Authentication (4 requirements)

**Context**: User login and session management

| ID | Requirement | Trigger Type |
|----|-------------|--------------|
| REQ-001 | The system SHALL validate credentials against the user database | Event (login attempt) |
| REQ-002 | The system SHALL lock account after 5 failed attempts | Event (failed attempt) |
| REQ-003 | WHEN session expires THEN the system SHALL clear user data | State transition |
| REQ-004 | The system SHALL encrypt all passwords with bcrypt cost ≥12 | Generic |
```

---

### [NEEDS CLARIFICATION] Markers

When writing the specification, mark the aspects the user **explicitly deferred** during the grill.
This creates a bidirectional link with `specs.spec-check`, which resolves these markers. An aspect
that was never put to the user is not a marker: it is a missing question — go back and ask it.

**When to use a marker**:

Mark with `[NEEDS CLARIFICATION: specific question]` ONLY when ALL of these are true:
1. The question was **asked** during the Phase 2 grill
2. The user **deferred** it ("not now", "I have to check") rather than answering or delegating
3. The choice **significantly impacts feature scope**, security, or user experience

**When NOT to use a marker**:

| Situation | What to do instead |
|-----------|--------------------|
| The user answered | Write the answer as a requirement |
| The user delegated ("decide for me") | Write your recommendation and record it in Assumptions as delegated |
| The question was never asked | Ask it now — see *Areas the Grill MUST Cover* |
| It is a technical decision (storage, protocol, framework) | Out of scope here; it belongs to the technical plan |

**Marker syntax**:

```markdown
The system must support [NEEDS CLARIFICATION: which payment providers should be supported at launch?] for processing transactions.
```

The marker is placed INLINE within the requirement text. It does not replace the requirement — the requirement still stands with a best-guess default. The marker flags the uncertainty.

**Rules**:

- **More than 3 markers is a symptom** that the grill stopped early: offer to resume it rather than trimming the list
- **Prioritize by impact**: scope > security/privacy > user experience > technical details
- Each marker must contain a **specific question** (not a vague "needs clarification")
- The surrounding requirement text should still be meaningful with the default assumption
- Do NOT create a separate "Needs Clarification" section — markers are inline

**Examples of good markers**:

```markdown
# Good: specific, scope-impacting
The system must process refunds [NEEDS CLARIFICATION: should refunds be automatic or require manual approval?] within 5 business days.

# Good: security-impacting
User data must be retained [NEEDS CLARIFICATION: what is the data retention period required by GDPR/compliance?] according to regulatory requirements.

# Good: UX-impacting with multiple interpretations
Search results should be sorted [NEEDS CLARIFICATION: by relevance, recency, price, or user-selectable?] by default.
```

**Examples of bad markers**:

```markdown
# Bad: never asked, so not deferred
User sessions expire [NEEDS CLARIFICATION: after how long?] automatically.
→ Session lifetime was never put to the user. Ask it, with your recommendation.

# Bad: too vague
The system must be [NEEDS CLARIFICATION: fast?] for all users.
→ Bad marker. Make it measurable: "The system must respond to user actions within 2 seconds."

# Bad: implementation detail (not scope-level)
The database should use [NEEDS CLARIFICATION: PostgreSQL or MySQL?] for storage.
→ This is an implementation decision, not a spec-level ambiguity. Don't mark.
```

**After spec generation**:

If any markers were placed, include a note in the completion summary:
```
Specification created with 2 [NEEDS CLARIFICATION] markers:
  1. "Which payment providers should be supported?"
  2. "Should guest checkout be allowed?"

Next: Run /skill:specs-kit-spec-check to resolve.
```

---

## Phase 7: Specification Review

**Goal**: Review the generated functional specification for quality, completeness, and EARS compliance

**IMPORTANT**: The functional specification should be technology-agnostic (WHAT), but technical details discussed during
brainstorming are preserved separately in `brainstorming-notes.md` for use by `spec-to-tasks`.

**Actions**:

1. Review the specification yourself (there is no subagent dispatch; do it in this session). Check the file at docs/specs/[id]/YYYY-MM-DD--feature-name.md for:

    1. **Completeness**: All required sections are present (Business Context, Functional Requirements, User Interactions, Acceptance Criteria, Integration Requirements, Out of Scope, Open Questions)

    2. **Functional Focus**: Verify the specification is purely functional:
       - NO mention of frameworks, libraries, or tools
       - NO technical patterns or architectural styles
       - NO code or pseudo-code
       - Focuses on WHAT, not HOW

    3. **Quality**: Content is clear, specific, and actionable

    4. **Testability**: Acceptance criteria are clear and testable

    5. **Acceptance Criteria Taxonomy**: Verify that:
       - Every acceptance criterion is tagged with `[IMP]`, `[SEF]`, or `[EXT]`
       - No `[SEF]` or `[EXT]` is disguised as `[IMP]` (e.g., "git worktree list shows worktree" should be `[SEF]`, not `[IMP]`)
       - At least 60% of criteria are `[IMP]`; if not, flag as "Under-specified — needs more prescriptive criteria"

    6. **Formatting**: Proper markdown structure, consistent formatting

    7. **Clarity**: Language is professional, concise, and unambiguous

    8. **EARS Compliance**: All requirements have REQ-ID, use SHALL/WILL/MAY, and have appropriate triggers

    9. **Negative Requirements**: At least 3 present with REQ-NR prefix and SHALL NOT syntax

    10. **Non-Goals**: At least 3 present with explanations

    Provide:
    - Overall assessment (Excellent / Good / Needs Revision)
    - List of any missing sections or content
    - Specific issues found (if any)
    - Any technical details that should be removed
    - EARS violations (if any)
    - Recommendations for improvement (if needed)

2. Synthesize the review findings

3. **Use the ask_user_question tool to present the review findings**:

   Present options based on agent assessment:
    - **Option A**: Document is excellent, proceed to next steps
    - **Option B**: Minor revisions needed (agent will specify what)
    - **Option C**: Major revisions needed (regenerate with corrections)

4. If revisions are needed:
    - For minor revisions: Edit the document directly based on agent feedback
    - For major revisions: Re-run Phase 6 with updated instructions from agent
    - Optionally: Re-run Phase 7 with another review if significant changes were made

5. Once approved, mark documentation phase complete

---

## Phase 8: Next Steps Recommendation

**Goal**: Recommend the appropriate next command in the workflow

**Actions**:

1. The functional specification is complete. The next step is to convert it to executable tasks:

   **For converting specification to tasks**: Recommend `/skill:specs-kit-spec-to-tasks`
    - Use when: Converting functional specification to trackable tasks
    - Arguments: `docs/specs/[id]/`

2. **Use the ask_user_question tool to present the recommendation**:

   Present options:
    - **Option A**: Run spec-check first, then generate tasks (recommended)
    - **Option B**: Skip review and go directly to task generation (warning: may have quality issues)
    - **Option C**: Exit and review the specification manually

3. Include the pre-filled commands:

```bash
# Recommended: Run spec-check first, then generate tasks
/skill:specs-kit-spec-check docs/specs/[id]/
/skill:specs-kit-spec-to-tasks docs/specs/[id]/

# Alternative: Skip review and generate tasks directly
/skill:specs-kit-spec-to-tasks docs/specs/[id]/
```

   - The functional specification has been saved at `docs/specs/[id]/YYYY-MM-DD--feature-name.md`
   - The task list will be saved at `docs/specs/[id]/YYYY-MM-DD--feature-name--tasks.md`
   - Individual tasks will be in `docs/specs/[id]/tasks/TASK-XXX.md`

---

## Phase 9: Summary

**Goal**: Document what was accomplished

**Actions**:

1. Mark all todos complete
2. Summarize:
    - **Original Idea**: What was brainstormed
    - **Input Mode**: Free-Form Idea / Structured Document (ADR reference if applicable)
    - **Scope Assessment**: Small / Medium / Large (and user choice if large)
    - **Scope Split Decision**: [If applicable: "User chose to split into N specifications - focusing on Spec A: [name]" OR "User chose to continue with single specification despite large scope warning"]
    - **Approach Selected**: Which approach was chosen and why
    - **Integration Context**: Key integration requirements (if any)
    - **Functional Specification Created**: Key aspects of the specification
    - **Spec ID**: `[id]` (e.g., `001-hotel-search-aggregation`)
    - **Document Location**: `docs/specs/[id]/YYYY-MM-DD--feature-name.md`
    - **EARS Validation**: Number of requirements validated, any violations fixed
    - **Specification Review**: Review outcome and any revisions made
    - **[NEEDS CLARIFICATION] Markers**: Count and list of markers (if any)
    - **Recommended Next Step**: 
      - If scope was split: "Complete this specification's implementation, then run /skill:specs-kit-brainstorm for Spec B: [name]"
      - Otherwise: "Generate task list with /skill:specs-kit-spec-to-tasks"

---

## Integration with Development Commands

This brainstorming command produces a **functional specification** that feeds into the modular workflow:

### Output Flow

```
/skill:specs-kit-brainstorm
↓
Phase 0: Input Mode Detection (ADR/RFC or free-form)
↓
Phase 1-2: Context Discovery & Grilling
↓
Phase 3: Functional Approach Exploration (MVP / Balanced / Comprehensive)
↓
Phase 4: Optional Codebase Exploration (for integration context only)
↓
Phase 5: Functional Specification Presentation (validated incrementally)
↓
Phase 6: Documentation (specialist agent)
       + Ontology initialization (docs/specs/ontology.md)
↓
Phase 7: Specification Review (quality verification with code-reviewer agent)
↓
[Creates: docs/specs/[id]/YYYY-MM-DD--feature-name.md]
[Creates: docs/specs/[id]/user-request.md]
[Creates: docs/specs/[id]/brainstorming-notes.md]
[Creates: docs/specs/[id]/decision-log.md]
[Creates/Updates: docs/specs/ontology.md (domain terms)]
↓
[Recommends: spec-check + spec-to-tasks]
↓
/skill:specs-kit-spec-to-tasks docs/specs/[id]/
↓
[Ensures: docs/specs/architecture.md exists]
[Refines: docs/specs/ontology.md]
[Creates: docs/specs/[id]/YYYY-MM-DD--feature-name--tasks.md]
[Creates: docs/specs/[id]/tasks/TASK-XXX.md]
↓
/skill:specs-kit-task-implementation --task="docs/specs/[id]/tasks/TASK-XXX.md"
↓
[Implements single task]
```

### Specification as Reference

The functional specification created by this command serves as:

1. **Reference during implementation**: The development commands can read the specification for context
2. **Communication tool**: Can be shared with team members for review
3. **Documentation**: Becomes part of project's functional specification history
4. **Task generation input**: Used by `spec-to-tasks` to create executable tasks
5. **Organized storage**: All related files (spec, tasks, individual tasks) are grouped in `docs/specs/[id]/`

### Re-entering Brainstorming

If implementation reveals specification issues, you can re-run `/skill:specs-kit-brainstorm`:
- The previous specification will be preserved in its folder
- A new specification will be created with the current date
- You can reference the previous specification during the new brainstorming session

## Todo Management

Throughout the process, maintain a todo list like:

```
[ ] Phase 0: Input Mode Detection & ADR Discovery (if applicable)
[ ] Phase 1: Context Discovery
[ ] Phase 1.5: Complexity Assessment & Scope Validation (split if scope too large)
[ ] Phase 2: Grilling the Idea (one question at a time, no quota)
[ ] Phase 3: Functional Approach Exploration
[ ] Phase 4: Contextual Codebase Exploration (Optional)
[ ] Phase 5: Functional Specification Presentation
[ ] Section 1: Business Context
[ ] Section 2: Functional Requirements
[ ] Section 3: User Interactions
[ ] Section 4: Acceptance Criteria (with [IMP]/[SEF]/[EXT] taxonomy)
[ ] Section 5: Integration Requirements
[ ] Phase 5.3: Non-Goals Definition
[ ] Phase 6: Specification Generation
[ ] Phase 6.1: Ontology Initialization/Enrichment (docs/specs/ontology.md)
[ ] Phase 6.5: EARS Validation
[ ] Phase 7: Specification Review
[ ] Phase 8: Next Steps Recommendation
[ ] Phase 9: Summary
```

Update the status as you progress through each phase and section.

**CRITICAL**: Phase 1.5 MUST assess scope size before proceeding:
- If scope is too large (>15 estimated tasks), guide user to split into multiple specifications
- Present split options clearly (by domain or by priority)
- If user chooses to split: focus ONLY on first spec, recommend brainstorming for remaining specs
- If user chooses to continue anyway: log warning and note potential rejection by spec-to-tasks

---

**Note**: This command follows a collaborative, iterative approach with specialist agents to ensure designs are:
- Based on actual codebase exploration (not assumptions)
- Well-thought-out and validated incrementally
- Documented professionally with specialist assistance
- Reviewed for quality before proceeding
- Ready for implementation with clear next steps

--- 

## Examples

### Example 1: Simple Feature Idea

```bash
/skill:specs-kit-brainstorm Add user authentication with JWT tokens
```

### Example 2: Complex Feature

```bash
/skill:specs-kit-brainstorm Implement real-time notifications using WebSockets
```

### Example 3: Existing Behavior Change (out of scope)

Brainstorm does not handle changes to existing behavior (e.g., "make the payment processing behavior easier to maintain"). It only produces new functional specifications.

### Example 4: Bug Fix (out of scope)

Brainstorm does not handle bug fixes (e.g., "fix the race condition in order processing"). It only produces new functional specifications.

### Example 5: New Performance Feature

```bash
/skill:specs-kit-brainstorm Design a caching capability to reduce API response times
```

### Example 6: Integration

```bash
/skill:specs-kit-brainstorm Integrate Stripe payment processing for subscriptions
```

### Example 7: ADR-Based Specification

```bash
/skill:specs-kit-brainstorm @docs/adr/039-git-worktree-management.md
```

### Example 8: Full Workflow (after brainstorming)

```bash
# Step 1: Brainstorm and generate functional specification
/skill:specs-kit-brainstorm Design a microservices architecture for the reporting module

# Step 2: Convert specification to tasks
/skill:specs-kit-spec-to-tasks docs/specs/001-reporting-module/

# Step 3: Implement specific tasks
/skill:specs-kit-task-implementation --task="docs/specs/001-reporting-module/tasks/TASK-001.md"
/skill:specs-kit-task-implementation --task="docs/specs/001-reporting-module/tasks/TASK-002.md"
```

This separates WHAT (functional specification) from HOW (implementation), following the "divide et impera" principle.
