---
name: superplane-canvas-builder
description: Design and build SuperPlane workflow canvases from requirements. Translates workflow descriptions into canvas YAML with triggers, components, edges, and expressions. Use when the user wants to create a new workflow, build a canvas, design a pipeline, or wire up components. Triggers on "build canvas", "create workflow", "design pipeline", "automate".
---

# SuperPlane Canvas Builder

Translate workflow requirements into SuperPlane canvas YAML.

## Quick Reference

| Task | Command |
| --- | --- |
| List components | `superplane index components` |
| Components from integration | `superplane index components --from <integration>` |
| Describe a component | `superplane index components --name <name>` |
| List triggers | `superplane index triggers --from <integration>` |
| Create canvas | `superplane canvases create --file canvas.yaml` |
| Update canvas | `superplane canvases update -f canvas.yaml` |

## Order of Operations

Always follow this sequence. The CLI is the primary path — it gives exact names, IDs, and schemas that documentation cannot reliably substitute.

### 1. Verify CLI and Connect

```bash
superplane whoami
```

If `command not found`: **stop**. Tell the user to install the CLI from https://docs.superplane.com/installation/cli and re-run the task. Do not attempt to install it on their behalf. Do not silently fall back to doc-based design.

If not yet connected:

```bash
superplane connect <URL> <TOKEN>
superplane whoami
```

### 2. Understand the Workflow

Before running discovery commands, identify what the workflow needs:

- **What starts it?** → trigger (schedule, webhook, GitHub push, manual)
- **What steps happen?** → each step is a component node
- **Any decisions?** → If or Filter components for branching
- **Any waits?** → Approval, Time Gate, Wait components
- **Which external systems?** → each maps to a provider (e.g., GitHub, Slack, Daytona)

Collect the list of **required providers** from this analysis — you will check them in the next step.

### 3. Discover and Verify Integrations

Run `superplane integrations list` to get all connected integrations in the org. Compare against the required providers from step 2.

**If any required provider is missing:** stop and tell the user before writing any YAML. Example:

> This canvas needs GitHub and Daytona integrations. Your org has GitHub connected but **Daytona is not connected**. Please connect it in the SuperPlane UI (Settings → Integrations) before proceeding.

Do not generate YAML that references providers the org has not connected — it will fail with "integration is required" on every affected node.

**Once all providers are confirmed connected**, discover exact names and schemas:

```bash
superplane integrations list                          # connected instances → real integration IDs
superplane index triggers --from <provider>           # exact trigger names
superplane index components --from <provider>         # exact component names
```

Inspect required config fields and payload shape:

```bash
superplane index triggers --name github.onPush
superplane index components --name semaphore.runWorkflow
```

List runtime options for `integration-resource` fields:

```bash
superplane integrations list-resources --id <id> --type <type>
```

### 4. Select Components and Wire the Graph

Use the **exact** trigger and component names from step 3 — not guesses from documentation.

- Every component needs at least one incoming edge
- Triggers have no incoming edges
- Use named channels for branching (Filter → `passed`/`failed`, If → `true`/`false`)
- Use Merge to fan-in parallel branches

See [Components & Triggers Reference](references/components-and-triggers.md) for the full list.

### 5. Position Nodes

Every node needs a `position: { x, y }`. Nodes are **515px wide × 215px tall** — use these spacing rules to prevent overlap:

| Direction | Increment | Why |
| --- | --- | --- |
| Horizontal (x) | **+600px** per column | 515 width + 85 gap |
| Vertical (y) | **+300px** per row | 215 height + 85 gap |

Start the first node (trigger) at `{ x: 120, y: 100 }`.

**Linear pipeline** — same y, increment x:

```
Trigger: { x: 120, y: 100 }  →  Step A: { x: 720, y: 100 }  →  Step B: { x: 1320, y: 100 }
```

**Branching** — branches share the same x column, spread on y. Center the source node vertically relative to its branches:

```
                                ┌─ Branch A: { x: 1320, y: 100 }
Source: { x: 720, y: 250 }  ───┤
                                └─ Branch B: { x: 1320, y: 400 }
```

**Fan-in (Merge)** — next x column after branches, y centered between them:

```
Branch A: { x: 1320, y: 100 } ──┐
                                 ├── Merge: { x: 1920, y: 250 }
Branch B: { x: 1320, y: 400 } ──┘
```

For 3+ branches, keep adding 300 to y for each branch and center the source/merge accordingly.

### 6. Configure Expressions

Every node output and `root()` returns an **envelope**: `{ data: {...}, timestamp, type }`. The actual payload fields live under `.data`.

Reference upstream data with Expr language inside `{{ }}`:

| Pattern | Description |
| --- | --- |
| `$['Node Name'].data.field` | Named node's output field |
| `root().data.field` | Root trigger event field |
| `previous().data.field` | Immediate upstream field |

> **Common mistake:** writing `$['Create Sandbox'].id` instead of `$['Create Sandbox'].data.id`. Always include `.data.` to reach the actual payload.

**Verify expressions against real payloads.** The CLI commands `superplane index triggers --name <name>` and `superplane index components --name <name>` only return name/label/description — not payload schemas. After the first run (even a failing one), inspect the actual payload structure:

```bash
superplane executions list --canvas-id <id> --node-id <nid> -o yaml
```

Look at:
- `rootEvent.data.data` — the trigger's actual event payload (note the double `.data`: the event envelope wraps the webhook payload)
- `input.data` — what the node received from its upstream node

This is the only reliable way to discover field paths for expressions.

**Trigger payloads follow the external system's webhook format.** For example, `github.onPRComment` uses GitHub's `issue_comment` webhook — PR data is under `data.issue.pull_request` (not `data.pull_request`), and that sub-object only contains URLs, not the full PR with `head.ref`. Do not assume payload structure from the trigger name; always inspect a real execution.

### 7. Apply

```bash
superplane canvases create --file canvas.yaml
# or update an existing canvas:
superplane canvases update --file canvas.yaml
```

Then verify:

```bash
superplane canvases get <name>
```

Check for `errorMessage` or `warningMessage` on any node.

## Fallback: When CLI Is Not Available

If the CLI cannot be installed or used (e.g., user declines, environment restriction):

1. Build the canvas YAML from documentation and skill references.
2. Use **placeholders** for integration IDs (e.g., `<GITHUB_INTEGRATION_ID>`) and list which providers the canvas requires.
3. Add a clear note to the user that they must:
   - Connect any missing integrations in the SuperPlane UI (Settings → Integrations).
   - Install the CLI or use the UI to obtain real integration IDs.
   - Replace all placeholders before applying.
   - Run `superplane canvases create --file canvas.yaml` (or use the UI) to apply.

This path is slower and less reliable. Always prefer the CLI.

## Common Patterns

### Linear: Trigger → A → B → C

```yaml
nodes:
  - { id: trigger, ..., position: { x: 120, y: 100 } }
  - { id: a, ..., position: { x: 720, y: 100 } }
  - { id: b, ..., position: { x: 1320, y: 100 } }
  - { id: c, ..., position: { x: 1920, y: 100 } }
edges:
  - { sourceId: trigger, targetId: a, channel: default }
  - { sourceId: a, targetId: b, channel: default }
  - { sourceId: b, targetId: c, channel: default }
```

### Branch: Filter → passed / failed

```yaml
nodes:
  - { id: trigger, ..., position: { x: 120, y: 250 } }
  - { id: filter, ..., position: { x: 720, y: 250 } }
  - { id: on-success, ..., position: { x: 1320, y: 100 } }
  - { id: on-failure, ..., position: { x: 1320, y: 400 } }
edges:
  - { sourceId: trigger, targetId: filter, channel: default }
  - { sourceId: filter, targetId: on-success, channel: passed }
  - { sourceId: filter, targetId: on-failure, channel: failed }
```

### Fan-out / Fan-in

```yaml
nodes:
  - { id: trigger, ..., position: { x: 120, y: 250 } }
  - { id: a, ..., position: { x: 720, y: 100 } }
  - { id: b, ..., position: { x: 720, y: 400 } }
  - { id: merge, ..., position: { x: 1320, y: 250 } }
  - { id: final, ..., position: { x: 1920, y: 250 } }
edges:
  - { sourceId: trigger, targetId: a, channel: default }
  - { sourceId: trigger, targetId: b, channel: default }
  - { sourceId: a, targetId: merge, channel: default }
  - { sourceId: b, targetId: merge, channel: default }
  - { sourceId: merge, targetId: final, channel: default }
```

### Approval Gate

```yaml
nodes:
  - { id: ci-done, ..., position: { x: 120, y: 100 } }
  - { id: timegate, ..., position: { x: 720, y: 100 } }
  - { id: approval, ..., position: { x: 1320, y: 100 } }
  - { id: deploy, ..., position: { x: 1920, y: 100 } }
edges:
  - { sourceId: ci-done, targetId: timegate, channel: default }
  - { sourceId: timegate, targetId: approval, channel: default }
  - { sourceId: approval, targetId: deploy, channel: approved }
```

## When to Use Other Skills

| Need | Use Skill |
| --- | --- |
| CLI commands and authentication | superplane-cli |
| Debug a failed run | superplane-monitor |

## Documentation

For agents that can fetch URLs, the full SuperPlane docs are available in LLM-friendly format:

- Compact index: https://docs.superplane.com/llms.txt
- Full content: https://docs.superplane.com/llms-full.txt

## References

- [Components & Triggers](references/components-and-triggers.md) — All built-in components and trigger types
