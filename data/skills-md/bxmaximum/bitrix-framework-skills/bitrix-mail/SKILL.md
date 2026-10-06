---
name: bitrix-mail
description: 'Mail events and templates (CEventType, CEventMessage), Mail\Event::send/sendImmediate and the b_event queue, #FIELD# macros, attachments, Mail::sendResult, sender Identity, mail hooks. Use when sending e-mail from code or debugging lost mail.'
---

# Bitrix mail

Baseline: main 23.0+ · Verified: main 26.800.0

| Task | Read |
| --- | --- |
| Event types, templates, `#FIELD#` macros, HTML escaping | `rules/templates.md` |
| Send (queue or immediate), attachments, `Mail::sendResult()`, sender identity, SMTP choice | `rules/sending.md` |
| Hooks, queue processing and cron, testing, delivery diagnostics | `rules/hooks-testing.md` |

SMTP servers and the `smtp` section of `.settings.php`: `bitrix-settings`. Types and templates in migrations: `bitrix-sprint-migration`.

## Invariants

- Send through a mail event with an admin-editable template (`Mail\Event::send()`); build a raw message with `Mail::sendResult()` only when no template fits.
- The queue (`b_event`) is the default; it is drained after hits or by cron. Use `sendImmediate()` only when the caller needs the outcome now.
- `C_FIELDS` values: strings or arrays of strings. The queue stores objects as `(string)` via `__toString()`, or `''` without it.
- In HTML templates print user data as `#HTML_FIELD#`; `#FIELD#` is inserted raw.
- Validate every address that comes from user input (`check_email()`) before it reaches a field used in `EMAIL_TO`, `CC` or headers.
- A template must be bound to the site: create it with `CEventMessage`, not `EventMessageTable::add()`.
