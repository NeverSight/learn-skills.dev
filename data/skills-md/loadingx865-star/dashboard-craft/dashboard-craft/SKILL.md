---
name: dashboard-craft
description: 数据看板 / 运营大屏 / 工业控制台的前端工程化开发规范与交付门禁。Engineering workflow, design tokens, chart and component unification, multi-resolution and multi-browser verification, quality gates, and delivery handoff for dashboard, KPI screen, control room, large display, data visualization, admin console, and plant TV projects. Use when building, iterating, refactoring, or reviewing a dashboard-type frontend, when a UI must render correctly on factory TVs, video walls, or control-room displays at 1080p/1440p/4K, or when the user mentions 看板, 大屏, 控制台, 数据可视化, KPI 大屏, 拼接屏. Also use to audit an existing dashboard for hardcoded styles, inconsistent chart theming, or missing responsive verification. 不适用于营销官网、作品集等表达型页面（那类页面请用 frontend-design 类 skill）。
license: MIT
compatibility: 需要 Python 3.9+（scripts/ 下的校验脚本仅用标准库）。refresh_toolchain.py 需要访问 registry.npmjs.org；内网环境请加 --offline。assets/templates/playwright.viewports.ts 需要 Node.js 与 @playwright/test。本 skill 面向 React / Vue 看板类前端，与具体框架版本无关。
metadata:
  version: "2.2.0"
  updated: "2026-09-20"
  author: loadingx865-star
  applies-to: React / Vue 看板类前端
---

# dashboard-craft

看板前端工程化开发规范。把"AI 辅助开发看板"从随机发挥，变成**有约束、有门禁、可验证**。

## 解决什么问题

AI 辅助开发看板时反复出现的三类事故：

1. **适配漂移** —— 开发时只看自己的显示器，交付到工厂电视、控制室大屏时 UI 变形、字号过小、图表模糊。
2. **风格断层** —— 第二期看板与第一期的配色、字号、图表样式不一致，因为设计决策靠每次现场发挥。
3. **拼凑实现** —— 功能能跑，但组件各写各的，越开发越乱。

根因不是"AI 不够强"，而是**缺少约束层与门禁层**。本规范用 8 个阶段解决，每个阶段都有明确的**产出物**与**通过条件（Gate）**。Gate 未通过，不进入下一阶段。

## 五条铁律

违背任一条，产出即视为不合格，必须回退。

1. **无约束不开发** —— 环境约束卡未填写完整，不得写第一行 UI 代码。
2. **无真源不写样式** —— 颜色、字号、间距、圆角、阴影、图表配色必须来自 design tokens，禁止页面内硬编码色值与魔法数字。硬编码包括：hex 色值（含 JSX 属性与内联样式里的字面量）、`rgb()/hsl()`、Tailwind 调色板原子类（`bg-slate-900`）、Tailwind 颜色关键字类（`text-white`）、任意值尺寸（`text-[13px]`）、内联样式数值。**由 `scripts/validate_tokens.py --fail-on-hardcode` 机器判定，不接受口头声明。**
3. **无矩阵不交付** —— 交付前必须跑完"分辨率 × 浏览器"验证矩阵，截图基线已存档。矩阵文件与基线路径由 `scripts/check_gates.py` 校验。
4. **一个概念一处实现** —— 同类组件与图表只有一个实现入口；禁止为赶进度另写一套。**新增看板只允许新增配置与布局编排**：图表与业务组件跨看板复用同一份实现，改一处应全部看板生效。（跨看板复用属人工确认项，见 `references/05-components-charts.md`）
5. **偏离必须登记** —— 任何对设计真源的偏离，都要写入页面级覆盖文件并说明理由，禁止静默偏离。

## 流程总览

| 阶段 | 名称 | 核心产出 | 通过条件（Gate） |
|---|---|---|---|
| 0 | 约束锁定 | 环境约束卡 | 目标分辨率/浏览器/缩放/网络/数据频率全部明确 |
| 1 | 设计单一真源 | design tokens + MASTER 规范 | token 通过校验脚本；图表与缩放策略成文 |
| 2 | 规格与拆票 | spec + 纵向切片任务 | 每张票有可验证验收标准与依赖关系 |
| 3 | 骨架先行 | Layout Shell + 响应式策略 | 空骨架在全部目标分辨率下不破版 |
| 4 | 组件与图表 | 受限组件层 + 图表封装 | 无页面级临时样式；图表全部走封装 |
| 5 | 适配验证 | 多分辨率截图基线 | 矩阵跑通，无溢出/裁切/重叠 |
| 6 | 质量门禁 | 性能/a11y/测试报告 | 预算达标，冒烟全绿，视觉 diff 无意外 |
| 7 | 交付存档 | 交付包 + 基线资产 | 基线存档、回归资产可复跑、文档齐全 |

**阶段 1 与阶段 2 可并行**；阶段 5 与阶段 6 每完成一个功能切片即可增量执行，不必等全部功能完成。

## Gate 机器判定（不接受口头声明）

每个阶段的 Gate 必须由脚本判定，AI 不得自行声称"已通过"。检查对象是**目标项目目录**。

| 阶段 | 判定方式 | 命令 |
|---|---|---|
| 0 | 约束卡存在且无空项/占位符 | `python <skill>/scripts/check_gates.py --project . --stage 0` |
| 1 | token 结构合法、无硬编码样式 | `python <skill>/scripts/validate_tokens.py --tokens design-system/design-tokens.json --src src,app --fail-on-hardcode` |
| 2 | 任务文件含可验证验收标准 | `python <skill>/scripts/check_gates.py --project . --stage 2` |
| 3 | 布局骨架入口存在 | `python <skill>/scripts/check_gates.py --project . --stage 3` |
| 4 | 组件与图表封装各有唯一入口 | `python <skill>/scripts/check_gates.py --project . --stage 4` |
| 5 | 矩阵无未测项、基线已登记 | `python <skill>/scripts/check_gates.py --project . --stage 5` |
| 6 | 报告正文含性能/a11y/冒烟/视觉结论 | `python <skill>/scripts/check_gates.py --project . --stage 6` |
| 7 | README 含部署与回滚 | `python <skill>/scripts/check_gates.py --project . --stage 7` |

一键全查：`python <skill>/scripts/check_gates.py --project .`（`<skill>` 是本 skill 的安装目录）。

**标准项目结构**（Gate 检查据此定位文件，没按此结构组织时才需要 `--tokens/--src` 手动指定）：

```
design-system/
├── constraints-card.md      阶段 0 环境约束卡
├── MASTER.md                阶段 1 人读规范（必须含缩放策略、图表规范、目录结构）
├── design-tokens.json       阶段 1 机读真源
└── pages/<page>.md          页面级受限偏离
specs/*.md                   阶段 2 任务票（每票含验收标准）
acceptance-matrix.md         阶段 5 验收矩阵（含截图基线位置）
src/layouts|views|app        阶段 3 布局骨架入口
src/components + src/charts  阶段 4 组件与图表唯一入口
*report*.md                  阶段 6 性能/a11y/冒烟/视觉报告
README.md                    阶段 7 部署与回滚说明
```

**参数与配置错误不算通过**：`--stage` 只接受 0-7，传其他值直接报参数错误；显式 `--src` 指向的路径全部不存在时判失败——扫描没跑起来等于没检查，脚本不会拿"没有告警"冒充"通过"。

**非标准目录约定也可行**：若项目用 `app/views`、`lib/ui`、`lib/charts` 这类结构，在 MASTER 的「目录结构」小节登记真实路径即可通过阶段 3/4。登记必须按类别语义词对齐（骨架 / 组件 / 图表分别登记），登记一个不相关的目录不会放行整个结构 Gate。

**汇报格式**：每阶段结束时必须贴出脚本命令与其退出码。退出码非 0 即视为 Gate 未通过，不得进入下一阶段。

## 阶段执行要点

### 阶段 0 —— 约束锁定

先问清、再动手。必须落到纸面的是：

- **显示终端**：工厂电视 / 控制室拼接屏 / 办公显示器 / 笔记本 / 移动端，各自型号与物理分辨率。
- **浏览器**：目标浏览器及最低版本，是否包含国产内核浏览器（内核版本、是否缺 WebGL / 导出 / 字体特性）。
- **兼容目标与降级**：Browserslist 查询串、是否需要 legacy 产物、DOM polyfill 清单。**不因老设备就把源码退回 ES5**，目标是声明兼容范围、由构建链按需降级（见 `references/09-toolchain-landscape.md`）。
- **缩放与 DPI**：系统缩放（100% / 125% / 150%）、浏览器缩放、设备像素比。
- **观看距离与交互方式**：是否只读展示、是否需要鼠标/触摸/遥控/键盘操作。
- **数据特性**：刷新频率、单页数据点量级、是否 7×24 长时间运行。
- **网络环境**：是否内网、带宽上限、是否允许外部 CDN（内网通常需本地化字体与依赖）。

模板见 `assets/templates/constraints-card.md`，方法见 `references/01-constraints.md`。

### 阶段 1 —— 设计单一真源

产出 `design-system/MASTER.md` 与 `design-tokens.json`：

- token 分层：**基础值 → 语义值 → 组件值**，上层只引用下层。
- 布局网格：栅格列数、间距刻度、断点定义（含 2560 / 3840 等大屏专用断点）。
- 图表规范：图表库唯一选型、色板顺序、坐标轴/图例/提示框统一样式、空数据与加载态。
- 主题：是否多主题、如何切换。
- 兼容目标：Browserslist 查询串与构建降级策略（若目标含老浏览器）。

大屏特有问题必须在此定死：**字号随分辨率缩放策略**（等比缩放 / 断点重排 / 混合）。这一条决定后期约 90% 的返工量。

> **「避免写死 px」与「整体 scale 缩放」是两条路线，不能同时主张**：选 scale 就按固定设计稿写尺寸（px 必须来自 token 刻度），选重排就用 `rem`/`clamp()` 派生。不要把两句话混着说。

起点模板见 `assets/templates/MASTER.md` 与 `assets/templates/design-tokens.example.json`，方法见 `references/02-design-system.md`。

### 阶段 2 —— 规格与拆票

把设计真源转成可执行任务。每张票是**纵向切片**（贯穿数据 → 组件 → 验证），不是"先写完所有组件再写所有页面"。每张票必须写明交付的可验证行为、阻塞依赖、可勾选的验收标准。

方法见 `references/03-spec-and-tickets.md`。

### 阶段 3 —— 骨架先行

先搭不填肉的 Layout Shell：导航、内容区、栅格容器、卡片槽位、异常态占位。

**关键动作**：骨架必须在全部目标分辨率下先过一遍，确认不破版，再开始填充内容。这一步把适配问题从"交付前"提前到"第一天"。

方法见 `references/04-shell-responsive.md`。

### 阶段 4 —— 组件与图表

- 组件只从受限底座取用（统一组件库 + token），禁止页面内造样式。
- 图表**只有一个封装入口**：统一处理尺寸自适应、主题、空数据、加载、错误、销毁重建，以及 scale 方案下的 DPR 补偿。
- **看板即组合**：第 N 个看板只新增配置与布局编排，复用既有图表与业务组件，禁止复制出第二份实现。
- 每个组件写完后，立即在最小与最大目标分辨率自检。

方法见 `references/05-components-charts.md`。

### 阶段 5 —— 适配验证

用固定视口矩阵截图并与基线比对：

- 视口矩阵覆盖阶段 0 列出的每个真实终端。
- 检查项：溢出、裁切、重叠、字体回退、意外滚动条、图表模糊。
- 基线入库，后续每次改动自动 diff。

模板见 `assets/templates/acceptance-matrix.md`，配置样例见 `assets/templates/playwright.viewports.ts`。

### 阶段 6 —— 质量门禁

- 性能预算：首屏时间、包体积、长时间运行内存曲线。
- 可访问性：对比度、焦点可见、键盘可达。
- 冒烟测试：核心数据链路可跑通。
- 视觉回归：无未登记差异。

四类结论都必须写进报告正文（文件名含 `report`/`报告`），`check_gates.py --stage 6` 会逐项检查；只写"性能"一项的报告不算通过。

方法见 `references/06-verification-matrix.md`。

### 阶段 7 —— 交付

交付包必须包含：源码、设计真源、截图基线、验证报告、部署与回滚说明、可复跑的回归资产。

方法见 `references/07-delivery-handoff.md`。

## 贯穿线：AI 协作规则

AI 是本流程的执行者，必须遵守输入规范与禁止项：

- 任务下达前的 **prompt 模板**（含必填约束字段）。
- **禁止项清单**（禁止引入新图表库、禁止硬编码颜色、禁止跳过骨架直接开发页面等）。
- **变更影响面分析**：改动共享组件或图表前，先列出受影响页面清单。
- **单一真源优先**：样式冲突时以 token 为准，不以页面现状为准。

完整规则见 `references/08-ai-collaboration.md`。

## 工具链选型与更新

本规范绑定当前主流前端工具，**不写死版本**，通过 `references/09-toolchain-landscape.md` 维护"选型 + 更新机制"：

- 记录工具的角色、替代方案、更新频率。
- 用 `scripts/refresh_toolchain.py` 实时拉取最新版本，生成差异报告。
- 每季度复核一次，或在大版本发布时触发。

**升级原则**：小步升级、升级必回归、禁止在交付冲刺期做大版本跃迁。

## 参考文件索引

| 文件 | 用途 |
|---|---|
| `references/01-constraints.md` | 阶段 0 约束锁定方法 |
| `references/02-design-system.md` | 阶段 1 设计单一真源 |
| `references/03-spec-and-tickets.md` | 阶段 2 规格与拆票 |
| `references/04-shell-responsive.md` | 阶段 3 骨架与响应式/大屏适配 |
| `references/05-components-charts.md` | 阶段 4 组件与图表规范 |
| `references/06-verification-matrix.md` | 阶段 5-6 验证矩阵与门禁 |
| `references/07-delivery-handoff.md` | 阶段 7 交付存档 |
| `references/08-ai-collaboration.md` | AI 协作规则与 prompt 模板 |
| `references/09-toolchain-landscape.md` | 工具链选型与持续更新机制 |
| `assets/templates/` | 可直接复制的落地模板 |
| `assets/examples/` | 参考实现形态（图表封装 / 大屏缩放 / 断点 Hook） |
| `scripts/validate_tokens.py` | token 校验 + 硬编码样式检测 |
| `scripts/check_gates.py` | 各阶段 Gate 机器判定 |
| `scripts/refresh_toolchain.py` | 工具链版本实时拉取（支持 --offline） |
