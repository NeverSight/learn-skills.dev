---
name: island-mode-server
description: >
  Build an on-premise fallback server that keeps a live two-way RxDB replica of
  a site's slice of Firestore, takes over serving LAN terminals when the cloud
  is unreachable, and flushes offline work back on reconnect. Use when: (1) a
  physical site (store, gym, clinic, warehouse) must keep taking bookings,
  moving stock and toggling hardware through an internet outage, (2) kiosk or
  staff PWAs must switch between a cloud API and a local API on their own,
  (3) an existing offline server needs auditing: a reconnect flush that
  double-counts stock, a replica that stops pulling, a failover that never
  finds the box, (4) the user mentions: island mode, offline fallback server, LAN
  failover, on-prem replica, local server with two-way sync to Firestore,
  "the site keeps working when the internet is down", replicateFirestore,
  rxdb/plugins/replication-firestore, serverTimestamp checkpoint,
  _offlineCreated, _locallyModified, syncedIds, FieldValue.increment,
  heartbeat cron, apiBaseUrl, HMAC device auth, island.local, avahi. Carries
  the three replication tiers, the checkpoint stamp every cloud write needs,
  the per-ID stock-delta fold-out, idempotent ingestion keyed on
  client-generated IDs, the offline-gated staff token fallback, the
  heartbeat and status chain, and a 17-test vitest suite for the trust-critical
  logic. Node/NestJS local server and Firestore cloud with Next.js route
  handlers as the reference API; the HTTP framework, IdP and vocabulary are
  seams in architecture.md. Not a read cache, not multi-master sync between
  sites, and not for a cloud database other than Firestore.
---

# Island-Mode Server

A small Node server runs at the physical site holding a live RxDB replica of
the site's slice of Firestore. While the internet is up it is invisible; when
the internet drops, kiosk and staff terminals on the LAN fail over to it and
the site keeps taking orders, moving stock and toggling hardware. On
reconnect, offline work flushes back to the cloud. The one idea the design
turns on: **sync is two systems, not one**. Document-level RxDB replication
keeps state current, and an HTTP flush of business events lets the cloud
apply them with its own logic (stock increments, audit ingestion). Neither
alone is sufficient.

## When to use

- A site must survive internet outages with real writes (bookings, stock,
  hardware control), not just cached reads.
- Terminals are browser-based (PWA or kiosk) and must fail over transparently.
- Firestore is the cloud source of truth and stays that way.

## When NOT to use

- Pure read caching, or a PWA that only needs Firestore's built-in offline
  persistence: the Firebase SDK already does that, with no server.
- A different cloud database (Supabase, Postgres): the replication tier
  concept travels, but every template here is Firestore-specific.
- Multi-master sync between peer sites: this design is strictly
  hub-and-spoke, with the cloud as source of truth and last-write-wins
  conflicts.

## Architecture

```
            Internet
               |
      +--------+---------+
      | Cloud (SSoT)     |  Firestore + public API + cron status marker
      +--------+---------+
        |             |
   RxDB replication  HTTP flush (reconnect)
        |             |
      +-+-------------+-+
      | Local server    |  Node/NestJS + RxDB, LAN :443 via nginx TLS
      +--------+--------+
               |
     LAN: kiosk PWA, staff PWA, hardware controllers
```

The seam contract with the host lives in
[architecture.md](references/architecture.md) (*Adaptation contract*): the
rename table from `location / booking / inventory / lock / staff / pricing`,
the tenant field, the cloud API framework, the IdP and the hardware auth.

## Critical facts

1. **Every cloud write to a replicated collection stamps the checkpoint
   field and `_deleted: false`.** The RxDB Firestore plugin pulls by
   `serverTimestamp > checkpoint`, so an unstamped document is never pulled.
2. **Each collection gets one of three replication tiers.** Pull-only for
   config the site consumes, bidirectional for operational state the site
   mutates, push-only for logs the site produces; the wrong tier for a
   collection is the main design error.
3. **In-memory RxDB storage loses all offline work on an offline restart.**
   The replica repopulates from Firestore, but offline-created documents are
   gone, so the storage trade-off is decided explicitly in
   [replication.md](references/replication.md).
4. **Cloud ingestion is idempotent.** The flush is at-least-once, so every
   apply is keyed on the client-generated ID and checks a receipt only the
   ingestion writes, never the document replication pushes.
5. **Bidirectional pushes carry only local changes.** The push filter sends
   documents flagged `_offlineCreated` or `_locallyModified`, so pulled cloud
   documents do not bounce back.
6. **Terminals prefer the cloud.** Failover engages only after N consecutive
   health failures, and while offline they keep rescanning for the local
   server on every tick, not once at the transition.

## Hard rules

> **Never expose the cloud sync-ingestion endpoints without auth.** They apply
> stock increments and inject orders. A shared-secret header is the minimum.

> **Never verify offline staff tokens leniently while online.** The
> decode-without-verification fallback is an accepted LAN-only trade-off; it
> must be gated on the server actually being offline, or it becomes a bypass
> of signature verification.

> **Never reset local stock deltas for transactions that have not confirmed as
> synced.** Reset per ID on acknowledgment, or offline sales double-count or
> vanish from availability.

> **Never let the local server invent business rules the cloud owns** (opening
> hours, pricing). Replicate the config and compute from it, or island-mode
> behaviour diverges from the website.

## Quick start

Copy each code block as written to the path on its first line; renames, imports and seams are the only edits.
Variants and extra hardening go in new files around a template; a suspected defect goes in the handover.

1. Model collections into tiers and name the seams:
   [architecture.md](references/architecture.md).
2. Stand up RxDB and replication with custom-token auth and security rules:
   [replication.md](references/replication.md).
3. Add the reconnect flush and idempotent cloud ingestion:
   [sync-flush.md](references/sync-flush.md).
4. Wire the heartbeat and status chain and client failover:
   [network-failover.md](references/network-failover.md).
5. Guard the local API and mirror the endpoints terminals need:
   [auth.md](references/auth.md), [local-api.md](references/local-api.md).
6. Deploy on site: both env files keep every name in operations.md
   (`GOOGLE_APPLICATION_CREDENTIALS` is a path read from the environment, not
   to be inlined; `LOCATION_ID` required), systemd, nginx TLS, mDNS, CORS:
   [operations.md](references/operations.md).
7. Carry [behavior.test.ts](assets/behavior.test.ts) into `local-server/src/`,
   point its `../next/` imports at `lib/island/` and `lib/sync/`, install
   vitest, and run it unmodified: 17 tests.
8. Hand over the storage loss window, the `replicationStamp()` audit of the
   host's own writes, the mirrored secrets, and the terminal CA and CORS:
   [operations.md](references/operations.md) (*Handover*).

## Reference directory

| Scenario | Trigger keywords | Reference |
|---|---|---|
| Topology, tiers, seams, rename table | pull-only, bidirectional, push-only, dual-path, locationId, conflict | [architecture.md](references/architecture.md) |
| Replica setup, schemas, checkpoint trap | RxDB, replicateFirestore, serverTimestamp, custom token, storage-memory, firestore.rules | [replication.md](references/replication.md) |
| Reconnect flush, stock deltas, ingestion | flushAll, idempotent, receipt, FieldValue.increment, localDelta, syncedIds | [sync-flush.md](references/sync-flush.md) |
| Outage detection and API switching | heartbeat, lastHeartbeatAt, cron, NetworkManager, apiBaseUrl, failover | [network-failover.md](references/network-failover.md) |
| Local API auth | AuthGuard, HMAC, replay window, offline JWT fallback, kiosk key | [auth.md](references/auth.md) |
| Offline endpoints and writes | availability, mutex, offline booking, check-in, pricing stock filter | [local-api.md](references/local-api.md) |
| On-site deployment, env and handover | systemd, nginx, self-signed TLS, mDNS, avahi, CORS_ORIGINS, .env.example, handover, rollback | [operations.md](references/operations.md) |
| The ledger: what the audit changed, kept, added | provenance, audit, deviations, kept deliberately | [provenance.md](references/provenance.md) |
| Regression cover for the trust-critical logic | vitest, verifyHmac, decodeOfflineToken, delta fold-out, ingestion receipt, opening hours, rescan | [behavior.test.ts](assets/behavior.test.ts) |

Part of the [Timerise Skills](https://github.com/timerise-ai/skills) index, which lists the sibling skills.
