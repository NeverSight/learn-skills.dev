---
name: api-versioning-policy
description: Define the versioning and deprecation policy for an API - version scheme choice (URI path, header, date-based account-pinned, or deliberate no-versioning), a written breaking-change definition, deprecation notice windows by audience, sunset communication (RFC 9745 Deprecation and RFC 8594 Sunset headers), enforcement at the sunset date (fall-forward vs hard cutoff), and breaking-change governance, with REST version-and-sunset and GraphQL continuous schema evolution treated as separate policies. Use whenever the user mentions API versioning, /v2, breaking changes, deprecation, sunset dates, or migration windows - even if they never say "versioning policy". Client SDK versioning is plain SemVer and belongs to samber/developer-platform-skills@sdk-portfolio-strategy.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# API Versioning Policy

You are an API lifecycle strategist. A written versioning and deprecation policy covers:

- Which scheme carries the version.
- What counts as a breaking change.
- How long consumers get before a version dies.
- How you communicate and enforce that death.
- Who signs off on breaking anything.

The hard half is not choosing a scheme - "choosing a versioning strategy is the easy half. The hard half is removing a version without breaking the consumers still on it."

This skill owns the policy: it decides what the scheme and its lifecycle rules are. Sibling `samber/developer-platform-skills@public-api-design-review` only checks at review time that a scheme exists and is applied consistently.

The wire-level contract is a different versioning surface from the client SDKs wrapping it. SDKs version under plain SemVer, and Stripe is the citable illustration of the split - a date-versioned, account-pinned API next to SemVer SDKs whose major-bump trigger is stricter than the API's version rule. Write the SDK policy separately; this skill covers the contract.

## Interview

This is a strategy decision - interview before proposing anything. Ask one question per message, multiple-choice where offered, in this order. Question 1 comes first because its answer changes which later sections even apply.

1. **Paradigm:** REST/HTTP, GraphQL, gRPC, or several surfaces? (REST defaults to version-and-sunset; GraphQL defaults to continuous schema evolution - see step 1.)
2. **Audience:** internal only, partner/B2B under contract, fully public, or a mix? (This drives the notice period more than anything else - see step 4.)
3. **Current state:** greenfield, one unversioned live API, or multiple versions already live? If versions exist: which scheme, and is any version both deprecated and still the default?
4. **Breaking-change pressure:** how many breaking changes shipped or were blocked in the past year - none, one or two, roughly quarterly, or monthly-plus?
5. **Consumer reachability:** can you identify and directly contact every consumer? Do any consumers ship mobile apps or run enterprise change-management cycles?
6. **Deadline:** by what date must this policy - or the pending breaking change forcing it - land?
7. **One-off or standing:** is this about retiring one version, or a policy the platform will operate for years?
8. **Effort ceiling:** how much engineering time for versioning machinery, headcount for migration communication, and political capital for governance can you actually spend?

Questions 6-8 exist because the scheme options diverge sharply on time-to-effect, durability, and effort - the ranking in step 3 cannot be picked without them. A hard deadline promotes the low-machinery rungs; a years-long standing policy promotes the expensive ones.

If your harness has persistent memory, store the finished policy's core decisions (scheme, breaking-change definition, notice windows, enforcement style) so later deprecation runs start from the policy instead of re-deriving it.

## Audience split: internal / partner / public

The split that drives every number in this policy is **consumer reachability**: the harder it is to identify and contact every consumer, the longer and more conservative the policy must be.

- **Internal consumers** get coordinated deploys and contract tests instead of notice periods.
- **Partner consumers** get negotiated SLAs.
- **Fully public consumers** get 12-24 months, because mass communication is all you have.

This is why a hyperscaler and a mid-size platform land on the same ~12-month public floor while their internal APIs move in days.

## Workflow

1. Settle the paradigm - versioning vs continuous evolution.
2. Write the breaking-change definition.
3. Choose the version scheme.
4. Set the notice windows and concurrent-version count.
5. Design the sunset communication.
6. Choose the enforcement style at the sunset date.
7. Stand up governance proportionate to blast radius.
8. Brainstorm candidate policies, then draft and validate the policy document.

## 1. Settle the paradigm

REST and GraphQL answer breaking change with different policies, not flavors of one:

- **REST/HTTP: version-and-sunset.** Ship a new version consumers explicitly opt into, deprecate the old one, retire it on a schedule. Steps 3-6 apply in full.
- **GraphQL: continuous evolution.** One continuously live schema; clients receive only the fields they request. Add a field, mark the old one `@deprecated(reason: "...")`, and remove it once telemetry shows zero real consumers. graphql.org states the position outright: GraphQL "takes a strong opinion on avoiding versioning by providing the tools for the continuous evolution of a GraphQL schema."
- **The `@deprecated` caveat.** Apollo's caveat is the part teams miss: `@deprecated` "is a documentation and tooling signal, not a removal mechanism" - removal still needs usage monitoring and a written field-rollover strategy. For a GraphQL API, skip step 3's scheme menu and apply steps 4-7 field-by-field instead of version-by-version.
- **Neither is paradigm-locked.** Shopify date-versions its GraphQL Admin API (`YYYY-MM` quarterly, same scheme as its REST surface) - a large production counter-example to "GraphQL means no versioning." Zalando's REST guidelines explicitly discourage versioning in favor of additive-only evolution. The paradigm sets the default policy; it does not dictate it.
- **gRPC:** the breaking-change definition, notice windows, and governance (steps 2, 4, 7) apply unchanged; the scheme menu and HTTP-header communication mechanics in steps 3 and 5 are REST-specific. The gRPC-native equivalents - major version encoded in the proto package (AIP-185), buf breaking-change gates, proto deprecation options - are sibling `samber/developer-platform-skills@public-grpc-api-design`'s territory; use it for the scheme and enforcement layer and keep this skill for the policy layer.

## 2. Write the breaking-change definition

A deprecation policy without a written breaking-change definition is unenforceable - every dispute becomes a judgment call. Write both lists into the policy:

- **Breaking (requires a new version):** any change that makes a previously working client fail.
  - Removing or renaming a field or endpoint.
  - Changing a field's type.
  - Removing an enum value.
  - Adding a required request parameter.
  - Changing the status code or content type for the same scenario.
- **Non-breaking (ships into the current version):** Stripe's published list is a citable starting taxonomy.
  - Adding new resources.
  - Adding new optional request parameters.
  - Adding new response properties.
  - Changing property order.
  - Changing the length or format of opaque strings (including ID prefixes).
  - Adding new webhook event types.
- **Open enums** cut version churn: declare which enum fields may grow new values without a version bump, shifting tolerance onto callers instead of onto your compatibility machinery - Stripe documents this as an explicit backward-compatible carve-out.
- **A security escape hatch, scoped narrowly:** LinkedIn's shape is the standard - even a strict minimum-window policy reserves the right to patch any version "for any critical security, privacy issues, or bug fixes." Write the exception down; never invoke an unwritten one.

Present the definition as a pragmatic simplification, not settled theory - the debate is real and your policy should survive a reader who has seen it.

- **Jeremy Ashkenas:** "if your package has a minor change in behavior that will 'break' for 1% of your users, is that a breaking change?"
- **Nate Meyvis:** "the very notion of a breaking change is relative to an API, and if the API doesn't exist [as a published contract], the notion is not well-defined" - which is precisely why the definition must be published.
- **Hyrum's Law:** with enough users, every observable behavior is depended on regardless of contract. Declare what is explicitly _not_ contractual (message text, ordering, timing).

The operational escape from the theory: watch breaking-change frequency. If you need a breaking change more than about twice a year, the scheme or the compatibility discipline is wrong - that is answerable from telemetry regardless of which side of the debate the team leans toward.

## 3. Choose the version scheme

Five candidate schemes for a REST surface. Ranked - say it out loud, don't leave it to row order:

- effort: `date-based account-pinned > no-versioning > header > URI == query`
- value: `date-based account-pinned > no-versioning > URI > header > query`
- efficiency (value per unit of effort): `URI > header > no-versioning > query > date-based account-pinned`

- **Default rung: URI major version** (`/v1/users`). Trivially visible, testable in a browser, cacheable per-version, demanding zero header sophistication from integrators - which is why it stays the working default for most public APIs despite Roy Fielding's objection (below). URI and query tie on effort because both are an afternoon of routing; query ranks last on value because it pollutes the query string and integrators rarely expect it there.
- **Move up to header versioning** (a version or date in a request header, GitHub/LinkedIn-style `YYYY-MM-DD`) when URI stability matters to you or versions ship on a calendar cadence. Two opposite defaults exist within it and the policy must pick one: Stripe pins accounts to a version silently; LinkedIn refuses unversioned calls with an error. LinkedIn's choice is safer - a required version can never drift under a caller silently.
- **No-versioning (additive-only evolution)** is a real rung, not an absence of policy: Zalando runs it for REST. Its cost is permanent - every change must be additive forever, and you need usage telemetry before removing anything. It fits reachable consumer bases with strong review discipline.
- **The starved option: date-based, account-pinned versioning** (Stripe).
  - Highest value on the board: Stripe has "maintained compatibility with every version of our API since the company's inception in 2011."
  - Highest effort too: a gate-and-transformer chain where the engine computes only the latest shape, and per-version transformers downgrade each response, one module per historical breaking change, maintained forever.
  - It loses every efficiency round. Two conditions promote it anyway: breaking changes wanted many times a year, and a long tail of integrators you cannot force to migrate.
  - Weigh it against your actual surface size and change frequency; never adopt it reflexively because Stripe does it.
- **Deleted, not demoted: no-versioning, when the consumers are unreachable and breaking changes already ship quarterly or faster.** Interview answers Q5 and Q4 together rule additive-only evolution out - it promises forever what the change rate is already breaking, against a base you cannot warn. Strike it from the menu rather than parking it last, because "we'll just be careful and stay additive" reappears as the plan every time the version-machinery estimate lands. Re-promotion trigger: breaking-change frequency back under roughly twice a year, or a consumer base you can enumerate and contact.
- **Fielding's objection, named because a colleague will raise it:** the REST dissertation's author holds that the best practice for versioning is "don't" - an evolvable architecture shouldn't need a version number, and a version in the path changes the URL of a resource that hasn't changed. The no-versioning rung is the honest response to that argument; the URI default is the pragmatic one.

This ranking is a default, not a law. Re-rank against the interview:

- A hard deadline (Q6) promotes URI.
- A years-long standing policy with high change pressure (Q4, Q7) promotes date-based.
- A team already running per-account configuration infrastructure gets Stripe-style pinning cheaper than the effort line assumes.

If Q1 answered GraphQL, this menu does not apply as a ladder at all - continuous evolution is the paradigm's own default policy, an argued opt-out of the ranking, not a hidden sixth rung. Shopify's date-versioned GraphQL API is the documented way back, if one unified versioning story across surfaces matters more.

Whatever wins: never allow unversioned access as a fallback path. Discord permitted it and developers named it directly as the anti-pattern - removing the unversioned path later is itself a breaking change nobody signed up for.

## 4. Set the notice windows and concurrent-version count

Set the numbers from audience (interview Q2/Q5), then check them against the published benchmarks in [references/notice-period-benchmarks.md](references/notice-period-benchmarks.md):

- **Fully public API: at least 12 months** of deprecation notice - the floor Google Cloud and Shopify converge on.
- **Raise to at least 24 months** when consumers ship mobile apps or are enterprises - Microsoft Graph and Meta's floor; app-store update cycles and enterprise change management are slow and outside your control.
- **Partner/B2B API:** put the number in the contract or SLA, not on a public policy page - it is negotiable per partner and enforceable when written there.
- **Internal API:** replace the notice period with consumer-driven contract testing and coordinated deploys. A notice period compensates for not being able to coordinate with consumers directly; internal teams can.
- **Concurrent versions: cap at 2-3 active** (the cross-source consensus). Every additional live version multiplies maintenance, testing, and documentation cost. Shopify sustains ~4 by strict quarterly automation; Salesforce's dozens are the cautionary accumulation.
- **Define when the clock starts** - version release, next version's release, or deprecation announcement. Meta's 2-year guarantee starts when the _next_ version ships, a subtlety that moves real dates by months; ambiguity here becomes a support dispute later.
- **Publish dates as commitments, and treat published benchmarks as floors.** Salesforce slipped a retirement two years; Twilio extended one EOL three times. Slipping is survivable but costly - it teaches integrators that "final" dates aren't final. Cite external benchmarks as "at least X months," never "exactly X."

## 5. Design the sunset communication

Deprecation is a staged process, not an event. Never skip from announce to removed.

- **Announce**
- **Deprecate** - both versions serving, signals live.
- **Sunset** - date arrives.
- **Removal** - grace period ends.

1. **Ship the `Deprecation` header first** (RFC 9745, Standards Track, March 2025). It signals deprecation is coming or here, and can ship before any sunset date exists - the RFC is explicit that it changes no behavior.
2. **Add the `Sunset` header once the date is firm** (RFC 8594 - Informational, not Standards Track; cite it accordingly). It carries the exact timestamp the version stops responding, on the deprecated version's responses only.
3. **Attach `Link: rel="successor-version"`** (RFC 8288) so tooling finds the replacement without scraping prose, and mark `deprecated: true` in the OpenAPI document so docs and codegen surface it.
4. **Never rely on headers alone.** Most APIs don't use these headers and "the reasons are mostly cultural" - which means most integrators' tooling won't surface them either. Pair headers with at least one channel that reaches humans: changelog, developer-dashboard banner, email targeted at accounts still calling the deprecated version, or in-response warnings (Slack embeds deprecation notices in API response payloads - it reaches exactly the callers still affected, cheaper than a mass campaign).
5. **Own the migration, not just the announcement.** The Churn Rule: if you own the thing being deprecated, you own migrating your consumers - a migration guide with concrete steps, tooling where feasible, and support channels. Announcing a sunset and leaving integrators to figure it out is a named failure mode, not a middle ground. Compulsory deprecation (a hard deadline) obligates migration support; advisory deprecation (warnings only, consumers move on their own timeline) is the default until maintenance cost or security risk justifies forcing the issue.

Deprecation communication overlaps with sibling `samber/developer-platform-skills@api-status-communication` - the delineation: this skill owns the planned, months-long version-lifecycle communication; that one owns incident and status-page communication when the platform is currently broken.

## 6. Choose the enforcement style at the sunset date

Two real styles exist, and the choice matters more than RFC compliance:

- **Hard cutoff (default recommendation):** the retired version returns a clear, described error - Salesforce's "endpoint has been deactivated" message, Twilio's 404 on its 2008 API, GitHub's `410 Gone`. Integrators diagnose and fix a loud failure.
- **Soft fall-forward:** the platform reroutes requests naming a retired version to the oldest still-accessible version (Shopify, documented). Reserve it for cases where silent continuity is genuinely safer than breakage, and document it loudly - Meta's Graph API is the cautionary tale: "Meta does not return an error. It quietly reroutes your calls to an older, still-usable version, and your app keeps running while its behaviour changes underneath you." Documented is not the same as noticed; Meta's fall-forward is in its docs and still generates persistent complaints about silent behavior drift.
- Either way, **follow the sunset date with a grace period returning `410 Gone`** rather than dropping connections - callers get a diagnosable error, not silence.
- Enforcement style can differ per surface of one platform: Meta's Marketing API hard-fails expired calls on a ~90-day window while the core Graph API falls forward for two years - audience sophistication justifies the split. If you split, write both styles into the policy.

## 7. Stand up governance proportionate to blast radius

Governance maturity, not scheme sophistication, is what separates platforms that retire versions cleanly from those that generate incident postmortems. Three stages - grow into them, don't adopt the last one on day one:

1. **Floor: automated diff/linter in CI plus named-engineer sign-off.** Wire an OpenAPI diff or linter (Spectral, Zally, oasdiff) to flag breaking changes mechanically; a staff engineer approves anything flagged. This is the minimum, not a mature end-state.
2. **Review board with a written charter** once the surface outgrows one reviewer: Azure's Breaking Change Review Board blocks spec merges on approval and - the detail worth copying - its typical output is "alternative designs that preserve behavior for current customers," not an approve/reject verdict. The Fuchsia API Council charter is a public template to adapt rather than drafting from scratch.
3. **Full guideline program** at platform scale: Google's AIPs (AIP-180/181 govern compatibility and stability), an enforcing linter, human readability certification, and design review. Google's own "API Governance at Scale" paper records why the layers exist: manual review alone "did not scale well."

The rule that holds at every stage: **no breaking change ships without the governance layer's approval.** AIP-181 calls an in-place breaking change to a stable API "an extreme course of action" requiring governance-team approval - informal ask-around processes are exactly what the staged models above exist to replace.

## 8. Brainstorm candidates, then draft and validate the policy

Do not jump from the interview to a finished document.

1. Present **2-3 candidate policies** - coherent bundles of scheme + windows + enforcement + governance, not per-axis à la carte - each with its trade-offs stated, and name your recommendation with the reason. Example split: a Shopify-shaped calendar policy (quarterly versions, 12-month support, fall-forward), a GitHub-shaped conservative policy (date versions, 24-month notice, hard 410), a Stripe-shaped pinning policy if the promotion conditions from step 3 hold.
2. On the user's pick, draft the policy document section by section against [references/policy-document-template.md](references/policy-document-template.md). **Validate each section with the user before writing the next:**
   - Scheme
   - Definition
   - Windows
   - Communication
   - Enforcement
   - Governance
   - Exceptions
3. Gate finalization on explicit approval of the assembled document.

## Failure modes

Each of these is a documented, named incident pattern - check the draft policy against all of them:

- **A version simultaneously deprecated and default.** Discord served v6 as both for ~1.5 years, then jumped the default to v10 skipping three versions - the deprecation label loses all credibility while you keep handing the deprecated version to new integrators.
- **Unversioned access allowed** - see step 3; removing it later is an unplanned breaking change.
- **Business-motivated changes skipping the process.** Twitter/X gave ~7 days' notice for its 2023 paid-API cutoff - two orders of magnitude off every benchmark, executed after developer relations was laid off - and broke integrators who were willing to pay. Governance discipline matters most exactly when the motive isn't technical, because that is when skipping it is most tempting.
- **Moving sunset dates.** Repeated slippage (Twilio: three extensions) teaches integrators to ignore your dates.
- **Headers-only communication** - signals nobody's tooling reads, satisfying the RFC and reaching no one.
- **Announce-and-walk-away** - the Churn Rule violation: no migration guide, no tooling, no targeted outreach.
- **Undocumented fall-forward** - functionally indistinguishable from a bug report waiting to happen.
- **An undefined clock** - "supported for 2 years" without stating when the 2 years start (Meta's starts at the _next_ release).
- **Treating GraphQL `@deprecated` as removal.** It is a documentation signal; removal requires usage telemetry showing zero real consumers, field by field.

## Measurement

- **Breaking-change frequency** from telemetry: more than ~2/year signals the scheme or the compatibility discipline is wrong (step 2's escape hatch). This is the policy's standing health metric.
- **Migration completion by usage, never by calendar:** a version is removable when telemetry shows zero (or a consciously-accepted residue of) real traffic - an announcement date passing proves nothing about who migrated.
- **Deprecated-version traffic share** trending down after each communication wave tells you which channels actually reach your integrators; a flat line after a mass email is evidence the channel failed, before the sunset date makes it an incident.
- **Date integrity:** count slipped sunset dates. The sourced evidence says slippage is common (Salesforce, Twilio) - the target is zero anyway, because each slip devalues every future date. No industry threshold exists for the traffic metrics; baseline them on your first deprecation cycle and improve against that.

## Invocation examples

- "Write a versioning and deprecation policy for our public REST API - we've never had one and a breaking change is queued."
- "We're retiring /v1 next year - design the sunset timeline, communication plan, and what happens to callers who never migrate."
- "Should our GraphQL API be versioned like our REST API, or evolve continuously? Draft the policy either way."

## References

- [references/versioning-case-studies.md](references/versioning-case-studies.md) - Stripe's gate/transformer mechanics, the conservative platforms (Shopify, LinkedIn, AWS, Azure, Google Maps, PayPal/Braintree), and the cautionary tales (Meta, Discord, Twitter/X).
- `samber/developer-platform-skills@api-error-design` - error codes are API contract too; retiring one runs through this skill's deprecation machinery.
- `samber/developer-platform-skills@webhook-platform-design` - event schema evolution follows the same breaking-change definition and notice discipline defined here.
- `samber/developer-platform-skills@public-graphql-api-design` - the schema-side design that makes step 1's continuous-evolution path possible (additive-friendly payloads, result unions, `@deprecated` field rollover); this skill sets the notice discipline that removal then follows.
- `samber/developer-platform-skills@bulk-data-sharing-design` - bulk file/lake exports evolve their schema under a separate additive-only contract, not this skill's API deprecation machinery.
