---
name: create-specs
description: Transform reverse-engineering documentation into GitHub Spec Kit format. Initializes .specify/ directory, creates constitution.md, generates specifications from reverse-engineered docs, and sets up for /speckit slash commands. This is Step 3 of 6 in the reverse engineering process.
---

# Create Specifications (GitHub Spec Kit Integration)

**Step 3 of 6** in the Reverse Engineering to Spec-Driven Development process.

**Estimated Time:** 30 minutes (specs only) to 90 minutes (specs + plans + tasks)
**Prerequisites:** Step 2 completed (`docs/reverse-engineering/` exists with 9 files)
**Output:** `.specify/` directory with GitHub Spec Kit structure

---

## Thoroughness Options

Gear 3 generates different levels of detail based on configuration set in Gear 1:

**Option 1: Specs Only** (30 min - fast)
- Generate `.specify/specs/###-feature-name/spec.md` for all features
- Constitution and folder structure
- Ready for manual planning with `/speckit.plan`

**Option 2: Specs + Plans** (45-60 min - recommended)
- Everything from Option 1
- **PLUS**: Auto-generate `plan.md` for PARTIAL/MISSING features
- Ready for manual task breakdown with `/speckit.tasks`

**Option 3: Specs + Plans + Tasks** (90-120 min - complete roadmap)
- Everything from Option 2
- **PLUS**: Auto-generate comprehensive `tasks.md` (300-500 lines each)
- Ready for immediate implementation
- No additional planning needed

**Configuration:** Set during Gear 1 (Analyze) via initial questionnaire, stored in `.stackshift-state.json`

---

## When to Use This Skill

Use this skill when:
- You've completed Step 2 (Reverse Engineer)
- Have comprehensive documentation in `docs/reverse-engineering/`
- Ready to create formal specifications in GitHub Spec Kit format
- Want to leverage `/speckit` slash commands for implementation

**Trigger Phrases:**
- "Create specifications from documentation"
- "Transform docs into Spec Kit format"
- "Set up GitHub Spec Kit"
- "Initialize Spec Kit for this project"

---

## What This Skill Does

**Automatically** transforms reverse-engineering documentation into **GitHub Spec Kit format** using F002 automated spec generation:

1. **Read reverse engineering docs** - Parse `docs/reverse-engineering/functional-specification.md`
2. **Extract ALL features** - Identify every feature (complete, partial, missing)
3. **Generate constitution** - Create `.specify/memory/constitution.md` with project principles
4. **Create feature specs** - Generate `.specify/specs/###-feature-name/spec.md` for EVERY feature
5. **Implementation plans** - Create `plan.md` for PARTIAL and MISSING features only
6. **Enable slash commands** - Set up `/speckit.*` commands

**Critical**: This creates specs for **100% of features**, not just gaps!
- ✅ Complete features get specs (for future spec-driven changes)
- ⚠️ Partial features get specs + plans (show what exists + what's missing)
- ❌ Missing features get specs + plans (ready to implement)

**Result:** Complete spec coverage - entire application under spec control.

---

## Configuration Check (FIRST STEP!)

**Load state file to determine execution plan:**

```bash
# Check thoroughness level (set in Gear 1)
THOROUGHNESS=$(cat .stackshift-state.json | jq -r '.config.gear3_thoroughness // "specs"')

# Check route
ROUTE=$(cat .stackshift-state.json | jq -r '.path')

# Check spec output location (Greenfield may have custom location)
SPEC_OUTPUT=$(cat .stackshift-state.json | jq -r '.config.spec_output_location // "."')

echo "Route: $ROUTE"
echo "Spec output: $SPEC_OUTPUT"
echo "Thoroughness: $THOROUGHNESS"

# Determine what to execute
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

# If custom location, ensure .specify directory exists there
if [ "$SPEC_OUTPUT" != "." ]; then
  echo "Creating .specify/ structure at custom location..."
  mkdir -p "$SPEC_OUTPUT/.specify/specs"
  mkdir -p "$SPEC_OUTPUT/.specify/memory"
  mkdir -p "$SPEC_OUTPUT/.specify/templates"
  mkdir -p "$SPEC_OUTPUT/.specify/scripts"
fi
```

**Where specs will be written:**

| Route | Config | Specs Written To |
|-------|--------|------------------|
| Greenfield | spec_output_location set | `{spec_output_location}/.specify/specs/` |
| Greenfield | Not set (default) | `./.specify/specs/` (current repo) |
| Brownfield | Always current | `./.specify/specs/` (current repo) |


**Common patterns:**
- Same repo: `spec_output_location: "."` (default)
- New repo: `spec_output_location: "~/git/my-new-app"`
- Docs repo: `spec_output_location: "~/git/my-app-docs"`
- Subfolder: `spec_output_location: "./new-version"`

---

## 🤖 Execution Instructions

**IMPORTANT**: This skill uses automated spec generation tools from F002.

### Step 1: Install GitHub Spec Kit Scripts

**CRITICAL FIRST STEP:** Install the prerequisite scripts needed by `/speckit.*` commands:

```bash
# Install Spec Kit scripts to enable /speckit.* commands
if [ -f ~/git/stackshift/scripts/install-speckit-scripts.sh ]; then
  ~/git/stackshift/scripts/install-speckit-scripts.sh .
elif [ -f ~/stackshift/scripts/install-speckit-scripts.sh ]; then
  ~/stackshift/scripts/install-speckit-scripts.sh .
else
  # Download directly if script not available
  mkdir -p .specify/scripts/bash
  BASE_URL="https://raw.githubusercontent.com/github/spec-kit/main/scripts"
  curl -sSLf "$BASE_URL/bash/check-prerequisites.sh" -o .specify/scripts/bash/check-prerequisites.sh
  curl -sSLf "$BASE_URL/bash/setup-plan.sh" -o .specify/scripts/bash/setup-plan.sh
  curl -sSLf "$BASE_URL/bash/create-new-feature.sh" -o .specify/scripts/bash/create-new-feature.sh
  curl -sSLf "$BASE_URL/bash/update-agent-context.sh" -o .specify/scripts/bash/update-agent-context.sh
  curl -sSLf "$BASE_URL/bash/common.sh" -o .specify/scripts/bash/common.sh
  chmod +x .specify/scripts/bash/*.sh
  echo "✅ Downloaded GitHub Spec Kit scripts"
fi
```

**Why this is needed:**
- `/speckit.analyze` requires `scripts/bash/check-prerequisites.sh`
- `/speckit.implement` requires `scripts/bash/check-prerequisites.sh`
- `/speckit.plan` requires `scripts/bash/setup-plan.sh`
- `/speckit.specify` requires `scripts/bash/create-new-feature.sh`

**Without these scripts, Gear 4 (Gap Analysis) will fail when trying to run `/speckit.analyze`!**

### Step 2: Generate Specifications

Use the manual reconciliation approach to generate all specifications:

```bash
# Use the web reconciliation prompt to create all specs with 100% coverage
cat web/reconcile-specs.md
```

This will:
1. Parse `docs/reverse-engineering/functional-specification.md`
2. Extract EVERY feature (complete, partial, missing)
3. Generate constitution and ALL feature specs
4. Create implementation plans for incomplete features

**Expected output**:
- Constitution created
- 15-50 feature specs created (depending on app size)
- 100% feature coverage
- Implementation plans for incomplete features

### Step 3: Verify Success

After the tool completes, verify:
1. `.specify/memory/constitution.md` exists
2. `.specify/specs/###-feature-name/` directories created for ALL features
3. Each feature has `spec.md`
4. PARTIAL/MISSING features have `plan.md`

---

## If Automated Tool Fails

The MCP tool creates all Spec Kit files programmatically - it does NOT need `specify init`.

**The tool creates**:
- `.specify/memory/constitution.md` (from templates)
- `.specify/specs/###-feature-name/spec.md` (all features)
- `.specify/specs/###-feature-name/plan.md` (for incomplete features)
- `.claude/commands/speckit.*.md` (slash commands)

**If the MCP tool fails**, use the manual reconciliation prompt:

```bash
# Copy this prompt into Claude.ai:
cat web/reconcile-specs.md

# This will manually create all specs with 100% coverage
```

**DO NOT run `specify init`** - it requires GitHub API access and isn't needed since F002 creates all files directly.

This creates:
```
.specify/
├── memory/
│   └── constitution.md       # Project principles (will be generated)
├── templates/                # AI agent configs
├── scripts/                  # Automation utilities
└── specs/                    # Feature directories (will be generated)
    ├── 001-feature-name/
    │   ├── spec.md          # Feature specification
    │   ├── plan.md          # Implementation plan
    │   └── tasks.md         # Task breakdown (generated by /speckit.tasks)
    └── 002-another-feature/
        └── ...
```

**Note:** GitHub Spec Kit uses `.specify/specs/NNN-feature-name/` directory structure

### Step 2: Generate Constitution

From `docs/reverse-engineering/functional-specification.md`, create `.specify/memory/constitution.md`:

**Constitution includes:**
- **Purpose & Values** - Why this project exists, core principles
- **Technical Decisions** - Architecture choices with rationale
- **Development Standards** - Code style, testing requirements, review process
- **Quality Standards** - Performance, security, reliability requirements
- **Governance** - How decisions are made

**Use `/speckit.constitution` command:**
```
After generating initial constitution, user can run:
> /speckit.constitution

To refine and update the constitution interactively
```

### Step 3: Generate Specifications

Transform `docs/reverse-engineering/functional-specification.md` into individual feature specs in `.specify/specs/FEATURE-ID/`:

**Recommended:** Use the Task tool with `subagent_type=stackshift:technical-writer` for efficient, parallel spec generation.

**Directory Structure (per GitHub Spec Kit conventions):**

Each feature gets its own directory:
```
specs/001-user-authentication/
  ├── spec.md              # Feature specification
  └── plan.md              # Implementation plan
```

**spec.md format:**

```markdown
# Feature: User Authentication

## Status
⚠️ **PARTIAL** - Backend complete, frontend missing login UI

## Overview
[Description of what this feature does]

## User Stories
- As a user, I want to register an account so that I can save my data
- As a user, I want to log in so that I can access my dashboard

## Acceptance Criteria
- [ ] User can register with email and password
- [x] User can log in with credentials
- [ ] User can reset forgotten password
- [x] JWT tokens issued on successful login

## Technical Requirements
- Authentication method: JWT
- Password hashing: bcrypt
- Session duration: 24 hours
- API endpoints:
  - POST /api/auth/register
  - POST /api/auth/login
  - POST /api/auth/reset-password

## Implementation Status
**Completed:**
- ✅ Backend API endpoints (all 3)
- ✅ Database user model
- ✅ JWT token generation

**Missing:**
- ❌ Frontend login page
- ❌ Frontend registration page
- ❌ Password reset UI
- ❌ Token refresh mechanism

## Dependencies
None

## Related Specifications
- user-profile.md (depends on authentication)
- authorization.md (extends authentication)
```

**Use `/speckit.specify` command:**
```
After generating initial specs, user can run:
> /speckit.specify

To create additional specifications or refine existing ones
```

### Step 4: Generate Implementation Plans

For each **PARTIAL** or **MISSING** feature, create `plan.md` in the feature's directory:

**Location:** `.specify/specs/FEATURE-ID/plan.md`

**Format:**

```markdown
# Implementation Plan: User Authentication Frontend

## Goal
Complete the frontend UI for user authentication (login, registration, password reset)

## Current State
- Backend API fully functional
- No frontend UI components exist
- User lands on placeholder page

## Target State
- Complete login page with form validation
- Registration page with email verification
- Password reset flow (email + new password)
- Responsive design for mobile/desktop

## Technical Approach
1. Create React components using existing UI library
2. Integrate with backend API endpoints
3. Add form validation with Zod
4. Implement JWT token storage (localStorage)
5. Add route protection for authenticated pages

## Tasks
- [ ] Create LoginPage component
- [ ] Create RegistrationPage component
- [ ] Create PasswordResetPage component
- [ ] Add form validation
- [ ] Integrate with API endpoints
- [ ] Add loading and error states
- [ ] Write component tests
- [ ] Update routing configuration

## Risks & Mitigations
- Risk: Token storage in localStorage (XSS vulnerability)
  - Mitigation: Consider httpOnly cookies instead
- Risk: No rate limiting on frontend
  - Mitigation: Add rate limiting to API endpoints

## Testing Strategy
- Unit tests for form validation logic
- Integration tests for API calls
- E2E tests for complete auth flow

## Success Criteria
- All acceptance criteria from specification met
- No security vulnerabilities
- Pass all tests
- UI matches design system
```

**Use `/speckit.plan` command:**
```
After generating initial plans, user can run:
> /speckit.plan

To create or refine implementation plans
```

### Step 5: Mark Implementation Status

In each specification, clearly mark what's implemented vs missing:

- ✅ **COMPLETE** - Fully implemented and tested
- ⚠️ **PARTIAL** - Partially implemented (note what exists vs what's missing)
- ❌ **MISSING** - Not started

This allows `/speckit.analyze` to verify consistency.

---

## GitHub Spec Kit Slash Commands

After setting up specs, these commands become available:

### Validation & Analysis

```bash
# Check consistency between specs and implementation
> /speckit.analyze

# Identifies:
# - Specs marked COMPLETE but implementation missing
# - Implementation exists but not in spec
# - Inconsistencies between related specs
```

### Implementation

```bash
# Generate tasks from implementation plan
> /speckit.tasks

# Implement a specific feature
> /speckit.implement <specification-name>

# Runs through implementation plan step-by-step
# Updates implementation status as it progresses
```

### Clarification

```bash
# Resolve underspecified areas
> /speckit.clarify

# Interactive Q&A to fill in missing details
# Similar to our complete-spec skill
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
└── specs/                                 # Feature directories
    ├── 001-user-authentication/
    │   ├── spec.md                       # ⚠️ PARTIAL
    │   └── plan.md                       # Implementation plan
    ├── 002-fish-management/
    │   ├── spec.md                       # ⚠️ PARTIAL
    │   └── plan.md
    ├── 003-analytics-dashboard/
    │   ├── spec.md                       # ❌ MISSING
    │   └── plan.md
    └── 004-photo-upload/
        ├── spec.md                       # ⚠️ PARTIAL
        └── plan.md

docs/reverse-engineering/  # Keep original docs for reference
├── functional-specification.md
├── data-architecture.md
└── ...
```

### For Greenfield Separate Directory

If `greenfield_location` is an absolute path (e.g., `~/git/my-new-app`):

**After Gear 3, .specify/ exists in BOTH locations:**

**Original repo:**
```
~/git/my-app/
├── [original code]
├── .specify/           # Created here first
└── docs/
```

**New repo (created and initialized):**
```
~/git/my-new-app/
├── .specify/           # COPIED from original repo
├── README.md
└── .gitignore
```

**Why copy?**
- New repo needs specs for `/speckit.*` commands
- New repo is self-contained and spec-driven
- Can develop independently going forward
- Original repo keeps specs for reference

---

## Integration with Original Toolkit

**Reverse-Engineered Docs → Spec Kit Artifacts:**

| Original Doc | Spec Kit Artifact | Location |
|-------------|------------------|----------|
| functional-specification.md | constitution.md | `.specify/memory/` |
| functional-specification.md | Individual feature specs | `.specify/specs/` |
| data-architecture.md | Technical details in specs | Embedded in specifications |
| operations-guide.md | Operational notes in constitution | `.specify/memory/constitution.md` |
| technical-debt-analysis.md | Implementation plans | `.specify/specs/` |

**Keep both:**
- `docs/reverse-engineering/` - Comprehensive reference docs
- `.specify/memory/` - Spec Kit format for `/speckit` commands

---

## Step 4: Generate Plans (Optional - Thoroughness Level 2+)

**If user selected Option 2 or 3**, automatically generate implementation plans for all PARTIAL/MISSING features.

### Process

1. **Scan specs directory**:
   ```bash
   find .specify/specs -name "spec.md" -type f | sort
   ```

2. **Identify incomplete features**:
   - Parse status from each spec.md
   - Filter for ⚠️ PARTIAL and ❌ MISSING
   - Skip ✅ COMPLETE features (no plan needed)

3. **Generate plans in parallel** (5 at a time):
   ```javascript
   // For each PARTIAL/MISSING feature
   Task({
     subagent_type: 'general-purpose',
     model: 'sonnet',
     description: `Create plan for ${featureName}`,
     prompt: `
       Read: .specify/specs/${featureId}/spec.md

       Generate implementation plan following /speckit.plan template:
       - Assess current state (what exists vs missing)
       - Define target state (all acceptance criteria)
       - Determine technical approach
       - Break into implementation phases
       - Identify risks and mitigations
       - Define success criteria

       Save to: .specify/specs/${featureId}/plan.md

       Target: 300-500 lines, detailed but not prescriptive
     `
   });
   ```

4. **Verify coverage**:
   - Check every PARTIAL/MISSING spec has plan.md
   - Report summary (e.g., "8 plans generated for 8 incomplete features")

---

## Step 5: Generate Tasks (Optional - Thoroughness Level 3 Only)

**If user selected Option 3**, automatically generate comprehensive task breakdowns for all plans.

### Process

1. **Scan for plans**:
   ```bash
   find .specify/specs -name "plan.md" -type f | sort
   ```

2. **Generate tasks in parallel** (3 at a time - slower due to length):
   ```javascript
   // For each plan
   Task({
     subagent_type: 'general-purpose',
     model: 'sonnet',
     description: `Create tasks for ${featureName}`,
     prompt: `
       Read: .specify/specs/${featureId}/spec.md
       Read: .specify/specs/${featureId}/plan.md

       Generate COMPREHENSIVE task breakdown:
       - Break into 5-10 logical phases
       - Each task has: status, file path, acceptance criteria, code examples
       - Include Testing phase (unit, integration, E2E)
       - Include Documentation phase
       - Include Edge Cases section
       - Include Dependencies section
       - Include Acceptance Checklist
       - Include Priority Actions

       Target: 300-500 lines (be thorough!)

       Save to: .specify/specs/${featureId}/tasks.md
     `
   });
   ```

3. **Verify quality**:
   - Check each tasks.md is > 200 lines
   - Flag if too short (< 200 lines)
   - Report summary (e.g., "8 task files generated, avg 427 lines")

---

## Configuration

**In .stackshift-state.json:**

```json
{
  "config": {
    "gear3_thoroughness": "specs+plans+tasks",  // or "specs" or "specs+plans"
    "plan_parallel_limit": 5,
    "task_parallel_limit": 3
  }
}
```

**Or ask user interactively if not set.**

---

## Success Criteria

After running this skill, you should have:

**Thoroughness Level 1 (Specs Only):**
- ✅ `.specify/` directory initialized
- ✅ `constitution.md` created with project principles
- ✅ Individual feature specifications in `.specify/specs/`
- ✅ Implementation status clearly marked (✅/⚠️/❌)
- ✅ `/speckit.*` slash commands available

**Thoroughness Level 2 (Specs + Plans):**
- ✅ Everything from Level 1
- ✅ `plan.md` for every PARTIAL/MISSING feature
- ✅ 100% plan coverage for incomplete features
- ✅ Ready for manual task breakdown or `/speckit.tasks`

**Thoroughness Level 3 (Specs + Plans + Tasks):**
- ✅ Everything from Level 2
- ✅ `tasks.md` for every planned feature
- ✅ Comprehensive task lists (300-500 lines each)
- ✅ Complete roadmap ready for implementation
- ✅ No additional planning needed

---

## Next Step

Once specifications are created in Spec Kit format, proceed to:

**Step 4: Gap Analysis** - Use `/speckit.analyze` to identify inconsistencies and the gap-analysis skill to create prioritized implementation plan.

---

## Example Workflow

```bash
# This skill runs
1. specify init my-app
2. Generate constitution.md from functional-specification.md
3. Create individual feature specs from functional requirements
4. Mark implementation status (✅/⚠️/❌)
5. Generate implementation plans for gaps

# User can then run
> /speckit.analyze
# Shows: "5 PARTIAL features, 3 MISSING features, 2 inconsistencies"

> /speckit.implement user-authentication
# Walks through implementation plan step-by-step

> /speckit.specify
# Add new features as needed
```

---

## Technical Notes

- Spec Kit uses `.specify/` directory (not `specs/`)
- Specifications are markdown files, not JSON/YAML
- Implementation status uses emoji markers: ✅ ⚠️ ❌
- `/speckit` commands are slash commands in Claude Code, not CLI
- Constitution is a living document, update as project evolves
- Keep reverse-engineering docs as comprehensive reference
- Use `stackshift:technical-writer` agent for efficient parallel spec generation
- Always use `--ai claude` flag with `specify init` for non-interactive mode

---

**Remember:** This integrates your reverse-engineered codebase with GitHub Spec Kit, enabling the full `/speckit.*` workflow for ongoing development.
