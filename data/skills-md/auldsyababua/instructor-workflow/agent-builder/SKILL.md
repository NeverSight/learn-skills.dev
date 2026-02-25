---
name: agent-builder
description: Create complete Claude Code agents for the Traycer enforcement framework. This skill should be used when creating new agents or updating existing agents. Creates all agent components including system prompt, hooks, skills, commands, scripts, and reference docs. Also updates coordination documents that list available agents. Based on Anthropic's official agent development best practices.
---

# Agent Builder

This skill guides the creation of complete, production-ready Claude Code agents following Anthropic's official best practices for context engineering, tool design, skills architecture, and enforcement through hooks.

## When to Use

Use agent-builder when:
1. Creating a new agent from scratch
2. Major refactoring of an existing agent
3. Converting a concept/requirements into a functioning agent
4. Ensuring agent follows Anthropic best practices
5. Need to create all agent components (prompt, hooks, skills, commands, etc.)

## Agent Anatomy

A complete agent consists of:

### Core Files
```text
.claude/agents/<agent-name>.md  # Single file with YAML frontmatter + system prompt
docs/agents/<agent-name>/
└── ref-docs/              # Agent-specific reference documents (optional)
    └── *.md
docs/agents/shared-ref-docs/   # Shared reference documents (multi-agent)
    └── *.md
```

### Commands (Slash Commands)
```text
.claude/commands/
├── <agent-command-1>.md   # Explicit invocation commands
└── <agent-command-2>.md
```

### Skills (Complex Workflows)
```text
docs/skills/<skill-name>/
├── SKILL.md               # Skill definition with frontmatter
├── scripts/               # Executable automation
│   └── *.py
└── references/            # Documentation loaded as needed
    └── *.md
```

### Hooks (Enforcement)
```text
.claude/settings.json      # Project hooks
~/.claude/settings.json    # User hooks
```

Configuration in settings files:
```json
{
  "hooks": {
    "PreToolUse": [...],
    "PostToolUse": [...],
    "UserPromptSubmit": [...],
    "SessionStart": [...]
  }
}
```

### Agent-Specific Scripts
```text
docs/agents/<agent-name>/scripts/
└── *.py                   # Utility scripts (not part of skills)
```

### Coordination Updates

When creating new agents, update:
- **Other agent prompts**: If they reference available agents for delegation
- **Shared ref docs**: Agent coordination guides, addressing systems
- **Team documentation**: Agent capabilities matrix, workflow diagrams

## Agent Creation Workflow

### Phase 1: Requirements Analysis

**Input**: Agent requirements (purpose, responsibilities, constraints)

**Actions**:
1. Define agent's scope and boundaries
2. Identify integration points with other agents
3. Determine tools and permissions needed
4. Identify reusable patterns (→ Skills)
5. Identify explicit operations (→ Commands)
6. Identify enforcement rules (→ Hooks)

**Output**: Requirements document

### Phase 2: Architecture Design

**System Prompt Design**:
- Define agent role and expertise
- Set behavior at "right altitude" (Anthropic principle)
  - Not too prescriptive (hardcoded if-else)
  - Not too vague (assumes shared context)
  - Specific enough to guide, flexible for heuristics
- Organize with clear sections
- Start minimal, iterate based on failures

**Tool Selection**:
- Choose minimal viable set
- Each tool has clear, distinct purpose
- Avoid overlapping functionality
- Consider token efficiency

**Skills vs Commands Decision**:
| Use Skills For | Use Commands For |
|----------------|------------------|
| Complex multi-step workflows | Quick, frequently-used prompts |
| Multiple files/scripts needed | Single file sufficient |
| Automatic discovery desired | Explicit invocation preferred |
| Team standardization | Personal productivity |

**Hooks Planning**:
- Identify rules that MUST be enforced (not just prompted)
- Validation requirements (PreToolUse)
- Feedback mechanisms (PostToolUse)
- Context loading (SessionStart)
- Monitoring needs (logging, notifications)

### Phase 3: Component Creation

#### 3.1 Create Skills (Complex Workflows)

**Call**: Skill Creator skill

**For each skill**:
1. Define skill purpose and trigger conditions
2. Write SKILL.md with:
   - Clear `description` (what + when to use)
   - Step-by-step instructions
   - Examples
   - Progressive disclosure (reference additional files as needed)
3. Create scripts (if deterministic operations needed)
4. Create reference docs (if extensive documentation needed)
5. Add `allowed-tools` frontmatter (if restricting tool access)

**Example skill structure**:
```text
docs/skills/validation-protocol/
├── SKILL.md
├── scripts/
│   └── validate.py        # Deterministic validation
└── references/
    └── patterns.md        # Loaded as needed
```

#### 3.2 Create Commands (Slash Commands)

**Call**: Command Creator skill

**For each command**:
1. Define command purpose
2. Choose argument pattern (`$ARGUMENTS` or `$1, $2, $3`)
3. Write command file:
   - Frontmatter (description, argument-hint, allowed-tools)
   - Prompt with context (use `!` for bash, `@` for files)
4. Test command invocation

**Example command**:
```markdown
---
argument-hint: [file-path]
description: Validate code quality in specific file
tools:
---

Validate code quality in @$ARGUMENTS:

1. Check for code smells
2. Verify naming conventions
3. Assess complexity
4. Provide specific feedback
```

#### 3.3 Configure Hooks (Enforcement)

**Hook types to consider**:

**PreToolUse** (Validation/Blocking):
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-code.py"
        }]
      }
    ]
  }
}
```

**PostToolUse** (Feedback):
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{
          "type": "command",
          "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/format-code.sh"
        }]
      }
    ]
  }
}
```

**UserPromptSubmit** (Context Injection):
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [{
          "type": "command",
          "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/inject-context.py"
        }]
      }
    ]
  }
}
```

**SessionStart** (Setup):
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [{
          "type": "command",
          "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/load-agent-context.py"
        }]
      }
    ]
  }
}
```

**Hook script template** (Python):
```python
#!/usr/bin/env python3
import json
import sys

try:
    input_data = json.load(sys.stdin)

    # Access hook data
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Perform validation/processing
    # ...

    # Return result
    # Exit 0: Success
    # Exit 2: Block with stderr fed to Claude

    sys.exit(0)
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
```

#### 3.4 Write System Prompt

**File**: `.claude/agents/<agent-name>.md`

**Structure**:
```markdown
---
model: sonnet
description: <One-line agent purpose>
tools: [Tool1, Tool2, Tool3]
recommended-skills: [skill-name-1, skill-name-2]
---

**Project Context**: Read `.project-context.md` in the project root for project-specific information including <agent-relevant-items>.

# <Agent Name>

## Available Resources

**Shared Reference Docs** (`docs/agents/shared-ref-docs/`):
- [doc-name.md](docs/agents/shared-ref-docs/doc-name.md) - Description
- [another-doc.md](docs/agents/shared-ref-docs/another-doc.md) - Description

**Agent-Specific Resources**:
- Ref-docs: None  # Or list specific files in docs/agents/<agent-name>/ref-docs/
- Scripts: None   # Or list specific files

## Mission
[Clear statement of agent's purpose]

## Responsibilities

### ✅ THIS AGENT DOES
- [Specific responsibility 1]
- [Specific responsibility 2]

### ❌ THIS AGENT DOES NOT
- [What agent should not do]
- [Delegation pattern]

## Workflow

### Standard Process
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Coordination

**Delegates to**:
- Agent X: For [purpose]
- Agent Y: For [purpose]

**Receives from**:
- Agent A: [What they provide]

## Critical Constraints
- [Constraint 1]
- [Constraint 2]

## Decision-Making Protocol

**Act decisively (no permission)** when:
- [Scenario 1]
- [Scenario 2]

**Ask for permission** when:
- [Scenario 1]
- [Scenario 2]
```

## Agent Frontmatter Field Constraints

### name (Required)

**Constraints**:
- Maximum 64 characters
- Must contain only lowercase letters, numbers, and hyphens
- Cannot contain XML tags
- Cannot contain reserved words: "anthropic", "claude"

**Examples**: `code-reviewer`, `processing-pdfs`, `analyzing-spreadsheets`, `managing-databases`

### description (Required)

**Constraints**:
- Must be non-empty
- Maximum 1024 characters
- Cannot contain XML tags
- Should describe what the agent does and when to use it

**Best practice**: Always write in third person. Include both what the agent does and specific triggers/contexts for when to use it.

**Good example**:
```
description: Expert code reviewer. Use proactively after code changes to catch bugs, suggest improvements, and ensure code quality standards.
```

### tools (Optional)

**Behavior**:
- If omitted: inherits all tools from the main thread (default)
- If specified: comma-separated list of specific tools

**Format**: `tool1, tool2, tool3`

**Example**:
```yaml
tools: Read, Grep, Glob, Bash
```

**Common tool patterns**:
- Research: `Read, Glob, Grep, WebSearch, WebFetch, mcp__ref__*, mcp__exasearch__*`
- Backend Implementation: `Read, Write, Edit, Bash, Glob, Grep`
- Frontend Implementation: `Read, Write, Edit, Bash, Glob, Grep`
- DevOps: `Read, Write, Edit, Bash, Glob, Grep`
- QA/Testing: `Read, Bash, Glob, Grep`
- Tracking: `Read, Write, Bash, mcp__linear-server__*, mcp__github__*`

### model (Optional)

**Allowed values**:
- `sonnet` - Claude 3.5 Sonnet (default for sub-agents)
- `opus` - Claude 3 Opus
- `haiku` - Claude 3 Haiku
- `'inherit'` - Use the same model as the main conversation

**Default**: If omitted, uses `sonnet`

**Example**:
```yaml
model: sonnet
```

### Complete Valid Example

```yaml
---
name: code-reviewer
description: Expert code reviewer. Use proactively after code changes to catch bugs, suggest improvements, and ensure code quality standards.
tools: Read, Grep, Glob, Bash
model: sonnet
---
```

### Invalid Examples

**❌ Wrong: Name with uppercase**
```yaml
name: Code-Reviewer  # Must be lowercase-with-hyphens
```

**❌ Wrong: Reserved word**
```yaml
name: claude-reviewer  # Cannot contain "claude"
```

**❌ Wrong: Missing description**
```yaml
---
name: code-reviewer
tools: Read, Bash
---
```

**❌ Wrong: Extra forbidden fields**
```yaml
---
name: code-reviewer
description: Reviews code
domain: Development  # Forbidden field
version: 1.0         # Forbidden field
---
```

**❌ Wrong: Tools without key**
```yaml
---
name: code-reviewer
description: Reviews code
Read, Bash, Grep  # Missing "tools:" key
---
```

**Anthropic principles to follow**:
1. **Right altitude**: Specific guidance without hardcoded logic
2. **Clear sections**: Use headers/XML tags for organization
3. **Minimal to start**: Add based on failure modes
4. **Examples over rules**: Show canonical examples
5. **Avoid assumptions**: Make implicit context explicit

#### 3.5 Configure MCP Tools (if needed)

**When to use MCPs**:
- Agent needs external service integration (Linear, GitHub, Supabase)
- Third-party APIs required for agent function
- Specialized capabilities (web search, documentation lookup, code review)

**Available MCPs**:

**Project Management & Development**:
- **Linear** (`mcp__linear-server__*`) - Issue tracking, project management
- **GitHub** (`mcp__github__*`) - Repository operations, PRs, issues, workflows
- **Code Reviewer** (`mcp__claude-reviewer__*`) - Automated code review sessions

**Data & Infrastructure**:
- **Supabase** (`mcp__supabase__*`) - Database, auth, edge functions, migrations

**Research & Search**:
- **Exa Search** (`mcp__exasearch__*`) - Web search, company research, deep researcher
- **Ref** (`mcp__ref__*`) - Documentation search and retrieval
- **Perplexity** (`mcp__perplexity-ask__*`) - AI-powered research and Q&A

**Problem Solving**:
- **Sequential Thinking** (`mcp__BetterST__*`) - Complex multi-step reasoning

**MCP Server Configuration** (handled by Claude Code settings):

MCPs are configured in `~/.claude/settings.json` or project `.claude/settings.json`. The Traycer framework assumes MCPs are already configured by the user. Agents don't configure MCP servers—they just declare which MCP tools they use.

**In agent's YAML frontmatter, specify MCP tools needed**:

```yaml
---
model: sonnet
description: Agent that manages Linear issues and GitHub PRs
tools:
  - Read
  - Write
  - Edit
  - Bash
  # Linear MCP tools
  - mcp__linear-server__list_issues
  - mcp__linear-server__update_issue
  - mcp__linear-server__create_issue
  # GitHub MCP tools
  - mcp__github__create_pull_request
  - mcp__github__list_pull_requests
  - mcp__github__get_file_contents
recommended-skills: [skill-name-1, skill-name-2]
---
```

**In system prompt, document MCP tool usage**:

Add a section explaining when and how to use each MCP tool:

```markdown
## MCP Tools

### Linear Integration

**Issue Management**:
- `mcp__linear-server__list_issues` - Query issues with filters (team, assignee, state, labels)
  - Always filter by team to avoid cross-contamination
  - Example: `list_issues(team: "LAW", assignee: "me", state: "open")`

- `mcp__linear-server__update_issue` - Modify issue status, assignee, labels, description
  - Use for tracking work progress
  - Example: Mark issue as "In Progress" when starting work

- `mcp__linear-server__create_issue` - Create new issues for tracking work
  - Include team, title, description, labels
  - Link to parent issue if part of work block

**Critical constraints**:
- ALWAYS filter by team/project to prevent seeing wrong issues
- Read project-context.md for team/project IDs
- Never hardcode issue IDs in agent prompts

### GitHub Integration

**Repository Operations**:
- `mcp__github__get_file_contents` - Fetch file contents from repos
- `mcp__github__create_pull_request` - Create PRs programmatically
- `mcp__github__list_pull_requests` - Query PRs by state, filters

**Usage patterns**:
- Tracking agents use for PR creation after QA approval
- Action agents may read from repos for research
- Never push directly to main—always via PR

[Continue for other MCPs as needed...]
```

**Security & Best Practices**:

1. **API Keys**: Never reference API keys in agent prompts or scripts
   - MCPs are configured by user with env vars
   - Agents assume MCPs are available if listed in YAML frontmatter

2. **Tool Discovery**: List only tools agent actually needs
   - Don't use `mcp__linear-server__*` wildcard in production agent frontmatter (wildcards grant excessive permissions - use explicit tool listing for security and clarity)
   - Explicitly list each tool for clarity

3. **Documentation**: Explain tool usage constraints in system prompt
   - When to use each tool
   - Common parameters and patterns
   - Error handling approaches

4. **Testing**: Verify MCP tools work before deploying agent
   - Test with real API calls during evaluation phase
   - Handle MCP failures gracefully (tool may not be configured)

#### 3.7 Create Agent-Specific Reference Docs

**Location**: `docs/agents/<agent-name>/ref-docs/`

**Common ref docs**:
- `workflow-guide.md` - Detailed workflow steps
- `decision-matrix.md` - When to choose different approaches
- `examples.md` - Canonical examples
- `troubleshooting.md` - Common issues and solutions

**Keep concise**: If doc is for multiple agents, move to `shared-ref-docs/`

#### 3.7 Create Agent-Specific Scripts

**Location**: `docs/agents/<agent-name>/scripts/`

**For scripts that**:
- Are agent-specific (not reusable across agents)
- Don't fit within a skill
- Provide utility functions for agent operations

**Example**: `update-dashboard.py` for tracking agent's operations

### Phase 4: Integration & Updates

#### 4.1 Update Coordination Documents

**Files to update**:

1. **Other agent prompts** (if they delegate to this agent):
```markdown
## Available Agents

- **New Agent Name** (@new-agent-name): [Purpose]
  - Use for: [When to delegate]
  - Capabilities: [What it can do]
```

2. **Shared coordination guides**:
- `docs/agents/shared-ref-docs/agent-addressing-system.md`
- `docs/agents/shared-ref-docs/traycer-coordination-guide.md`

3. **Project context**:
- `.project-context.md` - Update "Active Agents" section

#### 4.2 Register Agent Alias (if applicable)

If agent has an @mention alias, document in:
- Coordination guides
- Agent's own prompt (how to invoke)
- Other agents that might delegate to it

### Phase 5: Testing & Iteration

#### 5.1 Create Evaluation Tasks

**Real-world tasks** that test:
- Core responsibilities
- Tool usage
- Error handling
- Coordination with other agents

**Good evaluation tasks**:
- Require multiple steps
- Test decision-making
- Cover edge cases
- Reflect actual use cases

**Example**:
```text
Task: Review PR #123 for security issues and code quality
Expected:
- Load PR diff
- Run security validation
- Check code standards
- Provide structured feedback
- Delegate fixes to Backend/Frontend/DevOps agents if needed
```

#### 5.2 Run Evaluations

**Process**:
1. Execute agent on evaluation tasks
2. Observe failures and confusion points
3. Read agent's reasoning (use extended thinking)
4. Analyze tool calls and responses
5. Identify areas for improvement

**Metrics to track**:
- Task completion rate
- Tool call efficiency
- Token consumption
- Error frequency
- Time to completion

#### 5.3 Iterate with Claude

**Collaborate with Claude to**:
- Analyze evaluation results
- Identify prompt improvements
- Refine tool descriptions
- Optimize hook configurations
- Improve skill instructions

**Use held-out test sets** to prevent overfitting

### Phase 6: Documentation & Handoff

#### 6.1 Create Agent README

**File**: `docs/agents/<agent-name>/README.md`

```markdown
# <Agent Name>

## Purpose
[What this agent does]

## When to Use
[Scenarios where you'd invoke this agent]

## Quick Start

### Prerequisites
- [Any setup required]

### Invocation
```text
@agent-name [task description]
```

## Capabilities
- [Capability 1]
- [Capability 2]

## Examples

### Example 1: [Use Case]
```text
User: [Request]
Agent: [Response pattern]
```

## Configuration

### Skills Used
- `skill-name`: [Purpose]

### Commands Available
- `/command-name`: [Purpose]

### Hooks Enforced
- PreToolUse: [What's validated]
- PostToolUse: [What feedback is provided]

## Coordination

### Delegates To
- Agent X: [When and why]

### Receives From
- Agent Y: [What work items]

## Troubleshooting

### Issue: [Common problem]
**Symptom**: [What you see]
**Solution**: [How to fix]
```

#### 6.2 Update Team Documentation

**Agent capabilities matrix**:
```markdown
| Agent | Purpose | Skills | Commands | Coordinates With |
|-------|---------|--------|----------|------------------|
| New Agent | [Purpose] | skill-1, skill-2 | /cmd-1, /cmd-2 | Agent-X, Agent-Y |
```

**Workflow diagrams**: Update if agent changes workflows

### Phase 7: Deployment

**Goal**: Deploy newly created agent to `.claude/agents/` and verify availability.

#### 7.1 Deploy Agent File

**Action**: Copy agent file to deployment location.

**Implementation**:
```bash
# Source location (created in Phase 3.4)
SOURCE_FILE="docs/agents/<agent-name>/<agent-name>-agent.md"

# Target location
TARGET_FILE=".claude/agents/<agent-name>-agent.md"

# Verify source exists
if [[ ! -f "$SOURCE_FILE" ]]; then
  echo "❌ Source file not found: $SOURCE_FILE"
  exit 1
fi

# Create target directory if missing
mkdir -p ".claude/agents"

# Deploy with permission preservation
cp -p "$SOURCE_FILE" "$TARGET_FILE"
```

**Verification**:
- File exists at `.claude/agents/<agent-name>-agent.md`
- File permissions preserved (should be readable)
- File content matches source (use `cmp -s` to verify)

```bash
# Verify deployment
if cmp -s "$SOURCE_FILE" "$TARGET_FILE"; then
  echo "✅ Agent file deployed successfully"
else
  echo "❌ Content mismatch after deployment"
  exit 1
fi
```

#### 7.2 Update Documentation Registry

**Action**: Update `docs/agents/README.md` with new agent entry.

**If README.md doesn't exist, create with template**:
```markdown
# Traycer Enforcement Framework - Agents

This directory contains agent system prompts and supporting resources for the Traycer Enforcement Framework.

## Deployed Agents

| Agent | File | Purpose | Status |
|-------|------|---------|--------|
| Frontend Agent | `frontend-agent.md` | Implements UI/UX components and client-side logic | ✅ Deployed |
| Backend Agent | `backend-agent.md` | Implements API endpoints and database operations | ✅ Deployed |
| DevOps Agent | `devops-agent.md` | Manages infrastructure and deployment operations | ✅ Deployed |

## Agent Directory Structure

Each agent has a directory at `docs/agents/<agent-name>/` containing:
- `<agent-name>-agent.md` - System prompt with YAML frontmatter
- `ref-docs/` - Agent-specific reference documents (optional)
- `scripts/` - Agent-specific utility scripts (optional)
- `README.md` - Agent documentation and usage guide

## Shared Resources

- `shared-ref-docs/` - Reference documents shared across multiple agents
- `documentation-validator/` - Agent for validating documentation quality

## Adding New Agents

New agents are created using the `agent-builder` skill, which handles:
1. Requirements analysis
2. Architecture design
3. Component creation (prompts, skills, commands, hooks)
4. Integration and testing
5. Documentation
6. Deployment to `.claude/agents/`
```

**If README.md exists, append new row**:
- Extract agent name from filename (e.g., `researcher-agent.md` → "Researcher Agent")
- Extract purpose from YAML frontmatter `description` field
- Insert row in table, maintaining alphabetical order by agent name

**Sort order**: Alphabetical by agent name for maintainability.

**Example**:
```markdown
| Research Agent | `researcher-agent.md` | Gathers information and provides technical research | ✅ Deployed |
```

#### 7.3 Run Verification

**Action**: Invoke bootstrap script verification for the newly deployed agent.

**Command**:
```bash
# Run verification function from bootstrap script
cd "$PROJECT_ROOT"
bash scripts/tef_bootstrap.sh --dry-run --local 2>&1 | grep -A 5 "Component Count Verification"
```

**Expected Output**:
```
=== Component Count Verification ===
  - Agents: 13  # Should increment by 1 from previous count
  - Skills: <count>
  - Commands: <count>
  - Hooks: <count>
```

**Verification Checklist**:
- [ ] Agent count increased by 1
- [ ] No warnings about missing files
- [ ] No errors in verification output
- [ ] New agent file appears in `find .claude/agents -name "*-agent.md"` output

#### 7.4 Confirm Deployment

**Action**: Report deployment success with summary.

**Output Format**:
```markdown
## Phase 7: Deployment - Complete ✅

**Agent Deployed**: <agent-name>-agent.md
**Deployment Location**: .claude/agents/<agent-name>-agent.md
**Documentation Updated**: docs/agents/README.md

**Verification Results**:
- ✅ Agent file copied successfully
- ✅ Permissions preserved (readable)
- ✅ Content matches source (cmp verified)
- ✅ Documentation registry updated
- ✅ Bootstrap verification passed
- ✅ Agent count: <new count>

**Next Steps**:
1. Restart Claude Code to load new agent
2. Test agent with: `@<agent-name> <test task>`
3. Review agent behavior and iterate if needed
```

#### 7.5 Optional: Skip Deployment

**Flag**: `--no-deploy`

**Behavior**: If `--no-deploy` flag provided to agent-builder skill, skip Phase 7 entirely.

**Use Cases**:
- Creating agent for different project (not current repo)
- Testing agent architecture without deployment
- Manual deployment preferred
- Deployment to custom location (not `.claude/`)

**Implementation**:

Add to skill frontmatter:
```yaml
argument-hint: [agent-requirements] [--no-deploy]
```

Parse arguments for `--no-deploy` flag:
- If flag present: Execute Phases 1-6 normally, skip Phase 7 (show skip message)
- If flag absent: Execute all Phases 1-7

**Skip Message** (when `--no-deploy` provided):
```markdown
## Phase 7: Deployment - Skipped ⏭️

**Reason**: --no-deploy flag provided

**Agent Created**: docs/agents/<agent-name>/<agent-name>-agent.md

**Manual Deployment**:
To deploy this agent manually:
1. Copy agent file: `cp docs/agents/<agent-name>/<agent-name>-agent.md .claude/agents/`
2. Update docs/agents/README.md with new agent entry
3. Verify: `bash scripts/tef_bootstrap.sh --dry-run --local`
4. Restart Claude Code to load agent
```

---

## Phase 8: Audit Mode (Validation)

**Purpose**: Validate existing agents for compliance with TEF standards

**When to Use**: After agent creation/modification, before deployment, or in CI/CD pipelines

**Command Pattern**:
```bash
/agent-builder --audit [--agent <name>] [--format json|markdown] [--verbose]
```

**Flags**:
- `--audit`: Enable audit mode (skips creation workflow)
- `--agent <name>`: Audit single agent (default: all agents in `.claude/agents/`)
- `--format json|markdown`: Report output format (default: markdown)
- `--verbose`: Show full compliance details for each check

---

### 8.1: Audit Workflow

**Steps**:
1. Read agent files from `.claude/agents/`
2. Run compliance checks (see 8.2)
3. Generate report (markdown or JSON)
4. Provide remediation guidance for failures
5. Exit with status code (0 = all pass, 1 = warnings, 2 = failures)

**Example Usage**:
```bash
# Audit all agents
/agent-builder --audit

# Audit single agent
/agent-builder --audit --agent backend-agent

# Audit with JSON output for CI/CD
/agent-builder --audit --format json > audit-report.json
```

---

### 8.2: Compliance Checks

Agent-builder audit mode validates 5 compliance criteria:

#### Check 1: No Duplicate YAML Frontmatter (CRITICAL)

**Criteria**: Agent file must have exactly ONE YAML frontmatter block
**Implementation**:
1. Read agent file line-by-line
2. Count occurrences of `---` (YAML delimiter) in first 20 lines
3. **PASS**: Exactly 2 occurrences (opening line 1, closing line ~6)
4. **FAIL**: More than 2 occurrences (duplicate blocks detected)

**Example**:
```
❌ FAIL: backend-agent.md - Duplicate YAML frontmatter detected (4 delimiters found, expected 2)
✅ PASS: frontend-agent.md - Single YAML frontmatter block (2 delimiters)
```

**Remediation**: Remove duplicate YAML blocks, merge fields into first block if needed

---

#### Check 2: YAML Frontmatter Completeness (REQUIRED)

**Criteria**: Agent YAML frontmatter must contain all required fields
**Required Fields**:
- `model: <model-id>` (e.g., `sonnet`)
- `description: <string>` (one-line agent description)
- `tools: [...]` (array of tool names, can be empty)
- `recommended-skills: [...]` (array of skill names, can be empty)

**Implementation**:
1. Parse YAML frontmatter (first block only, ignore duplicates)
2. Verify presence of each required field
3. **PASS**: All 4 fields present
4. **WARN**: Optional fields found in duplicate block (e.g., `friendly_name`)
5. **FAIL**: Missing any required field

**Example**:
```
✅ PASS: backend-agent.md - All required YAML fields present
❌ FAIL: example-agent.md - Missing required field: allowed-tools
⚠️  WARN: devops-agent.md - Optional field 'friendly_name' in duplicate block
```

**Remediation**: Add missing fields to YAML frontmatter

---

#### Check 3: Project Context Reference (REQUIRED)

**Criteria**: Agent prompt must reference `.project-context.md`
**Implementation**:
1. Search agent file for pattern: `**Project Context**:.*\.project-context\.md`
2. **PASS**: Pattern found anywhere in file
3. **FAIL**: Pattern not found

**Example**:
```
✅ PASS: researcher-agent.md - Project context reference found
❌ FAIL: example-agent.md - No project context reference found
```

**Remediation**: Add project context snippet to agent prompt (see agent-builder Phase 3.1 template)

---

#### Check 4: Valid Ref-Docs Path References (OPTIONAL)

**Criteria**: If agent references ref-docs, paths must exist
**Implementation**:
1. Extract ref-doc references from agent file (pattern: `docs/agents/<agent>/ref-docs/*.md` or `docs/agents/<agent>-agent/ref-docs/*.md`)
2. For each reference, verify file exists on disk
3. Check if agent has ref-docs directory (either `docs/agents/<agent>/ref-docs/` or `docs/agents/<agent>-agent/ref-docs/`)
4. **PASS**: All referenced paths exist OR no ref-doc references found
5. **WARN**: Agent has `ref-docs/` directory but no files in it
6. **FAIL**: Agent references non-existent ref-doc file

**Example**:
```
✅ PASS: documentation-validator.md - All ref-docs exist
⚠️  WARN: action-agent.md - ref-docs directory empty (docs/agents/action-agent/ref-docs/)
❌ FAIL: example-agent.md - Referenced ref-doc not found: docs/agents/example/ref-docs/missing.md
```

**Remediation**: Create missing ref-docs or remove references from agent prompt

---

#### Check 5: Valid Scripts Path References (OPTIONAL)

**Criteria**: If agent references scripts, paths must exist and be executable
**Implementation**:
1. Extract script references from agent file (pattern: `docs/agents/<agent>/scripts/*.sh` or similar)
2. For each reference, verify:
   - File exists on disk
   - File is executable (`-x` permission)
3. **PASS**: All referenced scripts exist and are executable OR no script references found
4. **WARN**: Script exists but is not executable (missing `chmod +x`)
5. **FAIL**: Agent references non-existent script

**Example**:
```
✅ PASS: documentation-validator.md - All scripts exist and executable
⚠️  WARN: example-agent.md - Script not executable: docs/agents/example/scripts/validate.sh
❌ FAIL: example-agent.md - Referenced script not found: docs/agents/example/scripts/missing.sh
```

**Remediation**: Create missing scripts or fix permissions (`chmod +x script.sh`)

---

### 8.3: Report Format

#### Markdown Report (Default)

```markdown
# Agent Audit Report

**Date**: 2025-11-03
**Audited Agents**: 12
**Overall Status**: ⚠️ WARNINGS (5 agents have issues)

---

## Summary

| Status | Count | Agents |
|--------|-------|--------|
| ✅ PASS | 8 | frontend-agent, backend-agent, devops-agent, qa-agent, researcher-agent, planning-agent, tracking-agent, browser-agent |
| ⚠️ WARN | 0 | (none) |
| ❌ FAIL | 4 | debug-agent, seo-agent, traycer-agent, software-architect |

---

## Detailed Results

### ❌ FAIL: backend-agent.md

**Issues**:
- ❌ Check 1: Duplicate YAML frontmatter (4 delimiters, expected 2)

**Remediation**:
Remove duplicate YAML block (lines 8-11). Merge `delegated_by` and `friendly_name` into first block if needed.

---

### ✅ PASS: backend-agent.md

**Status**: All checks passed
- ✅ Check 1: Single YAML frontmatter block
- ✅ Check 2: All required fields present (model, description, allowed-tools, recommended-skills)
- ✅ Check 3: Project context reference found
- ✅ Check 4: All ref-docs valid
- ✅ Check 5: No script references

---

[... repeat for all agents ...]
```

#### JSON Report (For CI/CD)

```json
{
  "audit_date": "2025-11-03",
  "total_agents": 12,
  "overall_status": "WARNINGS",
  "summary": {
    "pass": 7,
    "warn": 0,
    "fail": 5
  },
  "agents": [
    {
      "filename": "backend-agent.md",
      "status": "FAIL",
      "checks": {
        "no_duplicate_yaml": {
          "status": "FAIL",
          "message": "Duplicate YAML frontmatter (4 delimiters, expected 2)",
          "severity": "CRITICAL",
          "line_numbers": [1, 6, 8, 11]
        },
        "yaml_completeness": {
          "status": "PASS",
          "message": "All required fields present"
        },
        "project_context": {
          "status": "PASS",
          "message": "Project context reference found"
        },
        "ref_docs_valid": {
          "status": "WARN",
          "message": "ref-docs directory exists but is empty",
          "path": "docs/agents/backend-agent/ref-docs/"
        },
        "scripts_valid": {
          "status": "PASS",
          "message": "No script references found"
        }
      },
      "remediation": "Remove duplicate YAML block (lines 8-11)"
    }
  ]
}
```

---

### 8.4: Pass/Fail/Warning Criteria

**FAIL Criteria** (blocks agent deployment, exit code 2):
- Duplicate YAML frontmatter detected (Check 1)
- Missing required YAML field (Check 2)
- No project context reference found (Check 3)
- Agent references non-existent ref-doc or script file (Checks 4-5)

**WARN Criteria** (informational, exit code 1):
- Agent has ref-docs directory but it's empty (Check 4)
- Script exists but is not executable (Check 5)
- Optional YAML fields in duplicate block (Check 2)

**PASS Criteria** (exit code 0):
- Single YAML frontmatter block (Check 1)
- All required fields present (Check 2)
- Project context reference exists (Check 3)
- All referenced paths exist and are valid (Checks 4-5) OR no references made

---

### 8.5: CI/CD Integration

**GitHub Actions Example**:

```yaml
name: Agent Compliance Audit

on:
  pull_request:
    paths:
      - '.claude/agents/**'
      - 'docs/agents/**'

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run agent audit
        run: |
          claude-code run "/agent-builder --audit --format json" > audit-report.json

      - name: Check audit status
        run: |
          status=$(jq -r '.overall_status' audit-report.json)
          if [ "$status" == "FAIL" ]; then
            echo "❌ Agent audit failed"
            exit 1
          elif [ "$status" == "WARNINGS" ]; then
            echo "⚠️  Agent audit has warnings"
            exit 0
          else
            echo "✅ Agent audit passed"
            exit 0
          fi

      - name: Post audit report as comment
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const report = JSON.parse(fs.readFileSync('audit-report.json', 'utf8'));
            // Format and post as PR comment
```

---

### 8.6: Known Limitations

**Deferred Check**:
- **Check 6 (Filename-Directory Matching)**: Not implemented due to mixed naming patterns
  - Legacy agents use old directories (e.g., `backend/`, `frontend/`)
  - Canonical agents use `*-agent/` directories (e.g., `backend-agent/`, `frontend-agent/`)
  - Will be enabled once legacy migration is complete

**Future Enhancements**:
- Auto-remediation (`--fix` flag to auto-repair common issues)
- Ref-docs linting (validate Markdown syntax, check internal links)
- Code example validation (verify bash/Python snippets are syntactically valid)

---

## Best Practices (Anthropic Guidance)

### 1. Context Engineering

**Treat context as finite resource**:
- Every token depletes "attention budget"
- Good context = smallest set of high-signal tokens
- Progressive disclosure for skills

**System prompt altitude**:
- Not too prescriptive (hardcoded logic)
- Not too vague (assumes context)
- Specific guidance + flexible heuristics

**Just-in-time retrieval**:
- Load data dynamically using tools
- Maintain lightweight identifiers (paths, IDs)
- Leverage metadata (folders, timestamps)

### 2. Tool Design

**Choose tools intentionally**:
- More tools ≠ better outcomes
- Each tool: clear, distinct purpose
- Consolidate related operations
- If human can't pick tool, agent can't either

**Return meaningful context**:
- Prioritize relevance over flexibility
- Natural language > cryptic IDs
- Token-efficient responses
- Consider `response_format` enum

**Excellent descriptions**:
- Explain like to new hire
- Make implicit context explicit
- Unambiguous parameters
- Small refinements = big improvements

### 3. Skills Architecture

**Keep skills focused**:
- One capability per skill
- "PDF form filling" not "Document processing"

**Clear descriptions**:
- What skill does + when to use it
- Include specific triggers
- Example: "Use when working with Excel files, .xlsx format"

**Progressive disclosure**:
1. Metadata (always loaded)
2. SKILL.md body (when triggered)
3. Resources (as needed)

### 4. Hooks for Enforcement

**Use hooks for deterministic control**:
- Don't rely on prompting for critical rules
- Hooks always execute vs agent choice

**Hook event selection**:
- PreToolUse: Validation, blocking
- PostToolUse: Feedback, formatting
- UserPromptSubmit: Context injection, validation
- SessionStart: Setup, environment loading

**Security**:
- Hooks run with your credentials
- Review scripts before registering
- Quote shell variables: `"$VAR"`
- Block path traversal
- Use absolute paths

### 5. Production Checklist

Before deploying agent:

**Phase 1-6 Verification**:
- [ ] Agent file created at `docs/agents/<name>/<name>-agent.md`
- [ ] YAML frontmatter contains all required fields (model, description, allowed-tools, recommended-skills)
- [ ] YAML frontmatter validates successfully (valid syntax)
- [ ] Project context snippet present immediately after frontmatter
- [ ] Available Resources section populated (Shared + Agent-Specific)
- [ ] System prompt at right altitude
- [ ] Tools have clear names and descriptions
- [ ] Skills use progressive disclosure
- [ ] Commands tested with arguments
- [ ] Hooks enforce critical rules
- [ ] Evaluation covers real-world tasks
- [ ] Security review complete
- [ ] No hardcoded secrets
- [ ] Paths are repo-relative
- [ ] Coordination documented
- [ ] Team documentation updated
- [ ] MCP tools listed in frontmatter (explicit, not wildcards)
- [ ] MCP tool usage documented in system prompt
- [ ] MCP tool constraints explained (filters, parameters)
- [ ] MCP error handling defined
- [ ] MCP tools tested with real API calls

**Phase 7 Deployment Verification**:
- [ ] Agent file deployed to `.claude/agents/<name>-agent.md`
- [ ] File permissions preserved (readable)
- [ ] Content matches source (`cmp -s` verification passed)
- [ ] `docs/agents/README.md` updated with new agent entry
- [ ] Agent appears in alphabetical order in README.md table
- [ ] Agent description extracted from YAML frontmatter
- [ ] Bootstrap verification passed (no errors or warnings)
- [ ] Agent count incremented by 1 in verification output
- [ ] New agent file appears in `find .claude/agents -name "*-agent.md"` output
- [ ] If `--no-deploy` flag used: Manual deployment instructions provided

**Phase 8: Audit** - Run compliance audit
- [ ] Run: `/agent-builder --audit --agent <agent-name>`
- [ ] All checks PASS (no FAIL status)
- [ ] Warnings reviewed and acceptable
- [ ] JSON report generated: `/agent-builder --audit --agent <agent-name> --format json`

## Integration with Other Skills

**Agent Builder orchestrates**:

```text
Agent Requirements
        ↓
Agent Builder Skill
        ├→ [Reusable patterns identified]
        │  └→ Calls: Skill Creator Skill
        │     └→ Creates: docs/skills/<skill>/
        │
        ├→ [Explicit operations identified]
        │  └→ Calls: Command Creator Skill
        │     └→ Creates: .claude/commands/<cmd>.md
        │
        └→ [Assembles complete agent]
           ├→ Creates: .claude/agents/<name>.md (single file with YAML frontmatter)
           ├→ Creates: docs/agents/<name>/ref-docs/ (if needed)
           ├→ Configures: .claude/settings.json (hooks)
           └→ Updates: Coordination docs
```

**What Agent Builder decides**:
- System prompt (agent-specific logic)
- Skills (reusable workflows)
- Commands (explicit prompts)
- Hooks (enforcement rules)
- Tools (capabilities needed)
- Ref docs (supporting documentation)

## Common Patterns

### Pattern 1: Validation Agent

**Components**:
- **System prompt**: Define validation rules and process
- **Skills**: `validation-protocol` (multi-step validation)
- **Commands**: `/validate-file`, `/validate-pr`
- **Hooks**:
  - PreToolUse: Block invalid operations
  - PostToolUse: Auto-format after edits
- **Tools**: Read, Grep, Glob (read-only)

**Example**: QA Agent

### Pattern 2: Implementation Agent

**Components**:
- **System prompt**: Execute implementation work for specific domain (frontend/backend/devops)
- **Skills**: Domain-specific implementation patterns
- **Commands**: Domain-specific commands (e.g., `/deploy`, `/build`, `/api-test`)
- **Hooks**:
  - PreToolUse: Validate domain boundaries (backend can't touch frontend/*)
  - SessionStart: Load project context
- **Tools**: Read, Write, Edit, Bash, Glob, Grep (domain-scoped)

**Examples**: Backend Agent, Frontend Agent, DevOps Agent

### Pattern 3: Execution Agent

**Components**:
- **System prompt**: Execute instructions verbatim
- **Skills**: Minimal (focused execution)
- **Commands**: `/git-commit`, `/linear-update`
- **Hooks**:
  - SessionStart: Load environment
  - PreToolUse: Validate parameters
- **Tools**: Full access (Write, Edit, Bash, Linear MCP)

**Example**: Tracking Agent

### Pattern 4: Coordination Agent

**Components**:
- **System prompt**: Delegate to specialists, never execute
- **Skills**: `delegation-protocol`, `work-breakdown`
- **Commands**: `/delegate`, `/status`
- **Hooks**:
  - UserPromptSubmit: Parse work requests
  - Stop: Update progress tracking
- **Tools**: Task (subagents), Linear (read-only)

**Example**: Traycer

### Pattern 5: Research Agent

**Components**:
- **System prompt**: Gather evidence, analyze options
- **Skills**: `research-methodology`, `citation-standards`
- **Commands**: `/deep-research`, `/compare-options`
- **Hooks**:
  - SessionStart: Load research context
  - PostToolUse: Log sources consulted
- **Tools**: WebSearch, WebFetch, Read, MCP tools

### Pattern 6: Integration Agent (with MCPs)

**Components**:
- **System prompt**: Document MCP tool usage, constraints, error handling
- **Skills**: `api-integration-protocol`, `error-recovery`
- **Commands**: `/sync-linear`, `/create-pr`, `/search-docs`
- **Hooks**:
  - PreToolUse: Validate MCP parameters (team filters, required fields)
  - PostToolUse: Log API calls for debugging
  - SessionStart: Verify MCP availability
- **Tools**: MCP tools (Linear, GitHub, Supabase, etc.) + Read, Grep
- **Config**: Explicitly list MCP tools needed

**Example Agents**:
- **Tracking Agent**: Uses Linear MCP for issue updates, GitHub MCP for PRs
- **Research Agent**: Uses Exa Search MCP for web research, Ref MCP for docs
- **Database Agent**: Uses Supabase MCP for migrations and queries

**Critical patterns**:
- Always filter Linear queries by team/project
- Handle MCP unavailability gracefully
- Document required MCP configuration in agent README
- Test with real APIs during evaluation phase

## Troubleshooting Agent Creation

### Issue: Agent ignores instructions

**Symptom**: Agent doesn't follow system prompt

**Causes**:
- Prompt too vague (lacks concrete signals)
- Prompt too prescriptive (hardcoded logic)
- Missing examples

**Solutions**:
1. Add canonical examples
2. Increase specificity without hardcoding
3. Use clear section headers
4. Test with edge cases

### Issue: Agent calls wrong tools

**Symptom**: Agent uses inappropriate tools

**Causes**:
- Overlapping tool functionality
- Unclear tool descriptions
- Tool names ambiguous

**Solutions**:
1. Consolidate overlapping tools
2. Improve tool descriptions (explain to new hire)
3. Use namespacing (prefixes/suffixes)
4. Show examples in descriptions

### Issue: Agent runs out of context

**Symptom**: Context window fills up

**Causes**:
- Verbose tool responses
- Loading unnecessary skills
- No progressive disclosure

**Solutions**:
1. Implement token-efficient tools
2. Use progressive disclosure in skills
3. Add pagination/filtering to tools
4. Configure auto-compaction
5. Use structured note-taking

### Issue: Hooks not enforcing rules

**Symptom**: Agent bypasses validation

**Causes**:
- Hooks not registered correctly
- Matcher pattern wrong
- Hook script errors

**Solutions**:
1. Check hooks in settings.json
2. Test matcher patterns
3. Run `claude --debug` to see hook execution
4. Verify script permissions (`chmod +x`)
5. Test hook script independently

### Issue: Skills not triggering

**Symptom**: Agent doesn't use skill

**Causes**:
- Description too generic
- YAML syntax errors
- Skill in wrong location

**Solutions**:
1. Make description specific (what + when)
2. Validate YAML frontmatter
3. Check file location (.claude/skills/ or ~/.claude/skills/)
4. Test with explicit mention of skill purpose

## Quick Reference

**Creating agents**:
1. Analyze requirements
2. Design architecture (prompt, tools, skills, commands, hooks)
3. Create components (call sub-skills as needed)
4. Write system prompt with YAML frontmatter
5. Set up hooks
6. Create documentation
7. Run evaluations
8. Iterate
9. Update coordination docs

**File locations**:
- Agent file: `.claude/agents/<name>.md` (single file with frontmatter)
- Agent ref docs: `docs/agents/<name>/ref-docs/` (if agent-specific)
- Shared ref docs: `docs/agents/shared-ref-docs/` (for multi-agent resources)
- Skills: `docs/skills/<skill-name>/`
- Commands: `.claude/commands/<cmd>.md`
- Hooks: `.claude/settings.json`

**Anthropic principles**:
- Context is finite - use wisely
- Right altitude in prompts
- Tools: clear, distinct, consolidated
- Skills: focused, clear descriptions, progressive disclosure
- Hooks: deterministic enforcement
- Evaluate with real-world tasks

## Resources

For detailed best practices, see `references/agent-development-guide.md`:
- Complete agent architecture examples
- Evaluation methodology
- Hook patterns and examples
- Skill vs command decision trees
- Common anti-patterns to avoid
