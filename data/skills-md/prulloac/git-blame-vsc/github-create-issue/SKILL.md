---
name: github-create-issue
description: Create GitHub issues with intelligent template matching and tool selection. Automatically detects and applies issue templates from .github/ISSUE_TEMPLATE directory using smart matching. Leverages tools in order of precedence (GitHub MCP Server → GitHub CLI → REST API). Use when you need to create a new GitHub issue, optionally with labels, assignees, milestones, or project assignment. The skill handles template matching intelligently—when multiple templates exist, it analyzes the issue description to suggest the best template, asking for clarification only when ambiguous.
---

# GitHub Create Issue Skill

Create GitHub issues using the best available tool with intelligent template matching.

## When to Use This Skill

Use this skill when you need to:
- Create a new GitHub issue in the current repository
- Apply matching issue templates from `.github/ISSUE_TEMPLATE/`
- Add metadata like labels, assignees, milestones, or projects
- Automatically determine the right tool (MCP Server, CLI, or REST API)

## Quick Start

### Basic Issue Creation
```
Create a GitHub issue titled "App crashes on startup" with body "The app crashes immediately after launching on Windows 10"
```

The skill will:
1. Check for available templates matching "crashes on startup"
2. Suggest bug template if available
3. Create the issue using the best available tool

### With Metadata
```
Create a GitHub issue titled "Add dark mode support" labeled as "enhancement,ui" assigned to @sarah with the feature template
```

## Workflow

### Phase 1: Template Detection
The skill scans `.github/ISSUE_TEMPLATE/` for available templates:
- Supports `.md` (Markdown) and `.yml`/`.yaml` (YAML) formats
- Extracts template names, metadata, and content
- Works with any template structure or naming convention

### Phase 2: Intelligent Matching
When issue description is provided, the skill matches it to templates:
- Extracts meaningful keywords from each template's filename and metadata
- Scores templates based on keyword overlap with issue description
- Auto-selects template if one clearly matches (score significantly higher than others)
- Presents all available options to user if scores are ambiguous or no clear match

This approach works with any template type—templates are matched by their own names and metadata, not by predefined issue categories.

### Phase 3: Issue Creation
Uses tools in order of precedence:
1. **GitHub MCP Server** (when in Claude context with GitHub tools available)
2. **GitHub CLI** (`gh` command, requires authentication)
3. **GitHub REST API** (requires `GITHUB_TOKEN` environment variable)

The skill attempts each tool until one succeeds.

## Tool Selection Details

### GitHub CLI (gh)
**Best for**: Interactive workflows, local development, pre-existing auth

**Requirements**:
- `gh` command installed
- Authenticated via `gh auth login`

**Supports**: title, body, labels, assignees, milestone

### GitHub REST API
**Best for**: CI/CD, automation, programmatic access

**Requirements**:
- `GITHUB_TOKEN` or `GH_TOKEN` environment variable
- Token must have `repo` scope

**Supports**: title, body, labels, assignees, milestone

**Note**: Projects require a separate API call after issue creation

### GitHub MCP Server
**Best for**: Integrated Claude workflows

**Requirements**: Claude with GitHub MCP Server enabled

**Supports**: All fields including projects

## Template Format Examples

### Markdown Template
```markdown
---
name: Bug Report
title: "[Bug]: "
description: "Report a bug"
labels: ["bug"]
---

## Describe the bug
[Description here]

## Steps to reproduce
1. Step one
2. Step two
```

### YAML Template
```yaml
name: Feature Request
description: Suggest an enhancement
labels: ["enhancement"]
assignees: ["lead-dev"]
```

## Configuration

### Environment Variables

```bash
# GitHub CLI authentication (handled by gh auth login)
# No manual setup needed

# REST API authentication
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
# or
export GH_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

### Repository Detection

The skill automatically detects:
- Repository owner and name from git remote URL
- Current directory as repository root (can be overridden)

## Common Scenarios

### Scenario 1: Simple Template Matching
**User Input**: "Create issue: App won't start on macOS"

**Flow**:
1. Finds all templates in `.github/ISSUE_TEMPLATE/`
2. Scores templates by keyword match (looks for words in template names/metadata)
3. If strong match found (e.g., template named "bug-report"), suggests it
4. Creates issue with selected template

### Scenario 2: Multiple Equally Relevant Templates
**User Input**: "New feature: support environment variables"

**Flow**:
1. Finds multiple templates that could apply
2. Displays options: "Which template? 1) Enhancement 2) Feature Request 3) Other"
3. Uses selected template
4. Creates issue

### Scenario 3: Custom Template Types
**User Input**: "Create issue for security concern"

**Flow**:
1. Finds templates including custom ones (e.g., "security-disclosure", "vulnerability-report")
2. Matches based on template name and metadata
3. Suggests best match or presents options
4. Creates issue with matched template

### Scenario 4: No Templates Available
**User Input**: "Create a quick issue"

**Flow**:
1. No templates in `.github/ISSUE_TEMPLATE/`
2. Creates issue directly with just title and body

### Scenario 5: Tool Fallback
**User Input**: Create issue (gh CLI not installed)

**Flow**:
1. Detects gh CLI unavailable
2. Attempts GitHub REST API
3. Checks for `GITHUB_TOKEN` environment variable
4. Falls back with error if neither tool available

## Reference

For detailed information about:
- GitHub API and CLI options: See [api-guide.md](references/api-guide.md)
- Template matching algorithm details: See [template_matcher.py](scripts/template_matcher.py)
- Issue creation implementation: See [issue_creator.py](scripts/issue_creator.py)

## Error Handling

The skill handles these common errors gracefully:

| Error | Solution |
|-------|----------|
| "gh: not found" | Install GitHub CLI from https://cli.github.com |
| "Not authenticated" | Run `gh auth login` to authenticate |
| "GITHUB_TOKEN not set" | Set GITHUB_TOKEN environment variable |
| "Repository not found" | Verify git remote is configured correctly |
| "Invalid labels" | Check that labels exist in the repository |

## Integration Example

When using this skill in Claude tasks:

```
I need to create a GitHub issue for the current bug we found. 
The issue should mention that the API timeout is causing data loss.
Apply the appropriate template and create it.
```

The skill will:
1. Scan for all templates in `.github/ISSUE_TEMPLATE/`
2. Match templates based on their names and metadata (not hardcoded categories)
3. Suggest best matching template or present options
4. Create the issue using available tools
5. Return issue URL or error details

Or with custom template types:

```
Create a security issue about a potential XSS vulnerability
```

If the repository has custom templates like "security-disclosure" or "vulnerability-report", the skill will intelligently match based on the template names themselves.
