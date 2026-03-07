---
name: groove-work-review
description: "Evaluate output, identify lessons, decide accept/rework. Use after implementation."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

# groove-work-review

## Outcome

The artifact is reviewed for correctness, quality, and fit to plan. Lessons are identified for the compound stage. A clear accept/rework decision is made with rationale. Review notes are captured in the task body.

## Acceptance Criteria

- Artifact is evaluated against the plan and acceptance criteria
- Specific gaps or issues are identified (not vague "needs improvement")
- Accept or rework decision is stated with rationale
- Lessons are noted for `/groove-work-compound`
- Review notes appended to stage task body
- Stage task created in backend: `YYYY-MM-DD, Review`

## Constraints

- Read `tasks:` from `.groove/index.md` to determine backend
- Be thorough — 80% of compound loop value is here and in plan
- If rework: note specific gaps and link back to which plan step was missed or unclear
- If accept: still note what worked well and what could be improved next time
- Do not skip review even for small changes — capture something
- Create stage task via `/groove-utilities-task-create` if `tasks != none` (title `YYYY-MM-DD, Review`)
