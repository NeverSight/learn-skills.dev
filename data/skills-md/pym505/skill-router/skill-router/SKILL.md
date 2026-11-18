---
name: skill-router
description: Use when handling a non-trivial request to select the smallest useful skill set by purpose, artifact, provider, runtime, freshness, risk, and repository rules, with live catalog fallback for incomplete exposed catalogs.
---

# Skill Router

Route first. Act only after every selected `SKILL.md` is read completely.

## Inputs and Catalog

Use the user request, nearest `AGENTS.md`, workspace/runtime ownership, authorization boundary, and the currently exposed skill/plugin names, descriptions, paths, and invocation policies.

The exposed catalog is the fast path. When it is shortened, incomplete, or ambiguous, read [Live Catalog Search](references/catalog-search.md) and scan current discovery roots and enabled plugins. The scanner is recall support, not a registry or routing authority.

Never maintain a static skill, repository, engine, provider, or path table. Keep skills in their existing supported locations; paths are semantic evidence, not placement rules or allowlists. A new skill participates through its live metadata without a router edit.

## Baseline

- Follow the user's and repository's required skills when available. This router has no mandatory companion skills.
- Surface material assumptions, choose the smallest sufficient scope, and preserve unrelated work.
- Keep communication concise without omitting uncertainty or verification evidence.
- Before claiming completion, inspect fresh evidence appropriate to the task. Skill selection alone is not evidence of completion.

## Dynamic Selection

1. Parse purpose, action, object, artifact, runtime, provider, freshness, risk, and requested side effect.
2. Add explicit user selections and repository-required skills as mandatory candidates.
3. Compare remaining facets semantically with exposed descriptions, triggers, and exclusions.
4. If the fast path is incomplete or ambiguous, use live catalog search. Its text score is recall only; make the final choice semantically from the returned descriptions.
5. Prefer the most specific candidate for the primary outcome. Add another only for a distinct artifact, provider, runtime, verification, or risk boundary.
6. Require a source-, provider-, or platform-specialized skill to match a requested surface or a distinct evidence need. Freshness alone does not justify a social, community, or provider-specific workflow.
7. Resolve overlaps by matching the real runtime and operating-surface owner. Do not select duplicate broad workflows for one responsibility.
8. If no installed description matches, check discovery or installation only when the missing capability is necessary; otherwise continue without inventing a skill.

Do not use fixed scores, hardcoded names, keyword-only routing, or a closed allowlist. Explain non-obvious selections from matched facets and descriptions.

## Catalog Lifecycle

For skill installation, update, removal, plugin enable, or plugin disable, follow [Live Catalog Search](references/catalog-search.md). Validate the owning runtime with `python scripts/catalog_scan.py --audit --format json`; never edit the router or a manual registry to register a skill.

The catalog injected into a task is a snapshot. Lifecycle changes appear in the next task or after runtime reload; do not claim the current snapshot changed in place.

## Invariants

- Preserve Windows/WSL, browser profile, account, provider, and runtime ownership.
- Never switch the model, reasoning effort, or service tier as a routing action.
- Skill selection does not grant permission to implement, send, publish, deploy, submit, delete, pay, or expand scope.
- Explicit user choices and more specific repository instructions override inferred routing.

## Execution Protocol

1. Announce the selected skill combination and each role in one short line.
2. Read every selected `SKILL.md` completely before task actions.
3. Read conditional references only when directed or needed.
4. Perform the task with repository and user instructions taking precedence.
5. Treat every new user turn as a routing boundary. Re-evaluate purpose, action, stage, requested validation, repeated failures, context health, domain, artifact, provider, runtime, and risk even when the screen or repository is unchanged.
6. Within one user turn, re-route only when one of those facets materially changes.

Planning to implementation, implementation to debugging, and ordinary debugging to repeated-failure recovery are material stage changes. For bounded implementation plus self-review, consider an available iteration skill; for rediscovery, contradictory completion claims, or repeated observable failures, consider an available handoff skill. These are capability matches, not required companion packages.

Do not repeatedly load the router after the route is stable within the same user turn. A later user turn starts a fresh routing decision. Do not turn routine defaults into user questions.

## Trivial Requests

For a self-contained request needing no tools, workspace context, provider, or specialist method, apply the baseline and answer directly without loading additional skills.
