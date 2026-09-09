---
name: playwright-skill
description: Flagship Playwright skill pack for planning, authoring, debugging, documenting, and operationalizing Playwright. Routes E2E, API, component, visual, accessibility, CI/CD, coverage, docs, CLI automation, and handoff workflows.
metadata:
  dispatcher-layer: information
  dispatcher-lifecycle: active
  dispatcher-category: testing
  dispatcher-capabilities: ui-automation, playwright, coverage-planning, automation-routing
  dispatcher-accepted-intents: implement_ui_confirmation_test, plan_playwright_coverage, diagnose_playwright_failure, document_playwright_tests
  dispatcher-input-artifacts: repo_context, requirements, test_case_set, existing_playwright_suite, failing_ui_scenario
  dispatcher-output-artifacts: playwright_test, coverage_plan, root_cause_report, automation_docs, routing_request
  dispatcher-stack-tags: playwright, ui-testing, browser-automation
  dispatcher-risk: high
  dispatcher-writes-files: true

---

# Playwright Skill Pack

> **Author:** jovd83 | **Version:** 2.1.1


Use this root skill as the package entrypoint for general Playwright requests. It is responsible for routing work to the smallest useful subskill, applying the shared standards of this repository, and keeping the package boundaries clear.

Do not load every guide by default. Read only the subskill and reference files that materially help with the current task.

## Responsibilities

- Route broad or ambiguous Playwright requests to the right subskill.
- Apply the shared testing standards used across this repository.
- Keep core testing guidance separate from optional planning, documentation, and handoff workflows.

## Boundaries

- Do not duplicate deep implementation guidance that already lives in a focused subskill.
- Do not treat this repository as shared-memory infrastructure. If durable cross-agent knowledge is needed beyond one repo or skill, integrate an external shared-memory skill instead of storing it here implicitly.

## Dispatcher Integration

Use `skill-dispatcher` as the primary integration layer whenever this package needs help from another skill or when a broader orchestrator is deciding whether Playwright is the right execution layer.

- Prefer dispatcher-led routing by intent, especially for tasks such as `implement_ui_confirmation_test`, `render_test_artifact`, and `generate_test_data`.
- Prefer the repository's native browser automation stack over Playwright when repo evidence points elsewhere.
- Use Playwright as the default browser automation choice only when the repository supports it already, the user asks for it, or dispatcher policy explicitly selects it.
- Treat direct paths to sibling skills as a compatibility fallback, not as the primary routing contract.

## Routing Map

| Need | Use |
|---|---|
| Generic Playwright request or unclear starting point | [orchestrator/SKILL.md](orchestrator/SKILL.md) |
| Writing or fixing Playwright tests | [core/SKILL.md](core/SKILL.md) |
| CI, sharding, artifacts, containerized execution | [ci/SKILL.md](ci/SKILL.md) |
| Page object structure or fixture-vs-helper decisions | [pom/SKILL.md](pom/SKILL.md) |
| Cypress or Selenium migration | [migration/SKILL.md](migration/SKILL.md) |
| CLI browser automation | [playwright-cli/SKILL.md](playwright-cli/SKILL.md) |
| Requirements extraction | [analysis/SKILL.md](analysis/SKILL.md) |
| Coverage planning | [coverage_plan/generation/SKILL.md](coverage_plan/generation/SKILL.md) and [coverage_plan/review/SKILL.md](coverage_plan/review/SKILL.md) |
| Coverage-plan maintenance | [coverage_plan/auto-sync/SKILL.md](coverage_plan/auto-sync/SKILL.md) |
| Narrative test documentation or format conversion | Dispatch `render_test_artifact` through `skill-dispatcher`; fall back to `C:\projects\skills\test-artifact-export-skill\SKILL.md` when needed |
| Automation-code documentation or failure diagnosis | [documentation/tests/SKILL.md](documentation/tests/SKILL.md) or [documentation/root_cause/SKILL.md](documentation/root_cause/SKILL.md) |
| Human or agent handoff workflows | [documentation/handover/SKILL.md](documentation/handover/SKILL.md) and [documentation/session-state/SKILL.md](documentation/session-state/SKILL.md) |
| Test-case export to Xray, Zephyr, TestLink, or TestRail | Dispatch `render_test_artifact` through `skill-dispatcher`; fall back to `C:\projects\skills\test-artifact-export-skill\SKILL.md` when needed |
| Test-management integrations after export exists | [mappers/](mappers/), and [reporters/](reporters/) subskills |
| IDE-specific setup help | [installers/](installers/) subskills |

## Operating Workflow

1. Inspect the existing repository, tests, and requirements before prescribing structure.
2. Infer the user's intent when it is clear; ask for clarification only when the decision would materially change the artifact or scope.
3. Choose the smallest subskill that can complete the task well.
4. Load only the relevant reference guides or scripts for that path.
5. Produce concrete outputs such as code, plans, documentation, or validation results instead of generic advice.

## Shared Standards

- Prefer user-facing locators and web-first assertions.
- Avoid placeholder tests, placeholder assertions, and fake completion claims.
- Keep state in fixtures, UI behavior in page objects when repetition or complexity justifies them, and helpers stateless.
- Mock external dependencies selectively; do not hide the behavior of the system under test behind unnecessary mocks.
- Keep requirements, plans, documentation, and executable tests traceable to one another when the workflow includes planning or documentation.

## Gotchas

- **Context Weight**: This is a large skill pack. Avoid loading the full file registry or the root skill for simple tasks; jump straight to the smallest relevant subskill (e.g., `core/`) to keep reasoning sharp.
- **Path Resolution**: When providing file paths to subskills, ensure they are absolute or clearly relative to the project root. Subskills often have their own local standards for where they look for tests.
- **Statelessness**: Unless you use the `documentation/session-state/` workflow, assume each agent interaction is stateless. If you need to "resume" work, you must explicitly read the previous session's artifacts or handoffs.
- **Playwright-Specific Pitfalls**: For detailed technical gotchas regarding nested locators, async races, and flaky tests, always refer to [core/common-pitfalls.md](core/common-pitfalls.md).

## Memory Model

- Runtime memory: ephemeral reasoning and task state for the current thread.
- Project-local persistent memory: artifacts such as coverage plans, handovers, and session-state files created inside the target repository.
- Shared memory: optional and external. Promote information into shared memory only when it is stable, reusable across tasks, and belongs outside this skill pack.

## Package Shape

- `core/`, `ci/`, `pom/`, `migration/`, and `playwright-cli/` are the reusable testing foundation.
- `analysis/`, `coverage_plan/`, and `documentation/` add planning and traceability workflows.
- `documentation/handover/` and `documentation/session-state/` are optional operational workflows for multi-session or multi-operator work.
- `mappers/`, `reporters/`, `reporting/`, and `installers/` are optional extensions, not prerequisites for ordinary Playwright authoring.
- The standalone `test-artifact-export-skill` skill remains the canonical formatter/exporter for narrative test cases and tool-ready artifacts, but reach it through `skill-dispatcher` first when cross-skill routing is available.

## Use the Root Skill Well

- Stay at the root only for routing, package discovery, or repo-wide standards.
- Move into a focused subskill as soon as the task is specific enough.
- Keep the package coherent: update the README, changelog, metadata, and validation artifacts when repo-level behavior changes.