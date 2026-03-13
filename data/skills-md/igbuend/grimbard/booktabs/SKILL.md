---
name: booktabs
description: "LaTeX booktabs/tabularx/multirow/longtable packages for professional tables. Use when helping users create well-formatted tables, multi-page tables, or improve table appearance."
---

# booktabs + tabularx + multirow + longtable — Professional Tables

**CTAN:** https://ctan.org/pkg/booktabs | https://ctan.org/pkg/tabularx  
**Manual:** `texdoc booktabs`

## Setup

```latex
\usepackage{booktabs}    % professional horizontal rules
\usepackage{tabularx}    % auto-width columns
\usepackage{multirow}    % cells spanning rows
\usepackage{longtable}   % multi-page tables
\usepackage{colortbl}    % colored rows/cells (optional)
\usepackage{siunitx}     % number alignment (optional)
```

## Ugly vs Professional — Before/After

### ❌ Bad Table

```latex
\begin{tabular}{|l|c|r|}
\hline
Name & Score & Grade \\ \hline
Alice & 95 & A \\ \hline
Bob & 82 & B \\ \hline
Carol & 78 & C \\ \hline
\end{tabular}
```

### ✅ Good Table

```latex
\begin{tabular}{lcc}
\toprule
Name  & Score & Grade \\
\midrule
Alice & 95    & A \\
Bob   & 82    & B \\
Carol & 78    & C \\
\bottomrule
\end{tabular}
```

**Rules:** Never use vertical lines. Never use `\hline`. Use `\toprule`, `\midrule`, `\bottomrule`.

## booktabs Rules

| Command | Use |
|---------|-----|
| `\toprule` | Top of table (thicker) |
| `\midrule` | Between header and body |
| `\bottomrule` | Bottom of table (thicker) |
| `\cmidrule(lr){2-4}` | Partial rule spanning columns 2–4 |
| `\addlinespace` | Extra vertical space (group separator) |
| `\addlinespace[5pt]` | Custom extra space |

### cmidrule Trimming

```latex
\cmidrule(l){1-2}   % trim left
\cmidrule(r){3-4}   % trim right
\cmidrule(lr){2-3}  % trim both
\cmidrule{1-4}      % no trim
```

### Grouped Rows Example

```latex
\begin{tabular}{llr}
\toprule
Category & Item   & Price \\
\midrule
Fruit    & Apple  & 1.20 \\
         & Banana & 0.80 \\
\addlinespace
Dairy    & Milk   & 2.50 \\
         & Cheese & 4.00 \\
\bottomrule
\end{tabular}
```

## tabularx — Auto-Width Columns

```latex
% X columns expand to fill \textwidth
\begin{tabularx}{\textwidth}{lXr}
\toprule
ID & Description & Price \\
\midrule
1  & A very long description that will wrap automatically & \$10 \\
2  & Short & \$20 \\
\bottomrule
\end{tabularx}
```

| Column type | Behavior |
|-------------|----------|
| `l`, `c`, `r` | Fixed (natural width) |
| `X` | Expands to fill remaining space (left-aligned) |
| `>{\centering\arraybackslash}X` | Centered X column |
| `>{\raggedleft\arraybackslash}X` | Right-aligned X column |
| `p{3cm}` | Paragraph, fixed width |

## multirow

```latex
\usepackage{multirow}

\begin{tabular}{lcr}
\toprule
\multirow{2}{*}{Name} & \multicolumn{2}{c}{Scores} \\
\cmidrule(l){2-3}
 & Math & English \\
\midrule
Alice & 95 & 88 \\
Bob   & 72 & 91 \\
\bottomrule
\end{tabular}
```

Syntax: `\multirow{nrows}{width}{content}` — use `*` for auto width.

`\multicolumn{ncols}{alignment}{content}` — built into LaTeX.

### Complex Header Example

```latex
\begin{tabular}{lcccccc}
\toprule
& \multicolumn{3}{c}{Treatment A} & \multicolumn{3}{c}{Treatment B} \\
\cmidrule(lr){2-4} \cmidrule(lr){5-7}
Subject & Pre & Post & $\Delta$ & Pre & Post & $\Delta$ \\
\midrule
1 & 5.2 & 3.1 & $-2.1$ & 4.8 & 4.5 & $-0.3$ \\
2 & 6.1 & 2.8 & $-3.3$ & 5.5 & 5.2 & $-0.3$ \\
\bottomrule
\end{tabular}
```

## longtable — Multi-Page Tables

```latex
\usepackage{longtable}

\begin{longtable}{lcc}
% Header for first page
\toprule
Name & Value & Unit \\
\midrule
\endfirsthead

% Header for continuation pages
\multicolumn{3}{l}{\textit{Continued from previous page}} \\
\toprule
Name & Value & Unit \\
\midrule
\endhead

% Footer for all pages except last
\midrule
\multicolumn{3}{r}{\textit{Continued on next page}} \\
\endfoot

% Footer for last page
\bottomrule
\endlastfoot

% Data rows
Alpha   & 1.0 & m \\
Beta    & 2.5 & kg \\
% ... many more rows ...
Omega   & 9.9 & s \\

\caption{Long experimental data.}
\label{tab:longdata}
\end{longtable}
```

**Note:** `longtable` replaces `tabular` entirely (not inside `table` environment). Caption and label go inside.

## colortbl — Row and Cell Coloring

```latex
\usepackage{colortbl}
\usepackage[table]{xcolor}  % or load xcolor with table option

% Colored row
\rowcolor{blue!10}
Alice & 95 & A \\

% Colored cell
Alice & \cellcolor{green!20} 95 & A \\

% Alternating row colors (xcolor table option)
\rowcolors{2}{gray!10}{white}  % start at row 2, alternate
\begin{tabular}{lcc}
\toprule
\rowcolor{white}  % override for header
Name & Score & Grade \\
\midrule
Alice & 95 & A \\  % gray
Bob & 82 & B \\    % white
Carol & 78 & C \\  % gray
\bottomrule
\end{tabular}
```

## siunitx S Columns — Number Alignment

```latex
\usepackage{siunitx}

\begin{tabular}{l S[table-format=3.2] S[table-format=1.3]}
\toprule
{Material} & {Density} & {Error} \\
\midrule
Steel      & 785.00    & 0.050 \\
Aluminum   & 270.00    & 0.120 \\
Titanium   & 450.00    & 0.008 \\
Gold       & 1932.00   & 0.300 \\
\bottomrule
\end{tabular}
```

**S column:** Aligns numbers by decimal point. Wrap text headers in `{...}`.

| S option | Example | Meaning |
|----------|---------|---------|
| `table-format` | `3.2` | 3 digits . 2 decimals |
| `table-format` | `+2.1e3` | sign, digits, exponent |
| `round-mode` | `places` | Round to decimal places |
| `round-precision` | `2` | Number of decimal places |

## Full Example — Publication-Quality Table

```latex
\begin{table}[htbp]
  \centering
  \caption{Performance comparison of algorithms.}
  \label{tab:comparison}
  \begin{tabular}{l S[table-format=2.1] S[table-format=3.0] c}
    \toprule
    {Method} & {Accuracy (\%)} & {Time (ms)} & {Converged?} \\
    \midrule
    Baseline   & 72.3 & 150 & Yes \\
    Improved   & 85.1 & 230 & Yes \\
    Proposed   & 91.7 &  98 & Yes \\
    \addlinespace
    Oracle     & 99.2 &  45 & N/A \\
    \bottomrule
  \end{tabular}
\end{table}
```

## Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| Vertical lines | Using `|` in column spec | Remove them — use whitespace |
| `\hline` | Old habit | Use `\toprule/\midrule/\bottomrule` |
| Table too wide | Too many columns | Use `tabularx` with `X` columns, or `\resizebox` |
| `longtable` in `table` | Incompatible | `longtable` replaces `table` environment |
| `\multirow` misaligned | Row height differences | Add `\rule{0pt}{2.5ex}` or adjust manually |
| `S` column header error | Text in S column | Wrap header in `{...}` |
| Footnotes in table | `\footnote` fails in tabular | Use `\tablefootnote` (tablefootnote pkg) or threeparttable |
| `booktabs` + `colortbl` gaps | Rules have gaps with color | Add `\abovetopsep=0pt` or use `\arrayrulecolor` |

## Tips

- **Three rules only:** `\toprule`, `\midrule`, `\bottomrule` — almost never need more
- Use `\addlinespace` to group rows visually instead of extra rules
- Put `\caption` above the table (convention for tables, unlike figures)
- `\small` or `\footnotesize` before tabular to shrink wide tables
- `threeparttable` package for proper table footnotes
- `\arraystretch` to adjust row height: `\renewcommand{\arraystretch}{1.2}`
