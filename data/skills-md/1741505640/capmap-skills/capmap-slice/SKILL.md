---
name: capmap-slice
description: >-
  大需求拆垂直切片：在规格就绪后，于切片/<方案stem>/ 下落盘
  <方案stem>-NN-短名.md（Blocked by DAG、触及、Demo），人工 quiz 通过后方案标已拆分；
  输出推荐运行模式后必须停住。禁止主动开跑或多开会话。
---

# capmap-slice — 拆垂直切片（DAG）

原则：[lifecycle](../capmap-system/reference/lifecycle.md) · [status-tags](../capmap-system/reference/status-tags.md) · [templates](../capmap-system/reference/templates.md)

## 启动

1. 读 `capmap.yaml` → `docs_root`
2. 方案须为 `体量/大`，且规格已存在（通常 `状态/规格中` 且人已确认规格）
3. 路径：`<docs_root>/方案/<主题>/切片/<方案stem>/`

## 硬规则

1. 每张切片必须是 **垂直切片**（可单独 Demo 的行为路径），禁止纯横切片（「先建表再写 API」）
2. 文件名：`<方案stem>-NN-<短名>.md`（NN 从 01 起；**全局唯一**）
3. 文首：类型 `切片` + `状态/待开发`；含 Blocked by、触及、Demo
4. `Blocked by` 构成 **DAG**，禁止成环；quiz 时展示依赖图
5. 触及路径重叠的切片：拆分时加边或拆开，避免可同时开工却改同一路径
6. quiz：粒度、依赖边、能否 Demo、触及冲突 — **人确认前不改方案为已拆分**
7. 人确认后：方案 → `状态/已拆分`；填写方案「执行拆分」
8. **推荐运行模式**（如先 01，再并行 02+03）：写在规格/方案执行拆分中
9. **禁止主动开跑**：不得把任何切片标为 `开发中`；不得 spawn 多会话；推荐后 **停住等人点名**
10. 下一步由用户点名后走 [capmap-gate](../capmap-gate/SKILL.md)

## Checklist

```
- [ ] 1. 读规格与方案；确认体量/大
- [ ] 2. 起草切片列表 + DAG + 触及（先展示 quiz，未批准不落盘或仅草案）
- [ ] 3. 人确认后落盘 <方案stem>-NN-*.md（皆待开发）
- [ ] 4. 方案 → 已拆分；更新执行拆分与推荐运行模式
- [ ] 5. 展示当前 frontier；停住，等人点名
```

## 不做

- 不写规格正文（除非用户同时要求）→ [capmap-spec](../capmap-spec/SKILL.md)
- 不领取/交票/验收 → [capmap-gate](../capmap-gate/SKILL.md)
