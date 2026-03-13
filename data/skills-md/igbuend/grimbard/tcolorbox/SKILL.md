---
name: tcolorbox
description: "LaTeX tcolorbox package for colored and framed boxes. Use when helping users create theorem boxes, callouts, code listings in boxes, definition boxes, or any styled framed content."
---

# tcolorbox — Colored & Framed Boxes

**CTAN:** https://ctan.org/pkg/tcolorbox  
**Manual:** `texdoc tcolorbox` (~500 pages)

## Setup

```latex
\usepackage[most]{tcolorbox}
% 'most' loads: skins, breakable, listings, theorems, fitting, hooks, xparse
% For minimal: \usepackage{tcolorbox} then \tcbuselibrary{...}

\tcbuselibrary{skins}       % enhanced appearance
\tcbuselibrary{breakable}   % boxes across pages
\tcbuselibrary{theorems}    % theorem integration
\tcbuselibrary{listings}    % code listings in boxes
\tcbuselibrary{listingsutf8} % UTF-8 code listings
```

## Basic Usage

```latex
\begin{tcolorbox}
  This is a simple colored box.
\end{tcolorbox}

\begin{tcolorbox}[colback=blue!5, colframe=blue!75!black, title=My Title]
  A box with title and custom colors.
\end{tcolorbox}
```

## Common Options

| Option | Default | Description |
|--------|---------|-------------|
| `colback` | `black!5!white` | Background color |
| `colframe` | `black!75!white` | Frame color |
| `coltitle` | `white` | Title text color |
| `colbacktitle` | (from `colframe`) | Title background |
| `coltext` | `black` | Body text color |
| `title` | (none) | Box title |
| `fonttitle` | | Title font (`\bfseries\large`) |
| `fontupper` | | Upper (main) body font |
| `fontlower` | | Lower part font |
| `arc` | `1mm` | Corner radius |
| `boxrule` | `0.5mm` | Frame thickness |
| `leftrule` | (from boxrule) | Left rule only |
| `toprule` | (from boxrule) | Top rule only |
| `width` | `\linewidth` | Box width |
| `left` | `4mm` | Left padding |
| `right` | `4mm` | Right padding |
| `top` | `2mm` | Top padding |
| `bottom` | `2mm` | Bottom padding |
| `boxsep` | `1mm` | All-sides padding |
| `sharp corners` | | Remove rounding |
| `rounded corners` | ✅ | Default |
| `halign` | `justify` | `left`, `center`, `right`, `justify` |
| `valign` | `top` | `top`, `center`, `bottom` |

## Box Styles

### Titled Box

```latex
\begin{tcolorbox}[
  colback=yellow!10,
  colframe=yellow!50!black,
  title=Warning,
  fonttitle=\bfseries,
  coltitle=black,
]
  Be careful with this operation.
\end{tcolorbox}
```

### Left Bar (callout style)

```latex
\begin{tcolorbox}[
  enhanced,
  colback=blue!5,
  colframe=blue!5,       % hide frame
  borderline west={3pt}{0pt}{blue!70},
  sharp corners,
  boxrule=0pt,
]
  \textbf{Note:} This is a callout-style box.
\end{tcolorbox}
```

### Minimalist

```latex
\begin{tcolorbox}[
  enhanced,
  colback=gray!5,
  colframe=gray!5,
  boxrule=0pt,
  arc=0pt,
  left=10pt,
]
  Clean, simple box.
\end{tcolorbox}
```

### Upper/Lower Parts

```latex
\begin{tcolorbox}[
  colback=white,
  colframe=blue!50!black,
  title=Theorem,
]
  $a^2 + b^2 = c^2$
  \tcblower
  This is the proof part (lower section).
\end{tcolorbox>
```

## Breakable Boxes (Multi-Page)

```latex
\tcbuselibrary{breakable}

\begin{tcolorbox}[breakable, colback=white, colframe=blue!50!black]
  Very long content that may span multiple pages...
  % The box will automatically break at page boundaries
\end{tcolorbox}

% Enhanced breakable (better visuals)
\begin{tcolorbox}[enhanced jigsaw, breakable, colback=white, colframe=blue!50!black]
  Long content...
\end{tcolorbox}
```

## Theorem Boxes

```latex
\tcbuselibrary{theorems}

% Define theorem types
\newtcbtheorem[number within=section]{theorem}{Theorem}{
  colback=blue!5,
  colframe=blue!50!black,
  fonttitle=\bfseries,
}{thm}

\newtcbtheorem[number within=section]{definition}{Definition}{
  colback=green!5,
  colframe=green!50!black,
  fonttitle=\bfseries,
}{def}

\newtcbtheorem[number within=section]{example}{Example}{
  colback=yellow!5,
  colframe=yellow!50!black,
  fonttitle=\bfseries,
}{ex}

\newtcbtheorem[number within=section]{proposition}{Proposition}{
  colback=red!5,
  colframe=red!50!black,
  fonttitle=\bfseries,
}{prop}

% Usage — two arguments: title and label
\begin{theorem}{Pythagoras}{pythagoras}
  For a right triangle with legs $a$, $b$ and hypotenuse $c$:
  \[ a^2 + b^2 = c^2 \]
\end{theorem}

\begin{definition}{Group}{group}
  A \emph{group} is a set $G$ with a binary operation...
\end{definition}

% Reference: Theorem~\ref{thm:pythagoras}
```

### Theorem with Proof Below

```latex
\newtcbtheorem{mythm}{Theorem}{
  colback=blue!5,
  colframe=blue!50!black,
  fonttitle=\bfseries,
  separator sign={\ ---},
  description delimiters parenthesis,
}{thm}

\begin{mythm}{Fundamental Theorem}{fundamental}
  Every continuous function on $[a,b]$ is integrable.
  \tcblower
  \textit{Proof.} By construction... $\square$
\end{mythm}
```

## Code Boxes (Listings)

```latex
\tcbuselibrary{listings}
% or \tcbuselibrary{listingsutf8} for UTF-8

% Inline listing box
\begin{tcblisting}{
  colback=gray!5,
  colframe=gray!75!black,
  listing only,        % show only code (not rendered)
  title=Python Example,
  listing options={language=Python, basicstyle=\ttfamily\small},
}
def hello():
    print("Hello, world!")
\end{tcblisting}

% Side-by-side: code + output
\begin{tcblisting}{
  colback=white,
  colframe=blue!50!black,
  listing side text,   % code left, text right
  title=LaTeX Example,
}
$\int_0^1 x^2\, dx = \frac{1}{3}$
\end{tcblisting}
```

### Code Box Style

```latex
\newtcblisting{codebox}[2][]{
  colback=gray!5,
  colframe=gray!80!black,
  title=#2,
  fonttitle=\bfseries\ttfamily,
  listing only,
  listing options={
    basicstyle=\ttfamily\small,
    keywordstyle=\color{blue},
    commentstyle=\color{green!60!black},
    stringstyle=\color{red!70!black},
    #1
  },
}

% Usage
\begin{codebox}[language=Python]{my\_script.py}
import numpy as np
x = np.linspace(0, 1, 100)
\end{codebox}
```

### Using minted Instead of listings

```latex
\tcbuselibrary{minted}

\begin{tcblisting}{
  listing engine=minted,
  minted language=python,
  minted style=monokai,
  colback=gray!10,
  listing only,
}
def hello():
    print("Hello!")
\end{tcblisting}
```

## Skins

```latex
\tcbuselibrary{skins}

% Enhanced (required for many visual features)
\begin{tcolorbox}[enhanced, ...]

% Bicolor (different upper/lower colors)
\begin{tcolorbox}[bicolor, colback=blue!10, colbacklower=green!10, ...]

% Beamer style
\begin{tcolorbox}[beamer, colback=blue!10, colframe=blue!50!black]

% Watermark
\begin{tcolorbox}[enhanced, watermark text=DRAFT, watermark color=red!20]
```

## Custom Box Definitions

```latex
% Simple named box
\newtcolorbox{important}{
  colback=red!5,
  colframe=red!50!black,
  fonttitle=\bfseries,
  title=Important,
}

% Box with parameter
\newtcolorbox{mybox}[1]{
  colback=blue!5,
  colframe=blue!50!black,
  title=#1,
  fonttitle=\bfseries,
}

% Box with optional + required args
\newtcolorbox{notebox}[2][]{
  enhanced,
  colback=yellow!10,
  colframe=yellow!50!black,
  title=#2,
  #1,  % optional overrides
}

% Usage
\begin{important}
  Don't forget this!
\end{important}

\begin{mybox}{Title Here}
  Content.
\end{mybox}

\begin{notebox}[colback=red!10]{Warning}
  Override the background.
\end{notebox}
```

## Complete Example: Lecture Notes Setup

```latex
\usepackage[most]{tcolorbox}

\newtcbtheorem[number within=section]{theorem}{Theorem}{
  enhanced, breakable,
  colback=blue!3, colframe=blue!50!black,
  fonttitle=\bfseries,
  separator sign={.},
}{thm}

\newtcbtheorem[number within=section]{definition}{Definition}{
  enhanced, breakable,
  colback=green!3, colframe=green!50!black,
  fonttitle=\bfseries,
}{def}

\newtcbtheorem[number within=section]{example}{Example}{
  enhanced, breakable,
  colback=yellow!5, colframe=yellow!50!black,
  fonttitle=\bfseries,
}{ex}

\newtcolorbox{remark}{
  enhanced,
  colback=gray!5, colframe=gray!5,
  borderline west={3pt}{0pt}{gray!50},
  sharp corners, boxrule=0pt,
}

\newtcolorbox{warning}{
  enhanced,
  colback=red!5, colframe=red!50!black,
  fonttitle=\bfseries, title=Warning,
}
```

## Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| Box doesn't break across pages | Missing `breakable` | Add `breakable` option |
| Visual artifacts when breaking | Standard skin + breakable | Use `enhanced jigsaw` + `breakable` |
| `enhanced` features not working | Forgot `skins` library | Use `\tcbuselibrary{skins}` or `[most]` |
| Theorem numbering wrong | Wrong counter | Check `number within` option |
| Listing encoding errors | UTF-8 in code | Use `listingsutf8` library |
| Overfull boxes | Box wider than margins | Set `width=\linewidth` explicitly |
| Colors too bright | Full saturation | Use `color!intensity` like `blue!50!black` |
| `\newtcbtheorem` needs 2 args | Forgot label | `\begin{thm}{Title}{label}` — both required |
| tcolorbox + hyperref conflict | Load order | Load tcolorbox after hyperref |

## Tips

- Use `[most]` when loading to get all common libraries
- `enhanced` skin is needed for `borderline`, `watermark`, `shadow`, etc.
- Combine `breakable` + `enhanced jigsaw` for clean page breaks
- Mix `\newtcbtheorem` with `\newtcolorbox` — theorems for numbered, plain boxes for unnumbered
- Use `\tcbset{...}` for global defaults across all boxes
- Colors: mix with black for professional look: `blue!50!black` not `blue`
