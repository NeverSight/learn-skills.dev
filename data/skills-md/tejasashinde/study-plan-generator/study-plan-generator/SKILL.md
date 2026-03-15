---
name: study-plan-generator
description: "Use when user asks to 'create study plan', 'make a learning roadmap', 'edit my study plan', 'modify existing study plan', or similar. Generates structured, goal-oriented study plans for any subject over a specified time period and allows iterative editing of previously generated files."
---

# Study Plan Generator

## Purpose

Creates structured, realistic, and actionable study plans based on:
- A defined time period
- A clearly specified subject

Supports:
- First-time generation
- Editing an existing generated file on subsequent runs

---

# Operational Modes

The skill operates in TWO modes:

1. Generation Mode (first run)
2. Edit Mode (subsequent runs)

Claude must determine mode based on user intent.

---

# Mode Detection

## Generation Mode (Default)

Trigger when user says:
- "Create a study plan"
- "Make a learning roadmap"
- "Plan my studies"
- "Learn X in Y weeks"

If no existing file is referenced, proceed with full generation workflow.

---

## Edit Mode (Second Run / Refinement Mode)

Trigger when user says:
- "Edit the study plan"
- "Modify the file"
- "Update week 3"
- "Make it more intense"
- "Change timeline to 6 weeks"
- "Adjust daily hours"
- "Revise the generated plan"

When this happens:

1. Ask for the existing file (if not already in context).
2. Load the previously generated study plan.
3. Identify requested changes.
4. Modify only affected sections.
5. Preserve structure and formatting.
6. Save updated version properly.

Do NOT regenerate from scratch unless explicitly requested.

---

# Generation Workflow

## Step 1: Collect Required Inputs (MANDATORY)

Before generating the study plan, confirm:

1. Time Period  
2. Subject Specificity  

If vague or missing:
- Ask clarifying questions
- Do NOT generate generic plan

---

## Step 2: Clarify Constraints (Optional)

Ask about:
- Hours per day
- Exam prep vs mastery
- Experience level

If none provided:
- Assume 1–2 hours/day
- 5–6 days/week

---

## Step 3: Design the Study Plan

Required structure:

1. Overview
2. High-Level Roadmap
3. Weekly Breakdown
4. Daily Study Template
5. Milestones
6. Final Capstone

---

## Step 4: Save File (Generation Mode)

Save as:

`{subject}-{time-period}-study-plan.docx`

Example:
`introductory-spanish-4-weeks-study-plan.docx`

Confirm to user:
"Your study plan has been saved as [filename]."

---

# Edit Mode Workflow (Second Run)

When user wants to modify:

## Step 1: Identify Change Scope

Determine whether change affects:
- Entire plan (timeline change)
- Specific week
- Daily workload
- Milestones
- Difficulty level
- Format/style only

Ask clarifying questions if ambiguous.

---

## Step 2: Apply Targeted Edits

Rules:

- Preserve unaffected weeks
- Maintain logical progression
- Adjust dependencies (if timeline changes, rebalance all weeks)
- Update milestones if pacing changes

Examples:

If timeline increases:
- Redistribute content evenly
- Add enrichment tasks

If intensity increases:
- Increase practice volume
- Add extra exercises

If subject changes:
- Regenerate fully (ask confirmation)

---

## Step 3: Save Updated Version

Overwrite or version intelligently:

Option A (default):
Overwrite existing file.

Option B (recommended best practice):
Save versioned file:

`{subject}-{time-period}-study-plan-v2.docx`
`-v3.docx`, etc.

Confirm:
"Updated version saved as [filename]."

---

# Editing Constraints

Do NOT:
- Remove structure
- Collapse weekly breakdown
- Delete milestones unless requested
- Downgrade quality

Ensure edited file still satisfies:

- Clear segmentation
- Weekly breakdown
- Practical tasks
- Logical progression

---

# Example Interaction (Edit Mode)

User:
"Make week 2 more intense."

Assistant:
1. Loads existing file.
2. Modifies week 2.
3. Ensures pacing alignment.
4. Saves new version.
5. Confirms update.

---

User:
"Change it from 4 weeks to 6 weeks."

Assistant:
1. Recalculate distribution.
2. Expand roadmap.
3. Adjust milestones.
4. Save versioned update.

---

# Edge Case Handling

If user edits without file context:
Ask:
"Please upload or paste the previously generated study plan so I can modify it."

If user requests full redesign:
Confirm:
"Would you like me to regenerate from scratch?"

---

# Completion Criteria

For Generation:
- Structured plan
- Saved file

For Edit Mode:
- Correct sections modified
- Logical consistency preserved
- Version saved properly
- No structural degradation

---

# Performance Notes

- Use iterative refinement logic.
- Modify surgically, not destructively.
- Maintain educational quality.
- Always confirm file save action.