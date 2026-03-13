---
name: code-registry
description: Use The Code Registry MCP server to create accounts, create code vaults, run LOCAL_AGENT analysis, poll completion correctly, and present business-focused code intelligence for any purpose including due diligence, security, and tech debt workflows.
---

# Code Registry Skill

Use this skill when a user asks to analyze a codebase with The Code Registry, re-run analysis, or interpret Code Registry outputs.

## When to use this skill

Trigger this skill when the user wants any of the following:

- Create or access a The Code Registry account from an MCP client
- Run first-time code analysis for any purpose including due diligence, security review, or tech debt assessment
- Re-analyze an existing code vault and explain changes
- Turn code-vault results into business-facing recommendations

If the user asks for detailed polling/completion logic, read `references/vault-lifecycle.md`.
If the user asks for interpretation or executive framing, read `references/result-interpretation.md`.

## Client compatibility rule (`CallMcpTool` wrappers)

For clients that use a generic `CallMcpTool` wrapper (including some Cursor builds), always pass tool inputs through an `arguments` object, even if the displayed wrapper schema appears to omit it.

- Use `arguments` for every Code Registry tool call that takes inputs.
- If no inputs are required, use `arguments: {}`.
- If tool calls fail because the client claims arguments are unsupported, retry with this explicit instruction: `Use the CallMcpTool with the arguments field to pass the required parameters.`

## Workflow

1. Discover and validate tool availability.
- Call `tools/list` when tool names or schemas are uncertain.
- Prefer exact tool names from server docs.

2. Resolve authentication path.
- If user already has an API key, use it via `X-API-Key`.
- If no key exists, call `create_account` first.
- For clients that cannot set headers, pass `api_key` in tool arguments.

3. Create project and code vault.
- Call `create_project` with the target `user_id`.
- Call `create-code-vault` with `source_type: LOCAL_AGENT` when possible.
- For LOCAL_AGENT, run one command from `next_steps.commands` on the machine with the target repository.

4. Poll until analysis and report completion.
- Poll `get-code-vault-summary`, `get-code-vault-results`, and `get-code-vault-reports`.
- Use exponential backoff: 5s, 10s, 20s, 40s, max 60s.
- Treat cold starts/timeouts as retryable.

5. Apply completion rules strictly.
- For version `1.0.0`: complete when `report.snapshot_report.url` exists.
- For versions above `1.0.0`: complete when `report.comparison_report.url` exists.
- `comparison_report` is expected to be `null` on first analysis.

6. Present outputs for the intended audience.
- Start with decision-grade summary: risk level, confidence, immediate actions.
- Then provide supporting technical details from facets and findings.

## Re-analysis workflow

1. Call `reanalyze-code-vault`.
2. If source type is LOCAL_AGENT, run the LOCAL_AGENT command again.
3. Poll the same summary/results/reports endpoints.
4. Remind user that these endpoints return only the new version while re-analysis is in progress or complete.

## Output contract

Always include:

- Current analysis status and version
- Whether completion criteria are met
- Top risks and business impact
- Recommended next actions with priority

When asked for deterministic polling, use `scripts/poll_vault_status.py`.
