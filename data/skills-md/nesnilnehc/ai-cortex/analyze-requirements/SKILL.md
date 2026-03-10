---
name: analyze-requirements
description: Transform vague intent into validated, testable requirements through diagnostic state progression and structured dialogue. Use when user has an idea, feature request, or problem statement that needs requirements clarification before design or implementation.
tags: [writing, eng-standards, documentation]
version: 1.0.0
license: MIT
related_skills: [brainstorm-design, refine-skill-design, discover-skills]
recommended_scope: both
metadata:
  author: ai-cortex
  evolution:
    sources:
      - name: "requirements-analysis"
        repo: "https://github.com/jwynia/agent-skills"
        version: "1.0.0"
        license: "MIT"
        type: "fork"
        borrowed: "Diagnostic state model (RA0-RA5), problem-first methodology, anti-patterns, constraint inventory, health check questions"
      - name: "request-analyzer"
        repo: "https://github.com/staruhub/ClaudeSkills"
        version: "1.0.0"
        license: "MIT"
        type: "integration"
        borrowed: "Structured quality assessment (clarity/specificity/completeness), decision matrix, skill coordination pattern"
      - name: "brainstorm-design"
        repo: "nesnilnehc/ai-cortex"
        version: "1.0.0"
        license: "MIT"
        type: "reference"
        borrowed: "Phase-based workflow, HARD-GATE pattern, incremental dialogue approach"
    enhancements:
      - "Unified diagnostic states with structured quality assessment"
      - "Added request triage for quick vs. deep analysis"
      - "Defined clear handoff boundary with brainstorm-design"
      - "Added output persistence with file naming conventions"
      - "Comprehensive self-check aligned with core objective"
triggers: [project start, start project, requirements, analyze requirements]
input_schema:
  type: free-form
  description: Vague idea, feature request, problem statement, or user requirement to analyze
output_schema:
  type: document-artifact
  description: Validated requirements document written to docs/requirements-planning/<topic>.md (docs/requirements/<topic>.md accepted for backward compatibility)
---

# Skill: Analyze Requirements

## Purpose

Diagnose requirements-level problems and transform vague intent into validated, testable requirements. Guide developers from "I want to build X" to a clear problem statement, prioritized needs, explicit constraints, and bounded scope — all before any design or implementation begins.

---

## Core Objective

**Primary Goal**: Produce a validated requirements document where every requirement is testable, scoped, and grounded in a real problem.

**Success Criteria** (ALL must be met):

1. ✅ **Problem articulated**: A clear problem statement exists that does not reference any solution or technology
2. ✅ **Needs are testable**: Every requirement has acceptance criteria or a concrete "done looks like..." description
3. ✅ **Constraints inventoried**: Real constraints (budget, time, skills, dependencies) are separated from assumptions
4. ✅ **Scope bounded**: V1 boundary is explicit with deferred items listed and triggers for reconsidering documented
5. ✅ **User confirmed**: User explicitly approved the validated requirements (said "approved", "looks good", "proceed", or equivalent)
6. ✅ **Document persisted**: Requirements document written to agreed location and committed

**Acceptance Test**: Can someone unfamiliar with the project read the requirements document and understand the problem, who has it, what "done" looks like, and what is out of scope — without asking clarifying questions?

---

## Scope Boundaries

**This skill handles**:

- Vague intent → Validated requirements document
- Problem discovery and articulation
- Need clarification and acceptance criteria writing
- Constraint inventory and assumption mapping
- Scope definition and prioritization (V1 vs. later)
- Requirements quality assessment (clarity, specificity, completeness)

**This skill does NOT handle**:

- Design and architecture decisions (use `brainstorm-design`)
- Implementation planning or task lists (use implementation planning skills)
- Code writing (use development skills)
- Code review (use `review-code`)
- Technology selection (mention constraints, but technology choice belongs to design phase)

**Handoff point**: When requirements are validated (all success criteria met), hand off to `brainstorm-design` for design exploration, or to implementation planning if design is trivial.

---

## Use Cases

- **New project kickoff**: Developer says "I want to build X" — extract the real problem and validated needs before any design.
- **Feature request triage**: Stakeholder submits vague feature request — clarify problem, scope, and acceptance criteria.
- **Scope creep prevention**: Project keeps growing — apply prioritization and explicit V1 boundary.
- **Requirement validation**: Existing requirements feel incomplete — diagnose which state they are in and progress them.
- **Constraint discovery**: Mid-project surprise blockers — surface hidden constraints and assumptions before they derail work.

---

## Behavior

### Interaction Policy

- **Defaults**: Infer current state from input; start from earliest unresolved state
- **Choice options**: One question at a time; offer `[A][B][C]` when possible
- **Confirm**: Before exiting to design handoff; before writing requirements doc

### HARD-GATE: No Design Before Validation

```text
DO NOT propose architecture, choose technologies, create designs,
or write code until requirements are validated.

Requirements describe PROBLEMS and NEEDS, not SOLUTIONS.
If a requirement mentions technology, it is a solution in disguise.
```

### Phase 0: Triage

**Announce at start:** "I'm using the analyze-requirements skill to validate requirements before any design or implementation."

Perform a quick quality assessment of the input:

| Dimension | Score range | What to check |
| :--- | :--- | :--- |
| **Clarity** | 0–100% | Is there a single unambiguous interpretation? Are terms defined? |
| **Specificity** | 0–100% | Is context provided? Are success criteria mentioned? Is scope bounded? |
| **Completeness** | 0–100% | Is all necessary information present? Are constraints mentioned? |

**Decision matrix**:

| Overall score | Action |
| :--- | :--- |
| < 40% | Start from State RA0 (problem discovery) |
| 40–70% | Identify the earliest problem state and start there |
| > 70% | Validate quickly and focus on gaps |

### Phase 1: Diagnose — Identify the Current State

Progress through states sequentially. Do NOT skip states — if the problem is not clear, do not discuss needs.

#### State RA0: No Problem Statement

**Symptoms**: Starting with a solution ("I want to build X"); feature list without problem grounding; "everyone needs this" reasoning; cannot articulate who has what problem.

**Key questions** (ask one at a time):

- "What specific frustration or pain point led to this idea?"
- "What are people (or you) doing today instead?"
- "What happens if this does not exist? Who suffers and how?"
- "If you are the user, what triggered you thinking about this now?"

**Interventions**:

- Problem Statement Brief: capture who has what problem and why it matters
- "Five users" test: name 5 specific people who would benefit (even if one is yourself)
- Jobs-to-be-Done: "When I [situation], I want to [motivation], so I can [outcome]"
- Problem archaeology: trace the origin back to a specific frustration event

**Exit criteria**: A problem statement exists that does not mention any solution or technology.

#### State RA1: Solution-First Thinking

**Symptoms**: Technology choices before problem clarity ("needs a database", "should use React"); requirements describe implementation rather than needs; cannot explain requirements without referencing technology.

**Key questions**:

- "What is the need behind this feature?"
- "If that technology did not exist, what would you still need?"
- "Are you solving YOUR problem or copying someone else's solution?"
- "Is this technology required (constraint) or just familiar (preference)?"

**Interventions**:

- "Remove the solution" exercise: describe the need without ANY implementation words
- Function extraction: rewrite each requirement as "The system must [verb]..." without technology terms
- Constraint vs. preference distinction: separate hard constraints from defaults

**Exit criteria**: Every requirement describes a need, not an implementation. Technology references are either removed or explicitly documented as real constraints.

#### State RA2: Vague Needs

**Symptoms**: Cannot describe what "done" looks like; adjective-based requirements ("fast", "easy", "intuitive"); requirements that cannot be tested; "users should be able to..." without specifics.

**Key questions**:

- "Can you give a specific example scenario?"
- "What would a disappointing implementation look like vs. a great one?"
- "What is the minimum that would satisfy this need?"
- "How would you know if this requirement is met?"

**Interventions**:

- Acceptance scenario writing: "Given [context], when [action], then [outcome]"
- Specificity ladder: who specifically? doing what specifically? when specifically?
- "Done looks like..." exercise: describe the smallest thing that would satisfy
- Testability check: if you cannot write a test for it, you do not understand it yet

**Exit criteria**: Every requirement has acceptance criteria. No adjective-only requirements remain.

#### State RA3: Hidden Constraints

**Symptoms**: Surprise dependencies appearing late; no explicit constraint inventory; assumptions treated as facts; discovering blockers mid-discussion.

**Key questions**:

- "What external dependencies exist?"
- "What resources, skills, and time do you actually have?"
- "What would kill this project if it turned out to be true?"
- "What are you assuming is true that you have not validated?"

**Interventions**:

- Constraint Inventory: list budget, time, skills, dependencies, integrations as **real constraints**
- Assumption mapping: separate validated facts from unvalidated assumptions
- Risk pre-mortem: "It is 6 months later and this failed. Why?"
- Dependency discovery: what must exist before this can work?

**Exit criteria**: A constraint inventory exists with explicit separation of real constraints vs. assumptions.

#### State RA4: Scope Creep

**Symptoms**: Every feature feels equally important; no V1 boundary; "while we are at it..." additions; requirements expanding faster than they are satisfied.

**Key questions**:

- "If you could only ship 3 things, what are they?"
- "What could you cut and still solve the core problem?"
- "What is the smallest useful version?"
- "What triggers reconsidering deferred items?"

**Interventions**:

- Cut-first approach: start with everything out, add back only what is essential
- Force-rank: strict ordering, no ties
- Walking skeleton: identify the thinnest useful version
- MoSCoW: Must / Should / Could / Won't
- Deferred features list with explicit triggers for reconsidering

**Exit criteria**: V1 boundary is explicit. Deferred items are listed with triggers. No ambiguity about what is in scope.

#### State RA5: Requirements Validated

**Indicators**:

- Problem statement exists without solution references
- Every requirement is testable with acceptance criteria
- Constraints are inventoried (real vs. assumed)
- Scope is bounded with explicit V1 definition
- Could explain to someone unfamiliar and have them understand the need

**Next step**: Hand off to `brainstorm-design` with the Validated Requirements Document.

### Phase 2: Validate — Confirm with User

1. **Present the requirements summary** in structured format (see Output section)
2. **Ask for explicit approval**: "Do these requirements accurately capture what you need?"
3. **Iterate if needed**: Return to the relevant state if gaps are found

### Phase 3: Persist — Write the Document

1. **Determine output location**:
   - Default: `docs/requirements-planning/<topic>.md`
   - Compatibility: existing projects using `docs/requirements/<topic>.md` may keep that path temporarily
   - Ask user if a different location is preferred
2. **Write the document** following the output template
3. **Commit to version control**
4. **Announce completion and handoff**

---

## Input & Output

### Input

- **User request**: Vague idea, feature request, problem statement, or existing requirements to validate.
- **Project context**: Existing codebase, documentation, constraints (discovered during exploration).
- **User responses**: Answers to diagnostic questions, feedback on assessments, approval of validated requirements.

### Output

#### Validated Requirements Document

```markdown
# [Topic] Requirements

**Date:** YYYY-MM-DD
**Status:** Validated
**Approved by:** [User name or "User"]

## Problem Statement

[Who has what problem and why it matters. No solution or technology references.]

## Need Hierarchy

### Must Have (V1)

| ID | Need | Acceptance Criteria |
| :--- | :--- | :--- |
| R-01 | [Testable need] | Given [X], when [Y], then [Z] |
| R-02 | [Testable need] | [Measurable criterion] |

### Should Have (V1 if time permits)

| ID | Need | Acceptance Criteria |
| :--- | :--- | :--- |
| R-03 | [Testable need] | [Criterion] |

### Could Have (Post-V1)

| ID | Need | Trigger to reconsider |
| :--- | :--- | :--- |
| R-04 | [Deferred need] | [When to revisit] |

## Constraint Inventory

### Real Constraints (Validated)

- [Budget, time, skills, dependencies, integrations]

### Assumptions (Unvalidated)

- [Assumptions that need validation, with plan to validate]

## Scope Definition

- **In scope (V1):** [Explicit list]
- **Out of scope:** [Explicit list]
- **Walking skeleton:** [Thinnest useful version]

## Open Questions

- [Any remaining unknowns with plan to resolve]
```

#### Conversation vs. File

| Goes to file | Stays in conversation |
| :--- | :--- |
| Problem statement | Five Whys exploration |
| Need hierarchy with acceptance criteria | Prioritization discussion |
| Constraint inventory | Assumption discovery dialogue |
| Scope definition | Cut/keep negotiations |
| Validated requirements | Clarifying questions |

---

## Restrictions

### Hard Boundaries

- **No design before validation**: Do NOT propose architecture, choose technologies, or create designs until requirements are validated.
- **No skipping states**: If problem is unclear (RA0), do NOT discuss needs (RA2) or scope (RA4). Progress sequentially.
- **One question at a time**: Do not overwhelm the user with multiple diagnostic questions in a single message.
- **Developer decides**: Diagnose, question, and guide — the developer makes the final call on priorities and scope.
- **No vague acceptance**: Do not accept adjective-based requirements ("fast", "intuitive") as complete. Push for testable criteria.
- **No solution language**: Requirements must describe problems and needs, not implementations. Flag and rewrite solution-disguised requirements.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- **Design and architecture**: Proposing solutions, choosing technologies, creating design documents → Use `brainstorm-design`
- **Implementation planning**: Creating task lists, file paths, code structure → Use implementation planning skills
- **Code writing**: Writing any implementation code → Use development skills
- **Code review**: Reviewing existing code → Use `review-code`
- **Skill refinement**: Improving skill documents → Use `refine-skill-design`

**When to stop and hand off**:

- User says "approved", "looks good", "proceed" → Requirements validated, hand off to `brainstorm-design`
- User asks "how should we design this?" → Hand off to `brainstorm-design`
- User asks "can you write the code?" → Requirements complete, hand off to development workflow (suggest design step if skipped)
- User says requirements are "good enough" → Confirm all success criteria met, then hand off

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] **Problem articulated**: Clear problem statement exists without solution or technology references
- [ ] **Needs are testable**: Every requirement has acceptance criteria or "done looks like..." description
- [ ] **Constraints inventoried**: Real constraints separated from assumptions
- [ ] **Scope bounded**: V1 boundary explicit with deferred items and triggers documented
- [ ] **User confirmed**: User explicitly approved the validated requirements
- [ ] **Document persisted**: Requirements document written to agreed location and committed

### Process Quality Checks

- [ ] **States not skipped**: Progressed through diagnostic states sequentially (did not jump from RA0 to RA4)
- [ ] **One question at a time**: Did not overwhelm user with multiple questions per message
- [ ] **No solution language**: Requirements describe needs, not implementations
- [ ] **Developer decided**: Guided and questioned, but developer made final priority and scope calls
- [ ] **Adjectives resolved**: No vague adjective-only requirements remain ("fast", "intuitive", "easy")
- [ ] **Assumptions separated**: Unvalidated assumptions are flagged separately from real constraints

### Health Check Questions

Before declaring requirements validated, ask yourself:

1. If this project failed, what would be the most likely reason related to requirements?
2. Is the developer building what they need or what they know how to build?
3. What is explicitly NOT in scope?
4. Is the scope achievable with the actual constraints?
5. What assumptions have not been validated?
6. Could someone unfamiliar explain the requirements back correctly?

### Acceptance Test

**Can someone unfamiliar with the project read the requirements document and understand the problem, who has it, what "done" looks like, and what is out of scope — without asking clarifying questions?**

If NO: Requirements are incomplete. Return to the earliest unresolved state.

If YES: Requirements are validated. Persist and hand off to `brainstorm-design`.

---

## Examples

### Example 1: Greenfield Project — "I want to build a static site generator"

**User**: "I want to build a static site generator."

**Agent announces**: "I'm using the analyze-requirements skill to validate requirements before any design or implementation."

**Triage**: Clarity 30%, Specificity 10%, Completeness 10%. Start from RA0.

**RA0 — Problem discovery**:

Agent: "What specific frustration with existing static site generators led to this idea?"

User: "I'm tired of the complexity. I just want to write markdown and get HTML."

Agent: "What do you do today instead?"

User: "I use Hugo but spend more time debugging configuration than writing content."

**Problem statement captured**: "Solo content creator wastes time debugging SSG configuration instead of writing. Needs a zero-configuration path from Markdown to HTML."

**RA1 — Solution-first check**:

Agent: "You mentioned Hugo — is there anything about Hugo specifically that you need to preserve, or is 'Markdown → HTML' the core need regardless of tool?"

User: "Just Markdown to HTML. I don't care how."

**Exit RA1**: Need confirmed without technology lock-in.

**RA2 — Specificity**:

Agent: "What would 'done' look like for the simplest useful version?"

User: "I point it at a folder of .md files and get a folder of .html files with basic styling."

Agent: "How would you know the output is correct?"

User: "Each .md file produces one .html file. Links between pages work. It looks readable on mobile."

**Acceptance criteria captured**:

- R-01: Each `.md` file → one `.html` file (1:1 mapping)
- R-02: Internal links resolve correctly
- R-03: Output is readable on mobile (viewport meta, readable font size)

**RA3 — Constraints**:

Agent: "What time and skills do you have for this?"

User: "Evenings and weekends, maybe 10 hours/week. I know JavaScript well."

**Constraint inventory**: Time: 10 hrs/week; Skills: JavaScript proficiency; Dependency: none identified.

**RA4 — Scope**:

Agent: "If you could only ship 3 features, what are they?"

User: "Markdown to HTML, basic CSS, and a dev server with live reload."

**Scope defined**:

- V1 Must: Markdown→HTML, default CSS, dev server
- Deferred: Themes, plugins, custom templates (trigger: after V1 is usable for 2 weeks)
- Walking skeleton: CLI that converts one `.md` file to `.html`

**RA5 — Validated**: Agent presents summary, user says "looks good." Document written to `docs/requirements-planning/static-site-generator.md`.

### Example 2: Edge Case — Solution-Disguised Requirements

**User**: "I need a React app with a PostgreSQL database, GraphQL API, and Redis caching."

**Agent announces**: "I'm using the analyze-requirements skill to validate requirements before any design or implementation."

**Triage**: Clarity 60% (clear technologies), Specificity 20% (no problem stated), Completeness 15%. Start from RA0.

**RA0 — Problem discovery**:

Agent: "These are all technology choices. What problem are you trying to solve? Who has the problem?"

User: "Oh... I need to track inventory for my small business. I currently use spreadsheets and keep losing data."

**Problem statement**: "Small business owner loses inventory data due to spreadsheet limitations. Needs reliable inventory tracking."

**RA1 — Solution-first cleanup**:

Agent: "Let's rewrite the requirements without technology. 'React, PostgreSQL, GraphQL, Redis' are all solutions. What needs do they represent?"

Rewritten:

- ~~React app~~ → "Need a user interface accessible from multiple devices"
- ~~PostgreSQL~~ → "Data must survive server restarts and not be lost"
- ~~GraphQL API~~ → "Need to query inventory flexibly (by name, category, location)"
- ~~Redis caching~~ → "Frequently accessed data should load quickly"

Agent: "Is 'load quickly' testable? How fast is acceptable?"

User: "Under 2 seconds for the inventory list page."

**Exit RA1**: Requirements rewritten as needs. Technology choices deferred to design phase.

**RA2–RA5**: Continue through states. Final document captures needs without technology assumptions, allowing `brainstorm-design` to explore the right solution (which might be a simple spreadsheet alternative, not a full-stack app).

### Example 3: Edge Case — Mid-Project Scope Creep

**User**: "We started building a todo app but now it needs calendar integration, team collaboration, file attachments, and AI-powered task suggestions. We're 3 weeks behind."

**Agent announces**: "I'm using the analyze-requirements skill to validate requirements before expanding scope."

**Triage**: Clarity 50%, Specificity 40%, Completeness 30%. Scope creep symptoms — start from RA4 (earlier states likely resolved if 3 weeks in, but verify).

**Quick RA0 check**: "What was the original problem this todo app solves?"

User: "I need to stop forgetting tasks and deadlines for my freelance projects."

**Problem confirmed** — proceed to RA4.

**RA4 — Scope creep intervention**:

Agent: "If you could only ship 3 features from the full list, which 3 would solve the core problem of not forgetting tasks?"

User: "Basic task list, due dates with reminders, and... that's really it for now."

Agent: "So calendar integration, team collaboration, file attachments, and AI suggestions are all additions beyond the core problem. Should we defer them?"

**Scope redefined**:

- V1 Must: Task CRUD, due dates, reminders
- Deferred: Calendar integration (trigger: after using reminders for 1 month), collaboration (trigger: when freelance becomes team), attachments (trigger: user request), AI suggestions (trigger: 100+ tasks)
- Walking skeleton: CLI or simple UI that creates tasks with due dates and sends reminder notifications

**RA5 — Validated**: Requirements refocused. 3-week delay becomes manageable. Document updated.

---

## Anti-Patterns

### The Solution Specification

**Problem**: Requirements describe implementation, not needs. "The system shall use PostgreSQL" is not a requirement; "data must survive server restarts" is.

**Fix**: For each requirement, ask "could this be satisfied a different way?" If yes, you captured implementation, not need.

### The Stakeholder Fiction

**Problem**: Developer imagining requirements instead of discovering them. "Users will want..." without evidence.

**Fix**: If you are the user, be honest about YOUR needs. If building for others, talk to them or cite analogous evidence. Do not invent users.

### The Infinite Backlog

**Problem**: Requirements grow without prioritization. Everything is equally important.

**Fix**: Force-rank. If you could only ship ONE thing, what is it? Then two? This reveals actual priorities.

### The Premature Precision

**Problem**: Specifying details that do not matter yet. Designing notification preferences before validating anyone wants notifications.

**Fix**: Stub uncertain areas with "TBD after [X] validated." Focus precision on V1 Must items.

### The Constraint Blindness

**Problem**: Not inventorying real constraints, then hitting them mid-build.

**Fix**: Explicit constraint inventory BEFORE finalizing requirements.

---

## Appendix: Integration Map

### Upstream (feeds into this skill)

| Source | When | What it provides |
| :--- | :--- | :--- |
| User request | New project or feature idea | Raw intent to analyze |
| Existing documentation | Mid-project validation | Partial requirements to diagnose |

### Downstream (this skill feeds into)

| Target skill | When | What it receives |
| :--- | :--- | :--- |
| `brainstorm-design` | Requirements validated | Validated Requirements Document as design input |
| Implementation planning | Design is trivial | Validated requirements with scope and constraints |

### Handoff contract

| This skill outputs | Target skill expects |
| :--- | :--- |
| Problem statement | Design context |
| Need hierarchy with acceptance criteria | Functional requirements |
| Constraint inventory | Architecture constraints |
| Scope definition (V1 boundary) | Design scope |
