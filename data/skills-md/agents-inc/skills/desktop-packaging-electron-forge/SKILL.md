---
name: desktop-packaging-electron-forge
description: Electron Forge build toolchain -- makers, publishers, code signing, fuses, hooks, CI/CD packaging
---

# Electron Forge Packaging

> **Quick Guide:** Electron Forge v7 is the official Electron build toolchain. Configure via `forge.config.ts` with typed imports from `@electron-forge/shared-types`. Use **makers** to produce platform-specific installers (Squirrel for Windows, DMG/ZIP for macOS, deb/rpm for Linux). Use **publishers** to upload artifacts (GitHub Releases, S3, Snapcraft). Always code-sign production builds -- macOS requires both signing and notarization. Enable Electron **Fuses** to harden the binary at package time. Use **hooks** (`prePackage`, `postMake`) for custom build logic. Electron itself MUST be a `devDependency` -- Forge bundles only `dependencies`.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST place `electron` in `devDependencies` -- Forge provides the Electron binary during packaging; placing it in `dependencies` bloats the app by ~200MB)**

**(You MUST code-sign macOS builds with `osxSign` and `osxNotarize` in `packagerConfig` -- unsigned apps are blocked by Gatekeeper on macOS 10.15+)**

**(You MUST enable `asar: true` in `packagerConfig` -- without ASAR, your source code ships as plain-text files readable by any user)**

**(You MUST store signing credentials in environment variables -- never hardcode secrets in `forge.config.ts`)**

**(You MUST enable Fuses (`FuseV1Options.RunAsNode: false`, `OnlyLoadAppFromAsar: true`) for production security -- without them, attackers can bypass ASAR integrity and run arbitrary Node.js code)**

</critical_requirements>

---

**Auto-detection:** Electron Forge, electron-forge, forge.config.ts, forge.config.js, @electron-forge, maker-squirrel, maker-dmg, maker-deb, maker-rpm, maker-zip, maker-flatpak, maker-snap, maker-appx, maker-wix, maker-pkg, maker-msix, publisher-github, publisher-s3, publisher-snapcraft, plugin-vite, plugin-webpack, plugin-fuses, FusesPlugin, osxSign, osxNotarize, electron-forge make, electron-forge publish, electron-forge package

**When to use:**

- Configuring `forge.config.ts` for packaging and distribution
- Choosing and configuring makers for target platforms
- Setting up publishers for automated release distribution
- Code signing macOS (notarization) or Windows (Authenticode) builds
- Enabling Electron Fuses for binary hardening
- Adding build hooks for custom pre/post-packaging logic
- Setting up CI/CD pipelines for cross-platform builds
- Deciding between Electron Forge and electron-builder

**When NOT to use:**

- Electron app architecture (main/renderer process, IPC, preload) -- use the Electron framework skill
- Choosing or configuring a bundler for renderer code in isolation
- Auto-update implementation (that is an Electron framework concern, not a Forge concern)
- UI framework selection for renderers

**Key patterns covered:**

- forge.config.ts structure with typed configuration
- Platform-specific maker selection and configuration
- macOS code signing + notarization setup
- Windows Authenticode signing (traditional + Azure Trusted Signing)
- Fuses plugin for binary hardening
- Publisher configuration (GitHub, S3, Snapcraft)
- Build hooks and lifecycle
- CI/CD cross-platform build matrix
- Forge vs electron-builder decision framework

---

<philosophy>

## Philosophy

Electron Forge is a **unified build pipeline** that composes first-party Electron tools (`@electron/packager`, `@electron/rebuild`, `@electron/osx-sign`, `@electron/notarize`, `@electron/fuses`) into a single workflow. Rather than reimplementing build logic, Forge orchestrates existing tools through three steps:

1. **Package** -- `@electron/packager` creates the platform-specific app bundle (.app, .exe)
2. **Make** -- Makers transform the bundle into distributable installers (.dmg, .msi, .deb)
3. **Publish** -- Publishers upload make artifacts to distribution targets (GitHub, S3)

**Why Forge over alternatives:**

- First-party: maintained by the Electron team, receives new features (ASAR integrity, universal macOS builds) as soon as they ship
- Composable: makers, publishers, and plugins are independent npm packages
- TypeScript-native: `forge.config.ts` with full type inference since v7

**Key constraint:** Forge runs makers only for the current host OS by default. Cross-platform builds require CI/CD with per-platform runners (macOS for .dmg, Windows for .exe, Linux for .deb).

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: forge.config.ts Structure

The configuration file defines packaging options, makers, publishers, plugins, and hooks. All fields are optional.

```typescript
import type { ForgeConfig } from "@electron-forge/shared-types";
import { FusesPlugin } from "@electron-forge/plugin-fuses";
import { FuseV1Options, FuseVersion } from "@electron/fuses";

const config: ForgeConfig = {
  packagerConfig: {
    asar: true,
    icon: "./assets/icon", // omit extension -- Forge picks .icns/.ico/.png
    name: "MyApp",
    executableName: "my-app",
    appBundleId: "com.example.myapp",
  },
  makers: [
    /* see Pattern 2 */
  ],
  publishers: [
    /* see Pattern 5 */
  ],
  plugins: [
    /* see Pattern 4 */
  ],
  hooks: {
    /* see Pattern 6 */
  },
};

export default config;
```

**Key constraint:** You cannot override `dir`, `arch`, `platform`, `out`, or `electronVersion` in `packagerConfig` -- Forge sets these internally.

See [examples/core.md](examples/core.md) for full configuration with makers, signing, and fuses.

---

### Pattern 2: Maker Selection by Platform

Each maker produces a specific installer format for a target OS. Install only the makers you need.

| Maker            | Package                          | Platform     | Output                    |
| ---------------- | -------------------------------- | ------------ | ------------------------- |
| Squirrel.Windows | `@electron-forge/maker-squirrel` | Windows      | `.exe` (auto-updating)    |
| WiX MSI          | `@electron-forge/maker-wix`      | Windows      | `.msi`                    |
| MSIX             | `@electron-forge/maker-msix`     | Windows      | `.msix`                   |
| AppX             | `@electron-forge/maker-appx`     | Windows      | `.appx` (Microsoft Store) |
| DMG              | `@electron-forge/maker-dmg`      | macOS        | `.dmg`                    |
| PKG              | `@electron-forge/maker-pkg`      | macOS        | `.pkg` (Mac App Store)    |
| ZIP              | `@electron-forge/maker-zip`      | macOS, Linux | `.zip`                    |
| deb              | `@electron-forge/maker-deb`      | Linux        | `.deb` (Debian/Ubuntu)    |
| RPM              | `@electron-forge/maker-rpm`      | Linux        | `.rpm` (Fedora/RHEL)      |
| Flatpak          | `@electron-forge/maker-flatpak`  | Linux        | `.flatpak`                |
| Snap             | `@electron-forge/maker-snap`     | Linux        | `.snap`                   |

**Recommended starter set:** Squirrel (Windows) + DMG + ZIP (macOS) + deb (Linux).

See [examples/core.md](examples/core.md) for maker configuration examples.

---

### Pattern 3: Code Signing

macOS and Windows both require code signing for distribution. Without it, OS security warnings block or discourage installation.

#### macOS (Sign + Notarize)

```typescript
packagerConfig: {
  osxSign: {},  // empty object activates defaults -- signs with first valid identity
  osxNotarize: {
    appleId: process.env.APPLE_ID,
    appleIdPassword: process.env.APPLE_PASSWORD,  // app-specific password, NOT Apple ID password
    teamId: process.env.APPLE_TEAM_ID,
  },
},
```

**Requirements:** Apple Developer Program membership, "Developer ID Application" certificate in Keychain, `hardenedRuntime: true` (required for notarization).

#### Windows (Authenticode)

```typescript
// Squirrel maker with traditional certificate
{
  name: "@electron-forge/maker-squirrel",
  config: {
    certificateFile: process.env.WIN_CSC_LINK,
    certificatePassword: process.env.WIN_CSC_KEY_PASSWORD,
  },
},
```

**Key point:** Since June 2023, private keys for code signing certificates must be stored on FIPS 140 Level 2 hardware. Azure Trusted Signing is the modern alternative for Windows -- see [examples/signing.md](examples/signing.md).

See [examples/signing.md](examples/signing.md) for full signing configuration, notarization strategies, and Azure Trusted Signing setup.

---

### Pattern 4: Fuses Plugin (Binary Hardening)

Fuses are bits in the Electron binary flipped at package time to enable/disable features permanently.

```typescript
import { FusesPlugin } from "@electron-forge/plugin-fuses";
import { FuseV1Options, FuseVersion } from "@electron/fuses";

plugins: [
  new FusesPlugin({
    version: FuseVersion.V1,
    [FuseV1Options.RunAsNode]: false,
    [FuseV1Options.EnableCookieEncryption]: true,
    [FuseV1Options.EnableNodeOptionsEnvironmentVariable]: false,
    [FuseV1Options.EnableNodeCliInspectArguments]: false,
    [FuseV1Options.EnableEmbeddedAsarIntegrityValidation]: true,
    [FuseV1Options.OnlyLoadAppFromAsar]: true,
    [FuseV1Options.GrantFileProtocolExtraPrivileges]: false,
  }),
],
```

**Why critical:** Without `RunAsNode: false`, attackers can set `ELECTRON_RUN_AS_NODE=1` and run arbitrary code. Without `OnlyLoadAppFromAsar: true`, ASAR integrity validation can be bypassed by placing files alongside the archive.

**Verification:** `npx @electron/fuses read --app /path/to/packaged/app`

See [examples/core.md](examples/core.md) for the full fuses configuration with explanations.

---

### Pattern 5: Publishers

Publishers upload make artifacts to distribution targets.

```typescript
publishers: [
  {
    name: "@electron-forge/publisher-github",
    config: {
      repository: { owner: "my-org", name: "my-app" },
      prerelease: true,
    },
  },
],
```

| Publisher | Package                               | Target               |
| --------- | ------------------------------------- | -------------------- |
| GitHub    | `@electron-forge/publisher-github`    | GitHub Releases      |
| S3        | `@electron-forge/publisher-s3`        | Amazon S3 bucket     |
| Snapcraft | `@electron-forge/publisher-snapcraft` | Snap Store           |
| GCS       | `@electron-forge/publisher-gcs`       | Google Cloud Storage |

**Authentication:** Use `GITHUB_TOKEN` env var for GitHub publisher. Use AWS credentials (env vars or shared credentials file) for S3.

See [examples/publishers.md](examples/publishers.md) for publisher configuration with CI/CD integration.

---

### Pattern 6: Build Hooks

Hooks insert custom logic at specific points in the build lifecycle.

```typescript
hooks: {
  prePackage: async (config, platform, arch) => {
    // Run before @electron/packager -- generate assets, validate config
  },
  postMake: async (config, makeResults) => {
    // Run after all makers -- rename artifacts, upload to CDN, notify
    // Return modified makeResults array to affect subsequent steps
    return makeResults;
  },
},
```

| Hook                | When                            | Can Mutate?                           |
| ------------------- | ------------------------------- | ------------------------------------- |
| `generateAssets`    | Before start or package         | No                                    |
| `prePackage`        | Before @electron/packager       | No                                    |
| `packageAfterCopy`  | After packager copies build dir | No                                    |
| `packageAfterPrune` | After devDependencies pruned    | No                                    |
| `postPackage`       | After package completes         | No                                    |
| `preMake`           | Before makers run               | No                                    |
| `postMake`          | After makers complete           | Yes -- return modified `MakeResult[]` |
| `readPackageJson`   | Every package.json read         | Yes -- return modified package.json   |

See [examples/hooks.md](examples/hooks.md) for hook implementation examples.

---

### Pattern 7: Bundler Plugins (Vite / Webpack)

Forge plugins integrate bundlers for compiling main and renderer process code with HMR.

```typescript
import { VitePlugin } from "@electron-forge/plugin-vite";

plugins: [
  new VitePlugin({
    build: [
      { entry: "src/main.ts", config: "vite.main.config.mts" },
      { entry: "src/preload.ts", config: "vite.preload.config.mts" },
    ],
    renderer: [
      { name: "main_window", config: "vite.renderer.config.mts" },
    ],
  }),
],
```

**Status:** The Vite plugin is marked **experimental** as of v7.5.0 -- minor versions may include breaking changes.

**Key detail:** The plugin injects global variables (`MAIN_WINDOW_VITE_DEV_SERVER_URL`, `MAIN_WINDOW_VITE_NAME`) for loading the renderer in dev vs production. Declare these in a `.d.ts` file for TypeScript.

See [examples/core.md](examples/core.md) for Vite plugin setup and global variable declarations.

</patterns>

---

<decision_framework>

## Decision Framework

### Forge vs electron-builder

```
Choosing a build tool?
+-- Want first-party Electron support (ASAR integrity, universal macOS)?
|   +-- YES --> Electron Forge (receives features same-day as Electron)
+-- Need YAML-based config, NSIS installer, or broad community support?
|   +-- YES --> electron-builder (more installer targets, larger community)
+-- Need maximum customization for enterprise?
|   +-- YES --> electron-builder (more config options, NSIS scripting)
+-- Starting a new project?
    +-- YES --> Electron Forge (official recommendation, TypeScript config)
```

| Factor                | Electron Forge              | electron-builder          |
| --------------------- | --------------------------- | ------------------------- |
| Maintainer            | Electron team               | Community                 |
| Config format         | TypeScript / JavaScript     | YAML / JSON / JS          |
| New Electron features | Same-day                    | Delayed                   |
| Plugin ecosystem      | Makers, publishers, plugins | Built-in monolith         |
| Windows installers    | Squirrel, WiX, MSIX, AppX   | NSIS, Squirrel, MSI, AppX |
| macOS installers      | DMG, ZIP, PKG               | DMG, ZIP, PKG, MAS        |
| npm downloads         | ~50K/week                   | ~1.4M/week                |
| Architecture          | Composable packages         | Monolithic                |

### Maker Selection

```
Which maker for your platform?
+-- Windows?
|   +-- Auto-updating desktop app --> Squirrel.Windows
|   +-- Enterprise/IT deployment --> WiX MSI
|   +-- Microsoft Store --> AppX or MSIX
+-- macOS?
|   +-- Direct distribution --> DMG (drag-to-install) + ZIP (for auto-updater)
|   +-- Mac App Store --> PKG
+-- Linux?
|   +-- Debian/Ubuntu --> deb
|   +-- Fedora/RHEL --> RPM
|   +-- Universal sandboxed --> Flatpak or Snap
```

</decision_framework>

---

**Detailed resources:**

- [examples/core.md](examples/core.md) -- forge.config.ts setup, makers, Vite plugin, fuses, dependency management
- [examples/signing.md](examples/signing.md) -- macOS notarization, Windows Authenticode, Azure Trusted Signing, entitlements
- [examples/publishers.md](examples/publishers.md) -- GitHub, S3, Snapcraft publishers with CI/CD patterns
- [examples/hooks.md](examples/hooks.md) -- Build lifecycle hooks, custom makers, extending Forge
- [reference.md](reference.md) -- Maker/publisher quick-reference tables, fuse options, CLI commands, Forge vs builder comparison

---

<red_flags>

## RED FLAGS

**Critical Issues:**

- Placing `electron` in `dependencies` instead of `devDependencies` -- bloats the packaged app by ~200MB because Forge already provides the binary
- Shipping without code signing -- macOS Gatekeeper blocks unsigned apps entirely; Windows SmartScreen shows scary warnings
- Hardcoding signing credentials in `forge.config.ts` -- secrets end up in version control; always use `process.env`
- Not enabling ASAR (`asar: false`) -- ships your source code as readable plain-text files
- Not setting `RunAsNode: false` fuse -- allows `ELECTRON_RUN_AS_NODE=1` to execute arbitrary code with your app's permissions

**Architecture Issues:**

- Running `electron-forge make` on macOS expecting Windows .exe output -- makers run only on the target OS (use CI/CD with per-platform runners)
- Placing native modules (better-sqlite3, sharp) inside ASAR without `asarUnpack` -- native addons cannot load from inside an ASAR archive
- Not running `@electron/rebuild` for native modules -- modules compiled for system Node.js crash in Electron's Node.js runtime (Forge runs rebuild automatically during package, but manual installs need it)
- Using `electron-forge package` for distribution -- this produces an uninstallable app bundle; use `make` for distributable installers

**Configuration Mistakes:**

- Setting `asar: true` without `asarUnpack` for native modules -- the app will crash at runtime trying to load the native addon
- Forgetting the `platforms` array on makers -- maker runs on all platforms and fails on unsupported ones
- Using `osxNotarize` without `osxSign` -- notarization requires a signed binary; Apple rejects unsigned submissions
- Using your Apple ID password instead of an app-specific password for `osxNotarize` -- regular passwords are rejected when 2FA is enabled

**Gotchas & Edge Cases:**

- `electron-forge start` in dev mode does not run makers -- dev mode uses unpackaged source; always test with `make` before release
- Notarization takes 2-10 minutes per build -- factor this into CI/CD timeout settings
- Squirrel.Windows handles first-run events (shortcuts, desktop icons) -- your main process must handle Squirrel startup events or the app opens multiple times during install
- `__dirname` resolves to virtual ASAR paths in packaged builds -- use `app.isPackaged` + `process.resourcesPath` for resource file paths
- The Vite plugin is experimental since v7.5.0 -- minor version bumps may include breaking changes to its config shape
- Azure Trusted Signing paths must not contain spaces -- signing fails silently if any path has spaces
- Forge hooks run in parallel, not sequentially -- do not rely on execution order between hooks of the same type

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST place `electron` in `devDependencies` -- Forge provides the Electron binary during packaging; placing it in `dependencies` bloats the app by ~200MB)**

**(You MUST code-sign macOS builds with `osxSign` and `osxNotarize` in `packagerConfig` -- unsigned apps are blocked by Gatekeeper on macOS 10.15+)**

**(You MUST enable `asar: true` in `packagerConfig` -- without ASAR, your source code ships as plain-text files readable by any user)**

**(You MUST store signing credentials in environment variables -- never hardcode secrets in `forge.config.ts`)**

**(You MUST enable Fuses (`FuseV1Options.RunAsNode: false`, `OnlyLoadAppFromAsar: true`) for production security -- without them, attackers can bypass ASAR integrity and run arbitrary Node.js code)**

**Failure to follow these rules will produce insecure, bloated, or unsigned builds that OS security mechanisms will block or warn users about.**

</critical_reminders>
