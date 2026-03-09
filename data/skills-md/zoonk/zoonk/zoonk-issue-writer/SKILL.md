---
name: zoonk-issue-writer
description: "Write detailed user stories from implementation plans and post to GitHub. Use after planning with zoonk-issue-planning. Acts as a product owner, providing context and acceptance criteria while leaving room for implementation decisions."
license: MIT
metadata:
  author: zoonk
  version: "1.0.0"
---

# Issue Writer Skill

Write detailed user stories from implementation plans and post them to GitHub.

## Role

This skill acts as a **product owner layer**. It takes structured issue breakdowns (from `zoonk-issue-planning`) and transforms them into well-written user stories that give engineers the context they need without dictating implementation.

## When to Use

- After exiting plan mode with an approved implementation plan
- After running `zoonk-issue-planning` to break down a plan into issues
- When the user asks to "write issues" or "create GitHub issues" from a plan

## Workflow

### Step 1: Review the Plan

Read the implementation plan and issue breakdown. Understand:

- The overall goal and why it matters
- How issues relate to each other (dependencies, epic structure)
- Key technical insights from the planning phase

### Step 2: Write User Stories

For each issue in the breakdown, write a user story using the template below. Focus on:

- **Why** this matters (context)
- **What** success looks like (acceptance criteria)
- Leave the **how** to the implementing engineer

### Step 3: Review with User

Present the written stories for approval before posting. Allow edits.

### Step 4: Post to GitHub

Use `zoonk-github-issues` skill to create the issues with proper types, labels, and dependencies.

## User Story Template

Use this adaptive template. Required sections appear in every issue. Optional sections appear when they add value.

```markdown
## Context

[1-3 sentences. Why does this matter? What problem or pain point does it solve?]

## Goal

[1-2 sentences. What this issue accomplishes when complete.]

## Scope

**Included:**

- [What's in scope]

**Not included:**

- [What's explicitly out of scope - handled elsewhere or deferred]

## Technical Notes

- [Relevant file or component]
- [Pattern to follow from codebase]
- [Key insight from planning phase]

## Acceptance Criteria

- [ ] [Testable outcome 1]
- [ ] [Testable outcome 2]
- [ ] [Testable outcome 3]
```

### Section Guidelines

| Section             | When to Include                     | When to Skip           |
| ------------------- | ----------------------------------- | ---------------------- |
| Context             | Always                              | Never                  |
| Goal                | Always                              | Never                  |
| Scope               | Larger issues, unclear boundaries   | Small, obvious scope   |
| Technical Notes     | Planning revealed specific insights | Generic implementation |
| Acceptance Criteria | Always                              | Never                  |

## Issue References in Specs

### During Spec Writing (Before GitHub Issues Exist)

When writing specs that will become GitHub issues later:

1. **Never use `#NUMBER` format in specs** - These aren't GitHub issues yet
2. **Reference other specs by file name** instead:
   - BAD: `See issue #18 for details`
   - GOOD: `See spec 18-get-org-courses.md for details`

3. **Never add relationship metadata** - GitHub handles these:
   - No "Blocked by: #X" lines (use GitHub API)
   - No "Parent: #X" lines (use sub-issue feature)
   - No sub-issue lists (GitHub shows these automatically)
   - No summary tables (GitHub UI displays this)

### After GitHub Issues Exist

Cross-references to **real GitHub issues** are fine when providing context:

- "Out of scope, handled by #1234"
- "See #1234 for the course endpoint this depends on"

**But verify the reference first** - never trust #NUMBER from specs. Check GitHub to confirm the issue exists and is the correct one.

## Writing Guidelines

### 1. Context Over Commands

Engineers need to understand _why_ before _how_. Good context enables better decisions.

```markdown
// BAD
Add a button to the header.

// GOOD
Users currently can't access settings without navigating through three menus.
Adding a settings shortcut reduces friction for power users.
```

### 2. Specific But Not Prescriptive

Mention files and patterns when they help. Don't dictate implementation details.

```markdown
// BAD
In `src/components/Header.tsx`, add a `<Button variant="ghost">`
on line 47 after the logo div.

// GOOD
The header component (`src/components/Header.tsx`) is the right place.
Follow the existing icon button pattern used for the notification bell.
```

### 3. Clear Scope Boundaries

Prevent scope creep by stating what's out of scope. Reference where it's handled.

```markdown
## Scope

**Included:**

- Settings button in header
- Navigate to existing settings page

**Not included:**

- Redesigning settings page (tracked in #234)
- Mobile navigation changes (separate issue)
```

### 4. Testable Acceptance Criteria

Each checkbox should be verifiable. Avoid vague criteria.

```markdown
// BAD

- [ ] Works correctly
- [ ] Good UX

// GOOD

- [ ] Settings icon visible in header on desktop viewports
- [ ] Clicking icon navigates to /settings
- [ ] Icon has hover state matching other header icons
```

### 5. Concise Writing

Engineers skim. Use bullets, short sentences, no walls of text.

## Examples

### Good User Story

```markdown
## Context

Course creators currently can't reorder chapters after creation. They must delete
and recreate chapters in the desired order, losing all lesson content.

## Goal

Enable drag-and-drop reordering of chapters within the course editor.

## Scope

**Included:**

- Drag-and-drop UI for chapter list
- Persist new order to database
- Optimistic UI updates

**Not included:**

- Reordering lessons within chapters (separate issue #456)
- Keyboard-only reordering (accessibility follow-up)

## Technical Notes

- Chapter list is in `apps/editor/src/components/course/ChapterList.tsx`
- Use `@dnd-kit` (already in dependencies) - see `LessonList` for pattern
- Order is stored in `chapter.position` field

## Acceptance Criteria

- [ ] Chapters can be reordered via drag-and-drop
- [ ] New order persists after page refresh
- [ ] Dragging shows visual feedback (lifted card, drop indicator)
- [ ] Order updates optimistically (no loading state)
```

### Bad User Story

```markdown
## Description

We need to add drag and drop to chapters. Use dnd-kit. The component is in
ChapterList.tsx. Add a DndContext wrapper, then make each chapter a draggable
item with useDraggable hook. On drag end, call the updateChapterOrder mutation.
Make sure to add a loading spinner while saving. Also we should probably add
keyboard support but that can come later. Test it works.

## Tasks

- [ ] Add DndContext
- [ ] Add useDraggable to chapters
- [ ] Call mutation on drag end
- [ ] Add loading state
```

**Why it's bad:**

- Dictates implementation (hooks to use, exact code structure)
- No context on why this matters
- Vague acceptance criteria ("test it works")
- Mixes scope (mentions keyboard support "later")
- Tasks instead of outcomes

### Epic Example

For epics, provide higher-level context and link to sub-issues:

```markdown
## Context

Our current authentication only supports email/password. Users have requested
social login options, and analytics show 40% abandonment at signup. Social auth
reduces friction and increases conversion.

## Goal

Add Google and GitHub OAuth as login options alongside existing email/password.

## Sub-Issues

- #101 - Google OAuth integration
- #102 - GitHub OAuth integration
- #103 - Account linking (connect social to existing account)
- #104 - Auth provider UI in login/signup forms

## Acceptance Criteria

- [ ] Users can sign up/login with Google
- [ ] Users can sign up/login with GitHub
- [ ] Existing users can link social accounts
- [ ] Auth flow works on mobile browsers
```

## Advanced Patterns

### Writing Specs to Files (Pre-Review Workflow)

For large projects, write specs to files for review before creating GitHub issues:

**Directory structure:**

```
/tasks/specs/
├── PATTERNS.md                    # Shared patterns for similar issues
├── epic-name/
│   ├── 01-first-issue.md
│   ├── 02-second-issue.md
│   └── 03-third-issue.md
└── another-epic/
    └── ...
```

**Benefits:**

- Enables batch review before GitHub creation
- Allows easy editing via pull request
- Keeps related issues organized by epic

### Shared Pattern Documents

When writing specs for similar issues (e.g., CRUD endpoints, API resources), create a `PATTERNS.md` that defines:

- Common URL structures
- Standard request/response formats
- Error handling patterns
- Permission models

Individual specs then reference patterns: "See PATTERNS.md for CRUD pattern."

**Example reference in spec:**

```markdown
## Technical Notes

See PATTERNS.md for CRUD pattern.

- Requires `create` permission in org
- Generate slug from title (unique within parent)
```

### Acceptance Criteria Guidelines

**DO include:**

- [ ] Testable behavioral outcomes
- [ ] API response formats and status codes
- [ ] Permission/error handling requirements
- [ ] OpenAPI schema requirements

**DON'T include:**

- [ ] "Tests exist" or "Integration test written" (testing is implicit)
- [ ] Implementation steps disguised as criteria
- [ ] Vague criteria like "works correctly"

Testing is an implicit requirement for all issues. Don't add acceptance criteria like "unit tests written" or "e2e tests pass" - that's assumed.

## References

- **Issue Breakdown**: Use `zoonk-issue-planning` skill first to structure the breakdown
- **GitHub API**: Use `zoonk-github-issues` skill to post issues with proper types/dependencies
