---
name: create-specs
description: "Transforms 11 reverse-engineering documents from Gear 2 into GitHub Spec Kit specifications with three thoroughness levels (specs-only, specs+plans, specs+plans+tasks). Creates .specify/ directory with constitution, feature specs, implementation plans, and task breakdowns. Gear 3 of 6 in reverse engineering pipeline. Triggered by: 'create specs from reverse engineering docs', 'generate spec kit from documentation', 'run gear 3', 'transform docs into spec kit'."
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
---

# Create Specifications (GitHub Spec Kit Integration)

**Gear 3 of 6** in the Reverse Engineering to Spec-Driven Development process.

**Estimated Time:** 30 minutes (specs only) to 90 minutes (specs + plans + tasks)
**Prerequisites:** Gear 2 completed (`docs/reverse-engineering/` exists with 11 files)
**Output:** `.specify/` directory with GitHub Spec Kit structure

---

## Thoroughness Options

Gear 3 generates different levels of detail based on configuration set in Gear 1:

**Option 1: Specs Only** (30 min)
- `.specify/specs/NNN-feature-name/spec.md` for all features
- Constitution and folder structure
- Ready for manual planning with `/speckit.plan`

**Option 2: Specs + Plans** (45-60 min)
- Everything from Option 1
- Auto-generated `plan.md` for PARTIAL/MISSING features
- Ready for manual task breakdown with `/speckit.tasks`

**Option 3: Specs + Plans + Tasks** (90-120 min)
- Everything from Option 2
- Auto-generated `tasks.md` (300-500 lines each)
- Complete roadmap ready for immediate implementation

Configuration is set during Gear 1 (Analyze) via initial questionnaire, stored in `.stackshift-state.json`.

---

## Step 1: Load Configuration

Verify the state file exists and load execution parameters.

```bash
# Guard: state file must exist
if [ ! -f .stackshift-state.json ]; then
  echo "ERROR: .stackshift-state.json not found. Run Gear 1 (Analyze) first."
  exit 1
fi

# Load configuration
THOROUGHNESS=$(cat .stackshift-state.json | jq -r '.config.gear3_thoroughness // "specs"')
ROUTE=$(cat .stackshift-state.json | jq -r '.route // .path')
SPEC_OUTPUT=$(cat .stackshift-state.json | jq -r '.config.spec_output_location // "."')

echo "Route: $ROUTE"
echo "Spec output: $SPEC_OUTPUT"
echo "Thoroughness: $THOROUGHNESS"

# Determine execution flags
case "$THOROUGHNESS" in
  "specs")
    echo "Will generate: Specs only"
    GENERATE_PLANS=false
    GENERATE_TASKS=false
    ;;
  "specs+plans")
    echo "Will generate: Specs + Plans"
    GENERATE_PLANS=true
    GENERATE_TASKS=false
    ;;
  "specs+plans+tasks")
    echo "Will generate: Specs + Plans + Tasks (complete roadmap)"
    GENERATE_PLANS=true
    GENERATE_TASKS=true
    ;;
  *)
    echo "Unknown thoroughness: $THOROUGHNESS, defaulting to specs only"
    GENERATE_PLANS=false
    GENERATE_TASKS=false
    ;;
esac

# If custom output location, create .specify directory there
if [ "$SPEC_OUTPUT" != "." ]; then
  echo "Creating .specify/ structure at custom location: $SPEC_OUTPUT"
  mkdir -p "$SPEC_OUTPUT/.specify/specs"
  mkdir -p "$SPEC_OUTPUT/.specify/memory"
  mkdir -p "$SPEC_OUTPUT/.specify/templates"
  mkdir -p "$SPEC_OUTPUT/.specify/scripts"
fi
```

**Where specs are written:**

| Route | Config | Specs Written To |
|-------|--------|------------------|
| Greenfield | `spec_output_location` set | `{spec_output_location}/.specify/specs/` |
| Greenfield | Not set (default) | `./.specify/specs/` (current repo) |
| Brownfield | Always current | `./.specify/specs/` (current repo) |

Log: "PROGRESS: Configuration loaded. Route=$ROUTE, Thoroughness=$THOROUGHNESS."

---

## Step 2: Install GitHub Spec Kit Scripts

Install prerequisite scripts needed by `/speckit.*` commands downstream.

```bash
if [ -f ~/git/stackshift/scripts/install-speckit-scripts.sh ]; then
  ~/git/stackshift/scripts/install-speckit-scripts.sh .
elif [ -f ~/stackshift/scripts/install-speckit-scripts.sh ]; then
  ~/stackshift/scripts/install-speckit-scripts.sh .
else
  mkdir -p .specify/scripts/bash
  BASE_URL="https://raw.githubusercontent.com/github/spec-kit/main/scripts"
  curl -sSLf "$BASE_URL/bash/check-prerequisites.sh" -o .specify/scripts/bash/check-prerequisites.sh
  curl -sSLf "$BASE_URL/bash/setup-plan.sh" -o .specify/scripts/bash/setup-plan.sh
  curl -sSLf "$BASE_URL/bash/create-new-feature.sh" -o .specify/scripts/bash/create-new-feature.sh
  curl -sSLf "$BASE_URL/bash/update-agent-context.sh" -o .specify/scripts/bash/update-agent-context.sh
  curl -sSLf "$BASE_URL/bash/common.sh" -o .specify/scripts/bash/common.sh
  chmod +x .specify/scripts/bash/*.sh
fi
```

Verify: confirm `.specify/scripts/bash/check-prerequisites.sh` exists. Without these scripts, Gear 4 (Gap Analysis) will fail when running `/speckit.analyze`.

Log: "PROGRESS: Spec Kit scripts installed."

---

## Step 3: Generate Specifications (Automated Path)

Execute the automated reconciliation prompt to generate all specs with 100% feature coverage.

```bash
cat web/reconcile-specs.md
```

Use the output of this prompt to:
1. Parse `docs/reverse-engineering/functional-specification.md`
2. Extract EVERY feature (complete, partial, missing)
3. Generate `.specify/memory/constitution.md`
4. Create `.specify/specs/NNN-feature-name/spec.md` for ALL features
5. Create `plan.md` for PARTIAL/MISSING features

### Checkpoint: Verify Automated Path Succeeded

After running the reconciliation prompt, verify ALL of these:

```bash
# Check 1: Constitution exists
test -f .specify/memory/constitution.md && echo "OK: constitution.md exists" || echo "FAIL: constitution.md missing"

# Check 2: At least one spec exists
SPEC_COUNT=$(find .specify/specs -name "spec.md" -type f 2>/dev/null | wc -l)
echo "Spec count: $SPEC_COUNT"
if [ "$SPEC_COUNT" -eq 0 ]; then
  echo "FAIL: No specs generated"
fi
```

**IF both checks pass:** Log "PROGRESS: Automated spec generation succeeded. $SPEC_COUNT specs created." Continue to Step 4.

**IF either check fails:** Execute the manual fallback in `operations/manual-spec-generation.md`. Read that file and follow its Fallback Steps 1-5. Then continue to Step 4.

---

## Step 4: Generate Plans (Thoroughness Level 2+)

**IF GENERATE_PLANS is false:** Skip this step. Log "PROGRESS: Plan generation skipped (thoroughness=specs)."

**IF GENERATE_PLANS is true:** Read and execute `operations/plan-generation.md`. This dispatches parallel subagents to generate `plan.md` for every PARTIAL/MISSING feature.

### Checkpoint: Verify Plan Coverage

```bash
INCOMPLETE=$(grep -rl "PARTIAL\|MISSING" .specify/specs/*/spec.md 2>/dev/null | wc -l)
PLANS=$(find .specify/specs -name "plan.md" -type f 2>/dev/null | wc -l)
echo "Incomplete features: $INCOMPLETE, Plans generated: $PLANS"
```

Confirm plan count matches incomplete feature count. Report any gaps.

Log: "PROGRESS: Plan generation complete. $PLANS plans for $INCOMPLETE incomplete features."

---

## Step 5: Generate Tasks (Thoroughness Level 3 Only)

**IF GENERATE_TASKS is false:** Skip this step. Log "PROGRESS: Task generation skipped (thoroughness does not include tasks)."

**IF GENERATE_TASKS is true:** Read and execute `operations/task-generation.md`. This dispatches parallel subagents to generate comprehensive `tasks.md` for every planned feature.

### Checkpoint: Verify Task Quality

```bash
TASK_COUNT=$(find .specify/specs -name "tasks.md" -type f 2>/dev/null | wc -l)
echo "Task files generated: $TASK_COUNT"
```

Confirm task count matches plan count. Flag any tasks.md under 200 lines.

Log: "PROGRESS: Task generation complete. $TASK_COUNT task files generated."

---

## Step 6: Copy to Output Location (Greenfield Only)

**IF `spec_output_location` is "." (default):** Skip this step.

**IF `spec_output_location` is a different path:** Copy the generated `.specify/` directory to the target location.

```bash
if [ "$SPEC_OUTPUT" != "." ]; then
  cp -r .specify/* "$SPEC_OUTPUT/.specify/"
  echo "Copied .specify/ to $SPEC_OUTPUT/.specify/"
fi
```

Verify: confirm `$SPEC_OUTPUT/.specify/memory/constitution.md` exists at the target.

Log: "PROGRESS: Specs copied to $SPEC_OUTPUT."

---

## Step 7: Final Verification

Run all success criteria checks for the configured thoroughness level.

**All Levels:**
- [ ] `.specify/` directory exists
- [ ] `.specify/memory/constitution.md` exists and is non-empty
- [ ] `.specify/specs/NNN-feature-name/` directories exist for ALL features
- [ ] Each feature has `spec.md` with status markers (COMPLETE/PARTIAL/MISSING)
- [ ] `.specify/scripts/bash/check-prerequisites.sh` exists

**Thoroughness Level 2+ (Specs + Plans):**
- [ ] Every PARTIAL/MISSING feature has `plan.md`
- [ ] 100% plan coverage for incomplete features

**Thoroughness Level 3 (Specs + Plans + Tasks):**
- [ ] Every planned feature has `tasks.md`
- [ ] Each `tasks.md` is 200+ lines

Report a summary:
```
COMPLETE: Gear 3 finished.
- Constitution: created
- Specs: [N] generated (100% coverage)
- Plans: [N] generated (or "skipped")
- Tasks: [N] generated (or "skipped")
- Output location: [path]
```

---

## Output Structure

After this skill completes:

```
.specify/
├── memory/
│   └── constitution.md                    # Project principles
├── templates/
├── scripts/
│   └── bash/                              # Spec Kit automation scripts
└── specs/
    ├── 001-feature-name/
    │   ├── spec.md                        # Feature specification
    │   ├── plan.md                        # Implementation plan (level 2+)
    │   └── tasks.md                       # Task breakdown (level 3)
    └── 002-another-feature/
        └── ...

docs/reverse-engineering/                  # Kept as reference
├── functional-specification.md
├── data-architecture.md
└── ...
```

---

## Error Recovery

| Error | Recovery |
|-------|----------|
| `.stackshift-state.json` missing | Stop. Instruct user to run Gear 1 first. |
| `web/reconcile-specs.md` not found | Use manual fallback in `operations/manual-spec-generation.md`. |
| Automated spec generation produces no output | Use manual fallback in `operations/manual-spec-generation.md`. |
| Subagent task fails during plan/task generation | Re-run the failed subagent. If it fails again, generate that plan/task inline. |
| `spec_output_location` directory does not exist | Create it with `mkdir -p`. |
| Spec Kit scripts download fails (curl errors) | Warn user. Gear 4 will need scripts installed manually. |

---

## Configuration Reference

**In .stackshift-state.json:**

```json
{
  "route": "brownfield",
  "config": {
    "gear3_thoroughness": "specs+plans+tasks",
    "spec_output_location": ".",
    "plan_parallel_limit": 5,
    "task_parallel_limit": 3
  }
}
```

---

## Next Step

Proceed to **Gear 4: Gap Analysis** -- use `/speckit.analyze` to identify inconsistencies and the gap-analysis skill to create a prioritized implementation plan.
