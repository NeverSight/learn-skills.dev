---
name: project-verification
description: "Use when creating, auditing, or repairing a project's repeatable verification runbook, harness, or feature map. Excludes routine check execution, product fixes, and test design."
---

# Project verification

Build or maintain project-local instructions that another agent can execute and check. Keep reusable decision rules here; put commands, selectors, ports, credential requirements, expected effects, and feature coverage in the consuming repository.

## Scope and authority

Audit requests stay read-only. Authoring and maintenance requests authorize scoped, reversible runbook or harness changes and their verification. Product repairs belong to engineering or debugging under the user's existing authorization; designing test coverage belongs to test-design. Running an established recipe belongs to the verifier role and does not require rewriting it.

Prefer the project's existing launchers, test tools, and documentation locations. Add a harness only for a demonstrated gap. Keep one source of truth for commands already owned by project tooling.

Driving shared services, installing host software, publishing changes, or deploying requires the applicable authorization. Do not infer it from a request to make verification repeatable. Keep secrets out of recipes and captured evidence.

## Required result

Every runnable recipe identifies:

- Prerequisites, working directory, configuration, and isolated test state.
- Launch or attachment instructions with observable readiness, expected build, and instance ownership checks before driving it.
- A real user, API, or CLI path with concrete inputs and observable success and failure criteria.
- Evidence paths that survive cleanup, plus the revision, configuration, commands, and results needed to interpret them.
- Cleanup limited to resources owned by this run, including recovery after a partial failure.

A listening port or healthy response alone proves neither ownership nor build identity. Refuse to drive or terminate an instance whose identity cannot be established. Give concurrent workers isolated state; assign one driver when they must share mutable application state.

Keep a feature map proportionate to the request. Distinguish executed paths, failed paths, blocked paths, and unexercised paths. A working launch or one successful path does not validate the rest of the map.

## Choose the branch

- When creating or extending a recipe, read [authoring.md](references/authoring.md).
- When auditing drift or repairing an existing recipe, read [maintenance.md](references/maintenance.md).

## Completion

Before calling a generated or materially changed recipe ready, have a fresh agent execute a representative path from the written instructions against isolated state. Give it repository guidance, the recipe, the acceptance goal, and authorized access, without private setup hints. Check its artifacts and command evidence, repair omissions, and repeat the affected portion. If a fresh agent or required environment is unavailable, report the recipe as drafted or partially verified.

Report the artifact locations, exercised coverage, remaining gaps, evidence retained after cleanup, and any product defect or authority blocker. An audit finishes with findings; an authored recipe finishes with demonstrated execution and honest coverage limits.

## Provenance

Inspired by pstack's [create-verification-skill](https://github.com/cursor/plugins/blob/6ed0f7a9504f577d7529064103cecce9be7dfc5e/pstack/skills/create-verification-skill/SKILL.md) and [maintain-verification-skill](https://github.com/cursor/plugins/blob/6ed0f7a9504f577d7529064103cecce9be7dfc5e/pstack/skills/maintain-verification-skill/SKILL.md), v0.15.2. Adapted for Codex and project-local tooling.
