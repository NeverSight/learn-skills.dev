---
name: ralph-tdd
description: Ralph TDD loop — autonomous coding with TDD and mutation testing. Use when running autonomous coding loops, implementing features from a backlog, or when asked about "ralph", "ralph loop", "afk coding", or "autonomous tdd".
---

# Ralph TDD Loop

**Naming**: Skill and script are both **ralph-tdd** (the capability). Ralph is designed to run AFK (away-from-keyboard); the script is `ralph-tdd.sh`.

Ralph runs AI coding agents in an AFK loop. The agent picks tasks from a backlog, implements with TDD, verifies test quality with mutation testing, and commits. You come back to working code.

**TDD**: Use the [mattpocock/skills/tdd](https://www.aihero.dev/skill-test-driven-development-claude-code) skill for red-green-refactor and vertical slicing (one test → one impl). Install: `npx skills add mattpocock/skills@tdd`. Ralph adds the backlog loop and mutation gate on top.

## Architecture

```
┌──────────────────────────────────────────────────────┐
│ RALPH OUTER LOOP (per task)                          │
│                                                      │
│  1. Read .ralph/progress.md + .ralph/lessons.md     │
│  2. Read backlog (Linear, GitHub Issues, PRD, etc.)  │
│  3. Pick highest-priority unfinished task             │
│  4. TDD red-green-refactor (see ref below)           │
│  5. Run feedback loops (types, lint, tests)           │
│  6. Verify: "Would a staff engineer approve this?"   │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │ MUTATION QUALITY GATE (see ref below)          │  │
│  │  7. Run incremental mutation testing           │  │
│  │  8. Kill survivors on touched files            │  │
│  │  9. Repeat until score >= 95%                  │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  10. Mark task done, append to .ralph/progress.md    │
│      Update .ralph/lessons.md if anything learned    │
│  11. Commit                                          │
└──────────────────────────────────────────────────────┘
```

Outer loop = Ralph picking tasks. Inner loop = mutation quality gate. The gate prevents "green but useless" tests — a constraint the AI can't cheat its way out of.

### Mutation quality gate (steps 7–9)

After tests pass: run `npm run test:mutate:incremental` (or project equivalent). For each surviving mutant on **files you changed**, write a test that would fail with the mutation, then re-run until mutation score ≥ 95% on those files. **Full workflow and setup**: use the **mutation-testing** skill (this repo; install with Ralph stack).

## Reference guide

Everything except progress format comes from installed skills (install with Ralph stack). Project-specific commands: use package.json scripts and config (vitest.config, playwright.config).

| Topic | Use | Load when |
|-------|-----|-----------|
| **TDD** | [mattpocock/skills@tdd](https://www.aihero.dev/skill-test-driven-development-claude-code) | Red-green-refactor, vertical slices, good vs bad tests |
| **Vitest** | antfu/skills@vitest | Unit tests, Vitest API |
| **Mutation testing** | mutation-testing skill (this repo) | Stryker, survivors, setup |
| **E2E** | wshobson/agents@e2e-testing-patterns | E2E/Playwright patterns |
| **AGENTS.md** | create-agents-md skill (this repo) | Creating AGENTS.md when missing |
| **Progress format** | [references/progress-format.md](references/progress-format.md) | Appending to .ralph/progress.md or .ralph/lessons.md (Ralph-specific) |

## Pre-Flight Checklist

**Before going AFK, gather all of this.** Ask the user until every item is answered.

| # | Question | Default |
|---|----------|---------|
| 1 | Project name and working directory | — |
| 2 | Backlog source (Linear team, GitHub repo, local PRD file) | — |
| 3 | Tasks to skip or focus on? | Priority order |
| 4 | How many iterations? | 5 |
| 5 | Agent runtime — see [Agent Runtimes](#agent-runtimes) | Codex |
| 6 | Permission mode — see [Permission Modes](#permission-modes) | Full auto |
| 7 | Feedback commands: typecheck, lint, test, mutation | Auto-detect |
| 8 | Does AGENTS.md exist? If not, the Ralph script will prompt the agent to run the **create-agents-md** skill first. | — |
| 9 | Start fresh .ralph/progress.md or continue existing? | Fresh |
| 10 | Does .ralph/lessons.md exist? Create if not (persists across sprints). | — |
| 11 | Commit per task, or batch? | Per task |
| 12 | Branch — current or create new? | Current |
| 13 | Anything off-limits? | None |

After gathering answers, confirm back:

```
Ready to go AFK:
- Project: [name] on branch [branch]
- Backlog: [source] — [N] iterations, priority order
- Agent: [runtime] with [permission mode]
- Feedback: tsc → biome → vitest → stryker (incremental)
- Commit after each task

Anything to change?
```

Only start after user confirms.

## Agent Runtimes

The Ralph TDD script supports multiple agent CLIs. Set `AGENT_CMD` in the script.

| Runtime | Command | Notes |
|---------|---------|-------|
| **Codex** (default) | `codex --approval-mode full-auto -q` | OpenAI Codex CLI. `-q` for quiet/non-interactive. |
| **Claude Code** | `claude -p --dangerously-skip-permissions` | Full auto. Best for AFK. |
| **Claude Code (semi)** | `claude -p --permission-mode acceptEdits` | Allows edits, blocks shell. May stall AFK. |

For true AFK, use full-auto permission modes. Semi-auto modes may prompt for approval and stall the loop.

## Permission Modes

| Mode | Claude Code Flag | Codex Flag | Risk | Best For |
|------|-----------------|------------|------|----------|
| **Full auto** | `--dangerously-skip-permissions` | `--approval-mode full-auto` | Agent can run any command | Trusted repos, overnight runs |
| **Accept edits** | `--permission-mode acceptEdits` | `--approval-mode auto-edit` | Blocks on shell commands | Semi-trusted, may stall |
| **Default** | (none) | `--approval-mode suggest` | Blocks on everything | Not suitable for AFK |

**Recommendation**: Use full-auto for AFK. The mutation testing quality gate and test suite act as safety nets. If tests pass and mutations are killed, the code is likely correct regardless of what commands ran.

## Setup

### 1. Run the Ralph TDD script

See [scripts/ralph-tdd.sh](scripts/ralph-tdd.sh) and run it directly from the skills repo (no copy required).

Make executable:

```bash
chmod +x /Users/jonathanmumm/src/skills/ralph-tdd/scripts/ralph-tdd.sh
```

Run:

```bash
/Users/jonathanmumm/src/skills/ralph-tdd/scripts/ralph-tdd.sh \
  --project /abs/path/to/your-repo \
  --iterations 5
```

Optional:

```bash
# Use Claude runtime instead of Codex
/Users/jonathanmumm/src/skills/ralph-tdd/scripts/ralph-tdd.sh \
  --project /abs/path/to/your-repo \
  --iterations 5 \
  --agent claude
```

Typically run AFK.

### 2. Create .ralph/progress.md

Ralph scripts write progress and lessons under **`.ralph/`** and ensure `.ralph/` is in the project’s `.gitignore` so these files are not committed.

```markdown
# Progress

Agent working memory. Delete after sprint.

---
```

See [references/progress-format.md](references/progress-format.md) for entry format and promise tags (COMPLETE, BLOCKED, DECIDE).

### 3. Create AGENTS.md (if missing)

The agent's onboarding doc — project description, tech stack, feedback commands, conventions, off-limits. If `AGENTS.md` doesn't exist, the Ralph script instructs the agent to run the **create-agents-md** skill (this repo) to create it from the template, then continue.

### 4. Create .ralph/lessons.md

```markdown
# Lessons

Patterns and rules learned during development. Review at the start of each iteration.

---
```

The agent updates this file after any failed approach, mistake, or course correction. Unlike .ralph/progress.md (what was done), .ralph/lessons.md captures **what to avoid** — it persists across iterations and prevents repeating the same class of mistake.

See [references/progress-format.md](references/progress-format.md) for entry format and promise tags (COMPLETE, BLOCKED, DECIDE).

## Task Prioritization

1. **Architectural decisions** — cascade through entire codebase
2. **Integration points** — reveals incompatibilities early
3. **Unknowns / spikes** — fail fast
4. **Features** — implementation work
5. **Polish** — save for last

## Task Sources & Work Tracking

**Use Linear for tracking work** when the backlog is a Linear team: mark the current task in-progress when starting, and mark it done when the task is complete (before committing). Use Linear MCP or `linear` CLI. Same idea for GitHub Issues or a local PRD — update status so progress is visible.

| Source | How |
|--------|-----|
| **Linear** | MCP or CLI. Mark issue in-progress → implement → mark done. Preferred when available. |
| **GitHub Issues** | `gh issue list`, `gh issue close` (or update labels/state) |
| **PRD file** | Local `prd.md` with checklist; tick off items as done |

## Optional: Critical work before backlog

Some setups (e.g. pro-ralph) use a **STEERING.md** (or similar) file that the agent must complete before picking backlog tasks: one-time env fixes, install deps, install Playwright browsers, start dev server, etc. You can add a step in your prompt: "Check .agent/STEERING.md (or PROJECT_ROOT/STEERING.md); complete items in sequence and remove when done. Only then proceed to the backlog." This avoids burning iterations on broken env.

## Alternative Loop Types

Same Ralph pattern works for non-feature work:

| Loop | Focus |
|------|-------|
| **Mutation Score** | Kill surviving mutants across codebase |
| **Test Coverage** | Write tests for uncovered lines |
| **Lint** | Fix lint errors one at a time |
| **Refactor** | Code smells → extract, simplify |
