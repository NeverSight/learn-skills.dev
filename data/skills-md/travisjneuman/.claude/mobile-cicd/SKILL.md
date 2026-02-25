---
name: mobile-cicd
description: >-
  Fastlane, GitHub Actions for mobile, code signing (iOS provisioning, Android keystores), beta distribution (TestFlight, Firebase App Distribution), and app store submissions. Use when setting up mobile build pipelines, automating releases, or managing signing.
---

# Mobile CI/CD Skill

Automated build, test, sign, and deploy pipelines for iOS and Android apps.

---

## Fastlane

### iOS Fastfile

```ruby
# ios/fastlane/Fastfile
default_platform(:ios)

platform :ios do
  desc "Run tests"
  lane :test do
    run_tests(scheme: "MyApp")
  end

  desc "Build and upload to TestFlight"
  lane :beta do
    increment_build_number(xcodeproj: "MyApp.xcodeproj")
    match(type: "appstore", readonly: true)
    build_app(scheme: "MyApp", export_method: "app-store")
    upload_to_testflight(skip_waiting_for_build_processing: true)
    slack(message: "New iOS beta uploaded to TestFlight")
  end

  desc "Deploy to App Store"
  lane :release do
    match(type: "appstore", readonly: true)
    build_app(scheme: "MyApp", export_method: "app-store")
    upload_to_app_store(
      submit_for_review: true,
      automatic_release: false,
      force: true
    )
  end
end
```

### Android Fastfile

```ruby
# android/fastlane/Fastfile
default_platform(:android)

platform :android do
  desc "Run tests"
  lane :test do
    gradle(task: "test")
  end

  desc "Build and upload to Play Store internal track"
  lane :beta do
    gradle(task: "bundleRelease")
    upload_to_play_store(
      track: "internal",
      aab: "app/build/outputs/bundle/release/app-release.aab"
    )
  end

  desc "Promote to production"
  lane :release do
    upload_to_play_store(
      track: "internal",
      track_promote_to: "production",
      rollout: "0.1" # 10% rollout
    )
  end
end
```

---

## Code Signing

### iOS (match)

```ruby
# Matchfile
git_url("https://github.com/org/certificates.git")
storage_mode("git")
type("appstore")
app_identifier("com.example.myapp")

# Usage
match(type: "development")  # Dev certificates
match(type: "appstore")     # Distribution certificates
```

### Android (Keystore)

```bash
# Generate keystore (once)
keytool -genkey -v -keystore release.keystore \
  -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000

# Store securely - NEVER commit to git
# Use CI secrets or encrypted storage
```

```groovy
// android/app/build.gradle
android {
    signingConfigs {
        release {
            storeFile file(System.getenv("KEYSTORE_PATH") ?: "release.keystore")
            storePassword System.getenv("KEYSTORE_PASSWORD")
            keyAlias System.getenv("KEY_ALIAS")
            keyPassword System.getenv("KEY_PASSWORD")
        }
    }
}
```

---

## GitHub Actions

### React Native / Expo

```yaml
# .github/workflows/mobile-ci.yml
name: Mobile CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npm test
      - run: npx tsc --noEmit

  build-ios:
    needs: test
    runs-on: macos-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - uses: ruby/setup-ruby@v1
        with: { ruby-version: '3.2' }
      - run: npm ci
      - run: cd ios && bundle install && bundle exec fastlane beta
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD: ${{ secrets.APPLE_APP_PASSWORD }}

  build-android:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { java-version: '17', distribution: 'temurin' }
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: cd android && bundle install && bundle exec fastlane beta
        env:
          KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
          KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
```

---

## EAS Build (Expo)

```json
// eas.json
{
  "cli": { "version": ">= 12.0.0" },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal",
      "ios": { "simulator": false },
      "channel": "preview"
    },
    "production": {
      "channel": "production",
      "autoIncrement": true
    }
  },
  "submit": {
    "production": {
      "ios": { "appleId": "your@email.com", "ascAppId": "1234567890" },
      "android": { "serviceAccountKeyPath": "./google-sa-key.json" }
    }
  }
}
```

```bash
# Build for preview
eas build --profile preview --platform all

# Build for production
eas build --profile production --platform all

# Submit to stores
eas submit --platform ios --latest
eas submit --platform android --latest

# OTA update (no store review)
eas update --branch production --message "Bug fix"
```

---

## Beta Distribution

| Platform | iOS | Android |
|----------|-----|---------|
| First-party | TestFlight | Play Store internal track |
| Firebase | App Distribution | App Distribution |
| Expo | EAS internal distribution | EAS internal distribution |

---

## App Store Optimization (ASO)

- Title: Primary keyword + brand (30 chars iOS, 50 chars Android)
- Subtitle/Short description: Secondary keywords
- Screenshots: Show key features, use device frames
- Keywords field (iOS only): Comma-separated, no spaces
- Update release notes with each version
- Respond to reviews (improves ranking)

---

## Release Checklist

- [ ] All tests passing on CI
- [ ] Version number bumped
- [ ] Build number incremented
- [ ] Release notes written
- [ ] Screenshots updated (if UI changed)
- [ ] Beta tested by QA team
- [ ] Code signing valid and not expiring soon
- [ ] Privacy policy URL current
- [ ] App review guidelines compliance checked

---

## Related Resources

- `~/.claude/skills/react-native/SKILL.md` - React Native development
- `~/.claude/skills/flutter-development/SKILL.md` - Flutter development
- `~/.claude/agents/mobile-release-manager.md` - Release management agent
- `~/.claude/rules/workflows/deployment-cicd.md` - General CI/CD patterns

---

_Automate everything. Sign securely. Ship confidently._
