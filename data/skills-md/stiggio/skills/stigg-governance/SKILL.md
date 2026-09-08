---
name: stigg-governance
description: Use for per-entity budget and spend-control work in Stigg Governance — enforcing usage limits over whatever hierarchy of sub-units a customer needs to budget (the entity model is customer-defined, not fixed) — defining entity types with attribution keys, building the customer's own tree, assigning limits per entity for a feature or credit currency, dimensional scoping, querying the governance tree for balances, and runtime enforcement. Triggers include "per-entity budget", "per-team spend limit", "per-agent token cap", "cost center limits", "sub-customer limits", "per-project budget", "entity type", "attribution keys", "governance tree", "budget enforcement", "scoped assignment", "GovernanceNotEnabled", "keep entities in sync", "re-parent entity", "CannotReportUsageForEntitlementWithMeterError". Skip for account-level credit grants / pools / ledger (stigg-credits), feature gating with no entity hierarchy (stigg-entitlements), or catalog modeling (stigg-pricing-modeling).
---

# Stigg Governance — Per-Entity Budget Enforcement

Governance layers **per-entity budget enforcement** on top of Stigg credits and features. Where credits answer "how much can this *customer* consume?", governance answers "how much can this customer's *own sub-units* consume?" — whatever the vendor needs to budget, with hierarchical roll-up and hard-limit enforcement. **The entity model is arbitrary and customer-defined** — Stigg imposes no fixed hierarchy, so don't assume one (see Step 1).

You drive Stigg governance **through the Stigg MCP** — the `execute` tool runs SDK code, `search_docs` resolves exact shapes. That's how the agent explores, configures, and test-checks governance: entity types, entities, assignments, tree queries, and one-off checks all go through `execute` using the SDK's beta namespace (e.g. `client.v1Beta.…`). **Production runtime enforcement is separate:** the live entitlements check that gates real customer requests runs on the vendor's **hot path via the Stigg SDK/edge**, not through the MCP — the MCP is for agent-side setup and exploration, not the request-time gate. This skill owns the *mental model*; it does not cover connection, keys, or setup — those belong to the **`stigg-mcp`** skill.

> **Private-beta surface.** Governance is currently a **private-beta** part of the Stigg API. Its shape may change at GA, so **re-check exact routes and field names via `search_docs`** rather than treating anything here as permanent.

## Step 0 — Preflight: Is Governance Enabled? (do this FIRST)

Run ONE probe via the MCP `execute` tool: `client.v1Beta.entityTypes.list()` (no customer id needed).

- Fails with error `code` **`GovernanceNotEnabled`** → **STOP.** Tell the user to contact Stigg to enable Governance. Do not retry or work around it.
- Succeeds → proceed to Step 1. An empty list is expected — nothing is configured yet.

## Step 1 — Elicit the Model: ASK, Don't Assume (do this BEFORE defining entity types)

**The governance entity model is fully arbitrary and customer-defined.** There is **no default hierarchy** — Stigg ships none, and any dept/team/agent shape is just *one* possibility, not a template. Before defining a single entity type, **ask the customer what they want to govern** and build strictly from their answer. Do **not** propose or assume a hierarchy. Ask:

- **What units do you budget?** (their own vocabulary — teams, projects, regions, tenants, sub-accounts, cost centers, agents, workspaces…)
- **How do they nest / roll up?** (which contains which, and how deep — the tree caps at 4 levels)
- **Which levels actually carry budgets?** (only levels that hold a limit or need roll-up belong in the tree; fold the rest away)
- **What identifies a unit on a usage event?** (the dimension key(s) your events already emit — these become the attribution keys, max 2 per type)

Model from their answer: "we budget by project, and projects belong to a client" → build `client → project`. Every worked example below and in the references is *one possible model* — it teaches the API's *shape*, never the model to adopt.

**Sequence:** preflight (Step 0) → elicit the model (this step) → entity types → entities → assignments → runtime.

## Prerequisites — depend on what you're budgeting

Governance budgets sit *on top of* an existing feature or credit currency; they don't replace it. **What's required differs for a feature vs. a credit currency** — the two follow different paths, so read the row that matches your assignment (`featureId` or `currencyId`).

- **Feature (`featureId`) — needs an entitling active subscription.** The gating check only reaches the governance chain when the customer has an **ACTIVE subscription that entitles the feature** — otherwise it short-circuits with a standard denial (`NoActiveSubscription`; `NoFeatureEntitlementInSubscription` = subscribed but the plan lacks the feature) and never consults the tree. **Entitle the feature via an active subscription BEFORE checks can pass.** Assignment upsert does **no** entitlement validation — it accepts a budget for an un-entitled feature, so the gap surfaces only later at check time. Order it: catalog + subscription first (see `stigg-pricing-modeling` / `stigg-subscriptions`), then budgets.

- **Credit currency (`currencyId`) — does NOT require a subscription.** Credits run on a different path: the check reads the customer's **credit pool** directly, and credits can be granted and consumed with **no active subscription or assigned plan**. What a credit budget needs instead is a **credit currency that exists and a funded pool** (a grant — recurring, prepaid, promotional, or manual). Set the currency up via **`stigg-credits`**, then add per-entity budgets.

Setting up a feature catalog (plan, feature, subscription — a FREE plan needs `charges.pricingType` before publishing) is **not** governance's job: do it via **`stigg-pricing-modeling`** (catalog) and **`stigg-subscriptions`** (provisioning); credit currencies and grants live in **`stigg-credits`**. Then add per-entity budgets.

## Before You Start

Per the umbrella `stigg` skill: **search first.** Governance is a private-beta surface whose shape may change — confirm operation names, field names, and body shapes via `search_docs` (or the Mintlify Stigg docs MCP) before authoring. This skill owns the mental model; the live surface owns the shapes.

## The Four Pieces

`entity type → entity → assignment → governance tree` — a **type** (which declares the attribution keys) is defined **once per environment** and instantiated **per customer** as **entities**; an **assignment** budgets one `(entity, featureId|currencyId)` pair; the **tree** reports usage-vs-budget and never gates. Each is detailed below.

## Entity Types

An **entity type** declares a kind of sub-customer unit — whatever the customer named in Step 1 (a project, region, tenant, cost center, agent, …) — and, critically, its **attribution keys**: up to **2** event-dimension keys whose values identify which entity a usage event belongs to. An entity type is **defined once per environment** and shared across every customer in that environment. Operations: **list** and **upsert** (bulk `PUT`, idempotent). Design attribution keys before reporting any usage; retro-attributing old events is not a thing.

## Entities

**Entities** are the instances of those types, **created per customer** (under a customer) — many per customer, up to **4 levels** deep, in whatever shape Step 1 surfaced (e.g. `client → project`, or `region → tenant → workspace`). To **place or move a node in the tree, set `parentId` on the `upsertAssignment` operation** (`client.v1Beta.customers.assignments.upsert`) — tri-state: **omit** = leave the parent unchanged, **`null`** = make it a root, an **entity id** = set/change it. `parentId` is the entity's **single parent** (one position per entity), set on the assignment, not per feature/currency. (Practical note: the *entity* upsert rejects `parentId`, and `metadata` has no structural role, so parenting happens on `upsertAssignment`.) Operations: **list / get / upsert (bulk `PUT`) / archive / unarchive**. **Re-parenting is leaf-only** (a non-leaf move is rejected); **archive is NOT leaf-gated** — archiving a parent orphans its still-active children, so archive/re-home descendants bottom-up yourself. Full rules: `references/entity-model.md`.

## Keeping Entities in Sync

Entities are an **ongoing mirror of the vendor's source of truth**, not a one-time import — the hierarchy lives in your system first; the tree is a projection. Wire governance ops into the code paths that mutate your model: **register → entity upsert; rename/attribute-change → idempotent re-upsert; deprovision/delete → archive (bottom-up); restructure → set `parentId` on the entity's `upsertAssignment` to move the node (leaf-only)**. Since upsert is idempotent bulk `PUT`, a declarative "push the desired tree each sync" pattern works. Full mapping + the unshipped allocation-return caveat: `references/entity-lifecycle.md`.

## Assignments — the Budgets

An **assignment** sets a limit for one `(entity, featureId|currencyId)` pair:

- `entityId` — The entity being budgeted (any level of the customer's tree).
- `featureId` **or** `currencyId` — What's being limited — exactly one: a **`featureId`** (metered feature) **or** a **`currencyId`** (credit currency). Mutually exclusive.
- `usageLimit` — The budget for the cadence window.
- `cadence` — A **single-unit** ISO-8601 duration for the reset window, e.g. `'P1M'` (monthly) or `'P10D'` (every 10 days). It must be one unit only — a composite like `'P1M10D'` (1 month *and* 10 days) is **not** allowed.
- `scopeEntityIds` — Optional — defines a dimension-scoped sub-budget; it narrows **when** the budget applies. `[]` (empty) = a node-wide budget that always applies. Non-empty (e.g. `['model-gpt4o']`) = the budget applies only when every listed entity is present in the request's resolved set (the ancestors + dimension matches from attribution). Use it instead of everything under the assignee for specific (typically dimensional) entities.

Operations: **list / upsert**. A `currencyId` assignment budgets *credit consumption* — unrelated to billing currency (USD/EUR). Worked examples: `references/assignments.md`.

## Reporting Usage — the Meter-Type Fork

Ingest never gates; it records consumption and rolls up the tree. **The endpoint depends on the target feature's meter type:**

- **Calculated / incremental meters** (your app computes the number) → **`client.v1.usage.report`**: synchronous, echoes `currentUsage`. Required: `customerId`, `featureId` (feature OR credit id), `value`.
- **Raw-events meters** (Stigg aggregates raw events — count/sum/unique) → **`client.v1.events.report`** (reportEvent): the **required** path for these today (`usage.report` cannot report raw-events–metered features — use `events.report`/reportEvent instead); high-volume, eventually-consistent. reportEvent has **no `featureId`** — the meter is matched by **`eventName`** (+`idempotencyKey`).

Both carry attribution in **`dimensions`** (the entity type's attributionKey values, e.g. `{ "projectId": "proj-atlas", "regionId": "eu-west" }`) → attributes to the matching entity **and every ancestor**.

> **Read the feature's meter to pick the path.** The Feature type exposes `hasMeter` / `meter` / `meterType` — inspect the `meter` config to tell a raw-events meter (→ `events.report`) from a calculated/incremental one (→ `usage.report`). Note `meterType` alone doesn't flag "raw events" (a raw-events feature can read `INCREMENTAL`), so read the `meter` config and confirm fields via `search_docs`. Keep a definitive fallback: on **`CannotReportUsageForEntitlementWithMeterError`** from `usage.report`, it's a raw-events meter — switch to `events.report`. Shapes + examples: `references/enforcement-and-usage.md`.

## Enforcement and Balances

Two distinct reads — do not mix them up. This is the **hot-path (enforcement) vs cold-path (observability)** split; the full framing is in `references/enforcement-vs-observability.md`:

1. **Access (gates requests):** the standard entitlements **check** — `client.v1Beta.customers.entitlements.check`, passing `featureId` **or** `currencyId`, optional `requestedUsage` (default 1), and attribution `dimensions`. When governance is enabled, the governance chain enriches the check. **An entity is blocked when ANY ancestor has hit its hard limit** — a child with budget left is still blocked if any of its parents is exhausted. A **feature** (`featureId`) check also needs an entitling active subscription; a **credit** (`currencyId`) check does not (see Prerequisites).
2. **Balances (observability):** the **governance tree query** — the `retrieveGovernance` operation — returns the entity nodes; remaining budget = `usageLimit − currentUsage`. **By default it runs tree-only: `usageLimit` / `currentUsage` / `utilization` / `cadence` come back `null`;** pass `featureIds` and/or `currencyIds` params (repeat for multiple) to hydrate config + usage for those features / credit currencies. The read model **may lag by minutes** — use it for dashboards and alerts, **never** to gate access. Full semantics: `references/enforcement-and-usage.md`.

## Surface Map

Operations run through the MCP `execute` tool as `@stigg/typescript` SDK calls (bulk upserts are idempotent). Each operation → its SDK call (via MCP `execute`):

- **Entity types — list / upsert (bulk)** — `client.v1Beta.entityTypes.*`
- **Entities — list / get / upsert (bulk) / archive / unarchive** — `client.v1Beta.customers.entities.*`
- **Assignments — list / upsert** — `client.v1Beta.customers.assignments.*`
- **Entitlements check (not gated by governance enablement — it still gates access)** — `client.v1Beta.customers.entitlements.check`
- **Governance tree query (pass `featureIds` / `currencyIds` to hydrate)** — `client.v1Beta.customers.retrieveGovernance(id, { ... })`
- **Ingest — calculated/incremental meter** — `client.v1.usage.report`
- **Ingest — raw-events meter (by `eventName`)** — `client.v1.events.report`

Don't guess operation names or shapes — confirm exact operations via `search_docs`.

**API vs UI — different assignment models, by design.** The API targets **one feature or credit currency per assignment** (`(entity, featureId|currencyId)`). The dashboard UI intentionally **auto-creates an unlimited assignment across ALL of the entity's features and credit currencies** (you edit limits per row). So UI- and API-created entities look different — don't be surprised, and don't "repair" one to match the other.

**Via the Stigg MCP:** the MCP exposes only **`execute`** (sandboxed TypeScript over the SDK) and **`search_docs`** — no one-tool-per-endpoint mapping. Governance ops go through `execute` using the SDK namespaces above. Connection, keys, and environment setup are the **`stigg-mcp`** skill's job — if `execute` or `search_docs` won't connect, that's where the troubleshooting lives, not here.

## When NOT to Use This Skill

- Account-level credit currencies, grants, pools, ledger, auto-recharge → `stigg-credits`.
- Feature gating / usage reporting with no per-entity budgets → `stigg-entitlements`.
- Modeling features / plans / credit currencies in the catalog → `stigg-pricing-modeling`.
- Provisioning / canceling subscriptions → `stigg-subscriptions`.

## Common Mistakes

Each mistake — the fix:

- Retrying after `GovernanceNotEnabled` — It's an account-level enablement state (governance isn't enabled for this account), not a transient error. Tell the user to contact Stigg; stop.
- Treating an empty 200 as "not enabled" — Empty = enabled but unconfigured. Proceed to model.
- Gating access from the tree query — The tree is a read model that may lag by minutes. Gate with the entitlements check only.
- Debugging "child has budget but is blocked" as a bug — Ancestor semantics: any exhausted ancestor blocks the whole subtree. Check the tree upward.
- Defining more than 2 attribution keys, or >4 hierarchy levels — Hard limits. Redesign the model (e.g. fold a level into `scopeEntityIds`).
- Reporting usage without attribution-key dimensions — Usage won't attribute to any entity — budgets never accrue. Design dimensions up front.
- Always calling `usage.report`, or always `events.report` — It's a meter-type fork. Calculated/incremental → `usage.report`; raw-events → `events.report` (reportEvent, by `eventName`). If `usage.report` returns `CannotReportUsageForEntitlementWithMeterError`, switch to reportEvent.
- Passing a `featureId` to reportEvent — reportEvent targets the meter by `eventName` (+`idempotencyKey`), not `featureId`; attribution rides in `dimensions`.
- Creating a **feature** (`featureId`) assignment and expecting checks to pass — Assignment upsert does no entitlement validation. The feature must be entitled via an active subscription first, else check denies with `NoActiveSubscription`/`NoFeatureEntitlementInSubscription`.
- Assuming a **credit** (`currencyId`) budget needs a subscription like a feature does — It doesn't — credits are a different path. The check reads the credit pool directly; credits can be granted/consumed with no subscription. It needs a credit currency + funded pool, not a subscription (`stigg-credits`).
- Reading the tree and getting `null` limits/usage — Tree-only mode. Pass `featureIds`/`currencyIds` to hydrate config + usage.
- Treating an MCP connection error as a governance problem — Connection/setup issues (bad key, wrong environment) are `stigg-mcp`'s domain — fix them there, then re-run the governance op.
- Re-parenting a node that still has children — Re-parent is leaf-only — a non-leaf move is rejected. Move/archive children first, then move the former parent. The rejection is not transient, so don't retry it.
- Assuming archive is leaves-only — It isn't — archiving a parent orphans its active children. Archive/re-home descendants bottom-up yourself; the platform won't stop you.
- Putting `parentId` on the entity upsert (or in `metadata`) — The entity upsert rejects `parentId`, and `metadata` has no structural role. Set `parentId` on the `upsertAssignment` operation to place/move the node.
- Treating entities as a one-time import — They're an ongoing mirror of your source of truth — wire upsert/archive/re-parent into your create/update/delete/restructure paths (`references/entity-lifecycle.md`).
- Reading `currencyId` as a billing currency — It's a credit currency (see `stigg-credits`), not USD/EUR.
- Expecting per-endpoint MCP tools for governance — The MCP has only `execute` + `search_docs`. Drive the SDK through `execute`.
