---
name: i-validate-user-story-completion
description: Validate implemented user stories against approved acceptance criteria with BDD, Gherkin feature files, and pytest-bdd. Use after g-implement-repository-work when one or more implemented stories need completion evidence before pull request creation, when tests/validation scenarios must be created or run, or when sdlc_docs/trace_workflow.md must record user-story validation status. Do not use for initial implementation TDD, requirements authoring, architecture design, release deployment, or pull request creation.
---

# User Story Completion Validation

## Purpose

Confirm that implemented user stories satisfy approved acceptance criteria through executable BDD scenarios. Treat approved Product Requirements, implementation evidence, existing tests, and workflow traceability as inputs. Produce validation evidence, not new product scope.

## Governing Rules

- Work in English.
- Use the exact skill identifier `i-validate-user-story-completion`.
- Treat `sdlc_docs/trace_workflow.md` as the canonical workflow status file when present.
- Verify Product Requirements are approved and the selected user stories have implementation evidence before creating validation scenarios.
- Use Gherkin feature files under `tests/validation/features/`.
- Use pytest-bdd step definitions under `tests/validation/steps/`.
- Map every selected acceptance criterion to at least one scenario or record why it cannot yet be validated.
- Preserve acceptance-criterion meaning. Do not add product behavior, validation rules, error handling, roles, data, or workflows not approved upstream.
- Keep BDD validation separate from implementation TDD. Route missing implementation behavior to `g-implement-repository-work`.
- Use `pytest` and `pytest-bdd`; do not introduce `unittest.TestCase`.
- Require explicit approval of the visible validation proposal before local writes.
- Re-read affected files and `trace_workflow.md` immediately before writing.
- Do not commit, push, create pull requests, close issues, move project items, or publish comments without separate approval.
- Never claim validation passed unless the command was executed successfully.

## Canonical Inputs

Read the applicable project-owned artifacts when present:

```text
sdlc_docs/01_requirements/product_requirements.md
sdlc_docs/02_architecture/architecture.md
sdlc_docs/02_architecture/code-level.md
sdlc_docs/03_implementation/backlog_priority.md
sdlc_docs/trace_workflow.md
tests/README.md
tests/validation/
pyproject.toml or equivalent test configuration
```

Use implementation evidence from local status tracking, changed files, commits, or the selected issue. Do not hardcode any project-specific paths beyond the generic SDLC and pytest-bdd conventions above.

## Traceability Ownership

The skill owns the `User story validation` row in `sdlc_docs/trace_workflow.md`.

Controlled overlap with `Implementation` is allowed when both rows are `In Progress` and validation work is limited to implemented story subsets with explicit evidence.

Allowed fields on the owned row:

```text
Status
Current activity
Evidence
Missing or blocked
Next action
```

The skill may update only handoff fields in an `Implementation` row after validation passes, and only when that row exists and the workflow explicitly uses it. It must not modify requirements, architecture, repository preparation, foundation, pull request, release, or unrelated increment rows.

Use these row patterns when a project template has no stronger local convention:

```markdown
| User story validation | Initial Release | Not Started | BDD User Story Completion Validation | implemented stories available | BDD validation has not run | Run i-validate-user-story-completion |
| User story validation | Initial Release | In Progress | BDD User Story Completion Validation | selected implemented stories and approved requirements; subset scope and commands recorded | BDD mapping or validation execution pending for remaining stories | Continue i-validate-user-story-completion |
| User story validation | Initial Release | Blocked | BDD User Story Completion Validation | attempted BDD validation | implementation evidence, acceptance criteria, or scenario execution blocked | Resolve blocker with i-validate-user-story-completion or route upstream |
| User story validation | Initial Release | Complete | BDD User Story Completion Validation | passing `tests/validation` command and story-scenario mapping | None | Run h-create-implementation-pull-request |
```

Before every traceability write:

1. copy the current trace file to a temporary location outside the repository;
2. prepare the proposed after-file;
3. validate only authorized row and field changes;
4. reject unauthorized changes and preserve the original file;
5. report changed fields and unauthorized-change count.

Use `scripts/validate_bdd_validation.py` for objective checks. Do not replace a missing validator with manual confidence.

## Workflow

1. Locate the repository root.
2. Identify the selected implemented story or stories.
3. Read approved Product Requirements and acceptance criteria for the selected scope.
4. Read implementation evidence and existing validation tests.
5. Verify pytest-bdd configuration and `tests/validation/features/` plus `tests/validation/steps/`.
6. Read `references/bdd-validation-policy.md`.
7. Create the acceptance-criterion to scenario mapping.
8. Identify missing information, unsupported behavior, or implementation gaps.
9. If blocking information is missing, update the validation row to `Blocked` or `Under Clarification`, report the blocker, and stop.
10. Present the validation proposal: selected stories, criteria, scenario names, feature files, step files, commands, trace updates, and out-of-scope work.
11. Stop for explicit approval before local writes.
12. Re-read affected files and traceability after approval.
13. Create or update Gherkin feature files.
14. Create or update pytest-bdd step definitions.
15. Run targeted validation scenarios.
16. Run the full validation command for the selected scope or `tests/validation`.
17. Run `scripts/validate_bdd_validation.py`.
18. If validation fails because implementation is incomplete, record the failing scenario and route to `g-implement-repository-work`.
19. If validation fails because acceptance criteria are unclear, route to `c-manage-product-requirements`.
20. If validation passes, update authorized traceability fields and set next action to `Run h-create-implementation-pull-request`.
21. Report scenario coverage, command results, files changed, trace fields changed, and remaining gaps.

During overlap with ongoing implementation, keep `User story validation` as `In Progress` for subset evidence and do not claim full-stage completion until selected completion gates are met.

## Completion Gates

Validation is complete only when:

- every selected approved acceptance criterion is mapped to a scenario or explicitly blocked;
- every mapped scenario is implemented as Gherkin and pytest-bdd steps;
- validation tests pass for the selected scope;
- BDD evidence names the exact commands and results;
- traceability is updated only through authorized fields;
- no product behavior, requirements, architecture, or foundation decision was invented;
- downstream action is `Run h-create-implementation-pull-request` only after validation passed.

## Resources

- Read `references/bdd-validation-policy.md` before mapping scenarios.
- Read `references/golden-example/browser-task-board/README.md` when a concrete progressive example is useful.
- Run `scripts/validate_bdd_validation.py` after creating or updating validation scenarios.


## Progressive Audit Resources

- Read `references/golden-example/README.md` only when a progressive concrete example is useful.
- Read `references/process_flowchart.md` only for human explanation or audit.
