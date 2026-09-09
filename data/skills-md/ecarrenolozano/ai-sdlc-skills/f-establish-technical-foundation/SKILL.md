---
name: f-establish-technical-foundation
description: Establish or simplify a repository technical foundation after product requirements, architecture, and repository preparation are approved. Use before implementing product issues when the repository needs a reproducible source layout, dependencies, local run commands, pytest and pytest-bdd, quality checks, CI, and concise developer documentation. Require a visible proposal and human approval before local writes, create only technical scaffolding and smoke tests, preserve approved architecture, and never implement user-story behavior or perform remote GitHub actions.
---

# Establish Technical Foundation

## Purpose

Prepare the smallest repository foundation that lets developers implement approved work safely and reproducibly. Keep the workflow practical: inspect, propose, obtain approval, establish the foundation, validate it, and request final acceptance.

## Core Rules

- Work in English.
- Use the complete identifier `f-establish-technical-foundation`.
- Treat approved Project Context, Product Requirements, Architecture, ADRs, Workflow Traceability, and the current repository as authoritative.
- Start only after Project Context, Product Requirements, Architecture, and Repository preparation are complete.
- Preserve approved product behavior and architecture boundaries.
- Do not implement user stories, business rules, product APIs, product persistence, or product UI behavior.
- Create only technical scaffolding, configuration, developer commands, CI, and technical smoke tests.
- Prefer existing viable tooling over replacement.
- Use `pytest` for new Python tests and configure `pytest-bdd` for later validation work.
- Require explicit approval of the visible local-change proposal before modifying files.
- Require explicit final acceptance before changing Technical foundation to `Complete`.
- Re-read affected files immediately before writing. Re-propose when relevant state changed.
- Do not install interpreters or dependencies, commit, push, create pull requests, modify issues, or move project items without separate approval.
- Do not create persistent assessment reports or execution logs. Put durable instructions in existing repository documentation.
- Never claim a command passed unless it was executed successfully.

## Canonical Inputs

Read these when present:

```text
sdlc_docs/00_inception/project_context.md
sdlc_docs/01_requirements/product_requirements.md
sdlc_docs/02_architecture/architecture.md
sdlc_docs/02_architecture/adr/
sdlc_docs/trace_workflow.md
README.md
WORKFLOW.md
CONTRIBUTING.md
pyproject.toml or the approved manifest
lockfiles
src/ and other approved source roots
tests/
docs/development.md
.github/workflows/
.pre-commit-config.yaml
```

Run `scripts/inspect_technical_foundation.py` before drafting the proposal.

## Minimum Foundation

Adapt paths to the approved architecture. A typical Python browser application may use:

```text
frontend/
src/<python-package>/
tests/
├── unit/
├── integration/
├── regression/
└── validation/
    ├── features/
    └── steps/
```

Establish only what the repository needs now:

- source boundaries matching the approved architecture;
- dependency and lockfile strategy;
- reproducible install and local run commands;
- pytest and pytest-bdd configuration;
- minimal technical smoke tests;
- linting, formatting, typing, coverage, and build commands when applicable;
- minimal CI using the same commands;
- concise developer and test documentation;
- generated-file exclusions;
- Workflow Traceability updates after approval.

Do not create speculative product packages, empty architecture layers, product scenarios, or fake coverage.

## Pytest Policy

Use the conventions in `references/pytest-policy.md` and the templates in `assets/`.

Keep these primary categories:

- `tests/unit/`: isolated technical or product units.
- `tests/integration/`: collaboration among real components.
- `tests/regression/`: confirmed defects only; create subdirectories later when needed.
- `tests/validation/`: future approved behavior scenarios using pytest-bdd.

During foundation work:

- create only technical smoke tests;
- keep regression and validation categories empty unless real approved content already exists;
- allow scoped `conftest.py` files;
- use the visual module template as guidance, not as a rigid parser contract;
- do not create `unittest.TestCase` tests;
- do not generate product Gherkin scenarios.

## Distribution and Local Execution

Do not turn packaging into a larger problem than the approved scope requires.

When a local browser application is explicitly intended to run from a repository checkout, document that convention clearly. In that case, a successful Python wheel build validates the Python package only and does not need to represent the complete browser application.

When the approved architecture requires an installable or deployable application artifact, route material packaging decisions to `d-design-product-architecture` instead of inventing them here.

The Browser Task Board golden example uses checkout-based local execution.

## Approval Boundaries

### Local Foundation Proposal

Before changing files, show:

- repository and current state;
- approved constraints;
- proposed source and test structure;
- dependencies and commands;
- files to create, modify, preserve, or remove;
- technical smoke tests;
- CI and documentation changes;
- environment actions requiring developer approval.

Stop and wait for approval.

### Final Acceptance

After applying and validating the approved changes, show:

- changed files;
- commands and exit codes;
- passed, failed, intentionally empty, or unavailable checks;
- remaining limitations;
- confirmation that no product behavior or remote action was performed.

Keep Technical foundation at `Pending Approval` until the user explicitly accepts the result.

## Workflow

1. Locate the repository root.
2. Read approved context, requirements, architecture, ADRs, and workflow trace.
3. Verify Architecture and Repository preparation are complete.
4. Inspect manifests, source roots, tests, CI, and developer documentation.
5. Run `scripts/inspect_technical_foundation.py` in read-only mode.
6. Identify only the missing or contradictory foundation elements.
7. Route product ambiguity to `c-manage-product-requirements` and material architecture conflicts to `d-design-product-architecture`.
8. Define the smallest viable foundation using existing approved tooling.
9. Define pytest, pytest-bdd, test categories, and technical smoke tests.
10. Define reproducible commands, quality checks, minimal CI, and concise documentation.
11. Present the exact local-change proposal and stop for approval.
12. Re-read affected files and repository state after approval.
13. Apply only the approved foundation changes without product behavior.
14. Run repository commands and `scripts/validate_foundation.py`.
15. Fix foundation defects without weakening valid tests or checks.
16. Review the final diff against the approved proposal.
17. Set Technical foundation to `Pending Approval` and request final acceptance.
18. After explicit acceptance, set Technical foundation to `Complete` and hand off to `g-implement-repository-work` when installed.

See `references/process-flowchart.md` for the matching visual workflow.

## Validation

Run from the repository root:

```bash
python3 .agents/skills/f-establish-technical-foundation/scripts/validate_foundation.py .
```

Also run the commands declared by the repository. A typical uv-based project uses:

```bash
uv sync --locked --all-groups
uv run pytest --collect-only
uv run pytest tests/unit
uv run pytest tests/integration
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv build
```

Report intentionally empty categories accurately. Do not add fake tests merely to avoid pytest exit code 5.

Use `uv lock` followed by `uv sync --all-groups` only for a deliberate dependency update.

## Completion Gate

Use `references/completion-gates.md`. The foundation is ready only when:

- approved architecture boundaries are represented;
- installation and local execution are documented;
- pytest and pytest-bdd are configured;
- required test categories exist;
- technical smoke tests and configured quality checks pass;
- CI uses the documented reproducible commands;
- developer documentation is sufficient to start work;
- no product story was implemented;
- final human acceptance was received.

## Resources

Read only when needed:

- `references/foundation-rules.md`
- `references/pytest-policy.md`
- `references/completion-gates.md`
- `references/process-flowchart.md`
- `references/golden-example/browser-task-board/README.md`
- `assets/unit_test_template.py`
- `assets/integration_test_template.py`
- `assets/regression_test_template.py`
- `assets/bdd_feature_template.feature`
- `assets/test_bdd_scenario_template.py`

## Handoffs

- Product behavior ambiguity -> `c-manage-product-requirements`.
- Material architecture conflict -> `d-design-product-architecture`.
- GitHub issue mismatch -> `e-sync-repository-requirements`.
- Accepted technical foundation -> `g-implement-repository-work` when installed.

Never invoke another skill automatically.


## Progressive Audit Resources

- Read `references/golden-example/README.md` only when a progressive concrete example is useful.
- Read `references/process_flowchart.md` only for human explanation or audit.
