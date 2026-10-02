---
name: academic-figure-analyzer
description: 把仓库、论文/草稿、参考图分析成可交接结果（SemanticArchitecture@1、FigurePlan@1、ReferenceAnalysis@1），不写 prompt，也不生图。
metadata:
  version: "1.0.0"
---

# Academic Figure Analyzer

把仓库、论文或草稿、参考图分析成可交接结果。本 skill 不写 prompt，也不生图。

先检查输入内容，再选择路径。不要把所有 URL 当成仓库：打开页面或正文后，再判断它是论文、代码仓库，还是图。

检查时看这三件事：

- 正文、章节或 LaTeX/Markdown 结构 → 论文或草稿
- 源码、README、依赖与入口脚本 → 仓库
- 图本身、图注，或 PDF 里的嵌入图 → 参考图

## 路由

### 草稿、大纲或完整手稿

Markdown、LaTeX、PDF 正文，或论文 URL 打开后的正文，读 `references/paper.md`，产出 Figure Plan v1。

- 笔记、大纲、早期草稿：只规划 Figure 1（Overall Framework），不要强行补实验图。
- 含实验结果的完整手稿：按论文主张规划多图。
- 当前环境读不了 PDF 或网页时，报告限制，不要编造章节结构。

### 仓库

本地仓库路径，或打开后确认为代码仓库的 URL，读 `references/repo.md`，产出 Semantic Architecture Handoff v1。任务或框架分类不确定时，再读 `references/keywords.md`。

### 论文加仓库

论文与用户意图决定叙事和拓扑。仓库只核验参数、张量维度、模块名与执行方向，不另起一套架构。

### 参考图

外部风格参考图、PDF 中的图，或图片，读 `references/reference-figure.md`，产出 ReferenceAnalysis v1。

- PDF 正文与图注用 PDF reader。
- 只有需要抽出图片候选时，才运行 `scripts/extract_pdf_figures.py`。
- 该脚本只按尺寸筛候选，不是结构分类器；保留、丢弃或不确定仍由证据判断。

证据不足时读 `references/missing-info-policy.md`。标出缺失项，不要补造模块、边或数值。

## 交接

字段与 JSON 形状以对应 reference 里的定义为准，此处不重写 schema：

- Semantic Architecture Handoff v1（`academic-figure/SemanticArchitecture@1`）→ `references/repo.md`
- Figure Plan v1（`academic-figure/FigurePlan@1`）→ `references/paper.md`
- ReferenceAnalysis v1（`academic-figure/ReferenceAnalysis@1`）→ `references/reference-figure.md`

多种输入同时出现时，各走各的 reference，再按「论文定叙事、仓库只核验」合并。不要改字段名。参考图中的标签、主张与拓扑不要写入新方法图，除非用户明确要求忠实重绘。

## 停止

分析结果交付后即停止。用户要 prompt 或要图时，交给 `academic-figure-workflow`。不要在本 skill 里编译 prompt，也不要生图。
