---
name: gtm-agent
description: Triggers when a user asks to deploy, set up, get running, connect, check, repair, or upgrade GTM Agent (the Slack agent that runs these skills on Vercel) for an organization, with phrasings like "get gtm-agent running for Acme", "deploy the GTM agent to our Slack", "connect the workflow project for Acme", "check the Acme deployment", or "upgrade our GTM agent". Owns the agent's Vercel project, its Slack connector, the workflow project, and the wiring between them and the workspace repository. Not for the workspace, ICPs, personas, fit checks, or the workflows themselves, which belong to gtm-workspace, gtm-icp, gtm-persona, gtm-qualify-prospects, and gtm-workflow.
---

# GTM Agent

## Trigger

Apply this skill when a request concerns getting GTM Agent deployed, connected, checked, or upgraded for an organization.

## Scope

One deployment is: a private copy of the agent template `eliasstravik/gtm-agent` as the repository `gtm-agent-<slug>`, deployed as the Vercel project `gtm-agent-<slug>`; a Slack connector `slack/gtm-agent-<slug>` installed in the organization's Slack; the workspace repository `gtm-<slug>` (empty until the agent's first save, save for the workflow runtime); and, unless declined, the Vercel project `gtm-<slug>-workflows` connected to that repository's `workflows/` folder with a Turso database. The scripts in `scripts/` do every step through the GitHub and Vercel CLIs; `references/setup.md` lists what each step creates and every variable it sets. The workspace's contents belong to the other gtm skills.

## Inputs

The request; the organization's workspace slug (the contract's slug rule; from an existing `~/.gtm/<slug>/` when one exists); the Vercel team slug (`vercel teams ls`; ask when more than one); the GitHub owner (the signed-in user unless the request names an organization); optionally a Slack channel id (`C0…`, at the bottom of a channel's About tab) for workflow notifications; `references/setup.md`.

## Roles

The user has the GitHub and Vercel CLIs signed in on this computer, completes the Slack install in the browser when the script says so, accepts the Turso marketplace terms the first time a team uses it, invites the bot to a channel, and says the first sentence in Slack; the agent runs the scripts, relays exactly what the user must do, and reports the outcome.

## Procedure

Talk by the six rules in [interaction](../gtm-workspace/references/interaction.md); reproduce [the dialogues](references/interactions.md). Before any job, confirm this computer can do it: `gh auth status` and `vercel whoami` both succeed, and `node --version` is 22 or newer. When they do not, or when this is the hosted agent itself (no `vercel` on PATH, or `GTM_RUN_SECRET` reads `host`), run nothing: say what is missing in one sentence and that a teammate runs `/gtm-agent` on a computer with both CLIs signed in.

| Job | Do |
| --- | --- |
| Deploy | Ask for the Vercel team only when `vercel teams ls` shows more than one; ask for a channel id only when the user mentions workflow notifications. Say the one sentence of what will happen and that it takes about five minutes. Run `node scripts/setup.mjs --slug <slug> --team <team> [--github-owner <owner>] [--channel <id>]` from this skill's folder, streaming its output. When it prints the Slack address, relay it with the three things to do on that page (choose the workspace, add the listed events and scopes under Advanced, Allow) and wait; the script continues by itself. Exit 2 names one human step (the Slack install, or `vercel integration accept-terms tursocloud`): relay it, wait, run the same command again. Exit 0: close with the two Slack lines the script printed. Exit 1: report the failing line in plain words and offer Doctor. |
| Connect | The workflow project alone, for a deployment made before this skill or with `--no-workflows`: the same command with `--agent-project <name>` when the agent project has another name; the script skips what exists. |
| Doctor | `node scripts/doctor.mjs --slug <slug> --team <team> [--github-owner <owner>] [--agent-project <name>] [--workflow-project <name>] [--slack-connector <uid>]`; report the failing lines in business terms with their fixes; run again with `--fix` when the user accepts the safe fixes (project settings, obsolete variables). Slack events and scopes are the one fix the dashboard owns: give the connector's Advanced page and the exact names. |
| Upgrade | In the agent checkout (`~/.gtm/.agents/<slug>/`, or the repository the user names): `git fetch template && git merge template/main`, resolve nothing by hand (the copy carries no local changes; when it does, stop and say so), `git push`; the push deploys. Then Doctor. When the workflow runtime is behind, say so and hand off to gtm-workflow's Upgrade. |

Names are fixed by the slug: `gtm-<slug>` (workspace repository), `gtm-agent-<slug>` (agent repository and project), `gtm-<slug>-workflows` (workflow project), `slack/gtm-agent-<slug>` (connector), the Turso database `gtm-<slug>`. A deployment made by hand before this skill keeps its names; pass them as overrides.

## Outputs

A live agent answering in Slack, wired to its workspace repository and, unless declined, a live workflow project; the doctor's report; the two Slack lines: invite the app, then `@gtm-agent-<slug> set up our GTM workspace`.

## Exceptions

Secrets never pass through the conversation: the scripts generate them and place them with `vercel env add`; the GitHub token is the CLI's own (`gh auth token`), which reaches every repository that user can write, and the user may replace `GTM_GITHUB_TOKEN` with a fine-grained token later. A Vercel Hobby account cannot hold a team: say that a Pro team is needed and stop. A GitHub organization that has not installed the Vercel GitHub app makes `vercel git connect` fail: name the install (Vercel → Settings → Git) and run again. The Slack app answers mentions only until its Advanced events and scopes are set; Doctor says which are missing. Requires `gtm-workspace` and `gtm-workflow` installed alongside this skill; when either is missing, say to install it with `npx skills add eliasstravik/gtm-skills -s <name> -y` (add `-g` when this skill lives in the global skills directory), then retry.

## QC

- The user did at most these by hand: two CLI logins, one Slack browser trip, the Turso terms once, the invite, the first sentence.
- No secret value appeared in the conversation or a reply.
- Doctor ends with "All good." before the deployment is called done; every failing line was reported with its fix.
- The closing reply carries the two Slack lines and nothing about commits, builds, or checks.

## References

[setup.md](references/setup.md) for what the scripts create, every variable, and the by-hand equivalent; [interactions](references/interactions.md) dialogues; from gtm-workspace: [interaction](../gtm-workspace/references/interaction.md), [contract](../gtm-workspace/references/contract.md); from gtm-workflow: [deploy.md](../gtm-workflow/references/deploy.md).
