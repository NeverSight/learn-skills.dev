---
name: pgfplots
description: "LaTeX pgfplots package for data visualization and plotting. Use when helping users create line plots, bar charts, scatter plots, histograms, 3D surfaces, or any scientific/data plot in LaTeX."
---

# pgfplots — Data Visualization & Plotting

**CTAN:** https://ctan.org/pkg/pgfplots  
**Manual:** `texdoc pgfplots`

## Setup

```latex
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}  % ALWAYS set this — enables latest features

% Optional libraries
\usepgfplotslibrary{fillbetween, groupplots, statistics, colorbrewer, polar}
```

## Basic Plot

```latex
\begin{tikzpicture}
\begin{axis}[
  xlabel={$x$},
  ylabel={$f(x)$},
  title={My Plot},
  grid=major,
]
  \addplot[blue, thick, domain=-3:3, samples=100] {x^2};
  \addlegend{$x^2$}
\end{axis}
\end{tikzpicture}
```

## Axis Environments

| Environment | Description |
|-------------|-------------|
| `axis` | Standard linear axes |
| `semilogxaxis` | Log scale on x-axis |
| `semilogyaxis` | Log scale on y-axis |
| `loglogaxis` | Log scale on both axes |
| `polaraxis` | Polar coordinates (requires `polar` library) |

## Axis Options Reference

| Option | Example | Description |
|--------|---------|-------------|
| `xlabel` | `xlabel={Time (s)}` | X-axis label |
| `ylabel` | `ylabel={Voltage}` | Y-axis label |
| `title` | `title={Results}` | Plot title |
| `xmin/xmax` | `xmin=0, xmax=10` | Axis limits |
| `ymin/ymax` | `ymin=-1, ymax=1` | Axis limits |
| `domain` | `domain=0:2*pi` | Default plot domain |
| `samples` | `samples=200` | Default sample count |
| `grid` | `grid=major` | `major`, `minor`, `both`, `none` |
| `legend pos` | `legend pos=north west` | Legend placement |
| `width/height` | `width=10cm` | Axis dimensions |
| `axis lines` | `axis lines=middle` | `box`, `left`, `middle`, `none` |
| `enlargelimits` | `enlargelimits=0.1` | Pad axis range |
| `xtick` | `xtick={0,1,...,5}` | Custom tick positions |
| `xticklabels` | `xticklabels={A,B,C}` | Custom tick labels |
| `x tick label style` | `x tick label style={rotate=45}` | Tick label formatting |
| `legend style` | `legend style={at={(0.5,-0.2)}}` | Legend customization |
| `cycle list name` | `cycle list name=color list` | Color cycling |
| `scaled ticks` | `scaled ticks=false` | Disable tick scaling |
| `restrict y to domain` | `restrict y to domain=-10:10` | Clip extreme values |

## Plot Types & Examples

### Line Plot (from expression)

```latex
\begin{axis}[domain=0:2*pi, samples=100, grid=major,
  legend pos=south west]
  \addplot[blue, thick] {sin(deg(x))};
  \addplot[red, thick, dashed] {cos(deg(x))};
  \legend{$\sin(x)$, $\cos(x)$}
\end{axis}
```

### Line Plot (from data)

```latex
\begin{axis}[xlabel=Year, ylabel=Value]
  \addplot coordinates {
    (2018, 10) (2019, 15) (2020, 12) (2021, 20) (2022, 25)
  };
\end{axis}
```

### Scatter Plot

```latex
\begin{axis}[only marks, xlabel=$x$, ylabel=$y$]
  \addplot[mark=*, blue] coordinates {
    (1,2) (2,3.5) (3,2.8) (4,5.1) (5,4.2)
  };
  % Or with mark options:
  \addplot+[mark=o, mark size=3pt, red] coordinates { ... };
\end{axis}
```

### Bar Chart

```latex
\begin{axis}[
  ybar,                    % vertical bars (xbar for horizontal)
  symbolic x coords={A, B, C, D},
  xtick=data,
  ylabel={Count},
  nodes near coords,       % value labels on bars
  bar width=15pt,
]
  \addplot coordinates {(A,20) (B,35) (C,30) (D,15)};
  \addplot coordinates {(A,25) (B,20) (C,40) (D,10)};
  \legend{2022, 2023}
\end{axis}
```

### Stacked Bar

```latex
\begin{axis}[ybar stacked, symbolic x coords={Q1,Q2,Q3,Q4}, xtick=data]
  \addplot coordinates {(Q1,10) (Q2,15) (Q3,12) (Q4,18)};
  \addplot coordinates {(Q1,8)  (Q2,10) (Q3,15) (Q4,12)};
  \legend{Product A, Product B}
\end{axis}
```

### Histogram

```latex
\usepgfplotslibrary{statistics}

\begin{axis}[ybar interval, ylabel=Frequency, xlabel=Value]
  \addplot+[hist={bins=10, data min=0, data max=100}]
    table[y index=0] {data.csv};
\end{axis}
```

### Box Plot

```latex
\usepgfplotslibrary{statistics}

\begin{axis}[boxplot/draw direction=y]
  \addplot[boxplot prepared={
    lower whisker=2, lower quartile=4,
    median=6, upper quartile=8, upper whisker=10
  }] coordinates {};
\end{axis}
```

### Area / Fill Between

```latex
\usepgfplotslibrary{fillbetween}

\begin{axis}
  \addplot[name path=upper, blue, thick, domain=0:4] {x^2};
  \addplot[name path=lower, red, thick, domain=0:4] {x};
  \addplot[fill=blue!10] fill between[of=upper and lower, soft clip={domain=1:3}];
\end{axis}
```

### Error Bars

```latex
\begin{axis}
  \addplot+[error bars/.cd, y dir=both, y explicit]
    coordinates {
      (1, 2) +- (0, 0.5)
      (2, 4) +- (0, 0.8)
      (3, 3) +- (0, 0.3)
    };
\end{axis}
```

### 3D Surface

```latex
\begin{axis}[view={45}{30}, xlabel=$x$, ylabel=$y$, zlabel=$z$,
  colormap/viridis]
  \addplot3[surf, domain=-2:2, domain y=-2:2, samples=25]
    {exp(-x^2 - y^2)};
\end{axis}
```

### 3D Mesh

```latex
\begin{axis}[view={60}{30}]
  \addplot3[mesh, domain=-2:2, domain y=-2:2, samples=20]
    {sin(deg(x)) * cos(deg(y))};
\end{axis}
```

### Contour

```latex
\begin{axis}[view={0}{90}]  % top-down view
  \addplot3[contour filled, domain=-2:2, domain y=-2:2, samples=30]
    {exp(-x^2 - y^2)};
\end{axis}
```

### Parametric Plot

```latex
\begin{axis}[axis equal]
  \addplot[domain=0:360, samples=100, thick, blue]
    ({cos(x)}, {sin(x)});  % circle
\end{axis}
```

### Polar Plot

```latex
\usepgfplotslibrary{polar}

\begin{polaraxis}
  \addplot[domain=0:360, samples=100, thick]
    {1 + cos(x)};  % cardioid
\end{polaraxis}
```

## Data from Files

```latex
% CSV file: data.csv
% x, y
% 1, 2.3
% 2, 4.1
% ...

\begin{axis}
  \addplot table[col sep=comma, x=x, y=y] {data.csv};
  
  % TSV (default separator is space/tab)
  \addplot table[x index=0, y index=1] {data.tsv};
  
  % With expression on column
  \addplot table[x=time, y expr=\thisrow{value}*100] {data.csv};
\end{axis}
```

## Color Maps

```latex
% Built-in colormaps
colormap/hot, colormap/cool, colormap/viridis,
colormap/bluered, colormap/greenyellow, colormap/jet

% Custom
\pgfplotsset{
  colormap={mymap}{rgb255(0cm)=(0,0,180); rgb255(1cm)=(0,180,0); rgb255(2cm)=(180,0,0)}
}

% Colorbar
\begin{axis}[colorbar, colormap/viridis]
```

## Multiple Axes

```latex
\begin{tikzpicture}
\begin{axis}[
  axis y line*=left, xlabel=Time, ylabel=Temperature,
  ymin=0, ymax=100,
]
  \addplot[blue, thick] coordinates {(1,20)(2,40)(3,60)(4,80)};
  \label{plot:temp}
\end{axis}

\begin{axis}[
  axis y line*=right, axis x line=none,
  ylabel=Pressure, ymin=0, ymax=10,
]
  \addplot[red, thick, dashed] coordinates {(1,2)(2,5)(3,3)(4,8)};
  \label{plot:press}
\end{axis}
\end{tikzpicture}
```

## Group Plots

```latex
\usepgfplotslibrary{groupplots}

\begin{tikzpicture}
\begin{groupplot}[
  group style={group size=2 by 2, horizontal sep=1.5cm, vertical sep=1.5cm},
  width=6cm, height=5cm,
]
  \nextgroupplot[title=Plot 1]
    \addplot {x};
  \nextgroupplot[title=Plot 2]
    \addplot {x^2};
  \nextgroupplot[title=Plot 3]
    \addplot {sqrt(x)};
  \nextgroupplot[title=Plot 4]
    \addplot {ln(x)};
\end{groupplot}
\end{tikzpicture}
```

## Annotations

```latex
\begin{axis}
  \addplot[blue, thick, domain=0:5] {x^2};
  
  % Pin annotation
  \node[pin=60:{Maximum}] at (axis cs:4, 16) {};
  
  % Arrow annotation
  \draw[->, thick] (axis cs:2, 10) -- (axis cs:3, 9)
    node[above, pos=0] {Note};
  
  % Vertical line
  \draw[dashed, gray] (axis cs:2.5, 0) -- (axis cs:2.5, 25);
  
  % Horizontal band
  \draw[fill=red!10, draw=none] (axis cs:0,5) rectangle (axis cs:5,10);
  
  % Text node
  \node at (axis cs:1, 20) {$f(x) = x^2$};
\end{axis}
```

## Mark Options

| Mark | Description |
|------|-------------|
| `*` | Filled circle |
| `o` | Open circle |
| `square*` | Filled square |
| `square` | Open square |
| `triangle*` | Filled triangle |
| `diamond*` | Filled diamond |
| `x` | Cross |
| `+` | Plus |
| `star` | Star |
| `none` | No marks |

```latex
\addplot+[mark=triangle*, mark size=3pt, mark options={fill=red}] ...;
```

## Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| "Dimension too large" | Large values or domain | Use `restrict y to domain`, check domain |
| Missing `compat` warning | No `\pgfplotsset{compat=..}` | Add `\pgfplotsset{compat=1.18}` |
| Trig functions wrong | pgfplots uses degrees | Use `sin(deg(x))` for radians input |
| Bars overlapping | Multiple bar plots without grouping | Use `ybar` with `bar shift` or legend |
| Legend in wrong spot | Default position | Set `legend pos=north west` etc. |
| 3D plot too slow | Too many samples | Reduce `samples` for 3D |
| Axis labels cut off | Tight bounding box | Use `trim axis left/right` or increase margins |
| Fill between fails | Paths not named | Add `name path=A` to each plot |
| CSV column error | Wrong separator | Set `col sep=comma` for CSV files |
| `\addlegendentry` order | Must follow its `\addplot` | Put legend entry right after its plot |
