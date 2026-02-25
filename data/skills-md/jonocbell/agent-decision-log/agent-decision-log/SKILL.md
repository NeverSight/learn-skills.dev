---
name: agent-decision-log
description: "Persistent decision log that creates a read-write feedback loop: read previous decisions before starting work, respect or supersede them, and write new Y-statement records as you go. Activates during any task involving architectural, structural, or design decisions - choosing libraries, designing schemas, creating modules, making tradeoffs, selecting patterns. Also activates when DECISIONS.md already exists in the project. Do NOT activate for trivial changes like typos, renames, or formatting."
license: Apache-2.0
metadata:
  author: jonocbell
  version: "1.0.0"
---

# Decision Log

## What this skill does

This skill creates institutional memory for codebases. It works as a loop:

1. **Read** — Before starting work, check for existing decisions and let them shape your approach
2. **Work** — Build what the user has asked for
3. **Write** — Record the significant decisions you made and why

Without this loop, every agent session starts from zero. The code shows what was built, but not why it was built that way, what alternatives were considered, or what tradeoffs were accepted. Over time, this creates codebases where nobody — human or machine — can explain the rationale behind key choices.

This skill fixes that. Decisions persist between sessions. The agent that works on this project tomorrow benefits from the reasoning of the agent that worked on it today.

---

## Step 1: Read existing decisions

At the start of every task, check whether `DECISIONS.md` exists in the project root.

**If it exists**, read it before doing anything else. These are decisions made by previous agents or developers. They represent accumulated reasoning about this specific project and should be treated seriously.

When reading existing decisions:

- **Note active constraints.** If a previous decision chose a specific library, pattern, or architecture, your work should be consistent with that choice unless there is a strong reason to change it.
- **Identify relevant context.** Previous decisions often contain rationale that applies to your current task, such as "we chose this database because the client needs multi-currency support later." That context should inform how you approach related work.
- **Look for conventions.** The collection of decisions often reveals implicit standards (error handling patterns, naming conventions, architectural style) even when no single decision states them explicitly.
- **Check for staleness.** If a decision references a constraint that no longer applies (a library that has been removed, a requirement the user has since changed), note this but do not silently ignore the decision. Flag it in your new records.

**If it does not exist**, that is fine. Proceed with the task and create the file when you make your first significant decision.

### How previous decisions should influence your work

Previous decisions are strong defaults, not rigid constraints. Follow this hierarchy:

1. **Respect by default.** If a previous decision is relevant to your current task, follow the established approach unless the user's request directly conflicts with it or you have a clear technical reason not to.
2. **Ask when uncertain.** If the user's request seems to conflict with a previous decision, mention the conflict and ask how they want to proceed before overriding it. For example: "There's an existing decision to use Zod for validation across the project. Your request uses Joi. Would you like me to stick with Zod for consistency, or switch to Joi and update the decision log?"
3. **Supersede when justified.** If you have a clear reason to change direction, do it — but write a new decision record that explicitly supersedes the old one and explains what changed. Never silently contradict a previous decision.

---

## Step 2: Work on the task

Build what the user has asked for. As you work, be aware of the decisions you are making. Not every line of code involves a decision worth recording, but many tasks involve at least one significant choice. Stay alert for the moments described in the "When to write a record" section below.

---

## Step 3: Write new decision records

After implementing a decision (not before — you need to know what you actually did), append a record to `DECISIONS.md` in the project root. Create the file if it does not exist, using the template in `references/DECISIONS_TEMPLATE.md`.

### The Y-Statement format

Every decision record follows the Y-statement format, an established convention in software architecture. It captures the essential elements of a decision in a single structured statement.

**Short form** (for straightforward decisions):

> In the context of [situation], facing [concern], we decided for [option] to achieve [quality], accepting [downside].

**Long form** (preferred when the decision is complex or consequential):

> In the context of [situation], facing [concern], we decided for [option] and neglected [alternatives], to achieve [desired outcome], accepting [downside], because [rationale].

Each field serves a purpose:

- **Context**: The use case or task that prompted the decision. Ground this in what you were actually asked to do.
- **Concern**: The specific tension, constraint, or competing requirement you faced.
- **Decision**: What you chose. Be specific about the pattern, library, structure, or approach.
- **Alternatives neglected**: What you genuinely considered but rejected. Do not fabricate alternatives to make the record look thorough.
- **Desired outcome**: The quality attribute the decision serves — extensibility, performance, simplicity, security, maintainability, etc.
- **Downside accepted**: What you knowingly gave up. Every decision has a cost; name it.
- **Rationale**: Additional reasoning, especially context from the user's requirements that influenced the choice.

### Record template

```markdown
### [Short title describing the decision]

**Date:** YYYY-MM-DD
**Status:** Accepted
**Files:** [key files created or changed]

In the context of [situation],
facing [concern],
we decided for [option]
and neglected [alternatives],
to achieve [desired outcome],
accepting [downside],
because [rationale].
```

See `references/examples.md` for worked examples across different decision types, including superseding previous decisions and referencing earlier decisions in new work.

### When to write a record

Write a decision record when you:

- Create a new module, service, or significant file structure
- Choose a library, framework, or external dependency
- Design or modify a data model, schema, or database structure
- Define an API contract or endpoint pattern
- Make a security-related choice (authentication, data handling, access control)
- Make a performance tradeoff (caching, query optimisation, data structure choice)
- Choose between meaningfully different implementation approaches
- Introduce a pattern that will be repeated across the codebase
- Deviate from an existing convention in the codebase
- **Supersede or contradict a previous decision in the log**

Do NOT write a record for:

- Bug fixes where the fix is obvious from the error
- Formatting or linting changes
- Renaming for clarity
- Minor refactors that do not change behaviour or structure
- Changes where there was only one reasonable option

When in doubt: "Would a developer joining this project in six months benefit from knowing why I did this?" If yes, write the record.

### Superseding previous decisions

When a new decision contradicts or replaces an earlier one, do two things:

1. Update the old record's status:

```markdown
**Status:** Superseded by "Title of new decision"
```

2. In the new record, add a **Supersedes** field and explain what changed. See Example 7 in `references/examples.md` for a worked example.

---

## Writing guidelines

**Write after implementing, not before.** You need to record what you actually did, not what you planned to do.

**Keep records concise.** A good record is 3-8 lines. The Y-statement format is deliberately compact. If you are writing paragraphs, you are overexplaining.

**Use plain language.** Write for a developer who understands the codebase but was not present for this session. Avoid jargon specific to the current conversation.

**Reference the user's requirements when relevant.** If the user said something that directly shaped the decision ("we will need multi-currency support later"), include it in the rationale. This is exactly the context that gets lost between sessions.

**Do not fabricate alternatives.** Only list options you genuinely considered. If the choice was straightforward, say so.

**Group related decisions.** If a single task involves multiple connected decisions, write them as separate records or combine them if tightly coupled. Use your judgement.

---

## Working in teams

When multiple engineers are working in the same repo with their own agents, decisions will be written on separate branches. This is fine. The single-file approach means git will occasionally produce merge conflicts on `DECISIONS.md`, but these are trivial to resolve because each record is an independent block of text.

The more important issue is not merge conflicts but contradictory decisions. Two agents on different branches might make opposite choices without knowing about each other. One chooses Zod, the other chooses Joi. Both write valid records. This is actually useful — when the branches merge, the contradiction is visible in the log in a way it would not be visible in the code alone.

Follow these practices when working on a branch:

- **Check for upstream changes.** Before making a significant decision, check whether `DECISIONS.md` on the main branch has been updated since your branch was created. If new decisions have been added that are relevant to your current work, read them and account for them.
- **Note your branch context.** If you are aware that your work is happening in parallel with other active branches, mention this in your decision record. For example: "This decision was made on branch feature/auth-redesign. If other branches have made related choices about session management, those should be reconciled at merge time."
- **Flag decisions that need team alignment.** Some decisions are local to a feature and safe to make independently. Others affect the whole codebase and should not be made in isolation. If you are making a decision that could conflict with work happening elsewhere (choosing a major dependency, changing a shared data model, altering an API contract), note it clearly so reviewers catch it during PR review.

When reviewing pull requests, check the decision records alongside the code. If two PRs contain conflicting decisions, resolve the conflict before merging and update the losing record's status to superseded.

---

## What this is not

**Not a changelog.** This does not record every change. The git history does that. This records the reasoning behind significant choices.

**Not a design document.** This does not describe the full architecture. It captures individual decision points. Over time, the collection tells the story of how the architecture evolved and why.

**Not an ADR process.** Traditional Architecture Decision Records are heavyweight documents created through a deliberate review process. This is lighter and more continuous — decisions are captured in the flow of work, not as a separate activity.
