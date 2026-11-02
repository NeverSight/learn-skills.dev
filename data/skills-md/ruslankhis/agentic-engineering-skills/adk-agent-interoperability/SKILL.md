---
name: adk-agent-interoperability
license: MIT
description: >-
  Connect, expose or audit Python Google ADK agents across process boundaries
  with MCP and A2A: tool-source selection (FunctionTool, OpenAPIToolset,
  McpToolset, Toolbox, Application Integration), consuming MCP servers
  (connection, lifecycle, tool_filter, prefixes, headers, the confirmation
  flag, SDK pin), exposing an agent as an MCP server, the sub-agents versus
  remote A2A topology decision, consuming a remote agent with RemoteA2aAgent
  (agent cards, task states, streaming, timeouts), exposing with to_a2a and
  registering on Agent Runtime or Gemini Enterprise. Use when an agent must
  call or be called by another service or framework, or to review MCP and A2A
  wiring. Do not activate for the MCP threat model, allowlists or pinning
  policy (adk-agent-security), in-process orchestration (adk-workflow-design),
  OAuth plumbing (adk-tool-auth-and-secrets), one API call's retry policy
  (safe-api-tool-calls) or deployment (deploy-adk-on-google-cloud).
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  source-chapter: "cross-framework"
  verified-against: "google-adk 2.8.0 source and adk-python main CHANGELOG, 2026-10-08"
  version: "2026.10.28"
---

# ADK agent interoperability

Wire an ADK agent to tools and agents that live in another process, service,
team or framework, and leave each boundary with a written contract and an
observable check. MCP is the vertical boundary (agent to tools); A2A is the
horizontal one (agent to agent). Everything that crosses either boundary is
data the other side chose to send: tool descriptions, tool results, agent
cards, task messages. Every claim here carries an evidence label (vendor
guidance, documented behaviour, independent evidence, community report,
source-verified against google-adk 2.8.0 unless another version is named).

## Inspect before choosing a mode

1. Read the existing boundaries: every `McpToolset` (connection params class,
   `tool_filter`, `tool_name_prefix`, `header_provider`, `require_confirmation`,
   `tool_list_cache_ttl_seconds`), `OpenAPIToolset`, `ToolboxToolset`,
   `ApplicationIntegrationToolset`, `AgentTool`, `RemoteA2aAgent` (card
   source, `use_legacy`, `timeout`, auth), `to_a2a` or `to_mcp_server` call
   sites, `agent.json` files, and how the Runner is started (`adk web`,
   `adk api_server --a2a`, uvicorn, Agent Runtime). The sibling
   `adk-agent-security` inventory script already lists MCP toolsets without
   filters, stdio transports and remote A2A agents from source; reuse its
   output instead of re-scanning.
2. Record the pins: `google-adk`, `mcp`, `a2a-sdk`. ADK 2.8.0 pins
   `mcp>=1.24,<2` and `a2a-sdk[http-server]>=0.3.4,<2` (source-verified
   `pyproject.toml`). Read [compatibility](references/compatibility.md) before
   quoting any behaviour: MCP SDK 2.x arrives in 2.9.0, the a2a-sdk 0.3 and
   1.x shapes differ, and several remote-agent fixes land in 2.9.0 to 2.11.0.
   Preserve the pins; present an upgrade as a decision with its CHANGELOG
   entries. When a ticket or contract names an MCP server, state both the
   `mcp` major version the agent installs and the specification revision
   the server speaks: the python-sdk v2 line (2.3.0 on PyPI, 2026-10-02)
   speaks 2026-07-28 and renames `FastMCP` to `MCPServer` with the old
   import path removed, while 2.8.0 pins SDK 1.x
   ([compatibility](references/compatibility.md)).
3. Record the hosting and identity facts: where the agent runs, where each
   MCP server and remote agent runs, which principal calls whom, and whether
   a token for one party is ever visible to another.
4. Run the two live-artefact helpers against servers you are allowed to
   query. Both are read-only toward the server (they list; they never call a
   tool or send a message), stdlib only, loopback by default:

   ```bash
   python "$SKILL_DIR/scripts/mcp_tool_inventory.py" --command "npx -y @modelcontextprotocol/server-filesystem@<exact version> ./data" --out mcp-manifest.json
   python "$SKILL_DIR/scripts/mcp_tool_inventory.py" --url http://127.0.0.1:8080/mcp --diff mcp-manifest.json
   python "$SKILL_DIR/scripts/agent_card_check.py" --url http://localhost:8001/a2a/check_prime_agent --installed-a2a-sdk 0.3.9
   ```

   `--allow-remote` is needed for any non-loopback host and is an approval
   step: ask the owner before the first connection to a server you did not
   start. `--command` runs the command you give it; use the exact command
   the agent uses. Exit 0 means inspected, 2 means bad arguments, 3 means a
   source failed (`partial`); `agent_card_check.py --fail-on error` (or
   `review`) and `--fail-on-diff` exit 1 when such a finding is reported, for CI.
   Findings whose `heuristic` is true are reading prompts, never verdicts.
   For a signed card, add
   `--require-signature` and `--key-host <host serving the agreed key set>`;
   the helper checks the signature's structure, not its validity
   ([signed agent cards](references/a2a-contracts.md#signed-agent-cards)).

Ask only what source and servers cannot settle: who operates each server or
remote agent, what the SLA and failure budget of the remote call is, which
registry or platform must list the agent, and who the human controller is.

## Choose the relevant path

| Mode | Decision and reference |
| --- | --- |
| (a) Tool-source selection | Read [selection](references/selection.md): FunctionTool versus OpenAPIToolset versus McpToolset versus MCP Toolbox for Databases versus Application Integration versus AgentTool-wrapped toolset, with the context-cost and determinism trade-offs and an observable check per row. |
| (b) Consume an MCP server | Read [mcp-consumption](references/mcp-consumption.md): connection params and timeouts, synchronous definition for deployment, pooled sessions keyed by headers, `header_provider`, `tool_filter`, `tool_name_prefix`, `tool_list_cache_ttl_seconds`, `require_confirmation`, `close()`, the SDK 1.x contract versus the 2026-07-28 specification, and MCP Apps widgets (`_meta.ui`): what ADK attaches, and the capability and visibility duties it leaves to you. |
| (c) Expose ADK as an MCP server | Read [mcp-exposure](references/mcp-exposure.md): `to_mcp_server` (one tool, one session per connection, stdio or streamable-http chosen by the caller) versus hand-built servers with `adk_to_mcp_tool_type`, and what the exposed description promises. |
| (d) Topology decision | Read [topology](references/topology.md): one agent, in-process sub-agents or `AgentTool`, or a remote A2A agent; the vendor criteria and the independent evidence on when multi-agent helps and how it fails. |
| (e) Consume a remote A2A agent | Read [a2a-contracts](references/a2a-contracts.md) and [remote-failures](references/remote-failures.md): `RemoteA2aAgent` card resolution and validation, task states including INPUT_REQUIRED, AUTH_REQUIRED and REJECTED, `a2a:` metadata keys, streaming, timeouts, failure as error events, and peer messages as data rather than user authority. |
| (f) Expose via A2A and register | Read [a2a-contracts](references/a2a-contracts.md), and [platform-registration](references/platform-registration.md) only when the ticket registers the agent on a platform: `to_a2a` and `adk api_server --a2a`, what the generated card contains and omits, persistent task stores, Agent Runtime's A2A template and Gemini Enterprise registration fields and auth. |
| (g) Audit existing wiring | Use all references plus [evaluation-across-boundaries](references/evaluation-across-boundaries.md) and the [review checklist](assets/interop-review-checklist.md); report per boundary with `file:line`, the contract gap, the observable check, the evidence label and the owning skill. Change nothing unless asked. |

A request often needs two rows (select a source, then consume it; decide the
topology, then expose and consume). Keep them in one change set.

## Implement the smallest coherent change

State the boundaries you will add or change, the pins you keep and the tests
you will write before editing. Then:

- Define `McpToolset` and `RemoteA2aAgent` synchronously at module level in
  `agent.py`; deployment targets load the module without an event loop
  (documented behaviour, ADK MCP deployment page). The exception is a peer
  whose signed card must be verified before use: that fetch is async, so
  build that agent in a startup factory
  ([signed agent cards](references/a2a-contracts.md#signed-agent-cards)). Choose the transport from
  the environment (`K_SERVICE` set means Cloud Run: Streamable HTTP; local
  means stdio) rather than editing code per environment.
- Always pass `tool_filter` (a list of names or a predicate) and, with more
  than one toolset, `tool_name_prefix`. Record the reviewed tool
  definitions with `mcp_tool_inventory.py --out` and commit the manifest; a
  later `--diff` that reports `rug_pull_signal` is a change request.
- Supply per-user or refreshing credentials through
  `header_provider(readonly_context)`; it is the only header path whose
  values vary per session and it also selects the pooled MCP session
  (`adk-tool-auth-and-secrets` owns the token lifecycle). Never forward a
  token issued for your agent to a downstream server.
- Treat a remote agent as an external API: give `RemoteA2aAgent` a
  deliberate `timeout`, decide what the parent does on an error event, and
  keep retries and idempotency with `safe-api-tool-calls`.
- Consume task state from `event.custom_metadata["a2a:response"]` and the
  `a2a:task_id` and `a2a:context_id` keys; a remote `input-required` or
  `auth-required` pause reaches the parent as a long-running function call
  that only the controlling user may answer.
- When exposing, publish a card that describes capability and declares
  `securitySchemes`; keep instructions, tool docstrings and internal state
  out of it. Serve with a persistent `task_store` when more than one
  instance runs.
- Write the contract table for each boundary (input, output, identity,
  failure result, timeout, consumer) before wiring, as
  `adk-workflow-design` does for in-process edges.

Do not loosen a `tool_filter`, widen `--allow-remote`, or switch
`use_legacy` to make a test pass; each is a contract change with its own
evidence.

## Permissions and consequential operations

<!-- shared:consequential-operations-brief -->
Inspection is read-only, and code generation authorises no deployment, paid
call or live test. Before any consequential operation (an API, billing or
quota change, a billable resource, a secret, IAM, a data migration, a
deployment, a deletion, or a paid or destructive test), read
[consequential operations](references/operating-rules.md#consequential-operations),
present the exact scope and limits, obtain explicit approval and end the turn
to wait for it. Cleanup is a separate confirmed operation on resources this
workflow created.
<!-- /shared:consequential-operations-brief -->

Listing a server's tools, fetching a card and reading source are read-only.
Connecting to a server or agent you did not start, registering an agent in
Agent Registry or Gemini Enterprise, enabling an API, granting
`roles/run.invoker` or any IAM binding, and exposing an endpoint without
authentication are approvals: state the target, the principal and the cost
or exposure, and wait for a yes. Never run `--command` with a server command
you have not read; it executes on the host with your identity.

## Validate and finish

Read [validation](references/validation.md). Produce: the manifest and card
reports before and after; a fake-server test per boundary that shows the
agent handling a normal result, a timeout, an error and (for A2A) an
`input-required` pause without acting on peer text as user authority; the
contract table; and, when approved, a live exchange on the pinned versions
labelled as such. A fact read in the installed package is `offline (source
read)` and a fake server is `local (mocked)`. Report files changed, commands
with actual output, each boundary's residual risk and the owning skill for
each deferred concern.

<!-- shared:evidence-labels-brief -->
Label each result with its tier (`offline`, `local`, `live` or `release`) and
outcome (`pass`, `fail`, `blocked` or `not run`) as
[evidence labels](references/operating-rules.md#evidence-labels) defines them;
earlier, vendor and documentation-only results are `historical`,
`vendor-measured` or `guidance`, never this session's evidence.
<!-- /shared:evidence-labels-brief -->

Independent community project; not affiliated with or endorsed by Google.
