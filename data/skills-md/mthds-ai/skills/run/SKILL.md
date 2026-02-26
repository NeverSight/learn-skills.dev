---
name: run
description: Run MTHDS methods and interpret results. Use when user says "run this pipeline", "execute the workflow", "execute the method", "test this .mthds file", "try it out", "see the output", "dry run", or wants to execute any MTHDS method bundle and see its output.
---

# Run MTHDS methods

Execute MTHDS method bundles and interpret their JSON output.

## Process

**Prerequisite**: See [CLI Prerequisites](../shared/prerequisites.md)

### Step 1: Identify the Target

| Target | Command |
|--------|---------|
| Pipeline directory (recommended) | `mthds-agent pipelex run pipe <bundle-dir>/` |
| Specific pipe in a directory | `mthds-agent pipelex run pipe <bundle-dir>/ --pipe my_pipe` |
| Bundle file directly | `mthds-agent pipelex run pipe bundle.mthds -L <bundle-dir>/` |
| Pipe by code from library | `mthds-agent pipelex run pipe my_pipe` |

> **Directory mode** (recommended): Pass the pipeline directory as target. The CLI auto-detects `bundle.mthds`, `inputs.json`, and sets `-L` automatically — no need to specify them explicitly. This also avoids namespace collisions with other bundles.

### Step 2: Prepare Inputs and Check Readiness

#### Fast path — inputs just prepared

If inputs were already prepared during this conversation — via `/inputs` (user-data, synthetic, or mixed strategy), or by manually assembling `inputs.json` with real values earlier in this session — skip the schema fetch and readiness check. The inputs are ready. Proceed directly to Step 3 with a normal run.

This applies when you just wrote or saw `inputs.json` being written with real content values. It does NOT apply after `/build` (which saves a placeholder template) or after `/inputs` with the template strategy.

#### Full check — cold start

If `/run` is invoked without prior input preparation in this session, perform the full readiness check:

Get the input schema for the target:

```bash
mthds-agent pipelex inputs pipe bundle.mthds
```

**Output:**
```json
{
  "success": true,
  "pipe_code": "process_document",
  "inputs": {
    "document": {
      "concept": "native.Document",
      "content": {"url": "url_value"}
    },
    "context": {
      "concept": "native.Text",
      "content": {"text": "text_value"}
    }
  }
}
```

Fill in the `content` fields with actual values. For complex inputs, use the /inputs skill.

#### Input Readiness Check

Before running, assess whether inputs are ready. This prevents runtime failures from placeholder values.

**No inputs required**: If `mthds-agent pipelex inputs pipe` returns an empty `inputs` object (`{}`), inputs are ready — skip to Step 3.

**Inputs required**: If inputs exist, check `inputs.json` for readiness:

1. Does `inputs.json` exist in the bundle directory?
2. If it exists, scan all `content` values for placeholder signals:
   - **Template defaults**: `"url_value"`, `"text_value"`, `"number_value"`, `"integer_value"`, `"boolean_value"`, or any value matching the pattern `*_value`
   - **Angle-bracket placeholders**: values containing `<...>` (e.g. `<path-to-cv.pdf>`, `<your-text-here>`)
   - **Non-existent file paths**: `url` fields pointing to local files that don't exist on disk

**Readiness result**:
- **Ready**: `inputs.json` exists AND all content values are real (no placeholders, referenced files exist) → proceed to Step 3 with normal run
- **Not ready**: `inputs.json` is missing, OR contains any placeholder values → proceed to Step 3 with dry-run fallback

### Step 3: Choose Run Mode

#### If inputs are not ready

Default to `--dry-run --mock-inputs` and inform the user:

> "The inputs for this pipeline contain placeholder values (not real data). I'll do a dry run with mock inputs to validate the pipeline structure."

After the dry run, offer the user these options:
- **Prepare real inputs** — use `/inputs` to fill in actual values, then re-run
- **Provide files** — if the pipeline expects file inputs (documents, images), ask the user to supply file paths
- **Keep dry run** — accept the dry-run result as-is

#### Run modes reference

| Mode | Command | Use When |
|------|---------|----------|
| **Dry run + mock inputs** | `mthds-agent pipelex run pipe <bundle-dir>/ --dry-run --mock-inputs` | Quick structural validation, no real data needed, or inputs not ready |
| **Dry run with real inputs** | `mthds-agent pipelex run pipe <bundle-dir>/ --dry-run` | Validate input shapes without making API calls (auto-detects `inputs.json`) |
| **Full run** | `mthds-agent pipelex run pipe <bundle-dir>/` | Production execution (auto-detects `inputs.json`) |
| **Full run inline** | `mthds-agent pipelex run pipe <bundle-dir>/ --inputs '{"theme": ...}'` | Quick execution with inline JSON inputs |
| **Full run without graph** | `mthds-agent pipelex run pipe <bundle-dir>/ --no-graph` | Execute without generating graph visualization |
| **Full run with memory** | `mthds-agent pipelex run pipe <bundle-dir>/ --with-memory` | When piping output to another method |

> **Graph by default**: Execution graphs (`live_run.html` / `dry_run.html`) are now generated automatically. Use `--no-graph` to disable.

### Inline JSON for Inputs

The `--inputs` flag accepts both file paths and inline JSON. The CLI auto-detects: if the value starts with `{`, it is parsed as JSON directly. This is the fastest path — no file creation needed for simple inputs.

```bash
# Inline JSON
mthds-agent pipelex run pipe <bundle-dir>/ --inputs '{"theme": {"concept": "native.Text", "content": {"text": "nature"}}}'

# File path (auto-detected in directory mode)
mthds-agent pipelex run pipe <bundle-dir>/
```

### Step 4: Present Results

After a successful run, **always show the actual output to the user** — never just summarize what fields exist.

#### Output format modes

The CLI has two output modes:

- **Compact (default)**: stdout is the concept's structured JSON directly — no envelope, no `success` wrapper. This is the primary output of the method's main concept. Parse the JSON directly for field access.
- **With memory (`--with-memory`)**: stdout has `main_stuff` (with `json`, `markdown`, `html` renderings) + `working_memory` (all named stuffs and aliases). Use this when piping output to another method.

The `output_file` and `graph_files` are written to disk as side effects (paths appear in logs/stderr), not in compact stdout.

#### 4a. Determine what to show

**In compact mode** (default), the output is the concept JSON directly. Show the fields to the user:

```json
{
  "clauses": [...],
  "overall_risk": "high"
}
```

**In `--with-memory` mode**, the output structure depends on the pipe architecture:

```
if main_stuff is non-empty (not {} or null):
    → main_stuff is the primary output (single unified result)
else:
    → working_memory.root holds the primary output (multiple named results)
```

| Pipe Type | `main_stuff` present? | What to show |
|-----------|----------------------|--------------|
| PipeLLM, PipeCompose, PipeExtract, PipeImgGen | Always | `main_stuff` |
| PipeSequence | Always (last step) | `main_stuff` |
| PipeBatch | Always (list) | `main_stuff` |
| PipeCondition | Always | `main_stuff` |
| PipeParallel with `combined_output` | Yes | `main_stuff` |
| PipeParallel without `combined_output` | No (`{}`) | `working_memory.root` entries |

#### 4b. Show the output content

**In compact mode**: show the JSON fields directly. For structured concepts, format for readability.

**In `--with-memory` mode when `main_stuff` is present** (most pipe types):

- Show `main_stuff.markdown` directly — this is the human-readable rendering. Display it as-is so the user sees the full output.
- For structured concepts with fields, also show `main_stuff.json` formatted for readability.

**In `--with-memory` mode when `main_stuff` is empty** (PipeParallel without `combined_output`):

- Iterate `working_memory.root` and present each named result.
- For each entry, show the `content` field with its key as a label.
- Example: "**french_translation**: Bonjour le monde" / "**spanish_translation**: Hola mundo"

**For dry runs**: Show the same output but clearly label it as mock/simulated data.

#### 4c. Output file

- The CLI automatically saves the full JSON output next to the bundle (`live_run.json` or `dry_run.json`).
- The output file path appears in runtime logs (stderr), not in compact stdout.

#### 4d. Present graph files

- Graph visualizations are generated by default (`live_run.html` / `dry_run.html`). Use `--no-graph` to disable.
- The graph file path appears in runtime logs (stderr), not in compact stdout.

#### 4e. Mention intermediate results

- If the pipeline has multiple steps, briefly note key intermediate values from `working_memory` (e.g., "The match analysis intermediate step scored 82/100").
- Offer: "I can show the full working memory if you want to inspect any intermediate step."

#### 4f. Suggest next steps

- Re-run with different inputs
- Adjust prompts or pipe configurations if output quality needs improvement

### Step 5: Handle Errors

When encountering runtime errors, re-run with `--log-level debug` for additional context:

```bash
mthds-agent --log-level debug pipelex run pipe <bundle-dir>/ --inputs data.json
```

For all error types and recovery strategies, see [Error Handling Reference](../shared/error-handling.md).

### Execution Graphs

Execution graph visualizations are generated by default alongside the run output. Use `--no-graph` to disable.

```bash
mthds-agent pipelex run pipe <bundle-dir>/
```

Graph files (`live_run.html` / `dry_run.html`) are written to disk next to the bundle. Their paths appear in runtime logs on stderr, not in compact stdout. When using `--with-memory`, `graph_files` is included in the returned JSON envelope.

### Piping Methods

The run command accepts piped JSON on stdin when `--inputs` is not provided. This enables chaining methods:

```bash
mthds-agent pipelex run method extract-terms --inputs data.json --with-memory \
  | mthds-agent pipelex run method assess-risk --with-memory \
  | mthds-agent pipelex run method generate-report
```

When methods are installed as CLI shims, the same chain is:

```bash
extract-terms --inputs data.json --with-memory \
  | assess-risk --with-memory \
  | generate-report
```

- Use `--with-memory` on intermediate steps to pass the full working memory envelope.
- The final step omits `--with-memory` to produce compact output.
- `--inputs` always overrides stdin when both are present.
- Upstream stuff names are matched against downstream input names. Method authors should name their outputs to match the downstream's expected input names.

## Reference

- [CLI Prerequisites](../shared/prerequisites.md) — read at skill start to check CLI availability
- [Error Handling](../shared/error-handling.md) — read when CLI returns an error to determine recovery
- [MTHDS Agent Guide](../shared/mthds-agent-guide.md) — read for CLI command syntax or output format details
- [MTHDS Language Reference](../shared/mthds-reference.md) — read for .mthds syntax documentation
- [Native Content Types](../shared/native-content-types.md) — read when interpreting pipeline outputs or preparing input JSON, to understand the attributes of each content type
