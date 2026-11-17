---
name: magpie-quota
description: Check how much is left of the user's AI subscriptions, coding plans and API key balances through magpie (usemagpie.ai) — each usage window's percent used and when it resets, each key's balance, and which account answered last. Use when the user asks how much quota, usage, credit or allowance is left, before starting a long or expensive task, when a request fails with a rate limit or quota error, or to wait until a subscription has allowance again.
---

# magpie quota

[magpie](https://usemagpie.ai) knows every subscription (Claude, Codex,
Copilot, Gemini and others), coding plan and API key the user has added, and
reads what is left of each from its vendor. Ask it rather than guessing or
calling vendors yourself.

## Read what is left

```sh
magpie quota --json            # every subscription, plan and key balance
magpie quota codex --json      # only some: provider id, name, or kind
magpie quota subscription --json   # kind: subscription, plan or balance
```

It asks the vendors now (or uses a reading under a minute old), whether or
not magpie's app is running. Without `--json` it prints a table for people.

If the `magpie` command isn't found, the running app answers the same JSON
on its gateway (port 3425 unless the user changed it in Settings → Gateway):

```sh
curl -s http://127.0.0.1:3425/v1/magpie/quotas
```

## Read the JSON

A list, one entry per account, plan or key:

- `provider`, `name`: the provider's id and display name; `user` the
  account (email or login) when there are several; `plan` the plan's name.
- `kind`: `subscription` (signed-in account), `plan` (coding plan bought
  with a key) or `balance` (a key's money).
- `windows`: each usage window (`name` like "5 hours" or "Weekly"), with `used`
  and `remaining` in percent (0–100), `resetsAt` when it starts again (an
  RFC 3339 time), `unlimited` when it has no limit, and `display` /
  `amount` / `limit` / `unit` when the vendor counts it ("1.2k / 3k").
- `balance`: what a key or account holds, in its own currency or credits
  ("$12.40", "¥37.22", "1.2K credits").
- `error`: why it couldn't be read; say this to the user rather than
  treating the account as empty.
- `asOf` / `readAt`: when the reading was taken, if not just now.
- `lastServedAt`, `last`: when it last answered a request through magpie's
  gateway, and `last: true` on the one that answered most recently.

A window with `remaining` 0 is used up until `resetsAt`. Tell the user the
numbers that matter for their question (what is low, what is used up, when
it comes back) instead of pasting the whole list.

## Wait for allowance

To go on with work a limit stopped, block until a subscription (any of its
accounts) or one account has allowance again:

```sh
magpie quota wait codex                  # exits 0 once there is allowance
magpie quota wait me@example.com --timeout 6h
```

Exit codes: 0 allowance again, 1 timed out, 2 unknown name, 130 Ctrl+C. It
says on stderr what it waits for and until when.

## History

```sh
magpie quota history codex --json --days 7
```

What magpie has read of each window over time (kept 45 days).

## Don't

- Don't run `magpie quota reset`: it spends one of a Codex account's
  rate-limit resets and can't be undone. Only the user decides that.
- Don't change `magpie quota credits`, `auto-reset` or `alert` settings
  unless the user asks.
