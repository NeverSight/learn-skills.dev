---
name: tiangolo-library-skills
description: Install and manage AI agent skills from Python/JS libraries so agents always use up-to-date patterns
triggers:
  - install library skills for my project
  - set up agent skills from dependencies
  - add library skills for Claude Code
  - update agent skills for my libraries
  - use library-skills to configure my AI agent
  - install FastAPI skills for my agent
  - set up .agents directory with library skills
  - run library-skills to scan dependencies
---

# Library Skills

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Library Skills lets AI coding agents use libraries as intended — always up to date. Libraries (e.g. FastAPI, Streamlit) embed official AI skills in each release, and `library-skills` discovers those installed packages and wires their skills into your project's `.agents` directory as symbolic links. When you upgrade a library, its skills update automatically.

---

## Installation & Quick Start

No global install required. Run directly with `uvx` (Python) or `npx` (JavaScript/TypeScript):

```bash
# Python projects
uvx library-skills

# JavaScript/TypeScript projects
npx library-skills
```

For Claude Code (which doesn't yet support the standard `.agents` directory):

```bash
uvx library-skills --claude
# Also installs into .claude/skills in addition to .agents
```

---

## What It Does

1. Scans your project's installed dependencies (e.g. from the active virtualenv or `node_modules`)
2. Finds libraries that publish their own skills at [agentskills.io](https://agentskills.io)
3. Prompts you to select which skills to install
4. Creates symbolic links under `.agents/` (and optionally `.claude/skills/`) pointing into the installed package

Because they are symlinks, upgrading the library (e.g. `pip install -U fastapi`) automatically updates the skill content — no need to re-run `library-skills`.

---

## CLI Reference

```bash
uvx library-skills [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--claude` | Also install skills in `.claude/skills/` for Claude Code compatibility |
| `--help` | Show help message and exit |

---

## Directory Structure After Installation

```
my-project/
├── .agents/
│   └── fastapi -> /path/to/venv/lib/python3.x/site-packages/fastapi/skills/
├── .claude/
│   └── skills/
│       └── fastapi -> /path/to/venv/lib/python3.x/site-packages/fastapi/skills/
├── src/
│   └── main.py
└── pyproject.toml
```

---

## Python Project Workflow

### 1. Create and activate a virtualenv with your dependencies

```bash
uv venv
source .venv/bin/activate
uv add fastapi streamlit
```

### 2. Run library-skills

```bash
uvx library-skills
# → Scans .venv, finds fastapi, streamlit with embedded skills
# → Prompts: Install fastapi skills? [Y/n]
# → Creates .agents/fastapi -> .venv/lib/.../fastapi/skills/
```

### 3. For Claude Code users

```bash
uvx library-skills --claude
# → Creates .agents/fastapi AND .claude/skills/fastapi
```

---

## JavaScript/TypeScript Project Workflow

### 1. Install dependencies

```bash
npm install
# or
pnpm install
```

### 2. Run library-skills

```bash
npx library-skills
# or with Claude support
npx library-skills --claude
```

---

## Real Code Example: FastAPI with Up-to-Date Skills

After installing FastAPI skills, your agent will use current patterns, not deprecated ones.

```python
# main.py — agent uses skills to write correct, modern FastAPI code
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
async def create_item(item: Item):
    return item
```

With skills installed, the agent reads the embedded SKILL.md from the FastAPI package and applies the documented patterns — including any new features added in the latest release.

---

## How Library Authors Publish Skills

If you are a library author who wants to embed skills in your package:

1. Create a `skills/SKILL.md` (or similar) inside your package directory
2. Publish the package to PyPI or npm
3. Register at [agentskills.io](https://agentskills.io) so `library-skills` can discover it

```
my-library/
├── my_library/
│   ├── __init__.py
│   └── skills/
│       └── SKILL.md   ← embedded skill, shipped with every release
├── pyproject.toml
└── README.md
```

---

## Common Patterns

### Re-running after upgrading libraries

Skills update automatically via symlinks. But if you add new libraries that have skills, re-run:

```bash
uvx library-skills
```

### Committing `.agents/` to version control

Symlinks can be committed so the whole team benefits:

```bash
git add .agents/
git commit -m "Add library skills for fastapi"
```

Teammates need the same virtualenv path for symlinks to resolve, so consider using relative symlinks or documenting the setup.

### Checking which skills are installed

```bash
ls -la .agents/
# fastapi -> /home/user/project/.venv/lib/python3.12/site-packages/fastapi/skills
# streamlit -> /home/user/project/.venv/lib/python3.12/site-packages/streamlit/skills
```

---

## Troubleshooting

### `uvx library-skills` finds no skills

- Make sure you have a virtualenv activated (or the packages are installed in the current environment)
- The library must ship its own skills — not all libraries do yet; check [agentskills.io](https://agentskills.io)

### Symlinks are broken after moving the project

Symlinks are absolute by default. Re-run `uvx library-skills` from the new location to recreate them.

### Claude Code doesn't load skills from `.agents/`

Use the `--claude` flag to also install into `.claude/skills/`:

```bash
uvx library-skills --claude
```

### Skills are stale after `pip install -U fastapi`

Skills update automatically via symlinks — no action needed. If they don't, verify the symlink target points into the virtualenv:

```bash
readlink .agents/fastapi
```

---

## Key Concepts

| Concept | Explanation |
|---------|-------------|
| **Library Skill** | A `SKILL.md` (or similar file) shipped inside a library package |
| **`.agents/` directory** | Standard location where agent skills are discovered by AI coding tools |
| **Symlink** | `library-skills` uses symlinks so skills stay in sync with installed library version |
| **agentskills.io** | Registry of libraries that publish agent skills |
| **`--claude`** | Flag to also populate `.claude/skills/` for Claude Code compatibility |

---

## Links

- **Documentation**: [https://library-skills.io](https://library-skills.io)
- **Source Code**: [https://github.com/tiangolo/library-skills](https://github.com/tiangolo/library-skills)
- **Skills Registry**: [https://agentskills.io](https://agentskills.io)
- **PyPI**: [https://pypi.org/project/library-skills](https://pypi.org/project/library-skills)
- **npm**: [https://www.npmjs.com/package/library-skills](https://www.npmjs.com/package/library-skills)
