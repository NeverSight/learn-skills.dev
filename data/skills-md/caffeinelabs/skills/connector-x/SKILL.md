---
name: connector-x
description: >-
  MANDATORY recipe for every Caffeine build that posts to X (Twitter) from a
  canister. The supported path is the `x-client` mops package (X API v2) over
  outbound HTTPS, with per-user OAuth 2.0 (PKCE, no client secret). Hand-rolling
  `ic.http_request` calls to `api.x.com` is a FORBIDDEN anti-pattern — it
  bypasses bearer auth, the non-replicated-outcall safeguard, and the package's
  null-field JSON handling. Load this skill whenever the user, spec, or any prior
  task mentions posting a tweet, "tweet this", X/Twitter, sharing to X, or any
  equivalent phrasing — and BEFORE writing any code that touches an X endpoint.
version: 0.3.0
caffeineai-subscription: [none]
compatibility:
  mops:
    x-client: "~0.3.0"
---

# Posting to X with `x-client`

Motoko bindings for the [X API v2](https://developer.x.com/en/docs/x-api),
generated from X's OpenAPI spec. The write path is **`TweetsApi.createPosts`**
(`POST /2/tweets`); the request model is **`TweetCreateRequest`**.

# Backend

A minimal canister that posts a tweet on behalf of a user holding an OAuth 2.0
bearer token (token acquisition/refresh is canister-side — see below). Non-
replicated is the default, so you just supply the token; every optional field
must be present, and `null` means "not supplied":

```motoko filepath=src/backend/main.mo
import { createPosts } "mo:x-client/Apis/TweetsApi";
import { type TweetCreateRequest } "mo:x-client/Models/TweetCreateRequest";
import { defaultConfig } "mo:x-client/Config";

persistent actor {
  // Post a tweet on behalf of a user holding an OAuth 2.0 bearer token.
  public func postTweet(accessToken : Text, body : Text) : async () {
    let cfg = { defaultConfig with auth = ?#bearer accessToken };
    let req : TweetCreateRequest = {
      text_ = ?body;
      for_super_followers_only = null; poll = null; reply = null;
      reply_settings = null; media = null; geo = null; quote_tweet_id = null;
      nullcast = null; direct_message_deep_link = null; community_id = null;
      card_uri = null; edit_options = null; made_with_ai = null;
      paid_partnership = null; share_with_followers = null;
    };
    ignore await* createPosts(cfg, req);
  };
}
```

The text field is `text_ : ?Text` (the trailing underscore avoids the Motoko
keyword collision; it serialises to the JSON key `"text"`).

## OAuth 2.0 setup — PKCE, no client secret

Every write endpoint (`/2/tweets` most prominently) needs a **per-user OAuth 2.0
bearer token**. `x-client` is built for the **PKCE** flow, so there is **no
client secret** — only a public **Client ID**.

1. Visit the [X Developer Portal](https://developer.x.com/en/portal/dashboard),
   create a Project (Free tier = 1500 posts/month), and an **App**.
2. App → **Settings → User authentication settings → Edit**, toggle **OAuth 2.0**
   on. **Type of App**: `Web App, Automated App or Bot` (PKCE). Do **not** pick
   `Native App` or a "Confidential Client" — those force a client-secret flow this
   client does not emit.
3. **Callback URI**: your canister's HTTPS endpoint receiving `?code=…`, exact
   string match (e.g. `https://<canister-id>.ic0.app/oauth/x/callback`).
4. **Scopes** to request at authorise-time:

   | Scope | Why |
   |---|---|
   | `tweet.write` | **Required** for `createPosts` / posting |
   | `tweet.read` | Show "connected as @…" in the UI |
   | `users.read` | Resolve the authenticated user |
   | `offline.access` | Issue a **refresh token** (access tokens last ~2 h) |

5. Save; copy the **OAuth 2.0 Client ID** (a ~30-char public string). It is **not
   a secret** — safe to commit, log, or hard-code.

**Deployment models** — pick one or support both: a single **canister-wide**
Client ID set once by an admin (default), or **per-user** Client IDs for
multi-tenant apps that shouldn't share rate-limit quota.

Scopes are requested at authorise-time but silently absent from the issued token
if unticked — "Insufficient OAuth scope" on `createPosts` almost always means
`tweet.write` was missing.

## Calls are non-replicated by default

Every `x-client` call is an `http_request` on the IC. The package ships
`is_replicated = ?false` in `defaultConfig`: X is side-effecting (posting mutates
state) and its rate-limit headers / response timestamps vary per request, so a
*replicated* outcall — every subnet node issuing the request, the IC demanding a
bit-identical response, ~13× cycles — would post duplicates and fail consensus.
You don't set it yourself; the default is correct. Override with
`is_replicated = ?true` only if you specifically need consensus.

## Optional fields: leave them `null`

`x-client` strips null-valued optional fields from the outbound JSON (via the
`serde-core` `skip_null_fields` option), so `/2/tweets` sees only the fields you
set. Construct a `TweetCreateRequest` with `text_ = ?"…"` and every other field
`null` (as in the snippet above) and the body validates. Motoko requires all
record fields to be present at the value site — the `null`s are how you say "not
supplied".

## Sub-object rules for the non-null optionals

If you set `poll`, `reply`, `geo`, `media`, or `edit_options` to `?Some`, X
enforces that sub-object's own required fields — you cannot send an empty object,
so either leave the field `null` or populate it fully:

- `poll` — `options` (≥ 2) and `duration_minutes`.
- `reply` — `in_reply_to_tweet_id`.
- `media` — `media_ids` (must be pre-uploaded).
- `geo` — `place_id`.

## Token refresh

Access tokens expire (~2 h). Before each call the canister should refresh when
within a safety buffer of `expires_at`, POSTing `grant_type=refresh_token` to
`https://api.x.com/2/oauth2/token` with the stored `refresh_token` and Client ID.
**X rotates refresh tokens on every refresh** — store the *new* `access_token`
*and* `refresh_token`; reusing the old refresh token returns 400 and forces
re-authorisation. `x-client` has no knowledge of refresh — it's canister-side;
see the `posting-to-x` extension for the canonical code shape.

## Rate limits

Free tier: 1500 posts/month, 500 reads/month per app. Back off on HTTP 429 in
production; never silently retry a post (a retry may duplicate the tweet). X's
rate-limit headers come back in the response body but the package does not
interpret them.
