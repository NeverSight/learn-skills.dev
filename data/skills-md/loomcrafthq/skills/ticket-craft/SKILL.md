---
name: ticket-craft
description: >
  Create, enrich, organize, and track production-quality tickets optimized for
  execution by a developer or AI agent with zero ambiguity. Platform-agnostic
  (Linear, Jira, GitHub Issues, Notion, Asana). Use this skill whenever the user
  mentions tickets, issues, backlogs, sprint planning, or project management —
  even if they just say "create a task", "what's next", "I'm done with X", or
  "break this feature into tickets". Triggers on any signal related to PM workflow:
  starting, completing, or planning work items.
license: MIT
metadata:
  author: loomcrafthq
  version: "1.0.0"
---

# Ticket Craft

Skill for creating, enriching, organizing, and tracking production-quality tickets.
Optimized for execution by a developer or AI agent with zero ambiguity.
Platform-agnostic.

---

## Step 0: Bootstrap — context and PM tool

Execute before any action.

### 0a. Detect PM tool via MCP

| MCP detected | PM tool |
|--------------|---------|
| Linear MCP | Linear |
| Jira MCP | Jira |
| GitHub MCP | GitHub Issues |
| Notion MCP | Notion |
| Asana MCP | Asana |
| None | Ask the user |

If multiple PM MCPs are connected: ask which one to use.
If none: offer dry-run mode (tickets as Markdown, no push).

### 0b. Load project context

Read in this order, stop at first success:

1. `CLAUDE.md` or `.claude/CLAUDE.md`
2. `README.md` or `README.rst`
3. `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`
4. If nothing accessible: mini-questionnaire (project name, stack, PM tool if not detected)

Extract: project name, tech stack, architecture conventions, teams.
Only ask questions whose answers cannot be found in files.

---

## Mode detection

| Signal | Mode |
|--------|------|
| Ticket ID mentioned, "complete issue X", "enrich this ticket" | **ENRICH** |
| Idea, concept, feature, or project without an ID | **DEFINE** |
| "what's next", "grab the next ticket", "next task" | **NEXT** |
| "ticket done", "I pushed", "it's done", ID + completion signal | **DONE** |
| "I'm starting", "I'm taking ticket X", ID + start signal | **START** |

---

## MODE ENRICH — Complete an existing ticket

1. Fetch the ticket via MCP
2. Identify missing or insufficient fields
3. Fill in using the standard template (see Template section)
4. Update via MCP

---

## MODE START — Start a ticket

Triggers: "I'm starting ticket X", "I'm taking X", or after MODE NEXT if the user
confirms they want to start the suggested ticket.

1. Fetch the ticket via MCP to confirm its title
2. Set status to **In Progress** via MCP
3. Confirm: "Ticket X — [title] moved to In Progress."

Note: if Claude Code is available, START can be invoked automatically after a ticket
is received via NEXT, without waiting for an explicit signal.

---

## MODE DONE — Close a ticket

Manual triggers: "ticket done", "I pushed", "it's done", "close ticket X".
Automatic trigger from Claude Code: after a successful git push, call this mode.

1. Identify the relevant ticket (explicit ID, or the unique active In Progress ticket)
2. Set status to **Done** via MCP
3. If other tickets were blocked by this one, report them:
   "The following tickets are now unblocked: [list]"
4. Automatically suggest the next ticket via MODE NEXT

---

## MODE NEXT — Next ticket

Global aggregation: active milestone + Todo + Backlog, in that order of preference.

### Selection algorithm

1. Fetch via MCP all non-completed tickets:
   - In Progress status (absolute priority — check if a ticket is already in progress)
   - Todo status
   - Backlog status
   - Include the active milestone if one exists

2. Build the dependency graph:
   - Exclude all tickets where at least one `blockedBy` is not in Done status
   - Keep only "unblocked" tickets (no active dependency)

3. Sort unblocked tickets:
   - Descending priority (Urgent > High > Normal > Low)
   - At equal priority: In Progress > Todo > Backlog
   - Still equal: active milestone before out-of-milestone

4. Return the first ticket in the list:
   - Title, ID, current status, size, priority
   - 2-3 line summary of the ticket
   - List of tickets it will unblock once completed

5. Offer to start it: "Do you want me to move this ticket to In Progress?"

---

## MODE DEFINE — Define a project or feature from an idea

### Step 1: Chat interview

Never generate tickets before having sufficient answers.

**Isolated feature:**
- End-user goal?
- Known technical constraints? (existing auth, DB schema, third-party APIs?)
- Edge cases or specific business rules?
- Definition of done?

**Full project:**
- Problem being solved?
- User personas?
- Must-have vs nice-to-have?
- Constraints: deadline, imposed stack, third-party integrations?
- References or inspirations?

Keep going until there's enough context. Signal: "I have enough to generate the backlog."

### Step 2: Verify or create the project in the PM tool

Via MCP: search for existing project. If absent, create it with name + description.

### Step 3: Generate issues in logical order

**Creation order** (IDs reflect the sequence):

1. Infrastructure / setup — Urgent priority
2. Data layer / models — High priority
3. Backend / API — High to Normal priority
4. Frontend / UI — Normal priority
5. Third-party integrations — Normal to Low priority
6. Polish / nice-to-have — Low priority

**Principles:**
- 1 ticket = 1 clear responsibility, implementable in 1 session without context switching
- Fine granularity to minimize dependencies
- Assign `blockedBy` after all tickets are created (IDs known)

### Step 4: Mandatory summary table

| ID | Title | Size | Priority | Status | Blocked by |
|----|-------|------|----------|--------|------------|
| #1 | Setup database | M | Urgent | Todo | — |
| #2 | User model + migrations | S | High | Todo | #1 |
| #3 | POST /register endpoint | M | High | Todo | #1, #2 |

---

## Ticket template

Each ticket follows this format in the description field.
Goal: implementable without asking any questions.

```markdown
## Context
Why this ticket exists. What problem it solves. Link to the broader project.

## Scope
**In scope:**
- ...

**Out of scope:**
- ...

## Technical Specs
Stack used, architecture constraints, relevant endpoints, DB schema if applicable,
specific libraries, patterns to follow.
Be exhaustive: no unknowns should remain.

## Acceptance Criteria
- [ ] Criterion 1 (objectively verifiable)
- [ ] Criterion 2

## Definition of Done
- [ ] Code implemented and working
- [ ] 0 lint / type checking errors
- [ ] Unit tests for business logic
- [ ] 0 regressions on existing features
- [ ] [Ticket-specific criteria]

## QA Checklist
Reproducible steps for a human or QA agent.
- [ ] ...

## Edge Cases & Gotchas
Identified edge cases, boundary behaviors, errors to handle explicitly.
- ...
```

---

## T-Shirt Sizing

Map to the PM tool's native system if different from story points.

| Size | Value | Criteria |
|------|-------|----------|
| XS | 1 | Less than 1h, trivial change |
| S | 2 | 1-3h, well-defined scope |
| M | 3 | 3-8h, minor unknowns |
| L | 5 | 1-2 days, real complexity |
| XL | 8 | More than 2 days — split if possible |

XL ticket: split unless truly indivisible.

---

## Priority

Adapt to the PM tool's native values (Linear: 1-4, Jira: Highest/High/Medium/Low/Lowest).

| Level | Context |
|-------|---------|
| Urgent / Highest | Blocking other tickets, infra foundation |
| High | Critical for MVP, on the critical path |
| Normal / Medium | Main non-blocking feature |
| Low | Nice-to-have, polish, future iterations |

---

## Status mapping

Adapt to the detected PM tool's native statuses.

| Generic status | Linear | Jira | GitHub Issues |
|----------------|--------|------|---------------|
| Backlog | Backlog | Backlog | open + label backlog |
| Todo | Todo | To Do | open |
| In Progress | In Progress | In Progress | open + label in-progress |
| Done | Done | Done | closed |

---

## Title format

**[Verb] [Subject]** or **[Verb] [Subject] — [Context]**

Examples:
- "Implement JWT authentication"
- "Create User model + migrations"
- "Add GET /matches endpoint"
- "Configure CI/CD pipeline"

---

## Quality rules

- Never create a ticket without Acceptance Criteria
- Never create a ticket without Technical Specs filled in
- Dependencies declared in the PM tool's native field, not just in the text
- Labels / tags: use existing ones, create if necessary
- Summary table always displayed after batch generation
- After each DONE, report unblocked tickets and suggest the next one
