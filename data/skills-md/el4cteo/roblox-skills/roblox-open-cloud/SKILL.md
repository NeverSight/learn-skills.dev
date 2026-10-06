---
name: roblox-open-cloud
description: Open Cloud REST APIs and HttpService - API keys/OAuth, v2 patterns, data/memory stores from outside, publishMessage, place publishing, server restarts, Luau execution, bans, configs/experiments, notifications, webhooks with roblox-signature verification, rate limits, Secrets. Use when building external tools, dashboards, bots, CI/CD, admin panels, or calling web APIs from a game.
---

# Roblox Open Cloud and HttpService

Base URL: `https://apis.roblox.com`. Prefer **Open Cloud** endpoints (API key or OAuth 2.0, stable).
Legacy cookie-authenticated `*.roblox.com` web APIs can break without notice — don't build on them.

## Authentication

- **API keys** (Creator Dashboard → Open Cloud → API Keys): for your own/your group's resources and
  automation. Grant the minimum scopes per universe, set an **IP allowlist** (CIDR) and **expiration**,
  store as a secret (CI secret, vault), send as header `x-api-key: <key>`. Group-owned resources need a
  key created under the group. Introspect a key with `POST /api-keys/v1/introspect`.
- **OAuth 2.0** (authorization code + PKCE): apps acting on behalf of other users (third-party tools).
- Never ship keys in game scripts, attributes, or client code.

## Common endpoints (v2 unless noted)

| Task | Endpoint |
| --- | --- |
| Data store entries | `GET/POST /cloud/v2/universes/{u}/data-stores/{ds}/entries`, `GET/PATCH/DELETE .../entries/{id}`, `:increment`, `:listRevisions`; scopes via `/scopes/{scope}/entries` |
| Ordered data stores | `/cloud/v2/universes/{u}/ordered-data-stores/{ods}/scopes/{scope}/entries[...]` |
| Memory stores | `/cloud/v2/universes/{u}/memory-store/sorted-maps/{map}/items`, `/queues/{q}/items[:read|:discard]`, `memory-store:flush` |
| Cross-server message into live servers | `POST /cloud/v2/universes/{u}:publishMessage` `{ "topic": "...", "message": "..." }` |
| Publish a place file | `POST /universes/v1/{u}/places/{p}/versions?versionType=Published|Saved` (body: `.rbxl`) |
| Restart servers (after an update) | `POST /cloud/v2/universes/{u}:restartServers` |
| Run Luau in a cloud server | `POST /cloud/v2/universes/{u}/places/{p}[/versions/{v}]/luau-execution-session-tasks` |
| Bans | `PATCH /cloud/v2/universes/{u}/user-restrictions/{userId}?updateMask=gameJoinRestriction` (scope `universe.user-restriction:write`), `user-restrictions:listLogs` |
| Experience notifications | `POST /cloud/v2/users/{userId}/notifications` |
| Secrets store | `/cloud/v2/universes/{u}/secrets` |
| Configs / experiments | `/creator-configs-public-api/v1/configs/universes/{u}/repositories/{repo}[/draft|/publish]`, `/experimentation/...` |
| Universe/place settings | `GET/PATCH /cloud/v2/universes/{u}`, `/cloud/v2/universes/{u}/places/{p}` |
| Assets, badges, game passes, developer products, groups, users, inventory | See the Open Cloud reference by feature. |

The authoritative list with scopes and per-endpoint rate limits is the Open Cloud reference
(`create.roblox.com/docs/cloud/reference`) and its OpenAPI description — check it before writing a client.

## Patterns

- **Pagination**: pass `maxPageSize`; follow `nextPageToken` → `pageToken` until empty.
- **Long-running operations**: some calls return an operation `path`; poll `GET /cloud/v2/{path}` until `done`.
- **Filtering**: `filter` query parameter on list endpoints that support it.
- **Rate limits**: read the `x-ratelimit-*` response headers; on `429`, back off exponentially with jitter.
  Data store budgets are **shared** between Open Cloud and live game servers — throttle bulk scripts so they
  don't starve the game (see `roblox-data-stores`).
- **Errors**: JSON `{ code, message }`; retry only `429` and `5xx`.

```bash
# Read one player's data store entry
curl -s "https://apis.roblox.com/cloud/v2/universes/$UNIVERSE_ID/data-stores/PlayerData/entries/User_$USER_ID" \
  -H "x-api-key: $ROBLOX_API_KEY"

# Announce to all live servers (the game subscribes to the "Announcements" topic)
curl -s -X POST "https://apis.roblox.com/cloud/v2/universes/$UNIVERSE_ID:publishMessage" \
  -H "x-api-key: $ROBLOX_API_KEY" -H "Content-Type: application/json" \
  -d '{"topic":"Announcements","message":"{\"text\":\"Update in 5 minutes\"}"}'
```

## HttpService inside games

- Enable **Allow HTTP Requests** (Experience Settings → Security). Server-side only.
- Limits: 500 requests/min per server for external URLs; Open Cloud calls have a separate
  2,500/min per server budget. Always `pcall`; handle non-2xx (`response.Success`).
- Store keys in the experience **Secrets store** (Creator Hub) and read with `HttpService:GetSecret(name)`,
  which returns an opaque `Secret` usable in headers (and `AddPrefix`/`AddSuffix`), not a readable string.
- Only a **subset** of Open Cloud endpoints can be called from games (assets, bans, configs, data/memory
  stores, messaging, notifications, and more — check the in-game HTTP docs list). Calls to other
  `roblox.com` domains are blocked.

```luau
--!strict
local HttpService = game:GetService("HttpService")

local function postToWebhook(url: string, payload: { [string]: any }): boolean
	local ok, response = pcall(function()
		return HttpService:RequestAsync({
			Url = url,
			Method = "POST",
			Headers = { ["Content-Type"] = "application/json" },
			Body = HttpService:JSONEncode(payload),
		})
	end)
	if not ok then
		warn("HTTP request failed to send:", response)
		return false
	end
	if not response.Success then
		warn(`HTTP {response.StatusCode}: {response.StatusMessage}`)
	end
	return response.Success
end

local function banViaOpenCloud(universeId: number, userId: number, reason: string): boolean
	local ok, response = pcall(function()
		return HttpService:RequestAsync({
			Url = `https://apis.roblox.com/cloud/v2/universes/{universeId}/user-restrictions/{userId}?updateMask=gameJoinRestriction`,
			Method = "PATCH",
			Headers = {
				["Content-Type"] = "application/json",
				["x-api-key"] = HttpService:GetSecret("OpenCloudKey"),
			},
			Body = HttpService:JSONEncode({
				gameJoinRestriction = { active = true, displayReason = reason, privateReason = reason },
			}),
		})
	end)
	return ok and response.Success
end

return { postToWebhook = postToWebhook, banViaOpenCloud = banViaOpenCloud }
```

In-game, prefer native APIs (`Players:BanAsync`, `DataStoreService`) over calling Open Cloud for the same thing.
Never log or send player chat/PII to third parties without a legitimate purpose and compliance review.

## Webhooks (Roblox → your server)

Configure in Creator Dashboard → Webhooks. Triggers: subscription purchased/renewed/cancelled/refunded/
resubscribed, right-to-erasure requests, commerce order paid/refunded, transaction refunded.
Verification details and a Node/Python verifier: [references/webhooks.md](references/webhooks.md).

## Related skills

`roblox-data-stores` (budgets, schema), `roblox-tooling` (CI publishing), `roblox-testing` (Luau
execution tests), `roblox-analytics-liveops` (configs, experiments), `roblox-security` (bans, secrets).
