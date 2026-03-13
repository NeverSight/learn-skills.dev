---
name: insight-pdf
description: Generates professional corporate/business report PDFs from text or Markdown via HTML. Uses ECharts for advanced visualizations (heatmaps, radar, gauge, sankey), rich design system (gradient covers, stat cards, callout boxes, progress bars, timelines), and professional typography. Use when the user wants enterprise-quality report PDFs with modern data storytelling.
---

# Insight PDF

企业级报告 PDF 生成 skill。用户项目目录**仅生成最终 PDF**，无 HTML、node_modules 等中间产物。

## 完整工作流

1. **设计系统** — 应用 reference 中的配色、字体、网格、封面规范及可视化组件
2. **生成 HTML（内存）** — 使用 `templates/insight-report.html`，替换占位符；正文从 Markdown 转 HTML，使用 ECharts 图表、stat cards、callout boxes、progress bars、timelines 等组件
3. **写入临时目录** — 将 HTML 写入系统临时目录（如 `/tmp/insight-pdf-<uuid>/report.html`）
4. **调用 convert 脚本** — `node <skill-dir>/scripts/convert.js <temp-html-path> <project-dir>/report.pdf`
5. **清理** — 转换成功后删除临时目录

**用户项目最终只得到 PDF 文件，无其他生成物。**

## 可视化能力

| 类型 | 支持 |
|------|------|
| 图表库 | ECharts + Chart.js |
| 基础图表 | 柱状图、折线图、饼图、散点图 |
| 高级图表 | 热力图、雷达图、仪表盘、桑基图 |
| 信息图 | 进度条、对比块、时间线、徽章 |
| 数据组件 | Stat Cards、Callout Boxes、Enhanced Tables |

## 新增视觉组件

| 组件 | 用途 |
|------|------|
| ECharts Charts | 高级可视化（热力图、雷达图、仪表盘、桑基图） |
| Progress Bars | 进度可视化，支持渐变填充 |
| Comparison Blocks | 并排对比展示关键指标 |
| Timeline | 时间线可视化，展示事件流程 |
| Badges | 标签徽章，状态标识 |
| Stat Cards | 展示关键指标，支持图标、数值、标签 |
| Callout Boxes | 高亮重要信息（info/warning/success） |
| Enhanced Tables | 斑马纹表格，专业样式 |
| Gradient Cover | 渐变背景封面，装饰性强调条 |

## 设计规范引用

| 维度 | 规范 |
|------|------|
| 配色 | 主色深蓝 `#1e3a5f`，8色图表调色板，强调色 `#0ea5e9` |
| 字体 | 标题 serif（Libre Baskerville/Georgia），正文 sans-serif（Source Sans 3/Inter） |
| 封面 | 渐变背景、装饰性强调条、专业排版 |
| 图表 | ECharts 扁平配置、无动画、设计系统配色 |
| 布局 | 模块化网格、信息图组件、清晰层级 |

## 首次安装（在 skill 目录，非项目目录）

```bash
cd skills/insight-pdf   # 或 ~/.cursor/skills/insight-pdf
npm install
npx playwright install chromium
```

## Agent 执行示例

1. 生成完整 HTML 内容（参考 templates/insight-report.html 与 reference）
2. 写入临时目录：
   ```bash
   TEMP_DIR=$(mktemp -d)/insight-pdf-$$; mkdir -p "$TEMP_DIR"
   # 将 HTML 写入 $TEMP_DIR/report.html
   ```
3. 调用转换（skill 目录路径需为绝对路径）：
   ```bash
   node /path/to/skills/insight-pdf/scripts/convert.js "$TEMP_DIR/report.html" "$(pwd)/report.pdf"
   ```
4. 删除临时目录：`rm -rf "$TEMP_DIR"`

## 依赖缺失时

若转换失败且错误提示 Chromium 未安装，引导用户到 **skill 目录**（非项目目录）执行：

```bash
cd skills/insight-pdf && npm install && npx playwright install chromium
```
