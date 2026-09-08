---
name: service-discoverability
description: "Make a canister app discoverable to an AI agent from just its URL, including through ICP MCP. Covers publishing a /.well-known/ic-architecture manifest of your canisters — generated at deploy time from real canister IDs via the static-site recipe's presync hook and envsubst — plus exposing candid:service (interface), a getApiDoc query method (behavior), an optional OQL schema/execute data surface, and a /.well-known/ii-derivation-origin file (identity). Publishing that manifest opts the app into ICP MCP and is itself the operator's acceptance of the ICP MCP App Operator Terms, so confirm with the app's operator before deploying it. Use when making an app agent-ready or available through ICP MCP, for agent/service discovery, the well-known ic-architecture manifest, or generating that manifest at deploy time. Do NOT use for the sign-in flows that consume the derivation origin: use agent-web-identity for the agent/CLI web-identity link, or internet-identity for adding II login to a frontend."
license: Apache-2.0
compatibility: "icp-cli >= 0.3.0 with the @dfinity/static-site recipe; envsubst (gettext) for templating"
metadata:
  title: Service Discoverability
  category: Frontend
---

# Service Discoverability

## What This Is

When an AI agent is handed only your app's URL (e.g. `https://yourapp.com`), it should be able to work out the rest on its own: which canisters the app comprises, what each one does, how to call them, how to query their data, and how to act as the signed-in user. No human supplying canister IDs, no bespoke integration.

This skill covers what a canister app **publishes** to make that possible, across five layers. Layer 1 is gated: it is what an app publishes to participate in [ICP MCP](https://internetcomputer.org/icp-mcp/), and publishing it accepts an agreement on the operator's behalf — read **Before Layer 1** before writing that file. Layers 2-5 are ungated and independently adoptable; each is useful on its own, and together they make an app agent-ready.

| Layer | Question it answers | Mechanism |
|-------|---------------------|-----------|
| 1. Composition | Which canisters make up this app, and what is each for? | `/.well-known/ic-architecture` JSON manifest |
| 2. Interface | What methods and types does a canister expose? | `candid:service` metadata |
| 3. Behavior | How does it actually behave (units, lifecycle, gotchas)? | `getApiDoc` query method |
| 4. Data | How do I query its data without a method per question? | OQL `schema` + `execute` query methods |
| 5. Identity | How do I act as the signed-in user, under the right principal? | `/.well-known/ii-derivation-origin` file |

The load-bearing move for Layers 1 and 5 is **generating the well-known files at deploy time**, because the canister IDs (and the mainnet origin) differ per network. This skill uses the [`@dfinity/static-site`](https://github.com/dfinity/icp-cli-recipes/blob/main/recipes/static-site/README.md) recipe's `presync` hook to do that — the same pattern demonstrated by the community example [`raymondk/demo-ic-architecture`](https://github.com/raymondk/demo-ic-architecture/tree/main/frontend/ic-architecture).

## Before Layer 1: The Operator Must Accept the ICP MCP App Operator Terms

**Stop here before you create, generate, or deploy `/.well-known/ic-architecture`.** That file is not only configuration. Availability through [ICP MCP](https://internetcomputer.org/icp-mcp/) is governed by the [ICP MCP App Operator Terms](https://internetcomputer.org/icp-mcp/app-operator-terms/) — **version 1.1, effective 2026-09-02**, the version current when this skill was written — an agreement between DFINITY Stiftung (the "DFINITY Foundation") and the app's **operator** — and **publishing a valid manifest is, on its own, the act that accepts them** and opts the app in. No signature step, no checkbox, nothing further. An agent that adds the manifest to a build on its own initiative has entered its user into a contract without asking.

Name that version to the user: it is what they are accepting. **Check the top of the terms page before you do** — the terms are versioned independently of this skill (section 14), so if the page shows a version later than the one above, the page is right and this skill is stale. Tell the user the version the page shows, and say the skill's copy is out of date so it gets fixed.

**Do not publish until the user has confirmed both points below.** Put them in your own words, link the terms, and let the user read before they answer.

**1. They are the operator, or authorized to bind it.** The operator is the person or entity legally authorized to operate the app and declare its canisters. Building the app is not the same as operating it — section 1: *"If you develop an application but do not operate it, these Terms are for its operator to accept, not you."* A contractor, agency, or employee on someone else's app routes the decision to the operator rather than publishing and moving on.

**2. They accept what publishing permits.** Under section 2, participation lets the ICP MCP server, acting for users who have authorized their AI assistant through Internet Identity:

- read the manifest, the `candid:service` metadata of the **canisters the manifest declares**, and what `getApiDoc` / `get_api_doc` returns;
- index and cache that metadata, and describe the app and its API to assistants and their users, including in any public listing of participating apps;
- submit **query calls and, for users who authorized actions, state-changing (update) calls** to those declared canisters, signed with the per-application Internet Identity identities of those users; and
- fetch the app's published files from its origin to keep the above current.

Participation is free in both directions: DFINITY charges nothing for it and owes nothing for it.

### The manifest is the switch, and it is the whole scope

- **Only declared canisters are in scope.** ICP MCP retrieves canister metadata and submits query or update calls **only** to canisters listed in a valid manifest. Never list a canister the operator does not run or is not entitled to expose — section 5 is a standing representation, repeated every time the file is served, that every declared canister is operated by the operator or under their authority.
- **Without a valid manifest, none of that happens.** ICP MCP may still fetch and describe the app's public website, but metadata retrieval and canister calls are refused.
- **Removing the manifest is the off switch** — registered or not. Once ICP MCP observes the removal, new metadata reads and query/update calls stop; this is also the fastest mitigation if the origin or a declared canister is compromised (section 7). It does **not** stop ICP MCP fetching the public website or describing public information; for that, ask DFINITY to suspend participation at `mcp@dfinity.org`.
- **Deactivating is not terminating.** Removing the manifest ends participation; ending the *agreement* is a separate act — notice to `mcp@dfinity.org` (section 11). Neither undoes calls already executed on the Internet Computer, and sections 8, 12, 13 and 15 (personal data, warranties, liability, governing law) survive termination. Tell an operator asking how to get out both halves, not just the file deletion.
- **Keeping the manifest published is continuing acceptance**, including of an updated version of the terms. An operator who does not accept a new version ends participation before it takes effect.

### Registration is optional

Registration is **not** a condition of participation and is **not** what opts the app in — the manifest already did that. It exists so DFINITY knows who the operator is: to reach them with the notices the terms provide for (sections 10, 11, 14), and to have a record of who accepted and of which version, which publication alone does not show.

To register, the operator emails `mcp@dfinity.org` with: the operator's legal name and country; the name, role, and email of the accepting representative; the app's origin domain(s); the canister IDs the manifest declares; the URL of the app's own privacy policy, so ICP MCP can present it to users considering the app; and the version of the terms being accepted — read from the top of the terms page at that moment, which is where section 3 says it is shown. The version named in **Before Layer 1** is the one current when this skill was written; if the page disagrees, the page wins and its value is what goes in the email. Keep the registration current as any of those change.

### Obligations that outlive the deploy

These bind for as long as the manifest is published, so raise them with the user while the app is being made discoverable, not after:

- **Accuracy (section 6).** The manifest, the Candid interface, and the `getApiDoc` text must identify the app correctly, describe what each method actually does, and stay in sync as the app changes. Never present a state-changing method as read-only or harmless, and never conceal a fee or transfer it performs.
- **No assistant manipulation (section 6).** Published metadata and API docs describe the API and nothing more — no instructions telling the assistant to ignore its user, change its safety behavior, exfiltrate data, or avoid or disparage other apps. A hard constraint on `getApiDoc` content.
- **Security (section 7).** The operator is responsible for control of the origin, the canisters' security and upgrade paths, and the integrity of the discoverability files.
- **Personal data (section 8).** Requests reaching the app carry personal data — call arguments, per-application identities, and whatever the canisters return. Each party is an independent controller; the operator handles that data lawfully and keeps an accurate privacy policy available to the app's users. The [ICP MCP Privacy Policy](https://internetcomputer.org/icp-mcp/privacy-policy/) covers what ICP MCP discloses to the app, not what the app then does with it.

## Prerequisites

- `icp-cli` **and** `ic-wasm`, installed together: `npm install -g @icp-sdk/icp-cli @icp-sdk/ic-wasm`. See the `icp-cli` skill.
- The frontend deployed with the **`@dfinity/static-site`** recipe (the recommended way to host a frontend on the IC — see the `static-site` skill). This is what auto-serves `/.well-known/` files and runs the `presync` hook with deployed canister IDs available.
- `envsubst` (from GNU gettext) for templating the manifest. Any other templating mechanism works too (a small Node/`jq` script); `envsubst` is just the simplest.

## Layer 1: Composition — the `ic-architecture` manifest

> **Gated.** Publishing this file opts the app into ICP MCP and accepts the [ICP MCP App Operator Terms](https://internetcomputer.org/icp-mcp/app-operator-terms/) on the operator's behalf. Confirm with the operator first — see **Before Layer 1** above.

Publish a JSON document at the origin's `/.well-known/ic-architecture` that lists every canister and its role:

```json
{
  "version": "1.0.0",
  "canisters": [
    {
      "id": "hcv4s-uaaaa-aaabq-qaaba-cai",
      "name": "frontend",
      "role": "the frontend"
    },
    {
      "id": "hmxr2-pqaaa-aaabq-qaaaa-cai",
      "name": "backend",
      "role": "the backend",
      "description": "orders + inventory API; call getApiDoc() first"
    }
  ]
}
```

Field rules:

- `version` — the manifest schema version.
- `id` — **required**, a canister principal.
- `name`, `role` — human-readable labels; `description` is optional. These fields are untrusted, so a consumer sanitizes them before use.
- Unknown fields must be ignored, so the format can grow (e.g. per-canister network hints, or an api-doc pointer) without breaking older readers.

### Generate it at deploy time (the `presync` pattern)

Canister IDs differ per network (local, staging, mainnet), so **never commit hard-coded IDs**. Produce the file in the deploy pipeline, which already knows the IDs. With the `@dfinity/static-site` recipe this is the **`presync`** hook: it runs at sync time, *after* the canisters exist, so their IDs are resolvable.

`frontend/canister.yaml` (the per-canister config referenced from your top-level `icp.yaml`; see the `static-site` skill for the project layout):

```yaml
name: frontend
recipe:
  type: "@dfinity/static-site@v0.3.3"
  configuration:
    build:
      # Runs BEFORE the canister exists — no canister IDs available here.
      - npm ci
      - npm run build
    presync:
      # Runs AFTER canisters exist, with each canister's ID exported as ICP_CLI_CID_<NAME>.
      - mkdir -p dist/.well-known
      - envsubst < ic-architecture/tmpl."$ICP_CLI_ENVIRONMENT".json > dist/.well-known/ic-architecture
    dir: dist
```

- The static-site recipe exports each project canister's ID into `presync` as `ICP_CLI_CID_<NAME>` (name upper-cased, non-alphanumerics → `_`; e.g. `backend` → `ICP_CLI_CID_BACKEND`). Other vars: `ICP_CLI_CID` (this canister), `ICP_CLI_NETWORK`.
- `$ICP_CLI_ENVIRONMENT` is the environment being deployed (e.g. `local`, `ic`), exported into the `presync` shell. It selects the matching template, so the same hook serves every network.
- **`presync` runs with the canister directory as its working directory.** The relative `ic-architecture/...` path therefore resolves *inside the frontend canister directory* — put the templates at `frontend/ic-architecture/`, alongside `canister.yaml` (as the example project does). A path resolved from the repo root instead would make `envsubst` read nothing and silently write an empty manifest (Pitfall 7).
- Pin the recipe to the current release (`@dfinity/static-site@v0.3.3` here); check the static-site recipe releases and the `static-site` skill for the latest.

Keep one template per environment under `frontend/ic-architecture/`, with `envsubst` placeholders for the IDs.

`frontend/ic-architecture/tmpl.local.json`:

```json
{
  "version": "1.0.0",
  "canisters": [
    { "id": "${ICP_CLI_CID_FRONTEND}", "name": "frontend", "role": "the frontend" },
    { "id": "${ICP_CLI_CID_BACKEND}", "name": "backend", "role": "the backend", "description": "orders + inventory API; call getApiDoc() first" }
  ]
}
```

`frontend/ic-architecture/tmpl.ic.json` (mainnet) is the same shape; only fixed fields like a static external dependency would differ.

**Alternative — the reference demo's form.** [`raymondk/demo-ic-architecture`](https://github.com/raymondk/demo-ic-architecture/tree/main/frontend/ic-architecture) resolves the IDs explicitly with `icp canister status` rather than the exported vars — useful if you need an ID the recipe does not export. Its `presync` is:

```yaml
    presync:
      - mkdir -p dist/.well-known
      - >-
        FRONTEND_ID=$(icp canister status frontend --id-only -e "$ICP_CLI_ENVIRONMENT")
        BACKEND_ID=$(icp canister status backend --id-only -e "$ICP_CLI_ENVIRONMENT")
        envsubst < ic-architecture/tmpl."$ICP_CLI_ENVIRONMENT".json > dist/.well-known/ic-architecture
```

with the template using `${FRONTEND_ID}` / `${BACKEND_ID}` instead. `icp canister status <name> --id-only -e <env>` prints just the canister ID (there is no `icp canister id` command).

### Serve it correctly

- **`.well-known/` is uploaded automatically** by the static-site recipe (it traverses `.well-known/` even though it skips other dotfiles). A file at `dist/.well-known/ic-architecture` is served at `/.well-known/ic-architecture` with **no extra config** — no `.ic-assets.json5`, no SPA-exemption rule.
- **A real file beats the SPA fallback.** With the static-site `/*  /index.html  200` rewrite, the manifest is a real file, so it is served directly; the rewrite only catches paths with no matching file. (The *legacy* `@dfinity/asset-canister` resolves the same way — its `index.html` fallback likewise fires only when no file matches — but there the manifest has to be uploaded in the first place: `.ic-assets.json5` needs `{ "match": ".well-known", "ignore": false }`, or the hidden directory never ships. On a non-IC host, check that host's own routing precedence; where rewrites shadow real files, exempt `/.well-known/*`.)
- **Set the content type.** Extensionless files do not get `application/json` automatically. Add a `_headers` file (at the root of `dir`, e.g. via `public/_headers`) so the manifest is served as JSON:

```text
/.well-known/ic-architecture
  Content-Type: application/json
```

See the `static-site` skill for `_headers`/`_redirects` details.

## Layer 2: Interface — `candid:service`

Expose your Candid interface as the canister's public `candid:service` metadata — the standard IC mechanism, embedded by default by the `@dfinity/motoko` and `@dfinity/rust` recipes. It lets an agent fetch exact method signatures and types and encode/decode calls correctly. **Do not strip it** from the build.

An agent (or you, to verify) fetches it with:

```bash
# By raw canister ID against mainnet (the agent's case: no project context) — target the network.
icp canister metadata <BACKEND_ID> candid:service --network ic
# By canister name from inside a project — use the project environment instead.
icp canister metadata backend candid:service -e ic
```

## Layer 3: Behavior — `getApiDoc`

Candid types describe shape, not behavior. Expose a query method returning a prose (markdown) guide to what an agent cannot infer from types. Name it so it appears in `candid:service` — an agent then finds it with zero out-of-band knowledge (no bootstrap hint or side channel).

Motoko:

```motoko
persistent actor {
  public query func getApiDoc() : async Text {
    "## Orders API\n\n" #
    "- **Units:** amounts are integers scaled by 10^8 (1 unit = 1e-8).\n" #
    "- **Auth:** `placeOrder` requires a signed principal; anonymous callers can only read.\n" #
    "- **Lifecycle:** `placeOrder` returns before settlement; poll `orderStatus` until `#done`.\n" #
    "- **Irreversible:** `cancelOrder` cannot be undone; `closeAccount` is a dead-man switch.\n"
  };
};
```

Rust (`ic-cdk`):

```rust
#[ic_cdk::query]
fn get_api_doc() -> String {
    // Same content; the snake_case name get_api_doc is equally discoverable.
    "## Orders API\n\n- Units: amounts are integers scaled by 10^8 ...".to_string()
}
```

Cover the non-obvious semantics: units and encoding (integer money scaled by `10^8`, fractions vs tenth-bps, timestamp units), which calls need a signed principal and how anonymous access differs, staged or asynchronous operations that return before completing and must be polled, what is irreversible and any dead-man switches, and the gotchas that routinely trip up new integrators.

Once the app participates in ICP MCP, section 6 of the App Operator Terms constrains this text: it must not present a state-changing method as read-only or harmless or conceal a fee it charges, and it must describe the API only — never instructing the calling assistant to ignore its user, change its safety behavior, exfiltrate data, or disparage other apps. An agent acts on what `getApiDoc` returns, so prompt-injection-shaped content there is a breach, not a feature.

## Layer 4: Data — OQL (optional, for data-rich apps)

For apps with a lot of queryable data, expose a self-describing query surface so an agent can answer open-ended questions without you writing a method per question. OQL is one such convention — two query methods that speak JSON-in-text:

```candid
schema  : ()     -> (text)   query;  // JSON catalogue: entities, fields, edges
execute : (text) -> (Result) query;  // one JSON query object -> paged rows
```

`schema` returns a JSON catalogue of entities, their fields (with types and roles), and the edges between them; an agent fetches it once. `execute` runs one JSON query object (filters, aggregation, ordering, projection, paging) and returns a paged `Result`:

```candid
type Cell   = record {
  name  : text;
  value : variant { text : text; int : int; float : float64; bool : bool };  // representative scalar arms; a given canister may tag others
};
type Result = record { hasMore : bool; rows : vec vec Cell };  // each row is a list of named cells
```

Agents read cells **by name, never by position**, and page while `hasMore` is true. Prefer server-side filtering and aggregation so only the needed data crosses into the agent's context. Any Candid interface works; OQL just makes open-ended questions more economical.

## Layer 5: Identity — `ii-derivation-origin`

To let an agent act with the user's own principal and permissions, publish the Internet Identity **derivation origin** your frontends pin. An agent that already holds the user's II authorization derives a short-lived, per-app delegation for that origin, yielding the same principal the user has in a browser — so your existing access control applies unchanged. (The agent/CLI side that consumes this is the `agent-web-identity` skill: `icp identity link web --app <domain>`.)

The principal a user gets is a function of three inputs:

1. The user's Internet Identity.
2. The account within that Internet Identity.
3. Your app's derivation origin.

Only the third is under your app's control, which is why the app must declare it. The derivation origin defaults to the **visible** origin: the origin the user's agent was asked to act on (agentic flows) or the origin in the browser address bar (classical flows). Publishing the file matters when an app is reachable from more than one origin (e.g. a rebrand or a secondary frontend): the visible origin may then differ from the origin identities are derived for, and the file tells the agent which origin to request derivations for.

Publish, at each supported frontend origin, `/.well-known/ii-derivation-origin` whose body is the canonical `https://host` origin on a single line:

```text
https://hcv4s-uaaaa-aaabq-qaaba-cai.icp.net
```

- If the derivation origin is just the app's own visible origin, you may omit the file; its absence means "derive for the visible / requested origin itself."
- Generate it at deploy time with the same `presync` pattern when the origin is a per-network canister URL; for a custom domain it is a one-line static file (e.g. `public/.well-known/ii-derivation-origin`).
- **Do not confuse it with `ii-alternative-origins`.** A custom origin is enabled by two coupled files: the app pins `derivationOrigin` in its II configuration, and the derivation origin itself publishes `/.well-known/ii-alternative-origins` listing the origins allowed to derive against it. That list is the inverse relation — "who may point here," not "where does this app point" (Pitfall 8). On the default `*.icp0.io` / `ic0.app` canister origins, do **not** set a custom `derivationOrigin` at all (the `internet-identity` skill's Mistake #8 explains why it breaks auth); a custom one goes hand in hand with a custom domain — see the `custom-domains` skill.

## How an Agent Traverses This

Published independently, the layers are consumed in one order — each step exists to let the agent skip work at the next:

1. `GET /.well-known/ic-architecture` → every canister ID, and which one to call, from whichever labels identify it (`name`, `role`, `description`).
2. `candid:service` on that canister → exact signatures and types, plus the names `getApiDoc` / `schema` / `execute`, which is why those must live in the interface and not a side channel.
3. `getApiDoc()` → the semantics the types cannot carry, including **which calls need a signed principal**.
4. `/.well-known/ii-derivation-origin`, or the visible origin when absent → derive the user's delegation and act as the signed-in user, so existing access control applies unchanged.
5. `schema()` once, then `execute(...)` per question, filtered and aggregated server-side.

The identity step is numbered 5 as a layer but happens **before the first protected call**: step 3 is where the agent learns which methods require a signed principal, so anything gated — a protected `execute`, or any update call — has to wait for the delegation. Only unauthenticated reads can run ahead of it.

Steps 1-3 take an agent from a bare URL to a correctly-encoded, correctly-understood call in three round trips. Each layer left unpublished replaces one of them with guessing — an unlabeled manifest alone costs a `candid:service` fetch per canister (Pitfall 10).

## Deployment Checklist

- [ ] **Terms accepted:** the app's **operator** — not a developer or agent acting for them — has read the [ICP MCP App Operator Terms](https://internetcomputer.org/icp-mcp/app-operator-terms/) and confirmed, *before* the manifest ships. Publishing it is the acceptance; there is no separate step.
- [ ] **Registration (optional):** if the operator wants notices and a record of who accepted which version, they email `mcp@dfinity.org` with the details in **Before Layer 1**, including the app's own privacy-policy URL.
- [ ] **Composition:** the deploy pipeline emits `/.well-known/ic-architecture` (real JSON, extensionless path) with real per-environment canister IDs.
- [ ] **Content type:** a `_headers` rule serves the manifest as `application/json`.
- [ ] **Reachability (non-static-site hosts only):** `/.well-known/ic-architecture` actually resolves. Automatic on the static-site canister; on the legacy `@dfinity/asset-canister` the directory needs an `.ic-assets.json5` un-ignore rule to be uploaded at all; on a non-IC host, exempt `/.well-known/*` from the SPA catch-all if that host's rewrites shadow real files.
- [ ] **Interface:** `candid:service` metadata is present (not stripped).
- [ ] **Behavior:** the backend exposes `getApiDoc` / `get_api_doc` returning markdown.
- [ ] **Data (if applicable):** data-rich canisters expose OQL `schema` + `execute`.
- [ ] **Identity (if custom):** publish the effective origin in `/.well-known/ii-derivation-origin` (canonical `https://host`, one line).

## Verify (Acceptance Tests)

Run against the deployed origin (`APP` = your frontend host):

```bash
# 1. Manifest is real JSON listing the canisters (not the SPA shell).
curl -s https://APP/.well-known/ic-architecture | jq '.canisters[].id'

# 2. Backend exposes candid:service; fetch it against a canister ID from step 1
#    (confirm it declares getApiDoc, plus schema/execute if data-rich).
icp canister metadata <BACKEND_ID> candid:service --network ic

# 3. If you pin a CUSTOM derivation origin, it is published as the canonical
#    https://host. Use -f so a 404 is an error and the fallback fires: curl -s
#    alone exits 0 on 404, so the "default" branch would never run.
curl -sf https://APP/.well-known/ii-derivation-origin || echo "default (https://APP)"
```

Locally, the static-site recipe serves the same paths — e.g. `curl http://frontend.local.localhost:8000/.well-known/ic-architecture`.

## Pitfalls

1. **Hard-coding canister IDs.** IDs differ per network, so committing them ships a manifest that is wrong on every environment but the one it was written for. Generate at deploy time in `presync`.

2. **Putting ID resolution in `build` instead of `presync`.** `build` runs *before* the canisters exist, so no IDs are available (`ICP_CLI_CID_*` are unset and `icp canister status` has nothing to return). Only `presync` runs after creation with IDs available.

3. **Assuming the manifest is served, without setting its content type.** The extensionless file is served, but not as `application/json` unless a `_headers` rule says so. Add the `Content-Type: application/json` block above.

4. **Expecting `.ic-assets.json5` to matter.** That is the *legacy* asset canister's config; the static-site (certified-assets) canister ignores it. `.well-known/` is uploaded automatically and needs no un-ignore rule. The legacy canister is the reverse: it needs `{ "match": ".well-known", "ignore": false }` or the directory is never deployed — an upload problem, not a routing one.

5. **Writing the file with a `.json` extension.** The path is exactly `/.well-known/ic-architecture` (and `/.well-known/ii-derivation-origin`) — no extension, matching the IC `.well-known` convention (`ic-domains`, `ii-alternative-origins`).

6. **`envsubst` clobbering unintended `${...}`.** With no arguments `envsubst` substitutes *every* environment variable it finds. If a template contains a `${...}` you do not want replaced, restrict it: `envsubst '$ICP_CLI_CID_FRONTEND $ICP_CLI_CID_BACKEND'`.

7. **A missing `tmpl.<env>.json`, or templates in the wrong directory.** `$ICP_CLI_ENVIRONMENT` selects the template by name; if the file for the current environment is absent — or lives at the repo root while `presync` runs from the canister directory — `envsubst` reads nothing and writes an empty manifest. Keep one template per environment, under the frontend canister directory.

8. **Reading `ii-alternative-origins` to find the derivation origin.** It is the inverse relation (who may derive against this origin), not a pointer to it. There is no reverse lookup; using it backwards **silently** yields the wrong principal — a plausible wrong answer, not an error. Publish and read `ii-derivation-origin` for the forward fact.

9. **Naming the behavior method undiscoverably.** The name must appear in `candid:service`, so use `getApiDoc` / `get_api_doc`. A method reachable only via an out-of-band hint defeats zero-knowledge discovery.

10. **Listing canisters without labels that identify them.** `id` is the only required field, so a manifest of bare IDs is valid, and it still earns its keep: the agent gets the app's canisters without discovering them out of band. What it loses is the routing — with nothing to tell the backend from the frontend, the agent pays a `candid:service` fetch per entry and infers roles from method names. Label every entry with whatever identifies it (`name` is often enough; add `role`, and `description` where the purpose is not obvious from the name).

11. **Stripping `candid:service`.** Some minified/size-optimized builds drop wasm metadata. Keep it — it is what makes the interface fetchable. Verify with `icp canister metadata <id> candid:service --network ic`.

12. **Publishing the manifest without asking the operator.** The likeliest agent failure here is treating `/.well-known/ic-architecture` as ordinary build config and adding it unprompted. It is the act that accepts the [ICP MCP App Operator Terms](https://internetcomputer.org/icp-mcp/app-operator-terms/) and opts the app into query and update calls from AI assistants. Confirm with the user first, and confirm they are the **operator** — section 1 says a developer who does not operate the app cannot accept for its operator.

13. **Mistaking registration for the opt-in, or for the opt-out.** Registration is optional and changes nothing about participation: an unregistered app whose manifest is published is fully participating and fully bound. Registration only tells DFINITY who accepted, which version, and where to send notices. Symmetrically, there is nothing to "unregister" to stop participating — **removing the manifest** is the off switch. Removing it deactivates participation; *terminating the agreement* is a separate act, a notice to `mcp@dfinity.org` (section 11). Neither undoes calls already executed on the Internet Computer, and sections 8, 12, 13 and 15 — personal data, warranties, liability and governing law — survive termination. "Delete the file and you are done" is wrong, not merely incomplete.

14. **Expecting manifest removal to delist the app entirely.** Deleting it stops new metadata reads and query/update calls once ICP MCP observes the removal, but ICP MCP may still fetch the app's public website and describe publicly available information. To be dropped from user-facing presentation, the operator asks DFINITY at `mcp@dfinity.org`.

15. **Declaring canisters the operator does not control.** It is tempting to list a third-party ledger or an ecosystem canister the app merely calls. Serving the manifest is a repeated representation (section 5) that **every** declared canister is operated by the operator or under their authority, and it makes those canisters eligible for update calls under the app's participation. List only your own.

## Additional References

- Load `static-site` for the `@dfinity/static-site` recipe: `presync`/`build`, `_redirects`/`_headers`, `.well-known/` auto-upload, and canister-ID injection.
- Load `agent-web-identity` for the agent/CLI side that *consumes* the derivation origin (`icp identity link web --app <domain>`).
- Load `internet-identity` for adding II sign-in to a frontend (it also explains when *not* to set `derivationOrigin`).
- Load `custom-domains` for serving from your own domain, which then becomes your derivation origin.
- Load `icp-cli` for `icp.yaml` / `canister.yaml`, environments, and the recipe system.
- Load `canister-security` for access control on the methods agents call.
- Authoritative human guide: [Service discoverability](https://docs.internetcomputer.org/guides/frontends/service-discoverability/).
- The terms publishing the manifest accepts: [ICP MCP App Operator Terms](https://internetcomputer.org/icp-mcp/app-operator-terms/), and what ICP MCP is: [ICP MCP](https://internetcomputer.org/icp-mcp/).
- What ICP MCP discloses to a participating app, and what it processes on registration: [ICP MCP Privacy Policy](https://internetcomputer.org/icp-mcp/privacy-policy/).
- Candid interface reference for the typed interface agents read: [Candid interface](https://docs.internetcomputer.org/guides/canister-calls/candid/).
- Community example of the Layer 1 generation (a personal repo — illustrative, not a stable dependency): [`raymondk/demo-ic-architecture`](https://github.com/raymondk/demo-ic-architecture/tree/main/frontend/ic-architecture).
