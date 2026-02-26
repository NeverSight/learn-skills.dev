---
name: catalog-repair
description: "自愈：扫描 topics.md 一致性并修复"
tools: ["Bash"]
---

## Purpose

Check and fix consistency of the topics.md index against actual `.memory/` files.

## Checks

1. Dead links → topics.md references non-existent files → auto-delete (`fixed`)
2. Missing registration → bucket files not indexed in topics.md → `ai_actions`
3. Duplicate topics → same topic header appears multiple times → `manual_actions`
4. Invalid anchors → `#anchor` not found in target file → `ai_actions` (if close match) or `manual_actions`

## Required Flow

```bash
memory-hub catalog-repair
```

## Output

JSON envelope with:
- `data.fixed`: auto-fixed items
- `data.ai_actions`: items AI should self-heal
- `data.manual_actions`: items requiring human confirmation

## Post-Processing

After receiving results:
- `ai_actions` non-empty → AI executes self-healing (register missing files via `memory.index`, fix anchors), then runs `catalog-repair` again to confirm cleared
- `manual_actions` non-empty → report to user before task ends
