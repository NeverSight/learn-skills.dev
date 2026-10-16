---
name: capacitor-app-upgrade-v8-to-v9
description: Upgrades a Capacitor app from v8 to v9 (prerelease, installed with @next until GA). Covers preflight (Node 24, Xcode 27, Android Studio 2026.1.1, UIScene adoption from 8.5), `npx cap migrate`, and the manual checklist - iOS 16 target, @UIApplicationMain to @main, removed CAPBridge APIs, AGP 9.2.1, Gradle 9.5.1, SDK 37/minSdk 26, gradle.properties cleanup, built-in Kotlin, jcenter removal, core-ktx, proguard-android.txt rename, optional Cordova runtime, `cap run --url`, push `alert` removal, splash fade default. Use for "upgrade to Capacitor 9", errors like "'@UIApplicationMain' is deprecated", "Could not find method jcenter()", getDefaultProguardFile('proguard-android.txt') failures, duplicate Kotlin plugin, duplicate class core-ktx, "unknown option '-l'". Do not use for 8.4 to 8.5 UIScene only (use capacitor-uiscene-migration), plugin libraries (use capacitor-plugin-upgrade-v8-to-v9), or older majors.
allowed-tools:
  - Bash(node -e *)
---

# Capacitor App Upgrade v8 to v9

Capacitor 9 is a prerelease (`next` dist-tag, 9.0.0-alpha.x as of October 2026). Install with `@next`; switch to `@latest` / `^9.0.0` once 9.0.0 is GA. Tell the user it is not GA before upgrading a production app, and work on a branch.

Canonical source: https://capacitorjs.com/docs/updating/9-0

## When to Use

TRIGGER when:
- App is on `@capacitor/core` 8.x and the user wants Capacitor 9
- Build errors after moving to Xcode 27 / Swift 6, AGP 9, or Gradle 9 in a Capacitor 8 app
- `npx cap run -l --host ...` no longer works (`--url` replaced it)
- Push notifications `presentationOptions: ['alert']` stopped showing banners on iOS
- Cordova-plugin-free app fails on `CapacitorCordova` / `com.getcapacitor.cordova` references after upgrading

Do not use:
- App still on 7 or older -> `capacitor-app-upgrades` (chain majors first)
- Only the 8.4 -> 8.5 UIScene step -> `capacitor-uiscene-migration`
- Plugin library repo -> `capacitor-plugin-upgrade-v8-to-v9`
- CocoaPods to SPM move -> `cocoapods-to-spm` (recommended, separate step)

## Live Project Snapshot

!`node -e "const fs=require('fs');if(!fs.existsSync('package.json'))process.exit(0);const pkg=JSON.parse(fs.readFileSync('package.json','utf8'));const out=[];for(const section of ['dependencies','devDependencies']){for(const [name,version] of Object.entries(pkg[section]||{})){if(name.startsWith('@capacitor/'))out.push(section+'.'+name+'='+version)}}out.push('node='+process.version);const p='ios/App/App/';out.push('ios.SceneDelegate='+fs.existsSync(p+'SceneDelegate.swift'));out.push('ios.Podfile='+fs.existsSync('ios/App/Podfile'));console.log(out.sort().join('\n'))"`

## Procedure

### 1. Preflight (stop and report if any fails)

```bash
node --version                     # must be >= 24
xcodebuild -version                # must be Xcode 27+
java -version                      # use the JDK bundled with Android Studio 2026.1.1+
grep -c UIApplicationSceneManifest ios/App/App/Info.plist
git status --short                 # clean tree, so the migration diff is reviewable
```

- Node < 24 or Xcode < 27: ask the user to upgrade tooling first.
- No scene manifest or no `SceneDelegate.swift`: the app has not adopted UIScene. Run the `capacitor-uiscene-migration` skill on 8.5 first, verify it, then return here. Doing both at once hides which step broke deep links.
- Inventory native customizations before migrating: custom `AppDelegate`/`SceneDelegate` code, custom `CAPBridgeViewController` subclass, local plugins in `ios/App/App` or `android/app/src`, extra variables in `variables.gradle`, Cordova plugins (`npx cap ls`).

### 2. Packages and automated migration

```bash
npm i -D @capacitor/cli@next
npx cap migrate
```

`cap migrate` updates dependencies and the template-shaped native files, and prints what it could not do. It is not built for monorepos; migrate those by hand. Then bump every other `@capacitor/*` package to `@next` (official plugins are 9.0.0 too) and check Capgo/third-party plugins for a Capacitor 9 compatible release (`npm view <pkg> peerDependencies`).

### 3. Manual checklist (verify each, even if migrate reported success)

- iOS -> `references/ios.md`: Xcode 27, iOS 16.0 in pbxproj + Podfile, `@main`, removed `CAPBridge`/bridge APIs in app code, SPM recommendation.
- Android -> `references/android.md`: gradle.properties cleanup, `variables.gradle` values, remove `targetSdkVersion`, `proguard-android-optimize.txt`, explicit `rootProject.ext` defs, core-ktx, Kotlin plugin removal, `jcenter()`, AGP 9.2.1, Gradle 9.5.1, google-services 4.5.0.
- Plugins, CLI, config -> `references/plugins-and-cli.md`: official plugin variable bumps, push `alert`, splash `launchFadeOutDuration`, `cap run --url`, Cordova runtime now optional.

### 4. Sync, build, verify

`npx cap sync`, then run everything in `references/verification.md`: leftover-symbol greps, both native builds, device checks. Report results per platform.

## Traps

- `android.builtInKotlin=false` or `android.sdk.defaultTargetSdkToCompileSdkIfUnset=false` left in `gradle.properties` (the AGP Upgrade Assistant writes them) breaks the build. Delete the whole AGP 8 compatibility block.
- `proguard-android.txt` fails at configuration time even with `minifyEnabled false`.
- Leaving `apply plugin: 'kotlin-android'` next to AGP 9's built-in Kotlin fails with a duplicate-plugin error, also inside local plugin modules.
- Apps with zero Cordova plugins no longer get `CapacitorCordova` / `capacitor-cordova-android`. Native code importing those symbols stops compiling; there is no flag to force-include them.
- Pre-UIScene AppDelegate code (`CAPBridge.handleOpenUrl`, `application(_:open:)` custom logic) both fails to compile and would never be called. Move it to the SceneDelegate.
- CocoaPods Trunk is expected to go read-only on December 2, 2026. Offer `cocoapods-to-spm` after the upgrade is green.

## Error Handling

| Error | Fix |
|---|---|
| `'@UIApplicationMain' is deprecated` (error in Swift 6 mode) | Replace with `@main` |
| `Cannot find 'CAPBridge' in scope` | Use `ApplicationDelegateProxy.shared` APIs (`references/ios.md`) |
| `Could not find method jcenter()` | Replace with `mavenCentral()` in every `build.gradle`, including local plugins |
| Configuration failure mentioning `proguard-android.txt` | Use `proguard-android-optimize.txt` |
| Kotlin plugin already applied / duplicate plugin `org.jetbrains.kotlin.android` | Remove `kotlin-android`, `kotlin-gradle-plugin` classpath, `kotlin-stdlib` |
| Duplicate class `androidx.core.*` (core-ktx) | Drop old `core-ktx`, depend on `androidx.core:core:1.19.0` |
| `Could not get unknown property 'androidxAppCompatVersion'` | Add `def x = rootProject.ext.x` at the top of `app/build.gradle` |
| Namespace collision between library modules | A plugin kept a scaffold/forked `namespace`; update or report that plugin |
| `error: unknown option '-l'` on `cap run` | `npx cap run <platform> --url http://<ip>:<port>` |
| `npm ERR! engine` / Node version error | Node 24+ |

## References

Only load a reference when its topic is in play.

| File | Load when |
|---|---|
| `references/ios.md` | Any iOS step or iOS build error |
| `references/android.md` | Any Android/Gradle step or build error |
| `references/plugins-and-cli.md` | Official plugin behavior changes, live reload, Cordova plugins |
| `references/verification.md` | After sync: greps, builds, device checklist |

Related skills: `capacitor-uiscene-migration`, `capacitor-app-upgrades`, `capacitor-plugin-upgrade-v8-to-v9`, `cocoapods-to-spm`, `capacitor-push-notifications`, `capacitor-splash-screen`.
