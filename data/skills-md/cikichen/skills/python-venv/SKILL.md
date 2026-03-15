---
name: python-venv
description: "Python environment management skill. Automatically detect project type and existing environments, recommend based on popularity. Minimize interruptions, only ask when necessary."
---

# Python Environment Management Skill

## Core Principles

1. **Reuse Existing Environments** - Don't recreate, reuse existing virtual environments
2. **Use Project-Type Decision** - Auto-select based on lock files
3. **Recommend by Popularity** - uv > pip > conda > venv
4. **Minimize Interruption** - Only ask when necessary

---

## Tool Popularity Ranking

| Priority | Tool | Best For |
|----------|------|----------|
| 🥇 | uv | New projects, fast installs |
| 🥈 | pip | Compatibility first |
| 🥉 | conda | Data science, specific versions |
| 4 | venv | Built-in, no extra install |
| 5 | poetry | Existing poetry.lock |
| 6 | pipenv | Existing Pipfile (declining) |

---

## Decision Flow

```
┌─────────────────────────────────────┐
│  Detect project dependency files     │
└─────────────────────────────────────┘
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
  Clear decision       Unclear
    ↓                   ↓
  Use directly     Detect existing env
                        ↓
                  ┌─────┴─────┐
                  ↓           ↓
              Has env        No env
                  ↓           ↓
              Reuse      Assess complexity
                            ↓
                  ┌─────────┴─────────┐
                  ↓                   ↓
              Simple task       Needs deps
                  ↓                   ↓
            System Python      Recommend uv/conda
```

---

## 1. Clear Decisions (Execute Directly, No Ask)

When these files are detected, use the corresponding tool directly:

| Detected File | Execute |
|--------------|---------|
| `uv.lock` exists | `uv sync` or `uv pip install -r requirements.txt` |
| `poetry.lock` exists | `poetry install` |
| `environment.yml` exists | `conda env create -f environment.yml` |
| `Pipfile.lock` exists | `pipenv install` |

---

## 2. Detect Existing Environments (Reuse First)

```bash
# Priority: uv venv > conda > venv

# 2.1 Detect uv virtual environment
ls -la .venv/ 2>/dev/null && uv pip list 2>/dev/null | head -3

# 2.2 Detect conda environment
conda info --envs 2>/dev/null | grep "*" || echo $CONDA_PREFIX

# 2.3 Detect standard venv
ls -la venv/ .venv/ env/ 2>/dev/null

# 2.4 If exists → Reuse (activate and run commands)
```

**Reuse Example:**
```
Detected existing .venv/ directory
→ Activate: source .venv/bin/activate
→ Run: uv pip install <package>
```

---

## 3. When Unclear (Assess Complexity)

| Scenario | Action |
|----------|--------|
| Stdlib only, no 3rd party | System Python (python3) |
| Simple pip install test | System Python (temp) |
| Has requirements.txt | Recommend uv > pip > venv |
| Has pyproject.toml | Recommend uv > pip |
| Multi-file project, needs isolation | Recommend uv |

---

## 4. When to Ask User (Only These Cases)

✅ **Ask:**
1. Empty project + first dependency install → Ask which tool
2. Both requirements.txt + pyproject.toml → Ask which to use
3. User explicitly wants different tool → e.g., "I want conda"

❌ **Don't Ask:**
- Has uv.lock but user didn't specify
- Has .venv/ directory
- Regular pip install task

---

## 5. Recommended Tool (No Clear Directive)

```
First: uv
  ├── uv venv (create)
  ├── uv pip install (install)
  └── uv sync (sync)

Backup: pip
  ├── python3 -m venv .venv
  └── pip install

Special: conda
  ├── conda create -n envname python=x.x
  └── conda env create
```

---

## Detection Commands

```bash
# Check available tools
which uv
which conda
which pip
which python3

# Check project files
ls -la *.lock pyproject.toml requirements.txt environment.yml Pipfile 2>/dev/null

# Check existing environments
ls -la .venv/ venv/ env/ 2>/dev/null
conda info --envs 2>/dev/null

# Check current environment
echo $VIRTUAL_ENV
echo $CONDA_PREFIX
```

---

## Interaction Examples (Only When Needed)

```
🔍 Detection result:
- Project file: pyproject.toml
- Existing env: None
- Recommended: uv (fastest)

Running: uv pip install <package>
```

```
🔍 Detection result:
- Project file: requirements.txt
- Existing env: None
- Recommended: uv

Available options:
1) uv (recommended) - faster
2) pip - better compatibility
3) venv - uses stdlib
4) conda - if specific version needed

Enter option or press Enter to use recommended:
```

---

## Quick Command Reference

| Action | uv | pip | conda | venv |
|--------|-----|-----|-------|------|
| Create env | `uv venv` | - | `conda create` | `python3 -m venv` |
| Install pkg | `uv pip install` | `pip install` | `conda install` | `pip install` |
| Install deps | `uv sync` | `pip install -r` | `conda env create` | `pip install -r` |
| Activate | (auto) | (auto) | `conda activate` | `source venv/bin/activate` |

---

## Core Principle

**"Do more, ask less"** - Execute directly when you can determine, only ask when truly unclear.
