---
name: setup-brad-frost-skills
description: START HERE after installing Brad Frost's skills — run this once to get everything set up. Finds which of the skills you installed, runs the setup each one needs (the limits interview), and tells you how to use the ones that need no setup. Use when the user says "setup brad frost skills", runs /setup-brad-frost-skills, has just installed this collection, or asks how to get started with these skills.
---

# Setup: Brad Frost skills

You are the front door for this collection. Your job is to find out what
the person actually installed, run the setup that those skills need, and
get out of the way. You are a router, not a second interview — never
duplicate or paraphrase another skill's questions; invoke that skill and
let it speak for itself.

## 1. Find what's installed

Check which of these skills are available to you. Prefer your own view of
the installed skills; otherwise look for the directories in the agent's
skills locations (`~/.claude/skills/`, `.claude/skills/`,
`~/.agents/skills/`, `.agents/skills/`, or wherever this agent keeps
them):

| Family | Skills | Needs setup? |
|---|---|---|
| Limits | `limits-setup`, `limits-sessions`, `limits-quiet-hours`, `limits-endings`, `limits-energy` | **Yes** — the interview |
| Design systems | `ds-inspection`, `ds-adoption-plan` | No |
| Design systems | `ds-ascii` | **Yes** — build the design system profile |
| Product design | `product-inspection` | No |
| Product design | `vibe-killer` | **Yes** — build the design system profile |

If none of them are present, say so plainly and stop — tell them to
install first (`npx skills add bradfrost/skills -g`). Don't guess, and
don't run setup for a skill that isn't there.

## 2. Say what you found

One short line, then get on with it. For example:

> "Found the limits skills and the design system inspection skills. The
> limits skills need a quick setup; the inspection skills don't. Let's do
> the limits."

Nothing more — no feature tour, no list of everything each skill can do.

## 3. Run the setups that are needed

**If any `limits-*` skill is installed:** run the `limits-setup` skill and
follow it exactly. It owns its own script, its own questions, and its own
close. Do not restate its questions here, and do not add your own framing
around them.

If a config already exists at `~/.config/ai-limits/config`, say so and ask
whether they want to review and change their limits or leave them as they
are. Never silently overwrite limits someone already set.

**If `ds-ascii` is installed:** it needs a profile of the design system
it will be labeling before its first render. Ask whether they have a design
system they want it pointed at. If they do, run that skill's
`intake/PROFILE-INTAKE.md`, which reads the component vocabulary from a
manifest or an MCP where it can and interviews them where it can't. If they
don't have one, or they'd rather do it later, say that the skill will build
the profile the first time they use it and move on.

**If `vibe-killer` is installed:** it needs a profile of the design system
it will be converting pages onto. Ask whether they have one in mind. If they
do, run that skill's `intake/SYSTEM-INTAKE.md`, which reads the component
vocabulary and the runtime out of an MCP, a manifest, or a repo where it can
and interviews them where it can't. If they don't have a design system yet,
or they'd rather do it later, say the skill will build the profile the first
time they use it and move on.

If both `ds-ascii` and `vibe-killer` are installed, run whichever intake
they want first and say that the second one will read the first's profile
rather than asking everything again.

**As more skills in this collection grow setup steps, they get added
here** — this skill is the one place a person has to remember.

## 4. Point at what needs no setup

For anything installed that needs no setup, one line each — what it does
and how to start it:

- **`ds-inspection`** — run `/ds-inspection` from inside your design
  system's project
- **`product-inspection`** — run `/product-inspection` from inside the
  product's project
- **`ds-adoption-plan`** — run `/ds-adoption-plan` from inside a product
  you want moved onto your design system

Skip the ones they didn't install.

## 5. Close

If the limits interview ran, it already delivered its own close — don't
add a second one. Otherwise end plainly: they're set up, and they can run
this again any time they install more of these skills.
