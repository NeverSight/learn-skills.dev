---
name: full-send
description: "Build an internally reviewed feature plan from its shared folder, prove the draft pull requests and run code review."
disable-model-invocation: true
license: MIT
compatibility: "Requires T3 Code and its MCP server `t3-code`, Git, and an authenticated GitHub CLI."
---

# Full-send

Read the [rules of every route](../bmode/SKILL.md) and apply them throughout. Use the status line after each phase. Take all build context from the plan folder. For a different request in the build thread, use the route selection in the linked skill.

## Preflight

Stop if the t3-code MCP tools are absent. Check the sibling paths linked by this skill and its references. If one is missing, stop and print `bunx --bun skills add 0xr3ngar/bstack`. Load the [setup](../bmode-setup/SKILL.md) settings in order: the request, `~/.config/bstack/preferences.md`, then the [defaults and tool table](../bmode-setup/references/defaults.md). Use `orchestrator_capabilities` for each named model and effort. If a required model is unavailable, report the choices to the originating lead for a decision.

Read request.md, plan.md, plan-details.md and state.md. If the user requested plan-first review, verify their explicit go-ahead for the current plan before starting or resuming implementation. If it is missing, return the plan to the originating thread and wait. Use the [state record and legacy migration](../bmode/references/documents.md). Read the origin and plan-reviewed base. If the plan or internal review is incomplete, have the originating thread complete that phase and resume automatically. Preserve any existing build progress. Recover missing files or thread IDs from the plan and launch records before reporting a blocker.

Get this thread's ID with `t3_thread_configure`. If done, return the recorded results. If an explicit pause is still in effect, preserve it. If another live thread has the handoff, identify it to the origin so it can collect the running build. Otherwise record this thread if needed and resume from the last completed step. Honor an explicit user stop. Accept a resume relayed by the originating thread.

Read the plan documents, repository agent, contributing and writing rules, and the proof procedure in research.md. Split by the plan's PR table, preserving order and bases. Write one [build brief](references/build-brief.md) per PR in build/.

## Build

Use the [PR owner procedure](references/pr-owner.md) in both modes. Run the [provider usage check](../bmode-setup/references/defaults.md#provider-usage) before starting builders. If a design decision fails in the code, write evidence in build/ and return it to the originating lead. The lead resolves it from the feature request or reruns internal design review and resumes the build. Escalate only a genuine blocker or consequential choice the evidence cannot settle. Diagnose failures with [root cause fix](../root-cause-fix/SKILL.md).

Record each transition as `pr <n> <branch> <thread or inline> <state>`. Use the newest line for each PR.

**Threads.** Start independent trunk PRs at once. For a dependent PR, wait for acceptance of the one below, then add its link to the brief. Use `t3_thread_launch` with a worktree from the assigned base and the implementer model. Send the first message from the route rules with `Route: change` and `Brief: <absolute path>`. Record started. Wait with `t3_thread_wait`, including delegated work. Read the report with `t3_thread_read`.

Record handed-back. Check the diff against the plan and, for a stacked PR, verify the branch sits on the current head below. Record accepted if both hold. Otherwise record started and send the correction with `t3_thread_send`, prefixed with `Route: change`. Wait again. Send fixes or restacks only after handback.

**Inline.** Build each PR yourself, in order, following the same procedure. Write the same state transitions. Check the diff and ancestry before accepting it.

**Restack.** After a lower head changes, restack each dependent PR lowest first. Record started before sending the instruction or running `gh stack`. In threads mode each PR owner rebases onto the new lower head, checks, pushes with `--force-with-lease` and hands back. In inline mode run the restack yourself and repeat the checks and handback.

**Resume.** Skip accepted PRs if the lower head is still their ancestor. Restack otherwise. For handed-back PRs inspect the diff. For started PRs in threads mode, send “continue” with the route line once the thread is idle and wait. In inline mode check out the recorded branch and resume at the first incomplete PR owner step. Record `built <prs>` once accepted.

## Verify and review

For each stack, verify its top. In threads mode fetch and detach the lead checkout at the pushed head. In inline mode check out the top branch. Run every planned case on the real surface from research.md. Record the runs and gaps in build/verify.md. Record verified only for demonstrated behavior. If the repository has no real surface, say what remains unproved.

Run [swarm](../swarm/SKILL.md) in code mode on the whole change. Give the exact head and commit range per PR. Reviewers use read-only git. Fetch and update the brief with new heads before each later round. Return accepted fixes to the PR owner, mark started, restack dependents after handback and verify affected behavior again. Record each round's scores in state.md.

Return the draft PR URLs, heads, checks, every round's scores, real-surface results and remaining gaps to the originating thread. Include them in the last message for the waiting lead. Record done when complete. Leave the PRs in draft. Leave merges, ready state, reviews, posts and resolutions to the user. Later PR feedback follows the upkeep route.
