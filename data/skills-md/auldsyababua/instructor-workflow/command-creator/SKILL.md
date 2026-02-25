---
name: command-creator
description: Define custom Claude Code slash commands for agents in the Traycer enforcement framework. This skill should be used when creating or updating agents and needing to specify reusable prompts that agents can execute as slash commands. Commands are Markdown files stored in .claude/commands/ and referenced in agent config.yaml files. This is for Claude Code slash commands (/command-name), not bash/CLI commands.
---

# Command Creator

This skill guides the creation of Claude Code slash commands for agents in the Traycer enforcement framework. Claude Code commands are custom slash commands defined as Markdown files containing prompts.

## When to Use

Use command-creator when:
1. Creating custom slash commands for an agent
2. Defining reusable prompts that should be invoked explicitly
3. Building commands that need dynamic arguments
4. Organizing frequently-used agent prompts

## Understanding Claude Code Commands

### What Are Commands?

**Claude Code commands** are custom slash commands that:
- Are Markdown (.md) files containing prompts
- Live in `.claude/commands/` (project) or `~/.claude/commands/` (personal)
- Are invoked with `/command-name` syntax
- Support dynamic arguments via placeholders
- Can execute bash commands before running
- Can reference files using `@` prefix

**Commands are NOT**:
- Bash/CLI scripts
- Python/JavaScript code
- Complex workflows (those are Skills)
- Automatically triggered (they require explicit invocation)

### Commands vs Skills vs System Prompt

| Element | Purpose | Example | Invocation |
|---------|---------|---------|------------|
| **Commands** | Quick, reusable prompts | `/git-commit`, `/review-pr` | Explicit: `/command-name` |
| **Skills** | Complex workflows with multiple files | `security-validation`, `test-standards` | Automatic based on context |
| **System Prompt** | Agent personality and core behavior | Agent role, coordination logic | Always active |

**Use commands when**:
- You have a frequently-used prompt
- Need explicit control over when it runs
- Prompt fits in a single Markdown file
- Want to pass dynamic arguments

**Use skills when**:
- Workflow requires multiple steps
- Need scripts, references, or assets
- Want automatic discovery based on context
- Multiple agents share the capability

**Use system prompt when**:
- Defining agent's core role
- Specifying agent-specific behavior
- Coordination with other agents

## Command Structure

### Basic Command File

**File**: `.claude/commands/optimize.md`

```markdown
Analyze this code for performance issues and suggest optimizations:
```

**Invocation**: `/optimize`

### Command with Frontmatter

**File**: `.claude/commands/git-commit.md`

```markdown
---
tools:
argument-hint: [message]
description: Create a git commit
model: haiku
---

Create a git commit with message: $ARGUMENTS
```

**Invocation**: `/git-commit "fix: resolve login bug"`

### Frontmatter Fields

| Field | Purpose | Default | Example |
|-------|---------|---------|---------|
| `allowed-tools` | Tools command can use | Inherits from conversation | `Bash(git add:*)` |
| `argument-hint` | Expected arguments | None | `[pr-number] [priority]` |
| `description` | Brief description | First line | `Create a git commit` |
| `model` | Specific model | Inherits from conversation | `haiku` |
| `disable-model-invocation` | Prevent SlashCommand tool | false | `true` |

## Command Features

### 1. Arguments

#### All Arguments with `$ARGUMENTS`

Captures all arguments as a single string:

```markdown
---
description: Fix a GitHub issue
---

Fix issue #$ARGUMENTS following our coding standards:
1. Understand the issue
2. Locate relevant code
3. Implement solution
4. Add tests
5. Prepare PR description
```

**Usage**:
```bash
/fix-issue 123 high-priority
```
`$ARGUMENTS` becomes: `"123 high-priority"`

#### Positional Arguments with `$1`, `$2`, `$3`

Access specific arguments individually:

```markdown
---
argument-hint: [pr-number] [priority] [assignee]
description: Review pull request
---

Review PR #$1 with priority $2 and assign to $3.
Focus on security, performance, and code style.
```

**Usage**:
```bash
/review-pr 456 high alice
```
- `$1` = `"456"`
- `$2` = `"high"`
- `$3` = `"alice"`

### 2. Bash Command Execution

Execute bash commands before prompt runs using `!` prefix:

```markdown
---
tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*)
description: Create a git commit based on current changes
---

## Context

- Current git status: !`git status`
- Staged and unstaged changes: !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Based on the above changes, create a single git commit with an appropriate message.
```

**Important**: Must include `allowed-tools` with `Bash` tool for bash execution.

### 3. File References

Include file contents using `@` prefix:

```markdown
---
description: Review specific file implementation
---

Review the implementation in @src/utils/helpers.js and suggest improvements.
```

**Multiple files**:
```markdown
Compare @src/old-version.js with @src/new-version.js and highlight differences.
```

### 4. Namespacing

Organize commands in subdirectories:

**Project structure**:
```text
.claude/commands/
├── git-commit.md          # /git-commit (project)
├── frontend/
│   └── component.md       # /component (project:frontend)
└── qa/
    └── review.md          # /review (project:qa)
```

**Personal structure**:
```text
~/.claude/commands/
├── security-review.md     # /security-review (user)
└── templates/
    └── pr-template.md     # /pr-template (user:templates)
```

**Conflict handling**:
- User vs project commands with same name: **NOT SUPPORTED**
- Commands in different subdirectories: **ALLOWED**

## Creating Commands

### Step 1: Determine Command Scope

**Project commands** (`.claude/commands/`):
- Shared with team via git
- Project-specific workflows
- Show "(project)" in `/help`

**Personal commands** (`~/.claude/commands/`):
- Personal workflows across all projects
- Not shared with team
- Show "(user)" in `/help`

### Step 2: Design Command Interface

**Name**: Use lowercase, hyphens for spaces
- Good: `git-commit`, `review-pr`, `fix-issue`
- Bad: `GitCommit`, `review_pr`, `fixIssue`

**Arguments**: Decide on argument pattern
- Simple: Use `$ARGUMENTS` for all args
- Structured: Use `$1`, `$2`, `$3` for specific args

**Prompt**: Write clear instructions
- Explain what the command should do
- Provide context (use `!` for bash, `@` for files)
- Specify expected output format

### Step 3: Create Command File

**For project command**:
```bash
mkdir -p .claude/commands
cat > .claude/commands/review-pr.md << 'EOF'
---
argument-hint: [pr-number]
description: Review pull request for code quality
---

Review pull request #$ARGUMENTS:

1. Check for security vulnerabilities
2. Verify test coverage
3. Assess code quality and style
4. Suggest improvements

Provide summary in Markdown format.
EOF
```

**For personal command**:
```bash
mkdir -p ~/.claude/commands
cat > ~/.claude/commands/security-scan.md << 'EOF'
---
description: Scan code for security issues
---

Scan this code for security vulnerabilities:
- Hardcoded secrets
- Insecure dependencies
- Authentication issues
- Input validation problems
EOF
```

### Step 4: Add Frontmatter

Enhance command with metadata:

```markdown
---
# Brief description shown in /help
description: Create a git commit

# Hint shown during autocomplete
argument-hint: [message]

# Tools the command can use
tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)

# Specific model (optional)
model: haiku

# Prevent SlashCommand tool from invoking (optional)
disable-model-invocation: false
---

Your command prompt here with $ARGUMENTS
```

### Step 5: Test Command

```bash
> /help
# Verify command appears in list

> /command-name arg1 arg2
# Test execution with arguments
```

### Step 6: Reference in Agent Config

**File**: `docs/agents/tracking-agent/config.yaml`

```yaml
name: tracking-agent

commands:
  - git-commit       # References .claude/commands/git-commit.md
  - linear-update    # References .claude/commands/linear-update.md
  - review-pr        # References .claude/commands/review-pr.md
```

**Important**: Reference by name **without** `.md` extension.

## Command Examples

### Example 1: Simple Command

**File**: `.claude/commands/optimize.md`

```markdown
Analyze the performance of this code and suggest three specific optimizations:
```

**Usage**: `/optimize`

### Example 2: Command with Arguments

**File**: `.claude/commands/fix-issue.md`

```markdown
---
argument-hint: [issue-number]
description: Fix a GitHub issue following project standards
---

Fix issue #$ARGUMENTS following these steps:

1. **Understand**: Read issue description and requirements
2. **Locate**: Find relevant code in codebase
3. **Implement**: Create solution addressing root cause
4. **Test**: Add appropriate tests
5. **Document**: Prepare concise PR description

Follow project coding standards and conventions.
```

**Usage**: `/fix-issue 123`

### Example 3: Git Commit Command

**File**: `.claude/commands/git-commit.md`

```markdown
---
tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*), Bash(git log:*)
description: Create a git commit based on current changes
---

## Context

- Current git status: !`git status`
- Staged and unstaged changes: !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent 10 commits: !`git log --oneline -10`

## Your Task

Based on the above git context, create a single git commit:

1. **Analyze changes**: Review the git diff
2. **Choose files**: Select relevant files to stage
3. **Write message**: Create commit message following format:
   - Type: `feat|fix|docs|refactor|test|chore`
   - Format: `<type>: <description>`
   - Example: `feat: add user authentication`
4. **Create commit**: Execute git commands to stage and commit

**Important**: Follow this repository's commit message style (see recent commits).
```

**Usage**: `/git-commit`

### Example 4: Positional Arguments

**File**: `.claude/commands/review-pr.md`

```markdown
---
argument-hint: [pr-number] [priority] [assignee]
description: Review pull request with priority and assignment
---

Review pull request #$1:

**Priority**: $2
**Assign to**: $3

**Review checklist**:
1. Security vulnerabilities
2. Performance issues
3. Code style violations
4. Test coverage
5. Documentation completeness

Provide detailed review comments with severity levels.
```

**Usage**: `/review-pr 456 high alice`

### Example 5: File Reference Command

**File**: `.claude/commands/explain-file.md`

```markdown
---
argument-hint: <file-path>
description: Explain implementation of a specific file
---

Explain the implementation in @$ARGUMENTS:

1. **Purpose**: What does this file do?
2. **Structure**: How is the code organized?
3. **Key functions**: What are the main functions/classes?
4. **Dependencies**: What does it depend on?
5. **Usage**: How is it used elsewhere?

Provide clear, beginner-friendly explanation.
```

**Usage**: `/explain-file src/utils/helpers.js`

## Agent Config Integration

### Declaring Commands

**File**: `docs/agents/qa-agent/config.yaml`

```yaml
name: qa-agent
description: Quality assurance and validation agent

# Skills for complex workflows
skills:
  - security-validation
  - test-standards
  - code-quality-standards

# Commands for explicit invocations
commands:
  - review-pr         # Quick PR review
  - security-scan     # Security check
  - test-coverage     # Coverage analysis

ref_docs:
  - test-audit-protocol.md
  - traycer-coordination-guide.md
```

### Commands in Agent Workflow

**Agent can use commands**:
1. **Manually**: User invokes `/review-pr 456`
2. **Programmatically**: Via `SlashCommand` tool (if enabled)

**SlashCommand tool requirements**:
- Command must have `description` frontmatter
- Not disabled via `disable-model-invocation: true`
- Character budget not exceeded (15,000 chars default)

## Framework Integration (Traycer Enforcement Framework)

When creating commands for the Traycer enforcement framework:

### Command Location

Commands live in: `.claude/commands/<command-name>.md`

Example:
```text
.claude/commands/
├── git-commit.md
├── review-pr.md
└── your-new-command.md
```

### Agent Assignment

**When called standalone** (user asks to create a command):
1. Ask user which agents should use this command
2. Suggest agents based on command's purpose:
   - Git operations → tracking-agent
   - Code validation → qa-agent
   - Implementation → action-agent
   - Workflow coordination → workflow-upgrade-assistant
3. List suggested agents for user confirmation

**When called by agent-builder**:
- Agent context provided automatically
- No need to ask about agent assignment

### Updating Agent Config

After creating the command, update each agent's config.yaml:

**File**: `docs/agents/<agent-name>/config.yaml`

Add command name (without .md extension) to `commands:` section:
```yaml
commands:
  - existing-command-1
  - existing-command-2
  - your-new-command    # Add here (no .md extension)
```

### Complete Workflow

1. Create command file: `.claude/commands/<command-name>.md`
2. Add frontmatter (description, argument-hint, allowed-tools)
3. Write command prompt with $ARGUMENTS or $1, $2, $3
4. **Determine which agents use this command** (ask user or use agent-builder context)
5. **Update each agent's config.yaml** to reference the command
6. Test command with `/command-name args`

## Best Practices

### 1. Keep Commands Simple

**Good**: Single-purpose, clear prompt
```markdown
Review this code for security vulnerabilities
```

**Bad**: Multiple unrelated tasks
```markdown
Review code for security, performance, style, tests, documentation, and deployment issues
```

### 2. Use Descriptive Names

**Good**: `review-pr`, `git-commit`, `fix-issue`
**Bad**: `r`, `gc`, `fix`

### 3. Provide Context with Bash

**Good**: Include relevant git context
```markdown
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -5`
```

**Bad**: Assume context is known
```markdown
Create a commit
```

### 4. Document Expected Arguments

**Good**: Clear argument hint
```markdown
---
argument-hint: [pr-number] [priority] [assignee]
---
```

**Bad**: No hint, unclear usage

### 5. Use Frontmatter

**Good**: Complete metadata
```markdown
---
description: Review pull request
argument-hint: [pr-number]
tools: Bash(gh pr view:*)
---
```

**Bad**: No frontmatter (description defaults to first line)

### 6. Namespace Organization

**Good**: Organized by function
```text
.claude/commands/
├── git/
│   ├── commit.md
│   ├── branch.md
│   └── push.md
├── qa/
│   ├── review.md
│   └── test.md
```

**Bad**: Flat structure with many commands

## Common Patterns

### Pattern 1: Context-Rich Commands

Include bash output for context:

```markdown
---
tools: Bash(git status:*), Bash(git diff:*)
---

## Context
- Git status: !`git status --short`
- Changes: !`git diff --stat`

## Task
[Your instructions based on context]
```

### Pattern 2: Structured Arguments

Use positional args for structured input:

```markdown
---
argument-hint: [component] [action] [target]
---

$1: Component name
$2: Action to perform
$3: Target file/directory

Execute $2 on $1 targeting $3.
```

### Pattern 3: File-Based Commands

Reference specific files:

```markdown
Review @$ARGUMENTS for:
1. Code quality
2. Security issues
3. Performance concerns
```

Usage: `/review src/auth.js`

### Pattern 4: Multi-Step Workflows

Break complex tasks into steps:

```markdown
Execute deployment workflow for $ARGUMENTS:

**Phase 1: Pre-deployment**
- [ ] Run tests
- [ ] Security scan
- [ ] Build artifacts

**Phase 2: Deployment**
- [ ] Deploy to staging
- [ ] Verify health checks
- [ ] Deploy to production

**Phase 3: Post-deployment**
- [ ] Monitor metrics
- [ ] Verify functionality
- [ ] Document deployment
```

## Integration with Agent Builder

When using Agent Builder skill to create an agent:

1. **Agent Builder analyzes requirements**
2. **Identifies frequently-used prompts** → Candidates for commands
3. **Calls Command Creator** to define command specifications
4. **Creates command files** in `.claude/commands/`
5. **References commands** in `config.yaml`

**Command Creator provides**:
- Command file structure
- Frontmatter recommendations
- Argument patterns
- Integration with agent workflow

## Quick Reference

**Creating commands**:
1. Choose scope (project vs personal)
2. Design command interface (name, arguments)
3. Write prompt in Markdown
4. Add frontmatter (description, argument-hint, allowed-tools)
5. Test with `/command-name args`
6. Reference in agent config.yaml

**Command naming**:
- Use: `git-commit`, `review-pr`, `fix-issue`
- Avoid: `GitCommit`, `review_pr`, `fixIssue`

**File location**:
- Project: `.claude/commands/command-name.md`
- Personal: `~/.claude/commands/command-name.md`

**Config reference**:
```yaml
commands:
  - command-name  # No .md extension
```

## Resources

For detailed patterns and examples, see `references/command-examples.md`:
- Complete command specifications from existing agents
- Argument design patterns
- Frontmatter best practices
- Integration examples
