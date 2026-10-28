---
name: clawd-code-python-port
description: Python port of Claude Code agent harness — tools, commands, task orchestration, and CLI entrypoint via oh-my-codex
triggers:
  - how do I run clawd-code
  - how do I use the Python port of Claude Code
  - clawd-code CLI commands
  - how do I add a tool to clawd-code
  - how does the agent harness work in clawd-code
  - how do I extend clawd-code with new commands
  - how do I run the parity audit in clawd-code
  - how do I verify the Python workspace in clawd-code
---

# clawd-code Python Port

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

## What This Project Does

**clawd-code** is an independent Python rewrite of the Claude Code agent harness, built from scratch for educational purposes. It captures the architectural patterns of Claude Code — tool wiring, command dispatch, task orchestration, and agent runtime context — in clean Python, without copying any proprietary TypeScript source.

The project is orchestrated end-to-end using [oh-my-codex (OmX)](https://github.com/Yeachan-Heo/oh-my-codex), a workflow layer on top of OpenAI Codex. It is **not affiliated with or endorsed by Anthropic**.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/instructkr/clawd-code.git
cd clawd-code

# (Optional but recommended) Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies (if a requirements.txt or pyproject.toml is present)
pip install -r requirements.txt
# or
pip install -e .
```

No API keys are needed for the manifest/summary/CLI commands. If you extend the query engine to call a live model, set your key via environment variable:

```bash
export ANTHROPIC_API_KEY="your-key-here"
export OPENAI_API_KEY="your-key-here"
```

---

## Repository Layout

```
.
├── src/
│   ├── __init__.py
│   ├── commands.py       # Command port metadata
│   ├── main.py           # CLI entrypoint
│   ├── models.py         # Dataclasses: subsystems, modules, backlog
│   ├── port_manifest.py  # Python workspace structure summary
│   ├── query_engine.py   # Renders porting summary from active workspace
│   ├── task.py           # Task orchestration primitives
│   └── tools.py          # Tool port metadata
├── tests/                # unittest-based verification
└── assets/
```

---

## Key CLI Commands

All commands run via `python3 -m src.main <subcommand>`.

```bash
# Print a human-readable porting summary
python3 -m src.main summary

# Print the current Python workspace manifest
python3 -m src.main manifest

# List current Python modules/subsystems (paginated)
python3 -m src.main subsystems --limit 16

# Inspect mirrored command inventory
python3 -m src.main commands --limit 10

# Inspect mirrored tool inventory
python3 -m src.main tools --limit 10

# Run parity audit against local ignored archive (when present)
python3 -m src.main parity-audit

# Run the full test suite
python3 -m unittest discover -s tests -v
```

---

## Core Data Models (`src/models.py`)

The dataclasses define the shape of the porting workspace:

```python
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Module:
    name: str
    status: str          # e.g. "ported", "stub", "backlog"
    source_path: str
    notes: Optional[str] = None

@dataclass
class Subsystem:
    name: str
    modules: List[Module] = field(default_factory=list)
    description: Optional[str] = None

@dataclass
class PortManifest:
    subsystems: List[Subsystem] = field(default_factory=list)
    backlog: List[str] = field(default_factory=list)
    version: str = "0.1.0"
```

---

## Tools System (`src/tools.py`)

Tools are the callable units in the agent harness. Each tool entry carries metadata for dispatch:

```python
from dataclasses import dataclass
from typing import Callable, Optional, Any, Dict

@dataclass
class Tool:
    name: str
    description: str
    parameters: Dict[str, Any]          # JSON-schema style param spec
    handler: Optional[Callable] = None  # Python callable for this tool

# Example: registering a tool
def read_file_handler(path: str) -> str:
    with open(path, "r") as f:
        return f.read()

READ_FILE_TOOL = Tool(
    name="read_file",
    description="Read the contents of a file at the given path.",
    parameters={
        "path": {"type": "string", "description": "Absolute or relative file path"}
    },
    handler=read_file_handler,
)

# Tool registry pattern
TOOL_REGISTRY: Dict[str, Tool] = {
    READ_FILE_TOOL.name: READ_FILE_TOOL,
}

def dispatch_tool(name: str, **kwargs) -> Any:
    tool = TOOL_REGISTRY.get(name)
    if tool is None:
        raise ValueError(f"Unknown tool: {name}")
    if tool.handler is None:
        raise NotImplementedError(f"Tool '{name}' has no handler yet.")
    return tool.handler(**kwargs)
```

---

## Commands System (`src/commands.py`)

Commands are higher-level agent actions, distinct from raw tools:

```python
from dataclasses import dataclass
from typing import Optional, Callable, Any

@dataclass
class Command:
    name: str
    description: str
    aliases: list
    handler: Optional[Callable] = None

# Example command
def summarize_handler(context: dict) -> str:
    return f"Summarizing {len(context.get('files', []))} files."

SUMMARIZE_COMMAND = Command(
    name="summarize",
    description="Summarize the current workspace context.",
    aliases=["sum", "overview"],
    handler=summarize_handler,
)

COMMAND_REGISTRY = {
    SUMMARIZE_COMMAND.name: SUMMARIZE_COMMAND,
}

def run_command(name: str, context: dict) -> Any:
    cmd = COMMAND_REGISTRY.get(name)
    if not cmd:
        raise ValueError(f"Unknown command: {name}")
    if not cmd.handler:
        raise NotImplementedError(f"Command '{name}' not yet implemented.")
    return cmd.handler(context)
```

---

## Task Orchestration (`src/task.py`)

Tasks wrap a unit of agent work — a goal, a set of tools, and a result:

```python
from dataclasses import dataclass, field
from typing import List, Optional, Any

@dataclass
class TaskResult:
    success: bool
    output: Any
    error: Optional[str] = None

@dataclass
class Task:
    goal: str
    tools: List[str] = field(default_factory=list)   # tool names available
    context: dict = field(default_factory=dict)
    result: Optional[TaskResult] = None

    def run(self, dispatcher) -> TaskResult:
        """
        dispatcher: callable(tool_name, **kwargs) -> Any
        Implement your agent loop here.
        """
        try:
            # Minimal stub: just report goal received
            output = f"Task received: {self.goal}"
            self.result = TaskResult(success=True, output=output)
        except Exception as e:
            self.result = TaskResult(success=False, output=None, error=str(e))
        return self.result

# Usage
from src.tools import dispatch_tool

task = Task(
    goal="Read README.md and summarize it",
    tools=["read_file"],
    context={"working_dir": "."},
)
result = task.run(dispatcher=dispatch_tool)
print(result.output)
```

---

## Query Engine (`src/query_engine.py`)

The query engine renders a porting summary from the active manifest:

```python
from src.port_manifest import build_manifest
from src.query_engine import render_summary

manifest = build_manifest()
summary = render_summary(manifest)
print(summary)
```

You can also invoke it from the CLI:

```bash
python3 -m src.main summary
```

---

## Port Manifest (`src/port_manifest.py`)

Build and inspect the current workspace manifest programmatically:

```python
from src.port_manifest import build_manifest

manifest = build_manifest()

for subsystem in manifest.subsystems:
    print(f"[{subsystem.name}]")
    for module in subsystem.modules:
        print(f"  {module.name}: {module.status}")

print("Backlog:", manifest.backlog)
```

---

## Adding a New Tool

1. Define a handler function in `src/tools.py`.
2. Create a `Tool` dataclass instance.
3. Register it in `TOOL_REGISTRY`.
4. Write a test in `tests/`.

```python
# src/tools.py

def list_dir_handler(path: str):
    import os
    return os.listdir(path)

LIST_DIR_TOOL = Tool(
    name="list_dir",
    description="List files in a directory.",
    parameters={"path": {"type": "string"}},
    handler=list_dir_handler,
)

TOOL_REGISTRY["list_dir"] = LIST_DIR_TOOL
```

---

## Adding a New Command

```python
# src/commands.py

def lint_handler(context: dict) -> str:
    files = context.get("files", [])
    return f"Linting {len(files)} files (stub)."

LINT_COMMAND = Command(
    name="lint",
    description="Lint the current workspace files.",
    aliases=["check"],
    handler=lint_handler,
)

COMMAND_REGISTRY["lint"] = LINT_COMMAND
```

---

## Running Tests

```bash
# Run all tests with verbose output
python3 -m unittest discover -s tests -v

# Run a specific test file
python3 -m unittest tests.test_tools -v
```

Example test pattern:

```python
# tests/test_tools.py
import unittest
from src.tools import dispatch_tool
import tempfile, os

class TestReadFileTool(unittest.TestCase):
    def test_read_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("hello clawd")
            path = f.name
        try:
            result = dispatch_tool("read_file", path=path)
            self.assertEqual(result, "hello clawd")
        finally:
            os.unlink(path)

if __name__ == "__main__":
    unittest.main()
```

---

## Parity Audit

When a local ignored archive of the original snapshot is present, run:

```bash
python3 -m src.main parity-audit
```

This compares the current Python workspace surface against the archived root-entry file surface, subsystem names, and command/tool inventories, reporting gaps.

---

## Common Patterns

### Chaining tools in a task loop

```python
from src.tools import dispatch_tool
from src.task import Task

task = Task(
    goal="Read and list files",
    tools=["read_file", "list_dir"],
    context={"working_dir": "."},
)

# Manual tool chain (before full agent loop is implemented)
files = dispatch_tool("list_dir", path=".")
for fname in files[:3]:
    content = dispatch_tool("read_file", path=fname)
    print(f"--- {fname} ---\n{content[:200]}")
```

### Using the manifest in automation

```python
from src.port_manifest import build_manifest

def unported_modules():
    manifest = build_manifest()
    stubs = []
    for sub in manifest.subsystems:
        for mod in sub.modules:
            if mod.status != "ported":
                stubs.append((sub.name, mod.name, mod.status))
    return stubs

for subsystem, module, status in unported_modules():
    print(f"{subsystem}/{module} → {status}")
```

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError: src` | Run commands from the repo root, not inside `src/` |
| `NotImplementedError: Tool 'x' has no handler` | The tool is registered but the Python handler hasn't been written yet — implement `handler` in `tools.py` |
| `parity-audit` does nothing | The local ignored archive must be present at the expected path; see `port_manifest.py` for the expected location |
| Tests not discovered | Ensure test files are named `test_*.py` and located in `tests/` |
| Import errors after adding a module | Add `__init__.py` to any new package subdirectory |

---

## Key Links

- **Repository:** https://github.com/instructkr/clawd-code
- **oh-my-codex (OmX):** https://github.com/Yeachan-Heo/oh-my-codex
- **Related essay:** [Is legal the same as legitimate?](https://writings.hongminhee.org/2026/03/legal-vs-legitimate/)
- **Not affiliated with Anthropic.**
