---
name: b-end-design-system
description: "B端工业级设计系统与组件规范执行Skill。将资深UI/UX设计系统、组件选型否定判据(avoidWhen/doNot)、弹窗抽屉模态解耦、六大业务页面模板骨架、0.5px微边框与光学同心圆角转化为可执行的AI生成与审查约束。用于B端页面设计、组件搭建、代码审查与高保真原型还原。"
version: 1.0.0
tags: [design-system, ui-ux, b-end, components, rules, archetypes]
---

# B端设计系统与组件规范 AI 执行引擎 (Ludi Design System Skill)

本 Skill 是面向 AI 编程助手（Agent、Claude Code、Cursor、Windsurf、Codex 等）的可执行设计系统指令层。它彻底终结“AI 拼装页面毫无设计感、组件乱堆、弹窗抽屉滥用、色彩失控”的行业通病，将资深设计师的决策直觉转化为确定性的工程生成约束。

---

## 核心执行工作流 (Standard Workflow)

每当接收到任何 B 端界面生成、修改或审查需求时，按以下六步顺序执行：

```
[步骤 1: 需求解构] ──► 抽取实体角色、核心对象、操作频次与生命周期状态
        │
[步骤 2: 模板匹配] ──► 从六大页面骨架中唯一确定页面形态 (references/05)
        │
[步骤 3: 布局骨架] ──► 搭建 PageHeader -> FilterPanel -> DataSection -> BulkActionBar
        │
[步骤 4: 选型判据] ──► 执行 7 大否定判据，确定 Modal vs Drawer vs Page (references/03 & 06)
        │
[步骤 5: 原子约束] ──► 坚守 Button 唯一主操作、Badge 80% 浅底深字、0.5px 微边框 (references/01 & 02)
        │
[步骤 6: 闭环走查] ──► 运行 15 项设计系统硬门禁与五态检查 (references/07)
```

---

## 必须遵守的三大底层硬红线 (Non-Negotiable Redlines)

1. **绝对禁止粗黑边框与机器居中**：
   - 分割线与卡片边框优先采用 **0.5px 精细微边框**（如 `border: 1px solid rgba(226, 232, 240, 0.7)`）。
   - 外层与内层元素必须满足**同心圆角几何法则**：$R_{outer} = R_{inner} + Padding$。
   - 图标+文字按钮做光学重心微调，模态弹窗垂直位置固定于视口 38.2% 黄金分割位。

2. **操作区与业务状态严肃性**：
   - **主操作唯一**：一个独立操作区域（页头、表格工具栏、弹窗底栏）**最多只能有 1 个 Primary 主按钮**。
   - **审批与责任二选一中立**：“审批通过”与“驳回”均采用次级按钮样式，严禁用视觉色差诱导用户。
   - **Badge 80% 浅底深字黄金法则**：严禁无业务语义的彩虹乱配色；严禁用深色刺眼底色；必须带明确业务文案。

3. **浮层防丢失与破坏性阻力**：
   - **弹窗防手滑丢失**：含录入表单的 Dialog/Modal 必须显式设置 `maskClosable={false}`。
   - **模态 ≠ 阻断**：查看详情优先使用**侧边抽屉 (Drawer)** 或同页展开，保留列表背景上下文；需要独立协同分享时使用独立整页；避免无脑使用居中阻断弹窗。
   - **高危操作阻力**：删除、清空、扣费必须使用 `ConfirmDialog`，标题中立交代对象，描述交代不可逆后果，按钮采用明确动宾文案（如“彻底删除”）。

---

## 深度参考规范库导航 (References Index)

遇到具体设计决策时，精准查阅 `references/` 目录下的专门手册：

- **基石与视觉法则**：[01-design-tokens-and-foundations.md](./references/01-design-tokens-and-foundations.md)
  - 色彩语义四层分级、0.5px 微边框配方、同心圆角几何计算、阴影防 overflow 裁切公式。
- **基础原子组件**：[02-primitive-components.md](./references/02-primitive-components.md)
  - Button 五层视觉阶梯、主操作判定五步法、Badge 业务映射表、Radio/Switch/Select 否定判据。
- **浮层与反馈系统**：[03-overlays-dialog-drawer.md](./references/03-overlays-dialog-drawer.md)
  - 模态与阻断解耦、Modal vs Drawer 选型决策树、三档推荐尺寸与三分屏高度、从列表进入详情四大判据。
- **复合组件与数据结构**：[04-composite-components.md](./references/04-composite-components.md)
  - DataGrid 表格列三向对齐、FilterPanel 三态、DescriptionGrid 四层区隔、BulkActionBar、五态覆盖法。
- **六大页面模板骨架**：[05-page-templates-and-archetypes.md](./references/05-page-templates-and-archetypes.md)
  - 列表页 5 种形态、表单页 4 级复杂度、详情页 3 种模式、看板 KPI 约束、设置页即时保存判据。
- **组件选型 7 大否定判据与反模式**：[06-component-priority-and-anti-patterns.md](./references/06-component-priority-and-anti-patterns.md)
  - 量级/频次/时长/重要性/语义/结构错配的退出机制、40+ 条高频避坑红线。
- **交付前自查硬清单**：[07-design-system-audit-checklist.md](./references/07-design-system-audit-checklist.md)
  - 15 项视觉与交互门禁走查表。

---

## 开箱即用实战模板 (Templates)

生成真实代码时，可直接参考或复制 `templates/` 目录中的标准工程代码：
- `templates/list-page-template.tsx`：标准查询表格 + 批量浮条 + 抽屉轻编辑 + 确认删除弹窗。
- `templates/form-page-template.tsx`：Top-aligned 标签置顶 + 卡片语义分组 + 离开防丢脏检查。
- `templates/detail-page-template.tsx`：DetailHeader + DescriptionGrid + Tabs 辅助页签 + 审计时间线。
- `templates/dashboard-page-template.tsx`：问候语 + 4个核心 KPI 趋势卡片 + 轻量原生柱状图 + 快捷直通。

---

## 自动化校验脚本 (Lint Script)

代码生成完成后，可随时执行 Python 走查脚本自检：
```bash
python scripts/audit-design-rules.py path/to/your/code
```
