---
name: g-implement-repository-work
description: Plan and implement repository work after approved requirements, approved architecture, synchronized repository issues, and a completed technical foundation. Use when Codex must either (1) create or update sdlc_docs/03_implementation backlog-priority guidance from unresolved issues without implementing code, or (2) implement one explicitly selected user story, bug, refactor, or small technical issue through developer-owned hybrid code-level architecture design, relevant best-practice references, Ping-Pong TDD where "Tester driver" defines/creates RED tests and "Developer navigator" implements only enough code to pass them, user-visible RED-GREEN-REFACTOR status updates, guarded local status-tracking documentation updates such as sdlc_docs/trace_workflow.md and sdlc_docs/03_implementation/backlog_priority.md, pytest-based evidence, approved tests structure, local-write approval, and no remote GitHub or version-control actions without separate explicit approval.
---

# Repository Work Implementation

## Purpose

Support implementation planning and local implementation while preserving approved requirements and architecture. In backlog priority planning mode, create or update `sdlc_docs/03_implementation/` guidance that helps humans manually order unresolved repository issues. In single issue implementation mode, implement exactly one explicitly selected repository issue through developer-owned code design, small pytest-based RED-GREEN-REFACTOR cycles, and remote repository actions left under human control.

## Operating Modes

Choose exactly one mode from the user's request:

- **Backlog priority planning mode:** use when the user asks to organize unresolved issues, suggest implementation order, prepare implementation planning, or create/update `sdlc_docs/03_implementation/`. This mode does not require one selected issue and must not write production code.
- **Single issue implementation mode:** use when the user asks to implement, dry-run, or propose work for one selected issue. This mode requires exactly one selected issue or approved work item and follows the TDD workflow.

If the request is ambiguous, default to backlog priority planning only when the user asks about unresolved issues or priority order; otherwise require one selected issue before implementation.

## Governing Rules

- Work in English.
- Use the exact skill identifier `g-implement-repository-work`; never use a shortened or single-letter alias.
- In single issue implementation mode, implement one explicitly selected issue per execution unless the user explicitly approves a split or combined scope.
- In backlog priority planning mode, suggest a manual priority order for unresolved issues; do not select, assign, move, close, or implement an issue automatically.
- Treat unresolved issues, the selected issue when present, approved Product Requirements, accepted Architecture and ADRs, completed Technical foundation, and current repository as authoritative inputs.
- Do not invent acceptance criteria, product behavior, architecture, estimates, assignees, files, classes, functions, or dependencies.
- Design code in harmony with approved C4 containers, components, ADRs, and acceptance criteria before writing tests or production code.
- Developers may decide modules, classes, functions, route handlers, interactions, and internal schemas only inside existing approved architecture boundaries.
- Maintain hybrid code-level architecture under `sdlc_docs/02_architecture/`: use `sdlc_docs/02_architecture/code-level.md` as the central index and `sdlc_docs/02_architecture/containers/<container>/code-level.md` for per-container code maps when implementation introduces or changes meaningful code structure, route contracts, persistence adapter shape, frontend interaction modules, or cross-component interactions.
- Use Mermaid diagrams in code-level Markdown when sequence, flow, class/module, or object/state diagrams clarify non-trivial implementation design.
- Keep Structurizr DSL canonical for C4 system, container, component, and deployment views. Do not use Structurizr to list every file, class, or function.
- Keep `sdlc_docs/03_implementation/` for backlog priority and implementation coordination artifacts, not architecture ownership.
- Maintain local implementation status tracking after validated single-issue implementation. Update only implementation-owned fields in `sdlc_docs/trace_workflow.md`, `sdlc_docs/03_implementation/backlog_priority.md`, and any existing local implementation tracker that records issue completion, remaining work, current status, or next action. Do not modify earlier phase rows or remote GitHub/project status unless separately approved.
- Do not use code-level design to authorize product behavior, dependencies, persistence strategy, deployment topology, or architecture changes.
- Require an explicit human approval of the visible local implementation proposal before modifying repository files.
- Re-read the issue and affected repository state immediately before local writes. Stop and present an updated proposal when material state changed after approval.
- Implement new behavior through small observable `RED -> GREEN -> REFACTOR` cycles.
- Do not add production behavior before a meaningful related test has failed for the expected reason.
- Use Ping-Pong TDD as an ordered collaboration, not a loose parallel review: `Tester driver` defines the intended behavior as failing tests, then `Developer navigator` implements only enough production code to pass those tests after meaningful RED exists.
- Before the proposal, spawn two subagents simultaneously when available. The tester subagent name must contain `Tester driver`; the developer subagent name must contain `Developer navigator`. If subagents are unavailable, simulate those two named roles explicitly in the proposal.
- Keep the user informed during Ping-Pong TDD: report what each role is doing, which tests are proposed, which tests are created, and the current RED, GREEN, or REFACTOR status after each implementation cycle.
- Do not weaken assertions, delete valid tests, add skips, add `xfail`, or alter expected outcomes merely to obtain green results.
- Use `pytest` for new Python tests. Do not introduce `unittest.TestCase`.
- Use the approved test structure and the templates as flexible guidance, not as rigid formatting law.
- Do not create product BDD scenarios during normal implementation. Reserve `pytest-bdd` feature scenarios for the later validation workflow unless the selected issue explicitly belongs to validation.
- Do not silently change Product Requirements, Architecture, ADRs, dependency strategy, or repository-wide technical foundation.
- Do not commit, push, create pull requests, comment, assign, label, move, close, or reopen issues, or modify a GitHub Project without separate explicit approval. Backlog priority planning produces manual guidance only.
- Do not create persistent TDD reports, transaction files, or implementation statistics. Keep execution evidence in the conversation, tests, diff, and normal version-control history.
- Never claim a command passed unless it was executed and returned the reported result.

## Backlog Priority Planning Preconditions

Confirm all of the following before proposing or writing `sdlc_docs/03_implementation/` artifacts:

1. The repository is identified.
2. Product Requirements are approved.
3. Architecture is `Complete`.
4. Repository preparation is `Complete`.
5. Technical foundation is `Complete`.
6. Unresolved repository issues or approved work items are discoverable.
7. The current working tree and issue list source are known.

Use `scripts/inspect_implementation_readiness.py --mode backlog-priority` before drafting the planning proposal.

Read `references/backlog-priority-policy.md` before ranking unresolved issues.

## Single Issue Implementation Preconditions

Confirm all of the following before proposing implementation:

1. The repository is identified.
2. Exactly one issue, issue URL, or approved work item is selected explicitly.
3. The related requirement or defect is clear enough to test.
4. Product Requirements are approved.
5. Architecture is `Complete` when the work can affect architectural boundaries.
6. Repository preparation is `Complete`.
7. Technical foundation is `Complete`.
8. The repository defines reproducible test and quality commands.
9. The current working tree and baseline test state are known.

Use `scripts/inspect_implementation_readiness.py --mode single-issue --issue <issue>` before drafting the proposal.

Route unresolved work instead of guessing:

- unclear or changed behavior -> `c-manage-product-requirements`;
- material architecture impact -> `d-design-product-architecture`;
- issue does not match approved requirements -> `e-sync-repository-requirements`;
- missing or inadequate repository foundation -> `f-establish-technical-foundation`.

## Work Classification

Classify the selected issue before choosing tests:

- **User story or behavior change:** map approved acceptance criteria to observable tests, then use RED-GREEN-REFACTOR.
- **Bug:** reproduce the confirmed defect with a failing regression test before fixing it.
- **Refactor:** establish a green behavioral baseline or add characterization tests, refactor, and keep the suite green. Do not invent a failing functional test.
- **Documentation or configuration:** use the smallest relevant validator or executable example. Do not force a fake TDD cycle when no executable behavior exists.

## Test Placement

Use the primary purpose and level of the test:

```text
tests/unit/
tests/integration/
tests/regression/
tests/validation/
```

- Place isolated rules, values, functions, and services under `tests/unit/`.
- Place real component collaboration, Flask client, SQLite, filesystem, process, or API-contract checks under `tests/integration/`.
- Place confirmed bug protection under `tests/regression/unit/` or `tests/regression/integration/`, creating only the required level when the defect exists.
- Leave product Gherkin scenarios under `tests/validation/` for the validation workflow.
- Use directory-level `conftest.py` files for shared fixtures at the smallest useful scope.
- Avoid duplicating the same behavior across multiple test levels without a clear reason.

Read `references/test-placement.md` when the correct level is unclear.

## Test Module Style

Use the templates in `assets/` as a preferred visual organization:

- module purpose and test categories in the docstring;
- standard-library, third-party, and local imports;
- fixtures and setup;
- class test cases when grouping improves navigation;
- nominal, negative, edge, and regression sections only when relevant.

Adapt the template. Do not keep empty decorative sections or duplicate the same tests as methods and free functions.

## Developer Code Design

Before proposing local writes, translate the selected issue into a minimal code-level design:

- map planned code elements to approved architecture elements;
- identify modules, classes, functions, route handlers, interactions, and test locations likely needed for this issue;
- identify whether the central `sdlc_docs/02_architecture/code-level.md` index and any relevant `sdlc_docs/02_architecture/containers/<container>/code-level.md` maps must be created, updated, or left unchanged because they already cover the planned structure;
- include Mermaid diagrams when they clarify non-trivial runtime sequence, control flow, class/module relationships, or object/state shape;
- separate developer-owned implementation decisions from material architecture or product decisions that must be routed backward.

Read `references/code-design-policy.md` before drafting or updating code-level design.

## Best Practices

Read only the best-practice markdown references relevant to the selected issue and affected languages/frameworks. Start from `references/best-practices/README.md`, which is an expandable index. Users may add more markdown links to that index over time.

For Python implementation or tests, read `references/best-practices/python-best-practices.md` unless the index points to a more specific Python reference.

When no relevant best-practice reference exists, state that explicitly in the proposal and proceed with the repository's existing conventions.

## Ping-Pong TDD Review

Before the visible proposal, use two simultaneous subagents when the environment supports them to prepare the Ping-Pong cycle:

- **Tester driver subagent:** name the subagent with the words `Tester driver`; derive the tests that express the intended logic, edge cases, test paths, and meaningful RED expectations from approved acceptance criteria or defect evidence.
- **Developer navigator subagent:** name the subagent with the words `Developer navigator`; derive the minimal architecture-aligned implementation strategy that should be written only after the Tester driver tests are created and fail for the expected reason.

The main agent reconciles both outputs into one proposal. If subagents are unavailable, include explicit `Tester driver` and `Developer navigator` notes in the proposal instead of skipping the review.

During approved implementation, preserve this order for each behavior:

1. `Tester driver` proposes or creates the next smallest test that captures intended logic.
2. The main agent runs the test and confirms meaningful RED.
3. `Developer navigator` proposes or creates the minimum production code needed for that exact failing test.
4. The main agent runs the target and related tests and confirms GREEN.
5. The main agent refactors only while tests are green and confirms REFACTOR did not change behavior.

If subagents cannot directly edit files, the main agent may create the test and production code locally, but must explicitly attribute the test intent to `Tester driver` and the implementation response to `Developer navigator`.

Tell the user the current Ping-Pong TDD status at these moments:

- after the two subagents are started or the named role simulation begins;
- after `Tester driver` proposes tests and edge cases that define the intended logic;
- after `Developer navigator` proposes the minimal implementation strategy constrained by those tests;
- after the main agent reconciles both roles into the proposal;
- after each RED test is created and run;
- after each GREEN implementation is completed and tested;
- after each REFACTOR step and confirmation that tests stayed green.

Each status update should name the behavior, test path when known, command result, and whether the cycle is currently RED, GREEN, or REFACTOR.

## TDD Cycle

For each smallest approved behavior:

### RED: Tester Driver

1. Add or modify the smallest relevant test.
2. Run that test directly.
3. Confirm it fails.
4. Confirm the failure represents the missing behavior or reproduced defect.
5. Tell the user which test was created or modified and that the cycle is currently RED.

A meaningful RED is not:

- a syntax error;
- a broken import;
- a missing fixture;
- a misconfigured environment;
- an unrelated pre-existing failure;
- an incorrect assertion.

Correct the test or environment problem and demonstrate the meaningful failure before changing production behavior.

### GREEN: Developer Navigator

1. Add the minimum clear production code required by the approved behavior.
2. Run the target test.
3. Confirm it passes.
4. Run nearby affected tests.
5. Tell the user which implementation behavior passed and that the cycle is currently GREEN.

Do not deliberately create poor code, but do not implement speculative behavior outside the issue.

### REFACTOR

1. Improve names, structure, duplication, or boundary clarity while the tests are green.
2. Run the target and related tests again.
3. Confirm behavior remains unchanged.
4. Tell the user what changed during refactor and that the cycle remains GREEN after REFACTOR.

Repeat the cycle for the next smallest behavior.

Read `references/tdd-policy.md` for bugs, refactors, and failure interpretation.

## Backlog Priority Planning

Use this mode to create or update implementation coordination docs without implementing product behavior.

Create or update:

- `sdlc_docs/03_implementation/README.md`;
- `sdlc_docs/03_implementation/backlog_priority.md`.

The priority document should include:

- unresolved issue inventory and source date;
- suggested implementation order;
- dependency and readiness rationale;
- architecture and foundation implications;
- risks, blockers, and routing notes;
- explicit statement that the order is manual guidance and no GitHub issue or project mutation occurred.

Do not store code-level architecture in `03_implementation`.

## Approval Boundaries

### Approval 1: Backlog Priority Planning Proposal

Before writing planning artifacts, show:

- repository and issue source;
- unresolved issue inventory;
- ranking criteria;
- proposed artifact paths;
- known risks and out-of-scope items;
- statement that no production code, GitHub issue, or project board change is included.

Approval applies only to the latest visible planning proposal.

### Approval 2: Local Implementation Proposal

Before writing, show:

- repository and selected issue;
- related requirement and acceptance criteria;
- current baseline result;
- proposed behaviors and test levels;
- likely files to create or modify;
- code-level architecture files to create, update, or leave unchanged;
- Mermaid diagrams expected or explicit reason they are not useful;
- planned local status-tracking documentation updates after successful validation, including `sdlc_docs/trace_workflow.md` and `sdlc_docs/03_implementation/backlog_priority.md` when present;
- dependencies or foundation changes, if any;
- commands to run;
- known risks and out-of-scope items.

Approval applies only to the latest visible proposal.

### Approval 3: Material Deviation

Stop and request new approval when implementation reveals:

- new product scope;
- changed acceptance criteria;
- a new dependency;
- a material architecture decision;
- a repository-wide foundation change;
- a need to split or combine issues;
- a substantially different implementation strategy.

### Approval 4: Remote or Version-Control Action

Treat each of these as separate from local implementation approval:

- commit;
- push;
- pull request;
- issue comment;
- assignment or label change;
- board transition;
- issue closure or reopening.

## Backlog Priority Planning Workflow

1. Locate the repository root.
2. Confirm backlog priority planning mode.
3. Read unresolved repository issues or approved work items.
4. Read Product Requirements, Architecture, ADRs, Workflow Traceability, and existing `03_implementation` docs.
5. Confirm Repository preparation and Technical foundation are `Complete`.
6. Inspect Git state and issue source freshness.
7. Read `references/backlog-priority-policy.md`.
8. Draft the proposed priority order and artifact update.
9. Present the backlog priority planning proposal.
10. Stop and wait for explicit approval.
11. Create or update `sdlc_docs/03_implementation/README.md` and `sdlc_docs/03_implementation/backlog_priority.md`.
12. Review the diff for scope and manual-only wording.
13. Present the priority result and stop without GitHub, project-board, or version-control actions.

## Single Issue Implementation Workflow

1. Locate the repository root.
2. Read the explicitly selected issue or work item.
3. Confirm that exactly one issue is in scope.
4. Read the related Product Requirements and acceptance criteria.
5. Read the relevant Architecture, ADRs, Workflow Traceability, existing `03_implementation` guidance, and code-level architecture docs.
6. Confirm Repository preparation and Technical foundation are `Complete`.
7. Inspect source, tests, manifests, commands, and Git state.
8. Run the relevant baseline tests and record pre-existing failures.
9. Classify the work as story, bug, refactor, or documentation/configuration.
10. Read relevant best-practice references from `references/best-practices/README.md`.
11. Run Ping-Pong TDD review with `Tester driver` and `Developer navigator` roles and report each role's status to the user.
12. Draft the developer code design and architecture element mapping.
13. Decide whether the central code-level index and per-container code-level maps must be created, updated, or left unchanged with justification.
14. Identify useful Mermaid sequence, flowchart, class, or object/state diagrams for the code-level docs.
15. Map approved behavior to the smallest useful tests and locations.
16. Prepare the exact local implementation proposal, including code design, best-practice references, `Tester driver` and `Developer navigator` notes, Mermaid plan, and TDD plan.
17. Stop and wait for explicit approval.
18. Re-read the issue and affected repository state.
19. Select the smallest remaining approved behavior.
20. Have `Tester driver` propose or create the next test, execute it to confirm meaningful RED, and tell the user the current test status.
21. Have `Developer navigator` propose or create the minimum clear implementation for that RED test, confirm GREEN, and tell the user the implementation status.
22. Refactor while preserving GREEN and tell the user the post-refactor status.
23. Repeat steps 19-22 until the approved issue scope is covered.
24. Run relevant unit, integration, and regression tests.
25. Run the full repository quality commands required by the foundation.
26. Review the final diff for scope, architecture, tests, documentation, Mermaid diagrams, and code-level map alignment.
27. Run `scripts/validate_implementation_result.py` for objective repository checks.
28. Update only local implementation status-tracking documentation with issue evidence, current status, remaining gaps, and next action. Include `sdlc_docs/trace_workflow.md` and `sdlc_docs/03_implementation/backlog_priority.md` when they exist.
29. Present code-design, Ping-Pong TDD evidence, `Tester driver` and `Developer navigator` contributions, status-tracking documentation updates, files changed, command results, and remaining limitations.
30. Stop without committing, pushing, opening a pull request, or changing the issue.
31. Propose any remote or version-control action separately and wait for approval.

Keep `references/process-flowchart.md` aligned with these workflows.

## Completion Gates

Declare the local implementation ready for review only when:

- the selected issue scope is fully covered or remaining gaps are explicit;
- code-level design is aligned with approved architecture and the central/per-container code-level architecture docs exist, were updated, or are explicitly justified as already current;
- useful Mermaid diagrams were included for non-trivial code-level sequence, flow, class/module, or object/state design, or omitted with a clear reason;
- relevant best-practice references were applied or declared unavailable/not applicable;
- Ping-Pong TDD `Tester driver` and `Developer navigator` roles were used or explicitly simulated;
- user-visible status updates reported proposed tests, created tests, and RED-GREEN-REFACTOR outcomes;
- each new behavior has meaningful RED evidence;
- each implemented behavior reached GREEN;
- refactoring preserved GREEN;
- a bug fix has a reproducing regression test;
- relevant unit, integration, and regression tests pass;
- the foundation's full quality commands pass or limitations are reported honestly;
- local implementation status-tracking documentation was updated after validation, or each existing tracker was left unchanged with an explicit reason that it was already current;
- no valid test was weakened, skipped, or deleted to obtain green;
- no unrelated behavior was added;
- no unapproved requirement, architecture, dependency, or foundation change was made;
- the final diff matches the approved issue;
- no remote or version-control action was performed without separate approval.

Read `references/completion-gates.md` before presenting the final result.

## Result Format

Use `references/proposal-and-result-patterns.md` for the proposal and final result. Include concise evidence for each cycle:

```text
Behavior: <approved behavior>
RED: <command and expected failure>
GREEN: <command and passing result>
REFACTOR: <what changed and confirmation that tests stayed green>
```

Do not manufacture RED evidence from memory. State when evidence is unavailable.

## References

- Read `references/backlog-priority-policy.md` before ranking unresolved issues or creating `sdlc_docs/03_implementation/`.
- Read `references/code-design-policy.md` before drafting developer code design or changing central or per-container code-level architecture docs.
- Read `references/best-practices/README.md` before selecting language or framework best-practice references.
- Read `references/test-placement.md` when the correct test level is unclear.
- Read `references/tdd-policy.md` when interpreting RED, GREEN, REFACTOR, bug, refactor, or documentation/configuration work.
- Read `references/completion-gates.md` before presenting the final result.

## Golden Example

Use `references/golden-example/browser-task-board/` as the continuation of the Browser Task Board example. It demonstrates backlog priority planning and implementing `US-0001` through several small TDD cycles without changing architecture or performing GitHub actions.

## Scripts

- `scripts/inspect_implementation_readiness.py`: inspect repository readiness and baseline inputs without modifying files.
- `scripts/validate_implementation_result.py`: perform objective post-implementation checks without judging formatting preferences.
- `scripts/run_regression_tests.py`: validate the skill policy, workflow/flowchart alignment, scripts, and golden example.


## Progressive Audit Resources

- Read `references/golden-example/README.md` only when a progressive concrete example is useful.
- Read `references/process_flowchart.md` only for human explanation or audit.
