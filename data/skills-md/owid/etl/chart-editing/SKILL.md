---
name: chart-editing
description: Edit and preview .chart.yml files for OWID graph steps. Use when user wants to edit chart config, preview charts, change chart appearance, or work with graph step chart files.
---

# Chart Editing

Edit `.chart.yml` files that define OWID Grapher chart configurations, then preview changes.

## File Locations

- Chart configs: `etl/steps/graph/<namespace>/<version>/<short_name>.chart.yml`
- Schema: `schemas/chart-schema.json` (read this to understand valid fields)
- DAG definitions: `dag/graph/<namespace>.yml` (maps graph steps to data dependencies)

## Before Editing

1. **Read the schema** at `schemas/chart-schema.json` to understand all valid fields, enums, and nested structures
2. **Read the target `.chart.yml`** to understand current config
3. **Check the DAG** in `dag/graph/<namespace>.yml` to understand which dataset the chart depends on

## Chart Config Formats

### Simple format (single indicator)

Used for charts with one indicator and no dimension toggles:

```yaml
title: Which countries have banned chick culling?
tab: map
hasMapTab: true
chartTypes: []
yAxis:
  min: auto
map:
  hideTimeline: true
  colorScale:
    customCategoryColors:
      Banned: '#4881c6'
      No laws: '#b6a28c'
    customNumericColorsActive: true
$schema: https://files.ourworldindata.org/schemas/grapher-schema.010.json
originUrl: /animal-welfare
dimensions:
  - property: y
    catalogPath: status
```

Key fields: `dimensions[].property` (y/x/size/color) and `dimensions[].catalogPath` (column name in the dataset).

### Multi-dimensional format (explorer-like)

Used for charts with multiple indicator combinations selectable via dropdowns:

```yaml
slug: covid/covid#covid_cases

definitions:
  common_views:
    - config:
        tab: map
        originUrl: ourworldindata.org/coronavirus

title:
  title: COVID-19 confirmed cases
  title_variant: ""

default_selection:
  - World
  - Europe
  - Asia

topic_tags:
  - COVID-19

dimensions:
  - slug: period
    name: Period
    choices:
      - slug: weekly
        name: Weekly
      - slug: biweekly
        name: Biweekly

  - slug: metric
    name: Indicator
    choices:
      - slug: absolute
        name: Absolute number
      - slug: per_capita
        name: Per million people

views:
  - dimensions:
      period: weekly
      metric: absolute
    indicators:
      y:
        - catalogPath: weekly_cases

  - dimensions:
      period: weekly
      metric: per_capita
    indicators:
      y:
        - catalogPath: weekly_cases_per_million
```

Key differences from simple: `title` is an object `{title, title_variant}`, `dimensions` defines UI facets (not indicators), actual indicators are in `views[].indicators.y[].catalogPath`.

## Previewing Charts

Charts are previewed via the staging server. The staging URL follows this pattern:

```
http://staging-site-{branch}/grapher/{slug}
```

where `{branch}` is the current git branch name (with `/._` replaced by `-`, truncated to 28 chars).

### PNG screenshot (for visual inspection)

Fetch the PNG directly from the staging server using `WebFetch`:

```
http://staging-site-{branch}/grapher/{slug}.png?nocache
```

Add `&tab=map` or `&tab=chart` to control which tab is shown.

**Prerequisite**: The chart must be pushed to staging first. If the user has the VSCode chart preview extension open, this happens automatically via `etlr --watch`. Otherwise push manually:
```bash
.venv/bin/etlr graph://<namespace>/<version>/<slug> --graph --graph-push --private
```

## Editing Workflow

1. Read the chart file and schema
2. Make edits using the Edit tool (preserve YAML comments with ruamel if needed)
3. Push to staging: `.venv/bin/etlr graph://<namespace>/<version>/<slug> --graph --graph-push --private`
4. Fetch the PNG from `http://staging-site-{branch}/grapher/{slug}.png?nocache` to verify visually
5. If the chart looks wrong, read the schema for correct field names/values

## Common Edits

- **Change default tab**: Set `tab` to `chart`, `map`, `table`, `line`, `slope`, `discrete-bar`, or `marimekko`
- **Change selected entities**: Edit `selectedEntityNames` array
- **Change colors**: Edit `map.colorScale.customCategoryColors` or `colorScale.customCategoryColors`
- **Change color scheme**: Set `baseColorScheme` or `map.colorScale.baseColorScheme` (see schema for valid values)
- **Hide/show map tab**: Set `hasMapTab: true/false`
- **Add chart note**: Set `note` field
- **Change axis**: Edit `yAxis` or `xAxis` with `min`, `max`, `scaleType`, `label`

## Validation

Chart configs should conform to `schemas/chart-schema.json`. Key constraints:
- `tab` enum: `chart`, `map`, `table`, `line`, `slope`, `discrete-bar`, `marimekko`
- `chartTypes` enum items: `LineChart`, `ScatterPlot`, `StackedArea`, `DiscreteBar`, `StackedDiscreteBar`, `SlopeChart`, `StackedBar`, `Marimekko`
- `dimensions[].property` enum: `y`, `x`, `size`, `color`, `table`
- `addCountryMode` enum: `add-country`, `change-country`, `disabled`
