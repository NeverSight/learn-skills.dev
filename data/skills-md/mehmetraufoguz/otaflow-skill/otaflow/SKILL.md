---
name: otaflow
description: Publish, promote, roll back and pause over-the-air (OTA) updates for an Expo app with Otaflow and its `otaflow` command line. Use when the user wants to ship a JavaScript update to installed Expo apps without a store release, set up Otaflow for a project (login, link an app, create the code-signing key, configure expo-updates, channels and runtime versions), publish to preview or production, approve or request a promotion, undo a bad update, pause a channel, create CI keys, or debug an Otaflow error or an update that does not reach devices.
license: MIT
---

# Otaflow

Otaflow is an update server for Expo apps (the Expo Updates protocol) with a dashboard at https://otaflow.com and a command line, `otaflow` (npm package `otaflow`, Node.js 22 or newer). An update is signed **on the developer's machine or in their CI** with a code-signing key that Otaflow never sees. Two channels exist: `preview` (every publish lands here first) and `production` (what users get).

Read as needed:
- `references/setup.md`: project and build setup (`app.json`, channels, runtime versions, environment values). **Most "update does not arrive" problems are here.**
- `references/commands.md`: every command and flag (`otaflow <command> --help` shows the same flags for your installed version).
- `references/concepts.md`: how it works, roles, rollbacks, safety properties.
- `references/ci.md`: CI keys and a GitHub Actions example.
- `references/troubleshooting.md`: error messages and fixes, and why a device did not update.

## What it can and cannot do

- Ships **JavaScript and assets** only. Anything native (a new native package, an Expo SDK upgrade, config plugins, icons, entitlements) needs a new binary: the update targets a runtime version, and a native change makes a new one.
- Updates run in **release builds** of the app. Expo Go and debug / development-client builds do not apply them.
- **iOS** is the tested platform (`--platform ios`, the default). `--platform android` publishes and is served the same way, but it has not been run on an Android device yet: say so rather than promising it works.
- Devices download an update at launch and run it on the launch **after** that. There is no instant push.

## When helping someone

1. **Find out the situation first.** Run `otaflow whoami`; look for `.otaflow/project.json` (the folder is linked to an app) and `certs/certificate.pem`; check `expo-updates` is in `package.json`; check `app.json` has an `updates` block. Don't assume.
2. **Never touch the private signing key.** Do not print it, read it into the conversation, copy it into the project, commit it, or put it in an environment file. The certificate (`certs/certificate.pem`) is public and is committed; the private key lives in the user's config folder (or `OTAFLOW_SIGNING_KEY` / `OTAFLOW_SIGNING_KEY_PATH` in CI secrets).
3. **Ask before anything that reaches users or changes access:** promoting to production, publishing straight to `production`, any `rollback`, `pause` / `resume`, `keys revoke`, `apikey create` / `delete`, `storage connect` / `disconnect`, and `members role` / `access` / `remove` / `invite`. Say what it will do and to which channel. Publishing to `preview` is safe to run.
4. **Verify with commands, don't guess.** `otaflow list` shows each channel, its head update and recent updates. Read what it prints; do not assume a publish or promotion landed.
5. **Prefer `--json`** when you need to parse output; every command supports it.
6. **Do not work around a refusal.** If the CLI refuses (dirty git tree, a value from `.env` in the bundle, a role that may not do something), explain why and fix the cause. Never pass `--new-runtime` just to get past an error; see `references/troubleshooting.md`.
7. **Do not print secrets.** `apikey create` prints the key once on stdout: capture it straight into a secret store or a variable, and never echo it back or paste it into a file in the repository.

## Quick map: what the user asks, what to do

| The user wants to... | Do |
|---|---|
| Start using Otaflow on a project | Install and sign in, create the app, `init`, `keys init`, configure `app.json`, make a release build (below, and `references/setup.md`). |
| Ship a JavaScript fix | Commit, `otaflow publish -m "..."`, check `otaflow list`, test on a preview build, then `otaflow promote`. |
| Ship but they are not the owner | `otaflow promote` creates a request; the owner or manager approves. |
| Undo the latest update | `otaflow rollback --channel production --previous`. |
| Stop an update spreading right now | `otaflow pause --channel production`. |
| Wire it into CI | `references/ci.md`. |
| Check a project's setup | `otaflow doctor`: it checks login, key, certificate, `app.json` and runtime, and says what to fix. |
| Keep the updates in their own bucket | `otaflow storage connect`, **before the first publish** (`references/commands.md`, "Your own bucket"). |
| Add or manage people | `otaflow members list` / `invite` / `role` / `access` / `remove` (owner). |
| See what happened | `otaflow log` (owner and manager). |
| Find out why a device did not update | `references/troubleshooting.md`, section "On the device". |
| Ship something native | Not possible over the air: a new binary is needed. |

## Install and sign in

```bash
npx otaflow --help           # or: npm install --global otaflow
otaflow login                # prints a code and a link: the user opens it, checks the code, clicks Allow
otaflow whoami
```

## Set up a project (once)

```bash
otaflow apps create --name "My App" --slug my-app    # the account owner creates apps; the slug is permanent
cd <the Expo project folder>                          # in a monorepo: the app's own folder
otaflow init --app my-app                            # writes .otaflow/project.json
otaflow keys init                                    # makes the key, writes certs/certificate.pem, registers the public half
```

`keys init` keeps the private key **outside** the project and prints where (`~/.config/otaflow/keys/<appId>/main.key.pem`). Tell the user to back it up (a password manager): Otaflow cannot recover it, and without it no update reaches installed apps until a new binary ships.

Then `app.json` needs the update URL, the certificate and a runtime policy:

```json
{
  "expo": {
    "runtimeVersion": { "policy": "fingerprint" },
    "updates": {
      "url": "https://ota.otaflow.com/u/<slug>/manifest",
      "codeSigningCertificate": "./certs/certificate.pem",
      "codeSigningMetadata": { "keyid": "main", "alg": "rsa-v1_5-sha256" }
    }
  }
}
```

`codeSigningMetadata.keyid` must equal the key id used to sign (`--key-id`, default `main`). The binary also has to **ask for a channel**: add `"requestHeaders": { "expo-channel-name": "production" }` (or `preview`) under `updates` for the builds that should follow it. EAS Build only does this by itself for Expo's own update host, so with Otaflow you set it yourself. Details, per-profile channels and the runtime-version pitfalls are in `references/setup.md`.

Make a **release build** with this configuration once; updates reach that binary from then on. A binary built before these settings is not reached.

## Every day

```bash
git commit -am "Fix the checkout crash"                  # the project folder's git tree must be clean
EXPO_PUBLIC_API_URL=https://api.example.com otaflow publish -m "Fix the checkout crash"   # to preview
otaflow list                                             # check the head of preview
otaflow promote                                          # preview -> production
```

- `publish` exports **without reading `.env` files**: values the app needs at build time (`EXPO_PUBLIC_*`) must be in the environment of the `publish` command, or the update ships without them. See `references/setup.md`.
- `publish` refuses a dirty git tree (for the project folder), a commit that is already a channel's head, and a bundle that contains values from the project's `.env` files.
- Devices download an update at their **next launch** and run it on the one **after** that.
- `promote`: the account **owner** promotes directly. Anyone else (a member, or an API key) creates a request; the owner or the manager approves with `otaflow promotions approve --request <id>` or in the dashboard. `promote --wait` waits for the decision. The same signed bytes move to production: nothing is exported or signed again.

## When an update is wrong

| Situation | Do this |
|---|---|
| It must stop spreading now | `otaflow pause --channel production` (no key needed; installs keep what they run). `resume` when ready. |
| The latest update is broken | `otaflow rollback --channel production --previous` |
| Go back to the JavaScript inside the binary | `otaflow rollback --channel production --embedded` |
| Go back to a specific older update (owner) | `otaflow rollback --channel production --to <updateId>` |

A rollback is a **new** update carrying an older update's content, so devices move to it like any update (the same two-launch delay applies). The **manager** can only undo the latest update. Each publish signs, ahead of time, the rollbacks that could undo it, so a manager without the key can run `otaflow rollback --previous` (or use the dashboard's Undo button); `--prepared` forces that path. If the update changed data stored on the device (a local database migration), a rollback does not undo that data: publish a fix instead of rolling back.

## CI

Use a key scoped to one app and some actions, never a person's login. See `references/ci.md`.

```bash
otaflow apikey create --app my-app --name "GitHub Actions" --actions publish,request_promote   # shown once
```

A key can publish to preview and request a promotion; it can never approve one.
