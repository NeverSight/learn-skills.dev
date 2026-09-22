---
name: connector-spotify
description: >-
  MANDATORY recipe for every Caffeine build that reads Spotify catalog data or
  drives a user's Spotify account from a canister. The supported path is the
  `spotify-client` mops package (Spotify Web API) over outbound HTTPS with an
  OAuth 2.0 bearer token minted off-chain. Hand-rolling `ic.http_request` calls
  to `api.spotify.com` is a FORBIDDEN anti-pattern — it bypasses the
  non-replicated-outcall safeguard (player state and `progress_ms` differ per
  node and fail consensus), the generated JSON decoding, and the bearer
  handling. Load this skill whenever the user, spec, or any prior task mentions
  Spotify, a song, track, artist, album, playlist, music search, new releases,
  genres, markets, "what's playing", recently played, the queue, player controls
  (play / pause / skip / shuffle / repeat), a saved library, podcasts (shows or
  episodes), chapters or audiobooks — and BEFORE writing any code that touches a
  Spotify endpoint.
version: 0.3.0
caffeineai-subscription: [none]
compatibility:
  mops:
    spotify-client: "~0.3.0"
---

# Spotify with `spotify-client`

Motoko bindings for the
[Spotify Web API](https://developer.spotify.com/documentation/web-api),
generated from Spotify's official OpenAPI spec: **15 API modules, 270
operations**. The package is built in **icp-cli mode** (`mo:ic/Types` for the
management-canister interface), so it pulls `ic` as a dependency and pins
PocketIC in `[toolchain]`.

# Backend

Reading catalog data and driving the player. The token always comes from the
caller — the canister never holds a Spotify client secret:

```motoko filepath=src/backend/main.mo
import { getTrack } "mo:spotify-client/Apis/TracksApi";
import { getInformationAboutTheUsersCurrentPlayback; skipUsersPlaybackToNextTrack } "mo:spotify-client/Apis/PlayerApi";
import { type Config; defaultConfig } "mo:spotify-client/Config";

persistent actor {
  func config(accessToken : Text) : Config = { defaultConfig with auth = ?#bearer accessToken };

  // Catalog read — a client-credentials token suffices. `market = ""` omits the
  // parameter; empty strings and zeroes are how optional query params are
  // dropped, there is no `?Text` to leave null.
  public func trackName(accessToken : Text, id : Text) : async ?Text {
    let track = await* getTrack(config accessToken, id, "");
    track.name;
  };

  // User read — needs a user token with `user-read-playback-state`. An idle
  // player answers 204 with an empty body, which the generated decoder cannot
  // parse, so it rejects; treat that as "nothing playing", not as an error.
  public func nowPlaying(accessToken : Text) : async ?Bool {
    try {
      let state = await* getInformationAboutTheUsersCurrentPlayback(config accessToken, "", "");
      state.is_playing;
    } catch (_err) {
      null;
    };
  };

  // User write — needs `user-modify-playback-state`. Returns `()`, and since
  // 0.3.0 a non-2xx status rejects, so a missing scope or an expired token
  // surfaces here instead of looking like success.
  public func skip(accessToken : Text) : async () {
    await* skipUsersPlaybackToNextTrack(config accessToken, "");
  };
}
```

## Auth: the canister never sees a client secret

Every call needs an **OAuth 2.0 bearer access token**, minted off-chain and
passed in. Two flows matter:

1. **Client Credentials** — server-to-server, no user. Reads public catalog
   only: `search`, `getTrack`, `getAnAlbum`, `getAnArtist`, `getNewReleases`,
   `getCategories`, `getAvailableMarkets`, public playlists, public shows. It
   **cannot** touch any `/me/*` endpoint, the library, or the player.
2. **Authorization Code with PKCE** — user-facing. Required for every `/me/*`
   call, playlist mutation, library write and player command, each gated by its
   own scope (`user-read-playback-state`, `user-modify-playback-state`,
   `playlist-modify-public`, `user-library-read`, …). Scopes absent from the
   token surface as 403, not as a validation error.

Tokens expire after **one hour** and refresh is off-chain too. Treat a 401 as
"ask the client to refresh and retry", never as a permanent failure, and never
store a client secret in the canister.

## Calls are non-replicated by default

The package ships `is_replicated = ?false` in `defaultConfig`, and **91 of the
135 operations depend on it**. The generator already pins non-replication per
request for the 27 `PUT` and 17 `DELETE` operations, because the IC requires it
there — so playlist edits and library saves were never at risk. The default is
what covers the rest:

- the **7 `POST`s**, which include `addToQueue` and both skip endpoints. These
  are not idempotent, so replicated they would queue a track ~13 times and skip
  ~13 tracks;
- all **84 `GET`s**, which are non-deterministic for the player —
  currently-playing carries `timestamp` and `progress_ms`, differing per node —
  and would cost ~13x the cycles even where they agree.

You don't set the flag yourself; the default is correct. Override with
`is_replicated = ?true` only together with a `transform` that strips the
volatile fields.

**Upgrading from 0.2.x — the old advice was backwards.** That skill told callers
to keep `is_replicated = null` for mutations "because consensus matters", and
showed `let userCfg = { cfg with is_replicated = null }`. Carrying that forward
is now actively harmful: `null` means replicated, so every `addToQueue` and
skip would fire once per replica. Delete any such override and take
`defaultConfig` as it comes.

## Everything in a response is optional

Spotify marks almost no response field required, so the models are all-optional:
`TrackObject.name : ?Text`, `.artists : ?[SimplifiedArtistObject]`,
`CurrentlyPlayingContextObject.is_playing : ?Bool`. Reach through with a `do ?`
block rather than nested `switch`es, and decide what absence means for your
caller — Spotify omits fields your token's scopes don't cover.

## IDs, not URIs

Endpoint parameters take Spotify's base-62 **IDs**
(`11dFghVXANMlKmJXsNCbNl`), not URIs (`spotify:track:11dFghVXANMlKmJXsNCbNl`)
and not URLs. When a user pastes a Spotify link, extract the segment after the
last `/` and before any `?`. The `uris` parameters on playlist operations are
the exception — those do take full `spotify:track:…` URIs.

## Starting playback

`PlayerApi.startAUsersPlayback` takes the four fields as scalars —
`context_uri : ?Text`, `uris : ?[Text]`, `position_ms : ?Int` — and
`transferAUsersPlayback` takes `play : ?Bool`. Pick one of `uris` (explicit
tracks) or `context_uri` (an album, artist or playlist), never both.

`offset` is the exception: it is a free-form object in the spec, so the
generator maps it to `?Map<Text, Text>` and serialises **every value as a
string**. `{"uri": "spotify:track:…"}` therefore works, while Spotify's other
documented form `{"position": 5}` goes out as `{"position": "5"}` and is
rejected. Offset into a context by URI, not by index.

## One operation does not work

`PlaylistsApi.uploadCustomPlaylistCover` — the spec declares the body as
`image/jpeg` (`format: byte`), but the generator only ever emits JSON request
bodies, so the call sends `Content-Type: application/json` with the base64
wrapped in JSON quotes. Spotify rejects it. This is not new in 0.3.0: 0.2.2
JSON-wrapped the raw `Blob` instead, equally wrong on the wire. Do not offer
custom playlist cover upload, and do not hand-roll it with `ic.http_request`;
raise it on
[`caffeinelabs/skills-internal`](https://github.com/caffeinelabs/skills-internal).

Everything else in the surface is sound — unlike some connectors, there are no
stubbed `oneOf` converters, no operation silently dropping its request body, and
no endpoint returning a non-JSON body through the JSON decoder.

## The idle player rejects instead of returning "nothing playing"

`PlayerApi.getInformationAboutTheUsersCurrentPlayback` and
`getTheUsersCurrentlyPlayingTrack` answer **204 with an empty body** when
playback is not active. The generated code treats every 2xx as the 200 schema
and runs the JSON decoder over it, so an idle player produces
`Error.reject(… Failed to parse JSON …)` rather than an absent value. Wrap both
in `try`/`catch` and read a rejection as "nothing playing", as the §Backend
sample does.

This is a codegen gap, not a Spotify quirk: the spec declares
`'204': Playback not available or active` for the first operation (the generator
ignores no-content 2xx responses and has no `?T` return shape for them), while
for the second Spotify returns 204 in practice without declaring it at all.
Modelling declared no-content responses would change the generated signature to
`?CurrentlyPlayingContextObject`, so it belongs in the plugin as its own
change.

## Every write now reports its status

Until 0.3.0 the 43 operations returning `async* ()` — `skip`, `pause`,
`addToQueue`, every library and playlist mutation — discarded the HTTP response
entirely, so a 401, 403 or 429 was indistinguishable from success. They now
reject on any non-2xx status. Expect `try`/`catch` around writes to actually
fire: a missing scope surfaces as 403 where it previously looked like a
successful no-op.

## Cycles and response sizes

`defaultConfig.cycles = 30_000_000_000` suits a typical single-object read.
Large pages need more: `search` with `limit=50`, `getAnAlbum` on a long
tracklist, or `getAudioAnalysis` (which returns a very large object) want
`cycles = 100_000_000_000` and an explicit
`max_response_bytes = ?2_000_000`.

## Errors

Non-2xx responses and decode failures `throw Error.reject(…)`. The client is
generated with `diagnostics`, so the message is
`HTTP <status> body[<n>B]=<first 100 chars>: <reason>` — enough to separate a
401 (expired token) from a 403 (missing scope) from a 404 (bad ID) without extra
logging. Catch with `try`/`catch` and surface `Error.message(err)`.
