---
name: team-ship
description: Assemble role-based AI teammates to ship ideas from concept to production via agent teams. Use when orchestrating multi-role delivery.
allowed-tools: Read, Glob, Grep, Write($JAAN_OUTPUTS_DIR/**), Task, AskUserQuestion, Edit(jaan-to/config/settings.yaml)
argument-hint: "[initiative] [--track fast|full] [--detect] [--roles role1,role2] [--dry-run] [--resume]"
context: fork
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Requires jaan-init setup.
---

# team-ship

> Assemble a virtual company of AI teammates — each a role — to ship an idea from concept to production.

## Context Files

- `${CLAUDE_PLUGIN_ROOT}/skills/team-ship/roles.md` - Role definitions (CRITICAL — teammate roster)
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/team-ship-reference.md` - Spawn prompts, dependency algo, schemas
- `$JAAN_CONTEXT_DIR/tech.md` - Tech stack context
- `$JAAN_CONTEXT_DIR/config.md` - Project configuration
- `$JAAN_TEMPLATES_DIR/jaan-to-team-ship.template.md` - Orchestration log template
- `$JAAN_LEARN_DIR/jaan-to-team-ship.learn.md` - Past lessons (loaded in Pre-Execution)
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` - Language resolution protocol

## Input

**Arguments**: $ARGUMENTS

| Argument | Effect |
|----------|--------|
| `[initiative]` | Idea to build (required unless --detect or --resume) |
| `--track fast` | 8-skill fast track: PM → Backend → Frontend → QA → DevOps |
| `--track full` | 20-skill full track: all roles, all design steps (default) |
| `--track tdd` | TDD track: qa-test-cases → qa-tdd-orchestrate → qa-test-mutate → qa-quality-gate |
| `--detect` | Detect audit mode: 5 parallel auditors → detect-pack |
| `--roles role1,role2` | Custom role selection from roles.md |
| `--dry-run` | Display planned team structure without spawning |
| `--resume` | Resume from last checkpoint |

---

## Pre-Execution Protocol

**MANDATORY** — Read and execute ALL steps in: `${CLAUDE_PLUGIN_ROOT}/docs/extending/pre-execution-protocol.md`
Skill name: `team-ship`
Execute: Step 0 (Init Guard) → A (Load Lessons) → B (Resolve Template) → C (Offer Template Seeding)

Also read context files if available:
- `$JAAN_CONTEXT_DIR/tech.md` — Tech stack for teammate context
- `$JAAN_CONTEXT_DIR/config.md` — Project configuration

### Language Settings

Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_team-ship`

> **Language exception**: Generated code, skill commands, YAML, and role names remain in English.

---

# PHASE 0: Validation & Setup

## Thinking Mode

ultrathink

Use extended reasoning for:
- Analyzing initiative scope and complexity
- Selecting optimal track and team composition
- Planning dependency graph and execution phases
- Reviewing checkpoint for resume scenarios

## Step 1: Environment Checks

1. **Agent Teams enabled?** Read `jaan-to/config/settings.yaml` for `agent_teams_enabled`.
   If `false` or missing:
   > "Agent Teams is not enabled. To use team-ship:
   > 1. Add `agent_teams_enabled: true` to `jaan-to/config/settings.yaml`
   > 2. Set environment variable: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
   > 3. Restart Claude Code session"
   **STOP** — do not proceed.

2. **Resume mode?** If `--resume` flag:
   - Scan `$JAAN_OUTPUTS_DIR/team/` for most recent `checkpoint.yaml`
   - If found → load checkpoint, skip to resume point (see reference: "Resume Logic")
   - If not found → inform user, offer to start fresh

## Step 2: Parse Arguments

1. Extract `initiative` text (everything not a flag)
2. Determine track: `--track fast`, `--track full` (default), `--detect`, or `--roles`
3. Check for `--dry-run` flag

## Step 3: Read Role Catalog

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/team-ship/roles.md`
2. Filter roles by selected track
3. If `--roles` specified: filter to only those roles
4. For `--detect`: select only detect-* roles

## Step 4: Build Team Roster

For each selected role from roles.md:
1. Extract: Title, Model, Skills (for selected track), Phase, Dependencies, Messages
2. Build dependency graph

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/team-ship-reference.md`
> section "Dependency Graph Resolution Algorithm" for phase grouping logic.

3. Group roles into execution phases by dependency resolution
4. Calculate: total skills, teammate count, max concurrent teammates

## Step 5: Read Tech Context

Read `$JAAN_CONTEXT_DIR/tech.md` (if exists) — summarize in 2-3 lines for spawn prompts.
This summary is injected into each teammate's spawn prompt as `{tech_context_summary}`.

---

# DRY-RUN GATE

If `--dry-run` flag is set:

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/team-ship-reference.md`
> section "Dry-Run Display Format" for the output template.

Display team plan: roster, phases, dependency graph, token estimate.
Write plan to `$JAAN_OUTPUTS_DIR/team/{id}-{slug}/plan.md`.
**STOP** — do not spawn teammates.

---

# HARD STOP — Team Composition Approval

Present to user:

```
TEAM COMPOSITION
────────────────
Track: {track} ({skill_count} skills)
Initiative: "{initiative}"

Teammates ({count}):
  {role}: {skills_list} [{model}]
  ...

Phases:
  Phase 1: {roles} → PRD approval gate
  Phase 2: {roles} (parallel)
  Phase 3: {roles} (parallel)
  Phase 4: Verify + Changelog (lead)
```

> "Assemble this team and begin? [y/n/edit]"

If edit: let user adjust roles, track, or model choices. Rebuild roster.

**Do NOT proceed without explicit approval.**

---

# PHASE 1: Define (PM Teammate)

## Step 6: Spawn PM Teammate

If `--detect` mode: skip to Phase 2 (Detect Mode).

1. Read spawn prompt template from reference file
   > **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/team-ship-reference.md`
   > section "PM Teammate Prompt" for the full prompt template.
2. Fill template variables: `{initiative}`, `{slug}`, `{tech_context_summary}`
3. Spawn PM teammate with configured model
4. Wait for PM to message lead with PRD path and story paths

## Step 7: PRD Approval Gate

When PM completes:
1. Read PRD summary from output path
2. Present PRD summary to user

> "The PM has drafted the PRD. Review it at: {prd_path}
> Approve to spawn the build team? [y/n/edit]"

If no: provide feedback to PM teammate, PM revises, repeat.
If yes: shut down PM teammate (free context), proceed to Phase 2.

Update checkpoint: phase=1, pm=done, artifacts.prd_path, artifacts.entities.

---

# PHASE 2: Design + Build (Parallel Teammates)

## Step 8: Spawn Build Team

Determine Phase 2 roles from roster (those with Phase=2).

For each Phase 2 role:
1. Read spawn prompt template from reference file
   > **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/team-ship-reference.md`
   > section "{Role} Teammate Prompt" for each role's template.
2. Fill template variables: `{prd_path}`, `{stories_path}`, `{entities}`, `{slug}`
3. Spawn teammate with role's configured model
4. Register in shared task list

For `--detect` mode, instead spawn all detect-* roles from roster in parallel.

## Step 9: Monitor & Coordinate

While Phase 2 teammates are active:
1. Relay inter-teammate messages (Backend→Frontend API contract, etc.)
2. Monitor task completion via shared task list
3. Update checkpoint after each role completes a skill
4. If a teammate goes idle, TeammateIdle hook redirects to unclaimed tasks
5. If TaskCompleted hook rejects quality, relay feedback to teammate

When all Phase 2 roles report done:
- For `--detect` mode: lead runs `/jaan-to:detect-pack` to consolidate. Skip to Phase 4 wrap-up.
- For build tracks: shut down Phase 2 teammates, proceed to Phase 3.

Update checkpoint: phase=2, role statuses.

---

# PHASE 3: Integration + Ship

## Step 9a: TDD Track Execution (--track tdd)

If `--track tdd` selected, execute this specialized pipeline instead of standard Phase 2-3:

### TDD Pipeline:
1. **qa-test-cases** -- Generate BDD test cases from initiative
2. **qa-tdd-orchestrate** -- Run RED/GREEN/REFACTOR cycles with context isolation
3. **qa-test-mutate** -- Validate test effectiveness via mutation testing
4. **qa-quality-gate** (if available) -- Compute composite quality score

If `qa-quality-gate` skill is not available: skip with explicit warning: "Quality gate skill not available -- skipping composite scoring. Run qa-test-run coverage report as fallback."

### TDD-Specific Roles:

**tdd-writer** role:
- Spawn prompt restricts to: requirements text + test framework docs ONLY
- Excluded: implementation plans, existing source code, scaffold output
- Skills: qa-test-cases, qa-tdd-orchestrate (RED phase)

**tdd-implementer** role:
- Spawn prompt restricts to: failing test output + test file content ONLY
- Excluded: requirements text, RED agent reasoning, architecture plans
- Skills: qa-tdd-orchestrate (GREEN phase)

### Execution Rules:
- Max 5 concurrent teammates per phase (fan-out cap)
- DAG validation: verify dependency graph is acyclic before spawning
- After TDD pipeline completes, skip to Phase 4 (Verify + Wrap Up)

Update checkpoint: track=tdd, pipeline stages.

---

## Step 10: Integration (Lead Runs)

Lead executes directly (not a teammate — integration touches multiple output dirs):
1. `/jaan-to:dev-project-assemble` — wire scaffolds together
2. `/jaan-to:dev-output-integrate` — copy to project locations

If integration fails: update checkpoint (status=paused), present error to user.

## Step 11: Spawn Phase 3 Teammates

After integration succeeds, spawn Phase 3 roles from roster:
- QA teammate: message to proceed with `qa-test-generate` → `qa-test-run`
- DevOps teammate (spawn)
- Security teammate (spawn, full track only)

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/team-ship-reference.md`
> section "DevOps Teammate Prompt" and "Security Teammate Prompt".

Wait for all Phase 3 teammates to complete. Monitor same as Step 9.

Update checkpoint: phase=3, role statuses.

---

# PHASE 4: Verify + Wrap Up

## Step 12: Verification

Lead runs directly:
1. `/jaan-to:dev-verify` — build + runtime validation
2. If tests failed in QA: present results, offer fix-and-retry cycle
3. `/jaan-to:release-iterate-changelog` — generate changelog

## Step 13: Cleanup

1. Shut down any remaining teammates
2. Clean up team resources

## Step 14: Write Orchestration Log

Write to `$JAAN_OUTPUTS_DIR/team/{id}-{slug}/log.md` using template.

Include: initiative, track, team roster, phase timeline, skill outputs, test results, final status.

## Step 15: Final Checkpoint

Update checkpoint: phase=4, status=completed.

> "Team work complete. Orchestration log: {log_path}
> All outputs in: $JAAN_OUTPUTS_DIR/"

---

## Step 16: Capture Lessons

> "Any feedback on the team orchestration? [y/n]"

If yes: run `/jaan-to:learn-add team-ship "{feedback}"`

---

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- Role-based orchestration with configurable teammates
- Token-optimized via reference extraction
- Maintains human control at gate checkpoints

## Definition of Done

- [ ] Environment checks passed (agent teams enabled, env var set)
- [ ] Team roster approved by user
- [ ] All roles completed their skill chains
- [ ] PRD approved at Phase 1 gate
- [ ] Integration successful (dev-project-assemble + dev-output-integrate)
- [ ] Tests passing (qa-test-run)
- [ ] Verification complete (dev-verify)
- [ ] All teammates shut down
- [ ] Team cleaned up
- [ ] Orchestration log written
- [ ] Checkpoint marked as completed
