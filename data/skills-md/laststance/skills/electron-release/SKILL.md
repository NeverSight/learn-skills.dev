---
name: electron-release
description: Guides Electron app release process including build, code signing, notarization, and GitHub Release with auto-update support. Use when releasing Electron apps, creating DMG installers, setting up auto-update, or troubleshooting notarization issues.
---

# Electron Release Guide

Complete release workflow for Electron applications with auto-update support.

## Supported Configurations

| Stack | Platform | Build Type | Status |
|-------|----------|------------|--------|
| Vite + electron-builder | macOS | Local | ✅ Documented |
| Other configurations | - | - | 📝 To be added |

## Quick Start (macOS + Vite + electron-builder)

```bash
# 1. Build with notarization
APPLE_KEYCHAIN_PROFILE=your-profile pnpm build:mac

# 2. Rename ZIPs (GitHub converts spaces to dots)
cp "dist/App Name-X.Y.Z-arm64-mac.zip" "dist/App-Name-X.Y.Z-arm64-mac.zip"
cp "dist/App Name-X.Y.Z-mac.zip" "dist/App-Name-X.Y.Z-mac.zip"

# 3. Create release with ALL files
gh release create vX.Y.Z \
  dist/latest-mac.yml \
  "dist/App-Name-X.Y.Z-arm64-mac.zip" \
  "dist/App-Name-X.Y.Z-mac.zip" \
  dist/app-name-X.Y.Z-arm64.dmg \
  dist/app-name-X.Y.Z-x64.dmg \
  --title "vX.Y.Z" --notes "Release notes..."
```

## Complete Workflow

### Phase 1: Pre-Release

1. **Update version** in `package.json`
2. **Commit version bump**:
   ```bash
   git add package.json
   git commit -m "chore(release): bump version to X.Y.Z"
   git push origin main
   ```

### Phase 2: Build

3. **Build with notarization**:
   ```bash
   APPLE_KEYCHAIN_PROFILE=your-profile pnpm build:mac
   ```

   | Env Var | Purpose |
   |---------|---------|
   | `APPLE_KEYCHAIN_PROFILE` | Keychain profile for notarization |
   | Alternative: `APPLE_ID`, `APPLE_APP_SPECIFIC_PASSWORD`, `APPLE_TEAM_ID` | Direct credentials |

4. **Verify build output**:
   ```bash
   ls -la dist/*.dmg dist/*.zip dist/*.yml
   ```

   Expected files:
   - `latest-mac.yml` - Auto-update metadata
   - `App Name-X.Y.Z-arm64-mac.zip` - ARM64 update payload
   - `App Name-X.Y.Z-mac.zip` - x64 update payload
   - `app-name-X.Y.Z-arm64.dmg` - ARM64 installer
   - `app-name-X.Y.Z-x64.dmg` - x64 installer

### Phase 3: Prepare Release Assets

5. **Rename ZIP files** (critical for auto-update):
   ```bash
   # GitHub converts spaces to dots, but latest-mac.yml expects hyphens
   cp "dist/App Name-X.Y.Z-arm64-mac.zip" "dist/App-Name-X.Y.Z-arm64-mac.zip"
   cp "dist/App Name-X.Y.Z-mac.zip" "dist/App-Name-X.Y.Z-mac.zip"
   ```

6. **Verify `latest-mac.yml` URLs match renamed files**:
   ```bash
   cat dist/latest-mac.yml
   # Check that 'url:' entries match your renamed ZIP filenames
   ```

### Phase 4: GitHub Release

7. **Create release with all required files**:
   ```bash
   gh release create vX.Y.Z \
     dist/latest-mac.yml \
     "dist/App-Name-X.Y.Z-arm64-mac.zip" \
     "dist/App-Name-X.Y.Z-mac.zip" \
     dist/app-name-X.Y.Z-arm64.dmg \
     dist/app-name-X.Y.Z-x64.dmg \
     --title "vX.Y.Z" \
     --notes "$(cat <<'EOF'
   ## What's Changed
   - Feature 1
   - Bug fix 2
   EOF
   )"
   ```

8. **Verify release assets**:
   ```bash
   gh release view vX.Y.Z --json assets --jq '.assets[].name'
   ```

## Required Files for Auto-Update

| File | Purpose | Missing = |
|------|---------|-----------|
| `latest-mac.yml` | Version + SHA512 hashes | "No updates available" |
| `*-arm64-mac.zip` | ARM64 update payload | Download fails on M1/M2/M3 |
| `*-mac.zip` | x64 update payload | Download fails on Intel |
| `*.dmg` | Manual download | No manual install option |

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| DMG only, no ZIP | Auto-update silently fails | Upload all ZIP files |
| Missing `latest-mac.yml` | "No updates available" | Upload `latest-mac.yml` |
| Wrong ZIP filename | Download error | Rename to match `latest-mac.yml` URLs |
| No notarization env var | Gatekeeper blocks app | Set `APPLE_KEYCHAIN_PROFILE` |
| Spaces in filename | 404 on download | Rename: spaces → hyphens |

## Troubleshooting

### "Download error" on auto-update
```bash
# Check if filenames match
cat dist/latest-mac.yml | grep url:
gh release view vX.Y.Z --json assets --jq '.assets[].name'
# URLs in yml must exactly match asset names
```

### "No updates available"
```bash
# Verify latest-mac.yml is uploaded
gh release view vX.Y.Z --json assets --jq '.assets[].name' | grep yml
```

### Gatekeeper blocks app
```bash
# Rebuild with notarization
APPLE_KEYCHAIN_PROFILE=your-profile pnpm build:mac
# Check build log for "notarization successful"
```

## electron-builder.yml Reference

```yaml
mac:
  target:
    - target: dmg
      arch: [arm64, x64]
    - target: zip
      arch: [arm64, x64]
  notarize: true
  hardenedRuntime: true

publish:
  provider: github
  owner: your-org
  repo: your-repo
```

## Success Criteria

- [ ] Build completes with "notarization successful"
- [ ] All 5 files uploaded to GitHub Release
- [ ] ZIP filenames match `latest-mac.yml` URLs exactly
- [ ] Test: older version detects update
- [ ] Test: download and install succeeds
