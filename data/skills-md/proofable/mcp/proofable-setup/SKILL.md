---
name: proofable-setup
description: Add Proofable to any MCP client, sign in, and reuse profile, proofs, listings, and agents.
license: Apache-2.0
compatibility: Requires an MCP-capable client that can register a remote HTTP server.
metadata:
  author: Proofable
  version: "0.1.7"
  homepage: https://docs.proofable.me/mcp/setup
---

# Set up Proofable

Give AI agents identity, scoped access, and proof of every action.

Add this hosted endpoint to your MCP client, then finish the sign-in it opens:

`https://mcp.proofable.me/mcp`

If the client offers the Proofable plugin, install it instead of adding the URL by hand. Keep one Proofable connection per client.

Have the CLI?

```bash
proofable setup
```

After sign-in, ask:

```text
Show my Proofable profile and the proofs I can reuse.
```

Call `proofable_context` once. Do not fetch every proof body. Summarize the result as Passed, Action needed, or Blocked.

For a specific requirement, ask:

```text
Check whether I already have the proof needed for this task. Reuse it if it qualifies; otherwise show me the next step.
```

Then, if you need agents:

```text
Show what my agents are allowed to do.
```

The agent lives on the signed-in profile by default. Ask for a dedicated spend account only when the agent should pay from its own account. Open **Connections** on proofable.me to link apps.

Full page: https://docs.proofable.me/mcp/setup

Optional project mount (`cursor`, `claude`, `codex`, `hermes`, `openclaw`, or `opencode`; VS Code uses `cursor`):

```bash
proofable mount <agentId> --apply cursor
```
