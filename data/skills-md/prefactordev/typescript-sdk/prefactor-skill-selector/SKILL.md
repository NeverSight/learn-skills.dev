---
name: prefactor-skill-selector
description: Use when choosing which Prefactor SDK skill to load for agent instrumentation or for building a custom provider integration on top of @prefactor/core.
---

# Prefactor Skill Selector

Use this file as a router for Prefactor skills.

## Available Skills

- `skills/bootstrap-existing-agent-with-prefactor-cli/SKILL.md`: bootstrap Prefactor resources for an existing agent using CLI (`profile`, `environment`, `agent`, `agent_instance`) and prepare runtime env vars/package choice.
- `skills/instrument-existing-agent-with-prefactor-sdk/SKILL.md`: instrument an existing agent with Prefactor SDK so coding tools can see runs, llm/tool spans, token usage, and failures.
- `skills/create-provider-package-with-core/SKILL.md`: create a new provider package as a thin adapter over `@prefactor/core` with core-first boundaries and tracing conventions.

## Selection Rules

- If the request is about provisioning Prefactor resources via CLI for an existing app, load `skills/bootstrap-existing-agent-with-prefactor-cli/SKILL.md` first.
- If the request is about adding telemetry to an existing agent without rewriting business logic, load `skills/instrument-existing-agent-with-prefactor-sdk/SKILL.md`.
- If the request is about creating a custom provider adapter with `@prefactor/core`, load `skills/create-provider-package-with-core/SKILL.md`.

## Default Workflow

When instrumenting an existing agent, default to this order:

1. Run `skills/bootstrap-existing-agent-with-prefactor-cli/SKILL.md` to set up resources (`environment`, `agent`, `agent_instance`).
2. Install required Prefactor npm package(s) via the project's package manager.
3. Choose the matching adapter package if available (`@prefactor/langchain`, `@prefactor/ai`, `@prefactor/openclaw`).
4. For adapter-style instrumentation (`@prefactor/langchain` or `@prefactor/ai`), keep `init`, `withSpan`, and `shutdown` imports from that same adapter package (or pass an explicit tracer when using core `withSpan`).
5. If no matching adapter package exists, use `skills/create-provider-package-with-core/SKILL.md`.
6. Instrument the existing agent with `skills/instrument-existing-agent-with-prefactor-sdk/SKILL.md`.
