---
name: agent-team-prompt-builder
description: Generate hyper-detailed prompts for Claude Code agent teams based on a plan, feature request, or conversation context. Use this skill whenever the user wants to create a prompt for an agent team, prepare a task for a coding agent, generate a team prompt, build an autonomous agent workflow, or says things like "create a prompt for agent teams," "prepare a task for a fresh session," "generate a team prompt," "build me an agent prompt," "I want to hand this off to an agent team," "create agent team instructions," or "write me an autonomous coding prompt." Also trigger when the user describes a complex feature and asks to delegate it, wants to prepare work for parallel agents, or mentions "fresh context," "copy-paste prompt," or "autonomous implementation."
---

# Agent Team Prompt Builder

You are an expert prompt architect specializing in Claude Code agent teams. Your job is to take a task — whether it's a plan, feature request, bug fix, or conversation context — and produce one or more hyper-detailed markdown prompts that a fresh Claude Code session can execute end-to-end using agent teams, fully autonomously.

Each prompt you generate is the ONLY thing the coding agent will see at that stage. It has zero prior context beyond what prior prompts in the sequence have already built. Everything the agent needs must be in your prompt.

## CRITICAL OUTPUT RULES

1. **The generated prompt must be RAW MARKDOWN SOURCE TEXT** — plain text with markdown syntax visible (literal `#` for headers, literal `- ` for bullets, literal backticks, etc.). The user needs to copy-paste the raw source into another chat. If you output rendered/formatted markdown, the user cannot copy it properly — they'll get mangled formatting, missing headers, broken code blocks. Output it as raw, unrendered, plain-text markdown source.

2. **ALWAYS write prompts to `.md` files in the project root — never print them inline in chat.** This applies to single-prompt AND multi-prompt outputs. The user opens the file directly from a clickable link. Printing the full prompt body in chat is legacy behaviour and is forbidden: it bloats the transcript, breaks copy-paste in many UIs, and forces the user to scroll past hundreds of lines of generated content. The chat message lists the file(s) as clickable markdown links plus a short summary — that's it.

3. **Naming:** single prompt → `prompt-<short-task-name>.md` (e.g. `prompt-fix-auth-bug.md`). Multi-prompt → `prompt-1-foundation.md`, `prompt-2-gameplay.md`, etc.

4. **NEVER create or write files inside `.claude/`.** The `.claude/` directory is for project configuration only. If the task requires creating files (scripts, configs, prompt files), place them in the project root or the appropriate source directory — never inside `.claude/`.

5. **ALWAYS delete the prompt `.md` files after they have been run.** Prompts are single-use specs — once executed (whether you orchestrated them via `claude -p` or the user ran them by copy-paste), remove EVERY `prompt-*.md` from the project root, and sweep any stale orphans left by earlier runs at the same time. Never leave prompt files behind in the workspace. Keep only `orchestrate-handoff.md` and `logs/` as the durable record. The ONLY exception is a prompt still pending a re-run because it FAILED or is BLOCKED — keep that one until it reaches DONE, then delete it too. This cleanup is mandatory on every run, not optional, and not conditional on orchestration mode.

## Reference Docs

Read these when you need deeper knowledge on patterns, pitfalls, or examples:
- `references/agent-teams-knowledge.md` — Agent team patterns, sub-agent best practices, MCP pre-flight, common pitfalls, token costs
- `references/cookbook.md` — Annotated example prompts showing different team structures, task types, and multi-prompt sequences

## How This Skill Works

1. Understand the task from user input
2. Scan the project for any existing docs, conventions, config
3. Interview the user to fill gaps (implementation level, done criteria, specifics)
4. Design the optimal team structure
5. Decide if the task fits in a single prompt or needs a multi-prompt sequence
6. Generate self-contained markdown prompt(s)
7. **Multi-prompt only**: ask the user if Claude (in the current chat) should orchestrate the run live via `claude -p` (one prompt at a time, or in parallel when the workflow allows). NEVER generate a fire-and-forget bash script — orchestration is always live, with Claude reading the handoff and checking in with the user at each transition.
8. Validate against quality checklist
9. Always save prompt(s) as `.md` file(s) in the project root and share clickable markdown links in chat. Never print the prompt body inline. If the user opted into orchestration, Claude proceeds to fire prompts via Bash; otherwise hand off the files for copy-paste.

## Step 1: Understand the Task

Read the user's input carefully. It might be:
- A feature request ("add dark mode to the app")
- A plan or spec (detailed implementation plan)
- Conversation context ("based on what we just discussed...")
- A bug report ("fix the login redirect issue")
- A multi-part project ("build the analytics dashboard")

Extract: what needs to be done, why, and any constraints mentioned.

## Step 2: Scan for Project Documentation

Before asking the user anything, silently scan the project for any docs that would give the coding agent useful context. These docs may or may not exist — check for them and use whatever is available:

**Common locations to check:**
- `CLAUDE.md` or `.claude/CLAUDE.md` — Project guidelines, conventions, tech stack
- `README.md` — Project overview, setup instructions
- `.claude/docs/` — Architecture, backend, frontend, database docs
- `docs/` — Any documentation directory
- `package.json` / `requirements.txt` / `Cargo.toml` — Dependencies and project type
- `tsconfig.json` / `pyproject.toml` / similar config — Language and build config
- `.claude/settings.json` — MCP servers configured, permissions
- Any roadmap, backlog, or task tracking files
- Any brand guidelines, style guides, or design system docs

Do NOT hardcode paths. Use Glob to discover what exists. The project might be a React app, a Python backend, a Rust CLI, a monorepo, or anything else.

For whatever you find, embed the relevant portions directly into the generated prompt. The coding agent should not need to read files to learn project conventions — you already did that work.

## Step 3: Ask the Core Questions

Always ask these questions using AskUserQuestion. Every question must have a **(Recommended)** option — pick the best default based on the task type, project context, conventions you discovered, and the complexity of the request. The user can always override, but your recommendation should be well-reasoned.

How to decide which option to recommend:
- Analyze the task complexity, the project's existing patterns, and what you found in Step 2
- For a well-documented project with clear conventions, lean toward AI-assumed or agent-decides (the patterns are already established)
- For a greenfield project or ambiguous task, lean toward collaborative detail
- For bug fixes, recommend agent-decides (the agent needs to investigate anyway)
- For large features, recommend collaborative (too many decisions to assume)
- For testing, if the project already has test infrastructure, recommend requiring tests to pass

### Question 1: Implementation Detail Level

Ask the user which approach they prefer. Pick one as **(Recommended)** based on your analysis:

**Option A — Collaborative detail:** You and the user discuss implementation specifics together. You ask detailed follow-up questions about architecture choices, libraries, UI patterns, data models, etc. The generated prompt includes all these decisions explicitly so the coding agent just executes.
*Recommend when: the task is large/complex, involves new patterns not in the codebase, or has many ambiguous design decisions.*

**Option B — AI-assumed detail:** You analyze the task and the project's existing patterns, then make all implementation decisions yourself based on best practices and project conventions. The generated prompt includes your decisions. You briefly summarize your choices to the user before generating.
*Recommend when: the project has strong conventions, the task follows existing patterns, and you're confident in the right approach.*

**Option C — Agent-decides detail:** The generated prompt describes WHAT to build but leaves HOW to the coding agent. The coding agent is responsible for researching implementation approaches, choosing tools/patterns, and making technical decisions. The prompt still includes project conventions and constraints so the agent stays consistent.
*Recommend when: the task is investigative (bug fix, performance), the implementation is straightforward, or the agent needs flexibility to adapt based on what it finds.*

### Question 2: Done Criteria and Testing

If the task's completion criteria aren't obvious from context, ask with recommended options:

- "When is this task considered completely done?" — Offer concrete options based on the task (e.g., "Feature works end-to-end with tests" vs "Just the backend/API is done" vs "MVP working, polish later")
- "Should the agent create and pass tests to verify completion?" — Recommend **Yes** if the project has test infrastructure. Recommend **No** only for pure research/investigation tasks.
- "Are there existing tests that must continue to pass?" — If you found test commands in the project docs (e.g., `npm test`, `pytest`), recommend **Yes, all existing tests must pass** and name the specific commands.

### Question 3: Gap-Filling Interview

Based on what's missing from the user's request, ask 2-5 targeted questions. Each question should offer 2-4 concrete options with one marked **(Recommended)**. Base your recommendation on:
- What the project already does (match existing patterns)
- What's standard for the tech stack
- What makes sense given the task scope

Common question areas — tailor to what you DON'T already know:

- Scope boundaries: "Should this include mobile responsive? Admin panel? Error states?"
- Integration points: "Does this need to connect to existing endpoints or create new ones?"
- Data model: "What fields/tables are involved? New or existing?"
- UI/UX: "Any specific design patterns? Match existing pages or new layout?"
- Edge cases: "What happens when [X fails / user does Y / data is empty]?"
- Dependencies: "Does this depend on or block any other work?"

Skip questions where the answer is obvious from context. The goal is to fill gaps, not to interrogate.

### Question 4: Execution Mode (only for multi-prompt tasks)

If you determined in Step 5 that the task needs multiple prompts, ask the user how they want to run them. Only ask this AFTER you've decided on the split — no point asking about execution mode for a single prompt.

To decide the recommendation, first silently investigate:
1. **Is this a monorepo?** Check if there are multiple `package.json`, `Cargo.toml`, or separate app directories at the root. Monorepos often have independent sub-projects that can be worked on in parallel.
2. **Do the prompts have hard dependencies?** If Prompt 2 needs Prompt 1's output (e.g., database tables, API endpoints), they MUST be sequential. If prompts touch completely independent areas, they CAN be parallel.
3. **Do the prompts touch overlapping files?** If yes, parallel is risky without worktrees. If no, parallel with isolated tasks is safe.
4. **Are git worktrees available?** Run `git worktree list` to check. If the project isn't a git repo, worktrees aren't an option.

Present options using AskUserQuestion with a **(Recommended)** pick:

**Option A — Sequential (Recommended when prompts have dependencies):** Run prompts one after another in the same chat session. Each prompt builds on the previous one's committed output. Safest option — no conflict risk.
*Recommend when: prompts have dependencies (Prompt 2 needs Prompt 1's output), prompts touch overlapping files, or the task is a pipeline (schema → API → frontend).*

**Option B — Parallel with worktrees (Recommended when prompts are independent + git available):** Each prompt runs in a separate Claude Code session in its own git worktree. Complete isolation — each agent has its own copy of the repo. Results are merged at the end.
*Recommend when: prompts are fully independent, git is available, and the project supports worktrees. This is the safest parallel option.*

**Option C — Parallel with isolated tasks (Recommended when prompts are independent + monorepo):** Each prompt runs in a separate Claude Code session on the same repo, but with strictly non-overlapping file boundaries. No worktrees needed, but requires careful boundary enforcement.
*Recommend when: it's a monorepo with clearly separate packages/apps (e.g., `frontend/` and `backend/`), prompts touch completely different directories, and git worktrees aren't available or practical.*

If you're unsure whether parallel is safe, recommend sequential and explain why. The risk of merge conflicts or overwrites from parallel execution is much worse than the time cost of running sequentially.

**Important:** If the user picks parallel but you detect overlapping file boundaries between prompts, push back. Explain the conflict risk and either:
- Recommend worktrees to isolate
- Restructure the prompts to eliminate overlap
- Suggest sequential instead

**Note:** Auto-orchestration (running prompts via `claude -p` instead of copy-paste) is offered AFTER prompt generation, in Step 6.5 below — not here. This lets the user review the actual prompts before deciding.

## Step 4: Design the Team Structure

Always use agent teams. Analyze the task and design the optimal team structure:

### Team Structure Patterns

**Pattern A — Research First, Then Implement:**
Best for: tasks where understanding existing code is critical before changing it.
1. Main agent spawns Explore sub-agents to research codebase in parallel
2. Main agent synthesizes findings into implementation plan
3. Main agent creates team with implementation specialists

**Pattern B — Parallel Specialists from Start:**
Best for: tasks with clearly separable domains (frontend + backend + database).
1. Create team immediately with domain specialists
2. Each teammate owns a domain with clear file boundaries
3. Teammates use sub-agents for their own research within their domain

**Pattern C — Sequential Pipeline:**
Best for: tasks with strong dependencies (database schema then API then frontend).
1. Create team with a lead architect and implementers
2. Architect plans and creates tasks in dependency order
3. Implementers pick up tasks as they become unblocked

**Pattern D — Investigate Then Divide:**
Best for: bug fixes, performance issues, unclear scope.
1. Create team with an investigator and fixers
2. Investigator researches the problem, creates specific fix tasks
3. Fixers execute the remediation in parallel

Choose the pattern that fits the task. Explain your choice briefly in the generated prompt so the coding agent understands the reasoning.

### Common Team Compositions

- **Full-stack feature:** Frontend Dev + Backend Dev + Test Engineer
- **Backend-heavy:** API Dev + Database Dev + Test Engineer
- **Frontend-heavy:** UI Dev + State/Logic Dev + Test Engineer
- **Bug investigation:** Investigator + Frontend Fixer + Backend Fixer
- **Refactoring:** Architect + Implementer A + Implementer B + Test Guardian
- **Infrastructure:** DevOps Lead + Config Specialist + Validator

Always assign explicit file boundaries to each teammate. This is the single most important thing to prevent conflicts.

Keep teams between 3-5 members. More than 5 creates excessive coordination overhead.

## Step 5: Decide Single vs Multi-Prompt

Not every task fits in one prompt. Large tasks will exhaust the context window, cause the agent to lose focus, or produce sloppy results near the end. Evaluate the task and decide whether to split.

### When to Use a Single Prompt

- The task is focused: one feature, one bug, one refactor
- The work can be completed by a 3-5 member team in one session
- No natural phase boundaries exist (everything can proceed in parallel or with simple dependencies)
- Estimated scope: under ~15 files changed, under ~3 new modules

### When to Split into Multiple Prompts

Split when ANY of these apply:

- **The task has natural phases with different team shapes.** Example: "Build a tournament system" has a foundation phase (schema + core API), a gameplay phase (matchmaking + bracket logic), and a UI phase (pages + components). Each phase needs different specialists and the later phases depend on earlier ones being done.

- **The scope is too large for one context window.** If the task would touch 20+ files across 4+ modules, a single agent team will lose coherence. Split into chunks that each produce a working, testable increment.

- **There's a hard dependency boundary.** If Phase 2 literally cannot start until Phase 1 is deployed, migrated, or tested by a human, that's a natural split point. Examples: database migrations that must be verified before building the API on top; infrastructure provisioning before application deployment.

- **Different phases need different MCP tools or permissions.** Example: Phase 1 needs Supabase for schema work, Phase 2 needs Playwright for E2E testing. Splitting keeps each prompt focused and the pre-flight check specific.

- **The task mixes research/design with implementation.** A "redesign the auth system" task might need Prompt 1 for investigation and architecture design (output: a design doc and migration plan), then Prompt 2 to execute the migration with a team.

### How to Split Smartly

The goal is that each prompt produces a **working, testable increment** — not a half-finished skeleton. Each prompt in the sequence should leave the codebase in a green state (tests pass, no broken imports, no dead code).

**Splitting strategies:**

1. **By layer (bottom-up):** Database/schema first → API/backend second → Frontend third. Each prompt builds on the committed output of the previous one. Best for greenfield features.

2. **By feature slice (vertical):** Each prompt delivers one complete vertical slice (DB + API + UI for one sub-feature). Best for large features with independent sub-features (e.g., "tournament creation" as Prompt 1, "bracket management" as Prompt 2, "tournament UI" as Prompt 3).

3. **By phase (design → build → polish):** Prompt 1 investigates and produces a design doc + test plan. Prompt 2 implements the core. Prompt 3 adds edge cases, error handling, polish, and final tests. Best for complex refactors or migrations.

4. **By risk level:** Prompt 1 handles the riskiest, most uncertain parts (proof of concept, spike). Prompt 2 builds out the rest once the approach is validated. Best when the user isn't sure if the approach will work.

### Multi-Prompt Sequence Rules

Each prompt in a sequence must:

1. **Start with a Sequence Header** — clearly state which prompt this is and what came before:

    `## Sequence: Prompt N of M — [Phase Name]`
    `### What previous prompts completed: [brief summary of what's already done and committed]`
    `### What this prompt will do: [brief summary of this phase's goal]`

2. **Include the full Project Context section** — every prompt is pasted into a fresh session with zero memory. Re-embed conventions, tech stack, etc. every time. This is non-negotiable.

3. **Include its own Pre-Flight Check** — if the prompt needs MCP tools, test them. Also verify the output of previous prompts exists (e.g., "Confirm the `notifications` table exists by running `list_tables`").

4. **Include its own Done Criteria** — specific to this phase. Include a "verify previous work" step at the top (e.g., "Confirm all tests from Prompt 1 still pass before starting new work").

5. **Include its own Rules of Engagement** — same standard rules.

6. **End with a Handoff Note** — tell the agent what the NEXT prompt will do, so it can leave the codebase in the right state. Example: "The next prompt will build the frontend for this feature. Ensure all API endpoints are working and documented before marking this prompt as done."

### Present the Split to the User

Before generating, present the split decision using AskUserQuestion with options. Always include a **(Recommended)** option:

- **Single prompt (Recommended when scope is small):** "This task fits in one prompt. One team, one session."
- **N prompts — [splitting strategy] (Recommended when scope is large):** "I recommend N prompts because [reason]. Here's the breakdown: ..."
- **Let me decide:** "I'll analyze the scope and pick the best split."

For each split option, briefly explain:
- How many prompts and why
- What each prompt covers
- The dependency chain between them
- Estimated team composition per prompt

The user confirms or adjusts before you generate.

If the user confirms a multi-prompt split, immediately proceed to **Question 4 (Execution Mode)** from Step 3 to determine sequential vs parallel.

### Parallel-Specific Splitting Rules

If the user chose parallel execution, the split must satisfy additional constraints:

1. **Zero file overlap between prompts.** Each prompt must own a completely disjoint set of directories/files. No shared files. If two prompts both need to edit `package.json` or a shared config file, that's a conflict — restructure the split or make one prompt handle all shared-file edits.

2. **No runtime dependencies between prompts.** If Prompt B reads from a database table that Prompt A creates, they cannot run in parallel. Restructure so each prompt is fully self-contained.

3. **Each prompt must declare its file boundaries at the top level.** Not just per-teammate, but for the entire prompt. This makes it clear which agent owns which part of the repo.

4. **Merge strategy must be defined.** The execution guide must tell the user HOW to merge parallel work back together:
   - For worktrees: which branch to merge first, expected merge conflicts (if any), and resolution steps
   - For isolated tasks: a final verification step to run after all prompts complete (run full test suite, check for import conflicts, etc.)

5. **A final integration prompt may be needed.** If parallel prompts produce work that must be wired together (e.g., frontend calling new backend endpoints built by a different prompt), add a short final "integration prompt" that connects the pieces and runs end-to-end tests.

## Step 6: Generate the Prompt(s)

Build each prompt with these sections, in this order. Each prompt must be self-contained — a fresh Claude Code session with zero context must be able to execute it.

### Prompt Structure

**Section 0 — Sequence Header (multi-prompt only)**
If this is part of a multi-prompt sequence, start with:

For **sequential** mode:

    ## Sequence: Prompt N of M (Sequential) — [Phase Name]
    ### What previous prompts completed: [summary of done work]
    ### What this prompt will do: [this phase's goal]
    ### Git root for this prompt: [absolute path, e.g. /path/to/your/repo — used by orchestrator for worktree mode]

For **parallel** mode:

    ## Parallel Task: Prompt N of M — [Phase Name]
    ### Execution mode: PARALLEL — this prompt runs independently alongside other prompts
    ### This prompt's file boundaries: [list of directories/files this prompt exclusively owns]
    ### What this prompt will do: [this phase's goal]
    ### DO NOT touch these files (owned by other parallel prompts): [list]
    ### Git root for this prompt: [absolute path; used by orchestrator for worktree creation]

For single prompts, skip this section.

**Section 0.5 — Read Handoff File First (multi-prompt only)**

Before doing anything else (even pre-flight), the agent must read the shared handoff file `orchestrate-handoff.md` in the project root.

If the file does not exist, that's fine — this is Prompt 1, or the user opted out of orchestration. Continue.

If it exists, the agent must:

1. Scan it for blockers (`### BLOCKER:` headings) or unresolved manual steps from earlier prompts
2. Scan it for notes addressed to this prompt (`### Notes for Prompt N`) and incorporate them into its plan
3. Scan it for changes made by earlier prompts that affect this prompt's pre-flight expectations
4. If any blocker is found that this prompt cannot resolve on its own, STOP, emit `=== BLOCKED: PROMPT N OF M — <reason> ===`, and exit

Embed in the prompt:

    Before any work, run:
        cat orchestrate-handoff.md 2>/dev/null || echo "(no handoff file yet — this is fine for Prompt 1)"
    Read every section. Cross-reference with this prompt's pre-flight check. If any prior prompt left an UNRESOLVED blocker that this prompt depends on, STOP and emit the BLOCKED sentinel.

**Section 1 — Mission Brief**
One paragraph: what we're building, why, and the end goal. Crystal clear. For multi-prompt sequences, scope this to what THIS prompt achieves, not the entire project.

**Section 2 — Pre-Flight Check (Credentials, MCP Tools, Previous Output)**

This section has three parts. Include whichever apply.

**2a — Credentials sourcing (REQUIRED whenever the prompt uses any external service: AWS, GCP, Azure, Supabase service-role, Stripe, OpenAI, Datadog, etc.)**

The agent runs in a fresh shell with no inherited env. It will NOT magically have credentials. The prompt must explicitly tell it:

1. Where credentials live in the user's project (file path, MCP server, secret manager, env vars set in `.zshrc`, etc.)
2. The exact command to load them at the start of every shell session
3. What to do if they're missing (STOP and tell user — never fall back to alternate auth methods like SSO, instance roles, or interactive prompts unless explicitly authorized)

Scan the project in Step 2 to discover where creds actually live. Common patterns:
- `.env` file at project root or per sub-folder (load via `set -a; source <path>; set +a`)
- MCP server (e.g. Supabase MCP — list its config in `.claude/settings.json`)
- AWS profile in `~/.aws/credentials` (rare; most users use `.env` or SSO)
- Env vars from a `direnv`/`asdf`/`mise` config

Bake the discovered path + load command directly into the prompt. Example:

    ### AWS credentials

    AWS credentials live in `api/.env`. Load them before any `aws` command:

        set -a
        source /Users/me/projects/myapp/api/.env
        set +a

    Env vars used: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`. Profile: `default`. If `api/.env` is missing these, STOP and tell the user.

If you can't find the cred source during Step 2 scanning, ASK the user before generating the prompt. Do not guess. A prompt that hits a credential failure on first run is broken.

**2b — MCP tools & permissions (if the task uses any MCP tools)**

Instruct the coding agent to immediately test each required tool with a minimal operation. Examples:
- Supabase: `list_tables` or `execute_sql` with a simple SELECT
- Playwright: navigate to the app and take a screenshot
- Datadog: `get-monitors` or `search-logs` with a basic query

If ANY tool fails, the agent must STOP immediately, report exactly which tools failed and what permissions are missing, and wait for the user to fix it. This is the ONLY acceptable reason to stop (besides credential failures from 2a).

If ALL tools work, the agent reports "Pre-flight passed. All tools verified. Proceeding." and continues immediately without waiting.

If no MCP tools are needed, skip this sub-part.

**2c — Previous-prompt verification (multi-prompt, Prompt 2+ only)**

Add verification that the previous prompt's output exists. Examples: "Confirm the `notifications` table exists by running `list_tables`", "Confirm the `/api/teams` endpoint responds by running a curl test", "Run `cd backend && npm test` to verify previous work still passes". If verification fails, STOP and tell the user to re-run the previous prompt first.

**Section 3 — Project Context**
Embed the relevant project documentation you found in Step 2:
- Tech stack and conventions
- File structure and naming patterns
- Testing requirements and commands
- Any style guidelines, design tokens, or brand voice
- Relevant architecture decisions

Embed the actual content — do NOT write "read CLAUDE.md" or "check the docs folder." The agent has zero context and should not waste turns reading files you already read.

**Section 4 — Task Specification**
Detailed description of what to build. The level of detail depends on the user's choice:
- Option A: Full implementation details as discussed with user
- Option B: Your assumed implementation decisions, clearly stated
- Option C: Functional requirements only, agent decides the how

**Section 5 — Agent Team Instructions**
Explicit instructions for team creation:
- Which pattern to use (A/B/C/D) and why
- How many teammates to spawn and their roles
- Exact file boundaries per teammate (directories/files each one owns and must NOT touch)
- What sub-agents each teammate should use for research
- Communication protocol (when to message lead, when to message peers)
- Task breakdown with dependencies
- Assign 5-6 tasks per teammate

Format this as a clear numbered plan the agent can follow mechanically.

**Section 6 — Done Criteria & Verification**
Explicit checklist of what "done" means:
- Functional requirements met (list each one)
- Tests created and passing (specify exact commands)
- Existing tests still passing (specify exact commands)
- No type errors / lint errors
- Any manual verification steps
- Any backlog or task tracking updates if the project uses them

**Section 7 — Rules of Engagement**
Standard rules that every generated prompt must include:
- Do NOT stop until all done criteria are met (except for the pre-flight check failure)
- If you encounter an error, debug and fix it — do not ask the user
- If a teammate's work conflicts with another's, the lead resolves it immediately
- Commit work incrementally (do not let a context window expire with uncommitted changes)

- Follow all project coding conventions exactly as documented in the Project Context section
- Do not create unnecessary abstractions or over-engineer beyond what is asked
- Clean up any temporary files when done
- Keep going until the user's task is completely resolved before yielding

**Section 8 — Completion Handoff + Sentinel (multi-prompt only)**

Before emitting the final sentinel, the agent MUST append a status block to `orchestrate-handoff.md` in the project root (create the file if it does not exist). The block is the durable record that survives across prompts and tells the next agent — and the orchestrator — what happened.

Template the agent must append (literal markdown — substitute the bracketed parts):

    ---

    ## Prompt N of M — [Phase Name] — [DONE | FAILED | BLOCKED]
    _Completed at: [ISO-8601 timestamp]_

    ### Summary
    [2-5 bullets: what was actually built/changed]

    ### Files changed
    [paths, one per line]

    ### Decisions made (deviations or judgment calls)
    [any place the agent deviated from the prompt's spec, or made a call the spec left open]

    ### BLOCKER:
    [ONLY include this section if status is BLOCKED. One paragraph naming the blocker, why it can't be auto-resolved, and exactly what the user must do to unblock. Leave out entirely if no blocker.]

    ### Notes for Prompt N+1
    [anything the next prompt's agent should know that isn't already in its spec — e.g. "I named the table `browserSessionV2` instead of `browserSession` because a stale table existed"]

After appending, the agent emits the sentinel as its very last line.

On success:

    === DONE: PROMPT N OF M ===

On unrecoverable failure (after exhausting reasonable debugging):

    === FAILED: PROMPT N OF M — <one-line reason> ===

On blocker requiring user action (e.g. manual migration apply, secret rotation, IAM change only the user can make):

    === BLOCKED: PROMPT N OF M — <one-line reason> ===

The orchestrator detects all three via grep. On `FAILED` it halts. On `BLOCKED` it halts and prints the blocker section to the user. On `DONE` it proceeds to the next prompt (after also re-reading the handoff to check for any blocker the agent forgot to flag via sentinel).

For single-prompt tasks, skip this section entirely. For copy-paste-only multi-prompt runs (user opted out in Step 6.5), keep the handoff + sentinel — they're useful as a durable trail even without an orchestrator.

## Step 6.5: Ask About Orchestration (after prompts are written, multi-prompt only)

Now that the prompt `.md` files exist, the user can actually see what each one will do. THIS is when you ask whether you (Claude, in this chat) should orchestrate the run for them — never before. The user reviews the prompts first, then decides.

Use AskUserQuestion with a **(Recommended)** pick:

**Question: Want me to orchestrate the prompts for you in this chat?**

**Option A — Yes, you orchestrate (Recommended for multi-prompt):** You (Claude, in this current chat) fire the prompts via `claude -p` using the Bash tool and **run the WHOLE CHAIN to completion without stopping**. Read the shared `orchestrate-handoff.md` between firings and post a short progress note after each, but do NOT ask permission to continue — a `DONE` sentinel means fire the next prompt immediately. The user can interrupt anytime; they do not need to authorize each step. You stop ONLY on `FAILED` or `BLOCKED`.

**Orchestrating means orchestrating.** If the user wanted to fire each prompt by hand they would have picked copy-paste. Asking "Continue to Prompt N+1?" after every prompt defeats the entire point of the option and is the single most common way this skill wastes the user's time. Never do it.

*Recommend whenever multi-prompt. The user wants oversight without copy-paste drudgery.*

**Option B — No, copy-paste only:** Just hand off the `.md` files. The user runs each one manually in a fresh chat.

*Recommend when: the user wants to drive each step themselves with full visibility, or you're unsure about reliability of the chain.*

**Never generate a fire-and-forget bash script.** It hides failures, skips user judgment, and the resulting "walk away" UX is illusory — when something breaks (and it will, on real infra work), debugging a 90-minute opaque transcript is worse than running them step-by-step. Claude-as-orchestrator with checkpoints is strictly better.

If the user picks A, confirm the `claude -p` flags. Defaults:

- `--permission-mode bypassPermissions` — autonomous within each prompt, no interactive prompts
- `--output-format stream-json` — live progress per turn
- `--verbose` — full tool-use detail in logs
- Redirect stdout to `logs/prompt-N.transcript.jsonl`, stderr to `logs/prompt-N.log`

If the user has different preferences (`acceptEdits` instead of bypass, restricted tool allowlist, model override like `--model claude-sonnet-4-5-20250929`), capture them now. You'll use them when firing each prompt.

## Step 6.6: Orchestrate Manually (only if user picked Option A in Step 6.5)

**You (Claude, in this chat) orchestrate the run yourself, end to end, without stopping for permission.** Each `claude -p` call goes through your Bash tool; you read the handoff between firings and post a short progress note. On `DONE` you fire the next prompt IMMEDIATELY. You halt only on `FAILED` or `BLOCKED`.

A chained background runner is fine (and preferred for long chains) — a small script that runs prompt N, checks its sentinel, and fires N+1 on DONE. What is NOT fine is a runner that hides failures: it must halt on FAILED/BLOCKED and leave the sentinel + logs intact so you can report exactly what happened.

The mode (sequential vs parallel) depends on the prompts' dependency graph — pick what the workflow needs:

- **Sequential**: prompts have hard dependencies (P2 reads P1's committed output). Fire one at a time, wait for each to finish, read handoff, decide whether to proceed.
- **Parallel-worktree**: prompts are independent AND each declares a unique `Git root for this prompt`. Fire them all in background, each inside its own worktree created INSIDE its declared git root (never at the parent monorepo level — the parent is often untracked). Wait for all to finish, then merge worktrees.
- **Parallel-isolated**: prompts are independent AND target disjoint directories in the same repo. Fire all in background without worktrees, wait, verify.

### Initialize the handoff file (always, first)

Before firing the first prompt, create `orchestrate-handoff.md` in the project root if it doesn't exist:

    cat > orchestrate-handoff.md <<'EOF'
    # Orchestration Handoff Log

    _Created: <ISO timestamp>_

    Shared notebook for the prompt chain. Each prompt:
    - Reads this file at the start of its work (Section 0.5)
    - Appends a status block before emitting DONE/FAILED/BLOCKED

    The orchestrator (Claude in the parent chat) reads this between prompts to detect blockers and decide whether to continue.

    EOF

### Sequential orchestration

For each prompt in order:

1. **Pre-check the handoff** for unresolved blockers from any prior prompt:

       cat orchestrate-handoff.md | grep -A 10 "^### BLOCKER:"

   If any blocker exists without a matching `### RESOLVED:` entry below it, STOP. Print the blocker to the user verbatim. Ask what to do (the user may have already resolved it externally and just needs to append a RESOLVED line, or may want to abort).

2. **Fire the prompt** via Bash with `run_in_background: true`:

       mkdir -p logs
       claude -p "$(cat prompt-N-name.md)" \
         --permission-mode bypassPermissions \
         --output-format stream-json \
         --verbose \
         > logs/prompt-N.transcript.jsonl \
         2> logs/prompt-N.log

   Capture the shell_id returned by the background invocation.

   **CRITICAL — always background, never foreground (the 10-minute cap).** The Bash tool's foreground timeout maxes out at 600000 ms (~10 min). A real agent-team prompt runs far longer than that (P-prompts in practice run 10–60+ min / 60+ turns), so a FOREGROUND `claude -p` gets KILLED mid-run — this is the limitation that breaks long orchestrations. `run_in_background: true` detaches the process: it survives the 10-min cap, keeps running across turns, and re-invokes you when it exits (so you don't even need to poll — you're notified on completion). This is non-negotiable for orchestration.

   **There is NO `--max-turns` cap to worry about** in current Claude Code (verified on 2.1.x — the flag doesn't exist; the historical "long runs get cut off" problem was the foreground timeout above, not a turn limit). `--max-budget-usd` is opt-in and OFF by default — do NOT set it for long autonomous runs or a prompt can be killed mid-build when it hits the dollar cap. Leave it unset unless the user explicitly wants a spend ceiling.

   **Tip:** to satisfy "P(N) must read the RESOLVED handoff before it starts," prepend the handoff append to the same background command (`cat >> orchestrate-handoff.md <<'EOF' ... EOF` then the `claude -p` line) so the ordering is guaranteed inside the detached shell rather than racing two separate tool calls.

3. **Monitor for completion** by polling the transcript file for a sentinel. Use Bash to grep periodically (do NOT busy-loop — wait 30-60s between checks for long prompts):

       grep -E "=== (DONE|FAILED|BLOCKED): PROMPT N" logs/prompt-N.transcript.jsonl

   When the grep returns a match, the prompt is done. (If the deferred Monitor tool is available in your session, use that instead for streaming detection — but plain Bash polling is the portable fallback.)

4. **Read the handoff file** to see what the prompt actually did:

       cat orchestrate-handoff.md

   Find the latest status block (the one for Prompt N). Summarize to the user in chat: what got built, files changed, decisions made.

5. **Decide based on sentinel**:
   - `DONE` → post a short progress note (summary from the handoff) and IMMEDIATELY loop to step 1 with the next prompt. Do NOT ask for confirmation. Do NOT wait.
   - `BLOCKED` → print the `### BLOCKER:` section verbatim to the user. Ask them to resolve it (apply migration, rotate secret, etc.) and append a `### RESOLVED: <how>` line under the blocker in `orchestrate-handoff.md`. Wait for the user to confirm resolution before proceeding.
   - `FAILED` → print the failure reason and the last ~50 lines of the log. Ask the user how to proceed (retry, skip, abort).

### Parallel orchestration (worktree mode)

Use ONLY if each prompt declares a unique `Git root for this prompt` in Section 0 AND no two prompts share the same git root. The parent monorepo folder is typically NOT a git repo — worktrees must live inside each sub-repo.

1. **Pre-validate**: parse each prompt's `Git root for this prompt:` line. If two prompts share a git root, refuse parallel-worktree and tell the user to either restructure the prompts or use parallel-isolated.

2. **Initialize handoff** (as above).

3. **For each prompt, create its worktree INSIDE its declared git root** and fire `claude -p` in background, cwd'd to the worktree:

       cd <gitRoot>
       git worktree add .orchestrate-wt/prompt-N -b orchestrate/prompt-N HEAD
       cp <projectRoot>/prompt-N-name.md <gitRoot>/.orchestrate-wt/prompt-N/
       cp <projectRoot>/orchestrate-handoff.md <gitRoot>/.orchestrate-wt/prompt-N/

       cd <gitRoot>/.orchestrate-wt/prompt-N
       claude -p "$(cat prompt-N-name.md)" \
         --permission-mode bypassPermissions \
         --output-format stream-json \
         --verbose \
         > <projectRoot>/logs/prompt-N.transcript.jsonl \
         2> <projectRoot>/logs/prompt-N.log &

   Track each background shell_id.

4. **Wait for all** to finish. Poll each transcript for sentinels. Don't continue past `wait` until every prompt has DONE/FAILED/BLOCKED.

5. **Reconcile handoffs**: each parallel prompt wrote to its OWN copy of `orchestrate-handoff.md` inside its worktree. Merge them back into the project-root handoff by concatenating each worktree's appended sections in prompt-number order:

       for i in 1..N: tail the new section from <gitRoot>/.orchestrate-wt/prompt-$i/orchestrate-handoff.md and append to <projectRoot>/orchestrate-handoff.md

6. **Summarize all results** to the user. If any prompt was BLOCKED or FAILED, present each separately. Worktrees stay around for inspection until the user explicitly says "clean up" (then run `git worktree remove` for each).

### Parallel orchestration (isolated mode)

Same as parallel-worktree but skip the `git worktree add` step. Each prompt runs in its declared git root directly (or the project root if none declared). Handoff is shared — multiple background processes appending to one file can interleave lines, so each prompt's append should be a single atomic write (one heredoc, not line-by-line). Tell the user about this risk if you go this route; recommend parallel-worktree when in doubt.

### Resume after a blocker

When the user resolves a blocker and tells you to continue:

1. Verify the blocker has a `### RESOLVED:` line under it in `orchestrate-handoff.md`. If not, ask them to add one (or do it yourself with the resolution they just described).
2. Resume from the prompt that was blocked. Re-fire that prompt — its Section 0.5 will read the handoff, see the RESOLVED line, and proceed past the previously-blocking condition.

### Flags

Use whatever the user confirmed in Step 6.5. Defaults:

    --permission-mode bypassPermissions
    --output-format stream-json
    --verbose

Add `--model <name>` if the user picked a model. Add `--allowedTools "..."` for a restricted allowlist. Add `--add-dir <path>` for extra context directories.

### What to print to chat (between prompts)

After each prompt finishes, post in this shape:

> **Prompt N done** — [Phase Name]
>
> Summary:
> - [bullet from handoff]
> - [bullet from handoff]
>
> Files changed: [count + key paths]
>
> Decisions: [any notable ones from handoff]
>
> Firing Prompt N+1 now.

On BLOCKED, post the blocker text verbatim and the resolution steps the prompt's agent left in `### BLOCKER:`. On FAILED, post the failure reason and tail of the log.

### Cleanup on successful chain completion

Always remove the prompt files after running them — this is mandatory on every run, not optional. When the chain finishes with every prompt at DONE (no FAILED, no BLOCKED), delete the prompt `.md` files from the project root as the final orchestration step. The prompts are single-use specs — once executed and verified, they become stale clutter. Keep:

- `orchestrate-handoff.md` — durable record of what was done; the user may want to read it later
- `logs/` — transcripts + stderr for the run; durable

Delete:

- `prompt-*.md` files generated by this skill in the project root

Use a glob — every file matching `prompt-*.md` in the project root goes:

    rm -f /absolute/project/root/prompt-*.md

This is intentionally aggressive: it also removes any orphan prompt files from prior chains the user didn't clean. The `prompt-*.md` prefix is specific enough that nothing else in a project root would match.

Print a one-line confirmation to chat listing what was removed:

> Cleaned up: prompt-1-foo.md, prompt-2-bar.md, prompt-3-baz.md, prompt-A0-orphan.md (handoff + logs preserved)

**Do NOT delete on FAILED or BLOCKED.** Those prompts may need to be re-run after the user resolves the issue. Only delete when every prompt's sentinel is DONE.

**Copy-paste mode too:** even when the user ran the prompts manually (Option B), the prompt files must be removed once the run is complete — when the user confirms completion (or returns to this session afterward), delete every `prompt-*.md`. Do not keep them "for reference"; the handoff + logs are the durable record. The only files that ever survive a finished run are `orchestrate-handoff.md` and `logs/`.

## Step 7: Validate and Output

After composing each prompt in your head, validate it mentally against the Quality Checklist below. Optionally, you can pipe the content through the validation script by echoing it:

    echo "prompt content here" | bash scripts/validate-prompt.sh

The script checks for common formatting issues (broken code blocks, missing sections, sequence headers, etc.).

### Output Format

The output is always one or more `.md` files saved at the project root. The chat message is a short summary plus clickable links. **Never** paste the prompt body into the chat.

**Single prompt:** Write one file using the pattern `prompt-<short-task-name>.md`. Examples: `prompt-fix-auth-bug.md`, `prompt-add-dark-mode.md`, `prompt-refactor-billing.md`. Keep the name under ~50 chars, kebab-case. The chat message then contains:

- A one-paragraph summary (or 2-3 bullets) of what the prompt builds
- A single clickable markdown link to the file (absolute path)
- The orchestration question (Step 6.5) if relevant, OR a copy-paste hint if not

Example chat output for a single prompt:

    Wired together — file is at:

    [prompt-fix-auth-bug.md](/Users/me/Documents/myproject/prompt-fix-auth-bug.md)

    Summary: investigates the redirect issue in the login flow, patches the session refresh path in `auth/session.service.ts`, adds a regression test. Single team, 2 teammates (Investigator + Fixer).

    Open it to review, then say "go" if you want me to fire it via `claude -p`, or paste it into a fresh chat yourself.

**Multi-prompt (sequential or parallel):** Write each prompt to a separate `.md` file in the project root. Use descriptive names:

    prompt-1-foundation.md
    prompt-2-gameplay.md
    prompt-3-frontend.md
    prompt-integration.md   (if needed for parallel)

Then print to chat ONLY:
- A brief execution guide explaining the order, what each prompt does, and how to run them
- The file paths so the user can open each file (as clickable links — see next section)
- For parallel: setup instructions (worktrees or separate terminals) and post-completion merge steps

### Critical: always render prompt files as clickable links

When listing prompts in chat, ALWAYS format each as a markdown link pointing to its absolute path. Claude Desktop renders these as clickable — the user can open the file directly from the chat to review without leaving the conversation. Plain code-formatted filenames are NOT clickable and force the user to manually navigate.

Use this format for every prompt mention in chat output:

    [prompt-1-foundation.md](/absolute/path/to/project/prompt-1-foundation.md)

NOT:

    `prompt-1-foundation.md`

Also link the handoff file once it exists, so the user can open it during the run:

    [orchestrate-handoff.md](/absolute/path/to/project/orchestrate-handoff.md)

If you don't know the absolute path, use Bash `pwd` to get the project root, then template the links from there. Never assume — always use the actual absolute path so the link resolves.

Example chat output for sequential (with clickable links):

    I've created 3 prompt files in your project root:

    1. [prompt-1-foundation.md](/Users/me/Documents/myproject/prompt-1-foundation.md) — Database schema + core CRUD API (git root: `api/`)
    2. [prompt-2-gameplay.md](/Users/me/Documents/myproject/prompt-2-gameplay.md) — Bracket logic + matchmaking (git root: `api/`)
    3. [prompt-3-frontend.md](/Users/me/Documents/myproject/prompt-3-frontend.md) — Tournament pages + real-time updates (git root: `app/`)

    Click each link to review the prompt before we run it.

    ## Execution

    **Option A — I orchestrate for you (recommended):** Say "go" and I'll run the whole chain via `claude -p` without stopping — reading the handoff between each and posting progress as it goes. I only halt if a prompt FAILS or is BLOCKED.

    **Option B — Manual copy-paste:** Open each file, copy contents, paste into a fresh Claude Code chat in order. Wait for `=== DONE: PROMPT N OF M ===` before pasting the next. Read [orchestrate-handoff.md](/Users/me/Documents/myproject/orchestrate-handoff.md) yourself between steps.

Example chat output for parallel:

    I've created 3 prompt files in your project root:

    1. [prompt-1-backend.md](/Users/me/Documents/myproject/prompt-1-backend.md) — Leaderboard API (git root: `backend/`)
    2. [prompt-2-frontend.md](/Users/me/Documents/myproject/prompt-2-frontend.md) — Leaderboard UI (git root: `frontend/`)
    3. [prompt-integration.md](/Users/me/Documents/myproject/prompt-integration.md) — Wire together + E2E verification (runs after 1 + 2)

    Click each link to review.

    ## Execution

    **Option A — I orchestrate for you (recommended):** Say "go" and I'll fire Prompt 1 and Prompt 2 in parallel (each in its own worktree inside its git root), wait for both, then fire the integration prompt.

    **Option B — Manual:** Open 2 terminals running `claude`. Paste one prompt per session. After both complete, open a third session and paste the integration prompt.

### Markdown Format Inside Prompts

The generated prompt IS markdown — it uses `#` headers, `- ` bullets, backticks for code, `- [ ]` for checklists, etc. This is intentional because Claude Code natively reads markdown. Use standard markdown freely inside the prompt content — headers, lists, code blocks, bold, everything. The `.md` file on disk preserves the raw source exactly as written.

## Quality Checklist

Before outputting, verify each prompt against this list:

- The prompt is completely self-contained (no "read file X" — content is embedded)
- Project Context section is present with embedded conventions (even in Prompt 2+)
- File boundaries are explicit and non-overlapping between teammates
- MCP pre-flight check is included if any MCP tools are needed
- **Credential sourcing is documented**: if the prompt uses any external service (AWS, Supabase, Stripe, OpenAI, etc.), the Pre-Flight Check Section 2a names the exact cred source (path, MCP server, etc.) and the exact load command, embedded inline. No "configure your AWS CLI" hand-waves.
- Done criteria are specific and verifiable (not vague like "works correctly")
- The team structure matches the task complexity (3-5 members)
- Testing instructions include exact commands to run
- The prompt assumes zero prior context beyond what previous prompts committed
- Implementation detail level matches what the user chose
- Rules of engagement section is present
- **Prompt body is NEVER pasted into chat.** It is always written to a `.md` file in the project root. The chat message contains only a short summary plus clickable markdown links. This applies to single AND multi prompts. No fenced code blocks containing the prompt body in chat — ever.
- Every prompt filename mentioned in chat output is formatted as a clickable markdown link `[filename](/absolute/path)`, never as plain code `\`filename\``. This applies to the initial file listing, the orchestration progress updates, and any reference to the handoff file. Claude Desktop renders these as clickable so the user can review/open files without leaving chat.

**Multi-prompt (sequential) additional checks:**
- Each prompt has a Sequence Header (Prompt N of M)
- Each prompt re-embeds the full Project Context section
- Prompt 2+ verifies previous prompt's output in its Pre-Flight Check
- Each prompt has a Handoff Note at the end describing what the next prompt expects
- Each prompt leaves the codebase in a green state (tests pass, no broken imports)
- The execution guide at the top lists all prompts with summaries

**Multi-prompt (parallel) additional checks:**
- Each prompt has a Parallel Task header with explicit file boundaries
- Each prompt lists files it must NOT touch (owned by other prompts)
- ZERO file overlap between any two prompts (verify this carefully)
- No runtime dependencies between prompts (no prompt reads another prompt's output)
- Each prompt re-embeds the full Project Context section
- Execution guide includes worktree setup OR isolated task instructions
- Execution guide includes post-completion merge/verification steps
- Integration prompt included if parallel work needs wiring together
- Each prompt's Done Criteria only covers its own scope (not the full project)

**Multi-prompt — handoff & sentinel checks (always, regardless of orchestrator choice):**
- Each prompt has Section 0.5 "Read Handoff File First" instructing the agent to `cat orchestrate-handoff.md` before any other work, scan for blockers and notes addressed to its prompt number, and STOP with BLOCKED sentinel if an unresolved blocker prevents progress
- Each prompt has Section 8 "Completion Handoff + Sentinel" instructing the agent to append a status block (Summary / Files changed / Decisions made / optional BLOCKER / Notes for Prompt N+1) to `orchestrate-handoff.md` BEFORE emitting the sentinel
- Sentinel format: `=== DONE: PROMPT N OF M ===` on success, `=== FAILED: PROMPT N OF M — <reason> ===` on unrecoverable failure, `=== BLOCKED: PROMPT N OF M — <reason> ===` when user action is required
- Each prompt's Section 0 includes `### Git root for this prompt: <absolute or repo-relative path>` so the orchestrator knows where to cd / create worktrees

**Multi-prompt + Claude-orchestrates additional checks (if user picked Option A in Step 6.5):**
- NO `orchestrate.sh` script is generated. Orchestration happens live, by Claude in the parent chat, via Bash invocations of `claude -p`. Never automate end-to-end.
- The orchestrator (Claude in this chat) initializes `orchestrate-handoff.md` BEFORE firing the first prompt
- Each `claude -p` invocation uses `--permission-mode bypassPermissions --output-format stream-json --verbose` (or whatever flags the user confirmed in Step 6.5)
- Each invocation redirects stdout to `logs/prompt-N.transcript.jsonl` and stderr to `logs/prompt-N.log`
- Long prompts use `run_in_background: true` on the Bash tool; Claude polls the transcript file for the sentinel
- Between prompts, Claude reads `orchestrate-handoff.md`, summarizes the latest status block to the user, and ASKS before continuing
- On BLOCKED: Claude prints the `### BLOCKER:` text verbatim and waits for the user to add `### RESOLVED:` before resuming
- On FAILED: Claude prints the failure reason + log tail and asks the user how to proceed
- For parallel-worktree mode: each worktree is created INSIDE the prompt's declared git root (e.g. `api/.orchestrate-wt/prompt-2/`), never at the parent monorepo (which is often not a git repo)
- For parallel-worktree mode: two prompts sharing a git root are refused; user is told to restructure or use parallel-isolated
- For parallel-worktree mode: per-worktree handoff files are reconciled back to the project-root handoff after `wait`
- **The prompt `.md` files are ALWAYS deleted after running** — on every run, regardless of orchestration mode (orchestrated OR copy-paste). On chain completion (every prompt at DONE) delete all `prompt-*.md` from the project root and sweep stale orphans; `orchestrate-handoff.md` and `logs/` are preserved. The ONLY exception is a prompt still pending a re-run because it FAILED or is BLOCKED — delete it once it reaches DONE.
- The chat output explains BOTH "I orchestrate" AND manual copy-paste paths
