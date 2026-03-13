---
name: project-planning
description: Create structured project planning documents for new software projects, features, or initiatives. Use when starting a new project and need to generate specifications, implementation plans, and task breakdowns that AI coding agents can use to write code. Outputs include project spec, implementation phases, and a current/next steps task list.
---

# Project Planning Skill

Help developers create comprehensive project planning documents by gathering requirements, asking clarifying questions, and generating structured specifications that AI coding agents can use for implementation.

## Information Gathering Phase

Before creating any documents, you MUST gather all necessary information. Ask questions conversationally, grouping related questions together. Do not overwhelm the user with all questions at once.

### Required Information Checklist

#### Project Vision
- [ ] Project name or working title
- [ ] One-sentence description of what you're building
- [ ] The problem being solved (why does this need to exist?)
- [ ] Target users (who will use this?)
- [ ] Desired outcomes (what does success look like?)

#### Scope & Requirements
- [ ] Core features (must-have functionality)
- [ ] Nice-to-have features (if time permits)
- [ ] Explicit non-goals (what are we NOT building?)
- [ ] Any existing solutions or alternatives considered

#### Technical Context
- [ ] Is this a new project or addition to existing codebase?
- [ ] If existing: repository location, tech stack, key patterns
- [ ] If new: preferred tech stack, languages, frameworks
- [ ] External dependencies or integrations needed
- [ ] Data storage requirements (database, files, etc.)

#### Constraints
- [ ] Hard constraints (security, compliance, performance)
- [ ] Dependencies on other systems or teams
- [ ] Known technical limitations or risks
- [ ] Budget or resource constraints (if applicable)

#### Success Criteria
- [ ] How will you know when this is complete?
- [ ] Specific acceptance criteria or tests
- [ ] Performance requirements (if any)
- [ ] Quality requirements (test coverage, documentation, etc.)

### Question Strategy

Ask questions in phases based on complexity:

**Phase 1: Vision (Always ask first)**
- What are you trying to build?
- What problem does it solve and for whom?

**Phase 2: Scope (After understanding vision)**
- What are the core features needed for an MVP?
- What is explicitly out of scope?

**Phase 3: Technical (After scope is clear)**
- What's the technical context? (new project vs existing, tech stack)
- Any integrations or dependencies?

**Phase 4: Constraints & Success (Final clarifications)**
- Any hard constraints to be aware of?
- How will we verify success?

See [clarifying-questions.md](references/clarifying-questions.md) for comprehensive question bank by project type.

## Document Generation Phase

After gathering requirements, generate the following documents. Present each document and ask for feedback before proceeding to the next.

### Document 1: PROJECT-SPEC.md

The main specification document. See [document-templates.md](references/document-templates.md) for full template.

```markdown
# [Project Name] Specification

## Overview
**Project:** [Name]
**Status:** Planning
**Last Updated:** [Date]

### Problem Statement
[What problem are we solving? Why does this matter?]

### Target Users
[Who will use this? What are their needs?]

### Success Criteria
[How will we know this is successful? Be specific and measurable.]

## Requirements

### Core Requirements (Must Have)
1. [Requirement 1]
   - Acceptance: [How to verify]
2. [Requirement 2]
   - Acceptance: [How to verify]

### Secondary Requirements (Should Have)
1. [Requirement]

### Non-Goals (Explicitly Out of Scope)
- [Thing we are NOT building]
- [Another thing out of scope]

## Technical Context

### Tech Stack
- **Language:** [e.g., TypeScript]
- **Framework:** [e.g., React 18, Next.js 14]
- **Database:** [e.g., PostgreSQL]
- **Key Dependencies:** [List major libraries]

### Architecture Overview
[Brief description of system architecture]

### Integration Points
- [External system 1]: [How we integrate]
- [External system 2]: [How we integrate]

## Constraints

### Technical Constraints
- [Constraint 1]

### Security Requirements
- [Requirement 1]

### Performance Requirements
- [Requirement 1]

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [How to mitigate] |

## Open Questions
- [ ] [Question that needs resolution]
```

### Document 2: IMPLEMENTATION-PLAN.md

Phased implementation plan with task breakdowns.

```markdown
# [Project Name] Implementation Plan

## Overview
This document outlines the implementation phases and tasks for [Project Name].

**Estimated Phases:** [N]
**MVP Phase:** [Which phase delivers MVP]

## Phase 1: [Phase Name] (Foundation)

### Objective
[What this phase accomplishes]

### Prerequisites
- [What must be true before starting]

### Tasks

#### 1.1 [Task Name]
- **Description:** [What needs to be done]
- **Files:** [Files to create/modify]
- **Acceptance:** [How to verify completion]
- **Dependencies:** None

#### 1.2 [Task Name]
- **Description:** [What needs to be done]
- **Files:** [Files to create/modify]
- **Acceptance:** [How to verify completion]
- **Dependencies:** Task 1.1

### Phase 1 Deliverables
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]

### Phase 1 Verification
```bash
# Commands to verify phase completion
npm test
npm run build
```

## Phase 2: [Phase Name] (Core Features)

[Repeat structure...]

## Phase N: [Phase Name] (Polish & Launch)

[Repeat structure...]

## Dependency Graph

```
Phase 1 ──→ Phase 2 ──→ Phase 3
                 ↘        ↗
                  Phase 2b
```

## Technical Decisions Log

| Decision | Options Considered | Choice | Rationale |
|----------|-------------------|--------|-----------|
| [Decision] | [Option A, B, C] | [Choice] | [Why] |
```

### Document 3: TASKS.md

Current and next steps for AI agents to execute.

```markdown
# [Project Name] Task Tracker

## Current Status
**Phase:** [Current Phase]
**Last Updated:** [Date]
**Next Action:** [Brief description]

---

## Active Tasks (In Progress)

### [ ] [Task ID]: [Task Name]
**Phase:** [Phase Number]
**Priority:** High/Medium/Low
**Status:** In Progress

**Context:**
[Why this task exists, what it accomplishes]

**Implementation Steps:**
1. [ ] [Specific step 1]
2. [ ] [Specific step 2]
3. [ ] [Specific step 3]

**Files to Modify:**
- `path/to/file.ts` - [What to change]
- `path/to/other.ts` - [What to change]

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Verification:**
```bash
# How to verify this task is complete
npm test path/to/test
```

---

## Next Tasks (Ready to Start)

### [ ] [Task ID]: [Task Name]
**Phase:** [Phase Number]
**Priority:** High/Medium/Low
**Blocked By:** None

**Context:**
[Brief context]

**Implementation Steps:**
1. [ ] [Step 1]
2. [ ] [Step 2]

---

## Backlog (Future Tasks)

### [ ] [Task ID]: [Task Name]
**Phase:** [Phase Number]
**Blocked By:** [Task ID]

---

## Completed Tasks

### [x] [Task ID]: [Task Name]
**Completed:** [Date]
**Notes:** [Any relevant notes]
```

## Output Guidelines

### For AI Agent Consumption

The generated documents must be optimized for AI coding agents:

1. **Be Specific About Tech Stack**
   - Include exact versions: "React 18.2 with TypeScript 5.0"
   - List all key dependencies
   - Specify coding conventions

2. **Make Tasks Actionable**
   - Each task should be completable in a single session
   - Include specific file paths when known
   - Provide verification commands

3. **Include Context at Every Level**
   - Why does this task exist?
   - What patterns should be followed?
   - What files are related?

4. **Use Checklists for Progress**
   - AI agents can update checkboxes as they complete work
   - Human reviewers can quickly see status

5. **Specify Non-Goals Clearly**
   - Prevents scope creep
   - AI agents won't add unrequested features

### Document Formatting

- Use Markdown with clear headings
- Include code blocks for commands and examples
- Use tables for structured comparisons
- Keep sections focused and scannable
- Include verification steps that can be run

## Iteration & Updates

After generating initial documents:

1. **Review with User**
   - Present each document section by section
   - Ask for feedback and corrections
   - Clarify any assumptions made

2. **Refine Based on Feedback**
   - Update documents with corrections
   - Add missing details
   - Remove irrelevant sections

3. **Establish Update Cadence**
   - TASKS.md: Update after each completed task
   - IMPLEMENTATION-PLAN.md: Update after each phase
   - PROJECT-SPEC.md: Update when requirements change

## Wrap Up

After generating all documents, offer:

1. **Review & Refinement**: Go through each document section by section
2. **Priority Adjustment**: Reorder tasks based on dependencies or preferences
3. **Scope Negotiation**: Adjust scope if project seems too large for available time
4. **First Task Kickoff**: Begin implementing the first task immediately
5. **Export Options**: Save documents to specific locations in the codebase
