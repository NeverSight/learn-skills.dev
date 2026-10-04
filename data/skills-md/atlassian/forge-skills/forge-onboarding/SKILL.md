---
name: forge-onboarding
description: Guide a first-time Forge builder through deploying a stock Rovo Agent, then turning it into Forge Guru, a documentation companion. Use for Forge onboarding, a first Forge or Rovo app, or resuming this tutorial. Route unrelated existing-app changes, debugging, reviews, and connector work to the specialist skills.
license: Apache-2.0
metadata:
  labels: "confluence,jira,atlassian,forge,onboarding,rovo,agent"
  maintainer: amoore
  namespace: cloud
---

# Forge onboarding

Help the user ship and use an app while learning the manifest, module, and backend function.
The default journey has two loops: deploy the stock Rovo Agent, then customize the same
registered app into Forge Guru. Adapt the teaching pace to the user.

## Load guidance by phase

Read only the reference for the current phase, plus any reference it conditionally requires.
Do not preload the entire journey, README, assets, or evaluation cases.
Use these stable phase names in state and transitions; do not depend on numbered steps.

| Phase | Read when | Reference | Evidence to advance |
| --- | --- | --- | --- |
| `welcome` | Starting a new guided session | Use the short welcome below | User is ready, or has already asked to start |
| `setup` | Prerequisites are unknown or a tool fails | [Setup](references/setup.md) | Tools and authentication work; warnings are distinguished from blockers |
| `orientation` | User wants introductory teaching | [Mental model](references/mental-model.md) | Concepts explained, or user skips them |
| `scaffold` | Choosing targets and registering an app | [Environment and scaffold](references/environment-and-scaffold.md) | Registered app and stock files verified |
| `hello-world` | Walking through, deploying, and using the stock app | [Loop 1](references/loop-1-hello-world.md) | Deployment, target installation, and stock action observed |
| `guru` | Customizing and deploying the docs companion | [Loop 2](references/loop-2-forge-guru.md) | Authorized edits verified, upgrade installed, response quality checked |
| `next-steps` | Closing the tutorial | [Next steps](references/next-steps.md) | Outcome and relevant next route explained |
| Recovery | An observed failure needs investigation | [Recovery](references/recovery.md) | Failure resolved or concrete blocker reported |
| Platform check | A phase needs current CLI, schema, or endpoint facts | [Platform contract](references/platform-contract.md) | Relevant fact verified and evidence recorded |

Default transition: `welcome → setup → orientation → scaffold → hello-world → guru → next-steps`.
Recovery returns to the interrupted phase. An exit stops the workflow immediately.

## Keep a compact session record

Retain these values in conversation context, updating them after meaningful actions:

| State | Record |
| --- | --- |
| Position | Phase, last completed action, next action, requested teaching pace |
| Local environment | OS/shell, Node and CLI versions, authentication result, accepted warnings |
| Local target | Absolute parent directory and app path; whether destination existed before creation |
| Atlassian target | Account, Developer Space name/ID, exact site, product, environment |
| Identity | Registered `app.id`, runtime, actual agent key/name, handler and action names |
| Progress | Scaffold verified; edits applied; dependencies installed; lint result; deployments and installs confirmed |
| Live evidence | Stock action observed; Guru response and whether it used search or fallback |
| Authorization | Exact approved actions, targets and impacts; terms consent separate from creation |

Do not store credentials. Do not create a progress file unless the user requests one.
Record consent as an action and target, not a blanket permission for future commands.

### Skip, exit, and resume

- Honor "skip setup", "skip to Loop 1", "less explanation", and "exit".
- Skip introductions, conceptual lessons, and file walkthroughs when requested. Do not repeat
  a ready-check when the user has already said to proceed.
- When skipping setup, reuse known results. Run only missing checks needed for the next
  command. A version warning is not a failed executable: explain it once and honor the
  user's choice to continue if the tools run.
- Collect targets when needed. Creation needs a directory and Developer Space; installation
  needs a site. A missing site need not block scaffolding.
- The stock live-action checkpoint is the default. If explicitly skipped, mark it unverified
  and continue with authorized customization; do not claim it was observed.
- Skipping teaching does not supply credentials, select ambiguous targets, accept terms,
  or authorize deployment or installation.
- On exit, stop tools and questions. Briefly state what changed and what remains, using
  recorded evidence. Do not keep offering the next tutorial step.
- On resume, reuse context and inspect the app. Check identity and installation as relevant.
  Never rerun creation over an existing app or replay completed edits, installs, consent,
  or lessons without a reason.
- Without a session record, infer progress from read-only inspection and ask only about
  unresolved choices. Directory existence alone does not prove a valid scaffold.

## Preserve execution boundaries

1. Explain each imminent command briefly, including its effect. Batch explanations for
   independent checks. Report observed results rather than anticipated success.
2. Keep secrets out of chat and files. Login and unexpected credential prompts go to the
   user's interactive terminal; never ask them to paste an API token here.
3. Before creation, provisioning, deployment, installation, or upgrade, resolve the action
   and target and show its effects. Reuse explicit authorization for that same scope;
   otherwise ask. Local walkthroughs and read-only checks need no extra gate.
4. Terms and billing consent are separate from "build my app". The sibling creation helper
   currently passes `--accept-terms`. Read the scaffold reference before invoking it; use
   it only with specific informed consent, or let the user run interactive creation.
5. Register apps through `forge create`. Use the sibling helper for agent-run scaffolding.
   Run deploy and install directly. Never invent an app ID or an unregistered replacement.
6. Default to `development` and state it in environment-sensitive commands. A development
   environment does not make real site data harmless; prefer a test site and minimal
   permissions. A different environment/site requires a separately scoped decision.
7. Preserve user files and app identity. Inspect the destination before creation. Never delete
   a failed scaffold, overwrite an existing directory, or recreate an app without confirming
   the exact target and consequences. Preserve partial output for diagnosis.
8. Keep stock source and manifest unchanged until authorized Guru customization. Dependency
   installation may update the package lock and dependencies; explain that distinction.
9. Default to separate approval for manifest and backend changes in Loop 2. A user can
   authorize the disclosed bundle together; do not ask again for the same approved edit.
   Always preserve `app.id`, runtime, and unrelated manifest/package settings.
10. Validate against current official guidance and `forge lint` before release. Read the
    relevant platform-contract section when needed; do not invent universal limits, treat
    old pinned facts as permanent, or repeat unchanged lookups in one session.
11. Do not perform unrequested source-control operations. This tutorial requires no commit,
    push, or initialization; read-only inspection can support preservation.
12. A deployment does not prove an agent works. Record installation and live behavior
    separately. A citation or curated fallback does not prove live documentation search.

## Dependencies and attribution

The sibling `forge-app-builder` supplies `scripts.create_forge_app`. Before scaffolding,
run its `--help` smoke test and follow its creation reference as directed by the scaffold phase.
Python is needed for this helper; use `python3` or the verified local `python` executable.
Do not install dependencies merely to greet or teach the user.

Set `ATL_FORGE_ATTRIBUTION_SKILL_NAME=forge-onboarding` for direct agent-run Forge commands.
Use an environment mapping when supported; otherwise use the user's shell syntax from
[Setup](references/setup.md#attribution). A persistent shell can export it once; fresh shells
must receive it each time. Exclude user-run login and tunnel commands.
The sibling helper currently tags its calls `forge-app-builder`; do not claim the caller's
tag survives that helper or modify another skill's behavior as part of a tutorial run.

## Teach concisely

Start each phase with its user-facing title. Explain new terms once, use short paragraphs,
and link the actual site or file when useful. Prefer concise concept summaries over scripts
to recite. Ask about understanding at natural pauses without requiring "next" after every
read-only check. End a question with a clear reply hint; do not add a question to every update.
Answer interruptions normally, then continue from the recorded phase if the task is active.

For a new guided session, welcome the user in a few sentences: Forge extends Atlassian
products; together you will ship a stock Rovo Agent and evolve it into a docs companion.
Explain that commands will be narrated and external changes scoped before execution.
Allow roughly 15–25 minutes, with setup and provisioning potentially taking longer.
Ask if they are ready only if they have not already asked to begin.

## Completion and handoff

Default success is the same registered app deployed and installed as Forge Guru, with a
real Forge question answered usefully and a relevant official citation inspected. Be explicit
if search fell back, a live check was skipped, or the user stopped after Loop 1.
Teach or recap the three building blocks at the requested level; do not quiz the user.
Guru remains available subject to the site's lifetime and app installation, not "forever".

Use `forge-app-builder` for subsequent feature work, `forge-debugger` for sustained diagnosis,
`forge-app-review` for release review, and `forge-connector` for connector work. Read
[Next steps](references/next-steps.md) when closing or discussing those routes.
