---
name: etherscan
description: >-
  Navigate Etherscan website features, API endpoints, CLI commands, and MCP
  tools. Use when selecting an Etherscan interface, locating an explorer page
  or developer utility, constructing or troubleshooting API requests,
  automating terminal workflows, connecting or calling Etherscan MCP tools,
  handling authentication, confirming chain support, interpreting errors, or
  comparing capabilities, limits, and behavior across Etherscan interfaces.
---

# Etherscan orchestrator

Route an Etherscan task to the right interface, then to the right page, endpoint, command, or tool. Use this skill as a workflow and rulebook, not as a source of live chain data. Treat the selected reference and the live authority it names as canonical for current parameters and behavior.

## Follow the workflow

1. Before discovering interfaces, consider the task-relevant specialized skills available in the current environment. Match the user's use case against their descriptions and select the most specific applicable skill; honor an explicitly requested skill when it applies.
2. When a specialized skill matches, read and follow it completely. Let it own clarification, capability discovery, transport selection, execution, and output; do not independently impose Website, API, CLI, or MCP or add output that violates its contract. Stop this workflow unless the selected skill explicitly returns control.
3. For example, use [the `etherscan-flow` skill](../etherscan-flow/SKILL.md) for tracing or following money across hops; scam, hack, exploit, drain, phishing, rug-pull, or compromised-wallet investigations; transaction or address flow visualization and case generation; or business and entity income, revenue, fees, spending, expenses, and treasury profiles. Preserve its JSON-only output and per-operation transport priority: official Etherscan CLI → Etherscan MCP → current-invocation `apikey=` → other documented key sources.
4. Keep ordinary explorer navigation in this workflow. For example, route "show this transaction on Etherscan" to the Website unless the user asks to trace or visualize its flow.
5. When no specialized skill matches, clarify only the chain, target, intent, plan, or output details that the request leaves unresolved.
6. Discover the Etherscan-relevant tools and connections available in the current environment, then briefly tell the user what is available.
7. Honor an explicitly requested interface; otherwise select one from [Select the interface](#select-the-interface).
8. Read that interface reference completely before acting. Read another only for an explicit comparison, required fallback, or genuinely cross-interface workflow.
9. Confirm the exact chain and chain ID through the selected reference's authority. Never infer support from EVM compatibility.
10. Construct the exact page, endpoint, command, or tool call documented by that authority.
11. Return the result with throttling, pagination, truncation, plan restrictions, and error context intact.

## Discover local capabilities

Use non-mutating checks to identify the task-relevant Etherscan interfaces available in the current environment before choosing a route.

- Check whether the Etherscan CLI is installed. If it is, inspect its reported version and live help rather than assuming its commands or flags.
- Inspect callable MCP connections and their advertised tools when discovery is available. Distinguish configured, connected, and authenticated access from a merely documented MCP server.
- Note relevant browser, web, or HTTP access when it materially affects how the task can be completed.
- Briefly mention the relevant capabilities found, such as an installed Etherscan CLI and version, and explain when one changes the selected route.
- Treat an unavailable check as unknown rather than claiming that the capability does not exist.
- Do not install software, authenticate, connect accounts, reveal credentials, or read secret values merely to inventory capabilities.

## Clarify before acting

Ask only for information that is required and genuinely missing.

- Confirm the exact chain and chain ID; one API key spans many chains, so an implicit chain can produce a valid result for the wrong network.
- Identify the address, transaction, token, contract, or block in scope. Distinguish target types when the live capability documents different behavior for them.
- Distinguish read-only inspection from verification, broadcast, configuration deletion, or another external write.
- Confirm API-plan access when the selected endpoint or tool is gated. Prefer an available free-tier route when the plan is unknown, or state that access may be restricted.
- Choose interactive review, structured JSON or CSV, or an agent tool call according to the requested output.

## Select the interface

Honor an explicitly requested interface first. Otherwise, choose by the user's intended execution environment and output.

| Interface | Read | Use it for |
| --- | --- | --- |
| Website | [Website feature reference](references/site.md). | Locate explorer pages, user-facing tools, exports, token approvals, contract utilities, trackers, and support resources. |
| API | [API reference](references/api.md). | Select endpoints, construct requests, interpret responses, check authentication, plans, rate limits, errors, and supported chains. |
| CLI | [CLI reference](references/cli.md). | Select terminal commands, configure the client, automate queries, produce structured output, paginate, and export data. |
| MCP | [MCP reference](references/mcp.md). | Connect an MCP client, discover tools, inspect schemas, construct calls, and distinguish MCP-layer failures from API-level errors. |

When the user does not specify an interface, apply these defaults.

- Prefer the website for an interactive human workflow.
- Prefer the API for an application integration or when the broadest endpoint coverage is required.
- Prefer the CLI for terminal automation, pipelines, or exports.
- Prefer MCP for agent-driven, read-only tool calls when an authenticated MCP connection is available.

## Respect capability boundaries

- Do not infer that a capability available through one interface exists through another. Discover current capabilities through the selected interface's live authority.
- Treat MCP as read-only unless current tool discovery and official documentation explicitly establish a state-changing capability. Require the same exact authorization applied to every other write.
- Confirm the exact chain and chain ID instead of inferring support from EVM compatibility.
- Verify volatile parameters, schemas, availability, plan access, limits, and supported chains through the authority named by the selected reference.
- Preserve throttling, pagination, truncation warnings, restrictions, and returned error context.
- Switch interfaces only when the selected reference shows that the original interface cannot complete the task or the user requests another interface.

## Apply guardrails

- Replace any exposed Etherscan API key with `YourApiKeyToken`. Never print, commit, reproduce, or place credentials in prompts, source files, logs, or output.
- Avoid uncontrolled retry loops, and respect both plan-wide and endpoint-specific throttles.
- Require explicit user authorization for the exact contract-verification submission, signed raw-transaction broadcast, destructive configuration change, or other state-changing action.
- Prefer read-only inspection until the user authorizes the exact state-changing action, payload, and chain.
- Preserve API, transport, validation, and application-level errors as distinct failure contexts.

## Workflow checks

Use these representative cases to verify routing and guardrail behavior after changing this skill. Treat them as behavioral guidance, not live API assertions.

| Request or condition | Expected behavior |
| --- | --- |
| Show an address in the block explorer. | Use the website reference and an interactive address page. |
| Export a wallet's ERC-20 transfers to CSV from a terminal. | Use the CLI reference and its pagination and CSV support. |
| Call an agent tool to retrieve a balance. | Use MCP when live discovery advertises a matching tool; inspect its current schema before calling it. |
| Integrate token-holder counts into a backend. | Use the API and discover the current endpoint from official documentation; do not invent an MCP tool. |
| The Etherscan CLI is installed locally. | Mention the installed version, inspect its live help, and use it when it matches the requested environment and output. |
| An MCP server is documented but live discovery is unavailable. | Report its availability as unknown; do not describe it as connected or infer its tool inventory. |
| The user explicitly requests an interface. | Honor it unless it cannot perform the task; explain any required fallback. |
| A balance request omits the chain. | Ask for the chain or chain ID before querying. |
| A capability may restrict target types or plan access. | Verify and surface the current restrictions before calling it. |
| A workflow requests a verification or signed transaction broadcast. | Confirm the exact payload, chain, interface, and authorization before submission. |
| A workflow requests an MCP verification or broadcast. | Verify whether live discovery exposes the operation; otherwise offer an authorized interface that does. |
| Input contains an API key or requests stored CLI credentials. | Replace the key with `YourApiKeyToken` and never print the stored plaintext credential. |

## Further references

- Use the bundled [website](references/site.md), [API](references/api.md), [CLI](references/cli.md), and [MCP](references/mcp.md) references for interface-specific discovery and durable behavior.
- Follow the selected reference's authority order. Treat the exact live page, endpoint specification, CLI help, or MCP schema as authoritative when it conflicts with bundled content.
