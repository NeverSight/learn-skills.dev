---
name: telegram-bot-gotd-contrib
description: "Add or repair operational helpers for gotd/td Go MTProto clients: floodwait retries, rate limiting, session/peer/recovery storage, background lifecycle, RPC instrumentation, and connection management."
---

# gotd/contrib

Use alongside telegram-bot-gotd for optional MTProto infrastructure. This is a companion module, not an HTTP Bot API framework.

## Choose only the needed helpers

- Read [the integration guide](references/guide.md) for verified packages, retry ordering, bbolt/Redis storage, peer caches, update recovery, background running, and OpenTelemetry.
- Consult [the dated sources](references/sources.md) for the checked versions and exact constructors. Database packages and telemetry initialization differ between releases.
- Separate session storage, peer/access-hash caching, update-recovery state, and application business data. Persist each concern required by the task.
- Check the restored account's actual identity before forwarding updates into peer stores, recovery handlers or business effects. A session store can already be authorized as a user or a different bot.
- Run a scheduler-based floodwait.Waiter around the client lifecycle; configure retry/wait bounds. A limiter's sample rate is not Telegram's universal allowance.
- Install and configure the selected database or telemetry exporter. Helpers do not provision infrastructure or automatically secure secrets.
- Use one owner of an account session unless the application's concurrency model explicitly supports more. Size core client pools for measured transfer needs.

## Starter

[assets/reliable-echo/main.go](assets/reliable-echo/main.go) combines bbolt session/recovery storage, peer collection, bounded retries, verified bot identity and a typed dispatcher. Its local database contains account credentials. [Offline tests](assets/reliable-echo/main_test.go) check identity/update gating, reply/error handling and a real temporary bbolt close/reopen; they do not contact Telegram.

Build checks do not exercise live updates, reconnection, storage services, proxy reachability, or Telegram RPC behavior. Add targeted integration tests for those requirements.

When flood waits, queued delivery or transfers need user-facing progress, use [bot UX](../telegram-bot-ux/SKILL.md) for accurate status/recovery copy and [accessibility](../telegram-bot-accessibility/SKILL.md) for readable alternatives. Infrastructure middleware alone cannot tell a user that a business action completed.

## Upstream status

Before adopting a newer API or dependency, check [automated source observations](references/upstream-status.md) and compare them with the reviewed baseline.
