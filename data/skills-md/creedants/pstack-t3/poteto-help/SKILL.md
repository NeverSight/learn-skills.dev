---
name: poteto-help
description: "Guides users through pstack setup, $poteto-mode, and picking the skill, playbook, or principle for a task. Type $poteto-help with a question."
---

# Poteto help

Read [the pstack-t3 runtime](../pstack-runtime/SKILL.md) before spawning workers, choosing models, scheduling, or isolating work. It maps those steps onto T3's orchestrator tools.

Answer the user's question about pstack, hand them a prompt they can send, and link the file the answer came from. For a help question, don't start the work. The user asked how, and a pstack run spends real tokens, so let them send the prompt.

A message that asks for work, such as "use pstack to fix this bug", is not a help question. Read [`poteto-mode`](../poteto-mode/SKILL.md), do the work under it, and mention once that the next task should start with `$poteto-mode`.

This file maps questions to the skills and guide sections that hold the answers. Those files own the details. Read the file you route to before you quote it, and trust it when it disagrees with this map. The links here point into the installed skills, which the user may not be able to open, so give the user the file's public copy: `https://github.com/creedants/pstack-t3/blob/main/` followed by its path.

## Find out what they need

Infer the need from the message and the conversation. A named situation, such as "which skill reviews a PR?", goes straight to its section. If the need is still unclear, ask one multiple-choice question with these options, then answer only the section they pick:

- Get set up
- Start a task with `$poteto-mode`
- Pick a skill for a situation
- Fix a run that went wrong
- Make pstack my own

Check the state that changes the answer, and mention it only when it does:

- No `.pstack/t3-roles.json`, and no `~/.config/pstack-t3/roles.json` or `$XDG_CONFIG_HOME/pstack-t3/roles.json`, means `$setup-pstack` hasn't run for this user, so every role uses its default model. [Built-in defaults](../pstack-runtime/SKILL.md#built-in-defaults) lists them.
- No `verify-*` skill or other app harness in the project means agents have no scripted way to drive the app. Mention `$create-verification-skill` when the question is about proving a change works.

When no roles file exists and it matters, ask whether the user wants to pick a model for each role and a reasoning budget now. It matters when the user is new, the question is about setup or cost, or the answer depends on which models run. Ask at most once per chat. If the need is also unclear, ask both questions together. Offer two choices:

- Now: give them `$setup-pstack` to type, and answer their question too.
- Later: answer their question, and add one line saying every role keeps its default model until they run `$setup-pstack`.

## Get set up

1. `git clone https://github.com/creedants/pstack-t3.git ~/pstack-t3`, then run `python3 scripts/install.py` in that directory. Then run `python3 scripts/install.py doctor`. Each provider should show the same count on both sides of `N/N pstack-t3`.
2. Run [`$setup-pstack`](../setup-pstack/SKILL.md). It asks for a reasoning budget, maps a model to each role, and writes `~/.config/pstack-t3/roles.json`, or `$XDG_CONFIG_HOME/pstack-t3/roles.json` when that variable is set. Every skill reads that file when it resolves roles.
3. Start a real task with `$poteto-mode`, a goal, and a check that can pass or fail.

Typing `$name` loads a skill. Most skills can also load when the request matches their description. `$poteto-help` has a narrow description, so type it. The [README](https://github.com/creedants/pstack-t3/blob/main/README.md) and [install section](https://github.com/creedants/pstack-t3/blob/main/docs/guide.md#1-install-two-minutes) have the details. Offer to word their first prompt with them, per [`references/prompting.md`](references/prompting.md).

If cost is the worry, say where the tokens go and how to spend fewer. pstack spends extra tokens on subagents and review panels. Rerun `$setup-pstack` and pick a smaller budget or cheaper models. A role set to `inherit` runs on the chat's model, which saves tokens when the chat runs on a cheaper model. A shorter panel list runs fewer subagents, one for each entry. Save `$poteto-mode` for work that needs rigor.

pstack-t3 runs in T3 Code. [Outside T3](../pstack-runtime/SKILL.md#outside-t3) covers other hosts.

## Start a task with `$poteto-mode`

`$poteto-mode` matches the task to a playbook, copies the playbook's steps into the todo list, and runs the other skills as the steps need them. A step it skips stays in the list as `skip: <reason>`. A good prompt states the goal and how to tell it's done. It doesn't list skills, because a hand-written sequence tends to drop or reorder steps the playbook would keep. Read [`references/prompting.md`](references/prompting.md) before you help word one. [The guide's first task](https://github.com/creedants/pstack-t3/blob/main/docs/guide.md#3-your-first-rigorous-task) has an example.

Whether `$poteto-mode` stays on:

- Naming `$poteto-mode` in a message attaches the skill to that message. It fades as the chat moves on.
- T3 has no switch that pins the skill on later tasks. Start the next task with `$poteto-mode` again.

Mid-chat, "new task" makes the mode match a fresh playbook. `$poteto-mode` already uses the poteto-agent persona for the subagents its playbook steps spawn. To get the same style from a subagent of your own, call `delegate_task` and paste the body of [`../pstack-runtime/agents/poteto-agent.md`](../pstack-runtime/agents/poteto-agent.md) at the top of the brief. [The runtime](../pstack-runtime/SKILL.md) has the call shape.

## Pick a skill

The default answer is `$poteto-mode`, which runs most of the others when its steps need them. Name a skill directly when the user wants more or less of something than the playbook gives. Read the skill before you recommend it, and give one example prompt.

| The user wants to | Skill |
|---|---|
| Do any non-trivial task with rigor | [`$poteto-mode`](../poteto-mode/SKILL.md) |
| Know how code works now, or where new code should live | [`$how`](../how/SKILL.md) |
| Know why code is shaped this way, or where a number came from | [`$why`](../why/SKILL.md) |
| Understand a change or subsystem, explained plainly | [`$teach`](../teach/SKILL.md) |
| Catch up on their own recent work on a topic | [`$recall`](../recall/SKILL.md) |
| Catch up on everything in this chat since their last message, with enough context to decide each action item | [`$ketchup`](../ketchup/SKILL.md) |
| Know what a small diff could break outside itself | [`$blast-radius`](../blast-radius/SKILL.md) |
| Settle types and module shape before code that crosses a function boundary | [`$architect`](../architect/SKILL.md) |
| Get several attempts at one brief, merged into the best one | [`$arena`](../arena/SKILL.md) |
| Run parallel checks over slices, or race workers | [`$swarm`](../swarm/SKILL.md) |
| Let many agents write one repo without colliding | [`$landing`](../landing/SKILL.md) |
| Have different models review a diff and try to break it | [`$interrogate`](../interrogate/SKILL.md) |
| Fix a bug test-first when a cheap local test exists | [`$tdd`](../tdd/SKILL.md) |
| Apply TypeScript rules to `.ts` or `.tsx` work | [`$typescript-best-practices`](../typescript-best-practices/SKILL.md) |
| Strip comments before review, using a reviewer that didn't write them | [`$no-comments`](../no-comments/SKILL.md) |
| Clean AI tells out of prose | [`$unslop`](../unslop/SKILL.md) |
| Write docs, an RFC, a README, a PR description, or a commit message to a standard | [`$technical-writing`](../technical-writing/SKILL.md) |
| Hear the last reply again in plain words | [`$bro`](../bro/SKILL.md) |
| Give agents a scripted way to drive the app and prove behavior | [`$create-verification-skill`](../create-verification-skill/SKILL.md) |
| Bring a verification skill and its feature map back in line with the app | [`$maintain-verification-skill`](../maintain-verification-skill/SKILL.md) |
| Vet a performance number before reporting or acting on it | [`$benchmark-checklist`](../benchmark-checklist/SKILL.md) |
| Run a large or cross-cutting change, or one to review after stepping away | [`$figure-it-out`](../figure-it-out/SKILL.md) |
| Give a project or focus area a standing coordinator | [`$brigade`](../brigade/SKILL.md) |
| Run one executive admin over the coordinators on one repository | [`$brigade-admin`](../brigade-admin/SKILL.md) |
| Keep a decision log during a run, and review it afterward | [`$show-me-your-work`](../show-me-your-work/SKILL.md) |
| Pick a model for each role and a reasoning budget | [`$setup-pstack`](../setup-pstack/SKILL.md) |
| See how a skill delegates, picks models, isolates work, and schedules | [`$pstack-runtime`](../pstack-runtime/SKILL.md) |
| Turn their own working habits into a personal mode skill | [`$automate-me`](../automate-me/SKILL.md) |
| Write or tune a skill so it works on every provider T3 runs | [`$pstack-author-skill`](../pstack-author-skill/SKILL.md) |
| Turn what a finished task taught into skill edits | [`$reflect`](../reflect/SKILL.md) |
| Stop agents from repeating the same mistakes in this repo | [`$correct`](../correct/SKILL.md) |
| Build a page whose buttons wake a Grok Bot over a webhook | [`$make-bot-ui`](../make-bot-ui/SKILL.md) |
| Find their way around pstack | `$poteto-help` |

If a skill directory next to this one is missing from the table, read its frontmatter and route by its description. The `principle-*` directories are covered under principles below.

Close calls:

- `$how` explains what the code does. `$why` explains the reasons. `$teach` runs one or both and explains the result plainly.
- `$arena` gives every worker the same brief and merges the best parts. `$swarm` splits work into slices or a race and returns one report.
- `$architect` implements right after it settles the design. Add "with checkpoint" to review the design before it writes code.
- `$interrogate` reviews the diff. `$blast-radius` looks for breakage outside the diff and proves the one fact that makes the change safe.
- `$recall` rebuilds context across recent chats. `$ketchup` covers only this chat since the user's last message. Resuming one specific chat or branch is the Session pickup playbook.
- `$figure-it-out` designs one rigorous run. The Orchestrate playbook runs a program that spans days and many PRs. The Autonomous run playbook drives one task to a finish condition.
- `$landing` is the queue several agents share when they write one repo. `$brigade` is the standing thread that sends work to that queue.

Not in pstack:

- `$deslop`, `control-cli`, and `control-ui` are optional. Use them when they are installed. If `$deslop` is not installed, strip the slop with [`$unslop`](../unslop/SKILL.md). If `control-cli` or `control-ui` is not installed, drive a CLI in the terminal and a web UI with T3's preview tools.
- Recurring work uses `schedule_task`, a T3 tool.
- pstack has no `$orchestrate` skill. Orchestrate is a `$poteto-mode` playbook. If the `$` picker shows `$orchestrate`, another skill provides it.

## Playbooks and principles

Playbooks are step lists inside `$poteto-mode`, not skills, so they have no `$` command of their own. Inside `$poteto-mode`, describing the task picks one, and these phrases name one directly:

- "babysit this pr" or "check on pr 123" runs Babysit. It drives the PR to merge-ready and stops there. It doesn't merge unless the user asks to merge, land, or ship.
- "land the stack" runs Shipping.
- "take over this branch" runs Session pickup.
- "pause safely" runs Pause safely.
- "full autopilot on this queue" runs Autopilot-full. "stack them, don't ship" runs Autopilot-stack.
- "run the eval playbook" runs Eval.

Without `$poteto-mode`, a phrase such as "babysit this pr" can start the host's own skill for the same job instead. The Playbooks section of [`poteto-mode`](../poteto-mode/SKILL.md) lists every playbook and when it applies. Opening, babysitting, and landing a PR are the [opening](../poteto-mode/playbooks/opening-a-pr.md), [babysit](../poteto-mode/playbooks/babysit.md), and [shipping](../poteto-mode/playbooks/shipping.md) playbooks.

pstack has no planning skill. T3's plan mode works alongside it. For work that spans phases or stacked PRs, asking `$poteto-mode` for a plan runs the [Multi-phase plan playbook](../poteto-mode/playbooks/multi-phase-plan.md), which writes the plan and doesn't implement it. For a design question, the Prototype playbook or `$architect` settles it in code first.

Principles are one-rule skills that `$poteto-mode` reads and cites in its replies. The user rarely invokes one. They steer with the names instead, as in "apply prove it works. show me the real output." Typing `$principle-<name>` still loads one on demand. The [skills catalog](https://github.com/creedants/pstack-t3/blob/main/docs/skills.md#principles) lists them.

## Fix a run that went wrong

| Symptom | Fix |
|---|---|
| The mode stopped applying after a few turns | It was loaded by one message and faded. Start each task with `$poteto-mode`, or name it again when it drifts. |
| A question got treated as the next step of the last task | Say "new task", or say the turn doesn't need the mode. |
| A new model choice had no effect | A project `.pstack/t3-roles.json` overrides the same role from the user file. Run `roles.py show` to see which file won. [Where roles live](../pstack-runtime/SKILL.md#where-roles-live). |
| Runs cost more than expected | See the cost paragraph under Get set up. |
| A skill didn't load on its own | Typing `$name` always loads a skill. A skill also loads when its description matches, and `$poteto-mode` doesn't run every skill. |
| Parallel agents overwrote each other | Give each writer its own git worktree. For several agents on one repo, use [`$landing`](../landing/SKILL.md) so each claims paths before it writes. |
| An overnight run moved but finished nothing | `schedule_task` needs a check that can pass or fail, not a duration. See [Leave it running](https://github.com/creedants/pstack-t3/blob/main/docs/guide.md#6-leave-it-running). |
| The reply claims success from a green build | Ask for the real command, flow, stored value, or profile. That's the prove-it-works principle. |

For a run that drifts, [`references/prompting.md`](references/prompting.md) has one-line steers. [Tips and pitfalls](https://github.com/creedants/pstack-t3/blob/main/docs/guide.md#tips-and-pitfalls) has more.

## Make pstack my own

- [`$automate-me`](../automate-me/SKILL.md) drafts a personal mode skill from the user's own history, to use alongside `$poteto-mode`.
- [`$reflect`](../reflect/SKILL.md) after a session turns its lessons into skill edits the user approves.
- `$poteto-mode write a skill for <workflow>` runs the authoring playbook. [`$pstack-author-skill`](../pstack-author-skill/SKILL.md) writes one for every provider T3 runs. The eval playbook tests a skill change blind.
- Fix a misbehaving skill in its own PR, not inside the feature work where it went wrong.

## Reply

Lead with the answer. Give at most one example prompt in a code block, adapted from [`references/recipes.md`](references/recipes.md) when one fits, then the link to that file. Keep it short unless the user asked for the whole map.
