---
name: scientific-figure-pro
description: Generate publication-ready scientific figures in Python/matplotlib with a consistent figures4papers house style. Use when creating or refining academic bar/trend/heatmap/scatter/multi-panel figures, enforcing visual consistency, or exporting paper-ready PNG/PDF/SVG outputs.
---

# Scientific Figure Pro

Use this skill to create or revise publication figures with consistent aesthetics from the figures4papers project.

## Workflow

1. Identify the figure family (bar, trend, heatmap, scatter, multi-panel, conceptual illustration).
2. Load helper APIs from `scripts/scientific_figure_pro.py`.
3. Apply style first with `apply_publication_style(...)`.
4. Build the figure using `make_*` helpers.
5. Export with `finalize_figure(...)` to keep layout and output defaults consistent.

## Use The Helper Module

Load by file path when package imports are inconvenient:

```python
import importlib.util
from pathlib import Path
import matplotlib.pyplot as plt

module_path = Path("skills/scientific-figure-pro/scripts/scientific_figure_pro.py")
spec = importlib.util.spec_from_file_location("scientific_figure_pro", module_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
```

## Core APIs

- `FigureStyle(...)`: Configure typography and axis linewidth.
- `apply_publication_style(style=None)`: Apply global rcParams.
- `create_subplots(nrows, ncols, figsize, **kwargs)`: Create flattened axes.
- `make_grouped_bar(...)`: Build grouped bars with publication defaults.
- `make_trend(...)`: Build trend lines with optional confidence shadow.
- `make_heatmap(...)`: Build heatmaps with optional labels and annotations.
- `make_scatter(...)`: Build clean scatter plots.
- `make_sphere_illustration(...)`: Build conceptual shaded sphere panels.
- `finalize_figure(fig, out_path, formats=None, dpi=300, pad=0.05)`: Save outputs consistently.

## Style Policy

- Use Helvetica/Arial-like sans-serif families.
- Remove top/right spines.
- Keep legends frameless.
- Use semantic palette mapping:
  - blue for target/proposed method,
  - green for improvements,
  - red for contrasts/baselines,
  - neutral for support categories.
- Use `dpi=300` by default and `dpi=600` for dense bar panels.

## Practical Defaults

- Dense benchmark bars: `FigureStyle(font_size=24, axes_linewidth=3)` and wide canvas.
- Compact analysis charts: `FigureStyle(font_size=15 or 16, axes_linewidth=2)`.
- Finalize every figure through `finalize_figure(...)` instead of direct `plt.savefig(...)`.

## Dependencies

- Python 3.8+
- `matplotlib`
- `numpy`

## References

- Read `references/design_theory.md` when you need style rationale and reproduction rules.
