---
name: crowdsec-service-api
description: Use when the user wants to drive the CrowdSec Console **Service API (SAPI)** — the premium cloud REST API at admin.api.crowdsec.net — to programmatically manage blocklists (add/remove/bulk IPs, share, subscribe engines), allowlists, firewall/appliance integrations (Palo Alto, Fortinet, Cisco, F5, Sophos, pfSense/OPNsense…), remediation ROI metrics, and org-level decisions. Acts on the user's behalf with their API key. This is the cloud/API skill — for the local engine, cscli, and bouncers use the `crowdsec` skill.
verified:
  - date: 2026-07-29
    version: "1.70.52"
    env: sapi
    notes: "key resolution + GET /info validation + list recipes against production SAPI"
---

# CrowdSec Service API (SAPI) — cloud blocklist / allowlist / integration automation

SAPI is the **premium** REST API behind the CrowdSec Console. It manages
**cloud-side** objects (private blocklists, allowlists, decisions, firewall integrations)
that then push down to enrolled engines and bouncers. It is **not** the local
engine API — there is no `cscli` here, only HTTPS.

- **Base URL:** `https://admin.api.crowdsec.net/v1`
- **Auth:** `x-api-key: <key>` header on every call. (One exception: the
  integration *content* endpoint uses HTTP Basic with credentials minted at
  integration creation — see [references/integrations.md](./references/integrations.md).)
- **Interactive API docs:** <https://admin.api.crowdsec.net/v1/docs> · spec
  <https://admin.api.crowdsec.net/v1/openapi.json>

## Boundary — this skill vs the `crowdsec` skill

| You want to… | Use |
|---|---|
| Create/manage a **private blocklist** in the cloud, push IPs to it via API | this skill |
| Wire a firewall/appliance (Palo Alto, Fortinet…) to a cloud **integration** | this skill |
| Manage **cloud allowlists**, subscribe engines/tags/orgs to lists | this skill |
| Create/manage **org-level decisions** (targeted or ad-hoc bans, non-IP scopes, per tag/entity) | this skill |
| Pull **remediation ROI metrics** | this skill |
| Install / run / debug the **local engine**, `cscli`, bouncers, WAF | the `crowdsec` skill |
| **Enroll** an engine into the Console (`cscli console enroll`) | the `crowdsec` skill → `references/install/console.md` |
| Configure a **local** allowlist/whitelist on one engine | the `crowdsec` skill → `references/configure/allowlists.md` |

Cloud allowlists/blocklists here only take effect on an engine once that engine
is enrolled **and** subscribed to the list. The enrollment half lives in the
`crowdsec` skill.

## Operating contract

Every call here hits production and can change what subscribed engines enforce.

**1 — Resolve the key.** Never echo it, never write it anywhere but the file
below:
```bash
KEY="${CROWDSEC_SAPI_KEY:-$(cat ~/.config/crowdsec/sapi_key 2>/dev/null)}"
[ -n "$KEY" ] || echo "No key: export CROWDSEC_SAPI_KEY or store it in ~/.config/crowdsec/sapi_key (chmod 0600)"
```

**2 — Validate before acting** — one read call confirms the key and shows *which
tenant* is about to change:
```bash
curl -s -H "x-api-key: $KEY" https://admin.api.crowdsec.net/v1/info
# → {"organization_id":"…","subscription_type":"…","api_key_name":"…"}
```

**3 — Classify read vs mutate.** `GET` / download / `POST …/search` are safe —
run them directly. Every **`POST` / `PATCH` / `DELETE` that changes state**
requires **explicit confirmation first**: present the exact URL and JSON body,
then wait for a yes.

**4 — Extra-danger operations** — spell out the consequence in plain words
*before* the confirm, because subscribed engines **enforce** these lists, so a
change can block or unblock real traffic and is hard to undo:

| Operation | Why it's dangerous |
|---|---|
| `POST …/ips/bulk_overwrite` | Replaces the **entire** blocklist content. |
| `DELETE /blocklists/{id}` · `/allowlists/{id}` · `/integrations/{id}` | Removes the object and everyone's subscription/feed to it. |
| `POST …/ips/delete` | Un-blocks IPs fleet-wide. |
| `POST /decisions` with `target.type: org` | Bans fleet-wide across every enrolled engine in the org. |
| `…/shares` / unshare | Grants/revokes another **organization** access. |
| any `…/subscribers` change | Changes which engines/bouncers enforce the list. |

**5 — Clean up** any object created only to test a recipe. A key that was exposed
anywhere in transit must be rotated.

## Step — Detect the intent

| Cue from user | Go to |
|---|---|
| "test my key", "what org / plan am I on" | [references/authentication.md](./references/authentication.md) |
| "create a blocklist", "push IPs from my SIEM/SOAR", "expire IPs", "share a blocklist with another org", "subscribe my engine to a list" | [references/blocklists.md](./references/blocklists.md) |
| "cloud allowlist via API", "allow my office/CDN across the fleet" | [references/allowlists.md](./references/allowlists.md) |
| "connect Palo Alto / Fortinet / Cisco / F5 / Sophos / pfSense / OPNsense", "firewall integration", "pull IP list in vendor format", "paginate the feed" | [references/integrations.md](./references/integrations.md) |
| "remediation metrics", "how much did CrowdSec save / block", "ROI dashboard" | [references/metrics.md](./references/metrics.md) |
| "org-level decisions via API", "aggregated decisions" | [references/decisions.md](./references/decisions.md) |

## Step — curl cheat sheet

All assume `KEY` is set (see operating contract). `jq` optional for readability.

| Purpose | Command |
|---|---|
| Who am I / validate key | `curl -s -H "x-api-key: $KEY" $B/info` |
| List blocklists | `curl -s -H "x-api-key: $KEY" "$B/blocklists"` |
| List allowlists | `curl -s -H "x-api-key: $KEY" "$B/allowlists"` |
| List integrations | `curl -s -H "x-api-key: $KEY" "$B/integrations"` |
| List / find decisions | `curl -s -H "x-api-key: $KEY" "$B/decisions"` · `…?ips=1.2.3.4` |
| Remediation metrics | `curl -s -H "x-api-key: $KEY" "$B/metrics/remediation?start_date=$FROM&end_date=$TO"` |
| Add IPs to a blocklist *(mutating — confirm)* | `curl -s -H "x-api-key: $KEY" -H 'Content-Type: application/json' -X POST "$B/blocklists/$ID/ips" -d '{"ips":["1.2.3.4"]}'` |
| Create a decision *(mutating — confirm)* | `curl -s -H "x-api-key: $KEY" -H 'Content-Type: application/json' -X POST "$B/decisions" -d '{"duration":"4h","origin":"cscli","scenario":"manual","scope":"Ip","type":"ban","value":"1.2.3.4","target":{"type":"org","value":"<org>"}}'` |

where `B=https://admin.api.crowdsec.net/v1`.

## Hard don'ts

- Don't send a mutating call before the URL + body have been shown and approved
  (see operating contract §3–4).
- Don't use `…/ips/bulk_overwrite` when the user means "add a few IPs" — that's
  `…/ips`. `bulk_overwrite` wipes the list first.
- Don't print, log, or persist the API key anywhere but
  `~/.config/crowdsec/sapi_key`. Resolve it from there or from the env var only.
- Don't assume a cloud allowlist/blocklist is enforced just because the API call
  succeeded — the engine must be enrolled and subscribed, and it pulls on a poll
  cycle (verify locally via the `crowdsec` skill).

## Docs

Canonical: <https://docs.crowdsec.net/u/console/service_api/getting_started>. Each
`references/` file cites the specific upstream page and the live OpenAPI operation
it derives from.
