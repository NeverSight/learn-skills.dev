---
name: relay
description: Set up or troubleshoot a Relay agent with relaymessenger, or implement and review a Relay v1 SDK, Webhook, WebSocket, or messaging integration.
---

# Relay v1

Use the locked Relay v1 contract instead of remembered examples.

## Ground truth

1. Read the [locked source record](references/relay-v1-lock.json).
2. Read `contracts/relay-v1-openapi.yaml` from the public Relay-SDK repository
   at `api.public_source.commit` in the lock (or the SDK commit when that field
   is absent), and verify its hash against the API lock. The
   Server commit records its origin; private Server repository access is not
   required. If the public copy and lock disagree, report the stale source.
3. Read the relevant guide and implementation evidence when it is available in
   the workspace.
4. Use Relay docs MCP for discovery when it is available, not to override the
   locked OpenAPI. A plain skill installation does not prove MCP is configured;
   the public contract copy remains usable without it. If a search result
   disagrees with the lock, report it as stale and do not use its route, field,
   event, or package.
5. Prefer `@relaymessenger/sdk` for TypeScript and show equivalent cURL when
   teaching an HTTP operation.

For CLI onboarding, existing Agent Tokens, connecting a runtime, and skill
installation, read [CLI and skills](references/cli-and-skills.md). Creating a
messaging identity and running the code that answers it are separate steps.

**Never invent a route, resource, field, event, package, or migration.** Label
unproved behavior `unknown`.

## Agent event path

Relay derives an agent's event path from saved Webhook subscriptions:

| Saved configuration | Path |
| --- | --- |
| One or more Webhook subscriptions | Webhooks |
| Zero Webhook subscriptions | WebSocket |

There is no transport mode or toggle. A socket upgrade while any subscription
exists returns HTTP `409`. Creating the first subscription closes connected
agent sockets; deleting the final subscription makes the WebSocket path
available. Read [Agent events](references/agent-events.md) before changing
subscriptions or connection code.

## Core model

Relay uses Contacts, Handles, Chats, Messages, parts, Attachments, reactions,
and per-recipient delivery state. A Contact has `kind: "user" | "agent"`.

For details, read only the reference needed:

- [Messaging](references/messaging.md) for sends, parts, Attachments, replies,
  reactions, mentions, and receipts.
- [Chats and Contacts](references/chats-and-contacts.md) for groups,
  membership periods, Add requests, blocks, Contact Cards, and history.
- [Agent events](references/agent-events.md) for Webhooks, WebSocket, ACK,
  path changes, FULL sync, typing, retries, and `trace_id`.
- [SDK and authentication](references/sdk-and-auth.md) for Agent Tokens,
  anonymous creation, scoped deletion, environments, retries, and errors.

## Verification

Prove the integration at its real boundaries:

- signature verification over raw webhook bytes;
- durable event commit before webhook `2xx` or WebSocket ACK;
- duplicate `event_id` handling;
- idempotent REST replies;
- reconnect/replay and FULL-sync behavior for WebSocket consumers;
- first-subscription and last-subscription path changes;
- Webhook SSRF and redirect handling;
- direct and group Message behavior relevant to the product.

Keep Agent Tokens in trusted backend storage. Use a staging API root only with
credentials created in that same environment.
