---
name: github-create-label
description: Create GitHub issue labels using intelligent tool selection. Automatically leverages tools in order of precedence (GitHub MCP Server → GitHub CLI → REST API). Use when you need to create new labels in a repository with optional customization (name, description, color). Includes support for detecting available authentication methods and graceful fallback between tools.
---

# GitHub Create Label Skill

Create GitHub issue labels using the best available tool with automatic tool selection.

## When to Use This Skill

Use this skill when you need to:
- Create a new label in the current repository
- Create multiple labels with specific names, descriptions, and colors
- Use the best available tool (MCP Server, CLI, or REST API) automatically
- Define labels before creating issues or assigning them

## Quick Start

### Create a Single Label

**Input**: "Create a label called 'bug' with description 'Something isn't working' and color d73a4a"

**Process**:
1. Detects available tools (MCP Server → CLI → REST API)
2. Uses the first available tool
3. Creates the label with provided parameters
4. Returns success confirmation

### Create Multiple Labels

**Input**: "Create these labels: bug (red #d73a4a), enhancement (cyan #a2eeef), documentation (blue #0075ca)"

**Process**:
1. Parses label definitions
2. Creates each label using available tool
3. Returns list of created labels or errors

## Tool Selection Workflow

The skill attempts label creation in this precedence order:

### 1. GitHub MCP Server
**Best for**: Integrated Claude workflows
**When available**: Claude with GitHub tools enabled
**Advantages**: Native integration, no external tools needed

### 2. GitHub CLI (gh)
**Best for**: Local development, interactive workflows
**When available**: `gh` command installed and authenticated
**Command**: `gh label create --name --description --color`

**Requirements**:
- `gh` command installed
- Authenticated via `gh auth login`

### 3. GitHub REST API
**Best for**: CI/CD, automation, programmatic access
**When available**: `GITHUB_TOKEN` or `GH_TOKEN` environment variable set
**Endpoint**: `POST /repos/{owner}/{repo}/labels`

**Requirements**:
- `GITHUB_TOKEN` or `GH_TOKEN` environment variable
- Token must have `repo` scope

## Label Parameters

### Required
- **name** (string): Label name
  - Max 50 characters
  - Examples: "bug", "enhancement", "documentation"

### Optional
- **description** (string): Label description
  - Max 100 characters
  - Examples: "Something isn't working"
  - Default: empty string

- **color** (string): Hex color code
  - 6 characters without # prefix
  - Examples: "d73a4a" (red), "a2eeef" (cyan), "0075ca" (blue)
  - Default: random color assigned by GitHub

## Common Label Patterns

### Bug Tracking
```
bug: d73a4a (red)
"Something isn't working"

help wanted: 008672 (dark green)
"Extra attention is needed"
```

### Feature Management
```
enhancement: a2eeef (cyan)
"New feature or request"

good first issue: 7057ff (purple)
"Good for newcomers"
```

### Documentation & Questions
```
documentation: 0075ca (blue)
"Improvements or additions to documentation"

question: cc317c (purple)
"Further information is requested"
```

### Maintenance
```
wontfix: ffffff (white)
"This will not be worked on"

invalid: e4e669 (yellow)
"This doesn't seem right"
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

### Scenario 1: Create Standard Labels for New Repository

**User Input**: "Set up standard labels for bug tracking and feature management"

**Process**:
1. Creates "bug" label (red)
2. Creates "enhancement" label (cyan)
3. Creates "documentation" label (blue)
4. Creates "help wanted" label (dark green)
5. Returns confirmation

### Scenario 2: Create Custom Label

**User Input**: "Create a label for security issues with color ff0000"

**Process**:
1. Parses label: name="security", color="ff0000"
2. Uses available tool to create
3. Returns confirmation

### Scenario 3: Tool Fallback

**User Input**: Create label (gh CLI not installed)

**Process**:
1. Detects gh not available
2. Checks for GITHUB_TOKEN
3. Uses REST API if available
4. Returns error if no tools available

### Scenario 4: Batch Label Creation

**User Input**: Create labels from a list

**Process**:
1. Iterates through label definitions
2. Creates each label using available tool
3. Tracks successes and failures
4. Returns summary report

## Reference

For detailed information about:
- GitHub API and CLI commands: See [api_reference.md](references/api_reference.md)
- Label color suggestions and examples
- Error handling and troubleshooting

## Error Handling

The skill handles these common errors gracefully:

| Error | Solution |
|-------|----------|
| "gh: not found" | Install GitHub CLI from https://cli.github.com |
| "Not authenticated" | Run `gh auth login` to authenticate |
| "GITHUB_TOKEN not set" | Set GITHUB_TOKEN environment variable |
| "Repository not found" | Verify git remote is configured correctly |
| "Label already exists" | Use different name or update existing label |
| "Invalid color format" | Use 6-character hex code (e.g., d73a4a) |
| "Name too long" | Keep label name under 50 characters |

## Integration Example

When using this skill in Claude tasks:

```
I need to set up labels for this repository.
Create these labels:
- bug (red, "Something isn't working")
- enhancement (cyan, "New feature or request")
- documentation (blue, "Documentation improvements")
- help wanted (dark green, "Extra attention needed")
```

The skill will:
1. Check for available tools in order of precedence
2. Create each label using the best available tool
3. Return confirmation for each created label
4. Report any errors that occur

## Best Practices

1. **Consistency**: Use consistent naming across projects (lowercase, hyphens for spaces)
2. **Documentation**: Always include descriptions for clarity
3. **Colors**: Use colors to create visual patterns (red for bugs, green for help, blue for docs)
4. **Batch Creation**: Create all needed labels upfront during project setup
5. **Naming Conventions**: Follow repository guidelines for label naming
