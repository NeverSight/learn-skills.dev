---
name: raycast-script-creator
description: Create valid Raycast script-commands that integrate with the Raycast launcher. Use this skill when users request creating Raycast scripts, automation commands for Raycast, or workflow shortcuts for the Raycast app. This skill ensures all outputs conform to Raycast's required metadata format and structural conventions.
---

# Raycast Script Creator

## Overview

Create valid Raycast script-commands with proper metadata formatting and structure. Raycast script-commands are executable scripts that integrate with the Raycast launcher, enabling quick access to custom workflows, system commands, and automation tasks from anywhere on macOS.

## When to Use This Skill

Activate this skill when users request:
- "Create a Raycast script to..."
- "Make a Raycast command for..."
- "Build a script-command that..."
- "Add a Raycast shortcut to..."
- Any task involving creating automation scripts for the Raycast launcher

## Core Principles

### 1. Metadata is Mandatory

Every Raycast script MUST include properly formatted metadata comments at the top of the file. The three required fields are:
- `@raycast.schemaVersion` (always set to 1)
- `@raycast.title` (the display name in Raycast)
- `@raycast.mode` (how output is presented)

### 2. Output Mode Selection

Choose the appropriate mode based on the script's purpose:

- **silent** - Instant commands with minimal output (toggle settings, quick actions)
- **compact** - Long-running background tasks (network requests, API calls)
- **fullOutput** - Scripts with substantial output to display (file contents, logs)
- **inline** - Auto-refreshing data displayed in search results (requires `@raycast.refreshTime`)

### 3. Language Support

Raycast supports multiple scripting languages:
- Shell/Bash (most common)
- Python
- JavaScript/Node.js
- Ruby
- Swift
- AppleScript

## Creating Raycast Scripts

### Step 1: Understand the User's Request

Determine:
1. What action should the script perform?
2. What output (if any) should be displayed?
3. Does it need user input (arguments)?
4. Should it run in the background or show results?
5. Is confirmation needed before execution?

### Step 2: Select the Appropriate Template

Choose a template from `assets/` based on the preferred language:
- `template.sh` - Shell/Bash scripts (recommended for most tasks)
- `template.py` - Python scripts
- `template.js` - JavaScript/Node.js scripts
- `template.rb` - Ruby scripts
- `template.swift` - Swift scripts
- `template.applescript` - AppleScript

### Step 3: Configure Metadata

Start with the template and update the metadata fields:

**Required Fields:**
```bash
# @raycast.schemaVersion 1
# @raycast.title [Descriptive Title]
# @raycast.mode [silent|compact|fullOutput|inline]
```

**Recommended Optional Fields:**
```bash
# @raycast.icon [emoji or file path]
# @raycast.packageName [Category Name]
# @raycast.description [What the script does]
```

**Additional Optional Fields:**
```bash
# @raycast.needsConfirmation [true|false]
# @raycast.currentDirectoryPath [directory path]
# @raycast.refreshTime [10s|1m|12h|1d] (required for inline mode)
# @raycast.author [Your Name]
# @raycast.authorURL [Your URL]
```

### Step 4: Implement the Script Logic

Write the actual script code below the metadata comments. The script should:
- Perform the requested action
- Output appropriate information (based on mode)
- Handle errors gracefully
- Exit with proper exit codes (0 for success, non-zero for failure)

### Step 5: Validate the Script

Ensure:
1. All three required metadata fields are present
2. The chosen mode matches the script's behavior
3. If using inline mode, `@raycast.refreshTime` is specified
4. The shebang line is correct for the language
5. File has executable permissions
6. For bash scripts, consider running through ShellCheck

## Common Patterns and Examples

### Pattern 1: Open Application or Folder (silent mode)

Use when creating shortcuts to open applications, folders, or files instantly.

```bash
#!/bin/bash
# @raycast.schemaVersion 1
# @raycast.title Open Downloads
# @raycast.mode silent
# @raycast.icon 🗂️
# @raycast.packageName System Tools

open ~/Downloads
```

### Pattern 2: Development Environment Launcher (compact mode)

Use for opening projects in editors or starting development servers.

```bash
#!/bin/bash
# @raycast.schemaVersion 1
# @raycast.title Open Project in Cursor
# @raycast.mode compact
# @raycast.icon 💻
# @raycast.packageName Developer Tools

cursor ~/Documents/my-project
```

### Pattern 3: System Information Display (fullOutput mode)

Use for displaying detailed information, logs, or multi-line output.

```bash
#!/bin/bash
# @raycast.schemaVersion 1
# @raycast.title System Info
# @raycast.mode fullOutput
# @raycast.icon 💻
# @raycast.packageName System Tools

echo "System Information:"
echo "==================="
system_profiler SPHardwareDataType SPSoftwareDataType
```

### Pattern 4: Live Status Monitor (inline mode)

Use for displaying auto-refreshing data like system stats or API data.

```bash
#!/bin/bash
# @raycast.schemaVersion 1
# @raycast.title CPU Usage
# @raycast.mode inline
# @raycast.icon 📊
# @raycast.refreshTime 5s
# @raycast.packageName System Monitor

top -l 1 | grep "CPU usage" | awk '{print "CPU: " $3 " " $5}'
```

### Pattern 5: Destructive Action with Confirmation (needsConfirmation)

Use for actions that modify system state or delete files.

```bash
#!/bin/bash
# @raycast.schemaVersion 1
# @raycast.title Clear Downloads Folder
# @raycast.mode compact
# @raycast.icon 🗑️
# @raycast.needsConfirmation true
# @raycast.packageName System Tools

rm -rf ~/Downloads/*
echo "Downloads folder cleared"
```

### Pattern 6: Script with Arguments

Use when the script needs user input at runtime.

```bash
#!/bin/bash
# @raycast.schemaVersion 1
# @raycast.title Create Folder
# @raycast.mode compact
# @raycast.icon 📁
# @raycast.argument1 { "type": "text", "placeholder": "Folder name" }

mkdir -p "$1"
echo "Created folder: $1"
```

## Important Constraints and Best Practices

### File Naming
- Avoid `.template.` in filenames (reserved for templates requiring configuration)
- Use descriptive, kebab-case names: `open-downloads.sh`, `system-info.py`
- Include file extension matching the language

### Script Permissions
- Scripts must be executable: `chmod +x script-name.sh`
- Typically stored in `~/.config/raycast/scripts/` or custom script directories

### Shell Environment
- Scripts run in non-login shells by default
- To use login shell: `#!/bin/bash -l`
- `/usr/local/bin` is automatically in `$PATH`

### Error Handling
- Use exit code 0 for success
- Use non-zero exit codes for failures (triggers error notification)
- Provide meaningful error messages via stderr

### Output Guidelines
- **silent mode**: Minimal or no output
- **compact mode**: Last line shown in toast
- **fullOutput mode**: All output displayed
- **inline mode**: First line shown and refreshed

### Metadata Comments
- Use `#` for Shell, Python, Ruby
- Use `//` for JavaScript, Swift
- Place metadata at the top of the file, after the shebang
- Format: `# @raycast.fieldName value`

## Workflow Decision Tree

When creating a Raycast script, follow this decision process:

1. **What language?** → Choose template from `assets/`
2. **What's the output behavior?**
   - No output needed → `mode: silent`
   - Background task → `mode: compact`
   - Detailed output → `mode: fullOutput`
   - Auto-refreshing data → `mode: inline` + add `refreshTime`
3. **Needs confirmation?** → Add `needsConfirmation: true`
4. **Needs user input?** → Add `argument1`, `argument2`, or `argument3`
5. **Part of a group?** → Set `packageName` to category
6. **Visual icon?** → Set `icon` to emoji or file path

## Reference Documentation

For detailed information about metadata fields and output modes, refer to:
- `references/raycast-metadata.md` - Complete metadata reference with all fields and modes

## Templates

All language templates are available in the `assets/` directory:
- `assets/template.sh` - Bash/Shell
- `assets/template.py` - Python 3
- `assets/template.js` - JavaScript/Node.js
- `assets/template.rb` - Ruby
- `assets/template.swift` - Swift
- `assets/template.applescript` - AppleScript

## Output Format

Always output a complete, valid Raycast script with:
1. Proper shebang line
2. All required metadata fields
3. Appropriate optional metadata
4. Functional script implementation
5. Comments explaining key logic (if complex)

The script should be ready to save, make executable, and use immediately in Raycast.
