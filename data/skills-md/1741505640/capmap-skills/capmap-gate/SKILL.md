---
name: capmap-gate
description: >-
  大需求切片门禁：在切片/<方案stem>/ 内计算 frontier（依赖均已验收的待开发切片），
  展示并可复述推荐运行模式；仅在用户点名后开干。交票须 Demo 步骤+自测摘要→待验收；
  仅人确认后已验收并重算 frontier。禁止主动开跑、禁止 Agent 自评通过。
---

# capmap-gate — 切片 frontier / 交票 / 验收

原则：[lifecycle](../capmap-system/reference/lifecycle.md) · [status-tags](../capmap-system/reference/status-tags.md)

## 启动

1. 读 `capmap.yaml` → `docs_root`
2. 定位方案与 `切片/<方案stem>/`（stem = 方案文件名）
3. 方案宜为 `体量/大` 且处于 `已拆分` 或 `开发中`

## 核心概念

| 词 | 含义 |
|----|------|
| **frontier** | 该方案切片目录内：全部 Blocked by 切片均为 `已验收`（或无依赖），且自身为 `待开发` 的集合 |
| **点名** | 用户明确「开 01」「并行开 02 和 03」等；未点名不得开跑 |
| **交票** | Agent 写入 Demo 步骤 + 自测摘要后标 `待验收` |

## 硬规则

1. **只**处理当前方案 `切片/<方案stem>/` 下的切片（不要串到其他方案）
2. 未点名：只展示 frontier、触及冲突提示、推荐运行模式 → **停住**
3. 点名后：校验目标 ⊆ frontier；触及重叠不得同时 `开发中`；合法则标 `开发中`；方案若仍为 `已拆分` 可改为 `开发中`
4. **禁止**领取非 frontier；**禁止** Agent 主动开跑或 spawn
5. 交票 → `待验收`：切片文必须有 **Demo 步骤** 与 **自测摘要**；缺则不得标待验收
6. `待验收` → `已验收`：**仅人确认**（如「通过」「验收完成」）；Agent 不得自评
7. 验收后重算 frontier 并展示；仍不自动开下一张
8. 全部切片 `已验收` 后：走 [capmap-dev](../capmap-dev/SKILL.md)；标完已开发后询问是否转测试；未齐时勿标方案已开发
9. 切片验收 ≠ 功能验证；整功能仍走 [capmap-test](../capmap-test/SKILL.md)（经用户确认转测后）

## 动作速查

| 用户意图 | 行为 |
|----------|------|
| 看 frontier / 能开啥 | 列出 frontier + 推荐；停住 |
| 开某张 / 并行开这些 | 校验后标开发中；开始该切片工作（本窗一张） |
| 交票 / 做完了 | 写 Demo+自测 → 待验收；等人 |
| 验收通过 | 已验收 → 重算 frontier → 展示；停住 |

## Checklist

```
- [ ] 1. 解析方案 stem 与切片目录
- [ ] 2. 计算 frontier；检查触及冲突
- [ ] 3. 无点名 → 展示后停住
- [ ] 4. 有点名 → 合法开干（开发中）
- [ ] 5. 交票材料齐全 → 待验收
- [ ] 6. 人确认 → 已验收 → 重算 frontier
```

## 不做

- 不拆新切片清单（大改拆分）→ [capmap-slice](../capmap-slice/SKILL.md)
- 不写功能测试文档 → [capmap-test](../capmap-test/SKILL.md)
