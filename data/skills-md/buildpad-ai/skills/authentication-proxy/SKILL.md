---
name: authentication-proxy
description: Authentication proxy pattern reference. All browser-to-backend communication MUST go through Next.js API proxy routes. Never call Supabase auth or DaaS backend directly from client components. Automatically loaded as background context.
user-invokable: false
---

# Authentication Proxy Pattern

## CRITICAL RULE

```
❌ Browser → DaaS Backend directly       (CORS error on a Supabase project; no cookie session on an Engine project)
❌ Browser → supabase.auth.signIn()      (session cookie not set for proxy)
✅ Browser → /api/auth/login → Supabase  (same-origin, no CORS; on an Engine project the Supabase client signs in at the Engine)
✅ Browser → /api/items/* → DaaS Backend (proxied server-side, to NEXT_PUBLIC_BUILDPAD_DAAS_URL)
```

The rule holds for both kinds of project. On a Supabase project the data backend is the DaaS application and sign-in goes to Supabase Auth. On an Engine project the data API's address is the Engine_URL, which both `NEXT_PUBLIC_BUILDPAD_DAAS_URL` and `NEXT_PUBLIC_SUPABASE_URL` hold. The Studio's address is an administration interface: send no data call to it. On an Engine project the data API serves no request without a session; only the sign-in, `GET /api/server/info` and the Engine's password routes are served without one (an application must not use them: on an Engine project an administrator resets a user's password). The requests that take their tenant from the header `X-Tenant-Id` are the password sign-in, XAppHub sign-in and anonymous reads of public files. A browser can send `X-Tenant-Id` to the Engine from another origin, without cookies or credentials: the Engine allows that header from any origin and allows no credentialed cross-origin request. Even so, the request that names the tenant is the sign-in made through the application's own server route, which sends `X-Tenant-Id` with the value of `NEXT_PUBLIC_BUILDPAD_TENANT_ID`. A public file shown in a browser is loaded through a signed URL from `/api/files/signed-url`, not by an anonymous read. A request without a session that names no tenant is served from the Engine's host plane, not from the project. A request with a session takes its tenant from the session.

## Auth Routes

| Action         | Route                        | Method                                         |
| -------------- | ---------------------------- | ---------------------------------------------- |
| Login          | `/api/auth/login`            | POST `{ email, password }`                     |
| Logout         | `/api/auth/logout`           | POST                                           |
| Get user       | `/api/auth/user`             | GET                                            |
| OAuth callback | `/api/auth/callback`         | GET (handles both Supabase and external OAuth on a Supabase project; XAppHub sign-in only on an Engine project) |
| External OAuth | `/api/auth/oauth/[provider]` | GET (initiates external SSO; on an Engine project the provider `my-apps` only) |

These routes are installed by the CLI (`pnpm cli add --all` or `--with-api`). On an Engine project the login, logout and get-user routes are used, and the OAuth callback and provider routes only as the CLI's `external-oauth-engine` module writes them, for XAppHub sign-in: those of the `external-oauth` module cannot be used there.

On an Engine project the Supabase client is kept for sign-in only. Password sign-in, session refresh, reading the signed-in user and sign-out work through it, and its default sign-out ends the user's sessions on every device. An account that holds no role in the project's tenant is refused at password sign-in. XAppHub sign-in also works through it while the project's XAppHub connector is connected: the application's server gives the ID token from XAppHub to `signInWithIdToken` with the provider `my-apps`, and ends the session of an account that holds no role yet (the `add-external-oauth` skill). Not available on an Engine project: sign-up; OAuth sign-in with any provider other than XAppHub; magic link and one-time code; password recovery; changing a password, an email or a profile through the Supabase client; the Supabase client's code exchange; and the Supabase administration API. The Platform's password-less handoff opens the Studio; it is not a way for an application to sign a user in.

On an Engine project multi-factor enrolment, challenge and verification are not served through the Supabase client. The Engine's own routes, each called with the user's session, are `POST /api/auth/mfa/enroll`, `GET /api/auth/mfa/factors`, `POST /api/auth/mfa/verify` and `POST /api/auth/mfa/unenroll`; a session that still needs its second factor is accepted elsewhere only after `POST /api/auth/mfa/verify`.

## Login Pattern

```tsx
// ✅ CORRECT: Via proxy route
const response = await fetch("/api/auth/login", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ email, password }),
  credentials: "include",
});

// ❌ WRONG: Direct Supabase client
const supabase = createClient();
await supabase.auth.signInWithPassword({ email, password });
```

## Logout Pattern

```tsx
// ✅ CORRECT — clears both the Supabase session AND the scope cookie
await fetch("/api/auth/logout", { method: "POST", credentials: "include" });
router.push("/login");
router.refresh();
```

> **Bug 20:** The logout route **must** clear the `daas_resource_uri` cookie. This cookie persists after logout and contains the previous user’s scope URI. When the next user logs in, the stale URI is forwarded as `X-Resource-Uri`, causing an immediate 403 FORBIDDEN_SCOPE.
>
> In `app/api/auth/logout/route.ts`, inside `performLogout`, always add:
> ```ts
> cookieStore.delete('daas_resource_uri');
> ```

Additionally, `ScopeContext` should validate the cookie against the user’s actual available scopes after loading — if the stored URI is not in the user’s list, clear it (defensive second layer).

## Data API Pattern

```tsx
// ✅ CORRECT: Through proxy route
const res = await fetch("/api/items/todos?filter[status][_eq]=active");

// ❌ WRONG: Direct to DaaS backend from browser
// (localhost:3000 is a local DaaS backend; a local Engine answers on localhost:8080)
const res = await fetch("http://localhost:3000/api/items/todos");
```

Buildpad UI components may call the data API directly through `DaaSProvider`, which sends the signed-in user's token; hand-written fetches go through a proxy route.

## Server-Side Auth Headers

In API routes, use the auth-headers helper to forward the user's JWT. `DAAS_URL` is the address in `NEXT_PUBLIC_BUILDPAD_DAAS_URL`: the DaaS backend on a Supabase project, the Engine_URL on an Engine project.

```tsx
import { getAuthHeaders } from "@/lib/api/auth-headers";

export async function GET(request: Request) {
  const headers = await getAuthHeaders();
  const response = await fetch(`${DAAS_URL}/api/items/todos`, { headers });
  return Response.json(await response.json());
}
```

On an Engine project every data call carries the signed-in user's access token as `Authorization: Bearer <access token>`, from the application's own server route or from the SDK. The Engine accepts no cookie session on its data API. The token in the project's MCP configuration is accepted only on the MCP endpoint `/api/mcp`: never send it, or any other administrator token, to the data API.

## External OAuth (SSO)

This section is for a Supabase project only. On an Engine project only XAppHub sign-in is available, while the project's XAppHub connector is connected: the application's server signs in to the Engine with `signInWithIdToken` (provider `my-apps`), through the CLI's `external-oauth-engine` module, as [add-external-oauth](../add-external-oauth/SKILL.md) says. Sign-in with any other provider is not available there: tell the developer so and stop, and build no substitute.

For external identity providers (Azure AD, Okta, Auth0, Google, custom OIDC), on a Supabase project:

```tsx
// ✅ CORRECT: Via OAuth initiation route
const handleSSOLogin = () => {
  window.location.href = "/api/auth/oauth/generic";
  // Or with return URL:
  window.location.href = "/api/auth/oauth/azure?returnTo=/dashboard";
};

// ❌ WRONG: Supabase's signInWithOAuth (not configured for self-hosted)
await supabase.auth.signInWithOAuth({ provider: "azure" });
```

See [add-external-oauth](../add-external-oauth/SKILL.md) for full implementation details (on an Engine project that skill adds XAppHub sign-in only).

Key points:

- Next.js acts as OAuth client (not Supabase)
- Session set via `supabase.auth.setSession()` (not manual cookies)
- Claims extracted from access_token, id_token, AND userinfo endpoint

## References

- [Authentication proxy details](references/authentication-proxy.instructions.md)
- [External OAuth implementation](../add-external-oauth/SKILL.md) (on an Engine project, XAppHub sign-in only)
