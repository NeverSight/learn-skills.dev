---
name: brainstorm
description: Facilitate structured idea exploration and product/design specification. Use when a user wants to talk through an idea, refine it via iterative questions, and converge on a clear design/spec (and later an implementation plan), especially after inspecting the current project state.
---

# Brainstorm

Use this skill to guide a user from a rough idea to a clear design/spec by asking targeted questions, one at a time, after first inspecting the project state.

## Workflow

1. **Scan the project context**
   - Review the working directory to understand the current state, constraints, and any existing docs or code.
   - Summarize what you saw in 2-4 sentences only if it helps frame the next question.

2. **Ask refining questions (one per message)**
   - Ask exactly one question per response.
   - Prefer multiple-choice questions with 3-5 options; include an "Other: ____" option when helpful.
   - For multiple-choice questions, mark exactly one option as recommended so the user has a clear default.
   - In Codex `request_user_input`, mark the recommended choice by suffixing the label with `(Recommended)`. In Claude `AskUserQuestion`, use an explicit `recommended` flag when available or clearly label one option as recommended.
   - Use open-ended questions only when options would be misleading.
   - Sequence questions from highest-uncertainty to lowest-uncertainty.
   - Do not ask questions that can be trivially answered by inspecting the repo or using available tools; look it up first.
   - Keep each question tightly scoped and decision-oriented.
   - For Claude, ask questions via AskUserQuestion.

3. **Converge on understanding**
   - Once the idea is clear enough to describe a design/spec, stop asking questions.
   - Explicitly indicate you are switching from questions to describing the design.

4. **Describe the design in sections**
   - Provide the design/spec in sections of ~200-300 words each.
   - After each section, ask whether it looks right so far before continuing.
   - Incorporate feedback and revise the next section accordingly.

5. **Beads + planning handoff**
   - After the final spec section is approved, summarize the spec into bead fields: title, description, design, acceptance.
   - Ask one multiple-choice question covering the next step (beads and/or plan), and mark one option as recommended. Example choices: create a single bead, create an epic + milestones, proceed to plan only, or pause.
   - If beads are requested and granularity is unclear, ask a single follow-up question to choose between a single bead vs an epic with milestone beads.
   - Decision rule for granularity:
     - Single bead: 1-3 sessions, cohesive flow, minimal handoffs.
     - Epic + milestones: longer work or clear checkpoints, even if sequential. Use linear dependencies if steps must be done in order.
   - If a plan is requested, provide a concise spec recap (goals, non-goals, UX, data/logic, constraints, acceptance) to seed the plan.
   - If a plan is created later, link it in the bead design field.

## Style rules

- Ask only one question per message.
- Keep momentum: no long preambles or multi-paragraph lead-ins.
- Use concrete language and avoid filler.
- Do not announce the skill or preface with meta statements like "Using the brainstorm skill because...".
- When asking about beads/plan, use a single multiple-choice question; only follow up if bead granularity needs a choice.
- For each multiple-choice question, ensure exactly one option is explicitly marked as recommended.
