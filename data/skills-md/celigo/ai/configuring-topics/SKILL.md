---
name: configuring-topics
description: Configure Celigo Event Streams topics -- durable message channels that let one flow publish records and any number of other flows consume them, each from its own position. Covers creating and registering topics, retention and licensing, publisher and listener steps, publishing, reading and purging messages, listener positions, and delete rules. Use when creating or registering a topic, wiring a topic publisher or listener, publishing or inspecting messages, diagnosing a listener that never runs, or deleting a topic.
---

<!-- TIER:1 -->

# Configuring Topics (Event Streams)

A topic is a **named, durable message channel**. Publishers append messages; every listener receives all of them, reading from its own position at its own pace; and a message stays readable until the topic's retention window ends, whether or not anything read it. A topic decouples the flow that produces an event from the flows that consume it: add a consumer without touching the producer, pause one consumer while the others carry on, and let it catch up from where it stopped.

A topic is an account resource that lives in one environment, outside any integration -- like a lookup cache. Flows use it through two steps, neither of which takes a connection:

- **Publisher** -- an import with `adaptorType: "TopicImport"`. Every record it receives becomes one message.
- **Listener** -- an export with `adaptorType: "TopicExport"` and `type: "stream"`, the page generator of a flow that runs when messages arrive.

Concerns when working with topics:

- **The topic** -- name, retention, the license that gates it, and registration on the integrations whose flows use it
- **Publishing** -- a publisher step in a flow, API, or Tool, or a direct publish call
- **Listening** -- a listener step, and the flow-enable transition that subscribes it
- **Messages** -- reading what is retained (never moves a listener) and purging it (irreversible)
- **Positions** -- each listener's offset on the topic: where its next run resumes

## How to Run the Steps

This skill names each step by what it reads or changes; the exact calls depend on how you reach the account. Read the one reference that matches your tools -- both follow the step numbers of How to Build an Event Stream below, then the headings of Messages and Positions, Diagnosing a Listener That Never Runs, and Delete, Restore, and Copies:

- **Celigo MCP tools** (`upsert_export`, `upsert_import`, `upsert_flow`, `patch_flow`, ...) -- [references/mcp.md](references/mcp.md). The deployed server has no topic tools: it writes the listener and publisher steps and their flows, while creating, registering, publishing to, reading, purging, and deleting topics take the CLI, the Celigo UI, or the REST API.
- **The `celigo` CLI** -- [references/cli.md](references/cli.md)

Listing topics and reading messages, positions, dependencies, and the audit log only read. Creating, updating, registering, deregistering, and deleting a topic write to the account. Publishing reaches every flow subscribed to the topic -- each one processes the message -- and purging deletes every retained message for good, so confirm both with the user first.

## When to Use a Topic

| Need | Use |
|---|---|
| One event, several independent consumers | A topic -- each listener flow receives every message |
| Hand records from one flow to others | A topic -- chaining with `_runNextFlowIds` passes no records ([building-flows > Configure chaining](../building-flows/SKILL.md#10-configure-chaining-if-needed)) |
| A consumer that can be paused and catch up | A topic -- a listener whose flow is disabled keeps its position and resumes from it, as long as the messages are still retained |
| Enrich records mid-flow from published data | Not a topic -- a listener can't be a lookup step. Listen in its own flow, or keep the reference data in a [lookup cache](../configuring-lookup-caches/SKILL.md) |
| React to events in an outside system | A listener on that system (webhook, NetSuite or Salesforce listener, CDC) -- [configuring-exports > Listeners](../configuring-exports/SKILL.md#listeners). An outside system can also publish to a topic directly, with an API token scoped to it |

## Quick Reference

### Topic Fields

| Field | Rules |
|---|---|
| `name` | Send one: the API saves a topic without a name, and it can't be told apart in lists. Up to 200 characters. Names aren't unique -- steps bind the `_id`, so a rename never breaks one |
| `description` | Up to 5,120 characters; display only |
| `retentionMs` | Milliseconds a message stays readable, read or not. Default `604800000` (7 days); at least `3600000` (1 hour); at most `7776000000` (90 days) and the license's `topics.retentionCeilingDays`. Shortening it drops messages older than the new window |
| `externalId` | Your own key, to find the topic again without storing its id (a list filter) |
| `draft` | Set only on create: the topic deletes itself 48 hours later unless an update sets `draft` to `false` |
| `__integrationIds` | Create only: registers the new topic on these integrations. Never stored or echoed back; a registration that fails is reported in `__failedIntegrationRegistrations`, and the topic is still created |

Only `name` and `description` can be changed on their own. Any other change is a full update, and a full update clears `description` and `externalId` and resets `retentionMs` to 7 days when the body leaves them out -- always send the complete topic.

### License and Quota

Event Streams is licensed. The account license carries `topics.enabled`, `topics.topicsAllowed` (how many topics the account may hold), and `topics.retentionCeilingDays`. Listing topics works on every account; creating or updating one, and every message operation, needs the entitlement -- without it they fail with `topics_subscription_required` (422 on topic writes, 403 on message calls). The quota is checked when a topic is created or restored from the recycle bin (`topics_limit_exceeded`), nothing warns as the account approaches it, and topics in the recycle bin don't count.

### The Two Steps

| Step | Resource | Required | Defaults | Schema |
|---|---|---|---|---|
| Publisher | import, `adaptorType: "TopicImport"` | `topic._topicId` | `topic.batchSize` 1000 | [configuring-imports topic.yml](../configuring-imports/references/schemas/topic.yml) |
| Listener | export, `adaptorType: "TopicExport"`, `type: "stream"` | `topic._topicId` | `topic.startPosition` `latest`, `topic.maxWaitTimeMs` 30000 | [configuring-exports topic.yml](../configuring-exports/references/schemas/topic.yml) |

`topic._topicId` is the topic's `_id`, never its name. Neither step takes a `_connectionId`: with one, the save validates the step as that connection's adaptor and fails. The step rules live in [configuring-exports > Listeners](../configuring-exports/SKILL.md#listeners) and [configuring-imports > Topic Imports](../configuring-imports/SKILL.md#topic-imports-event-streams); this skill covers the topic they share.

### Schema Index

The listener and publisher step schemas are the `topic.yml` files linked under The Two Steps. The topic's own request and response shapes -- the topic, publish and its per-message results, a page of messages, a listener's position, and the purge result -- are on the API reference's [Topics](https://developer.celigo.com/api/api-reference/data-stores/topics.md) page (agent-readable markdown).

## Related Skills

- [configuring-exports > Listeners](../configuring-exports/SKILL.md#listeners) -- the topic listener step (`TopicExport`)
- [configuring-imports > Topic Imports](../configuring-imports/SKILL.md#topic-imports-event-streams) -- the publisher step (`TopicImport`)
- [building-flows > Create disabled, test, enable](../building-flows/SKILL.md#11-create-disabled-test-enable) -- enabling a flow is what subscribes its listener
- [configuring-imports > Writing Exactly Once](../configuring-imports/SKILL.md#writing-exactly-once) -- idempotent writes in listener flows
- [managing-integrations](../managing-integrations/SKILL.md) -- registration on integrations, cloning, and promotion across environments
- [managing-api-tokens > Decide the scope](../managing-api-tokens/SKILL.md#3-decide-the-scope) -- tokens that can publish to and read only named topics
- [configuring-lookup-caches](../configuring-lookup-caches/SKILL.md) -- the other environment resource registered on integrations; use it for enrichment

<!-- TIER:2 -->

## How to Build an Event Stream

### 1. Plan publishers and listeners

- **The message.** What one message stands for (an order, an order line), and its shape: any JSON object up to 1 MiB serialized. A listener's flow receives each message as its record, exactly as it was published -- no envelope, no timestamp.
- **Who publishes.** A publisher step in a flow, an API, or a Tool, or a direct publish call -- from outside Celigo too, with an API token scoped to the topic.
- **Who listens.** One listener flow per consumer. Every listener receives every message, from its own position.
- **Retention.** At least the longest time a listener may be paused or failing before someone fixes it. Messages older than the window are dropped whether or not anything read them; a listener paused longer than that never sees them and resumes from the earliest message left.
- **Duplicates.** The same message can be processed more than once (step 7), so plan an idempotent write for every listener flow.

### 2. Check for an existing topic

List the account's topics, filter by `externalId`, or list what one integration has registered. Names aren't unique: before reusing a topic, confirm it by `_id` and description, and see what already publishes to and listens on it (its dependencies).

### 3. Create the topic and register it

Create the topic with a name, a description of what it carries, and a retention period; add an `externalId` if something must find it again by key. Flows publish and listen on topics registered on their integration. Register the topic on create (`__integrationIds`) or afterwards through the integration's topic registration -- or let the flow do it: saving a flow with a step bound to a topic registers that topic on the flow's integration. Registration adds no alias, unlike a lookup cache's.

### 4. Build the publisher

An import with `adaptorType: "TopicImport"` and `topic._topicId`, with no connection and no create, update, or upsert logic: every record becomes one message.

- Without a mapping, the message is the record as the step received it; a mapping reshapes it.
- With `oneToMany: true` and `pathToMany`, each element of that array is published as its own message, carrying the rest of the parent record (without the array) under `_PARENT`.
- `topic.batchSize` (default 1000) is how many records go per publish request; lower it when messages are large.

The step can publish from a flow, from an API, from a Tool reached through a `ToolImport` step, or on its own through an import invoke. A flow or API test run publishes nothing -- import steps are mocked there -- while an invoke publishes for real to every subscribed flow.

### 5. Build the listener and its flow

An export with `adaptorType: "TopicExport"`, `type: "stream"`, and `topic._topicId`, with no connection, no `cdc` object, and no `isLookup`. Make it the flow's page generator and create the flow with `disabled: true` and no schedule.

- **`topic.startPosition`** -- `latest` (the default) delivers only messages published after the listener subscribes; `earliest` first replays every message the topic still holds, the moment it subscribes. It's read when the listener is created and whenever its `_topicId` changes, so to reprocess retained history create a new listener with `earliest`.
- **`topic.maxWaitTimeMs`** -- how long the listener collects messages before handing the flow a batch, at least 1000 (default 30000). The first run after a publish starts roughly that long after it; lower it for latency on a quiet topic. The export's `pageSize` caps the records per batch.

Without `type: "stream"` the export still saves but runs as a batch export that never starts on a publish -- see [configuring-exports > Listeners](../configuring-exports/SKILL.md#listeners) for the repair.

### 6. Enable the flow to subscribe

The listener subscribes when its flow goes from disabled to enabled; within about half a minute its position appears (step 3 of Diagnosing a Listener That Never Runs) -- or, on a topic nothing has been published to yet, with the first publish, which the listener still receives. A flow created already enabled never subscribes: it doesn't run when messages are published, and its listener has no position until the flow is disabled and enabled again. Under `latest`, anything published before the subscription formed is skipped -- enable first, then publish. After repairing a listener, disable and re-enable its flow.

Then publish a test message (or invoke the publisher with one record) and confirm the flow ran.

### 7. Make every listener flow's writes idempotent

A message can reach the destination more than once, so key each listener flow's write on the message's business key ([configuring-imports > Writing Exactly Once](../configuring-imports/SKILL.md#writing-exactly-once)):

- An `earliest` listener replays every retained message when it subscribes.
- Every listener processes every message -- including a listener in a copy of the flow cloned within the same environment, which keeps the topic.
- A retried error re-sends its record ([building-flows > Duplicate Records](../building-flows/SKILL.md#duplicate-records)).
- A listener whose saved position expired or was purged resumes from the earliest message still retained.

## Messages and Positions

**Publish.** The body is `{"messages": [ {...}, ... ]}` -- each message one JSON object, at most 1 MiB (1,048,576 bytes) serialized; a bare array fails with 400 `invalid_messages`, and an empty array publishes nothing. A 200 means the body was valid, not that every message was published: read each `responses[].statusCode`. An oversized message fails on its own with 422 `topic_publish_event_too_large` while the rest of the batch publishes. The first publish to a new topic provisions its stream and takes a few seconds longer than later ones.

**Read.** Messages come back oldest first, at most 100 per page (default 50), each as `{timestamp, payload}`, where `payload` is the message as published. Follow `nextPageURL` until it's absent, and narrow by publish time with `time_gt` and `time_lte` (epoch milliseconds). There's no search. Reading never moves any listener's position.

**Purge.** Deletes every retained message and keeps the topic, its retention, its registrations, and its subscriptions; it can't be undone, and the topic's audit log records it as a `purge` of `messages`. Offsets keep counting after a purge, and enabled listeners receive the next messages as usual. Purge empties the topic; deleting it removes the topic -- choose as with [a lookup cache](../configuring-lookup-caches/SKILL.md#purge-vs-delete----data-vs-resource).

**Positions.** For one listener on one topic the position is `{hasCursor, offset}`, where `offset` is the next message the listener will read, counted from the start of the stream.

- `hasCursor: false` (offset `-1`) -- most often the listener has never subscribed (its flow hasn't gone from disabled to enabled since it was saved, it was saved without `type: "stream"`, or it doesn't listen to this topic), or nothing has ever been published to the topic: an enabled listener's position appears with the first publish, and it still receives that message.
- A disabled flow keeps its listener's position, and on re-enable the flow receives everything published meanwhile.
- While no message has expired or been purged, the retained message count minus `offset` is the listener's backlog.
- When the message at a listener's position is no longer retained -- it expired or was purged -- the listener still reports `hasCursor: true` with that offset, and its next run resumes from the earliest message still retained, whatever its `startPosition`.

## Diagnosing a Listener That Never Runs

1. **Read the listener export.** It needs `adaptorType: "TopicExport"`, `type: "stream"`, and the `_id` of the topic the publisher uses in `topic._topicId`. Without the type, repair the export as in step 5, then toggle the flow.
2. **Read the flow.** It must be enabled. A flow created enabled has never subscribed: disable it, then enable it.
3. **Read the listener's position.** `hasCursor: false` most often means it never subscribed (steps 1 and 2), or that the topic has never received a message (step 4) -- then the position appears with the first publish. `hasCursor: true` means it's subscribed.
4. **Read the topic's messages.** While nothing has expired or been purged, the retained count minus `offset` is what the listener hasn't read yet. Nothing unread, or no message with a `timestamp` after the flow was enabled, means nothing was published since it subscribed: check the publisher. Flow and API test runs publish nothing, and a publish answers 200 even when a message was rejected.
5. **Allow for the batch window.** A run starts about `maxWaitTimeMs` (default 30 seconds) after a publish. Then read the flow's runs and errors as for any flow ([troubleshooting-flows](../troubleshooting-flows/SKILL.md#diagnostic-workflow)).
6. **Records missing from runs.** Under `latest`, messages published before the subscription formed were skipped; messages that expired past `retentionMs` (or were purged) before the listener read them are gone, and it carried on from the earliest message left. To reprocess what is still retained, add a new listener with `startPosition: "earliest"`.

## Delete, Restore, and Copies

- **Delete is refused while anything binds the topic**: any export or import with its `topic._topicId` -- even one in no flow -- or a flow that contains one. The 422 `dependencies_not_deleted` names each blocker; read the topic's dependencies, then delete or repoint each one.
- **Deregistering is refused while a step in that integration binds the topic** (400 `not_allowed`). Deleting the topic needs no deregister first: the delete drops it from every integration it was registered on.
- **A deleted topic sits in the recycle bin for 30 days**, missing from lists and answering 404 on reads. Restoring it brings back its retained messages but not its registrations -- register it again. Purging it from the bin deletes it and its messages for good, and steps that bound it must be purged from the bin first.
- **A clone within the same environment keeps the topic.** A cloned export, import, or whole flow keeps `topic._topicId`, so the clone of a listener flow is one more consumer once enabled. A copy in another environment needs that environment's topic: after cloning into another environment, installing a template, or pulling changes, check each topic step's `topic._topicId`.

<!-- TIER:3 -->

## Pre-Submit Checklist

- [ ] The license has Event Streams enabled, and a create leaves the account within `topicsAllowed`
- [ ] `retentionMs` is between one hour and 90 days and within the license's `retentionCeilingDays`
- [ ] A full update of the topic carries `description`, `externalId`, and `retentionMs`
- [ ] The topic is registered on every integration whose flows publish or listen (or a flow save registers it)
- [ ] Listener: `adaptorType: "TopicExport"`, `type: "stream"`, `topic._topicId` set to the topic's `_id`; no `_connectionId`, `cdc`, or `isLookup`
- [ ] Publisher: `adaptorType: "TopicImport"`, `topic._topicId` set to the topic's `_id`; no `_connectionId`
- [ ] `startPosition` chosen deliberately -- `earliest` replays everything retained
- [ ] The listener flow was created with `disabled: true` and no schedule, and is enabled only when ready
- [ ] Every listener flow's write is idempotent
- [ ] Every publish result was checked per message

## Gotchas

1. **A listener flow created enabled never subscribes.** It doesn't run on a publish and its listener has no position until the flow goes from disabled to enabled.
2. **`latest` skips what came before the subscription.** Messages published before the flow was enabled -- or while a flow created enabled sat unsubscribed -- never reach that listener.
3. **`earliest` replays everything retained** the moment the listener subscribes, without any new publish. Make sure the flow's writes are idempotent first.
4. **A listener saved without `type: "stream"`** saves without error and never runs on a publish; a PATCH can't add the type.
5. **A full update erases what it omits.** `description` and `externalId` are cleared and `retentionMs` goes back to 7 days.
6. **A publish 200 isn't per-message success.** Read every `responses[].statusCode`; a message over 1 MiB fails alone.
7. **Test runs publish nothing; an invoke publishes for real**, to every subscribed flow.
8. **Purge is irreversible.** It keeps subscriptions and offsets keep counting -- there's no rewind.
9. **Names aren't unique.** Bind and look up by `_id` (or `externalId`).
10. **Any binding blocks the delete**, even an export or import that's in no flow -- and once the topic is in the recycle bin, the deleted steps that bound it block its purge until they're purged.
11. **Restore doesn't re-register.** Register the restored topic on each integration again.
12. **A cloned listener flow is another consumer.** Same-environment clones keep `topic._topicId`.

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `topics_subscription_required` (422 on create or update, 403 on message calls) | The license doesn't include Event Streams | Check the license's `topics.enabled`; the account owner contacts Celigo |
| 422 `topics_limit_exceeded` | The account holds `topicsAllowed` topics | Delete or reuse an unused topic (topics in the recycle bin don't count), or have the account owner ask Celigo to raise the limit |
| 422 `min` on `retentionMs` | Under one hour (`3600000`) | Use at least `3600000` |
| 422 `topics_retention_exceeds_entitlement` and `max` | Over the license ceiling or 90 days | Stay within `retentionCeilingDays` and `7776000000` |
| 422 `... is not a whitelisted property` on a PATCH | Only `/name` and `/description` patch | Send a full update with every field |
| 400 `invalid_messages` on publish | The body isn't `{"messages": [...]}` | Wrap the messages in a `messages` array |
| `topic_publish_event_too_large` in `responses[]` | One message over 1 MiB serialized | Trim or split that message; the rest were published |
| 422 `invalid_ref` "... is not a valid topic._topicId" | Not a topic `_id` in this environment -- often the name | Look the id up by name or `externalId` |
| 422 `missing_required_field` "http subschema not defined" | A `_connectionId` on a topic step | Remove the connection |
| 422 `not_supported` "Lookup functionality is not available for Stream Export" | `isLookup: true` on a listener | Listen in a separate flow; enrich from a lookup cache |
| 422 `dependencies_not_deleted` on delete | An export, import, or flow still binds the topic | Delete or repoint each one named, then retry |
| 400 `not_allowed` on deregister | A step in the integration binds the topic, or it isn't registered there | Repoint or delete the steps first |
| 404 "already in the Recycle Bin" | The topic was deleted | Restore it, then register it again |
| Listener flow never runs | Not subscribed, nothing published, or the batch window | [Diagnosing a Listener That Never Runs](#diagnosing-a-listener-that-never-runs) |
