---
name: port-workflows
description: "Build Port workflows: node-based automations made of triggers (self-service forms, context lake events), action nodes (webhook, upsert entity, GitHub/GitLab/Azure DevOps/Claude managed agents integration actions, Kafka, Cursor Agent, AI), condition and input nodes, JQ templating between nodes, and self-service trigger permissions, authored as workflow JSON against the Port API. Use when asked to create a Port workflow, add a trigger to a workflow, add an action node, wire up a self-service workflow, add branching with a condition node, add an approval step to a workflow, build an event-driven automation in Port, or write workflow JSON. Port workflows are Port's own nodes-and-edges automation graph, not a CI/CD pipeline file like GitHub Actions."
license: MIT
compatibility: "Claude Code, Cursor, Codex CLI, GitHub Copilot"
metadata:
  version: "1.0.0"
  author: port-labs
  repository: https://github.com/port-labs/port-skills
  tags: port,workflows,automation,reference
  summary: Build Port workflows with triggers, action nodes, and conditions
---

# Port workflows

A workflow is Port's visual, node-based automation layer. Nodes (triggers,
actions, conditions, inputs) connect into a graph; running the workflow walks
that graph, passing each node's output to the next as JQ-templated data.

## Use this skill when

Use this skill to author or edit workflow JSON: adding a self-service or
event trigger, adding an action node (webhook, upsert entity, an integration
action, Kafka, Cursor Agent, or AI), branching with a condition node, gating
on human approval with an input node, or wiring the connections and JQ
templates between them. This skill is reference-only: the JSON it produces is
valid without a live Port account, though applying it needs API credentials
(see [Prerequisites](#prerequisites)).

Out of scope: Port's older, single-step Actions & Automations model (not
covered by a skill in this repo yet), blueprint schema design (`port-blueprints`), and
CI/CD pipeline files such as `.github/workflows/*.yml`, GitHub Actions is a
separate product that a workflow can *trigger* (via `INTEGRATION_ACTION`)
but does not replace.

## Prerequisites

- Go over the `port-getting-started` skill first if this is your first time
  working with Port.
- To create or update workflows without MCP: a Port `CLIENT_ID` and
  `CLIENT_SECRET` (**...** menu > **Credentials** in the Port app),
  exchanged for a bearer token at `POST https://api.port.io/v1/auth/access_token`.
- If Port's MCP server is connected, this skill can use its workflow tools
  (`list_workflows`, `get_workflow`, `upsert_workflow`) to read or apply a
  workflow directly instead of you copying JSON in by hand, but the raw API
  calls in [Step 6](#step-6---create-or-update-via-the-port-api) always
  work as a fallback. Search `search_port_knowledge_sources` for anything
  this skill doesn't cover.
- Workflows are in open beta: cross-check unfamiliar fields against
  [docs.port.io/workflows](https://docs.port.io/workflows/overview) before
  shipping.

## Step 1 - Sketch the graph and pick trigger type(s)

Precondition: you know what should start the automation and what it should do.
Action: decide `SELF_SERVE_TRIGGER` (a user submits a form on demand),
`EVENT_TRIGGER` (an entity is created, updated, deleted, or a timer property
expires), or both, a workflow can define multiple trigger nodes feeding the
same downstream graph. Then list the actions in order: webhook calls, entity
upserts, integration dispatches, AI steps, with any branching (condition) or
human approval (input) points.
Fallback: if the trigger is unclear, default to a self-service trigger, it is
the safer, opt-in default and easiest to test.

## Step 2 - Configure the trigger node(s)

Precondition: trigger type chosen.
Action: for `SELF_SERVE_TRIGGER`, define `userInputs.properties` (and
`required`); for `EVENT_TRIGGER`, define `event.type` and
`blueprintIdentifier`, plus an optional JQ `condition` to filter which events
fire the workflow. Full field reference, including `contexts` (bolt-menu and
create-entity surfacing) and `variant`, is in
[references/node-types.md](references/node-types.md#trigger-nodes).
Fallback: never add `title`, `icon`, or `description` to a trigger node,
those fields are ignored there and belong on action nodes instead.

## Step 3 - Add action and flow nodes

Precondition: trigger is defined.
Action: add one node per step. See
[references/node-types.md](references/node-types.md) for the full field
reference and JSON shape of every node type: `WEBHOOK`, `UPSERT_ENTITY`,
`INTEGRATION_ACTION` (GitHub, Claude managed agents, and others), `KAFKA`,
`CURSOR_AGENT`, `AI_AGENT`, `AI`, `CONDITION`, `INPUT`. Reference upstream
data with JQ templates, see
[references/data-flow.md](references/data-flow.md).
Fallback: if a step just needs to call an HTTP API, prefer `WEBHOOK` over
building a custom integration, and prefer `UPSERT_ENTITY` over a raw
`WEBHOOK` call to Port's entity API, it is simpler and less error-prone.

## Step 4 - Wire connections

Precondition: nodes exist.
Action: add a `connections` entry (`sourceIdentifier`, `targetIdentifier`)
per edge. `CONDITION` and `INPUT` nodes need `sourceOutletIdentifier` (or
`fallback: true`) on every outgoing connection, matching one of the node's
`outlets`. Trigger nodes can only be sources, never targets. Each node (and
each outlet) can have at most one outgoing connection, fan-out is not
supported, chain nodes sequentially instead.
Fallback: got a fan-out requirement (one node feeding two independent next
steps)? Split it into two workflows, or serialize the two branches behind a
single downstream node instead of trying to fan out directly.

## Step 5 - Set self-service permissions

Precondition: workflow has a `SELF_SERVE_TRIGGER` node.
Action: set `permissions` on the trigger node's `config`. Omitted or `{}`
means Admin only. See
[references/permissions.md](references/permissions.md) for static
(`roles`/`users`/`teams`) and dynamic `policy` rules (based on user, team, or
form-input properties).
Fallback: event triggers have no `permissions` field, event-driven workflows
run under the organization's automation identity, not a specific user.

## Step 6 - Create or update via the Port API

Precondition: you have a bearer token and a complete workflow JSON body
(`identifier`, `nodes`, `connections`, at minimum).

Action: use the endpoints below (`workflow_identifier` is the workflow's
`identifier`).

| Operation | Method | Path |
|---|---|---|
| Create | `POST` | `/v1/workflows` |
| List | `GET` | `/v1/workflows` |
| Get | `GET` | `/v1/workflows/{workflow_identifier}` |
| Update (creates a new version) | `PUT` | `/v1/workflows/{workflow_identifier}` |
| Delete | `DELETE` | `/v1/workflows/{workflow_identifier}` |
| Trigger a run | `POST` | `/v1/workflows/{workflow_identifier}/runs` |

```bash
curl -L -X POST 'https://api.port.io/v1/workflows' \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H 'Content-Type: application/json' \
  --data @workflow.json
 ```

Fallback: a `409` on create means the `identifier` is taken, `PUT` an update
instead. A `422` usually means a `connections` entry references a node
identifier that doesn't exist, or a `CONDITION`/`INPUT` connection is missing
`sourceOutletIdentifier`, check [Common pitfalls](#common-pitfalls) below.

## Complete examples

[assets/self-service-deploy-workflow.json](assets/self-service-deploy-workflow.json) -
self-service trigger, environment branching with a `CONDITION` node, and a
Slack notification.

[assets/event-driven-ai-incident-response.json](assets/event-driven-ai-incident-response.json) -
event trigger with a JQ filter, an `AI` node with `outputSchema` for
structured output, and an entity upsert.

[assets/approval-workflow.json](assets/approval-workflow.json) - self-service
trigger gated by an `INPUT` approval step before a production deploy.

## Common pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| `.outputs.my-node.field` silently returns nothing | Hyphens in a node identifier break JQ dot notation (`-` reads as subtraction) | Use bracket notation `.outputs["my-node"].field`, or keep node identifiers snake_case so dot notation works |
| Adding `variables` makes existing output references break | `variables` **replaces** a node's entire default output, `response` and friends disappear | Re-declare anything downstream still needs inside `variables`, e.g. `"response": "{{ .result.response }}"` |
| `CONDITION`/`INPUT` connection has no effect, or workflow rejects it | Missing `sourceOutletIdentifier` (or `fallback: true`) on the connection | Every outgoing connection from a `CONDITION` or `INPUT` node must set `sourceOutletIdentifier` matching one of the node's `outlets`, or `fallback: true` |
| `UPSERT_ENTITY` (or another structured node) after an `AI` node gets nothing | The AI node emitted free-form text, not JSON | Set `outputSchema` (JSON Schema, `type: "object"`) on the AI node, then parse with `{{ .outputs.node_id.response \| fromjson \| .field }}` |
| Event trigger fires but `.outputs.trigger.diff.before` is unexpectedly `null` | `ENTITY_CREATED` has no `before`, `ENTITY_DELETED` has no `after` | Branch on `.outputs.trigger.action` (`CREATE`/`UPDATE`/`DELETE`) before reading `diff.before`/`diff.after` |
| Workflow silently does nothing when a node fails mid-graph | Default `onFailure` is `"terminate"`, the whole run stops | Set `"onFailure": "continue"` on `WEBHOOK`, `UPSERT_ENTITY`, `KAFKA`, or `INTEGRATION_ACTION` nodes that shouldn't block the rest of the run |
| GitHub Actions workflow never fires | Used `WEBHOOK` to call the GitHub API by hand, or used the wrong field name for status reporting | Use `INTEGRATION_ACTION` with `integrationProvider: "github-ocean"`, and `reportWorkflowStatus` (not `reportStatus`) to get status back in Port |

## Quick reference

- Node types: `SELF_SERVE_TRIGGER`, `EVENT_TRIGGER` (triggers); `WEBHOOK`,
  `UPSERT_ENTITY`, `INTEGRATION_ACTION`, `KAFKA`, `CURSOR_AGENT`, `AI_AGENT`,
  `AI` (actions); `CONDITION`, `INPUT` (flow control). Full reference:
  [references/node-types.md](references/node-types.md).
- Data access: `{{ .outputs["node_id"].field }}` (previous node output),
  `{{ .outputs.trigger.field }}` (always aliases the trigger that fired),
  `{{ .secrets["name"] }}`, `{{ .workflowRun.trigger.by.email }}`. Full
  reference: [references/data-flow.md](references/data-flow.md).
- Permissions: `{}`/omitted = Admin only; `roles`/`users`/`teams` = static OR
  match; `policy` = dynamic rules over `user`, `userTeams`, or `form`
  context. Full reference: [references/permissions.md](references/permissions.md).
- Auth: `POST /v1/auth/access_token` with `clientId`/`clientSecret` for a
  bearer token; no `Authorization` header needed when a workflow node itself
  calls `https://api.port.io`.
- Workflow top-level fields: `identifier` (required, ≤60 chars,
  `^[A-Za-z0-9@_:-]+$`), `title`, `icon`, `description`, `category` (groups
  it in the UI), `allowAnyoneToViewRuns` (default `true`), `nodes`,
  `connections`.
