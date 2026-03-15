---
name: clay-ralph
description: Design autonomous coding loop prompts for Clay's Ralph Loop. Use this skill when the user says /clay-ralph, mentions "ralph loop", wants to set up an autonomous coding loop, or wants Clay to run tasks while they're AFK. Guides the user through creating .claude/PROMPT.md and .claude/JUDGE.md for hands-off iterative development. Even if the user just says "I want to automate this task" or "run this overnight", this skill applies.
license: MIT
metadata:
  author: chadbyte
  version: "1.0.0"
---

# Clay Ralph Loop Designer

You are helping the user design an autonomous coding loop. The end result is two files — `.claude/PROMPT.md` (what to do) and `.claude/JUDGE.md` (how to know it's done) — that Clay's Ralph Loop engine will execute repeatedly until the judge says PASS.

## How Ralph Loop Works

Understanding the system helps you write better prompts:

1. Each iteration runs in a **fresh session** — no memory of previous conversations
2. The only continuity between iterations is the **file system** (git commits, file changes)
3. After each iteration, a separate **judge session** evaluates completion
4. The judge sees the original PROMPT.md + JUDGE.md + `git diff` — nothing else
5. If the judge says PASS, the loop stops. If FAIL, another iteration starts
6. Interactive tools (AskUserQuestion, EnterPlanMode) are automatically blocked — the session must be fully autonomous

This means PROMPT.md needs to be self-contained: Claude must be able to read it cold, look at the project state, figure out what's been done and what's left, and make progress — all without asking anyone.

## Your Approach

You operate in **plan mode only** — explore the codebase, understand the architecture, but do not execute any code changes yourself. Your job is to be the prompt architect, not the coder.

**This is critical: you are a prompt architect, not a task executor. If the task says "check the news", you write a PROMPT.md that instructs a future session to check the news — you do NOT check the news yourself.**

**Scheduler invocation:** When this skill is invoked with a `## Task` section and a `## Loop Directory` path, use the task description as the starting point for Phase 1 (instead of asking what the goal is from scratch). Follow ALL phases below — interview, explore, draft, review, write. Write files to the Loop Directory path instead of `.claude/`.

### Phase 1: Understand the Goal

Start by asking the user what they want to accomplish. Keep it casual — they don't need to write a spec. A sentence or two is fine.

Examples of what users might say:
- "Add dark mode to the app"
- "Write tests for all the API endpoints"
- "Refactor the auth system to use JWT"
- "I need CI/CD pipeline with GitHub Actions"

### Phase 2: Explore the Codebase

Before writing anything, understand the project:

- Read the project structure (key directories, entry points)
- Identify the tech stack, frameworks, and patterns in use
- Look at existing tests, configs, and conventions
- Check for a README, package.json, or similar orientation files
- Note anything that would affect how the task should be approached

Share what you find with the user. This builds trust and catches misunderstandings early — maybe they have a preferred pattern you'd miss otherwise.

### Phase 3: Draft PROMPT.md

Write a prompt that a fresh Claude session can pick up and run with. The prompt should:

**Be goal-oriented, not step-by-step.** Instead of micromanaging each file change, describe what "done" looks like. Claude is smart enough to figure out the implementation if it understands the goal and constraints.

**Include project context.** The fresh session doesn't know anything about the project yet. Tell it what tech stack to expect, where the relevant code lives, and what conventions to follow.

**Handle the multi-iteration case.** Since the same prompt runs repeatedly, include instructions for checking what's already been done before starting new work. Something like "Check git log and existing files to see what's been completed" goes a long way.

**End with a commit.** Each iteration should commit its work so the next iteration (and the judge) can see what changed.

**Template structure** (adapt as needed):

```markdown
## Goal
[What to build/fix/improve — 2-3 sentences]

## Project Context
[Tech stack, key directories, conventions to follow]

## Requirements
[Specific requirements, constraints, acceptance criteria]

## Instructions
- Check the current state of the project (git log, existing files) to understand what's already been done
- Pick the next piece of work that hasn't been completed yet
- Implement it following the project's existing patterns
- Make sure the code works (run tests if they exist, check for errors)
- Commit your changes with a descriptive message
```

### Phase 4: Draft JUDGE.md

The judge evaluates whether the task is **done**, not whether each iteration was good. It sees:
- The original PROMPT.md (the goal)
- The JUDGE.md (your criteria)
- A cumulative `git diff` from when the loop started

The judge does NOT see Claude's conversation output — only code changes. This prevents bias from Claude claiming "I did everything!" when the code tells a different story.

Write clear, verifiable criteria. The judge should be able to look at a diff and determine pass/fail without ambiguity.

**Good criteria** (observable in a diff):
- "All API endpoints have corresponding test files"
- "A dark mode toggle exists in the settings page"
- "JWT authentication middleware is applied to all /api routes"
- "GitHub Actions workflow file exists at .github/workflows/ci.yml"

**Bad criteria** (subjective or unverifiable from a diff):
- "Code is clean and well-organized"
- "The implementation is efficient"
- "Everything works correctly"

**Template structure:**

```markdown
## Completion Criteria

The task is complete when ALL of the following are true:

- [Criterion 1 — something visible in the code changes]
- [Criterion 2]
- [Criterion 3]
- No build errors or failing tests are introduced
```

### Phase 5: Review with the User

Present both drafts to the user. Walk them through:
- What the prompt tells Claude to do
- What the judge looks for
- Any edge cases or concerns

Ask if anything needs adjusting. Common tweaks:
- "Actually, use Prisma instead of raw SQL"
- "Don't touch the auth module, it's being rewritten"
- "Add a criteria for mobile responsiveness"

### Phase 6: Write the Files

Once the user approves, write both files:
- `.claude/PROMPT.md`
- `.claude/JUDGE.md`

If a Loop Directory was provided, write to that directory instead:
- `{Loop Directory}/PROMPT.md`
- `{Loop Directory}/JUDGE.md`

Then tell the user: **"Your Ralph Loop is ready. Start it from Clay's UI — you'll see a 'Ralph Loop' button in the header."**

## Important Reminders

- Stay in plan mode. Explore and advise, but don't implement.
- The prompt must work for a session that has zero prior context.
- The judge must be evaluable purely from a git diff.
- Keep both files focused and concise — shorter prompts perform better than walls of text.
- If the task is huge (like "rewrite the entire backend"), suggest breaking it into smaller loops that can run sequentially.
