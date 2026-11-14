---
name: single-sign-in
description: "Let a user sign in once and be signed in across a whole suite of apps on sibling subdomains: opening a second app needs no second visit to Internet Identity, and signing out of one signs them out of all. Covers the shared record with CookieStateStorage, the /reauth route that silently acquires each app's own credential under transport: 'redirect' and prompt: 'none', the per-origin /.well-known/ii-auth-callbacks document, reading signed-in-elsewhere on load and offering it mid-session, and what ends the session. Use when a suite of apps under one domain should need a single sign-in, when moving between them asks the user to sign in again, or when /reauth bounces in a loop. Every app must already derive from one elected primary origin: load user-sign-in and settle that first. Do NOT use for a single app on one origin, which needs none of this, for apps on unrelated domains, which cannot share a cookie, or for staff signing in with their organization's identity provider (use organization-sign-in)."
license: Apache-2.0
compatibility: "@icp-sdk/auth >= 11.0.0"
metadata:
  title: Single Sign-In
  category: Auth
---

# Single Sign-In

## Prerequisite

Load the `user-sign-in` skill first and settle "Your app's identity is its primary origin". Everything here assumes one elected primary origin whose `ii-alternative-origins` already authorizes every sibling.

That is not a courtesy link. Apps share a sign-in only when they share a principal, and a shared cookie does not produce one. Build this on top of separate principals and every app reads a record naming an account it can never hold, which is the `/reauth` loop in that skill's mistakes list.

## What this gets you

A user of a suite of apps, say `chat.example.com`, `hr.example.com` and `docs.example.com`, signs in once. Every other app in the suite opens already signed in, with no second visit to Internet Identity, and signing out of any one signs them out of all.

Principals are per origin, so every app must derive from **one** primary origin, listed in that origin's `/.well-known/ii-alternative-origins`. Without it each app sees a different user and there is nothing to share.

## 1. Share the record

Every app builds its client with the same derivation origin and the same cookie domain, so a sign-in on one writes a record the others read:

```javascript
import { AuthClient, CookieStateStorage, InteractionRequiredError } from "@icp-sdk/auth/client";

const clientOptions = {
  derivationOrigin: "https://<primary-canister-id>.icp.net",
  stateStorage: new CookieStateStorage({ domain: "example.com" }),
};
```

Choosing that domain means trusting every origin under it. Do not do it on a domain whose subdomains you do not control.

## 2. Acquire the sign-in on a `/reauth` route

An app that reads `signed-in-elsewhere` asks Internet Identity for its own credential for that account. It runs on page load with no user gesture, where a popup is blocked, so it uses `transport: "redirect"` on a route of its own, from a second client (`prompt` and `hint` are fixed when a client is built):

```javascript
// Runs on the /reauth route.
async function reauth() {
  const status = new AuthClient(clientOptions).getStatus();

  if (status.state !== "signed-in-elsewhere") {
    location.replace("/");
    return;
  }

  const authClient = new AuthClient({
    ...clientOptions,
    transport: "redirect",
    prompt: "none",
    hint: status.principal, // answer for the account already signed in
  });

  try {
    await authClient.signIn({
      returnTo: new URLSearchParams(location.search).get("next") ?? "/",
    });
  } catch (error) {
    if (error instanceof InteractionRequiredError) {
      // Nothing to resume, so the shared record is stale: clear it, or every
      // app on the domain keeps sending the user back here.
      await authClient.signOut().catch(() => {});
    }
    location.replace("/");
  }
}

reauth();
```

Without `hint`, a provider holding more than one session refuses rather than guessing: `InteractionRequiredError` with `reason` `account_selection_required`. If what comes back is for a different account than `hint` asked for, the client refuses it and throws `AccountMismatchError`.

## 3. Declare the callback on every app origin

A redirect sign-in is delivered only to a callback the returning origin itself declares, so every app serves `/.well-known/ii-auth-callbacks` on its own origin (not once on the derivation origin), listing its own `/reauth`:

```json
{ "callbacks": ["https://chat.example.com/reauth"] }
```

The entry is matched exactly (the full URL, no fragment), and II reads the document cross-origin. With `@dfinity/static-site`, add a `_headers` block:

```
/.well-known/ii-auth-callbacks
  Content-Type: application/json
  Access-Control-Allow-Origin: *
```

Validation fails closed: undeclared, unreadable, or not exactly matching, and the sign-in never comes back. The route must also terminate locally: the response arrives in the URL fragment, and a `3xx` carrying none re-attaches it to wherever it forwards.

## 4. Pick it up on load, on every page

Every page, not only those requiring a sign-in, reads the status as it loads and hands `signed-in-elsewhere` to `/reauth` with the page to return to:

```javascript
const authClient = new AuthClient(clientOptions);
const status = authClient.getStatus();

// Only this state: signed-out and expired both mean a normal sign-in, and
// sending them to /reauth just bounces the user back.
if (status.state === "signed-in-elsewhere") {
  location.replace(`/reauth?next=${encodeURIComponent(location.pathname + location.search)}`);
}
```

## 5. Jump on load, ask afterwards

Once a page is open, the status of that same client can still turn `signed-in-elsewhere` (someone signs in on a sibling in another tab). Redirecting a page the user is working on throws away their work, so subscribe and offer the same redirect behind a button:

```javascript
authClient.subscribe(() => {
  if (authClient.getStatus().state === "signed-in-elsewhere") {
    showResumeDialog(() =>
      location.replace(`/reauth?next=${encodeURIComponent(location.pathname + location.search)}`),
    );
  }
});
```

## What ends the session

**Every state change travels the same way: through the shared record.** Whatever happens to the session, on this app or a sibling, the record is what carries it, each app's `subscribe()` fires, and `getStatus()` answers the new state. There is no second mechanism and no waiting period to account for, so the three cases below differ in what they mean, not in how they reach the other apps.

- `signOut()` ends the session at Internet Identity, clears this app's credentials, and removes the shared record. Every sibling reads `signed-out`.
- `maxTimeToIdle` on `signIn()` ends the session when nobody uses any of the apps; omitted, Internet Identity applies seven days.
- Signing in to another account on any app replaces the session for the whole suite. The record now names a different account, so a sibling that has no credential for it reads `signed-in-elsewhere` and goes through `/reauth` silently, exactly as on a first sign-in.

### Render from the subscription, not from a value read at load

A tab finds out as soon as its browser can tell it. Reading a cookie raises no event, so where the browser has the Cookie Store API that is immediate, and otherwise it is the next time that page is shown or its window regains focus.

So there is a window where one tab knows and another does not, and it is the ordinary case rather than an edge case:

- The user has `hr.example.com` open in one tab and `chat.example.com` in another.
- They sign out in the HR tab. The shared record is gone immediately.
- The chat tab is in the background and has not been told yet. It is still showing the signed-in screen, with the user's name in the corner and their chats on it.

That tab fixes itself only if it re-reads the state when it hears. So call `getStatus()` inside the `subscribe()` callback and render from that, rather than from a status read once when the page loaded:

```javascript
// Re-read on every change, including a sibling's sign-out.
authClient.subscribe(() => render(authClient.getStatus()));
render(authClient.getStatus()); // and once for the initial paint
```

A page that reads the status only at load keeps showing a signed-in screen to a user who is signed out, until something else happens to reload it.

### Service workers

A service worker reads the single sign-in too (`@icp-sdk/auth` 11.2.0 or later; see "In a web or service worker" in the `user-sign-in` skill). With no page of its own origin open, it sees a sibling subdomain's sign-in or sign-out only once a page of its origin opens.
