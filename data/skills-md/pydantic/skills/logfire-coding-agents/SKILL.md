---
name: logfire-coding-agents
description: Connect Claude Code or Codex itself to Logfire telemetry, or route a coding agent's model requests through Pydantic AI Gateway. Use for coding-session recording, capture policies, Gateway agent configuration, temporary proxy launches, status, or removal. Not for instrumenting an application or routing an application's model client.
---

# Connect Coding Agents to Logfire

Use the exact Rust CLI executable supplied by the handoff for every operation;
examples call it `logfire-cli`. Preserve its region, organization, project, and
data directory. Do not replace it with a package launcher or install a second
exporter by hand. These commands require `--beta`.

Without a prepared handoff, follow [native CLI connection](./references/connection.md).
The same skill is distributed in the Logfire plugin; plugin installation alone
does not supply a CLI session, project credential, or capture consent.

Distinguish three independent capabilities:

- **Telemetry:** record the coding agent's activity in the selected project.
- **Gateway:** route the agent's model requests through the organization's paid
  Gateway access. This does not enable telemetry.
- **MCP:** let the agent query Logfire. MCP OAuth is owned by the agent's MCP
  client; CLI login or telemetry setup does not authenticate that client.

Honor the user's stated goal and agent. Ask only for missing choices; do not
enable all three because the user asked to connect one. For application code,
use [instrumentation](../logfire-instrumentation/SKILL.md) or the
[application Gateway skill](../logfire-gateway/SKILL.md) instead.

## Confirm the destination

A prepared handoff already selected the origin, organization, project, and
local SDK credential: reuse those without repeating account commands or
creating another write token. Otherwise follow the shared
[connection reference](./references/connection.md).
Do not guess another project when access fails.

Keep account credentials out of prompts, logs, and child environments. Leave
credential storage and settings writes to the CLI. If a saved helper will
invoke this executable later, use a persistent installed path, not a temporary
build or cache directory.

## Choose the requested workflow

- To observe Claude Code or Codex, read [session telemetry](./references/telemetry.md).
- To route coding-agent inference, read [Gateway routing](./references/gateway.md).
- For both, configure telemetry first, then Gateway. Preserve each integration's
  destination and settings independently.

Do not launch another setup agent or a nested interactive coding session just
to configure this one. Explain any required restart. Finish with the configured
agent, destination, capture or routing choice, observed verification result,
and one next action. Configuration is not proof of ingestion or inference.
