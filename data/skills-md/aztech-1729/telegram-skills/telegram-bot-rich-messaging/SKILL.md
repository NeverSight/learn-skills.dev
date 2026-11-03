---
name: telegram-bot-rich-messaging
description: Design formatted Telegram reports, product catalogs, storefront messages, rich blocks and AI reply streaming. Use for content rendering and interaction layout; combine with the chosen framework, keyboards, and payments skills when the task requires them.
---

# Rich messaging and generated replies

Use [Bot UX](../telegram-bot-ux/SKILL.md) for journeys/button hierarchy and
[Accessibility](../telegram-bot-accessibility/SKILL.md) for readable content and
linear reading order; this skill owns rendering/payload/streaming behavior.

## Choose the output mode

Read [rendering guide](references/guide.md) for formatting, catalogs, reports and media layout. Read [streaming guide](references/streaming.md) for native drafts, stop handling and edit-based fallback. [Sources](references/sources.md) record the 2026-10-04 / Bot API 10.3 baseline.

- **Plain text:** simplest reliable output, including transient status and arbitrary user text.
- **Regular formatted messages:** HTML/MarkdownV2 or explicit entities for ordinary chat output.
- **Rich Messages:** structured content when supported by the chosen Bot API/SDK and target client.
- **Mini App:** browser layout when the interaction needs arbitrary CSS, large tables/forms or substantial client-side state.

Use real feature availability to choose the rendering path; a library's `send_message` is not a wrapper for every rich content method.

## Implementation invariants

- Escape dynamic values for the selected format. Split long content at valid boundaries without cutting entities, tags or surrogate pairs.
- Use UTF-16 offsets for message entities. Prices/metrics/status must come from application data, not invented popularity or fulfillment claims.
- Treat catalog callback payloads as opaque identifiers or validated compact commands. Check product existence, current price and buyer entitlement on the server.
- A storefront renderer does not implement inventory, payment completion or delivery. Load [payments](../telegram-bot-payments-stars/SKILL.md) for that workflow.
- Scope active generation by bot/chat/topic/draft identity. Coalesce updates, respect retry parameters and cancel underlying generation when asked to stop.
- Send the final persistent result separately from a temporary draft. Handle long answers and failed final delivery explicitly.
- Prefer minimal edits to an existing interactive view; tolerate expired/deleted messages and unchanged-content errors without hiding unrelated failures.

## Reusable raw payload builders

[assets/payloads.py](assets/payloads.py) builds regular/rich draft payloads and final Rich Message payloads without guessing SDK signatures. It performs local validation and no network calls. Use the framework's verified request path to send them; do not log token-bearing URLs.

```bash
python -m unittest discover -s telegram-bot-rich-messaging/tests
```

## Validate the actual presentation

Exercise escaping, non-BMP emoji, long answers, stale callbacks, cancellation, retry/backoff and final persistence. Preview representative content in the target Telegram clients before promising exact appearance. Keep fallback rendering when the application requires it.

## Upstream status

Before adopting a newer API or dependency, check [automated source observations](references/upstream-status.md) and compare them with the reviewed baseline.
