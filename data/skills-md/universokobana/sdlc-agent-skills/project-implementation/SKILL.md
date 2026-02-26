---
name: project-implementation
description: Implement a project from its documentation and specification. Use when asked to "implement project", "continue implementation", "build from docs", "implement from spec", or when the user wants to progressively implement a documented project following a todo checklist. Reads project docs, creates implementation plans and todo lists, and implements incrementally with tests and commits.
---

# Project Implementation

## Overview

Implement a project that is documented and specified in a docs folder. Work through a structured todo list, implementing ALL phases and sections in a single continuous session, running tests, committing, and updating progress tracking files after each step.

### Docs Folder Resolution

The docs folder is determined as follows:
1. **If the user specifies a folder path in their prompt** → use that path as the docs folder (e.g., `specs/`, `project/docs/`, `my-feature/`)
2. **If NO folder is specified** → default to `./docs/`

All tracking and planning files (`implementation.md`, `todo.md`, `implemented.md`, `questions.md`) are read from and written to this docs folder.

> **Example:** If the user says "implement project from specs/my-app/", then all files are at `specs/my-app/implementation.md`, `specs/my-app/todo.md`, etc.

In the instructions below, `<docs-folder>` refers to the resolved docs folder path.

**Core principles:**

- **NEVER stop between phases.** Implement ALL phases from start to finish in one continuous session. Do NOT pause after completing a phase to ask if you should continue — just continue.
- **NEVER ask the user questions.** If you encounter ambiguity, uncertainty, or need to make a decision, make your best judgment based on the documentation and record the question/decision in `<docs-folder>/questions.md` for later review. NEVER use AskUserQuestion or stop to ask for input.
- **Never skip tests.** Never mark a task as done without verified implementation. Always commit after each completed section. Always update tracking files before moving to the next task.

### Questions Protocol

When you encounter a question, ambiguity, or need to make a judgment call:

1. **DO NOT stop or ask the user** — make the best decision you can based on available documentation
2. **Record it in `<docs-folder>/questions.md`** with the following format:

   ```markdown
   ## [Phase X — Section Name]

   **Q:** What is the expected behavior when X happens?
   **Decision:** I chose to do Y because Z.
   **Impact:** Low/Medium/High — affects [description].
   ```

3. **Continue implementing** — the user will review `<docs-folder>/questions.md` after all development is complete

## The Process

### Phase 1: Read Project Documentation

1. **Read all files in `<docs-folder>/`**

   ```bash
   find <docs-folder>/ -type f -name '*.md' | sort
   ```

   Read every documentation file to understand the full project scope, architecture, and requirements.

2. **Read `<docs-folder>/implementation.md`** (Implementation Plan)

   - If it **exists** → read it carefully to understand the phases, order of execution, and dependencies
   - If it **does NOT exist** → create it from the specification files in `<docs-folder>/`:
     - Analyze all spec documents
     - Break the project into logical implementation phases (Phase 0: Setup, Phase 1: Core, Phase 2: Features, etc.)
     - Each phase should have clear deliverables and acceptance criteria
     - Write the plan to `<docs-folder>/implementation.md`

3. **Read `<docs-folder>/todo.md`** (Task Checklist)

   - If it **exists** → read it to understand what needs to be done
   - If it **does NOT exist** → create it from `<docs-folder>/implementation.md`:
     - Convert each phase into a section with checkbox items
     - Each item should be a single, atomic, implementable task
     - Use the format `- [ ]` for pending and `- [x]` for completed
     - Group by phase, with clear section headers
     - Example structure:

       ```markdown
       # Project Name — TODO

       ---

       ## Phase 0 — Setup

       ### Initialization
       - [ ] Create `package.json`
       - [ ] Create `tsconfig.json`
       - [ ] Create `.gitignore`

       ### Build
       - [ ] Install dev dependencies
       - [ ] Create build config
       - [ ] Validate `npm run build` works
       - [ ] Validate `npm run test` works

       ### Directory Structure
       - [ ] Create `src/` directories
       - [ ] Create `__tests__/` directories

       ---

       ## Phase 1 — Core Feature

       ### Sub-feature A
       - [ ] Implement X
       - [ ] Implement Y
       - [ ] Write tests for X and Y
       ```

4. **Read `<docs-folder>/implemented.md`** (Implementation Log)

   - If it **exists** → read it to understand what was already done and where to resume
   - If it **does NOT exist** → create it with this initial content:

     ```markdown
     # Implementation Log

     > Auto-updated after each implementation cycle.

     ---
     ```

### Phase 2: Determine Where to Resume

1. Compare `<docs-folder>/todo.md` with `<docs-folder>/implemented.md`
2. Find the **first unchecked item** (`- [ ]`) in `todo.md`
3. That is the starting point for this session

### Phase 3: Implementation Loop

For **each unchecked section/group** in `todo.md`, repeat:

#### 3a. Implement

- Read the task description
- Implement the minimum required to complete all items in the current section/group
- Follow project conventions found in the documentation
- Stay focused on the scope — no "while I'm here" changes

#### 3b. Run Tests

```bash
# Run the project's test command (detect from package.json, Makefile, etc.)
npm run test
# or
bundle exec rspec
# or
pytest
# or whatever the project uses
```

- All tests MUST pass before proceeding
- If tests fail, fix them before moving on
- If the section introduces new behavior, write tests for it

#### 3c. Commit

```bash
git add <changed files>
git commit -m "feat: <description of what was implemented>

Co-Authored-By: Claude <noreply@anthropic.com>"
```

- One commit per completed section/group
- Use conventional commits: `feat:`, `fix:`, `chore:`, `refactor:`, `test:`
- Commit message in the project's language (follow existing commit style)

#### 3d. Update `<docs-folder>/todo.md`

Mark all completed items as done:

```markdown
- [x] Create `package.json`  ← was `- [ ]`
```

#### 3e. Update `<docs-folder>/implemented.md`

Append a summary of what was implemented:

```markdown
## Phase 0 — Setup > Initialization

- Created `package.json` with scope `@project/name`
- Created `tsconfig.json` targeting ES2022
- Created `.gitignore`

**Commit:** `abc1234`
```

#### 3f. Commit Tracking Updates and Continue

After updating tracking files:

1. **Commit the tracking file updates**:
   ```bash
   git add <docs-folder>/todo.md <docs-folder>/implemented.md <docs-folder>/questions.md
   git commit -m "docs: update implementation progress

   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

2. **Immediately continue to the next unchecked section** — do NOT stop, do NOT ask the user, do NOT restart the process. Loop back to step 3a with the next section.

**CRITICAL: Do NOT stop between phases.** The entire project must be implemented in a single continuous session. Move from one section to the next without interruption until ALL items in `todo.md` are checked.

### Phase 4: Completion

When all items in `todo.md` are checked (`- [x]`):

1. Run the full test suite one final time
2. Update `<docs-folder>/implemented.md` with a completion summary
3. If `<docs-folder>/questions.md` has entries, inform the user to review it
4. Inform the user that implementation is complete

## Quick Reference

| Step | Action | Success Criteria |
|------|--------|-----------------|
| 1. Read docs | Load all project documentation | Full understanding of scope |
| 2. Plan | Create/read implementation.md | Clear phased plan exists |
| 3. Todo | Create/read todo.md | Granular checklist exists |
| 4. Resume | Find first unchecked item | Know where to start |
| 5. Implement | Code the current section | All items in section done |
| 6. Test | Run tests | All tests pass |
| 7. Commit | Git commit the implementation | Clean commit history |
| 8. Track | Update todo.md + implemented.md | Progress recorded |
| 9. Continue | Loop to step 5 with next section | All phases completed |

## Red Flags — STOP and Reassess

- Implementing without reading ALL docs first
- Skipping test execution after implementation
- Marking tasks done without actually implementing them
- Making changes outside the scope of the current section
- Committing without running tests
- Not updating tracking files after each cycle
- **Stopping between phases to ask the user questions** — save questions to `<docs-folder>/questions.md` and continue
- **Pausing after a phase to ask "Shall I continue?"** — ALWAYS continue automatically
- Moving to the next section when tests are failing

**NEVER STOP. NEVER ASK. Follow the process until ALL phases are complete.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "This section is trivial, skip tests" | Every implementation needs test verification. |
| "I'll update todo.md at the end" | Update after EACH section, not after all. |
| "I'll do multiple sections before committing" | One commit per section keeps history clean. |
| "Tests aren't set up yet, skip them" | Setting up tests IS part of Phase 0. |
| "I remember what was done, skip reading docs" | Always re-read — context may have been cleared. |
| "The todo is too granular" | Granular tasks = clear progress + clean commits. |
| "Let me ask the user about this" | Save to `<docs-folder>/questions.md` and keep going. |
| "Phase X is done, let me check with the user" | NEVER stop — continue to the next phase immediately. |

## Notes

- **NEVER stop between phases** — implement ALL phases in one continuous session
- **NEVER ask the user questions** — save decisions and questions to `<docs-folder>/questions.md`
- **One section per commit** — keeps commits atomic and history clean
- **The todo.md is the source of truth** — if it's not checked, it's not done
- **The implemented.md is the audit log** — always record what was done and the commit hash
- **Detect the project's tech stack** from docs and existing files to use the correct test/build commands
- **The questions.md is for post-implementation review** — the user reads it after everything is done
