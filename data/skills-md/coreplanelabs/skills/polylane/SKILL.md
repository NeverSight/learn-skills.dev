---
name: polylane
description: Investigate production and assess production impact with the Polylane platform. Use when debugging anything live — a production issue, outage, error spike, latency regression, or failing deploy; root-causing from logs, metrics, traces, or alerts; answering "what broke", "what changed", or "is prod affected"; exploring cloud infrastructure, services, or dependency topology; and for on-call triage, postmortems, rollbacks, and remediation. Also use BEFORE making or shipping any code or infrastructure change, to check its blast radius against what is actually running. Covers the full platform — context graph (clouds, integrations, topology, repositories, memories), detection (issues, change intelligence, advisories, scans), investigation (threads, feed, escalations), and remediation (autofix, automations, skills) — plus connecting a stack and querying it. Retrieve from Polylane docs — never guess commands or schemas.
---

# Polylane Platform

Polylane is an agent-powered production operations platform: it builds a live context graph of your stack, detects problems from telemetry, investigates them with agents, and remediates through reversible operations and reviewed pull requests.

This file carries process and conventions — no catalogs, schemas, or limits, which all have live sources. **Retrieve before you cite.**

## Retrieval Sources

| Source | How to retrieve | Use for |
|--------|----------------|---------|
| Polylane docs | `https://docs.polylane.com` — agent index at `/llms.txt`, raw markdown per page at `/raw/<path>.md` | Concepts, feature behaviour, schemas |
| Docs MCP | `https://docs.polylane.com/mcp` — `list-pages`, `get-page` (no auth) | Same content, as tools |
| Platform MCP | `https://mcp.polylane.com/mcp` | Live workspace queries: graph, telemetry, code |
| CLI help | `polylane --help`, `polylane <resource> <verb> --help` | Command surface of the installed version |
| API | `https://api.polylane.com/v1/reference`; `polylane api list` / `api describe <op>` | Every REST operation and its schema |
| Public catalogs | `GET /v1/public/{integrations,automations,skills}/catalog`, `GET /v1/public/billing/plans`, `GET /v1/scopes` | Integration types, templates, plans and limits, scopes |

## The Four-Step Loop

```
Context ──▶ Detection ──▶ Investigation ──▶ Remediation
(connect)   (find issues)  (root-cause)      (fix + prevent)
```

Every primitive belongs to one step. Docs pages mirror this: `/context`, `/detection`, `/investigation`, `/remediation`.

| Concept | One line |
|---------|----------|
| Workspace | The tenancy unit; everything below is workspace-scoped |
| Context graph | Nodes (resources) + typed edges (`deploys_to`, `connects_to`, `invokes`, …), populated by cloud syncs and integrations |
| Issue | One detection record (Polylane check or provider alert); deduped by fingerprint — a match within 24 h **reopens** rather than duplicates; triage verdict is Incident / No incident |
| Thread | Persistent agent-run transcript; every automation run and investigation is one |
| Investigation | Agent work on a confirmed issue; parallel hypothesis sub-agents vote confirmed / refuted / inconclusive |
| Automation | Unattended run: trigger → instructions → tools → actions → destinations (see the `polylane-automations` skill) |
| Autofix | Agent-written fix that always lands as a pull request, never a direct push |
| Skill | Reusable instruction set attachable to threads and automations |
| Memory | Saved confirmed finding, resurfaced in future agent runs |

## Connecting a Stack

Connect in this order — each stage unlocks the next:

1. **One cloud + one observability tool** → the graph populates and detection starts. Discover what's connectable from the catalog (`polylane integration catalog`, or `GET /v1/public/integrations/catalog`), and check the user's repo for provider config files before recommending.
2. **The code host (GitHub)** → change intelligence on PRs, code-aware investigation, autofix.
3. **Chat (Slack)** → message triggers and result destinations.

How things connect (per-provider flags: `polylane integration connect --help` / `cloud connect --help`):

- **AWS** — a CloudFormation stack creating a read-only role; no stored keys.
- **GitHub, Sentry, Vercel, Slack** — app-install browser flows. These exit 0 when the URL is generated, not when the install completes — confirm afterwards.
- **Most observability tools and clouds** — an API token.
- **Any MCP server** — connectable as an integration; its tools become available to agents.

**Verify, don't assume:** `integration list`, `cloud list`, then `service list` — resources appearing means the first sync worked (it also produces a "discovery" change record). For fully agent-driven onboarding from nothing (account → workspace → API key → MCP → clouds), fetch and follow <https://api.polylane.com/v1/public/setup/prompt.md>.

## Investigating with Polylane

The method, whatever the interface (CLI commands shown; the platform MCP's `runTool` reaches the same capabilities):

1. **Anchor** — flagged already? `issue show <id>` + `issue timeline <id>`. Only a symptom? `service find "<query>"` to locate the resource. Nothing yet? `issue list --active`.
2. **Check what changed first** — most incidents follow a change: `feed list --category change|release --since 24h`.
3. **Gather evidence on the affected service** — `service logs <id> --since 1h --grep error`, `service metrics <id> --since 1h`, `service graph <id> --direction both` for blast radius.
4. **Correlate with code** — `repo grep <repo> "<pattern>"`, `repo read <repo> <path>`.
5. **Go past the fixed surface when needed** — `tools search "<capability>"` then `tools run <name>` runs any provider-native query (CloudWatch, Datadog, Honeycomb, …) the connected stack supports.
6. **Record as you go** — `issue note` for actions taken, `issue milestone` at state changes ("Mitigated"), `memory save` for confirmed findings only — memories feed every future run.
7. **Hand off when useful** — `thread ask "<question>" --context <ids>` gives Polylane's own agent your accumulated context (ids are prefix-typed, see below).

Done when there's a root cause or an evidence-backed leading hypothesis, recorded on the issue.

## Checking Production Impact Before a Change

Before editing or shipping code that touches a live system, use the graph to see what you're about to affect:

1. **Map the change to production** — which resources does this code serve? `service find "<name>"`, or the repository's `deploys_to` edges (`repo show`, `tools run findNodes`).
2. **Blast radius** — `service graph <id> --direction inbound`: everything that depends on what you're changing.
3. **Is it already degraded?** — `issue list --active` filtered to the service. Ship nothing into an open incident.
4. **What else is in flight?** — `feed list --category change|release --since 24h`; avoid stacking changes on an unsettled deploy.
5. **Ship with a watch** — Polylane's PR review comments production impact on the PR automatically (it walks `deploys_to` edges); `babysit-<provider>-deployment` and `auto-rollback-<provider>-deployment` automation templates cover the deploy window.
6. **Confirm after deploy** — `service logs` / `service metrics --since <deploy>` against the pre-change baseline, and check the deploy's change record in the feed.

## Interfaces

```
├─ Terminal / scripts / CI → polylane CLI (see polylane-cli skill)
├─ Coding agent → platform MCP or CLI; wire both with `polylane setup`
├─ Programmatic → REST API (api.polylane.com/v1)
├─ No account yet → `polylane auth signup`, or hand any coding agent
│  https://api.polylane.com/v1/public/setup/prompt.md to onboard from scratch
└─ Humans → console.polylane.com (every API object carries a _html_url deep link)
```

## The Platform MCP: Five Tools, Everything Reachable

`https://mcp.polylane.com/mcp` (streamable HTTP; OAuth with dynamic client registration, or `x-api-key` for headless). It exposes exactly **five tools** no matter how much is connected — instead of one MCP tool per capability, it **executes your code on the Polylane backend**, where the full surface is bound:

| Tool | What it does |
|------|-------------|
| `searchTools` | Discover the workspace's agent tools and their schemas — the same tools Polylane's own agent uses (observability queries across every connected provider, graph traversal, code search, deployments, audit logs). **Call this first**; the roster is filtered to your credential. |
| `runTool` | Run one agent tool by exact name, args as a nested `params` object matching its schema. |
| `runCode` | Run a parameterless async TypeScript arrow on the backend, where every agent tool is `await tools.<name>(args)` (`tools.__describe(["name"])` fetches types). Use it whenever a task needs more than one tool call. |
| `search` | Query the Polylane OpenAPI spec ($refs pre-resolved): a parameterless async arrow using the sandbox global `codemode.spec()`. |
| `execute` | Call any REST operation: `codemode.request({ method, path, query, body })`. Find the endpoint with `search` first. |

**Why code execution matters:** chaining N tool calls costs one round trip, and intermediate data (log lines, node lists, the full spec) stays on the backend — only what your code returns enters your context, and large results are truncated. So filter, join, and aggregate *in the code*, and return the summary:

```ts
async () => {
  const types = await tools.__describe(["findNodes"]);  // exact input/output types
  const nodes = await tools.findNodes({ query: "checkout" });
  // ...chain further tools.<name>() calls on the results here...
  return nodes;  // return only what you need in context
}
```

**Write gating:** writes require the `agent_tools:write` scope **and** the `x-polylane-allow-writes: true` header; a safety model screens every write regardless, and clients supporting elicitation get an approval prompt. An OAuth session can span workspaces — pass `workspaceId` (id or slug) per call; an API key is bound to one workspace — omit it.

## Conventions the Lookups Don't Confess

**REST.** List/get/patch/delete take `workspaceId` in the **path** (`/v1/{resource}/{workspaceId}[/{id}]`); create is `POST /v1/{resource}` with `workspaceId` in the **body** — a workspaceId in a POST path 403s. Responses are enveloped (`success`, `result`, `error`); plan-limit rejections are **HTTP 426** naming the exceeded dimension. Single objects carry `_html_url` (console deep link) and `_links` (next-step operations) — follow `_links` instead of guessing paths.

**IDs are prefix-typed** — infer the resource type from the prefix (the CLI's `--context` relies on this): `ws_` workspace, `usr_` user, `thrd_` thread, `iss_` issue, `acc_` cloud account, `int_` integration, `repo_` repository, `mem_` memory, `auto_` automation, `fix_` autofix, `skl_` skill, `ask_` escalation, `scan_` scan report, `art_` artifact, `sk_` API key.

**Scopes** are `resource:action` strings (`issues:read`, `agent_tools:write`); enumerate them via `GET /v1/scopes`. `agent_tools:write` is **not** in the CLI's default OAuth scope set — mint an API key carrying it when an agent needs write tools.

## Safety Model (the autonomy dial)

1. **Read-only default** — cloud accounts connect read-only; writes are refused until a workspace admin turns read-only off.
2. **Reversible operations** — when enabled: restarts, deploy rollbacks. Every write passes a safety review, and writes only happen in chat threads, never background runs.
3. **Code gated by review** — agents never push to the default branch; fixes are PRs through CI and human approval.
