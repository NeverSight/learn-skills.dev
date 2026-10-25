---
name: repo-conventions-setup
description: "Records a repository's working conventions for AI agents in its agent instructions file: where work items live, how specifications and notes are laid out, which checks to run, and what agents must not do. Use when a repository first adopts agent skills or its conventions change. Not for installing skills and not for choosing a tracker or toolchain."
disable-model-invocation: true
---

# Repo Conventions Setup

## Purpose
Give agents one place to learn how this repository works, so other skills do not guess about trackers, document locations, or checks. The result is a short, accurate conventions section in the repository's agent instructions file.

## When to use
- Use when: a repository is adopting agent skills, agents keep guessing where things go or how to verify work, or conventions have changed.
- Do not use when: the task is installing or syncing skills, or selecting tools the repository does not already use.

## Inputs
- Required: access to the repository.
- Optional: the requester's answers about conventions, and an existing agent instructions file (commonly `AGENTS.md`).
- Assumptions: the requester owns the conventions; the skill records them and does not invent them.

## Process
1. Find existing evidence: the README, contribution guide, agent instructions file, scripts, configuration, and recent work items or notes. Do not ask what the repository already answers.
2. List what is still unknown from these topics: where work items live (any tracker, files, or none) and the status words used; where specifications, decisions, and notes are stored; the commands that check the work (tests, lint, build, validation); branch and commit conventions; and actions agents must not take without approval.
3. Ask the unknowns one question at a time, offering options with a recommendation drawn from what you found.
4. Draft a conventions section using the [conventions template](templates/conventions.md). Use plain words for statuses and locations, not tool-specific features.
5. Run each check command that is safe to run and record whether it worked. Mark any command not run as unverified.
6. Add the section to the agent instructions file, or update the existing one in place, preserving everything else. Show the requester the change before it is final.

## Rules and heuristics
- Required: never invent commands, paths, statuses, or policies. Unknown stays unknown and is listed as open.
- Required: do not overwrite existing instructions; merge, and flag conflicts for the requester.
- Required: keep it vendor-neutral. A tracker or tool is named only where the repository already uses it.
- Recommended: keep the section short enough to be read in full by every agent session.

## Checks
- Every path and command in the section exists or is marked unverified.
- Nothing in the file was removed unintentionally, and no secrets were added.
- Each convention traces to repository evidence or to a requester answer.

## Output
Return the updated or new conventions section, the file it was written to, the commands verified and unverified, and open items.

## Completion criteria
- The conventions section exists in the agent instructions file and the requester has seen it.
- Unknowns and unverified commands are listed rather than guessed.
