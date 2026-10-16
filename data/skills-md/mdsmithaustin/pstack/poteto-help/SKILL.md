---
name: poteto-help
description: Guides users through pstack setup, /poteto-mode, and picking the skill, playbook, or principle for a task. Type /poteto-help with a question.
---

# Poteto help

Answer the user's question about pstack, hand them a prompt they can send, and link the file the answer came from. For a help question, don't start the work. The user asked how, and a pstack run spends real tokens, so let them send the prompt.

A message that asks for work, such as "use pstack to fix this bug", is not a help question. Use the **poteto-mode** skill and do the work under it.

This file maps questions to the skills and guide pages that hold the answers. Those files own the details. Read the file you route to before you quote it, and trust it when it disagrees with this map. Read a sibling skill from the installed skills root. The README and guide pages don't ship with an installed skill, so read them from a pstack checkout when the session runs in one, and otherwise from their public copy. Give the user the file's public copy: `https://github.com/mdsmithaustin/pstack/blob/main/` followed by its repository path, such as `skills/how/SKILL.md` or `docs/guide/01-setup.md`. A skill's file sits under `skills/`, so a path relative to the skills root, such as `how/SKILL.md`, 404s.

## Find out what they need

Infer the need from the message and the conversation. A named situation, such as "which skill reviews a PR?", goes straight to its section. If the need is still unclear, ask one multiple-choice question with these options, then answer only the section they pick:

- Get set up
- Start a task with `/poteto-mode`
- Pick a skill for a situation
- Fix a run that went wrong
- Make pstack my own

Check the state that changes the answer, and mention it only when it does:

- No `~/.agents/pstack-models.md` and no workspace `.agents/pstack-models.md` means `/setup-pstack` hasn't run for this user, so every role uses its default model.
- No `verify-*` skill or other app harness in the project means agents have no scripted way to drive the app. Mention `/create-verification-skill` when the question is about proving a change works.

When the models config is missing and it matters, ask whether the user wants to pick a model for each role and a reasoning budget now. It matters when the user is new, the question is about setup or cost, or the answer depends on which models run. Ask at most once per chat. If the need is also unclear, ask both questions together. Offer two choices:

- Now: give them `/setup-pstack` to type, and answer their question too.
- Later: answer their question, and add one line saying every role keeps its default model until they run `/setup-pstack`.

## Get set up

1. Install from the project root with `npx skills add mdsmithaustin/pstack`, and pick the targets the user runs. `-g` installs user-level instead of per-project.
2. Run [`/setup-pstack`](../setup-pstack/SKILL.md). It checks the bundled personas, asks for a reasoning budget, maps a model to each role, and writes `~/.agents/pstack-models.md`. Skills read that file the next time they run. On Claude Code it also sets the skill listing, so the skills that load only by name stop showing their descriptions.
3. Start a real task with `/poteto-mode`, a goal, and a check that can pass or fail.

The skills that load from the user's words are listed under Fix a run that went wrong. For invocation behavior and the Claude Code setup requirement, see the [README](https://github.com/mdsmithaustin/pstack/blob/main/README.md#get-started). [Guide page 1](https://github.com/mdsmithaustin/pstack/blob/main/docs/guide/01-setup.md) covers setup in detail. Offer to word their first prompt with them, per [`references/prompting.md`](references/prompting.md).

If cost is the worry, say where the tokens go and how to spend fewer. pstack spends extra tokens on subagents and review panels. Rerun `/setup-pstack` and pick a smaller budget or cheaper models. A role set to `auto` or `inherit-parent` runs on the session's model, which saves tokens when the session runs on a cheaper model. A shorter panel list runs fewer subagents, one for each entry. Save `/poteto-mode` for work that needs rigor.

pstack runs in Claude Code, Codex, Hermes, and Grok Build. Most workflow skills, including `/poteto-mode`, `/how`, `/why`, and `/poteto-teach`, spawn subagents with per-role models. The [`pstack-harness`](../pstack-harness/SKILL.md) skill maps spawning, models, worklists, and loops to each CLI. Hermes has no translation for the shipped Claude aliases, so on Hermes a default role runs on the session model and a default multi-model panel becomes a same-model panel. A Hermes model name written in the models config runs as written.

## Start a task with `/poteto-mode`

`/poteto-mode` matches the task to a playbook, copies the playbook's opening prose and steps into the worklist, and runs the other skills as the steps need them. A step it skips stays in the list as `skipped: <reason>`. With the task tools off, the worklist is a numbered list in chat. A good prompt states the goal and how to tell it's done. It doesn't list skills, because a hand-written sequence tends to drop or reorder steps the playbook would keep. Read [`references/prompting.md`](references/prompting.md) before you help word one. [Guide page 2](https://github.com/mdsmithaustin/pstack/blob/main/docs/guide/02-poteto-mode.md) has examples.

`/poteto-mode` is sticky. Once invoked, it stays on for the conversation, applies itself when a playbook matches or the task needs rigor, and stays out of the way otherwise. The user opts out by saying so. In a very long chat, the CLI may compress older messages and drop the mode, so tell the user to invoke `/poteto-mode` again if it stops applying. Mid-chat, "new task" makes the mode match a fresh playbook. `/poteto-mode` already uses `poteto-agent` for the subagents its playbook steps spawn. To get the same style from a subagent of your own, spawn the `poteto-agent` persona as the **pstack-harness** skill's Spawn a role section describes. `/setup-pstack` can register it as a native agent.

## Pick a skill

The default answer is `/poteto-mode`, which runs most of the others when its steps need them. Name a skill directly when the user wants more or less of something than the playbook gives. Read the skill before you recommend it, and give one example prompt.

| The user wants to | Skill |
|---|---|
| Do any non-trivial task with rigor | [`/poteto-mode`](../poteto-mode/SKILL.md) |
| Know how code works now, or where new code should live | [`/how`](../how/SKILL.md) |
| Know why code is shaped this way, or where a number came from | [`/why`](../why/SKILL.md) |
| Understand a change or subsystem, explained plainly | [`/poteto-teach`](../poteto-teach/SKILL.md) |
| Catch up on their own recent work on a topic | [`/recall`](../recall/SKILL.md) |
| Catch up on everything in this chat since their last message, with enough context to decide each action item | [`/ketchup`](../ketchup/SKILL.md) |
| Know what a small diff could break outside itself | [`/blast-radius`](../blast-radius/SKILL.md) |
| Settle types and module shape before code that crosses a function boundary | [`/architect`](../architect/SKILL.md) |
| Get several attempts at one brief, merged into the best one | [`/arena`](../arena/SKILL.md) |
| Run parallel checks over slices, or race workers, as parallel subagents | [`/swarm`](../swarm/SKILL.md) |
| Have different models review a diff and try to break it | [`/interrogate`](../interrogate/SKILL.md) |
| Fix a bug test-first when a cheap local test exists | [`/poteto-tdd`](../poteto-tdd/SKILL.md) |
| Apply TypeScript rules to `.ts` or `.tsx` work | [`/typescript-best-practices`](../typescript-best-practices/SKILL.md) |
| Strip comments before review, using a reviewer that didn't write them | [`/no-comments`](../no-comments/SKILL.md) |
| Clean slop out of the code a branch changed before a commit | [`/deslop`](../deslop/SKILL.md) |
| Clean AI tells out of prose | [`/unslop`](../unslop/SKILL.md) |
| Write docs, an RFC, a README, a PR description, or a commit message to a standard | [`/technical-writing`](../technical-writing/SKILL.md) |
| Update or review the docs a change affects | [`/documentation-impact`](../documentation-impact/SKILL.md) |
| Hear the last reply again in plain words | [`/bro`](../bro/SKILL.md) |
| Give agents a scripted way to drive the app and prove behavior | [`/create-verification-skill`](../create-verification-skill/SKILL.md) |
| Bring a verification skill and its feature map back in line with the app | [`/maintain-verification-skill`](../maintain-verification-skill/SKILL.md) |
| Write a test invocation, CI gate, or shell assertion that can't pass while measuring nothing | [`/verify-commands`](../verify-commands/SKILL.md) |
| Find the edge cases and must-nevers in a spec before any code exists | [`/spec-probes`](../spec-probes/SKILL.md) |
| Probe a running product, feature, or PR for unreported bugs | [`/runtime-probes`](../runtime-probes/SKILL.md) |
| Vet a performance number before reporting or acting on it | [`/benchmark-checklist`](../benchmark-checklist/SKILL.md) |
| Run a large or cross-cutting change, or one to review after stepping away | [`/figure-it-out`](../figure-it-out/SKILL.md) |
| Keep a decision log during a run, and review it afterward | [`/show-me-your-work`](../show-me-your-work/SKILL.md) |
| Pick a model for each role and a reasoning budget | [`/setup-pstack`](../setup-pstack/SKILL.md) |
| Turn their own working habits into a personal mode skill | [`/automate-me`](../automate-me/SKILL.md) |
| Turn what a finished task taught into skill edits | [`/reflect`](../reflect/SKILL.md) |
| Stop agents from repeating the same mistakes in this repo | [`/correct`](../correct/SKILL.md) |
| Build a page whose buttons wake a Grok Bot over a webhook | [`/make-bot-ui`](../make-bot-ui/SKILL.md) |
| Find their way around pstack | `/poteto-help` |

If a skill directory next to this one is missing from the table, read its frontmatter and route by its description. The `principle-*` directories are covered under principles below.

Close calls:

- `/how` explains what the code does. `/why` explains the reasons. `/poteto-teach` runs one or both and explains the result plainly.
- `/arena` gives every worker the same brief and merges the best parts. `/swarm` splits work into slices or a race and returns one report.
- `/architect` implements right after it settles the design. Add "with checkpoint" to review the design before it writes code.
- `/interrogate` reviews the diff. `/blast-radius` looks for breakage outside the diff and proves the one fact that makes the change safe.
- `/deslop` cleans code. `/unslop` cleans prose.
- `/recall` rebuilds context across recent chats. `/ketchup` covers only this chat since the user's last message. Resuming one specific chat or branch is the Session pickup playbook.
- `/figure-it-out` designs one rigorous run. The Orchestrate playbook runs a program that spans days and many PRs. The Autonomous run playbook drives one task to a finish condition.

Not in pstack:

- `control-cli` and `control-ui` belong to a Cursor plugin. pstack drives the app through the project's own `verify-<app>` skill, which `/create-verification-skill` writes.
- `/loop` is the CLI's wake mechanism, not a pstack skill. Claude Code has one built in. In a CLI without one, re-prompt on an interval or run a watcher subagent.
- pstack has no `/orchestrate` skill. Orchestrate is a `/poteto-mode` playbook. If the slash menu shows `/orchestrate`, another skill set provides it.

## Playbooks and principles

Playbooks are step lists inside `/poteto-mode`, not skills, so they have no slash command. Inside `/poteto-mode`, describing the task picks one, and these phrases name one directly:

- "babysit this pr" or "check on pr 123" runs Babysit. It drives the PR to merge-ready and stops there. It doesn't merge unless the user asks to merge, land, or ship.
- "review this pr" runs Code review, for someone else's pull request, branch, or diff.
- "land the stack" runs Shipping.
- "take over this branch" runs Session pickup.
- "pause safely" runs Pause safely.
- "full autopilot on this queue" runs Autopilot-full. "stack them, don't ship" runs Autopilot-stack.
- "run the eval playbook" runs Eval.

Without `/poteto-mode`, a phrase such as "babysit this pr" can start a similarly named skill from the CLI or another skill set instead. The Playbooks section of [`poteto-mode`](../poteto-mode/SKILL.md) lists every playbook and when it applies. [Guide page 6](https://github.com/mdsmithaustin/pstack/blob/main/docs/guide/06-verify-and-ship.md) covers opening, babysitting, and landing a PR.

pstack has no planning skill. A CLI's own plan mode works alongside it. For work that spans phases or stacked PRs, asking `/poteto-mode` for a plan runs the [Multi-phase plan playbook](../poteto-mode/playbooks/multi-phase-plan.md), which writes the plan and doesn't implement it. For a design question, the Prototype playbook or `/architect` settles it in code first.

Principles are one-rule skills that `/poteto-mode` reads and cites in its replies. The user rarely invokes one. They steer with the names instead, as in "apply prove it works. show me the real output." Typing `/principle-<name>` still loads one on demand. [Guide page 8](https://github.com/mdsmithaustin/pstack/blob/main/docs/guide/08-principles.md) lists them.

## Fix a run that went wrong

| Symptom | Fix |
|---|---|
| The mode stopped applying | Invoke `/poteto-mode` again, or start each task with it. |
| A question got treated as the next step of the last task | Say "new task", or say the turn doesn't need the mode. |
| A new model choice had no effect | A workspace `.agents/pstack-models.md` overrides the home file, and a harness section such as `## codex` beats a flat line. On Claude Code, a written effort applies only once `/setup-pstack` has registered pstack's effort agents. |
| Runs cost more than expected | See the cost paragraph under Get set up. |
| A skill didn't load on its own | On Codex, and on Claude Code once `/setup-pstack` sets the skill listing, only `/setup-pstack`, `/how`, `/why`, `/unslop`, `/deslop`, `/documentation-impact`, `/verify-commands`, `/spec-probes`, and `/runtime-probes` load from the user's words. The others load when the user types them or when another pstack skill, such as `/poteto-mode`, tells the agent to use them. `/poteto-mode` doesn't run every skill. |
| Parallel agents overwrote each other | Give each agent its own worktree. |
| An overnight run moved but finished nothing | `/loop` needs a check that can pass or fail, not a duration. See [guide page 7](https://github.com/mdsmithaustin/pstack/blob/main/docs/guide/07-overnight.md). |
| The reply claims success from a green build | Ask for the real command, flow, stored value, or profile. That's the prove-it-works principle. |

For a run that drifts, [`references/prompting.md`](references/prompting.md) has one-line steers. [Guide page 10](https://github.com/mdsmithaustin/pstack/blob/main/docs/guide/10-recipes-and-pitfalls.md) has more pitfalls and the recipes worth copying.

## Make pstack my own

- [`/automate-me`](../automate-me/SKILL.md) drafts a personal mode skill from the user's own history, to use alongside `/poteto-mode`.
- [`/reflect`](../reflect/SKILL.md) after a session turns its lessons into skill edits the user approves.
- `/poteto-mode write a skill for <workflow>` runs the authoring playbook. The eval playbook tests a skill change blind.
- Fix a misbehaving skill in its own PR, not inside the feature work where it went wrong.

[Guide page 9](https://github.com/mdsmithaustin/pstack/blob/main/docs/guide/09-make-it-yours.md) covers each of these.

## Reply

Lead with the answer. Give at most one example prompt in a code block, adapted from [`references/recipes.md`](references/recipes.md) when one fits, then the link to that file. Keep it short unless the user asked for the whole map.
