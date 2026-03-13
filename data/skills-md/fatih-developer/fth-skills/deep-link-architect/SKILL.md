---
name: deep-link-architect
description: Design and implement Universal Links (iOS) and App Links (Android) architectures. Plan URL schemas, manifest/entitlement configurations, domain validation, fallback strategies, and test scenarios.
---

# Deep Link Architect Protocol

Deep linking is notoriously fragile. A missing trailing slash, a cached `apple-app-site-association` file, or a misconfigured Intent Filter can break user flows. This skill treats deep linking as a cross-platform architectural feature, not just a couple of configuration files.

**Core principle:** A deep link must always resolve gracefully, whether the user has the app installed or not, and regardless of the platform.

---

## Workflow

```
1. Define the routing schema (Domain, Paths, Parameters)
2. Architect iOS Universal Links (`apple-app-site-association`, Entitlements)
3. Architect Android App Links (`assetlinks.json`, Intent Filters)
4. Design the Fallback Strategy (App not installed / Desktop)
5. Generate a testing checklist
```

---

## Step 1: Schema Definition
Define exactly what the URLs will look like.
- **Base Domain:** e.g., `app.example.com`
- **Paths:** e.g., `/user/:id`, `/post/:id`
- **Avoid Custom Schemes:** (e.g., `myapp://`) unless strictly for local internal app routing or legacy support, as they prompt annoying security dialogs and fail gracefully. Default to `https://`.

## Step 2: iOS Universal Links
Provide the exact configuration needed for iOS:
- The content of the `apple-app-site-association` (AASA) file.
- Instructions on where to host it (`/.well-known/`).
- The necessary additions to the Xcode `Entitlements` file (`applinks:app.example.com`).
- *Note:* Remind the developer that the AASA file must NOT have a `.json` extension.

## Step 3: Android App Links
Provide the exact configuration needed for Android:
- The content of the `assetlinks.json` file.
- Instructions on where to host it (`/.well-known/`).
- The specific `<intent-filter>` blocks required in the `AndroidManifest.xml` (must include `android:autoVerify="true"`).

## Step 4: Fallback & Web Strategy
What happens if the app isn't installed?
- Standard deep links just fail. Universal/App links fallback to the website.
- Suggest a strategy: Does the mobile website show a "Smart App Banner" to download the app? Does it redirect to the App Store/Play Store directly using Firebase Dynamic Links (deprecated) or a service like Branch.io/Adjust?

## Step 5: In-App Routing
How is the incoming URL handled inside the app code?
- Native: `scene(_:continue:)` (iOS) / `onNewIntent` (Android).
- Cross-platform: Expo Router, React Navigation Deep Linking config, or Flutter `GoRouter`.

---

## Output Format

```markdown
# 🔗 Deep Link Architecture Plan

**Domain:** `https://[YourDomain]`
**Routing Paths:** [List of paths handled by the app]

## 🍎 iOS Universal Links

### 1. Hosted File (`apple-app-site-association`)
```json
// Exact JSON required
```
*Host this at: `https://[YourDomain]/.well-known/apple-app-site-association` (No .json extension)*

### 2. Xcode Entitlements
- Add: `applinks:[YourDomain]`

## 🤖 Android App Links

### 1. Hosted File (`assetlinks.json`)
```json
// Exact JSON required. Recommend generating via Android Studio or Play Console.
```
*Host this at: `https://[YourDomain]/.well-known/assetlinks.json`*

### 2. Android Manifest (`AndroidManifest.xml`)
```xml
// Intent filter snippet with autoVerify="true"
```

## 🔄 In-App Routing Strategy
[Code snippet or configuration for React Navigation / Flutter / Native to catch the URL and route to the correct screen].

## 🛡 Fallback & Edge Cases
- **If app is not installed:** [What happens on the web URL?]
- **Testing steps:** [Exactly how to test using `xcrun simctl` and `adb shell am start`]
```

---

## When to Skip
- The user is asking about network API routing (backend router).
- The user is asking about web-only routing (e.g., Next.js App Router).

---

## Guardrails
- **No Third-Party by Default:** Do not immediately suggest Branch or AppsFlyer unless the user explicitly needs deferred deep linking (install attribution) or complex marketing links. Stick to native Universal/App Links first.
- **AASA Caching:** Always warn iOS developers that Apple's CDN caches the AASA file for 24-48 hours. Provide the bypass query param for testing (`?mode=developer`).

---

## References
See `references/EXAMPLES.md` for a worked case.
