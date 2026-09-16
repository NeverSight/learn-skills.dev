---
name: solana-mobile-publishing
description: Build, sign, and publish an Android APK to the Solana dApp Store with the dapp-store CLI. Use when shipping a Solana mobile app to the dApp Store for the first time, releasing an update, signing a release APK, setting up a publisher account and App NFT, or debugging a release build that works fine in debug.
---

# Publishing to the Solana dApp Store

Shipping to the dApp Store splits into a one-time setup that mints an on-chain App NFT, and a
per-release loop of build, sign, publish. The one-time half is where the irreversible decisions
live, so get it right before the first release rather than after.

```bash
npm install -g @solana-mobile/dapp-store-cli@latest
```

Node 18 or newer. `npx @solana-mobile/dapp-store-cli` works too if you would rather not install
globally.

**Use 1.0.1 or newer.** Earlier versions are deprecated and will not work.

## Non-negotiable constraints

**APK only. An `.aab` is rejected.** Build with `assembleRelease`, never `bundleRelease`. This
catches out anyone whose muscle memory comes from Google Play, where the bundle is the default.

**The keystore and the publisher wallet are both permanent.** An update has to be signed with
the same key as the release before it, and the App NFT lives in the publisher wallet. Lose
either and there is no recovery path and no support ticket that fixes it — the app can only be
re-listed from scratch under a new identity. Neither belongs inside the repository: ask where
the keystore should live before generating one, and keep it out of the project tree.

**If you also ship to Google Play, use a different signing key.** One key per store. Sharing one
means a compromise or loss takes out both listings at once.

## First: work out which situation you are in

| Situation | Do this |
| --- | --- |
| No publisher account yet | [One-time setup](#one-time-setup) |
| Publisher exists, shipping a release | [Build a signed APK](#build-a-signed-apk), then [Publish](#publish) |
| Shipping an update to a live app | [Shipping an update](#shipping-an-update) |
| Release build crashes but debug is fine | Read [references/signing.md](references/signing.md#release-only-failures) |
| A publish died partway through | [Resume a failed publish](#resume-a-failed-publish) |
| App is a wrapped web app, not React Native | [Web apps](#web-apps) |

## One-time setup

### The publisher keypair comes first

The CLI signs as the publisher with a keypair **file**, and connecting a wallet in the browser
portal does not produce one. Settle that file before registering anything, because the wallet
connected in the portal has to be the same key — arriving at it in the other order means
exporting a browser wallet's private key to disk, which is worse in every respect.

If a keypair already exists for this purpose, use its path, and ask which one rather than
reaching for whatever `~/.config/solana/id.json` happens to hold — that is usually a throwaway
dev key, and signing with the wrong one means the portal does not recognise the publisher.

If there is no keypair yet, **the developer generates it, not the agent**:

```bash
solana-keygen new --silent --outfile ~/.config/solana/publisher.json
```

`--silent` suppresses the seed phrase. Without it the twelve words go to stdout, and an agent's
stdout is a transcript and a log file — the whole wallet in plain text somewhere nobody is
guarding it. Drop `--silent` only in a terminal whose output is not being recorded, and back the
keypair file up either way: with the phrase suppressed, that file is the only copy. An agent
should only ever be handed the path.

Treat that file exactly like the release keystore: it is as permanent as the App NFT it
controls, so it belongs in a secrets store or a password manager, never in the repository. See
[references/signing.md](references/signing.md#create-the-keystore) for the same reasoning
applied to the Android key.

### Then register the publisher

Import that keypair into a wallet you control long-term and register at
https://publish.solanamobile.com with it. The portal creates the publisher, takes the dApp
listing details, and mints the App NFT.

Creating the listing is not the same step as minting the App NFT, and the CLI cannot do either
— it publishes *versions* of an app that already exists. A listing that has been filled in but
whose App NFT was never minted looks complete in the portal and fails at step 2 of the publish
with `App NFT and wallet authority must exist before publishing a version`. Confirm the listing
has both an App NFT and a wallet authority before the first release.

Fund the wallet before starting — the portal currently asks for roughly 0.2 SOL to cover
transaction fees and metadata storage. Treat that figure as indicative and read the number the
portal actually quotes, since it moves with rent and storage pricing. That is the registration
cost, and it is separate from the CLI's own preflight, which refuses to start a publish unless
the signer holds 0.016 SOL.

Then mint an API key at **Dashboard > Settings > API keys** and put it in the environment:

```bash
export DAPP_STORE_API_KEY='paste-the-portal-api-key'
```

`DAPP_STORE_API_KEY` is the variable the CLI reads by default. Typed at an interactive prompt,
that `export` also lands in the shell's history file, so prefer sourcing it from a secrets
manager over pasting it in. `--api-key-env <name>` points the CLI at a different variable, and
`--api-key-stdin` reads the key from stdin instead, which is the better choice in CI where the
environment is easier to dump than a pipe:

```text
printf '%s' "$DAPP_STORE_API_KEY" | dapp-store --api-key-stdin <publish flags>
```

That is only the key-passing shape — the full invocation is under [Publish](#publish), which
needs an APK you have not built yet at this point.

Two flags exist for pointing the CLI at a non-production portal: `--local-dev` allows a
localhost portal and skips the self-update gate, and `--skip-self-update` bypasses that gate on
its own — but only alongside `--local-dev`, so passing it by itself fails with
`` `--skip-self-update` is only allowed together with `--local-dev` ``. Local-dev mode rejects
any portal URL that is not local, so it is not the way to reach a hosted staging portal; use
`--portal-url` for that.

## Build a signed APK

Which command applies depends on who holds the keystore — the same split as
[references/signing.md](references/signing.md#which-signing-path-applies).

**EAS-managed credentials.** Build with the `dapp-store` profile, which forces an APK:

```bash
eas build --platform android --profile dapp-store
```

EAS signs it and hands back a download URL, so there is no `android/app/build/outputs/` path in
this flow. Either download the artifact and publish the local file, or pass the URL to
`--apk-url` and skip the download — but download it for an update, because `--apk-url` also
skips the signature check below.

**Local signing** — bare React Native, or Expo building locally:

```bash
(cd android && ./gradlew :app:assembleRelease)
```

The subshell matters: without it the `cd` persists, and the repository-root-relative paths in
every later command resolve under `android/` and fail.

The APK lands at `android/app/build/outputs/apk/release/app-release.apk`.

**Either way, confirm the APK is signed by the key you expect before uploading.** `$APK` here
and in [Publish](#publish) is whichever file the build produced — the Gradle output path above,
or the artifact downloaded from EAS.

```bash
"$ANDROID_HOME"/build-tools/<version>/apksigner verify --print-certs "$APK"
```

`apksigner` is not on `PATH` on a normal Android SDK install — a bare `apksigner` gets you
`command not found`. It lives under `$ANDROID_HOME/build-tools/<version>/`; pick the highest
version installed.

`apksigner verify` reads the APK and nothing else — no keystore, no private key — so it works on
a downloaded EAS artifact exactly as it does on a local build. On an update, compare the printed
SHA-256 fingerprint against the previous release's. That comparison is the only pre-upload way
to catch a build signed with the wrong keystore, and a wrong key on an update is the one failure
with no recovery path.

**Read the certificate name, not just the exit code.** A stock Expo prebuild wires the release
variant to the *debug* keystore, so an unconfigured release APK is signed — just with the wrong
key. `apksigner verify` passes it happily. If the printed DN is `CN=Android Debug`, the signing
config never took effect; see
[references/signing.md](references/signing.md#gradle-signing-config).

One more thing worth checking before upload: a default React Native release APK bundles every
ABI and runs to well over 100 MB. Building for one architecture
(`./gradlew :app:assembleRelease -PreactNativeArchitectures=arm64-v8a`) typically cuts that by
more than half.

Keystore creation, the Gradle signing config, the EAS build profile, and the failure modes that
only appear in release builds: [references/signing.md](references/signing.md).

## Publish

One command, for a first release and every release after it:

```bash
dapp-store \
  --apk-file "$APK" \
  --keypair ~/.config/solana/publisher.json \
  --whats-new "Initial release"
```

`$APK` is the file from the build step — the Gradle output path or the downloaded EAS artifact.
There is no default, and a bare `./app-release.apk` only works if you copied it there yourself.
An EAS build URL can go straight to `--apk-url https://…` instead, which publishes the hosted
APK without a local copy.

`--keypair <path>` selects the Solana signer. The CLI assumes no default keypair path, so pass
it explicitly; the path above is a placeholder for whichever keypair holds the publisher
identity. `--verbose` prints the release and session identifiers as they are emitted, which is
what you need if the run fails.

The portal drives the publication itself, so there is no RPC endpoint to configure for that.
`--rpc-url <url>` does exist but is hidden from `--help`, and it only feeds the preflight that
checks the signer's balance before submitting. The portal itself defaults to
`https://publish.solanamobile.com`; `--portal-url <url>` or `DAPP_STORE_PORTAL_URL` retargets
it, which you need only when Solana Mobile has given you a staging portal.

**Retargeting the portal means retargeting the RPC too.** That preflight reads mainnet whatever
`--portal-url` says, so a staging portal on devnet rejects a funded wallet before the publish
starts:

```text
Signer <address> has 0.000000 SOL, but publishing needs at least 0.016000 SOL available
```

The balance is real, just on another cluster. Pass `--portal-url` and `--rpc-url` together:

```bash
dapp-store \
  --apk-file "$APK" \
  --keypair ~/.config/solana/publisher.json \
  --whats-new "Initial release" \
  --portal-url https://staging.publish.solanamobile.com \
  --rpc-url https://api.devnet.solana.com
```

The CLI calls `dotenv.config()` at startup, so a `.env` in the working directory supplies both
that variable and the API key without saying so. Convenient in your own project, a hazard in one
you cloned: a `DAPP_STORE_PORTAL_URL` someone else committed sends your API key to their host,
and the only thing checked about it is that it is HTTPS. Read `.env` before publishing from a
repository you did not create, and pass `--portal-url` explicitly to override whatever it sets.

The portal infers which app it is updating from the APK's package name, so that name must match
the listing created during setup. A mismatch reads as a missing app rather than as a naming
error. The name comes from `expo.android.package` on Expo and `applicationId` in
`android/app/build.gradle` on a bare project — check whichever your project actually owns.

If you are scripting this, pass `--idempotency-key <key>` and **reuse the same value on every
retry of that release**. Omitting it is not a neutral default: the CLI generates a fresh
`randomUUID()` per invocation, so a retry looks like a new publish and can ship twice. Capture
the key alongside the release id before the first attempt.

### Resume a failed publish

A publish is a multi-step session. Whether a failure leaves anything to resume depends on where
it died: a failure during the minting steps is rolled back, and the CLI says so —
`Rolling back failed publication release` / `Failed publication release cleaned up`. After that
message there is no session left and a fresh publish is the right move. Reach for `resume` when
the run died without cleaning up, typically a network drop mid-session:

```bash
dapp-store resume \
  --release-id "$RELEASE_ID" \
  --keypair ~/.config/solana/publisher.json
```

`resume` validates `--keypair` the same way a publish does and fails with a
`--keypair is required` error without it. Pass **exactly one** of `--release-id` or
`--session-id` — supplying both is rejected outright, despite the usage line in `--help`
showing them together.

Both identifiers come from the output of the original run, which is the argument for `--verbose`
on anything non-interactive. Note what `--verbose` prints *when*: the release id and publication
session id are only emitted once APK ingestion succeeds. A run that dies during ingestion prints
only an **ingestion** session id, and that is a different identifier — `--session-id` wants the
publication session id and will not accept it. A failure that early has nothing to resume
anyway; fix the cause and publish again.

## Shipping an update

Same command as a first release. Three things have to be true or it fails or silently ships
nothing new:

- **Bump `versionCode`** — but in the file that actually owns it. On a bare project that is
  `android/app/build.gradle`. On Expo it is `expo.android.versionCode` in `app.json` or
  `app.config.*`, and editing `build.gradle` there is pointless because prebuild regenerates it.
  A freshly scaffolded Expo app often has neither `expo.version` nor `expo.android.versionCode`
  in `app.json` at all — Expo falls back to `1.0.0` and `1`. Add both keys before the first
  release rather than discovering they are missing when the second one needs to be higher.
  If `cli.appVersionSource` is `"remote"`, EAS owns `versionCode` outright: set `autoIncrement`
  on the build profile instead of editing any local file. Android orders releases by this
  integer, and it is what the store uses to decide what is newer.
- **Bump `versionName` too** — `expo.version` on Expo, `versionName` in `build.gradle` on a
  bare project. The CLI submits both as release metadata, and `versionName` is the string users
  see in the listing. Nothing rejects an unchanged one, so an update moving only `versionCode`
  ships silently showing the previous version.
- **Sign with the original keystore.** See the constraint above; there is no recovery.

## Review

Submissions go to human review, which takes a few business days — read the current figure from
the docs rather than planning a launch around a number quoted here. The common rejections
are an unsigned APK, a package name that does not match the listing, a missing privacy policy,
and content that falls outside the publisher policy. The policy is the authority on the last one
and it changes — read it rather than guessing.

## Web apps

A wrapped web app takes a different route: a web manifest, a Bubblewrap build, and Digital Asset
Links published at `/.well-known/assetlinks.json`. Only go there if the app genuinely is a PWA
being wrapped. A React Native app follows the native APK path above, and Bubblewrap will only
add a layer that breaks Mobile Wallet Adapter.

Full walkthrough: https://docs.solanamobile.com/recipes/general/publishing-a-web-app

## Reference material

- [references/signing.md](references/signing.md) — keystore creation, Gradle signing config,
  the EAS build profile, and release-only failures including the ProGuard footgun

## Related skills

- `solana-mobile` — scaffolding, toolchain checks, development builds
- `solana-mobile-wallet` — the wallet integration that has to survive the release build

## Links

- dApp Store docs: https://docs.solanamobile.com/dapp-store/intro
- Publishing CLI: https://docs.solanamobile.com/dapp-store/publishing-cli
- Building and signing an APK: https://docs.solanamobile.com/dapp-store/build-and-sign-an-apk
- Publisher policy: https://docs.solanamobile.com/dapp-store/publisher-policy
- Publishing portal: https://publish.solanamobile.com
- CLI and tooling source: https://github.com/solana-mobile/dapp-publishing
