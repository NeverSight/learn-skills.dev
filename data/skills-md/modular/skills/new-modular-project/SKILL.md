---
name: new-modular-project
description: Creates a new Mojo or MAX project. Use when wanting to start a new Mojo or MAX project, initializing the Pixi or UV environment to use Mojo or MAX, or when the user wants to begin a new Mojo or MAX project from scratch.
---

When the user wants to create a new project, first infer as many options as
possible from the user's request (e.g., "new Mojo project" means type=Mojo,
"called foo" means name=foo). Then use a structured multiple-choice prompt (not
plain text) to gather only the **remaining unspecified** options in a single
interaction. Do NOT ask about options the user has already provided or implied.
The options to determine are:
1. **Project name** — ask if not specified
2. **Type of project** — Mojo or MAX (infer from context if the user said "Mojo project" or "MAX project")
3. **Environment manager** — Pixi (recommended) or uv
4. **If uv**: **UV project type** — full uv project (`uv init` + `uv add`, recommended) or quick uv environment (`uv venv` + `uv pip install`, lighter weight)
5. **Channel** — nightly (latest features, recommended) or stable (production) 

Then follow the appropriate section below (Pixi or uv) to initialize the
project and choose `max` or `mojo` as appropriate. For stable versions in the
below examples, `mojo` will start with a 0. prefix (0.26.1.0.0.0) where `max`
packages will not (26.1.0.0.0).

NOTE: Do not look for or use `magic` for Mojo or MAX projects, it is no longer
supported. Pixi has fully replaced its capabilities.

---

## Pixi (Recommended)

Pixi manages Python, Mojo, and other dependencies in a reproducible
manner inside a controlled environment.

First, determine if `pixi` is installed. If it is not available for use at the
command line, install it using the latest instructions found on
https://pixi.prefix.dev/latest/#installation

You may need to place the `pixi` tool in the local shell environment after
installation if it had not already been installed.

### Nightly

```bash
# New project
pixi init [PROJECT] \
  -c https://conda.modular.com/max-nightly/ -c conda-forge \
  && cd [PROJECT]
pixi add [max / mojo]
pixi shell

# Existing project - add to pixi.toml channels first:
# [workspace]
# channels = ["https://conda.modular.com/max-nightly/", "conda-forge"]
pixi add [max / mojo]
```

### Stable (v26.1.0.0.0)

```bash
# New project
pixi init [PROJECT] \
  -c https://conda.modular.com/max/ -c conda-forge \
  && cd [PROJECT]
pixi add "[max / mojo]==0.26.1.0.0.0"
pixi shell

# Existing project
pixi add "[max / mojo]==0.26.1.0.0.0"
```

---

## uv

uv is a fast and very popular package manager, familiar to developers coming
from a Python background. It also works well with Mojo projects.

### Nightly (project)

```bash
uv init [PROJECT] && cd [PROJECT]
uv add [max / mojo] \
  --index https://whl.modular.com/nightly/simple/ \
  --prerelease allow
```

### Stable (project)

```bash
uv init [PROJECT] && cd [PROJECT]
uv add [max / mojo] \
  --extra-index-url https://modular.gateway.scarf.sh/simple/
```

### Nightly (quick environment)

```bash
mkdir [PROJECT] && cd [PROJECT]
uv venv
uv pip install [max / mojo] \
  --index https://whl.modular.com/nightly/simple/ \
  --prerelease allow
```

### Stable (quick environment)

```bash
mkdir [PROJECT] && cd [PROJECT]
uv venv
uv pip install [max / mojo] \
  --extra-index-url https://modular.gateway.scarf.sh/simple/
```

When using `uv`, you can use `max` or `mojo` directly by working within the project environment:

```bash
 source .venv/bin/activate
```

---

## pip

Standard Python package manager.

### Nightly

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install --pre [max / mojo] \
  --index https://whl.modular.com/nightly/simple/
```

### Stable

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install [max / mojo] \
  --extra-index-url https://modular.gateway.scarf.sh/simple/
```

---

## Conda

For conda/mamba users.

### Nightly

```bash
conda install -c conda-forge \
  -c https://conda.modular.com/max-nightly/ [max / mojo]
```

### Stable (v26.1.0.0.0)

```bash
conda install -c conda-forge \
  -c https://conda.modular.com/max/ "[max / mojo]==0.26.1.0.0.0"
```

---

## Version Alignment with MAX

If using MAX with custom Mojo kernels, versions must match:

```bash
# Check alignment
uv pip show mojo | grep Version   # e.g., 0.26.2
pixi run mojo --version           # Must match major.minor (e.g., 0.26.2)
```

Mismatched versions cause kernel compilation failures. Always use the same channel (stable or nightly) for both.

---

## References

- [Mojo Installation Guide](https://docs.modular.com/mojo/manual/install)
- [Mojo Stable Docs](https://docs.modular.com/stable/mojo/)
- [Mojo Nightly Docs](https://docs.modular.com/mojo/)
