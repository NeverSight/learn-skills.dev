---
name: analyze-codebase-workflow
description: >
  Analyze an arbitrary codebase to auto-detect workflows, data pipelines,
  and file dependencies using putior's put_auto() engine. Produces an
  annotation plan that maps detected I/O patterns to source files across
  30+ supported languages with 862 auto-detection patterns. Use when
  onboarding onto an unfamiliar codebase to understand data flow, starting
  putior integration in a project without existing annotations, auditing a
  project's data pipeline before documentation, or preparing an annotation
  plan before running annotate-source-files.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: workflow-visualization
  complexity: intermediate
  language: multi
  tags: putior, workflow, analysis, auto-detect, polyglot, data-pipeline
---

# Analyze Codebase Workflow

Survey an arbitrary repository to auto-detect data flows, file I/O, and script dependencies, then produce a structured annotation plan for manual refinement.

## When to Use

- Onboarding onto an unfamiliar codebase and need to understand data flow
- Starting putior integration in a project that has no PUT annotations yet
- Auditing an existing project's data pipeline before documentation
- Preparing an annotation plan before running `annotate-source-files`

## Inputs

- **Required**: Path to the repository or source directory to analyze
- **Optional**: Specific subdirectories to focus on (default: entire repo)
- **Optional**: Languages to include or exclude (default: all detected)
- **Optional**: Detection scope: inputs only, outputs only, or both (default: both + dependencies)

## Procedure

### Step 1: Survey Repository Structure

Identify source files and their languages to understand what putior can analyze.

```r
library(putior)

# List all supported languages and their extensions
list_supported_languages()
list_supported_languages(detection_only = TRUE)  # Only languages with auto-detection

# Get supported extensions
exts <- get_supported_extensions()
```

Use file listing to understand repo composition:

```bash
# Count files by extension in the target directory
find /path/to/repo -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -20
```

**Expected:** A list of file extensions present in the repo, with counts. Map these against `get_supported_extensions()` to know coverage.

**On failure:** If the repo has no files matching supported extensions, putior cannot auto-detect workflows. Consider whether the language is supported but files use non-standard extensions.

### Step 2: Check Language Detection Coverage

For each detected language, verify auto-detection pattern availability.

```r
# Check which languages have auto-detection patterns (15 languages, 862 patterns)
detection_langs <- list_supported_languages(detection_only = TRUE)
cat("Languages with auto-detection:\n")
print(detection_langs)

# Get pattern counts for specific languages found in the repo
for (lang in c("r", "python", "javascript", "sql")) {
  patterns <- get_detection_patterns(lang)
  cat(sprintf("%s: %d input, %d output, %d dependency patterns\n",
    lang,
    length(patterns$input),
    length(patterns$output),
    length(patterns$dependency)
  ))
}
```

**Expected:** Pattern counts printed for each language. R has 124 patterns, Python 159, JavaScript 71, etc.

**On failure:** If a language returns no patterns, it supports manual annotations but not auto-detection. Plan to annotate those files manually.

### Step 3: Run Auto-Detection

Execute `put_auto()` on the target directory to discover workflow elements.

```r
# Full auto-detection
workflow <- put_auto("./src/",
  detect_inputs = TRUE,
  detect_outputs = TRUE,
  detect_dependencies = TRUE
)

# Exclude build scripts and test helpers from scanning
workflow <- put_auto("./src/",
  detect_inputs = TRUE,
  detect_outputs = TRUE,
  detect_dependencies = TRUE,
  exclude = c("build-", "test_helper")
)

# View detected workflow nodes
print(workflow)

# Check node count
cat(sprintf("Detected %d workflow nodes\n", nrow(workflow)))
```

For large repos, analyze subdirectories incrementally:

```r
# Analyze specific subdirectories
etl_workflow <- put_auto("./src/etl/")
api_workflow <- put_auto("./src/api/")
```

**Expected:** A data frame with columns including `id`, `label`, `input`, `output`, `source_file`. Each row represents a detected workflow step.

**On failure:** If the result is empty, the source files may not contain recognizable I/O patterns. Try enabling debug logging: `workflow <- put_auto("./src/", log_level = "DEBUG")` to see which files are scanned and which patterns match.

### Step 4: Generate Initial Diagram

Visualize the auto-detected workflow to assess coverage and identify gaps.

```r
# Generate diagram from auto-detected workflow
cat(put_diagram(workflow, theme = "github"))

# With source file info for traceability
cat(put_diagram(workflow, show_source_info = TRUE))

# Save to file for review
writeLines(put_diagram(workflow, theme = "github"), "workflow-auto.md")
```

**Expected:** A Mermaid flowchart showing detected nodes connected by data flow edges. Nodes should be labeled with meaningful function/file names.

**On failure:** If the diagram shows disconnected nodes, the auto-detection found I/O patterns but couldn't infer connections. This is normal — connections are derived from matching output filenames to input filenames. The annotation plan (next step) will address gaps.

### Step 5: Produce Annotation Plan

Generate a structured plan documenting what was found and what needs manual annotation.

```r
# Generate annotation suggestions
put_generate("./src/", style = "single")

# For multiline style (more readable for complex workflows)
put_generate("./src/", style = "multiline")

# Copy suggestions to clipboard for easy pasting
put_generate("./src/", output = "clipboard")
```

Document the plan with coverage assessment:

```markdown
## Annotation Plan

### Auto-Detected (no manual work needed)
- `src/etl/extract.R` — 3 inputs, 2 outputs detected
- `src/etl/transform.py` — 1 input, 1 output detected

### Needs Manual Annotation
- `src/api/handler.js` — Language supported but no I/O patterns matched
- `src/config/setup.sh` — Only 12 shell patterns; complex logic missed

### Not Supported
- `src/legacy/process.f90` — Fortran not in detection languages

### Recommended Connections
- extract.R output `data.csv` → transform.py input `data.csv` (auto-linked)
- transform.py output `clean.parquet` → load.R input (needs annotation)
```

**Expected:** A clear plan separating auto-detected files from those needing manual annotation, with specific recommendations for each file.

**On failure:** If `put_generate()` produces no output, ensure the directory path is correct and contains source files in supported languages.

## Validation

- [ ] `put_auto()` executes without errors on the target directory
- [ ] Detected workflow has at least one node (unless repo has no recognizable I/O)
- [ ] `put_diagram()` produces valid Mermaid code from the auto-detected workflow
- [ ] `put_generate()` produces annotation suggestions for files with detected patterns
- [ ] Annotation plan document created with coverage assessment

## Common Pitfalls

- **Scanning too broadly**: Running `put_auto(".")` on a repo root may include `node_modules/`, `.git/`, `venv/`, etc. Target specific source directories.
- **Expecting full coverage**: Auto-detection finds file I/O and library calls, not business logic. A 40-60% coverage rate is typical; the rest needs manual annotation.
- **Ignoring dependencies**: The `detect_dependencies = TRUE` flag catches `source()`, `import`, `require()` calls that link scripts together. Disabling it loses cross-file connections.
- **Language mismatch**: Files with non-standard extensions (e.g., `.R` vs `.r`, `.jsx` vs `.js`) may not be detected. Use `get_comment_prefix()` to check if an extension is recognized. Note that extensionless files like `Dockerfile` and `Makefile` are supported via exact filename matching.
- **Large repos**: For repos with 100+ source files, analyze by module/directory to keep diagrams readable.

## Related Skills

- `install-putior` — prerequisite: putior must be installed first
- `annotate-source-files` — next step: add manual annotations based on the plan
- `generate-workflow-diagram` — generate final diagram after annotation is complete
- `configure-putior-mcp` — use MCP tools for interactive analysis sessions
