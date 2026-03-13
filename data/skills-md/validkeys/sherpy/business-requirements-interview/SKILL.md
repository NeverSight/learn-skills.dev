---
name: business-requirements-interview
description: Conducts structured interviews to gather comprehensive business requirements. Asks one question at a time with multiple-choice options, tracks progress in JSONL format, and generates structured business-requirements.yaml output. Use when starting a new project or feature to ensure clear understanding of goals, scope, users, and success criteria.
---

# Business Requirements Interview

This skill guides you through a structured interview process to gather comprehensive business requirements for a software project.

## Interview Process

### Rules

1. **One question at a time** - Never ask multiple questions in a single turn
2. **Provide options** - Each question includes 2-5 recommended options plus free-form input
3. **Track progress** - All Q&A pairs are immediately appended to `business-interview.jsonl`
4. **Resume capability** - If JSONL exists, continue from last question
5. **Structured output** - Generate `business-requirements.yaml` upon completion

### Interview Categories

The interview covers these areas in order:

1. **Problem Definition & Scope**

   - What problem are you solving?
   - What's the core value proposition?
   - What's in scope vs out of scope?

2. **User Personas & Use Cases**

   - Who are the primary users?
   - What are their goals?
   - What are their pain points?

3. **Success Criteria & Metrics**

   - How will you measure success?
   - What are the key outcomes?
   - What metrics matter?

4. **Constraints & Dependencies**

   - Technical constraints?
   - Business constraints?
   - Timeline constraints?
   - External dependencies?

5. **Priority & Timeline**
   - What's the MVP scope?
   - What's the timeline?
   - What's the priority order?

## Question Format

Each question follows this structure:

```
## [Category Name]

**Question:** [Clear, specific question]

**Options:**
1. [Option 1] (Recommended) - [Brief description of this approach]
2. [Option 2] - [Brief description]
3. [Option 3] - [Brief description]
4. Type your own answer
```

## Example Questions

### Problem Definition

```
## Problem Definition

**Question:** What is the primary problem your project aims to solve?

**Options:**
1. Automate manual workflow (Recommended) - Replace time-consuming manual processes with automated workflows
2. Improve existing solution - Enhance or replace current tooling that's inadequate
3. New capability - Build something entirely new that doesn't exist yet
4. Type your own answer
```

### User Personas

```
## User Personas

**Question:** Who are your primary target users?

**Options:**
1. Individual developers (Recommended) - Solo developers working on personal or small projects
2. Development teams - Small to medium teams collaborating on shared codebases
3. Enterprise organizations - Large teams with complex workflows and compliance needs
4. End users (non-technical) - Users who interact with the product but don't write code
5. Type your own answer
```

### Scope Definition

```
## Scope Definition

**Question:** What is the initial scope for this project?

**Options:**
1. MVP/Proof of concept (Recommended) - Minimal viable product to validate core assumptions
2. Full-featured release - Complete implementation of all planned features
3. Iterative enhancement - Start with core features, expand over time
4. Type your own answer
```

## JSONL Format

Track all questions and answers in `business-interview.jsonl`:

```json
{"id":1,"category":"Problem Definition","question":"What is the primary problem your project aims to solve?","answer":"Automate manual workflow - Replace time-consuming manual processes with automated workflows","timestamp":"2025-01-27T10:00:00Z"}
{"id":2,"category":"User Personas","question":"Who are your primary target users?","answer":"Individual developers - Solo developers working on personal or small projects","timestamp":"2025-01-27T10:05:00Z"}
```

## Output Format

Generate `business-requirements.yaml` with this structure:

```yaml
project: [project-name]
version: "1.0.0"
generated: [timestamp]

overview:
  problem: |
    [Problem description]
  value_proposition: |
    [Core value being delivered]
  scope:
    in_scope:
      - [Item 1]
      - [Item 2]
    out_of_scope:
      - [Item 1]
      - [Item 2]

personas:
  - name: [Persona Name]
    description: [Who they are]
    goals:
      - [Goal 1]
      - [Goal 2]
    pain_points:
      - [Pain point 1]
      - [Pain point 2]

use_cases:
  - name: [Use Case Name]
    actor: [Who performs it]
    description: [What they do]
    outcome: [What they achieve]

functional_requirements:
  - id: FR-1
    category: [Category]
    description: [Requirement description]
    priority: [high/medium/low]
    rationale: [Why this is needed]

non_functional_requirements:
  performance:
    - [Performance requirement 1]
  security:
    - [Security requirement 1]
  usability:
    - [Usability requirement 1]
  reliability:
    - [Reliability requirement 1]

success_criteria:
  - criterion: [Success criterion]
    metric: [How to measure]
    target: [Target value]

constraints:
  technical:
    - [Technical constraint 1]
  business:
    - [Business constraint 1]
  timeline:
    - [Timeline constraint 1]
  budget:
    - [Budget constraint 1]

dependencies:
  internal:
    - [Internal dependency 1]
  external:
    - [External dependency 1]

timeline:
  phase: [Phase name]
  duration: [Duration]
  milestones:
    - [Milestone 1]
    - [Milestone 2]

assumptions:
  - [Assumption 1]
  - [Assumption 2]

risks:
  - risk: [Risk description]
    probability: [high/medium/low]
    impact: [high/medium/low]
    mitigation: [Mitigation strategy]
```

## Usage

To start a new interview:

```
/business-requirements-interview
```

To resume an existing interview (if `business-interview.jsonl` exists):

```
/business-requirements-interview
```

The skill will automatically:

1. Check for existing `business-interview.jsonl`
2. Resume from the last question if found
3. Continue asking questions until complete
4. Generate `business-requirements.yaml` when finished

## Best Practices

1. **Be specific** - Provide detailed answers when using free-form input
2. **Think broadly** - Consider edge cases and future needs
3. **Prioritize ruthlessly** - Not everything can be in MVP
4. **Document assumptions** - Make implicit assumptions explicit
5. **Consider constraints** - Be realistic about technical and business limitations

## Review & Gap Analysis

After generating `business-requirements.yaml`, automatically perform a gap analysis:

### Completeness Check

**Overview Section:**

- [ ] Problem statement is clear and specific
- [ ] Value proposition explains the "why"
- [ ] Scope clearly defines in/out of scope items
- [ ] Scope is realistic for the timeline

**Personas:**

- [ ] All user types are represented
- [ ] Each persona has clear goals
- [ ] Pain points are specific, not generic
- [ ] Personas are distinct (not overlapping)

**Requirements:**

- [ ] Functional requirements are testable
- [ ] Priority is assigned to each requirement
- [ ] Rationale explains why each requirement exists
- [ ] No duplicate or conflicting requirements

**Non-Functional Requirements:**

- [ ] Performance targets are measurable
- [ ] Security requirements address key risks
- [ ] Usability requirements are specific
- [ ] Reliability requirements are realistic

**Success Criteria:**

- [ ] Each criterion has a metric
- [ ] Targets are achievable and measurable
- [ ] Criteria align with business goals

**Constraints:**

- [ ] Technical constraints are realistic
- [ ] Business constraints are acknowledged
- [ ] Timeline is feasible
- [ ] Budget constraints are explicit

**Dependencies:**

- [ ] Internal dependencies identified
- [ ] External dependencies documented
- [ ] Critical path dependencies noted

### Consistency Check

- [ ] No contradictions between requirements
- [ ] Priorities align with scope
- [ ] Timeline aligns with requirements complexity
- [ ] Success criteria align with scope

### Gap Identification

**Common Gaps to Check:**

- Missing edge cases in requirements
- Unstated assumptions about users
- Implicit constraints not documented
- Missing error handling scenarios
- Unclear success/failure criteria
- Missing integration points
- Undocumented business rules

### Review Output

Generate a gap analysis report with:

```yaml
gap_analysis:
  completeness_score: [1-10]
  consistency_score: [1-10]

  gaps_found:
    - category: [category]
      issue: [description]
      severity: [high/medium/low]
      recommendation: [how to address]

  strong_areas:
    - [what's well-defined]

  suggestions:
    - [improvement suggestions]

  ready_for_next_phase: [yes/no/with-modifications]
```

If critical gaps found (severity: high), ask:

> "I've identified some gaps in the business requirements. Would you like to:
>
> 1. Address them now (I'll ask follow-up questions)
> 2. Proceed to technical requirements (address later)
> 3. Review the gaps and decide"

## Next Steps

After completing the business requirements interview and gap analysis:

1. Review gap analysis report
2. Address any critical gaps
3. Use `/technical-requirements-interview` to derive technical specifications
4. Use `/implementation-planner` to generate implementation plans

## Examples

See [examples/](./examples/) for sample output files.
