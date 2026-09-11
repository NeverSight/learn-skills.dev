---
name: agent-html
description: 为 AI Agent 提供基于 shadcn/ui 极简现代美学的单文件 HTML 组件化规范与母版体系。当用户要求“生成 HTML 页面/网页”、“前端可视化大盘/看板”、“面试/分析/测试报告”、“对比矩阵/方案比对”、“review 结果做成可视化页面”、“代码审查报告”、“不要输出 markdown 墙/不要文字墙”、“把分析结果做成可交互单文件网页”等场景时，务必使用本 Skill。零构建、零 npm、严禁引入外部 CDN（无断网白屏风险），纯原生 HTML/CSS/SVG，支持暗黑模式与双击秒开。
---

# Agent HTML 设计系统与组件化规范

本规范指导 AI Agent 如何生成**高信息密度、工业级质感、零外部依赖、双击秒开**的单文件 HTML。

---

## 零、价值研判准则：何时用 HTML，何时坚决不用 (Judgment Rules)

> **黄金法则**：*Markdown 是事实来源（Source of Truth），HTML 是人类决策与评审表面（Human Review Surface）。*

并不是所有输出都需要制作成 HTML。在动手前，AI Agent 必须先做价值研判：

### 1. 优先使用 HTML 的场景（具备以下任一特征）：
- **空间性与多维性 (Spatial)**：宽屏数据大盘、左右双栏日志审查器、指标统计网格、密集状态看板；
- **并行与对比性 (Parallel / A-B)**：基准 vs 挑战者、版本 Diff、模型评测、方案取舍矩阵；
- **可交互与即时过滤 (Interactive / Filterable)**：包含数十条记录需毫秒级搜索、多 Tab 切换、手风琴折叠展开；
- **供人类正式决策/归档 (Human Review Surface)**：正式架构评审、面试录用报告、技术复盘白皮书、发布日志。

### 2. 坚决不要使用 HTML 的场景（留在终端 Markdown 即可）：
- **线性单线条内容**：普通的问答、短解释、单次代码段说明（< 200 字）；
- **纯终端命令/脚本**：用户需要立即在终端复制执行的 shell 命令；
- **无空间结构的信息**：没有表格、没有对比、没有维度的流水账文本；强行输出 HTML 会打断用户终端心流并浪费 Token。

---

## 一、10 大反模式规避清单 (Anti-Patterns to Avoid)

在生成 HTML 时，严禁出现以下常见 AI 反模式：

1. **穿 HTML 外衣的普通 Markdown (Markdown in an HTML Trenchcoat)**：只是用 `<p>` 和 `<h1>` 包裹几大段流水账文字，完全没用上卡片、网格、状态徽章与 Callout。
2. **偷渡外网 CDN / 远程字体**：引入 Tailwind CDN、Google Fonts、CDN 脚本。在离线环境、内网机房直接白屏失效。
3. **交互死胡同 (Dead-end UI / No Copy-back)**：用户在页面上做了筛选、勾选或人工审核，但页面没有任何“复制结果”或“导出 Markdown”按钮，导致操作无法带回终端给 Agent。
4. **硬编码固定高度截断 (Fixed-height Truncation)**：设置 `height: 400px; overflow: hidden;`，在不同系统或字体大小下导致内容直接被切断。
5. **假装支持暗黑模式**：部分元素硬编码 `#ffffff` 或 `#000000`，在暗黑模式下文字或背景融为一体不可见。
6. **缺乏移动端/小屏响应式**：未加 `<meta name="viewport">` 或缺乏 `@media` 断点，分屏小窗口下横向滚动条爆炸。
7. **缺乏空状态处理 (Empty State)**：表格或列表在搜索无果时白茫茫一片，未提供“暂无匹配记录”提示。
8. **打印样式缺失 (@media print)**：报告类页面未做 `@media print` 样式优化，用户需要导出 PDF 时按钮乱飞。
9. **图表引入重型第三方库**：为了画简单折线图引入 Chart.js/ECharts（有断网白屏风险），必须坚持纯原生矢量 SVG。
10. **丢失关键元数据与数据精度**：过度美化排版却丢掉了关键错误码、时间戳、原始 ID 或 Trace，导致失去工程核验价值。

---

## 二、为什么这样设计？(Design Principles & The "Why")

1. **为什么坚决追求纯单文件与零外部依赖（Zero-Dependency Standalone）？**
   - 很多可视化报告、用例审查工具常在内网机房、无公网访问的隔离环境（Air-gapped）、或本地离线存档中打开。
   - 引入 Tailwind CDN (`cdn.tailwindcss.com`) 或第三方字体库，会在弱网下引发白屏（FOUC）、CDN 节点下线失效或公司 CSP 策略拦截。因此必须将精炼的 CSS 变量与极简微脚本直接内嵌。

2. **为什么严格采用 shadcn/ui 的 Zinc/Slate 中性色体系？**
   - 大模型在自由发挥时容易产生“AI审美漂移”——随机的大圆角、大面积刺眼渐变色、过大的无意义留白。
   - shadcn 的核心是：**冷灰中性底色、精准 1px 微细浅色边框、高信息密度、语义化状态点（Green/Amber/Red）**。这种排版能让任何数据报表看起来都像资深前端工程师耗费数日精心调校过的专业企业级产品。

3. **为什么必须原生内置暗黑模式（Light / Dark Theme）？**
   - 工程师与运维人员大量在暗黑 IDE/终端环境下工作。通过 CSS 变量原生映射，仅需 5 行原生 JS 即可实现丝滑切换，零构建成本却能极大提升使用体验。

---

## 二、六大通用布局母版与渐进式披露 (Progressive Disclosure)

不要从零手写完整页面。接到需求后，首先从以下 6 种**通用布局母版**中选择最贴近的骨架。支持中英文双语母版体系，根据用户输入语言对齐：
- **英文场景**：参考 `assets/templates/en/<name>.html`
- **中文场景**：参考 `assets/templates/zh/<name>.html`

| 布局模式 | 中文母版路径 | 英文母版路径 | 适用需求与核心结构 |
| :--- | :--- | :--- | :--- |
| **Report 报告**<br>(Document / Report) | `assets/templates/zh/report.html` | `assets/templates/en/report.html` | **技术选型、架构审查、故障复盘、面试报告、需求说明、发布日志**。<br>结构：自适应宽屏容器（默认 1200px ~ 1280px，支持宽屏自适应扩展至 96%，避免宽屏下表格被挤扁）、悬浮目录（Sticky TOC with ScrollSpy）、核心结论 Callout、KPI 概览栏、多章节 `<details>` 折叠手风琴、一键复制为 Markdown 导出。 |
| **Dashboard 数据面板**<br>(Dashboard & Data Grid) | `assets/templates/zh/dashboard.html` | `assets/templates/en/dashboard.html` | **资源监控、用量大盘、考勤/调休管理、订单/任务流管理**。<br>结构：宽屏网格，顶部操作栏、4 列自适应 KPI 统计卡、原生 SVG 走势图与柱状图、实时双重过滤表格、一键复制表格 (MD)。 |
| **Inspector 审查工作台**<br>(Master-Detail Workbench) | `assets/templates/zh/inspector.html` | `assets/templates/en/inspector.html` | **日志/Trace 审查、Prompt 调试器、JSONL 编辑器、配置管理**。<br>结构：视口充满（100vh），左侧条目列表过滤，右侧动态联动渲染选中条目详情、人工审查裁决条（Pass/Fix/Reject）、复制审查结论发回 Agent。 |
| **Compare 对比**<br>(Side-by-Side Comparison) | `assets/templates/zh/compare.html` | `assets/templates/en/compare.html` | **模型 A/B 测试、Prompt 改版前后对比、架构版本 diff、产品套餐/特性矩阵**。<br>结构：并排双栏卡片（基准 vs 挑战者）、核心裁决 Callout、量化差异对照表（Delta 胜负判定标签）、一键导出 Markdown。 |
| **Timeline 时间线**<br>(Timeline & Postmortem) | `assets/templates/zh/timeline.html` | `assets/templates/en/timeline.html` | **发布路线图 (Roadmap)、变更历史 (Changelog)、突发事件复盘 (Postmortem)**。<br>结构：左侧单轨垂直时间线、状态节点小圆点、精确时间戳与操作人 Tag、可展开诊断日志、一键复制时间轴为 Markdown。 |
| **Kanban 看板**<br>(Triage & Agile Kanban) | `assets/templates/zh/kanban.html` | `assets/templates/en/kanban.html` | **缺陷分类整理、需求优先级排序、任务状态流转**。<br>结构：4 列敏捷看板（Backlog, In Progress, Blocked, Done）、纯原生 HTML5 拖拽排序（零依赖）、一键复制分拣结果回 Agent 闭环。 |

> 💡 **组件字典查阅**：如需查看所有按钮变体、胶囊徽章、常用 24 个矢量图标、原生纯 SVG 图表与实时组件效果，可直接读取 `references/components.md` 或在浏览器中打开 `assets/index.html`。

---

## 三、微 CSS 核心基座 (Micro-CSS Base)

在生成 HTML 时，务必将以下约 75 行 CSS 基座放入 `<head><style>` 中，它是所有组件质感一致的基石：

```css
:root {
  --bg: #fafafa;
  --card: #ffffff;
  --card-fg: #09090b;
  --primary: #18181b;
  --primary-fg: #fafafa;
  --primary-hover: #27272a;
  --secondary: #f4f4f5;
  --secondary-fg: #18181b;
  --muted: #f4f4f5;
  --muted-fg: #71717a;
  --border: #e4e4e7;
  --ring: #18181b;
  --radius: 8px;
  --radius-sm: 6px;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);

  --ok: #16a34a;   --ok-bg: #f0fdf4;   --ok-border: #bbf7d0;
  --warn: #d97706; --warn-bg: #fffbeb; --warn-border: #fde68a;
  --err: #dc2626;  --err-bg: #fef2f2;  --err-border: #fecaca;
  --info: #2563eb; --info-bg: #eff6ff; --info-border: #bfdbfe;
}

[data-theme="dark"] {
  --bg: #09090b;
  --card: #121215;
  --card-fg: #fafafa;
  --primary: #fafafa;
  --primary-fg: #18181b;
  --primary-hover: #e4e4e7;
  --secondary: #27272a;
  --secondary-fg: #fafafa;
  --muted: #18181b;
  --muted-fg: #a1a1aa;
  --border: #27272a;
  --ring: #d4d4d8;

  --ok: #4ade80;   --ok-bg: #052e1680;   --ok-border: #166534;
  --warn: #fbbf24; --warn-bg: #451a0380; --warn-border: #854d0e;
  --err: #f87171;  --err-bg: #450a0a80;  --err-border: #991b1b;
  --info: #60a5fa; --info-bg: #17255480; --info-border: #1e40af;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: var(--bg);
  color: var(--card-fg);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 500;
  height: 34px;
  padding: 0 12px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  background: var(--card);
  color: var(--card-fg);
  cursor: pointer;
  text-decoration: none;
  transition: all 0.15s ease;
}
.btn:hover { background: var(--secondary); }
.btn-primary { background: var(--primary); color: var(--primary-fg); border-color: var(--primary); }
.btn-primary:hover { background: var(--primary-hover); opacity: 0.95; }
.btn-destructive { background: var(--err); color: #fff; border-color: var(--err); }
.btn-sm { height: 28px; padding: 0 8px; font-size: 12px; }

.badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 500;
  height: 20px;
  padding: 0 7px;
  border-radius: 9999px;
  border: 1px solid var(--border);
  background: var(--secondary);
  color: var(--secondary-fg);
}
.badge-dot { width: 5px; height: 5px; border-radius: 9999px; background: currentColor; }
.badge-success { background: var(--ok-bg); color: var(--ok); border-color: var(--ok-border); }
.badge-warning { background: var(--warn-bg); color: var(--warn); border-color: var(--warn-border); }
.badge-danger  { background: var(--err-bg);  color: var(--err);  border-color: var(--err-border); }
.badge-info    { background: var(--info-bg); color: var(--info); border-color: var(--info-border); }
```

---

## 四、高频原子 HTML 插槽字典 (Atomic HTML Snippets)

> 💡 **原子积木按需索取 (Progressive Disclosure)**：本节列举最核心的高频插槽。如需查阅完整 24 个研发矢量图标、复合多色段环形图、水平耗时排行榜等详细代码片段，可使用 `read` 工具查阅本 Skill 目录下的 `references/components.md`。

### 1. 指标卡片 (Stat Card)
```html
<div class="stat-card" style="padding: 18px 20px; background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);">
  <div style="display: flex; justify-content: space-between; font-size: 13px; color: var(--muted-fg);">
    <span>可用剩余额度</span>
    <span style="color: var(--ok); font-weight: 600;">↑ 正常</span>
  </div>
  <div style="font-size: 26px; font-weight: 700; margin: 6px 0 2px;">3.5 天</div>
  <div style="font-size: 12px; color: var(--muted-fg);">本月总产生：7.5 天</div>
</div>
```

### 2. 执行摘要提示条 (Callout / Alert)
```html
<div style="padding: 14px 16px; border-radius: var(--radius); border: 1px solid var(--ok-border); background: var(--ok-bg); font-size: 13px; line-height: 1.5; margin-bottom: 16px;">
  <strong style="color: var(--ok); display: flex; align-items: center; gap: 6px; margin-bottom: 4px;">
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
    <span>核心评估结论</span>
  </strong>
  <span>系统整体稳定性与架构设计符合上线标准，建议推进下一阶段发布。</span>
</div>
```

### 3. 可折叠审查项手风琴 (Accordion)
```html
<details style="border-bottom: 1px solid var(--border);">
  <summary style="list-style: none; padding: 12px 0; font-size: 14px; font-weight: 600; cursor: pointer; display: flex; justify-content: space-between; user-select: none;">
    <span>1. 分布式容灾与降级验证</span>
    <span style="color: var(--muted-fg);">▾</span>
  </summary>
  <div style="padding-bottom: 14px; font-size: 13px; color: var(--muted-fg); line-height: 1.6;">
    已验证跨可用区自动切流，模拟机房断网后 2.4s 内完成健康检测与流量重新路由。
  </div>
</details>
```

### 4. 数据表格与搜索框 (Table with Search)
```html
<div class="card">
  <div style="padding: 12px 16px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center;">
    <input type="text" id="searchInput" placeholder="实时搜索过滤..." style="height: 32px; padding: 0 10px; border-radius: var(--radius-sm); border: 1px solid var(--border); background: var(--bg); color: var(--card-fg); outline: none;">
  </div>
  <table id="dataTable" style="width: 100%; border-collapse: collapse; font-size: 13px; text-align: left;">
    <thead>
      <tr style="background: var(--secondary); color: var(--muted-fg); border-bottom: 1px solid var(--border);">
        <th style="padding: 10px 16px;">项目编号</th>
        <th style="padding: 10px 16px;">负责人</th>
        <th style="padding: 10px 16px;">状态</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom: 1px solid var(--border);">
        <td style="padding: 10px 16px;">TASK-001</td>
        <td style="padding: 10px 16px;">陈云青</td>
        <td style="padding: 10px 16px;"><span class="badge badge-success"><span class="badge-dot"></span>已完成</span></td>
      </tr>
    </tbody>
  </table>
</div>
```

### 5. 常用纯矢量 SVG 图标字典 (24 个精选工程图标)
所有图标均基于 `viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"`，通过继承字色自动融入暗黑模式：
- 搜索: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>`
- 成功: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>`
- 警告: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`
- 复制: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>`
- 日历: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>`
- 终端: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="4 17 10 11 4 5"/><line x1="12" x2="20" y1="19" y2="19"/></svg>`
- 过滤: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>`
- 外链: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>`
- 用户: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`
- 折叠: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m6 9 6 6 6-6"/></svg>`
- 删除: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>`
- 下载: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>`
- Git分支: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="6" y1="3" x2="6" y2="15"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/></svg>`
- Git提交: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><line x1="1.05" y1="12" x2="7" y2="12"/><line x1="17.01" y1="12" x2="22.96" y2="12"/></svg>`
- Git PR: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M13 6h3a2 2 0 0 1 2 2v7"/><line x1="6" y1="9" x2="6" y2="21"/></svg>`
- 缺陷/Bug: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="8" height="14" x="8" y="6" rx="4"/><path d="m19 7-3 2"/><path d="m5 7 3 2"/><path d="m19 19-3-2"/><path d="m5 19 3-2"/><path d="M20 13h-4"/><path d="M4 13h4"/><path d="m10 4 1 2"/><path d="m14 4-1 2"/></svg>`
- 服务器: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="20" height="8" x="2" y="2" rx="2" ry="2"/><rect width="20" height="8" x="2" y="14" rx="2" ry="2"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/></svg>`
- 数据库: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>`
- CPU算力: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M9 1v3"/><path d="M15 1v3"/><path d="M9 20v3"/><path d="M15 20v3"/><path d="M20 9h3"/><path d="M20 15h3"/><path d="M1 9h3"/><path d="M1 15h3"/></svg>`
- 心跳/探活: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>`
- 安全防护: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>`
- 鉴权锁定: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>`
- 刷新/重试: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/><path d="M16 21h5v-5"/></svg>`
- 系统设置: `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>`

### 6. 轻量原生图表规范 (Zero-CDN Pure SVG Charts)
在生成数据大盘与报表时，**严禁引入 Chart.js / ECharts / Recharts 等外部 CDN 库**。图表统一采用纯原生矢量 SVG 实现：
- **零网络依赖**：脱机、内网机房 100% 秒开，绝无 CDN 挂掉或白屏风险；
- **暗黑模式自适应**：直接使用 `var(--primary)`、`var(--border)`、`var(--muted-fg)` 等主题变量，无须额外 JS 监听重绘；
- **自适应视口**：设定统一 `viewBox="0 0 500 150"` 与 `style="width: 100%; height: auto;"`，Retina 屏幕与打印完美保真。

#### A. 面积折线趋势图 (Area Trend Line Chart)
```html
<div class="card" style="padding: 16px 20px;">
  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
    <div>
      <div style="font-size: 14px; font-weight: 600;">24小时吞吐量趋势 (TPS)</div>
      <div style="font-size: 12px; color: var(--muted-fg);">平均 TPS: 1,420 · 峰值: 2,890</div>
    </div>
    <span class="badge badge-success"><span class="badge-dot"></span>+14.8% 环比</span>
  </div>
  <svg viewBox="0 0 500 150" style="width: 100%; height: auto; overflow: visible;">
    <defs>
      <linearGradient id="trendAreaGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="var(--primary)" stop-opacity="0.25"/>
        <stop offset="100%" stop-color="var(--primary)" stop-opacity="0.00"/>
      </linearGradient>
    </defs>
    <!-- 网格参考虚线 -->
    <line x1="30" y1="20" x2="490" y2="20" stroke="var(--border)" stroke-dasharray="3 3" />
    <line x1="30" y1="60" x2="490" y2="60" stroke="var(--border)" stroke-dasharray="3 3" />
    <line x1="30" y1="100" x2="490" y2="100" stroke="var(--border)" stroke-dasharray="3 3" />
    <line x1="30" y1="130" x2="490" y2="130" stroke="var(--border)" />
    <!-- Y 轴刻度 -->
    <text x="22" y="24" font-size="10" fill="var(--muted-fg)" text-anchor="end">3k</text>
    <text x="22" y="64" font-size="10" fill="var(--muted-fg)" text-anchor="end">2k</text>
    <text x="22" y="104" font-size="10" fill="var(--muted-fg)" text-anchor="end">1k</text>
    <text x="22" y="133" font-size="10" fill="var(--muted-fg)" text-anchor="end">0</text>
    <!-- 渐变阴影面积与折线 -->
    <path d="M 40 110 Q 90 95, 130 85 T 220 50 T 310 75 T 400 35 T 480 45 L 480 130 L 40 130 Z" fill="url(#trendAreaGrad)" />
    <path d="M 40 110 Q 90 95, 130 85 T 220 50 T 310 75 T 400 35 T 480 45" fill="none" stroke="var(--primary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />
    <!-- 关键数据点与峰值气泡 -->
    <circle cx="220" cy="50" r="3.5" fill="var(--card)" stroke="var(--primary)" stroke-width="2"/>
    <circle cx="400" cy="35" r="4.5" fill="var(--ok)" stroke="var(--card)" stroke-width="2"/>
    <g transform="translate(400, 18)">
      <rect x="-24" y="-12" width="48" height="18" rx="4" fill="var(--primary)" />
      <text x="0" y="1" font-size="10" font-weight="600" fill="var(--primary-fg)" text-anchor="middle">2,890</text>
    </g>
    <!-- X 轴刻度 -->
    <text x="40" y="145" font-size="10" fill="var(--muted-fg)" text-anchor="middle">00:00</text>
    <text x="130" y="145" font-size="10" fill="var(--muted-fg)" text-anchor="middle">04:00</text>
    <text x="220" y="145" font-size="10" fill="var(--muted-fg)" text-anchor="middle">08:00</text>
    <text x="310" y="145" font-size="10" fill="var(--muted-fg)" text-anchor="middle">12:00</text>
    <text x="400" y="145" font-size="10" fill="var(--muted-fg)" text-anchor="middle">16:00</text>
    <text x="480" y="145" font-size="10" fill="var(--muted-fg)" text-anchor="middle">20:00</text>
  </svg>
</div>
```

#### B. 柱状对比分布图 (Column Bar Chart)
```html
<div class="card" style="padding: 16px 20px;">
  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
    <div>
      <div style="font-size: 14px; font-weight: 600;">各模块响应延迟分布 (ms)</div>
      <div style="font-size: 12px; color: var(--muted-fg);">P95 阶段统计基准</div>
    </div>
    <span class="badge"><span class="badge-dot"></span>6 个服务模块</span>
  </div>
  <svg viewBox="0 0 500 150" style="width: 100%; height: auto; overflow: visible;">
    <!-- 网格参考虚线 -->
    <line x1="30" y1="20" x2="490" y2="20" stroke="var(--border)" stroke-dasharray="3 3" />
    <line x1="30" y1="60" x2="490" y2="60" stroke="var(--border)" stroke-dasharray="3 3" />
    <line x1="30" y1="100" x2="490" y2="100" stroke="var(--border)" stroke-dasharray="3 3" />
    <line x1="30" y1="130" x2="490" y2="130" stroke="var(--border)" />
    <!-- Y 轴刻度 -->
    <text x="22" y="24" font-size="10" fill="var(--muted-fg)" text-anchor="end">120</text>
    <text x="22" y="64" font-size="10" fill="var(--muted-fg)" text-anchor="end">80</text>
    <text x="22" y="104" font-size="10" fill="var(--muted-fg)" text-anchor="end">40</text>
    <text x="22" y="133" font-size="10" fill="var(--muted-fg)" text-anchor="end">0</text>
    <!-- 柱状单元: x, y, width, height, rx -->
    <rect x="52" y="106" width="36" height="24" rx="4" fill="var(--primary)" opacity="0.85" />
    <text x="70" y="100" font-size="10" font-weight="600" fill="var(--card-fg)" text-anchor="middle">24</text>
    <text x="70" y="145" font-size="10" fill="var(--muted-fg)" text-anchor="middle">网关</text>

    <rect x="124" y="82" width="36" height="48" rx="4" fill="var(--primary)" opacity="0.85" />
    <text x="142" y="76" font-size="10" font-weight="600" fill="var(--card-fg)" text-anchor="middle">48</text>
    <text x="142" y="145" font-size="10" fill="var(--muted-fg)" text-anchor="middle">鉴权</text>

    <rect x="196" y="38" width="36" height="92" rx="4" fill="var(--warn)" opacity="0.9" />
    <text x="214" y="32" font-size="10" font-weight="600" fill="var(--warn)" text-anchor="middle">92</text>
    <text x="214" y="145" font-size="10" fill="var(--muted-fg)" text-anchor="middle">订单</text>

    <rect x="268" y="95" width="36" height="35" rx="4" fill="var(--primary)" opacity="0.85" />
    <text x="286" y="89" font-size="10" font-weight="600" fill="var(--card-fg)" text-anchor="middle">35</text>
    <text x="286" y="145" font-size="10" fill="var(--muted-fg)" text-anchor="middle">支付</text>

    <rect x="340" y="112" width="36" height="18" rx="4" fill="var(--primary)" opacity="0.85" />
    <text x="358" y="106" font-size="10" font-weight="600" fill="var(--card-fg)" text-anchor="middle">18</text>
    <text x="358" y="145" font-size="10" fill="var(--muted-fg)" text-anchor="middle">存储</text>

    <rect x="412" y="66" width="36" height="64" rx="4" fill="var(--primary)" opacity="0.85" />
    <text x="430" y="60" font-size="10" font-weight="600" fill="var(--card-fg)" text-anchor="middle">64</text>
    <text x="430" y="145" font-size="10" fill="var(--muted-fg)" text-anchor="middle">检索</text>
  </svg>
</div>
```

#### C. KPI 卡片内嵌迷你走势线 (Sparkline)
```html
<div class="stat-card" style="padding: 16px 20px; background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);">
  <div style="display: flex; justify-content: space-between; font-size: 13px; color: var(--muted-fg);">
    <span>每日活跃会话 (DAU)</span>
    <span style="color: var(--ok); font-weight: 600;">↑ +18.2%</span>
  </div>
  <div style="display: flex; align-items: flex-end; justify-content: space-between; margin-top: 6px;">
    <div>
      <div style="font-size: 24px; font-weight: 700; line-height: 1.1;">48,290</div>
      <div style="font-size: 12px; color: var(--muted-fg); margin-top: 4px;">近 7 日持续攀升</div>
    </div>
    <svg width="84" height="28" viewBox="0 0 84 28" fill="none" style="overflow: visible;">
      <path d="M 2 24 L 16 20 L 30 22 L 44 14 L 58 16 L 70 6 L 82 2" stroke="var(--ok)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="82" cy="2" r="2.5" fill="var(--ok)"/>
    </svg>
  </div>
</div>
```

#### D. 复合环形占比分布图 (Multi-Segment Donut Chart)
利用纯 SVG `<circle stroke-dasharray stroke-dashoffset>` 构造多色拼接圆环，中央标注总量，右侧排列图例：
```html
<div class="card" style="padding: 16px 20px;">
  <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 8px;">
    <span style="font-weight: 600;">节点运行健康度分布</span>
    <span class="badge badge-success">99.8% 达标</span>
  </div>
  <div style="display: flex; align-items: center; justify-content: space-between; gap: 16px;">
    <svg viewBox="0 0 160 160" style="width: 90px; height: 90px; flex-shrink: 0;">
      <!-- 底环 (周长 2*PI*54 ≈ 339.3) -->
      <circle cx="80" cy="80" r="54" fill="none" stroke="var(--secondary)" stroke-width="20"/>
      <!-- 绿段 65% (220.5), 偏移 0 -->
      <circle cx="80" cy="80" r="54" fill="none" stroke="var(--ok)" stroke-width="20" stroke-dasharray="220.5 339.3" stroke-dashoffset="0" transform="rotate(-90 80 80)"/>
      <!-- 黄段 25% (84.8), 偏移 -220.5 -->
      <circle cx="80" cy="80" r="54" fill="none" stroke="var(--warn)" stroke-width="20" stroke-dasharray="84.8 339.3" stroke-dashoffset="-220.5" transform="rotate(-90 80 80)"/>
      <!-- 红段 10% (33.9), 偏移 -305.3 -->
      <circle cx="80" cy="80" r="54" fill="none" stroke="var(--err)" stroke-width="20" stroke-dasharray="33.9 339.3" stroke-dashoffset="-305.3" transform="rotate(-90 80 80)"/>
      <text x="80" y="77" text-anchor="middle" font-size="16" font-weight="700" fill="var(--card-fg)">1,280</text>
      <text x="80" y="93" text-anchor="middle" font-size="10" fill="var(--muted-fg)">Nodes</text>
    </svg>
    <div style="font-size: 12px; display: flex; flex-direction: column; gap: 6px; flex: 1;">
      <div style="display: flex; justify-content: space-between;"><span style="color: var(--ok);">● 65% 正常运行</span><strong>832</strong></div>
      <div style="display: flex; justify-content: space-between;"><span style="color: var(--warn);">● 25% 负载预警</span><strong>320</strong></div>
      <div style="display: flex; justify-content: space-between;"><span style="color: var(--err);">● 10% 异常降级</span><strong>128</strong></div>
    </div>
  </div>
</div>
```

#### E. 水平对比排行榜 (Horizontal Ranking Bar)
特别适合微服务或长命名实体的耗时排行与资源占用比对：
```html
<div class="card" style="padding: 16px 20px;">
  <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 12px;">
    <span style="font-weight: 600;">核心模块响应耗时 Top 3 (ms)</span>
    <span style="font-size: 11px; color: var(--muted-fg);">P95 阶段</span>
  </div>
  <div style="display: flex; flex-direction: column; gap: 8px; font-size: 12px;">
    <div>
      <div style="display: flex; justify-content: space-between; margin-bottom: 3px;"><span>1. 数据库连接池等待 (DB Pool)</span><strong>280ms</strong></div>
      <div style="background: var(--secondary); height: 6px; border-radius: 9999px; overflow: hidden;"><div style="background: var(--err); width: 85%; height: 100%;"></div></div>
    </div>
    <div>
      <div style="display: flex; justify-content: space-between; margin-bottom: 3px;"><span>2. 模型首字生成 (LLM First Token)</span><strong>195ms</strong></div>
      <div style="background: var(--secondary); height: 6px; border-radius: 9999px; overflow: hidden;"><div style="background: var(--warn); width: 60%; height: 100%;"></div></div>
    </div>
    <div>
      <div style="display: flex; justify-content: space-between; margin-bottom: 3px;"><span>3. 网关鉴权解析 (Auth Gateway)</span><strong>48ms</strong></div>
      <div style="background: var(--secondary); height: 6px; border-radius: 9999px; overflow: hidden;"><div style="background: var(--primary); width: 22%; height: 100%;"></div></div>
    </div>
  </div>
</div>
```

---

## 六、经典微交互原生脚本 (Micro Vanilla JS)

### 1. 暗黑模式切换按钮（建议所有页面右上角均标配）
```javascript
const toggle = document.getElementById('themeToggle');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
if (prefersDark) document.documentElement.setAttribute('data-theme', 'dark');

toggle?.addEventListener('click', () => {
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  document.documentElement.setAttribute('data-theme', isDark ? 'light' : 'dark');
});
```

### 2. 表格前端毫秒级实时搜索过滤
```javascript
document.getElementById('searchInput')?.addEventListener('input', (e) => {
  const q = e.target.value.toLowerCase().trim();
  document.querySelectorAll('#dataTable tbody tr').forEach(tr => {
    tr.style.display = (!q || tr.textContent.toLowerCase().includes(q)) ? '' : 'none';
  });
});
```

### 3. 一键导出回 Markdown 文本 (Copy as Markdown)
页面顶部或侧边标配导出按钮，允许用户将当前 HTML 结论零损耗带走（发飞书、贴 GitHub Issue/PR 或发群）：
```javascript
document.getElementById('copyMarkdownBtn')?.addEventListener('click', () => {
  const md = `# ${document.querySelector('h1').innerText}\n\n` +
    `> 状态：${document.querySelector('.badge')?.innerText || '已归档'}\n\n` +
    `## 核心结论\n${document.querySelector('.callout')?.innerText || ''}\n`;
  navigator.clipboard.writeText(md).then(() => {
    const btn = document.getElementById('copyMarkdownBtn');
    const orig = btn.innerText;
    btn.innerText = '已复制 Markdown!';
    setTimeout(() => { btn.innerText = orig; }, 1800);
  });
});
```

### 4. 人工审查决策汇总回传 Agent (Review Verdict Copy-Back)
工作台或审查器母版中，记录用户在页面的单项决策并生成结构化文本，方便用户一键复制粘回终端让 Agent 接着执行：
```javascript
document.getElementById('exportDecisionBtn')?.addEventListener('click', () => {
  let lines = ['### 人工审查结论回传 (Review Decisions)'];
  document.querySelectorAll('.item-row').forEach(row => {
    const id = row.getAttribute('data-id');
    const verdict = row.getAttribute('data-verdict') || 'PASS';
    lines.push(`- [${verdict}] ${id}: ${row.getAttribute('data-name')}`);
  });
  lines.push('\n请根据上述人工裁决结果继续处理下一步任务。');
  navigator.clipboard.writeText(lines.join('\n')).then(() => {
    alert('审查结论已复制到剪贴板，可直接在终端中 Cmd+V 发给 Agent 继续执行！');
  });
});
```

### 5. 长文档悬浮目录与阅读进度监听 (Sticky TOC ScrollSpy)
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const id = entry.target.getAttribute('id');
      document.querySelectorAll('.toc-link').forEach(link => {
        link.classList.toggle('active', link.getAttribute('href') === '#' + id);
      });
    }
  });
}, { rootMargin: '-20% 0px -70% 0px' });

document.querySelectorAll('section[id]').forEach(el => observer.observe(el));
```

### 6. 页脚 Colophon 溯源元数据印章
在每个交付的单文件 HTML 底部必须附带正式的归档印记：
```html
<footer style="margin-top: 40px; padding-top: 16px; border-top: 1px solid var(--border); font-size: 12px; color: var(--muted-fg); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
  <div>Generated by <strong>Agent HTML</strong> · 零依赖单文件规范 · 100% 离线自包含</div>
  <div>时间戳：2026-09-08 · 基准：main@HEAD · 状态：已正式归档</div>
</footer>
```

### 7. 原生 HTML5 看板跨列拖拽逻辑 (Kanban Drag & Drop)
零外部库，仅 ~30 行原生事件监听即可实现卡片跨列拖拽：
```javascript
let dragged = null;
document.querySelectorAll('.card-item').forEach(card => {
  card.addEventListener('dragstart', () => { dragged = card; card.classList.add('dragging'); });
  card.addEventListener('dragend', () => { card.classList.remove('dragging'); dragged = null; });
});
document.querySelectorAll('.kanban-col').forEach(col => {
  col.addEventListener('dragover', (e) => { e.preventDefault(); col.classList.add('drag-over'); });
  col.addEventListener('dragleave', () => col.classList.remove('drag-over'));
  col.addEventListener('drop', (e) => {
    e.preventDefault();
    col.classList.remove('drag-over');
    if (dragged) col.querySelector('.cards-container').appendChild(dragged);
  });
});
```

---

## 七、交付自验与质量门禁 (Self-Verification Gate)

AI Agent 在完成任何单文件 HTML 输出后，**推荐在终端中执行本地静态自检脚本**进行无消耗的语法与规范验收：

```bash
node scripts/validate.mjs <generated_file.html>
```

该脚本将零网络、零 Token 地确定性校验以下 7 项标准：
1. `[ZERO_CDN]` 是否含有外部外网 script / link CDN 引用；
2. `[THEME_TOKENS]` 是否具备 `--bg/--card/--primary` 变量底座与暗黑模式支持；
3. `[VIEWPORT]` 是否具备移动端小屏响应式 viewport；
4. `[TAG_HYGIENE]` svg/dialog/details 等关键标签是否正确对称闭合；
5. `[AFFORDANCE]` 是否具备复制/导出出口（杜绝交互死胡同）；
6. `[COLOPHON]` 是否包含溯源归档印章；
7. `[WIDTH_HYGIENE]` 容器自适应性：严禁将主容器硬编码为过窄的死宽度（如 800px-860px），导致宽屏左右大量留白、数据表格被严重挤压。包含多列表格或对比矩阵的场景，`.container` 基础宽度推荐 `max-width: 1280px`（或 `width: 100%; max-width: 1380px`），表格外层应包裹 `<div class="table-wrap" style="overflow-x: auto; width: 100%;">`。
```
