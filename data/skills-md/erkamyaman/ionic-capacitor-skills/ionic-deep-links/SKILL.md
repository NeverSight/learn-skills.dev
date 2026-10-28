---
name: ionic-deep-links
description: Handle deep links in an Ionic Capacitor app — custom URL schemes (myapp://), iOS Universal Links, and Android App Links. Trigger when adding password-reset links, share-to-app URLs, OAuth callbacks, magic-link sign-in, or branded https:// links that open the app instead of the browser.
license: MIT
metadata:
  author: erkamyaman
  version: '1.0'
---

# Deep Links (URL schemes + Universal Links + App Links)

Three flavors of deep linking that you'll likely need together:

| Type | Looks like | Verified by | Use when |
|------|-----------|-------------|----------|
| Custom scheme | `myapp://reset-password?token=…` | Nothing | Internal flows, OAuth callbacks. Easy. Anyone can register the scheme. |
| iOS Universal Link | `https://yourapp.com/reset-password?token=…` | `apple-app-site-association` file on your domain | Branded links that should open the app or fall back to the web. |
| Android App Link | `https://yourapp.com/reset-password?token=…` | `assetlinks.json` on your domain | Same goal as Universal Links, on Android. |

You usually want **all three** for a polished app: one URL works on iOS and Android (Universal/App), with custom schemes as a fallback for cases where verified linking isn't possible.

## When to consult

- **Custom URL scheme + `@capacitor/app` listener**: [custom-scheme.md](references/custom-scheme.md)
- **iOS Universal Links** (entitlement + AASA file): [ios-universal-links.md](references/ios-universal-links.md)
- **Android App Links** (intent filters + assetlinks.json): [android-app-links.md](references/android-app-links.md)
- **Routing the link to a page**: [routing.md](references/routing.md)

## Canonical URL shape

Pick one path prefix per concern and use it consistently across custom schemes, Universal Links, and App Links so the same router code handles all three:

| Concern              | Custom scheme                                | Universal/App Link                       |
|----------------------|----------------------------------------------|------------------------------------------|
| Auth (reset / OAuth callback / magic link) | `myapp://auth/<flow>?...`     | `https://yourapp.com/auth/<flow>?...`    |
| Invites              | `myapp://invite/<code>`                      | `https://yourapp.com/invite/<code>`      |
| Share                | `myapp://share/<id>`                         | `https://yourapp.com/share/<id>`         |

The auth path is shared across `ionic-firebase`, `ionic-supabase`, and password-reset / OAuth-callback flows in this scaffold:

- Magic link: `https://yourapp.com/auth/finish-signin?...`
- Password reset: `myapp://auth/reset-password?token=...`
- OAuth callback (Supabase): `myapp://auth/callback#access_token=...`

Routing logic in the deep-link handler matches on `pathname.startsWith('/auth/')` and delegates to the right flow.

## Hard rules

- ✅ Use `@capacitor/app`'s `appUrlOpen` listener — it fires for all three flavors uniformly.
- ✅ Host the AASA / `assetlinks.json` files at your domain root with the right `Content-Type` (`application/json`, no extension).
- ✅ Test with `xcrun simctl openurl` (iOS sim) and `adb shell am start -a android.intent.action.VIEW -d "<url>"` (Android emulator).
- ❌ Don't rely on custom schemes alone for password reset / OAuth — modern OS versions and email clients increasingly suppress them.
- ❌ Don't forget to call `App.getLaunchUrl()` on cold-start — `appUrlOpen` may not fire reliably for cold opens (it does in many Capacitor versions, but the behavior is platform- and version-dependent). Belt-and-suspenders: always check `getLaunchUrl()` once at boot.

## Library

```bash
npm install @capacitor/app
npx cap sync
```
