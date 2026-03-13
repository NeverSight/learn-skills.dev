---
name: beads-create
description: File Beads epics/issues from a finalized plan/spec AND do the polish pass (clarity, acceptance criteria, sizing, deps). Use when asked to create Beads from a plan/spec (OpenSpec, PRD, design doc), convert an external plan into Beads structure, or review/refine an existing Beads set.
---

# Beads Create

Use this skill to create Beads from a plan/spec and do the review pass so implementers can just pick up issues and ship.

## Workflow

1. **Load beads guidance if needed**
   - If bd CLI usage or bead structure is unclear, consult the official Beads GitHub repo at `https://github.com/steveyegge/beads` and follow the documented workflow for your installed `bd` version.

2. **Decide which mode you are in**
   - If the user has a finalized plan/spec and wants Beads filed: do Create mode.
   - If the user already has Beads and wants them improved: do Review mode (skip straight to step 5).

3. **Confirm the plan is ready (Create mode)**
   - Ensure there is a finalized plan or spec outside Beads.
   - If the plan is still fuzzy, ask for revisions first and iterate up to 5 times before importing.

4. **Translate the plan into Beads structure (Create mode)**
   - Create epics that map to major milestones or deliverables.
   - Create issues for concrete, implementable tasks.
   - **Hierarchy rule**: When an epic has child milestones/tasks, create them as
     hierarchical children (dotted IDs like `EPIC.1`, `EPIC.2`) rather than
     separate top-level issues with only parent-child deps. Follow the bd CLI
     “Create epic with hierarchical child tasks” flow (create the epic, then
     create children so bd auto-assigns `EPIC.N` IDs). Verify the returned IDs;
     if bd doesn’t assign dotted IDs, stop and ask the user how to proceed.
   - Add dependencies, ordering constraints, and opportunities for parallel work.

5. **Review and polish (Create mode + Review mode)**
   - Fix vague titles, missing acceptance criteria, or unclear scope.
   - Ensure each issue is something one agent can do in a single task.
   - Verify dependencies, sequencing, and opportunities for parallel work.
   - Add missing design notes / decision context.
   - Split oversized issues; merge duplicates; delete fluff.

6. **Add implementation detail**
   - Include design notes, assumptions, and acceptance criteria on each issue.
   - Make tasks small and unambiguous so a fresh agent can pick up a single issue.

7. **Single-pass**
   - Do one focused pass in the current context.
   - If another pass is needed, say so explicitly and recommend a separate follow-up run.

8. **Restart the agent**
   - Finish this task, then stop. Encourage a fresh agent for the next task to keep sessions small.

## Output expectations

- Provide a concise mapping of epics and issues you created.
- Call out any dependencies or blockers that need user confirmation.
- If asked to iterate beyond 5 plan revisions, say you do not think it can be improved further.
