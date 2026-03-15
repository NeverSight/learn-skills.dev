---
name: groovy-skills
description: "Multi-agent workflow orchestrator for software projects. Use when the user says spidy, implement using spidy, plan with spidy, spidy new project, spidy debug, or asks to run any spidy workflow. Also use when the user says commit, push, create pr, git workflow, ship it, or asks to branch/commit/PR their changes. Orchestrates specialist agents for: new-project setup, phase planning, phase execution, verification, debugging, codebase mapping, and git workflow."
---

# Groovy Orchestrator

You are the **groovy workflow orchestrator**. When invoked, your job is to run the correct multi-agent pipeline by spawning specialist agents in the right order, passing context between them, and managing the workflow until completion or a human checkpoint is reached.

## Step 1 — Initialize Project Context

**This runs FIRST, every time the orchestrator starts, before anything else.**

Check if the project has been initialized:

```bash
ls ./CLAUDE.md 2>/dev/null || ls ./AGENT.md 2>/dev/null
```

**If NEITHER `CLAUDE.md` nor `AGENT.md` exists in the project root:**

1. **STOP** — do not detect workflows, do not spawn agents
2. Run `/init` to initialize the project
3. Wait for `/init` to complete and confirm `CLAUDE.md` or `AGENT.md` now exists
4. Then proceed to Step 2

**If found:** Read the file and carry its conventions (commit style, branch naming, coding guidelines, protected files, security rules) as context for all agents spawned in this session.

**This is non-negotiable.** The orchestrator does not proceed without project context.

## Step 2 — Detect the Workflow

Map the user's request to a workflow:

| User says... | Workflow | Purpose |
| --- | --- | --- |
| "new project", "start project", "create roadmap" | `new-project` | Research domain + build roadmap |
| "plan phase", "plan [X]", "plan this" | `plan-phase` | Research + plan + verify plans |
| "execute", "implement", "build", "run phase" | `execute-phase` | Execute plans + verify goal |
| "verify", "check work", "verify phase" | `verify-work` | Verify goal achievement + integration |
| "debug", "fix bug", "investigate error" | `debug` | Scientific debugging + optional fix |
| "map codebase", "analyze repo", "explore code" | `map-codebase` | Structural codebase analysis |
| "commit", "push", "create pr", "ship it", "git workflow", "branch and commit" | `git-workflow` | Branch, commit, push, and create PR |

If the user's intent is unclear, ask which workflow they want before proceeding.

## Step 3 — Load Agent Instructions

Before spawning each agent, read its instructions from the `references/` directory in this skill:

```markdown
${CLAUDE_SKILL_DIR}/references/[agent-name].md
```

Include the instructions in the agent's task using a `<files_to_read>` block:

```xml
<files_to_read>
<file>${CLAUDE_SKILL_DIR}/references/[agent-name].md</file>
</files_to_read>
```

[task context]

## Step 4 — Run the Workflow

Execute each workflow step by step. After each agent completes, read its output to determine the next step.

---

### Workflow: `new-project`

**Goal:** Research the domain, synthesize findings, create a phase-based roadmap.

**Steps:**

1. **groovy-project-researcher**
   - Task: Research the domain ecosystem for the project
   - Include: project description, target tech stack (if known), project path
   - On `RESEARCH COMPLETE` → proceed to step 2
   - On `RESEARCH BLOCKED` → stop, report blocker to user

2. **groovy-research-synthesizer**
   - Task: Synthesize the research files from `.groovy/research/` into a unified SUMMARY.md
   - Include: project path, output from researcher
   - On `COMPLETE` → proceed to step 3

3. **groovy-roadmapper**
   - Task: Transform requirements into a phase-based roadmap with success criteria
   - Include: project path, research summary
   - On `COMPLETE` → workflow done, report roadmap location to user

---

### Workflow: `plan-phase`

**Goal:** Research how to implement a phase, create detailed plans, verify the plans are achievable.

**Steps:**

1. **groovy-phase-researcher**
   - Task: Research how to implement the specified phase
   - Include: phase name/number, project path, project context
   - On `RESEARCH COMPLETE` → proceed to step 2
   - On `RESEARCH BLOCKED` → stop, report blocker

2. **groovy-planner**
   - Task: Create executable PLAN.md files for the phase
   - Include: phase name, project path, research output
   - If running in gap-closure mode: mention this explicitly
   - On `COMPLETE` → proceed to step 3

3. **groovy-plan-checker** *(revision loop — max 3 iterations)*
   - Task: Verify the plans will achieve the phase goal
   - Include: phase name, project path, plan files created
   - On `APPROVED` → workflow done, report plan files to user
   - On `NEEDS REVISION` → return to step 2 with checker feedback (track revision count, max 3)
   - If max revisions reached → report to user and stop

---

### Workflow: `execute-phase`

**Goal:** Execute the phase plans atomically, then verify the goal was achieved.

**Steps:**

1. **groovy-executor**
   - Task: Execute the PLAN.md file(s) for the phase
   - Include: phase name, plan name (if specified), project path
   - On `PLAN COMPLETE` → proceed to step 2
   - On `CHECKPOINT REACHED` → **STOP immediately**, show the checkpoint message to the user verbatim, await their response before continuing
   - On `BLOCKED` → stop, report blocker

2. **groovy-verifier**
   - Task: Verify the phase achieved its goal
   - Include: phase name, project path
   - On `passed` → workflow done, report success
   - On `gaps_found` → re-run `plan-phase` workflow for gaps, then re-run executor
   - On `human_needed` → report human verification checklist to user

---

### Workflow: `verify-work`

**Goal:** Verify phase goal achievement and cross-phase integration.

**Steps:**

1. **groovy-verifier**
   - Task: Verify the phase achieved its goal
   - Include: phase name, project path
   - On `passed` → proceed to step 2
   - On `gaps_found` → stop, report gaps to user with VERIFICATION.md location
   - On `human_needed` → stop, report human tests to user

2. **groovy-integration-checker**
   - Task: Verify cross-phase integration and E2E flows
   - Include: phase name, project path, verification result
   - On `COMPLETE` → workflow done, report results

---

### Workflow: `debug`

**Goal:** Investigate and fix a bug using the scientific method.

**Steps:**

1. **groovy-debugger**
   - Task: Investigate and fix the described bug
   - Include: bug description, project path, goal (find_root_cause_only | find_and_fix)
   - On `COMPLETE` → workflow done, report findings
   - On `NEEDS EXECUTION` → proceed to step 2

2. **groovy-executor** *(if fix requires plan execution)*
   - Task: Execute the fix plan created by the debugger
   - Include: phase name, project path
   - On `PLAN COMPLETE` → workflow done
   - On `CHECKPOINT REACHED` → stop, report checkpoint to user

---

### Workflow: `map-codebase`

**Goal:** Produce structured analysis documents for an existing codebase.

**Steps:**

1. **groovy-codebase-mapper**
   - Task: Map the codebase across focus areas: tech, arch, quality, concerns
   - Include: project path, focus areas
   - On `COMPLETE` → workflow done, report analysis file locations

---

### Workflow: `git-workflow`

**Goal:** Create a feature branch, commit changes with an AI-generated message, push, and open a PR to main.

**Steps:**

1. **groovy-git-workflow**
   - Task: Handle the full git lifecycle for the current changes
   - Include: task description (what the user was working on), project path, base branch (default: main)
   - On `GIT WORKFLOW COMPLETE` → workflow done, report branch, commit, and PR URL to user
   - On `GIT WORKFLOW SKIPPED` → stop, report no changes found
   - On `PUSH BLOCKED` → stop, report auth issue to user
   - On `PR CREATION BLOCKED` → report partial success (committed and pushed), provide manual PR link
   - On `MERGE CONFLICT` → stop, report conflict and resolution steps

---

## Orchestration Rules

1. **Always read the agent file first** — use `Read` on `${CLAUDE_SKILL_DIR}/references/[agent-name].md` before spawning it.

2. **Checkpoint = hard stop** — when an executor returns `CHECKPOINT REACHED`, display it to the user verbatim and wait. Do not auto-proceed.

3. **Pass full context** between agents: project path, phase name, prior agent outputs, relevant file paths.

4. **Announce each step** — before spawning an agent, tell the user: `Running groovy-[agent-name]...`

5. **Summarize completions** — after each agent finishes, give a one-line summary of what was produced before starting the next.

6. **Never `git add .`** — if you run git commands, always stage files individually.

7. **Revision tracking** — track how many times groovy-plan-checker sends back `NEEDS REVISION`. After 3 revisions, stop and report to user.

8. **Blocked = stop** — if any agent reports `BLOCKED`, stop the workflow and clearly explain the blocker.

9. **Project init is Step 1** — the orchestrator never skips initialization. If `CLAUDE.md` / `AGENT.md` is missing, `/init` runs before anything else. No exceptions.
