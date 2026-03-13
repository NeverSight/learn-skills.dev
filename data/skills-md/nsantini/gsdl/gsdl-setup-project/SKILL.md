---
name: gsdl-setup-project
description: Set up new project structure with tasks directory and seed file for research workspace. Use when the user wants to start a new project, create a project structure, initialize a new idea, or mentions starting something new.
disable-model-invocation: true
---

# Setup Project

Creates a standardized project structure for new ideas, prototypes, or tools in the research workspace. Each project gets its own isolated folder with task tracking and documentation structure.

## Goal

Ensure every new idea, prototype, or tool is organized into its own dedicated folder structure. This keeps the workspace clean and ensures each project has proper context, requirements, and task tracking from the start.

## Project Structure Requirements

Every new project must include:

1. **Isolated Project Folder**: Dedicated directory under `.planning/` (e.g., `.planning/project-name/`)
2. **Tasks Directory**: For PRDs and task lists at `.planning/project-name/tasks/`
3. **Seed File**: Initial idea capture at `.planning/project-name/seed.md`
4. **Containment**: All planning files stay within `.planning/[project-name]/`

## Setup Workflow

### Step 1: Identify Project Name

Choose a short, descriptive name:
- Use **kebab-case** (lowercase with hyphens)
- Keep it concise and meaningful
- Examples: `user-authentication`, `task-manager`, `api-client`

### Step 2: Create Directory Structure

Create the project folders:

```bash
mkdir -p .planning/[project-name]/tasks
```

### Step 3: Create Seed File

Create `.planning/[project-name]/seed.md` to capture the initial idea:

**Seed File Purpose**:
- Informal and flexible format
- Captures raw thinking before formalization
- Serves as input for PRD creation

**What to Include**:
- The initial problem or opportunity
- Rough feature ideas or concepts
- Inspiration or reference links
- Questions or uncertainties
- Any initial thoughts that will help inform the PRD

### Step 4: Confirm Setup

Inform the user:
- Show the created structure
- Confirm the seed file location
- Explain next steps (creating PRD, etc.)

## Seed File Format

The seed file is intentionally informal and flexible. Here's a template:

```markdown
# [Project Name]

## Initial Idea
[Brief description of what you want to build]

## Problem/Opportunity
[What problem does this solve? Why build this?]

## Key Features (Initial Thoughts)
- Feature idea 1
- Feature idea 2
- Feature idea 3

## Inspiration/References
- [Links to similar tools, articles, etc.]

## Questions/Uncertainties
- Question 1?
- Question 2?

## Next Steps
- [ ] Create PRD
- [ ] Generate task list
```

## Complete Directory Structure Example

After setup, the project should look like:

```
workspace-root/
├── .planning/
│   └── project-name/
│       ├── seed.md           # Initial idea capture
│       └── tasks/            # PRDs and task lists
│           └── (empty initially)
└── (source code files live at workspace root, not in .planning/)
```

As the project evolves:

```
workspace-root/
├── .planning/
│   └── project-name/
│       ├── seed.md
│       └── tasks/
│           ├── prd-feature-name.md
│           └── tasks-prd-feature-name.md
├── src/
│   └── (implementation files)
├── tests/
│   └── (test files)
└── README.md
```

## Integration with Other Skills

After setting up a project, guide the user through the workflow:

1. **gsdl-setup-project** (this skill) → Creates structure and seed.md
2. **gsdl-create-prd** → Uses seed.md to generate PRD
3. **gsdl-create-plan** → Breaks down PRD into tasks
4. **gsdl-execute-plan** → Guides implementation

## Important Rules

1. **Containment**: All planning files (seed, PRDs, task lists) must stay within `.planning/[project-name]/`
2. **Implementation code lives at workspace root**: Source files, tests, and README go at the repo root — not inside `.planning/`
3. **Consistent naming**: Use kebab-case for project names
4. **Seed first**: Always create seed.md before PRD

## Example Interaction

```
User: "I want to start a new project for user authentication"

AI: "I'll set up a new project structure for user authentication.

Created:
- .planning/user-authentication/
- .planning/user-authentication/tasks/
- .planning/user-authentication/seed.md

The seed file is ready for you to document your initial ideas. Once you've added your thoughts to the seed file, I can help you create a PRD using the gsdl-create-prd skill.

Would you like me to help you populate the seed file now, or would you prefer to write it yourself first?"
```

## Edge Cases

### Project Already Exists

If a project folder already exists:
1. Check if it has the required structure (tasks/, seed.md)
2. Add missing components without overwriting existing files
3. Inform the user what was added

### Similar Project Names

If a similar project name exists:
1. Suggest an alternative name or numbered suffix
2. Ask the user to confirm or provide a different name
3. Examples: `auth-system-2`, `auth-system-v2`, `oauth-integration`

### Multiple Projects

If the user wants to set up multiple projects:
1. Set up each project separately
2. Confirm each project's structure before moving to the next
3. Summarize all created projects at the end

## File Path Standards

Always use full paths relative to workspace root:
- **Correct**: `.planning/[project-name]/tasks/prd-feature.md`
- **Correct**: `src/components/Auth.tsx` (implementation code lives at workspace root, not in `.planning/`)
- **Incorrect**: `[project-name]/tasks/prd-feature.md` (missing `.planning/` prefix)
- **Incorrect**: `./src/Auth.tsx` (relative path)

## Next Steps After Setup

After creating the project structure, typically:

1. **Populate seed.md**: Either help the user fill it out or let them do it
2. **Create PRD**: Use the gsdl-create-prd skill to formalize requirements
3. **Generate tasks**: Use gsdl-create-plan to break down the PRD
4. **Start implementation**: Use gsdl-execute-plan to guide development

## Quick Setup Command

For quick reference, the complete setup:

```bash
mkdir -p .planning/[project-name]/tasks
touch .planning/[project-name]/seed.md
```

Then populate the seed file with the initial idea.
