---
name: why-review
description: '[Review & Quality] Audit completed feature/refactor for reasoning quality with Understanding Score (0-5)'
argument-hint: [optional-focus-area]
---

# /why-review -- Understanding Verification

Audit a completed feature or refactor for reasoning quality. Produces an Understanding Score (0-5).

## Summary

**Goal:** Verify that changes were made with understanding, not just pattern compliance.

| Step | Action          | Key Notes                                           |
| ---- | --------------- | --------------------------------------------------- |
| 1    | Gather changes  | List all files changed in current session/branch    |
| 2    | Reasoning audit | For each significant change, check WHY articulation |
| 3    | ADR alignment   | Cross-reference against docs/adr/ decisions         |
| 4    | Score & report  | Understanding Score (0-5) with specific gaps        |

**Scope:** Runs in all 9 code-producing workflows: feature, refactor, bugfix, migration, batch-operation, deployment, performance, quality-audit, verification.

## Workflow

### Step 1: Gather Changes

```bash
git diff --stat main...HEAD
```

List all changed files since branch diverged from main. Filter to significant changes (skip formatting, imports-only). If on main or no branch history, use `git diff --stat HEAD~5` as fallback.

### Step 2: Reasoning Audit

For each significant change, evaluate:

- **WHY articulated?** Was there a Design Intent statement or commit message explaining reasoning?
- **Alternatives considered?** Did the change mention rejected approaches?
- **Principle identified?** Can the change be linked to a known pattern/ADR?

### Step 3: ADR Alignment

Cross-reference against `docs/adr/`:

- Does this change align with or deviate from existing ADRs?
- If deviating, is the deviation documented and justified?

### Step 4: Understanding Score

**Scoring Rubric:**

| Score | Criteria                                                                          |
| ----- | --------------------------------------------------------------------------------- |
| 5     | All changes have articulated WHY, alternatives considered, ADR alignment verified |
| 4     | Most changes explained, minor gaps in reasoning                                   |
| 3     | Some reasoning, some "followed the pattern" without explanation                   |
| 2     | Mostly compliance-based, little reasoning articulated                             |
| 1     | No reasoning articulated -- pure pattern following                                |
| 0     | Changes contradict existing ADRs without justification                            |

**Output format:**

```
## Understanding Score: [X]/5

### Reasoning Found
- [file]: [reasoning articulated]

### Reasoning Gaps
- [file]: [what's missing -- e.g., "no justification for choosing CQRS over simple CRUD"]

### ADR Alignment
- [ADR-001]: Aligned / Deviated (justified) / Deviated (unjustified)

### Recommendation
[If score < 3: "Investigate whether changes were mechanical. Consider documenting the WHY before committing."]
```

## Important Notes

- This is a soft review -- never blocks commits
- Treat score < 3 as a flag to investigate, not a failure
- Focus on architectural decisions, not formatting choices
- When in doubt, ask: "Could someone explain why this change was made without reading the diff?"

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
