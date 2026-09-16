---
name: agentic-development
description: Use for non-trivial software development work that benefits from staged product/design/test/coding/review flow, including feature work, UI/UX changes, bug fixes, refactors, E2E findings, prompt generation for the next development stage, freeze handling, and multi-chat or sub-agent handoff.
license: MIT
compatibility: Requires access to the target project repository. Sub-agent or multi-thread delegation is optional; manual multi-chat execution is fully supported.
metadata:
  version: "0.1.1"
  source: "TaurusWood/agentic-dev-system"
---

# Agentic Development

Use this skill as a lightweight controller for the development method defined by `agentic-dev-system`.

The skill controls **workflow semantics**: stage selection, authority boundaries, freezes, output contracts, and handoffs. It does not assume the runtime can create chats, spawn agents, manage worktrees, or persist orchestration state.

## Canonical runtime protocol

The normative runtime semantics are defined only in these references:

- `references/workflow.md` — routing and lifecycle;
- `references/stage-contracts.md` — stage authority and done/stop contracts;
- `references/freeze-output.md` — freeze establishment, integrity preflight, freeze breaks, and output profiles;
- `references/prompt-composition.md` — execution-prompt composition.

Do not invent a second Role Contract or freeze protocol from a copied prompt or explanatory document. If another artifact conflicts with these references, stop and surface the conflict instead of choosing whichever version is easier.

## Core rule

Repository code and versioned project documents are authoritative. Chat history and generated prompts are execution context, not durable truth.

## Start every task this way

1. Inspect the target repository before proposing changes.
2. Read project-local `AGENTS.md` / equivalent instructions when present.
3. Locate only the product docs, technical docs, tests, task packet, and code relevant to the task.
4. Classify the task entry path and current stage using `references/workflow.md`.
5. Load `references/stage-contracts.md` for the selected stage.
6. If any upstream freeze is consumed, load `references/freeze-output.md` and perform its freeze-integrity preflight before writing.
7. Execute the stage within its authority boundary.
8. Return a concise Human Brief and, when another stage must continue, an Agent Handoff or a ready-to-use next-stage prompt.

Do not require a project profile file. Infer the project map from existing repository instructions and structure unless the project explicitly provides one.

## Route the task

Read `references/workflow.md` when deciding where a task enters or what stage comes next.

Typical routing:

- New/changed user-visible behavior with unresolved intent -> PRD / Product Discussion.
- UX/UE or gameplay behavior still being explored -> PRD / Product Discussion.
- Frozen product intent that needs implementation planning -> Technical Design.
- Frozen design that needs acceptance coverage -> Test.
- Frozen tests/design ready for implementation -> Coding.
- Completed module implementation -> Module CR.
- Several reviewed modules need assembly -> Integration / top-level coding.
- Integrated iteration needs system-level verification -> Final CR.
- Bug/E2E finding -> first determine whether it is an implementation defect, product-contract defect, or design-contract defect; route to the owning stage instead of assuming Coding.

If the user explicitly requests a stage, honor it unless a missing prerequisite makes safe execution impossible.

## Stage authority

Read `references/stage-contracts.md` before executing or generating a prompt for a specific stage.

Roles are authority boundaries, not personas. Do not replace explicit ownership, forbidden actions, stop conditions, and done criteria with generic role-play such as “senior engineer”.

## Freeze and output rules

Read `references/freeze-output.md` whenever a freeze exists, a downstream contradiction is found, or a stage result must be handed to a human/agent.

Critical rules:

- a freeze is established only at a committed revision after the owning stage's required review/approval;
- downstream stages verify frozen paths before editing;
- after TEST FREEZE, Coding must not edit frozen tests merely to regain green status;
- a new/bug-regression test contract normally needs baseline sensitivity evidence before TEST FREEZE.

Raise `FREEZE_BREAK_REQUIRED` to the owning stage when a frozen contract is invalid instead of repairing it downstream.

Default human output is Human Brief. Use Human Discussion only for material decisions, real trade-offs, Freeze Break approval, or when explicitly requested.

## Prompt generation

Read `references/prompt-composition.md` when the user asks for a task/stage prompt or when the next stage cannot be delegated automatically.

Prompt generation is a composition practice, not a separate truth source:

`current intent + stage contract + repository truth + task/freeze context -> execution prompt`

Explore uncertain product/UX/bug/architecture questions with natural-language discussion. Once intent is stable, prefer standardized prompts for repetitive Test, Coding, CR, Integration, and Final CR work.

## Delegation capability

If the runtime supports sub-agents/threads and the user wants delegation, it may execute the next bounded stage through that native capability, using the same stage contract and repository artifacts.

If the runtime does not support delegation, do not pretend it does. Finish the current stage and provide a ready-to-paste next-stage prompt.

The method must remain valid in both modes.

## Scope discipline

- Keep module work vertical and bounded.
- Do not absorb unrelated findings unless they block correctness.
- Record non-blocking findings for backlog/handoff.
- Do not let Test redesign Product, Coding redesign Tests, or CR silently rewrite upstream contracts.
- Prefer first-hand repository evidence over retelling another agent's prose summary.

## Learning rule

Do not modify this methodology during active project work just because one task was awkward. Record reusable failure patterns. Promote a change to the base skill only when it is recurring or high-impact and the new rule is simpler than the failure it prevents.
