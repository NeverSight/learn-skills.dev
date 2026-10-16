---
name: gravitas-highstakes
description: >
  Mandatory checkpoint skill for irreversible/high-stakes changes (schema
  migrations, file deletion, auth/security changes, production config,
  force-pushes). Use when a task risks hard-to-reverse damage.
license: MIT
---

# GRAVITAS High-Stakes Skill

For Tier-2 actions (hard-to-reverse, high-stakes), follow this skill
**in addition to** the standard GRAVITAS cognitive loop. This skill
enforces explicit user checkpoints.

---

## Steps

### 1. State the Change and Tier Classification

Before doing anything, explicitly state:
- **What** you plan to change (specific files, tables, configs)
- **Why** this is Tier 2 (what makes it hard to reverse)
- **What** could go wrong

Format:
```
This is a Tier-2 action because: [reason]
Plan:
  1. [specific step]
  2. [specific step]
  ...
Risk: [what could break]
```

### 2. Present the Plan + Adversarial Critique

Run the full Pillar 2 process:
- Write the numbered plan
- Run the adversarial critique (separate reasoning pass)
- Revise the plan based on critique
- Present the revised plan to the user

### 3. Dry Run (if available)

If a dry-run, lint, test, or validation command is available for this
type of change, run it now:

```
# turbo — auto-approved, no user confirmation needed for this step
```

Examples:
- Database migration: `--dry-run` flag
- Config change: schema validation
- Code change: type check + lint
- Deployment: preview environment

### 4. STOP — Wait for Explicit User Confirmation

**Do not execute the plan yet.** Present the plan and ask for confirmation:

```
I've completed the reconnaissance, plan, and adversarial critique.
This is a Tier-2 (irreversible/high-stakes) action.

[Show the plan]

Do you want me to proceed with this plan? Please confirm explicitly.
```

Wait for the user's response. Do not proceed until they confirm.

### 5. Execute the Confirmed Plan

Only after explicit confirmation:
1. Execute each step in the plan
2. After each step, verify it succeeded
3. If any step fails, **stop immediately** — do not continue with the plan

### 6. Re-Verify After Execution

After all steps complete:
1. Run any available post-change verification
2. Re-read the changed files to confirm edits landed
3. If applicable, run the full test suite

Report back with:
- What was changed
- Evidence it's working
- Any concerns or follow-ups

---

## Abort Conditions

Stop the skill and report to the user if:
- A dry-run reveals unexpected side effects
- The plan needs to change mid-execution
- A verification step fails
- The user requests changes to the plan at any point

---

## Example: Database Migration

```
This is a Tier-2 action because: schema changes are irreversible once applied.

Plan:
  1. Create migration file: ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT false
  2. Run migration against dev database
  3. Update ORM model to include new column
  4. Add NOT NULL constraint after backfill (separate migration)

Risk: If the backfill is incomplete, the NOT NULL constraint will fail.
      If the migration runs in production prematurely, it could lock the table.

Dry run: psql --dry-run (or migration tool's dry-run flag)
```

[Wait for user confirmation]

[Execute and verify]
