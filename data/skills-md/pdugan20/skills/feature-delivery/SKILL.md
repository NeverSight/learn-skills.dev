---
name: feature-delivery
license: MIT
description: Take a substantial production feature from an idea or selected behavior through specification, coordinated implementation, integration, and staged user availability. Use when delivery spans meaningful product or architecture decisions, multiple repositories or subsystems, important data or security boundaries, client and backend compatibility, or controlled rollout. Do not use for UI direction exploration, bounded feature spikes, hardening-only work, deployment of an already completed build, small fixes, or ordinary isolated changes.
---

# Feature Delivery

## Core principle

Coordinate the whole path to users, not only the code change. Establish evidence
and contracts before prescribing architecture, then report source, environment,
distribution, and exposure states independently.

## Delivery process

1. **Qualify the outcome.** Confirm that this is production feature delivery.
   Route UI comparison to `code-native-ui-ideation`, a bounded learning
   experiment to the applicable feature-spike skill. Handle a dedicated
   hardening or release-readiness request directly under repository production
   instructions or a separately requested release-readiness capability. Handle
   an ordinary isolated change directly.
2. **Investigate before designing.** Read applicable instructions and inspect
   the current behavior, architecture, tests, repositories, environments,
   release path, and uncommitted work. Do not infer a backend boundary, data
   contract, or deployment topology from the request alone. If the relevant
   repositories are unavailable, present architecture options only as
   hypotheses and stop at the discovery plan; do not label one recommended or
   sequence its implementation until evidence supports it.
3. **Establish the delivery contract.** Resolve only decisions that materially
   change product behavior, architecture, data, security, compatibility, or
   rollout. Capture the outcome, non-goals, acceptance criteria, impact map,
   selected design, risks, and release gates using
   [references/specification.md](references/specification.md). Use
   [assets/feature-delivery-template.md](assets/feature-delivery-template.md)
   when a durable handoff is useful; a bounded single-repository feature can
   keep the same fields in the working plan or conversation. Get the user's
   approval for unresolved material choices before implementation.
4. **Map boundaries and order.** For more than one repository, service,
   environment, schema, or distributed client version, follow
   [references/cross-repository-delivery.md](references/cross-repository-delivery.md).
   Publish producer contracts before consumers depend on them. Define
   backward/forward compatibility, migrations, branch and environment
   relationships, integration evidence, gating, and rollback per layer.
5. **Select the execution mode.** Record whether the work will use proportional
   inline execution, explicitly requested and available Superpowers, an
   available agent team, or a mixed/human handoff. Verify named external skills
   and delegation capabilities are discoverable in the current runtime before
   selecting them; documentation or user intent alone does not prove
   availability. If a requested mode is unavailable, name the missing
   capabilities and offer proportional inline execution or a pause for
   installation as explicit choices. Do not impersonate a missing skill or
   silently switch modes. Follow
   [references/execution-modes.md](references/execution-modes.md). Activating
   this skill never implicitly authorizes strict TDD, worktrees, agent teams,
   branch finishing, or other explicit-only skills. Every delivery plan must
   contain an explicit `Execution mode: <mode> — <rationale>` line; silence is
   not a selection.
6. **Plan dependency-ordered checkpoints.** Make each checkpoint independently
   verifiable and name its owner, repository, inputs, outputs, tests, and exit
   evidence. Parallelize only independent work after interfaces and ownership
   are stable.
7. **Implement and verify proportionally.** Work in coherent, inspectable
   batches. Add tests according to regression, data, security, concurrency, and
   platform risk. Exercise user-visible behavior in the real browser, relevant
   simulator, or device. Run focused checks throughout and each repository's
   broader production or CI gate before claiming source readiness.
8. **Integrate and stage availability.** Verify real contracts and supported
   version combinations, not only mocks and per-repository tests. Follow
   [references/staged-rollout.md](references/staged-rollout.md) for development,
   backend deployment, internal distribution, TestFlight or preview channels,
   exposure, observation, rollback, and temporary-gate cleanup.
9. **Report multidimensional status.** Report each independently true state,
   attached evidence, blocker, next gate, and authorization needed. Never use a
   merged change, green client suite, deployed backend, distributed binary, or
   enabled flag as a synonym for “available to users.”

## Boundaries

- Preserve unrelated user work and follow repository-specific instructions.
- Keep private product plans, credentials, production data, and personal data
  out of specifications, prompts, fixtures, logs, and reports.
- Identify targets as local, development, staging, internal distribution, or
  production before mutation. Prefer emulators, synthetic fixtures, test users,
  and development services while resolving behavior.
- Do not deploy, publish a build, change live configuration, mutate production
  data, merge, push, or open a pull request without the authorization required
  by the active working agreement.
- For visual decisions, work in code. Do not use ImageGen, generated mockups, or
  a detached option picker unless the user explicitly requests them.
