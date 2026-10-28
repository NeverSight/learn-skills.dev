---
name: claw-code-harness
description: Better Harness Tools for Claude Code — a Python (and in-progress Rust) rewrite of the Claude Code agent harness, with CLI tooling for manifest inspection, parity auditing, and tool/command inventory.
triggers:
  - "set up claw-code harness"
  - "use claw-code to inspect tools"
  - "run parity audit claw-code"
  - "claw-code manifest summary"
  - "claw-code command inventory"
  - "claw-code python harness"
  - "claw-code subsystems list"
  - "claw-code tool port metadata"
---

# Claw Code Harness

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Claw Code is a clean-room Python (with Rust port in progress) rewrite of the Claude Code agent harness. It provides tooling to inspect the port manifest, enumerate subsystems, audit parity against an archived source, and query tool/command inventories — all via a CLI entrypoint and importable Python modules.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/instructkr/claw-code.git
cd claw-code

# Install dependencies (standard library only for core; extras for dev)
pip install -r requirements.txt  # if present, else no external deps required

# Verify the workspace
python3 -m unittest discover -s tests -v
```

No PyPI package yet — use directly from source.

---

## Repository Layout

```
.
├── src/
│   ├── __init__.py
│   ├── commands.py       # Python-side command port metadata
│   ├── main.py           # CLI entrypoint
│   ├── models.py         # Dataclasses: Subsystem, Module, BacklogState
│   ├── port_manifest.py  # Current Python workspace structure summary
│   ├── query_engine.py   # Renders porting summary from active workspace
│   ├── task.py           # Task primitives
│   └── tools.py          # Python-side tool port metadata
└── tests/                # Unittest suite
```

---

## CLI Reference

All commands are invoked via `python3 -m src.main <command>`.

### `summary`
Render the full Python porting summary.
```bash
python3 -m src.main summary
```

### `manifest`
Print the current Python workspace manifest (file surface + subsystem names).
```bash
python3 -m src.main manifest
```

### `subsystems`
List known subsystems, with optional limit.
```bash
python3 -m src.main subsystems
python3 -m src.main subsystems --limit 16
```

### `commands`
Inspect mirrored command inventory.
```bash
python3 -m src.main commands
python3 -m src.main commands --limit 10
```

### `tools`
Inspect mirrored tool inventory.
```bash
python3 -m src.main tools
python3 -m src.main tools --limit 10
```

### `parity-audit`
Run parity audit against a locally present (gitignored) archived snapshot.
```bash
python3 -m src.main parity-audit
```
> Requires the local archive to be present at its expected path (not tracked in git).

---

## Core Modules & API

### `src/models.py` — Dataclasses

```python
from src.models import Subsystem, Module, BacklogState

# A subsystem groups related modules
sub = Subsystem(name="tool-harness", modules=[], status="in-progress")

# A module represents a single ported file
mod = Module(name="tools.py", ported=True, notes="tool metadata only")

# BacklogState tracks overall port progress
state = BacklogState(
    total_subsystems=8,
    ported=5,
    backlog=3,
    notes="runtime slices pending"
)
```

### `src/tools.py` — Tool Port Metadata

```python
from src.tools import get_tools, ToolMeta

tools: list[ToolMeta] = get_tools()
for t in tools[:5]:
    print(t.name, t.ported, t.description)
```

### `src/commands.py` — Command Port Metadata

```python
from src.commands import get_commands, CommandMeta

commands: list[CommandMeta] = get_commands()
for c in commands[:5]:
    print(c.name, c.ported)
```

### `src/query_engine.py` — Porting Summary Renderer

```python
from src.query_engine import render_summary

summary_text: str = render_summary()
print(summary_text)
```

### `src/port_manifest.py` — Manifest Access

```python
from src.port_manifest import get_manifest, ManifestEntry

entries: list[ManifestEntry] = get_manifest()
for entry in entries:
    print(entry.path, entry.status)
```

---

## Common Patterns

### Pattern 1: Check how many tools are ported

```python
from src.tools import get_tools

tools = get_tools()
ported = [t for t in tools if t.ported]
print(f"{len(ported)}/{len(tools)} tools ported")
```

### Pattern 2: Find unported subsystems

```python
from src.port_manifest import get_manifest

backlog = [e for e in get_manifest() if e.status != "ported"]
for entry in backlog:
    print(f"BACKLOG: {entry.path}")
```

### Pattern 3: Programmatic summary pipeline

```python
from src.query_engine import render_summary
from src.commands import get_commands
from src.tools import get_tools

print("=== Summary ===")
print(render_summary())

print("\n=== Commands ===")
for c in get_commands(limit=5):
    print(f"  {c.name}: ported={c.ported}")

print("\n=== Tools ===")
for t in get_tools(limit=5):
    print(f"  {t.name}: ported={t.ported}")
```

### Pattern 4: Run tests before contributing

```bash
python3 -m unittest discover -s tests -v
```

### Pattern 5: Using as part of an OmX/agent workflow

```bash
# Generate summary artifact for an agent to consume
python3 -m src.main summary > /tmp/claw_summary.txt

# Feed into another agent tool or diff against previous checkpoint
diff /tmp/claw_summary_prev.txt /tmp/claw_summary.txt
```

---

## Rust Port (In Progress)

The Rust rewrite is on the [`dev/rust`](https://github.com/instructkr/claw-code/tree/dev/rust) branch.

```bash
# Switch to the Rust branch
git fetch origin dev/rust
git checkout dev/rust

# Build (requires Rust toolchain: https://rustup.rs)
cargo build

# Run
cargo run -- summary
```

> The Rust port aims for a faster, memory-safe harness runtime. It is **not yet merged** into main. Until then, use the Python implementation for all production workflows.

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'src'` | Running from wrong directory | `cd` to repo root, then `python3 -m src.main ...` |
| `parity-audit` exits with "archive not found" | Local snapshot not present | Place the archive at the expected local path (see `port_manifest.py` for the path constant) |
| Tests fail with import errors | Missing `__init__.py` | Ensure `src/__init__.py` exists; re-clone if needed |
| `--limit` flag not recognized | Old checkout | `git pull origin main` |
| Rust build fails | Toolchain not installed | Run `curl https://sh.rustup.rs -sSf \| sh` then retry |

---

## Key Design Notes for AI Agents

- **No external runtime dependencies** for the core Python modules — safe to run in sandboxed environments.
- **`query_engine.py`** is the single aggregation point — prefer it over calling individual modules when you need a full picture.
- **`models.py` dataclasses** are the canonical data shapes; always import types from there, not inline dicts.
- **`parity-audit` is read-only** — it does not modify any tracked files.
- The project is **not affiliated with Anthropic** and contains no proprietary Claude Code source.
