---
name: unity-ios-secure-backend
description: "Secure Unity iOS leaderboards with Apple Game Center identity verification and App Attest checked by a Node/NestJS backend. Use for GKLocalPlayer authentication, fetchItemsForIdentityVerificationSignature, publicKeyURL/signature/salt/timestamp verification, RSA-SHA256, DCAppAttestService attestation/assertions, credentialId/keyId, certificate nonce extraction, client/server request hashes, anti-cheat score submission, replay protection, Swift/ObjC++ bridges, Unity C# networking, or NestJS verification. Diagnose GKError 15/not recognized by Game Center, request_hash_mismatch, unknown_key, gc_auth_failed, and score-submit 401 responses."
---

# Unity iOS Secure Backend (Game Center identity + App Attest)

Make an online leaderboard for a Unity iOS game **un-spoofable**: the server only accepts a score if (a) it came from a real Apple ID (Game Center identity verification) and (b) it came from a genuine, unmodified build of *your* app on a real device (App Attest), and (c) the proof is bound to the exact bytes of *this* request. A Node/NestJS backend verifies all three. Gameplay must stay fully playable with **no** Game Center and **no** network — security is best-effort on top of a working local game, never a gate on play.

This skill is the hard-won residue of a long debugging session. Every claim below is grounded in shipped code; the byte-level crypto details live in `references/crypto-details.md`.

## Doctrine (these override convenience)

1. **The chain runs strictly in sequence, so an early failure masks every later bug.** Order on the server is: parse GC headers → verify GC identity (401 stops here) → compute request hash → App Attest attestation/assertion → persist score. Until GC passed, the App Attest code **never executed even once** — so three real App Attest bugs (OID length, SPKI-vs-raw-point keyId, fabricated root CA) sat latent and surfaced one at a time only as each prior gate opened. Expect this. Fix the first failing stage, redeploy, and the *next* latent bug appears. Do not assume "the rest works" because it compiled.
2. **Make every stage report its EXACT reason, end to end.** The server returns a typed machine code (`gc_auth_failed`, `request_hash_mismatch`, `unknown_key`, …) **plus** diagnostic detail in the message (e.g. the server-computed `clientDataHash`, whether the cert nonce was found, candidate count), and the client surfaces it on-device (a HUD line, the win card). An opaque "401" or "couldn't submit" is useless across a device round-trip you can't attach a debugger to. The client also logs `LastClientHash` (the base64 hash it signed) so you can diff it against the server's reported `cdh`.
3. **NEVER add a production bypass for App Attest.** No "if attest fails, submit anyway" path. If App Attest is unsupported/unavailable/failed, the client does NOT submit and shows a non-blocking message; the local leaderboard is untouched. A bypass is a cheat hole.
4. **Security never blocks gameplay.** Local-first: store the score locally, then fire-and-forget the remote POST. No GC / no network / declined sign-in → outcome is `NotSignedIn` / `AttestUnavailable` / `NetworkError`, all **non-errors** that the player never feels. In the Editor and non-iOS, every native call resolves to a clean "not available" so the game runs.
5. **Client and server must hash the EXACT same bytes.** The whole scheme collapses if the client signs bytes the server doesn't reproduce. Build the request body once, send *those* bytes, hash *those* bytes; on the server capture the raw body **before** JSON parsing and hash that. Never re-serialize a parsed DTO to hash it — key order/whitespace/unicode normalization will differ.

## The architecture (one POST, three proofs)

Client → `POST /api/scores/submit` with a JSON body and these headers:

- **Game Center identity** (proves a real Apple ID): `X-GC-Player-Id`, `X-GC-Player-Id-Alt` (comma-separated candidates), `X-GC-Public-Key-Url`, `X-GC-Signature`, `X-GC-Salt`, `X-GC-Timestamp`, `X-GC-Bundle-Id`.
- **App Attest** (proves genuine app + binds the request): `X-App-Attest-Key-Id` (always) + exactly ONE of `X-App-Attest-Attestation` (first use of a key) or `X-App-Attest-Assertion` (subsequent uses).
- Body: `{"submissionId","score","mode","difficulty","puzzleId","displayName"}` in a FIXED field order (it gets hashed).

Server pipeline (`scores.controller.ts` → `scores.service.ts`):
1. `gameCenter.verify(identity)` → throws 401 `gc_auth_failed` or returns a stable `userId`.
2. `computeClientDataHash('POST', '/api/scores/submit', rawBody)` from the **raw** captured bytes.
3. Attestation (registers a new key) or assertion (verifies an existing key) against that hash.
4. Only then persist the score (idempotent on `(userId, submissionId)`).

Read access (`GET /api/scores/top`) is **public** — no GC / no App Attest. Anyone reads the board; only writes are gated.

## Native layer (iOS) — the bridge shape

Three files under `Plugins/iOS/`: a Swift Game Center class, a Swift App Attest class, and an ObjC++ `.mm` shim. The pattern (use it for any Unity↔Swift async callback):

- Swift exposes `@_cdecl("__name")` C entry points. The `.mm` shim forward-declares those `extern "C"` symbols and wraps them in stable plugin-owned `Game*` functions — **do NOT `#import` the Unity-generated `-Swift.h`** umbrella (its name varies per build target and breaks the shim); resolve at link time instead.
- C# calls them via `[DllImport("__Internal")]`, guarded `#if UNITY_IOS && !UNITY_EDITOR`. The Editor/non-iOS branch returns "not available" so the game runs.
- Async results marshal back as `(int requestId, const char* jsonUtf8)` through one registered callback; C# keeps a `Dictionary<int, continuation>` and dispatches by `requestId`. The callback method needs `[AOT.MonoPInvokeCallback(typeof(NativeCallback))]` for IL2CPP. Strings from native `strdup` are freed on the C# side.

## Game Center identity — gotchas

1. **Architecture.** At launch install `GKLocalPlayer.local.authenticateHandler` (silent if signed in; iOS may present its own login UI, which the player may dismiss — never block). At submit time call `fetchItems(forIdentityVerificationSignature:)` → `(publicKeyURL, signature, salt, timestamp)`. The server downloads the cert from `publicKeyURL` (must be an https `apple.com` host), then verifies an **RSA-SHA256** signature over `playerId + bundleId + timestamp(big-endian uint64 MILLISECONDS) + salt`.

2. **"This application is not recognized by Game Center" (GKError 15 / "no game matching descriptor").** The bundle id is not registered with Apple's Game Center backend. The `com.apple.developer.game-center` **entitlement alone is NOT enough.** FIX: in **App Store Connect**, the app must have Game Center enabled — in the *new* GC experience, create at least one Game Center **component (a Leaderboard)** for the app version. That registration is what makes `fetchItems` stop returning "not recognized." You do **NOT** need to submit or get the leaderboard approved; merely creating the component registers the bundle id.

3. **Which player id is signed over is AMBIGUOUS, and `teamPlayerID` can be EMPTY on some devices.** This bit hard and in two ways:
   - `gamePlayerID`-only → the RSA signature 401s (Apple signed over a different id).
   - `teamPlayerID`-only → empty on some devices → identity looks "incomplete" → the client **silently skips the whole submission** (no POST at all). That silent skip is the nastiest symptom: nothing in the server logs.
   - **SOLUTION (both sides):** the client picks a guaranteed-non-empty **primary** (`teamPlayerID` → `gamePlayerID` → legacy `playerID`, first non-empty) so the identity is always "complete" and the submit proceeds, AND sends **all** non-empty candidate ids (`teamPlayerID`, `gamePlayerID`, legacy `playerID`) via `X-GC-Player-Id-Alt`. The server tries each candidate as the signed id until the RSA signature verifies, and derives the stable user id from **whichever verified**. Do not hard-code one id — what Apple signs varies across iOS versions.

4. **TestFlight uses the PRODUCTION Game Center environment** (not sandbox). Sign in with the normal Apple ID, not a sandbox tester. (This pairs with `APP_ATTEST_ENV=production` below — both must be production for TestFlight/App Store.)

5. **Replay protection at the GC layer:** reject stale timestamps (the verifier rejects anything older/newer than `GC_MAX_TIMESTAMP_AGE_SECONDS`, default 600). The timestamp is **milliseconds**; it is written big-endian uint64 into the signed payload — get the unit wrong and every signature fails.

## App Attest (server verification) — the latent bugs

These were ALL latent — none ran until Game Center passed (doctrine #1). They then surfaced in order:

6. **The Apple App Attest Root CA must be the REAL Apple cert.** A fabricated/placeholder PEM (wrong middle base64 lines) crashes startup with **"bad base64 decode"** the moment `new X509Certificate(...)` runs under `VERIFIER_MODE=real` — the server never binds a port and healthchecks fail. Get the genuine cert from `apple.com/certificateauthority` (Apple App Attestation Root CA). **Store it as an array of lines joined with `'\n'`, NOT a template literal** — a multi-line template literal can pick up CRLF / `\r` from git or the build, embedding `\r` in the base64 lines → same "bad base64 decode" crash. The array-join makes it immune to line-ending mangling.

7. **Cert nonce extraction — OID length off-by-one (the root cause of EVERY `request_hash_mismatch`).** The App Attest nonce lives in a cert extension under OID `1.2.840.113635.100.8.2`. That OID encodes to **9 content bytes**, so its DER is `06 09 2a 86 48 86 f7 63 64 08 02`. Searching for `06 0a …` (length **10**) never matches → the nonce comes back `null` → the computed `nonce != certNonce` for **every** request → every submission fails `request_hash_mismatch`. FIX: search for the OID **content** bytes only (`2a 86 48 86 f7 63 64 08 02`, prefix-independent so a wrong length byte can't break it), then scan forward for the `04 20` (OCTET STRING, 32 bytes) marker and take the next 32 bytes as the nonce.

8. **keyId / credentialId = SHA256 of the UNCOMPRESSED X9.63 EC point**, i.e. `0x04 || X || Y` (65 bytes for P-256) — the `SecKeyCopyExternalRepresentation` form, NOT the SPKI DER. Hashing the SPKI DER (`cert.publicKey.export({format:'der',type:'spki'})`) never matches `credentialId` → `invalid_attestation`. Rebuild the raw point from the JWK `x`/`y` (`Buffer.concat([0x04, x, y])`) and hash that. (You still keep the SPKI DER around — it's what you store to verify later assertions.)

9. **Request-hash agreement (the whole scheme hinges on this).** Capture the raw request body **before parsing** — body-parser's `verify` callback stashes `req.rawBody = Buffer.from(buf)`. Compute on **both** sides, identically:
   ```
   bodyHash       = SHA256(rawBodyBytes)
   clientDataHash = SHA256( UTF8("POST\n/api/scores/submit\n") + bodyHash )
   ```
   App Attest nonce = `SHA256(authData || clientDataHash)` must equal the cert/assertion nonce. The client passes `base64(clientDataHash)` down to `DCAppAttestService` as the `clientDataHash:` argument — the App Attest proof is computed **outside** the JSON body (no circular hashing). Method + path are part of the signed prefix; keep the route string in sync on both sides.

10. **Attestation → assertion lifecycle + stale-key recovery.** First submission per key = attestation (`generateKey()` → persist the keyId in UserDefaults → `attestKey()`); later ones = assertion (`generateAssertion()`). The client persists the keyId and uses `HasKey` to choose. **The trap:** if that first attestation never registers server-side — e.g. an earlier GC 401 stopped the request *before* App Attest ran — the client keeps sending **assertions for a key the server has never seen** → 400 `unknown_key`, forever. FIX: on a `unknown_key` (or "attestation required") response, the client **clears the persisted key and re-attests once** (`AppAttest.ClearKey()` → retry the submit with `retried=true`). This self-heals devices stuck from the GC-broken era.

11. **`APP_ATTEST_ENV` must be `production`** for TestFlight/App Store. The attestation's `aaguid` encodes development vs production (`"appattestdevelop"` vs `"appattest\0…"`); a mismatch against the expected environment is rejected (`invalid_attestation`). Pair with the production GC environment (#4). Also: `expectedAppId` = `"{APPLE_TEAM_ID}.{APP_BUNDLE_ID}"` and the attestation's `rpIdHash` must equal `SHA256(appId)`.

## Anti-cheat hardening already in place (don't regress these)

- **Strictly-increasing sign counter.** Each assertion carries a counter; the server updates it with a guarded `UPDATE … WHERE signCount < newCount`, so a replayed assertion (same counter) loses the race and is rejected `replayed_counter`. Two concurrent replays can't both win.
- **Key ownership.** A key is bound to the first user that registered it; an assertion/attestation under another user's id is rejected `key_registered_to_another_user`.
- **Idempotent writes.** Score insert is `ON CONFLICT DO NOTHING` on `(userId, submissionId)`; a duplicate returns the original row, `idempotent:true` — retries are safe.
- **Public read leaks no userId.** `GET /top` returns `{rank, name, score}` only; `name` falls back to `Player####` (last 4 of the user id) when there's no display name.

## Debugging methodology (the meta-lesson)

When a multi-stage verification chain "doesn't work":
1. **Find which stage actually fails** — the typed error code tells you (`gc_auth_failed` vs `request_hash_mismatch` vs `unknown_key`). Don't theorize; read the code the device got back.
2. **Fix that stage, redeploy, retest** — and expect the *next* latent stage to fail, because it was never exercised. Budget for several round-trips, not one fix.
3. **Diff the two hashes** when you hit `request_hash_mismatch`: the client's `LastClientHash` (base64 of what it signed) vs the server's logged `cdh`. Equal hashes but still a mismatch → the cert-nonce extraction is returning null (the `04 20`/OID bug), not a body disagreement. Unequal hashes → the bodies differ (re-serialization, an extra field, raw-body not captured).
4. **Surface diagnostics on-device.** You cannot attach a debugger to a TestFlight build mid-fetch; the win card / a HUD line carrying `LastIdentityError`, `LastClientHash`, and the server's reply is your only window.
5. **Never weaken security to "make it work."** No App Attest bypass, no skipping the signature check. Every fix above keeps the gate intact.

## Grounding files (read these to verify any claim)

Server (NestJS): `server/src/game-center/real-game-center.verifier.ts`, `server/src/app-attest/real-app-attest.verifier.ts`, `server/src/scores/scores.controller.ts`, `server/src/scores/scores.service.ts`, `server/src/raw-body.ts`, `server/src/common/request-hash.ts`, `server/src/common/errors.ts`.
Native iOS: `Assets/<YourGame>/Plugins/iOS/GameCenter.swift`, `AppAttest.swift`, `NetBridge.mm`.
Unity C#: `Assets/.../Scripts/Game/Net/GameCenter.cs`, `AppAttest.cs`, `RemoteScoreClient.cs`, `RemoteLeaderboard.cs`.

Byte-level crypto layouts (authData parsing, raw EC point, OID/nonce DER, signed payload) are in `references/crypto-details.md`.

## Field notes & lessons

- Initial skill. Captures the GC-identity + App Attest + NestJS verification chain and the nine debugged failures: not-recognized-by-GC registration, ambiguous/empty player id (try-all-candidates), real Apple root CA (array-joined PEM), OID 9-vs-10 byte nonce extraction, keyId = SHA256(uncompressed EC point) not SPKI, raw-body request-hash agreement, attestation→assertion lifecycle + unknown_key self-heal, production env for TestFlight, and the sequential-chain-masks-later-bugs methodology.
