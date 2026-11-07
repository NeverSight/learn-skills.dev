---
name: axiom-metrics-chart
description: Render saved Axiom metrics v2 or v3 JSON as line charts in a terminal or transcript. Uses Unicode/ASCII by default and supports PNG/SVG/sixel with gnuplot. Use when plotting metrics query results.
---

# axiom-metrics-chart

Turns a metrics query response into a **multi-series line chart**.

Input is a saved `{metadata, series}` response in metrics v2 or v3 format. For MCP results, call `queryMetrics` with `truncate: false` and save its `structuredContent` as the input JSON. The default CSV preview can omit series and samples.

## TL;DR

```bash
# From a file, stdout picks the best renderer for your terminal:
python3 scripts/metrics_chart.py response.json

# Read the same saved response from stdin:
python3 scripts/metrics_chart.py < response.json

# Force a zero-dependency ASCII chart (always works, anywhere):
python3 scripts/metrics_chart.py --format ascii response.json
```

> **Aggregate first.** Charts are only readable with a *handful* of series.
> The cleanest result comes from a query that already groups/aggregates to a few
> lines (e.g. `group by status` rather than per-`pod`). This skill's series
> reduction (below) is a safety net for high-cardinality results, **not** a
> substitute for aggregating in the query.

## Input format (metrics v2/v3)

```json
{
  "metadata": {
    "group_keys": ["code", "method"],
    "warnings": [],
    "unit": "ms",
    "custom_unit": "millisec"
  },
  "series": [
    {
      "metric": "http_requests",
      "tags": { "code": 200, "method": "GET", "path": "/" },
      "start": 1750753164,
      "resolution": 60,
      "data": [420.0, 42.0, 30.0, 9.0, 15.0, 18.0]
    }
  ]
}
```

| Field                 | Meaning                                                                 |
| --------------------- | ----------------------------------------------------------------------- |
| `metadata.group_keys` | Tags the query grouped on → used to build legend labels.                |
| `metadata.warnings`   | Shown as `⚠` captions under the chart.                                  |
| `metadata.unit`       | Canonical y-axis unit (`ms`, `bytes`, …), unless `ignore_unit` is true. |
| `metadata.custom_unit`| Human y-axis label; overrides `unit` when supplied. |
| `metadata.ignore_unit` | Discard `unit`; only an explicitly supplied `custom_unit` applies. |
| `series[].start`      | Unix **seconds** (UTC) of `data[0]`.                                    |
| `series[].resolution` | **Seconds** per point; `x[i] = start + resolution*i` (uniform spacing). |
| `series[].data`       | Y values; **`null` = gap** (the line breaks, it is not drawn as 0).     |

The parser also accepts v2/v2a (same shape with an extra per-series `summary`,
ignored) and the v0/v1 bare-array form, so you can feed older responses too.

## Behaviour

- **Labels** come from `group_keys` values joined with ` | ` → `200 | GET`
  (not `code=200,method=GET`). Without `group_keys`, falls back to `k=v` tags.
- **Local time** axis by default; `--tz UTC` or `--tz Europe/Berlin` to override.
- **Gaps**: `null` points break the line.
- **Series reduction** (unless `--all`), in order:
  1. **Collapse overlapping** series whose lines essentially coincide (within
     `--eps`, default 2% of the y-range); the most prominent is kept.
  2. **Top-N** by peak value (`--top`, default 8).
  3. The legend prints **how many were dropped**, e.g.
     `showing 8 of 30 series (5 overlapping, 17 low/hidden)`, plus the
     aggregate-your-query tip.

## Output formats

`--format auto` (default) picks the best renderer for the context:

- an **inline image** when `gnuplot` is installed and the terminal supports
  images (Kitty/Ghostty, iTerm2);
- a **PNG file plus a "display this file" instruction** when output is
  piped/captured (e.g. an AI agent harness) and `gnuplot` is installed — the
  agent then displays the file;
- **ASCII** in a plain terminal, or whenever `gnuplot` is unavailable.

Force a specific backend with `--format`:

| `--format` | Needs     | Output                                                        |
| ---------- | --------- | ------------------------------------------------------------- |
| `auto`     | —         | inline image, else a PNG file + display instruction when piped, else ASCII |
| `ascii`    | nothing   | Unicode braille line chart; renders in any terminal/transcript/CI log. |
| `png`      | gnuplot   | PNG; displayed inline (Kitty/iTerm2) or written to `--output`/temp. |
| `svg`      | gnuplot   | SVG written to `--output` or a temp file (path printed).      |
| `sixel`    | gnuplot   | sixel stream to stdout (terminals with sixel support).        |

If an image format is requested but `gnuplot` is missing, it prints a note and
falls back to ASCII — it never hard-fails.

## Using from an AI agent / harness

Terminal harnesses (e.g. pi) collapse tool output and don't repaint inline
ANSI, so ASCII charts come out monochrome and folded. **Prefer images:** render
a file and let the agent display it. With `--format auto` (the default) this is
automatic whenever output is piped and `gnuplot` is installed — the skill
writes a PNG and prints:

```
metrics-chart: wrote image to /tmp/metrics-chart-XXXX.png
→ Display this file to the user with your image tool (e.g. read it); do not paste its contents.
```

The agent should then **display that file** (its image/`read` tool renders it
inline, in colour, un-folded). To control the path, pass `--output chart.png`.
Do not paste the PNG bytes or the ASCII into chat.

## Options

| Flag                | Default | Meaning                                            |
| ------------------- | ------- | -------------------------------------------------- |
| `--format`          | `auto`  | `auto`/`ascii`/`png`/`svg`/`sixel`.                |
| `--tz NAME`         | local   | IANA tz for the x-axis; `UTC` for UTC.             |
| `--top N`           | `8`     | Max series after collapse; must be >= 1.           |
| `--eps F`           | `0.02`  | Overlap threshold as a fraction of the y-range.    |
| `--all`             | off     | Draw every series (disable collapse + top-N).      |
| `--width` / `--height` | auto | Chart size (cells for ASCII, pixels for images).   |
| `--title TEXT`      | —       | Chart title.                                       |
| `--output PATH`     | —       | Write png/svg to PATH instead of a temp file.      |
| `--color` / `--no-color` | auto | Force ANSI colour on/off (default: on when a TTY). |

## Dependencies

- **Default path: none.** Pure Python 3.9+ standard library. The ASCII renderer
  always works.
- **Optional: `gnuplot`** (one system binary) for PNG/SVG/sixel. Install only if
  you want high-fidelity images.

## Why not graphviz?

`graphviz` (`dot`/`neato`) lays out node-edge graphs; it has no numeric/time
axis and cannot plot `data[i]` over time. This payload is a numeric time series
with no graph structure, so graphviz does not apply. `gnuplot` is the correct
image backend. (matplotlib is avoided on purpose: it is a heavy multi-package
pip install.)

## Tests

```bash
cd scripts && python3 -m unittest test_metrics_chart -v
```

The parser tests are pinned to the golden bytes from the metrics query
service's `service/query/src/server/tests.rs`.
