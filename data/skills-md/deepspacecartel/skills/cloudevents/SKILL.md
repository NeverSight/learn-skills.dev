---
name: cloudevents
description: How to design and review event payloads per the CloudEvents specification v1.0 (https://cloudevents.io/, a CNCF graduated project) - project-agnostic. Covers the required/optional/extension context attributes (id, source, specversion, type, time, subject, datacontenttype, dataschema), the abstract type system, the JSON event format (structured vs. batched mode, data vs. data_base64), protocol bindings (HTTP binary/structured mode headers, Kafka, AMQP, MQTT, NATS, WebSockets), documented extensions (distributed tracing, partitioning, sequence, sampledrate, dataref), and versioning guidance from the primer. Use when designing or reviewing an event schema, webhook payload, message-queue/event-bus message format, or any "envelope" for event-driven/pub-sub systems, or when asked to make events interoperable across producers/consumers/brokers.
---

# CloudEvents (v1.0)

A CNCF-graduated spec for describing event data in a common envelope,
so routers, brokers, and consumers can handle events from any source
without source-specific parsing logic. Full spec at
[github.com/cloudevents/spec](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md).
Current version: **1.0** (the spec text itself is at a `1.0.x` patch
level; `specversion` on the wire is always the literal string `"1.0"`
— patch releases don't change it).

CloudEvents defines three layers, and most design questions are about
picking the right one:
1. **Context attributes** — the envelope's metadata (this file).
2. **Event format** — how the envelope+data serialize to bytes, e.g.
   JSON ([`references/json-format.md`](references/json-format.md)).
3. **Protocol binding** — how the serialized event maps onto a
   transport (HTTP headers, Kafka headers, AMQP properties, ...), see
   [`references/protocol-bindings.md`](references/protocol-bindings.md).

## Context attributes

All attribute values are one of the abstract types below — never bind
an attribute directly to a language-native type without going through
this mapping.

### Required

| Attribute | Type | Meaning |
|---|---|---|
| `id` | String | Identifies the event. **MUST** be non-empty. `source` + `id` **MUST** be unique for each distinct event (re-sending the same occurrence should reuse the same `id`). |
| `source` | URI-reference | The context in which the event happened — the producer, not the consumer. Non-empty; absolute URI recommended. E.g. `https://github.com/cloudevents`, `urn:uuid:6e8bc430-9c3a-11d9-9669-0800200c9a66`. |
| `specversion` | String | The spec version in use. **MUST** be `"1.0"`. |
| `type` | String | The kind of occurrence. Non-empty; **SHOULD** be prefixed with a reverse-DNS name you control, and often encodes a version, e.g. `com.github.pull_request.opened`, `com.example.object.deleted.v2`. |

### Optional

| Attribute | Type | Meaning |
|---|---|---|
| `time` | Timestamp | When the occurrence happened (RFC 3339). If the actual time is unknown, producers may use current time — but must be consistent about which they use for a given `source`. |
| `subject` | String | The subject of the event *within the context of `source`* — use when `source` alone is too coarse for a consumer to filter on, e.g. `source` is a storage bucket and `subject` is the specific blob name (`mynewfile.jpg`). |
| `datacontenttype` | String (RFC 2046 media type) | Content type of `data`. Case-insensitive comparison. If absent, JSON format implies `application/json`. |
| `dataschema` | URI | Identifies the schema `data` adheres to. A backward-incompatible schema change **SHOULD** get a new `dataschema` URI (see Versioning below). |

### Extensions

Anything beyond the above is an extension attribute — same naming
rules and type system, no predefined meaning in the core spec. See
[`references/extensions.md`](references/extensions.md) for the
documented ones (distributed tracing, partitioning key, sequence,
sampling rate, claim-check `dataref`) before inventing your own; reuse
one of these rather than minting a near-duplicate. Extensions exist for
**routing and processing metadata** — application data belongs in
`data`, not in a new extension attribute.

## Naming rules (all attributes, including extensions)

- Lowercase ASCII letters and digits only (`[a-z0-9]`), no hyphens or
  underscores.
- Should start with a letter.
- Non-empty; keep it under ~20 characters.
- Never use the name `data` (reserved).

## The abstract type system

| Type | Notes |
|---|---|
| Boolean | `true`/`false` |
| Integer | 32-bit signed range (-2,147,483,648 to 2,147,483,647) |
| String | Unicode, excluding control chars (U+0000-001F, U+007F-009F) and unpaired surrogates |
| Binary | Byte sequence, Base64-encoded (RFC 4648) on the wire |
| URI | Absolute URI (RFC 3986 §4.3) |
| URI-reference | Relative or absolute URI (RFC 3986 §4.1) |
| Timestamp | RFC 3339 |

Every event format (JSON, Avro, Protobuf, ...) defines its own mapping
from these abstract types to its native types — don't assume JSON's
mapping (e.g. Integer → JSON number) applies elsewhere.

## Quick example (JSON format)

```json
{
  "specversion": "1.0",
  "id": "6e8bc430-9c3a-11d9-9669-0800200c9a66",
  "source": "https://github.com/cloudevents",
  "type": "com.github.pull_request.opened",
  "time": "2018-04-05T17:31:00Z",
  "datacontenttype": "application/json",
  "subject": "cloudevents/spec/pull/123",
  "data": {
    "number": 123
  }
}
```

## Versioning (from the primer)

- **`type`** carries the compatibility contract: keep the same `type`
  as long as `data` changes stay backward-compatible; bump `type` (a
  new reverse-DNS suffix, or an embedded version like `.v2`) on a
  breaking change. Consumers are entitled to assume a given `type`'s
  data only changes compatibly.
- On a breaking change, producers should emit both old and new `type`
  for a transition window rather than cutting over instantly.
- **`dataschema`** should track schema evolution: update it for
  compatible changes, change it together with `type` for incompatible
  ones. Treat it as informational/tooling metadata, not a compatibility
  mechanism on its own.
- Decide and document a versioning scheme (semver-in-type, date-based,
  etc.) up front, before calling any event type "stable" —
  see [[semver]] if you need a scheme.

## Size limits

- Producers should keep events compact and reference large payloads
  externally (see the `dataref` extension) rather than inlining them.
- Intermediaries must forward events up to 64 KiB; consumers should
  accept at least that much. Treat 64 KiB as the safe interoperability
  floor, not a hard ceiling every transport enforces.
- Extension attributes are especially cost-sensitive in HTTP binary
  mode: they become individual headers, and many HTTP servers cap total
  header size as low as 8 KiB.

## Gotchas

- `specversion` is always the literal `"1.0"` on the wire — don't
  encode the spec's own patch version (e.g. `1.0.2`) there.
- `source` identifies the *producer's* context, not the consumer and
  not an intermediary that merely relayed the event.
- `data` and `data_base64` (JSON format) are mutually exclusive — see
  [`references/json-format.md`](references/json-format.md) for exactly
  when each applies.
- In HTTP **binary mode**, `datacontenttype` maps to the real
  `Content-Type` header and must NOT also appear as a `ce-datacontenttype`
  header — every other attribute (including extensions) gets a `ce-`
  prefix. Details and other transports in
  [`references/protocol-bindings.md`](references/protocol-bindings.md).
- Don't invent a nested `"extensions": {...}` object — extension
  attributes sit flat at the top level alongside the core ones, exactly
  like core attributes.
- A generic/self-explanatory occurrence doesn't need a bespoke `type`
  taxonomy any more than a REST API needs a bespoke error shape for
  everything — see [[rfc9457]] for the same tension on the error side.
