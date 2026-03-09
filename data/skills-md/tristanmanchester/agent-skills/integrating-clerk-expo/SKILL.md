---
name: integrating-clerk-expo
description: >-
  Integrates Clerk authentication into React Native Expo apps using @clerk/clerk-expo.
  Covers ClerkProvider setup, secure token caching (expo-secure-store), Expo Router/React Navigation auth guards,
  custom sign-in/sign-up flows (email/password + email codes), SSO/OAuth (useSSO), Sign in with Apple (useSignInWithApple),
  biometrics (useLocalCredentials), offline support, and production deployment allowlisting.
  Use when the user mentions Clerk + Expo, @clerk/clerk-expo, Expo Router auth, SSO/OAuth redirects, or deploying Clerk in a mobile app.
allowed-tools: Read,Write,Bash(git:*),Bash(node:*),Bash(npm:*),Bash(pnpm:*),Bash(yarn:*),Bash(bun:*),Bash(npx:*),Bash(expo:*),Bash(eas:*),Bash(python:*)
---

# Clerk authentication in Expo (React Native)

## Key constraints (read first)

- **Expo native apps do not support Clerk email links**. Prefer **email verification codes** (`email_code`) or other strategies.
- **Clerk prebuilt UI components are not supported on Expo native**. Use **custom flows** (your own screens) plus the **control components**:
  `<ClerkLoaded>`, `<ClerkLoading>`, `<SignedIn>`, `<SignedOut>`, `<Protect>`.
- Default session tokens are in-memory; for native apps you almost always want a **secure token cache** (Expo SecureStore).

## What this skill does

When implementing Clerk in an Expo app, follow these workflows to:
- Install and configure `@clerk/clerk-expo` and environment keys
- Wrap the app in `<ClerkProvider>` with a secure `tokenCache`
- Build custom sign-in/sign-up screens (email + password, email codes)
- Protect routes/screens in **Expo Router** or **React Navigation**
- Add OAuth / Enterprise SSO flows via `useSSO()` (and fix redirect/deeplink pitfalls)
- Add native **Sign in with Apple** (iOS, native build) via `useSignInWithApple()`
- Add optional biometric re-auth via `useLocalCredentials()`
- Optionally enable experimental offline bootstrapping via `__experimental_resourceCache`
- Prepare for production deployment (domain + allowlisted redirect URLs)

## Fast checklist (default: Expo Router)

Copy/paste and tick off:

- [ ] In Clerk Dashboard, **enable Native API** for the application.
- [ ] Install: `@clerk/clerk-expo`
- [ ] Add `.env`: `EXPO_PUBLIC_CLERK_PUBLISHABLE_KEY=...`
- [ ] Wrap the root with `<ClerkProvider tokenCache={tokenCache}>`
- [ ] Install SecureStore and use Clerk’s `tokenCache` helper
- [ ] Create `(auth)` route group with `sign-in.tsx`, `sign-up.tsx`, and an `(auth)/_layout.tsx` redirect guard
- [ ] Add a sign-out button using `useClerk().signOut()`
- [ ] Protect signed-in content using `<SignedIn>` / `<SignedOut>` / `<Protect>` or `useAuth()` + redirects
- [ ] If using OAuth/SSO: implement `useSSO()` + `expo-auth-session` redirect URL + `WebBrowser.maybeCompleteAuthSession()`
- [ ] If iOS Apple sign-in is required: native build + `useSignInWithApple()`
- [ ] If you need resilience offline: `__experimental_resourceCache={resourceCache}` and handle `network_error`
- [ ] Production: acquire a domain and allowlist mobile SSO redirect URLs

If you need full code examples, open:
- [`references/QUICKSTART.md`](references/QUICKSTART.md)
- [`references/CUSTOM_FLOWS.md`](references/CUSTOM_FLOWS.md)
- [`references/SSO_OAUTH.md`](references/SSO_OAUTH.md)
- [`references/HOOKS_AND_COMPONENTS.md`](references/HOOKS_AND_COMPONENTS.md)

---

## Decide the routing setup

### If the project uses Expo Router
Signals:
- `expo-router` dependency
- an `app/` directory with route files like `app/_layout.tsx`

➡️ Follow: **Expo Router workflow** (below).

### If the project uses React Navigation directly (no Expo Router)
Signals:
- `App.tsx` with `NavigationContainer` and stacks
- no `app/` directory

➡️ Follow: **React Navigation workflow** (below).

---

## Workflow A — Expo Router (recommended default)

### 1) Install + env key

- Install `@clerk/clerk-expo`
- Set `EXPO_PUBLIC_CLERK_PUBLISHABLE_KEY` in `.env`

### 2) Root layout: ClerkProvider + secure token cache

In `app/_layout.tsx` (or the project’s root layout), wrap your app:

```tsx
import { ClerkProvider } from '@clerk/clerk-expo'
import { tokenCache } from '@clerk/clerk-expo/token-cache'
import { Slot } from 'expo-router'

export default function RootLayout() {
  return (
    <ClerkProvider tokenCache={tokenCache}>
      <Slot />
    </ClerkProvider>
  )
}
```

Notes:
- Ensure `expo-secure-store` is installed (required by the `tokenCache` helper).
- Keep *only* the **publishable** key in the client.

### 3) Auth route group + redirect guard

Create `app/(auth)/_layout.tsx` that redirects signed-in users away from auth screens:

```tsx
import { Redirect, Stack } from 'expo-router'
import { useAuth } from '@clerk/clerk-expo'

export default function AuthLayout() {
  const { isSignedIn } = useAuth()
  if (isSignedIn) return <Redirect href="/" />
  return <Stack />
}
```

### 4) Build custom sign-in / sign-up screens

Use Clerk hooks (`useSignIn`, `useSignUp`) and prefer `email_code` verification.

See:
- [`references/CUSTOM_FLOWS.md`](references/CUSTOM_FLOWS.md)

### 5) Protect signed-in routes

Options (pick one, don’t mix randomly):

- **Declarative**: Wrap signed-in areas with `<SignedIn>` and `<SignedOut>`.
- **Gate a subtree**: Use `<Protect>` around content that requires auth.
- **Imperative**: In a layout, check `useAuth()` and `<Redirect>` to `/sign-in`.

See:
- [`references/ROUTING.md`](references/ROUTING.md)

---

## Workflow B — React Navigation (no Expo Router)

### 1) Wrap the root

Wrap your `NavigationContainer` (or your app root) with `<ClerkProvider tokenCache={tokenCache}>`.

### 2) Split navigation by auth state

- While `!isLoaded`: render a splash/loading screen
- When `isSignedIn`: render your “app” stack
- Else: render your “auth” stack

See:
- [`references/ROUTING.md`](references/ROUTING.md)

---

## OAuth / Enterprise SSO in Expo (useSSO)

Use `useSSO()` for OAuth + enterprise SSO. In native, you must provide a valid **redirect URL** (often via `AuthSession.makeRedirectUri(...)`) and ensure your **redirect URLs are allowlisted** for production.

See:
- [`references/SSO_OAUTH.md`](references/SSO_OAUTH.md)
- [`references/DEPLOYMENT.md`](references/DEPLOYMENT.md)

---

## Sign in with Apple (iOS native build)

`useSignInWithApple()` is iOS-only and requires a **native build** (won’t work in Expo Go).
Always handle `ERR_REQUEST_CANCELED`.

See:
- [`references/APPLE_SIGNIN.md`](references/APPLE_SIGNIN.md)

---

## Biometrics (store local credentials)

`useLocalCredentials()` can store password credentials on-device and allow biometric sign-in later (Face ID / fingerprint). Only works for **password-based** sign-in attempts.

See:
- [`references/BIOMETRICS.md`](references/BIOMETRICS.md)


## Passkeys

Clerk supports passkeys (WebAuthn). In Expo apps, you’ll integrate passkeys through custom flows; follow Clerk’s passkeys reference for the latest supported strategies and platform constraints.

See:
- [`references/PASSKEYS.md`](references/PASSKEYS.md)
---

## Offline support (experimental)

You can enable experimental offline bootstrapping via `__experimental_resourceCache`. Treat as experimental; add good error handling for `network_error`.

See:
- [`references/OFFLINE_SUPPORT.md`](references/OFFLINE_SUPPORT.md)

---

## Validation loop (recommended)

1) Run the setup verifier:

```bash
python scripts/verify_expo_clerk_setup.py .
```

2) Start Expo with a clean cache:

```bash
npx expo start -c
```

3) Test flows:
- fresh install → sign up → verify code → app screen
- app restart → user still signed in (token cache working)
- sign out → user returns to auth stack (token cleared)

---

## THE EXACT PROMPT — Implement Clerk in an Expo app

Use this when delegating to another coding agent:

```
You are implementing Clerk authentication in a React Native Expo app.

1) Detect whether this app uses Expo Router (app/ directory) or React Navigation.
2) Install and configure @clerk/clerk-expo with EXPO_PUBLIC_CLERK_PUBLISHABLE_KEY.
3) Wrap the root with <ClerkProvider tokenCache={tokenCache}> and ensure expo-secure-store is installed.
4) Implement custom sign-in and sign-up screens (email + password, with email verification code strategy 'email_code').
5) Protect signed-in routes appropriately for the chosen router.
6) If OAuth/SSO is requested, implement useSSO() with expo-auth-session redirectUrl and WebBrowser.maybeCompleteAuthSession().
7) Add sign-out.
8) Provide a short test plan and run scripts/verify_expo_clerk_setup.py.

Be precise and keep changes minimal. Do not use email link flows on native.
```

---

## Quick search (when reading bundled references)

```bash
grep -Rni "useSSO" references/
grep -Rni "tokenCache" references/
grep -Rni "enterprise_sso" references/
grep -Rni "__experimental_resourceCache" references/
```
