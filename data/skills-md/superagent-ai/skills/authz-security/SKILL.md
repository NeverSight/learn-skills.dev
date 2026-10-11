---
name: authz-security
description: Review application source code for broken authorization — IDOR / Broken Object Level Authorization (OWASP API1), Broken Function Level Authorization (API5), mass assignment (API3), multi-tenant isolation gaps, and privilege escalation. Reads routes, controllers, resolvers, and data models offline and reports the missing ownership/role check at file:line with a framework-correct fix. No running app, no credentials, no tools. Trigger when reviewing endpoints/handlers, auditing a PR diff that adds or changes routes, hardening a multi-tenant SaaS, or when the user asks "is this endpoint authorized?", "can a user access another user's data?", "IDOR", "BOLA", or "broken access control".
---

# Authorization Security Scanner

This skill turns the model into an authorization reviewer. Read the routes, controllers, resolvers, and data models; walk the detection passes; report each missing access-control check with a severity and a concrete, framework-correct fix. No tools to install, no app to run, no credentials — the analysis is the model reading the code.

Broken access control is the OWASP Top 10's #1 web risk (A01) and the top two API risks (API1 BOLA, API5 BFLA). It tops the lists precisely because automated tools miss it: there is no dangerous function call to grep for. The bug is the **absence** of a check, and confirming it requires understanding the application's ownership model — which is exactly what a model reading the code can do and a signature scanner cannot.

## Mental model

Authentication answers *who are you?* Authorization answers *are you allowed to do this, to this specific object?* This skill is only about the second question. A handler can be perfectly authenticated and still be a critical vulnerability.

Every privileged operation can be escalated along two axes:

- **Horizontal** — acting on another user's object at the same privilege level. Manipulate an object identifier (`/orders/1042` → `/orders/1043`) and you read someone else's data. This is **BOLA / IDOR** (OWASP API1).
- **Vertical** — reaching a function above your privilege level. A normal user hitting an admin endpoint. This is **BFLA** (OWASP API5).

The defect is almost always *missing code*, not *wrong code*: a query that filters by object id but not by owner, an admin route guarded by "is logged in" but not "is admin," a body that binds straight to a model. So you are scanning for a **gap**, not a pattern.

**When you cannot tell whether a check exists, assume it does not, and flag it for confirmation.** The cost of a false positive is a review comment. The cost of a false negative is every user's data. This asymmetry governs every judgment call below.

## Scan procedure

Walk these passes in order. Pass 0 builds the context the rest depend on — do not skip it.

### Pass 0: map the ownership and tenancy model

You cannot tell that a check is missing until you know what "owning" an object means here. Before reading a single endpoint, read the data layer — ORM models, schema, migrations — and establish:

- **For each resource, who owns it?** Look for an owner/scope column: `user_id`, `account_id`, `org_id`, `tenant_id`, `team_id`, `workspace_id`. A resource with such a column must never be returned or mutated without scoping to it.
- **What is the principal?** Where does the authenticated identity come from — `request.user` from a session, `req.user` set by auth middleware, a verified JWT `sub` claim? This is the *only* trustworthy identity. Note it.
- **What is the tenancy strategy?** Row-level (shared tables with a `tenant_id` column) is where almost all multi-tenant BOLA hides, because isolation depends on every single query remembering the filter. Schema- or database-per-tenant pushes the boundary lower and is harder to get wrong.

Write this map down (even informally). Every later finding is "principal P touched object O without confirming P may access O" — you need to know O's owner to make the call.

### Pass 1: enumerate handlers and the objects they touch

List every entry point: REST routes, controller actions, GraphQL resolvers, RPC/gRPC methods, server actions. For each, record:

- HTTP method + path (or resolver name).
- The object(s) it reads or mutates.
- **Where the object identifier comes from**: path param, query string, request body, or the session/token.

Flag every handler that loads or mutates an object **by a client-supplied identifier** — those are the BOLA candidates for Pass 2. A handler that only ever uses the principal's own id from the session (`GET /me`, `current_user.orders`) is low risk and can be deprioritized.

### Pass 2: object-level authorization (BOLA / IDOR) — OWASP API1

For every handler flagged in Pass 1, ask: **is there a check that the principal owns or may access this specific object?** An acceptable check takes one of three forms:

1. **Owner-scoped query** — the lookup itself includes the owner, so a non-owned id simply isn't found:
   ```python
   invoice = Invoice.objects.get(id=id, org=request.user.org)   # 404 on someone else's
   ```
2. **Explicit post-load check** — load, then compare to the principal and reject:
   ```python
   invoice = Invoice.objects.get(id=id)
   if invoice.org_id != request.user.org_id:
       raise PermissionDenied
   ```
3. **Centralized policy / ability** — a guard that encodes the rule: `authorize! :read, invoice` (Pundit/CanCanCan), `@PreAuthorize("hasPermission(#id,...)")`, an OPA/Cedar/OpenFGA decision, a policy gate.

If the object is loaded by a client-supplied id with **none** of these — only the id, on the assumption that "you had to be logged in to get here" — that is the canonical IDOR. **Authentication is not authorization.**

```javascript
// [P0] BOLA — Express: looks up by id, never checks ownership
app.get("/api/orders/:id", requireAuth, async (req, res) => {
  const order = await Order.findByPk(req.params.id);
  res.json(order);
});

// Fixed — scope to the authenticated principal
app.get("/api/orders/:id", requireAuth, async (req, res) => {
  const order = await Order.findOne({
    where: { id: req.params.id, userId: req.user.id },
  });
  if (!order) return res.sendStatus(404);
  res.json(order);
});
```

Severity: **P0** for a sensitive read or any write/delete reachable by any authenticated user; **P1** if the id space is large and unguessable *and* the data is low-sensitivity (still a finding — unguessable ids leak).

### Pass 3: function-level authorization (BFLA / vertical) — OWASP API5

Endpoints that perform privileged actions — user management, role changes, admin dashboards, data exports, billing, internal tooling, feature flags — must check the principal's **role or permission**, not merely that they are authenticated.

Flag:

- An `/admin/*` route or a privileged action guarded only by an authentication middleware, with no role/permission assertion in the handler or its middleware chain.
- Role checks performed only in the frontend (a hidden button) while the API endpoint is open.
- "Hidden" admin endpoints relying on obscurity — undocumented paths with no guard.

```python
# [P1] BFLA — authenticated, but any user can promote anyone to admin
@router.post("/users/{id}/role")
def set_role(id: int, body: RoleIn, user=Depends(current_user)):
    User.objects.filter(id=id).update(role=body.role)

# Fixed — assert the privilege
@router.post("/users/{id}/role")
def set_role(id: int, body: RoleIn, user=Depends(current_user)):
    if not user.is_admin:
        raise HTTPException(403)
    User.objects.filter(id=id).update(role=body.role)
```

### Pass 4: mass assignment / excessive property binding — OWASP API3

When a handler binds the whole request body to a model — `User.update(req.body)`, `Model(**request.data)`, `user.update_attributes(params[:user])`, `Object.assign(entity, req.body)` — ask which fields the client should *not* control: `role`, `is_admin`, `is_verified`, `email_verified`, `owner_id`, `org_id`, `tenant_id`, `balance`, `price`, `status`. If any reachable, the client escalates privilege or moves objects between tenants by adding a field.

Fix: allowlist the writable fields explicitly — strong params, a serializer/DTO with named fields, a Pydantic model scoped to inputs. Never bind a raw body to a persistence model.

### Pass 5: trusting client-supplied identity

The principal — and the tenant — must be derived server-side from the session or a verified token, **never** from a client-controlled value. Flag any of these used for an authorization decision or query scoping:

- `user_id` / `account_id` / `org_id` read from the **request body, query string, path, or a custom header** (`X-User-Id`, `X-Tenant`).
- A JWT claim trusted **without** verifying signature, issuer, audience, and expiry.

```javascript
// [P0] — scopes by a query param the caller controls
app.get("/api/invoices", requireAuth, async (req, res) => {
  res.json(await Invoice.findAll({ where: { userId: req.query.userId } }));
});
// Fixed: scope by the session principal, ignore client-supplied identity
//   where: { userId: req.user.id }
```

### Pass 6: consistency and edge surfaces

Authorization bugs cluster where coverage is uneven. Check each:

- **Sibling verbs.** `GET /orders/:id` checks ownership but `PUT`/`PATCH`/`DELETE` on the same resource don't (or the reverse). Verify *every* method, not just read.
- **Nested resources.** `/orgs/:orgId/projects/:projectId` — is the parent→child link verified (does the project actually belong to the org, and the user to the org)? A common bug checks the leaf and trusts the path prefix.
- **Batch / bulk endpoints.** They accept an array of ids — the check must run on *every element*, not the first. Same for GraphQL aliased queries.
- **List / collection endpoints.** `GET /invoices` has no id to swap, so it's easy to forget it must be scoped to the tenant. An unscoped list leaks the whole table — often a worse P0 than a single-object IDOR.
- **GraphQL.** `node(id:)` / global object identification and every field resolver that loads a related object must enforce authorization per resolver; checking only the query root is insufficient.
- **Newly added endpoints in a diff.** A `v2` route, a fresh controller action, a new field resolver — these are exactly where the guard was forgotten. Treat any new object-by-id handler in a diff as an automatic Pass-2 review.

### Pass 7: indirect or non-controls

Things that resemble authorization but are not. Each of these, when it is the *only* thing between users, carries the same severity as the missing check it is standing in for:

- **Middleware/route ordering.** Relying on registration order so a guard runs first — trivially broken when a route is later added above it, or when a framework matches a more specific route first.
- **Frontend-only enforcement.** Button hidden, SPA route guarded, while the API behind it is open.
- **Secret identifiers.** UUIDs or slugs as the *only* control. IDs leak via logs, `Referer` headers, error messages, and API responses, and UUIDv1 is partly predictable. Unguessable ids are defense-in-depth, never the check (**P3** when authz is otherwise correct).
- **Default-allow config.** A framework default that permits when no rule matches: a missing `permission_classes`, Spring `permitAll()`, a catch-all route, a policy engine queried but whose default decision is allow.

## Finding format

Report each finding in this structure. Group by severity, P0 first.

```
[P0] bola in app/controllers/orders_controller.rb:42
  #show loads Order by params[:id] with no ownership check. Any authenticated
  user can read any order by changing the id (sequential integers).
  Principal: current_user. Order belongs to a user via user_id.

  Vulnerable:
    def show
      @order = Order.find(params[:id])
    end

  Fix (scope the lookup to the owner; 404s on non-owned ids):
    def show
      @order = current_user.orders.find(params[:id])
    end
```

If the user pastes a snippet without a path, refer to "the handler" and use line numbers within the snippet. Always name the object, its owner, and the principal — that triad is the proof the check is missing.

## Severity scale

- **P0** — exploitable now by any authenticated (often any unauthenticated) user, no chain: a missing object-level check on a sensitive read or any write/delete, an admin function reachable by a normal user, an unscoped collection endpoint, or scoping keyed on client-supplied identity. Block merge.
- **P1** — missing role check on a less-sensitive action, mass assignment of a privilege/tenant field, or a BOLA gated only by a large unguessable id space. Block merge on anything that touches other users' data.
- **P2** — uneven coverage not yet exploitable: one verb scoped and a sibling ambiguous, tenant scoping present but fragile, a check that depends on middleware you can't confirm statically.
- **P3** — defense-in-depth: predictable ids where authz is otherwise correct, missing authorization regression tests, reliance on id secrecy as a secondary layer.

## When the code looks fine

After all passes, if nothing fires:

1. Say so explicitly, and state what you verified: the ownership model from Pass 0, the handlers enumerated, and that every object-by-id path and privileged function carries a check across all verbs.
2. Note what static review **cannot** confirm: runtime middleware wiring and ordering, the actual body of a centralized policy you didn't see, framework defaults, and whether deployed config matches the code.
3. Recommend confirming at runtime with a dynamic BOLA test (two accounts, swap ids) against a running instance — the complementary offensive check this skill does not perform — and walking `references/checklist.md`.

A clean static read does not prove the deployment is safe.

## Reference files

- `references/frameworks.md` — what a *correct* ownership and role check looks like in each major stack (Express/NestJS, Django/DRF, Rails + Pundit/CanCanCan, Spring Security, Laravel, Go). Read it to recognize whether a check is present or absent in idiomatic code, and to write the fix in the project's own conventions.
- `references/patterns.md` — "I want to do X authorization safely" recipes: owner-scoped queries, a centralized policy layer, deny-by-default, server-derived identity, secure multi-tenant scoping. Read it when proposing the fix, not just naming the gap.
- `references/checklist.md` — a flat per-endpoint / per-resource / per-application checklist with a triage order. Use it for a full audit, for scanning many endpoints at once, or when prioritizing findings at scale.

## What this skill won't do

- It won't run the app, send requests, or need credentials. It reads source. For runtime confirmation, pair it with a dynamic BOLA tester (two accounts, swap object ids) — that is the offensive complement to this defensive review.
- It won't replace an authorization engine (OPA/Rego, AWS Cedar, OpenFGA, Oso). It checks that whatever mechanism exists is actually applied on *every* path, including the ones added yesterday.
- It won't wave through a missing check because exploitability is unproven. When it cannot confirm a check exists, it flags it — the false-positive cost is a comment; the miss is a breach.
- It won't accept authentication as authorization. "You must be logged in" is never the answer to "may *this* user touch *this* object?"
