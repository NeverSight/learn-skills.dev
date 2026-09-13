---
name: swe-method
description: Guide for working through a Jira story efficiently by separating context gathering, immutable evidence collection, codebase exploration, human-in-the-loop specification refinement, execution planning, and implementation. Use when turning a ticket into a reliable engineering workflow instead of jumping straight to code.
---

# SWE Method

Use this workflow to work through a Jira story with enough context and validation to avoid speculative implementation.

## Step 1: Define Context

Bring together the resources you already know about up front.

### Specification

- Jira ticket ID

### Additional Context Index

- Slack thread URLs
- Session IDs from AI-tool interactions
- Meeting transcripts
- Personal notes
- Parent, related, and child tasks
- Existing branches and PRs

## Step 2: Fetch Data Into An Immutable Layer

Gather the source material you will reason from and keep it separate from interpretation so later steps are grounded in facts rather than memory.

## Step 3: Explore Codebase And Systems

Based on the specification and additional context, inspect the real repositories, branches, PRs, APIs, schemas, CLIs, and surrounding systems that the work depends on.

## Step 4: Human-In-The-Loop Specification Refinement

Rules:

- The bigger the task, the harder it is to disambiguate everything up front.
- The longer the autonomous run, the larger the divergence risk from the engineer's intended outcome.

Sizing guidance:

- Tiny and repetitive tasks: the HIL step can often be skipped and decisions encoded in a skill.
- Small tasks: do a lightweight HIL planning step, then automate implementation.
- Larger tasks: break the work into smaller subtasks and refine each before execution.

Use the agent's question flow to extract one decision at a time and store the clarified specification in a spec file or spec folder.

Question types can include:

- Requirements that depend on stakeholders or teammates
- Design decisions the engineer can make or escalate

## Step 5: Execution Plan

The specification is about what to build. The execution plan is about how to build it without hallucinating missing facts.

In brownfield systems, especially when databases, APIs, CLIs, or SDKs are involved, do not let the agent assume schemas or response shapes. Validate them first.

Execution plans may include HIL steps that expose the agent to:

- Real API responses
- Real DB schemas
- Real CLI or SDK behavior

Only after assumptions are validated should tests be written against those facts.

Example execution plan for a class change:

1. Query the API or DB the class depends on.
2. Use the observed shape to define a test case.
3. Implement until the test passes.
4. Refactor and simplify.
5. Update docs.

## Step 6: Implementation

Two workable paradigms:

- Implement a slice, run it end to end against the real system, troubleshoot until it behaves correctly, then add tests to lock it down.
- Validate real external behavior first, then do TDD using tests grounded in factual responses rather than imagined ones.

Alternate implementation with cleanup so code quality and conventions are applied continuously rather than deferred to the end.
