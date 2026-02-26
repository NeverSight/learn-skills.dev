---
name: sdd-engineering
description: A hybrid engineering workflow combining Strict Spec-Driven Development (EARS) with Autonomous Harness Engineering.
---
# SDD Engineering Skill
Description: A hybrid engineering workflow combining Strict Spec-Driven Development (EARS) with Autonomous Harness Engineering.

## The 4-Step Engineering Loop

### Phase 1: Legislation (The Kiro Phase)
**Goal:** Eliminate ambiguity.
1.  **Ingest:** Read user intent.
2.  **Translate:** Convert intent into **EARS Syntax** (See `identity/ears-syntax.md`).
3.  **Freeze:** Output `docs/requirements.md`. Once written, this is the LAW.
4.  **Design:** Generate `docs/architecture.mermaid` and `docs/api-contract.md`.

### Phase 2: Harnessing (The OpenAI Phase)
**Goal:** Prepare the safety net.
1.  **Test Gen:** Before coding, generate a `verification_plan.md`.
    * *Rule:* Every "SHALL" in EARS must have a corresponding Check/Test.
2.  **Linter Setup:** Define project-specific constraints (e.g., "No circular dependencies in module X").

### Phase 3: Execution (The Coding Phase)
**Goal:** Implement with evidence.
1.  **Code:** Implement features defined in Phase 1.
2.  **Observe:** Use logs/prints to verify behavior (Agent Vision).
3.  **Check:** Run the tests defined in Phase 2.

### Phase 4: Reconciliation (The Living Doc Phase)
**Goal:** Prevent drift.
1.  **Drift Check:** Did the code change require a Spec update?
2.  **Sync:** If yes, UPDATE `docs/requirements.md` FIRST.
3.  **Commit:** Only commit when Spec == Code == Tests.

## Prime Directive
> "Code is a liability. Specifications are assets. Do not write code that is not specified. Do not specify what you cannot verify."

## Instructions for Agents

When adopting this skill, you must adhere to the following strict behaviors:
1. **Never commit code** without updating the corresponding specification document first, especially when dealing with ambiguous intent.
2. Before generating any files, you **MUST output a `<thinking>` block** to analyze ambiguity (Kiro requirement) and plan the testing strategy (Harness requirement).
