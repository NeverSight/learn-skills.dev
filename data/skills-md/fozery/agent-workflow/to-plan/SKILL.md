---
name: to-plan
description: "Turn an existing task into a saved implementation plan, without creating a specification or tickets."
argument-hint: "[task reference, discussion or existing plan to revise]"
disable-model-invocation: true
---

# To Plan

Produce one Markdown implementation plan for a task whose desired outcome is already understood. Work from a request, discussion, ticket or specification; no upstream artifact or other skill is required.
Read applicable project instructions for sources, artifact locations, writing rules and workflow settings. Use the defaults below where the project specifies none.
Planning permits investigation and the authorized plan write, not implementation, tracker mutations or implementation-agent launches. Follow project approval gates. The optional diagram branch below permits only separately approved drawing delegation.

## 1. Establish the task and destination

Read the source task and relevant project instructions. Identify the desired outcome, exclusions, constraints and how success will be observed. Link authoritative requirements instead of recreating a specification.

Reuse the task's configured artifact location and naming convention. Otherwise, save `plan.md` in its existing artifact directory, beside its specification or `issues/` directory when present. With no established location, use `.scratch/<task-slug>/plan.md`, using the task ID or a stable descriptive slug. A specification and tickets need not exist. Ask only when the task or destination is ambiguous.

Identify any existing plan before drafting. Revise the same plan when requested; preserve unrelated content and follow its ownership rules. Do not overwrite a different task's plan or create a competing record. If the required source or write location is unavailable, report the affected blocker rather than claiming a saved plan.

**Done when:** the source task, outcome, boundaries and permitted destination are identified.

## 2. Ground the approach in the code

Inspect the relevant implementation, callers, similar features and representative tests. Find the existing project commands for verification. Check domain terms and accepted decisions where relevant.

Choose the smallest approach that satisfies the task and follows established patterns. Ask about unresolved behavior or consequential trade-offs that block a responsible plan. Mark unsupported assumptions and their affected work; a blocked draft is not ready for execution. Use research or experiments only through the project's permitted process, without starting implementation as part of planning.

**Done when:** the approach has code evidence, required decisions are settled or explicitly blocked, and checks come from the project's actual tooling.

## 3. Draft the plan

Use the project's format. Otherwise, include these compact sections:

- **Task and scope:** source reference, intended outcome, exclusions and plan status. Use `Proposed` until the owner approves the current revision.
- **Context and approach:** relevant code and source pointers, the chosen approach and its important constraints. Give enough context for an executor who did not see the conversation.
- **Work packages:** ordered, checkable pieces of implementation. Each names its result, relevant files or symbols, genuine dependencies, and a verification command or observable scenario with its expected result. For multiple services, group packages by service and executor responsibility as described below.
- **Open decisions:** only unresolved choices or blockers, with the affected work. Omit this section when none remain.

Keep the breakdown proportional to the task. Group incidental setup and documentation with the change that needs them. Split work where its result can be meaningfully checked, not into a fixed number of steps.

If the project selects `excalidraw-diagram`, a diagram may help explain an architectural alternative or service interaction. Use that skill's offer-and-consent procedure; only an approved, separate diagram worker generates it. This optional artifact does not launch implementers or make diagrams a prerequisite for a saved plan. Link the result rather than copying its scene data into the plan.

### Multiple services or repositories

Keep one shared plan. Include a **Shared contracts and integration** section before the service work packages:

- Identify providers and consumers, interaction direction, and the relevant method, endpoint, event or other interface. Define the inputs, outputs and failure behavior that must agree across services. Include authentication, compatibility or delivery guarantees only where the change needs them. Link existing authoritative schemas; define each new or changed contract once and label unresolved decisions.
- Name the owner of each shared contract or schema change. Service packages refer to that definition rather than copying it. State which work depends only on an agreed contract and which requires another service to be implemented.
- State integration order and a cross-service scenario with its expected observable result. Local checks in each service do not by themselves prove the interaction works.

For each service, give the repository and proposed executor role, allowed files or components, required changes, consumed and produced contracts, prerequisites and local checks. An executor needs the common goal, its package and relevant shared contracts, not every other service's internal implementation. Executor roles describe responsibility; they do not launch agents or require a separate agent for every service.

For proposed parallel work, make file ownership disjoint, including shared schemas and configuration. Overlapping work needs an explicit owner and sequence. Reuse this ownership rule for parallel work within one service too.

Identify the common plan's location and how executors in each repository or worktree can read it. A path local to one worktree is not proof of shared access. Follow project storage rules; if no accessible location is known, resolve that handoff before calling the plan ready.

### Keep the plan proportional

Preserve test, review and delivery settings from the project. Describe required behavior and useful verification without writing the whole implementation or imposing TDD, reviewers, commit cadence or another skill. Distinguish expected results from checks actually run. Include migration or recovery steps only when the change needs them.

**Done when:** every requested outcome maps to concrete work and a check. Multi-service work has explicit responsibility boundaries, consistent shared contracts, integration order and a cross-service check. Parallel ownership and access to the common plan are clear.

## 4. Save, check and hand over

Follow the project's approval procedure before saving. Reuse permission already covering the plan write. Save the complete plan at the identified destination; creating only a chat response does not complete this skill.

Check the saved artifact, local links, code pointers, requirement coverage and dependency order. Check consistency between packages' interfaces. If the code or source requirements changed during planning, revise affected steps before handoff. A substantive revision needs renewed approval under the project's rules; keep its status accurate.

Return the saved path, a brief approach summary, open decisions and the next approval or execution action. The executor must read the plan, its source task and applicable project instructions, then recheck relevant code before implementation. Approval of the plan alone does not authorize execution.

Stop after handing over the plan. A tracker-backed decomposition or a particular implementation skill is optional and must support the chosen input; this skill does not invoke either.

**Done when:** one readable task-linked plan is saved, its readiness and verification limits are explicit, and implementation has not started.
