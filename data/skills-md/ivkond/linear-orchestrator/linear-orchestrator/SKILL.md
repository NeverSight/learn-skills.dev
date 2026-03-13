---
name: linear-orchestrator
description: >
  Orchestrates spec-driven feature development in Linear — automatically detects which
  development framework is installed (Spec-Kit, BMAD METHOD, Superpowers) and follows
  its native workflow while syncing artifacts to Linear via MCP (projects, documents,
  milestones, issues, comments). Supports autonomous agent dispatch: spawns Claude
  subagents to implement Linear issues with minimal human involvement.

  Use this skill whenever the user wants to: plan or kick off a new feature, break down
  requirements into Linear issues, run a structured development workflow tracked in Linear,
  sync specs or plans to Linear, manage feature lifecycle from idea to completion, get a
  project status report from Linear, dispatch agents to implement tasks, set up a new
  Linear project with agents, or automate development with AI agents.

  Trigger keywords: "plan feature", "spec to linear", "new project", "feature kickoff",
  "create tasks in linear", "track this in linear", "project status", "break down feature",
  "speckit linear", "bmad linear", "superpowers linear", "spec-driven", "structured workflow",
  "dispatch agents", "run agents", "implement tasks", "setup linear", "configure agents",
  "setup project", "automate development".
---

# Linear Orchestrator

This skill bridges structured development frameworks (Spec-Kit, BMAD METHOD, Superpowers)
with Linear project tracking and autonomous agent dispatch.

**Three entry points** — pick the one that matches what the user needs:

| User says... | Mode |
|---|---|
| "setup", "configure project", "get started" | → **[Setup Wizard](#setup-wizard)** |
| "dispatch", "run agents", "implement tasks" | → **[Agent Dispatch](#agent-dispatch)** |
| "plan", "create spec", "new feature", "status" | → **[Framework Workflow](#framework-workflow)** |

---

## Setup Wizard

When the user wants to configure a new project or the environment for the first time,
read `references/setup-wizard.md` and follow it completely.

The wizard covers:
1. Verifying Linear MCP connection
2. Selecting or creating a Linear team/project
3. Creating standard labels
4. Installing the `linear-implementer` subagent to `.claude/agents/`
5. Configuring agent count and dispatch strategy
6. Running a verification test

**Trigger:** user says "setup", "configure", "get started", "initialize project",
or this is clearly their first time using the skill (no `.claude/agents/linear-implementer.md` exists).

---

## Agent Dispatch

When the user wants to trigger agents to implement Linear issues autonomously,
read `references/agent-dispatch.md` and follow it.

The dispatch flow:
1. Read ready issues from Linear (todo, no open blockers, `delegate` set)
2. Determine how many agents to spawn based on task count and conflict analysis
3. Spawn Claude subagents — one per non-conflicting task group
4. Each subagent reads its issue, implements, updates Linear
5. Collect results and report

**Trigger:** user says "dispatch", "run agents", "implement ready tasks", "implement [ISSUE-ID]",
"start agents", or there are issues in Linear with state `todo` and `delegate` set.

---

## Framework Workflow

For planning, spec creation, task breakdown, and status reporting, first detect the
installed framework, then route to its workflow file.

### Step 1: Detect Framework

```bash
# Spec-Kit
ls .specify/ 2>/dev/null && echo "SPECKIT" || true

# BMAD METHOD
ls .bmad-core/ 2>/dev/null && echo "BMAD" || true

# Superpowers
ls .claude-plugin/ 2>/dev/null && echo "SUPERPOWERS" || \
  ls .claude/skills/superpowers/ 2>/dev/null && echo "SUPERPOWERS" || true
```

Also ask the user directly — it's often faster.

### Step 2: Route

| Framework detected | Read this file |
|---|---|
| Spec-Kit (`.specify/` exists) | `references/framework-speckit.md` |
| BMAD METHOD (`.bmad-core/` exists) | `references/framework-bmad.md` |
| Superpowers (`.claude-plugin/` or `.claude/skills/superpowers/`) | `references/framework-superpowers.md` |
| None | `references/framework-none.md` |

> Multiple frameworks detected → ask the user which to use.

---

## Shared Utilities

### Linear MCP Quick Reference

```
save_project(name, description, state, addTeams)
save_issue(title, description, team, project, milestone, labels,
           priority, state, blocks, blockedBy, delegate, assignee)
create_document(title, project, content)
save_milestone(name, project, targetDate, description)
save_comment(issueId, body)
list_issues(project, label, state, delegate)
list_milestones(project)
list_issue_statuses(team)
get_user("me")
list_teams()
```

Full reference: `references/linear-cheatsheet.md`

### Status Dashboard

When user asks "what's the status?" or "show progress":

1. `list_issues(project: "...", label: "linear-orchestrator")` — all tracked issues
2. Group by state: done / in_progress / blocked / todo / backlog
3. Show issues with `delegate` set separately as "agent queue"
4. Calculate `done_count / total * 100` per milestone
5. Present as a summary table with progress bars

### Conventions

- All issues get label `linear-orchestrator` for traceability
- Issue titles: imperative mood ("Add user auth", not "Adding")
- Documents: `[Project Name] — Type`
- Comments: `##` markdown headers
- Default priority: Normal (3)
- Agent-assigned issues: `delegate: "claude-code"`, label: `agent`
