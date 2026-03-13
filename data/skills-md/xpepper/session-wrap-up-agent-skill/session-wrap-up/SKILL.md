---
name: session-wrap-up
description: >
  Run at the end of a coding session, before handoff, or any time the user wants to capture what
  was learned. Review the conversation and recent git changes, identify corrections, decisions, new
  workflows, follow-up tasks, automation opportunities, and non-obvious gotchas, then update the
  right project docs and agent instruction files (AGENTS.md, CLAUDE.md, Copilot instructions,
  Cursor rules, or the project's equivalent) and persist durable lessons for future sessions.

  Use this skill whenever the user wants to wrap up, hand off work, save what was learned, update
  docs or agent instructions based on the session, capture lessons, record gotchas, preserve
  decisions, note next steps, ask what should be committed, or document recurring mistakes to avoid
  next time, even if they do not explicitly say "session wrap-up."
---

# Session Wrap-Up

Help close out a coding session by reviewing what changed, updating project docs and agent
instructions, preserving durable lessons, and surfacing any useful follow-up tasks.

## Outcomes

Aim to leave the project in a state where:

1. Project docs reflect anything humans now need to know.
2. Agent instructions capture anything that should change future agent behavior.
3. Durable lessons and next-step context are preserved without forcing the user to restate them.

## Operating Stance

- Start from evidence, not from memory. Use the conversation, git state, and the files themselves.
- Prioritize durable guidance over narration. Capture rules, gotchas, and decisions that will
  change future behavior.
- Scale the depth of the wrap-up to the size of the session. Do not run a heavy process for
  trivial, read-only, or one-off interactions unless the user explicitly wants it.
- If the user already named what matters, treat that as the starting point and fill in gaps
  yourself.
- Avoid duplicating the same lesson across multiple files unless duplication is genuinely useful.

## Step 1: Decide The Depth

Choose the lightest workflow that still preserves the right information.

Use the full workflow when:

- Significant code or docs changed
- The user asked for handoff or next-session context
- The session surfaced corrections, gotchas, or workflow changes
- There are unfinished tasks worth preserving

Use a lighter wrap-up when:

- The session was mostly exploration or quick Q&A
- No durable project knowledge changed
- The user only wants a short summary or commit guidance

If nothing meaningful changed, say so plainly instead of manufacturing updates.

## Step 2: Review The Session First

Before asking the user anything, build a picture of what happened this session from the
conversation itself.

Look for:

- Explicit things the user asked to capture
- Moments where the user corrected, redirected, or constrained the agent
- Decisions that changed the right future workflow
- Repeated confusion that a short instruction could have prevented
- Unfinished work or follow-up tasks worth carrying forward
- Repetitive manual work that suggests future automation

These are usually higher value than generic summaries of what changed in git.

## Step 3: Gather Repo Context

Now build a picture of what changed in the repository.

Run these to understand recent changes:

```bash
git log --oneline -20          # recent commits — focus on this session's work
git status --short             # any uncommitted changes
git diff --stat HEAD~5..HEAD   # which files changed across recent commits
```

If the repo is very new, shallow, or `HEAD~5` is unavailable, fall back to whatever history is
available instead of failing the wrap-up.

Use git to answer:

- Which files changed in ways that affect future contributors or agents?
- Were new commands, scripts, conventions, or workflows introduced?
- Is there anything the user did not mention that looks worth documenting?

## Step 4: Identify The Update Targets

Different projects use different conventions. Scan for whichever exist:

- `AGENTS.md` (Codex/OpenAI convention)
- `CLAUDE.md` (Claude Code convention)
- `.github/copilot-instructions.md` (GitHub Copilot)
- `.github/copilot-instructions-*.md` (scoped Copilot instructions)
- `.github/agents/*.md` (GitHub Copilot custom agents)
- `.cursorrules` or `cursor.rules` (Cursor)
- Existing handoff, notes, or context files already used by the repo
- Any file explicitly mentioned in the user's message

Read the ones that exist so you understand their current content and style before proposing
additions.

## Step 5: Build Candidate Captures

Review both the git changes and your conversation notes with this lens: look for things that would
meaningfully change how a future session approaches the project.

Prioritize candidates in this order:

1. Explicit user requests about what to preserve
2. Corrections or redirects that exposed a missing instruction
3. New workflows, commands, or conventions introduced during the session
4. Repo changes that affect setup, APIs, or team expectations
5. Recurring issues the user mentions from earlier sessions
6. Follow-up tasks or automation ideas that would reduce repeated friction

**Worth capturing in agent instructions:**

- New required steps in a workflow
- Gotchas or non-obvious constraints discovered
- New commands, tasks, or scripts added to the project
- Conventions established during the session
- Things that caused mistakes or confusion that instructions could prevent

**Worth capturing in project docs:**

- New public APIs or changed interfaces
- New setup steps or dependencies
- Changed deployment or build processes
- Human-facing workflow expectations

**Worth capturing as follow-up or automation suggestions:**

- Next-session priorities that are not obvious from git alone
- Repeated manual steps that could become a script, command, or skill
- Cleanup tasks intentionally deferred during the session

**Not worth capturing:**

- Implementation details that are obvious from reading the code
- One-off debugging steps specific to a single incident
- Things already documented accurately
- Speculation about future problems that did not actually surface

## Step 6: Optionally Fan Out Analysis

If the environment supports subagents and the session is large enough to justify the overhead, fan
out the analysis into a few independent read-only tracks before editing anything. Keep this
optional; skip it for small sessions.

Good parallel tracks:

- Doc/instruction updater: identify concrete doc or instruction deltas
- Lesson extractor: isolate durable gotchas, mistakes, and discoveries
- Follow-up suggester: identify unfinished work and next-session priorities
- Automation scout: identify repeated manual patterns that suggest automation

Keep each track narrow and structured. Do not let multiple agents edit files in parallel. After
they return, integrate the results centrally.

See `references/analysis-patterns.md` for a compact decision rule and role templates.

## Step 7: Validate Before Editing

Before touching files, validate every proposed capture against what already exists.

For each candidate:

1. Check whether it is already documented accurately.
2. If it partially overlaps an existing instruction, merge into the existing section instead of
   adding a duplicate note.
3. If it is new and actionable, keep it.
4. If it is vague, obvious, or redundant, drop it.

This validation step is mandatory even when you did not use parallel analysis.

## Step 8: Ask The User

Present a brief summary combining what you found from git and from the conversation review:

> "Here's what I think is worth capturing from this session: [bullet list]. Is there anything else
> you want to capture, or anything from this list you'd rather skip?"

Also ask whether there are any recurring issues or mistakes from past sessions worth capturing
while you are already updating the guidance.

If the environment supports structured user input, you may offer a short action selection such as:

- Update docs/instructions
- Record lessons learned
- Note follow-up tasks
- Capture automation ideas
- Skip

If structured input is unavailable, ask the same question in plain text and keep it concise.

If the user already gave a clear capture list, present your additions as a short supplement instead
of asking them to re-approve everything from scratch.

## Step 9: Make The Updates

For each thing to capture, decide where it goes.

### Agent instruction files

Add concise entries to the appropriate file. Match the existing style and tone. Prefer adding to
existing relevant sections over creating new ones.

Write for a future agent instance that has no memory of this session. Make entries actionable:

- Good: "Run `npm run lint` before every commit; CI fails otherwise."
- Bad: "We figured out that linting matters."

### Project documentation

Update READMEs or other docs only if something genuinely changed that users or developers need to
know. Do not add documentation for things that were already documented correctly.

### Lessons log

If a lesson is specific to this project but not a fit for the main instruction files, save it to:

```text
docs/agent/memories/lessons-learned.md
```

Create the directory and file if they do not exist. Use a simple dated log format:

```markdown
## YYYY-MM-DD

- [Lesson 1]
- [Lesson 2]
```

Append to the file; do not overwrite previous entries.

### Follow-up and handoff notes

If the session leaves behind non-obvious next steps, include them in the user-facing summary and
add them to an existing handoff or notes file if the project already uses one. Do not create a new
generic backlog file unless the user asks for it.

### Automation suggestions

If the wrap-up reveals repeated manual work, capture the automation idea in the user-facing summary
or in the project's existing notes. Do not build the automation by default; treat it as a
suggestion unless the user explicitly asks for implementation.

## Step 10: Report What You Did

Give the user a short summary of what was updated:

- Which files were modified and what was added
- Which follow-up items or automation ideas were surfaced
- Anything you decided to skip and why

Keep it brief. One or two sentences per file is enough.

## Principles

**Be selective.** A bloated `AGENTS.md` or `CLAUDE.md` that documents everything is worse than a
focused one that documents the things that actually prevent mistakes.

**Match the project's voice.** If the existing instructions are terse and technical, be terse and
technical. If they are friendly and explanatory, match that.

**Prefer edits over rewrites.** Add to the right existing section when possible instead of
restructuring the whole file.

**Capture the lesson, not the drama.** Convert frustration, backtracking, or correction moments
into calm, actionable guidance for the next session.

**Validate before duplicating.** Never add a new note until you have checked whether the repo
already says the same thing.

**Use parallelism only when it helps.** Optional fan-out is for larger sessions with clearly
independent analysis tracks. If it adds complexity without better output, skip it.
