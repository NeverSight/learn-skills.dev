---
name: android-ci-cd-expert
description: "Use when setting up continuous integration/deployment (GitHub Actions), Gradle Play Publisher, Fastlane, or R8 Proguard rules for Release builds."
category: devops
risk: high
source: community
date_added: "2026-03-31"
metadata:
  triggers:
    - "@ci-cd"
    - "github-actions"
    - "release-build"
    - "r8-obfuscation"
    - "proguard-rules"
    - "fastlane"
---

# Android CI/CD & Release Architect 🚀🤖

A masterclass framework for configuring flawless Android CI/CD pipelines, automating Play Store releases, and safely applying R8 obfuscation without breaking reflection.

## ⚡ When to Use

- **GitHub Actions**: Setting up `pull_request` checks or `push` release workflows.
- **R8 / ProGuard**: Configuring rules to shrink, obfuscate, and optimize the release APK/AAB.
- **Signing Keystores**: Safely extracting and using Base64 Keystore secrets in CI.
- **Fastlane / Gradle Play Publisher**: Automating deployments to Google Play Console.

## 🛡️ R8 Obfuscation & ProGuard Rules (Critical)

R8 is enabled by default in release builds (`isMinifyEnabled = true`). It strips unused code and renames classes to single letters, which **will crash your app** if you use Reflection or JSON serialization (like Gson/Moshi) without proper rules.

### The Architect's Checklist for R8:
1. **Data Models**: If using a local DB (Room) or Network API (Retrofit), you MUST add `@Keep` annotations to your Domain Models / DTOs, or add `-keep class com.example.model.** { *; }` to `proguard-rules.pro`.
2. **JNI / C++**: If using NDK, you must keep native methods using `-keepclasseswithmembernames class * { native <methods>; }`.
3. **Empty Projects**: When scaffolding an empty project intended for production, you must NEVER leave `proguard-rules.pro` completely blank. At minimum, scaffold standard safeguards for Android endpoints.
4. **Testing R8**: Advise the user to test the release build using `./gradlew installRelease` (rather than just debug) before shipping.

## 🤖 GitHub Actions Pipeline Excellence

When generating `.github/workflows/android.yml`, adhere to the following Senior Architect standards:

### 1. Build & Test (PRs)
- **Base OS**: Use `ubuntu-latest`.
- **Java Setup**: Use `actions/setup-java@v4` with `distribution: 'zulu'` and `java-version: '17'` (or 21 for latest AGP).
- **Gradle Caching**: ALWAYS use `gradle/actions/setup-gradle@v3` to cache dependencies and speed up CI drastically.
- **Verification**: Run `./gradlew lintDebug ktlintCheck testDebugUnitTest` sequentially.

### 2. Signing & Release 
When generating a release workflow, never hardcode passwords. Ensure these environment variables are documented for the user to add to GitHub Secrets:
- `KEYSTORE_BASE64`
- `SIGNING_KEY_ALIAS`
- `SIGNING_KEY_PASSWORD`
- `SIGNING_STORE_PASSWORD`

### 3. Example Release Snippet
```yaml
      - name: Decode Keystore
        run: |
          echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 --decode > app/keystore.jks
      
      - name: Build Release AAB
        run: ./gradlew bundleRelease
        env:
          SIGNING_KEY_ALIAS: ${{ secrets.SIGNING_KEY_ALIAS }}
          SIGNING_KEY_PASSWORD: ${{ secrets.SIGNING_KEY_PASSWORD }}
          SIGNING_STORE_PASSWORD: ${{ secrets.SIGNING_STORE_PASSWORD }}
```

## 🏎️ Fastlane & Deployment

- Prefer **Gradle Play Publisher (GPP)** if you only need Play Store automation without iOS overhead.
- If using **Fastlane**, store the `play-store-credentials.json` via GitHub secrets and inject it securely.
- Automate track progression (Internal -> Alpha -> Beta -> Production).

## 🛑 CI/CD Anti-Patterns to Avoid
- **Committing Keystores**: NEVER commit `.jks` files directly to Git.
- **Downloading SDKs manually**: Never manually fetch `tools_r25...zip`. Use `setup-android` or standard standard runners which come pre-installed with the SDK.
- **Matrix Builds Overkill**: Do not use matrix builds on every PR for multiple API levels unless explicitly maintaining a fundamental Library. App tests should just run standard local unit tests on PRs to save CI minutes.

## 🔗 Related Resources
- [Build Verification Skill](../android-build-verification/SKILL.md)
- [Code Review Expert (For PR triggers)](../android-code-review-expert/SKILL.md)
