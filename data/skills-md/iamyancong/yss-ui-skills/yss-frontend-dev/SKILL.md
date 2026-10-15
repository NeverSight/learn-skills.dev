---
name: yss-frontend-dev
description: 开发前端页面、新增或修改前端页面、列表页、表单、微应用业务功能总入口与流程编排器；develop a frontend page。通过状态识别与有限构件分流调度对应专业子 Skill。从零新建空工程项目请使用 create-yss-app，单独维护组件库自身请使用 library 类维护技能。
---

# YSS 前端业务开发与流程编排总线

本 Skill 是业务开发的总入口与分流路由，只做流程控制与子 Skill 渐进式调度，不内嵌具体组件实现细节。

---

## 触发条件

- 用户要求开发、新增或修改 Vue3 微应用前端页面、列表页、表单页或业务功能模块。
- 用户表达意图：“开发前端页面”、“新增业务功能”、“修改前端页面”、“develop a frontend page”。
- 需要在已有微应用中进行业务构件选型、子 Skill 调度与质量门禁校验。

---

## 不适用场景

- **空目录从零新建微应用工程**：当前目录无工程时，必须转交 `../create-yss-app/SKILL.md` 初始化骨架。
- **脱机离线创建微应用**：网络受限脱机时转交 `../yss-create-microapp/SKILL.md`。
- **组件库底层维护**：维护 yss-ui 组件库自身源码、单测或发版请使用 `library` 维护类技能。

---

## 硬约束（禁止/必须）

1. **必须先做状态识别**：若当前目录无 `micro-config.json` 且未依赖 `@yss-ui/components`，**禁止直接写业务代码**，必须转交 `create-yss-app` 且强走 `--dry-run` 预览确认。
2. **必须渐进式按需读取子 Skill**：禁止一次性读取全部 Skill，依据构件类型精准单步加载。
3. **查阅 API 必须使用 MCP**：禁止凭记忆手写组件属性，必须调用 `@yss-ui/mcp` 工具（`get_component_schema`、`get_component_docs`、`get_demo`）。
4. **必须执行本地质量门禁**：代码编写后必须运行工程已有的 `pnpm type-check` 和 `pnpm lint:check`。
5. **未命中构件必须显式标注缺口**：若需求涉及暂未封装的场景（如大屏看板），兜底至 `yss-ui-business-page-generation` 并在交付清单中显式标注【能力缺口】。

---

## 标准代码骨架

依据业务需求涉及的核心构成部件，按需单步加载对应子 Skill：

| 页面构成部件 / 需求特征 | 首要加载 Skill | 按需追加加载 |
|---|---|---|
| **标准列表页**（表格查询、远程分页、工具栏） | `../page-list-module/SKILL.md` | `../ytable-usage/SKILL.md`<br>`../use-table-height/SKILL.md`<br>`../use-url-state/SKILL.md` |
| **可编辑表格**（行内编辑、明细录入、增删行） | `../yedit-table-usage/SKILL.md` | `../use-table-height/SKILL.md` |
| **业务表单**（新增/编辑/查看/步骤向导） | `../page-form-module/SKILL.md` | `../yss-formily/SKILL.md`<br>`../formily-foundation/SKILL.md`<br>`../formily-step-flow/SKILL.md` |
| **树结构 / 左树右表**（组织架构、分类树） | `../ytree-usage/SKILL.md` | `../use-tree-height/SKILL.md` |
| **类 Excel 电子表格**（工作簿、复杂 Sheet） | `../ysheet-usage/SKILL.md` | — |
| **文件导入 / 报表导出下载** | `../yfile-import-usage/SKILL.md`<br>`../file-export-download/SKILL.md` | — |
| **接口对接 / 数据轮询 / 状态同步** | `../api-integration/SKILL.md` | `../use-polling-task/SKILL.md`<br>`../use-url-state/SKILL.md` |
| **主题 Token / 样式规范** | `../theme-token-usage/SKILL.md` | — |
| **未命中上述特定部件**（如大屏、仪表盘等） | `../yss-ui-business-page-generation/SKILL.md` | `../theme-token-usage/SKILL.md` |

---

## 交付检查清单

- [ ] 工程状态已识别，无工程场景已通过 `create-yss-app` 预检创建；
- [ ] 命中的子 Skill 列表记录清晰；
- [ ] 组件 API 契约均来自 `@yss-ui/mcp` 真实查阅记录，无虚构属性；
- [ ] 本地 `pnpm type-check` 与 `pnpm lint:check` 通过；
- [ ] 若存在未覆盖的构件，已在交付清单中显式标注【能力缺口】。

---

## 失败兜底策略

1. **未命中任何有限构件规则**：
   - 统一路由到 `../yss-ui-business-page-generation/SKILL.md` 结合 `../theme-token-usage/SKILL.md` 实现；
   - 在最终交付报告的缺口清单中注明当前未有独立封装 Skill，建议提 issue 追踪。
2. **工程缺少质量脚本**：
   - 若项目未配置 `type-check` 或 `lint` 脚本，在报告中如实说明，不强行执行报错命令。
