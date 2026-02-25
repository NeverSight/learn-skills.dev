---
name: maui-authentication
description: A brief description of what this skill does
---

# .NET MAUI — Authentication Skill

## Purpose

This skill provides agents with secure, cross-platform patterns for implementing authentication in .NET MAUI applications. It covers OAuth2, OpenID Connect, JWT handling, secure storage, token refresh, and platform-specific login flows using WebAuthenticator.

The goal is to ensure that all authentication-related code is safe, maintainable, and aligned with modern security practices.

## Core Principles

1. **Security first**
   Never store sensitive data in Preferences or plain text. Always use SecureStorage.
2. **Use platform-native authentication flows**
   - iOS/macOS: ASWebAuthenticationSession
   - Android: Chrome Custom Tabs
   - Windows: System browser
3. **Token lifecycle management**
   Always implement refresh token logic and expiration checks.
4. **Abstraction**
   Wrap authentication logic in services and interfaces to keep UI clean.
5. **Least privilege**
   Request only the scopes required for the app.

## Supported Authentication Patterns

- OAuth2 Authorization Code Flow (recommended)
- OpenID Connect (OIDC)
- JWT-based APIs
- Custom backend authentication
- Social logins (Google, Microsoft, Apple)

## Recommended Architecture

```code
Services
└─ Auth
   ├─ Interfaces
   └─ Models
```

## Agent Usage Guidelines

- When generating authentication code, always:
  - Use `WebAuthenticator.Default.AuthenticateAsync` for login.
  - Store tokens in SecureStorage.
  - Implement `IAuthService` and `AuthService`.
  - Provide `IsLoggedIn`, `LoginAsync`, `LogoutAsync`, and `RefreshTokenAsync`.
- When asked to “add login,” generate:
  - A LoginPage + LoginViewModel
  - AuthService + interface
  - Token models
  - SecureStorage helpers
- When asked to “secure an API call,” apply:
  - Bearer token injection
  - Expiration checks
  - Automatic refresh

## Out of Scope

- UI styling (covered in `maui-ui-best-practices`)
- Backend implementation details
- Deployment configuration
