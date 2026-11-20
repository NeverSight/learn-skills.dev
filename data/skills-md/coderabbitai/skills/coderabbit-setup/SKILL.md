---
name: coderabbit-setup
description: Check CodeRabbit setup for local CLI reviews and, when configured, connect the host's CodeRabbit MCP tools. Use for onboarding, reconnection, or diagnosing separate MCP and CLI sign-ins.
metadata:
  version: "0.1.0"
---

# Set up CodeRabbit

Report remote connection and local review readiness separately. Setup alone
does not authorize a review or source upload.

## Connect remote tools

Check whether the installed package or host provides a CodeRabbit MCP connection
to `https://mcp.coderabbit.ai/`. Use the host's own sign-in flow:

- **Antigravity:** use the plugin's `coderabbit_coderabbit` server. Open the
  plugin's Accounts tab or Customizations > Installed > MCP Servers in the App.
  In the CLI, inspect `/mcp` or choose Sign in on the plugin in `/plugin`.
- **Claude:** use Connect or Reconnect for the CodeRabbit server. In Claude
  Code, inspect the connection through `/mcp`.
- **Codex and other hosts:** use the configured CodeRabbit connection when
  present. A skills-only installation can proceed directly to local CLI setup.
  Report remote tools as unconfigured if the host has no CodeRabbit connection.

Let the user complete consent and select the intended organization. If the
host requests an authorization code, the user enters it directly into the
host's authentication dialog, never into chat. Do not read credential stores
or copy tokens between the host and CLI. Preserve other connections.
If a duplicate connection prevents discovery, explain the conflict before
changing it.

In Antigravity, if submitting the code fails with `invalid_grant` or “Invalid
authorization code,” use the native Restart sign-in action and complete a fresh
flow. Do not resubmit the rejected code or infer its cause from that message
alone. If the fresh flow also fails, report the error and stop retrying.

Verify the selected account and organization using `connection_status` or
`get_me` when available. A browser success page alone does not establish tool
discovery or access. If tools are absent, report the observed connection error
and use the host's reconnect flow. Do not promise capabilities beyond the
granted scopes, organization, plan and permissions.

## Prepare local reviews

Skip this step for a remote-tools-only request. Local reviews require a Git
working tree, the official CodeRabbit CLI, its own sign-in, and host
execution/network permission. Locate the installed
`code-review` skill and follow its `references/auth-recovery.md` for trusted
CLI discovery and authentication checks. That reference also routes to
Antigravity sandbox recovery when an installed executable is inaccessible.
Hand off missing CLI installation or login to the user through the official
[CLI instructions](https://docs.coderabbit.ai/cli).

MCP sign-in does not authenticate the CLI. Do not call `start_code_review`,
reserve a review, install a hook, or pass an MCP handoff into shell commands.
If local execution is unavailable, report that separately from the observed
MCP connection status. Remote tools remain usable only if the MCP check succeeded.
Configuration uses the installed `coderabbit-config` skill and needs no login.

If the user already requested a review, continue with the installed
`code-review` skill and preserve their scope. Otherwise summarize what is
ready and suggest “Review my uncommitted changes. Review only; do not edit.”
