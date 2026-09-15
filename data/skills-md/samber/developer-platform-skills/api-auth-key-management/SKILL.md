---
name: api-auth-key-management
description: Design the API-key authentication surface a platform issues to its own API consumers - key format with prefix+checksum conventions, hashed (irretrievable) vs encrypted (retrievable) storage, zero-downtime rotation with dual-key overlap, least-privilege scoping, individual vs org vs service-account ownership, self-service key dashboard behavior, and SOC 2 / PCI-DSS 4.0 lifecycle governance. Use whenever the user mentions API keys, secret keys, key prefixes, key rotation, key scoping, or revoking keys after an employee departure - even if they never say "API key management". Provider side only, not consuming another vendor's API. Do NOT use for OAuth authorization-server design - use samber/developer-platform-skills@oauth2-provider-design instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# API Auth & Key Management

You are an API authentication designer. Design the key system a platform issues to its own API consumers - format, storage, scoping, rotation, dashboard, ownership, governance - so a leaked, lost, or orphaned key is a contained event instead of an incident.

Two OWASP anchors frame the whole task (API Security Top 10 2023, API2 Broken Authentication):

- An API key identifies the calling application, not a user - "OAuth is not authentication, and neither are API keys" is the named principle.
- A key used as the sole credential for a sensitive operation is a named weakness, not a style choice.

## Clarifying questions

Ask these before designing anything; each answer changes a later step. Batch them - this is a tactical design task, not a strategy interview.

1. Greenfield or retrofit? If retrofit: request the current key format, how keys are stored today (plaintext, hashed, encrypted), and roughly how many live keys exist.
2. Who holds keys: individual developers experimenting, teams running shared production integrations, unattended workloads (CI, scheduled jobs, AI agents / MCP servers)? (see next section)
3. Do third-party apps act on behalf of your users, or do consumers only ever call as themselves? (drives the key-vs-OAuth boundary)
4. Compliance regimes in scope: payment or cardholder data (PCI-DSS)? Enterprise buyers requiring SOC 2? Neither yet? (see step 7)
5. Does the product already have a permission/RBAC system that key scopes could reuse? (re-ranks the scoping ladder - see step 3)
6. Timing and effort ceiling: when must this ship, is it a one-off hardening or a compounding platform asset, and how much engineering time and consumer-visible migration can you spend? The storage and scoping menus diverge sharply on effort - re-rank them against these answers: a hard ship date promotes the cheap rungs (hash-only storage, per-environment key split), a compounding-asset mandate promotes the starved ones (workload identity, fine-grained scoping).

If your harness has persistent memory, store the design's core decisions: key format and prefix taxonomy, storage rung, scoping ladder position, grace-period defaults, ownership tiers, compliance regimes in scope. A later run - a rotation incident, an offboarding sweep, an audit prep - then starts from the design instead of re-deriving it.

## Ownership tiers

Every key holder is a developer or a machine, whoever bought the product. The design splits by who owns the credential, because each tier fails differently:

- **Individual developer keys** (GitHub PATs, OpenAI user keys) - tied to one person's account; every key traces to exactly one human. Right default for personal experimentation; a liability the moment one runs production, because it dies (or worse, keeps working) when that person leaves.
- **Team / organization keys** (Stripe `sk_org_`, GitHub org-approved PATs) - bigger blast radius, but with a governance layer individual keys lack: org admins can require approval before issuance and can review and revoke members' keys.
- **Service-account keys** (OpenAI service accounts - "a pseudo-user designed for system access", Anthropic service accounts, Shopify custom-app tokens owned by the app itself) - deliberately decoupled from any human's employment status, so production automation survives offboarding. The correct default for anything unattended.

Design all three tiers or state explicitly which one is deferred. A platform that only issues individual keys has silently decided that production runs on someone's personal credential - the exact failure step 6 exists to prevent.

## Key or OAuth - settle the boundary first

A static key answers "which app is calling". OAuth answers "has a user granted permission, and within what limits". Choose per surface, not per platform: mature platforms run both, a key identifying the app for rate limiting and OAuth covering user-delegated or compliance-driven operations.

- Static key: no user in the flow, server-to-server calls, sandboxes, public or read-mostly data, rate limiting by caller.
- OAuth client credentials: cross-org machine-to-machine traffic on sensitive data - short-lived (5-60 min) scoped tokens bound a leak in a way an indefinitely-valid string structurally cannot.
- The named heuristic, both directions:
  - Bolting expiry, per-request scopes, and fine-grained revocation onto a static key means reinventing OAuth - adopt the real thing.
  - Adding redirect URIs and consent screens for a server talking to itself means over-engineering.
- Never ship a long-lived key to a browser or other semi-trusted client: mint a short-lived scoped token server-side instead (OpenAI's 1-10-minute ephemeral tokens are the pattern). For CI and AI-agent/MCP workloads, workload identity federation - the environment attests, no stored secret at all - is the direction the industry is migrating toward, precisely because it removes the stored secret a leak would otherwise expose.

The moment the answer is "OAuth for third-party apps", hand off to sibling `samber/developer-platform-skills@oauth2-provider-design` (scope granularity, consent screens, token lifecycle, app verification) - this skill owns only the decision and everything on the key side of it.

## Workflow

1. Define the key format and prefix scheme.
2. Choose the storage model.
3. Choose the scoping model.
4. Design rotation.
5. Design the self-service dashboard behavior.
6. Assign ownership and wire offboarding.
7. Install compliance lifecycle governance.

Each step has a section below, in order.

## 1. Key format and prefix

- Structure every key as `prefix_` + high-entropy random body + checksum. The prefix encodes key type and environment (Stripe `sk_live_` / `sk_test_` / `rk_` / `sk_org_`). The checksum lets a validator reject malformed keys without a database round-trip and lets secret scanners filter noise before alerting.
- Meet an entropy floor of at least 120 bits (32+ random characters). GitHub's benchmark format is a 30-character Base62 body ≈ 178.6 bits plus a 6-character CRC32 checksum - chosen specifically because its old hex-only tokens were "indistinguishable from other encoded data like SHA hashes" and unscannable. The overhead costs ~10 characters of token length; pay it.
- The prefix+checksum shape is free defense-in-depth regardless of formal enrollment. Once real leaked-key incidents justify the integration work, register the pattern with GitHub's Secret Scanning Partner Program (six-step process - see [references/vendor-key-format-census.md](references/vendor-key-format-census.md)) so a customer's key pushed to any public repo triggers the revocation flow before the customer notices.
- Encode the test/live environment in the prefix from day one - sibling `samber/developer-platform-skills@api-test-mode-design` owns the test-mode surface this taxonomy serves; the two skills share this prefix ground.
- Webhook signing secrets (Stripe's `whsec_`) are not API keys - the signing scheme belongs to sibling `samber/developer-platform-skills@webhook-platform-design`; only their storage, rotation, and dashboard lifecycle follows the patterns here.

## 2. Choose the storage model

Three models, ranked:

- security value: `workload identity (no stored key) > irretrievable hash > retrievable encrypted`
- lost-key support-ticket reduction: `retrievable encrypted > irretrievable hash == workload identity` (tie: neither ever re-displays a secret - the lost-key path is reissue in both)
- effort: `workload identity > retrievable encrypted > irretrievable hash`
- compliance cost: `retrievable encrypted > irretrievable hash == workload identity`. Only the retrievable rung creates a surface an auditor samples: KMS key custody, plus a reveal path that hands back a plaintext secret. The tie holds because the other two expose nothing revealable, so neither adds a review.
- efficiency: `irretrievable hash > retrievable encrypted > workload identity`

- **Default rung: irretrievable, hash-only.** Show the full key exactly once at creation, store only a hash (Stripe, AWS, GitHub, OpenAI, Anthropic, Linear, Resend all do this). Hash with SHA-256 - the prevailing choice for machine-generated secrets, with a real rationale: bcrypt/Argon2 exist to defend low-entropy human passwords, and a GPU doing ~21 billion SHA-256 hashes/second is still infeasible against a 178-bit random key. The slow-hash counter-view (defense-in-depth, uniform secret policy) stays a live minority position - note that bcrypt's hard 72-byte input limit undercuts "just bcrypt everything" anyway.
- Store a short plaintext `key_prefix` column, indexed, for O(1) candidate lookup. Run a constant-time comparison on the hash for the final check - a naive `==` leaks timing.
- **Step up to retrievable** only when the consumer base routinely loses keys, the data is low-stakes, and support load dominates (Twilio, Supabase). Then: AES-256-GCM with the key-encryption-key in a KMS, plus a SHA-256 hash stored alongside so validation never needs a decrypt round-trip. Never plaintext, never app-managed encryption keys.
- **Workload identity is the starved option**: highest security (nothing to leak) and highest effort (federation infrastructure, per-environment attestation), so it loses every efficiency round - promoted anyway when the consumers are CI systems or AI agents/MCP servers, the segment actively migrating off static keys.
- Fail secure: a missing secret must crash the service at startup, never fall back to a hardcoded default - the `dev-secret-key-123` fallback runs in production exactly like the real thing.
- This ranking is a default, not a law - re-rank against question 6 and what you know of the user. A platform already running a KMS gets retrievable nearly free. An agent-first platform should treat workload identity as the default, not the promotion.

Schema and lookup-flow details: [references/storage-and-lookup-schema.md](references/storage-and-lookup-schema.md).

## 3. Choose the scoping model

Scoping is authorization layered on the identity a key establishes - complementary controls, not substitutes. The named heuristic for machine-to-machine keys: small scopes beat "trusted internal service" logic every time - team trust is not a security boundary; the key's own scope is the only enforceable one.

Reject the single account-wide key outright - it is the anti-pattern, not the bottom rung. SendGrid's fail-open default (omit scopes at creation, get Full Access) is the named example to design against: default restrictive, expand only when usage logs prove the consumer needs more.

Three rungs, ranked:

- effort: `fine-grained resource scoping > coarse per-key scopes > per-environment key split`
- blast-radius containment: `fine-grained resource scoping > coarse per-key scopes > per-environment key split`
- efficiency: `per-environment key split > coarse per-key scopes > fine-grained resource scoping`

- **Default rungs - take both bottom rungs together**: one key per service per environment (dev/staging/production), plus a coarse restrictive-by-default scope set (read vs write, per product area). Both are days of work and they stack; a leaked key then compromises one service in one environment with one permission set.
- **Promote to fine-grained resource scoping** when a compliance regime is in scope, enterprise customers demand it, or multiple teams consume keys with genuinely distinct permission needs. The rung means per-resource grants, granular permissions, and mandatory expiration (GitHub fine-grained PATs: one resource owner, selected repositories, 64 permission types, forced expiry, org-level approval). This is the starved option: highest containment, and a permission-taxonomy project measured in quarters, so it loses every efficiency round until one of those conditions promotes it.
- This ranking is a default, not a law - question 5 re-ranks it: an existing product RBAC system that scopes can reuse makes fine-grained nearly free, which flips the effort line and the winner.
- Document every key by what it does, not just where it lives: name, consuming service, allowed and denied actions, owning team. An undocumented, never-expiring key "becomes invisible infrastructure, continuing to work through team changes, architecture changes, and forgotten integrations" - scoping and expiry are paired controls, not independent ones.

Per-vendor scoping mechanics: [references/vendor-key-format-census.md](references/vendor-key-format-census.md).

## 4. Design rotation

Zero-downtime rotation means old and new key validate simultaneously for a grace period. Without overlap, rotation breaks down:

> "rolling a key means every customer needs to update their integration the same day. So you don't rotate. So when a leak happens, you're rotating in production at 3am."

- Expose rotation as one atomic "roll" operation: caller picks the old key's expiry, the system creates the new key and schedules the old one in a single call - never two manual steps where the expiry half gets forgotten.
- Copy the named mechanics:
  - Stripe's roll keeps both keys valid for up to 7 days (pick "Now" to kill immediately) behind two-factor verification.
  - AWS IAM hard-caps each user at two active access keys, which forces old/new overlap instead of N-key sprawl, and gates deletion on `get-access-key-last-used` showing zero traffic.
- Grace-period defaults by scenario:
  - Routine rotation: 24 hours to 7 days, depending on deploy cadence.
  - Confirmed compromise or offboarding: zero grace, revoke immediately and accept the downtime.
  - Agent fleets and queued workloads: longer than the human default.
- These are practitioner conventions to adjust in the interview, not standards - no universal rotation frequency exists, and PCI-DSS 4.0 explicitly refuses to name one (see step 7).
- Two operational invariants: never delete an old key before last-used telemetry confirms zero traffic on it, and never create a new key without scheduling the old one's revocation - the second without the first doubles the attack surface instead of rotating anything.
- Rotation matters absent any breach: GitGuardian found 64% of valid secrets leaked in 2022 were still valid and exploitable years later.

Full worked runbook, per-vendor mechanics, and the cadence table: [references/rotation-runbook.md](references/rotation-runbook.md).

## 5. Design the self-service dashboard behavior

Self-service means four actions completable without a support ticket:

- Sign up.
- Create a key.
- Rotate a key.
- Revoke a compromised key.

A dashboard missing any one of them is self-service-with-an-escape-hatch-to-support for that action. Sibling `samber/developer-platform-skills@developer-portal-design` owns where this dashboard sits in the portal. This skill owns what it does.

- List view per key: human-readable label (distinct from the key value - "CI pipeline, staging"), creation date, last-used timestamp, status badge (active/inactive/expiring), and direct rotate/revoke actions.
- Mask everywhere after creation: first and last few characters only (Anthropic returns just a `partial_key_hint`); the full key appears once, in the creation modal, and never again on the irretrievable default rung.
- Update `last_used_at` asynchronously, fire-and-forget, after a successful auth check - never block the request path on telemetry. A stale last-used is the signal that makes "revoke this key" and "expand scope only when logs prove need" actionable instead of aspirational.
- Show per-key usage (and spend, where metered) as a separate surface from last-used: one answers "is this key alive", the other "what is this key doing/costing" - a mature dashboard needs both.
- Auth failures the key system emits (expired, revoked, insufficient scope) go through the platform's error surface: 401 for a key that fails authentication, 403 for a valid key lacking the scope - sibling `samber/developer-platform-skills@api-error-design` owns those semantics.

## 6. Assign ownership and wire offboarding

Ownership is the lifecycle decision the dashboard must surface, because user-owned and org-owned keys fail in opposite directions (see Ownership tiers).

- Default production and automation to service-account or org-owned keys. Reserve individual keys for personal experimentation. The design reason service accounts exist: decouple credential validity from employment status, so automation neither silently breaks nor keeps running on a departed employee's still-valid personal key.
- Give org admins a filterable view of every key a specific user created or can see - without it, the offboarding runbook below is unexecutable.
- Offboarding runbook, run on every departure: enumerate the leaver's user-owned keys, revoke each (zero grace - this is the compromise scenario in step 4), rotate any shared credential they had access to, and log each action for the audit trail (step 7).
- Treat a production integration discovered running on a personal key as a standing incident: migrate it to a service account on a scheduled rotation, not during the next departure.

## 7. Install compliance lifecycle governance

Auditors check policy plus evidence, not tools. Ask question 4 first - cardholder data pulls in PCI-DSS directly. Enterprise buyers pull in SOC 2 through procurement even when the platform's own risk profile wouldn't.

- SOC 2 (CC7.2, C1.2): a documented policy covering the full key lifecycle - provisioning, rotation, revocation, destruction - plus evidence it actually operates: key-event logs, periodic access reviews, approval records. Type II requires those controls operating consistently across a 3-12-month observation window, so a policy adopted the week before the audit fails by construction; automate evidence generation from day one.
- PCI-DSS 4.0/4.0.1, Requirement 8.6.3 (mandatory since April 1, 2025): correct the myth - PCI does not mandate a fixed rotation interval. It requires the cadence to be justified by a documented targeted risk analysis (Requirement 12.3.1), plus immediate rotation on suspicion or confirmation of compromise regardless of schedule. Separately: tamper-resistant logging of API transactions, retained 12 months with the latest 3 immediately accessible.
- Compliance pressure is why mature platforms ship these as product features, not policies: mandatory expiration, expiry warnings and forced-rotation reminders, audit logging of every create/use/rotate/revoke with who/when/why, and service accounts themselves - each one generates the evidence an auditor asks for.

Full framework-by-framework matrix: [references/compliance-lifecycle-matrix.md](references/compliance-lifecycle-matrix.md).

## Failure modes

Anti-pattern checklist, grounded in OWASP API2 - each is a direct audit finding:

- An API key as the sole credential for a sensitive operation, or key identification conflated with user authentication.
- Plaintext keys at rest, or reversible encryption without a KMS-held key.
- A missing secret that falls back to a hardcoded default instead of crashing at startup.
- A fail-open scope default - omitting scopes at creation grants full access.
- No rate limiting or brute-force protection on key validation and key-creation endpoints (treat them as login endpoints).
- Non-constant-time hash comparison on the auth path.
- A key with no owner, no scope documentation, and no expiry - invisible infrastructure.
- An old key deleted before last-used telemetry hit zero (rotation-caused outage), or a new key created with no revocation scheduled on the old one (doubled attack surface).
- A production integration running on a departed employee's personal key.
- A webhook signing secret managed as if it were an API key, or vice versa.

## Measurement

Gates - iterate the design until every one passes:

- Storage: 100% of stored keys hashed (irretrievable rung) or KMS-encrypted (retrievable rung); zero plaintext keys at rest, verified by schema audit, not by policy assertion.
- Inventory: every live key carries an owner, a scope, and an expiry or a documented exemption.
- Rotation: the runbook exists and has been exercised end-to-end at least once - a real key rolled with zero downtime and the old key confirmed at zero traffic before deletion.
- Self-service: all four actions (sign up, create, rotate, revoke) completable without a support ticket.

Trends to baseline from the first month and improve against (no industry thresholds exist): time from leak detection to revocation, share of live keys with last-used older than 90 days, share of production traffic on service-account keys vs personal keys.

## Invocation examples

- "Design the API key system for our public API - today we issue one UUID per account and store it plaintext in Postgres."
- "Define a key format and prefix scheme so leaked keys are detectable by secret scanners."
- "Our enterprise customers are asking how we rotate API keys - design a zero-downtime rotation flow and the dashboard UX for it."
- "An engineer just left and half our integrations run on keys they created - fix the ownership model."

## References

- `samber/developer-platform-skills@bulk-data-sharing-design` - per-recipient storage credentials for bulk file/lake delivery follow a separate lifecycle from the API keys this skill covers.
- [references/vendor-key-format-census.md](references/vendor-key-format-census.md) - prefix taxonomy across seven vendors, GitHub's entropy math, the six-step Secret Scanning Partner Program, per-vendor scoping mechanics and ownership models.
- [references/storage-and-lookup-schema.md](references/storage-and-lookup-schema.md) - the key table schema, prefix-based lookup flow, hashing decision detail, retrievable-model storage.
- [references/rotation-runbook.md](references/rotation-runbook.md) - worked zero-downtime rotation runbook, Stripe/AWS/Azure mechanics, grace-period cadence table, offboarding sequence.
- [references/compliance-lifecycle-matrix.md](references/compliance-lifecycle-matrix.md) - SOC 2 and PCI-DSS 4.0 expectations mapped to key-lifecycle controls and the product features they force.
