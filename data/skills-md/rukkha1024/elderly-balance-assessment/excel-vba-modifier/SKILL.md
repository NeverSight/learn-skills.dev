---
name: excel-vba-modifier
description: Safely modify Excel VBA code using xlwings. Checks Trust Center permissions, reads/writes modules, and runs test macros. Always creates backups before modifications.
---

# Excel VBA Modifier Skill

> Safe VBA code modification with xlwings

## Overview

Automates VBA code modifications while ensuring safety:
- Verify Trust Center allows programmatic VBA access
- Read VBA module code from .xlsm files
- Write/modify VBA module code safely
- Run test macros to validate changes
- Automatic backup before modifications

## When to Use

- **Modifying VBA code**: Safe xlwings-based editing
- **Testing macro changes**: Run macros to validate
- **Debugging VBA**: Read module code without manual editing
- **Batch updates**: Apply changes to multiple macros
- **Following safety rules**: Automatic backup and validation

## Usage

```bash
# Check Trust Center permissions
conda run -n excel python script/modify_vba.py check-trust perturb_inform.xlsm

# Read a VBA module
conda run -n excel python script/modify_vba.py read perturb_inform.xlsm Module2

# Write/modify a VBA module (from file)
conda run -n excel python script/modify_vba.py write perturb_inform.xlsm Module2 new_code.vba

# Run a macro to test
conda run -n excel python script/modify_vba.py run perturb_inform.xlsm BuildMetaSummary
```

## Features

### Trust Center Checking
```bash
conda run -n excel python script/modify_vba.py check-trust file.xlsm
```

Output:
```
✓ Trust Center check passed
✓ VBA project access allowed
```

### Reading VBA Code
```bash
conda run -n excel python script/modify_vba.py read file.xlsm Module2
```

Outputs module code to console (can redirect to file).

### Writing VBA Code
```bash
# Write from file
conda run -n excel python script/modify_vba.py write file.xlsm Module2 new_code.vba

# Automatically creates backup first
# Then replaces module with new code
```

### Running Macros
```bash
# Test macro after modification
conda run -n excel python script/modify_vba.py run file.xlsm BuildMetaSummary

# With arguments (if applicable)
conda run -n excel python script/modify_vba.py run file.xlsm Sub1 arg1 arg2
```

## Safety Features

✓ Automatic backup before modifications
✓ Trust Center validation
✓ Test macro execution
✓ Error handling and rollback
✓ Windows only (COM access)

## Integration with Other Skills

- **excel-backup-manager**: Auto-backup before writes
- **excel-inspector**: Understand VBA structure
- **excel-na-utils**: Helper functions for VBA code

## Requirements

- **OS**: Windows only (xlwings COM access)
- **Package**: xlwings
- **Trust Center**: Must allow programmatic VBA access
- **Excel**: Installed and configured

## Error Handling

| Error | Solution |
|-------|----------|
| Trust Center blocked | Enable in Excel: File > Options > Trust Center |
| Module not found | Use `excel-inspector` to list modules |
| Write failed | Check file isn't open in Excel |
| Macro failed | Check syntax in new VBA code |

## Workflow

```
User request
    ↓
Check Trust Center
    ↓
Create backup (via excel-backup-manager)
    ↓
Read current module
    ↓
Write new module
    ↓
Run test macro
    ↓
Report success/failure
```

## Files

- `vba_modifier.py`: Core VBA modification logic
- `trust_center_checker.py`: Trust Center validation
- CLI: `script/modify_vba.py`
