---
name: spring-ai
description: >-
  Diagnose and operate Spring AI projects with version-aware Maven or Gradle checks for ChatClient,
  advisors, retrieval, conversation memory, tool/MCP boundaries, streaming, configuration, and
  observability. Use for setup compatibility, local smoke checks, and failure triage; do not use for
  provider-specific model evaluation, general Java/Spring development, security threat modeling, or
  production rollout governance.
license: MIT
compatibility: Requires Python 3.8+ standard library; Maven/Gradle are optional and only needed to run a project build.
metadata:
  tags: spring-ai, spring-boot, java, maven, gradle, chatclient, rag, mcp, diagnostics
  verified_date: "2026-09-14"
  supported_spring_ai: 2.0.1 (current stable documentation); 1.0.9 maintenance reference
---

# Spring AI

Use this operational skill to inspect a real Maven or Gradle Spring AI project before changing it. The included diagnostic CLI is offline and provider-neutral: it reads build files, application configuration, and source to report compatibility clues, unsafe defaults, missing conversation IDs, streaming prerequisites, tool/MCP boundaries, retrieval configuration, and observability risks. It never sends prompts or exposes API-key values.

## Entry check

Confirm the project root and whether the task is read-only or will modify configuration/code. Read-only diagnosis can proceed. Before the first state-changing action, confirm the target project, scope, and rollback path (usually a reviewed commit or revert); the CLI itself is read-only.

Run:

```sh
python3 spring-ai/scripts/spring_ai_check.py --root /path/to/project --json
```

The result is stable JSON with `status`, `project`, `facts`, `findings`, and `errors`. Exit 0 means no error-severity finding; exit 1 means an error-severity finding or warnings promoted by `--strict`; exit 2 means an invalid invocation or unreadable project.

## Workflow

1. Run the checker and retain its JSON output with the project revision.
2. Resolve build compatibility findings against the official Spring AI and Spring Boot documentation in `references/source-index.md`; do not infer support from a transitive dependency alone.
3. Inspect ChatClient advisor order and parameters. Every memory-advisor call needs an explicit conversation identifier derived from the application’s authenticated/session boundary; never use a shared default.
4. For retrieval, verify document ownership/authorization before retrieval context enters a prompt. Test empty retrieval, stale data, provider errors, and latency separately.
5. For tools and MCP, treat model tool requests as untrusted proposals. The application owns authorization and execution. Bound tool names, arguments, timeout, retry, side effects, and audit fields. Verify MCP transport and schema against the current project dependency.
6. For streaming, preserve partial output as provisional until completion; test cancellation, timeout, disconnect, and failed completion. Do not treat a partial stream as a committed answer or side effect.
7. Keep prompt/completion logging disabled by default in production. If enabled temporarily, document redaction, access, retention, and rollback.
8. Run the project’s own tests/build when dependencies and provider credentials are available. The checker does not prove provider connectivity, model quality, RAG correctness, or production readiness.

## Scope and routing

- ChatClient/advisors, Spring configuration, local diagnostics, and framework troubleshooting belong here.
- Model quality, evaluator design, statistical comparisons, and trace schemas belong to `agent-evals-and-observability`.
- Authority, fallback, disablement, budgets, and rollout belong to `agent-production-operations`.
- Threat modeling and security implementation belong to `secure-software-engineering`.
- General Java/Spring application design belongs to the relevant engineering skill.

## Version posture

The official documentation currently presents Spring AI 2.0.1 as the latest stable line and retains a 1.0 reference (1.0.9). APIs differ across lines: for example, current 2.0 documentation describes `ToolCallingAdvisor` as the ChatClient tool loop, while 1.x applications may use model-internal tool loops. The checker reports observed versions and flags uncertainty; it does not rewrite dependencies or claim that a version combination is supported without a primary compatibility source. Re-check `references/source-index.md` and release notes when upgrading.

## Completion

Stop when the project’s build/config/source facts, findings, owner routes, and limitations are recorded, or when an external dependency (provider credentials, unavailable build tool, private artifact repository) is explicitly marked blocked. Do not claim a successful live smoke test from static diagnostics.
