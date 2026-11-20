---
name: bmode
description: "Start every thread here. Route a problem, a feature, a failing check, a review or a question to its playbook."
disable-model-invocation: true
license: MIT
compatibility: "Requires T3 Code and its MCP server `t3-code`, Git, and an authenticated GitHub CLI."
---

# Bmode

Start every user thread with `/bmode <request>`. Take the problem from the user. Work out the solution.

## Preflight

Check for the t3-code MCP tools. If absent, stop and say this workflow needs T3 Code. Check the sibling paths linked here and in the playbooks and references. If any are missing, stop and print `bunx --bun skills add 0xr3ngar/bstack`.

Read the [settings and tool table](../bmode-setup/references/defaults.md). Apply the request, then `~/.config/bstack/preferences.md`, then the defaults. If the file is absent, use the defaults. Run [setup](../bmode-setup/SKILL.md) on request. Resolve the models and efforts needed by the current phase with `orchestrator_capabilities`. If a required model is unavailable, give the available choices and ask which one to use. Apply the [provider usage check](../bmode-setup/references/defaults.md#provider-usage) at feature preflight and before launching agents. Keep the current thread model outside the feature route.

## Choose a route

Follow an explicit `Route:` line. Route `/bmode <slug>` for an existing plan folder to feature. Otherwise honor the route the user asks for, or infer it from the request. If two fit, pick the lighter one and say what would move it up. Start the reply with `Route: <route>. <short reason>`. Announce a later change of route. Read only the selected playbook.

| Route | Request | Result |
| --- | --- | --- |
| [Feature](playbooks/feature.md) | New behavior or a refactor that needs design | Plan, run a swarm review, build, verify and return draft PRs here. |
| [Bug](playbooks/bug.md) | Failure, red check or flaky test | Proved draft fix and code review, or evidence the behavior is correct. |
| [Change](playbooks/change.md) | Small or specified change | Demonstration and proved draft PR. Review on request. |
| [Review](playbooks/review.md) | Another contributor’s PR | Verdict, checked findings and draft comments. |
| [Upkeep](playbooks/upkeep.md) | The user's own PR | Updated branch, checks and feedback. |
| [Question](playbooks/question.md) | Explain something | Answer from code and history. |
| [Audit](playbooks/audit.md) | Find improvements | Ranked findings. Start work only on request. |
| [Writing](playbooks/writing.md) | Message, document or deck | Draft in the user's voice. |
| [Chores](playbooks/chores.md) | Tickets, hours or counts | Report what changed. |

## Rules of every route

1. Follow [unslop](../unslop/SKILL.md). Give the result first. Number questions. Draw structures as “Draw the diagram” in [yeet](../yeet/SKILL.md) describes.
2. End each phase with one status line giving the phase, result and next phase. Use `send_to_user` for text the user must see before the turn ends.
3. Read the repository’s skills and documents first.
4. A feature request authorizes planning, implementation, verification and opening draft PRs. Keep the originating thread responsible for delivery. Infer routine choices from the request, evidence and repository rules. Honor a request to read or approve the plan before building. Otherwise interrupt only for an explicit stop, a genuine blocker after recovery attempts, or consequential input you cannot infer. For a blocker, give the evidence and ask only for the action or decision that unblocks it. Open PRs as drafts. Merge, post, resolve, approve or re-request review only on the user's word for that action.
5. On “stop” or “pause”, immediately cancel each delegate with `task_cancel`. Send each started thread the following message with `t3_thread_send`, mode `restart`. Wait for each with `t3_thread_wait`, including delegated work. Wait again after a timeout, then report the state.

   > Stop. Stop every agent that you started, as rule 5 of bmode says, wait for each stopped thread with t3_thread_wait and wait again after a timeout, start nothing, and report the state.

6. Use native stacks for dependent PRs. Use `gh stack` to create and restack them when installed. For an authorized merge, use its merge operation if available.
7. Stop a bug fix that needs a behavior choice or design and present the options. Move a change that needs design to feature and say so. A started thread stops and reports instead.

## Start a thread

Use `t3_thread_launch` with `workspaceStrategy` and `modelSelection`. Send this first message with the absolute installed path:

```text
Read <absolute path>/bmode/SKILL.md and follow it.
Route: <route>
<task or brief>
```

A PR owner gets `Route: change` and `Brief: <plan folder>/build/brief-<pr>.md`. A batch bug gets `Route: bug` and a task with the ticket, findings, batch context and base fix branch if any. An audit finding gets `Route: change` and the finding as its task. For the build thread use the handoff in the [feature playbook](playbooks/feature.md).

1. A started thread keeps its assigned route. Prefix every later message to it with its route except the stop message. A message without the prefix or stop instruction is from the user and may change its route. The build thread starts directly on the build skill.
2. When a playbook would move up or wait for the user, stop and give the evidence and options in the last message.
3. Every started thread, including the build, reports to its parent. Wait with `t3_thread_wait` and `untilDelegatedWorkSettled: true`, then use `t3_thread_read` and bring the report to the user.
4. Pass a stop to every agent you started and wait as rule 5 requires.
5. Honor an explicit pause until the user resumes in either thread. Relay the instruction to the affected child with its route line (the build thread uses its build command). For a timeout or recoverable interruption, resume from the record yourself.
