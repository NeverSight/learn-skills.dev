---
name: expo-testing
description: Build, install, and test Expo/React Native apps on simulators and physical devices. Use when asked to "run on simulator", "install on device", "test on phone", "run detox", "preview build", or "build and test".
---

# Expo Testing

Build, install, and test Expo/React Native apps on iOS simulators and physical devices.

## Detect Project Config

Before doing anything, read the project's config to determine:

1. **Bundle ID** — from `app.config.js`, `app.config.ts`, or `app.json` → `expo.ios.bundleIdentifier`
2. **EAS profiles** — from `eas.json` → available build profiles (development, preview, production)
3. **Detox config** — from `.detoxrc.js` or `detox.config.js` → test runner, build commands, device configs
4. **Deep link scheme** — from `app.config.js` → `expo.scheme`
5. **Package manager** — `bun.lockb` → bun, `pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, else npm

## Two Paths

### Path 1: Simulator (default)

Use for automated testing, TDD loops, and AFK runs.

```
1. Prebuild (if native code changed)
   npx expo prebuild --platform ios --clean

2. Build for simulator
   xcodebuild -workspace ios/<AppName>.xcworkspace \
     -scheme <AppName> \
     -configuration Debug \
     -sdk iphonesimulator \
     -derivedDataPath ios/build

3. Install on booted simulator
   xcrun simctl install booted ios/build/Build/Products/Debug-iphonesimulator/<AppName>.app

4. Launch
   xcrun simctl launch booted <bundleId>
```

**Auto-rebuild detection**: Check if any of these changed since last build:
- `ios/` directory contents (native modules)
- `package.json` or lock file (new native dependencies)
- `app.config.js` / `app.json` (config changes)
- Any file matching `*.podspec` or `Podfile`

If none changed, skip prebuild and xcodebuild — just reinstall and launch.

### Path 2: Physical Device

Use for manual testing, sharing with others, or testing hardware-specific features.

**Local (tethered via USB):**
```
npx expo run:ios --device
```
Lists connected devices and installs directly.

**EAS cloud build (shareable):**
```
1. Build
   eas build --profile preview --platform ios

2. Download and install
   # EAS provides a QR code / install link
   # Or download .ipa and install via Finder/Apple Configurator
```

**Device registration** (first time only):
```
eas device:create
# Follow the URL to register the device's UDID
```

## Running Detox Tests

After build + install on simulator:

```
# Full suite
npx detox test --configuration ios.sim.debug

# Specific test file
npx detox test --configuration ios.sim.debug e2e/<testFile>.e2e.ts

# With screenshots on failure (default Detox behavior)
# Artifacts saved to artifacts/ directory
```

**Before running Detox**, check if the Detox binary needs rebuilding:
```
npx detox build --configuration ios.sim.debug --if-missing
```

This skips the build if the binary already exists and is up to date.

## Best Practices for E2E

- **Use `testID` props** on interactive elements for reliable selectors
- **Disable Detox synchronization** for screens with animations or timers:
  ```typescript
  await device.disableSynchronization();
  // interact with animated screen
  await device.enableSynchronization();
  ```
- **Deep links for test entry points**: If the app has a URL scheme configured (`expo.scheme` in app config), you can launch directly to a screen:
  ```typescript
  await device.openURL({ url: '<scheme>://e2e' });
  ```
  If no scheme exists and you need E2E entry points, consider adding one — it lets tests skip onboarding and jump to the screen under test.

## Screenshot Capture

For dogfooding and bug discovery, capture screenshots:

```typescript
// In Detox tests
await device.takeScreenshot('descriptive-name');
```

Screenshots are saved to the Detox artifacts directory (configurable in `.detoxrc.js`). Ensure the artifacts directory is in `.gitignore`.

For manual screenshot capture on simulator:
```bash
xcrun simctl io booted screenshot screenshots/<name>.png
```

Store dogfooding artifacts in `.dogfooding/` (gitignored):
```
.dogfooding/
  screenshots/
  findings.md
  logs/
```

## Failure Artifacts

When tests fail, preserve everything useful for debugging:
- **Screenshots** — Detox captures automatically on failure
- **Device logs** — `xcrun simctl spawn booted log stream --level error`
- **Console output** — from the test runner
- **Sentry** — check for crash reports if Sentry is configured

## Parallel Simulator Isolation

When running multiple swarms/agents overnight that both need simulators, each must use its own:

```bash
# Create a named simulator for this agent
xcrun simctl create "Swarm-1" "iPhone 16"
# Returns a UDID like: 4A2B3C4D-5E6F-7890-ABCD-EF1234567890

# Boot it
xcrun simctl boot <UDID>

# Build and install targeting that specific simulator
xcrun simctl install <UDID> ios/build/Build/Products/Debug-iphonesimulator/<AppName>.app
xcrun simctl launch <UDID> <bundleId>
```

For Detox, target a specific device by name in `.detoxrc.js`:

```js
devices: {
  simulator: {
    type: 'ios.simulator',
    device: { type: 'iPhone 16', name: 'Swarm-1' }
  }
}
```

**Cleanup after the run:**
```bash
xcrun simctl delete <UDID>
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `No bundle URL present` | Run `npx expo start` in another terminal first |
| Build fails after adding package | `npx expo prebuild --platform ios --clean` then rebuild |
| Simulator not found | `xcrun simctl list devices available` to find booted device |
| Detox timeout | Increase timeout in `.detoxrc.js`, check for missing `testID` |
| EAS build queue slow | Use local builds for simulator testing, EAS for device sharing |
| `xcrun simctl install` fails | Check the .app path — Debug vs Release, simulator vs device |
