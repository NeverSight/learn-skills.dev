---
name: create-durable-plan
description: Use when asked to create a durable plan, or to save the current conversation's plan to the `docs/plans` folder.
---

# Create durable plan

## Use this skill when

- You are asked to create a durable plan.
- You are asked to save a plan from the current conversation to `docs/plans`.

## Setup

- Read the skill `about-docs-folder`.

## Instructions

- Create the plan in a new plan folder (see `about-docs-folder` for the folder structure and naming).
- Write the plan with durable changes.
  - Avoid over-specific implementation details that are likely to go stale.
  - However, include enough information/details so that agents can follow the direction and goals of the plan accurately.
- If HTML artifacts exist as part of the conversation or plan, include them in the plan folder.
