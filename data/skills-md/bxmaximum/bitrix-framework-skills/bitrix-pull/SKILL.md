---
name: bitrix-pull
description: Covers Pull module — sending realtime events to users/channels from PHP, JS subscription overview, watch tags, when to use Pull vs Messenger vs agents, link to BitrixVue. Applied for live UI updates, notifications, collaborative screens. Key terms — pull, Bitrix\Pull\Event, CPullWatch, CPullChannel, BX.PULL.subscribe, extendWatch, queue server, push.
---

# Realtime Pull (`pull`)

`pull` delivers **short realtime commands** to browsers/mobile via a queue server (WebSocket / long polling / JSON-RPC). Baseline: main **23.0+**. Requires the Pull/queue server to be enabled (`CPullOptions::GetQueueServerStatus()`); otherwise events are dropped after buffering logic.

```php
\Bitrix\Main\Loader::includeModule('pull');
```

## Pull vs Messenger vs Agents

| Mechanism | Use for |
| --- | --- |
| **Pull** | Instant UI sync (“row updated”, counters, presence-like hints) |
| **Messenger** (`bitrix-background-jobs`) | Reliable async **work** with retries/queues (**Since 25.100.300**, alpha) |
| **Agents / cron** | Periodic batch jobs, cleanup, polling external systems |

Do not use Pull as a job queue. Do not use Messenger to push browser paint updates — emit Pull from the worker when the UI must refresh.

## Send to User(s) from PHP

Primary API: `Bitrix\Pull\Event::add($recipient, array $parameters, $channelType = \CPullChannel::TYPE_PRIVATE)`.

Required in `$parameters`: `module_id`, and either `command` (+ optional `params`) or push payload fields.

```php
<?php declare(strict_types=1);

use Bitrix\Main\Loader;
use Bitrix\Pull\Event;

Loader::includeModule('pull');

Event::add($userId, [
    'module_id' => 'vendor.module',
    'command' => 'item.updated',
    'params' => [
        'id' => $itemId,
        'title' => $title,
    ],
    // 'expiry' => 86400, // optional; default applied in Event::prepareParameters
]);

// Multiple users:
Event::add([1, 2, 3], [
    'module_id' => 'vendor.module',
    'command' => 'list.refresh',
    'params' => [],
]);
```

- Recipients: user IDs, channel IDs (32-char strings), or `Bitrix\Pull\Model\Channel` instances.
- Channel types: `\CPullChannel::TYPE_PRIVATE` (default), `TYPE_SHARED`, etc.
- Sending is deferred via `Application::addBackgroundJob` / `Event::send` on epilog — usually you only call `add()`.
- Legacy wrappers: `CPullStack`, `Bitrix\Pull\Push::add` (push notifications path).

On failure, inspect `Event::getLastError()`.

## Shared Tags (`CPullWatch`)

Subscribe users to a **tag**, then broadcast to everyone watching that tag:

```php
<?php declare(strict_types=1);

use Bitrix\Main\Loader;

Loader::includeModule('pull');

\CPullWatch::Add($userId, 'VENDOR_ITEM_' . $itemId);

\CPullWatch::AddToStack('VENDOR_ITEM_' . $itemId, [
    'module_id' => 'vendor.module',
    'command' => 'item.updated',
    'params' => ['id' => $itemId],
]);
```

- `CPullWatch::Extend($userId, $tags)` — refresh subscriptions (also used from pull controllers/JS).
- Tag messages still go through `Event::add` under the hood.

## JS Subscription Overview

Client global: `BX.PULL` (`PullClient`, extension `pull.client` / product core load). Subscribe:

```javascript
const unsubscribe = BX.PULL.subscribe({
    moduleId: 'vendor.module',
    command: 'item.updated', // optional; omit to get all module commands
    callback: (params, extra, command) => {
        // update UI
    },
});

// Watch tag (pairs with CPullWatch):
BX.PULL.extendWatch('VENDOR_ITEM_' + itemId);
```

`subscribe` returns an unsubscribe function. Alternative: `attachCommandHandler` with an object exposing `getModuleId()` and command methods.

In BitrixVue apps (`bitrix-vue`), subscribe in `mounted` / setup and unsubscribe on unmount; keep `moduleId`/`command` identical to PHP `Event::add`.

Queue helper extension: `pull.queuemanager` wraps `BX.PULL.subscribe` + `extendWatch` for list/grid sync patterns.

## Push (Mobile)

Optional `push` / `pushParamsCallback` keys on `Event::add` enqueue mobile push via `CPushManager` when push is enabled (`CPullOptions::GetPushStatus()`). Treat as a separate channel from browser Pull commands.

## Operational Notes

- Parameters must be UTF-8; invalid encoding is rejected.
- Keep payloads small (IDs + flags); fetch heavy data via AJAX/REST after the event.
- Shared channel / guest modes depend on Pull options — verify before designing guest UX.
- Module may expose REST helpers (`Bitrix\Pull\Rest`, controller `config` for watch extend) when `restIntegration` is enabled in pull `.settings.php`.

## Checklist

- [ ] `pull` module loaded; queue server enabled in environment.
- [ ] Events use stable `module_id` + `command` names shared with JS.
- [ ] Recipients are user IDs or valid channels; tags use `CPullWatch` consistently.
- [ ] UI handlers unsubscribe / avoid leaks in SPA/Vue.
- [ ] Pull not used as a durable job queue (use Messenger/agents).
- [ ] Large data loaded on demand after the signal.

## Related skills

`bitrix-background-jobs`, `bitrix-vue`, `bitrix-extensions`, `bitrix-controllers`, `bitrix-rest`.
