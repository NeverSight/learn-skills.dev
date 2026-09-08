---
name: capmap-archive
description: >-
  将已闭环的方案归档到 <docs_root>/_archive：更新能力底图、移动全文、删除活跃副本。
  宜在开发标识之后，并视需要完成测试/规范。docs_root 见 .agents/skills/capmap-system/capmap.yaml。
---

# capmap-archive — 方案归档

原则：[lifecycle](../capmap-system/reference/lifecycle.md) · Tag：[status-tags](../capmap-system/reference/status-tags.md)

## 启动

1. 读 `.agents/skills/capmap-system/capmap.yaml` → `docs_root`、`archive_policy`
2. 确认方案已可归档（建议：已 capmap-dev；若需要则测试/规范已挂链）

## 硬规则

1. 全文 → `<docs_root>/_archive/方案/<主题>/`
2. **删除**活跃副本（不留 stub）
3. 文首回链底图；§6 考古行
4. **不**把 `规范/`、`测试/` 当方案删掉（测试可选另存 `_archive/测试/`）

## Checklist

```
- [ ] 1. 解析 docs_root；待归档列表
- [ ] 2. 核对底图 §1/§2/§3；底图无 `状态/*` Tag
- [ ] 3. 移入 _archive；删活跃副本；§6 更新；归档文 YAML：`方案` + `状态/已归档`
- [ ] 4. 自检主题目录
```

若用户只要「代码完了就归档方案」：允许，但须在底图保留 §2，并提醒测试/规范未做。
