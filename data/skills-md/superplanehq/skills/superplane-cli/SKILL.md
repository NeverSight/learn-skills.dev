---
name: superplane-cli
description: Use when working with the SuperPlane CLI to discover integrations, components, and triggers, build or troubleshoot canvases, manage secrets, and monitor executions. Covers authentication, list/get commands, interpreting configuration schemas, wiring channels between nodes, resolving integration binding issues, and inspecting runs. Triggers on "superplane", "canvas", "workflow", "CLI", "connect", "integration is required", "execution".
---

# SuperPlane CLI

Operate a SuperPlane instance through the `superplane` CLI.

## Quick Reference

| Task | Command |
| --- | --- |
| Connect to org | `superplane connect <URL> <TOKEN>` |
| Who am I | `superplane whoami` |
| List/switch contexts | `superplane contexts` |
| List canvases | `superplane canvases list` |
| Create canvas | `superplane canvases create <name>` |
| Create canvas from YAML | `superplane canvases create --file canvas.yaml` |
| Export canvas | `superplane canvases get <name>` |
| Update canvas | `superplane canvases update --file canvas.yaml` |
| List available providers | `superplane index integrations` |
| Describe a provider | `superplane index integrations --name github` |
| List connected integrations | `superplane integrations list` |
| Inspect connected integration | `superplane integrations get <id>` |
| List integration resources | `superplane integrations list-resources --id <id> --type <type>` |
| List components | `superplane index components` |
| Components from provider | `superplane index components --from github` |
| Describe a component | `superplane index components --name semaphore.runWorkflow` |
| List triggers | `superplane index triggers` |
| Triggers from provider | `superplane index triggers --from github` |
| Describe a trigger | `superplane index triggers --name github.onPush` |
| List secrets | `superplane secrets list` |
| Create secret | `superplane secrets create --file secret.yaml` |
| List events | `superplane events list --canvas-id <id>` |
| Trace event executions | `superplane events list-executions --canvas-id <id> --event-id <eid>` |
| List node executions | `superplane executions list --canvas-id <id> --node-id <nid>` |
| Cancel execution | `superplane executions cancel --canvas-id <id> --execution-id <eid>` |

## Verify CLI Is Installed

Before any CLI operation, confirm the CLI is available:

```bash
superplane whoami
```

If this returns `command not found`, the CLI is **not installed**. Stop and tell the user:

> The SuperPlane CLI is not installed. Install it from https://docs.superplane.com/installation/cli and then re-run this task.

Do **not** attempt to install the CLI on behalf of the user. Do **not** continue with doc-based guesswork — the CLI provides exact trigger names, component names, integration IDs, and config schemas that documentation cannot reliably substitute.

## Core Workflow

### 1. Authenticate

Create a service account in the SuperPlane UI, then:

```bash
superplane connect https://superplane.example.com <API_TOKEN>
superplane whoami
```

### 2. Discover What Exists

Run these first to understand what's available:

```bash
superplane index integrations          # available providers
superplane integrations list           # connected instances in this org
superplane index triggers              # all trigger types
superplane index components            # all component types
```

Narrow to one provider:

```bash
superplane index triggers --from github
superplane index components --from github
```

Inspect required config fields and payload shapes:

```bash
superplane index triggers --name github.onPush
superplane index components --name semaphore.runWorkflow
```

List runtime options for `integration-resource` fields (e.g., repos, projects):

```bash
superplane integrations list-resources --id <integration-id> --type <type> --parameters key1=value1,key2=value2
```

Use `superplane integrations list` first to find valid integration IDs.

### 3. Build a Canvas Incrementally

Create a blank canvas, then iterate:

```bash
superplane canvases create my-canvas
superplane canvases get my-canvas > canvas.yaml
# edit canvas.yaml
superplane canvases update --file canvas.yaml
```

See [Canvas YAML Spec](references/canvas-yaml-spec.md) for the full format.

### 4. Manage Secrets

```bash
superplane secrets create --file secret.yaml
superplane secrets list
superplane secrets update --file secret.yaml
superplane secrets delete <name_or_id>
```

### 5. Monitor Runs

```bash
superplane events list --canvas-id <id>
superplane events list-executions --canvas-id <id> --event-id <eid>
```

### 6. Troubleshooting Checklist

Run after every canvas update:

```bash
superplane canvases get <name>
```

Check:
- All required `configuration` fields are present
- Edges use the correct output channels
- No node `errorMessage` remains (especially "integration is required")
- No `warningMessage` about duplicate names
- Expressions reference existing node names (case-sensitive)

## Resolving "integration is required"

When a field type is `integration-resource` (like `repository` or `project`), the node needs a connected integration instance.

1. `superplane integrations list` — confirm the provider is connected
2. `superplane integrations get <id>` — inspect the connection
3. Add `integration.id` to the node in the canvas YAML
4. `superplane integrations list-resources --id <id> --type <type>` — find valid resource values
5. `superplane canvases update --file canvas.yaml` — apply the fix
6. `superplane canvases get <name>` — verify errors are cleared

## When to Use Other Skills

| Need | Use Skill |
| --- | --- |
| Design a canvas from requirements | superplane-canvas-builder |
| Debug a failed execution | superplane-monitor |

## Documentation

For agents that can fetch URLs, the full SuperPlane docs are available in LLM-friendly format:

- Compact index: https://docs.superplane.com/llms.txt
- Full content: https://docs.superplane.com/llms-full.txt

## References

- [Canvas YAML Spec](references/canvas-yaml-spec.md) — Full YAML format with examples
