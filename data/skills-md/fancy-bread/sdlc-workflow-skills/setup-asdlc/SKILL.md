---
name: setup-asdlc
description: Initialize a repository for ASDLC adoption with AGENTS.md and directory structure
disable-model-invocation: true
---

# Setup ASDLC

## Overview
Initialize a repository for ASDLC adoption by creating AGENTS.md template, directory structure (specs/, .plans/), and basic configuration. This command prepares repositories to use ASDLC patterns while remaining optional—other commands work without running setup.

## Definitions

- **AGENTS.md**: Agent Constitution file that defines project context, operational boundaries, and command registry for AI agents.
- **specs/**: Directory containing permanent living specifications for features.
- **.plans/**: Directory containing transient task-level implementation plans.
- **schemas/**: Directory containing JSON Schema definitions for validation (Standardized Parts pattern).
- **MCP**: Model Context Protocol — framework for AI agents to connect to external services.
- **Standardized Parts**: ASDLC pattern for schema-enforced structure and validation.

## Prerequisites

- **None required.** This command is optional and can be run at any time.
- **MCP setup is optional** — command will check MCP status but won't block if unavailable.
- **Git repository** — command works best in a Git repository but doesn't require it.

## Purpose
Enable teams to quickly adopt ASDLC patterns by automating initial repository setup. This command creates the foundational structure (AGENTS.md, specs/, .plans/) that supports ASDLC workflows while maintaining flexibility—teams can use other commands without running setup.

## Steps

1. **Check for existing AGENTS.md**
   - Check if `AGENTS.md` exists in repository root
   - If exists: Report "AGENTS.md already exists, skipping creation"
   - If missing: Proceed to generate template (Step 2)

2. **Generate AGENTS.md template** (if missing)
   - Read existing `AGENTS.md` from this repository as template reference (if available)
   - Create `AGENTS.md` with template structure:
     - Project Mission placeholder: `> **Project Mission:** [Your project mission statement]`
     - Core Philosophy placeholder: `> **Core Philosophy:** [Your core development philosophy]`
     - ASDLC Alignment placeholder: `> **ASDLC Alignment:** [Your ASDLC alignment statement]`
     - Identity & Persona section with placeholders
     - Tech Stack section with placeholders
     - Operational Boundaries (3-tier structure):
       - Tier 1 (ALWAYS): Non-negotiable standards
       - Tier 2 (ASK): High-risk operations requiring Human-in-the-Loop
       - Tier 3 (NEVER): Safety limits
     - Command Registry (empty, to be populated)
     - Development Map (placeholder)
     - Common Pitfalls section (examples)
   - Report: "Created AGENTS.md template"

3. **Create specs/ directory**
   - Check if `specs/` directory exists
   - If exists: Report "specs/ directory already exists, skipping creation"
   - If missing: Create `specs/` directory
   - Check if `specs/README.md` exists
   - If missing: Copy `specs/README.md` from this repository (if available) or create basic README
   - Report: "Created specs/ directory with README.md"

4. **Create .plans/ directory**
   - Check if `.plans/` directory exists
   - If exists: Report ".plans/ directory already exists, skipping creation"
   - If missing: Create `.plans/` directory
   - Create `.plans/.gitkeep` file to ensure directory is tracked by Git
   - Report: "Created .plans/ directory"

5. **Detect if schemas/ directory is needed**
   - Check if `schemas/` directory exists
   - If exists: Report "schemas/ directory already exists, skipping creation"
   - If missing: Check for schema indicators:
     - If `AGENTS.md` exists, search for keywords: "Standardized Parts", "schema", "validation"
     - If any keyword found: Create `schemas/` directory and `schemas/README.md` template
     - Report: "Detected need for schemas/ (found: {keyword} in AGENTS.md)" or "No schemas/ needed (no indicators found)"

6. **Create schemas/README.md template** (if schemas/ was created)
   - Create `schemas/README.md` with template explaining:
     - When schemas are needed (Standardized Parts pattern)
     - Link to ASDLC Standardized Parts pattern
     - Note: Can be added later if needed
   - Report: "Created schemas/README.md template"

7. **Optional: Verify MCP setup** (non-blocking)
   - Attempt to run `python schemas/validate_mcps.py --list` (if available)
   - If successful: Report "MCP setup detected"
   - If fails or unavailable: Report "MCP setup not detected (optional, can be configured later)"
   - Continue regardless of result

8. **Optional: Verify issue tracker connection** (non-blocking)
   - Attempt to call lightweight MCP tool (e.g., `mcp_atlassian_getAccessibleAtlassianResources` or `mcp_github_list_commits`)
   - If successful: Report "Issue tracker connection verified"
   - If fails or unavailable: Report "Issue tracker connection not available (optional, can be configured later)"
   - Continue regardless of result

9. **Generate setup summary**
   - Report what was created vs skipped
   - Provide next steps guidance:
     - "Next steps: Customize AGENTS.md with your project details"
     - "Configure MCP servers (see docs/reference/mcp-setup.md)"
     - "Create your first spec with /create-plan"

## Tools

### Filesystem Tools
- `read_file` - Read existing AGENTS.md and specs/README.md as templates
- `write` - Create new files (AGENTS.md, specs/README.md, schemas/README.md)
- `list_dir` - Check if directories exist
- `glob_file_search` - Find existing files

### Terminal Tools
- `run_terminal_cmd` - Execute commands:
  - `python schemas/validate_mcps.py --list` (if available) - Check MCP setup
  - `git status` (optional) - Verify Git repository

### MCP Tools (Optional, Non-Blocking)
- `mcp_atlassian_getAccessibleAtlassianResources` - Verify Atlassian/Jira connection
  - Parameters: None
  - Error handling: If fails, report but continue
- `mcp_github_list_commits` - Verify GitHub connection
  - Parameters: `owner`, `repo` (if available)
  - Error handling: If fails, report but continue

## Expected Output

### Fresh Repository Setup
```
🚀 ASDLC Setup Complete

Created:
  ✅ AGENTS.md template
  ✅ specs/ directory with README.md
  ✅ .plans/ directory
  ⚠️  schemas/ not needed (no indicators found)

MCP Status:
  ⚠️  MCP setup not detected (optional, can be configured later)
  ⚠️  Issue tracker connection not available (optional, can be configured later)

Next steps:
  1. Customize AGENTS.md with your project details
  2. Configure MCP servers (see docs/reference/mcp-setup.md)
  3. Create your first spec with /create-plan
```

### Partial Setup (AGENTS.md exists)
```
🚀 ASDLC Setup Complete

Skipped:
  ⚠️  AGENTS.md already exists

Created:
  ✅ specs/ directory with README.md
  ✅ .plans/ directory
  ✅ schemas/ directory (detected: Standardized Parts in AGENTS.md)

MCP Status:
  ✅ MCP setup detected
  ✅ Issue tracker connection verified

Next steps:
  1. Create your first spec with /create-plan
```

### Full Setup Already Exists
```
🚀 ASDLC Setup Complete

All directories and files already exist:
  ✅ AGENTS.md
  ✅ specs/ directory
  ✅ .plans/ directory
  ✅ schemas/ directory

MCP Status:
  ✅ MCP setup detected
  ✅ Issue tracker connection verified

Repository is already set up for ASDLC!
```

## When to Use

- **New repository** - Set up ASDLC structure from scratch
- **Existing repository** - Add ASDLC structure to existing project
- **Team onboarding** - Standardize setup across team members
- **ASDLC adoption** - Begin using ASDLC patterns and workflows

## Error Handling

**If AGENTS.md template generation fails:**
- Report error but continue with directory creation
- Provide manual creation instructions

**If directory creation fails:**
- Report which directories failed
- Provide manual creation instructions
- Continue with other operations

**If MCP verification fails:**
- Report warning but continue (MCP is optional)
- Provide MCP setup documentation link

**If file copy fails (specs/README.md):**
- Create basic README.md with minimal content
- Report that template copy failed

## Notes

- This command is **optional** — other commands work without running setup
- Command **never overwrites** existing files or directories
- MCP verification is **non-blocking** — command succeeds even if MCP is unavailable
- Schema detection is **intelligent** — only creates schemas/ if indicators are found
- All operations are **idempotent** — safe to run multiple times

## Guidance

### Role
Act as a **setup assistant** helping teams initialize their repository for ASDLC adoption. You are helpful, non-intrusive, and provide clear guidance.

### Instruction
Execute the setup workflow to prepare a repository for ASDLC by creating AGENTS.md template, directory structure, and optional configuration checks. Always check for existing files before creating, never overwrite, and provide clear feedback on what was created vs skipped.

### Context
- This command enables teams to quickly adopt ASDLC patterns
- Command is optional—other commands work without running setup
- Based on recommendations from FB-32 analysis
- Follows skill structure standards from AGENTS.md
- **ASDLC patterns**: [Agent Constitution](asdlc://agent-constitution), [The Spec](asdlc://the-spec), [Standardized Parts](asdlc://standardized-parts)
- **ASDLC pillars**: **Factory Architecture** (command station), **Standardized Parts** (schema-enforced structure), **Quality Control** (validation gates)

### Examples

**ASDLC**: [Agent Constitution](asdlc://agent-constitution) — AGENTS.md implements this pattern. [Standardized Parts](asdlc://standardized-parts) — Schema detection aligns with this pattern.

**Example: Fresh Repository**
```
User runs: /setup-asdlc
Result: Creates AGENTS.md, specs/, .plans/, reports summary
```

**Example: Existing Repository**
```
User runs: /setup-asdlc
Result: Skips existing files, creates missing directories, reports what was added
```

### Constraints

**Rules (Must Follow):**
1. **Operational Standards Compliance**: This command follows operational standards (documented in AGENTS.md if present, but apply universally):
   - **File Operations**: Follow best practices for file operations and directory structure
   - **Safety Limits**: Never commit secrets, API keys, or sensitive data in generated files
   - **AGENTS.md Optional**: This command creates AGENTS.md, but other commands work without it. Standards apply regardless.
   - See AGENTS.md §3 Operational Boundaries (if present) for detailed standards
2. **Never Overwrite** - Always check for existing files/directories before creating
3. **Optional MCP** - MCP verification must not block command execution
4. **Intelligent Detection** - Only create schemas/ if indicators are found in AGENTS.md
5. **Clear Feedback** - Report what was created vs skipped with clear messages
6. **Idempotent** - Command must be safe to run multiple times
7. **Template-Based** - Use existing AGENTS.md and specs/README.md as templates when available

**Existing Standards (Reference):**
- Command structure: See AGENTS.md §6 Command Structure Standards
- Directory conventions: specs/ for specs, .plans/ for plans
- File naming: AGENTS.md at root, specs/README.md for specs documentation
- MCP setup: See docs/reference/mcp-setup.md for MCP configuration
- Schema validation: See schemas/README.md for when schemas are needed

### Output
1. **Setup Summary**: Report of what was created vs skipped
2. **MCP Status**: Optional verification results (non-blocking)
3. **Next Steps**: Guidance on customizing AGENTS.md and configuring MCP
4. **Clear Feedback**: Explicit messages for each operation (created, skipped, detected)

The command prepares the repository for ASDLC adoption while maintaining flexibility and never overwriting existing files.
