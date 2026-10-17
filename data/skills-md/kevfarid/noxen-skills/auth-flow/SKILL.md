---
name: auth-flow
description: >
  Use when designing or reviewing a login/authentication flow — passwordless
  or OTP verification, where the session token is stored, or why a user
  appears logged out after a refresh or on the server. Trigger on tasks like
  "add OTP login", "where should the session token live", "user gets logged
  out on reload", or "read the logged-in user in a server-rendered page". If
  the project runs on Next.js App Router, also load `nextjs/app-router` for
  the `next/headers` specifics. For the interceptor that attaches the token
  to requests, see the sibling `http-layer` skill. Do NOT trigger for generic
  form-building — see `react-patterns`.
metadata:
  version: 1.0
  collection: noxen
---

# Noxen — Auth Flow

Part of the **Noxen** skill set (a personal engineering standard for React +
TypeScript + Tailwind). This skill covers the login/session flow only — for
attaching the token to outgoing requests see `http-layer`.

## Flow: Login → Verify → Session

```
1. User submits email or phone     → validated with Zod, POSTed to the backend
2. Backend sends an OTP            → UI opens a verification step (modal or route)
3. User submits the OTP            → backend returns { user, token } on success
4. Client stores the session:
     - token   → cookie (persists across reload/SSR)
     - user    → in-memory auth context (fast, but lost on reload)
5. Redirect to the post-login destination
```

```ts
verifyEmail(email, otp).then(({ user, token }) => {
  login(user);                          // in-memory context
  setCookie(SESSION_TOKEN_KEY, token);  // the actual source of truth
  redirect(POST_LOGIN_ROUTE);
});
```

## Two Places Hold Auth State — Only One Is Truth

The in-memory context is convenient (no cookie parsing to read `user.name`
in a component) but disappears on every full page load. The cookie is the
persistent source of truth. Reconcile them by re-hydrating the context from
the cookie on every page load, rather than trusting the context alone:

```ts
// a root layout / entry point, run before the tree renders
const user = await getSessionUser(); // reads the cookie, calls /users/me
<AuthProvider initialUser={user}>{children}</AuthProvider>
```

If reading the session fails (missing or expired token), treat that as an
implicit logout rather than an error to recover from — clear the cookie and
redirect to the login route. Don't let a stale invalid token linger.

## Client vs. Server Token Source

Whichever environment reads the token to attach it to requests needs its own
implementation if it can't share a cookie API — e.g. browser code uses
`document.cookie`, a server-rendered request needs a framework API instead:

```ts
// insert-token.ts (client) — reads document.cookie
export const insertToken = (config) => withAuthHeader(config, getCookie(TOKEN_KEY));

// insert-token-server.ts (server) — reads via the framework's server cookie API
export const insertTokenServer = async (config) =>
  withAuthHeader(config, await getServerCookie(TOKEN_KEY));
```

Both must produce the identical header (`Authorization: Bearer <token>`) —
the only difference is where the token comes from. See `http-layer` for
where these get registered.

## Hard Rules

- The cookie (or equivalent persistent store) is the single source of truth for the token — the in-memory context is a cache of it, never the reverse.
- Re-hydrate the in-memory auth context from the persistent token on every full page load, don't assume it survived.
- A missing or invalid token on session read is an implicit logout, not an error state to display.
- Client and server token readers stay as separate functions — never branch one function on environment.
