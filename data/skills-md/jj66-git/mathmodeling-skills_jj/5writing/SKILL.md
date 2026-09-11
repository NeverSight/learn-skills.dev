---
name: 5writing
description: "数学建模竞赛论文撰写阶段，支持 Typst 和 LaTeX 双引擎。根据 ANALYSIS_MODELING_REPORT.md、RESULTS_REPORT.md 和 figures/*.pdf 选择比赛模板、排版引擎、组织章节、插入图表，并在适用的全国大学生数学建模竞赛论文中生成证据驱动的 AI 工具使用声明与使用详情。"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch
---

# 竞赛论文撰写（Typst / LaTeX）

本 skill 承接 `3coding-visual` 和 `4drawio`。前序阶段只提供真实数据、图表 PDF 和记录文件；本阶段负责选择比赛模板和排版引擎、组织论文结构，并决定每张图表放入哪个章节。

**Typst 引擎**下可调用 typst-author skill 学习 typst 写法；**LaTeX 引擎**参考本文件末尾的"LaTeX 写作要点"小节。

## 数学建模规范参考

如需领域判断，读取 `../mathmodel-references/math_modeling_norms.md` 中的“论文写作”“图表与可视化”和“非数据图工具选择”小节。该文件只作为规范知识库，论文结构仍按比赛模板和当前赛题内容决定。

## 模板族

本技能内捆绑的模板位于：

```text
templates/zh/<竞赛>/main.typ         # Typst 模板
templates/zh/<竞赛>-latex/main.tex   # LaTeX 模板
templates/en/<竞赛>/main.typ         # Typst 模板
templates/en/<竞赛>-latex/main.tex   # LaTeX 模板
```

**LaTeX 模板覆盖范围**：所有中文模板和英文模板均已提供 LaTeX 版本（`-latex` 后缀），使用 xelatex 编译。

支持的中文模板（Typst + LaTeX 双版本）：

```text
apmcm, changsanjiao, cumcm, default, diangongbei, dongsansheng,
huashubei, huaweibei, huazhongbei, mathorcup, mcm, shuweibei, stats, wuyibei
```

华为杯、华中杯、五一杯统一使用 `huaweibei`、`huazhongbei`、`wuyibei` 作为模板。

支持的英文模板（Typst + LaTeX 双版本）：

```text
apmcm, default, mcm
```

## 全国赛（CUMCM）硬性写作规则

当竞赛识别为全国大学生数学建模竞赛、国赛或 `CUMCM` 时，默认采用以下不可省略的结构约束：

- **不添加目录**：不得调用 `#outline`、`\tableofcontents` 或自定义目录页；摘要后直接进入正文。只有用户或赛事官方模板明确要求目录时才可例外，并在构建记录中说明依据。
- **问题分析分层**：`2_analysis` 必须先给出全题总体分析，再按 `问题一/问题二/...` 分点展开；每个小问至少写清任务目标、已知数据或证据、决策变量/关键因素、约束与评价指标、模型选择理由、输出及其与后续章节的关系。
- **证据驱动**：每个小问的判断都要绑定题干、数据报告、文献或已验证实验结果；没有来源的推断标记为待核验，不得用空泛的“需要综合考虑”替代证据。
- **结构自适应**：题目有几个子问题就生成几个对应小节，不得只写“总体分析”而遗漏子问题，也不得凭空增加题目没有的子问题。

问题分析推荐顺序：`总体分析 → 问题一 → 问题二 → … → 问题间依赖与信息流`。每个小问可使用编号条目，但条目必须是完整的论证句，不是关键词堆砌。

论文中的所有数值图表结论必须来自 `reports/RESULTS_REPORT.md` 或 `figures/*`。不得编造、估算或使用不同的四舍五入方式。

## Academic writing 增强层（可选）

如果当前项目采用严格的 `workflow-orchestrator` 目录，则
`results/Qx/reports/frozen_numbers.json`、`qx_solution_package_for_writer.md` 和人工决策日志的
优先级高于本 skill 的简化 `RESULTS_REPORT.md` 输入。可在正式排版前调用 `academic-paper`
的 `plan` / `outline-only` 模式生成全局提纲、页数预算和 claim-evidence map；正文仍由
`paper-section-writer` 按 Qx solution package 撰写。本 skill 只负责模板、引擎、组装和编译，
不得让 academic journal 默认结构覆盖比赛模板。


## 工作流

### 步骤 0：确定排版引擎

**撰写论文前必须让用户选择排版引擎。** 引擎决定后续所有步骤（模板路径、章节文件扩展名、图片插入语法、编译命令），选错会导致整篇论文格式错误。

使用 AskUserQuestion 工具向用户询问："撰写论文使用哪种排版引擎？"

- 选项 1：LaTeX（xelatex 编译，数学建模竞赛主流，模板已全部就绪）— 推荐选项放第一位
- 选项 2：Typst（typst 编译，调用 typst-author skill 辅助写作）

询问前先读取 `plan.md` 的"用户偏好 → 排版引擎"字段作为预选项：
- 若 plan.md 已记录引擎选择，向用户确认："检测到之前选择的引擎是 <LaTeX/Typst>，是否沿用？"
- 若 plan.md 不存在或未记录引擎选择，直接询问用户选择。
- 若用户未明确指定或跳过，**默认使用 LaTeX**。

根据确定的引擎选择对应模板族：

- **Typst 引擎**：使用 `templates/<lang>/<竞赛>/main.typ`，调用 typst-author skill。编译命令 `typst compile main.typ`。
- **LaTeX 引擎**：使用 `templates/<lang>/<竞赛>-latex/main.tex`，xelatex 编译（中文和英文均需跑两遍解决交叉引用）。编译命令 `xelatex -interaction=nonstopmode main.tex`（执行两次）。

**后续步骤中的所有代码示例、文件扩展名、图片插入语法都必须按所选引擎选择对应版本，不要混用。**

### 步骤 1：选择语言和模板


除非用户明确要求中文，否则 MCM/ICM/COMAP 一律使用英文。所有中文竞赛名称使用中文。

模板键示例（Typst 引擎）：

```text
长三角 -> zh/changsanjiao
APMCM 英文版 -> en/apmcm
全国赛/国赛/CUMCM -> zh/cumcm
统计建模 -> zh/stats
MCM/ICM/COMAP -> en/mcm
```

模板键示例（LaTeX 引擎）：

```text
全国赛/国赛/CUMCM -> zh/cumcm-latex
MCM/ICM/COMAP -> en/mcm-latex
```

### 步骤 2：准备模板

用以下命令检查捆绑模板是否可访问（`SKILL_DIR` 为本 skill 所在目录）：

**Typst 模板**：

```bash
ls "$SKILL_DIR/templates/zh/<竞赛>/main.typ" 2>/dev/null && echo "OK" || echo "MISSING"
```

- **文件存在（OK）**：直接将 `templates/zh/<竞赛>/` 整目录复制到 `paper/`。这些模板是自包含入口文件，不依赖额外共享样式文件。
- **文件不存在（MISSING）**：说明 skill 未完整安装或在沙箱中，此时依照本 SKILL.md 步骤 3 列出的对应节文件结构，从零重建最小可编译 Typst 框架，并在 `paper/` 内注明"重建自 default 结构"。

存在匹配模板时，绝不从零开始写论文。

**LaTeX 模板**：

```bash
ls "$SKILL_DIR/templates/zh/<竞赛>-latex/main.tex" 2>/dev/null && echo "OK" || echo "MISSING"
```

- **文件存在（OK）**：将 `templates/zh/<竞赛>-latex/` 整目录复制到 `paper/`。
- **文件不存在（MISSING）**：说明 skill 未完整安装或在沙箱中，此时依照本 SKILL.md 步骤 3 列出的对应节文件结构，从零重建最小可编译 LaTeX 框架，并在 `paper/` 内注明"重建自 default-latex 结构"。


### 步骤 3：构建图表规划

Before inserting any figure, read `paper/figures/figure_manifest.json`,
`paper/figures/figure_qa_log.md`, and `paper/issues/issue_register.md` when present. Insert a
required final figure only when its editable source exists, its visual QA is `PASS`, and it has no
`OPEN` or `BLOCKING` issue. A rendered Mermaid or TikZ image may occupy the intended slot during
drafting, but mark the paper build as blocked while its manifest state is `PLACEHOLDER`,
`AWAITING_SAVE`, or `UNVERIFIED_MCP_FALLBACK`. Do not describe a placeholder as final and do not
allow G5/G6 to pass.

在写正文各节之前，根据 `figures/*.pdf`、`reports/RESULTS_REPORT.md`，以及 `reports/DRAWIO_REPORT.md`（如果存在）构建图表规划：

论文仅插入 `modeling-figure-orchestrator` 已标记 `PASS` 的必要图表。核对核心模型原理、关键结果对比、敏感性/稳健性分析和决策方案四类内容已覆盖或有不适用说明；同类信息优先合并，不用多幅低信息密度图占版面。

对全国赛论文，图表规划还必须包含一张论文整体示意图（通常命名为 `fig_paper_overview` 或 `fig_roadmap`）。当正文出现重要算法、求解器或迭代机制时，按论证需要自主选择 `algorithm flowchart`（输入—处理—判断—输出）、`algorithm concept/mechanism diagram`（模块、变量、反馈和作用机理），或两者组合；只有当流程和机制都承担不可替代的解释任务时才同时生成。无论选择哪一种，都要保留可编辑源文件并通过同一套逻辑 QA。

```text
图表规划
fig_roadmap.pdf -> 引言/问题重述
fig_flow_q1.pdf -> 问题一模型构建
fig_flow_q2.pdf -> 问题二模型构建
fig_pipeline.pdf -> 数据预处理/方法节
结果图 -> 对应的结果节
```

图片路径相对于写入该图片的文件：写在 `paper/main.typ` 或 `paper/main.tex` 中通常用 `../figures/xxx.pdf`，写在 `paper/sections/*.typ` 或 `paper/sections/*.tex` 中通常用 `../../figures/xxx.pdf`。

**Typst 引擎**图片插入：

```typst
#figure(
  image("../../figures/fig_q1_error_dist.pdf", width: 100%),
  caption: [问题一预测误差分布],
)
```

**LaTeX 引擎**图片插入：

```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=\textwidth]{../../figures/fig_q1_error_dist.pdf}
  \caption{问题一预测误差分布}
  \label{fig:q1_error}
\end{figure}
```

英文论文使用英文图注。

排版时单栏图宽度使用 `100%`/`\textwidth`，跨栏图不超过页面总版心。保持图高 >=5 cm；核心结果图可占约 1/3-1/2 页。编译后在实际缩放比下检查图内最小字号 >=7.5 pt（中文六号），并核验有效分辨率、线条和文字清晰度；矢量图优先，位图按最终插入尺寸达到清晰可读即可，不把 300 dpi 当作无条件门槛。若缩印后文字低于六号或出现模糊、锯齿、裁切，必须回到绘图阶段修复。

### 步骤 4：撰写各节

写 `2_analysis.typ`/`2_analysis.tex` 时，先完成全题问题链，再逐题落地。逐题小节必须按照“目标—证据—变量—约束/指标—方法理由—输出”的顺序组织；若某项不适用，写出基于题面或数据的理由。不得把多个小问合并成一段笼统描述。

**以下章节文件名按所选引擎使用 `.typ`（Typst）或 `.tex`（LaTeX）扩展名。** 例如 Typst 引擎用 `1_restatement.typ`，LaTeX 引擎用 `1_restatement.tex`。文件名主体保持一致。

中文数学建模通用模板各节文件（`changsanjiao`、`diangongbei`、`huashubei`、`mathorcup`、`wuyibei`）：

```text
1_restatement.typ  - 问题重述与分析
2_analysis.typ     - 数据理解与总体思路
3_assumptions.typ  - 模型假设
4_symbols.typ      - 符号说明
5_problem1.typ     - 问题一建模与求解
6_problem2.typ     - 问题二建模与求解
7_problem3.typ     - 问题三建模与求解
...         - 根据题目调整问题数量  
8_evaluation.typ   - 灵敏度分析、模型评价与推广
A_code.typ         - 附录代码
```

国赛/华中杯/华为杯（`cumcm`、`huazhongbei`、`huaweibei`）按以下章节结构：

```text
1_restatement.typ
2_analysis.typ
3_assumptions.typ
4_symbols.typ
5_problem1.typ
6_problem2.typ
7_problem3.typ
...        - 根据题目调整问题数量
8_sensitivity.typ
9_evaluation.typ
A_code.typ
```

东三省模板（`dongsansheng`）额外使用单独摘要文件：

```text
abstract.typ
1_restatement.typ
2_analysis.typ
3_assumptions.typ
4_symbols.typ
5_problem1.typ
6_problem2.typ
7_problem3.typ
...       - 根据题目调整问题数量
8_evaluation.typ
A_code.typ
```

数维杯模板（`shuweibei`）保留原 LaTeX 的示例入口命名：

```text
Abstract.typ
Introduction.typ
2_analysis.typ
3_assumptions.typ
4_symbols.typ
5_problem1.typ
6_problem2.typ
7_problem3.typ
...      - 根据题目调整问题数量
8_evaluation.typ
Appendices1.typ
A_code.typ
```

中文默认模板（`default`）：

```text
1_restatement.typ
2_assumptions.typ
3_symbols.typ
4_problem1.typ
5_problem2.typ
6_problem3.typ
...      - 根据题目调整问题数量
7_sensitivity.typ
8_evaluation.typ
A_code.typ
```

中文统计建模各节文件：

```text
1_introduction.typ
2_method.typ
3_data.typ
4_analysis.typ
5_results.typ
6_conclusion.typ
A_code.typ
```

英文 MCM/APMCM 各节文件（`en/mcm`、`en/apmcm`、`zh/mcm`、`zh/apmcm`）：

```text
1_introduction.typ
2_assumptions.typ
3_model_design.typ
4_solution.typ
5_sensitivity.typ
6_strengths_weaknesses.typ
7_conclusions.typ
A_code.typ
```

**LaTeX 模板章节文件**（对应 `-latex` 后缀模板，结构与 Typst 版本一一对应）：

国赛 LaTeX 模板（`zh/cumcm-latex`，对应 `cumcm` Typst 版本）：

```text
1_restatement.tex
2_analysis.tex
3_assumptions.tex
4_symbols.tex
5_problem1.tex
6_problem2.tex
7_problem3.tex
8_sensitivity.tex
9_evaluation.tex
A_code.tex
```

MCM/ICM LaTeX 模板（`en/mcm-latex`）：

```text
1_introduction.tex
2_assumptions.tex
3_model_design.tex
4_solution.tex
5_sensitivity.tex
6_strengths_weaknesses.tex
7_conclusions.tex
A_code.tex
```

其余 LaTeX 模板（`changsanjiao-latex`、`default-latex`、`huashubei-latex`、`mathorcup-latex`、`wuyibei-latex`、`huazhongbei-latex`、`huaweibei-latex`、`diangongbei-latex`、`dongsansheng-latex`、`shuweibei-latex`、`stats-latex`、`apmcm-latex`、`mcm-latex`、`en/apmcm-latex`、`en/default-latex`）的章节文件命名与上述结构类似，以 `main.tex` 中 `\input{}` 引用的文件名为准。

英文默认模板（`en/default`）：

```text
1_introduction.typ
2_assumptions.typ
3_notations.typ
4_model.typ
5_sensitivity.typ
6_evaluation.typ
7_conclusions.typ
A_code.typ
```

**正文写作应使用连贯的学术段落。避免在最终论文中出现工作流内部名称，如 `reports/`、`figures/` 或 `CLAUDE.md`。**

### 步骤 5：全国大学生数学建模竞赛 AI 工具使用声明（2026 年试行）

当比赛为全国大学生数学建模竞赛（CUMCM），且适用 2026 年 9 月 1 日起试行的《人工智能工具使用规定》时，必须完整读取并执行 `references/cumcm-ai-tool-disclosure-2026.md`。

在生成声明前，先核对团队记录、AI 交互记录、版本历史、终端与测试记录，建立逐环节事实表。不得仅根据用户希望的措辞推断实际使用范围，也不得把建模、算法设计、代码生成、数据分析、作图、资料检索或论文写作伪装成“代码调试”。

- 若证据证明竞赛全过程未使用任何 AI 工具，使用规定中的“未使用”声明，不生成虚构的使用详情。
- 若证据证明 AI 仅用于代码调试，使用“主要用于代码调试”的声明，并生成 `supporting-materials/AI 工具使用详情.pdf`。
- 若 AI 用于代码调试和前期框架辅助，而模型、程序、结果、图表与论文均由队员后续实质性重构和核验，使用“主要用于代码调试及前期框架辅助”的声明，并在详情中逐项写明 AI 提供的初始框架、人工重构内容和验证证据。
- 若 AI 还用于其他环节，必须按实际用途完整披露；不得套用“仅代码调试”样稿。
- 若记录不足以确认真实使用范围，将声明和支撑材料标记为 `BLOCKED`，列出待团队确认的事实，不得自行补写工具、版本、提示词或核验结果。

“AI 工具使用声明”必须放在论文参考文献之前。声明正文使用官方规定的原句，不得改写为同义表述。若声明使用了 AI，详情 PDF 必须包含工具名称及版本或型号、具体用途和环节、主要提示方式与使用过程、典型交互（如提供），以及 AI 输出的采纳、人工修改和核验情况。

### 步骤 6：参考文献

只使用真实存在的参考文献。文件名按引擎选择：Typst 用 `paper/references.typ`，LaTeX 用 `paper/references.tex`。

**Typst 引擎**：

```typst
#set enum(numbering: "[1]")
#enum[
  作者. 题名[J]. 期刊名, 年份, 卷(期): 页码.
  Author. "Title." Journal or Conference, year.
]
```

正文上标引用：`相关研究已用于物流网络优化#super("[1]")。`

**LaTeX 引擎**：

```latex
\begin{thebibliography}{99}
  \bibitem{ref1} 作者. 题名[J]. 期刊名, 年份, 卷(期): 页码.
  \bibitem{ref2} Author. "Title." Journal, year.
\end{thebibliography}
```

正文引用用 `\cite{ref1}` 或 `\cite{ref1,ref2}`。

### 步骤 7：最后撰写摘要或总结

在所有章节完成后撰写中文摘要或英文 Summary Sheet。必须包含每个子问题的方法和精确的数值结果。

调用 `writing-modeling-abstracts`。单段摘要保留 3-5 组语义加粗，合计覆盖核心方法、关键模型、核心指标、结论数值和末尾关键词；加粗只包围关键词本身，不得包围完整句子。

全国赛摘要和正文终检还要确认：摘要后无目录页；问题分析同时存在总体分析和逐题分点分析；每个重要算法至少有一种与其解释负荷匹配的算法图示，必要时同时引用流程框图与概念/机制图，且图源和 QA 状态为 `PASS`。

### 步骤 8：生成支撑材料 ZIP 和论文附录清单

当竞赛为全国大学生数学建模竞赛或其广东赛区时，完整读取并执行 `references/cumcm-supporting-materials-package.md`。参赛论文 PDF 不得放进压缩包；支撑材料必须作为单独文件提交。

1. 将所有必要支撑材料整理到一个匿名目录中，包括全部可运行源程序、自主查阅的数据资料（赛题原始数据除外）、必要的大篇幅中间结果，以及使用 AI 时的 `AI 工具使用详情.pdf`。
2. 运行 `scripts/package_supporting_materials.ps1`。脚本使用 7-Zip 生成单个 ZIP，在压缩前创建 `支撑材料文件清单.md`，清单记录每个材料文件的相对路径、字节数和 SHA-256，并将清单一并放入 ZIP。
3. 把清单中的材料文件列表同步写入论文附录。论文附录与 ZIP 内清单必须逐项一致；源程序既要进入论文附录，也要进入 ZIP。
4. ZIP 必须小于 20 MiB，并通过 `7z t` 完整性测试。达到或超过上限、清单不一致、存在身份信息或包含承诺书/编号专用页时，标记为 `BLOCKED`，不得提交。
5. 最终关闭论文 PDF 和 ZIP，再通过比赛客户端生成并提交各自的 MD5。生成 MD5 后不得重新打开保存文件；若文件发生改变，必须在截止时间前重新生成并提交 MD5。

打包脚本返回成功只证明 ZIP 创建、清单生成、大小门禁和 `7z t` 通过，不代表支撑材料已经可以提交。必须继续执行 `6verity` 的 Step 9，完成解压复现、清单与论文附录比对以及匿名性和元数据检查。

Windows 调用示例：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$SKILL_DIR\scripts\package_supporting_materials.ps1" `
  -SourceDirectory ".\supporting-materials" `
  -OutputZip ".\submission\supporting-materials.zip"
```

若确实没有支撑材料，不生成空 ZIP，并在论文附录中写明“本论文没有支撑材料”。

## LaTeX 写作要点

以下要点供 **LaTeX 引擎**使用。Typst 引擎请调用 typst-author skill 获取语法帮助。

### 编译命令

```bash
# 中文模板（xelatex，跑两遍解决交叉引用）
xelatex main.tex && xelatex main.tex

# 英文模板（xelatex，同样跑两遍）
xelatex main.tex && xelatex main.tex
```

### 文档结构

```latex
\documentclass[a4paper,12pt]{article}   % 英文
\documentclass[a4paper,12pt]{ctexart}   % 中文

\usepackage{...}   % 宏包加载
\usepackage{graphicx}   % 图片支持
\usepackage{booktabs}   % 三线表
\usepackage{amsmath,amssymb}   % 数学公式
\usepackage{hyperref}   % 交叉引用（需两遍编译）
```

### 图表插入

```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=\textwidth]{../../figures/fig_q1.pdf}
  \caption{图注}
  \label{fig:q1}
\end{figure}

% 三线表
\begin{table}[htbp]
  \centering
  \caption{表注}
  \begin{tabular}{ccc}
    \toprule
    \textbf{列1} & \textbf{列2} & \textbf{列3} \\
    \midrule
    数据 & 数据 & 数据 \\
    \bottomrule
  \end{tabular}
\end{table}
```

### 交叉引用

```latex
如图~\ref{fig:q1}所示，...   % 图片引用
式~(\ref{eq:objective}) 给出...   % 公式引用
见第~\pageref{fig:q1} 页   % 页码引用
```

### 数学公式

```latex
行内公式：$f(x) = \sum_{i=1}^n \theta_i \phi_i(x)$

行间公式：
\begin{equation}
  \mathcal{L}(\theta) = \frac{1}{N}\sum_{i=1}^N (y_i - \hat{y}_i)^2
  \label{eq:objective}
\end{equation}
```

### 章节和强调

```latex
\section{问题重述}
\subsection{问题背景}
\textbf{问题一：} xxx   % 对应 Typst 的 #strong
```
