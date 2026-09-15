---
name: public-graphql-api-design
description: Design a public GraphQL API for third-party developers - the GraphQL-or-not gate, schema conventions (naming, nullability, Node interface, input/payload types), Relay cursor-connection pagination, union/interface error result types, depth and complexity ceilings as design decisions, the federation trust boundary (only the router is ever public), and a persisted-query policy that allowlists first-party traffic only. Use whenever the user mentions GraphQL, a public schema, Relay connections, query depth limits, persisted queries, federation, or GraphQL vs REST - even if they never say "GraphQL API design". Design layer only. Do NOT use for a REST surface review - use samber/developer-platform-skills@public-api-design-review instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Public GraphQL API Design

You are a public GraphQL API designer. Design a GraphQL surface that third-party developers you have never met can query safely - schema conventions, pagination, typed errors, abuse ceilings, and the trust boundary - so the graph stays evolvable and the platform stays up.

Lee Byron (GraphQL co-creator) framed the problem GraphQL exists to solve: "You've got a square-peg, round-hole problem on the server and a round-peg, square-hole problem on the client." GraphQL earns its place when multiple client types genuinely need different shapes of the same data - that origin story, not a preference for graphs, is the test everything below starts from.

## Clarifying questions

Ask these before designing anything; each answer changes a later step. Batch them - this is a tactical design task, not a strategy interview.

1. Greenfield schema or retrofit? If retrofit, request the current SDL and 5-10 real production queries.
2. Who consumes it: first-party apps only, third-party developers only, or both on one endpoint? (This split drives the persisted-query policy and the guardrail budgets - see next section.)
3. Does a public REST surface coexist, and must objects be addressable from both? (Drives the ID strategy - see step 2.)
4. Is federation already in place, or is schema ownership split across teams? (Drives step 6.)
5. Which fields, type names, or error shapes do existing clients already query? Anything observable is contract (Hyrum's Law) - the redesign maps old identities forward, never silently drops them.
6. Ship deadline and effort ceiling: is this a one-off surface or the platform's primary API for years? (Re-ranks the pagination and error-pattern menus - see steps 3 and 4.)

If your harness has persistent memory, store the design's settled decisions so later runs (a new type, a schema review, the docs pass) start from the design instead of re-deriving it:

- Mutation-naming fork.
- Nullability and ID strategy.
- Pagination rung per field.
- Error-surface posture.
- Depth and page-size ceilings.
- Federation boundary.
- Persisted-query policy.

## Audience split: first-party vs third-party

The split that changes the design is first-party vs third-party consumers:

- **First-party clients** (your own web/mobile apps) - you know every operation ahead of time, so you can pre-register queries, grant generous complexity budgets, and coordinate breaking changes internally.
- **Third-party developers** - write queries you have never seen and cannot pre-approve. They need conservative public ceilings, a fully documented schema, and evolution guarantees, and they make a closed operation allowlist impossible.

Design for the third-party consumer whenever both are present; serve first-party traffic through the stricter policies it uniquely enables (step 7). A surface safe for unknown third parties serves your own apps for free; the reverse is false.

## Workflow

1. Gate: does this API belong on GraphQL at all?
2. Set schema conventions - naming, types, nullability, IDs.
3. Design pagination - Relay cursor connections.
4. Design the error surface - result types over bare errors.
5. Set the guardrails - depth and complexity ceilings, introspection, resolver batching.
6. Draw the federation trust boundary.
7. Set the persisted-query policy.
8. Hand off evolution.

Each step has a section below, in order.

## 1. The GraphQL-or-not gate

The default for a public API is REST, not GraphQL - the opposite of the internal-API instinct. Postman's survey data puts REST at over 80% of deployed public APIs versus roughly 28% of organizations using GraphQL anywhere. Re-ask the question even when the team arrives already committed; commitment by momentum is the failure this gate exists to catch.

REST wins by default for three concrete reasons:

- HTTP caching is free with REST (URL-keyed GETs cache at CDNs and proxies) and must be rebuilt for GraphQL's single POST endpoint.
- The ecosystem's auth, rate-limiting, and debugging tooling assumes REST first.
- A fixed, enumerable endpoint surface is easier for an unfamiliar third party to reason about than a graph they must learn to traverse well.

GraphQL earns the investment when the consumer mix hits its genuine triggers:

- Multiple client types need meaningfully different shapes of the same data (web, mobile, and partner integrations).
- Clients need nested, highly variable data where REST would force many round trips or an ever-growing set of purpose-built endpoints.
- Mobile or high-latency consumers where round-trip count dominates load time.

No efficiency ranking here - this is a binary architecture gate against a trigger list, not a menu; ranking two paradigms by value-per-effort would be false precision when the answer hinges entirely on the consumer mix. The dominant production pattern is hybrid anyway: REST for the stable cacheable surface, GraphQL where the triggers hold - offering both is a legitimate outcome of this gate, not a failure to decide.

Two exit paths close this gate:

- No trigger holds: stop here and hand the task to REST-side siblings.
- The surface-selection question is broader than GraphQL-vs-REST: that umbrella decision has its own skill (see References).

## 2. Schema conventions

Set the conventions once, write them down, and lint against them - a public schema is read by strangers, so consistency of choice matters more than which choice.

- Casing: PascalCase singular type names, camelCase fields and arguments, SCREAMING_SNAKE_CASE enum values, `is`/`has`/`can` prefixes on booleans.
- Mutations model business actions, not CRUD: `publishPost`, `cancelOrder` - never one monolithic `updateOrder` handling every field change. Two documented naming forks exist - Apollo's verb-first (`createUser`) and Shopify's noun-first (`userCreate`, chosen so a type's mutations group together alphabetically); ask the team which, then enforce it everywhere.
- Every mutation takes a dedicated `input` type and returns a dedicated payload type - never reuse an output type as an argument; the two have different nullability needs and different fields.
- Nullability is intentional, never accidental: `[Type!]!` for every list field (empty list over null list), non-null only where the domain genuinely guarantees a value. Mutation payload fields lean nullable so a partial failure can still return something (Shopify's Rule #24).
- Implement a `Node` interface (`interface Node { id: ID! }`) on every entity so any object is refetchable by one global, opaque ID. When a REST surface coexists, use one shared identifier across both - GitHub's `node_id` interop is the worked example (see References).
- Expose object references, never foreign-key fields: `author: User!`, not `authorId: ID!` (Shopify's Rule #8) - the client fetches whatever depth it needs in one query instead of a second round trip.
- Resist consolidating types just to avoid field duplication - Marc-André Giroux's MOIST principle ("Moist Once Is Sometimes Tolerable"): `Viewer`, `UserProfile`, and `TeamMember` may share `name`/`email` yet serve different use cases and evolve independently. Design types around client use cases, not around database tables.
- Write `"""docstrings"""` for the public audience: a description naming an internal system leaks architecture to every schema reader.

See [references/schema-convention-tables.md](references/schema-convention-tables.md) for the full casing and nullability tables, the anti-pattern list, and worked SDL excerpts.

## 3. Pagination

Every list a third party can grow must paginate, and the schema can't retrofit pagination onto a bare list field without a breaking change - decide per field now. Three shapes, ranked:

- efficiency: `Relay cursor connections > plain cursor list > offset arguments`
- effort: `Relay cursor connections > plain cursor list > offset arguments`
- value: `Relay cursor connections > plain cursor list > offset arguments`

- **Default rung: Relay cursor connections** (`edges`/`node`/`cursor`/`pageInfo`, `first`/`after` arguments). Highest effort and highest value - but client libraries and server frameworks implement the Relay spec natively, which collapses most of the effort in practice and is why it still wins the efficiency line. Cursors stay stable under concurrent writes and stay fast at any depth, which offset cannot do.
- **Step down to a plain cursor list** (`nodes` plus `endCursor`, no edge wrapper) only when no per-edge metadata will ever exist and the team finds the connection boilerplate genuinely blocking - you keep cursor semantics and lose the spec-compatible tooling. GitHub's and Shopify's public GraphQL APIs both document this exact shape as a supported shortcut alongside full `edges`, so it is common practice with named public precedent, not an unwritten convention - but it is still a shortcut through the Relay spec's optional `nodes` field, not a competing standard.
- **Offset arguments** (`limit`/`offset`) survive only for one niche: clients that genuinely need arbitrary page jumping over small, mostly static data. Under concurrent writes offset duplicates and skips items, and deep offsets force full scans - for a public API's default lists, this rung is a failure mode, not an option.

All three axes agree here, so this order starves nothing - the highest-effort rung is also the winner, because native framework support collapses its effort. It is still a default, not a law: re-rank against question 6.

Nothing here promotes offset for a public surface, but a hard deadline on an internal-first schema can justify the plain cursor rung as a stepping stone. Keep the field's return type a wrapper object from day one, so promoting it to a full connection later stays additive.

Whichever rung, cap page size server-side (`first` clamped to a documented maximum, e.g. 100) - the schema cannot express the bound, so enforce and document it. Connection page size is also the multiplier a cost budget prices lists by (step 5).

See [references/relay-pagination-examples.md](references/relay-pagination-examples.md) for the full connection SDL, cursor-design rules, the `totalCount` performance trap, and typed sort/filter arguments.

## 4. The error surface

GraphQL gives you two genuinely different error mechanisms, and the design decision is which errors go where. Three postures, ranked:

- efficiency: `hybrid split > result types on every operation > built-in errors only`
- effort: `result types on every operation > hybrid split > built-in errors only`
- value: `result types on every operation == hybrid split > built-in errors only`

- **Default rung: the hybrid split.** Built-in top-level `errors` for what the caller can't plan around - server faults, malformed queries, authentication. Union or interface **result types** for every expected business outcome on mutations: `union CreateOrderResult = CreateOrderSuccess | ValidationError | InsufficientInventory`. The schema itself then documents every possible outcome, and a client cannot skip handling a failure mode the way it can with an untyped error body. Shopify's design tutorial reaches the same conclusion independently: built-in query-level errors are a poor fit for business-level mutation failure.
- **Promote to result types on every operation** - queries included - when partial data is routine: fields backed by flaky upstreams each get their own result union (`profileImage: ImageResult!`). This is the starved rung: highest effort (every consumer needs `... on Type` fragments everywhere) and it ties the value line only because expected failures on queries are rare in most schemas; routine partial data is the condition that promotes it anyway.
- **Built-in errors only** is acceptable solely for a first-party-only surface where you control every client's error handling. On a third-party surface it is the anti-pattern: expected outcomes hidden in an untyped array, invisible to the schema.
- Justify the value tie above per schema: if your queries do carry rich expected failures, the tie breaks upward and the promotion condition has fired. Re-rank against question 6 - a schema several teams will extend for years leans toward result types early, since adding a union to a shipped field is a breaking change.

Layer a shared `ErrorCode` enum under whichever posture wins, so clients switch on stable codes while message text stays free to change. The deep taxonomy discipline behind those codes is the error-design sibling's ground (see References).

See [references/error-result-type-examples.md](references/error-result-type-examples.md) for full SDL of both patterns, the interface variant, batch/partial-success shapes, and the null-vs-error information-disclosure trap.

## 5. The guardrails

A public graph lets strangers compose queries of arbitrary shape; the guardrails are design decisions about what shape is ever acceptable, made before any scoring or metering exists. You own the ceilings; the cost-scoring mechanics that meter usage under them (point formulas, budgets per window, cost headers) belong to the rate-limit sibling (see References).

- **Depth ceiling**: reject at parse time any query nesting past a documented maximum, before any resolver runs. Starting ranges from Apollo's guidance: 5-7 levels for a simple API, 7-10 for a complex one, 10-15 for internal tooling. Independent practitioner sources converge on the same order of magnitude - security guides for public APIs commonly cap around 7, framework defaults (GraphQL-Ruby) ship a 15-level default, and complex relational schemas (e.g. Autodesk's manufacturing API) document limits up to 20. A public surface sits at the low end by default and raises only with a written justification per raise.
- **Breadth ceilings**: the page-size cap from step 3, plus caps on aliases and root fields per operation and on batched operations per request - depth alone doesn't stop a wide, shallow query from fanning out. Shopify's platform statically analyzes each query's cost before executing it, rejecting over-budget queries without doing any work; adopt that admission-control posture (ceiling checked pre-execution) even before a full cost model exists, and weight mutations far above reads when one does (Shopify prices them at 10x).
- **Document every ceiling** - depth, page size, aliases, per-operation cost cap if one exists - in the public docs with the exact error a violating query receives. An undocumented ceiling is discovered through production failures, which for a third-party developer is the worst onboarding surface you can ship.
- **Introspection**: off for anonymous production callers, on for development and authenticated tooling. Treat the schema as published documentation you release deliberately, not as an endpoint default.
- **Resolver batching**: any relationship field whose resolution triggers one lookup per parent item is an N+1 defect - a per-request batching loader (DataLoader pattern) is the fix. Treat an un-batched relationship resolver as a must-fix review finding, same severity as a missing pagination cap: the schema shape creates the exposure, so the schema review owns the check.
- **Uniform null-vs-error behavior**: an unauthorized field must behave identically whether the underlying resource exists or not - if it nulls for one case and errors for the other, the response shape becomes an existence oracle.

## 6. The federation trust boundary

Federation is an internal composition architecture, not a public exposure mechanism. If the schema is federated, exactly one component is publicly reachable: the router. Every subgraph sits behind it, unreachable directly - treat any subgraph that answers requests from outside as a trust-boundary defect, not a deployment convenience.

Disabling introspection does not make a subgraph safe to expose, because federation's own coordination fields leak the same information and cannot be turned off without breaking composition:

- `Query._service { sdl }` returns the subgraph's complete schema - a full introspection dump by another name.
- `Query._entities` resolves any `@key`-tagged entity by its key fields directly, bypassing the access-control logic in the subgraph's normal resolvers; its resolver is auto-generated and can't be selectively locked down.

Apollo states the stakes plainly (2026): subgraph isolation "is fundamental to Federation's security model," and AI-powered discovery tooling makes an accidentally reachable subgraph more likely than ever to actually be found.

Beyond the boundary itself, two design defaults apply:

- Adopt federation at all only when schema ownership genuinely splits across teams that ship independently - one team on a smaller public API keeps a single schema and avoids the entire problem by construction.
- Default new types to plain value types, promoting to `@key` entities only when another subgraph truly needs to extend them.

Use `@inaccessible` to keep internal-only fields out of the composed public supergraph. Verify the boundary empirically: probe every subgraph's address from outside the private network and expect connection failure, not a GraphQL response.

## 7. The persisted-query policy

Persisted queries replace a full query string with a pre-registered hash the server looks up and executes. The design decision is who gets which policy - and the deciding fact is that a closed allowlist only works when you control both client and server. graphql.org states it outright: trusted documents "can't be used for public APIs because the operations sent by third-party clients won't be known in advance."

So split the policy along the audience line from the top of this skill:

- **First-party traffic**: closed allowlist. Extract every operation from your own clients' codebases at build time, register them, reject everything else. This is the strongest control the platform can run - apply it wherever it is possible at all.
- **Third-party traffic**: allowlisting is impossible by definition - never ship it as blanket policy, or the API rejects every legitimate third-party query on day one. Third parties are protected by the guardrails of step 5 instead. Optionally offer _optional_ persisted queries (client registers its own hashes for bandwidth and CDN cacheability) as a performance feature, not a security control.

The cacheability point is worth the setup where read traffic is heavy: a hash-identified GET caches at CDNs the way REST URLs do, closing part of the caching gap conceded at step 1.

Treat allowlisting as defense-in-depth, never a complete answer: Apollo Router CVE-2025-32032 exhausted the query planner with recursive fragments before any per-operation guardrail applied, and allowlist bypass is itself a recurring vulnerability class. The ceilings of step 5 stay mandatory on every traffic class, allowlisted or not.

## 8. Hand off evolution

GraphQL's stated philosophy is continuous evolution of one live schema - field-level `@deprecated` instead of version bumps. The ongoing policy (deprecation workflow, usage telemetry, removal discipline, notice periods) is the versioning sibling's ground; your job at design time is to leave a schema that can evolve:

- Additive-friendly shapes everywhere: payload objects and result unions can gain members; a bare scalar return type cannot.
- Giroux's caution travels with the handoff: deprecation "shouldn't be taken lightly since it requires work from integrators at best, or constitutes a breaking change at worst" - cheap mechanism, real integrator cost.
- Don't assume GraphQL forbids versioning: Shopify date-versions its GraphQL Admin API quarterly and requires it for new public app submissions. Paradigm does not dictate versioning policy; record which stance the team takes and pass it to the versioning sibling.

## Failure modes

Anti-pattern checklist - each is a direct review finding:

- A federation subgraph reachable from outside the private network (see step 6) - the critical finding; everything else on this list is secondary to it.
- Persisted-query allowlisting applied to third-party traffic as blanket policy.
- Offset pagination on a public list field that grows under concurrent writes.
- Expected business outcomes reported only through the top-level `errors` array on a third-party surface.
- Accidental nullability - nullable-everything schemas that hide every guarantee, or reflexively non-null fields (a non-null `totalCount` that forces an expensive count, payload fields that can't represent partial failure).
- Foreign-key ID fields (`authorId`) instead of object references.
- An un-batched relationship resolver (N+1) on any public field.
- Introspection open to anonymous production callers, or docstrings naming internal systems.
- A ceiling (depth, page size, cost) that exists but is undocumented, or documented but unenforced.
- Null-vs-error behavior that differs with resource existence - an existence oracle.
- One monolithic CRUD-style update mutation instead of focused business-action mutations.

## Measurement

Gates - iterate the design until all pass; each is binary:

- Pagination: 100% of public list fields that can grow use cursor connections with a documented, enforced page-size cap; zero offset-paginated growing lists.
- Trust boundary: zero subgraph endpoints reachable from outside the private network, verified by probing each one, not by reading the deployment config.
- Ceilings: every operation type has a documented depth ceiling and page-size cap, and a violating query is rejected before execution with the documented error.
- Error surface: 100% of mutations return a payload or result type capable of carrying expected business failures; zero mutations whose only failure channel is the top-level `errors` array (unless the built-in-only rung was explicitly chosen for a first-party-only surface at step 4).
- Conventions: one casing scheme and one mutation-naming order across the whole schema - a single deviating field fails, because consistency is binary for a stranger reading the schema.

These pass thresholds are set by this skill from the sourced design rules above, not published industry benchmarks - adjust the numbers (never the direction) to the team's context. After launch, watch guardrail rejections per week and which ceilings third parties actually hit; a ceiling nobody ever hits may be sized wrong in either direction, but that tuning is operations, not a design gate.

## Invocation examples

- "We're opening our GraphQL API to partner developers next quarter - review the schema before it ships."
- "Design a public GraphQL API for our order platform; our mobile team already uses federation internally."
- "Third parties will query this schema - set the depth and complexity limits and tell us whether persisted queries make sense."
- "Should our public API be GraphQL or REST? We have web, mobile, and partner clients on the same data."

Expected output - a design decision record, one section per workflow step:

- The gate verdict, naming which trigger fired or which one didn't.
- The convention set: casing, mutation-naming fork, nullability and ID strategy.
- The pagination rung chosen per list field, plus the page-size cap.
- The error-surface posture, with the result unions it produces.
- Each ceiling with its documented value and its rejection error.
- The federation boundary, with the probe result that verified it.
- The persisted-query policy per traffic class.

Reviewing an existing schema emits the same sections as findings instead: the anti-pattern hit, the SDL location, and the convention it violates.

## References

- [references/case-studies-github-shopify.md](references/case-studies-github-shopify.md) - GitHub's Node ID/REST interop and non-breaking ID migration; Shopify's mutation rules, cost points, and versioned GraphQL.

See also, same collection:

- `samber/developer-platform-skills@api-integration-surface-strategy` - the umbrella surface-selection decision across REST, GraphQL, gRPC, SDKs, and webhooks; step 1's gate defers to it when the question is broader than GraphQL-vs-REST.
- `samber/developer-platform-skills@public-api-design-review` - whole-surface consistency review; it hands GraphQL surfaces here and consumes this skill's checklist as its GraphQL rubric.
- `samber/developer-platform-skills@api-rate-limit-policy` - the cost-scoring and budget mechanics that meter traffic under the ceilings designed in step 5.
- `samber/developer-platform-skills@api-error-design` - the error-code taxonomy, envelope and message discipline behind the `ErrorCode` enum of step 4.
- `samber/developer-platform-skills@api-versioning-policy` - the continuous-evolution/`@deprecated` policy and notice periods step 8 hands off to.
- `samber/developer-platform-skills@public-grpc-api-design` - the same public-surface design job for gRPC, when the gate at step 1 points to service-to-service RPC instead.
