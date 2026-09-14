---
name: install-with-ai
description: Installs Userflow.js into new or existing applications. Default install is init() + identify() (after sign-in/sign-up) + reset() only. Use when someone wants to install Userflow, add Userflow.js, or wire Userflow into a codebase. Installation only — verifying an existing install or recommending attributes is out of scope.
metadata:
  author: userflow
  version: "1.1"
---

# Userflow.js Installation

This skill installs Userflow.js correctly and minimally. The install changes which users get identified, which directly affects the customer's Monthly Active User (MAU) count and bill — so follow the core rules below exactly.

**AGENTS.md convention:** For any reference to `agents.md.template`, append a "Userflow installation" section to the project's AGENTS.md recording: install method (npm or script tag), the file where init() lives, the file(s) where identify() and reset() live, the environment-token source, and the user-ID field used.

## Scope

Install only, for a new or existing codebase. The default install is three calls: `init()` once per page load, `identify()` after sign-in/sign-up, and `reset()` on sign-out. Verifying an existing install and recommending which attributes to send are separate capabilities and out of scope here.

## Core Rules (non-negotiable — apply throughout)

1. **Authenticated users only.** Call `identify()` only after sign-in/sign-up, and again on loads where a user is already signed in. Never identify public or anonymous visitors on a default install — every identified user counts toward MAU and can cause overages.
2. **Keep it simple.** The default install is `init()` + `identify()` + `reset()`. Use any other function (`identifyAnonymous`, `group`, `track`, `setCustomNavigate`, `start`, identity verification) only when the customer explicitly asks — see Advanced.
3. **Client-side only — requires a browser.** Userflow requires a browser to initialize; it is not built for server-side rendering. You may safely *import* the package from shared code (the import won't crash on the server), but `init()`, `identify()`, and `reset()` must be *called* only in the browser, never during server rendering — on the server there's no DOM, no browser session, and no way to show flows. In React Server Components / Next.js App Router, call them from a Client Component marked `"use client"`, not a Server Component.
4. **One token per environment.** Each Userflow environment (Production, Staging) has its own token. Never use one environment's token in another.
5. **No universal install.** Read the codebase and adapt placement to the actual framework. If you can't determine the framework, the auth flow, the user ID, or the environment token, ask — don't guess.
6. **Never initialize twice.** If Userflow is already initialized in the codebase, do not generate new install code or rewrite the existing setup. Point to where the existing `init()` lives and do not continue with a new installation.
7. **The user ID is the customer's choice.** Userflow accepts any stable, unique identifier the customer chooses. A database ID is recommended because changing the identifier later creates a *new* Userflow user — but don't restrict it; email is allowed if they want it.

---

## Step 1 — Analyze the Codebase

**If you have repository access,** inspect the project before asking anything, and determine:

| Read | Determine |
|---|---|
| `package.json` / lockfile / build config | Is `userflow.js` already installed? Is there a bundler (Vite, Webpack, Rollup)? Which framework — or no build step (server-rendered / plain HTML)? |
| App entry / bootstrap (`main.*`, `index.*`, `App.*`, root layout/template) | Where `init()` runs once on load |
| Auth / session code (sign-in, sign-up, session restore, sign-out) | Where `identify()` and `reset()` belong |
| User model / session object | The user ID to use and the fields available (name, email, signup timestamp) |

Then restate your findings as assumptions and confirm once — e.g. *"React + Vite app; users sign in via `useAuth()`; ID is `user.id`. I'll init at app boot and identify in the post-login path. Correct?"* — then proceed. Name the customer's real framework, auth entry point, and ID field in your code and summaries.

**If you do not have repository access** — or the customer is non-technical (a founder or PM) and doesn't know their stack — do not guess or invent file paths. Either ask for the essentials (framework, auth library, where sign-in/sign-up and sign-out happen, the user-ID field), or, if they can't answer, switch to the Developer Handoff Spec (below) and stop pressing for technical detail.

---

## Step 2 — Install

### 2.1 Get the environment token

The token comes from the Userflow UI, and someone with Userflow access can supply it two ways:

1. **Settings → Environments** — copy the **Userflow.js Token** for the target environment.
2. **Settings → Installation** — select the target environment and the install snippet appears with the token **already filled in** (NPM and HTML tabs, matching the method in 2.2). Whoever has access can click **"Copy all instructions (to send to a developer)"** to hand the full snippet — token included — to the developer doing the install. This is the easiest path when the person installing doesn't have Userflow access themselves. (The same page has a **Verify installation** button, which maps to Step 3.)

Either way, use the token for the environment this build targets, and wire it through any existing environment config so each environment uses its own token (Core rule 4).

**If the customer hasn't provided a token,** ask for it and point them to either location above. If they can't supply it right now, do not invent, guess, or reuse a token found elsewhere in the codebase, and do not leave a literal placeholder in the code. Instead, wire the token as an environment variable using the project's existing env config, leave the value unset, and tell the customer exactly which variable to set (and in which file) before the install will work. State clearly that Userflow content will not appear until that value is set.

### 2.2 Choose the install method

- **Bundler / framework app** — npm:
  ```
  npm install userflow.js
  ```
  ```js
  import userflow from 'userflow.js'
  ```
  The package lazy-loads the full library from the CDN on first use and queues calls made before it's ready, so you can call `init()`/`identify()` immediately. It includes TypeScript type definitions, so `userflow` is typed automatically.

- **No build step / plain HTML** — use the official `<script>` snippet from the Userflow.js Installation docs (copy it verbatim — don't hand-write it). After it loads, the API is `window.userflow`. In a TypeScript project using the script tag, declare `window.userflow` (augment the global `Window` type) since there's no import to carry the types.

### 2.3 Initialize once

Call `init()` once per page load, before any other Userflow call, where the app boots (Core rule 3: client-side only). In component frameworks, make the call from a client lifecycle hook that runs once after mount (or an equivalent one-time client entry point) — never during render and never at module scope. The same applies to `identify()` and `reset()`: lifecycle hooks and event handlers, not render.

```js
userflow.init('<USERFLOW_TOKEN>')
```

### 2.4 Identify after authentication

Call `identify()` on the authenticated path only. Guard with `isIdentified()` so component re-renders and route changes don't re-identify the same user redundantly:

```js
// Call after sign-in / sign-up, and on loads where the user is already signed in.
// Only use this isIdentified() guard if your app does NOT switch accounts without
// a page reload. If it can, reset() then identify() on switch (see note below).
if (!userflow.isIdentified()) {
  userflow.identify(user.id, {
    name: user.name,
    email: user.email,
    signed_up_at: user.createdAt // ISO 8601, e.g. '2024-03-11T14:25:00Z'
  })
}
```

- `user.id` is the only required argument; the attributes object is optional and merged into existing attributes.
- `signed_up_at` must be ISO 8601.
- `isIdentified()` returns `false` again after a full page reload, so `identify()` still runs once per fresh load. On an **account switch without a reload**, call `reset()` first, then `identify()` the new user — don't let the guard skip the new identity. The guard exists to prevent duplicate `identify()` calls from re-renders; it must not prevent identifying a *different* authenticated user.
- For server-rendered template apps (JSP, PHP, Rails, Django), inject the real user values from the server into the authenticated page's template (the snippet still executes in the browser).

### 2.5 Reset on sign-out

```js
userflow.reset()
```

Add this to the sign-out handler so Userflow forgets the current user and hides active content (prevents the next user on a shared device inheriting the previous user's state).

**If sign-out is a server redirect** (no client-side sign-out handler — common in server-rendered template apps like JSP, PHP, Rails, Django): either call `reset()` from the logout control's `onsubmit`/`onclick` before navigation, or — preferred, since it avoids a navigation race — emit `reset()` at the top of the post-logout landing page.

### 2.6 Replace placeholders

Before finishing, confirm **no literal placeholder values remain** anywhere in the code — for example `<USERFLOW_TOKEN>`, `USER_ID`, `'USER_ID'`, `USER_EMAIL`, `USER_SIGNED_UP_AT`, or a copied `'YOUR_TOKEN'`. Every one must be a real, dynamic value read from the app. A leftover literal is the most common broken install.

### 2.7 Ask about extra attributes

Before finishing, ask whether the customer wants additional attributes — adding them now avoids wiring them in later:
- **User attributes** (e.g. `role`, `plan`) go in the `identify()` object.
- **Company/group attributes** use `group()` (Advanced), only if they want group-level targeting.

Add only what they specify, using snake_case names and ISO 8601 for datetimes. Don't invent attributes.

### 2.8 Check Content Security Policy (only if the app uses one)

If the app enforces a Content Security Policy, Userflow.js will be blocked unless its domains are allowed — a common cause of "nothing loads." Follow the [Content Security Policy doc](https://help.userflow.com/docs/content-security-policy) to add the required directives. If the app has no CSP, skip this.

---

## Step 3 — Verify the Install

Confirm each of the following:

- ✓ Userflow.js loads with no load errors in the browser console
- ✓ `init()` runs once, with the token for the environment you're testing
- ✓ `identify()` runs after sign-in — `userflow.isIdentified()` returns `true`
- ✓ The user appears in Userflow with the attributes you sent (Userflow's installation check confirms detection)
- ✓ On a public page while signed out, `userflow.isIdentified()` returns `false` — no anonymous/public-page identification (**the key MAU check**)
- ✓ `reset()` clears identity on sign-out (`isIdentified()` returns `false` afterward)
- ✓ No Userflow-related console errors

**If the user isn't appearing:**
- Open the browser **console** and check for Content Security Policy errors (see 2.8) or other load errors.
- Open the **Network** tab and confirm the identify request fired (requests to Userflow's domains).
- Confirm `identify()` actually ran (`isIdentified()` is `true`), the token matches the environment you're viewing, and no placeholders remain.

---

## Step 4 — Document

Append a **Userflow installation** section to `AGENTS.md`: install method, where `init()` / `identify()` / `reset()` live, the token source, and the user-ID field used. If `AGENTS.md` (or a Userflow section in it) already exists, **update or append — never overwrite the file or unrelated sections.** Note that identity verification (Advanced) is a recommended production-hardening step still pending, so future agents know.

---

## Framework Placement

The three calls are the same everywhere and always execute in the browser (Core rule 3); only placement differs.

| App type | `init()` | `identify()` |
|---|---|---|
| Bundler / client-rendered SPA (React, Vue, Angular, Svelte) | At app boot, once on load | In the post-auth code (sign-in/sign-up success) and on loads where a session exists |
| React Server Components / SSR (Next.js, Nuxt, SvelteKit) | Next.js App Router: a dedicated `"use client"` component rendered from `app/layout.tsx` — never the layout itself. Next.js Pages Router: `pages/_app.tsx` inside a mount effect. Other SSR frameworks: the equivalent client-only lifecycle | Client-side authenticated path, after hydration |
| Plain HTML / no bundler | After the script-tag snippet, via `window.userflow` | Only on authenticated pages |
| Server-rendered templates (JSP, PHP, Rails, Django) | Emit the loader `<script>` into the authenticated page's HTML — it executes in the browser on load | Emit the `identify()` call into authenticated-page templates only, with the user values injected server-side (the call still runs in the browser). For sign-out via server redirect, see 2.5 |

For Angular and shell / micro-frontend architectures, see the Angular & Shell guide in References.

---

## No Codebase Access — Developer Handoff Spec

If the customer is scoping for a developer rather than installing now, don't write code — generate `USERFLOW_INSTALL_SPEC.md` containing: install method and commands/snippet; the environment-token strategy; the full `init()` + `identify()` (with `isIdentified()` guard) + `reset()` code with the real ID field named; where each call goes (file hints); the core rules (authenticated-only, client-side only); and the Step 3 verification checklist. The generated document must be completely self-contained and require no context from this conversation.

(If the customer has Userflow UI access, Userflow's own **Settings → Installation → "Copy all instructions (to send to a developer)"** button is a built-in shortcut for the basic snippet + token. Generate the fuller `USERFLOW_INSTALL_SPEC.md` when they need placement guidance and the core rules alongside it.)

---

## Advanced — Only When the Customer Asks

Do not use these on a default install. Add one only when the customer requests that capability, and explain the trade-off.

- **`identifyAnonymous(attrs?)`** — a separate, opt-in way to identify signed-out visitors so they can see content. It is **not** a fallback for `identify()`: if a user is never identified, content simply doesn't show and they appear as "not identified" in the Userflow Debugger — that is expected. Anonymous visitors **count toward MAU and can cause overages**, so use it only with the customer's explicit consent.
- **Identity verification** — **ask the customer first; proceed only if they want it.** Pass a `signature` (HMAC-SHA256 of the user ID, computed with the environment's Secret Key) as the third argument: `userflow.identify(userId, attrs, { signature })` (same for `group()`). The Secret Key and signing stay on the backend, never in frontend code. Recommended for production; requires backend work.
- **`group(id, attrs?, { signature }?)` / `updateGroup(attrs)`** — associate the user with a company/account for account-level targeting (plan-gated). Call `group()` again when the active account changes.
- **`track(name, attrs?)`** — track custom events (`identify()` must be called first; page views are tracked automatically).
- **`start(id, { once })`** — start a specific flow/checklist programmatically.
- **`setCustomNavigate(url => router.push(url))`** — make in-flow "Go to page" actions use the app's client-side router.
- **Other methods:** `updateUser(attrs)`, `endAll()`, `remount()`, `on(event, listener)` / `off(event, listener)` exist for advanced control — see the Userflow.js Reference.

---

## Reference

- [Userflow.js Installation](https://help.userflow.com/docs/userflowjs-installation) — install methods (npm and script tag), placeholders, environments
- [Userflow.js Reference](https://help.userflow.com/docs/userflowjs-reference) — core methods (`init`, `identify`, `isIdentified`, `reset`) and advanced (`identifyAnonymous`, `updateUser`, `group`, `updateGroup`, `track`, `start`, `endAll`, `remount`, `on`/`off`, `setCustomNavigate`)
- [Userflow API Reference](https://help.userflow.com/docs/userflow-api-reference) — server-side user/group registration and the REST API
- [Identity verification](https://help.userflow.com/docs/identity-verification) — HMAC-SHA256 `signature` (third argument to `identify()`/`group()`), computed on the backend
- [Content Security Policy](https://help.userflow.com/docs/content-security-policy) — CSP directives needed for Userflow.js to load
- [Element inference and dynamic class names](https://help.userflow.com/docs/element-inference-and-dynamic-class-names) — targeting elements reliably when class names are dynamic
- [Using Userflow in Angular and Shell (Micro-Frontend) Applications](https://help.userflow.com/docs/using-userflow-in-angular-and-shell-micro-frontend-applications) — placement for Angular and micro-frontend/shell architectures
