---
name: visual-report
description: |
  将文字、图片、文件转换为交互式可视化网页报告。当用户想要：制作汇报材料、生成可视化报告、把内容整理成 PPT/PDF、创建信息图、将会议纪要/数据/文档可视化展示时使用此 skill。关键词包括：报告、汇报、可视化、PPT、PDF、信息图、dashboard、canvas、napkin 风格、数据展示。即使用户只是说"帮我整理成好看的格式"或"我要发给领导看"，也应该考虑使用此 skill。
  Use this skill for interactive visual reports, dashboards, executive-ready summaries, infographics, and PPT/PDF exports built from notes, documents, screenshots, tables, or datasets.
---

# Visual Report Generator

将用户提供的文字、图片、文件整合成精美的交互式可视化网页报告，支持导出为 PDF 和可编辑 PPT。

Create polished interactive visual reports from text, images, and files, with optional PDF export and editable PPT output.

在 Codex 中触发此 skill 时，默认要把报告实际落盘为当前工作目录内的文件，并返回绝对路径；不要只输出一段 HTML 代码。

## 设计风格：Dark Glass Morphism

采用 Gemini Canvas / Napkin 风格：
- **深色背景**：`background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%)`
- **玻璃拟态**：`.glass { background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }`
- **渐变卡片**：粉红、橙色、青色、紫色渐变
- **丰富图表**：根据数据类型自动选择柱状图、环形图、折线图、进度环等

## 核心理念

用户的目标是**快速产出专业的可视化汇报材料**，而不是阅读长篇文字。你的任务是：
1. 完整理解所有输入内容，不遗漏任何信息
2. 智能组织结构，让信息层次分明
3. 用可视化元素（卡片、图表、时间线、指标等）替代纯文字
4. 将图片放置在语义上最合适的位置
5. **智能选择图表类型**，让数据更直观
6. 当内容本质上更适合结构图、逻辑图、导图、时间线、决策树时，不要硬塞成普通卡片或表格

## 版式原则（必须遵守）

先决定**页面骨架**，再填充组件；不要先堆组件再拼页面。

必须遵守以下规则：

1. 先判断内容是**数据密集型**、**叙事复盘型**、**对比决策型**还是**卡片展示型**
2. 同一行或同一屏中的模块，信息量应大致平衡；不要让一个很短的模块占据一整列
3. 如果左右两列预计高度差明显，优先改成上下结构，或把较短的一侧拆成多个小模块补齐
4. **短表格（2-3行）/短列表（2-3项）/单段摘要**，不要单独和高密度模块并排占据整列
5. 表格、流程卡、时间线、图表的组合必须考虑视觉重心，避免出现大面积无意义留白
6. 当内容本身不适合双栏时，宁可做纵向叙事结构，也不要为了“版式丰富”强行左右并排

详细版式规则见 `references/layout-rules.md`。
结构图与逻辑图样式见 `references/visual-patterns.md`。

## 工作流程

### Step 0: 识别输出模式（必须首先执行）

根据用户输入判断输出模式：

| 关键词 | 输出模式 | 说明 |
|-------|---------|------|
| PDF、打印、下载 PDF | **PDF 模式** | 生成打印优化布局，并导出稳定 PDF |
| PPT、幻灯片、演示 | **PPT 模式** | 生成交互式幻灯片，支持键盘翻页 |
| 表格、Excel、数据表 | **表格模式** | 生成可排序/搜索/导出的交互表格 |
| 报告、汇报、可视化（默认） | **报告模式** | 生成标准可视化报告 |

**模式优先级**：用户明确指定 > 内容特征推断 > 默认报告模式

### Step 0.1: PPT 模式专属决策（仅 PPT 时必须执行）

如果输出模式是 **PPT 模式**，在写任何 HTML 之前，必须额外完成以下决策：

1. 先选一个 **PPT 主题家族**：`summit-dark`、`signal-grid`、`editorial-stage`、`ember-premium`
2. 再选一个 **幻灯片节奏**：封面页 → 章节页 → 指标页 / 论点页 / 双栏页 / 表格页 → 结尾页
3. 每页只表达 **一个主结论**；同一页超过 5 个要点或一段正文过长时，必须拆成两页
4. HTML 必须带语义标记，便于导出器识别版式：
   - `body[data-ppt-theme]`
   - `section.ppt-slide`
   - `data-slide-type="cover|section|metrics|two-column|bullets|table|closing"`
   - `.ppt-panel`、`.ppt-metric-card`、`.ppt-bullets`、`.ppt-summary`

PPT 主题、页面节奏和语义结构规则详见 `references/ppt-styles.md`。

### Step 0.2: PDF 模式专属决策（仅 PDF 时必须执行）

如果输出模式是 **PDF 模式**，不要把“浏览器打印”当成默认方案，必须先做以下判断：

1. 先判断是 **报告型 PDF** 还是 **幻灯片型 PDF**
   - 报告型 PDF：连续阅读、A4 纵向、多页滚动内容
   - 幻灯片型 PDF：逐页翻阅、16:9 横向、每页一个完整 screen
2. 为 PDF 单独准备 **打印重排规则**
   - 报告型 PDF：把复杂 grid / 双栏 / 卡片矩阵在打印时重排成更稳定的单栏或平衡结构
   - 幻灯片型 PDF：强制每张 slide 单独成页，隐藏导航点和交互控件
3. 不要只写简单的 `@media print` 就结束；如果用户明确要 PDF，默认运行导出脚本
4. 优先使用以下语义或辅助类，便于打印重排：
   - `.avoid-break`
   - `.print-stack`
   - `.pdf-page-break`
   - `.ppt-slide`

PDF 布局和打印重排规则详见 `references/pdf-export.md`。

### Step 1: 确定输出路径

在开始任何工作之前，**必须先确定当前工作目录**：
1. 读取系统上下文中的 `cwd`
2. 默认将此路径作为报告输出的目标目录
3. 构建完整的输出文件路径，例如：`{cwd}/report.html`
4. 如果用户明确指定了目录或文件名，优先使用用户指定路径

**示例**：如果用户在 `/Users/larry/Documents`，则输出路径为 `/Users/larry/Documents/report.html`

### Step 2: 分析输入内容

收集用户提供的所有材料：
- 文字内容（会议纪要、汇报要点、说明文档等）
- 图片（产品截图、流程图、数据图表等）
- 文件（PDF、Word、Excel 等）

对每个输入进行分类：
- **核心内容**：需要完整呈现的主体信息
- **支撑数据**：数字、指标、统计信息 → 用可视化组件展示
- **视觉素材**：截图、照片 → 智能放置到相关段落

### Step 2.1: 图片智能处理

判断每张图片的用途：

**展示型图片**（直接嵌入报告）：
- 产品截图、UI 界面
- 照片、示意图
- 用户明确说"展示"、"放上去"的图片

**数据型图片**（提取内容融入报告）：
- 表格截图 → 提取数据，生成可视化表格或图表
- 图表截图 → 提取关键数据点，重新绘制
- 流程图 → 理解流程，用更美观的方式重绘
- 用户说"如图所示的数据"、"根据这个表格"时

**判断依据**：
- 上下文提及方式："产品截图" vs "数据如下"
- 图片内容本身：是否包含大量文字/数字
- 用户意图：展示外观 vs 传达信息

### Step 3: 设计报告结构

先选**版式骨架**，再决定每个模块放在哪里。

根据内容类型选择合适的结构：

**纵向叙事版**（会议纪要、方法复盘、策略说明）：
```
标题 + 核心结论
├── 对比/结论区（全宽）
├── 流程/方法区（全宽或平衡双栏）
├── 关键收获卡片
└── 风险 / 下一步
```

**平衡双栏版**（左右内容密度接近时才使用）：
```
标题 + 核心结论
├── 左栏模块（信息量 A）
└── 右栏模块（信息量 B，A 与 B 接近）
```

**数据驾驶舱版**（经营复盘、渠道分析、销售数据）：
```
标题 + 核心发现
├── 关键指标卡片
├── 图表区域
├── 数据表格
└── 洞察与建议
```

**卡片矩阵版**（亮点、单品、模块展示）：
```
标题 + 一句话概述
├── 亮点卡片矩阵
├── 次级对比/补充信息
└── 结论/建议
```

**汇报型**（工作汇报、项目进展）：
```
标题 + 核心结论
├── 关键指标卡片（3-5个）
├── 主要内容（分模块，每模块配图）
├── 数据图表
└── 下一步计划 / 总结
```

**说明型**（产品介绍、方案说明）：
```
标题 + 一句话概述
├── 亮点/特性卡片
├── 详细说明（图文并茂）
├── 对比表格（如有）
└── 结论/建议
```

**数据型**（数据分析、统计报告）：
```
标题 + 核心发现
├── 关键数字大卡片
├── 图表区域
├── 数据表格
└── 洞察与建议
```

详细版式选择、模块配对和反留白规则见 `references/layout-rules.md`。

### Step 3.1: 模块配对检查（必须执行）

在开始写 HTML 前，先检查一次模块是否配对合理：

- 如果左侧是**短表格/短列表**，右侧不要放 4 个以上的高卡片堆栈；优先改成上下结构
- 如果一侧是**多步流程**，另一侧必须是图表组、卡片组或较丰富的摘要模块；不要只放一个短模块
- 如果某个模块内容只有 2-3 行，不要让它独占半屏高度
- 如果图表、表格、卡片数量明显不平衡，优先把短模块并入其他 section，而不是硬保留双栏
- 当你预估某一列会出现明显大块留白时，必须重排

### Step 4: 生成可视化报告

使用 HTML + Tailwind CSS + Chart.js 生成报告。

如果是 **PPT 模式**：
- 先按“幻灯片”组织 HTML，再考虑滚动浏览体验；不要把长报告直接塞进导出器
- 必须有版式节奏变化，不要连续 3 页使用完全相同的布局
- 指标页优先使用 3-4 张大卡片；长段落优先拆成论点页或双栏页
- 表格页一页只放 1 张表；如果行数过多，拆页或改成卡片摘要
- 给 PPT 导出器提供语义化结构，优先使用 `section.ppt-slide` 和 `references/ppt-styles.md` 中定义的类名

如果是 **PDF 模式**：
- 默认同时产出可预览的 HTML 和导出的 PDF
- 不要依赖用户手动 `Cmd/Ctrl + P`；优先运行 `scripts/export_pdf.py`
- HTML 中必须带打印重排 CSS，确保 PDF 导出时可自动改成更稳定的分页布局
- 即使用户最终使用 `Cmd/Ctrl + P`，页面本身也必须具备 print-safe CSS 和 `beforeprint` / `matchMedia('print')` 兼容逻辑
- 报告型 PDF 优先保证：单栏可读、模块不断裂、表格不跨页碎裂、图表不挤压
- 幻灯片型 PDF 优先保证：一页一张 slide、分页干净、交互控件隐藏、背景和色彩保留

**基础结构**：
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{标题}}</title>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
/* 打印时保留颜色 */
@media print {
  * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; color-adjust: exact !important; }
  body { background: #0f172a !important; }
  .no-print { display: none !important; }
}
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); min-height: 100vh; }
.glass { background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }
</style>
</head>
<body class="text-white p-8">
<div class="max-w-5xl mx-auto">...</div>
<script>Chart.defaults.color = '#94a3b8'; /* 图表代码 */</script>
</body>
</html>
```

**图表选择指南**（AI 自动判断）：

| 数据类型 | 推荐图表 | 示例场景 |
|---------|---------|---------|
| 多项对比（3-6项） | 柱状图 | 各渠道 GMV 对比 |
| 增长率/排名 | 横向条形图 | 品类 YOY 增长排名 |
| 占比（2-3项） | 环形图 | 流量来源占比 |
| 单一占比指标 | SVG 进度环 | 目标达成率 |
| 时间趋势 | 折线图 | 月度销售趋势 |

**核心组件**：
- 渐变指标卡片（突出关键数字）
- 玻璃表格（结构化数据）
- Chart.js 图表（数据可视化）
- 带图标列表项（爆款/亮点展示）

详细模板代码见 `references/templates.md`。
版式与模块组合规则见 `references/layout-rules.md`。

### Step 5: 输出文件（关键步骤 - 必须执行）

**⚠️ 这是最重要的步骤，必须完整执行以下操作：**

**默认输出路径：当前工作目录**
- 默认输出到当前 `cwd`：`{cwd}/report.html`
- 如果用户指定了其他路径，则使用用户指定的路径

**⚠️ 写入策略：分段写入大文件**

在 Codex 中，优先直接生成完整、可运行的 HTML 文件。对于复杂报告：

1. **简单报告（<4000字符）**：一次性写入
2. **复杂报告（>4000字符）**：
   - 先创建基础结构（`head` + 首屏内容）
   - 再分段补齐剩余内容，优先使用 `apply_patch` 在 `</body>` 前插入
   - 仅在确实必要时拆分为多个文件；默认优先保持单文件 HTML

**组件数量建议**：
- 指标卡片：3-4 个
- 图表：2-3 个（根据数据类型选择）
- 表格：1-2 个
- 列表项：按需

**写入后验证**：
```bash
open {输出文件路径}
```

如果环境不适合自动打开，至少要返回生成文件的绝对路径，并说明如何预览。

**文件要求**：
- 自包含，所有样式通过 Tailwind CDN 引入
- Chart.js 通过 CDN 引入
- 响应式设计，支持手机/平板/电脑查看
- 如果用户明确要 PDF，默认同时生成 `{cwd}/report.html` 和 `{cwd}/report.pdf`
- 如果用户明确要 PPT，默认同时生成 `{cwd}/report.html` 和 `{cwd}/report.pptx`

**导出说明**（告知用户）：
- PDF：`python ~/.codex/skills/visual-report/scripts/export_pdf.py /absolute/path/to/report.html /absolute/path/to/output.pdf`
- PPT：`python ~/.codex/skills/visual-report/scripts/export_pptx.py /absolute/path/to/report.html /absolute/path/to/output.pptx`

## 语言处理规则

- 根据用户输入语言自动选择报告语言
- 中文报告中保留约定俗成的英文术语：
  - 技术名词：API、SDK、UI、UX、App、Web
  - 缩写：KPI、ROI、OKR、SLA、MVP
  - 品牌/产品名：保持原样
- 不要强行翻译专业术语

## 质量检查清单

生成报告前确认：
- [ ] 所有输入信息都已包含，无遗漏
- [ ] 数据准确，数字无误
- [ ] 图片放置位置与上下文语义匹配
- [ ] 视觉层次清晰，重点突出
- [ ] 配色协调，专业美观
- [ ] 没有大面积无意义留白
- [ ] 左右栏内容密度平衡；如果不平衡，已经改成上下结构或拆分补齐
- [ ] 短表格 / 短列表没有单独占据整列
- [ ] 模块信息量与占位大小相匹配
- [ ] 如果是 PPT，已经选定主题家族，且封面 / 章节 / 内容 / 结尾页节奏明确
- [ ] 如果是 PPT，没有连续多页机械重复同一种版式
- [ ] 如果是 PPT，单页只表达一个主结论；超长内容已拆页
- [ ] 如果是 PDF，已经区分报告型 PDF 和幻灯片型 PDF
- [ ] 如果是 PDF，打印时复杂布局已重排，不会出现双栏碎裂和大面积错位
- [ ] 如果是 PDF，表格、图表、卡片都设置了避免分页断裂的规则

## 报告模板

参考 `references/templates.md` 获取完整的 HTML 模板代码。
参考 `references/layout-rules.md` 获取布局判断和模块组合规则。
如果是 PPT，额外参考 `references/ppt-styles.md` 获取主题家族、幻灯片节奏和语义类名。
如果是 PDF，额外参考 `references/pdf-export.md` 获取打印重排和分页规则。
如果内容需要流程图、逻辑图、导图、路线图、矩阵图，额外参考 `references/visual-patterns.md`。

## PDF 导出

当用户需要 PDF 时，运行 skill 目录下的脚本：

```bash
python ~/.codex/skills/visual-report/scripts/export_pdf.py /absolute/path/to/report.html /absolute/path/to/output.pdf
```

脚本会基于 Chrome headless 打开 HTML，等待页面渲染完成后再导出 PDF，并在导出时自动注入打印重排样式。优先使用该脚本，不要默认让用户手动打印。

## PPT 导出

当用户需要 PPT 时，运行 skill 目录下的脚本：

```bash
python ~/.codex/skills/visual-report/scripts/export_pptx.py /absolute/path/to/report.html /absolute/path/to/output.pptx
```

脚本会解析 HTML 结构，生成对应的 PPT 幻灯片。详见 `scripts/export_pptx.py`。

## 示例

**用户输入**：
> 帮我把这个会议纪要做成可视化报告：
> 1. Q4 销售额达成 120%，超额完成目标
> 2. 新增客户 50 家，重点客户 A 公司签约 200 万
> 3. 下季度目标：拓展华东市场
> [附：销售数据表格截图] [附：新产品界面截图]

**输出**：
- 标题卡片：Q4 销售总结
- 指标卡片：120% 达成率 | 50 新客户 | 200万 重点签约
- 数据图表：从截图提取数据，绘制柱状图
- 产品截图：放在"下季度计划"部分，配文字说明
- 下一步：华东市场拓展计划要点
