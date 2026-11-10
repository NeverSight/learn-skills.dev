---
name: xapi-provider
description: Register and operate xAPI provider services through the xapi-to CLI. Use when creating an HTTP, streaming, AI, or WebSocket service; configuring upstream authentication and billing; managing revisions, publishing, rollback, metrics, earnings, or a linked usage Skill. All xAPI management actions use CLI commands with a scoped XAPI key.
---

# xAPI Provider CLI

Use `npx xapi-to` for every xAPI management action. Do not call xAPI management
HTTP endpoints directly. Put service contracts and upstream credentials in JSON
files and pass them with `--file`; this avoids secrets and large payloads in shell
history.

## Start here

Check the installed CLI before building a payload:

```bash
npx xapi-to provider --help
npx xapi-to skill --help
```

The CLI reads the key from saved config, `XAPI_KEY`, or `XAPI_API_KEY`. Never
search the filesystem for a credential or reuse a key found in a fixture. If no
key is configured, ask the user to configure one without echoing it:

```bash
read -rsp 'xAPI key: ' XAPI_KEY_INPUT
printf '\n'
printf '%s\n' "$XAPI_KEY_INPUT" | npx xapi-to config set apiKey=-
unset XAPI_KEY_INPUT
```

Treat upstream values in `privateHeaders` the same way: receive them from the
user, store them only in the requested contract file, and never print them in a
summary. If a command returns a missing-scope error, stop and report the exact
scope. Do not try unrelated keys.

## Choose the workflow

- New service or contract shape: read
  [lifecycle management](reference/lifecycle-management.md), then start from a
  file in [`templates/`](templates/).
- Upstream authentication: read [authentication](reference/auth-types.md).
- Fixed, token, resource, or zero-price billing: read
  [billing](reference/billing-modes.md) and
  [free access](reference/free-api-access.md).
- AI models, typed Decisions, token accounting or upstream-cost billing: read
  [AI services](reference/ai-spec-and-models.md).
- HTTP/2 upstreams or transport metadata in OpenAPI contracts: read
  [HTTP transport](reference/http-transport.md). CLI import/update already
  passes the configuration; no HTTP/2 CLI flag is needed.
- Tripo model generation, texture or conversion: read
  [Tripo asynchronous tasks](reference/tripo-async.md). Verify the target backend
  has the adapter and migration before registering a private draft.
- WebSocket endpoints: read
  [WebSocket endpoints](reference/websocket-endpoints.md).
- OAuth user-context endpoints: read
  [OAuth user context](reference/oauth-user-context.md).
- Relay or aggregator onboarding: read
  [relay onboarding](reference/onboarding-openai-relay.md).
- Before any create or publish: apply the
  [validation checklist](reference/validation-checklist.md).

For a local service LOGO, use `provider create --file ./service.json --logo-file
./logo.png` after checking command help. Read the local LOGO section in
[lifecycle management](reference/lifecycle-management.md) for limits, scope,
conflict rules and upload failure handling.

## Standard lifecycle

Prepare `service.json`, then create and inspect the draft:

```bash
npx xapi-to provider create --file ./service.json
npx xapi-to provider list
npx xapi-to provider get <service-id>
npx xapi-to provider versions <service-id>
```

Use the returned version ID for contract changes. PATCH merges supplied fields;
`--replace` sends a full replacement. Preserve each endpoint's `endpointKey`
across working-revision clones and use the working endpoint ID for partial
patches; see the lifecycle reference for exact matching rules:

```bash
npx xapi-to provider version update \
  <service-id> <version-id> --file ./contract.patch.json
npx xapi-to provider diff <service-id> <major>
```

Submit only after inspecting the diff. Publishing can change live behavior and
the CLI deliberately does not retry an ambiguous write. A passing review can
automatically publish and switch the serving revision; submission is not a
dry run:

```bash
npx xapi-to provider publish \
  <service-id> <revision-id> --changelog-file ./CHANGELOG.md
npx xapi-to provider review <service-id> <revision-id>
npx xapi-to provider versions <service-id>
```

For a published major, create a working revision before editing it. Create a new
major only when the public contract needs a major-version boundary:

```bash
npx xapi-to provider revision start <service-id> <major>
npx xapi-to provider major create <service-id>
```

## Marketplace content and usage Skill

Update service-card content separately from the version contract:

```bash
npx xapi-to provider update <service-id> \
  --description "Short marketplace summary" \
  --about-file ./ABOUT.md \
  --website https://example.com
```

Generate, submit, wait for, link, and fingerprint a service-specific usage
Skill entirely through the CLI:

```bash
npx xapi-to provider skill scaffold \
  <service-id> --output ./my-service/SKILL.md
npx xapi-to skill submit --dir ./my-service
npx xapi-to skill wait <submission-id> --timeout 10m
npx xapi-to provider skill link <service-id> <skill-id>
npx xapi-to provider skill fingerprint \
  <service-id> --skill-version-id <skill-version-id>
npx xapi-to provider skill context <service-id>
```

The scaffold command refuses to overwrite an existing file unless `--force` is
explicit. Check its public URL, HTTP method, body and media types against the
serving contract before submitting; generated text can require correction.
Link only a Skill owned by the same provider. If `skill context`
reports contract drift, update and resubmit the Skill before recording a new
fingerprint. `drift: false` does not prove schemas, media types or transport
are unchanged; the current fingerprint tracks host, major and endpoint keys.
Use `provider skill unlink <service-id>` to remove the association.

## Observe, recover, and earn

```bash
npx xapi-to provider metrics --days 30
npx xapi-to provider metrics <service-id> --days 7
npx xapi-to provider events --limit 50
npx xapi-to provider events --after '<opaque-next-cursor>' --limit 50
npx xapi-to usage wait <request-id> --timeout 1m
```

Pass event cursors back unchanged. Inspect the target before changing live
routing:

```bash
npx xapi-to provider rollback \
  <service-id> <major> --revision <published-revision-id> \
  --reason-file ./ROLLBACK_REASON.md
npx xapi-to provider default-major <service-id> <major>
npx xapi-to provider deprecate <service-id> <major>
npx xapi-to provider restore <service-id> <major>
```

Do not automatically retry an ambiguous rollback response. Read `versions` and
`review` first. Deletion requires both `service:delete` and the explicit service
name or ID:

```bash
npx xapi-to provider delete <service-id> --confirm <service-name-or-id>
```

Provider earnings use the same configured key:

```bash
npx xapi-to earnings
npx xapi-to earnings list --status SETTLED
npx xapi-to earnings transfer 1 --idempotency-key <stable-operation-key>
```

Transfer is one-way. Confirm the amount and settled balance first. Retry only
with the same idempotency key and amount.

## Scope map

| CLI operation | Required scope |
|---|---|
| `provider create` | `service:create` |
| `provider list/get/versions/review/diff`, `provider skill context/scaffold` | `service:read` |
| `provider update`, `provider version update`, Skill link/unlink/fingerprint | `service:update` |
| `provider major create`, `provider revision start` | `version:create` |
| `provider publish` | `service:publish` |
| rollback/default-major/deprecate/restore | `service:rollback` |
| metrics/events | `observability:read` |
| `skill spec/status/wait` | `skill:read` |
| `skill submit` | `skill:submit` |
| earnings summary/list or transfer | `earnings:read` / `earnings:transfer` |
| `provider delete` | `service:delete` |

Scope and ownership are independent. A key with a scope cannot manage another
provider's service or Skill.
