---
name: apple-developer-toolkit
description: "All-in-one Apple developer skill with three integrated tools shipped as a single unified binary. (1) Documentation search across Apple frameworks, symbols, and 1,267 WWDC sessions from 2014-2025. No credentials needed. (2) App Store Connect CLI with 120+ commands covering builds (find/wait/upload), TestFlight, pre-submission validate, submissions, signing, subscriptions (family-sharable), IAP, analytics, Xcode Cloud, metadata workflows, release pipeline dashboard, insights, win-back offers, promoted purchases, product pages, nominations, accessibility declarations, pre-orders, pricing filters, localizations update, diff, webhooks with local receiver, workflow automation, and more. Requires App Store Connect API key. (3) Multi-platform app builder (iOS/watchOS/tvOS/iPad/macOS/visionOS) that generates complete Swift/SwiftUI apps from natural language with auto-fix, simulator launch, interactive chat mode, and open-in-Xcode. Requires an LLM API key and Xcode. Includes 38 iOS development rules and 12 SwiftUI best practice guides for Liquid Glass, navigation, state management, and modern APIs. All three tools ship as one binary (appledev). USE WHEN: Apple API docs, App Store Connect management, WWDC lookup, or building iOS/watchOS/tvOS/macOS/visionOS apps from scratch. DON'T USE WHEN: non-Apple platforms or general coding."
metadata:
  {
    "openclaw":
      {
        "emoji": "🍎",
        "requires":
          {
            "bins": ["node"],
            "anyBins": ["appledev"],
          },
        "install":
          [
            {
              "id": "appledev",
              "kind": "brew",
              "tap": "Abdullah4AI/tap",
              "formula": "appledev",
              "bins": ["appledev"],
              "label": "Apple Developer Toolkit - unified binary (Homebrew)",
            },
          ],
        "env":
          {
            "optional":
              [
                {
                  "name": "APPSTORE_KEY_ID",
                  "description": "App Store Connect API Key ID. Required only for App Store Connect features. Get from https://appstoreconnect.apple.com/access/integrations/api",
                },
                {
                  "name": "APPSTORE_ISSUER_ID",
                  "description": "App Store Connect API Issuer ID. Required only for App Store Connect features.",
                },
                {
                  "name": "APPSTORE_PRIVATE_KEY_PATH",
                  "description": "Path to App Store Connect API .p8 private key file. Required only for App Store Connect features. Alternative: use APPSTORE_PRIVATE_KEY or APPSTORE_PRIVATE_KEY_B64.",
                },
                {
                  "name": "LLM_API_KEY",
                  "description": "LLM API key for code generation. Required only for iOS App Builder. Supports multiple AI backends.",
                },
              ],
          },
      },
  }
---

# Apple Developer Toolkit

Three tools in one binary. Each part works independently with different credential requirements.

## Architecture

Ships as a single unified binary `appledev` with multi-call support:

```
appledev build ...    # iOS app builder (SwiftShip)
appledev store ...    # App Store Connect CLI
appledev b ...        # Short alias
appledev s ...        # Short alias
```

One binary, three tools, zero duplication.

## Credential Requirements by Feature

| Feature | Credentials Needed | Works Without Setup |
|---------|-------------------|-------------------|
| Documentation Search (Part 1) | None | Yes |
| App Store Connect (Part 2) | App Store Connect API key (.p8) | No |
| iOS App Builder (Part 3) | LLM API key + Xcode | No |

## Setup

### Part 1: Documentation Search (no setup needed)

Works immediately with Node.js:

```bash
node cli.js search "NavigationStack"
```

### Part 2: App Store Connect CLI

Install via Homebrew:

```bash
brew install Abdullah4AI/tap/appledev
```

Authenticate with your App Store Connect API key:

```bash
appledev store auth login --name "MyApp" --key-id "KEY_ID" --issuer-id "ISSUER_ID" --private-key /path/to/AuthKey.p8
```

Or set environment variables:

```bash
export APPSTORE_KEY_ID="your-key-id"
export APPSTORE_ISSUER_ID="your-issuer-id"
export APPSTORE_PRIVATE_KEY_PATH="/path/to/AuthKey.p8"
```

API keys are created at https://appstoreconnect.apple.com/access/integrations/api

### Part 3: iOS App Builder

Prerequisites: Xcode (with iOS Simulator), XcodeGen, and an LLM API key for code generation.

```bash
appledev build setup    # Checks and installs prerequisites
```

### Build from source

```bash
bash scripts/setup.sh
```

## Part 1: Documentation Search

```bash
node cli.js search "NavigationStack"
node cli.js symbols "UIView"
node cli.js doc "/documentation/swiftui/navigationstack"
node cli.js overview "SwiftUI"
node cli.js samples "SwiftUI"
node cli.js wwdc-search "concurrency"
node cli.js wwdc-year 2025
node cli.js wwdc-topic "swiftui-ui-frameworks"
```

## Part 2: App Store Connect

Full reference: [references/app-store-connect.md](references/app-store-connect.md)

| Task | Command |
|------|---------|
| List apps | `appledev store apps` |
| Upload build | `appledev store builds upload --app "APP_ID" --ipa "app.ipa" --wait` |
| Find build by number | `appledev store builds find --app "APP_ID" --build-number "42"` |
| Wait for build processing | `appledev store builds wait --build "BUILD_ID"` |
| Publish TestFlight | `appledev store publish testflight --app "APP_ID" --ipa "app.ipa" --group "Beta" --wait` |
| Submit App Store | `appledev store publish appstore --app "APP_ID" --ipa "app.ipa" --submit --confirm --wait` |
| Pre-submission validation | `appledev store validate --app "APP_ID" --version-id "VERSION_ID"` |
| List certificates | `appledev store certificates list` |
| Reviews | `appledev store reviews --app "APP_ID" --output table` |
| Update localizations | `appledev store localizations update --app "APP_ID" --locale "en-US" --name "My App"` |
| Sales report | `appledev store analytics sales --vendor "VENDOR" --type SALES --subtype SUMMARY --frequency DAILY --date "2024-01-20"` |
| Xcode Cloud | `appledev store xcode-cloud run --app "APP_ID" --workflow "CI" --branch "main" --wait` |
| Notarize | `appledev store notarization submit --file ./MyApp.zip --wait` |
| Status dashboard | `appledev store status --app "APP_ID" --output table` |
| Weekly insights | `appledev store insights weekly --app "APP_ID" --source analytics` |
| Metadata pull | `appledev store metadata pull --app "APP_ID" --version "1.2.3" --dir ./metadata` |
| Release notes | `appledev store release-notes generate --since-tag "v1.2.2"` |
| Diff localizations | `appledev store diff localizations --app "APP_ID" --path ./metadata` |
| Nominations | `appledev store nominations create --app "APP_ID" --name "Launch"` |
| Price point filter | `appledev store pricing price-points --app "APP_ID" --price 0.99` |
| IAP (family sharable) | `appledev store iap create --app "APP_ID" --family-sharable` |
| Subscription (family sharable) | `appledev store subscriptions create --app "APP_ID" --family-sharable` |

### Environment Variables

All environment variables are optional. They override flags when set.

| Variable | Description |
|----------|-------------|
| `APPSTORE_KEY_ID` | API Key ID |
| `APPSTORE_ISSUER_ID` | API Issuer ID |
| `APPSTORE_PRIVATE_KEY_PATH` | Path to .p8 key file |
| `APPSTORE_PRIVATE_KEY` | Raw private key string |
| `APPSTORE_PRIVATE_KEY_B64` | Base64-encoded private key |
| `APPSTORE_APP_ID` | Default app ID |
| `APPSTORE_PROFILE` | Default auth profile |
| `APPSTORE_DEBUG` | Enable debug output |
| `APPSTORE_TIMEOUT` | Request timeout |
| `APPSTORE_BYPASS_KEYCHAIN` | Skip system keychain |

## Part 3: Multi-Platform App Builder

Supports iOS, watchOS, tvOS, and iPad. Generates complete Swift/SwiftUI apps from natural language with AI-powered code generation.

```bash
appledev build                     # Interactive mode
appledev build setup               # Install prerequisites (Xcode, XcodeGen, AI backend)
appledev build fix                 # Auto-fix build errors
appledev build run                 # Build and launch in simulator
appledev build open                # Open project in Xcode
appledev build chat                # Interactive chat mode (edit/ask questions)
appledev build info                # Show project status
appledev build usage               # Token usage and cost
```

### Supported Platforms

| Platform | Status |
|----------|--------|
| iOS | Full support |
| iPad | Full support |
| macOS | Supported |
| watchOS | Supported |
| tvOS | Supported |
| visionOS | Supported |

### How it works

```
describe > analyze > plan > build > fix > run
```

1. **Analyze** - Extracts app name, features, core flow, target platform from description
2. **Plan** - Produces file-level build plan: data models, navigation, design
3. **Build** - Generates Swift source files, project.yml, asset catalog
4. **Fix** - Compiles and auto-repairs until build succeeds
5. **Run** - Boots Simulator and launches the app

### Interactive commands

| Command | Description |
|---------|-------------|
| `/run` | Build and launch in simulator |
| `/fix` | Auto-fix compilation errors |
| `/open` | Open project in Xcode |
| `/ask [question]` | Ask a question about the project |
| `/model [name]` | Switch model (sonnet, opus, haiku) |
| `/info` | Show project info |
| `/usage` | Token usage and cost |

## References

| Reference | Content |
|-----------|---------|
| [references/app-store-connect.md](references/app-store-connect.md) | Complete App Store Connect CLI commands |
| [references/ios-rules/](references/ios-rules/) | 38 iOS development rules |
| [references/swiftui-guides/](references/swiftui-guides/) | 12 SwiftUI best practice guides |
| [references/ios-app-builder-prompts.md](references/ios-app-builder-prompts.md) | System prompts for app building |

### iOS Rules (38 files)

accessibility, app_clips, app_review, apple_translation, biometrics, camera, charts, color_contrast, components, dark_mode, design-system, feedback_states, file-structure, forbidden-patterns, foundation_models, gestures, haptics, healthkit, live_activities, localization, maps, mvvm-architecture, navigation-patterns, notification_service, notifications, safari_extension, share_extension, siri_intents, spacing_layout, speech, storage-patterns, swift-conventions, timers, typography, view-composition, view_complexity, website_links, widgets

### SwiftUI Guides (12 files)

animations, forms-and-input, layout, liquid-glass, list-patterns, media, modern-apis, navigation, performance, scroll-patterns, state-management, text-formatting
