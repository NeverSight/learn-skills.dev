---
name: qa-methodology
description: >-
  Design and apply QA methodology for software teams: test strategy, regression testing,
  CI failure triage, test automation, quality gates and metrics, risk-based testing,
  exploratory testing, test design techniques, AI code quality gates (independent
  verification, artifact provenance, spec-first oracles, AI-review-comment triage,
  acceptance-criteria testability for Spec-Driven Development), mutation-guided test hardening and review evidence (surviving mutants,
  weak assertions, diff-aware mutation testing), agentic eval design (dataset test design, judge-as-system-under-test,
  flaky-eval discipline), QA career levels (Senior/Staff/Principal), and SDET
  engineering (test infrastructure, gTAA, CI/CD integration). Do not use for
  root-cause debugging of production incidents, security implementation or threat
  modeling, or evaluation framework governance and statistical analysis — route those
  to systematic-debugging, secure-software-engineering, and
  agent-evals-and-observability respectively.
license: MIT
compatibility: >-
  Platform-agnostic methodology. Scripts require Python 3.8+ (stdlib only).
  No CI platform, test framework, or AI agent mandate.
metadata:
  source_repo: hermes-profiles
  skill_version: "2.0.0"
  tags: qa, testing, quality-assurance, test-automation, regression, CI, quality-gates, risk-based-testing, exploratory-testing, mutation-testing, SDET, agentic-evals, AI-code-quality
---

# QA Methodology

Senior-to-principal QA and SDET methodology: test strategy, automation, regression, risk-based prioritization, exploratory testing, quality gates, AI code quality gates for agentic Spec-Driven Development, agentic eval design, career leveling, and SDET engineering.

## Ownership

| You own | You don't own |
|---------|--------------|
| Test strategy — what to test, at what level, with what priority | Root-cause debugging — route to [systematic-debugging](../systematic-debugging/SKILL.md) |
| Test automation — framework selection, parallelism, flaky management | Security implementation and threat modeling — route to [secure-software-engineering](../secure-software-engineering/SKILL.md) |
| E2E automation strategy and coverage decisions | Operating a browser test tool (Playwright) — authoring/running specs, selectors, network mocking, scraping — route to [playwright](../playwright/SKILL.md) |
| Regression suites — selection, impact analysis, suite evolution | Spec pipeline mechanics and gate verdicts — route to [spec-driven-development](../spec-driven-development/SKILL.md) |
| Quality gates — blocking vs advisory, metrics, DORA | Eval framework governance and statistics — route to [agent-evals-and-observability](../agent-evals-and-observability/SKILL.md) |
| Risk-based testing — P×I scoring, prioritization, registers | Verification verdicts against explicit criteria — route to [verification-methodology](../verification-methodology/SKILL.md) |
| Exploratory testing — SBTM charters, heuristics, tours | Feature implementation — that's the developer |
| AI code quality gates — independent verification, AC testability | Production monitoring and incident response — that's SRE |
| Mutation-guided test hardening — bounded mutation review evidence and survivor triage | Verification verdicts against explicit criteria — route to [verification-methodology](../verification-methodology/SKILL.md) |
| Agentic eval design — dataset design, judge bias, flaky-eval discipline | |
| QA career levels — Senior/Staff/Principal scope progression | |
| SDET engineering — test infrastructure, gTAA, CI/CD integration | |

## Core Principles

**If it isn't tested, it's broken.** Untested code is code whose failure mode hasn't been discovered yet.

**Quality is a property of the process, not the artifact.** Testing at the end doesn't create quality. Quality is designed in through strategy, automation, and gating throughout the cycle.

**Test behavior, not implementation.** Tests coupled to behavior survive refactoring; tests coupled to implementation break on it.

**Risk drives priority.** Not everything deserves equal test investment. Score probability × impact, then allocate accordingly.

**Flaky tests are worse than no tests.** A nondeterministic failure trains teams to ignore all failures. Quarantine on detection; rerun once, never twice.

**Independent verification is non-negotiable.** The implementing agent (or developer) must not self-verify. Separate session, fresh context, no shared priors.

## Loading Guide

| File | Load when |
|------|-----------|
| `references/test-strategy.md` | Designing a test strategy — pyramid shape, shift-left/right, cost-of-failure, coverage as diagnostic |
| `references/test-automation.md` | Selecting frameworks, parallelism/sharding, flaky quarantine, predictive ML test selection, mutation-guided hardening |
| `references/quality-gates-and-metrics.md` | Designing quality gates (blocking vs advisory), DORA metrics, vanity-vs-actionable metrics, mutation testing |
| `references/regression-testing.md` | Building regression suites — impact analysis, selection math, suite evolution, shift-right feedback |
| `references/test-data-management.md` | Test data strategy — fixtures, factories, time-travel, masking, GDPR/PII rules |
| `references/performance-testing.md` | Load/stress/soak testing — k6/Locust/Gatling/JMeter, SLO thresholds, CI cadence |
| `references/security-testing.md` | Security testing — OWASP Top 10:2025, STRIDE, SAST/DAST/SCA, supply chain/SBOM |
| `references/ci-failure-triage.md` | CI is red — exit-code taxonomy (1/2/126/127/137/139/143), git bisect, flake-vs-failure protocol |
| `references/test-debugging.md` | A test that should pass is failing — CI-vs-local divergence, ordering/shared state, mock binding |
| `references/risk-based-testing.md` | Prioritizing by risk — P×I formula, 5×5 matrix, risk workshop, register, reassessment triggers |
| `references/exploratory-testing.md` | Exploratory testing — SBTM, charter writing, SFDIPOT/HICCUPPS heuristics, tours |
| `references/test-design-techniques.md` | Choosing test design techniques — EP, BVA, decision tables, state transition, pairwise, error guessing |
| `references/qa-career-levels.md` | QA career growth — Senior/Staff/Principal scope, leveling mechanics, archetypes, misconceptions |
| `references/sdet-engineering.md` | SDET role and skills — gTAA/TAF architecture, POM, SOLID for tests, build-vs-buy, testability |
| `references/ai-code-quality-gates.md` | Reviewing AI-generated code — independent verification, AC testability, agent-test quality, human-in-the-loop |
| `references/ai-test-artifact-evidence.md` | Provenance, spec-first oracle review, generated-review triage, workflow evidence, and emergency exceptions for AI-assisted QA |
| `references/agentic-eval-design.md` | Designing agent evals — dataset test design, judge bias, flaky-eval discipline, CI gate tiers, replay |
| `templates/test-strategy.md` | Producing a test strategy document — fill in scope, risk tiers, level allocation, automation targets |
| `templates/risk-register.md` | Recording risk assessment results — fill in items, P×I scores, owners, mitigations |
| `templates/exploratory-charter.md` | Writing an SBTM charter — fill in target, resources, discovery goal, timebox |
| `templates/bug-report.md` | Filing a structured bug report — fill in reproduction steps, expected vs actual, severity |
| `templates/verification-plan.md` | Planning independent verification — fill in AC-to-method traceability, verifier assignment, exit criteria |
| `templates/mutation-review.md` | Recording bounded mutation review scope, classifications, survivor tests, and independent evidence |
| `templates/ai-assisted-verification-note.md` | Recording AI-assisted test/review provenance, independent oracle checks, and evidence disposition |
| `assets/risk-matrix-grid.md` | Scoring risks during a workshop — 5×5 P×I grid with zone thresholds |
| `assets/test-design-techniques-checklist.md` | Selecting techniques for a feature — quick-reference checklist mapping scenario type to technique |
| `assets/qa-definition-of-done.md` | Defining release readiness — QA contribution to definition of done |
| `scripts/risk-prioritize.py` | Computing P×I rankings from a risk-items JSON file |
| `scripts/check-ac-testability.py` | Checking acceptance criteria for vague verbs and missing observable outcomes |
| `evals/evals.json` | Running output-quality evals for this skill (schema v1, 15 cases) |

## Scripts

| Script | Invocation | Purpose |
|--------|-----------|---------|
| risk-prioritize | `python3 scripts/risk-prioritize.py --json <input.json>` | Reads risk items (probability, impact), computes P×I scores, emits ranked JSON |
| check-ac-testability | `python3 scripts/check-ac-testability.py <spec.md>` | Scans acceptance criteria for untestable language, exits non-zero if any are flagged |

## Triggers

Load this skill when the task involves:

- **Test strategy** — designing what/how/priority to test for a project or feature
- **Regression testing** — building, selecting, or evolving regression suites
- **CI triage** — diagnosing CI failures, exit codes, flake-vs-real classification
- **Test automation** — framework selection, parallelism, flaky quarantine, ML selection
- **Quality gates** — gate design, blocking vs advisory, metrics, DORA
- **Mutation-guided test hardening** — diff-aware mutation scope, surviving mutants, weak assertions, and review evidence
- **Risk-based testing** — P×I scoring, risk registers, prioritization workshops
- **Exploratory testing** — SBTM charters, oracle heuristics, session debriefs
- **Agentic evals** — eval dataset design, judge bias, flaky-eval discipline, CI tiers
- **SDD gate review** — QA ownership at spec-driven gates, AC testability, independent verification
- **SDET** — test infrastructure engineering, gTAA, CI/CD integration, career scope

## When not to use

Route to the named sibling skill instead:

- [spec-driven-development](../spec-driven-development/SKILL.md) — writing specs, running the SDD pipeline, gate verdict format, revision loops
- [agent-evals-and-observability](../agent-evals-and-observability/SKILL.md) — eval framework governance, statistical comparisons, telemetry and privacy controls, grader implementation
- [verification-methodology](../verification-methodology/SKILL.md) — collecting evidence and rendering verdicts against explicit pass/fail criteria
- [release-engineering](../release-engineering/SKILL.md) — composing test evidence into release-candidate readiness, promotion, go/no-go, production rollout, and rollback decisions; QA owns test strategy and gate semantics
- [systematic-debugging](../systematic-debugging/SKILL.md) — root-cause analysis of production incidents, bug reproduction, fault localization
- [secure-software-engineering](../secure-software-engineering/SKILL.md) — security implementation, threat modeling, secure defaults, dependency evaluation
- [playwright](../playwright/SKILL.md) — operating the Playwright tool itself: authoring and running E2E specs, selector robustness, network mocking, headless scraping, and headed debugging

## Stop and Exit Conditions

- **Test strategy complete when:** strategy document names risk tiers, level allocation, automation targets, and exit criteria for each tier.
- **Risk assessment complete when:** every identified risk has a P×I score, an owner, and a mitigation or acceptance decision recorded in the register.
- **CI triage complete when:** failure is classified (flake vs real, env vs code), root cause is localized, and a fix or escalation path is identified.
- **Gate review complete when:** every acceptance criterion maps to a verification method, the verifier is independent of the implementer, and evidence is attached.
- **Bounded escalation:** stop after three non-converging diagnostic passes and report the evidence collected so far.
