---
name: create-legacy-command
description: Interactive initialization script that generates an Antigravity Workflow, Rule, or legacy Claude /command. Use when you need a simple flat-file procedural instruction set.
disable-model-invocation: false
allowed-tools: Bash, Read, Write
---
# Legacy Command & Workflow Scaffold Generator

You are tasked with generating a flat-file execution routine, such as an Antigravity Workflow, an Antigravity Rule, or a legacy Claude command.

## Execution Steps:

1. **Information Prompt:**
   These flat-file formats do not have complex directories or YAML frontmatter dependencies. Because of their simplicity, you may use standard `echo` and `bash` commands to write them. You do NOT need the Python scaffold script for this specific action.

2. **Gather Requirements:**
   Ask the user what specific type of flat-file routine they need:
   - A Workspace Rule (for context)
   - A Workspace Workflow (for trajectory steps, e.g. `// turbo` tags)
   - A legacy Claude `/command`

3. **Scaffold the Routine:**
   Using bash file creation tools:
   - Create the file in the correct specific location (e.g. `.agent/workflows/`, `.agent/rules/`, or `.claude/commands/`).
   - Ensure the file *strictly* stays under the 12,000 character size limit constraint.
   - Write the sequence of steps based on the user's intent.

4. **Confirmation:**
   Print a success message showing the file location. Explain the difference between this flat-file approach and the richer `Agent Skills` standard.


## Next Actions
- Offer to run `audit-plugin` to validate the generated artifacts.
