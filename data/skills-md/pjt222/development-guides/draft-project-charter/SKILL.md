---
name: draft-project-charter
description: >
  Draft a project charter that defines scope, stakeholders, success criteria,
  and initial risk register. Covers problem statement, RACI matrix, milestone
  planning, and scope boundaries for both agile and classic methodologies.
  Use when kicking off a new project or initiative, formalizing scope after
  an informal start, aligning stakeholders before detailed planning begins,
  or transitioning from discovery to active project work.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: project-management
  complexity: basic
  language: multi
  tags: project-management, charter, scope, stakeholders, raci, risk-register
---

# Draft a Project Charter

Creates a structured project charter that establishes project boundaries, stakeholder agreements, and success criteria before detailed planning begins. Produces a comprehensive document covering scope, RACI assignments, milestone planning, and an initial risk register suitable for agile, classic, or hybrid project methodologies.

## When to Use

- Kicking off a new project or initiative
- Formalizing scope after an informal project start
- Aligning stakeholders before detailed planning begins
- Creating a reference document for scope decisions during execution
- Transitioning from discovery/ideation to active project work

## Inputs

- **Required**: Project name and brief description
- **Required**: Primary stakeholder or sponsor
- **Optional**: Existing documentation (proposals, briefs, emails)
- **Optional**: Known constraints (budget, deadline, team size)
- **Optional**: Methodology preference (agile, classic, hybrid)

## Procedure

### Step 1: Gather Project Context and Create Charter Template

Read any existing documentation (proposals, emails, briefs) to understand the project background. Identify the core problem or opportunity the project addresses. Create the charter file with a structured template that will be populated in subsequent steps.

Create a file named `PROJECT-CHARTER-[PROJECT-NAME].md` with this template:

```markdown
# Project Charter: [Project Name]
## Document ID: PC-[PROJECT]-[YYYY]-[NNN]

### 1. Problem Statement
[2-3 sentences describing the problem or opportunity this project addresses]

### 2. Project Purpose
[What the project will achieve and why it matters]

### 3. Scope
#### In Scope
- [Deliverable 1]
- [Deliverable 2]

#### Out of Scope
- [Exclusion 1]
- [Exclusion 2]

### 4. Deliverables
| # | Deliverable | Acceptance Criteria | Target Date |
|---|------------|---------------------|-------------|
| 1 | | | |

### 5. Stakeholders & RACI
| Stakeholder | Role | D1 | D2 | D3 |
|-------------|------|----|----|-----|
| | | | | |

*R=Responsible, A=Accountable, C=Consulted, I=Informed*

### 6. Success Criteria
| # | Criterion | Measure | Target |
|---|-----------|---------|--------|
| 1 | | | |

### 7. Milestones
| Milestone | Target Date | Dependencies |
|-----------|-------------|--------------|
| | | |

### 8. Risk Register
| ID | Risk | Likelihood | Impact | Severity | Mitigation | Owner |
|----|------|------------|--------|----------|------------|-------|
| R1 | | | | | | |

*Likelihood/Impact: Low, Medium, High*
*Severity = Likelihood × Impact*

### 9. Assumptions and Constraints
#### Assumptions
- [Key assumption 1]

#### Constraints
- [Key constraint 1]

### 10. Approval
| Role | Name | Date |
|------|------|------|
| Sponsor | | |
| Project Lead | | |
```

Fill in the document ID using format PC-[PROJECT]-[YYYY]-[NNN] (e.g., PC-WEBSITE-2026-001). Write a problem statement (2-3 sentences) that describes the current situation, the gap, and the impact. Write a project purpose statement (1 paragraph) explaining what will be achieved.

**Expected:** Charter file created with document ID, problem statement, and purpose filled in. Problem statement is specific and describes a measurable gap.

**On failure:** If project context is unclear, document specific questions for the sponsor in a QUESTIONS section at the top of the charter. If existing docs conflict, note contradictions in an OPEN ISSUES section and flag for stakeholder resolution.

### Step 2: Define Scope Boundaries

Create explicit lists of what is and is not included in the project scope. Write 3-5 in-scope deliverables with specific acceptance criteria for each. Write 3-5 out-of-scope items to prevent scope creep. Populate the Deliverables table with each deliverable, its acceptance criteria, and a target date.

**Expected:** Scope section has balanced in-scope and out-of-scope lists. Deliverables table contains 3-5 entries with specific, testable acceptance criteria. Target dates are realistic and sequenced logically.

**On failure:** If deliverables are vague, break down each into sub-deliverables with concrete outputs. If acceptance criteria are missing, ask: "How would we demonstrate this deliverable is complete?" If target dates are unavailable, mark as TBD and flag for milestone planning session.

### Step 3: Identify Stakeholders and Assign RACI

List all individuals or groups who will be affected by, contribute to, or have decision authority over the project. Include their organizational role. Create a RACI matrix mapping each stakeholder to each deliverable using:
- **R** (Responsible): Does the work
- **A** (Accountable): Final decision authority (only one A per deliverable)
- **C** (Consulted): Provides input before decisions
- **I** (Informed): Kept updated on progress

Ensure each deliverable has exactly one A and at least one R.

**Expected:** Stakeholders table lists 5-10 people with their roles. RACI matrix has one A per deliverable column. No deliverable is missing an R or has multiple As. Sponsor is A for final approval.

**On failure:** If stakeholder list is incomplete, cross-reference with organization chart and meeting attendees from discovery phase. If multiple As are identified, escalate the conflict to the sponsor for decision authority clarification. If no R exists, flag deliverable as unassigned and requiring resource allocation.

### Step 4: Define Success Criteria and Milestones

Write 3-5 measurable success criteria using SMART format (Specific, Measurable, Achievable, Relevant, Time-bound). Each criterion should tie to a quantifiable measure and target value. Define 4-6 key milestones representing major project stages or deliverable completions, with target dates and dependencies on prior milestones.

**Expected:** Success Criteria table has 3-5 entries with specific measures (e.g., "System uptime" measured as "% availability" with target "99.5%"). Milestones table shows logical project phases with realistic target dates. Dependencies are clearly noted.

**On failure:** If success criteria are vague (e.g., "improve quality"), rewrite as measurable outcomes with baseline and target values. If milestone dates are unrealistic, work backward from final deadline using estimated durations and buffers. If dependencies create circular logic, restructure milestone sequence or split conflicting milestones.

### Step 5: Create Initial Risk Register

Identify 5-10 risks that could impact project success. For each risk, assess likelihood (Low/Medium/High) and impact (Low/Medium/High), then calculate severity. Define a specific mitigation strategy for each risk and assign a risk owner responsible for monitoring and response. Include at least one risk in each category: scope, schedule, resource, technical, and external.

**Expected:** Risk Register has 5-10 entries covering scope, schedule, resource, technical, and external risks. Each risk has likelihood, impact, and severity assessed. Mitigation strategies are actionable and specific. Each risk has an assigned owner.

**On failure:** If risk list is incomplete, review scope boundaries, dependencies, stakeholder list, and assumptions for potential failure points. If mitigation strategies are generic ("monitor closely"), specify: What will be monitored? How often? What triggers action? If no one accepts risk ownership, assign to project lead temporarily and escalate to sponsor.

## Validation

- [ ] Charter file created with document ID
- [ ] Problem statement is specific and measurable
- [ ] Scope has both in-scope and out-of-scope items
- [ ] RACI matrix covers all deliverables
- [ ] Success criteria are measurable (SMART)
- [ ] At least 5 risks identified with mitigation strategies
- [ ] Milestones have target dates
- [ ] Approval section included

## Common Pitfalls

- **Scope without boundaries**: Listing in-scope items without explicit out-of-scope items leads to scope creep. Always define what you won't do.
- **Vague success criteria**: "Improve performance" is unmeasurable. Tie every criterion to a number with a baseline and target.
- **Missing stakeholders**: Overlooked stakeholders surface late and derail the project. Cross-reference org charts and prior project communications.
- **Risk register as checkbox**: Listing risks without actionable mitigation plans provides false confidence. Each risk needs a specific response strategy.
- **Over-detailed charter**: The charter is a compass, not a map. Keep it to 2-4 pages. Detailed planning happens later.

## Related Skills

- `create-work-breakdown-structure` — decompose charter deliverables into work packages
- `manage-backlog` — translate charter scope into a prioritized backlog
- `plan-sprint` — plan the first sprint from charter deliverables
- `generate-status-report` — report progress against charter milestones
- `conduct-retrospective` — review charter assumptions after execution
