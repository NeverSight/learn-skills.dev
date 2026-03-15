---
name: business-card-intake
description: Use when processing business-card images from 商务/图/未处理名片, renaming files by detected person name, moving cards to 商务/图/名片, and creating person notes from 模版/人物介绍 with YAML extracted from the card.
---

# Business Card Intake

## Overview
Use this skill to batch-process business card images with script-first reliability.

Pipeline:
1. Read images from `商务/图/未处理名片`
2. OCR detect person name and rename file to that name
3. Move renamed image to `商务/图/名片`
4. Create note in `商务/人物/<人物名>.md` from `模版/人物介绍.md`
5. Fill YAML fields from OCR text when available, leave unknown fields empty
6. Insert card image immediately after `## 照片::` on the same line

This version is self-contained and does not import repository `scripts/*`.
Dependency: `tesseract` must be available in PATH.

## Run

```bash
python3 skills/business-card-intake/scripts/process_cards.py
```

Useful options:

```bash
python3 skills/business-card-intake/scripts/process_cards.py --dry-run
python3 skills/business-card-intake/scripts/process_cards.py --backend tesseract
python3 skills/business-card-intake/scripts/process_cards.py --overwrite-notes
```

## Sync Existing People Notes (Structure Only)

Use this when `模版/人物介绍.md` changed and you want to update existing notes in `商务/人物` without adding new semantic content.

This sync does only structural adjustments:
- Reorder existing YAML keys to match the template order
- Sync all template inline fields `## 标题::` (add/remove/reorder by template, keep existing value when same title exists)

Run preview:

```bash
python3 skills/business-card-intake/scripts/sync_people_structure.py
```

Apply changes:

```bash
python3 skills/business-card-intake/scripts/sync_people_structure.py --apply
```

Template keys are now always strict (source of truth):

```bash
python3 skills/business-card-intake/scripts/sync_people_structure.py --apply
```

Strict behavior:
- Add missing YAML keys from template (use template default value)
- Remove YAML keys not present in template

Rename mapping (preserve values after key/title rename):

```bash
python3 skills/business-card-intake/scripts/sync_people_structure.py \
  --yaml-rename old_key:new_key \
  --inline-rename 旧标题:新标题 \
  --apply
```

Safety guard:
- Rename target must already exist in current template; otherwise script exits with error.

## Paths
- Input: `商务/图/未处理名片`
- Output images: `商务/图/名片`
- Output notes: `商务/人物`
- Template: `模版/人物介绍.md`

## Outputs
The script writes:
- `商务/图/名片/card_intake_log_YYYYMMDD_HHMMSS.csv`
- `商务/图/名片/card_intake_undo_YYYYMMDD_HHMMSS.sh`

Use the undo script to roll back image moves/renames quickly if needed.
