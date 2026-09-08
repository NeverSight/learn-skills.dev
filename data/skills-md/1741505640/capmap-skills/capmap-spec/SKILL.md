---
name: capmap-spec
description: >-
  大需求执行规格：在方案已确认且体量/大之后，写入
  <docs_root>/方案/<主题>/切片/<方案stem>/<方案stem>-00-规格.md（seams、范围、不做、依赖图意向），
  方案主状态标为规格中；等人确认规格后再交给 capmap-slice。禁止拆切片、禁止开跑编码。
---

# capmap-spec — 大需求执行规格

原则：[lifecycle](../capmap-system/reference/lifecycle.md) · [status-tags](../capmap-system/reference/status-tags.md) · [templates](../capmap-system/reference/templates.md)

## 启动

1. 读 `.agents/skills/capmap-system/capmap.yaml` → `docs_root`
2. 打开目标方案：须为 `状态/已确认`（或刚从确认进入本阶段）且 `体量/大`
3. 小需求 / 无体量 → **停止**，提示走短路径或先补体量

## 硬规则

1. **仅** `体量/大`
2. 规格路径：`<docs_root>/方案/<主题>/切片/<方案stem>/<方案stem>-00-规格.md`  
   （`<方案stem>` = 方案 md 文件名去掉 `.md`；文件名须 Vault 内唯一）
3. 规格至少含：Seams、范围（做/不做）、依赖图意向、推荐运行模式（可先占位）、验收证据
4. 方案主状态 → `状态/规格中`（保留 `体量/大`）
5. 方案「执行拆分」可先挂规格链接
6. **禁止**：拆切片文件、把切片标为开发中、暗示已开跑、自动 spawn
7. 写完后 **等人确认规格**；确认前不调用 / 不暗示进入 `capmap-slice` 落盘（可预告下一步）

## Checklist

```
- [ ] 1. 确认体量/大与方案路径
- [ ] 2. 创建切片/<方案stem>/（若不存在）
- [ ] 3. 写 <方案stem>-00-规格.md
- [ ] 4. 方案 Tag → 规格中；文首/执行拆分链到规格
- [ ] 5. 请用户确认规格；确认前停住
```

## 不做

- 不拆切片 → [capmap-slice](../capmap-slice/SKILL.md)
- 不派工/验收切片 → [capmap-gate](../capmap-gate/SKILL.md)
- 不更新底图「已开发」→ [capmap-dev](../capmap-dev/SKILL.md)
