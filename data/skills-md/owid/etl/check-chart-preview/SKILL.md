---
name: check-chart-preview
description: Check chart or multidim preview on the staging server using a browser. Use when user wants to visually verify a chart renders correctly on staging, take a screenshot of a chart, or QA a chart/mdim preview.
---

# Check Chart/Mdim Preview on Staging

Visually verify that a chart or multidimensional indicator page renders correctly on the staging server.

## Prerequisites

- The `agent-browser` skill must be available (for browser automation)
- A staging server must be running for the current git branch (check via `curl -s -o /dev/null -w "%{http_code}" http://<container>/`)
- The chart/mdim must have been pushed to staging already (either via `etlr --watch` in VSCode or manually)

## Getting the Staging URL

### Option 1: Helper script (recommended)

```bash
.venv/bin/python .claude/skills/check-chart-preview/get_staging_url.py <slug-or-path>
```

Accepts chart slugs, mdim slugs, or file paths:
```bash
# Chart slug (most common)
.venv/bin/python .claude/skills/check-chart-preview/get_staging_url.py life-expectancy

# Mdim slug
.venv/bin/python .claude/skills/check-chart-preview/get_staging_url.py energy/latest/energy_prices#energy_prices

# Export multidim file path
.venv/bin/python .claude/skills/check-chart-preview/get_staging_url.py etl/steps/export/multidim/energy/latest/energy_prices.config.yml

# Chart file path
.venv/bin/python .claude/skills/check-chart-preview/get_staging_url.py etl/steps/graph/covid/latest/covid-cases.chart.yml
```

### Option 2: Construct manually

1. Get the git branch: `git branch --show-current`
2. Compute container name: replace `/._` with `-` in branch name, strip any `staging-site-` prefix, prepend `staging-site-`, truncate the normalized part to 28 chars, strip trailing `-`
3. Determine chart type and URL:

| File type | URL pattern |
|---|---|
| `.chart.yml` (simple, no `#` in slug) | `http://<container>/grapher/<slug>` |
| `.chart.yml` (mdim, `#` in slug) | `http://<container>/admin/grapher/<catalogPath>` |
| `export/multidim/*.config.yml` or `*.py` | `http://<container>/admin/grapher/<namespace>/<version>/<shortName>%23<shortName>` |

For `.chart.yml`: the `slug` is in the YAML `slug:` field. For mdim slugs containing `#`, the catalogPath inserts the version from the file path.

For export multidim: derive from path `etl/steps/export/multidim/<namespace>/<version>/<shortName>.*` → catalogPath is `<namespace>/<version>/<shortName>#<shortName>`.

## Checking the Preview

Use the `agent-browser` skill to:

1. **Navigate** to the staging URL
2. **Wait** for the chart to render (look for the Grapher SVG or iframe content to load)
3. **Verify**:
   - No error banner or "Chart not found" message
   - Chart title is visible
   - Data points / map regions are rendered (not an empty chart)
   - For mdim: dimension dropdowns are present and functional
4. **Take a screenshot** and save to `ai/` directory

### Quick PNG check (non-mdim charts only)

For simple (non-mdim) charts, you can fetch a PNG directly without a browser:

```bash
curl -o ai/chart_preview.png "http://<container>/grapher/<slug>.png?nocache"
```

Add `&tab=map` or `&tab=chart` to control which tab is shown. This does NOT work for mdim charts.

## Pushing to Staging First

If the chart hasn't been pushed yet:

```bash
# For graph step charts
.venv/bin/etlr graph://<namespace>/<version>/<slug> --graph --graph-push --private

# For export multidim
.venv/bin/etlr export://multidim/<namespace>/<version>/<shortName> --export --private
```
