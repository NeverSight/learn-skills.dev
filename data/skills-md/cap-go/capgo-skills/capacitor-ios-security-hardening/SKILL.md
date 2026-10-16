---
name: capacitor-ios-security-hardening
description: Audits and progressively hardens Xcode security build settings for a Capacitor iOS app (ios/App/App.xcodeproj, scheme App) and native plugin code (Swift/ObjC/C, Package.swift, podspec). Covers `xcodebuild -showBuildSettings -json`, security compiler warnings, static analyzer checkers (`xcodebuild analyze`), Xcode Enhanced Security (ENABLE_ENHANCED_SECURITY, com.apple.security.hardened-process entitlements, pointer authentication / arm64e, memory tagging soft mode), what is safe for a WKWebView hybrid app vs what breaks CocoaPods, SPM binary xcframeworks or Cordova plugins, staged adoption, and a decision log. Use for "harden my iOS build", "enable Enhanced Security", security build settings audit, arm64e link errors after enabling pointer authentication, or Build and Analyze setup. Do not use for ATS/TLS, signing, secrets or WebView rules (capacitor-security), or App Store review (capacitor-apple-review-preflight).
allowed-tools:
  - Bash(xcodebuild -showBuildSettings *)
  - Bash(node *)
  - Bash(grep *)
  - Bash(lipo -archs *)
---

# Capacitor iOS Security Hardening

Audit the security-relevant Xcode build settings of a Capacitor app and its native plugins, then enable them in stages the user approves. This skill changes build settings and entitlements only. It never touches web code, ATS, signing, or secrets.

## When to Use

TRIGGER when:
- The user wants to audit or harden the iOS build configuration of a Capacitor app
- The user asks about Enhanced Security, `ENABLE_ENHANCED_SECURITY`, hardened-process entitlements, pointer authentication, arm64e, or memory tagging
- After enabling Enhanced Security, the link step fails with errors that mention `arm64e`
- A plugin author wants stricter warnings or static analysis for plugin Swift/ObjC/C code
- The user wants "Build and Analyze" / `xcodebuild analyze` in CI

Do not use:
- ATS, TLS pinning, signing, secrets, WebView config, Capsec scans: `capacitor-security`
- App Store privacy manifest and review checklist: `capacitor-apple-review-preflight`
- The AppDelegate to SceneDelegate migration: `capacitor-uiscene-migration`
- Android R8, network security config: `capacitor-security`

## Facts that change the plan

- **Build settings do not cross project boundaries.** Settings on the App target do not apply to Pods (`ios/App/Pods/Pods.xcodeproj`), to SPM packages (plugins, `CapApp-SPM`), or to the Cordova plugin package that `npx cap sync` generates. Hardening plugin code is done in the plugin repo (podspec / Package.swift), not in the app.
- **The App target of a stock Capacitor app is pure Swift** (`AppDelegate.swift`, `SceneDelegate.swift`). Clang warnings and analyzer checkers only matter if the app target has `.m`, `.mm`, `.c` or `.cpp` files. Detect languages before proposing them.
- **The Capacitor 8 templates already set three Stage A warnings** at project level (`GCC_WARN_ABOUT_RETURN_TYPE = YES_ERROR`, `GCC_WARN_UNINITIALIZED_AUTOS = YES_AGGRESSIVE`, `GCC_WARN_64_TO_32_BIT_CONVERSION = YES`). Report them as already hardened. Do not re-add them.
- **WKWebView content is not affected.** JavaScript and JIT run in WebKit's own processes. Enhanced Security entitlements apply to the app process and the native code linked into it (Capacitor runtime, plugins, SDKs).
- **Pointer authentication adds an `arm64e` slice** to device builds. Every binary linked into the app must also have `arm64e`, or the link fails. This is the main breakage risk in Capacitor apps. See [references/enhanced-security.md](references/enhanced-security.md).
- **Do not edit generated files.** `ios/App/Pods/**`, `Pods-App.*.xcconfig`, `ios/App/CapApp-SPM/Package.swift`, `ios/capacitor-cordova-ios-plugins/**` and `ios/debug.xcconfig` (SPM template, Debug only, CLI-managed) are rewritten by CocoaPods or `npx cap sync`. Put settings in the App project (Xcode Build Settings, which writes `project.pbxproj`) or in an xcconfig the team already owns.
- **The user owns the result.** Enhanced Security turns latent memory bugs into crashes. Report findings and get approval before changing anything. Test on real hardware before shipping.

## References

Only load a reference when its topic is in play.

| File | Load when |
|------|-----------|
| [references/settings-catalog.md](references/settings-catalog.md) | Building the audit table: every tracked setting, its hardened value, language scope, risk |
| [references/reading-build-settings.md](references/reading-build-settings.md) | Running `xcodebuild -showBuildSettings`, using the audit script, telling "explicitly disabled" from "default off" |
| [references/enhanced-security.md](references/enhanced-security.md) | Enabling the Enhanced Security capability, entitlements, pointer authentication with CocoaPods/SPM/binary SDKs, memory tagging |
| [references/plugin-authors.md](references/plugin-authors.md) | Hardening plugin code: podspec `pod_target_xcconfig`, Package.swift warning settings, analyzing a plugin repo, shipping arm64e xcframeworks |
| [references/decision-log.md](references/decision-log.md) | Creating or updating the team's decision document |

Script: [scripts/audit-build-settings.mjs](scripts/audit-build-settings.mjs) filters `xcodebuild -showBuildSettings -json` output to the tracked settings and marks each as hardened, default, or explicitly set (when given the pbxproj).

## Workflow

### 1. Brief and check source control

Tell the user in two or three sentences: you will audit first, write a plan, and change nothing until they approve. If the project has no git, recommend committing first. Stop if they decline.

### 2. Discover (read-only)

1. Confirm the iOS project: `ios/App/App.xcodeproj` exists. Note SPM (`ios/App/CapApp-SPM/`) vs CocoaPods (`ios/App/Podfile`, `App.xcworkspace`).
2. Read the Capacitor version from `package.json` (`@capacitor/ios`). Capacitor 8 deploys to iOS 15, Capacitor 9 to iOS 16 and needs Xcode 27.
3. Detect languages in the App target folder: `find ios/App/App -name '*.m' -o -name '*.mm' -o -name '*.c' -o -name '*.cpp'`. Also run `grep -E 'sourcecode\.cpp\.' ios/App/App.xcodeproj/project.pbxproj` to catch files whose type was overridden to C++/ObjC++.
4. List native dependencies that ship binaries: xcframeworks in `node_modules/**/ios/**`, `binaryTarget` in plugin `Package.swift` files, `vendored_frameworks` in podspecs.
5. Look for an existing decision document (`ios/xcode-security-settings.md` or similar) and read prior decisions.
6. Read evaluated settings for Debug and Release (see [references/reading-build-settings.md](references/reading-build-settings.md)):

```bash
xcodebuild -showBuildSettings -json -project ios/App/App.xcodeproj -target App -configuration Release > /tmp/app-release.json
node <skill>/scripts/audit-build-settings.mjs /tmp/app-release.json --pbxproj ios/App/App.xcodeproj/project.pbxproj
```

7. Read the entitlements file at the evaluated `CODE_SIGN_ENTITLEMENTS` path. The stock template has none; that is normal.

### 3. Build the plan and ask

Write the plan into the chat (or a file the user names). Group it by stage. Show only items that apply:

| Stage | Items | Default |
|-------|-------|---------|
| A. Compiler warnings | The five security warnings, only if C/ObjC/C++ is present in the target | on |
| B. Static analyzer | The security checkers plus the clang-tidy check; analyzer runs only on Analyze, so no build risk | on |
| C. Enhanced Security | Capability at project level, entitlements on the App target, pointer authentication with the dependency plan | on, after the dependency check |
| D. Memory tagging | `checked-allocations` + `soft-mode` | off, offer |
| E. Extra diagnostics | The noisier warnings | off, offer |
| F. Disabled settings | Ask about each explicit `= NO` that has no documented reason | on |

Ask the user to approve, edit or cancel. Real judgement calls to put to the user:
- A binary SDK with no `arm64e` slice: turn pointer authentication off on the App target (keeps the rest of Enhanced Security) or wait for the vendor.
- CocoaPods: add a `post_install` hook that enables pointer authentication on pod targets, or turn it off on the App target.
- Memory tagging: only with a plan to test on capable hardware.

### 4. Apply, one stage at a time

- Apply settings at the **project** level of `App.xcodeproj` so every target inherits them, unless the setting is per target (entitlements, pointer-authentication opt-out).
- Best path: ask the user to set them in Xcode (project > Build Settings > All). Then verify with `grep` on `project.pbxproj`. If you edit `project.pbxproj` yourself, edit only the `buildSettings` dictionaries of the project's own Debug and Release `XCBuildConfiguration` entries (the ones listed by the PBXProject `buildConfigurationList`), keep the `KEY = VALUE;` syntax, and re-run `-showBuildSettings` to confirm.
- Add Enhanced Security through **Signing & Capabilities > + Capability > Enhanced Security** on the App target. This creates or updates `App.entitlements` and wires `CODE_SIGN_ENTITLEMENTS`. Details: [references/enhanced-security.md](references/enhanced-security.md).
- After each stage, build (step 5) before starting the next one. If a stage breaks the build, revert that stage, record why in the decision log, and continue.

### 5. Verify

```bash
# Sync, then build for a device (arm64e only exists for device SDKs)
npx cap sync ios
xcodebuild -project ios/App/App.xcodeproj -scheme App -configuration Release \
  -destination 'generic/platform=iOS' CODE_SIGNING_ALLOWED=NO build
# CocoaPods projects: use -workspace ios/App/App.xcworkspace instead of -project

# Static analyzer
xcodebuild -project ios/App/App.xcodeproj -scheme App -configuration Debug \
  -destination 'generic/platform=iOS Simulator' analyze

# Confirm the slices of the built app binary
lipo -archs ~/Library/Developer/Xcode/DerivedData/App-*/Build/Products/Release-iphoneos/App.app/App
```

- Re-run the audit script. Every approved setting shows as hardened.
- Simulator builds keep working: simulator SDKs have no `arm64e`, and the build system drops it. Do not add a simulator-only opt-out.
- Run the app on a real device. Check launch, plugin calls, and the JS `pause` / `resume` events. With memory tagging in soft mode, collect the simulated crash reports from Xcode Organizer or the device logs (`ios-android-logs`).

### 6. Report and record

Report: what was enabled, what was already hardened, what was skipped and why, which dependencies block `arm64e`, and the action item to test on hardware before release. Then update the decision document ([references/decision-log.md](references/decision-log.md)).

## Error Handling

| Symptom | Cause | Fix |
|---------|-------|-----|
| Link fails with messages that mention `arm64e` after enabling Enhanced Security | A pod, SPM package or xcframework was built without `arm64e` | Find it with `lipo -archs`. Source pods: `post_install` hook. SPM source packages: workspace setting `iOSPackagesShouldBuildARM64e`. Binary with no slice: `ENABLE_POINTER_AUTHENTICATION = NO` on the App target and ask the vendor. See [references/enhanced-security.md](references/enhanced-security.md) |
| `Sandbox: rsync(...) deny(1) file-write-create` in `[CP] Embed Pods Frameworks` | `ENABLE_USER_SCRIPT_SANDBOXING = YES` with CocoaPods script phases | Keep it `NO` on the App target while on CocoaPods, record the reason, revisit after the SPM migration (`cocoapods-to-spm`) |
| New warnings flood after Stage A | Warnings were off before | Fix real bugs first. If a warning is in generated or vendored code, keep it on and defer that code; never flip `-Werror` for the whole project |
| Settings changed but `-showBuildSettings` shows the old value | Set on the wrong level, or a target-level value overrides the project | Check the target column in Xcode; remove the target override if it has no reason |
| App crashes at launch only on newer devices after memory tagging | Soft mode was turned off too early, or a native library has a memory bug | Re-enable soft mode, collect reports, fix or update the library (often bundled C code such as zip or SQLite) |
| Edits vanished after `npx cap sync` or `pod install` | A generated file was edited | Move the setting to the App project or to the plugin's own podspec / Package.swift |

## Related Skills

- `capacitor-security`: ATS, signing, secrets, WebView and storage security
- `cocoapods-to-spm`: SPM removes most pod-related hardening friction
- `capacitor-plugin-spm-support`: Package.swift layout for plugins
- `ios-android-logs`: capture crash and memory-tagging reports from devices
