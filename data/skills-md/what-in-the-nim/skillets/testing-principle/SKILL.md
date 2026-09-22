---
name: testing-principle
description: Apply behavior-focused pytest design when writing, revising, or reviewing Python tests.
---

# Testing Principle

Optimize for realistic behavior and readability before speed or isolation.

## Composition

Explicit user requirements and repository conventions come first. TDD controls test-first sequencing; this skill controls test design, including the private-logic exception below. Preserve agreed test boundaries; resolve conflicts with an explicit public-only requirement before adding private tests. Use [pytest-skill](../pytest-skill/SKILL.md) for syntax.

## Process

1. **Locate.** Identify the source module and public interface; classify unit versus integration coverage. Preserve existing test layout. For a new layout, mirror source paths under `tests/unit` (`src/acme/webhooks/sender.py` → `tests/unit/acme/webhooks/test_sender.py`); organize `tests/integration` by boundary or workflow.
2. **Model behavior.** Identify outcomes, failure modes, and input boundaries. Group related scenarios in stateless, behavior-named classes such as `TestWebhookFail`, without `__init__`. Classes represent behaviors, not production classes or shared setup.
3. **Choose collaborators.** Prefer real domain objects and in-process implementations. Replace only unavailable, destructive, nondeterministic, or prohibitively costly boundaries; runtime alone does not justify mocking. Prefer small fakes to interaction-heavy mocks. For LLM calls, apply the live-testing section below.
4. **Build fixtures.** Move complex or repeated construction into fixtures; keep actions and assertions visible. Use factory fixtures for variants. Choose the narrowest safe scope: function for mutable state, class/module for safely shared expensive setup, session for immutable or explicitly resettable resources. Broader scope requires reliable isolation.
5. **Parametrize.** Combine input variations sharing behavior; separate cases with different setup, action, or outcomes. Cover relevant normal, boundary, empty, invalid, and regression inputs. Add readable IDs when values alone are unclear.
6. **Assert contracts.** Prefer public outcomes and state over call order, representation, or incidental interactions. Private tests are exceptions for critical, complex or safety-sensitive logic that public tests cannot cover precisely enough. Keep them few, justify their coupling in the name or a short comment, and avoid using them to bypass awkward public behavior.
7. **Verify.** Run the narrowest relevant pytest target. Inspect collected node IDs for discoverable files, classes, and cases; verify selection by file and class/node ID. Audit every new or changed test against steps 1–6.

## Live LLM testing

For tests that can consume hosted LLM tokens, reuse an existing live-test switch or add `--run-live-llm`. A fixture selects deterministic mocked responses by default and the real provider in live mode. Change only the LLM boundary: run parsing and downstream behavior in both modes, rather than skipping the test by default.

Run live mode only when requested or required by project validation policy, with credentials available. Otherwise report live coverage as unverified.
