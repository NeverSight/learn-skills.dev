---
name: oauth2-provider-design
description: Design the OAuth2 authorization-server surface a B2B SaaS offers third-party apps - the OAuth 2.1 protocol baseline (PKCE for every client, no implicit or password grants, exact redirect matching), token TTL and refresh-rotation policy, scope taxonomy and granularity, consent-screen design with partial and incremental grants, client registration posture, and the tiered app-verification program. Use whenever the user mentions OAuth, "Sign in with X", access and refresh tokens, scopes, consent screens, PKCE, or third-party apps acting on a customer's behalf - even if they never say "OAuth provider". Issuer side only, not integrating against someone else's OAuth. Do NOT use for API-key design - use samber/developer-platform-skills@api-auth-key-management instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# OAuth2 Provider Design

You are an OAuth provider designer. Design the authorization-server surface a platform offers third-party apps: protocol profile, token lifecycle, scope taxonomy, consent screen, registration, verification. Do it so a compromised app or leaked token is a contained event, and so the platform never faces the forced retrofit Salesforce's ISV ecosystem lived through in 2026.

This is decision guidance for a platform/API team, not an RFC tutorial. The target profile is OAuth 2.1, with one precision to carry everywhere:

- RFC 9700 (BCP 240, the OAuth Security Best Current Practice) is final and ratified (January 2025).
- The consolidated OAuth 2.1 document (draft-ietf-oauth-v2-1) remains in draft. Check its current status before citing it as published.

The requirements are settled convergence regardless of the document's own publication status. Never state that OAuth 2.1 itself is a published RFC without first confirming that's still accurate.

## Clarifying questions

Ask before designing anything; each answer changes a later step. Batch them - this is tactical design, not a strategy interview.

1. Greenfield or retrofit? If retrofit: which grants run today, do any clients depend on the implicit or password grant, is refresh rotation on, and roughly how many registered apps exist.
2. Client population: server-side confidential apps, browser SPAs, native/CLI apps, AI agents or MCP hosts? (public vs confidential changes token policy - see step 1)
3. Do apps act only on behalf of a signed-in user, or also with their own identity (bot/app tokens, org-wide access)? (drives scope-to-token-type binding and admin consent - see step 2)
4. Data-sensitivity ceiling: can any scope reach _other users'_ data, bulk data, or regulated financial/health data? (sets the verification tier - see step 3 - and whether step 4 ever matters)
5. Who approves an install: individual end users only, or org admins too? (see the consent-surface split below)
6. Build substrate and effort ceiling: authorization server from scratch, or on an identity product that already ships rotation/DPoP as configuration? When must this ship, and is it a one-off unblock (an enterprise deal demanding OAuth) or the foundation of an app ecosystem? The menus below diverge sharply on effort - re-rank them against these answers.

If your harness has persistent memory, store the core decisions: grant list, TTLs and rotation posture, scope naming convention and token-type binding, verification tiers and thresholds. A later run (a scope addition, a review-program escalation, a token-theft incident) then starts from the design instead of re-deriving it.

## Who consents: end user, org admin, or both

The B2B/B2C split that matters here is who stands between the app and the grant:

- **B2C / individual users**: one consent surface - the end user's screen. Consent copy quality and scope minimalism carry the entire trust decision.
- **B2B / org-owned workspaces**: two consent surfaces. The end user consents, and an org admin can gate installs before or above that (Slack admin-approved apps; Microsoft admin consent, where app-identity permissions can only ever be consented by an admin). Slack's developer guidance names the consequence: "Asking for more permissions than necessary can cause users or admins to reject the installation" - over-scoping is a conversion risk at a gate the end user's "yes" cannot pass for you.

The protocol core, token lifecycle, and plain-language consent-copy rules are identical for both - only the approval topology and the app-identity/org-wide scope tier differ. A B2B provider must design the admin surface (approval queue, org-wide grant review, app-identity permission tier) as a first-class part of steps 2-3, not bolt it on when the first enterprise customer asks.

## Workflow

Build in this order - each stage is load-bearing for the next, and the order is the staged sequence the cross-provider research converged on:

1. Protocol core.
2. Scope taxonomy and consent screen.
3. Registration and verification program.
4. Advanced hardening - only when justified.

## 1. Protocol core

Implement `authorization_code` with PKCE (S256, mandatory for every client - public and confidential alike), `client_credentials`, `refresh_token`, and `device_authorization` (RFC 8628, for CLIs and headless clients). Do not implement `implicit` or the password grant - both are removed under OAuth 2.1; a greenfield server has no reason to ever support them.

- Exact string matching on redirect URIs, with the single standard exception of the port number in native-app `localhost` redirects. RFC 9700's own justification: pattern matching "turned out to be more complex to implement and more error-prone", with "several successful attacks exploiting flaws in the pattern-matching implementation... observed in the wild" (RFC 9700).
- Never accept bearer tokens in URI query strings - Authorization header or POST body only; query strings leak into logs, history, and Referer headers.
- Authorization codes: single-use, maximum 10-minute lifetime (RFC 6749 §4.1, reinforced by RFC 9700).
- Access tokens: default ~1 hour - the cross-provider convergence point (GitHub App and Google tokens ~1h, Microsoft Entra 60-90 min; provider docs - full table in [references/protocol-baseline.md](references/protocol-baseline.md)). Keep JWT access tokens short specifically because a JWT can't be revoked mid-lifetime the way an opaque database-backed token can.

**Refresh-token posture** - three candidates, ranked:

- security value: `sender-constrained (DPoP) > rotation + reuse detection > non-rotating with a per-client cap`
- third-party client-library compatibility: `non-rotating > rotation > DPoP`
- effort: `DPoP > rotation > non-rotating`
- efficiency: `rotation + reuse detection > non-rotating > DPoP`

- **Default rung: rotation with token-family reuse detection.** Every refresh token belongs to a family traceable to the original grant; a consumed token presented again revokes the whole family (the Auth0/Keycloak/Django OAuth Toolkit convergent pattern). Ship a reuse grace window from day one - around 10-30 seconds - or multi-tab SPAs and network retries will read as attacks and log real users out. RFC 9700 §4.14 states what the tripwire buys: the server "cannot determine which party submitted the invalid refresh token, but it will revoke the active refresh token" - it's a tripwire, not an investigation tool.
- **DPoP is the starved option**: strongest posture, and near-zero ecosystem support - 0 of 18 mainstream issuers with a working discovery document advertised DPoP support (MojoAuth issuer survey). Promote it when tokens guard financial or health data (FAPI 2.0 accepts DPoP or mTLS as its baseline) or when long-lived AI-agent tokens widen the theft blast radius; Bluesky's mandatory-DPoP deployment proves it production-viable at scale. Otherwise it's a support burden few client libraries can even meet yet - Stage 4, not here.
- **Non-rotating survives only in two bounded forms:**

  - Confidential clients, whose client authentication already sender-constrains redemption (RFC 9449's own carve-out - this is why 2.1 mandates "sender-constrained or rotated" only for public clients).
  - Google's capped-population model (max 100 refresh tokens per account per client, oldest silently invalidated; Google docs - this figure moved from a cached "50", re-verify at implementation).

  An indefinitely-reusable refresh token for a public client is not a rung to demote - it's banned under 2.1; delete it from the menu.

- Cap refresh-token lifetime hardest for browser clients: Microsoft's SPA-specific 24-hour refresh-token lifetime, versus 90-day inactivity elsewhere (Microsoft Learn), is the reusable threshold - a refresh token in browser storage is a structurally higher-exposure asset.
- This ranking is a default, not a law - re-rank against question 6: a provider building on an identity product that ships DPoP as configuration (Keycloak 26.4 does; vendor docs) flips DPoP's effort line, and a retrofit with thousands of live integrations flips rotation's.

Endpoints, storage mechanics (hashed tokens vs the grace window's cleartext need), and the compliance-gate pattern: [references/protocol-baseline.md](references/protocol-baseline.md).

## 2. Scope taxonomy and consent screen

Two granularity rungs, ranked - the broad catch-all scope is deleted below, not ranked:

- blast-radius containment: `fine-grained per-resource permissions > resource:action scopes`
- integrating developer's effort: `fine-grained > resource:action` (more decisions per install)
- provider effort: `fine-grained > resource:action` (a permission taxonomy is a quarters-long project)
- efficiency: `resource:action > fine-grained`

- **Default rung: `resource:action` naming with a read/write split and read-only defaults** - the dominant idiom across Slack, Microsoft Graph, and Stripe Connect (provider docs; comparison table in [references/scope-taxonomy-archetypes.md](references/scope-taxonomy-archetypes.md)). Name scopes after the same resource nouns the API itself uses - `samber/developer-platform-skills@public-api-design-review` owns that naming consistency.
- **Fine-grained per-resource permissions are the starved option** (GitHub Apps: 50+ independent permissions, per-repository restriction, 1-hour installation tokens; GitHub docs) - promoted when org admins demand approval policies, a compliance regime is in scope, or scopes reach org-wide data. Budget for the documented cost: GitHub's own fine-grained model still "cannot accomplish every task" the classic broad model can (GitHub docs). Granular models lag broad ones in edge-case coverage through the whole transition, so keep the coarse tier alive during migration rather than forcing a lossy cutover.
- **Deleted anti-pattern, not a bottom rung: the single broad catch-all scope.** GitHub's classic `repo` grants read and write to everything with no way to request less. GitHub's own fine-grained-PAT launch post frames coarse scopes plus immortal tokens as a leading contributor to real breaches (GitHub blog, 2022). Designing one in 2026 is choosing the failure mode the entire field is migrating off.

Taxonomy rules that are cheap now and ruinous to retrofit:

- **Additive-only, forever**: never repurpose an existing scope's meaning - repurposing silently changes what already-granted consents authorize, and scope changes invalidate refresh tokens, forcing re-consent (Google docs).
- **Bind every scope to a token type on day one** if apps can hold both app-identity and user-delegated access. Slack's same `chat:write` posts as the app on a bot token and as the human on a user token, and its own migration guidance warns that changing that binding later "requires reauthorization from every user" (Slack docs). Microsoft expresses the identical split as delegated-vs-application permissions with admin-only consent on the application side.
- Accept scope explosion as granularity's price where the resource types genuinely differ (Slack: four separate history scopes across conversation types) - the alternative is a DM grant that silently includes private channels.

Consent screen:

- Translate every scope into a plain-language sentence, per-scope - never grouped buckets, never the raw scope string.
- Support partial grants, and **diff granted-vs-requested scopes server-side, always**. With granular consent, the response scope set may not match the request even when the user appears to approve everything - a provider that assumes they match ships a silent capability mismatch into every integrating app (Google's granular-permissions model documents this trap).
- Support incremental authorization (request a scope when the feature needs it, not upfront), and design the re-consent screen to show **only the net-new scope**. Google's own implementation re-displays everything already granted alongside the delta, a documented practitioner complaint (GMass) about making integrating developers "look sloppy".
- No rigorous consent-conversion study exists - circulating drop-off percentages trace to vendor blogs, not measurements. Argue consent design on security and UX grounds; never cite a conversion figure as fact.

Full archetypes and consent mechanics: [references/scope-taxonomy-archetypes.md](references/scope-taxonomy-archetypes.md), [references/consent-screen-design.md](references/consent-screen-design.md).

## 3. Registration and verification program

**Client registration** - two rungs, ranked by control retained per unit of onboarding friction; open dynamic registration is deleted below, not ranked:

- control over who integrates: `manual/reviewed registration > gated dynamic registration`
- integration friction for developers: `manual > gated dynamic`
- efficiency: `manual/reviewed > gated dynamic`

- **Default: manual developer-portal registration with a review step.** The negative finding is the argument: no major B2B SaaS platform offers ungated public dynamic client registration - GitHub, Slack, Stripe, and Salesforce all require portal registration plus review. When every legitimate client goes through onboarding anyway, DCR's core value (registering a client with no prior relationship) doesn't apply.
- **Promote to gated DCR (RFC 7591 behind an initial access token, rate-limited, all metadata treated as untrusted input)** only when deliberately serving an MCP/AI-agent ecosystem where clients discover servers dynamically - the one population that can't pre-register.
- **Open, ungated DCR is deleted, not demoted**: a May 2026 preprint probing 119 OAuth-enabled remote MCP servers found DCR flaws in 96.6% of them, and the MCP spec itself walked DCR from SHOULD to MAY to deprecated across 2025-2026 (MCP spec revisions). Self-asserted registration metadata can impersonate any legitimate app's name and logo unless cryptographically attested - an open endpoint is a phishing kit.

**Verification tiers** - rank review depth by trust bought per unit of developer friction, and scale it to data sensitivity, never one bar for all apps:

- trust signal bought: `third-party security assessment > self-attestation > publisher identity verification`
- developer friction: `third-party assessment > self-attestation > identity verification`
- efficiency: `identity verification > self-attestation > third-party assessment`

- **Default rung: publisher identity verification for every listed app** - Microsoft's model: domain plus verified partner account, no fee, "verified in minutes" for a prepared publisher (Microsoft Learn). It proves continuity of identity, not quality - and pair it with Microsoft's real enforcement lever: unverified publishers can't receive consent for permissions beyond basic profile in risk-managed tenants.
- **Self-attestation is the middle rung** - cheap (Microsoft: "most attestations can be completed in one hour or less") and explicitly not independently verified (Microsoft Learn). Keep the three signals visually distinct on your listing surface: Microsoft's own docs say the identity badge "doesn't imply or indicate quality criteria" - one undifferentiated checkmark for identity, attestation, and audit misleads every buyer reading it.
- **Mandatory third-party security assessment is the starved rung**: months of calendar time, plus a direct assessor fee the _developer_ pays rather than you. That fee runs roughly an order of magnitude higher for the full-pentest tier than for the scan tier (community-reported CASA pricing; figures in the reference). One bright-line condition every studied program draws promotes it: **the moment a scope grants access to other users' data or PII, not just the requesting user's own** (cross-provider review-program comparison), with annual recurrence on CASA's 12-month cadence.
- Give unverified apps a legitimate testing lane, modeled on Google's: bounded named test users, a visible warning screen, and hard ceilings - Google's is a 100-user lifetime cap that verification alone lifts (current Google docs; older sources say 50) plus 7-day test-token expiry. "Verify before you scale" only works when the ceiling is real.
- Enforce at runtime, not just at review: reject any scope request that isn't a subset of what was declared and approved at registration - Google's unverified-app warning fires exactly on that divergence, because declarations drift.

The cautionary tale to cite when this stage gets deprioritized: the August 2025 Salesloft Drift OAuth-token campaign hit 700+ organizations (Google Threat Intelligence/Mandiant). Salesforce's response, four mandatory OAuth controls including PKCE and rotation on all connected apps enforced May 11, 2026 with de-listing as the penalty (Salesforce ISV communications), is what a forced retrofit looks like. Full program comparison: [references/app-verification-program.md](references/app-verification-program.md).

## 4. Advanced hardening - when justified

- **DPoP/mTLS sender-constraining**: differentiation, not baseline - the same 18-issuer survey found exactly one (Microsoft Entra) advertising mTLS and zero advertising DPoP or PAR (MojoAuth survey). Runtime cost is not the blocker (~2-10ms per request for DPoP, ~5-15ms per connection for mTLS) - absent client-library support is. Adopt when question 4 answered financial/health data or long-lived agent tokens.
- **PAR (RFC 9126) + Rich Authorization Requests**: for transaction-level consent - rendering "transfer $500 to account ending 4321" instead of a generic payment scope - and keeping that payload out of browser URLs. Named mechanisms to reach for at FAPI-adjacent sensitivity; noise for a typical B2B SaaS consent flow.
- Gated DCR, if question 2 surfaced an MCP/agent ecosystem (see step 3).

## Failure modes

Each is a named, documented trap - not a hypothetical:

- Shipping the implicit or password grant on a new server, or prefix/pattern redirect matching - the exact holes 2.1 closed after in-the-wild exploitation.
- Rotation without a grace window: legitimate concurrent refreshes (multi-tab, retries) trip reuse detection and log users out.
- Hashing refresh tokens at rest without handling the grace window's need to recognize a just-consumed token - a documented design tension to resolve deliberately (Django OAuth Toolkit docs), not discover in production.
- Assuming the granted scope set equals the requested one - partial consent makes the diff mandatory.
- Re-consent screens that re-display every already-granted scope instead of the delta.
- Repurposing an existing scope's meaning instead of adding a new scope.
- Deferring the bot-vs-user token-type split, then paying Slack's documented price: reauthorization from every user.
- One visual trust badge conflating identity verification, self-attestation, and independent audit.
- An open dynamic-registration endpoint.
- A testing lane whose user cap isn't enforced, or verification checked only at review time while runtime scope requests drift.
- Citing a consent drop-off percentage as measured fact.

## Measurement

Gates - iterate until every one passes:

- Protocol: the discovery document and a conformance pass show no implicit/password grant, PKCE rejected-if-absent for every client, exact redirect matching - verified by test, not assertion.
- Token lifecycle: reuse detection demonstrated in staging (replayed refresh token revokes the family); a concurrent-refresh test passes without a false-positive logout.
- Consent: every scope has per-scope plain-language copy; a partial-grant integration test exercises the server-side diff.
- Verification: every scope is classified into a tier with a named review requirement; runtime subset-of-approved enforcement is live; the unverified-lane cap is enforced, not documented.

Trends to baseline from launch (no industry thresholds exist): median app-review turnaround, share of apps requesting scopes their traffic never uses, reuse-detection trip rate (a proxy for both attacks and a too-tight grace window).

## Invocation examples

- "We're adding 'Sign in with Acme' and a third-party app directory - design the OAuth provider side."
- "Define the scope taxonomy for our public API's OAuth apps - today we have one `full_access` scope."
- "Our consent screen is a wall of scary permissions and admins keep rejecting installs - redesign it."
- "Set token TTLs and the refresh rotation policy for our authorization server."
- "Design the app verification program before we open the integrations directory."

## References

See also, same collection:

- `samber/developer-platform-skills@api-auth-key-management` - the key-or-OAuth boundary decision and everything on the key side of it; this skill starts once that decision lands on OAuth for third-party apps.
- `samber/developer-platform-skills@mcp-server-offering` - the MCP resource-server posture that consumes the authorization server designed here.
- `samber/developer-platform-skills@api-versioning-policy` - deprecating a scope or sunsetting a grant type follows the same notice-window and sunset-signalling discipline as any breaking API change.
- `samber/developer-platform-skills@app-marketplace-review` - the ongoing security/quality review process for listed apps; step 3 here designs the verification gate; that skill owns the standing review operation behind the marketplace.
