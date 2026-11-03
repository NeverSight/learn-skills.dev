---
name: telegram-bot-advanced-features
description: Design persistent state, durable jobs, webhook deployment, broadcasts, rate limits, retries, monitoring and tests for Telegram bots. Use when operational reliability or multi-worker behavior is part of the task; combine with the chosen framework skill.
---

# Telegram bot production engineering

Read [the engineering guide](references/guide.md) for database/session lifecycle, jobs, inbox/outbox, webhooks, containers, local Bot API servers, broadcasts and troubleshooting. Read [the source ledger](references/sources.md) for the 2026-10-04 API/framework baseline.

## Workflow

1. Establish runtime, database, deployment/update mode, expected load and failure tolerance. Polling and webhooks are mutually exclusive for a token; use one polling consumer and deliberate worker coordination.
2. Separate conversational state from business records. Use explicit ownership keys, constraints/migrations, per-task DB sessions and transactional service methods.
3. Persist work before acknowledging it. Use an inbox for duplicate inbound updates and an outbox/scheduled-job store for durable external work, with bounded attempts and leases.
4. Classify failures before retrying. Respect Telegram retry delays, stop permanent failures and reconcile ambiguous mutations instead of blindly resending.
5. Configure webhook authentication, TLS/proxy/body limits, secret injection, shutdown and health checks for the actual deployment.
6. Validate concurrency, rollback, restart, duplicate delivery, lease expiry and secret rejection offline. Test network/client behavior separately within the authorized scope.

## Invariants

- `AsyncSession` is not safe to share among concurrent tasks. Close sessions and dispose the async engine on shutdown; do not perform slow network I/O inside business transactions.
- In-memory state/jobs may be suitable for ephemeral flows, but durable business outcomes require persistent storage and a defined restart policy.
- An outbox prevents lost intent; leases and dedupe keys do not make a Telegram send exactly once. A timeout after dispatch can mean the send succeeded.
- Inspect the receiver's acknowledgment boundary: handler persistence after an in-memory queue does not protect the crash window before that handler starts. Track inbox receipt and processing completion separately.
- Rate limits vary by method/chat/global traffic. A fixed 25/s loop is not sufficient for every workload. Paid broadcasts spend Stars and must be a deliberate, authorized choice.
- Verify `X-Telegram-Bot-Api-Secret-Token` before processing a webhook; deduplicate separately. An obscured URL is not a substitute for the secret header.
- Local Bot API operation changes file/webhook limits, not every Telegram constraint. Do not describe it as “no limits.”

## Resources

- [scripts/durable_ops.py](scripts/durable_ops.py): offline secret validation, bounded retry decisions and a single-host SQLite leased outbox.
- [scripts/state_lifecycle.py](scripts/state_lifecycle.py): runnable SQLAlchemy 2 async/aiosqlite example with proper base/session/engine lifecycle and concurrent SQLite upsert.
- [offline tests](scripts/test_durable_ops.py) and [async state tests](scripts/test_state_lifecycle.py): run `python -m unittest discover -s telegram-bot-advanced-features/scripts -p 'test_*.py'` from the repository root. `SQLAlchemy[asyncio]`/aiosqlite are needed for the second test module.

Combine with Payments for receipt/fulfillment durability, Mini Apps for backend sessions, and Keyboards UI for callback authorization and sending policy.

## Upstream status

Before adopting a newer API or dependency, check [automated source observations](references/upstream-status.md) and compare them with the reviewed baseline.
