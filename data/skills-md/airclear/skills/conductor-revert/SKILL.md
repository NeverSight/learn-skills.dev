---
name: conductor-revert
description: Reverts logical units of work (Tracks, Phases, or Tasks) by analyzing git history and synchronizing the Conductor plans. Use when a user wants to undo specific changes and ensure the project's documentation reflects the rolled-back state.
---

# Conductor Revert

## Overview

This skill is a Git-aware assistant. Unlike a standard `git revert`, it understands the relationship between implementation commits and the Conductor documentation. It ensures that when code is reverted, the corresponding `plan.md` and `tracks.md` files are also reset to their previous states.

## When to Use

- When a user says "Undo that task," "Revert the last phase," or "I want to delete this track and its changes."
- To cleanly roll back a feature that isn't working as expected.

## Workflow

1.  **Target Identification:** Interactively help the user select which Track, Phase, or Task to revert.
2.  **Git Analysis:** Map the logical Conductor item to specific Git commit SHAs (both implementation and plan-update commits).
3.  **Plan Presentation:** Show the user exactly which commits will be reverted and in what order.
4.  **Safe Execution:** Perform the reverts, handle conflicts, and manually synchronize the Conductor artifacts to match the reverted code state.

## Implementation Details

Refer to the following protocols for detailed procedural instructions:

- **Resolution Protocol:** [references/resolution-protocol.md](references/resolution-protocol.md) - How to find Conductor artifacts.
- **Revert Protocol:** [references/revert-protocol.md](references/revert-protocol.md) - The logic for mapping Conductor items to Git history and executing reverts.

## Mandatory Constraints

- **Double Confirmation:** Always confirm the target selection AND the final execution plan before running `git revert`.
- **Reverse Order:** Reverts MUST be performed in reverse chronological order.
- **Plan Sync:** The final step MUST be verifying that `plan.md` or `tracks.md` reflects the reverted state.
