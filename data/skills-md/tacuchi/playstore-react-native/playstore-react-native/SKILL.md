---
name: playstore-react-native
description: >
  Guide and review the step-by-step preparation of a React Native project for Google Play Store
  release. Covers keystore generation, signing configuration, ProGuard/R8, and AAB build.
  Use when the user wants to publish, release, deploy, or prepare a React Native app for Play Store,
  or when they mention "react-native build-android", "bundleRelease react native", or "play store react native".
  Note: for Expo managed projects, use "eas build" instead.
---

# Play Store Release — React Native

Prepare a React Native (bare workflow) project to build a signed Android App Bundle (AAB) ready for Google Play Store.

> **Expo users**: If using Expo managed workflow, run `eas build --platform android` instead. This skill covers the bare React Native workflow.

## Workflow Overview

| Step | Action | Key file |
|------|--------|----------|
| 1 | Generate upload keystore | `upload-keystore.jks` |
| 2 | Create credentials file | `android/gradle.properties` |
| 3 | Configure signing in Gradle | `android/app/build.gradle` |
| 4 | Configure ProGuard / R8 | `android/app/proguard-rules.pro` |
| 5 | Build release AAB | CLI |
| 6 | Verify output | CLI + checklist |

---

## Step 1 — Generate Upload Keystore

```bash
keytool -genkeypair \
  -alias upload \
  -keyalg RSA -keysize 2048 \
  -validity 10000 \
  -storetype PKCS12 \
  -keystore upload-keystore.jks
```

Rules:
- `-validity 10000` = ~27 years. Google requires validity beyond Oct 22 2033.
- `-storetype PKCS12` — industry standard, avoids JKS migration warnings.
- With PKCS12, store password and key password **must be identical**.
- Store the `.jks` outside version control. Recommended: `~/.android/keystores/` or a secrets manager.

---

## Step 2 — Create Credentials

Add signing variables to `android/gradle.properties` (or `~/.gradle/gradle.properties` for global scope):

```properties
MYAPP_UPLOAD_STORE_FILE=upload-keystore.jks
MYAPP_UPLOAD_KEY_ALIAS=upload
MYAPP_UPLOAD_STORE_PASSWORD=<your-store-password>
MYAPP_UPLOAD_KEY_PASSWORD=<your-key-password>
```

Add to `.gitignore`:

```gitignore
*.jks
*.keystore
```

If credentials are in `android/gradle.properties`, ensure that file is in `.gitignore` or use `~/.gradle/gradle.properties` (per-user, never committed).

---

## Step 3 — Configure Signing in Gradle

Edit `android/app/build.gradle` (Groovy — default for React Native):

```groovy
android {
    signingConfigs {
        release {
            if (project.hasProperty('MYAPP_UPLOAD_STORE_FILE')) {
                storeFile file(MYAPP_UPLOAD_STORE_FILE)
                storePassword MYAPP_UPLOAD_STORE_PASSWORD
                keyAlias MYAPP_UPLOAD_KEY_ALIAS
                keyPassword MYAPP_UPLOAD_KEY_PASSWORD
            }
        }
    }

    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled enableProguardInReleaseBuilds
            shrinkResources enableProguardInReleaseBuilds
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

At the top of `android/app/build.gradle`, set the ProGuard flag:

```groovy
def enableProguardInReleaseBuilds = true
```

**Version management**: set `versionCode` and `versionName` in the `defaultConfig` block of the same file.

---

## Step 4 — ProGuard / R8

Create or edit `android/app/proguard-rules.pro`:

```proguard
# React Native Bridge
-keep class com.facebook.react.** { *; }
-keep class com.facebook.hermes.** { *; }
-keep class com.facebook.jni.** { *; }
-dontwarn com.facebook.**

# Hermes engine
-keep class com.facebook.hermes.unicode.** { *; }
-keep class com.facebook.jni.** { *; }

# SoLoader
-keep class com.facebook.soloader.** { *; }
-dontwarn com.facebook.soloader.**

# JNI — native module classes
-keepclassmembers class * {
    @com.facebook.react.uimanager.annotations.ReactProp <methods>;
}
-keepclassmembers class * {
    @com.facebook.react.bridge.ReactMethod <methods>;
}
-keep,includedescriptorclasses class * extends com.facebook.react.bridge.JavaScriptModule { *; }
-keep,includedescriptorclasses class * extends com.facebook.react.bridge.NativeModule { *; }

# OkHttp (used by React Native networking)
-dontwarn okhttp3.**
-dontwarn okio.**
-keep class okhttp3.** { *; }

# Keep native module registrations
-keep class com.facebook.react.PackageList { *; }
```

---

## Step 5 — Build Release AAB

```bash
# Option 1 — React Native CLI
npx react-native build-android --mode=release

# Option 2 — Gradle directly
cd android && ./gradlew bundleRelease
```

Useful flags:
- `./gradlew bundleRelease --stacktrace` — full stack trace on errors.
- `./gradlew clean bundleRelease` — clean before building.

Output: `android/app/build/outputs/bundle/release/app-release.aab`

---

## Step 6 — Verification Checklist

Run these checks before uploading:

```bash
# 1. Verify AAB exists
ls -lh android/app/build/outputs/bundle/release/app-release.aab

# 2. Verify signing
jarsigner -verify -verbose -certs android/app/build/outputs/bundle/release/app-release.aab

# 3. Check the signing certificate alias
keytool -printcert -jarfile android/app/build/outputs/bundle/release/app-release.aab

# 4. Verify versionCode (requires bundletool)
bundletool dump manifest --bundle=android/app/build/outputs/bundle/release/app-release.aab \
  | grep -E "versionCode|versionName"
```

Checklist:
- [ ] AAB signed with **upload** key (not debug)
- [ ] `versionCode` is higher than the previous upload
- [ ] `versionName` matches intended release
- [ ] `*.jks` and `*.keystore` are in `.gitignore`
- [ ] Credentials not committed (check `gradle.properties` location)
- [ ] `enableProguardInReleaseBuilds = true` is set
- [ ] Hermes is the JS engine (default since RN 0.70)

---

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `signingConfigs.release` not found | `signingConfigs` block placed after `buildTypes` | Move `signingConfigs` block before `buildTypes` |
| Hermes crash on release build | ProGuard stripped Hermes classes | Add Hermes `-keep` rules to `proguard-rules.pro` |
| `SYSTEM_ALERT_WINDOW` permission in release | Dev-only permission leaking into release manifest | Add `tools:node="remove"` in release `AndroidManifest.xml` overlay |
| `configureondemand` build failure | `org.gradle.configureondemand=true` in `gradle.properties` | Set to `false` — React Native requires all projects configured |
| APK rejected: "debug certificate" | Built without release signing | Verify `project.hasProperty` guard finds the credentials |

---

## Gotchas

1. **Groovy by default** — React Native projects use Groovy DSL (`build.gradle`, not `.gradle.kts`). Do not convert to Kotlin DSL unless the entire project has been migrated.

2. **`project.hasProperty()` guard** — The signing config uses a guard to avoid build failures when credentials are missing (e.g., on a fresh clone). Without the guard, `./gradlew assembleDebug` would fail if credentials aren't set up.

3. **Hermes vs JSC** — Hermes is the default engine since React Native 0.70. ProGuard rules must match the active engine. If the project uses JSC (legacy), adjust rules accordingly.

4. **New Architecture does not change signing** — React Native's New Architecture (TurboModules, Fabric) does not affect the signing or release build process. The same Gradle signing config applies.

5. **`enableProguardInReleaseBuilds`** — This flag is defined as a variable at the top of `build.gradle`, not in `gradle.properties`. Setting it in the wrong place has no effect.

6. **Expo managed workflow** — If the project uses Expo managed workflow (`app.json` with `expo` key, no `android/` directory), do NOT follow this skill. Use `eas build --platform android` instead. This skill is for bare React Native only.

7. **App Signing by Google Play** — Google re-signs your app with their key. The keystore you generate is the **upload key** only. If you lose it, you can request a reset through the Play Console.
