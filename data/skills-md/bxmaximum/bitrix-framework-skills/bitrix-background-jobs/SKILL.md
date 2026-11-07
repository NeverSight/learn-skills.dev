---
name: bitrix-background-jobs
description: 'Deferred and async work in Bitrix — CAgent agents and cron, Application::addBackgroundJob, Messenger queues (messages, receivers, brokers, messenger:consume). Use when moving work out of the request or scheduling it.'
---

# Background jobs

Baseline: main 23.0+ · Verified: main 26.800.0

| Task | Read |
| --- | --- |
| Periodic or delayed task, agents on cron, long agents | `rules/agents.md` |
| Short tail work after the response | `rules/background-job.md` |
| Queue: message, receiver, dispatch, retries | `rules/messenger.md` |
| Queue config, brokers, `messenger:consume`, kernel queues | `rules/messenger-config.md` |

Pick: schedule → agent (on cron); seconds of work after the response → `addBackgroundJob`; retries, volume, parallel workers → Messenger (**Since main 25.100.300**, alpha); one-off long migration → console command (`bitrix-console-commands`).

## Invariants

- Background code has no user context: agents and receivers set `global $USER = null`; no `$_SESSION`/cookies. Pass user/site IDs explicitly.
- On hits, agents, `web`-mode Messenger and `addBackgroundJob()` run after the response is sent, after `OnAfterEpilog` and `session_write_close()`, with the DB pool forced to master.
- Keep job code thin: resolve a service via `ServiceLocator::getInstance()->get()` and call it (no constructor DI in agents — `bitrix-framework`).
- Jobs must be idempotent: agents can run twice in parallel, messages can be redelivered.
- Log failures through a PSR-3 logger (`bitrix-logger`); remove your agents on module uninstall.
