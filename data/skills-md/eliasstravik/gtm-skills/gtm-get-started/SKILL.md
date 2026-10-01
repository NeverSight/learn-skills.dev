---
name: gtm-get-started
description: Triggers when someone new to GTM Skills asks where to begin, with phrasings like "how do I get started", "what do I do first", "where do I begin with gtm", or /gtm-get-started. Looks at what the workspace already has and takes the user through each missing step, handing it to its gtm skill in the same conversation. Not for requests that already name a job (a workspace, ICP, persona, fit check, workflow, or the Slack agent), which go straight to that gtm skill.
metadata:
  version: "0.2.5"
---

# GTM Get Started

## Trigger

Apply this skill when a request asks where to start or what to do next with GTM Skills and names no job.

## Scope

A guide: it reads the workspace, finds the next step, and hands that step to the gtm skill that owns it in the same conversation, then checks again. It never writes a file itself; every write is the owning skill's job.

## Inputs

The request; the workspace found by the discovery order in [the contract](../gtm-workspace/references/contract.md); its `icps/*/ICP.md` and `personas/*/PERSONA.md`.

## Roles

The user answers the owning skill's questions and picks the goal when the foundations are done; the agent reads, hands off, and carries on.

## Procedure

The first gtm skill used in a conversation checks once for a newer release, as [updates](../gtm-workspace/references/updates.md) says. Talk by the six rules in [interaction](../gtm-workspace/references/interaction.md); reproduce [the dialogues](references/interactions.md).

1. Take the first row whose check holds:

| Check | Hand off to |
| --- | --- |
| No workspace found | gtm-workspace, Create: the organization's workspace |
| No ICP | gtm-icp, Create: the companies to sell to |
| No persona | gtm-persona, Create: the people to sell to |
| All three exist | Ask **What next?** with **Check a company or person now (Recommended)** → gtm-qualify-prospects, **Check them on a schedule** → gtm-workflow, **Use it in Slack** → gtm-agent |

2. Say in one sentence what is already in place and what comes next, then hand off: load that skill (the host's skill tool, such as Skill, or read its `SKILL.md`) and follow its procedure for that job now. Never tell the user to say a phrase or run a slash command to start it. Ask only what the owning skill needs, such as the company name when the request names none.
3. When the owning skill closes its save, go back to step 1 and continue. After the user's pick in the last row, that skill's job is the rest of the conversation.

## Outputs

The missing foundations made by their own skills in one conversation, then the chosen skill's job; get-started itself writes no files.

## Exceptions

Requires the `gtm-workspace` skill installed alongside this one; when `../gtm-workspace/SKILL.md` is missing, run `npx skills add eliasstravik/gtm-skills -g -y`, then read the installed `SKILL.md` and continue. Several workspaces match and none is named: ask which, as the contract says. On the hosted Slack agent (`GTM_AGENT_HOSTED` is `1`), drop the Slack option. A workspace that looks broken (no `ORG.md`, unreadable files): hand off to gtm-workspace, Doctor. The user stops or changes course mid-way: follow the user; the next "how do I get started" picks up from what exists.

## QC

- Each step handed to its owning skill in the same conversation; no reply asks the user to say a phrase or run a command to start it.
- No file changed except by the owning skill's own save.

## References

[interactions](references/interactions.md); from gtm-workspace: [contract](../gtm-workspace/references/contract.md), [interaction](../gtm-workspace/references/interaction.md), [updates](../gtm-workspace/references/updates.md).
