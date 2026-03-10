---
name: create-work-breakdown-structure
description: >
  Create a Work Breakdown Structure (WBS) and WBS Dictionary from project
  charter deliverables. Covers hierarchical decomposition, WBS coding,
  effort estimation, dependency identification, and critical path candidates.
  Use after a project charter is approved, when planning a classic or waterfall
  project with defined deliverables, breaking a large initiative into manageable
  work packages, or establishing a basis for effort estimation and resource
  planning.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: project-management
  complexity: intermediate
  language: multi
  tags: project-management, wbs, work-breakdown-structure, classic, waterfall, planning
---

# Create a Work Breakdown Structure

Decompose project scope into a hierarchical set of work packages that can be estimated, assigned, and tracked. The WBS provides the foundation for effort estimation, resource planning, and schedule development by breaking down complex deliverables into manageable components.

## When to Use

- After a project charter is approved and scope is defined
- Planning a classic/waterfall project with defined deliverables
- Breaking down a large initiative into manageable work packages
- Establishing a basis for effort estimation and resource planning
- Creating a shared understanding of all required work

## Inputs

- **Required**: Approved project charter (especially scope and deliverables sections)
- **Required**: Project methodology (classic/waterfall, or hybrid with WBS for planning)
- **Optional**: Historical effort data from similar projects
- **Optional**: Team composition and available skills
- **Optional**: Organizational WBS templates or standards

## Procedure

### Step 1: Extract Deliverables from Charter
Read the project charter. List all deliverables and acceptance criteria. Group them into 3-7 top-level categories (these become WBS Level 1 elements).

**Expected:** List of Level 1 WBS elements matching charter deliverables.

**On failure:** If charter is vague, return to `draft-project-charter` to refine scope.

### Step 2: Decompose into Work Packages
For each Level 1 element, decompose into sub-elements (Level 2, Level 3). Apply the 100% rule: child elements must represent 100% of the parent's scope. Stop decomposing when work packages are:
- Estimable (can assign effort in person-days)
- Assignable (one person or team owns it)
- Measurable (clear done/not-done criteria)

Create a WBS outline:
```markdown
# Work Breakdown Structure: [Project Name]
## Document ID: WBS-[PROJECT]-[YYYY]-[NNN]

### WBS Hierarchy

1. [Level 1: Deliverable Category A]
   1.1 [Level 2: Sub-deliverable]
      1.1.1 [Level 3: Work Package]
      1.1.2 [Level 3: Work Package]
   1.2 [Level 2: Sub-deliverable]
2. [Level 1: Deliverable Category B]
   2.1 [Level 2: Sub-deliverable]
3. [Level 1: Project Management]
   3.1 Planning
   3.2 Monitoring & Control
   3.3 Closure
```

Apply WBS codes (1.1.1 format). Ensure 3-5 levels deep maximum. Always include a "Project Management" branch.

**Expected:** Complete WBS with 15-50 work packages, each with a unique WBS code.

**On failure:** If decomposition exceeds 5 levels, the scope is too large — consider splitting into sub-projects.

### Step 3: Write WBS Dictionary
For each work package (leaf node), write a dictionary entry:

```markdown
# WBS Dictionary: [Project Name]
## Document ID: WBS-DICT-[PROJECT]-[YYYY]-[NNN]

### WBS 1.1.1: [Work Package Name]
- **Description**: What this work package produces
- **Acceptance Criteria**: How to verify it's done
- **Responsible**: Person or role
- **Estimated Effort**: [T-shirt size or person-days]
- **Dependencies**: WBS codes this depends on
- **Assumptions**: Key assumptions for this work package

### WBS 1.1.2: [Work Package Name]
...
```

**Expected:** Dictionary entry for every leaf-node work package.

**On failure:** Missing dictionary entries indicate incomplete decomposition — revisit Step 2.

### Step 4: Estimate Effort
For each work package, apply one estimation method:
- **T-shirt sizing** (XS/S/M/L/XL) for early-stage planning
- **Person-days** for detailed planning
- **Three-point estimate** (optimistic/most likely/pessimistic) for high-uncertainty work

Create a summary table:
```markdown
## Effort Summary
| WBS Code | Work Package | Estimate | Method | Confidence |
|----------|-------------|----------|--------|------------|
| 1.1.1 | [Name] | 5 pd | person-days | High |
| 1.1.2 | [Name] | M | t-shirt | Medium |
```

Total effort = sum of all work packages.

**Expected:** Every work package has an effort estimate with stated confidence.

**On failure:** If confidence is Low on >30% of packages, schedule a refinement session with SMEs.

### Step 5: Identify Dependencies and Critical Path Candidates
Map dependencies between work packages:
```markdown
## Dependencies
| WBS Code | Depends On | Type | Notes |
|----------|-----------|------|-------|
| 1.2.1 | 1.1.1 | Finish-to-Start | Output of 1.1.1 is input to 1.2.1 |
| 2.1.1 | 1.1.2 | Finish-to-Start | |
```

Identify the longest chain of dependent work packages — this is the critical path candidate.

**Expected:** Dependency table with at least finish-to-start relationships identified.

**On failure:** If dependencies form cycles, the decomposition has errors — revisit Step 2.

### Step 6: Review and Baseline
Combine WBS and dictionary into final documents. Verify the 100% rule at every level. Get stakeholder sign-off.

**Expected:** WBS.md and WBS-DICTIONARY.md files created and reviewed.

**On failure:** If stakeholders identify missing scope, add work packages and re-estimate.

## Validation

- [ ] WBS file created with document ID and WBS codes
- [ ] 100% rule satisfied: children fully represent parent scope at every level
- [ ] Every leaf node has a WBS dictionary entry
- [ ] All work packages have effort estimates
- [ ] Dependencies identified with no circular references
- [ ] Project Management branch included
- [ ] Critical path candidates identified
- [ ] WBS depth does not exceed 5 levels

## Common Pitfalls

- **Confusing deliverables with activities**: WBS elements should be nouns (deliverables), not verbs (activities). "User Authentication Module" not "Implement Authentication".
- **Violating the 100% rule**: If children don't add up to 100% of parent scope, work will be missed.
- **Too shallow or too deep**: 2 levels is too vague for planning; 6+ levels is micromanagement. Target 3-5 levels.
- **Skipping Project Management branch**: PM work (planning, meetings, reporting) is real work that consumes effort.
- **Estimating before decomposing**: Estimate work packages, not categories. A Level 1 estimate is unreliable.
- **No dictionary**: A WBS without a dictionary is a tree of labels — the dictionary provides the definition of done.

## Related Skills

- `draft-project-charter` — provides the scope and deliverables that feed WBS decomposition
- `manage-backlog` — translate WBS work packages into backlog items for tracking
- `generate-status-report` — report progress against WBS % complete
- `plan-sprint` — if using hybrid approach, sprint-plan from WBS work packages
- `conduct-retrospective` — review estimation accuracy and decomposition quality
