---
name: config-reader
description: Read project config from .agents.yml and .agents.local.yml with local overrides. Supports dot notation for nested fields. Invoke with args "<field> <default>".
argument-hint: "<field> [default]"
disable-model-invocation: true
---

# Config Reader

Read and merge `.agents.yml` and `.agents.local.yml` configuration files. Local config overrides base config.

**Requires:** yq (`brew install yq` or `snap install yq`)

## Arguments

`$ARGUMENTS` format: `<field> [default]`

Examples:
- `auto_preview false` - get top-level field, default to "false"
- `plan.auto_create_task false` - get nested field, default to "false"
- `tech_stack generic` - get top-level field, default to "generic"
- `browser.type chrome` - get nested browser type
- `toolbox.build_task.design_system_path` - get deeply nested field

## Execution

Run the config reader script with parsed arguments:

```bash
bash {baseDir}/scripts/config_reader.sh FIELD DEFAULT
```

Replace `FIELD` and `DEFAULT` with the parsed arguments from `$ARGUMENTS`.

## Return Value

Return ONLY the config value (single line):
- `true`
- `rails`
- `github`

## Merge Logic

1. **Local checked first** - `.agents.local.yml` wins if key exists
2. **Fall back to base** - `.agents.yml` if not in local
3. **Default** - provided default if neither has the key

## Common Fields

| Field | Description | Typical Default |
|-------|-------------|-----------------|
| `auto_preview` | Auto-open markdown files | `false` |
| `plan.auto_create_task` | Auto-create tasks from plans | `false` |
| `tech_stack` | Primary tech stack | `generic` |
| `task_management` | Task tracking backend | `none` |
| `workflow` | Git workflow style | `branches` |
| `toolbox.build_task.design_system_path` | Design system location | (none) |
