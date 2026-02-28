---
name: wasm-compatibility
description: Check if a marimo notebook is compatible with WebAssembly (WASM) and report any issues.
---

# WASM Compatibility Checker for marimo Notebooks

Check whether a marimo notebook can run in a WebAssembly (WASM) environment — the marimo playground, community cloud, or exported WASM HTML.

## Instructions

### 1. Read the notebook

Read the target notebook file. If the user doesn't specify one, ask which notebook to check.

### 2. Extract dependencies

Collect every package the notebook depends on from **both** sources:

- **PEP 723 metadata** — the `# /// script` block at the top:
  ```python
  # /// script
  # dependencies = [
  #     "marimo",
  #     "torch>=2.0.0",
  # ]
  # ///
  ```
- **Import statements** — scan all cells for `import foo` and `from foo import bar`. Map import names to their PyPI distribution name using this table:

  | Import name | Distribution name |
  |---|---|
  | `sklearn` | `scikit-learn` |
  | `skimage` | `scikit-image` |
  | `cv2` | `opencv-python` |
  | `PIL` | `Pillow` |
  | `bs4` | `beautifulsoup4` |
  | `yaml` | `pyyaml` |
  | `dateutil` | `python-dateutil` |
  | `attr` / `attrs` | `attrs` |
  | `gi` | `PyGObject` |
  | `serial` | `pyserial` |
  | `usb` | `pyusb` |
  | `wx` | `wxPython` |

  For most other packages, the import name matches the distribution name.

### 3. Check each package against Pyodide

For each dependency, determine if it can run in WASM:

1. **Is it in the Python standard library?** Most stdlib modules work, but these do **not**:
   - `multiprocessing` — browser sandbox has no process spawning
   - `subprocess` — same reason
   - `threading` — emulated, no real parallelism (WARN, not a hard fail)
   - `sqlite3` — use `apsw` instead (available in Pyodide)
   - `pdb` — not supported
   - `tkinter` — no GUI toolkit in browser
   - `readline` — no terminal in browser

2. **Is it a Pyodide built-in package?** See [pyodide-packages.md](references/pyodide-packages.md) for the full list. These work out of the box.

3. **Is it a pure-Python package?** Packages with only `.py` files (no compiled C/Rust extensions) can be installed at runtime via `micropip` and will work. To check: look for a `py3-none-any.whl` wheel on PyPI (e.g. visit `https://pypi.org/project/<package>/#files`). If the only wheels are platform-specific (e.g. `cp312-cp312-manylinux`), the package has native extensions and likely won't work.

   Common pure-Python packages that work (not in Pyodide built-ins but installable via micropip):
   - `plotly`, `seaborn`, `humanize`, `pendulum`, `arrow`, `tabulate`
   - `dataclasses-json`, `marshmallow`, `cattrs`, `pydantic` (built-in)
   - `httpx` (built-in), `tenacity`, `backoff`, `wrapt` (built-in)

4. **Does it have C/native extensions not built for Pyodide?** These will **not** work. Common culprits:
   - `torch` / `pytorch`
   - `tensorflow`
   - `jax` / `jaxlib`
   - `psycopg2` (suggest `psycopg` with pure-Python mode)
   - `mysqlclient` (suggest `pymysql`)
   - `uvloop`
   - `grpcio`
   - `psutil`

### 4. Check for WASM-incompatible patterns

Scan the notebook code for patterns that won't work in WASM:

| Pattern | Why it fails | Suggestion |
|---|---|---|
| `subprocess.run(...)`, `os.system(...)`, `os.popen(...)` | No process spawning in browser | Remove or gate behind a non-WASM check |
| `multiprocessing.Pool(...)`, `ProcessPoolExecutor` | No process forking | Use single-threaded approach |
| `threading.Thread(...)`, `ThreadPoolExecutor` | Emulated threads, no real parallelism | WARN only — works but no speedup; use `asyncio` for I/O |
| `open("/absolute/path/...")`, hard-coded local file paths | No real filesystem; only in-memory fs | Fetch data via URL (`httpx`, `urllib`) or embed in notebook |
| `sqlite3.connect(...)` | stdlib sqlite3 unavailable | Use `apsw` or `duckdb` |
| `pdb.set_trace()`, `breakpoint()` | No debugger in WASM | Remove breakpoints |
| Reading env vars (`os.environ[...]`, `os.getenv(...)`) | Environment variables not available in browser | Use `mo.ui.text` for user input or hardcode defaults |
| `Path.home()`, `Path.cwd()` with real file expectations | Virtual filesystem only | Use URLs or embedded data |
| Large dataset loads (>100 MB) | 2 GB total memory cap | Use smaller samples or remote APIs |

### 5. Check PEP 723 metadata

WASM notebooks should list all dependencies in the PEP 723 `# /// script` block so they are automatically installed when the notebook starts. Check for these issues:

- **Missing metadata:** If the notebook has no `# /// script` block, emit a WARN recommending one. Listing dependencies ensures they are auto-installed when the notebook starts in WASM — without it, users may see import errors.
- **Missing packages:** If a package is imported but not listed in the dependencies, emit a WARN suggesting it be added.
Note: version pins and lower bounds in PEP 723 metadata are fine — marimo strips version constraints when running in WASM.

### 6. Produce the report

Output a clear, actionable report with these sections:

**Compatibility: PASS / FAIL / WARN**

Use these verdicts:
- **PASS** — all packages and patterns are WASM-compatible
- **WARN** — likely compatible, but some packages could not be verified as pure-Python (list them so the user can check)
- **FAIL** — one or more packages or patterns are definitely incompatible

**Package Report** — table with columns: Package, Status (OK / WARN / FAIL), Notes

Example:
| Package | Status | Notes |
|---|---|---|
| marimo | OK | Available in WASM runtime |
| numpy | OK | Pyodide built-in |
| pandas | OK | Pyodide built-in |
| torch | FAIL | No WASM build — requires native C++/CUDA extensions |
| my-niche-lib | WARN | Not in Pyodide; verify it is pure-Python |

**Code Issues** — list each problematic code pattern found, with the cell or line and a suggested fix.

**Recommendations** — if the notebook fails, suggest concrete fixes:
- Replace incompatible packages with WASM-friendly alternatives
- Rewrite incompatible code patterns
- Suggest moving heavy computation to a hosted API and fetching results

## Additional context

- WASM notebooks run via [Pyodide](https://pyodide.org) in the browser
- Memory is capped at 2 GB
- Network requests work but may need CORS-compatible endpoints
- Chrome has the best WASM performance; Firefox, Edge, Safari also supported
- `micropip` can install any pure-Python wheel from PyPI at runtime
- For the full Pyodide built-in package list, see [pyodide-packages.md](references/pyodide-packages.md)
