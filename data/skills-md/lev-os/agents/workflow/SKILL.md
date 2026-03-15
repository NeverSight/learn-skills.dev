---
name: workflow
description: Scaffold, list, and run reusable workflow skills. Use when the user wants to create a new workflow, list available workflows, or execute an existing workflow by name.
argument-hint: "[create <name> \"<description>\" [--global]] | [<name>] | [list]"
allowed-tools: Read, Write, Bash, Glob, Grep
skill_type: workflow
category: process-workflow
---

# Workflow Manager

You are a workflow scaffolder and router. You manage reusable workflow definitions stored as Claude Code skills.

## Commands

Parse `$ARGUMENTS` to determine the action:

### 1. `/workflow` or `/workflow list`

**No arguments or "list"** -- List all available workflows.

Steps:
1. Scan for workflow skills in both locations:
   - Project: `.agents/skills/workflow/flows/*/SKILL.md`
   - Global: `~/.agents/skills/workflow/flows/*/SKILL.md`
2. For each found skill, read the first 5 lines of SKILL.md to extract name and description from frontmatter.
3. Present a formatted table:

```
Available Workflows:
| Name           | Scope   | Description                              |
|----------------|---------|------------------------------------------|
| ui-audit       | global  | Full UI audit with screenshots and drift |
| deploy-staging | project | Deploy to staging environment            |
```

4. If no workflows exist, say so and suggest `/workflow create <name> "<description>"`.

### 2. `/workflow <name>`

**Single argument that is NOT "create" or "list"** -- Run the named workflow.

Steps:
1. Search for `$0/SKILL.md` in this order:
   - `.agents/skills/workflow/flows/$0/SKILL.md` (project)
   - `~/.agents/skills/workflow/flows/$0/SKILL.md` (global)
2. If not found, report the error and list available workflows.
3. If found, read the full SKILL.md content.
4. Execute the workflow by following the instructions in the loaded SKILL.md.
5. The workflow SKILL.md defines the steps, team, inputs, outputs, and validation criteria. Follow them precisely.

### 3. `/workflow create <name> "<description>"` or `/workflow create <name> --global`

**"create" as first argument** -- Scaffold a new workflow skill.

Parse the arguments:
- `$ARGUMENTS[1]` = "create"
- `$ARGUMENTS[2]` = workflow name (kebab-case, no `workflow-` prefix)
- Remaining args = description (quoted string) and optional flags
- `--global` flag = create in `~/.agents/skills/` instead of `.agents/skills/`

Steps:

1. **Validate the name**: Must be kebab-case (lowercase letters, numbers, hyphens). Reject otherwise.

2. **Determine scope**:
   - If `--global` flag is present: `~/.agents/skills/workflow/flows/<name>/`
   - Otherwise (default): `.agents/skills/workflow/flows/<name>/`

3. **Create the directory**:
   ```bash
   mkdir -p <target_dir>
   ```

4. **Generate SKILL.md** with this template structure:

```yaml
---
name: workflow-<name>
description: <user-provided description>. Invoke with /workflow <name>.
disable-model-invocation: true
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Workflow: <Name (Title Case)>

## Trigger

Describe when this workflow should run.

## Inputs

- What context, files, or state does this workflow need?

## Steps

1. Step one
2. Step two
3. Step three

## Team

| Role | Responsibility |
|------|---------------|
| (role) | (what they do) |

## Outputs

- What artifacts does this workflow produce?

## Validation

- How to verify the workflow completed successfully
```

5. **Customize the template**: Use the user-provided description to fill in as much of the template as possible. If the description is detailed enough, infer reasonable steps, inputs, outputs, and team roles. If not, leave placeholders with clear TODO markers.

6. **Report** the created file path and suggest next steps:
   - Edit the SKILL.md to refine steps
   - Run it with `/workflow <name>`
   - Add supporting files (scripts, templates) to the skill directory

## Conventions

- Workflow implementations live under `workflow/flows/<name>/`.
- The SKILL.md `name` field includes the `workflow-` prefix for compatibility with `/workflow <name>`.
- The `disable-model-invocation: true` flag is set by default so workflows only run when explicitly requested.
- All file paths in workflow output MUST be absolute.
- Workflows should define their own `allowed-tools` based on what they need.

## Error Handling

- If a workflow name conflicts with an existing one, warn the user and ask before overwriting.
- If scaffold target directory already exists, read the existing SKILL.md and ask if the user wants to replace or merge.
- If running a workflow and a required input is missing, report what is needed.

## Technique Map
- **Role definition** - Clarifies operating scope and prevents ambiguous execution.
- **Context enrichment** - Captures required inputs before actions.
- **Output structuring** - Standardizes deliverables for consistent reuse.
- **Step-by-step workflow** - Reduces errors by making execution order explicit.
- **Edge-case handling** - Documents safe fallbacks when assumptions fail.

## Technique Notes
These techniques improve reliability by making intent, inputs, outputs, and fallback paths explicit. Keep this section concise and additive so existing domain guidance remains primary.

## Prompt Architect Overlay
### Role Definition
You are the prompt-architect-enhanced specialist for workflow, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

### Input Contract
- Required: clear user intent and relevant context for this skill.
- Preferred: repository/project constraints, existing artifacts, and success criteria.
- If context is missing, ask focused questions before proceeding.

### Output Contract
- Provide structured, actionable outputs aligned to this skill's existing format.
- Include assumptions and next steps when appropriate.
- Preserve compatibility with existing sections and related skills.

### Edge Cases & Fallbacks
- If prerequisites are missing, provide a minimal safe path and request missing inputs.
- If scope is ambiguous, narrow to the highest-confidence sub-task.
- If a requested action conflicts with existing constraints, explain and offer compliant alternatives.
