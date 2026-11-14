---
name: tiendanube-oauth-apps
description: "Apply when implementing or reviewing how a Tiendanube / Nuvemshop app gets and keeps access to stores: creating the app in the Partners Portal, its URLs and Redirect URL, the OAuth 2 authorization code flow, the state parameter, exchanging the code at /apps/authorize/token, user_id as the store ID, scopes and why new scopes need a reinstall, storing one token per app and store pair, reinstallation without duplicated resources, uninstall cleanup, private apps installed with /admin/apps/{app_id}/authorize, demo stores, and Partner Action calls signed with the client secret. Use for the install callback, the token table, or an installation that sends the merchant to the partner login."
license: MIT
compatibility: "Tiendanube / Nuvemshop Admin API, version 2025-03. Apps built by partners; not for the official Admin MCP."
metadata:
  author: commente.me
  version: "0.1.0"
---

# OAuth apps: installation, tokens and scopes

## When this skill applies

Use this skill when a partner app needs authorization to call the Admin API for a store, and when it must stay correct across installs, reinstalls and uninstalls.

- Registering the app in the Partners Portal and filling its URLs
- Writing the Redirect URL handler that receives `code`
- Exchanging the code for an access token and saving it
- Choosing scopes and changing them later
- Handling a second installation of an app that is already installed
- Installing a private ("For Your Customers") app in a real store
- Calling endpoints that belong to the app rather than a store (billing plans)

Do not use this skill for:

- Headers, rate limit and pagination of API calls (use `tiendanube-rest-api`)
- Webhook registration and the privacy webhooks configured in the portal (use `tiendanube-webhooks`)
- Embedding the app's UI in the Admin with Nexo (use `tiendanube-admin-apps`)
- A merchant connecting an AI assistant to their own store: the official Admin MCP handles that OAuth itself; this skill is for developers who write the app

## Decision rules

- The only supported grant type is the authorization code. There is no token refresh step to build, because tokens do not expire.
- Access tokens do not expire. A token stops working when a new token is issued for the same app and store, or when the merchant uninstalls the app.
- The token response carries `user_id`, which is the store ID used in every API path. Some responses name the same value `store_id`.
- The authorization code lives 5 minutes. Exchange it immediately in the Redirect URL handler, not in a later job.
- A store you own is not special: integrating your own store still goes through installation and the OAuth flow.
- Scopes are fixed per app in the Partners Portal. The authorize URL cannot ask for an optional subset or add permissions per installation. Enable features in your own backend based on the merchant's configuration instead.
- Ask only for the scopes the app uses. Any write scope implies its read scope. Webhooks can only be registered for resources the app has scope for.
- New or changed scopes apply only after the app is uninstalled and installed again in each store; that issues a new token with the new scopes.
- Distribution: **App Store** apps go through homologation and are listed for every merchant; **For Your Customers** apps skip homologation and are installed only by the merchants you choose. The **In development** status does not block installation or OAuth in a real store.
- Endpoints documented as Partner Action (for example creating billing plans) live under `/{version}/apps/{app_id}` and use the app's client secret as the bearer token, with no store ID.

## Hard constraints

### Constraint: Exchange the code server-side, with a JSON body, using the same app's credentials

POST to `https://www.tiendanube.com/apps/authorize/token` (or the identical `nuvemshop.com.br` URL) with `client_id`, `client_secret`, `grant_type=authorization_code` and `code` in a JSON body.

**Why this matters**

Sending the fields as query parameters is a documented common failure. The code is bound to the app that requested it, so exchanging it with another app's credentials fails. The client secret belongs on your server only.

**Detection**

Credentials in the token URL query string, the exchange done from frontend JavaScript, a shared credentials constant used by several apps, or a missing `grant_type`.

**Correct**

```ts
app.get("/oauth/callback", async (req, res) => {
	if (req.query.state !== req.session.oauthState) return res.status(400).send("Invalid state");
	const r = await fetch("https://www.tiendanube.com/apps/authorize/token", {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({
			client_id: process.env.NS_CLIENT_ID,
			client_secret: process.env.NS_CLIENT_SECRET,
			grant_type: "authorization_code",
			code: req.query.code
		})
	});
	const { access_token, scope, user_id } = await r.json();
	await saveInstallation({ appId: process.env.NS_CLIENT_ID!, storeId: String(user_id), token: access_token, scope });
	res.redirect("/welcome");
});
```

**Wrong**

```ts
await fetch(
	`https://www.tiendanube.com/apps/authorize/token?client_id=${id}&client_secret=${secret}&grant_type=authorization_code&code=${code}`,
	{ method: "POST" }
);
```

### Constraint: Store credentials per app and store pair

Key every installation record by the app ID (`client_id`) and the store ID (`user_id`), and keep the token and granted scopes in that record.

**Why this matters**

A token is scoped to one app in one store. Two apps installed in the same store keep independent tokens and webhooks: authorizing or removing one leaves the other untouched. Picking the wrong record returns another store's data or `Invalid access token`; reusing a demo-store token for a client's store is the classic case.

**Detection**

A single `ACCESS_TOKEN` environment variable used for all stores, a table keyed only by store ID when the partner runs several apps, or cleanup code that deletes every record for a store when one app is uninstalled.

**Correct**

```sql
CREATE TABLE ns_installation (
  app_id      TEXT NOT NULL,
  store_id    TEXT NOT NULL,
  access_token TEXT NOT NULL,
  scope       TEXT NOT NULL,
  installed_at TIMESTAMPTZ NOT NULL,
  uninstalled_at TIMESTAMPTZ,
  PRIMARY KEY (app_id, store_id)
);
```

**Wrong**

```ts
const TOKEN = process.env.TIENDANUBE_TOKEN; // used for every store
```

### Constraint: Make reinstallation idempotent

When an already installed app is installed again, only replace the token. Do not create, change or delete store resources. Before creating anything (shipping carrier, payment provider, script, webhook), check with a `GET` that it does not exist yet.

**Why this matters**

Reinstalls happen every time scopes change. Creating resources again leaves duplicates in the merchant's Admin, such as two shipping carriers with the same name.

**Detection**

An install handler that always `POST`s carriers, scripts or webhooks without a prior lookup, or that deletes and recreates them.

**Correct**

```ts
await upsertInstallation(appId, storeId, access_token, scope);
const hooks = await listAll(storeId, access_token, "/webhooks");
for (const wanted of REQUIRED_HOOKS) {
	if (!hooks.some((h) => h.event === wanted.event && h.url === wanted.url)) {
		await createWebhook(storeId, access_token, wanted);
	}
}
```

**Wrong**

```ts
await createShippingCarrier(storeId, access_token, { name: "Acme Express" }); // on every install
```

### Constraint: Create store resources only after the merchant's account is usable

If your service approves merchants manually, generate the token first, let the merchant register, and create resources only after approval. Do not make the merchant install again after approval.

**Why this matters**

A carrier or payment provider that appears in the Admin before the account is approved cannot be used and confuses the merchant. Asking for a second installation after approval is called out as a bad experience.

**Detection**

Resource creation inside the OAuth callback for an app whose accounts need approval, or an approval email that links to the authorize URL again.

**Correct**

```ts
// callback: save token, then send to signup
await saveInstallation(...);
res.redirect(`/signup?store=${storeId}`);
// later, in the approval job
await provisionStoreResources(storeId);
await notifyMerchantApproved(storeId);
```

**Wrong**

```ts
await saveInstallation(...);
await provisionStoreResources(storeId); // account still pending review
```

## Preferred pattern

Install flow:

1. The merchant clicks install in the App Store, or opens `https://www.tiendanube.com/apps/{app_id}/authorize?state=<csrf>`. For a store other than your demo store, or a private app, the merchant appends `/admin/apps/{app_id}/authorize` to their own Admin URL.
2. The merchant accepts the scopes (skipped if already accepted).
3. The browser lands on your Redirect URL with `code` and `state`. Verify `state`.
4. Exchange the code within 5 minutes and save the record keyed by app and store.
5. Create or find the merchant's account in your service. Apps that create accounts automatically can read the store's data (email, business details) from `GET /store`.
6. Provision resources idempotently, only once the account can be used.

Portal configuration: all app URLs are required. Set the Redirect URL to an endpoint you control, the app URL (your panel), the preferences URL, the privacy policy URL, the three privacy webhook URLs, and support URL or email. The Redirect URL that the portal fills in by default, `https://partners.tiendanube.com/applications/authentication/{app_id}`, only works from the partner panel: leaving it makes installations ask for partner login. If the field is locked, contact partner support with the app ID, status, current URL and the callback you need; never ask the merchant for partner credentials.

Testing: create a demo store from the Partners Portal and use **Install application** with your partner credentials. When several stores share an email, use a separate browser session so the right store authorizes.

Uninstall: the merchant uninstalls from **My applications**. Nuvemshop removes the app's shipping carriers, payment providers, webhooks and scripts automatically; pages and other resources stay in the store. Delete anything else your app created while it still has access, and mark the installation as uninstalled when `app/uninstalled` arrives.

Sign-in to your own site: the same authorize link works as a login button. Add a `state` value (for example derived from the session) and check it on return; identify the user by the store ID that comes with the new token.

## Common failure modes

- Leaving the default Partners Portal Redirect URL, so merchants see a partner login screen.
- Expecting the landing page that prints a ready curl to show a `code` on later installations: it only does so on the first one. Capture `code` from your Redirect URL.
- Adding a scope in **Basic Data** and expecting existing tokens to gain it without a reinstall.
- Exchanging the code minutes later from a queue and getting an expired code.
- Using Postman with the fields in **Params** or with a non-JSON body type.
- Skipping `state`, which leaves the callback open to CSRF.
- Assuming an OAuth token proves a script or NubeSDK feature is active in the store; that needs its own validation.
- Treating a token as expired after some time and asking merchants to reinstall needlessly.

## Review checklist

- [ ] Redirect URL points to your own HTTPS endpoint, not the portal default
- [ ] `state` is generated, stored and checked
- [ ] Code exchange is server-side, JSON body, with `grant_type=authorization_code`
- [ ] Installation records are keyed by app ID and store ID and hold the token and granted scopes
- [ ] Scopes are minimal and the reinstall procedure is documented for scope changes
- [ ] Reinstall only replaces the token; resource creation checks for existing ones
- [ ] Resources are created only after the merchant's account is usable
- [ ] Partner Action calls use the client secret and `/apps/{app_id}` paths, never a store token

## Related skills

- [`tiendanube-rest-api`](../tiendanube-rest-api/SKILL.md): using the token and store ID in API requests
- [`tiendanube-webhooks`](../tiendanube-webhooks/SKILL.md): `app/uninstalled` and the privacy webhooks set in the portal
- [`tiendanube-admin-apps`](../tiendanube-admin-apps/SKILL.md): integrated apps inside the Admin
- [`tiendanube-shipping-payment-apps`](../tiendanube-shipping-payment-apps/SKILL.md): carriers and payment providers created at install time
- [`tiendanube-erp-integration`](../tiendanube-erp-integration/SKILL.md): authorizing an ERP connector

## Reference

- [Authentication](https://nuvemshop.dev/en-US/api/authentication.md): authorization code flow, token endpoint, user_id, app and store pairs, URLs, scopes, user sign-in, common problems
- [Installation Flow](https://nuvemshop.dev/en-US/api/guides/installation.md): approval and no-approval flows, reinstall behavior, resources removed on uninstall
- [Authentication for Partner Actions](https://nuvemshop.dev/en-US/api/guides/authentication-for-partner-actions.md): /apps/{app_id} paths with the client secret as bearer
- [Getting Started (apps)](https://nuvemshop.dev/en-US/apps/getting-started.md): partner registration, app creation, integrating your own store
- [Frequently asked questions about the Admin and apps](https://nuvemshop.dev/en-US/apps/admin/faq.md): demo store, private app installation, reinstall for new scopes, partner login redirect
- [Overview (Admin apps)](https://nuvemshop.dev/en-US/apps/admin/overview.md): distribution options, demo store, private app install, uninstall steps, editing permissions
- [Authentication (ERP guide)](https://nuvemshop.dev/en-US/apps/erp-guide/authentication.md): the same flow summarized for ERP connectors
- [Glossary](https://nuvemshop.dev/en-US/apps/glossary.md): Nuvemshop and Tiendanube as one platform with two domains
- [Frequently asked questions about the API](https://nuvemshop.dev/en-US/api/faq.md): where store_id and access_token come from, wrong-store tokens
