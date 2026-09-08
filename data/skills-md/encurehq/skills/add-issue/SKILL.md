---
name: add-issue
description: Draft and publish a Linear issue whose description is a complete, phased execution plan another agent can pick up cold and run. Use when the user says "create a Linear issue for X", "file a ticket for X", "add an issue to Linear", "write up a plan and put it in Linear", or wants work handed off to a teammate/agent via a Linear issue rather than implemented right now.
---

# Create a Linear issue with a phased plan

Draft a single Linear issue whose description is a complete, phased execution plan — good enough that a teammate's own agent can pick it up cold and execute it, with no further back-and-forth. This skill only **creates the issue**; it never implements anything itself, and the plan it writes never includes a commit step — whoever executes it decides that on their own.

## Step 1 — Gather context

Work from whatever is already in the conversation — don't ask the user to re-explain something already established. The arguments passed to this skill are the explanation of the issue to create; parse them for the substance (what to build/fix) plus any explicitly named project, assignee, or priority (see Step 4).

If the argument names a reference — a spec file path, an existing issue ID/URL, a PR — fetch it and read its full body before drafting anything.

Explore the codebase before drafting the plan:

- Find the files the plan will actually touch. Read them well enough to name exact paths, exact function/component names, and current line ranges — the plan must never say "similar to X" or "the usual pattern," it must show the pattern.
- Use the project's own domain vocabulary for naming — if the repo has a glossary or domain-model doc, read it; an issue that calls something by the wrong noun reads as written by someone who doesn't know the codebase.
- Respect any architecture-decision doc relevant to the area you're touching (an ADR directory, a `docs/decisions/` folder, whatever the repo calls it) — don't draft a plan that silently contradicts one.
- Look for a prefactoring opportunity that would make the real change easier ("make the change easy, then make the easy change"). If one exists, it becomes the plan's first phase.

## Step 2 — Draft the phased plan

Structure the issue description as **phases**, each a complete, checkable unit of work — not a layer-by-layer breakdown (schema-only, then API-only, then UI-only), a **vertical** slice through whatever layers this specific change touches. A phase should be small enough to fit in one fresh context window and leave something genuinely verifiable when it's done.

For each phase, write:

- **A short, specific title.**
- **Files** — exact paths, marked `Create:` or `Modify:` (with a line range for `Modify:` where you know it). Never a vague "the relevant component."
- **Steps** — ordered, concrete actions. Where a step is code, show the actual code (real function names, real types, matching what Step 1 found) — never pseudocode, never "add appropriate validation," never "similar to Task N, repeat the pattern" (the executing agent may read phases out of order and won't have Task N in front of it). Number them or use checkboxes so progress is trackable.
- **A verification step** — the concrete command or check that proves this phase actually works (a specific test file/name to run, a typecheck, a lint pass, a manual repro to confirm) — not "test the change," the actual command.

**Never a commit step.** Every phase ends at verification. Whether and how to commit is left to whoever executes the plan — that's the consuming repo's own convention to apply, not this issue's job to re-decide.

**No placeholders, anywhere.** Never write "TBD," "implement later," "add appropriate error handling," "write tests for the above" without the actual test code, or reference a type/function this issue never defines. A step that describes what to do without showing how is not done — fill it in or cut it.

**Completion criteria must be checkable, not vibes.** "Understanding reached" or "properly handled" tells the executing agent nothing about when to stop; "the 3 acceptance criteria below all pass" does. Every phase and the issue as a whole needs a bound the agent can test itself against, not just narrate satisfaction with.

**State the positive, not the prohibition.** Prefer "use `useTransition` for pending state" over "don't use `useState(false)` for pending state" — a banned pattern named in the plan is a pattern now sitting in the executing agent's context, and negation is a weak filter against it. Reserve an explicit "never do X" for a real guardrail (a destructive action, a security boundary), and even then pair it with what to do instead.

## Step 3 — Self-review before publishing

Re-read the drafted plan once, fresh:

- **Coverage** — does every part of what the user asked for map to a phase? List any gap and fix it before moving on.
- **Placeholder scan** — re-check for the red flags from Step 2. Fix inline, don't just note them.
- **Consistency** — do names, types, and file paths agree across phases? A function called `resolveActiveOrg` in one phase and `getActiveOrganization` in another is a bug the executing agent will trip on.
- **No embedded commit step** — confirm one didn't slip in.

## Step 4 — Resolve the issue's fields

- **Team** — call `mcp__plugin_linear_linear__list_teams`. If there's exactly one team in the workspace, use it without asking. If there's more than one and the user didn't name one, ask which.
- **Priority** — `0=None, 1=Urgent, 2=High, 3=Medium, 4=Low`. Default to **3 (Medium)**. Only use a different value if the user explicitly named one (a word like "urgent," "low priority," "high priority" — map it to the matching number).
- **Project** — only set one if the user named it. Resolve the name via `mcp__plugin_linear_linear__list_projects` (search by name); if more than one project plausibly matches, ask which rather than guessing. If the user named nothing, leave the issue **with no project**.
- **Assignee** — only set one if the user named a person. Leave it **unassigned** otherwise. Never guess an assignee from conversation context alone (e.g. "I'm working on this" isn't the same as "assign it to me" — only act on an explicit ask).

## Step 5 — Confirm, then publish

Show the user the drafted title, the full phased plan, and the resolved team/priority/project/assignee before creating anything — this is a persistent, team-visible artifact, so a quick look before it's published beats a fix-up after. Adjust based on their feedback if they want changes.

Once confirmed, create the issue with `mcp__plugin_linear_linear__save_issue` (`team`, `title`, `description` = the full phased plan as Markdown, plus `priority`/`project`/`assignee` per Step 4 — omit `project`/`assignee` entirely when neither was set, never pass a guessed value). This call is mandatory — drafting the plan and stopping short of actually creating the issue does not satisfy this skill.

Report back the created issue's identifier and URL.
