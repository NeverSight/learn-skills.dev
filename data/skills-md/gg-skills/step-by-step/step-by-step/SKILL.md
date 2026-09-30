---
name: step-by-step
description: when configuring step-by-step workflows — agent work with manual actions, rollout checklists, human-in-the-loop confirmation. MCP-compatible. Not for automated-only.
---

# GG → Step by Step → Workflow

## Overview

Use this skill to turn a task list, plan checklist, study rollout, or manual validation matrix into a
single-active-step workflow. It verifies what it can first, tells the user exactly what to do now,
offers chooseable help and automation paths, persists working state into a timestamped session
folder, and only advances after the current step is resolved.

## When to Use This Skill

**TRIGGER when:**
- A task mixes agent work with user-run manual actions or validations.
- Execution needs human-in-the-loop confirmation between steps.
- A plan, study, or task contains a sequential rollout, setup, or verification checklist.
- The user explicitly asks for step-by-step guidance or asks what to do next.

**SKIP when:**
- The entire task can be executed autonomously by the agent without user involvement.
- The user wants the full checklist dumped at once rather than guided interactively.
- No ordered step queue can be identified or safely created.

## Common Misconceptions

| # | Misconception | Correction | Key concept |
|---|---------------|------------|-------------|
| 1 | The agent should present all steps at once so the user sees the full plan. | Present exactly one active step at a time; the full queue is available in the session artifact. | Single-active-step |
| 2 | If a step seems obvious, the agent can mark it resolved without evidence. | Every resolution requires evidence that matches the step's verification method. | Evidence-gated |
| 3 | The session folder is optional if the conversation context is short. | Always initialize and persist to a timestamped session folder; it prevents context loss across handoffs. | Persistence |
| 4 | Chooseable options are just polite suggestions and can be omitted. | Every active-step packet must include `AUTOMATION_OPTIONS`, `HELP_OPTIONS`, and `CONTROL_OPTIONS`. | CHOOSEABLE_OPTIONS |
| 5 | If the user says a step is done, the agent should immediately advance. | Re-check resolution using repo state, command output, or explicit proof before advancing. | Verify before advance |
| 6 | All steps can be automated. | Some steps require human-only actions (manual review, decision, confirmation). | Human-only steps |
| 7 | The step queue is static. | Renormalize when dependencies change or steps are split. | Dynamic queue |
| 8 | Preflight checks are optional. | Always run preflight verifications before prompting the user. | Preflight verification |

## Quick Decision Guide

| Scenario | Use this skill | Instead use |
|----------|---------------|-------------|
| Choosing among alternatives before execution | No | `decisions/SKILL.md` |
| Executing a fully automatable batch | No | Direct agent execution |
| Guiding a manual rollout or setup checklist | Yes | -- |
| Resuming a completed study's verification list | Yes | `study/SKILL.md` for the study itself |
| Tracking checklist items for an external task tracker | Yes | Keep local completion notes and return a concise handoff summary |
| Planning with manual steps that need guidance | Yes | `plan/SKILL.md` for the plan itself |

## Step Quality Checklist

Use this checklist before presenting any active step. Each item is a gate—the step is not ready until all required items are satisfied.

| # | Checklist Item | Why It Matters | Gate |
|---|---------------|---------------|------|
| 1 | **Queue normalized** — Ordered step queue with STEP_IDs and status | Enables single-active-step | Pre-step |
| 2 | **Session folder initialized** — Timestamped folder in `.tmp/step-by-step/` | Enables persistence | Pre-step |
| 3 | **Next step identified** — Unresolved step with highest priority | Prevents skipping | Pre-step |
| 4 | **Preflight checks run** — Agent-verifiable checks completed | Reduces user burden | Pre-step |
| 5 | **Owner separated** — Agent vs user actions clearly distinguished | Prevents confusion | Draft |
| 6 | **Title concise** — Step title is one clear sentence | Enables fast scanning | Draft |
| 7 | **Prerequisites listed** — Dependencies are explicit | Prevents out-of-order | Draft |
| 8 | **Verification method stated** — Exact evidence required for resolution | Enables verification | Draft |
| 9 | **Chooseable options included** — AUTOMATION/HELP/CONTROL options present | Enables user agency | Draft |
| 10 | **Resolution criteria clear** — What counts as "done" is explicit | Prevents reopening | Closeout |
| 11 | **Persistence maintained** — State saved after every change | Enables resume | Closeout |
| 12 | **Handoff ready** — Outputs prepared for skill transitions | Enables coordination | Closeout |

### Quality Tiers

| Tier | Criteria | Use When |
|------|----------|----------|
| **Minimal** | Items 1–3, 6, 10 | Simple single-step task |
| **Standard** | Items 1–8, 10–11 | Multi-step workflow with human actions |
| **Full** | All 12 items | Complex rollout with cross-skill coordination |

### Pre-Step Verification

Before presenting an active step, verify:

```
□ Step queue normalized with STEP_IDs and positions
□ Session folder initialized in .tmp/step-by-step/
□ Next unresolved step identified
□ Preflight checks completed (agent-verifiable items)
□ Agent vs user actions separated
□ Title is concise (< 60 chars)
□ Prerequisites listed with dependencies
□ Verification method stated with exact evidence
□ Chooseable options included (AUTOMATION/HELP/CONTROL)
□ Resolution criteria clear
□ State will be persisted after this step
```

## Step Consistency Validator

Before presenting a step, run these consistency checks. A step that fails any check must be fixed before presentation.

### Consistency Check Matrix

| Check | What to Verify | How to Fix |
|-------|---------------|------------|
| **Step vs Prerequisites** | Prerequisites are resolved before this step | Reorder queue |
| **Step vs Verification** | Verification method can actually prove completion | Refine method |
| **Step vs Options** | Options are relevant to this step's actions | Update options |
| **Step vs Handoff** | Handoff outputs are ready if skill transition | Prepare outputs |
| **Queue vs Dependencies** | Dependencies match actual prerequisite chain | Renormalize |

### Red Flags (Never Present)

A step with any of these must be fixed before presenting:

- [ ] Step without verification method
- [ ] Step with unresolvable prerequisites
- [ ] Step without chooseable options
- [ ] Session folder not initialized
- [ ] Agent action presented as user-only
- [ ] User action presented as agent-only

## Non-Negotiable Policy

1. Normalize every task into an explicit ordered step queue before presenting the first active step.
2. Present exactly one active step at a time.
3. Run preflight verifications before each step; never delegate to the user what the agent can verify directly.
4. Separate agent-executable work from user-only actions in every step packet.
5. Every active-step packet must follow `references/step-presentation-contract.md` and include chooseable automation, help, and control options, presented as printed tokens **and** the harness Ask User picker when that tool is available (`chooseable-options/references/ask-user-harness.md`).
6. Do not mark a step resolved until evidence meets its verification method; if evidence is incomplete, state exactly what is missing and keep the step active.
7. Initialize a timestamped session folder before the first step, persist state after every status change, and preserve the queue until all steps are resolved, deferred, or blocked.

## Session Persistence

Every guided run creates a gitignored session folder under
`.tmp/step-by-step/YYYY-MM-DD-HHmmss-<session-slug>/`. Use a short slug
derived from the task title or checklist subject. Store artifacts per
`references/session-artifact-contract.md`.

Minimum required persisted outputs: normalized queue snapshot, current status of every step,
active-step packets, resolution evidence summaries, and final session summary.

## Step Queue Normalization

Normalize the step queue from the best available source in this order:

1. Explicit user checklist.
2. Active `.plans/...` checklist or execution section.
3. Active study rollout or validation list.
4. Active external task-tracker checklist or manual follow-up section.
5. Session-only fallback list created from the current conversation.

Normalize each step with:

- `STEP_ID`
- Queue position
- Human-readable title
- Owner (`user`, `agent`, or `shared`)
- Prerequisites
- Verification method
- Acceptable completion evidence
- Automations the agent can offer
- Current status (`pending`, `active`, `resolved`, `deferred`, `blocked`)

If the upstream artifact already contains ordering, preserve it unless a dependency conflict forces
reordering; if that happens, explain the reason before continuing.

## One-Step Interaction Loop

1. Build or ingest the ordered step queue.
2. Initialize the timestamped `.tmp/` session folder and persist the initial queue snapshot.
3. Identify the next unresolved step.
4. Run preflight checks and gather local evidence before prompting the user.
5. Present the active-step packet using `references/step-presentation-contract.md`.
6. Persist the active-step packet and current session state.
7. If the user chooses an automation option, execute the safe agent-side work first.
8. Wait for user evidence, confirmation, or follow-up questions.
9. Re-check resolution using repo state, command output, screenshots, logs, or explicit user proof.
10. Persist updated status back to the session folder and the active plan, study, or task artifact
    when one exists.
11. Move immediately to the next unresolved step, or remain on the same one if it is still open.
12. End with a short completion or blocked-state summary when the queue is exhausted or cannot
    advance.

## Accepted Response Modes

The current step remains active when the user:

- Chooses an option token.
- Asks for clarification.
- Requests more automation.
- Pastes evidence or command output.
- Says the step is complete.
- Says the step is blocked.
- Asks to split the step into smaller substeps.

Accept native picker selection, natural-language replies, and explicit selector tokens. If the user reply is ambiguous,
do not advance; restate the active step and ask only for the missing clarification.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| User is overwhelmed by the queue | Too many steps shown or unclear titles | Re-normalize with shorter titles and stricter dependency ordering. |
| Step keeps getting reopened | Verification method is too vague or evidence is insufficient | Refine the verification method to name exact evidence in `Resolution Check`. |
| Session state appears lost | State was not persisted after a status change | Check `.tmp/step-by-step/` for the latest session folder and reconcile `session-state.json` against `queue.json`. |
| User wants to skip a blocking step | The step blocks the remaining queue | Mark the step as `blocked`, explain the impact on downstream steps, and preserve the queue. |
| Cross-skill handoff loses step context | Session directory path was not handed off | Always include session directory path, `currentStepId`, and `queue.json` in handoff outputs. |

## Common Pitfalls

1. **Forgetting to initialize the session folder.** Always create the timestamped folder before presenting the first active step. See `references/session-artifact-contract.md`.
2. **Mixing agent-only and user-only actions.** Separate what the agent can do from what the user must do. Present user actions in `What You Need To Do` and agent actions in `What I Can Do For You`.
3. **Advancing on ambiguous replies.** If the user reply is unclear, restate the active step and request clarification rather than guessing.
4. **Skipping persistence after status changes.** Persist state after queue normalization, after every active-step packet, after every evidence change, and before any skill handoff.
5. **Presenting substeps as top-level steps.** If a step is split, update the normalized queue with the new substeps and renumber rather than presenting them ad-hoc.
6. **Omitting prerequisite summaries.** Every step packet must include a prerequisite summary so the user understands dependencies.

## Cross-Skill Coordination

- `plan/SKILL.md` — use when a plan contains manual execution, setup, or validation steps that should be guided interactively instead of dumped as a batch.
- `study/SKILL.md` — use when a completed study hands off a rollout, reproduction, or verification checklist.
- `decisions/SKILL.md` — use decisions for choosing among alternatives; return here once the direction is chosen and the user needs guided execution.
- `chooseable-options/SKILL.md` — owns printed-token plus native Ask User presentation for step options.
- `research-online/SKILL.md` — use when current external docs or product behavior must be checked before the current step can be resolved.

## Handoff Outputs

### To upstream workflow skills

- Normalized queue with step statuses.
- Current active `STEP_ID`.
- Evidence gathered for resolved steps.
- Blocker summary for any unresolved active step.
- Step-by-step session directory path.
- Recommended next step or explicit blocked state.

### To `plan/SKILL.md`

- Manual-step queue extracted from the plan.
- Completed vs remaining steps.
- Validation evidence produced during the interactive loop.
- Any steps that should be re-added to the plan as blockers or follow-ups.

### To downstream task tracking when explicitly requested

- Tracker URL/ID when present.
- Checklist items completed during the session.
- Evidence or output snippets worth persisting into the task body.
- Step-by-step session directory path.
- Deferred or blocked steps that must remain visible in task tracking.

## Reference Loading by Task Type

For diagnostic requests, inspect the latest session folder in
`.tmp/step-by-step/` before loading any reference files.

| Task type | Load these files | Skip |
|-----------|-----------------|------|
| Setting up or resuming a session | `session-artifact-contract.md` | `step-presentation-contract.md` |
| Presenting or reviewing a step packet | `step-presentation-contract.md` | `session-artifact-contract.md` |
| Debugging persistence or resume issues | `session-artifact-contract.md` | `step-presentation-contract.md` |
| Refining step structure or options | `step-presentation-contract.md` | `session-artifact-contract.md` |

Load only the subset the task needs.

## Local Corpus Layout

The `references/` folder is flat (no subfolders) and contains 2 files:

| File | Description |
|------|-------------|
| `session-artifact-contract.md` | Required `.tmp/` session-folder layout, filenames for queue snapshots and step records, persistence timing rules, and resume rules. |
| `step-presentation-contract.md` | Exact structure for the active-step packet, required chooseable option groups, and resolution-check rules. |

## Step Generation Template

Use this template when presenting an active step. Fill in each section with specific content.

### Active Step Packet Structure

```markdown
# Step: [STEP_ID] - [Concise title]
**Status:** active
**Quality Tier:** [Minimal | Standard | Full]
**Owner:** [user | agent | shared]
**Session:** [path to session folder]

## What This Step Does
[Brief description of what needs to happen]

## Prerequisites
- [ ] [Prerequisite step ID]: [What must be completed first]
- [ ] [Artifact path]: [Required artifact or context]

## What I Can Do For You
[Any agent-verifiable checks or automation]

## What You Need To Do
[Specific manual action with clear instructions]

## Verification Method
[How to verify this step is complete]
- Required evidence: [Specific output, screenshot, or confirmation]
- Agent will verify: [What the agent can check automatically]

## AUTOMATION_OPTIONS
- `STEP_[ID]_AUTOMATE_[ACTION]`: [Description of automation]

## HELP_OPTIONS
- `STEP_[ID]_HELP_[TOPIC]`: [Description of help topic]

## CONTROL_OPTIONS
- `STEP_[ID]_SKIP`: Skip this step
- `STEP_[ID]_DEFER`: Defer to later
- `STEP_[ID]_SPLIT`: Split into substeps

## Next Step
**Following:** [Next STEP_ID or "Queue exhausted"]
```

### Step Normalization Template

```json
{
  "STEP_ID": "STEP_001",
  "title": "Concise step title",
  "owner": "user|agent|shared",
  "prerequisites": ["STEP_000"],
  "verificationMethod": "How to verify completion",
  "acceptableEvidence": ["output", "screenshot", "confirmation"],
  "status": "pending|active|resolved|deferred|blocked",
  "automations": ["what the agent can offer"],
  "options": {
    "automation": ["STEP_001_AUTOMATE_*"],
    "help": ["STEP_001_HELP_*"],
    "control": ["STEP_001_SKIP", "STEP_001_DEFER", "STEP_001_SPLIT"]
  }
}
```

## Quick Commands

```bash
# Initialize a step-by-step session
# Runner alternatives: bunx tsx / pnpm dlx tsx / deno run -A npm:tsx / node --import tsx / yarn dlx tsx
npx tsx .agents/skills/step-by-step/scripts/init-session.ts --name <session-name> --source <source-plan-or-study>

# Check step completeness (12-item checklist)
npx tsx .agents/skills/step-by-step/scripts/check-step-completeness.ts --step <step-id>
npx tsx .agents/skills/step-by-step/scripts/check-step-completeness.ts --session <session-dir>

# Normalize a step queue from an artifact
npx tsx .agents/skills/step-by-step/scripts/normalize-queue.ts --source <artifact-path>

# Verify step resolution
npx tsx .agents/skills/step-by-step/scripts/verify-step.ts --step <step-id> --evidence <evidence-path>
```

## Bundled Assets

| File | Description |
|------|-------------|
| `assets/icon-small.svg` | Small skill icon for IDE agent listings. |
| `assets/icon-large.png` | Large skill icon for IDE agent listings. |

---

Guidance alignment: apply repository guidance consistently with `AGENTS.md`. If this skill file is
updated, run `npm run skills:sync` so IDEs pick up the new version immediately.

[^rt]: `npx tsx` accepts any standard runner — `bunx tsx`, `pnpm dlx tsx`, `deno run -A npm:tsx`, `node --import tsx`, or `yarn dlx tsx`. The first five auto-fetch `tsx` on demand; only `node --import tsx` requires `tsx` to be installed locally first (`npm i -D tsx`, or `npm i -g tsx` if you cannot reach the npm registry). Bun users can also skip `tsx` entirely and run TypeScript directly via `bun <script>`. Pick whichever your project ships. The canonical runtime decision table lives in the `skills-manager` skill under `Runtime Selection` (only available when working in the full `gg-skills` monorepo).
