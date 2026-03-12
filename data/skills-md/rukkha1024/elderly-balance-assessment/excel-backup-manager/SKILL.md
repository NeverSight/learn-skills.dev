---
name: excel-backup-manager
description: Create, manage, and restore Excel file backups with automatic timestamps. Use before modifying Excel files to ensure data safety and enable rollback if needed.
---

# Excel Backup Manager Skill

> Safe Excel file backup and restore functionality

## Overview

This skill automates Excel file backup management following CLAUDE.md safety protocols.

Key features:
- **Automatic timestamped backups**: `file.xlsm` → `file.backup.20251211_143000.xlsm`
- **Backup listing**: View all available backups
- **Selective restore**: Restore from any previous backup
- **Cleanup**: Remove old backups while preserving recent ones

## When to Use

- **Before modifying VBA code**: Always create a backup first
- **After errors**: Restore from a previous working version
- **Testing Excel changes**: Keep safe checkpoints
- **Data protection**: Prevent accidental data loss
- **Auditing**: Track modification history

## Usage

```bash
# Create a backup
conda run -n excel python script/backup_excel.py backup perturb_inform.xlsm

# List all backups
conda run -n excel python script/backup_excel.py list perturb_inform.xlsm

# Restore from backup
conda run -n excel python script/backup_excel.py restore file.backup.20251211_143000.xlsm

# Clean up old backups (keep 5 most recent)
conda run -n excel python script/backup_excel.py cleanup perturb_inform.xlsm --keep 5
```

## Output

### Backup Command
Creates backup in same directory:
```
perturb_inform.backup.20251211_143000.xlsm
```

### List Command
Shows all backups with sizes and timestamps:
```
Available backups for perturb_inform.xlsm:
1. perturb_inform.backup.20251211_143000.xlsm (170.5 KB) - 2025-12-11 14:30:00
2. perturb_inform.backup.20251211_140000.xlsm (170.5 KB) - 2025-12-11 14:00:00
3. perturb_inform.backup.20251210_180000.xlsm (170.3 KB) - 2025-12-10 18:00:00
```

### Cleanup Command
Removes old backups, keeps specified count:
```
✓ Removed 3 old backups
✓ Keeping 5 most recent backups
```

## Integration with VBA Modification

```python
from backup_manager import create_backup

# Always backup before modifying
backup_file = create_backup('perturb_inform.xlsm')
# backup_file = 'perturb_inform.backup.20251211_143000.xlsm'

# Now safe to modify VBA
try:
    modify_vba_code(...)
except Exception as e:
    restore_backup(backup_file)  # Rollback if failed
```

## Files

- `backup_manager.py`: Core backup logic
- CLI: `script/backup_excel.py`

## Related Skills

- `excel-vba-modifier`: Uses backups for safety
- `excel-inspector`: Analyze before backup

## Safety Features

✓ Timestamped naming prevents collisions
✓ Backup verification (file integrity check)
✓ Automatic cleanup (configurable retention)
✓ No overwrites (immutable backups)
✓ Works with any .xlsx/.xlsm files
