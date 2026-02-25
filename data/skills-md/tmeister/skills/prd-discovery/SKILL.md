---
name: prd-discovery
description: Interview the user and write a PRD for Ralph in .prd/prd-<feature>.md.
---

# PRD Discovery

Use this skill to interview the user and produce a clear PRD for Ralph execution.

## Inputs

- If a topic is provided, use it. Otherwise ask for a short description of the feature or bug.

## Workflow

1. **Initial prompt**
   - Ask what they want to build or fix and why.

2. **Context scan**
   - Check for existing specs or documentation, such as `specs/README.md`.
   - Review project overview files like `README.md` and package manifests.

3. **Interview**
   - Ask only critical questions that affect scope and acceptance criteria.
   - Cover: goals, users, constraints, scope, edge cases, success criteria.

4. **Draft PRD**
   - Use the PRD template.
   - Break into right sized user stories, each completable in one iteration.
   - Order stories by dependency: schema, backend, UI, aggregation.
   - Acceptance criteria must be verifiable.

5. **Save output**
   - Save to `.prd/prd-<feature>.md`.
   - Create `.prd` if missing.

6. **Confirm and next steps**
   - Show the file path.
   - Suggest converting with `/prd-to-json`.

## Rules

- Always include "Typecheck/lint/test passes" in every story.
- For UI stories, include "Verify in browser".
- If the scope is unclear, continue interviewing before writing.
