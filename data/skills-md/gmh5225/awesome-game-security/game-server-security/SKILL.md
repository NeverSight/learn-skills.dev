---
name: game-server-security
description: Review multiplayer authority, RPCs, sessions, authorization, replication, inventory, economy, purchases, retries, and replay. Use when server or backend state is the security boundary.
---

# Game server and backend security

Trace one consequential operation across client, transport, server, backend, provider, and durable state. Authentication is an input to authorization, not a substitute for it.

## Topic routing

- [Review guide](references/review-guide.md) for authority maps, attack objectives, authorization, economy state, network failure, and verification.
- [Time, ordering, and replay](references/time-ordering-and-replay.md) for clocks, retries, idempotency, prediction, and reconciliation.
- [Repository resources](references/repository-resources.md) for framework and transport selection.

Use `anti-cheat-systems` for detector enforcement, `game-engine-resources` for engine replication models, and `game-supply-chain-security` for released server or plugin artifacts.
