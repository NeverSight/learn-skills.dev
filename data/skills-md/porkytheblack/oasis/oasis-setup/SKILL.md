---
name: oasis-setup
description: Expert guide for integrating Oasis into Tauri applications. Use when working with oasis-sdk, auto-updates, crash reporting, user feedback, release workflows, or any Oasis-powered Tauri project.
---

# Oasis — Development Guide

You are an expert on the Oasis platform. Use this knowledge when integrating, debugging, or reviewing Oasis code in Tauri applications.

## What Oasis Is

Oasis is a self-hosted platform for managing Tauri application releases, collecting user feedback, and tracking crashes. Developers integrate the SDK into their Tauri app, configure the release workflow, and Oasis handles update distribution, crash collection, and feedback management.

**Repository**: https://github.com/porkytheblack/oasis
**License**: MIT

## Component Overview

| Component | Purpose | Location |
|-----------|---------|----------|
| `oasis-sdk` | Client SDK: feedback, crashes, breadcrumbs | `npm install oasis-sdk` |
| Server | Hono backend API for releases, crashes, feedback | `server/` |
| Dashboard | Next.js admin UI for managing apps | `dashboard/` |
| Release Workflow | Reusable GitHub Actions for Tauri builds | `.github/workflows/tauri-release.yml` |

## Architecture at a Glance

```
Tauri App + SDK → Oasis Server → Dashboard
       ↓                ↓
  Crash reports    Release management
  User feedback    Update distribution
  Breadcrumbs      Analytics
```

### API Key Types

| Type | Prefix | Use |
|------|--------|-----|
| Public | `pk_*` | SDK initialization (client-side) |
| CI | `uk_live_*` | GitHub Actions release registration |
| Admin | `uk_live_*` (admin scope) | Full dashboard access |

## Quick Start

### 1. Install SDK

```bash
npm install oasis-sdk
```

### 2. Initialize

```typescript
import { initOasis } from 'oasis-sdk';

const oasis = initOasis({
  apiKey: 'pk_my-app_xxxxxxxx',           // From Oasis dashboard
  serverUrl: 'https://updates.myapp.com', // Your Oasis server
  appVersion: '1.0.0',                    // Current app version
  enableAutoCrashReporting: true,         // Auto-capture uncaught errors
});
```

### 3. Collect Feedback

```typescript
await oasis.feedback.submit({
  category: 'bug',  // 'bug' | 'feature' | 'general'
  message: 'Description of the issue',
  email: 'user@example.com',
});

// Convenience methods
await oasis.feedback.reportBug('Bug description');
await oasis.feedback.requestFeature('Feature request');
```

### 4. Manual Crash Reporting

```typescript
try {
  riskyOperation();
} catch (error) {
  await oasis.crashes.captureException(error, {
    severity: 'error',  // 'warning' | 'error' | 'fatal'
    appState: { screen: 'checkout' },
  });
}
```

## SDK API Reference

### OasisConfig

```typescript
interface OasisConfig {
  apiKey: string;                         // Required: Public API key (pk_*)
  serverUrl: string;                      // Required: Oasis server URL
  appVersion: string;                     // Required: Current app version (semver)
  enableAutoCrashReporting?: boolean;     // Auto-capture errors (default: false)
  maxBreadcrumbs?: number;                // Max breadcrumbs (default: 50)
  timeout?: number;                       // Request timeout ms (default: 10000)
  debug?: boolean;                        // Enable debug logging (default: false)
  beforeSend?: (event) => event | null;   // Filter/modify events
  onError?: (error, event) => void;       // Called on send failure
}
```

### Feedback API

```typescript
await oasis.feedback.submit({ category, message, email?, metadata? });
await oasis.feedback.reportBug(message, email?);
await oasis.feedback.requestFeature(message, email?);
await oasis.feedback.sendFeedback(message, email?);
```

### Crash Reporting API

```typescript
await oasis.crashes.captureException(error, { severity?, appState?, tags? });
await oasis.crashes.report({ error, severity?, appState?, tags? });
oasis.crashes.enableAutoCrashReporting();
oasis.crashes.disableAutoCrashReporting();
```

### Breadcrumbs API

```typescript
oasis.breadcrumbs.add({ type, message, data? });
oasis.breadcrumbs.addNavigation(from, to);
oasis.breadcrumbs.addClick(target, data?);
oasis.breadcrumbs.addHttp(method, url, statusCode?);
oasis.breadcrumbs.addConsole(level, message);
oasis.breadcrumbs.addUserAction(action, data?);
oasis.breadcrumbs.getAll();
oasis.breadcrumbs.clear();
```

**Auto-collected:** Navigation, clicks, console messages, fetch requests.

### User Tracking

```typescript
oasis.setUser({ id, email?, username?, ...custom });
oasis.setUser(null);  // Clear user
```

### Utilities

```typescript
await oasis.flush();       // Flush event queue
oasis.getConfig();         // Get current config
oasis.destroy();           // Clean up resources
```

## Tauri Configuration

### Enable Auto-Updates

In `src-tauri/tauri.conf.json`:

```json
{
  "tauri": {
    "updater": {
      "active": true,
      "endpoints": [
        "https://YOUR_OASIS_SERVER/your-app-slug/update/{{target}}/{{current_version}}"
      ],
      "dialog": true,
      "pubkey": "YOUR_PUBLIC_KEY_HERE"
    }
  }
}
```

### Generate Signing Keys

```bash
npx @tauri-apps/cli signer generate -w ~/.tauri/myapp.key
```

- **Private key** → GitHub secret `TAURI_SIGNING_PRIVATE_KEY`
- **Public key** → `tauri.conf.json` under `updater.pubkey`

## GitHub Actions Workflow

Create `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    uses: porkytheblack/oasis/.github/workflows/tauri-release.yml@main
    with:
      app_slug: your-app-slug
      artifact_prefix: YourApp
      app_name: Your App Name
      app_dir: .
      distribute_to: r2,oasis,github
      auto_publish: true
      r2_public_url: https://cdn.example.com
    secrets:
      APPLE_CERTIFICATE: ${{ secrets.APPLE_CERTIFICATE }}
      APPLE_CERTIFICATE_PASSWORD: ${{ secrets.APPLE_CERTIFICATE_PASSWORD }}
      APPLE_SIGNING_IDENTITY: ${{ secrets.APPLE_SIGNING_IDENTITY }}
      APPLE_ID: ${{ secrets.APPLE_ID }}
      APPLE_PASSWORD: ${{ secrets.APPLE_PASSWORD }}
      APPLE_TEAM_ID: ${{ secrets.APPLE_TEAM_ID }}
      TAURI_SIGNING_PRIVATE_KEY: ${{ secrets.TAURI_SIGNING_PRIVATE_KEY }}
      TAURI_SIGNING_PRIVATE_KEY_PASSWORD: ${{ secrets.TAURI_SIGNING_PRIVATE_KEY_PASSWORD }}
      CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
      CLOUDFLARE_R2_ACCESS_KEY_ID: ${{ secrets.CLOUDFLARE_R2_ACCESS_KEY_ID }}
      CLOUDFLARE_R2_SECRET_ACCESS_KEY: ${{ secrets.CLOUDFLARE_R2_SECRET_ACCESS_KEY }}
      R2_BUCKET_NAME: ${{ secrets.R2_BUCKET_NAME }}
      OASIS_SERVER_URL: ${{ secrets.OASIS_SERVER_URL }}
      OASIS_CI_KEY: ${{ secrets.OASIS_CI_KEY }}
      NEXT_PUBLIC_OASIS_API_KEY: ${{ secrets.NEXT_PUBLIC_OASIS_API_KEY }}
      NEXT_PUBLIC_OASIS_SERVER_URL: ${{ secrets.NEXT_PUBLIC_OASIS_SERVER_URL }}
```

### Required Secrets

| Secret | Description |
|--------|-------------|
| `APPLE_CERTIFICATE` | Base64-encoded .p12 certificate |
| `APPLE_CERTIFICATE_PASSWORD` | Certificate password |
| `APPLE_SIGNING_IDENTITY` | e.g., "Developer ID Application: Name (TEAMID)" |
| `APPLE_ID` | Apple ID email |
| `APPLE_PASSWORD` | App-specific password |
| `APPLE_TEAM_ID` | Apple Developer Team ID |
| `TAURI_SIGNING_PRIVATE_KEY` | From `tauri signer generate` |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare account ID |
| `CLOUDFLARE_R2_ACCESS_KEY_ID` | R2 API access key |
| `CLOUDFLARE_R2_SECRET_ACCESS_KEY` | R2 API secret key |
| `R2_BUCKET_NAME` | R2 bucket name |
| `OASIS_SERVER_URL` | Your Oasis server URL |
| `OASIS_CI_KEY` | CI API key (`uk_live_*`) |

### Supported Platforms

| Platform | Target | Bundle Types |
|----------|--------|--------------|
| macOS (Apple Silicon) | `darwin-aarch64` | .dmg, .app.tar.gz |
| macOS (Intel) | `darwin-x86_64` | .dmg, .app.tar.gz |
| Linux | `linux-x86_64` | .AppImage, .deb, .AppImage.tar.gz |
| Windows | `windows-x86_64` | .exe (NSIS), .nsis.zip |

## Supporting Files

For extended documentation including workflow details and integration checklist, see [references/integration-guide.md](references/integration-guide.md).

## Common Gotchas

1. **API key prefix matters**: Public keys start with `pk_`, CI keys with `uk_live_`. Using the wrong type will fail silently.
2. **Update endpoint URL format**: Must include `{{target}}` and `{{current_version}}` placeholders exactly as shown.
3. **Signing key mismatch**: The public key in `tauri.conf.json` must match the private key used in CI. Regenerating keys without updating both will break updates.
4. **Events not sending**: Enable `debug: true` in SDK config to see network errors. Common causes: wrong serverUrl, CORS issues, invalid apiKey.
5. **Crashes not captured**: Auto-capture only works if `enableAutoCrashReporting: true` is set during `initOasis()`, not after.
6. **macOS signing failures**: `APPLE_SIGNING_IDENTITY` must match the certificate name exactly, including the team ID in parentheses.
7. **Release not appearing in app**: Check `auto_publish: true` in workflow. Unpublished releases exist in dashboard but aren't served to clients.
8. **dry_run for testing**: Use `dry_run: true` workflow input to test builds without uploading artifacts or registering releases.
9. **R2 public URL**: The `r2_public_url` must be the public-facing CDN URL, not the R2 API endpoint.
10. **Version format**: `appVersion` must be valid semver (e.g., "1.0.0", not "v1.0.0"). The workflow extracts version from git tags automatically.
