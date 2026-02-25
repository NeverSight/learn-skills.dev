---
name: 4d-run
description: Run a 4D method using tool4d command-line tool. Use this skill when the user wants to execute, test, or run a 4D project method. Automatically finds tool4d.app in standard locations (VS Code extensions, Antigravity). Supports running any project method with --dataless mode for testing without data file.
license: Apache 2.0
---

# 4D Method Runner

Run 4D project methods using tool4d command-line tool.

## Finding tool4d

tool4d can be located in two ways:

### 1. Environment Variable (Recommended if custom installation)

Set the `TOOL4D` environment variable to point to the tool4d executable:

```bash
export TOOL4D="/path/to/tool4d.app/Contents/MacOS/tool4d"
```

### 2. Auto-discovery from Extension

tool4d is typically installed by the 4D-Analyzer extension in one of these locations:
- VS Code: `$HOME/Library/Application Support/Code/User/globalStorage/4d.4d-analyzer/tool4d/`
- Antigravity: `$HOME/Library/Application Support/Antigravity/User/globalStorage/4d.4d-analyzer/tool4d/`

Within these directories, versions are stored in indexed folders (e.g., `21/100301/`). Always use the latest version available.

### Discovery Script

```bash
# Find tool4d in standard locations, return latest version
find_tool4d() {
    local search_paths=(
        "$HOME/Library/Application Support/Code/User/globalStorage/4d.4d-analyzer/tool4d"
        "$HOME/Library/Application Support/Antigravity/User/globalStorage/4d.4d-analyzer/tool4d/"
    )

    for base_path in "${search_paths[@]}"; do
        if [ -d "$base_path" ]; then
            # Find latest tool4d.app by sorting version folders
            local tool4d_path=$(find "$base_path" -name "tool4d.app" -type d 2>/dev/null | sort -V | tail -1)
            if [ -n "$tool4d_path" ]; then
                echo "$tool4d_path/Contents/MacOS/tool4d"
                return 0
            fi
        fi
    done
    return 1
}
```

## Running a Method

### Basic Command

```bash
"<tool4d_path>" --project="<project_path>" --startup-method=<method_name> --skip-onstartup --dataless
```

Parameters:
- `--project`: Full path to the `.4DProject` file
- `--startup-method`: Name of the method to execute (without `.4dm` extension)
- `--skip-onstartup`: Skip the On Startup method execution (recommended when running specific methods)
- `--dataless`: Run without a data file (recommended for testing)

### Example

```bash
"/Users/eric/Library/Application Support/Code/User/globalStorage/4d.4d-analyzer/tool4d/21/100301/tool4d.app/Contents/MacOS/tool4d" \
    --project="/path/to/Project/MyProject.4DProject" \
    --startup-method=test_MyFeature \
    --skip-onstartup \
    --dataless
```

## Output Handling

tool4d output appears on stderr. Common patterns:

- **ALERT calls**: `tool4d.HDLS ([Call of Forbidden Method] ALERT: <message>)`
- **Assertion failures**: `tool4d.4DRT [-10518] Assert failed: <message>`
- **Success**: Method completes without error output

### Logging from 4D Code

Use `LOG EVENT` to output messages:

```4d
LOG EVENT(Into system standard outputs; "message"; Information message)
```

Or write to a file:

```4d
File("/path/to/debug.txt").setText($debugText)
```

## Workflow

1. **Find tool4d**: Search standard locations for latest version
2. **Locate project**: Find the `.4DProject` file in the project directory
3. **Run method**: Execute with `--dataless` flag
4. **Parse output**: Check stderr for ALERT messages or errors
