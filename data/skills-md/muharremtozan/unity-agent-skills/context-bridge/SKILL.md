---
name: context-bridge
description: >
  Start a context synchronization session between World-Building and Unity projects.
  Scans the current project for critical updates (lore, mechanics, assets) and update
  a shared context file to keep the other project informed.
---

# Context Bridge

## Purpose

To maintain a synchronized "Basic and Critical" context between the **World-Building** (narrative/art) and **Unity** (gameplay/code) projects. This skill bridges the gap, allowing each project to know what has been realized in the other without full context loading.

## Usage Workflow

### 1. Scan & Summarize
Before running the script, you MUST:
1.  **Identify the current project**: Are we in `World-Building` or `Unity`?
2.  **Scan for key changes**: Look for recent updates in:
    - **World-Building**: New lore, character arcs, location descriptions, artistic direction.
    - **Unity**: New mechanics, implemented systems, asset requirements, level design constraints.
3.  **Draft a Summary**: Create a concise bulleted list of "Basic and Critical" information that the *other* project needs to know.
    - *Example (from WB)*: "New faction 'Iron Seekers' defined. Key colors: Rust & Orange. Values: Scavenging technology."
    - *Example (from Unity)*: "Combat system now supports 'Overheat' mechanic. UI needs heat bar assets."

### 2. Update Shared Context
Run the `update_context.py` script to save this summary.

```bash
# internal usage
python .agent/skills/context-bridge/scripts/update_context.py --project "<ProjectName>" --content "<Summary String>"
```

**Arguments:**
- `--project`: The project you are currently in. Valid values: `World-Building`, `Unity`.
- `--content`: The summarized text to save. Use `\n` for newlines if passing via command line, or use the interactive mode (script might support raw input).

*Note: The script will handle file creation and section management.*

## Shared File Structure
The shared context file (`PROJECTS_SHARED_CONTEXT.md`) will look like this:

```markdown
# Shared Project Context

## World-Building Context
[Last Updated: <Date>]
- Summary point 1
- Summary point 2

## Unity Context
[Last Updated: <Date>]
- Summary point 1
- Summary point 2
```

## Tips
- **Be Concise**: The other agent doesn't need every detail, just the "hooks" they need to respect or implement.
- **Don't Overwrite**: The script is designed to only replace YOUR project's section.
