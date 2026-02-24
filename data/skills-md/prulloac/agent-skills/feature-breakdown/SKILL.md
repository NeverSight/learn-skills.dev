---
name: feature-breakdown
description: Analyze feature specifications and decompose them into core components, individual tasks, and acceptance criteria. Use when you have a feature spec/idea and need to identify ALL the work required, define what success looks like, and create validation approaches. Focus on WHAT needs building and HOW to verify it's correct (not scheduling or timelines).
---

# Feature Breakdown Skill

**Answers the question: WHAT needs to be built and HOW do we know it works?**

This skill focuses on **decomposition and validation**, not scheduling or timelines.

## When to Use

Use this skill when you have a **feature specification or idea** and need to:
- Identify ALL the work required (no task left behind)
- Define what "done" looks like (acceptance criteria)
- Map component dependencies and relationships
- Create validation and testing strategies
- Know if the feature scope is realistic

**Key indicator**: You're asking "WHAT needs to be built?" and "HOW do we know it works?"

**Do NOT use this skill if**: You already have a feature breakdown and need to create a schedule/timeline (use feature-planning instead)

## Before You Start

Ensure you have:

1. A complete feature specification (or a clear description of what needs to be built)
2. Understanding of the codebase architecture
3. Clarity on technical constraints and dependencies

## Inputs

- Feature specification (provided by user or existing spec file)
- Optional: Project context, technical architecture details, team constraints

## Workflow Overview

The feature breakdown process transforms a specification into an executable implementation plan through these phases:

```
Specification Input
    ↓
Parse & Validate Spec
    ↓
Identify Components & Dependencies
    ↓
Break Into Implementation Tasks
    ↓
Define Acceptance Criteria
    ↓
Create Validation Plan
    ↓
Generate Completion Checklist
    ↓
Write Output File: docs/features/[feature-name]/breakdown.md
     ↓
Structured Implementation Plan (Ready for Team)
```

## Output Files

**MANDATORY FILE ORGANIZATION**: All feature files must be in `docs/features/<feature-name>/` subdirectory.

When this skill completes, it creates:

1. **Feature Breakdown Plan** (`docs/features/[feature-name]/breakdown.md`)
   - Complete implementation plan with all 8 sections
   - Contains tasks, acceptance criteria, dependencies, and completion checklist
   - Ready to share with team and track implementation progress
   - **Example**: `docs/features/user-authentication/breakdown.md`

2. **Optional: Validation Checklist** (`docs/features/[feature-name]/breakdown-validation.md`)
   - Used during execution to validate plan quality
   - Can be kept for reference or discarded after validation passes
   - **Example**: `docs/features/user-authentication/breakdown-validation.md`

The primary deliverable is the feature breakdown markdown file containing the complete plan.

## Core Workflow

### Phase 1: Parse and Validate Specification

**Input**: Feature specification (user-provided or file path)

1. **Extract specification information**:
   - Read and analyze the specification thoroughly
   - Document key requirements from the specification
   - Identify user scenarios and use cases
   - Extract functional and non-functional requirements
   - Note any constraints, dependencies, or assumptions

2. **Validate specification quality**:
   - Confirm specification includes all mandatory sections (user scenarios, functional requirements, success criteria)
   - Check that requirements are clear and testable
   - Identify any vague or conflicting requirements
   - If specification is incomplete, ask for clarification rather than proceeding with incomplete information

3. **Document specification insights**:
   - Create a brief summary of what needs to be built
   - List key technical areas that need implementation
   - Identify potential complexity areas and risks

### Phase 2: Identify Components and Dependencies

1. **Map feature components**:
   - Break the feature into logical components (e.g., backend service, database schema, frontend UI, API endpoints)
   - For each component, identify:
     - Primary responsibility
     - Integration points with other components
     - External dependencies (libraries, services, APIs)
     - Data models or schema involved

2. **Identify dependencies**:
   - List sequential dependencies (what must be done first)
   - Identify parallel work that can happen simultaneously
   - Note any blockers or prerequisite work
   - Document infrastructure requirements

3. **Create component diagram** (text-based):
   - Show relationships between components
   - Highlight data flows
   - Indicate external dependencies

### Phase 3: Break Into Implementation Tasks

Transform requirements into concrete, actionable implementation tasks. Each task should be:
- **Specific**: Clear about what will be implemented
- **Testable**: Includes acceptance criteria
- **Sized appropriately**: Completable in a reasonable timeframe (1-3 days of work typically)
- **Ordered logically**: Respecting dependencies

**Task structure**:

```markdown
## Task [N]: [Task Title]

**Component**: [Which component(s) this affects]

**Description**: [What needs to be implemented]

**Dependencies**: [List prerequisite tasks]

**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

**Implementation Notes**: [Technical considerations, architectural patterns, etc.]

**Estimated Effort**: [Small/Medium/Large - based on complexity]
```

**Task organization principles**:

1. **Group related work**: Tasks affecting the same component should be adjacent
2. **Respect dependencies**: Foundation tasks before features that depend on them
3. **Enable parallelization**: Independent tasks can be started simultaneously
4. **Balance task size**: Avoid tasks that are too large (>3 days) or trivial (<2 hours)

**Common task categories** (adapt to your feature):

- **Data Model/Schema Tasks**: Database schema, data migrations, entity definitions
- **API/Service Tasks**: API endpoints, service methods, business logic
- **Integration Tasks**: Third-party integrations, external API consumption
- **UI/UX Tasks**: UI components, user interactions, forms, displays
- **Testing Tasks**: Unit tests, integration tests, end-to-end tests
- **Validation Tasks**: Feature validation against requirements, performance testing
- **Documentation Tasks**: API documentation, architecture documentation, user guides
- **DevOps/Infrastructure Tasks**: Deployment configuration, environment setup

### Phase 4: Define Acceptance Criteria

For each task, establish clear acceptance criteria that are:

- **Objectively verifiable**: Can be tested and validated without ambiguity
- **Behavior-focused**: Describe what the code should do, not how it's implemented
- **Testable**: Can be verified through automated tests, manual testing, or code review
- **Independent**: Each criterion stands alone and can be verified independently

**Acceptance criteria should answer**: "How will we know this task is complete?"

**Example acceptance criteria**:

❌ Bad: "API endpoint is implemented"
✅ Good: "GET /users/:id returns user profile data with status 200 when user exists; returns 404 when user doesn't exist"

❌ Bad: "UI is responsive"
✅ Good: "Dashboard layout adapts properly on mobile (< 600px width), tablet (600-1024px), and desktop (> 1024px)"

### Phase 5: Create Validation Plan

Define how each requirement from the specification will be validated:

1. **Requirement-to-Task Traceability**: Map each spec requirement to one or more tasks that fulfill it
2. **Validation Methods**: For each requirement, specify how it will be validated:
   - Unit tests
   - Integration tests
   - End-to-end tests
   - Manual testing scenarios
   - Performance benchmarks
   - User acceptance testing

3. **Validation Checklist** (see templates/validation-checklist.md):
   - Lists all spec requirements
   - Maps to corresponding tasks
   - Documents validation method for each
   - Tracks validation status

### Phase 6: Generate Completion Checklist and Create Output File

Create a comprehensive checklist that defines what "done" means, then write the complete plan to a markdown file.

**Completion Checklist Structure**:

```markdown
# Feature Completion Checklist: [Feature Name]

## Implementation Complete
- [ ] All tasks in the implementation plan are complete
- [ ] Code changes merged to main branch
- [ ] No breaking changes to existing APIs (or properly documented)

## Quality Assurance
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] Code review approved
- [ ] No console errors or warnings in production build
- [ ] Performance benchmarks meet success criteria

## Requirement Validation
- [ ] All functional requirements implemented and tested
- [ ] All non-functional requirements met (performance, security, etc.)
- [ ] All user scenarios validated
- [ ] Success criteria from spec are met

## Documentation
- [ ] API documentation updated (if applicable)
- [ ] Internal documentation updated
- [ ] Architecture decisions documented
- [ ] Deployment notes documented

## Pre-Release
- [ ] Tested in staging environment
- [ ] Security review completed (if needed)
- [ ] Accessibility requirements verified
- [ ] Browser/device compatibility verified

## Deployment & Monitoring
- [ ] Deployed to production
- [ ] Feature flags working correctly (if applicable)
- [ ] Monitoring and alerts in place
- [ ] No critical issues in production
- [ ] Success metrics being tracked

## Post-Release
- [ ] User documentation/help updated
- [ ] Release notes published
- [ ] Stakeholders notified
- [ ] Metrics reviewed (if applicable)
```

**File Creation**:
After creating all sections above, write the complete implementation plan to a markdown file:

- **File path**: `docs/features/[feature-name]/breakdown.md`
  - Replace `[feature-name]` with a kebab-case version of the feature name
  - Create directory if it doesn't exist: `mkdir -p docs/features/[feature-name]`
  - Example: "user-authentication" → `docs/features/user-authentication/breakdown.md`
  - Example: "payment-processing" → `docs/features/payment-processing/breakdown.md`
  - **MANDATORY**: All feature files must be in this directory to maintain organization

- **File format**: Markdown with clear section headings
- **Include all 8 sections** from the output format listed below
- **Save to repository** so team members can access and reference during implementation

## Output Format

Generate a comprehensive implementation plan document with these sections:

### 1. Executive Summary
- Brief feature overview
- Key objectives
- Expected impact
- Success criteria

### 2. Component Architecture
- Component diagram (text-based ASCII or description)
- Component descriptions
- Integration points
- External dependencies

### 3. Implementation Tasks
- Organized list of all tasks (using structure from Phase 3)
- Task numbering and sequencing
- Dependency graph
- Parallelization opportunities identified

### 4. Acceptance Criteria Reference
- Quick lookup table mapping tasks to their acceptance criteria
- Helps validate work completion

### 5. Validation Plan
- Requirement-to-task traceability matrix
- Validation methods for each requirement
- Testing strategy
- Validation checklist

### 6. Completion Criteria
- Comprehensive checklist for feature completion
- Quality gates and checkpoints
- Sign-off requirements

### 7. Risk & Mitigation
- Identified risks or complexity areas
- Suggested mitigation approaches
- Fallback plans for critical items

### 8. Next Steps
- Instructions for implementation
- How to update plan as work progresses
- How to track completion

## Guidelines

### Task Sizing
- **Small** (1-2 days): Straightforward implementation, limited scope
- **Medium** (2-3 days): Moderate complexity, multiple integration points
- **Large** (3+ days): Complex implementation, should potentially be split

*Note*: If a task is estimated "Large," consider breaking it into smaller tasks.

### Acceptance Criteria Quality
- Each task should have 2-5 acceptance criteria
- Criteria should be specific, not vague
- Avoid implementation details; focus on behavior/outcomes
- Make sure criteria are independently verifiable

### Dependency Management
- Use sequential numbering to show natural order
- Mark truly parallel work clearly
- Identify critical path items
- Document blocked tasks and their blockers

### Staying Spec-Aligned
- Every task should trace back to a specification requirement
- If a task doesn't map to the spec, question whether it's needed
- If a spec requirement isn't covered, add a task or clarify why it's not needed

## Common Pitfalls to Avoid

❌ **Too detailed too soon**: Don't design implementation details; focus on "what" not "how"

❌ **Missing acceptance criteria**: Every task needs clear verification points

❌ **Ignoring dependencies**: Don't schedule work that depends on incomplete tasks

❌ **Vague requirements**: "Make it better" isn't a requirement; "Reduce load time by 40%" is

❌ **Over-scoping**: Keep tasks to reasonable size; don't try to batch too much work

❌ **Incomplete validation planning**: Don't assume testing; explicitly plan how requirements are validated

## Outputs and Deliverables

### Primary Output: Feature Breakdown Plan

**File**: `docs/features/[feature-name]-breakdown.md`

**Format**: Markdown document with 8 sections:

1. **Executive Summary**
   - Feature overview, objectives, expected impact
   - Success criteria from specification

2. **Component Architecture**
   - Component diagram (text-based ASCII)
   - Component descriptions and responsibilities
   - Integration points and data flows
   - External dependencies

3. **Implementation Tasks**
   - Ordered list of 10-40 concrete tasks
   - Each task with component, description, dependencies
   - Acceptance criteria for each task (2-5 per task)
   - Effort estimates (Small/Medium/Large)
   - Implementation notes and technical considerations

4. **Acceptance Criteria Reference**
   - Quick lookup table mapping tasks to criteria
   - Helps verify work completion

5. **Validation Plan**
   - Requirement-to-task traceability matrix
   - Validation methods for each specification requirement
   - Testing strategy (unit, integration, E2E, security)
   - Validation checklist

6. **Completion Criteria**
   - Comprehensive checklist defining "done"
   - Covers implementation, testing, documentation, deployment
   - Quality gates and sign-off requirements

7. **Risk & Mitigation**
   - Identified technical and project risks
   - Probability and impact assessment
   - Mitigation strategies for each risk
   - Fallback plans for critical items

8. **Next Steps**
   - Instructions for implementing the plan
   - How to track progress
   - How to update the plan during execution

**File Size**: Typically 3,000-8,000 words depending on feature complexity

### Secondary Output: Validation Checklist (optional)

**File**: `docs/features/[feature-name]-validation.md` (optional, can be deleted after validation)

**Purpose**: Quality validation performed during skill execution

**Contents**:
- Plan structure verification
- Task quality checks
- Acceptance criteria validation
- Traceability verification

### Using the Outputs

**For Implementation Teams**:
- Use the breakdown plan as the authoritative source for feature scope
- Reference tasks for sprint planning and assignment
- Track completion using the completion checklist

**For Project Management**:
- Use effort estimates for capacity planning
- Monitor progress against task list
- Reference success criteria for stakeholder communication

**For QA/Testing**:
- Use acceptance criteria for test case creation
- Reference validation plan for testing strategy
- Track requirement coverage

**For Leadership/Stakeholders**:
- Review executive summary for high-level overview
- Track progress through completion checklist
- Reference success criteria for release readiness

## See Also

For reference materials on how to use this skill effectively, see the included reference documents in the skill's `references/` directory.

## Example: Feature Breakdown Output

For a real example of how this output looks, see: `references/example-feature-breakdown.md`
