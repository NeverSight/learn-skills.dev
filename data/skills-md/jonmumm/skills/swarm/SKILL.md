---
name: swarm
description: >
  A multi-agent AI development workflow. Front-loads planning questions (grill-me),
  then launches parallel agents in Git worktrees: a Feature agent builds from a backlog
  via TDD, while CRAP, Mutation, and Acceptance agents continuously harden the codebase
  using deterministic metrics. Use when the user says "swarm", "run the swarm",
  "kick off a swarm", or wants to plan and then execute a long-running multi-agent run.
---

# Swarm

Plan first, then launch parallel AI agents that build features AND continuously
harden the codebase — all running in isolated Git worktrees.

## Workflow

```
Phase 1: PLAN (interactive, human-in-the-loop)
  ├── Activate grill-me: interrogate the plan until every branch is resolved
  ├── Source the backlog: pull tasks from Linear/GitHub/Jira → local file
  └── Pre-flight checklist: detect tooling, verify setup, confirm configuration

Phase 2: EXECUTE (AFK, multi-agent, overnight)
  └── Dispatcher creates Git worktrees, launches agents in parallel:
      ├── Feature Agent   — TDD through the backlog (subsumes ralph-tdd)
      ├── CRAP Agent      — refactors complex/untested functions
      ├── Mutation Agent   — kills surviving mutants
      └── Acceptance Agent — runs full E2E suite (optional)
```

## Architecture

```
main ← the integration branch (no agent works here directly)
│
├── .swarm/
│   ├── runs/
│   │   └── 2026-03-04T22-00/
│   │       ├── backlog.md        ← Task list for Feature Agent
│   │       ├── progress.md       ← Structured log of all agent activity
│   │       ├── report.md         ← Summary generated at shutdown
│   │       └── logs/
│   │           ├── feature.log
│   │           ├── crap.log
│   │           ├── mutate.log
│   │           └── accept.log
│   │
│   ├── lessons.md                ← Persists across ALL runs
│   │
│   ├── feature/   ← Git worktree (branch: swarm/feature)
│   ├── crap/      ← Git worktree (branch: swarm/crap)
│   ├── mutate/    ← Git worktree (branch: swarm/mutate)
│   └── accept/    ← Git worktree (branch: swarm/accept)
```

All four agents work in **isolated Git worktrees** on their own branches. Main is
the shared integration target — agents rebase from main, do their work, and merge
back. No agent works directly on main.

## Agent Roles

| Agent | Needs Backlog? | Driven By | What It Does |
|-------|---------------|-----------|-------------|
| **Feature** | ✅ Yes | `.swarm/runs/<ts>/backlog.md` | Picks tasks, implements via strict TDD, commits |
| **CRAP** | ❌ No | CRAP score calculator output | Finds functions with score > 30, refactors and/or adds tests |
| **Mutation** | ❌ No | Stryker incremental survivor report | Finds surviving mutants, writes targeted killing tests |
| **Acceptance** | ❌ No | E2E pass/fail | Runs Playwright/Detox, fixes failures or flaky tests |

The Feature Agent is backlog-driven. The quality agents are entirely self-directing —
their "backlog" IS the metrics output.

### Stop Conditions

- **Feature Agent**: stops when all tasks in `backlog.md` are checked off, or max iterations
- **Quality Agents**: stop when metrics converge (CRAP < 30 everywhere, mutation ≥ 95%), or max iterations
- **Acceptance Agent**: stops when E2E suite passes, or max iterations

## Phase 1: Planning

When the user invokes this skill, **activate grill-me behavior first**:

> Interview the user relentlessly about every aspect of this plan until we reach
> a shared understanding. Walk down each branch of the design tree, resolving
> dependencies between decisions one-by-one.

### Key questions to resolve:

1. **What are we building?** Clear description of features/project.
2. **Where is the backlog?**
   - **Linear** — pull issues from a Linear team (use Linear MCP)
   - **GitHub Issues** — pull from a GitHub repo (`gh issue list`)
   - **Jira** — pull from a Jira project
   - **Local file** — point to an existing PRD, requirements.md, or checklist
   - **Create new** — build a requirements doc together during planning
3. **Scope and priority?** How many tasks? What order?
4. **Acceptance criteria?** How do we know each task is done?

Once the plan is resolved, pull tasks from the source and write them to
`.swarm/runs/<timestamp>/backlog.md` as a checklist the Feature Agent will work through.
The Feature Agent can reference the remote source (Linear, GitHub) for deeper context
on individual tasks, but the local file drives the loop.

## Pre-Flight Checklist

After planning, run through all 6 stages before launching. Auto-detect as much as
possible, confirm with the user, and fix anything missing.

### Stage 1: Project Discovery

| # | Check | How |
|---|-------|-----|
| 1 | Project root | Current directory or `--project` flag |
| 2 | Git state clean? | No uncommitted changes |
| 3 | Working branch | Current branch (becomes integration target) |
| 4 | Package manager | Detect from lockfile: `bun.lockb` → bun, `pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, else npm |
| 5 | AGENTS.md exists? | If not, create using `create-agents-md` skill. Agents rely heavily on this. |

### Stage 2: Backlog

| # | Check | How |
|---|-------|-----|
| 6 | Backlog source | From planning phase |
| 7 | Write `.swarm/runs/<ts>/backlog.md` | Pull tasks, write local file |
| 8 | Confirm scope and priority | Show task list, get user approval |

### Stage 3: Command Detection

Auto-detect from `package.json` scripts, then confirm:

| # | Command | Look For |
|---|---------|----------|
| 9 | Test | `test`, `test:unit`, `vitest` |
| 10 | Typecheck | `typecheck`, `tsc`, `type-check` |
| 11 | Lint | `lint`, `biome`, `eslint` |
| 12 | Coverage | `test:coverage` |
| 13 | Mutation | `test:mutate`, `test:mutate:incremental` |
| 14 | E2E | `test:e2e`, `e2e` |

Show detected commands and confirm:

```
Detected commands (pnpm):
  Test:      pnpm test
  Typecheck: pnpm typecheck
  Lint:      pnpm lint
  Coverage:  pnpm test:coverage
  Mutate:    pnpm test:mutate:incremental
  E2E:       pnpm test:e2e

Correct? Any changes?
```

> **Note on Monorepos:** The Swarm orchestrator executes scripts from the **root** `package.json`. If working in a monorepo (like pnpm workspaces or Turborepo), ensure the root `package.json` contains proxy scripts (e.g., `"test": "pnpm --filter web test"`, `"test:mutate:incremental": "pnpm --filter web test:mutate:incremental"`) that delegate to the appropriate packages, or else the agents will fail to run verifications.

### Stage 4: Tooling Verification

| # | Check | If Missing |
|---|-------|-----------|
| 15 | Coverage outputs `lcov.info`? | Install coverage provider, configure. See [Setup](#setup) |
| 16 | Stryker configured? | Set up using `mutation-testing` skill |
| 17 | Pre-commit hooks (Husky)? | Set up using `setup-pre-commit` skill |
| 18 | Smoke test | Run test + typecheck + lint once to verify clean baseline |
| 19 | Sub-agent smoke test | Run `env -u CLAUDECODE claude --version` to verify sub-agents can be spawned |

### Stage 5: Launch Configuration

| # | Setting | Default |
|---|---------|---------|
| 20 | Which agents? | Feature + CRAP + Mutation |
| 21 | Include Acceptance agent? | Yes if E2E command detected |
| 22 | Agent runtime | Claude |
| 23 | Feature iterations | 10 |
| 24 | Quality iterations | 10 |
| 25 | Auto-merge to main? | Yes |

### Stage 6: Confirm and Launch

```
Pre-flight complete:
- Project: my-app on branch main (pnpm)
- Backlog: 12 tasks → .swarm/runs/2026-03-04T22-00/backlog.md
- Agents: Feature + CRAP + Mutation (10 iterations each)
- Commands: pnpm test │ typecheck │ lint │ test:coverage │ test:mutate:incremental
- Hooks: ✅ husky pre-commit (lint-staged + typecheck + test)
- Coverage: ✅ v8 → coverage/lcov.info
- Stryker: ✅ incremental mode
- Baseline: ✅ all checks pass

Launch swarm?
```

Only launch after user confirms.

## Setup

### Coverage (required for CRAP agent)

```bash
# Install coverage provider (adapt command to your PM)
npm i -D @vitest/coverage-v8
```

In `vitest.config.ts`:
```typescript
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov', 'json'],
      reportsDirectory: './coverage',
    },
  },
});
```

```json
{ "scripts": { "test:coverage": "vitest run --coverage" } }
```

### Stryker (required for Mutation agent)

Use the **mutation-testing** skill's setup guide. Ensure `test:mutate:incremental`
is configured. Preserve `.stryker-incremental.json` across runs for faster iteration.

### E2E (optional, for Acceptance agent)

Ensure `test:e2e` runs your Playwright or Detox suite. The swarm is agnostic to
which framework — it only calls the npm script.

### Pre-commit Hooks

Use the **setup-pre-commit** skill to configure Husky + lint-staged. This ensures
every agent commit passes typecheck + lint + tests before landing.

## Running the Swarm

**The preferred UX:** Do all planning interactively inside the *current* Claude Code session, and then have Claude launch the swarm directly from this same session (using the shell execution tool). Do NOT ask the user to open a separate terminal.

```bash
chmod +x /path/to/skills/swarm/scripts/swarm.sh

# Prefix with 'env -u CLAUDECODE' so that sub-agents can spawn properly!
env -u CLAUDECODE /path/to/skills/swarm/scripts/swarm.sh \
  --project /abs/path/to/your-repo \
  --agents feature,crap,mutate \
  --iterations 10 \
  --agent claude
```

The script:
1. Detects your package manager
2. Creates timestamped run directory
3. Ensures `.swarm/` is added to your project's `.gitignore`
4. Creates Git worktrees for each agent
5. Installs dependencies in each worktree
6. Launches agents in parallel
7. Generates `report.md` on exit (Ctrl+C or all agents done)
8. Cleans up worktrees

## Conflict Resolution

When an agent rebases from main and encounters a merge conflict:

1. Read the conflict markers (both sides)
2. Check `git log -5 --oneline` to understand what the other agent was doing
3. Read `.swarm/runs/<ts>/progress.md` for context on recent activity
4. Resolve the conflict using reasoning about both changes
5. Run the full test suite to verify the resolution
6. If tests pass, continue. If tests fail, abort the rebase and retry next iteration.

## Progress Tracking

All agents append to `.swarm/runs/<ts>/progress.md` using a structured format:

```markdown
# Swarm Progress — 2026-03-04T22:00

## [FEATURE] 22:14 — AUTH-42: User login flow ✅
Files: src/auth/login.ts, login.test.ts · Tests: +3 (47 total) · Commit: a1b2c3d

## [CRAP] 22:15 — processCheckout 142→18 ✅
File: src/checkout/handler.ts · CC: 14→4 · Coverage: 12%→91% · Commit: d4e5f6g

## [MUTATE] 22:17 — src/utils/math.ts killed 5/7 ✅
Score: 88%→94% · Tests: +5 · Commit: h7i8j9k

## [FEATURE] 22:19 — AUTH-43: Password reset ⛔ BLOCKED
Missing SMTP config for email service
```

This format is both human-scannable and machine-parseable. Agents reference this file
to understand what other agents have been doing (useful for conflict resolution).

`.swarm/lessons.md` persists across runs — agents append patterns and mistakes learned
so future runs benefit.

## How the CRAP Score Works

CRAP = **Change Risk Anti-Patterns**. Combines cyclomatic complexity with test coverage.

**Formula:** `CRAP(fn) = CC² × (1 - cov)³ + CC`

| CRAP Score | Meaning |
|-----------|---------|
| 1–5 | Clean — low complexity, well tested |
| 5–30 | Moderate — consider refactoring or adding tests |
| 30+ | Crappy — high complexity with poor coverage, refactor immediately |

The CRAP agent picks the worst function (score > 30) and either:
- **Extracts methods** to reduce CC
- **Adds tests** to increase coverage
- **Both** — split the function AND test the pieces

See [scripts/crap4ts.mjs](scripts/crap4ts.mjs) for the calculator.

## References

| Topic | Source | Load When |
|-------|--------|-----------|
| **Planning** | `grill-me` skill | Phase 1 — interrogating the plan |
| **TDD discipline** | `mattpocock/skills@tdd` | Feature Agent red-green-refactor |
| **Mutation setup** | `mutation-testing` skill | Pre-flight or Mutation Agent |
| **Pre-commit hooks** | `setup-pre-commit` skill | Pre-flight Stage 4 |
| **AGENTS.md** | `create-agents-md` skill | Pre-flight Stage 1 |
| **Agent prompts** | [references/agent-prompts.md](references/agent-prompts.md) | Phase 2 launch |
| **Worktree lifecycle** | [references/worktree-coordination.md](references/worktree-coordination.md) | Phase 2 launch |
