---
name: plan-sprint
description: >
  Plan a sprint by refining backlog items, defining a sprint goal, calculating
  team capacity, selecting items, and decomposing them into tasks. Produces
  a SPRINT-PLAN.md with goal, selected items, task breakdown, and capacity
  allocation. Use when starting a new sprint in a Scrum or agile project,
  re-planning after significant scope change, transitioning from ad-hoc work
  to structured sprint cadence, or after backlog grooming when items are ready
  for inclusion.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: project-management
  complexity: intermediate
  language: multi
  tags: project-management, sprint, agile, scrum, capacity, sprint-planning
---

# Plan a Sprint

Plan a time-boxed sprint by selecting refined backlog items up to team capacity, defining a clear sprint goal, and decomposing selected items into actionable tasks. This skill produces a complete sprint plan that guides team work for the duration of the sprint iteration.

## When to Use

- Starting a new sprint in a Scrum or agile project
- Re-planning a sprint after significant scope change
- Transitioning from ad-hoc work to structured sprint cadence
- After backlog grooming when items are ready for sprint inclusion
- Planning the first sprint after project charter approval

## Inputs

- **Required**: Product backlog (prioritized, with estimates)
- **Required**: Sprint duration (typically 1-2 weeks)
- **Required**: Team members and their availability
- **Optional**: Previous sprint velocity (story points or items completed)
- **Optional**: Sprint number and date range
- **Optional**: Carry-over items from previous sprint

## Procedure

### Step 1: Review and Refine Backlog Items

Read the current BACKLOG.md. For each candidate item near the top of the backlog, verify it has:

- Clear title and description
- Acceptance criteria (testable conditions)
- Estimate (story points or T-shirt size)
- No unresolved blockers

Refine any items missing these elements. Split items estimated larger than half the sprint capacity into smaller, more manageable pieces.

**Expected:** Top 10-15 backlog items are "sprint-ready" with acceptance criteria and estimates.

**On failure:** If items lack acceptance criteria, write them now. If items can't be estimated, schedule a refinement conversation and select only ready items.

### Step 2: Define Sprint Goal

Write a single clear sprint goal — one sentence stating what the sprint will achieve. The goal should be:

- Achievable within the sprint duration
- Valuable to stakeholders
- Testable (you can verify it was met at sprint end)

```markdown
**Sprint Goal**: [One sentence describing the objective]
```

Example: "Enable users to reset their password through email verification with two-factor authentication."

**Expected:** Sprint goal articulated as one clear, testable sentence.

**On failure:** If no coherent goal emerges, the backlog priorities may be scattered — consult the product owner to focus on a single valuable outcome.

### Step 3: Calculate Team Capacity

Calculate available person-days for each team member:

```markdown
## Team Capacity
| Team Member | Available Days | Overhead (%) | Net Capacity |
|-------------|---------------|-------------|--------------|
| [Name] | [Sprint days - PTO] | 20% | [Available × 0.8] |
| [Name] | [Sprint days - PTO] | 20% | [Available × 0.8] |
| **Total** | | | **[Sum] person-days** |
```

Overhead accounts for meetings, reviews, ad-hoc requests (typically 15-25%).

If using story points: use previous sprint velocity as capacity. If first sprint, use 60-70% of theoretical maximum.

**Expected:** Capacity calculated in person-days or story points with documented assumptions.

**On failure:** If no historical velocity exists, be conservative — plan to 60% capacity and adjust after the sprint. Better to under-commit and deliver than over-commit and fail.

### Step 4: Select Items and Compose Sprint Backlog

Select items from the top of the product backlog until capacity is reached. Decompose each selected item into tasks (2-8 hours each):

```markdown
# Sprint Plan: Sprint [N]
## Document ID: SP-[PROJECT]-S[NNN]

### Sprint Details
- **Sprint Goal**: [From Step 2]
- **Duration**: [Start date] to [End date]
- **Capacity**: [From Step 3] person-days / [N] story points
- **Team**: [List team members]

### Sprint Backlog
| ID | Item | Points | Tasks | Assignee | Status |
|----|------|--------|-------|----------|--------|
| B-001 | [Item title] | 5 | 4 | [Name] | To Do |
| B-002 | [Item title] | 3 | 3 | [Name] | To Do |
| B-003 | [Item title] | 8 | 6 | [Name] | To Do |
| **Total** | | **16** | **13** | | |

### Task Breakdown

#### B-001: [Item title]
**Acceptance Criteria**: [From backlog item]

- [ ] Task 1: [Description] (4h, [Assignee])
- [ ] Task 2: [Description] (2h, [Assignee])
- [ ] Task 3: [Description] (4h, [Assignee])
- [ ] Task 4: [Description] (2h, [Assignee])

#### B-002: [Item title]
**Acceptance Criteria**: [From backlog item]

- [ ] Task 1: [Description] (3h, [Assignee])
- [ ] Task 2: [Description] (4h, [Assignee])
- [ ] Task 3: [Description] (2h, [Assignee])

#### B-003: [Item title]
**Acceptance Criteria**: [From backlog item]

- [ ] Task 1: [Description] (3h, [Assignee])
- [ ] Task 2: [Description] (4h, [Assignee])
- [ ] Task 3: [Description] (2h, [Assignee])
- [ ] Task 4: [Description] (3h, [Assignee])
- [ ] Task 5: [Description] (4h, [Assignee])
- [ ] Task 6: [Description] (2h, [Assignee])

### Risks and Dependencies
| Risk | Impact | Mitigation |
|------|--------|-----------|
| [Risk 1] | [Impact] | [Mitigation] |
| [Risk 2] | [Impact] | [Mitigation] |

### Carry-Over from Previous Sprint
| ID | Item | Reason | Remaining Effort |
|----|------|--------|-----------------|
| B-XXX | [Item] | [Reason] | [Hours/points] |
```

**Expected:** Sprint backlog with items selected up to capacity, each decomposed into tasks with time estimates.

**On failure:** If total points exceed capacity, remove the lowest-priority item. Never exceed capacity by more than 10%. If dependencies block sequencing, re-order or defer items.

### Step 5: Document Commitments and Save

Write the sprint plan to `SPRINT-PLAN.md` (or `SPRINT-PLAN-S[NNN].md` for archival). Confirm:

- Sprint goal is achievable with selected items
- No team member is overallocated (>100% capacity)
- Dependencies between items are sequenced correctly
- Carry-over items are accounted for in capacity
- All acceptance criteria copied from backlog items

Run a final validation:

```bash
# Check that total task hours align with capacity
grep -A 100 "Task Breakdown" SPRINT-PLAN.md | grep -o '([0-9]*h' | sed 's/[^0-9]//g' | awk '{sum+=$1} END {print "Total hours:", sum}'
```

**Expected:** SPRINT-PLAN.md created with complete sprint backlog and task breakdown. Total hours should be ≤80% of available person-days × 8 hours.

**On failure:** If commitments don't align with goal, revisit item selection in Step 4. If task hours exceed capacity, remove the last item or decompose tasks more granularly.

## Validation

- [ ] Sprint goal is one clear, testable sentence
- [ ] Team capacity calculated with documented assumptions (overhead %, PTO accounted)
- [ ] Selected items do not exceed capacity (points or person-days)
- [ ] Every selected item has acceptance criteria copied into task breakdown
- [ ] Every selected item is decomposed into tasks (2-8 hours each)
- [ ] No team member overallocated beyond 100% capacity
- [ ] Carry-over items from previous sprint documented with remaining effort
- [ ] Dependencies between items sequenced correctly
- [ ] Risks and mitigations documented
- [ ] SPRINT-PLAN.md file created and saved

## Common Pitfalls

- **No sprint goal**: Without a goal, the sprint is just a bag of tasks. The goal provides focus and a basis for scope decisions mid-sprint.
- **Over-commitment**: Planning to 100% capacity ignores interruptions, bugs, and overhead. Plan to 70-80% to leave buffer for the unexpected.
- **Tasks too large**: Tasks over 8 hours hide complexity and make progress tracking difficult. Decompose until tasks are 2-8 hours.
- **Ignoring carry-over**: Unfinished items from the last sprint consume capacity this sprint. Account for them explicitly in capacity calculations.
- **Sprint goal as item list**: "Complete B-001, B-002, B-003" is not a goal. A goal describes the outcome: "Users can reset their password through email verification."
- **No task ownership**: Every task should have an assignee at planning time to surface capacity conflicts early.
- **Skipping acceptance criteria**: Tasks without acceptance criteria can't be tested. Copy acceptance criteria from backlog items into the task breakdown section.

## Related Skills

- `manage-backlog` — maintain and prioritize the product backlog that feeds sprint planning
- `draft-project-charter` — provides project context and initial scope for the first sprint
- `generate-status-report` — report sprint progress and velocity to stakeholders
- `conduct-retrospective` — review sprint execution and improve the planning process
- `create-work-breakdown-structure` — WBS work packages can feed the backlog in hybrid agile-waterfall approaches
