---
name: port-create-custom-oauth-app
description: "Register an org-scoped external interface app (a public/PKCE Auth0 OAuth client) for a custom UI, such as a Lovable-, v0- or bolt.new-built app, using Port's MCP tools, then wire the Authorization Code + PKCE grant into that UI so it can sign users in and call the Port API. Use when asked to 'build a custom UI on top of Port', 'connect my Lovable app to Port', 'register an OAuth app in Port', 'add Port login to my app', 'get a client ID for my external app', or 'fix a Callback URL mismatch / Service not found error when logging in with Port'. Out of scope: Port's own plugin and custom widget system (this skill never builds or installs anything inside Port itself), and managing Port's SSO or identity-provider connections."
license: MIT
compatibility: "Claude Code, Cursor, Codex CLI, GitHub Copilot"
allowed-tools:
  - list_external_interface_apps
  - upsert_external_interface_app
  - revoke_external_interface_app
metadata:
  version: "1.0.0"
  author: port-labs
  repository: https://github.com/port-labs/port-skills
  tags: port,oauth,pkce,auth0,external-interface,custom-ui,mcp-powered
  summary: Register an OAuth app for a custom UI and wire up PKCE login
---

# Port custom OAuth app

Register an org-scoped **public/PKCE** OAuth client, an *external interface
app*, so a custom UI you build outside Port can authenticate its own users
and call the Port API directly. There is never a `client_secret`: these are
PKCE public clients by design, so never ask for or invent one.

Registering, updating, and revoking apps takes **org admin** rights.

## Prerequisites

- Go over the `port-getting-started` skill first if this is your first time
  working with Port.
- Port's MCP server connected, as an org admin. The three tools above are
  the only way this skill documents for registering an app, so there is no
  non-MCP fallback here. Without them, search `search_port_knowledge_sources`
  or [docs.port.io](https://docs.port.io) for the current alternative rather
  than guessing an endpoint.
- Register and test against the **published**, publicly reachable URL of the
  UI, not a login-gated live preview, or the login redirect never lands.

## How to set it up

1. **Collect the inputs, never guess them:** app name, 1 to 5 exact redirect
   URIs, and the Port region (EU, US, or other) that decides the Auth0 domain
   and API base URL. See
   [references/registering-the-app.md](references/registering-the-app.md).
2. **Check existing apps, then register:** call
   `list_external_interface_apps`, then `upsert_external_interface_app`
   without `appId`. Keep `id` and `clientId` straight, they are not
   interchangeable. Same reference.
3. **Wire the PKCE flow into the UI:** popup-based login, `code_verifier`
   kept in the opener's memory (never in `state` or a URL), token exchange
   from a server route, `audience` set to the region's API base. See
   [references/pkce-flow.md](references/pkce-flow.md). A complete React
   example is in [assets/spa-example.md](assets/spa-example.md), and
   [references/popup-login-explained.md](references/popup-login-explained.md)
   explains why the popup flow is built the way it is.
4. **Call the Port API** with the access token, and account for the CORS
   allowlist's propagation delay. See
   [references/pkce-flow.md#calling-the-port-api](references/pkce-flow.md#calling-the-port-api).
5. **Check the code against the verification checklist** before telling the
   user it is done. See
   [references/pkce-flow.md#verification-checklist](references/pkce-flow.md#verification-checklist).
6. **Add the published URL as a redirect URI** once the UI is published, and
   manage or revoke apps later. See
   [references/registering-the-app.md#managing-apps](references/registering-the-app.md#managing-apps).

## Common pitfalls

More symptoms and the common mistakes to push back on are in
[references/troubleshooting.md](references/troubleshooting.md).

| Symptom | Cause | Fix |
|---|---|---|
| `Callback URL mismatch` loop on login | `redirect_uri` is not an exact match for a registered URI, or it is a login-gated preview origin | Read `window.location.origin` from the running app and register that exact origin and path, and test from the published URL |
| `Service not found: <audience>` | Wrong `audience` for the environment | Use the region's API base as the audience, never production's by default |
| `/oauth/token` fails with a bare `Failed to fetch` | Auth0 CORS-blocks the browser call, the origin is not in the app's Allowed Web Origins | Do the token exchange from a server route |
| `404: User with id "me" was not found` | Port has no `/v1/users/me` | Read claims from the decoded `id_token`, or call `/v1/users/{email}` |

## Quick reference

- Tools: `list_external_interface_apps`, `upsert_external_interface_app`,
  `revoke_external_interface_app`. All need org admin.
- `redirectUris`: 1 to 5, exact, absolute, no wildcards, `https://` only
  (`http://` allowed for `localhost` / `127.0.0.1`). An update **replaces**
  the whole set.
- `id` goes to `appId`. `clientId` goes in the frontend as `client_id`.
- Full detail: [registering-the-app](references/registering-the-app.md),
  [pkce-flow](references/pkce-flow.md),
  [popup-login-explained](references/popup-login-explained.md),
  [troubleshooting](references/troubleshooting.md).

## Examples

- [assets/spa-example.md](assets/spa-example.md): complete React SPA login
  flow, with the minimal `LoginPage`.
- [assets/login-page-anchor-ui.md](assets/login-page-anchor-ui.md): the
  default styled `LoginPage` using `@port-labs/anchor-ui`.
- [assets/port-proxy-fallback.md](assets/port-proxy-fallback.md): same-origin
  proxy for when the calling origin isn't a registered redirect URI.
