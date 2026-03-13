---
name: deep-plan
description: Takes a rough, unpolished prompt idea and autonomously turns it into an implementation plan. Researches the project deeply, asks clarifying questions, generates a precise internal prompt, then executes it to produce a structured plan with todos. Designed for plan mode. Use when the user gives a vague feature request, rough idea, or "dirty" prompt and wants a ready-to-execute implementation plan — e.g. "plan this", "deep plan", "turn this into a plan", "zaplanuj to", "zrób plan".
metadata:
  author: b4r7x
  version: "1.0.0"
  argument-hint: <rough-idea>
---

# Deep Plan

Takes a rough idea and autonomously produces an implementation plan — researching, clarifying, and executing without manual prompt refinement.

## Workflow

Execute all five phases in strict order. Do not skip phases. Do not show intermediate artifacts to the user unless asked.

### Phase 1 — Decompose the Dirty Prompt

Parse the user's rough input. Produce an internal working list:

1. **Task type**: implement / refactor / debug / add feature / migrate / integrate / remove
2. **Scope estimate**: single file / multi-file / cross-package / architectural
3. **Ambiguities**: list every unclear aspect (behavior, boundaries, edge cases, naming, approach)
4. **Deep-dive targets**: list specific files, modules, or patterns that need reading before planning

Do not output this list to the user. It drives the next phases internally.

### Phase 2 — Deep Research

#### 2a. Project context (always run)

Follow `references/project-research-playbook.md` — run the minimum required research:

```bash
cat README.md 2>/dev/null | head -80
cat CLAUDE.md 2>/dev/null | head -60
cat AGENTS.md 2>/dev/null | head -60
cat .github/copilot-instructions.md 2>/dev/null | head -40
cat .cursorrules 2>/dev/null | head -40
cat package.json 2>/dev/null | head -40
find . -maxdepth 2 -type d | grep -v node_modules | grep -v .git | head -25
git log --oneline -8 2>/dev/null
```

#### 2b. Task-specific deep dives

For each deep-dive target from Phase 1:
- Read the relevant source files (use `view`, `grep`, `glob`)
- Understand existing patterns, interfaces, and conventions in those areas
- Map dependencies — what does the target file import/export? What depends on it?
- Note any existing tests for affected code

Build an internal understanding of **current state** vs **desired state**.

### Phase 3 — Ask Clarifying Questions

Review the ambiguities list from Phase 1, filtered by what Phase 2 answered.

For each remaining ambiguity:
- Ask the user **one question at a time** using the `ask_user` tool
- Prefer **multiple-choice** questions (provide a `choices` array) — faster for the user
- Put the recommended option first with `(Recommended)` suffix
- Ask a maximum of 5 questions — if more remain, make reasonable inferences and state them in the plan

**Skip this phase entirely** if Phase 2 resolved all ambiguities.

Question quality guidelines:
- Ask about **behavior and scope**, not implementation details you can decide yourself
- Bad: "Should I use a for loop or map?" — decide this yourself
- Good: "Should the search be case-sensitive or case-insensitive?"
- Good: "Should this feature support batch operations or single-item only?"

### Phase 4 — Generate Internal Prompt

Using everything gathered in Phases 1–3, generate a structured prompt following `references/ai-coding-prompt-guide.md`.

**This prompt is internal — do NOT show it to the user.**

The prompt must target: **"Create a detailed implementation plan"** as its task.

Required fields:
- **Role**: matching the project's actual stack
- **Context**: framework, key libraries, relevant file paths (exact paths from Phase 2)
- **Task**: "Create an implementation plan for [specific feature/change]"
- **Constraints**: project conventions, what not to change, patterns to follow
- **Output format**: structured plan with approach, file changes, and actionable todos
- **Acceptance criteria**: what must be true when the plan is fully implemented
- **References**: exact file paths discovered in Phase 2

For complex multi-file tasks, use the XML format variant from the guide.

### Phase 5 — Execute and Produce Plan

Now execute the prompt you generated in Phase 4. Produce a structured implementation plan.

**The plan must include:**

1. **Problem statement** — one paragraph summarizing what needs to happen and why
2. **Approach** — high-level strategy (2-4 sentences)
3. **File changes** — for each file to create/modify:
   - File path
   - What changes and why
   - Key implementation details (not full code, but enough to execute without guessing)
4. **Todos** — ordered list of actionable tasks with clear descriptions
5. **Considerations** — edge cases, risks, things to verify after implementation

**If operating in plan mode** (the primary use case):
- Save the plan to `plan.md` in the session workspace
- Populate the SQL `todos` table with actionable items (descriptive kebab-case IDs, full descriptions)
- Set up `todo_deps` for any ordering constraints
- Call `exit_plan_mode` to present the plan for user approval

**If NOT in plan mode:**
- Output the plan directly in the response
- Still offer to populate todos if the user wants to track implementation

## Example

**User input:** "add dark mode"

**Phase 1 (internal):**
- Task: add feature
- Scope: multi-file (theme, components, storage)
- Ambiguities: toggle location? persist preference? system preference detection? which components?
- Deep-dive targets: existing theme/styling files, layout component, any CSS variables

**Phase 2:** Discovers Tailwind + CSS variables in `globals.css`, React context in `src/providers/`, localStorage usage in `src/lib/storage.ts`, 23 components using hardcoded colors.

**Phase 3 (asks user):**
- "Where should the dark mode toggle live?" → choices: ["Header nav bar (Recommended)", "Settings page", "Both"]
- "Should it detect system preference on first visit?" → choices: ["Yes (Recommended)", "No, default to light"]

**Phase 4 (internal prompt generated, not shown)**

**Phase 5 (plan output):**
```
## Problem
The app has no dark mode support. Users need a toggle in the header
that persists preference and respects system settings on first visit.

## Approach
Add a ThemeProvider using React context + CSS variables. Persist to
localStorage. Detect system preference via prefers-color-scheme media query.

## File Changes
- `src/providers/theme-provider.tsx` — new file, React context with light/dark/system
- `src/globals.css` — add CSS variables for dark palette under .dark class
- `src/components/header.tsx` — add toggle button
- `src/lib/storage.ts` — add theme preference getter/setter
...

## Todos
1. create-theme-provider — Create ThemeProvider with context, localStorage sync, system detection
2. add-css-variables — Define dark palette CSS variables in globals.css
3. add-toggle-ui — Add dark mode toggle to header
4. update-storage — Add theme preference to storage helpers
5. audit-components — Check 23 components for hardcoded colors, switch to CSS variables
```
