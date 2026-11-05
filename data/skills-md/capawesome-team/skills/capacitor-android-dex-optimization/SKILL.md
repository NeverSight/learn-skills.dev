---
name: capacitor-android-dex-optimization
description: "Guides the agent through enabling R8 in a Capacitor Android app so that it meets the Google Play DEX code optimization requirement (at least 25% obfuscation, optimization and shrinking from February 2027 for apps with more than 10 MB of DEX code). Covers `minifyEnabled true` with `proguard-android-optimize.txt` in `android/app/build.gradle`, the `-keep @interface com.getcapacitor.** { *; }` rule that prevents the startup crash in R8 full mode, per-plugin keep rules, resolving R8 'Missing class' build errors via `missing_rules.txt`, building a signed release APK with the debug keystore, and verifying with logcat, `mapping.txt` and the `r8.json` file inside the app bundle. Use when Play Console reports a DEX code optimization finding, when a Capacitor app crashes on startup after enabling `minifyEnabled`, or when R8 fails the release build. Do not use for iOS, resource shrinking, Capacitor plugin projects, Capacitor version upgrades, or non-Capacitor mobile frameworks."
license: MIT
compatibility: "Requires a Capacitor 6, 7 or 8 app with an `android/` platform, Android Gradle Plugin 8.0 or newer, a JDK matching the Capacitor version, and `adb` for on-device verification."
metadata:
  author: capawesome-team
  source: https://github.com/capawesome-team/skills/tree/main/skills/capacitor-android-dex-optimization
---

# Capacitor Android: DEX Code Optimization

Enable R8 in a Capacitor Android app and add the keep rules a Capacitor app needs so that the release build passes the Google Play DEX code optimization requirement without crashing at startup.

The Android project that `npx cap add android` generates sets `minifyEnabled false`, so R8 never runs and Google Play measures close to 0% obfuscation, optimization and shrinking. From February 2027, Google Play requires at least 25% in each category for apps with more than 10 MB of DEX code. Play reads the numbers from the `r8.json` file inside the app bundle for apps built with AGP 8.10 or newer.

## Prerequisites

| Requirement | Version |
| ----------- | ------- |
| Capacitor   | 6+      |
| Android Gradle Plugin | 8.0+ (8.10+ for the `r8.json` check in Step 6) |
| JDK         | 17 for Capacitor 6 and 7, 21 for Capacitor 8 |
| `adb`       | installed, with a device or emulator connected for Step 5 |

The project must be a Capacitor **app** (not a plugin) with an existing `android/` directory.

## Agent Behavior

- **Inspect before editing.** Read the current Gradle and ProGuard configuration first (Step 1). Never overwrite existing rules in `android/app/proguard-rules.pro`; append to them.
- **Keep rules narrow.** Never add `-keep class com.getcapacitor.** { *; }` or `-dontobfuscate`. Broad rules block the optimization that Google Play measures. `@capacitor/android` already ships consumer rules for plugin classes and their annotated methods.
- **Only release builds run R8.** Debug builds never show whether the rules are complete. Every verification step uses a signed release build.
- **Read `missing_rules.txt` before pasting it.** A `-dontwarn` rule is correct only for a class a plugin probes for at runtime (Step 4).

## Procedures

### Step 1: Analyze the Project

1. Verify the project is a Capacitor **app**: `package.json` lists `@capacitor/android` in `dependencies` and the `android/` directory exists. If `android/` is missing, abort and inform the user.
2. Read the `@capacitor/core` version from `package.json`. Record the major version.
3. Read the AGP version from `android/build.gradle`:

   ```groovy
   classpath 'com.android.tools.build:gradle:8.13.2'
   ```

   If the major version is below 8, abort and direct the user to the `capacitor-app-upgrades` skill first. Record whether the version is 8.10 or newer (this decides whether Step 6 applies).

4. Read the `release` build type in `android/app/build.gradle`. Record the values of `minifyEnabled`, `shrinkResources` (if present) and the `proguardFiles` line.
5. Read `android/app/proguard-rules.pro` and record every existing rule.
6. Read `android/gradle.properties` and record whether `android.enableR8.fullMode` is set. If it is set to `false`, inform the user that the keep rule in Step 3 makes this setting unnecessary and offer to remove it, because full mode produces higher optimization numbers.
7. Inventory the installed Capacitor plugins from `package.json` `dependencies`. Match these prefixes:

   - `@capacitor/*`
   - `@capawesome/*` and `@capawesome-team/*`
   - `@capacitor-community/*`
   - `@capacitor-firebase/*`
   - `@capacitor-mlkit/*`
   - `@revenuecat/*`
   - Any other package with `"capacitor"` in its `package.json` `keywords` array

   Record each plugin's package name. Step 3 uses this list.

### Step 2: Enable R8

In `android/app/build.gradle`, update the `release` build type. Replace `minifyEnabled false` with `minifyEnabled true` and replace `proguard-android.txt` with `proguard-android-optimize.txt`:

```diff
 android {
     buildTypes {
         release {
-            minifyEnabled false
-            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
+            minifyEnabled true
+            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
         }
     }
 }
```

`proguard-android.txt` contains `-dontoptimize`, which blocks most of what R8 could do, and AGP 9 no longer accepts that file by default. Do not add `shrinkResources true`. The Play metrics measure DEX code, and resource shrinking breaks resources that are referenced by name from JavaScript or `capacitor.config.ts` (for example the `smallIcon` of the Push Notifications plugin).

### Step 3: Add Keep Rules

1. If the Capacitor version recorded in Step 1 is below 8.6.0, append the Capacitor annotation rule to `android/app/proguard-rules.pro`. Skip this if the file already contains the exact rule or if the app is on Capacitor 8.6.0 or newer, which ships the rule in its consumer rules:

   ```diff
   +# Capacitor annotations: required below Capacitor 8.6.0 in R8 full mode (ionic-team/capacitor#8589)
   +-keep @interface com.getcapacitor.** { *; }
   ```

   R8 full mode (the default since AGP 8.0) strips annotations from classes that are not explicitly kept. Before Capacitor 8.6.0, `@capacitor/android` kept the classes annotated with `@CapacitorPlugin` but not the annotation types themselves. Without the rule, the build passes and the app crashes on startup with a `NullPointerException` in `com.getcapacitor.Plugin.getPermissionStates` the first time a plugin checks its permissions. The rule covers `@CapacitorPlugin`, `@Permission`, `@PermissionCallback`, `@ActivityCallback`, `@PluginMethod` and the legacy `@NativePlugin`.

2. For each plugin recorded in Step 1, look up its ProGuard rules and append them to `android/app/proguard-rules.pro` if they are missing:

   - Read the plugin's README in `node_modules/<package>/README.md` and search for a `Proguard`, `ProGuard` or `R8` section.
   - For Capawesome, Capacitor Firebase, Capacitor MLKit and RevenueCat plugins, the `capacitor-plugins` skill ships a reference file per plugin in its `references/` directory with the same section.

   Most plugins ship no rules of their own because the Capacitor consumer rules cover them. A plugin documents a rule only when it relies on reflection or serialization. Example for the Capawesome SQLite plugin:

   ```diff
   +# Capawesome plugins that rely on reflection
   +-keep class io.capawesome.capacitorjs.plugins.** { *; }
   ```

3. Do not add rules for `com.getcapacitor.**` classes, `@JavascriptInterface` methods, Firebase or Play Services. `@capacitor/android` declares its own consumer rules that keep every class annotated with `@CapacitorPlugin` together with its `@PluginMethod`, `@PermissionCallback` and `@ActivityCallback` methods. AGP's default rules keep `@JavascriptInterface` methods, and the large SDKs ship consumer rules of their own.

### Step 4: Build a Signed Release APK

Debug builds never run R8, and a release build has to be signed to install. Sign the local release build with the Android debug keystore through the properties that Android Studio injects into Gradle. This does not change `build.gradle`:

```bash
cd android
./gradlew assembleRelease \
  -Pandroid.injected.signing.store.file=$HOME/.android/debug.keystore \
  -Pandroid.injected.signing.store.password=android \
  -Pandroid.injected.signing.key.alias=androiddebugkey \
  -Pandroid.injected.signing.key.password=android
```

If `$HOME/.android/debug.keystore` does not exist, run any debug build once (`./gradlew assembleDebug`) to create it, then retry.

If the build fails with `Missing class` errors, R8 writes a ready-to-paste file to `android/app/build/outputs/mapping/release/missing_rules.txt`. Read each entry and decide per class:

| Case | Action |
| ---- | ------ |
| The plugin compiles against the library as `compileOnly` and probes for it at runtime with `Class.forName` (optional backend) | Add the `-dontwarn` rule to `android/app/proguard-rules.pro`. |
| The plugin calls the class unconditionally | Do **not** add `-dontwarn`. Add the missing dependency to `android/app/build.gradle` instead, or the app throws `NoClassDefFoundError` at runtime. |

Known optional backends:

```diff
+# Optional SQLite backends that the Capawesome SQLite plugin probes for at runtime
+-dontwarn io.requery.android.database.**
+-dontwarn net.zetetic.database.**
```

The Capawesome SQLite plugin compiles against both SQLCipher (`net.zetetic.database.**`) and requery's `sqlite-android` (`io.requery.android.database.**`) and bundles only the one selected in `android/variables.gradle`, so both `-dontwarn` lines are correct for that plugin.

Rebuild after every rule change until `assembleRelease` succeeds.

### Step 5: Verify on a Device

1. Confirm a device or emulator is connected with `adb devices`. If none is connected, hand the following checks to the user with the exact commands.
2. Install the release APK:

   ```bash
   adb install -r app/build/outputs/apk/release/app-release.apk
   ```

3. Clear logcat, launch the app, and watch for the failure signatures while it starts:

   ```bash
   adb logcat -c
   adb logcat | grep -E 'FATAL EXCEPTION|ClassNotFoundException|NoSuchMethodException|NullPointerException'
   ```

   The annotation crash from Step 3 appears within the first second. Afterwards, ask the user to run every flow that requests a permission or waits for another activity (camera, file picker, settings screen, sign-in) and watch logcat during each one.

4. Open `android/app/build/outputs/mapping/release/mapping.txt` and confirm that the plugin classes recorded in Step 1 still appear under their original names. Search for the plugin's Android package, for example `io.capawesome.capacitorjs.plugins`. A renamed plugin class means a keep rule is missing. Tell the user to archive `mapping.txt` with every release, since production stack traces need it.

### Step 6: Read the Play Numbers Before Uploading

Skip this step if the AGP version recorded in Step 1 is below 8.10: older versions do not write `r8.json`, and Play computes the numbers itself.

Build the app bundle with the same signing properties as Step 4 and read the R8 metadata from it:

```bash
./gradlew bundleRelease \
  -Pandroid.injected.signing.store.file=$HOME/.android/debug.keystore \
  -Pandroid.injected.signing.store.password=android \
  -Pandroid.injected.signing.key.alias=androiddebugkey \
  -Pandroid.injected.signing.key.password=android
unzip -p app/build/outputs/bundle/release/app-release.aab BUNDLE-METADATA/com.android.tools/r8.json
```

The file reports the obfuscation, optimization and shrinking percentages that Play Console shows in the app bundle explorer for that upload. Each must be at least 25%. If a value is below 25%, search `android/app/proguard-rules.pro` for broad rules (`-keep class **`, `-dontobfuscate`, `-dontoptimize`, `-dontshrink`) and narrow them.

### Step 7: Report

Summarize for the user:

1. The changes to `android/app/build.gradle` and `android/app/proguard-rules.pro`.
2. Any `-dontwarn` rule added and why it is safe, and any missing dependency that was added instead.
3. The three percentages from `r8.json` (if Step 6 ran).
4. That `mapping.txt` must be archived per release. An Android App Bundle embeds it in `BUNDLE-METADATA/`, so Play deobfuscates crash and ANR reports on its own. Only APK uploads need a manual upload in Play Console. The Firebase Crashlytics Gradle plugin uploads it automatically.
5. That the release build is now a standing test target: rerun Step 5 before every upload and check `missing_rules.txt` again whenever a plugin is added.

## Error Handling

- **App crashes on startup with `NullPointerException` at `com.getcapacitor.Plugin.getPermissionStates`**: The app is on Capacitor below 8.6.0 and the `-keep @interface com.getcapacitor.** { *; }` rule is missing from `android/app/proguard-rules.pro`. Add it (Step 3) and rebuild, or upgrade to Capacitor 8.6.0, which ships the rule (ionic-team/capacitor#8646).
- **Build fails with `Missing class <name>`**: Follow the `missing_rules.txt` decision table in Step 4.
- **Build fails because `proguard-android.txt` is not supported (AGP 9)**: Replace it with `proguard-android-optimize.txt` as in Step 2.
- **A plugin method is not found at runtime (`NoSuchMethodException`) or a plugin class is renamed in `mapping.txt`**: Add the plugin's documented keep rule from its README (Step 3, item 2). If the README has none, add `-keep class <plugin Android package>.** { *; }` for that plugin only and report it to the user as a candidate for an upstream fix.
- **`adb install` fails with `INSTALL_PARSE_FAILED_NO_CERTIFICATES`**: The release APK is unsigned. Rerun `assembleRelease` with the four `-Pandroid.injected.signing.*` properties from Step 4.
- **Permission checks return an empty result on Capacitor 8.5.2 or 8.5.3 without crashing**: Capacitor 8.5.2 added a null check in `getPermissionStates()` that hides the crash but returns an empty permission map, and `requestPermissions()` still throws. The keep rule from Step 3 is still required on those versions.
- **Resources missing at runtime after enabling `shrinkResources`**: Resources referenced by name from JavaScript or `capacitor.config.ts` are invisible to the resource shrinker. List them in `android/app/src/main/res/raw/keep.xml` with `tools:keep`, or remove `shrinkResources true`.

## Limitations

- The skill verifies a local release build signed with the debug keystore. The Play Console numbers are only final for the bundle that is uploaded.
- Setting `android.enableR8.fullMode=false` in `android/gradle.properties` also avoids the startup crash, but it lowers the optimization across the whole app and all its dependencies. The keep rule is the cheaper fix.
- Capacitor 8.6.0 ships the annotation keep rule and a rule for `@ActivityCallback` and `@PermissionCallback` methods on non-public base classes in its consumer rules. On 8.6.0 or newer, an existing `-keep @interface com.getcapacitor.** { *; }` line in the app is redundant but harmless. Leave it in place.

## Related Skills

- **`capacitor-app-development`** — General Android troubleshooting and app configuration.
- **`capacitor-plugins`** — Per-plugin reference files, including the ProGuard rules a plugin documents.
- **`capacitor-app-upgrades`** — Upgrade Capacitor and AGP to a version this skill supports.
- **`capawesome-cloud`** — Capawesome Cloud runs the Gradle build as is, so a project with `minifyEnabled true` produces the minified app bundle with the mapping file embedded.
