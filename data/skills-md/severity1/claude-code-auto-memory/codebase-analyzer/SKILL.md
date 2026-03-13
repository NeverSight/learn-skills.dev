---
name: codebase-analyzer
description: This skill should be used when the user asks to "initialize auto-memory", "create CLAUDE.md", "set up project memory", or runs the /auto-memory:init command. Analyzes codebase structure and generates CLAUDE.md files using the exact template format with AUTO-MANAGED markers.
---

# Codebase Analyzer

Analyze project structure and generate CLAUDE.md files interactively.

## Guidelines

**MANDATORY**: All rules below must be followed exactly. Violations produce incorrect CLAUDE.md content.

@../shared/references/guidelines.md

## Algorithm

### 1. Check Existing CLAUDE.md

If CLAUDE.md already exists, ask the user how to handle it:
- **Migrate**: Convert to auto-managed format (add markers)
- **Backup**: Create CLAUDE.md.backup and generate fresh
- **Merge**: Keep manual sections, add auto-managed sections
- **Cancel**: Abort initialization

### 2. Scan Directory Structure

Detect frameworks and build systems:
- `package.json` - Node.js/JavaScript
- `pyproject.toml`, `setup.py` - Python
- `Cargo.toml` - Rust
- `go.mod` - Go
- `Makefile` - Make-based builds
- `Dockerfile` - Container builds

Extract build/test/lint commands from config files.

### 3. Identify Subtree Candidates

Look for framework boundaries that warrant separate CLAUDE.md files:
- `src/` with 10+ source files
- `lib/` directory
- `packages/*` (monorepo packages)
- `apps/*` (monorepo applications)

### 4. Detect Code Patterns

Analyze source files for conventions:
- **Naming**: PascalCase, camelCase, snake_case usage
- **Imports**: ES6 modules, CommonJS, ordering patterns
- **Architecture**: Feature-based, layered, MVC patterns
- **Style**: Indentation, quotes, semicolons

### 5. Fetch Memory Guidelines (Optional)

If network available, fetch from `https://code.claude.com/docs/en/memory`:
- Use WebFetch tool
- Extract relevant sections for context
- Reference official guidelines above as primary source

### 6. Present Findings

Use AskUserQuestion to confirm:
- Detected framework and commands
- Suggested subtree locations
- Detected patterns

### 7. Generate CLAUDE.md

Generate files using the EXACT template structure. Follow these steps precisely:

1. **Copy template skeleton** - Use template file as the base structure
2. **Use exact marker format** - See Marker Syntax section below
3. **Replace placeholders** - Substitute `{{PLACEHOLDER}}` with detected content
4. **Include all required sections** - Even if content is minimal, include the section
5. **Add MANUAL section** at the end for user notes
6. **Size limits**: Root 150-200 lines, Subtrees 50-75 lines

## Marker Syntax

**CRITICAL**: Use the EXACT marker format below. Do NOT use variations.

```markdown
<!-- AUTO-MANAGED: section-name -->
## Section Heading

Content goes here

<!-- END AUTO-MANAGED -->
```

For user-editable content:

```markdown
<!-- MANUAL -->
## Custom Notes

Add project-specific notes here. This section is never auto-modified.

<!-- END MANUAL -->
```

**Common mistakes to avoid**:
- `<!-- BEGIN AUTO-MANAGED: name -->` - WRONG (no BEGIN prefix)
- `<!-- END AUTO-MANAGED: name -->` - WRONG (no name in closing tag)
- `<!-- AUTO-MANAGED section-name -->` - WRONG (missing colon)

## Section Definitions

### Root CLAUDE.md Sections

Generate these sections in order:

| Section Name | Heading | Required | Placeholder | Content |
|--------------|---------|----------|-------------|---------|
| `project-description` | ## Overview | Yes | `{{DESCRIPTION}}` | Project name, tagline, key features |
| `build-commands` | ## Build & Development Commands | Yes | `{{BUILD_COMMANDS}}` | Build, test, lint, run commands |
| `architecture` | ## Architecture | Yes | `{{ARCHITECTURE}}` | Directory tree, key files, data flow |
| `conventions` | ## Code Conventions | Yes | `{{CONVENTIONS}}` | Naming, imports, formatting rules |
| `patterns` | ## Detected Patterns | Yes | `{{PATTERNS}}` | AI-detected recurring code patterns |
| `git-insights` | ## Git Insights | No | `{{GIT_INSIGHTS}}` | Key commits, design decisions |
| `best-practices` | ## Best Practices | No | `{{BEST_PRACTICES}}` | From official Claude Code docs |

### Subtree CLAUDE.md Sections

Generate these sections in order:

| Section Name | Heading | Required | Placeholder | Content |
|--------------|---------|----------|-------------|---------|
| `module-description` | ## Purpose | Yes | `{{DESCRIPTION}}` | Module purpose and responsibility |
| `architecture` | ## Module Architecture | Yes | `{{ARCHITECTURE}}` | Module structure, key files |
| `conventions` | ## Module-Specific Conventions | Yes | `{{CONVENTIONS}}` | Module-specific rules |
| `dependencies` | ## Key Dependencies | Yes | `{{DEPENDENCIES}}` | Module dependencies |

## Templates

Reference the template files for exact structure:

### Root Template
@templates/CLAUDE.root.md.template

### Subtree Template
@templates/CLAUDE.subtree.md.template

## User Interactions

Use AskUserQuestion for:
1. Existing CLAUDE.md handling (migrate/backup/merge/cancel)
2. Subtree location confirmation
3. Final approval before writing files

## Output

After generating files, report:
- Files created/modified
- Sections populated
- Any warnings or suggestions
