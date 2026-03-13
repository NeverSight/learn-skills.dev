---
name: academic-latex-pipeline
description: >-
  Complete workflow for converting Korean/English academic survey Markdown into
  publication-quality LaTeX PDFs. Handles Obsidian artifact cleanup (wikilinks,
  mermaid), XeLaTeX compilation with Korean font support (ucharclasses + Noto
  Sans CJK KR), BibTeX citations, TikZ figure generation, tcolorbox example
  boxes, and iterative format review. Supports section-based folder structure
  with main.tex orchestrator and BibTeX refs.bib management. Use this skill
  whenever the user wants to build a PDF from an academic markdown file,
  compile a LaTeX survey paper, or fix formatting issues in an existing
  academic PDF. MANDATORY TRIGGERS: LaTeX survey, academic PDF, 서베이 PDF,
  논문 PDF 빌드, xelatex, build_latex.py, Korean academic paper, survey
  compilation
---

# Academic LaTeX Pipeline

Converts academic survey Markdown (often from Obsidian) into polished LaTeX PDFs. The pipeline has five phases, each with a decision gate before proceeding.

## When to Use

- User has a `.md` survey/paper and wants a PDF
- User wants to fix formatting in an existing LaTeX-compiled PDF
- User needs Korean font support in LaTeX (XeLaTeX + Noto Sans CJK KR)
- User wants to replace Mermaid diagrams with TikZ figures
- User mentions `build_latex.py` or survey compilation
- User wants to restructure a LaTeX project into section-based folders

## Phase Overview

```
Phase 1: Content Quality    → iterative-academic-writing skill, Critical=0 to pass
Phase 2: LaTeX Build        → MD→TEX→PDF pipeline with Korean fonts
Phase 3: Format Review      → Page-by-page visual inspection, fix overflows
Phase 4: Figure Validation  → TikZ rendering, captions, sizing
Phase 5: Git Management     → latex-project-manager skill for structure + push
```

---

## Phase 1: Content Writing Loop

Invoke `iterative-academic-writing` skill on the source `.md` file. The skill applies 14 academic writing principles with FactBase verification and hallucination detection.

**Gate**: Critical issues = 0 → proceed to Phase 2.

This phase ensures content quality before expensive LaTeX processing. Don't skip it — fixing content errors after PDF generation wastes time.

---

## Phase 2: LaTeX Build Pipeline

### 2.1 Project Structure

Projects use section-based folder organization for maintainability:

```
ProjectName/
├── main.tex                   # Shared preamble + project selector switch
├── <project>/
│   ├── content.tex            # \input orchestrator for all sections
│   ├── refs.bib               # BibTeX bibliography (NOT inline thebibliography)
│   ├── figures/               # Images and generated figures
│   │   └── .gitkeep
│   └── sections/
│       ├── 00_frontmatter.tex # \title, \author, \maketitle, \abstract
│       ├── 01_background.tex  # Each \section in its own file
│       ├── ...
│       └── NN_bibliography.tex # \bibliographystyle + \bibliography
├── .gitignore
└── build_and_compile.sh       # Optional: shell wrapper for compilation
```

For MD→TEX projects (Obsidian source), also include:
```
├── SourceDocument.md          # Obsidian source (excluded from git)
└── build_latex.py             # Python build script (MD → TEX → PDF)
```

**Multi-project layout**: Use `\newcommand{\professor}{project_name}` in `main.tex` to switch between projects sharing the same preamble. See `latex-project-manager` skill for details.

### 2.2 Bibliography Management (CRITICAL)

**Always use BibTeX `.bib` files. Never use inline `\begin{thebibliography}`.**

- Create `refs.bib` in the project folder root
- Use `\bibliographystyle{plainnat}` + `\bibliography{<project>/refs}`
- All references must use `\citep{}` or `\citet{}` — no plain text "(Author, Year)"
- 3-pass compilation: `pdflatex → bibtex → pdflatex → pdflatex`

### 2.3 Build Script (`build_latex.py`)

The build script handles the full MD→TEX transformation:

1. **Preprocess MD**: Strip wikilinks `[[...]]`, remove Obsidian YAML frontmatter, clean tags
2. **Pandoc conversion**: `pandoc input.md -f markdown -t latex`
3. **Inject preamble** with Korean font support:
   ```latex
   \usepackage{fontspec}
   \usepackage{ucharclasses}
   \setmainfont{Noto Sans CJK KR}
   \newfontfamily\hangulfont{Noto Sans CJK KR}
   \setTransitionsForCJK{\hangulfont}{}{}
   ```
   Why `ucharclasses` instead of `xeCJK`? The `xeCJK` package requires `ctexhook.sty` which is missing from many LaTeX distributions. `ucharclasses` is more portable.

4. **Replace Mermaid** blocks with TikZ figures
5. **Wrap examples** in `tcolorbox` environments
6. **Inject citations**: Match `PaperName (Year)` → `\cite{key_year}`
7. **Fix tables**: Use `p{Xcm}` columns instead of `l`/`c`/`r` to prevent overflow

### 2.4 Font Installation
```bash
mkdir -p ~/.local/share/fonts
# Download Noto Sans CJK KR from github.com/googlei18n/noto-cjk/releases
fc-cache -fv ~/.local/share/fonts/
```

### 2.5 Compilation (3-pass)
```bash
pdflatex -interaction=nonstopmode main.tex    # Pass 1 (or xelatex for Korean)
bibtex main                                    # Citations
pdflatex -interaction=nonstopmode main.tex    # Pass 2 (resolve refs)
pdflatex -interaction=nonstopmode main.tex    # Pass 3 (final)
```

### 2.6 Overfull Hbox Prevention (Preamble)
```latex
\tolerance=1000
\emergencystretch=3em
\hfuzz=2pt
```

**Gate**: Compilation succeeds without errors → proceed to Phase 3.

---

## Phase 3: Format Review Loop

Review the PDF page by page. Check for:

**Critical** (must fix, loop back):
- Table overflow beyond margins
- Missing or blank figures
- Unreadable/clipped text
- `[[wikilink]]` artifacts surviving preprocessing
- Undefined citations

**Minor** (can defer):
- Spacing tweaks, caption capitalization, color preferences

For each critical issue:
- Table overflow → adjust column widths, use `tabularx` with `X` columns
- Missing figures → test TikZ in standalone mode, simplify
- Wikilinks → fix regex in build script's preprocessing step
- Undefined citations → add entries to `refs.bib`

Recompile after fixes. Gate: no Critical issues → Phase 4.

---

## Phase 4: Figure/Image Review

For each TikZ figure:
1. Does it render correctly?
2. Is the caption present and descriptive?
3. Is sizing appropriate (`\resizebox{\textwidth}{!}{...}`)?
4. Is placement correct (`[H]` float specifier)?

Test problematic TikZ in isolation:
```latex
\documentclass[tikz]{standalone}
\usepackage{tikz}
\begin{document}
% TikZ code here
\end{document}
```

Gate: all figures correct → Phase 5.

---

## Phase 5: Git Management

Use `latex-project-manager push` for structured git operations.

### Files to include in repo:
- `main.tex`, `<project>/content.tex`, `<project>/sections/*.tex`
- `<project>/refs.bib`
- `<project>/figures/*`
- `.gitignore`
- `build_latex.py`, `build_and_compile.sh` (if applicable)

### Files to exclude:
- Original `.md` Obsidian source (stays in Obsidian vault only)
- `.obsidian/` directory
- LaTeX build artifacts (`.aux`, `.log`, `.out`, `.toc`, `.bbl`, `.blg`)
- PDF files (compiled on-demand)

### `.gitignore` template:
```
*.aux
*.log
*.out
*.toc
*.bbl
*.blg
*.synctex.gz
*.fls
*.fdb_latexmk
*.pdf
.DS_Store
```

### Git authentication:
- GitHub: `$GITHUB_TOKEN` env var or user-provided token
- Overleaf: `$OVERLEAF_TOKEN` env var (requires Premium plan for git access)

---

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Korean text missing | Verify Noto Sans CJK KR installed, check `fc-list \| grep Noto` |
| Overfull hbox | Increase `\tolerance`, `\emergencystretch`, reword long lines |
| Table overflow | Use `p{2cm}` or `X` columns, reduce content |
| Broken tcolorbox | Check `\tcbuselibrary{most}` is loaded |
| Undefined citations | Add missing keys to `refs.bib`, rerun bibtex |
| Mermaid not replaced | Check regex pattern in build script |
| pgfplots `\\` in labels | Use `{Label Text}` with `align=center` instead |
| `$\to$` in `\legend` | Use `\textrightarrow{}` instead |
| Inline thebibliography | Convert to `refs.bib` + `\bibliography{}` |

## English Version Generation

For bilingual projects, create a separate English build:
- Translate MD content (keep same structure)
- Use English-specific preamble (no CJK fonts needed, use standard `\usepackage[T1]{fontenc}`)
- Generate `survey_main_EN.tex` → `survey_main_EN.pdf`
- Both versions share `refs.bib`

## Related Skills

- `iterative-academic-writing` — Phase 1 content evaluation
- `latex-project-manager` — Phase 5 project structuring and git push
- `pdf` — General PDF manipulation (merge, split, forms)
