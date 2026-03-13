---
name: bootstrap-python-service
description: Bootstrap Python FastAPI services on macOS using uv with consistent project and workspace scaffolds. Use when creating a new backend/API service from scratch, scaffolding a single uv service project, scaffolding a uv workspace with package/service members, customizing scaffold defaults through layered YAML profiles, initializing pytest+ruff+mypy defaults, creating README.md, initializing git, and running initial validation commands.
---

# Bootstrap Python Service

## Purpose

Create production-oriented FastAPI starter layouts using one direct shell entrypoint backed by the shared `bootstrap-uv-python-workspace` scaffolding scripts.

## When To Use

- Use this skill for new FastAPI service scaffolds.
- Use this skill when the user wants either a single service project or a workspace with service members.
- Hand off to `bootstrap-uv-python-workspace` only when the task is generic `uv` scaffolding without FastAPI-specific expectations.

## Single-Path Workflow

1. Collect the required inputs:
   - `name`
   - `mode`
   - `path`
   - optional `python`, `members`, `profile_map`, `force`, `initial_commit`, `no_git_init`
2. Run the canonical entrypoint:
   ```bash
   scripts/init_python_service.sh --name <name> --mode <project|workspace>
   ```
3. Let the script delegate to the shared `bootstrap-uv-python-workspace` scaffolding layer.
4. Accept the built-in validation path:
   - `uv run pytest`
   - `uv run ruff check .`
   - `uv run mypy .`
5. Return the generated path plus the exact next-step run and check commands emitted by the script.

## Commands

```bash
# Project mode (default)
scripts/init_python_service.sh --name my-service

# Project mode with explicit options
scripts/init_python_service.sh --name my-service --mode project --python 3.13 --path /tmp/my-service

# Workspace mode with defaults (core-lib package + api-service service)
scripts/init_python_service.sh --name platform --mode workspace

# Workspace mode with explicit members and profile mapping
scripts/init_python_service.sh \
  --name platform \
  --mode workspace \
  --members "core-lib,billing-service,orders-service" \
  --profile-map "core-lib=package,billing-service=service,orders-service=service"

# Allow non-empty target directory
scripts/init_python_service.sh --name my-service --force

# Skip git initialization
scripts/init_python_service.sh --name my-service --no-git-init

# Create initial commit
scripts/init_python_service.sh --name my-service --initial-commit
```

## Inputs

- `name`: required
- `mode`: `project` or `workspace`; defaults to `project`
- `path`: optional target directory; defaults to `./<name>`
- `python`: optional Python version; defaults to `3.13`
- `members`: optional workspace member CSV for workspace mode
- `profile_map`: optional workspace profile CSV for workspace mode
- `force`: optional flag allowing non-empty target directories
- `initial_commit`: optional flag creating an initial commit after a successful scaffold
- `no_git_init`: optional flag disabling git initialization

## Outputs

- `status`
  - `success`: scaffold and built-in validation completed
  - `blocked`: prerequisites or target-directory constraints prevented the run
  - `failed`: the script started but validation or generation failed
- `path_type`
  - `primary`: the canonical shell entrypoint completed
- `output`
  - resolved project or workspace path
  - emitted run commands
  - emitted validation commands

## Defaults

- mode: `project`
- Python version: `3.13`
- quality tooling: `pytest`, `ruff`, `mypy`
- workspace default members: `core-lib,api-service`
- workspace default profiles: first member `package`, remaining members `service`

## Guardrails

- Refuse non-empty target directories unless `--force` is set.
- Require `uv` and `git` unless git initialization was explicitly disabled.
- Fail when workspace-only options are used in project mode.
- Fail when `--initial-commit` is combined with `--no-git-init`.

## FastAPI Guidance

Use uv FastAPI integration style as primary guidance:

```bash
uv add fastapi --extra standard
uv run fastapi dev app/main.py
# optional production-style local run
uv run fastapi run app/main.py
```

## Fallbacks and Handoffs

- The preferred path is always `scripts/init_python_service.sh`.
- Use `bootstrap-uv-python-workspace` directly only when FastAPI-specific behavior is not wanted.
- Recommend `bootstrap-python-mcp-service` instead when the user wants a FastMCP server rather than an HTTP API service.

## Automation Suitability

- Codex App automation: Medium. Useful for recurring FastAPI scaffold smoke checks and regression checks.
- Codex CLI automation: High. Strong fit for CI or scheduled scaffolder reliability checks.

## Codex App Automation Prompt Template

```markdown
Use $bootstrap-python-service.

Scope boundaries:
- Work only inside <REPO_PATH>.
- Create or validate scaffold output only in <TARGET_PATH>.
- Limit activity to scaffolding and verification; no unrelated refactors.

Task:
1. If <MODE:PROJECT|WORKSPACE> is PROJECT, run:
   `scripts/init_python_service.sh --name <SERVICE_NAME> --mode project --path <TARGET_PATH> --python <PYTHON_VERSION> <FORCE_FLAG> <GIT_INIT_MODE>`
2. If <MODE:PROJECT|WORKSPACE> is WORKSPACE, run:
   `scripts/init_python_service.sh --name <SERVICE_NAME> --mode workspace --path <TARGET_PATH> --python <PYTHON_VERSION> --members "<MEMBERS_CSV>" --profile-map "<PROFILE_MAP>" <FORCE_FLAG> <GIT_INIT_MODE>`
3. Validate generated checks:
   - `uv run pytest`
   - `uv run ruff check .`
   - `uv run mypy .`
4. If mode is PROJECT, also validate generated run commands:
   - `uv run fastapi dev app/main.py`
   - `uv run fastapi run app/main.py`

Output contract:
1. STATUS: PASS or FAIL
2. GENERATED_PATH: final output path
3. COMMANDS: exact commands executed
4. RESULTS: concise check outputs
5. If FAIL: short root-cause summary and minimal remediation steps
```

## Codex CLI Automation Prompt Template

```bash
codex exec --full-auto --sandbox workspace-write --cd "<REPO_PATH>" "<PROMPT_BODY>"
```

Optional machine-readable variant:

```bash
codex exec --json --full-auto --sandbox workspace-write --cd "<REPO_PATH>" "<PROMPT_BODY>"
```

`<PROMPT_BODY>` template:

```markdown
Use $bootstrap-python-service.
Scope is scaffolding plus verification only in <TARGET_PATH> under <REPO_PATH>.
Run the scaffold command for <MODE:PROJECT|WORKSPACE>, then run pytest, ruff, and mypy.
If project mode, confirm FastAPI dev/run commands are valid.
Return STATUS, generated path, exact command transcript, and minimal remediation on failure.
```

## Customization Placeholders

- `<REPO_PATH>`
- `<SERVICE_NAME>`
- `<MODE:PROJECT|WORKSPACE>`
- `<TARGET_PATH>`
- `<PYTHON_VERSION>`
- `<MEMBERS_CSV>`
- `<PROFILE_MAP>`
- `<FORCE_FLAG>`
- `<GIT_INIT_MODE>`

## Interactive Customization Workflow

1. Ask for mode, name, path, Python version, and git/force flags.
2. If workspace mode, also ask for members and profile map.
3. Return both:
- A YAML profile for durable reuse.
- The exact scaffold command to run.
4. Use this precedence order:
- CLI flags
- `--config` profile file
- `.codex/profiles/bootstrap-python-service/customization.yaml`
- `~/.config/gaelic-ghost/python-skills/bootstrap-python-service/customization.yaml`
- Script defaults
5. If users want temporary reset behavior:
- `--bypassing-all-profiles`
- `--bypassing-repo-profile`
- `--deleting-repo-profile`
6. If users provide no customization or profile files, keep existing script defaults unchanged.
7. See [`references/interactive-customization.md`](references/interactive-customization.md) for schema and examples.

## References

- `references/conventions.md`
- `references/customization.md`
- `references/interactive-customization.md`

## Script Inventory

- `scripts/init_python_service.sh`
- Delegates to the shared workspace bootstrap scripts shipped by `bootstrap-uv-python-workspace`.

## Assets

- `assets/README.md.tmpl`
