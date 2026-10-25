---
name: cx-rum-setup
description: >
  Use this skill when the user asks to "add RUM", "set up RUM", "install the RUM SDK",
  "add Coralogix RUM to my app", "create a RUM API key", "RUM public key",
  "init Coralogix RUM", "CoralogixRum.init", "add the browser SDK", "real user monitoring",
  "frontend monitoring", "monitor my web app", "session replay", "track frontend errors",
  "add RUM to React", "add RUM to Next.js", "add RUM to my mobile app",
  or wants to instrument a browser or mobile application with Coralogix Real User Monitoring
  end to end - RUM API key, SDK install, init code, and verifying data arrives.
metadata:
  version: "0.1.0"
---

# RUM Setup Skill

Use this skill to onboard an application to Coralogix Real User Monitoring (RUM): get a RUM API key, install the platform SDK, add the `init` call, and verify events land in the `rum.events` dataset.

---

## CLI Commands

| Command | Purpose |
|---|---|
| `cx iam api-keys list -o json` | List candidate keys and the team ID (no permissions in output) |
| `cx iam api-keys send-data-keys -o json` | List candidate send-data keys (no permissions in output) |
| `cx iam api-keys get <id> -o json` | Read a key's permissions (`keyInfo.keyPermissions`) and value |
| `cx iam api-keys create --from-file <file>` | Create the RUM key (write - needs approval + `--yes`) |
| `cx docs search <query>` / `cx docs fetch <suffix>` | Current SDK install and init docs per platform |
| `cx dataprime query --source rum.events '<query>'` | Verify RUM events arrive |
| `cx profiles list` | Profiles and regions - pick the active one for both key and `coralogixDomain` |

`cx iam` and `cx dataprime` take `-p <profile>` to target a specific team. `cx profiles` and `cx docs` are local commands - they take no `-p` (`cx profiles list -p ...` is an error).

---

## Workflow

### 1. Detect the platform

Inspect the user's repo before anything else. Signals overlap (React Native apps also list `react`; Flutter and React Native repos contain `ios/` and `android/` folders), so check **in this order and stop at the first match**:

| # | Signal | Platform |
|---|---|---|
| 1 | `pubspec.yaml` | Flutter SDK - ignore its `ios/` / `android/` folders |
| 2 | `package.json` with `react-native` (or `expo`) | React Native SDK - ignore `react` and native folders |
| 3 | `package.json` with `next` | Next.js (browser SDK, client-only init) |
| 4 | `package.json` with a browser signal - `react-dom`, `vue`, `@angular/core`, `svelte`, a browser bundler (`vite`, `webpack`, `parcel`), or an `index.html` entry | Browser SDK (`@coralogix/browser`) |
| 5 | `Podfile` / `Package.swift` / `*.xcodeproj` | iOS SDK |
| 6 | `build.gradle(.kts)` with Android plugin | Android SDK |

A `package.json` alone (Node backend, tooling) is **not** a browser app. If nothing matches, tell the user no supported client app was found instead of guessing.

### 2. Pick the profile - before any key operation

The key and the SDK domain must come from **one profile**, so settle it before touching keys. The active profile is `-p <name>` if given, else `$CX_PROFILE` if set, else the `DEFAULT` row of `cx profiles list` - don't just read the `DEFAULT` row. If there are several profiles and none was named, **ask the user which team the app belongs to now**, then pass `-p <name>` to every `cx iam` and `cx dataprime` call that follows.

`coralogixDomain` is that profile's `REGION` in upper case: `EU1`, `EU2`, `US1`, `US2`, `US3`, `AP1`, `AP2`, `AP3`.

### 3. Get a RUM API key

RUM keys are **public by design** - they ship inside client code. Create it with the **`SendRUMData` preset** - the same key the UI's RUM flow creates. That preset grants exactly one permission, `rum-ingress:SendData`, and is standalone: never add other presets or permissions. (Granting `rum-ingress:SendData` directly also works but shows as a `CUSTOM` key in the UI, so prefer the preset.) In Settings → API Keys a RUM key shows type "Send Your Data" with preset `SendRUMData`. Do **not** pick the `SendData` preset - it grants logs/metrics/spans ingest but not RUM, and makes the key secret, not public.

**Reuse first.** Check for an existing RUM key:

```bash
cx iam api-keys list -p <profile> -o json
cx iam api-keys send-data-keys -p <profile> -o json
```

These listings don't include permissions, so treat every row as a **candidate only** - never reuse a key based on its name. For each candidate run `cx iam api-keys get <id> -p <profile> -o json` and reuse it only if it is **active** (`keyInfo.active: true`) **and** `keyInfo.keyPermissions` has `SendRUMData` as its only preset and no other permissions (or `rum-ingress:SendData` as its only permission). Skip inactive keys - the SDK can't send with them. The value is in `keyInfo.value` (returned for unhashed keys - a hashed key can't be reused, create a new one).

**Create one if none exists.** This is a write - describe it to the user and get approval before passing `--yes` (same rules as `cx-platform-admin`).

```bash
cat > rum-key.json <<'EOF'
{
  "name": "<app-name> RUM",
  "owner": { "teamId": <team-id> },
  "keyPermissions": { "presets": ["SendRUMData"], "permissions": [] },
  "hashed": false
}
EOF
cx iam api-keys create --from-file rum-key.json -p <profile> --yes -o json
```

- `teamId`: read `cached_team_id` from the step-2 profile's file `~/.cx/profiles/<profile>.toml` (written by `cx init`), or the `owner.teamId` of any key in `cx iam api-keys list -o json`, or ask the user.
- `Permission denied`: RUM keys are Send-Your-Data (data-ingest) keys, so they need the `DATA-INGEST-API-KEYS` permissions, not the team custom-key ones:
  - on `send-data-keys` → the role lacks `DATA-INGEST-API-KEYS:READCONFIG` (view keys);
  - on `get` or `create` → the role lacks `DATA-INGEST-API-KEYS:MANAGE` (`get` needs it too, since it returns the key value).

  Don't retry with other payloads. Tell the user which permission is missing and ask them to get it, or to create it in **Settings → API Keys** - key type **Send Your Data Key**, role preset **`SendRUMData`** only (or have an admin do it), then continue from step 4 with the key value.
- `hashed: false` keeps the key value retrievable later - fine for a public RUM key.
- The response contains `value` - that is the `public_key` for the SDK.

### 4. Fetch the current SDK docs

SDK package names, versions, and options change - fetch them instead of guessing (see `coralogix-docs`):

```bash
cx docs search "RUM SDK installation <platform>" --limit 5
cx docs fetch <suffix-from-search>
```

### 5. Install and initialize

Use the profile and `coralogixDomain` from step 2.

Browser example (confirm against the fetched docs):

```bash
npm install @coralogix/browser
```

```ts
import { CoralogixRum } from '@coralogix/browser';

CoralogixRum.init({
  application: '<app-name>',
  environment: 'production',
  public_key: process.env.NEXT_PUBLIC_CX_RUM_KEY!, // or import.meta.env.VITE_CX_RUM_KEY
  coralogixDomain: 'EU1',
  version: '<app-version>',
});
```

Gotchas:

- **Init once, as early as possible** - the app entry point (`main.ts`, `index.tsx`, root layout).
- **Next.js:** init only on the client - a `'use client'` component that calls `init` in `useEffect`, rendered from the root layout. Never in server components.
- **Env vars:** keep the key in env config (`NEXT_PUBLIC_*`, `VITE_*`, `REACT_APP_*`), not hard-coded. It is public, but env config makes rotation easy.
- **`version`** should match the release - source maps and release comparison rely on it.
- **Source maps** (optional) are uploaded with `coralogix-rum-cli` and need a *separate* key - in the UI, key type **Team Key** with role preset **`SourceMapping`** (`source-mapping:ReadMapping` + `UploadMapping`) - never reuse the RUM key, and keep this one secret (CI only, not in client code). See `cx docs fetch user-guides/rum/cli/rum-cli.md` (search doesn't surface it).

### 6. Verify data arrives (optional)

Setup is done once the key exists and `init` is in place - data only flows after the app runs and users hit it, and the SDK sends in batches. Give the user this query to run later, or run it now if they load the app:

```bash
cx dataprime query --source rum.events \
  "filter \$d.version_metadata.app_name == '<app-name>' | limit 10" -p <profile> -o json
```

No rows? Check the browser network tab for requests to the RUM ingress endpoint. Ad blockers, a wrong `coralogixDomain`, or a key with extra permissions are the usual causes.

---

## Key Principles

- **RUM key = `SendRUMData` preset only** - nothing else on the key
- **Reuse before create**, and never pass `--yes` without user approval
- **Fetch SDK docs per platform** with `cx docs` - don't hard-code versions or options from memory
- **Client-side init only**, once, at the app entry point
- **Done = key + init in place** - hand over the `rum.events` query for checking data later

---

## Related Skills

- **`cx-platform-admin`** - general API key management
- **`coralogix-docs`** - fetch platform-specific SDK docs
- **`cx-telemetry-querying`** - query RUM data once it flows
