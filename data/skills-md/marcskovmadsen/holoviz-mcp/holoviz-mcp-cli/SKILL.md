---
name: holoviz-mcp-cli
description: Command reference for the holoviz-mcp CLI tool. Use the CLI when you have Bash/shell access and want direct access to HoloViz documentation, component introspection, and visualization tools.
metadata:
  version: "1.0.0"
  author: holoviz
  category: tooling
  difficulty: beginner
---

# holoviz-mcp CLI

The `holoviz-mcp` CLI provides direct access to HoloViz documentation, component introspection, and visualization tools from the command line.

## Installation

The recommended way to install is as a **uv tool**:

    uv tool install holoviz-mcp

This installs both `holoviz-mcp` and `hv` commands into an isolated environment. Use `hv` as a shorter alternative in all examples below (e.g., `hv search Panel Tabulator`, `hv pn get Button`).

## When to Use CLI vs MCP

- **Prefer MCP tools** when the HoloViz MCP server is loaded — they return structured, typed data (including images) and integrate natively with LLM tool calling
- **Use CLI** when MCP tools are not available but `holoviz-mcp` (or `hv`) is installed and you have Bash/shell access
- **Search the web** as a last resort when neither MCP tools nor CLI are available

## Output Formats

All tool commands support three output formats via `--output` / `-o`:

- `pretty` (default) — Rich terminal output with colors and tables, for humans
- `markdown` — Markdown-formatted text, optimized for LLMs
- `json` — Structured JSON, for scripts and programmatic use

Setup commands (`serve`, `install`, `update`) output human-readable text by default.

## Command Structure

Commands follow noun-verb pattern with Python import aliases for library-specific tools:

    holoviz-mcp <command>                  # general tools
    holoviz-mcp pn <command>               # Panel tools     (import panel as pn)
    holoviz-mcp hv <command>               # HoloViews tools (import holoviews as hv)
    holoviz-mcp hvplot <command>           # hvPlot tools    (import hvplot)

## Quick Reference

### Search & Documentation

    holoviz-mcp search Panel Tabulator      # search all indexed docs (no quotes needed)
    holoviz-mcp search query -p panel      # search within a project
    holoviz-mcp search query -n 5          # return up to 5 results
    holoviz-mcp doc get <path> <project>   # get specific document (use search to find paths)
    holoviz-mcp ref get <component>        # find reference guide (when you know the exact name)
    holoviz-mcp ref get <component> -p panel  # filter by project

### Skills

    holoviz-mcp skill list                 # list available skills with descriptions
    holoviz-mcp skill get <name>           # get skill content (always Markdown)

### Panel (pn)

    holoviz-mcp pn list                    # list all components
    holoviz-mcp pn list -P panel_material_ui  # filter by package
    holoviz-mcp pn list -m panel.widgets   # filter by module path
    holoviz-mcp pn get Button -P panel     # get full component details
    holoviz-mcp pn params Button -P panel  # get parameter details
    holoviz-mcp pn search input widget      # search components by keyword (no quotes needed)
    holoviz-mcp pn search chart -l 5       # limit results
    holoviz-mcp pn packages                # list Panel-related packages

### hvPlot

    holoviz-mcp hvplot list                # list plot types (~28 types)
    holoviz-mcp hvplot get scatter         # get plot-specific params (compact)
    holoviz-mcp hvplot get scatter --generic  # include generic options shared by all plot types
    holoviz-mcp hvplot get scatter --style bokeh  # include backend-specific style options
    holoviz-mcp hvplot get scatter --signature  # get function signature instead

### HoloViews (hv)

    holoviz-mcp hv list                    # list visualization elements (~60 elements)
    holoviz-mcp hv get Curve               # get Curve element docstring
    holoviz-mcp hv get Curve --backend matplotlib  # specify backend

### Projects

    holoviz-mcp project list               # list indexed projects (~20 projects)

### Display & Inspect

    holoviz-mcp inspect                    # inspect app at localhost:5006
    holoviz-mcp inspect http://localhost:8080  # inspect specific URL
    holoviz-mcp inspect --no-screenshot    # console logs only
    holoviz-mcp inspect --no-console-logs  # screenshot only
    holoviz-mcp inspect --full-page --delay 5  # full page with 5s delay

### Index Management

    holoviz-mcp update index               # refresh documentation index

## Tips

- Use `holoviz-mcp search` with specific terms for better results: "Tabulator pagination page_size" > "how to paginate a table"
- Use `holoviz-mcp pn get` when you need the full docstring, constructor signature, and parameters
- Use `holoviz-mcp pn params` when you only need parameter details (lighter, no docstring)
- Use `holoviz-mcp ref get` when you know the exact component name; use `search` for fuzzy/semantic lookup
- Pipe JSON output to `jq` for filtering: `holoviz-mcp pn list -o json | jq '.[].name'`
- Use `-o pretty` for human-readable output in the terminal
