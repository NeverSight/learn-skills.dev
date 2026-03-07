---
name: plotext-financial-chart
description: ASCII financial line charts for markdown using plotext dot marker. TRIGGERS - financial chart, line chart, plotext, price chart, trading chart, ASCII chart.
allowed-tools: Read, Bash, Write, Edit
---

# Plotext Financial Chart Skill

Create ASCII financial line charts for GitHub Flavored Markdown using plotext with dot marker (`•`). Pure text output — renders correctly on GitHub, terminals, and all monospace environments.

**Analogy**: `graph-easy` is for flowcharts. `plotext` with dot marker is for financial line charts.

## When to Use This Skill

- Adding price path / line chart diagrams to markdown documentation
- Visualizing trading concepts (barriers, thresholds, entry/exit levels)
- Any GFM markdown file needing financial data visualization
- User mentions "financial chart", "line chart", "price chart", "plotext", or "trading chart"

**NOT for**: Flowcharts or architecture diagrams — use `graph-easy` for those.

## Preflight Check

### All-in-One Preflight Script

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
python3 --version &>/dev/null || { echo "ERROR: Python 3 not found"; exit 1; }
if command -v uv &>/dev/null; then PM="uv pip"
elif command -v pip3 &>/dev/null; then PM="pip3"
else echo "ERROR: Neither uv nor pip3 found"; exit 1; fi
python3 -c "import plotext" 2>/dev/null || { echo "Installing plotext via $PM..."; $PM install plotext; }
python3 -c "
import plotext as plt, re
plt.clear_figure()
plt.plot([1,2,3], [1,2,3], marker='dot')
plt.plotsize(20, 5)
plt.theme('clear')
output = re.sub(r'\x1b\[[0-9;]*m', '', plt.build())
assert '•' in output
" && echo "✓ plotext ready (dot marker verified)"
PREFLIGHT_EOF
```

## Quick Start

```python
import re
import plotext as plt

x = list(range(20))
y = [97, 98, 100, 101, 100, 98, 100, 101, 102, 101,
     100, 98, 100, 101, 102, 103, 102, 101, 100, 100]

plt.clear_figure()
plt.plot(x, y, marker="dot", label="Price path")
plt.hline(103)    # Upper barrier
plt.hline(97)     # Lower barrier
plt.hline(100)    # Entry price
plt.title("Triple Barrier Method")
plt.xlabel("Time (bars)")
plt.ylabel("Price")
plt.plotsize(65, 22)
plt.theme("clear")
print(re.sub(r'\x1b\[[0-9;]*m', '', plt.build()))
```

## Mandatory Settings

Every chart MUST use these settings:

| Setting         | Code                        | Why                          |
| --------------- | --------------------------- | ---------------------------- |
| Reset state     | `plt.clear_figure()`        | Prevent stale data           |
| Dot marker      | `marker="dot"`              | GitHub-safe alignment        |
| No color        | `plt.theme("clear")`        | Clean text output            |
| Strip ANSI      | `re.sub(r'\x1b\[…', '', …)` | Remove residual escape codes |
| Build as string | `plt.build()`               | Not `plt.show()`             |

## Marker Reference

| Marker      | GitHub Safe | Use When                       |
| ----------- | ----------- | ------------------------------ |
| `"dot"`     | Yes         | **Default — always use**       |
| `"hd"`      | Yes         | Terminal-only, need smoothness |
| `"braille"` | No          | Never for markdown             |
| `"fhd"`     | No          | Never — Unicode 13.0+ only     |

## Rendering Command

```bash
/usr/bin/env bash << 'RENDER_EOF'
python3 << 'CHART_EOF'
import re
import plotext as plt

x = list(range(20))
y = [97, 98, 100, 101, 100, 98, 100, 101, 102, 101,
     100, 98, 100, 101, 102, 103, 102, 101, 100, 100]

plt.clear_figure()
plt.plot(x, y, marker="dot", label="Price path")
plt.hline(103)
plt.hline(97)
plt.hline(100)
plt.title("Triple Barrier Method")
plt.xlabel("Time (bars)")
plt.ylabel("Price")
plt.plotsize(65, 22)
plt.theme("clear")
print(re.sub(r'\x1b\[[0-9;]*m', '', plt.build()))
CHART_EOF
RENDER_EOF
```

## Embedding in Markdown (MANDATORY: Source Adjacent to Chart)

Every chart MUST be **immediately followed** by a `<details>` block with Python source. Explanatory text goes **after** the `<details>` block, never between chart and source.

```
✅ CORRECT: Chart → <details> → Explanatory text
❌ WRONG:   Chart → Explanatory text → <details>
```

See [./references/api-and-patterns.md](./references/api-and-patterns.md) for full embedding template.

## Mandatory Checklist

- [ ] `plt.clear_figure()` — Reset state
- [ ] `marker="dot"` — Dot marker for GitHub
- [ ] `plt.theme("clear")` + `re.sub()` strip — No ANSI codes
- [ ] `plt.title("...")` — Every chart needs a title
- [ ] `plt.xlabel` / `plt.ylabel` — Axis labels
- [ ] `plt.plotsize(65, 22)` — Fits 80-col code blocks
- [ ] `<details>` block **immediately after** chart (before any explanatory text)

## Troubleshooting

| Issue                 | Cause               | Solution                                      |
| --------------------- | ------------------- | --------------------------------------------- |
| ANSI codes in output  | Missing theme/strip | Add `plt.theme("clear")` and `re.sub()` strip |
| Misaligned on GitHub  | Wrong marker type   | Use `marker="dot"`, never braille/fhd         |
| Chart too wide        | plotsize too large  | Use `plt.plotsize(65, 22)` for 80-col blocks  |
| No diagonal slopes    | Too few data points | Use 15+ data points for visible slopes        |
| `ModuleNotFoundError` | Not installed       | Run preflight check                           |
| Empty output          | Missing `build()`   | Use `plt.build()` not `plt.show()`            |

## Resources

- [plotext GitHub](https://github.com/piccolomo/plotext)
- [Full API, patterns, and embedding guide](./references/api-and-patterns.md)
- [Tool selection rationale](./references/tool-selection.md)
