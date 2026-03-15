---
name: notebooklm-management
description: NotebookLM MCP server management - query notebooks, add from share links, handle auth, reset sessions. Use when working with Google NotebookLM notebooks for conversational research tasks.
license: MIT
---

# NotebookLM MCP Management

Use this skill when research should be grounded in NotebookLM notebooks instead of a generic web search.

## Current MCP Reality

This repository already targets a real NotebookLM MCP workflow. The concrete tool surface available in this environment includes:

- `get_health`
- `list_notebooks`, `search_notebooks`, `select_notebook`
- `ask_question`
- `add_notebook`, `update_notebook`, `remove_notebook`
- `list_sessions`, `reset_session`, `close_session`
- `setup_auth`, `re_auth`, `cleanup_data`

## Activation Conditions

- Querying a specific NotebookLM notebook
- Adding a notebook from a share URL
- Managing a notebook library or switching active notebooks
- Recovering authentication or cleaning NotebookLM state
- Continuing a multi-turn research session

## Recommended Workflow

1. Call `get_health` first to confirm authentication and server readiness.
2. Reuse an existing session when the task is the same.
3. Prefer `search_notebooks` or `list_notebooks` before asking the user to restate what is already in the library.
4. Use `ask_question` iteratively in the same session for deep work.
5. Use `setup_auth` or `re_auth` only when health indicates auth problems.

## Library Management Rules

- Do not add or remove notebooks without explicit user confirmation.
- When adding a notebook, collect URL, description, topics, and use cases first.
- Update metadata instead of creating duplicates when the notebook already exists.

## Troubleshooting

- Auth broken: `get_health` -> `re_auth`
- Stale browser state: `cleanup_data(preserve_library=true)` after closing browsers
- Wrong context: `reset_session` or switch notebooks
- Ambiguous notebook choice: search the library before creating a new one

## References & Resources

### Documentation
- [MCP Tool Reference](./references/mcp-tool-reference.md) - Current NotebookLM MCP operations and parameters
- [Troubleshooting Guide](./references/troubleshooting.md) - Auth recovery, cleanup, and session issues
- [Workflows](./references/workflows.md) - Library, query, and maintenance workflows

### Scripts
- [NotebookLM Helper](./scripts/notebooklm-helper.py) - Local helper for library exports and reporting when MCP access is unavailable
- [Scripts README](./scripts/README.md) - Quick commands for the helper script

### Examples
- [simple-query.py](./examples/simple-query.py) - Basic query pattern
- [multi-turn-conversation.py](./examples/multi-turn-conversation.py) - Session reuse pattern
- [library-management.py](./examples/library-management.py) - Library search and organization

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [notion-docs](../notion-docs/SKILL.md) | Alternative knowledge-management workflow |
| [documentation-authoring](../documentation-authoring/SKILL.md) | Create source material that can later be stored in NotebookLM |
