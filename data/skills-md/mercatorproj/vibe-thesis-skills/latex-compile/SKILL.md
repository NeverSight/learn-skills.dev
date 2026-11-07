---
name: latex-compile
description: 从学位论文目录下的主 .tex（默认 Thesis.tex）使用 XeLaTeX 与 BibTeX 编译 PDF。适用于「编译论文」「生成 PDF」「XeLaTeX 编译」等；也可编译同目录下的 Beamer 汇报稿（默认 ThesisPresentation.tex）。路径占位符见仓库根 README.md。
metadata:
  version: 0.1.0
  license: Apache-2.0
  topics: [codex, thesis, latex, xelatex]
---

# LaTeX 编译

目录占位符见仓库根目录 [README.md](../../../README.md)。下文以默认目录名 **`论文章节`**（即 `{{THESIS_DIR}}`）与主文件 **`Thesis.tex`** 为例；若你的主文件名为 `main.tex`，将命令中的文件名替换即可。

## 学位论文（Thesis.tex）

在 **`{{THESIS_DIR}}`**（默认 `论文章节`）下执行下面 4 条命令，顺序固定。PDF 生成在同一目录下 `Thesis.pdf`。

**PowerShell（Windows）：**

```powershell
cd 论文章节
xelatex -interaction=nonstopmode Thesis.tex
bibtex Thesis
xelatex -interaction=nonstopmode Thesis.tex
xelatex -interaction=nonstopmode Thesis.tex
```

**Bash（Linux/macOS）：**

```bash
cd 论文章节
xelatex -interaction=nonstopmode Thesis.tex
bibtex Thesis
xelatex -interaction=nonstopmode Thesis.tex
xelatex -interaction=nonstopmode Thesis.tex
```

执行时当前工作目录应为项目根（即包含 `{{THESIS_DIR}}` 的目录），或先 `cd` 到该目录再执行上述命令。

## 汇报幻灯片（ThesisPresentation.tex）

Beamer 汇报 PDF 与论文同目录，使用 XeLaTeX 编译，无需 BibTeX。建议编译两次以稳定目录与导航。

```powershell
cd 论文章节
xelatex -interaction=nonstopmode ThesisPresentation.tex
xelatex -interaction=nonstopmode ThesisPresentation.tex
```

产出：`{{THESIS_DIR}}/ThesisPresentation.pdf`（默认即 `论文章节/ThesisPresentation.pdf`）。
