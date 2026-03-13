---
name: brainstorming
description: >-
  Facilitates collaborative design exploration before implementation.
  Explores user intent, constraints, and requirements through structured
  dialogue, then produces an approved design document. Must be invoked
  when entering plan mode or planning any implementation. Triggers:
  brainstorm, design, plan, "let's think through," "how should we build."
---

<HARD-GATE>
Do NOT write any code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it. This applies to EVERY project regardless of perceived simplicity.
</HARD-GATE>

## Anti-Pattern: "Too Simple for a Design"

Every project goes through this process — a todo list, a single-function utility, a config change. "Simple" projects are where unexamined assumptions cause the most wasted work. The design can be a few sentences, but it must be presented and approved.

## Process

Complete these steps in order, creating a task for each:

### 1. Explore project context

Check files, docs, and recent commits to understand the current state.

### 2. Ask clarifying questions

- One question per message — if a topic needs more exploration, break it up
- Prefer multiple-choice questions; open-ended is fine when choices aren't obvious
- Focus on purpose, constraints, and success criteria

### 3. Propose 2–3 approaches

- Lead with your recommendation and explain why
- Include trade-offs for each approach
- Apply YAGNI ruthlessly — remove unnecessary features from all options

### 4. Present design incrementally

- Scale each section to its complexity (a sentence if simple, a few paragraphs if nuanced)
- Cover: architecture, components, data flow, error handling, testing
- Ask after each section whether it looks right — revise until approved
- Go back and clarify if something doesn't make sense

### 5. Write design doc

Save the approved design to `~/.agents/brainstorming/<project-name>/YYYY-MM-DD-<topic>.md` and give the path to the user. Plan mode continues with implementation planning.
