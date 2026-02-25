---
name: latex
description: "Comprehensive LaTeX reference for document creation, formatting, mathematics, tables, figures, bibliographies, and compilation. Use when helping users write, edit, debug, or compile LaTeX documents."
---

# LaTeX Skill

## 1. Overview

LaTeX is a markup language and typesetting system for producing high-quality documents. It excels at structured documents with complex formatting, mathematics, cross-references, and bibliographies.

**When to use LaTeX:**
- Academic papers, journal submissions
- Theses and dissertations
- Technical documentation
- CVs and résumés
- Presentations (Beamer)
- Books, reports, letters

**Key concepts:**

| Concept | Description |
|---------|-------------|
| **Preamble** | Everything before `\begin{document}` — class, packages, settings |
| **Document body** | Content between `\begin{document}` and `\end{document}` |
| **Commands** | Start with `\`, e.g. `\textbf{bold}`. Optional args in `[]`, required in `{}` |
| **Environments** | `\begin{name}...\end{name}` blocks for scoped formatting |
| **Packages** | Extensions loaded with `\usepackage{name}` in the preamble |

## 2. Document Structure

### Document Classes

```latex
\documentclass[options]{class}
```

| Class | Use case |
|-------|----------|
| `article` | Short documents, papers, assignments |
| `report` | Longer documents with chapters |
| `book` | Books (front/back matter, chapters) |
| `beamer` | Presentations/slides |
| `letter` | Formal letters |
| `memoir` | Flexible — replaces article/report/book |

### Common Class Options

```latex
\documentclass[12pt,a4paper,twocolumn,draft]{article}
```

| Option | Values |
|--------|--------|
| Font size | `10pt`, `11pt`, `12pt` |
| Paper | `a4paper`, `letterpaper`, `a5paper` |
| Columns | `onecolumn`, `twocolumn` |
| Sides | `oneside`, `twoside` |
| Draft | `draft` (shows overfull boxes, skips images) |

### Minimal Document

```latex
\documentclass[12pt,a4paper]{article}

% === PREAMBLE ===
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath, amssymb}
\usepackage{graphicx}
\usepackage{hyperref}

\title{My Document}
\author{Author Name}
\date{\today}

% === BODY ===
\begin{document}
\maketitle
\tableofcontents

\section{Introduction}
Content here.

\end{document}
```

## 3. Text Formatting

### Style Commands

| Command | Result |
|---------|--------|
| `\textbf{text}` | **bold** |
| `\textit{text}` | *italic* |
| `\underline{text}` | underlined |
| `\emph{text}` | emphasis (italic, or upright if already italic) |
| `\texttt{text}` | `monospace` |
| `\textsc{text}` | SMALL CAPS |
| `\textsf{text}` | sans-serif |

### Font Sizes

Smallest to largest:
```
\tiny  \scriptsize  \footnotesize  \small  \normalsize
\large  \Large  \LARGE  \huge  \Huge
```

Use as: `{\large This text is large.}` or as environment.

### Font Families

| Command | Declaration | Family |
|---------|-------------|--------|
| `\textrm{}` | `\rmfamily` | Serif (Roman) |
| `\textsf{}` | `\sffamily` | Sans-serif |
| `\texttt{}` | `\ttfamily` | Monospace |

### Alignment

```latex
\begin{center}    Centered text.    \end{center}
\begin{flushleft} Left-aligned.     \end{flushleft}
\begin{flushright} Right-aligned.   \end{flushright}
```

Or inline: `\centering`, `\raggedright`, `\raggedleft`

### Spacing

```latex
\vspace{1cm}          % vertical space
\hspace{2em}          % horizontal space
\vfill                % stretch vertical
\hfill                % stretch horizontal
\\[0.5cm]             % line break with extra space
\setlength{\parskip}{0.5em}   % paragraph spacing
\setlength{\parindent}{0pt}   % remove paragraph indent
\noindent             % suppress indent for one paragraph
```

Line spacing (requires `setspace` package):
```latex
\usepackage{setspace}
\onehalfspacing    % or \doublespacing, \singlespacing
```

### Special Characters

These characters must be escaped:

| Character | LaTeX | Character | LaTeX |
|-----------|-------|-----------|-------|
| `%` | `\%` | `$` | `\$` |
| `&` | `\&` | `#` | `\#` |
| `_` | `\_` | `{` | `\{` |
| `}` | `\}` | `~` | `\textasciitilde` |
| `^` | `\textasciicircum` | `\` | `\textbackslash` |

## 4. Document Organization

### Sectioning

```latex
\part{Part Title}           % only in report/book
\chapter{Chapter Title}     % only in report/book
\section{Section}
\subsection{Subsection}
\subsubsection{Subsubsection}
\paragraph{Paragraph}
\paragraphsub{Subparagraph}
```

Starred versions (`\section*{}`) suppress numbering and TOC entry.

### Table of Contents

```latex
\tableofcontents    % requires two compilations
\listoffigures
\listoftables
```

### Lists

```latex
% Bulleted
\begin{itemize}
  \item First item
  \item Second item
\end{itemize}

% Numbered
\begin{enumerate}
  \item First
  \item Second
\end{enumerate}

% Labeled
\begin{description}
  \item[Term] Definition here.
\end{description}
```

Customize with `enumitem` package:
```latex
\usepackage{enumitem}
\begin{enumerate}[label=(\alph*), start=1]
```

### Cross-References

```latex
\section{Methods}\label{sec:methods}
See Section~\ref{sec:methods} on page~\pageref{sec:methods}.
```

With `hyperref`, use `\autoref{sec:methods}` for automatic "Section 2" text.

**Rule:** Always place `\label` *after* `\caption` (in floats) or after the sectioning command.

### Footnotes

```latex
This has a footnote.\footnote{Footnote text here.}
```

## 5. Mathematics

### Inline vs Display

```latex
Inline: $E = mc^2$ or \(E = mc^2\)

Display:
\[ E = mc^2 \]

% Numbered equation:
\begin{equation}\label{eq:einstein}
  E = mc^2
\end{equation}
```

### Essential Packages

```latex
\usepackage{amsmath}    % align, cases, matrices, etc.
\usepackage{amssymb}    % extra symbols (ℝ, ℤ, etc.)
\usepackage{mathtools}  % extends amsmath (dcases, coloneqq, etc.)
```

### Common Constructs

```latex
% Fractions
\frac{a}{b}          \dfrac{a}{b}  (display-size)

% Roots
\sqrt{x}             \sqrt[3]{x}

% Sub/superscripts
x_{i}   x^{2}   x_{i}^{2}   a_{i,j}

% Sums, products, integrals
\sum_{i=1}^{n} x_i      \prod_{i=1}^{n} x_i
\int_{0}^{\infty} f(x)\,dx
\lim_{x \to \infty} f(x)

% Brackets (auto-sized)
\left( \frac{a}{b} \right)
\left[ ... \right]
\left\{ ... \right\}
```

### Matrices

```latex
\begin{pmatrix} a & b \\ c & d \end{pmatrix}   % (a b; c d)
\begin{bmatrix} a & b \\ c & d \end{bmatrix}   % [a b; c d]
\begin{vmatrix} a & b \\ c & d \end{vmatrix}   % |a b; c d| (determinant)
\begin{Bmatrix} a & b \\ c & d \end{Bmatrix}   % {a b; c d}
```

### Aligned Equations

```latex
\begin{align}
  f(x) &= x^2 + 2x + 1 \label{eq:f} \\
  g(x) &= x^3 - 1       \label{eq:g}
\end{align}

% No numbering:
\begin{align*}
  a &= b + c \\
  d &= e + f
\end{align*}
```

### Cases

```latex
f(x) = \begin{cases}
  x^2  & \text{if } x \geq 0 \\
  -x^2 & \text{if } x < 0
\end{cases}
```

### Greek Letters

| Lower | Command | Upper | Command |
|-------|---------|-------|---------|
| α | `\alpha` | Α | `A` |
| β | `\beta` | Β | `B` |
| γ | `\gamma` | Γ | `\Gamma` |
| δ | `\delta` | Δ | `\Delta` |
| ε | `\epsilon`, `\varepsilon` | Ε | `E` |
| θ | `\theta` | Θ | `\Theta` |
| λ | `\lambda` | Λ | `\Lambda` |
| μ | `\mu` | — | — |
| π | `\pi` | Π | `\Pi` |
| σ | `\sigma` | Σ | `\Sigma` |
| φ | `\phi`, `\varphi` | Φ | `\Phi` |
| ω | `\omega` | Ω | `\Omega` |

### Common Math Symbols

| Symbol | Command | Symbol | Command |
|--------|---------|--------|---------|
| ≤ | `\leq` | ≥ | `\geq` |
| ≠ | `\neq` | ≈ | `\approx` |
| ± | `\pm` | × | `\times` |
| ÷ | `\div` | · | `\cdot` |
| ∈ | `\in` | ∉ | `\notin` |
| ⊂ | `\subset` | ⊆ | `\subseteq` |
| ∪ | `\cup` | ∩ | `\cap` |
| ∞ | `\infty` | ∂ | `\partial` |
| ∇ | `\nabla` | ∀ | `\forall` |
| ∃ | `\exists` | → | `\to`, `\rightarrow` |
| ⇒ | `\Rightarrow` | ⇔ | `\Leftrightarrow` |
| ℝ | `\mathbb{R}` | ℤ | `\mathbb{Z}` |
| … | `\dots`, `\ldots`, `\cdots` | | |

## 6. Tables

### Basic Table

```latex
\begin{table}[htbp]
  \centering
  \caption{Results summary}\label{tab:results}
  \begin{tabular}{lcrp{4cm}}
    \toprule
    Name & Count & Score & Description \\
    \midrule
    Alpha & 10 & 95.2 & First entry \\
    Beta  & 20 & 87.1 & Second entry \\
    \bottomrule
  \end{tabular}
\end{table}
```

### Column Specifiers

| Spec | Alignment |
|------|-----------|
| `l` | Left |
| `c` | Center |
| `r` | Right |
| `p{width}` | Paragraph (top-aligned, fixed width) |
| `m{width}` | Middle-aligned paragraph (requires `array`) |
| `|` | Vertical line (avoid — use `booktabs` instead) |

### Key Packages

```latex
\usepackage{booktabs}   % \toprule, \midrule, \bottomrule (professional rules)
\usepackage{multirow}   % \multirow{nrows}{width}{text}
\usepackage{longtable}  % tables spanning multiple pages
\usepackage{tabularx}   % auto-width X columns
```

### Multi-column/row

```latex
\multicolumn{3}{c}{Spanning header} \\
\multirow{2}{*}{Tall cell}
```

## 7. Figures and Images

```latex
\usepackage{graphicx}

\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{images/photo.png}
  \caption{A descriptive caption.}\label{fig:photo}
\end{figure}
```

### includegraphics Options

| Option | Example |
|--------|---------|
| `width` | `width=0.5\textwidth` |
| `height` | `height=5cm` |
| `scale` | `scale=0.75` |
| `angle` | `angle=90` |
| `trim` | `trim=1cm 2cm 1cm 2cm, clip` (left bottom right top) |

### Float Placement

| Specifier | Meaning |
|-----------|---------|
| `h` | Here (approximately) |
| `t` | Top of page |
| `b` | Bottom of page |
| `p` | Dedicated float page |
| `!` | Override internal limits |
| `H` | Exactly here (requires `float` package) |

### Subfigures

```latex
\usepackage{subcaption}

\begin{figure}[htbp]
  \centering
  \begin{subfigure}[b]{0.48\textwidth}
    \includegraphics[width=\textwidth]{img1.png}
    \caption{First}\label{fig:sub1}
  \end{subfigure}
  \hfill
  \begin{subfigure}[b]{0.48\textwidth}
    \includegraphics[width=\textwidth]{img2.png}
    \caption{Second}\label{fig:sub2}
  \end{subfigure}
  \caption{Both images}\label{fig:both}
\end{figure}
```

## 8. Bibliographies and Citations

### BibTeX Workflow

1. Create `references.bib`:
```bibtex
@article{smith2023,
  author  = {Smith, John and Doe, Jane},
  title   = {An Important Paper},
  journal = {Journal of Examples},
  year    = {2023},
  volume  = {42},
  pages   = {1--15},
  doi     = {10.1234/example}
}

@book{knuth1984,
  author    = {Knuth, Donald E.},
  title     = {The {\TeX}book},
  publisher = {Addison-Wesley},
  year      = {1984}
}
```

2. In document:
```latex
\usepackage{natbib}  % or use biblatex
\bibliographystyle{plainnat}

As shown by \citet{smith2023}...  % Smith and Doe (2023)
This is known \citep{smith2023}.  % (Smith and Doe, 2023)

\bibliography{references}
```

3. Compile: `pdflatex → bibtex → pdflatex → pdflatex`

### BibLaTeX Workflow (Modern)

```latex
\usepackage[backend=biber, style=authoryear]{biblatex}
\addbibresource{references.bib}

\textcite{smith2023}   % Smith and Doe (2023)
\parencite{smith2023}  % (Smith and Doe, 2023)

\printbibliography
```

Compile: `pdflatex → biber → pdflatex → pdflatex`

### natbib vs biblatex

| Feature | natbib | biblatex |
|---------|--------|----------|
| Backend | BibTeX | Biber (recommended) |
| Flexibility | Limited styles | Highly customizable |
| Unicode | Poor | Full support |
| Recommendation | Legacy projects | New projects |

## 9. Code Listings

### verbatim

```latex
\begin{verbatim}
def hello():
    print("Hello, world!")
\end{verbatim}

Inline: \verb|some_code()|
```

### listings Package

```latex
\usepackage{listings}
\usepackage{xcolor}

\lstdefinestyle{mystyle}{
  basicstyle=\ttfamily\small,
  keywordstyle=\color{blue},
  commentstyle=\color{gray},
  stringstyle=\color{red},
  numbers=left,
  numberstyle=\tiny,
  frame=single,
  breaklines=true
}

\begin{lstlisting}[language=Python, style=mystyle, caption={Example}]
def factorial(n):
    """Compute factorial."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)
\end{lstlisting}
```

### minted Package (Prettier, Requires Pygments)

```latex
\usepackage{minted}

\begin{minted}[linenos, frame=lines, fontsize=\small]{python}
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
\end{minted}
```

Compile with: `pdflatex -shell-escape document.tex`

## 10. Presentations (Beamer)

```latex
\documentclass{beamer}
\usetheme{Madrid}          % or: Berlin, Warsaw, Metropolis, etc.
\usecolortheme{default}    % or: beaver, crane, dolphin, etc.

\title{My Presentation}
\author{Author}
\date{\today}

\begin{document}

\begin{frame}
  \titlepage
\end{frame}

\begin{frame}{Outline}
  \tableofcontents
\end{frame}

\section{Introduction}
\begin{frame}{Introduction}
  \begin{itemize}
    \item<1-> First point (appears on slide 1+)
    \item<2-> Second point (appears on slide 2+)
    \item<3-> Third point
  \end{itemize}
\end{frame}

\begin{frame}{With Columns}
  \begin{columns}
    \begin{column}{0.5\textwidth}
      Left content
    \end{column}
    \begin{column}{0.5\textwidth}
      Right content
    \end{column}
  \end{columns}
\end{frame}

\end{document}
```

**Popular themes:** `Madrid`, `Berlin`, `Metropolis` (modern, clean), `Warsaw`, `CambridgeUS`

### Overlay Commands

| Command | Effect |
|---------|--------|
| `\pause` | Show content incrementally |
| `\onslide<2>{text}` | Show on slide 2 only |
| `\only<1>{text}` | Only on slide 1 (no space reserved) |
| `\visible<2->{text}` | Visible from slide 2 onward |
| `\alert<2>{text}` | Highlighted on slide 2 |

## 11. Page Layout

### Margins (geometry)

```latex
\usepackage[margin=2.5cm]{geometry}
% or:
\usepackage[top=3cm, bottom=3cm, left=2cm, right=2cm]{geometry}
```

### Headers and Footers (fancyhdr)

```latex
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}                          % clear all
\fancyhead[L]{Left Header}
\fancyhead[R]{\rightmark}          % current section
\fancyfoot[C]{\thepage}            % page number center
\renewcommand{\headrulewidth}{0.4pt}
```

### Page Numbering

```latex
\pagenumbering{roman}   % i, ii, iii (for front matter)
\pagenumbering{arabic}  % 1, 2, 3 (for main content)
\thispagestyle{empty}   % no number on this page
```

### Multi-Column

```latex
\usepackage{multicol}
\begin{multicols}{2}
  Content in two columns...
\end{multicols}
```

## 12. Common Packages Reference

| Package | Purpose |
|---------|---------|
| `amsmath` | Enhanced math environments |
| `amssymb` | Extra math symbols (ℝ, ℤ, etc.) |
| `mathtools` | Extensions to amsmath |
| `graphicx` | Image inclusion |
| `hyperref` | Clickable links, PDF metadata |
| `geometry` | Page margins and dimensions |
| `booktabs` | Professional table rules |
| `multirow` | Multi-row table cells |
| `longtable` | Multi-page tables |
| `tabularx` | Auto-width table columns |
| `xcolor` | Color support |
| `listings` | Code listings |
| `minted` | Syntax-highlighted code (needs Pygments) |
| `tikz` | Programmatic graphics and diagrams |
| `pgfplots` | Data plots (built on TikZ) |
| `fancyhdr` | Custom headers/footers |
| `setspace` | Line spacing |
| `enumitem` | Customize list environments |
| `subcaption` | Subfigures and subtables |
| `float` | Extra float control (`[H]` placement) |
| `babel` | Language/hyphenation support |
| `inputenc` | Input encoding (`utf8`) |
| `fontenc` | Font encoding (`T1`) |
| `microtype` | Microtypographic enhancements |
| `cleveref` | Smart cross-references (`\cref`) |
| `siunitx` | SI units and number formatting |
| `algorithm2e` | Algorithm pseudocode |
| `natbib` | Citation management |
| `biblatex` | Modern bibliography management |
| `csquotes` | Context-sensitive quotation marks |
| `url` | Typeset URLs |
| `caption` | Customize caption formatting |
| `appendix` | Appendix management |

**Load order tip:** Load `hyperref` last (or near-last). Exceptions: `cleveref` goes after `hyperref`.

## 13. Compilation

### Engines

| Engine | Use when |
|--------|----------|
| `pdflatex` | Default. Most compatible. ASCII/Latin input. |
| `xelatex` | System fonts (TTF/OTF), full Unicode |
| `lualatex` | System fonts + Lua scripting, full Unicode |

### Compilation Sequence

```bash
# Basic document
pdflatex document.tex

# With bibliography (BibTeX)
pdflatex document.tex
bibtex document
pdflatex document.tex
pdflatex document.tex

# With bibliography (Biber/BibLaTeX)
pdflatex document.tex
biber document
pdflatex document.tex
pdflatex document.tex

# Automated (recommended)
latexmk -pdf document.tex           # pdflatex
latexmk -xelatex document.tex       # xelatex
latexmk -lualatex document.tex      # lualatex
latexmk -pdf -pvc document.tex      # continuous preview
```

### Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Undefined control sequence` | Typo or missing package | Check spelling; add `\usepackage` |
| `Missing $ inserted` | Math symbol outside math mode | Wrap in `$...$` |
| `Missing \begin{document}` | Error in preamble | Check preamble for typos |
| `File not found` | Wrong path or missing file | Check filename/path, check extension |
| `Overfull \hbox` | Line too wide | Rephrase, add `\allowbreak`, or use `\sloppy` |
| `Undefined citation` | Missing bib entry or no bibtex run | Run bibtex/biber, check .bib keys |
| `Too many unprocessed floats` | Too many figures queued | Add `\clearpage` or use `[H]` |
| `Dimension too large` | Image scaling issue | Check `width`/`height` values |
| `Package clash` | Two packages conflict | Load one, check docs for compatibility |

### Reading Log Files

- Look at the `.log` file for full error context
- Errors show as `!` lines
- Warnings show as `LaTeX Warning:` or `Package xyz Warning:`
- `Rerun to get cross-references right` → compile again

## 14. Tips and Best Practices

1. **Multi-file projects:** Use `\input{chapters/intro}` (inserts inline) or `\include{chapters/intro}` (adds `\clearpage`, enables `\includeonly`)
2. **Custom preamble:** Move package loading to `preamble.sty` or `preamble.tex`, then `\input{preamble}`
3. **Label after caption:** `\caption{...}\label{fig:x}` — never the reverse
4. **Non-breaking spaces:** `Figure~\ref{fig:x}`, `Section~\ref{sec:y}` — prevents linebreak before number
5. **Draft mode:** `\documentclass[draft]{article}` — speeds compilation, shows overfull boxes
6. **Use `\centering` not `center`** inside floats (avoids extra vertical spacing)
7. **Avoid `\\` for paragraph breaks** — use blank lines instead
8. **Use `booktabs`** — never `\hline` and vertical lines for professional tables
9. **Use `microtype`** — improves typography with zero effort
10. **Use `cleveref`** — `\cref{fig:x}` auto-generates "Figure 1" text
11. **Version control:** LaTeX is plain text — use Git
12. **One sentence per line** — makes diffs cleaner in version control

## 15. Quick Reference

### Most Common Commands

| Task | Command |
|------|---------|
| Bold | `\textbf{text}` |
| Italic | `\textit{text}` |
| Monospace | `\texttt{text}` |
| Section | `\section{Title}` |
| Reference | `\ref{label}` |
| Citation | `\cite{key}` |
| Footnote | `\footnote{text}` |
| Image | `\includegraphics[width=\textwidth]{file}` |
| URL | `\url{https://...}` or `\href{url}{text}` |
| List item | `\item` |
| New page | `\newpage` or `\clearpage` |
| Comment | `% comment` |
| Math inline | `$E=mc^2$` |
| Math display | `\[ E=mc^2 \]` |
| Fraction | `\frac{a}{b}` |

### Math Operators

| Command | Symbol | Command | Symbol |
|---------|--------|---------|--------|
| `\sin` | sin | `\cos` | cos |
| `\tan` | tan | `\log` | log |
| `\ln` | ln | `\exp` | exp |
| `\min` | min | `\max` | max |
| `\lim` | lim | `\sum` | Σ |
| `\prod` | Π | `\int` | ∫ |

### Arrows

| Command | Symbol |
|---------|--------|
| `\rightarrow`, `\to` | → |
| `\leftarrow` | ← |
| `\leftrightarrow` | ↔ |
| `\Rightarrow` | ⇒ |
| `\Leftarrow` | ⇐ |
| `\Leftrightarrow` | ⇔ |
| `\mapsto` | ↦ |
| `\uparrow` | ↑ |
| `\downarrow` | ↓ |

## References

- [LaTeX Project Documentation](https://www.latex-project.org/help/documentation/)
- [Overleaf Learn](https://www.overleaf.com/learn)
- [CTAN — Comprehensive TeX Archive Network](https://ctan.org/)
- [LaTeX2e: An unofficial reference manual](https://latexref.xyz/)
- [Detexify — Draw a symbol, find the command](https://detexify.kiber.ch/)
