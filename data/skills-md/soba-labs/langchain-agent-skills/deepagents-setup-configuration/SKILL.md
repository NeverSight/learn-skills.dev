---
name: deepagents-setup-configuration
description: Initialize, validate, and troubleshoot Deep Agents projects in Python or JavaScript using the `deepagents` package. Use when users need to create agents with built-in planning/filesystem/subagents, configure middleware/backends/checkpointing/HITL, migrate from `create_react_agent` or `create_agent`, scaffold projects with repo scripts, validate agent config files, and confirm compatibility with current LangChain/LangGraph/LangSmith docs.
---

# Deep Agents Setup and Configuration

Deep Agents are an agent harness on top of LangChain + LangGraph with built-in planning, filesystem context management, and subagent delegation.

## Use This Skill When

- You need a Deep Agent quickly (Python or JavaScript).
- You need subagents, filesystem-backed context, planning (`write_todos`), or long-term memory patterns.
- You need migration guidance from older `create_react_agent` flows.
- You need to scaffold a starter project with repository scripts.
- You need to statically validate an `agent.py` / `agent.js` / `agent.ts` config.
- You need safety checks before open-sourcing Deep Agents examples/templates.

## Tooling In This Skill

- `scripts/init_deep_agent_project.py`: scaffolds Python/JS projects with templates.
- `scripts/validate_deep_agent_config.py`: static checks for Deep Agent config quality.
- `references/deep-agents-reference.md`: detailed API, middleware, backends, migration, troubleshooting.
- `assets/templates/deep-agent-simple/`: minimal Python starter template.
- `assets/examples/basic-deep-agent/`: richer Python example.

## Recommended Workflow

1. Decide if Deep Agents is the right abstraction.
2. Scaffold with `init_deep_agent_project.py` (Python or JS).
3. Customize tools, prompt, backend, subagents, and persistence.
4. Run `validate_deep_agent_config.py`.
5. Use `references/deep-agents-reference.md` for advanced configuration.
6. Run the generated project and verify traces/behavior.

## Choose The Right Abstraction

| Need | Deep Agents | LangChain `create_agent` | LangGraph |
|------|-------------|--------------------------|-----------|
| Built-in planning/filesystem/subagents | ✅ Best fit | ⚠️ Manual middleware setup | ❌ Manual graph design |
| Fast path for complex multi-step tasks | ✅ | ⚠️ | ⚠️ |
| Fully custom graph topology | ❌ | ❌ | ✅ Best fit |
| Minimal/simple agent (1-3 steps) | ⚠️ Overhead | ✅ Best fit | ⚠️ |

## Initialize A Project

Use repo-local scripts and prefer `uv run`.

```bash
# Python simple template
uv run skills/deepagents-setup-configuration/scripts/init_deep_agent_project.py my-agent --language python --template simple --path skills/

# Python with subagents
uv run skills/deepagents-setup-configuration/scripts/init_deep_agent_project.py my-agent --language python --template with-subagents --path skills/

# Python CLI-config template (memory/checkpointer toggles)
uv run skills/deepagents-setup-configuration/scripts/init_deep_agent_project.py my-agent --language python --template cli-config --path skills/

# JavaScript template
uv run skills/deepagents-setup-configuration/scripts/init_deep_agent_project.py my-agent --language javascript --template simple --path skills/
```

Templates currently supported by the script:
- `simple`
- `with-subagents`
- `cli-config`

Generated outputs include:
- `agent.py` or `agent.js`
- `tools/example_tools.py` or `tools/example_tools.js`
- `.env.example`
- `README.md`
- `.gitignore`
- `pyproject.toml` (Python) or `package.json` (JavaScript)

## Validate Agent Configuration

Run static validation before shipping examples/templates:

```bash
uv run skills/deepagents-setup-configuration/scripts/validate_deep_agent_config.py path/to/agent.py
uv run skills/deepagents-setup-configuration/scripts/validate_deep_agent_config.py path/to/agent.js
uv run skills/deepagents-setup-configuration/scripts/validate_deep_agent_config.py path/to/agent.ts
```

Validator behavior:
- Errors on missing agent calls or invalid file types.
- Warns on risky/weak configs (missing prompt, odd backend usage, deprecated models).
- Supports dynamic config patterns (`create_deep_agent(**kwargs)`, `createDeepAgent(config)`), with warning that some static checks are skipped.
- Validates HITL style: `interrupt_on` / `interruptOn` should be mapping/object, and requires checkpointer.

## Current Deep Agents Defaults (Verified)

Default middleware includes:
1. `TodoListMiddleware`
2. `FilesystemMiddleware`
3. `SubAgentMiddleware`
4. `SummarizationMiddleware`
5. `AnthropicPromptCachingMiddleware`
6. `PatchToolCallsMiddleware`

Conditionally added middleware:
- `MemoryMiddleware` when `memory` is set
- `SkillsMiddleware` when `skills` is set
- `HumanInTheLoopMiddleware` when `interrupt_on` / `interruptOn` is set

## Core Configuration Patterns

```python
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-5-20250929",  # string or model object
    tools=[...],
    system_prompt="...",
    subagents=[...],          # optional delegation specialists
    middleware=[...],         # optional custom middleware
    store=store,              # needed for StoreBackend patterns
    backend=backend_factory,  # State/Store/Filesystem/Composite
    checkpointer=checkpointer # required for HITL interrupts
)
```

Backend guidance:
- `StateBackend` (default): thread-scoped, ephemeral.
- `StoreBackend`: persistent files via LangGraph store (requires `store=`).
- `CompositeBackend`: route prefixes (common `/memories/` -> `StoreBackend`).
- `FilesystemBackend`: direct disk access; use carefully, prefer `virtual_mode=True` with `root_dir`.

## HITL And Persistence

If using human approval interrupts:
- Python: use `interrupt_on={...}`
- JavaScript: use `interruptOn={...}`
- Always provide a checkpointer (`InMemorySaver`, `MemorySaver`, Sqlite/Postgres saver, etc.)

## Migration Guidance

- `langgraph.prebuilt.create_react_agent` is deprecated in LangGraph v1.
- For standard agents, prefer `langchain.agents.create_agent`.
- For harness capabilities (planning/filesystem/subagents), use `deepagents.create_deep_agent` / `createDeepAgent`.

## Versioning Note

- `deepagents` is currently a pre-1.0 package, so minor-version upgrades may include API changes.
- Re-validate generated templates and examples when bumping `deepagents` versions.

## Open-Source Safety Checklist

Before publishing this skill:
- Ensure no real secrets are committed (`.env.example` must stay placeholder-only).
- Remove generated artifacts like `__pycache__/` and `*.pyc` from skill folders.
- Avoid absolute local paths in code/examples.
- Keep provider credentials in environment variables only.
- Re-run validator on all shipped `agent.py` / `agent.js` templates.

## Troubleshooting Quick Hits

- Model/tool-call errors: verify tool-calling model and provider credentials.
- Files not persisting: confirm `StoreBackend` route + `store=` wiring.
- HITL not interrupting: verify interrupt mapping/object and checkpointer.
- Too much overhead for simple tasks: use `create_agent` or plain LangGraph.

## Resources

- `references/deep-agents-reference.md` for detailed API and migration patterns.
- `assets/templates/deep-agent-simple/` for minimal template files.
- `assets/examples/basic-deep-agent/` for a fuller runnable example.
- Python docs: https://docs.langchain.com/oss/python/deepagents/overview
- JavaScript docs: https://docs.langchain.com/oss/javascript/deepagents/overview
- LangGraph v1 migration: https://docs.langchain.com/oss/python/migrate/langgraph-v1
