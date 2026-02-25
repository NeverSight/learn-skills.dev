---
name: oasis-server-setup
description: Expert guide for integrating Oasis update server with Tauri apps for auto-updates, crash reporting, and feedback collection.
---

# Oasis Server Setup — Development Guide

You are an expert on the Oasis update server. Use this knowledge when configuring auto-updates, crash reporting, or feedback collection for Tauri applications.

## What It Is

Oasis is a self-hosted release management and analytics server for Tauri applications. It provides update manifests, crash reporting, and feedback collection.

**Server repo**: https://github.com/porkytheblack/oasis
**Reusable workflow**: `porkytheblack/oasis/.github/workflows/tauri-release.yml@main`

## Architecture at a Glance

```
┌─────────────────────────────────────────────────────────────────┐
│                      Tauri Desktop App                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ Auto-Update │  │ Crash SDK   │  │ Feedback SDK            │  │
│  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘  │
└─────────┼────────────────┼─────────────────────┼────────────────┘
          │                │                     │
          ▼                ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Oasis Server                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ /update     │  │ /crashes    │  │ /feedback               │  │
│  │ manifests   │  │ collection  │  │ collection              │  │
│  └──────┬──────┘  └─────────────┘  └─────────────────────────┘  │
└─────────┼───────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Cloudflare R2 (CDN)                           │
│         Artifact storage: .dmg, .exe, .AppImage                  │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Generate signing keys

```bash
npx @tauri-apps/cli signer generate -w ~/.tauri/keys/your-app.key
# Output: Public key + private key file
```

### 2. Configure tauri.conf.json

```json
{
  "plugins": {
    "updater": {
      "pubkey": "dW50cnVzdGVkIGNvbW1lbnQ6...",
      "endpoints": [
        "https://oasis.yourdomain.com/your-app/update/{{target}}-{{arch}}/{{current_version}}"
      ],
      "windows": {
        "installMode": "passive"
      }
    }
  }
}
```

### 3. Add updater capabilities

```json
// capabilities/default.json
{
  "permissions": [
    "updater:default",
    "updater:allow-check",
    "updater:allow-download-and-install",
    "process:default",
    "process:allow-restart"
  ]
}
```

### 4. Install Oasis SDK

```bash
pnpm add @oasis/sdk
```

### 5. Initialize SDK

```typescript
// lib/oasis.ts
import { initOasis } from '@oasis/sdk';

export const oasis = initOasis({
  apiKey: process.env.NEXT_PUBLIC_OASIS_API_KEY!,
  serverUrl: process.env.NEXT_PUBLIC_OASIS_SERVER_URL!,
  appVersion: '0.1.0',
  enableAutoCrashReporting: true,
});
```

### 6. Check for updates

```typescript
import { check } from '@tauri-apps/plugin-updater';
import { relaunch } from '@tauri-apps/plugin-process';

async function checkForUpdates() {
  const update = await check();
  if (update?.available) {
    await update.downloadAndInstall();
    await relaunch();
  }
}
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/{app_slug}/update/{target}-{arch}/{version}` | GET | Update manifest |
| `/sdk/{app_slug}/feedback` | POST | Submit feedback |
| `/sdk/{app_slug}/crashes` | POST | Report crashes |
| `/api/releases/{app_slug}` | POST | Register release (CI only) |

## Update Manifest Response

```json
{
  "version": "0.2.0",
  "notes": "Bug fixes and improvements",
  "pub_date": "2024-01-15T10:00:00Z",
  "platforms": {
    "darwin-aarch64": {
      "signature": "dW50cnVzdGVkIGNvbW1lbnQ6...",
      "url": "https://cdn.example.com/app/v0.2.0/App_aarch64.app.tar.gz"
    },
    "darwin-x86_64": {
      "signature": "...",
      "url": "https://cdn.example.com/app/v0.2.0/App_x64.app.tar.gz"
    },
    "windows-x86_64": {
      "signature": "...",
      "url": "https://cdn.example.com/app/v0.2.0/App_x64-setup.nsis.zip"
    },
    "linux-x86_64": {
      "signature": "...",
      "url": "https://cdn.example.com/app/v0.2.0/App_amd64.AppImage.tar.gz"
    }
  }
}
```

No update available returns `HTTP 204 No Content`.

## Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{{target}}` | Operating system | `darwin`, `windows`, `linux` |
| `{{arch}}` | CPU architecture | `x86_64`, `aarch64` |
| `{{current_version}}` | App version | `0.1.0` |

## API Keys

| Key Type | Format | Purpose |
|----------|--------|---------|
| Public Key | `pk_{app-slug}_{random}` | SDK operations (client-side) |
| CI Key | `ci_{app-slug}_{random}` | Release registration (server-side) |

Example: `pk_coco_a1b2c3d4e5f6g7h8`

## SDK Usage Patterns

### Feedback Submission

```typescript
// Categorized feedback
await oasis.feedback.submit({
  category: 'bug',        // 'bug' | 'feature' | 'general'
  message: 'Save button not working',
  email: 'user@example.com',
  metadata: { screen: 'settings' },
});

// Convenience methods
await oasis.feedback.reportBug('Description');
await oasis.feedback.requestFeature('Description');
await oasis.feedback.sendFeedback('Description');
```

### Crash Reporting

```typescript
// Manual capture
try {
  riskyOperation();
} catch (error) {
  await oasis.crashes.captureException(error, {
    appState: { screen: 'checkout' },
    severity: 'error',  // 'warning' | 'error' | 'fatal'
  });
}

// Toggle auto-capture
oasis.crashes.enableAutoCrashReporting();
oasis.crashes.disableAutoCrashReporting();
```

### Breadcrumbs

```typescript
oasis.breadcrumbs.addNavigation('/home', '/settings');
oasis.breadcrumbs.addClick('Save Button');
oasis.breadcrumbs.addHttp('POST', '/api/save', 200);
oasis.breadcrumbs.addCustom('wallet', 'Connected', { address: '0x...' });
```

### User Context

```typescript
// Set after authentication
oasis.setUser({
  id: 'user-123',
  email: 'user@example.com',
  username: 'johndoe',
});

// Clear on logout
oasis.setUser(null);
```

## SDK Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `apiKey` | `string` | required | Public API key |
| `serverUrl` | `string` | required | Oasis server URL |
| `appVersion` | `string` | required | Current app version |
| `enableAutoCrashReporting` | `boolean` | `false` | Catch uncaught errors |
| `maxBreadcrumbs` | `number` | `50` | Breadcrumb history limit |
| `timeout` | `number` | `10000` | Request timeout (ms) |
| `debug` | `boolean` | `false` | Enable debug logging |
| `beforeSend` | `function` | - | Filter/modify events |
| `onError` | `function` | - | Error callback |

## Required Secrets

| Secret | Description |
|--------|-------------|
| `OASIS_SERVER_URL` | Base URL (e.g., `https://oasis.yourdomain.com`) |
| `OASIS_CI_KEY` | CI key for release registration |
| `NEXT_PUBLIC_OASIS_API_KEY` | Public SDK key (exposed to client) |
| `NEXT_PUBLIC_OASIS_SERVER_URL` | Public server URL (exposed to client) |
| `TAURI_SIGNING_PRIVATE_KEY` | Update signing key |
| `TAURI_SIGNING_PRIVATE_KEY_PASSWORD` | Signing key password |

## Common Gotchas

1. **Public key in tauri.conf.json must match private key** — If you regenerate keys, update both the config and the GitHub secret.
2. **Endpoint URL uses double braces** — `{{target}}` not `{target}`. Single braces are for workflow variables.
3. **App slug must be consistent** — Use the same slug in workflow config, SDK init, and server registration.
4. **NEXT_PUBLIC_ prefix exposes to client** — Oasis public keys are safe to expose; CI keys are not.
5. **Version string must match semver** — Use `0.1.0`, not `v0.1.0` in code. Tags use `v` prefix.
6. **SDK init before crash reporting** — Call `initOasis()` early in app lifecycle to catch startup crashes.
7. **HTTP 204 means no update** — Don't treat this as an error; it's the expected response when current.
8. **Signature verification happens client-side** — Tauri verifies signatures using the embedded pubkey.
9. **R2 URLs must be publicly accessible** — The CDN URL in manifests must be reachable without auth.
10. **beforeSend can drop events** — Return `null` to filter sensitive data from crash reports.
