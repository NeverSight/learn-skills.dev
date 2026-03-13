---
name: jupyter-notebook-writing
description: Write Milvus application-level Jupyter notebook examples using a Markdown-first workflow with jupyter-switch for format conversion.
---

# Skill: Jupyter Notebook Writing

Write Milvus application-level Jupyter notebook examples as a DevRel workflow. Uses a Markdown-first approach — AI edits `.md` files, then converts to `.ipynb` via `jupyter-switch`.

> **Prerequisites**: Python >= 3.10, uv (`uvx` command available)

---

## When to Use

The user wants to create or edit a Jupyter notebook example, typically demonstrating Milvus usage in an application context (RAG, semantic search, hybrid search, etc.).

---

## Core Workflow: Markdown-First Editing

Jupyter `.ipynb` files contain complex JSON with metadata, outputs, and execution counts — painful for AI to edit directly. Instead:

1. **Write/Edit the `.md` file** — AI works with clean Markdown
2. **Convert to `.ipynb`** — using `jupyter-switch` for runnable notebook
3. **Keep both files in sync** — the `.md` is the source of truth for editing

### Format Convention

In the `.md` file:
- **Python code blocks** (` ```python ... ``` `) become **code cells** in the notebook
- **Everything else** becomes **markdown cells**
- Cell outputs are not preserved in `.md` (they get generated when running the notebook)

### Conversion Commands

```bash
# Markdown -> Jupyter Notebook
uvx jupyter-switch example.md
# produces example.ipynb

# Jupyter Notebook -> Markdown
uvx jupyter-switch example.ipynb
# produces example.md
```

- The original input file is never modified or deleted
- If the output file already exists, a `.bak` backup is created automatically

---

## Step-by-Step

### Creating a New Notebook

1. Create `example.md` with the content (see structure below)
2. Convert: `uvx jupyter-switch example.md`
3. Both `example.md` and `example.ipynb` now exist

### Editing an Existing Notebook

1. If only `.ipynb` exists, convert first: `uvx jupyter-switch example.ipynb`
2. Edit the `.md` file
3. Convert back: `uvx jupyter-switch example.md`

### Testing / Running

#### 1. Resolve the Jupyter execution environment

Before running any notebook, you must determine which Python environment to use. The system default `jupyter execute` may not have the required packages installed.

**Step A — Check for saved preference.** Look in the current project's `CLAUDE.local.md` for a `## Jupyter Notebook Execution` section. If it contains a kernel name, use it directly and skip to Step 2.

**Step B — If no saved preference, ask the user.** Detect available environments first:

```bash
# Discover conda/mamba environments
conda env list 2>/dev/null || mamba env list 2>/dev/null

# Discover registered Jupyter kernels
jupyter kernelspec list 2>/dev/null

# Check system default Python
which python3 2>/dev/null && python3 --version 2>/dev/null

# Check for local virtual environment in the working directory
ls -d .venv/ venv/ 2>/dev/null

# Check if a uv-managed project (pyproject.toml + .venv)
test -f pyproject.toml && test -d .venv && echo "uv/pip project venv detected"
```

Then present a numbered list of choices. Include all detected environments:

1. **System default** — run `jupyter execute` as-is, no `--kernel_name`
2. **Each detected conda/mamba environment** — show name and path
3. **Each registered Jupyter kernel** — show kernel name
4. **Local venv** (if `.venv/` or `venv/` found in working directory) — the Python inside that venv
5. **Custom** — let the user type a Python path or environment name

> **Note on uv projects:** If the working directory has `pyproject.toml` + `.venv/` (a uv-managed project), the local venv option covers this case. The user can also run `uv run jupyter execute example.ipynb` directly if jupyter is a project dependency.

For every option, also offer a "remember" variant. Example prompt:

```
Which Python environment should I use to run this notebook?

1. System default (jupyter execute as-is)
2. conda: myenv (/path/to/envs/myenv)
3. Jupyter kernel: some-kernel
4. Local venv (.venv/)
5. Custom — enter a path or environment name

Tip: add "remember" to save your choice (e.g. "2, remember"),
so it gets written to CLAUDE.local.md and I won't ask next time.
```

**Step C — Apply the chosen environment:**

| Scenario | Action |
|----------|--------|
| Already a registered Jupyter kernel | Use `jupyter execute --kernel_name=<name>` |
| Conda env not yet registered as kernel | Register first: `<env-python> -m ipykernel install --user --name <name> --display-name "<label>"`, then use `--kernel_name=<name>` |
| Custom Python path | Same as above — register as kernel first, then use `--kernel_name` |

**Step D — If the user chose "remember":** append or update a `## Jupyter Notebook Execution` section in the current project's `CLAUDE.local.md`:

```markdown
## Jupyter Notebook Execution

- **Jupyter kernel**: `<kernel-name>`
```

This ensures future runs skip the prompt and use the saved kernel directly.

#### 2. Prepare the notebook for execution

Before running, comment out "setup-only" cells in the `.md` file — cells that are meant for first-time users but should not run in an automated test environment. Specifically:

- **`pip install` cells** — dependencies should already be installed in the chosen Jupyter environment. If any packages are missing or need upgrading, install them externally in the target environment (with `--upgrade`), not inside the notebook.
- **API key / credential placeholder cells** — e.g. `os.environ["OPENAI_API_KEY"] = "sk-***********"`. Instead, set environment variables externally before running (export in shell, or inject via code before `jupyter execute`).
- **Mock / demo-only cells** — any cells that exist purely for illustration and would fail or interfere in a real run.

To comment out a cell, wrap its content in a block comment so the cell still executes (producing empty output) but does nothing:

```python
# # pip install --upgrade langchain pymilvus
# import os
# os.environ["OPENAI_API_KEY"] = "sk-***********"
```

This keeps the notebook structure intact (cell count, ordering) while preventing conflicts with the external Jupyter environment.

**For environment variables:** either `export` them in the shell before running `jupyter execute`, or prepend them to the command:

```bash
OPENAI_API_KEY="sk-real-key" jupyter execute --kernel_name=<name> example.ipynb
```

#### 3. Convert and run

1. Convert `.md` to `.ipynb` if needed
2. Install any missing dependencies in the target environment externally: `<env-python> -m pip install --upgrade <packages>`
3. Run: `jupyter execute --kernel_name=<name> example.ipynb` (omit `--kernel_name` if using system default)
4. If errors found, fix in the `.md` file, uncomment setup cells if needed for debugging, and re-convert

---

## Notebook Structure Template

A typical Milvus example notebook follows this structure:

```markdown
# Title

Brief description of what this notebook demonstrates.

## Prerequisites

Install dependencies:

` ``python
!pip install pymilvus some-other-package
` ``

## Setup

Import and configuration:

` ``python
from pymilvus import MilvusClient

client = MilvusClient(uri="http://localhost:19530")
` ``

## Prepare Data

Load or generate example data:

` ``python
# data preparation code
` ``

## Create Collection & Insert Data

` ``python
# collection creation and data insertion
` ``

## Query / Search

` ``python
# search or query examples
` ``

## Cleanup

` ``python
client.drop_collection("example_collection")
` ``
```

---

## Reference Documents

This skill includes two reference documents under `references/`. **Read them when the task involves their topics.**

| Reference | When to Read | File |
|-----------|-------------|------|
| **Bootcamp Format** | Writing a Milvus integration tutorial (badges, document structure, section format, example layout) | `references/bootcamp-format.md` |
| **Milvus Code Style** | Writing pymilvus code (collection creation, MilvusClient connection args, schema patterns, best practices) | `references/milvus-code-style.md` |

### Bootcamp Format (`references/bootcamp-format.md`)

Read this when the user is writing a **Milvus integration tutorial** for the bootcamp repository. It covers:
- Badge format (Colab + GitHub badges at the top)
- Document structure: Header -> Prerequisites -> Main Content -> Conclusion
- Dependency install format with Google Colab restart note
- API key placeholder conventions (`"sk-***********"`)
- Each code block should have a short text introduction before it

### Milvus Code Style (`references/milvus-code-style.md`)

Read this when the notebook involves **pymilvus code**. Key rules:
- **Always use `MilvusClient` API** — never use the legacy ORM layer (`connections.connect()`, `Collection()`, `FieldSchema()`, etc.)
- Always define schema explicitly (`create_schema` + `add_field`) — do not use the shortcut `create_collection(dimension=...)` without schema
- Include `has_collection` check before creating collections
- Add commented `consistency_level="Strong"` line in `create_collection()`
- No need to call `load_collection()` — collections auto-load on creation
- First MilvusClient connection must include the blockquote explaining `uri` options (Milvus Lite / Docker / Zilliz Cloud)

---

## Important Notes

- **Always edit the `.md` file**, not the `.ipynb` directly. The `.md` is easier for AI to read and write.
- **Keep both files** — `.md` for editing, `.ipynb` for running/sharing.
- After editing `.md`, always re-run `uvx jupyter-switch example.md` to sync the `.ipynb`.
