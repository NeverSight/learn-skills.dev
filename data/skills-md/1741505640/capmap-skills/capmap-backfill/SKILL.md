---
name: capmap-backfill
description: >-
  从 git 追溯并反补 <docs_root> 下能力底图 §4（及必要时 §1/§2/§5）。docs_root 见
  .agents/skills/capmap-system/capmap.yaml。适用于「反补底图」「从 git 整理变更轨迹」。可独立使用。
---

# capmap-backfill — git 追溯反补

原则：[capmap-system](../capmap-system/SKILL.md) · Tag：[status-tags](../capmap-system/reference/status-tags.md)

## 启动

1. 读 `.agents/skills/capmap-system/capmap.yaml` → `docs_root`、`main_branch`
2. 无配置 → 先 [capmap-init](../capmap-init/SKILL.md)

## 定位

- 策展：只合并关心的合入；按**能力**写 §4，非按月大表
- 不创建全局台账 / ledger_id

## 输入

- 主题 / 底图路径（相对 docs_root）
- 时间窗、代码路径或关键字
- 主分支（配置默认）

## 推荐命令

```bash
git log <main_branch> --oneline --no-merges --since="2 weeks ago" -- <code_path>...
git log <main_branch> --oneline --no-merges --grep="<kw>" -i
git show --stat <hash>
```

## Checklist

```
- [ ] 1. 解析 docs_root；锁定底图文件
- [ ] 2. git log 候选；必要时列出拟写入/跳过
- [ ] 3. 更新 §4（及必要 §1/2/5）；若改了 §1 → 同步 YAML `状态/*` 集合
- [ ] 4. 链接健全性（反补时一并修）：
       - 底图文首/§0 用**唯一文件名**列出进行中方案 `[[方案文件名]]`
       - 各方案文首有回链 `[[能力底图-…]]`（缺则补，见 templates）
       - 禁止写入 `\|`；别名用 `[[名|别名]]`
- [ ] 5. 汇报写入/跳过数量；孤儿笔记数（无入链且无出链）应为 0
```
