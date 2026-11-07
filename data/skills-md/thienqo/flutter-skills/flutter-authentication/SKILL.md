---
name: flutter-authentication
description: Implement, repair, or review Flutter user authentication and session lifecycle, including OAuth or OIDC redirects, PKCE, token refresh, logout, account switching, passkeys, and device re-authentication. Use when sign-in identity or session behavior is the task; route broad threat audits to flutter-security and request transport to flutter-networking.
---

# Flutter Authentication

Treat authentication as a protocol and account-state lifecycle spanning the identity provider, trusted backend, platform redirect surface, local session owner, and application UI. Preserve the project's provider, backend, SDK, router, storage, and state management unless migration is requested.

Do not add an SDK, client registration, redirect association, secret placeholder, account, or backend merely because the skill is selected.

## Preflight

Read `pubspec.yaml`, SDK constraints, sign-in entrypoints, provider and backend contract, registered clients and redirects, deep-link handling, token and account storage, refresh coordination, navigation guards, logout behavior, flavors, platform associations, and tests. Distinguish authentication, session state, authorization, and device-local re-authentication.

Native and web Flutter clients are public clients and cannot keep a reusable client secret. For OAuth or OIDC, use the established authorization-code flow with PKCE and an external user-agent where the provider supports it. Validate redirect ownership and correlate the response using state and, for OIDC, nonce as applicable. Never trust a redirect merely because its scheme matches.

## Load references conditionally

- Read [OAuth, OIDC, and redirects](references/oauth-oidc-and-redirects.md) for browser authorization, PKCE, state, nonce, callback ownership, deep links, and provider errors.
- Read [sessions and account state](references/sessions-and-account-state.md) for token ownership, coordinated refresh, expiry, logout, revocation, account switching, startup restoration, and offline behavior.
- Read [passkeys and device re-authentication](references/passkeys-and-device-reauthentication.md) for relying-party challenges, platform associations, passkey lifecycle, biometrics, and local authorization gates.

## Boundaries

- `flutter-security` owns threat modeling and broad hardening; this skill implements correct identity and session behavior.
- `flutter-networking` owns HTTP mechanics, interceptors, and generic retry; this skill defines authentication refresh and account semantics.
- `flutter-navigation` owns route and back-stack correctness; this skill defines authenticated, unauthenticated, callback, and re-authentication states.
- `flutter-persistence` owns storage mechanics; this skill defines credential sensitivity, account isolation, expiry, and deletion lifecycle.
- `flutter-platform-integration` owns custom native credential APIs or redirect mechanics when an existing plugin cannot satisfy them.

## Verification

Use a fake identity adapter for deterministic state transitions and an authorized non-production provider for end-to-end proof. Cover success, cancellation, denial, malformed or replayed callback, state and nonce mismatch, expired access token, concurrent refresh, refresh failure, revoked session, offline startup, logout, account switch, process restart, and platform link ownership.

For passkeys or device credentials, exercise real supported devices and cancellation or lockout behavior. State which provider, client type, platform, account state, redirect, storage, and backend checks were actually observed. A successful login screen or locally decoded token does not prove callback integrity, server authorization, refresh safety, revocation, or logout cleanup.

## Sources

- [OAuth 2.0 for Native Apps](https://www.rfc-editor.org/rfc/rfc8252)
- [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html)
- [Android passkeys](https://developer.android.com/identity/passkeys)
- [Apple Authentication Services](https://developer.apple.com/documentation/authenticationservices)
