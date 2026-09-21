---
name: latex
description: Use when converting a PDF into LaTeX/Beamer for academic templates (AEA, 经济研究, NAU, SCU), extracting structured content from PDFs, or compiling LaTeX documents.
---

# LaTeX

## 触发条件（满足其一）
- 把 PDF 转为 **AEA/经济研究/NAU/SCU** 模板的 LaTeX/Beamer，并编译成 PDF
- 需要从 PDF 抽取结构化内容（摘要/引言/文献综述/数据/方法/结果/结论）并写入模板
- 需要完整流水线：`marker_extract.py → 复制模板 → latex-server 写入 → compile.py`
- 只需要单点功能：`marker_extract.py` / 复制模板 / `latex-server` / `compile.py`

## 核心原则
- **先抽取再写模板**：有 PDF 时，必须先跑 `marker_extract.py`
- **只改内容，不改样式**：禁止修改 `.cls/.sty/.bst`
- **路径一律绝对路径**

## 资源导航（必须先看）
- 脚本：`/Users/lingguiwang/.codex/skills/latex/scripts/`
  - `marker_extract.py`（PDF → 中间产物）
  - `compile.py`（编译 LaTeX）
- 说明：`/Users/lingguiwang/.codex/skills/latex/references/`
  - `marker_extract.md`（参数与排错）
  - `compile.md`（编译参数与排错）
- 模板：`/Users/lingguiwang/.codex/skills/latex/assets/`
  - AEA：`/Users/lingguiwang/.codex/skills/latex/assets/AEA/`
  - 经济研究：`/Users/lingguiwang/.codex/skills/latex/assets/经济研究/`
  - NAU：`/Users/lingguiwang/.codex/skills/latex/assets/NAU/`
  - SCU：`/Users/lingguiwang/.codex/skills/latex/assets/SCU/`

## 端到端流程（推荐主流程）
1) **复制模板到工作目录**（绝对路径）
2) **运行 `marker_extract.py`**：PDF → 中间产物  
   - **优先使用 `--use_llm`**  
   - **若不使用 LLM，默认使用 `--torch_device mps`**  
   - **一般不使用 `--no_tables`，如需使用必须先征询用户**  
   - **默认超时 40 分钟**  
   - **若出现 `PermissionError(1, 'Operation not permitted')`，必须输出两套完整可运行命令（含 LLM 与不含 LLM），供用户本地直接运行**
3) **整理结构内容**：从 `document.md / equations.tex / references.bib` 提取并改写
4) **用 latex-server 写入模板 `.tex`**（仅改内容）
5) **运行 `compile.py` 编译 PDF**

## 公式处理策略（更新规则）
允许 **尽可能插入 `equations.tex` 中的全部公式**，并与 `document.md` 叙述对应，要求：
- 可整段插入 `equations.tex`（或分段插入到对应章节）
- 公式需与对应段落/章节一致（必要时加过渡说明）
- 写入后需人工快速检查（符号与上下文一致）

## 单点功能（可独立使用）

### A) 只做 PDF 抽取（marker_extract.py）
- 脚本：`/Users/lingguiwang/.codex/skills/latex/scripts/marker_extract.py`
- 说明：`/Users/lingguiwang/.codex/skills/latex/references/marker_extract.md`

重要说明：**仅支持单个 PDF 文件输入，不支持目录批量。**

本地深度学习管线（不加 `--use_llm`）：
```bash
python /Users/lingguiwang/.codex/skills/latex/scripts/marker_extract.py \
  "/abs/path/to/your.pdf" \
  -o "/abs/path/to/marker_out"
```

LLM 管线（优先使用 chatanywhere）：
```bash
python /Users/lingguiwang/.codex/skills/latex/scripts/marker_extract.py \
  "/abs/path/to/your.pdf" \
  -o "/abs/path/to/marker_out" \
  --use_llm --provider chatanywhere
```

**权限错误兜底（新增规则）**  
当遇到 `PermissionError(1, 'Operation not permitted')` 且无法通过常规权限设置解决时，必须输出 **两套完整可运行命令**（一套启用 LLM，一套不启用 LLM），示例：

不使用 LLM：
```bash
python /Users/lingguiwang/.codex/skills/latex/scripts/marker_extract.py \
  "/abs/path/to/your.pdf" \
  -o "/abs/path/to/marker_out" \
  --torch_device mps
```

使用 LLM：
```bash
python /Users/lingguiwang/.codex/skills/latex/scripts/marker_extract.py \
  "/abs/path/to/your.pdf" \
  -o "/abs/path/to/marker_out" \
  --use_llm --provider chatanywhere
```

LLM provider 支持：`openai` / `deepseek` / `chatanywhere` / `ollama` / `openrouter`

输出结构（每个 PDF 一个子目录）：
- `document.md`（正文）
- `equations.tex`（公式）
- `images/`（图片）
- `references.txt` / `references.bib`
- `manifest.json`

> 完整参数、模型选择与 API Key 说明见 `marker_extract.md`。

### B) 只复制模板
```bash
cp -R /Users/lingguiwang/.codex/skills/latex/assets/AEA /abs/path/AEA
cp -R /Users/lingguiwang/.codex/skills/latex/assets/经济研究 /abs/path/erj
cp -R /Users/lingguiwang/.codex/skills/latex/assets/NAU /abs/path/NAU
cp -R /Users/lingguiwang/.codex/skills/latex/assets/SCU /abs/path/SCU
```

### C) 只用 latex-server 写入模板
- `list_latex_files`：列出入口 `.tex`
- `read_latex_file`：读取全文定位
- `get_latex_structure`：查看章节结构
- `edit_latex_file`：精准插入/替换（仅改内容）
- `validate_latex`：基础语法校验

替换摘要（示例）：
```json
{
  "file_path": "/abs/path/to/main.tex",
  "operation": "replace",
  "search_text": "\\begin{abstract}",
  "new_text": "\\begin{abstract}\n这里替换为你的摘要内容。\n\\end{abstract}"
}
```

在某章节后插入“实证结果”小节（示例）：
```json
{
  "file_path": "/abs/path/to/main.tex",
  "operation": "insert_after",
  "search_text": "\\section{数据与方法}",
  "new_text": "\\section{实证结果}\n这里写实证结果正文。\n"
}
```

### D) 只编译（compile.py）
- 脚本：`/Users/lingguiwang/.codex/skills/latex/scripts/compile.py`
- 说明：`/Users/lingguiwang/.codex/skills/latex/references/compile.md`

最稳妥方式：
```bash
python /Users/lingguiwang/.codex/skills/latex/scripts/compile.py \
  --path "/abs/path/to/main.tex" \
  --output "/abs/path/to/project"
```

macOS 常见：指定可写 tmpdir（避免 Ghostscript 写系统临时目录失败）：
```bash
python /Users/lingguiwang/.codex/skills/latex/scripts/compile.py \
  --path "/abs/path/to/main.tex" \
  --output "/abs/path/to/project" \
  --tmpdir "/abs/path/to/project/.tmp"
```

编译输出：
- PDF：`<output>/build_pdf/`
- 日志：`<output>/build_logs/`

## 最小可运行示例工程（NAU Beamer + marker_extract 输出）
目标：在 NAU 模板目录内完成“抽取→写入→编译”。

1) 复制 NAU 模板
```bash
cp -R /Users/lingguiwang/.codex/skills/latex/assets/NAU /abs/path/to/NAU
```

2) 运行 `marker_extract.py` 生成中间产物（优先 LLM+chatanywhere）
```bash
python /Users/lingguiwang/.codex/skills/latex/scripts/marker_extract.py \
  "/abs/path/to/your.pdf" \
  -o "/abs/path/to/marker_out" \
  --use_llm --provider chatanywhere
```

3) 在 `/abs/path/to/NAU/slide.tex` 中写入内容
- 正文来自：`/abs/path/to/marker_out/<pdf_stem>/document.md`
- 公式来源：结合 `document.md` 的上下文，**尽可能插入 `equations.tex` 中的全部公式**，可整段或分段写入
- 参考文献来自：`/abs/path/to/marker_out/<pdf_stem>/references.bib`

公式写入示例（从 equations.tex 选取后粘贴）：
```tex
\begin{equation}
Y_{it} = \alpha + \beta X_{it} + \gamma Z_{it} + \varepsilon_{it}
\end{equation}
```

图片插入（示例）：
```tex
% 直接插图
\includegraphics[width=0.8\textwidth]{/abs/path/to/marker_out/<pdf_stem>/images/fig1.png}

% figure 环境
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.7\textwidth]{/abs/path/to/marker_out/<pdf_stem>/images/fig1.png}
  \caption{样本文字或图注}
  \label{fig:sample}
\end{figure}
```

参考文献最小引用示例：
```tex
文献回顾见 \cite{smith2020example}。

% 末尾
\bibliography{/abs/path/to/marker_out/<pdf_stem>/references.bib}
```

NAU 封面字段示例（中文）：
```tex
\title{研究标题：产业组织理论应用}
\author{凌贵旺}
\institute{南京农业大学经济管理学院}
\date{2025-12-31}
```

NAU 封面字段示例（英文）：
```tex
\title{Industrial Organization: An Application}
\author{Guiwang Ling}
\institute{College of Economics and Management, Nanjing Agricultural University}
\date{2025-12-31}
```

从 document.md 拆分为章节（模板片段）：
```tex
\section{引言}
% 从 document.md 抽取引言段落，整理为连贯文字

\section{文献综述}
% 从 document.md 抽取相关段落，去除重复与噪声

\section{数据与方法}
% 抽取数据来源、变量定义与识别策略

\section{实证结果}
% 结合图表与回归结果，给出结构化叙述

\section{结论与启示}
% 总结主要发现与政策含义
```

4) 编译
```bash
python /Users/lingguiwang/.codex/skills/latex/scripts/compile.py \
  --path "/abs/path/to/NAU/slide.tex" \
  --output "/abs/path/to/NAU"
```

## FAQ 入口
- 抽取与 LLM 相关问题：`/Users/lingguiwang/.codex/skills/latex/references/marker_extract.md`
- 编译与日志排错：`/Users/lingguiwang/.codex/skills/latex/references/compile.md`

## 常见问题（快速定位）
- 参考文献不出：确认 `.bib` 路径 + `biber/bibtex` 可用（见 `compile.md`）
- 中文字体告警：优先 `xelatex/lualatex`，检查字体
- 图片/表格找不到：检查 `\\includegraphics{}` 路径，isolated 模式注意 `../` 依赖
- Ollama 502/超时：确保 `NO_PROXY` 包含 `localhost,127.0.0.1`（见 `marker_extract.md`）

## 检查清单（交付前）
- [ ] 已用 `marker_extract.py` 生成 `document.md/equations.tex/references.bib`
- [ ] 仅修改 `.tex` 内容区，未改 `.cls/.sty/.bst`
- [ ] 所有路径为绝对路径
- [ ] `compile.py` 指定 `--output`，必要时指定 `--tmpdir`
- [ ] 查看 `build_logs`，确认无致命错误
- [ ] 若使用 LLM 自动写入公式，已人工核对符号与上下文一致

## 交付模板（YAML 附录）
```yaml
project_root: /abs/path/to/project
template: NAU
pdf_input: /abs/path/to/your.pdf
marker_out: /abs/path/to/marker_out/<pdf_stem>
main_tex: /abs/path/to/main.tex
compile_output: /abs/path/to/project
compile_logs: /abs/path/to/project/build_logs
notes: ""
```
