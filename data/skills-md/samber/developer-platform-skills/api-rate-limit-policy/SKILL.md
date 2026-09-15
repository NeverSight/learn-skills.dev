---
name: api-rate-limit-policy
description: Design the rate-limit policy a public API publishes to its consumers - the metering model per paradigm (REST request counting vs GraphQL cost points), tier and quota-vs-burst numbers, multi-tenant fairness, rate-limit headers (legacy X-RateLimit-* vs IETF RateLimit fields), 429 and Retry-After behavior, enterprise and partner overrides, and change-notice rules. Use whenever the user mentions rate limits, quotas, throttling tiers, 429 responses, noisy neighbors, or limit-increase requests - even if they never say "rate-limit policy". Policy layer only, not gateway configuration. Do NOT use for the 429 error envelope - use samber/developer-platform-skills@api-error-design instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# API Rate Limit Policy

You are an API rate-limit policy designer. Design the limits a public API publishes to its consumers - the metering model, the tier and burst numbers, the fairness rules, the headers, the throttle response, the override path, and how changes land - so an integrator can predict, observe, and adapt to throttling instead of discovering each ceiling by tripping it. Which gateway or middleware enforces the limit is out of scope; what the limit promises and how it is communicated is the whole scope.

Zuplo's one-line purpose statement is the mission: rate limiting sets "a policy of fair access to API resources and prevent[s] any single user or application from consuming excessive resources and impacting the experience of others." And GeekyAnts' framing is why this is policy work, not plumbing: "designing a rate limiter is fundamentally a strategic decision about fairness, scalability, and user experience."

## Clarifying questions

Ask these before designing anything; each answer feeds a numbered step. Batch them - this is a tactical design task, not a strategy interview.

1. Paradigm: REST-only, GraphQL-only, or both? (Request counting and cost points are incompatible metering models; step 1 picks per surface.)
2. Greenfield, or limits already enforced? If existing: request the currently enforced numbers and the currently documented numbers - drift between the two is the first finding.
3. What consumer tiers exist or are planned (free / self-serve paid / enterprise-partner), and are enterprise customers already asking for higher limits?
4. Abuse pressure: is the API scraped or hit adversarially, or is traffic mostly well-behaved integrations? (Promotes the sliding-window rung and a secondary guard in step 1.)
5. Has one customer's traffic ever degraded others' latency? (Raises the priority of step 3's fairness layers.)
6. Is the API served from more than one region? A limit enforced independently per region multiplies a caller's real global throughput by the region count - cited as "not theoretical, it's a real exploit vector" - so the published limit must state its scope.
7. What can the edge/gateway already emit? (An edge that produces IETF structured fields cheaply re-ranks the header menu in step 4; a gateway that can't count cost points constrains step 1.)
8. By when must the published policy land, is this a one-off fix (unblock one enterprise negotiation) or a compounding contract the platform operates for years, and what is the effort ceiling - engineering hours for limiter work, an on-call rotation to hold fairness layers, appetite for a consumer-visible change?

Question 8 exists because the algorithm menu (step 1) and the header menu (step 4) diverge sharply on time-to-effect, durability, and effort; neither ranking can be picked without it. Each answer moves a different rung:

- A hard date promotes whatever the current gateway already enforces, and the legacy header trio.
- A compounding mandate promotes the sliding window and the both-families rung.
- A low effort ceiling deletes the fairness layers of step 3 from this pass rather than parking them at the bottom, with "the first noisy-neighbour incident" as their unblocking condition.

## Consumer tiers

The consumer tier is the axis that changes this design, and it is not a mere segmentation: the tier ladder **is** the policy artifact this skill produces.

- **Anonymous/free callers** - keyed per IP or per free key; the tightest numbers, the first shed under load. They learn their limits from headers alone.
- **Self-serve paid integrators** - keyed per API key or org; published exact numbers they can capacity-plan against. They need a documented table.
- **Enterprise and partners** - published process instead of published numbers; overrides keyed to the authenticated principal (step 6). They need a named override path with lead times.

## Workflow

1. Pick the metering model per paradigm - and the algorithm, which is what the number promises.
2. Design tiers: quota and burst as two numbers, keyed deliberately.
3. Layer fairness and tenant isolation.
4. Choose the header family.
5. Design the throttle response: 429 and Retry-After.
6. Define the enterprise/partner override path.
7. Write the change-notice policy.

Each step has a section below, in order.

## 1. Pick the metering model

Two incompatible models exist, split by paradigm - never blend them:

- **REST: count requests.** GitHub REST is a flat 5,000 req/hr; Shopify REST is a 40-request bucket leaking 2/s. Simple, universally understood, blind to per-request cost.
- **GraphQL: price the query in cost points.** A one-scalar query and a 100-connection query differ enormously in server cost; the limit is a budget of points per window, with a published cost formula (GitHub: connection `first`/`last` ÷ 100, minimum 1; Shopify: scalar 0, object 1, mutation 10, pre-charge then refund). You own the pricing and budget policy; structural guards (depth ceilings, persisted queries) are schema design owned by `samber/developer-platform-skills@public-graphql-api-design`. See [references/graphql-cost-metering.md](references/graphql-cost-metering.md).
- When both surfaces exist, publish both models separately and state whether they share anything (GitHub: separate budgets, but one shared 100-concurrent-request secondary cap).
- Name the metering unit even when it is neither: Twilio meters concurrency - in-flight requests, not requests-per-window - a fundamentally different unit a caller must plan differently for.

The algorithm underneath is a policy choice too, because it defines what the published number promises (burst behavior, boundary behavior). Four options, ranked:

- efficiency: `token bucket > fixed window > sliding window > leaky bucket`
- effort: `sliding window > token bucket == leaky bucket > fixed window`
- value (public developer API): `token bucket > sliding window > leaky bucket > fixed window`

- **Default rung: token bucket** - bucket depth is the burst, refill rate is the sustained quota, so step 2's two numbers fall out of the algorithm for free. It rewards well-behaved bursty clients, it is Stripe's and GitHub's choice, and convergent vendor guidance (Stripe, Google Cloud, AWS API Gateway) calls it "the standard choice for most web services… start here unless you have a specific reason not to." The token-bucket == leaky-bucket effort tie is real: both maintain one bucket per key; they differ in intent, not implementation weight.
- **Step down to fixed window** only for internal or low-stakes limits where the documented flaw - up to 2× the limit at the window boundary - is harmless (Sentry accepts exactly this trade for simplicity). Its second flaw is the stampede: throttled clients synchronize their retries at the reset boundary, a failure mode the IETF draft itself acknowledges.
- **Promote to sliding window** under adversarial pressure (question 4). This is the starved option: boundary-proof and fairest, with the most precise `Retry-After`, but the highest compute cost - it loses every efficiency round, and scraping/abuse pressure is what promotes it anyway.
- **Choose leaky bucket when a burst is a threat, not a feature** - a fragile downstream or fan-out delivery. Shopify, a payments-adjacent platform, still chose it because flash-sale webhook fan-out dominated: "Each app has access to a bucket… Each second, a marble is removed."
- Naming trap: "token bucket" and "leaky bucket" get inverted informally more than any other pair in this space. In the published policy, describe the behavior (does idle time bank burst capacity, or does output stay constant?), never rely on the name alone.
- This is not one skill-wide decision: Stripe runs four limiter layers simultaneously (step 3), each with its own mechanism. The ranking is a default, not a law - re-rank against the interview answers and what you know of the user's stack; a gateway with a built-in sliding-window limiter gets that rung nearly free, which flips the effort line.

## 2. Design tiers: two numbers, keyed deliberately

- The plan→limit table is the special case among real platforms, not the default:
  - Stripe does not tier by plan at all - flat account defaults, per-API limits, support-granted overrides.
  - GitHub keys its primary limit off auth method: 60 unauthenticated / 5,000 per token / 15,000 Enterprise-org.
  - Shopify, Zoom, Auth0, and Anthropic do map limits to plan.
- Model limits as **identity/auth-scope × endpoint-class × account-override**, then decide deliberately whether plan is one of the inputs. See [references/vendor-limit-models.md](references/vendor-limit-models.md).
- Publish burst and sustained as **two explicit numbers**, never one blended figure. Burst = sustained is the widely-cited failure mode - it breaks legitimate spikes (webhook fan-out, scheduled reports) that need headroom above steady state; Stripe engineered its burst allowance deliberately and says so.
- Let the identifier a tier keys on change with the tier: IP for anonymous, user/token for authenticated, API key or org for paid, service identity for internal. Each step up the ladder is a policy decision to state, not an accident.
- Carve expensive operations out of the general budget with per-endpoint-class limits (Stripe publishes separate limits per API surface: Files 20 read/s, Search 20 read/s, Payouts 15 req/s + 30 concurrent).
- A secondary abuse guard - triggered by request shape (concurrency, per-endpoint pressure) rather than raw count - is legitimate and often necessary. But document that it exists and how it signals: GitHub's deliberately under-documented secondary limit is the named communication failure, where a caller under its published quota is throttled by an opaque layer it discovers only by tripping it.
- Decide deliberately whether a test/sandbox mode gets its own tier, and default to no: reusing the production numbers in test mode keeps integrators' throttling code honest, and several mature platforms do exactly that. Add a separate pre-production quota only against evaluation-volume abuse (free-tier scraping, load tests on a shared sandbox), shaped as an aggregate volume-and-scope cap rather than a faster per-minute limiter. `samber/developer-platform-skills@api-test-mode-design` decides whether that quota exists at all and carries the per-vendor postures; you design the tier once it does.
- State the published numbers as operational hints, not an SLA - every major platform reserves the right to lower limits for stability (step 7 owns how that lands).

## 3. Layer fairness and tenant isolation

Fairness is a policy decision, not a side effect of a good algorithm: the same token bucket applied to one shared pool lets the loudest tenant win by accident. The canonical incident is one tenant's runaway 2am batch job degrading every other tenant's latency while staying under any single cap.

1. **Tenant-level ceiling** - the overall limit per customer, where the tier table from step 2 applies.
2. **Per-user limit inside the tenant's allocation** - stops one user of a multi-seat account from spending the whole tenant budget.
3. **Per-endpoint-class carve-out** - a small allocation for expensive operations, independent of the general budget.

- Where a hard per-tenant cliff is too brutal, use weighted sharing instead: each tenant gets a weight (enterprise 10× a free tenant's share) and capacity divides proportionally, so a small tenant is never starved to zero when a large one saturates the pool. Cohere's production version combines tier weights with Deficit Round Robin and priority queues. The trade: you give up a deterministic guaranteed rate to eliminate the fully-blocked-small-tenant cliff.
- AWS's Builders' Library states the goal: with per-tenant quotas, "only the unplanned portion is rejected while other workloads continue with predictable performance" - and names the paradox to accept knowingly: a quota protects everyone else's availability while reducing the throttled tenant's own, even when spare capacity existed.
- Defense-in-depth is the mature end state. Stripe runs four limiter types simultaneously:
  - A request rate limiter - "by far the most important one".
  - A concurrency limiter for expensive endpoints.
  - A fleet load shedder reserving ~20% of capacity for critical methods.
  - A worker-utilization shedder that sheds by priority class: test-mode traffic first, then GETs, then POSTs.
- Load shedding is a different mechanism from rate limiting - it keys off overall system state, not the caller's own behavior, so a well-behaved tenant can still be shed under fleet stress. Say so in the published policy; a fairness promise that omits this overclaims.
- Internal fairness machinery (WFQ, DRR, shedders) is architecture, not published policy - document its externally observable effects (what a caller can see and when), not the mechanism.

## 4. Choose the header family

Two live options for the machine-readable limit state on responses, ranked. A third - emitting the IETF fields _alone_ - is deleted from the menu below rather than ranked last, so it cannot creep back in as scope:

| Option                      | Efficiency | Effort | Value | Durability |
| --------------------------- | ---------- | ------ | ----- | ---------- |
| legacy `X-RateLimit-*` trio | `+++`      | `++`   | `+`   | `++`       |
| both families               | `-`        | `--`   | `+++` | `--`       |

- **Default rung: the legacy trio** - `X-RateLimit-Limit` / `X-RateLimit-Remaining` / `X-RateLimit-Reset`. It is what nearly every client and SDK already parses; GitHub still emits only this family. Document your `Reset` semantics explicitly (epoch timestamp vs seconds-remaining - vendors genuinely differ).
- **Promote to both families** - the starved option, highest value and highest effort - when the edge emits IETF structured fields cheaply (question 7) or when advertising the policy itself matters: `RateLimit-Policy` lets a well-behaved client self-throttle before its first 429, which the legacy trio cannot express. Cloudflare adopted both header families in September 2025 - production traction worth citing from a Tier-1 platform.
- **Deleted from the menu, not ranked last: IETF fields alone.** Shipping them as your only limit-state signal breaks the clients you already have. Adoption is thin: GitHub and Stripe emit no IETF fields at all. The spec (`draft-ietf-httpapi-ratelimit-headers`) is Standards Track but pre-RFC, and has already changed syntax across draft versions, so today's field names can move under you.
- **Re-promotion trigger:** put this option back on the menu when the draft reaches RFC status, or when a second Tier-1 platform adopts it. Until then the IETF fields ship only inside the both-families rung - frame them as forward-looking in your docs, and cite them by their current names (`RateLimit`, `RateLimit-Policy`).
- Whatever you emit, headers are advisory hints, never guarantees - the draft itself says the values "are informative and MAY be ignored", and "5 remaining" does not promise five successful calls. Publish them as planning signals, not commitments.
- One posture sits outside this menu rather than below it: emitting no limit-state headers at all, Stripe's choice - react to 429s, throttle client-side. It is viable only when you also ship SDKs that retry internally, and it must read in the docs as a deliberate decision, never as an omission.
- This ranking is a default, not a law - re-rank against question 7 and the clients you actually have: an audience that is 90% your own SDKs weakens the legacy trio's compatibility argument, since you control both ends of the parse and can move the whole fleet in one SDK release.

See [references/header-families.md](references/header-families.md) for exact syntax, the cross-vendor comparison table, and sourcing caveats.

## 5. Design the throttle response

- Every throttle on a REST surface returns **HTTP 429** (RFC 6585) with a `Retry-After` header - no exceptions. RFC 6585 also forbids caching a 429; a caching layer that ignores this stretches the apparent throttle beyond its real duration.
- `Retry-After` has two valid RFC 9110 forms - delay-seconds and HTTP-date. Emit delay-seconds: the pervasive client bug is `parseInt`-ing an HTTP-date into `NaN` and retry-storming. The IETF draft's precedence rule applies whatever else you emit: `Retry-After` MUST take precedence over any computed reset.
- The 429 body is a plain instance of the API's error envelope - a machine-readable code such as `rate_limit_exceeded` - designed by `samber/developer-platform-skills@api-error-design`; never invent a rate-limit-specific format. This skill decides which signals appear (retry timing, and _which_ limit was hit - Stripe's `Stripe-Rate-Limited-Reason` is the model for disambiguating multiple limits); that skill owns the envelope's shape.
- **The named trap to design out: a throttle inside HTTP 200.** Shopify GraphQL returns a `THROTTLED` error code in a 200; GitHub GraphQL's primary limit returns 200 with an error body and `x-ratelimit-remaining: 0`. A status-code-only client treats both as success. If GraphQL's partial-result semantics force a body-level signal, document it as loudly as a status code, keep it machine-readable, and never mix conventions silently - Shopify returns 200-`THROTTLED` for cost limits but real 429s for resource limits, two cases a client must learn separately.
- Publish retry guidance next to the limits:
  - Honor `Retry-After`.
  - Back off exponentially **with jitter** - Marc Brooker, AWS: "The solution isn't to remove backoff. It's to add jitter."
  - State the consequence for hammering - GitHub: continuing while limited "may result in the banning of your integration".
- The client-side mechanics - backoff algorithms, retry budgets, idempotency keys - belong to `samber/developer-platform-skills@api-idempotency-retry`; you publish the expectations, it designs the implementation.

## 6. Define the enterprise/partner override path

- The cross-vendor pattern: self-serve tiers publish exact numbers; the top tier publishes a **process**. Overrides go through support, sales, or an account manager - almost never a dashboard toggle - and are keyed to the authenticated principal (API key, org, app installation), never a person.
- Pick which mechanism you are modeling and document it; "contact sales" with no process is the gap. Four named shapes exist:
  - Ticket-based with lead time - Zyte: ≥ 24h ahead, naming key, RPM, dates; Stripe: ≥ 6 weeks for large increases.
  - Spend-based auto-promotion - Anthropic's Tiers 1→4.
  - Plan-gated - Zoom, GitHub Enterprise.
  - Time-boxed self-serve burst - Auth0's 48-hours-per-month multiplier, the rare self-serve exception.
- State explicitly whether a higher-priced plan implies higher limits - OpenAI's Enterprise plan does not until limits are explicitly activated, which contradicts most buyers' assumption.
- An override may hold one dimension non-negotiable (GitHub's server-admin exemption still cannot bypass the GraphQL point quota) - decide which of your limits no override touches, and say so.
- Reserve in writing the right to lower any override for platform stability.

See [references/overrides-and-change-notice.md](references/overrides-and-change-notice.md) for all seven vendor mechanisms.

## 7. Write the change-notice policy

- The industry treats a limit-number change as **non-breaking** - IBM states it plainly: rate limits "can be adjusted on API endpoints during the lifetime of the API and does not require a version update." No version bump means no deprecation machinery fires, which is exactly why a written notice policy matters: nothing else forces communication. Keep the two regimes separate - version deprecation (6–24-month windows, `Deprecation`/`Sunset` headers) belongs to `samber/developer-platform-skills@api-versioning-policy`.
- Scale notice to blast radius. Stripe's ≥ 6-week lead time for large limit _increases_ is a reasonable symmetric floor for _decreases_.
- Introduce or tighten limits on live traffic via GitHub's own rollout sequence, communicating with affected callers before each tightening:
  1. Observe - log real traffic with no enforcement.
  2. Baseline - enforce at a high ceiling.
  3. Refine - tighten from observed data.
- Emergency reductions for platform stability are legitimate; reserve them in writing (Shopify and Stripe both do) so they are policy, not surprise.
- **Never silently change reset semantics** (epoch-seconds → seconds-remaining): it breaks client parsing invisibly instead of producing a visible error - the one limit change that warrants a major announcement by itself.
- In-band beats changelog: limits exposed via headers let well-behaved clients adapt automatically. Zuplo sets the tone for the rest: "provide ample notice and explain the reasons for the changes to maintain transparency and trust."

## Failure modes

Anti-pattern checklist - each is a direct audit finding:

- A throttle signaled inside HTTP 200 that the docs never mention.
- Burst set equal to sustained, or only one blended number published.
- One shared bucket for all tenants - noisy neighbor by design.
- A per-region limit presented as global (real throughput = limit × regions).
- A secondary/abuse limit whose existence is discoverable only by tripping it.
- A documented limit that differs from the enforced one, in either direction.
- Reset semantics changed silently.
- A 429 without `Retry-After`, or `Retry-After` emitted as an HTTP-date when delay-seconds would do.
- A policy that names token bucket but describes leaky-bucket behavior, or vice versa.
- An override granted verbally, keyed to nothing, documented nowhere.
- A published limit cited in a contract as an SLA commitment without the policy saying it is one.

## Measurement

Two gates; iterate the design until both pass.

- **Machine-readability: 100% of throttle responses carry a machine-readable signal a documented client can branch on** - a 429 with `Retry-After`, or a documented in-body code where paradigm constraints force a 200. A single undocumented 200-throttle path fails the gate, because a client can only be as correct as the worst-documented signal.
- **Documentation-enforcement parity: the published limits are the enforced limits.** Diff the docs against the enforcing configuration both directions: every documented number matches what is enforced, and every enforced limit - secondary guards included, at least their existence and trigger shape - appears in the docs. Zero drift.

Trends to baseline from your own first month (no industry thresholds exist):

- Per-tier 429 rate.
- Share of 429s followed by a retry inside the `Retry-After` window - clients not honoring it is a docs or SDK gap.
- Limit-related support tickets.
- Override requests per quarter - persistent volume means the published tiers are set too low.

## Invocation examples

- "Design rate-limit tiers for our public REST API - we have free, pro, and enterprise plans, and enterprise keeps asking for higher limits."
- "We're launching a public GraphQL API next to our REST API - how should rate limiting work across the two?"
- "Our biggest customer's batch jobs degrade everyone else's latency at night - design fairness into our limits without hard-blocking them."
- "Audit our rate-limit docs against what the gateway actually enforces, and pick the headers we should return."

## References

- [references/vendor-limit-models.md](references/vendor-limit-models.md) - what named platforms key limits on, per-API granularity, primary/secondary splits, burst-vs-sustained numbers, a minimal tier table.
- [references/header-families.md](references/header-families.md) - legacy and IETF header syntax, `Retry-After` mechanics, cross-vendor comparison, implementation notes.
- [references/graphql-cost-metering.md](references/graphql-cost-metering.md) - GitHub and Shopify cost formulas, pre-charge/refund accounting, the 1,000-point portability trap, policy takeaways.
- [references/overrides-and-change-notice.md](references/overrides-and-change-notice.md) - seven named override mechanisms, the limit-change vs version-deprecation distinction, rollout and notice benchmarks.

See also, same collection:

- `samber/developer-platform-skills@developer-portal-design` - where published limits, usage dashboards, and remaining-quota displays surface in the developer portal.
