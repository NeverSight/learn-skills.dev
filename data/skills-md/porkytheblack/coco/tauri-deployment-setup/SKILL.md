---
name: tauri-deployment-setup
description: Expert guide for setting up Tauri deployment pipelines with GitHub Actions, code signing, and Oasis update server integration.
---

# Tauri Deployment Setup — Development Guide

You are an expert on Tauri deployment pipelines. Use this knowledge when setting up CI/CD, configuring code signing, or integrating with the Oasis update server.

## What It Is

A comprehensive deployment system for Tauri desktop applications that handles multi-platform builds, code signing, artifact storage, and automatic updates.

**Reusable workflow**: `porkytheblack/oasis/.github/workflows/tauri-release.yml@main`
**This project's workflow**: `.github/workflows/release.yaml`

## Architecture at a Glance

```
Developer pushes tag → GitHub Actions triggers
                              ↓
        ┌─────────────────────┴─────────────────────┐
        ↓                     ↓                     ↓
   macOS Build           Windows Build         Linux Build
   (Apple signed)        (optional sign)       (AppImage)
        ↓                     ↓                     ↓
        └─────────────────────┬─────────────────────┘
                              ↓
                    Tauri Update Signing
                              ↓
        ┌─────────────────────┼─────────────────────┐
        ↓                     ↓                     ↓
   Upload to R2         Register with Oasis    GitHub Release
   (CDN storage)        (update manifest)      (user downloads)
```

## Quick Start

### 1. Install dependencies

```bash
pnpm add -D @tauri-apps/cli
```

### 2. Generate signing keys

```bash
npx @tauri-apps/cli signer generate -w ~/.tauri/keys/your-app.key
# Save the public key for tauri.conf.json
# Save the private key as TAURI_SIGNING_PRIVATE_KEY secret
```

### 3. Create release workflow

```yaml
# .github/workflows/release.yaml
name: Release

on:
  push:
    tags: ["v*"]

permissions:
  contents: write

jobs:
  release:
    uses: porkytheblack/oasis/.github/workflows/tauri-release.yml@main
    with:
      app_slug: your-app
      app_name: Your App
      artifact_prefix: YourApp
      app_dir: app
      distribute_to: r2,oasis,github
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
```

### 4. Configure updater in tauri.conf.json

```json
{
  "plugins": {
    "updater": {
      "pubkey": "YOUR_PUBLIC_KEY_HERE",
      "endpoints": [
        "https://oasis.yourdomain.com/{app_slug}/update/{{target}}-{{arch}}/{{current_version}}"
      ]
    }
  }
}
```

### 5. Trigger release

```bash
./app/scripts/bump-version.sh patch
git push && git push --tags
```

## Version Files to Sync

| File | Format | Location |
|------|--------|----------|
| `package.json` | `"version": "X.Y.Z"` | App root |
| `tauri.conf.json` | `"version": "X.Y.Z"` | src-tauri/ |
| `Cargo.toml` | `version = "X.Y.Z"` | src-tauri/ |
| Status bar | `vX.Y.Z` display | UI component |

Use `./app/scripts/bump-version.sh` to update all files automatically.

## Distribution Targets

| Target | Purpose | When to Use |
|--------|---------|-------------|
| `github` | GitHub Releases page | User downloads, changelog |
| `r2` | Cloudflare R2 CDN | Fast artifact delivery |
| `oasis` | Update server | Auto-update manifests |

Combine with comma: `distribute_to: r2,oasis,github`

## Required Secrets

### Apple Code Signing (macOS)

| Secret | Description |
|--------|-------------|
| `APPLE_CERTIFICATE` | Base64-encoded .p12 certificate |
| `APPLE_CERTIFICATE_PASSWORD` | Certificate password |
| `APPLE_SIGNING_IDENTITY` | e.g., "Developer ID Application: Your Name" |
| `APPLE_ID` | Apple ID email |
| `APPLE_PASSWORD` | App-specific password (not Apple ID password) |
| `APPLE_TEAM_ID` | 10-character Team ID |

### Tauri Update Signing

| Secret | Description |
|--------|-------------|
| `TAURI_SIGNING_PRIVATE_KEY` | Private key from signer generate |
| `TAURI_SIGNING_PRIVATE_KEY_PASSWORD` | Password used during generation |

### Cloudflare R2

| Secret | Description |
|--------|-------------|
| `CLOUDFLARE_ACCOUNT_ID` | Account ID from dashboard |
| `CLOUDFLARE_R2_ACCESS_KEY_ID` | R2 API token ID |
| `CLOUDFLARE_R2_SECRET_ACCESS_KEY` | R2 API token secret |
| `R2_BUCKET_NAME` | Bucket name |

### Oasis Server

| Secret | Description |
|--------|-------------|
| `OASIS_SERVER_URL` | e.g., `https://oasis.yourdomain.com` |
| `OASIS_CI_KEY` | CI authentication key |

## Tauri Capabilities

Add to `capabilities/default.json`:

```json
{
  "permissions": [
    "core:default",
    "core:window:default",
    "core:window:allow-start-dragging",
    "shell:default",
    "shell:allow-open",
    "dialog:default",
    "fs:default",
    "http:default",
    "updater:default",
    "updater:allow-check",
    "updater:allow-download-and-install",
    "process:default",
    "process:allow-restart"
  ]
}
```

## Release Commands (This Project)

| Action | Command |
|--------|---------|
| Bump patch | `./app/scripts/bump-version.sh patch` |
| Bump minor | `./app/scripts/bump-version.sh minor` |
| Bump major | `./app/scripts/bump-version.sh major` |
| Set version | `./app/scripts/bump-version.sh --set 2.0.0` |
| Preview | `./app/scripts/bump-version.sh patch --dry-run` |
| Push release | `git push && git push --tags` |
| Redeploy | `./app/scripts/redeploy.sh` |

## Common Gotchas

1. **Apple signing identity must match exactly** — Copy the full name from Keychain Access, including "Developer ID Application:" prefix.
2. **App-specific password, not Apple ID password** — Generate at appleid.apple.com under Security → App-Specific Passwords.
3. **Public key mismatch** — If updates fail signature verification, regenerate keys and update both `tauri.conf.json` and the GitHub secret.
4. **R2 public URL required** — Set `R2_PUBLIC_URL` as a repository variable (not secret) for the CDN base URL.
5. **Version mismatch breaks updates** — All version files must match. Use the bump script, not manual edits.
6. **Tag format matters** — Workflow triggers on `v*` tags. Use `v0.1.0`, not `0.1.0`.
7. **Workflow permissions** — Ensure `contents: write` permission for creating GitHub releases.
8. **macOS notarization takes time** — Apple notarization can take 5-15 minutes. Don't cancel the workflow early.
9. **Secrets are case-sensitive** — Double-check secret names match exactly.
10. **Dry run first** — Use `workflow_dispatch` with `dry_run: true` to test without uploading.
