---
name: frontend-page-discovery
description: Use when 需要从前端代码证据化产出“页面清单→功能点→业务流程→业务规则”，且项目路由入口不唯一、动态路由/权限/后端菜单复杂、团队容易脑补或遗漏证据链时。
---

# 前端页面清单逆向（证据化）

## 概览

目标：基于代码证据生成页面清单与单页说明文档（落盘到 `docs/`）。

## 何时使用 / 何时不使用

**使用时机（触发信号）**
- 你需要从前端代码得出**可追溯**的页面清单，并继续提炼流程/规则
- 项目路由入口复杂：多 SPA/微前端/多框架共存、运行时注入路由、后端下发菜单
- 团队常见问题：漏页、重复页、权限/动态路由无法落盘、规则总结缺证据

**不使用时机**
- 你只需要写 PRD/原型（这不是代码逆向）
- 你被要求“没代码也要给出你项目的真实页面清单/规则结论”（此时只能交付模板/示例，不能输出事实）

## 本技能的默认交付物（落盘到 docs/）

- `docs/frontend/pages/index.md`
- `docs/frontend/pages/<page_id>.md`
- `docs/frontend/flows/index.md`
- `docs/frontend/conflicts.md`

## 落盘模板（最小可用，可直接复制）

本技能的输出模板已迁移到 `assets/` 目录，以减少技能正文长度并保持模板可复用。

模板映射：
- `docs/frontend/pages/index.md` ← `<本SKILL.md目录>/assets/pages-index-template.md`
- `docs/frontend/pages/<page_id>.md` ← `<本SKILL.md目录>/assets/page-template.md`
- `docs/frontend/flows/index.md` ← `<本SKILL.md目录>/assets/flows-index-template.md`
- `docs/frontend/conflicts.md` ← `<本SKILL.md目录>/assets/conflicts-template.md`

## 硬规则（出现任一条：停止并纠正）

1. **禁止脑补**
   - 任何“页面/流程/规则”必须能指向证据（见下方证据格式）；否则写入 `Evidence Gaps`，不得写推测性结论。
2. **事实与示例必须物理隔离**
   - 若用户要求“大胆假设、不用证据”，只能输出 `EXAMPLE（示例）` 区块或模板；不得把示例写成项目事实，也不得与事实表格混排。
3. **输出字段必须齐全**
   - 页面索引必须包含 `module_name` `page_id` `page_name`。
   - 单页必须包含 `page_name` `breadcrumb` `ascii_wireframe` `核心任务` `关键规则摘要`。

## 证据格式（统一可复核）

每条结论至少附 1 条证据：

- **type**：`page_title | route_decl | file_convention | menu_static | menu_backend | nav_call | guard | api_call | state_machine | form_validation | other`
- **file**：相对路径
- **lines**：`start-end`
- **excerpt**：1–3 行关键摘录（原文）

缺证据时，必须写：

- **gap**：缺什么证据
- **candidate_locations**：可能在哪里找到（目录/文件类型/关键词）
- **impact**：对结论的影响（例如“无法确认是否存在后端下发菜单导致的隐藏页面”）

## 输出字段（必须出现在最终结果里）

- 页面索引：`module_name` `page_id` `page_name`
- 单页：`page_name` `breadcrumb` `ascii_wireframe` `核心任务` `关键规则摘要`

