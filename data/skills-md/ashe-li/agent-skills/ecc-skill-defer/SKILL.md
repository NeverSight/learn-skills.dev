---
name: ecc-skill-defer
description: Manage ECC skill loading — defer unused skills to save init tokens, restore on demand. Use when user wants to check, defer, or restore ECC skills.
user_invocable: true
---

# /ecc-skill-defer — ECC Skill 漸進式載入管理

管理 ECC skills 的 defer/restore 狀態，減少 init token 消耗。

## Instructions

Run the script at this skill's directory: `ecc-skill-defer/ecc-skill-defer.sh` (relative to the skills repo root), or the installed copy at `~/.claude/scripts/ecc-skill-defer.sh`.

### Available commands

| Command | Description |
|---------|-------------|
| `status` | Show active/deferred counts |
| `list` | Show all skills with their status |
| `apply` | Defer skills listed in config (use after ECC update) |
| `restore <name>` | Activate a single deferred skill |
| `restore --all` | Restore all deferred skills |

### Default behavior

If no argument is provided by the user, run `status` then `list`.

### Config

The defer list is at `ecc-skill-defer.conf` (same directory as the script). To add/remove skills from the defer list, edit this file then run `apply`.

### After restoring a skill

Tell the user: "Skill restored. It will be available in the **next session** (or after context reload)."

### Notes

- **規劃相關 skill 保護提醒：** design、assist 為核心規劃 skill，defer 這些 skill 會影響業界/學術參照與 ECC 資源分配的品質。defer 前應確認使用者了解此影響。
- **ECC 資源一致性：** apply 後應提示使用者當前可用資源清單，確保後續 skill 執行時能正確判斷可用的 agent/skill。
