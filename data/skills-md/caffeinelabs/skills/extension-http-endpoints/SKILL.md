---
name: extension-http-endpoints
description: >-
  Serve inbound HTTP from a Motoko canister (webhooks, curl POST/GET, bot
  callbacks, ingest/health APIs) via the IC HTTP Gateway methods
  `http_request` / `http_request_update`. Load whenever the user or spec needs
  a canister URL that external HTTP clients can hit — Stripe/GitHub/Slack
  webhooks, Telegram bots, health checks, or any plain REST-ish endpoint.
  NOT for calling external APIs from the canister (use
  `extension-http-outcalls`); NOT for certified static asset serving.
version: 0.2.1
compatibility:
  mops:
    caffeineai-http-endpoints: "~0.1.0"
    caffeineai-authorization: "~1.0.1"
caffeineai-subscription: [none]
---

# HTTP Endpoints (inbound)

Inbound HTTP for [Caffeine AI](https://caffeine.ai?utm_source=caffeine-skill&utm_medium=referral) Motoko backends via `mo:caffeineai-http-endpoints`.

## When to use which skill

| Need | Skill |
| --- | --- |
| External client (`curl`, webhook, bot) hits the canister over HTTPS | **this skill** |
| Canister calls an external HTTPS API | [`extension-http-outcalls`](../extension-http-outcalls/SKILL.md) |
| Typed OpenAI / Google / X / Stripe client | the matching domain skill (those wrap **outbound** calls) |

Do not implement inbound handlers with the management-canister `http_request` / `Call.httpRequest` outcall API — that is the opposite direction.

## How inbound HTTP works

1. Client hits the **backend** Motoko canister over HTTPS (not `*.caffeine.xyz`, custom domain, or frontend/asset canister).
2. The HTTP Gateway calls `http_request` (**query**).
3. Mutating routes return `Http.upgrade()` so the gateway re-issues as `http_request_update` (**update**).

**URLs**

- **Webhooks / POST:** `https://<backend-canister-id>.icp0.io/...` (or `.ic0.app`)
- **Uncertified GET (health / plaintext):** `https://<backend-canister-id>.raw.icp0.io/...` — non-raw gateways expect certified query bodies (out of scope)

# Backend

Use the prefabricated modules (do not modify them):

```mo:caffeineai-http-endpoints/Http
module {
  public type Request = { method : Text; url : Text; headers : [HeaderField]; body : Blob; certificate_version : ?Nat16 };
  public type Response = { status_code : Nat16; headers : [HeaderField]; body : Blob; streaming_strategy : ?StreamingStrategy; upgrade : ?Bool };

  public func path(url : Text) : Text;
  public func header(req : Request, name : Text) : ?Text; // case-insensitive
  public func text(status : Nat16, body : Text) : Response;
  public func upgrade() : Response; // query path asks gateway to call http_request_update
  public func notFound() : Response;
  public func methodNotAllowed() : Response;
  public func bodyText(req : Request) : ?Text; // null if body is not UTF-8; HMAC must use req.body
};
```

```mo:caffeineai-http-endpoints/MixinHttpEndpoints
mixin (
  onQuery : Http.Request -> Http.Response,
  onUpdate : Http.Request -> async Http.Response,
) {
  public query func http_request(req : Http.Request) : async Http.Response;
  public func http_request_update(req : Http.Request) : async Http.Response;
};
```

Add `mops add caffeineai-http-endpoints`. Wire handlers on the **existing** actor in `main.mo` — keep `MixinAuthorization`, do not replace the actor or redeclare `http_request*`.

`onQuery` must stay query-safe: no awaits, no state writes. Mutating work belongs in `onUpdate` after `Http.upgrade()` from the query path.

```motoko filepath=src/backend/main.mo
import Http "mo:caffeineai-http-endpoints/Http";
import MixinHttpEndpoints "mo:caffeineai-http-endpoints/MixinHttpEndpoints";
import AccessControl "mo:caffeineai-authorization/access-control";
import MixinAuthorization "mo:caffeineai-authorization/MixinAuthorization";

actor {
  let accessControlState : AccessControl.AccessControlState;
  include MixinAuthorization(accessControlState, null);

  func onHttpQuery(req : Http.Request) : Http.Response {
    let path = Http.path(req.url);
    if (req.method == "POST" and path == "/webhook") {
      return Http.upgrade();
    };
    if (req.method == "GET" and (path == "/" or path == "/health")) {
      return Http.text(200, "ok");
    };
    Http.notFound();
  };

  func onHttpUpdate(req : Http.Request) : async Http.Response {
    let path = Http.path(req.url);
    if (req.method == "POST" and path == "/webhook") {
      // Signature checks: Http.header(req, "stripe-signature"), HMAC over req.body
      ignore Http.bodyText(req);
      return Http.text(200, "received");
    };
    Http.notFound();
  };

  include MixinHttpEndpoints(onHttpQuery, onHttpUpdate);
};
```

The migration chain head:

```motoko filepath=src/backend/migrations/00000000_000000.mo
import AccessControl "mo:caffeineai-authorization/access-control";

module {
  type NewActor = {
    accessControlState : AccessControl.AccessControlState;
  };

  public func migration(_old : {}) : NewActor {
    { accessControlState = AccessControl.initState() };
  };
};
```

## Rules of thumb

- **Mutations only in `onUpdate`.** Query returns `Http.upgrade()` for POST/PUT/PATCH/DELETE routes that write.
- **Backend canister id only** for webhook URLs — project/frontend origins never reach Motoko `http_request`.
- **Uncertified GET → `.raw.icp0.io`.** Do not invent response certificates.
- **Prefer Candid + React** for app UI; use inbound HTTP only for external HTTP clients.
- **Auth:** no IC caller principal from webhook senders — verify signatures/secrets yourself (`Http.header`, raw `req.body`).
- **Large JSON:** keep payloads small/schema-simple, or store the blob and process elsewhere.

## How to `curl`

Uncertified GET on a non-raw host is a hard gateway failure (`503` / `backend_response_verification` / `Certification values not found`), not a 404 from your handler. POSTs that return `Http.upgrade()` skip that check.

```bash
# Reads — must be raw
curl https://<backend-canister-id>.raw.icp0.io/health

# Writes — non-raw is fine (update path)
curl -X POST https://<backend-canister-id>.icp0.io/webhook \
  -H 'content-type: application/json' \
  -H 'x-webhook-secret: …' \
  -d '{"event":"…"}'
```

`?canisterId=<id>` on `https://icp0.io/...` is an alternate host form. Prefer the canister subdomain. An IP/`localhost` GET with only `?canisterId=` can return an empty `204` instead of your body — treat that as the wrong URL shape, not an empty handler.

## Related

- [`extension-http-outcalls`](../extension-http-outcalls/SKILL.md) — canister → internet (module helpers, no inbound mixin)
- [`extension-stripe`](../extension-stripe/SKILL.md) — checkout via outcalls; inbound Stripe webhooks still use this skill
- [icskills#337](https://github.com/dfinity/icskills/issues/337) — upstream skill-gap discussion

## Local PocketIC (limitations)

PocketIC is useful for proving the upgrade dance, not as a drop-in `curl` replica.

- The `pocket-ic` binary is a **control server**. It does not listen for `curl` until a client (`@dfinity/pic`) creates an instance (include an NNS subnet) and calls `makeLive()`, which returns a **port**.
- There is no `mops` one-liner that prints a curl URL. The gateway dies with that Node/pic process.
- Once live, the same rules apply:
  - `http://<canister-id>.raw.localhost:<port>/health` — uncertified GET
  - `http://127.0.0.1:<port>/notes?canisterId=<id>` — POST / upgrade (worked in a live gateway test)
  - `http://<canister-id>.localhost:<port>/health` (no `.raw`) — `503` certification failure
- Do not document PocketIC as the way users hit production webhooks. Production URLs are the `*.icp0.io` / `*.raw.icp0.io` forms above.
