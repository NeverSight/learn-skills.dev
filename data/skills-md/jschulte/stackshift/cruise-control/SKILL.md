---
name: cruise-control
description: Automatic mode - shift through all 6 gears sequentially without stopping. Like cruise control or automatic transmission, this runs the entire StackShift workflow from analysis to implementation in one go. Perfect for unattended execution or when you want to let StackShift handle everything automatically.
---

# Cruise Control Mode 🚗💨

**Automatic transmission for StackShift** - Shift through all 6 gears sequentially without manual intervention.

---

## When to Use This Skill

Use cruise control when:
- You want to run the entire workflow automatically
- Don't need to review each step before proceeding
- Trust StackShift to make reasonable defaults
- Want unattended execution (kick it off and come back later)
- Prefer automatic over manual transmission

**Trigger Phrases:**
- "Run StackShift in cruise control mode"
- "Automatically shift through all gears"
- "Run the full workflow automatically"
- "StackShift autopilot"

---

## What This Does

Runs all 6 gears sequentially:

```
Gear 1: Analyze → Gear 2: Reverse Engineer → Gear 3: Create Specs →
Gear 4: Gap Analysis → Gear 5: Complete Spec → Gear 6: Implement
```

**Without stopping between gears!**

---

## Setup

### Initial Configuration (One-Time)

At the start, you'll be asked:

1. **Route Selection:**
   ```
   Choose your route:
   A) Greenfield - Shift to new tech stack
   B) Brownfield - Manage existing code
   ```

2. **Implementation Framework:**
   ```
   Choose implementation framework:
   A) GitHub Spec Kit - Feature specs in .specify/, /speckit.* commands
   B) BMAD Auto-Pilot - Auto-generate BMAD artifacts from reverse-eng docs
   C) BMAD Method - Same docs, hands off to BMAD's collaborative agents
   D) Architecture Only - Generate architecture.md with your constraints
   ```

3. **Clarifications Handling:** (Spec Kit only)
   ```
   How to handle [NEEDS CLARIFICATION] markers?
   A) Defer - Mark them, implement around them, clarify later
   B) Prompt - Stop and ask questions interactively
   C) Skip - Only implement fully-specified features
   ```

4. **Implementation Scope:** (Spec Kit only)
   ```
   What to implement in Gear 6?
   A) P0 only - Critical features only
   B) P0 + P1 - Critical and high-value
   C) All - Everything (may take hours/days)
   D) None - Stop after specs are ready
   ```

5. **BMAD Synthesize Mode:** (BMAD Auto-Pilot only)
   ```
   How should BMAD artifacts be generated?
   A) YOLO - Fully automatic, no questions (~10 min)
   B) Guided - Auto-fill + targeted questions (~15-20 min)
   ```
   Note: Interactive mode is not available in cruise control (requires manual interaction).

6. **Architecture Constraints:** (Architecture Only, asked once)
   ```
   Quick architecture setup:
   - Tech stack: [Same as current / specify]
   - Cloud provider: [AWS / GCP / Azure / Self-hosted]
   - Scale: [Startup / Growing / Enterprise]
   - Hard constraints: [free text or skip]
   ```

Then cruise control takes over!

7. **Portable Extraction Mode:** (Portable Extraction only)
   ```
   How should portable specs be generated?
   A) YOLO - Fully automatic, no questions (~10 min)
   B) Guided - Auto-fill + targeted questions (~15-20 min)
   ```
   Note: Interactive mode is not available in cruise control (requires manual interaction).

**Note**: For BMAD Method, questions 3-6 are skipped. For BMAD Auto-Pilot, questions 3-4 are skipped. For Architecture Only, questions 3-5 are skipped. For Portable Extraction, questions 3-6 are skipped.

---

## Execution Flow

### GitHub Spec Kit Path

#### Gear 1: Analyze (Auto)
- Detects tech stack
- Assesses completeness
- Sets route and framework (from your selections)
- Saves state with `auto_mode: true`
- Run AST analysis for deep code inspection (`node scripts/run-ast-analysis.mjs analyze .`)
- Cache results in `.stackshift-analysis/` for all subsequent gears
- **Auto-shifts to Gear 2** ✅

#### Gear 2: Reverse Engineer (Auto)
- Launches `stackshift:code-analyzer` agent
- Extracts documentation based on route
- Generates all 9 files (including integration-points.md)
- **Auto-shifts to Gear 3** ✅

#### Gear 3: Create Specifications (Auto)
- Calls automated spec generation (F002)
- Generates constitution (appropriate template for route)
- Creates all feature specs programmatically
- Creates implementation plans for incomplete features
- Sets up `/speckit.*` slash commands
- **Auto-shifts to Gear 4** ✅

#### Gear 4: Gap Analysis (Auto)
- Runs `/speckit.analyze`
- Identifies PARTIAL/MISSING features
- Creates prioritized roadmap
- Marks [NEEDS CLARIFICATION] items
- **Auto-shifts to Gear 5** ✅

#### Gear 5: Complete Specification (Conditional)
- If clarifications handling = "Defer": Skips, moves to Gear 6
- If clarifications handling = "Prompt": Asks questions interactively, then continues
- If clarifications handling = "Skip": Marks unclear features as P2, moves on
- **Auto-shifts to Gear 6** ✅

#### Gear 6: Implement (Based on Scope)
- If scope = "None": Stops, specs ready
- If scope = "P0 only": Implements critical features only
- If scope = "P0 + P1": Implements critical + high-value
- If scope = "All": Implements everything
- Uses `/speckit.tasks` and `/speckit.implement` for each feature
- **Completes!** 🏁

---

### BMAD Auto-Pilot Path

#### Gear 1: Analyze (Auto)
- Detects tech stack
- Assesses completeness
- Sets route and framework (`bmad-autopilot`)
- Saves state with `auto_mode: true`
- **Auto-shifts to Gear 2** ✅

#### Gear 2: Reverse Engineer (Auto)
- Launches `stackshift:code-analyzer` agent
- Extracts all 11 documentation files (including business-context.md and decision-rationale.md)
- Generates all docs in `docs/reverse-engineering/`
- **Auto-shifts to BMAD Synthesize** ✅

#### Gears 3-5: Replaced by BMAD Synthesize
- Runs `/stackshift.bmad-synthesize` in selected mode (YOLO or Guided)
- Auto-generates: prd.md, architecture.md, epics.md, ux-design-specification.md
- Writes to `_bmad-output/planning-artifacts/`
- **Auto-shifts to Gear 6** ✅

#### Gear 6: BMAD Handoff (Optional)
- If user wants BMAD refinement: Displays BMAD installation + `*workflow-init` instructions
- If artifacts are sufficient: Marks workflow complete
- **StackShift completes!** 🏁

---

### BMAD Method Path (Full Collaborative)

#### Gear 1: Analyze (Auto)
- Detects tech stack
- Assesses completeness
- Sets route and framework (from your selections)
- Saves state with `auto_mode: true`
- **Auto-shifts to Gear 2** ✅

#### Gear 2: Reverse Engineer (Auto)
- Launches `stackshift:code-analyzer` agent
- Extracts all 11 documentation files
- Generates all docs in `docs/reverse-engineering/`
- **Skips to Gear 6** ✅

#### Gears 3-5: Skipped
- BMAD agents handle PRD creation, architecture, and clarifications collaboratively
- StackShift's reverse-engineering docs provide rich context for BMAD

#### Gear 6: BMAD Handoff
- Displays instructions for BMAD installation and setup
- Provides `*workflow-init` command to start BMAD workflow
- Explains how to point BMAD to `docs/reverse-engineering/`
- **StackShift completes - BMAD takes over!** 🏁

---

### Architecture Only Path

#### Gear 1: Analyze (Auto)
- Detects tech stack
- Assesses completeness
- Sets route and framework (`architect-only`)
- Collects architecture constraints (tech stack, cloud, scale)
- Saves state with `auto_mode: true`
- **Auto-shifts to Gear 2** ✅

#### Gear 2: Reverse Engineer (Auto)
- Launches `stackshift:code-analyzer` agent
- Extracts all 11 documentation files
- Generates all docs in `docs/reverse-engineering/`
- **Auto-shifts to Architecture Generator** ✅

#### Gears 3-5: Replaced by Architecture Generator
- Runs `/stackshift.architect` with user constraints from Gear 1
- Generates architecture.md with Mermaid diagrams, ADRs, infrastructure
- **StackShift completes!** 🏁

---

### Portable Extraction Path

#### Gear 1: Analyze (Auto)
- Detects tech stack
- Assesses completeness
- Sets route and framework (`portable-extract`)
- Saves state with `auto_mode: true`
- **Auto-shifts to Gear 2** ✅

#### Gear 2: Reverse Engineer (Auto)
- Launches `stackshift:code-analyzer` agent
- Extracts all 11 documentation files
- Generates all docs in `docs/reverse-engineering/`
- **Auto-shifts to Portable Extraction** ✅

#### Gears 3-5: Replaced by Portable Extraction
- Runs `/stackshift.portable-extract` in selected mode (YOLO or Guided)
- Abstracts personas to [User], [Admin], [System]
- Filters non-portable stories (tech debt, CI/CD, platform-specific)
- Extracts business rules, data contracts, edge cases
- Generates epics.md and component-spec.md in `_portable-extract/`
- **StackShift completes!** 🏁

---

## Progress Monitoring

While cruise control is running, you can check progress:

```bash
# Check current gear and progress
cat .stackshift-state.json | jq '{currentStep, completedSteps, auto_mode}'

# Watch progress in real-time
watch -n 5 'cat .stackshift-state.json | jq .currentStep'
```

---

## Interrupting Cruise Control

You can stop cruise control at any time:

```
"Stop cruise control"
"Pause StackShift"
"Switch to manual mode"
```

This will:
- Save current state
- Set `auto_mode: false`
- Allow you to proceed manually from current gear

You can resume cruise control later:
```
"Resume cruise control from current gear"
```

---

## Example: Full Automatic Run

```
User: "Run StackShift in cruise control mode"

StackShift:
Setting up cruise control...

Choose your route:
A) Greenfield - Shift to new tech stack
B) Brownfield - Manage existing code

User: "B - Brownfield"

StackShift:
How to handle clarifications?
A) Defer - Clarify later
B) Prompt - Ask me now
C) Skip - Only implement clear features

User: "A - Defer"

StackShift:
Implementation scope?
A) P0 only
B) P0 + P1
C) All features
D) None (stop after specs)

User: "B - P0 + P1"

StackShift:
✅ Cruise control engaged! Shifting through all gears automatically...

🔍 Gear 1: Analyzing... ✅ Complete (2 min)
🔄 Gear 2: Reverse engineering... ✅ Complete (8 min)
📋 Gear 3: Creating specifications... ✅ Complete (5 min)
🔍 Gear 4: Gap analysis... ✅ Complete (3 min)
✨ Gear 5: Completing specs (deferred clarifications)... ✅ Complete (1 min)
🚀 Gear 6: Implementing P0 + P1 features... 🔄 In Progress (est. 45 min)

   Feature 1/8: user-authentication... ✅
   Feature 2/8: fish-management... ✅
   Feature 3/8: photo-upload... 🔄 In progress...

[... continues automatically ...]

🏁 All gears complete! Application at 85% implementation.

Deferred clarifications (3) saved in: .specify/memory/clarifications.md
You can resolve these later with: /speckit.clarify
```

---

## Configuration Options

Cruise control can be configured via state:

```json
{
  "auto_mode": true,
  "auto_config": {
    "route": "brownfield",
    "clarifications_strategy": "defer",
    "implementation_scope": "p0_p1",
    "pause_between_gears": false,
    "notify_on_completion": true
  }
}
```

---

## Use Cases

### 1. Overnight Execution
```
5pm: "Run cruise control, brownfield, P0+P1, defer clarifications"
9am: Check results, review generated specs, answer deferred questions
```

### 2. Demo Mode
```
"Show me what StackShift does - run full demo"
→ Runs cruise control with sample project
```

---

## Safety Features

### Checkpoints

Cruise control creates checkpoints at each gear:
- State saved after each gear completes
- Can resume from any checkpoint if interrupted
- Rollback possible if issues detected

### Validation

Before proceeding:
- Validates output files were created
- Checks for errors in previous gear
- Ensures prerequisites met

### User Intervention

Pauses automatically if:
- Critical error detected
- `/speckit.analyze` shows major inconsistencies
- Implementation fails tests
- Disk space low
- Git conflicts detected

---

## Manual Override

At any point, you can:

```
"Pause after current gear"
"Stop cruise control"
"Switch to manual mode"
"Take control"
```

State saved, you can continue manually from that point.

---

## Success Criteria

### GitHub Spec Kit Path

After cruise control completes:

- ✅ All 6 gears complete
- ✅ `.stackshift-state.json` shows 6/6 gears
- ✅ All output files generated
- ✅ GitHub Spec Kit initialized (`.specify/` directory)
- ✅ Features implemented (based on scope)
- ✅ Ready for production (or clarifications if deferred)

### BMAD Auto-Pilot Path

After cruise control completes:

- ✅ Gears 1, 2 complete + BMAD Synthesize complete
- ✅ `.stackshift-state.json` shows framework: "bmad-autopilot"
- ✅ `docs/reverse-engineering/` with all 11 files generated
- ✅ `_bmad-output/planning-artifacts/` with prd.md, architecture.md, epics.md, ux-design-specification.md
- ✅ Synthesis report with coverage percentages
- ✅ Ready for BMAD refinement or direct use

### BMAD Method Path

After cruise control completes:

- ✅ Gears 1, 2, 6 complete (3-5 skipped)
- ✅ `.stackshift-state.json` shows framework: "bmad"
- ✅ `docs/reverse-engineering/` with all 11 files generated
- ✅ BMAD handoff instructions displayed
- ✅ Ready for `*workflow-init` to create PRD/Architecture collaboratively

### Architecture Only Path

After cruise control completes:

- ✅ Gears 1, 2 complete + Architecture Generator complete
- ✅ `.stackshift-state.json` shows framework: "architect-only"
- ✅ `docs/reverse-engineering/` with all 11 files generated
- ✅ `architecture.md` with Mermaid diagrams, ADRs, infrastructure recommendations
- ✅ Cost estimation and migration path included

### Portable Extraction Path

After cruise control completes:

- ✅ Gears 1, 2 complete + Portable Extraction complete
- ✅ `.stackshift-state.json` shows framework: "portable-extract"
- ✅ `docs/reverse-engineering/` with all 11 files generated
- ✅ `_portable-extract/epics.md` with abstract personas and domain-grouped epics
- ✅ `_portable-extract/component-spec.md` with business rules, data contracts, edge cases
- ✅ Portability report with extraction summary and score
- ✅ Ready to copy to any target project

---

## Technical Notes

- Cruise control is a special skill that orchestrates other skills
- Each gear is still executed by its corresponding skill
- Auto mode can be toggled on/off at any time
- State tracks auto_mode for resume capability
- Great for CI/CD, batch processing, or overnight runs

---

**Remember:** Cruise control is like automatic transmission - convenient and hands-off. Manual mode (using individual skills) gives you more control. Choose based on your needs!

🚗 **Manual** = Control each gear yourself
🤖 **Cruise Control** = Let StackShift handle it

Both get you to the same destination!
