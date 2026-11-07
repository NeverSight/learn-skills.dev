---
name: curating-global-instructions
description: Use when adding to, trimming or reorganizing the instruction file loaded into every session whatever the project — the global CLAUDE.md, AGENTS.md, or whatever plays that role — or when it has grown past what a session can hold.
---

# Curating Global Instructions

The global instruction file is read at the start of every session, whatever the project. Its length is a cost paid by every session that follows, so it should hold what **governs the work**: rules, invariants and decisions that must not be re-derived.

**Core principle:** every section is either a *rule* — something that must fire unconditionally — or a *technique*, which needs a trigger. Rules stay. Techniques move to a skill, where they load when wanted.

## The one question

Ask it of every section, and of everything you are about to add:

> Is this a rule, or a technique?

**A rule** — a constraint, a decision, a precedence — fires whether or not anything else loads. It stays. **A technique** — how to do something, once you know you are doing it — has a trigger, and belongs in a skill. Adding without asking this is how the file grows; trimming without asking it is how a rule disappears.

## Before moving anything to a skill

**Compare against the skill's BODY, not its description.** A description answers *"should I open this?"*; it does not answer *"what is inside?"*. A section is a duplicate only if the body already carries it — and then it is pure duplication, however useful it reads.

**Test the trigger, honestly.** Content may move only when the trigger names a situation the agent can recognise from the request: *"I am building a UI"* and *"review this diff"* pass. It fails when the trigger requires the skill's own diagnosis first — *"the code feels brittle"*, *"cleanup looks missing"* — because the agent cannot know it needs the skill until it has already learned what the skill teaches. Where the trigger is weak, keep the rule and point at the skill in one line.

**Write the new skill's description as a trigger, not a summary** — a summary becomes a shortcut the agent follows instead of reading the body.

When the skill you are drafting is more than a few lines, read `writing-skills` first if it is available: it covers naming, placement and how to check the result.

## What never moves

- **A decision no skill can enforce.** A skill can be read; it cannot compel.
- **A rule that contradicts a harness default** — this file is the only place that can override one.
- **The single failure that costs most when no skill is opened.** State it outright even though a skill covers it; that duplication is deliberate.

## Working the file

**Measure, do not guess.** Count each section before and after. "Feels long" is not a measurement, and a total that moved without a per-section number cannot be reported.

**One move at a time, verified.** After moving a section, grep the names, paths and terms it carried — an orphaned reference to a section that no longer exists is the failure this work produces.

**Replace or delete a superseded line; never banner it.** A line explaining what the file used to say is itself a cost paid every session.

## Common mistakes

| Mistake | Fix |
|---|---|
| Trimming by feel, or toward a target percentage | Measure per section and report the numbers |
| Deleting a section because a skill "covers that area" | Read the body — areas are not contents |
| Moving content whose trigger needs the skill's own diagnosis (e.g. "the code feels brittle") | The agent cannot recognise the problem until the content has taught it; keep the rule |
| A description that summarizes the new skill's steps | Make it a trigger; see `writing-skills` |
