---
name: update-wyatt-skills
description: 用于更新 'wyatt_skills'仓库包含的技能集合, 当用户需要更新skills调用.
---

# Update Wyatt Skills

## Overview

本技能提供了一个便捷的方式来更新 `wyatt_skills` 相关的技能。它通过运行一个预定义的脚本来执行官方的更新命令。

## 使用方法

激活本技能后，运行 `scripts/update.sh` 脚本。

**注意：**
- 该脚本执行的是交互式命令。
- 在执行过程中，请提醒用户注意终端输出，并根据提示进行交互式选择。
- 不要尝试自动填充默认值，应由用户手动选择所需项。

### 脚本说明
- **路径**: `scripts/update.sh`
- **功能**: 执行 `pnpm dlx skills add Hu-Wentao/wyatt_skills` 命令。

## 资源

### scripts/
- `update.sh`: 包含更新逻辑的 Shell 脚本。
