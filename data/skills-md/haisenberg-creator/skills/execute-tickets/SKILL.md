---
name: execute-tickets
description: Autonomous orchestrator that chews through a batch of tickets by dispatching sub-agents. Use this after /to-tickets has published the work.
disable-model-invocation: true
---

# Execute Tickets

Act as the **orchestrator** for a batch of tickets. Do not write code yourself. Your job is to read the tickets, compute the frontier, and dispatch sub-agents to do the work.

## Process

### 1. Locate the tickets

Ask the user where the tickets are located (e.g., local `.scratch/` directory or a GitHub/Linear tracker URL) if not already provided in context. Read them to understand the dependency graph.

### 2. Compute the frontier

The **frontier** is the set of tickets that are not yet "Done" and have no uncompleted blockers. A ticket whose blockers are all marked "Done" is on the frontier.

### 3. Dispatch a sub-agent

Pick one ticket from the frontier. Read its **Required skills** field. Use your sub-agent tool to spawn a sub-agent with a prompt tailored to those skills:

- For standard engineering (`implement`):

  > "Read ticket <ticket-reference>. Create an implementation plan. Then apply the `implement` skill (using TDD, running typechecks, and committing your work). Once the code is committed, report back as Done."

- For UI/UX design or polish (`design-taste-frontend`, `emil-design-eng`):

  > "Read ticket <ticket-reference>. Create an implementation plan. Then apply the `design-taste-frontend` skill for layout/styling and `emil-design-eng` for interaction/polish. Skip strict TDD, produce a visual verification step instead, and commit your work. Once the code is committed, report back as Done."

- For exploratory design (`prototype`):
  > "Read ticket <ticket-reference>. Apply the `prototype` skill to build a throwaway prototype. Do not write production code. Report back as Done when the prototype is ready for user review."

Wait for the sub-agent to complete. Do not dispatch multiple sub-agents in parallel unless you are certain the tickets do not conflict.

### 4. Mark Done and Loop

When the sub-agent reports success:

1. Update the ticket's status to "Done" (either edit the local markdown file, or update the issue tracker).
2. Recompute the frontier.
3. Loop back to Step 3.

The session is complete when the frontier is empty and all tickets are marked "Done".
