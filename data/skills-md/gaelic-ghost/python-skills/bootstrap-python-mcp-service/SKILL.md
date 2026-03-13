---
name: bootstrap-python-mcp-service
description: Bootstrap Python MCP server projects and workspaces on macOS using uv and FastMCP with consistent defaults. Use when creating a new MCP server from scratch, scaffolding a single uv MCP project, scaffolding a uv workspace with package/service members, customizing scaffold defaults through layered YAML profiles, initializing pytest+ruff+mypy defaults, creating README.md, initializing git, running initial validation checks, or starting from OpenAPI/FastAPI with MCP mapping guidance.
---

# Bootstrap Python MCP Service

## Purpose

Create FastMCP starter layouts using one direct shell entrypoint backed by the shared `bootstrap-uv-python-workspace` scaffolding scripts plus deterministic MCP overlay logic.

## When To Use

- Use this skill for new FastMCP server scaffolds.
- Use this skill when the user wants OpenAPI or FastAPI-to-MCP mapping guidance alongside bootstrap.
- Recommend `bootstrap-python-service` when the user wants a FastAPI service but not an MCP server.

## Single-Path Workflow

1. Collect the required inputs:
   - `name`
   - `mode`
   - `path`
   - optional `python`, `members`, `profile_map`, `force`, `initial_commit`, `no_git_init`
2. Run the canonical entrypoint:
   ```bash
   scripts/init_fastmcp_service.sh --name <name> --mode <project|workspace>
   ```
3. Let the script delegate to the shared `bootstrap-uv-python-workspace` scaffolding layer, then apply the FastMCP overlay.
4. Accept the built-in validation path:
   - `uv run pytest`
   - `uv run ruff check .`
   - `uv run mypy .`
5. If the task starts from an existing API, optionally generate a mapping report with `uv run python scripts/assess_api_for_mcp.py ...`.
6. Return the generated path plus the exact next-step commands emitted by the script.

## Commands

```bash
# Project mode (default)
scripts/init_fastmcp_service.sh --name my-mcp-server

# Project mode with explicit options
scripts/init_fastmcp_service.sh --name my-mcp-server --mode project --python 3.13 --path /tmp/my-mcp-server

# Workspace mode with defaults (core-lib package + api-service service)
scripts/init_fastmcp_service.sh --name platform --mode workspace

# Workspace mode with explicit members and profile mapping
scripts/init_fastmcp_service.sh \
  --name platform \
  --mode workspace \
  --members "core-lib,tools-service,ops-service" \
  --profile-map "core-lib=package,tools-service=service,ops-service=service"

# Allow non-empty target directory
scripts/init_fastmcp_service.sh --name my-mcp-server --force

# Skip git initialization
scripts/init_fastmcp_service.sh --name my-mcp-server --no-git-init

# Create initial commit
scripts/init_fastmcp_service.sh --name my-mcp-server --initial-commit

# Generate MCP mapping guidance from OpenAPI
uv run python scripts/assess_api_for_mcp.py --openapi ./openapi.yaml --out ./mcp_mapping_report.md

# Generate MCP mapping guidance from existing FastAPI app
uv run python scripts/assess_api_for_mcp.py --fastapi app.main:app --out ./mcp_mapping_report.md
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
  - optional mapping-report path

## Defaults

- mode: `project`
- Python version: `3.13`
- quality tooling: `pytest`, `ruff`, `mypy`
- workspace default members: `core-lib,api-service`
- workspace default profiles: first member `package`, remaining members `service`

## Base UV/FastAPI Guidance

The shared scaffold basis follows uv FastAPI integration style:

```bash
uv add fastapi --extra standard
uv run fastapi dev app/main.py
```

This skill then overlays FastMCP dependencies and server files for MCP service members.

## API Import Guidance

When starting from OpenAPI or FastAPI, bootstrap first, then map endpoints to MCP primitives:

1. Generate mapping report with `scripts/assess_api_for_mcp.py`.
2. Classify endpoints into `Resources`, `Tools`, and `Prompts`.
3. Recommend RouteMaps/Transforms only when they improve usability.
4. Keep bootstrap deterministic; defer heavy custom mapping unless requested.

## FastMCP Docs Lookup

Use the `fastmcp_docs` MCP server for up-to-date framework details.

Suggested queries:

- `FastMCP quickstart server example`
- `FastMCP tools resources prompts best practices`
- `FastMCP RouteMap Transform`
- `FastMCP from OpenAPI`
- `FastMCP from FastAPI`

## Guardrails

- Refuse non-empty target directories unless `--force` is set.
- Require at least one service profile member in workspace mode.
- Require `uv` and `git` unless git initialization was explicitly disabled.
- Fail when workspace-only options are used in project mode.
- Fail when `--initial-commit` is combined with `--no-git-init`.

## Fallbacks and Handoffs

- The preferred path is always `scripts/init_fastmcp_service.sh`.
- Use `bootstrap-python-service` when the user wants FastAPI-only output.
- Use `bootstrap-uv-python-workspace` directly only when FastMCP-specific behavior is not wanted.

## Automation Suitability

- Codex App automation: Medium. Useful for recurring FastMCP scaffold checks and mapping-assessment checks.
- Codex CLI automation: High. Strong fit for CI-style scaffold validation.

## Codex App Automation Prompt Template

```markdown
Use $bootstrap-python-mcp-service.

Scope boundaries:
- Work only inside <REPO_PATH>.
- Create or validate scaffold output only in <TARGET_PATH>.
- Restrict work to scaffold generation, optional mapping report generation, and verification.

Task:
1. If <MODE:PROJECT|WORKSPACE> is PROJECT, run:
   `scripts/init_fastmcp_service.sh --name <MCP_SERVICE_NAME> --mode project --path <TARGET_PATH> --python <PYTHON_VERSION> <FORCE_FLAG> <GIT_INIT_MODE>`
2. If <MODE:PROJECT|WORKSPACE> is WORKSPACE, run:
   `scripts/init_fastmcp_service.sh --name <MCP_SERVICE_NAME> --mode workspace --path <TARGET_PATH> --python <PYTHON_VERSION> --members "<MEMBERS_CSV>" --profile-map "<PROFILE_MAP>" <FORCE_FLAG> <GIT_INIT_MODE>`
3. If <GENERATE_MAPPING_REPORT:TRUE|FALSE> is TRUE:
   - If <MAPPING_INPUT_MODE:NONE|OPENAPI|FASTAPI_IMPORT> is OPENAPI, run:
     `uv run python scripts/assess_api_for_mcp.py --openapi <MAPPING_INPUT_PATH> --out <TARGET_PATH>/mcp_mapping_report.md`
   - If <MAPPING_INPUT_MODE:NONE|OPENAPI|FASTAPI_IMPORT> is FASTAPI_IMPORT, run:
     `uv run python scripts/assess_api_for_mcp.py --fastapi <MAPPING_INPUT_PATH> --out <TARGET_PATH>/mcp_mapping_report.md`
4. Run verification checks in <TARGET_PATH>:
   - `uv run pytest`
   - `uv run ruff check .`
   - `uv run mypy .`

Output contract:
1. STATUS: PASS or FAIL
2. COMMANDS: exact commands executed
3. RESULTS: concise outcomes for scaffold and checks
4. If report generated: include report path
5. If FAIL: provide likely root cause and minimal remediation
```

## Codex CLI Automation Prompt Template

```bash
codex exec --full-auto --sandbox workspace-write --cd "<REPO_PATH>" "<PROMPT_BODY>"
```

`<PROMPT_BODY>` template:

```markdown
Use $bootstrap-python-mcp-service.
Scope is limited to scaffold generation in <TARGET_PATH>, optional mapping report generation, and verification checks.
Run only commands needed for this flow, then return STATUS, exact command transcript, concise results, and minimal remediation if failures occur.
```

## Customization Placeholders

- `<REPO_PATH>`
- `<MCP_SERVICE_NAME>`
- `<MODE:PROJECT|WORKSPACE>`
- `<TARGET_PATH>`
- `<PYTHON_VERSION>`
- `<MEMBERS_CSV>`
- `<PROFILE_MAP>`
- `<FORCE_FLAG>`
- `<GIT_INIT_MODE>`
- `<MAPPING_INPUT_MODE:NONE|OPENAPI|FASTAPI_IMPORT>`
- `<MAPPING_INPUT_PATH>`
- `<GENERATE_MAPPING_REPORT:TRUE|FALSE>`

## Interactive Customization Workflow

1. Ask for mode, name, path, Python version, and git/force flags.
2. If workspace mode, also ask for members and profile map.
3. Return both:
- A YAML profile for durable reuse.
- The exact scaffold command to run.
4. Use this precedence order:
- CLI flags
- `--config` profile file
- `.codex/profiles/bootstrap-python-mcp-service/customization.yaml`
- `~/.config/gaelic-ghost/python-skills/bootstrap-python-mcp-service/customization.yaml`
- Script defaults
5. If users want temporary reset behavior:
- `--bypassing-all-profiles`
- `--bypassing-repo-profile`
- `--deleting-repo-profile`
6. If users provide no customization or profile files, keep existing script defaults unchanged.
7. See [`references/interactive-customization.md`](references/interactive-customization.md) for schema and examples.

## References

- `references/mcp-mapping-guidelines.md`
- `references/fastmcp-docs-lookup.md`
- `references/customization.md`
- `references/interactive-customization.md`

## Script Inventory

- `scripts/init_fastmcp_service.sh`
- `scripts/assess_api_for_mcp.py`
- Delegates to the shared workspace bootstrap scripts shipped by `bootstrap-uv-python-workspace`.

## Assets

- `assets/README.md.tmpl`
