---
name: gsdl-create-plan
description: Generate a detailed implementation plan (task list) from a Product Requirements Document (PRD). Use when the user wants to break down a PRD into implementation tasks, create a plan from requirements, generate tasks from a PRD, or asks to "create a plan".
disable-model-invocation: true
---

# Generate Task List from PRD

Generates a detailed, step-by-step task list in Markdown format based on an existing Product Requirements Document (PRD). The task list guides a developer through implementation with parent tasks and detailed sub-tasks.

## Prerequisites

Before generating a task list:

1. **Project exists**: The project should have its own folder at `.planning/[project-name]/`
2. **PRD exists**: Ensure the PRD file exists at `.planning/[project-name]/tasks/prd-[feature-name].md`
3. **Tasks folder exists**: Confirm `.planning/[project-name]/tasks/` directory exists

## Output

The task list will be saved as:

- **Format**: Markdown (`.md`)
- **Location**: `.planning/[project-name]/tasks/`
- **Filename**: `tasks-[prd-file-name].md` (e.g., `tasks-prd-user-profile-editing.md`)
- **Full Path Example**: `.planning/my-cool-project/tasks/tasks-prd-user-authentication.md`

## Two-Phase Process

This skill follows a **two-phase workflow** to ensure alignment before diving into details.

### Phase 1: Generate Parent Tasks

1. **Receive PRD Reference**: The user points to a specific PRD file
2. **Read PRD from disk**: Read the PRD file directly from disk at its path — do **not** rely on any in-context version. The user may have edited the file since it was generated.
3. **Analyze PRD**: Analyze the functional requirements, user stories, and other sections from the file just read
4. **Create Parent Tasks**: Generate 5-7 high-level tasks required to implement the feature
5. **Present to User**: Show the parent tasks in the specified format (without sub-tasks yet)
6. **Pause for Confirmation**: Inform the user: "I have generated the high-level tasks based on the PRD. Review the tasks above — feel free to edit the PRD or suggest changes before we continue. Respond with 'Go' to generate the sub-tasks."

### Phase 2: Generate Sub-Tasks

1. **Wait for "Go"**: Only proceed after the user confirms with "Go"
2. **Re-read PRD from disk**: Before generating sub-tasks, read the PRD file from disk again to pick up any edits the user may have made since Phase 1
3. **Break Down Tasks**: For each parent task, create smaller, actionable sub-tasks based on the current PRD content
4. **Identify Files**: List potential files that will need to be created or modified
5. **Generate Final Output**: Combine everything into the complete task list structure
6. **Save Task List**: Save to the project's tasks directory

## Task List Structure

The generated task list must follow this exact format:

```markdown
## Relevant Files

- `src/path/to/potential/file1.ts` - Brief description of why this file is relevant (e.g., Contains the main component for this feature).
- `src/path/to/file1.test.ts` - Unit tests for `file1.ts`.
- `src/path/to/another/file.tsx` - Brief description (e.g., API route handler for data submission).
- `src/path/to/another/file.test.tsx` - Unit tests for `another/file.tsx`.
- `lib/utils/helpers.ts` - Brief description (e.g., Utility functions needed for calculations).
- `lib/utils/helpers.test.ts` - Unit tests for `helpers.ts`.

### Notes

- Implementation file paths are relative to the workspace root (e.g., `src/components/MyComponent.tsx`). Planning files (PRDs, task lists) live under `.planning/[project-name]/tasks/`.
- Unit tests should typically be placed alongside the code files they are testing (e.g., `MyComponent.tsx` and `MyComponent.test.tsx` in the same directory).
- Use `npx jest [optional/path/to/test/file]` to run tests. Running without a path executes all tests found by the Jest configuration.

## Tasks

- [ ] 1.0 Parent Task Title
  - [ ] 1.1 [Sub-task description 1.1]
  - [ ] 1.2 [Sub-task description 1.2]
- [ ] 2.0 Parent Task Title
  - [ ] 2.1 [Sub-task description 2.1]
- [ ] 3.0 Parent Task Title (may not require sub-tasks if purely structural or configuration)
```

## Task Breakdown Guidelines

### Parent Tasks

- Create 5-7 high-level tasks that represent major implementation phases
- Use numbered format: `1.0`, `2.0`, `3.0`, etc.
- Each parent task should represent a significant milestone
- Examples: "Set up project structure", "Implement core functionality", "Add validation and error handling"

### Sub-Tasks

- Break each parent task into specific, actionable items
- Use nested numbering: `1.1`, `1.2`, `1.3` under parent `1.0`
- Each sub-task should be concrete and implementable
- Sub-tasks should logically follow from the parent task
- Not all parent tasks require sub-tasks (e.g., simple configuration tasks)

### Relevant Files

- List every file that will be created or modified
- Include both implementation files and test files
- Use full paths relative to workspace root
- Provide a brief description for each file explaining its purpose
- Group related files together (implementation + tests)

## Target Audience

The task list is designed for a **junior developer** who will implement the feature. Tasks should be:
- Clear and specific
- Implementable without extensive guidance
- Ordered logically to build up the feature step by step

## Interaction Model

**IMPORTANT**: This skill requires user confirmation between phases:

1. Generate parent tasks → Show to user → **Wait for "Go"**
2. User responds with "Go" → Generate sub-tasks and complete the file

Do not proceed to Phase 2 until the user explicitly confirms the parent tasks are correct.

## Examples

### Phase 1 Output (Parent Tasks Only)

```markdown
## Tasks

- [ ] 1.0 Set up authentication module structure
- [ ] 2.0 Implement user login functionality
- [ ] 3.0 Implement user registration
- [ ] 4.0 Add session management
- [ ] 5.0 Create authentication UI components
- [ ] 6.0 Add error handling and validation
- [ ] 7.0 Write tests and documentation
```

### Phase 2 Output (Complete with Sub-Tasks)

```markdown
## Relevant Files

- `src/auth/login.ts` - Login endpoint handler
- `src/auth/login.test.ts` - Tests for login functionality
[... more files ...]

## Tasks

- [ ] 1.0 Set up authentication module structure
  - [ ] 1.1 Create auth directory structure
  - [ ] 1.2 Set up authentication configuration
  - [ ] 1.3 Install required dependencies
- [ ] 2.0 Implement user login functionality
  - [ ] 2.1 Create login endpoint
  - [ ] 2.2 Implement credential validation
  - [ ] 2.3 Generate and return JWT token
[... more tasks ...]
```
