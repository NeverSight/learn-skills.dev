---
name: market-research-html
description: "使用 HTML/CSS 格式生成综合性市场研究报告（50+页），风格模仿顶级咨询公司。具有专业排版、丰富的视觉生成、深度数据集成，支持多框架战略分析。HTML 格式使 AI 编辑和局部更新更加简便。"
allowed-tools: [Read, Write, Edit, Bash]
---

# 市场研究报告 (HTML 版)

## 概览

本技能旨在生成**50+页的专业级市场研究报告**，输出格式为 **HTML/CSS**。这种格式不仅保持了麦肯锡、BCG 等咨询公司的专业视觉严谨性，还极大地简化了 AI 对长文档的编辑、局部更新和内容追加过程。

**核心特性：**
- **AI 友好型格式**：HTML 结构清晰，支持通过 ID 定向更新章节，避免 LaTeX 常见的编译错误。
- **专业咨询风格**：通过内置 CSS 实现顶级排版、配色和交互式目录。
- **综合分析**：涵盖 TAM/SAM/SOM、波特五力、PESTLE、SWOT、BCG 矩阵等核心框架。
- **一键 PDF 转换**：利用浏览器的“打印”功能，配合打印优化 CSS，即可获得完美的纸质版报告。

**输出格式**：HTML5 + CSS3（包含打印样式），可选 JS 实现交互增强。

---

## 视觉增强要求

每份报告应在**开始时生成 6 个基本视觉内容**，使用 `scientific-schematics` 和 `generate-image` 工具。

### 视觉内容嵌入方法
在 HTML 中，使用 `<img>` 标签嵌入生成的图片：
```html
<div class="figure">
    <img src="figures/01_market_growth.png" alt="市场增长轨迹">
    <div class="caption"><b>图 2.1：</b> 市场增长轨迹预测 (2024-2034)</div>
</div>
```

---

## 工作流 (HTML 优先)

### 第一阶段：初始化与环境搭建
1. 创建项目文件夹。
2. 拷贝 `assets/style.css` 和 `assets/template.html`。
3. 创建 `figures/` 文件夹用于存放视觉资产。

### 第二阶段：研究与数据收集
使用 `research-lookup` 收集关键数据：
- 市场规模、CAGR、各细分市场占比。
- 前 10 名竞争对手及其份额。
- 监管政策、技术趋势。

### 第三阶段：视觉批量生成
使用 Python 脚本生成所有必需的图表：
```bash
python scripts/generate_market_visuals.py --topic "[市场名称]" --output-dir figures/
```

### 第四阶段：报告编写（AI 编辑逻辑）
1. **初始化骨架**：基于 `template.html` 创建初稿。
2. **分块填充**：AI 逐章填充内容。由于 HTML 标签闭合简单，AI 可以轻松处理 50+ 页的长文本。
3. **局部优化**：利用 `id`（如 `#chapter-4`）精确定位需要加深分析的部分。

### 第五阶段：预览与导出
1. 在浏览器中打开 HTML 文件进行即时预览。
2. 检查 CSS 样式是否正确加载。
3. 使用浏览器的“打印 -> 另存为 PDF”功能，确保勾选“打印背景图形”。

---

## 专业组件参考

在编写过程中，使用以下 HTML 类来实现咨询级组件：

| 组件名称 | HTML 代码示例 | 用途 |
|----------|---------------|------|
| **洞察框** | `<div class="insight-box box">...</div>` | 强调关键发现和深度洞察 |
| **数据框** | `<div class="data-box box">...</div>` | 展示核心统计数据和指标 |
| **风险框** | `<div class="risk-box box">...</div>` | 罗列潜在威胁和挑战 |
| **建议框** | `<div class="recommendation-box box">...</div>` | 提供可操作的战略建议 |
| **图表容器** | `<div class="figure">...</div>` | 包装图片并添加专业标题 |

---

## 50+页验证清单

- [ ] 包含标准封面及 hero 可视化。
- [ ] 交互式目录（侧边栏或置顶）。
- [ ] 执行摘要（含 Snapshot 框和投资论点）。
- [ ] 11 个核心分析章节完整（每章均有对应的 `section` 标签）。
- [ ] 至少包含 6 个核心图表（TAM/SAM/SOM, 五力, 风险矩阵等）。
- [ ] 所有数据点均在 HTML 中标记来源。
- [ ] 附录包含研究方法论和详细数据表。
- [ ] 打印预览中，各章节自动从新页面开始（CSS 分页控制）。

---

## 资源

- **`assets/style.css`**：定义所有视觉规范。
- **`assets/template.html`**：起始模板。
- **`references/`**：包含所有分析框架的详细文本指南。
- **`scripts/`**：包含 Python 自动化绘图工具。
