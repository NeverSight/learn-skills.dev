---
name: edgegap-deployments-api
description: 'Write backend code that starts, tracks and stops Edgegap game servers through the HTTP API: POST /v2/deployments with player IPs or coordinates, env vars and tags, ready/error/terminate webhooks, status polling within rate limits, stopping and cleaning up orphaned deployments, and handing players the address and external port. Use whenever building a custom matchmaker, allocator, lobby service or CI job for Edgegap (a CI job that only ships a new build: edgegap-launch, which uses edgegap/deploy-action), writing the allocator for EOS or Steam lobbies (choosing a matchmaker, or keeping Unity Matchmaker: edgegap-matchmaking; Nakama: edgegap-nakama), or when someone mentions api.edgegap.com, the Deploy API, deployment webhooks, request_id, or Edgegap error codes 422/429/410. Not for game clients, which must never hold the API token.'
metadata:
  version: "0.2.13"
---

# Edgegap Deployments API for your backend

Use this when the developer's own backend decides when a match starts: a custom matchmaker, a lobby service, an EOS or Steam lobby owner's backend. For Unity Matchmaker (UGS), Unity's `EdgegapAllocator` module already makes these calls: load `edgegap-ugs-matchmaker`. For Nakama, load `edgegap-nakama` instead: the Edgegap Fleet Manager for Nakama already makes these calls. For PlayFab Matchmaking, load `edgegap-playfab`: its Azure Functions already make them. If they just want players matched onto servers and have no backend yet, Edgegap's hosted matchmaker does all of this without code; prefer it. Choosing between these, and designing parties, regions or backfill: `edgegap-matchmaking`. A CI pipeline that only ships a new server build (create the version, smoke-test, promote) needs no code: use Edgegap's GitHub Action, `edgegap/deploy-action` (see `edgegap-launch`).

The code you write calls HTTP. When you act on Edgegap yourself while building it, follow the `edgegap` skill's [references/agent-rules.md](../edgegap/references/agent-rules.md). Endpoint shapes are in [references/api-reference.md](references/api-reference.md).

## Where the token lives

The Edgegap API token is organization-wide and cannot be scoped. It lives only in the backend's secret manager (loaded at startup by the backend, never read by you from the developer's machine), never in a game client, never in a game server or its env vars, never in a lobby owner's client (EOS and Steam guides that call the API from the lobby owner are for prototypes only). Read the base URL from config too, so tests can point elsewhere.

## The allocation flow

```
players grouped by your matchmaker / lobby
  → backend: POST /v2/deployments  {application, version, users[], environment_variables[], tags[], webhook_on_*}
  → 202 {request_id}                         (the server is still starting)
  → webhook_on_ready (or poll GET /v1/status/{request_id})
  → hand each player: fqdn or public_ip + ports.gameport.external
  → players connect, retrying for up to ~1 min (engine still loading after Ready)
  → match ends → server self-stops (ARBITRIUM_DELETE_URL) → webhook_on_terminated
```

Rules that keep it robust:

**Place the server with the players' locations.** `users` takes each player's public IP (`{"user_type":"ip_address","user_data":{"ip_address":"..."}}`) or coordinates (`geo_coordinates` with `latitude`/`longitude`). Edgegap then picks the location with the best and fairest ping for the whole group. Your backend sees each client's IP on its incoming request; don't ask clients to self-report it. One user is enough for testing; send all players for real matches.

**Pin the version.** Deploy a named app version from config (`prod`, `blue`/`green`, or a build tag), never "whatever is newest". Rollout is a config flip; rollback is flipping it back.

**Carry the match in env vars and tags.** `environment_variables: [{key: "MATCH_ID", value, is_hidden: false}]` configures the server (up to 20 per deployment, 4 KB each, no `ARBITRIUM_`/`MM_` names). Mark anything sensitive `is_hidden: true` (encrypted at rest, not readable back through the API), and keep it short-lived, e.g. a per-match join secret the server checks when players connect. Never the Edgegap API token. Add tags (40 characters max each) such as `match-<id>` and the mode, so you can find the deployment later.

**There is no idempotency key, so record before you retry.** The deploy call returns a new `request_id` each time. Store `match → request_id` as soon as the 202 arrives. If the call timed out without a response, look for an existing deployment tagged `match-<id>` (`GET /v1/deployments` with a tags filter) before deploying again, or you will split the lobby across two servers and pay for both.

**Prefer webhooks over polling.** Webhooks are the recommended integration: `webhook_on_ready`, `webhook_on_error`, `webhook_on_terminated`, each `{ "url": "..." }`. Ready and Error never both fire for one deployment. Webhooks are **not retried**, so keep the handler fast and always answer 2xx, and fall back to `GET /v1/status/{request_id}` when no webhook arrives in the expected time. Status and Context APIs are limited to 20 requests per second for the whole organization: polling every deployment in a loop does not scale. The webhook payload carries no documented signature, so put an unguessable per-match token in the webhook URL and check that the `request_id` matches your record.

**Ready is not "accepting players".** Ready means the container started; the engine may need up to a minute to load. Either have clients retry the connection every second for a bounded time, or have the server call your backend when it is truly ready and only then release the address.

**Handle errors as outcomes:**
| Response | Meaning | Do |
|---|---|---|
| `202` | Accepted, deployment starting | Record `request_id`, wait for webhook |
| `400` | Bad request (unknown app/version, bad body) | Fix the request; don't retry as is |
| `401` | Missing or malformed token (`Authorization: token <uuid>`) | Fix config |
| `422` | Couldn't allocate a server (resources too large for the tier, no capacity for those users) | Back off and retry, then tell players "finding a server…"; check vCPU/memory on the version |
| `429` | Rate limit: 40 deploys/s, 20 status+context/s, 10 list/s per organization | Back off; batch; use webhooks |
| `500` | Edgegap error | Retry with backoff, log the `request_id` if any |

On stop, `410` means already terminated: treat it as done.

**Close the loop.** Servers end their own deployments with self-stop. Your backend handles the exceptions: `DELETE /v1/stop/{request_id}` for an abandoned match (everyone left, or the match never started), and a periodic reconciliation. Scope it to deployments your backend created: filter on a tag only your backend sets (e.g. `allocator-prod`) and on `created_at` older than a few minutes, so you never touch matchmaker, test or other-environment deployments, or one whose 202 you haven't recorded yet. Compare that set with the matches you believe are live, and stop orphans by exact ID. The version's max duration is the backstop under that. Never use bulk stop with broad filters in production code; it can end live matches.

**Log the `request_id` everywhere** and show it to players in match history. It's the key Edgegap support needs, and the only way to find a deployment's logs before it stops.

## Allocator sketch

```typescript
const API = config.edgegapApiUrl ?? "https://api.edgegap.com";
const TOKEN = await secrets.get("edgegap-api-token");   // backend secret manager, never shipped
const headers = { Authorization: `token ${TOKEN}`, "Content-Type": "application/json" };

export async function allocate(match: Match): Promise<string> {
  const existing = await db.requestIdFor(match.id);       // retry-safe
  if (existing) return existing;

  const matchTag = `match-${match.id}`.slice(0, 40);
  for (let attempt = 0; attempt < 4; attempt++) {
    if (attempt > 0) {                                    // a failed call may still have deployed
      const found = await findByTag(matchTag);            // GET /v1/deployments, tags eq matchTag
      if (found) { await db.saveRequestId(match.id, found); return found; }
    }
    let res: Response;
    try {
      res = await fetch(`${API}/v2/deployments`, {
        method: "POST", headers,
        body: JSON.stringify({
          application: APP, version: PINNED_VERSION,
          users: match.players.map(p => ({ user_type: "ip_address", user_data: { ip_address: p.ip } })),
          environment_variables: [
            { key: "MATCH_ID", value: match.id, is_hidden: false },
            { key: "JOIN_SECRET", value: match.joinSecret, is_hidden: true },
          ],
          tags: [matchTag, ALLOCATOR_TAG, match.mode],    // ALLOCATOR_TAG scopes reconciliation
          webhook_on_ready: { url: `${PUBLIC_URL}/edgegap/ready/${match.webhookToken}` },
          webhook_on_error: { url: `${PUBLIC_URL}/edgegap/error/${match.webhookToken}` },
          webhook_on_terminated: { url: `${PUBLIC_URL}/edgegap/terminated/${match.webhookToken}` },
        }),
      });
    } catch {                                             // timeout: outcome unknown
      await sleep(500 * 2 ** attempt); continue;          // next loop looks up the tag first
    }
    if (res.status === 202) {
      const { request_id } = await res.json();
      await db.saveRequestId(match.id, request_id);
      return request_id;                                  // address arrives via webhook
    }
    if (res.status === 422 || res.status === 429 || res.status >= 500) {
      await sleep(500 * 2 ** attempt); continue;
    }
    throw new Error(`deploy failed ${res.status}: ${await res.text()}`);
  }
  throw new NoCapacityError(match.id);
}

// Webhook handler: answer fast, then deliver the address.
app.post("/edgegap/ready/:token", async (req, res) => {
  res.sendStatus(200);
  const d = req.body;                                     // request_id, fqdn, public_ip, ports, ...
  const match = await db.matchForWebhook(req.params.token, d.request_id);
  if (!match) return;
  const port = d.ports.gameport.external;
  await notifyPlayers(match, { host: d.fqdn, ip: d.public_ip, port });
});
```

## Integrations: check before hand-rolling

| Backend | How it meets Edgegap | Guide |
|---|---|---|
| Edgegap Matchmaker | Hosted; deploys and hands out addresses itself, no backend code | https://docs.edgegap.com/learn/matchmaking |
| Nakama (Heroic Labs) | The Edgegap Fleet Manager for Nakama (Go plugin) deploys from Nakama's matchmaker: use `edgegap-nakama` | https://github.com/edgegap/backend-nakama-edgegap-plugin |
| Unity Matchmaker (UGS) | Keep Unity's matchmaker; Unity's `EdgegapAllocator` Cloud Code module calls the Deploy API (skill `edgegap-ugs-matchmaker`) | https://docs.edgegap.com/docs/tools-and-integrations/deploy-from-ugs |
| PlayFab | Keep PlayFab matchmaking; two Azure Functions (rule on `match_found`, ready webhook) deploy near the players and hand out the address: use `edgegap-playfab` | https://github.com/edgegap/backend-game-sample-unity-playfab-matchmaker-fishnet-spaceedge |
| EOS lobbies (Unreal) | Lobby members store their IP; a backend service deploys for the lobby | https://docs.edgegap.com/docs/tools-and-integrations/unreal-eos-lobby-integration |
| Migrating from Multiplay, GameLift, Hathora | Concept mapping and migration steps | https://docs.edgegap.com/docs/tools-and-integrations |

Whichever row applies, the Edgegap token stays on the server side.
