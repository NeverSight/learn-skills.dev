---
name: swell-frontend-api
description: "Use this skill for Swell Frontend API operations: catalog and content, shopper sessions, carts, checkout, payments, customer accounts, subscriptions, localization and public app data. Applies inside Swell app frontends through the Apps SDK Storefront client and swell-js, and to independent storefronts using explicitly configured clients or direct API requests. Also covers storefront GraphQL and calls to app route functions. Pair with swell-app for app scaffolding, runtime setup, models, hosting and deployment; reuse its supplied clients and session helpers. Privileged store operations belong to swell-backend-api. Proxima / Liquid theme authoring and other platforms are outside scope."
allowed-tools: Read, Grep, Glob, Bash
---

# I. What This Covers

The Frontend API is the part of Swell a storefront calls with a public key. Every request acts for one shopper's session: it reads the catalog, content and settings, owns that shopper's cart and checkout, and manages the logged-in customer's account and subscriptions. It cannot administer the store: it writes only what the session owns, plus app collections that declare public permissions. Anything that needs a secret key belongs to `swell-backend-api`, behind a server or an app function.

This skill owns Frontend API operations in both Swell apps and independent storefronts. `swell-app` owns app scaffolding, runtime context, resource declarations, hosting and deployment. Use both for a Swell storefront app, or when a storefront feature needs an app model or function.

# II. Clients and Requests

**Which client.** Every client is a swell-js client or sends the same requests, so the references apply to all of them, and `swell` in their examples stands for the client the code has.

- **Inside a Swell app, keep the supplied client**: the scaffold's `getStorefront()` on the Vinext server and `useSwell()` in the browser, with their session wiring, as the `swell-app` skill's `references/frontend-storefront.md` describes. Do not add `swell.init()` or a cookie adapter of your own beside them.
- **Outside an app**, the reference below says which client fits a browser, a server and a caller without JavaScript.

**Read `references/clients-sessions.md`** before setting up a client outside an app, and before any server rendering, caching or static generation. The rules from it that change a design:

- The session is the identity. A token in the `swell-session` cookie carries the cart, the login, the locale and the currency: there is no cart id to keep.
- A server needs one client per request, with a cookie adapter that saves the token. Without one, each call is a new session with an empty cart, and nothing reports it.
- Change the cart or the account in a route handler, a server action or the browser, not while a page renders.
- Swell caches product, category and settings reads for five seconds. Cart and account reads are never cached, and the framework must not cache them either.

Two options the package does not explain: `useCamelCase: true` converts the keys of answers to camelCase and the keys of requests back to snake_case, and `timeout` applies only to card tokenization and payment gateway requests, so an ordinary call has no deadline unless you add one.

**How failures arrive.** A call fails in one of three ways, and which one depends on the call:

1. **It resolves with `errors`**, `{ errors: { <field>: { code, message } } }` in place of the record, for a value that fails validation.
2. **It rejects** with an `Error` that has `message`, `status`, `code` and `param`: a field the call does not accept, a missing login, a refused checkout step.
3. **It resolves empty.** A read of one record that finds nothing resolves with `null` or an empty string, and the same read can give either: test the answer for truth, never against `null`.

The cart, payments and accounts references each say which of these their calls do, under "How failures arrive". Two rejections belong to every call. A failing status whose body has no `error` key, such as an HTML error page, rejects with `code: 'connection_error'` and no `status`, so a test of `err.status >= 500` misses it. A network failure rejects with the runtime's own `TypeError`, which has none of these fields. `settings.load()` never rejects: on a failure it logs and resolves.

**Generic requests.** `swell.get(path, query)` and `swell.post`, `put` and `delete(path, body)` reach any `/api` path with the same key and session. A string as the second argument is added to the path (`swell.get('/products', 'blue-shoes')`); for an id and a body together use `swell.request(method, path, id, body)`.

- A list resolves with `{ count, page, limit, results }`: 15 records unless `limit` says otherwise, sorted by `id` descending. A query key it does not know is read as a `where` condition.
- `/carts`, `/accounts` and `/payments` are refused on these routes: use `swell.cart` and `swell.account`.
- `expand` takes only fields the model makes public. Any other rejects with `You can only expand public fields (<field>)`. A link the model publishes whole brings what a storefront read of the linked model returns: its public fields, of the records that read returns.
- `include` attaches a second query to each record, in one request: `include: { <key>: { url: '<path>', params: { <query field>: '<record field>' }, data: { limit: 3 } } }` puts `{ count, results }` under `<key>`. Each `<record field>` must be one the read returns, and a param on a field the second query is already limited by, as a scoped collection's account, rejects the call. The path can be an app collection, `/apps/<app_id>/<collection>`. A sub-query on a collection that is not public rejects the whole call.

**App data.** The generic requests are how a storefront reaches an app's collections, at `/apps/<app_id>/<collection>`. **Read `references/app-data.md`** before reading or writing app data from a storefront. The rules from it that change a design:

- A collection answers only what its model declares public. With nothing public, every call is refused.
- `scope: 'account'` limits reads and writes to the logged-in customer's own records, and `input.scope: 'account'` limits writes only. A scoped call, a create included, needs a login.
- Fields an app adds to a standard model are returned to any storefront when the app marks them public.

**TypeScript.** swell-js ships its own declarations: never install `@types/swell-js`. `SwellClient` is the type of a client. The declarations differ from the runtime in a few places. Where a call the references describe does not compile, cast, and leave the call as it is:

- **`products.get()` and `content.get()` are typed as never empty**, so the compiler does not ask for the check that a missing record needs.
- **A `useCamelCase` client is typed in snake_case** unless it is created as `swell.create<'camel'>(…)`.
- **`cart.getShippingRates()` is typed as a cart** and resolves with the rating. **`products.variation()` is typed as a product**, without `variant_id`.

**GraphQL.** The Frontend API is also served as GraphQL at `https://<store-id>.swell.store/graphql/v2`, with a playground at `/playground`. `/graphql` and `/graphql/v1` serve an older, deprecated schema: always write the `/v2` path.

- **Send the public key itself as the `Authorization` header.** The `Basic` form that the `/api` routes take answers with status 200 and an `AUTHENTICATION` error on every field.
- The session travels as on the `/api` routes: save the `X-Session` response header and send it back.
- A refused field arrives with status 200, as `null` under `data` and the reason under `errors`.
- The schema is built from the store's public models, its content models included, and kept for an hour: send `Cache-Control: no-cache` once after adding a model. Fields are camelCase, and a product query has no `$filters`.
- **There is no shipping-rate query and no payment tokenization**, so a GraphQL storefront still loads swell-js to check out.

# III. Catalog, Content and Settings

**Read `references/catalog.md`** for products, variants and `products.variation()`, stock, categories and facets with `$filters`, content, settings and menus, locales, currencies and price formatting. The rules from it that change a design:

- Only active products are returned, and a `fields` parameter is ignored.
- A product's `price` is already what this shopper pays; `orig_price` is present when it was lowered.
- `products.get()` includes variants and `products.list()` does not; `products.variation()` needs them and throws synchronously without them.
- `content.list()` returns published records only, while `content.get()` returns drafts too.
- `await swell.settings.load()` comes before `settings.get()`, the menus and `currency.format()`.

# IV. Cart and Checkout

The cart belongs to the session. `swell.cart` adds and changes items, takes the customer's email, addresses, shipping service, coupon and gift cards, and `cart.submitOrder()` turns the cart into an order.

- **Read `references/cart-checkout.md`** for the cart, the checkout sequence, guest and logged-in carts, account credit, the checkout settings and reading the order afterwards.
- **Read `references/payments.md`** for collecting a payment method: payment elements and `tokenize()`, redirect methods, `swell.card.createToken()` and saved cards.

The rules from them that change a design:

- Checkout calls reject, and item calls can also resolve with `errors`: handle both.
- Payment elements run only in a browser, and a card element exists only for some gateways; the others need a card form of your own.
- Collect the payment method last: a card authorization is for the amount due when it is made.
- `capture_total` is the amount to pay. `grand_total` does not subtract gift cards or account credit.
- An order is read back by its cart's `checkout_id`, which the order does not carry, and anyone who has that id can read the order.

# V. Accounts and Subscriptions

`swell.account` signs a customer up and in and holds the profile, addresses, saved cards and order history. `swell.subscriptions` and `swell.invoices` hold what a logged-in customer is billed for.

**Read `references/accounts-subscriptions.md`** for sign-up, login and logout, password recovery, addresses, order history, and creating, pausing, changing and canceling a subscription. The rules from it that change a design:

- `account.login()` resolves with `null` for wrong credentials. It does not reject.
- Logged out, `account.get()` resolves with `null` and every other account, subscription and invoice call rejects.
- A login or a logout changes the cart: read it again.
- A write resolves with `errors` for a bad value and rejects for a field it does not accept.
- A subscription is canceled, and a cancellation undone, with `canceled` and `cancel_at_end` together.
- **In tests, give customers an `example.com` address.** Sign-up, recovery and every order email the customer. Swell does not deliver to that domain, and it deactivates a store that sends too many real emails, test environment included.

# VI. Calling App Functions

`swell.functions.get`, `post`, `put` and `delete(appId, functionName, data)` call an app's route function at `/functions/<app_id>/<name>` with the storefront's key and session. Use one where a storefront feature needs app logic, such as a submission that must be checked, instead of making privileged data public.

- **The route must be marked public.** Any other needs a secret key, which a storefront never carries, and rejects with status 401.
- `get` sends `data` as the query and the other calls send it as the body. The function reads either as `req.data`, values sent as the query as strings.
- **Nothing is case-converted.** On a `useCamelCase` client too, the body is sent as written and the answer comes back as the function produced it.
- **An answer with an `error` key rejects**, whatever its status, with that status and message. A `SwellError` thrown in the function answers that way. A failing status without the key rejects as the `connection_error` above, so a response the route builds itself needs `{ error: { message, code } }`.

What the function receives, the shopper's session included, is in the `swell-app` skill's `references/functions-routes.md`, "Calling routes from outside Swell (hosted gateway)".
