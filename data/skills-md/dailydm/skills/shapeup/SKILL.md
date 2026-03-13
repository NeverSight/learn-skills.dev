---
name: shapeup
description: "ShapeUp: Facilitate the complete ShapeUp workflow with triad collaboration"
disable-model-invocation: true
---

# ShapeUp: Facilitate the complete ShapeUp workflow with triad collaboration

When the user types `/shapeup` (or `/shapeup <subcommand>`), facilitate the ShapeUp process from problem framing through delivery, ensuring triad collaboration and acknowledging PSQ process gates.

**IMPORTANT**: This command orchestrates the workflow by **actually running** the existing ShapeUp commands at appropriate phases:
- `/frame-coach` - **MUST run immediately** when user provides problem statement (external pitch or described problem). DO NOT create pitch files or proceed without running this first.
- `/shape` - Run when transitioning to Shaping stage (after Framing Gate passed)
- `/plan` - Run when entering Building phase (after Shaping Gate passed)
- `/breakdown` - Run after plan review is complete
- `/hillchart` - Run when checking project status in Building phase
- `/implement` - Guide user to run for individual tasks

**CRITICAL**: Do not just suggest these commands—actually execute them when the phase requires it. Never skip running `/frame-coach` when a user provides a problem statement.

## Core Philosophy

- **Two distinct phases**: Shaping (collaborative) and Building (execution)
- **Triad participation**: All 3 roles (PM, Designer, Engineer) collaborate during Shaping; team stays informed during Building
- **Process gates**: Acknowledge Framing Gate and Shaping Gate as stakeholder checkpoints
- **No handoffs**: Continuous collaboration or information sharing, not sequential handoffs

## Command Structure

```
/shapeup              → Show current phase, status, and suggested next action (asks for project if not specified)
/shapeup start        → Begin with external pitch (guides to /frame-coach) - for new projects
/shapeup shaping      → Enter/continue Shaping phase (all 3 roles) - specify project if not clear
/shapeup building     → Enter/continue Building phase - specify project if not clear
/shapeup status       → Show project state and gate status (asks for project if not specified)
```

## Phase 1: SHAPING (Triad Collaboration)

### Stage 1: Framing

**Entry**: User has external pitch (typically from Google Doc)

**Facilitator Action**:

1. **Welcome and project setup**:
   ```
   "Welcome to ShapeUp! Let's start a new project.
   
   First, I need to know the project details:
   - Domain name (e.g., 'payments', 'family-messaging', 'attendance-plus')
   - Project name (e.g., 'bank-deposit-reconciliation', 'attendance-notifications')
   
   This will create the project structure at:
   projects/<domain>/<project>/
   
   What domain and project name should we use?"
   ```
   
   **Action**: Wait for user to provide domain and project name. Then continue with pitch collection.

2. **Welcome and pitch collection**:
   ```
   "Great! Now let's start with your Problem.
   
   📄 Do you have an external pitch (from Google Doc)?
   
   If yes: Paste the key points (Problem, Who's affected)
           Note: Appetite will be set by leadership after reviewing
           the problem and first instinct solutions.
           I'll run /frame-coach to evaluate and refine the problem.
   
   If no:  Describe the problem you're trying to solve
           and I'll help you frame it.
   
   Remember: All triad members should be present for Framing."
   ```

   **CRITICAL ACTION**: 
   - When the user provides ANY problem statement or pitch content (whether from Google Doc or described directly), **STOP immediately**.
   - **DO NOT** create a pitch file or proceed with any other action.
   - **IMMEDIATELY run `/frame-coach`** with the exact problem statement the user provided.
   - Wait for `/frame-coach` to complete and show its output.
   - Only after `/frame-coach` has finished, proceed to step 2 (triad alignment).

3. **After /frame-coach runs**, prompt triad alignment:
   ```
   "Your framing has been evaluated. Let's align the triad on the problem:
   
   Discussion prompts (discuss together as a team):
   [Select 2 most relevant prompts from "Problem Alignment Prompts" library]
   
   Once aligned, let's capture first instinct solutions.
   (Note: Appetite will be set by leadership after reviewing problem + solutions)"
   ```
   
   **Action**: Select 2 prompts from the "Problem Alignment Prompts" library (either most relevant to the context or randomly). Surface only these 2 prompts to avoid overwhelming the triad.

4. **First instinct solutions** (before Framing Gate):
   ```
   "Let's capture first instinct solutions from each perspective.
   No wrong answers — we're exploring the solution space.
   
   Discussion prompts:
   [Select 2 most relevant prompts from "First Instinct Solutions Prompts" library]
   
   These instincts will inform our shaping. Often the best solutions
   combine insights from all three perspectives.
   
   Capture and document these first instinct solutions together."
   ```
   
   **Action**: Select 2 prompts from the "First Instinct Solutions Prompts" library (either most relevant to the context or randomly). Surface only these 2 prompts.

5. **Framing Gate** (after problem alignment and first instinct solutions):
   ```
   "Now that we have:
   ✅ Problem definition (refined via /frame-coach)
   ✅ Triad alignment on the problem
   ✅ First instinct solutions captured
   
   ⛳ FRAMING GATE CHECK
      Leadership reviews the problem and first instinct solutions, then:
      1. Sets the Appetite (time/effort allocation)
      2. Approves both the problem and first instinct solutions
      
      [ ] Yes, appetite set and both approved — proceed to Shaping
      [ ] Not yet — pause here, get leadership review and approval first
   
   The appetite is determined by leadership based on:
   - The problem's importance and priority
   - The complexity implied by the first instinct solutions
   - Available resources and business context
   
   Once appetite is set and approved, we'll proceed to formal shaping."
   ```

### Stage 2: Shaping

**Entry**: Problem aligned, first instinct solutions captured, Framing Gate passed (leadership set appetite and approved problem + first instinct solutions)

**If project not specified**:
```
"To continue with shaping, I need to know which project you're working on.

Please specify:
- The project name/path (e.g., 'payments/bank-deposit-reconciliation')
- Or say 'list projects' to see available projects"
```

**Action**: 
- If user says "list projects": Scan `projects/` directory, list all projects found, and ask user to select one.
- If user provides project path: Verify it exists, then proceed with shaping.
- Otherwise: Wait for user to specify project.

**Facilitator Action**:

1. **Run /shape command**:
   ```
   "Now let's shape the solution. I'll create a shaping doc and we'll
   refine it together.
   
   Running /shape with your pitch...
   ```
   
   **CRITICAL ACTION**: 
   - **STOP immediately** - do not proceed with any other action.
   - **IMMEDIATELY run `/shape`** with the pitch document (or reference to the pitch file).
   - Wait for `/shape` to complete and create the shaping.md file.
   - Only after `/shape` has finished, proceed to the review prompts (step 2).

2. **Breadboard review prompts**:
   ```
   "📐 BREADBOARD (Places, Affordances, Connections)
   
   Discussion prompts:
   [Select 2 most relevant prompts from "Breadboard Review Prompts" library]
   
   Discuss together, then confirm when ready."
   ```
   
   **Action**: Select 2 prompts from the "Breadboard Review Prompts" library (either most relevant to the context or randomly). Surface only these 2 prompts.

3. **Fat marker sketches/prototypes** (after breadboard is complete):
   ```
   "🎨 FOR THE DESIGNER: Fat Marker Sketches/Prototypes
   
   Now that the breadboard is complete, create fat marker sketches or 
   prototypes to visualize the solution at the right level of detail.
   
   Feel free to copy this prompt template to start in Figma:
   
   ---
   Make prototype: Replicate the attached page applying a hand-drawn fat 
   marker aesthetic: FIRST, ask the user which sections should remain 
   visually high-level/non-functional. For these sections, use skeleton-style 
   placeholders: light grey box characters (████████) with text-gray-400 and 
   .sketch-border (not thick) with grey borders instead of black. Create an 
   SVG filter in the root component (<svg width="0" height="0" 
   style={{ position: 'absolute' }}>) with feTurbulence 
   (type="fractalNoise", baseFrequency="0.05", numOctaves="3") and 
   feDisplacementMap (scale="3"). Define .sketch-border (2px black border, 
   2px border-radius, -2px offset) and .sketch-border-thick (4px black 
   border, 3px border-radius, -3px offset) in /styles/globals.css using 
   ::before pseudo-elements with absolute positioning, pointer-events: none, 
   and filter: url(#sketch-filter). Apply these classes to all containers, 
   cards, buttons, and navigation—never use standard Tailwind borders. Use 
   monospace fonts (font-mono) throughout with this hierarchy: page titles 
   (text-2xl font-bold), card/section labels (text-sm, often uppercase), 
   large metrics (text-3xl font-bold), supporting details (text-sm 
   text-gray-600), buttons (text-sm), module titles (font-bold), module 
   descriptions (text-xs text-gray-400), nav section headers (text-xs 
   font-bold). STRICT GREYSCALE ONLY: All colors must be white, gray-50, 
   gray-100, gray-200, gray-300, gray-400, gray-600, or black—no blues, greens, 
   reds, or any other colors. Sharp rectangular shapes (no rounded corners), 
   low-fidelity hand-drawn aesthetic. Add inline styles where needed: 
   style={{ borderBottom: '4px solid black' }}.
   ---
   
   The fat marker sketches help the team visualize the solution without 
   getting into pixel-perfect detail. They should match the breadboard's 
   places, affordances, and connections.
   
   While the designer works on sketches, the team can continue with rabbit 
   holes and no-gos. Share sketches when ready for triad review."
   ```

4. **Rabbit holes review prompts**:
   ```
   "🐰 RABBIT HOLES (Risks)
   
   Discussion prompts:
   [Select 2 most relevant prompts from "Rabbit Holes (Risks) Prompts" library]
   
   Discuss together, then confirm when ready."
   ```
   
   **Action**: Select 2 prompts from the "Rabbit Holes (Risks) Prompts" library (either most relevant to the context or randomly). Surface only these 2 prompts.

5. **No-gos review prompts**:
   ```
   "🚫 NO-GOS (Boundaries)
   
   Discussion prompts:
   [Select 2 most relevant prompts from "No-Gos (Boundaries) Prompts" library]
   
   Discuss together, then confirm when ready."
   ```
   
   **Action**: Select 2 prompts from the "No-Gos (Boundaries) Prompts" library (either most relevant to the context or randomly). Surface only these 2 prompts.

6. **Shaping complete check**:
   ```
   "📝 Shaping Complete Checklist:
   
   - [ ] Breadboard captures all key flows
   - [ ] Fat marker sketches/prototypes created (recommended)
   - [ ] Risks identified and classified
   - [ ] No-gos protect the appetite
   - [ ] All 3 roles have contributed and agree
   
   🎨 FOR THE DESIGNER: Design Review with Paul
   
   Before proceeding to the Shaping Gate, review the design artifacts 
   (breadboard, fat marker sketches/prototypes) with @Paul Hershey for 
   design QA and feedback.
   
   This review should happen before the Shaping Gate to ensure design 
   alignment before the Go/No-Go decision.
   
   ⛳ SHAPING GATE CHECK
      Has the Pitch been approved at the Shaping Gate (Go/No-Go)?
      
      [ ] Yes, Go decision — proceed to Building
      [ ] Not yet — pause here, schedule Shaping Gate review
      [ ] No-Go — archive this pitch, return to problem discovery
   
   If approved, I'll transition to Building phase."
   ```

## Phase 2: BUILDING (Execution)

### Transition to Building

**If project not specified**:
```
"To continue with building, I need to know which project you're working on.

Please specify:
- The project name/path (e.g., 'payments/bank-deposit-reconciliation')
- Or say 'list projects' to see available projects"
```

**Action**: 
- If user says "list projects": Scan `projects/` directory, list all projects found, and ask user to select one.
- If user provides project path: Verify it exists, then proceed with building.
- Otherwise: Wait for user to specify project.

**Facilitator Action**:
```
"Shaping complete! Transitioning to Building phase.

📋 PHASE CHANGE: Shaping → Building

The shaped solution is now locked. Any scope changes require
returning to Shaping phase with full triad.

💡 Reminder: Keep the team in the loop on progress throughout Building.
   Share updates in your team channel or standup.

Now I'll create the execution plan..."
```

**CRITICAL ACTION**: 
- **STOP immediately** - do not proceed with any other action.
- **IMMEDIATELY run `/plan`** with the shaping document (or reference to the shaping.md file).
- Wait for `/plan` to complete and create the plan.md file.
- Only after `/plan` has finished, continue with the plan review prompt.

```
"Plan created! Please review the plan with the team:

📋 PLAN REVIEW CHECKPOINT

The execution plan has been created at:
projects/<domain>/<project>/plan.md

Before breaking it down into tasks, review the plan together:

Discussion prompts:
[Select 2 most relevant prompts from "Plan Review Prompts" library]

Once the team has reviewed and approved the plan, let me know and I'll break it down into executable tasks."
```

**Action**: Select 2 prompts from the "Plan Review Prompts" library (either most relevant to the context or randomly). Surface only these 2 prompts. Then wait for user confirmation that the plan has been reviewed. After user confirms plan review is complete, continue with:

```
"Great! Now I'll break it down into executable tasks..."
```

**CRITICAL ACTION**: 
- **STOP immediately** - do not proceed with any other action.
- **IMMEDIATELY run `/breakdown`** with the plan document (or reference to the plan.md file).
- Wait for `/breakdown` to complete and create the task files.
- Only after `/breakdown` has finished, continue with the next steps.

```
"Tasks created! You can now:
  1. Review the tasks in projects/<domain>/<project>/tasks/
  2. Run /implement @tasks/<task-file> to execute individual tasks
  3. Run /hillchart to track progress
"
```

### During Building Phase

**Facilitator Action** (when checking status):
```
"Checking project status..."
```

**CRITICAL ACTION**: 
- **STOP immediately** - do not proceed with any other action.
- **IMMEDIATELY run `/hillchart`** with the project name/domain to get current progress.
- Wait for `/hillchart` to complete and show its output.
- Only after `/hillchart` has finished, display the results:

```
"📊 Project: [project-name]
 Phase: Building

 Progress:
   ✅ Framing Gate passed
   ✅ Shaping Gate passed  
   ✅ Plan complete
   🔄 Implementation in progress (Task X of Y)
   
 Hill Position: [percentage]% ([uphill/downhill status])
 [Include hill chart output from /hillchart command]
 
 💡 Reminder: Keep the team in the loop on progress.
    Share updates in your team channel or standup.
    
 ⏸️ Half-time reflection: [status]
    [If approaching midpoint: "Coming up after Task X"]
    [If at midpoint: "Time to assess scope and timeline"]
    [If past midpoint: "Completed at Task X"]
```

### Half-Time Scoping Reflection (Automatic Trigger)

**When**: Automatically triggered when ~50% of tasks are complete (or at midpoint milestone)

**Facilitator Action**:
```
"⏸️ HALF-TIME SCOPING REFLECTION

You're midway through the cycle. This is a mandatory pause point.

Time to assess:
• Are you on track to hit the appetite?
• What scope should be cut to ensure delivery?
• Are there any concerns to raise with the team?

Discussion prompts:
[Select 2 most relevant prompts from the following, or create 2 context-specific prompts]:
• What's taking longer than expected?
• What can we cut without breaking the core solution?
• Are we still aligned with the shaped solution?
• What would we do differently if starting over?

This is the moment to aggressively cut scope if needed.

Share your assessment with the team before continuing."
```

**Implementation note**: Calculate midpoint based on:
- Total number of tasks in breakdown (if available)
- Or milestone count (if using milestones)
- Or time elapsed (if tracking cycle duration)

### Approaching Delivery Gate

**Facilitator Action** (when implementation is ~90% complete):
```
"📦 Approaching Delivery

You're nearing completion. Before shipping:

🎨 FOR THE DESIGNER: Final Design Review with Paul

For projects with UI and UX implications, review the implemented design 
with @Paul Hershey for design QA as part of the build period. Design QA 
and remediation is included in the build appetite.

This review should happen before the Delivery Gate to ensure design 
quality before final stakeholder review.

⛳ DELIVERY GATE CHECK
   Leaders will review and approve the project output before
   delivery to customers.
   
   [ ] Delivery Gate scheduled
   [ ] Ready for final review
   
💡 Reminder: Keep the shaping team informed of delivery readiness.
```

## Status Command Details

When user runs `/shapeup status`:

1. **If project not specified**:
   ```
   "To check status, I need to know which project you're working on.
   
   Please specify:
   - The project name/path (e.g., 'payments/bank-deposit-reconciliation')
   - Or say 'list projects' to see available projects"
   ```
   
   **Action**: 
   - If user says "list projects": Scan `projects/` directory, list all projects found, and ask user to select one.
   - If user provides project path: Verify it exists, then proceed with status check.
   - Otherwise: Wait for user to specify project.

2. **Detect project state**:
   - Check for `projects/<domain>/<project>/pitch.md` (Framing stage)
   - Check for `projects/<domain>/<project>/shaping.md` (Shaping stage)
   - Check for `projects/<domain>/<project>/plan.md` (Planning stage)
   - Check for `projects/<domain>/<project>/tasks/` (Breakdown/Implementation stage)
   - Check task completion status (for half-time trigger)

2. **Show current phase and gate status**:
   - Framing Gate: Passed / Pending / Not started
   - Shaping Gate: Passed / Pending / Not started
   - Delivery Gate: Passed / Pending / Not started
   - Half-time: Completed / Upcoming / Not applicable

3. **Show progress indicators**:
   - Artifacts created (pitch, shaping, plan, tasks)
   - Task completion status
   - **CRITICAL ACTION**: If in Building phase and tasks exist:
     - **STOP immediately** - do not proceed with any other action.
     - **IMMEDIATELY run `/hillchart`** with the project name/domain to get current hill position.
     - Wait for `/hillchart` to complete.
     - Display the hill chart results in the status output.

4. **Provide next action suggestions**:
   - Based on current phase
   - Based on gate status
   - Based on missing artifacts

## Default Command Behavior

When user runs `/shapeup` without subcommand:

1. **If project not specified by user**:
   ```
   "Welcome to ShapeUp! To get started, I need to know which project you're working on.
   
   📋 Which project would you like to work on?
   
   Option 1: Existing project
   - I'll scan the projects/ directory and list available projects
   - You can select from the list or provide the project path
   
   Option 2: Brand new project
   - Confirm it's a new project
   - I'll guide you through /shapeup start
   
   Please specify:
   - The project name/path (e.g., 'payments/bank-deposit-reconciliation')
   - Or say 'new project' if this is brand new
   - Or say 'list projects' to see available projects"
   ```
   
   **Action**: 
   - If user says "list projects" or "show projects": Scan `projects/` directory, list all projects found (format: `projects/<domain>/<project>/`), and ask user to select one.
   - If user provides project path: Verify it exists, then proceed.
   - If user says "new project": Guide to `/shapeup start`.
   - Otherwise: Wait for user to specify project or confirm it's new.

2. **If project specified but not detected in filesystem**:
   ```
   "I don't see a project at that path. Is this a brand new project?
   
   [ ] Yes, new project — I'll guide you through /shapeup start
   [ ] No, existing project — please check the path or provide the correct project location"
   ```

3. **If project detected**: 
   - Detect current phase and artifacts
   - **CRITICAL ACTION**: If in Building phase with tasks:
     - **STOP immediately** - do not proceed with any other action.
     - **IMMEDIATELY run `/hillchart`** with the project name/domain.
     - Wait for `/hillchart` to complete.
     - Show current status with hill chart results and suggest next action
4. **If at gate checkpoint**: Prompt for gate status
5. **If at half-time**: Trigger half-time reflection

## Discussion Prompts Library

**IMPORTANT**: When surfacing discussion prompts, **select only 2 prompts** (either the most relevant 2 or randomly select 2) from the library below. Do not overwhelm the triad with all questions at once.

### Problem Alignment Prompts
- Is this the most important problem to solve right now?
- How does this problem manifest in the current user experience?
- Are there obvious risks or unknowns?
- What's the cost of NOT solving this?
- Who feels the pain most acutely?
- What evidence do we have that this is a real problem?

### First Instinct Solutions Prompts
- What's the simplest thing that would solve this for users?
- How might users interact with a solution? (Places, actions, visual cues)
- What's the most straightforward technical approach?
- What existing patterns could we leverage?
- What would a minimal viable solution look like?
- How does this fit with our current architecture?

### Breadboard Review Prompts
- Does this capture the key user touchpoints?
- Are these places technically feasible within the appetite?
- What UX edge cases should we consider?
- What existing patterns can we leverage?
- Does this match user expectations?
- Are there missing connections between places?

### Rabbit Holes (Risks) Prompts
- What technical unknowns could blow up the timeline?
- What UX edge cases need attention?
- What business/compliance risks exist?
- What's the riskiest unknown that needs de-risking?
- What would make this blow up the appetite?
- Are there dependencies we haven't accounted for?

### No-Gos (Boundaries) Prompts
- What's explicitly out of scope to protect appetite?
- What polish can we defer?
- What integrations are we NOT doing?
- What features are explicitly cut?
- What "nice-to-haves" should we avoid?
- What can wait for a future cycle?

### Plan Review Prompts
- Does the technical approach align with the shaped solution?
- Are the milestones realistic within the appetite?
- Are there any concerns about the rollout or feature flag plan?
- Does the testing strategy cover the key risks?
- Are there any missing pieces or unclear areas?
- Will this deliver the core value within the appetite?

## Key Principles

1. **Prompts are discussion starters, not role assignments**: All prompts are for the whole triad to discuss together. Different perspectives naturally emerge.

2. **Surface only 2 prompts at a time**: Select the 2 most relevant prompts from the library above, or randomly select 2. This prevents overwhelming the triad and keeps discussions focused.

3. **Gates are reminders, not blockers**: Prompt and remind about gates, but don't hard-block progress. Trust the team to follow the process.

4. **Half-time is automatic**: Calculate midpoint and trigger reflection automatically, don't wait for user to request it.

5. **Phase 2 is simple**: Don't track individual role status. Just remind to "keep the shaping team in the loop."

6. **No handoffs**: All 3 roles collaborate during Shaping. During Building, team stays informed but no explicit handoff checklists.

7. **Selective prompt surfacing**: Surface only 2 prompts at a time from the prompts library (either most relevant or randomly selected) to avoid overwhelming the triad. The full library is available for reference, but only show 2 prompts per discussion point.

## Integration with Other Commands

The facilitator **actually runs** these commands at the appropriate phases. **For each command, follow this pattern**:
1. **STOP immediately** - do not proceed with any other action
2. **IMMEDIATELY run** the required command
3. **Wait for completion** - let the command finish and show its output
4. **Only then proceed** to the next step

Commands to run:
- **/frame-coach**: **STOP and run immediately** when user provides problem statement (external pitch or described problem) in Framing stage. DO NOT create pitch files or proceed without running this first.
- **/shape**: **STOP and run immediately** when transitioning to Shaping stage (after Framing Gate passed). Wait for shaping.md to be created before proceeding.
- **/plan**: **STOP and run immediately** when entering Building phase (after Shaping Gate passed). Wait for plan.md to be created before proceeding.
- **/breakdown**: **STOP and run immediately** after plan review is complete. Wait for task files to be created before proceeding.
- **/hillchart**: **STOP and run immediately** when checking status in Building phase (if tasks exist). Wait for hill chart output before displaying results.
- **/implement**: Guide user to run for individual tasks (user-driven, not automatic)

**Critical**: The facilitator must execute these commands, not just suggest them. The commands do the actual work of creating artifacts (shaping.md, plan.md, tasks/, etc.). The facilitator provides context, prompts discussion, and orchestrates the workflow by running the right command at the right time. **Never skip running a required command or proceed before it completes.**
