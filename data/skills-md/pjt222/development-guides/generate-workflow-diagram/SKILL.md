---
name: generate-workflow-diagram
description: >
  Generate themed Mermaid flowchart diagrams from putior workflow data.
  Covers theme selection (9 themes including 4 colorblind-safe), output
  modes (console, file, clipboard, raw), interactive features (clickable
  nodes, source info), and embedding in README, Quarto, and R Markdown.
  Use after annotating source files and ready to produce a visual diagram,
  when regenerating a diagram after workflow changes, or when switching
  themes or output formats for different audiences.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: workflow-visualization
  complexity: basic
  language: R
  tags: putior, mermaid, diagram, theme, visualization, flowchart
---

# Generate Workflow Diagram

Generate a themed Mermaid flowchart diagram from putior workflow data and embed it in documentation.

## When to Use

- After annotating source files and ready to produce the visual diagram
- Regenerating a diagram after workflow changes
- Switching themes or output formats for different audiences
- Embedding workflow diagrams in README, Quarto, or R Markdown documents

## Inputs

- **Required**: Workflow data from `put()`, `put_auto()`, or `put_merge()`
- **Optional**: Theme name (default: `"light"`; options: light, dark, auto, minimal, github, viridis, magma, plasma, cividis)
- **Optional**: Output target: console, file path, clipboard, or raw string
- **Optional**: Interactive features: `show_source_info`, `enable_clicks`

## Procedure

### Step 1: Extract Workflow Data

Obtain workflow data from one of three sources.

```r
library(putior)

# From manual annotations
workflow <- put("./src/")

# From manual annotations, excluding specific files
workflow <- put("./src/", exclude = c("build-workflow\\.R$", "test_"))

# From auto-detection only
workflow <- put_auto("./src/")

# From merged (manual + auto)
workflow <- put_merge("./src/", merge_strategy = "supplement")
```

The workflow data frame may include a `node_type` column from annotations. Node types control Mermaid shapes:

| `node_type` | Mermaid Shape | Use Case |
|-------------|---------------|----------|
| `"input"` | Stadium `([...])` | Data sources, configuration files |
| `"output"` | Asymmetric `>...]` | Generated artifacts, reports |
| `"process"` | Rectangle `[...]` | Processing steps (default) |
| `"decision"` | Diamond `{...}` | Conditional logic, branching |
| `"start"` / `"end"` | Circle `((...))` | Entry/terminal nodes |

Each `node_type` also receives a corresponding CSS class (e.g., `class nodeId input;`) for theme-based styling.

**Expected:** A data frame with at least one row, containing `id`, `label`, and optionally `input`, `output`, `source_file`, `node_type` columns.

**On failure:** If the data frame is empty, no annotations or patterns were found. Run `analyze-codebase-workflow` first, or check that annotations are syntactically valid with `put("./src/", validate = TRUE)`.

### Step 2: Select Theme and Options

Choose a theme appropriate for the target audience.

```r
# List all available themes
get_diagram_themes()

# Standard themes
# "light"   — Default, bright colors
# "dark"    — For dark mode environments
# "auto"    — GitHub-adaptive with solid colors
# "minimal" — Grayscale, print-friendly
# "github"  — Optimized for GitHub README files

# Colorblind-safe themes (viridis family)
# "viridis" — Purple→Blue→Green→Yellow, general accessibility
# "magma"   — Purple→Red→Yellow, high contrast for print
# "plasma"  — Purple→Pink→Orange→Yellow, presentations
# "cividis" — Blue→Gray→Yellow, maximum accessibility (no red-green)
```

Additional parameters:
- `direction`: Diagram flow direction — `"TD"` (top-down, default), `"LR"` (left-right), `"RL"`, `"BT"`
- `show_artifacts`: `TRUE`/`FALSE` — show artifact nodes (files, data); can be noisy for large workflows (e.g., 16+ extra nodes)
- `show_workflow_boundaries`: `TRUE`/`FALSE` — wrap each source file's nodes in a Mermaid subgraph
- `source_info_style`: How source file info is displayed on nodes (e.g., as subtitle)
- `node_labels`: Format for node label text

**Expected:** Theme names printed. Select one based on context.

**On failure:** If a theme name is not recognized, `put_diagram()` falls back to `"light"`. Check spelling.

### Step 3: Custom Palette with `put_theme()` (Optional)

If the 9 built-in themes don't match your project's palette, create a custom theme with `put_theme()`.

```r
# Create custom palette — unspecified types inherit from base theme
cyberpunk <- put_theme(
  base = "dark",
  input    = c(fill = "#1a1a2e", stroke = "#00ff88", color = "#00ff88"),
  process  = c(fill = "#16213e", stroke = "#44ddff", color = "#44ddff"),
  output   = c(fill = "#0f3460", stroke = "#ff3366", color = "#ff3366"),
  decision = c(fill = "#1a1a2e", stroke = "#ffaa33", color = "#ffaa33")
)

# Use the palette parameter (overrides theme when provided)
mermaid_content <- put_diagram(workflow, palette = cyberpunk, output = "raw")
writeLines(mermaid_content, "workflow.mmd")
```

`put_theme()` accepts `input`, `process`, `output`, `decision`, `artifact`, `start`, and `end` node types. Each takes a named vector `c(fill = "#hex", stroke = "#hex", color = "#hex")`. Unset types inherit from the `base` theme.

**Expected:** Mermaid output with your custom classDef lines. Node shapes from `node_type` are preserved; only colors change. All node types use `stroke-width:2px` — override not currently supported via `put_theme()`.

**On failure:** If the palette object is not a `putior_theme` class, `put_diagram()` raises a descriptive error. Ensure you pass the return value of `put_theme()`, not a raw list.

**Fallback — manual classDef replacement:** For fine-grained control beyond what `put_theme()` offers (e.g., per-type stroke widths), generate with a base theme and replace classDef lines manually:

```r
mermaid_content <- put_diagram(workflow, theme = "dark", output = "raw")
lines <- strsplit(mermaid_content, "\n")[[1]]
lines <- lines[!grepl("^\\s*classDef ", lines)]
custom_defs <- c("  classDef input fill:#1a1a2e,stroke:#00ff88,stroke-width:3px,color:#00ff88")
mermaid_content <- paste(c(lines, custom_defs), collapse = "\n")
```

### Step 4: Generate Mermaid Output

Produce the diagram in the desired output mode.

```r
# Print to console (default)
cat(put_diagram(workflow, theme = "github"))

# Save to file
writeLines(put_diagram(workflow, theme = "github"), "docs/workflow.md")

# Get raw string for embedding
mermaid_code <- put_diagram(workflow, output = "raw", theme = "github")

# With source file info (shows which file each node comes from)
cat(put_diagram(workflow, theme = "github", show_source_info = TRUE))

# With clickable nodes (for VS Code, RStudio, or file:// protocol)
cat(put_diagram(workflow,
  theme = "github",
  enable_clicks = TRUE,
  click_protocol = "vscode"  # or "rstudio", "file"
))

# Full-featured
cat(put_diagram(workflow,
  theme = "viridis",
  show_source_info = TRUE,
  enable_clicks = TRUE,
  click_protocol = "vscode"
))
```

**Expected:** Valid Mermaid code starting with `flowchart TD` (or `LR` depending on direction). Nodes are connected by arrows showing data flow.

**On failure:** If the output is `flowchart TD` with no nodes, the workflow data frame is empty. If connections are missing, check that output filenames match input filenames across nodes.

### Step 5: Embed in Target Document

Insert the diagram into the appropriate documentation format.

**GitHub README (```mermaid code fence):**
````markdown
## Workflow

```mermaid
flowchart TD
  A["Extract Data"] --> B["Transform"]
  B --> C["Load"]
```
````

**Quarto document (native mermaid chunk via knit_child):**
```r
# Chunk 1: Generate code (visible, foldable)
workflow <- put("./src/")
mermaid_code <- put_diagram(workflow, output = "raw", theme = "github")
```

```r
# Chunk 2: Output as native mermaid chunk (hidden)
#| output: asis
#| echo: false
mermaid_chunk <- paste0("```{mermaid}\n", mermaid_code, "\n```")
cat(knitr::knit_child(text = mermaid_chunk, quiet = TRUE))
```

**R Markdown (with mermaid.js CDN or DiagrammeR):**
```r
DiagrammeR::mermaid(put_diagram(workflow, output = "raw"))
```

**Expected:** Diagram renders correctly in the target format. GitHub renders mermaid code fences natively.

**On failure:** If GitHub doesn't render the diagram, ensure the code fence uses exactly ` ```mermaid ` (no extra attributes). For Quarto, ensure the `knit_child()` approach is used since direct variable interpolation in `{mermaid}` chunks is not supported.

## Validation

- [ ] `put_diagram()` produces valid Mermaid code (starts with `flowchart`)
- [ ] All expected nodes appear in the diagram
- [ ] Data flow connections (arrows) are present between connected nodes
- [ ] Selected theme is applied (check init block in output for theme-specific colors)
- [ ] Diagram renders correctly in the target format (GitHub, Quarto, etc.)

## Common Pitfalls

- **Empty diagrams**: Usually means `put()` returned no rows. Check annotations exist and are syntactically valid.
- **All nodes disconnected**: Output filenames must exactly match input filenames (including extension) for putior to draw connections. `data.csv` and `Data.csv` are different.
- **Theme not visible on GitHub**: GitHub's mermaid renderer has limited theme support. The `"github"` theme is specifically designed for GitHub rendering. The `%%{init:...}%%` theme block may be ignored by some renderers.
- **Quarto mermaid variable interpolation**: Quarto's `{mermaid}` chunks don't support R variables directly. Use the `knit_child()` technique described in Step 5.
- **Clickable nodes not working**: Click directives require a renderer that supports Mermaid interaction events. GitHub's static renderer does not support clicks. Use a local Mermaid renderer or the putior Shiny sandbox.
- **Self-referential meta-pipeline files**: Scanning a directory that includes the build script generating the diagram causes duplicate subgraph IDs and Mermaid errors. Use the `exclude` parameter to skip them at scan time:
  ```r
  workflow <- put("./src/", exclude = c("build-workflow\\.R$", "build-workflow\\.js$"))
  ```
- **`show_artifacts = TRUE` too noisy**: Large projects may generate many artifact nodes (10–20+), cluttering the diagram. Use `show_artifacts = FALSE` and rely on `node_type` annotations to mark key inputs/outputs explicitly.

## Related Skills

- `annotate-source-files` — prerequisite: files must be annotated before diagram generation
- `analyze-codebase-workflow` — auto-detection can supplement manual annotations
- `setup-putior-ci` — automate diagram regeneration in CI/CD
- `create-quarto-report` — embed diagrams in Quarto reports
- `build-pkgdown-site` — embed diagrams in pkgdown documentation sites
