---
name: proxylane-api
description: Run a ProxyLane residential proxy account through its API. Use when the user asks to check their traffic or balance, buy residential traffic, create a sub-user (a login with its own GB limit) for an office, teammate or client, add or take back a sub-user's GB, pause or delete a sub-user, generate proxy lists, or report traffic usage per sub-user.
license: MIT
---

# ProxyLane API

By [ProxyLane](https://proxylane.dev?utm_source=skills.sh&utm_medium=referral&utm_campaign=agent-skills&utm_content=proxylane-api). The account holds residential traffic in GB. Each sub-user gets its own proxy login and a GB limit taken from that balance, so an office, a teammate or a client spends only what it was given. Full reference: [API docs](https://docs.proxylane.dev/resellers/overview?utm_source=skills.sh&utm_medium=referral&utm_campaign=agent-skills&utm_content=proxylane-api).

## 1. Connect

The key comes from the ProxyLane dashboard: **Settings** → **API keys**, or **API** in the sidebar for a one-click agent setup. It starts with `plr_`.

- Use `PROXYLANE_API_KEY` from the environment. If it is missing, ask the user to set it in their shell or secret store; do not ask them to paste it into chat. An older `PROXYLANE_RESELLER_KEY` also works.
- Never print, log or commit the key. The bundled script reads it and never echoes it.
- Check the connection with `python3 scripts/proxylane.py account`. It shows the traffic balance, the USD balance, the prices and the number of sub-users.

## 2. Know where the traffic is

| Place | Meaning |
| --- | --- |
| Traffic balance (`pool_gb`) | Residential GB on the account and not given to a sub-user yet. A purchase on the site and a `buy` over the API land here |
| USD balance | Money topped up in the dashboard. Pays for `buy` and ISP proxies |
| Sub-user limit | GB given to one sub-user. Only its traffic counts against it |
| Used | Traffic the sub-user already sent. It cannot be returned |
| Available | Limit minus used. Can be returned to the balance |

1 GB is 1,000,000,000 bytes. The API takes GB with up to three decimals; purchases are whole GB. Wholesale reseller accounts keep a separate pool at their own price; the commands are the same.

## 3. Ask before spending or destroying

These need the user's explicit yes, with the amount stated, before you run them:

- `buy` spends the USD balance. Say the GB and the total from `price_tiers` in `account`.
- `delete` stops a sub-user's login for good. Unused traffic returns to the balance.
- `suspend` cuts a sub-user off. Confirm the name.

`allocate` and `reclaim` only move traffic the account already owns; confirm them when the user did not name the sub-user and the amount.

Top-ups of the USD balance happen in the dashboard (card, PayPal or crypto). There is no API for payment; send the user to **Add funds** or **Add traffic** in the dashboard.

## 4. Do the work with the script

Run from the skill directory. Every command prints JSON.

```sh
python3 scripts/proxylane.py account
python3 scripts/proxylane.py buy 500
python3 scripts/proxylane.py create "Office Kyiv" --external-id office-1 --gb 100
python3 scripts/proxylane.py list --search office-1
python3 scripts/proxylane.py allocate SUBUSER_ID 10
python3 scripts/proxylane.py reclaim SUBUSER_ID 2
python3 scripts/proxylane.py reclaim SUBUSER_ID
python3 scripts/proxylane.py suspend SUBUSER_ID
python3 scripts/proxylane.py resume SUBUSER_ID
python3 scripts/proxylane.py delete SUBUSER_ID
python3 scripts/proxylane.py usage SUBUSER_ID --hourly --periods 24
python3 scripts/proxylane.py proxies SUBUSER_ID --country US --count 10 --format host_first > kyiv-us.txt
python3 scripts/proxylane.py history --limit 20
```

`proxies` gives sticky SOCKS5 lines by default, one session per line, like the dashboard. Use `--session rotating` for a new IP on every request and `--protocol http` for HTTP.

`buy`, `create`, `allocate` and `reclaim` send a fresh `Idempotency-Key`. If a response is lost, retry once with the same key, placed before the command: `python3 scripts/proxylane.py --key KEY_FROM_FIRST_TRY buy 50`. The API then returns the first result instead of charging or moving traffic twice.

Find sub-users by your own ID with `list --search`; `external_id` is unique per account. Keep the returned `id` for later calls.

## 5. Common jobs

**Split traffic between offices or teammates.** `account` → if the balance is short, propose `buy` with the total and wait for yes → `create` one sub-user per office with its GB → hand each office its `proxies` file. The same sub-users appear in the dashboard under **Residential Proxies** → **Team**, where the user can see each one's traffic, top it up, pause it or copy its proxies, so point them there to check the result.

**New client.** Same as above with the client's name and CRM ID as `external_id`. A brand-new login can take a few hours to work on every gateway; `login_warming_until` shows until when.

**Monthly refill.** `list --search ID` → `allocate` the new GB. To reset to a fixed monthly amount, `reclaim` the unused part first, then `allocate`.

**Stop a sub-user.** `suspend`. If it leaves for good, confirm and `delete`, which returns the unused GB.

**Usage report.** `list` for every sub-user's `traffic_used_gb` and `traffic_available_gb`, `usage ID` for the daily series, `account` for totals. Flag sub-users under 10% available.

## 6. Read errors

Errors are `{"error": {"code", "message", ...}}` on stderr with exit code 1.

| Code | Next step |
| --- | --- |
| `insufficient_balance` | Ask the user to add funds in the dashboard; `required_cents` is the price |
| `insufficient_pool_traffic` | Propose a `buy`; `available_bytes` is the traffic balance |
| `insufficient_subaccount_traffic` | Return less; `available_bytes` is what is left |
| `purchase_required` | Sub-users open after the first traffic purchase; propose `buy` |
| `subaccount_limit_reached` | Delete an unused sub-user or ask support to raise the limit |
| `idempotency_key_reused` | The key belongs to a different request; use a new one |
| `idempotency_in_progress` | Wait a few seconds and retry with the same key |
| `operation_in_review` | ProxyLane is checking that sub-user; stop and tell the user |
| `subaccount_deleted`, `subaccount_not_found` | Re-list; the ID is gone or wrong |
| `unauthenticated` | The key is wrong or revoked; ask for a new one in Settings → API keys |
| `rate_limited` | Slow down; 120 requests per minute per key |

`"updating": true` on a sub-user means a change is being applied; read it again a few seconds later. Do not repeat the change.
