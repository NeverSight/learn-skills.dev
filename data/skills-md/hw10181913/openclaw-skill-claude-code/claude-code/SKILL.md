---
name: claude-code
description: |
  Claude Code integration for OpenClaw. This skill provides interfaces to:
  - Query Claude Code documentation from https://code.claude.com/docs
  - Use Spec-Driven Development with spec-kit
  - Manage subagents and coding tasks
  - Execute AI-assisted coding workflows
  - Access best practices and common workflows
  Use this skill when users want to:
  - Get help with coding tasks
  - Query Claude Code documentation
  - Use spec-kit workflow for structured development
  - Manage AI-assisted development workflows
  - Execute complex programming tasks
homepage: https://code.claude.com/docs
---

# Claude Code Integration

This skill integrates Claude Code capabilities into OpenClaw, providing access to AI-assisted coding workflows, documentation, and best practices.

## What You Can Do

### 📚 Documentation Queries
- Query Claude Code documentation
- Get best practices and workflows
- Learn about settings and customization
- Troubleshoot common issues

### 🤖 Subagent Management
- Create coding subagents
- Manage agent teams
- Execute complex development tasks
- Automate code reviews and PR workflows

### 🛠️ Development Workflows
- Best practices for AI-assisted coding
- Common workflows and patterns
- Settings and configuration
- Troubleshooting guidance

## Usage Examples

### Query Documentation
```bash
# Get documentation about a specific topic
claude-code query "subagents"
claude-code query "best practices"
claude-code query "settings"
```

### Execute Coding Task
```bash
# Create a coding subagent for a complex task
claude-code task --description "Fix the login bug" --priority high
claude-code task --description "Refactor the database layer" --model claude-3-5-sonnet
```

### List Available Commands
```bash
# Show all available commands
claude-code --help
```

## Available Commands

### query
Query Claude Code documentation for a specific topic.

**Usage:**
```bash
claude-code query <topic>
```

**Examples:**
```bash
claude-code query "subagents"
claude-code query "agent-teams"
claude-code query "best practices"
claude-code query "common workflows"
claude-code query "settings"
claude-code query "troubleshooting"
```

**Topics include:**
- Subagents and agent teams
- Best practices and workflows
- Settings and customization
- Troubleshooting guide
- Plugins and extensions
- MCP (Model Context Protocol)
- Headless/Programmatic usage

### task
Create and execute a coding subagent task.

**Usage:**
```bash
claude-code task --description "<task description>" [--priority <level>] [--model <model-name>]
```

**Options:**
- `--description, -d`: Task description (required)
- `--priority, -p`: Task priority (low/medium/high, default: medium)
- `--model, -m`: Model to use (optional, uses default if not specified)

**Examples:**
```bash
claude-code task --description "Implement user authentication module"
claude-code task --description "Refactor database queries" --priority high
claude-code task --description "Write unit tests for the API" --model claude-3-5-sonnet
```

### docs
Get overview of Claude Code documentation sections.

**Usage:**
```bash
claude-code docs [section]
```

**Sections:**
- `quickstart` - Getting started guide
- `best-practices` - AI coding best practices
- `common-workflows` - Typical development workflows
- `settings` - Customization options
- `troubleshooting` - Common issues and solutions
- `all` - Full documentation overview (default)

**Examples:**
```bash
claude-code docs
claude-code docs quickstart
claude-code docs best-practices
claude-code docs troubleshooting
```

### info
Display Claude Code configuration and status.

**Usage:**
```bash
claude-code info
```

**Output includes:**
- Version information
- Available subagents
- Configured models
- MCP servers status

## Integration with OpenClaw

This skill works seamlessly with OpenClaw's native capabilities:

- **Subagents**: Claude Code subagents complement OpenClaw's subagent system
- **Code Execution**: Use with OpenClaw's exec tool for complete development workflow
- **File Management**: Combine with OpenClaw's read/write tools for full codebase management
- **Sessions**: Claude Code tasks integrate with OpenClaw's session management

## Example Workflows

### Complex Bug Fix
```bash
# 1. Query best practices for debugging
claude-code query "debugging best practices"

# 2. Create a subagent to investigate and fix
claude-code task --description "Find and fix the null pointer exception in userService.js" --priority high

# 3. Review the changes
claude-code query "code review best practices"
```

### New Feature Development
```bash
# 1. Get best practices for the feature type
claude-code query "API design best practices"

# 2. Create development task
claude-code task --description "Implement REST API for user management" --priority medium

# 3. Check settings for code style
claude-code query "code style settings"
```

### Code Review Automation
```bash
# 1. Query PR review best practices
claude-code query "PR review workflows"

# 2. Set up automated review task
claude-code task --description "Review all PRs in the last week" --priority low
```

## Configuration

### Environment Variables
Not required for basic usage. Claude Code integration uses OpenClaw's native capabilities.

### Models
Uses OpenClaw's configured default models. Override per task with `--model` option.

### Subagent Limits
Managed by OpenClaw's subagent configuration (default: 8 concurrent subagents).

## Notes

- This skill provides a wrapper around Claude Code documentation and workflows
- Complex coding tasks are executed through OpenClaw's native subagent system
- For direct Claude Code CLI usage, install Claude Code separately from https://claude.com/code
- All task execution happens through OpenClaw's secure agent infrastructure

## See Also

- Claude Code Official Docs: https://code.claude.com/docs
- OpenClaw Subagents: Use OpenClaw's native subagent functionality
- Best Practices: Integrated from Claude Code guidelines

---

# 🚀 Spec-Driven Development with Spec-Kit

## What is Spec-Driven Development?

Spec-Driven Development flips the script on traditional software development. Instead of coding first and treating specs as scaffolding, specifications become **executable** - directly generating working implementations rather than just guiding them.

## Spec-Kit Core Philosophy

- **Intent-driven**: Specifications define the "what" before the "how"
- **Rich specifications**: Guardrails and organizational principles
- **Multi-step refinement**: No one-shot code generation
- **AI-native**: Leverages advanced AI model capabilities

## Spec-Kit Workflow (7 Steps)

### Step 1: Install Spec-Kit CLI
```bash
# Install via uv (recommended)
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# Verify installation
specify check

# Initialize project with Claude Code
specify init <PROJECT_NAME> --ai claude
```

### Step 2: Establish Project Principles
Use `/speckit.constitution` command to create governing principles:
```markdown
/speckit.constitution Create principles focused on:
- Code quality standards
- Testing requirements
- User experience consistency
- Performance requirements
- Design system guidelines
```

Creates `.specify/memory/constitution.md` - your project's foundational guidelines.

### Step 3: Create the Specification
Use `/speckit.specify` to describe what to build:
```markdown
/speckit.specify Build an application that [describe your product vision]
Focus on:
- What the application does
- User stories and scenarios
- Core features and functionality
- User experience goals
NOT the tech stack!
```

### Step 4: Clarify Requirements (Optional but Recommended)
Use `/speckit.clarify` for structured questioning:
```markdown
/speckit.clarify 
```
Sequential, coverage-based questioning that records answers in Clarifications section.

### Step 5: Create Technical Plan
Use `/speckit.plan` to define your tech stack:
```markdown
/speckit.plan The application uses:
- Frontend: [React/Vue/Vanilla HTML+CSS+JS]
- Backend: [Node.js/Python/Go]
- Database: [PostgreSQL/MongoDB/LocalStorage]
- Key libraries: [list dependencies]
```

### Step 6: Generate Tasks
Use `/speckit.tasks` to break down implementation:
```bash
/speckit.tasks
```
Creates `tasks.md` with:
- Task breakdown by user story
- Dependency management
- Parallel execution markers ([P])
- File path specifications
- TDD structure

### Step 7: Execute Implementation
Use `/speckit.implement` to build:
```bash
/speckit.implement
```
Executes tasks in correct order, follows TDD approach, provides progress updates.

## Available Slash Commands

### Core Commands (Essential)
| Command | Description |
|---------|-------------|
| `/speckit.constitution` | Create/update project principles |
| `/speckit.specify` | Define what to build (requirements) |
| `/speckit.plan` | Create technical implementation plan |
| `/speckit.tasks` | Generate actionable task list |
| `/speckit.implement` | Execute all tasks |

### Optional Commands (Enhanced Quality)
| Command | Description |
|---------|-------------|
| `/speckit.clarify` | Structured requirements clarification |
| `/speckit.analyze` | Cross-artifact consistency analysis |
| `/speckit.checklist` | Quality validation checklists |

## Project Structure (After `specify init`)

```
PROJECT_NAME/
├── .specify/
│   ├── memory/
│   │   └── constitution.md      # Project principles
│   ├── scripts/
│   │   ├── check-prerequisites.sh
│   │   ├── common.sh
│   │   ├── create-new-feature.sh
│   │   ├── setup-plan.sh
│   │   └── update-claude-md.sh
│   └── specs/
│       └── 001-feature-name/
│           ├── spec.md           # Functional specs
│           ├── plan.md          # Technical plan
│           ├── tasks.md         # Implementation tasks
│           └── quickstart.md    # Run instructions
├── CLAUDE.md                     # AI assistant guidance
└── templates/
    ├── CLAUDE-template.md
    ├── plan-template.md
    ├── spec-template.md
    └── tasks-template.md
```

## Real-World Example: Skeuomorphic Todo App

### Step 1: Initialize Project
```bash
specify init todo-app-spec-kit --ai claude
cd todo-app-spec-kit
```

### Step 2: Create Constitution
```markdown
/speckit.constitution Create principles:
- Design Excellence: Skeuomorphic first, tactile feedback
- Code Quality: Clean architecture, progressive enhancement
- Testing: Visual testing, interaction testing
- User Experience: Intuitive, rewarding, calm design
```

### Step 3: Specify Requirements
```markdown
/speckit.specify Build a beautiful todo list app with:
- Tasks as index cards on a corkboard or notebook
- Add/edit/delete task functionality
- Mark complete with stamp animation
- Drag-and-drop reordering
- LocalStorage persistence
- Warm paper-like aesthetic with handwriting fonts
- Satisfying tactile interactions (crumpling, writing sounds)
```

### Step 4: Create Plan
```markdown
/speckit.plan Use:
- Pure HTML5/CSS3/JavaScript (no frameworks)
- LocalStorage for data persistence
- Google Fonts (Caveat handwriting)
- CSS animations for tactile effects
- Mobile-responsive design
- Fully offline-capable
```

### Step 5: Generate & Execute Tasks
```bash
/speckit.tasks    # Creates task breakdown
/speckit.implement  # Executes all tasks
```

## Benefits of Spec-Kit

✅ **Structured Process**: No more vague prompts
✅ **Quality Assurance**: Built-in checklists and validation
✅ **Parallel Exploration**: Multiple implementation paths
✅ **Documentation**: Automatic spec generation
✅ **Reproducible**: Same workflow for every project
✅ **AI-Optimized**: Commands designed for Claude Code

## Tips for Success

1. **Be Specific**: The more detailed your spec, the better the output
2. **Iterate**: Don't expect perfection on first try
3. **Use Clarify**: Address ambiguities before planning
4. **Follow Order**: constitution → specify → plan → tasks → implement
5. **Validate**: Use `/speckit.checklist` before declaring done

## Spec-Kit Documentation

- **Main Repo**: https://github.com/github/spec-kit
- **Detailed Guide**: https://github.com/github/spec-kit/blob/main/spec-driven.md
- **Video Overview**: https://www.youtube.com/watch?v=a9eR1xsfvHg

## Integration with This Skill

This Claude Code skill includes Spec-Kit knowledge! You can:

```bash
# Query Spec-Kit documentation
claude-code query "spec-kit"
claude-code query "spec-driven development"
claude-code query "specify CLI"

# Get workflow guidance
claude-code docs spec-workflow
```

## Example: Starting a New Project

```bash
# 1. Install spec-kit (one-time)
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# 2. Initialize project
specify init my-new-app --ai claude

# 3. In Claude Code, use the commands:
/speckit.constitution  # Set design principles
/speckit.specify      # Define your app
/speckit.plan         # Choose tech stack
/speckit.tasks        # Get task list
/speckit.implement     # Build it!
```

---

**Resources**:
- Spec-Kit GitHub: https://github.com/github/spec-kit
- This Skill's Repo: https://github.com/hw10181913/openclaw-skill-claude-code
- Documentation: https://code.claude.com/docs
