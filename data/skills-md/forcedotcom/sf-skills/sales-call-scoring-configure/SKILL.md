---
name: sales-call-scoring-configure
description: "Configure, set up, or repair AI Call Scoring (a.k.a. Call Coaching / Coaching Competencies) on an ECI-enabled Salesforce org. Flips ECICallScoringEnabled via SOAP Metadata API, enables Einstein Generative AI Platform if off, and manages Coaching Competency records (EnablementCompetencyDef Tooling API): install the 6 OOTB set, the 7 Momentum best-practice prompts, or conversationally author/edit/activate/deactivate custom competencies (8-active + 16000/255-char caps). TRIGGER when: user wants to turn on AI Call Scoring or Call Coaching, install OOTB or best-practice competencies, create/edit custom competencies, re-enable after sandbox refresh, or verify/repair partial Call Coaching setup on a 68+ ECI org. DO NOT TRIGGER when: no ECI license (direct to Agentforce for Sales), user wants to enable ECI/Momentum themselves (out of scope — Setup), Pipeline Management (use sales-agentforce-pipeline-management-configure), or custom agent (use agentforce-generate)."
metadata:
  version: "1.0"
  domains: ["Sales"]
  minApiVersion: "68.0"
  relatedSkills:
    - "sales-agentforce-pipeline-management-configure"
    - "agentforce-generate"
  cliTools:
    - tool: ["sf"]
      semver: ">=2.0.0"
    - tool: ["jq"]
      semver: ">=1.6.0"
    - tool: ["curl"]
      semver: ">=7.0.0"
  accessCheck: "(OrgPreferences.ConversationPilotPref) && (UserPermissions.ModifyAllData)"
---

# Sales Call Scoring — Configure

Configure **Call Coaching** (a.k.a. AI Call Scoring / Coaching Competencies)
on a Salesforce org. Detects the org's current state, enables dependent
features it is authorized to enable, and flips the `ECICallScoringEnabled`
org preference via the SOAP Metadata API.

## Scope

**In scope**
- **ECI-enabled orgs only.** The skill supports orgs on the ECI (Einstein
  Conversation Insights) arm (spike scope: ECI-only for MVP).
- Detect which of the 4 PRD-scoped org states the org is in.
- Enable **Einstein Generative AI Platform** if off (PRD-authorized dependency).
- Flip `enableECICallScoring` to `true` via SOAP Metadata API v68.
- Verify the change took effect.
- Idempotent — clean exit on states 3 and 4 (already enabled).

**Out of scope**
- **River Rush / Momentum detection.** Deferred until that arm goes live —
  see Key Considerations. A Momentum-only org today is not distinguished
  from any other ECI-off org; it gets the generic "ECI is not enabled"
  message from Phase 3, not a Momentum-specific one.
- **Enabling ECI or Momentum themselves.** PRD-explicit out-of-scope; the skill
  detects and messages the admin to enable ECI via Setup.
- **License provisioning.** Missing base licenses (Agentforce for Sales, ECI
  license) require an account-team ticket.
- **Competency CRUD.** Handled by sibling scripts in this same skill — see "Competency CRUD workflow" below (§S3-§S10) and the "Execution sequence" matrix.

## Prerequisites

1. **`sf` CLI authenticated** — `sf org login web --alias <org-alias>`.
2. ECI arm licensed and enabled: `ConversationPilot` org permission (Phase 0
   purchase gate) and `enableCallCoaching` pref (Phase 1, the
   `ConversationPilotPref` preference). (River Rush/Momentum is a separate
   arm covered by the same server-side gate but not checked by this skill
   yet — see Key Considerations.)
3. Site gate `com.salesforce.eci.callScoringEnabled` open on the org's pod
   (RelEng-controlled; not admin-toggleable).

Einstein GenAI Platform is a soft prerequisite — the skill enables it
automatically when off.

## Clarifying Questions

Ask the admin: target org alias? Sandbox refresh scenario? (The pref has
`disableOnSandboxCopy=true`, so it must be re-flipped after every refresh —
that's normal, not a failure.)

## Admin Communication Guidelines

**CRITICAL**: This skill serves admin users, not developers. The full 13-rule spec with rationale for each rule lives in [`references/admin-communication.md`](references/admin-communication.md) — consult it before your first response in this skill. Summary of the load-bearing rules:

1. **Run all bash commands in background** (`run_in_background: true`).
2. **Speak admin language, not entity language** — "Call Coaching", "Coaching Competency", "active/inactive". Never `EnablementCompetencyDef`, `enableECICallScoring`, `EvaluationInstructions`, `SourceCompetencyTemplate` in primary chat text.
3. **Hide technical details** — no record Ids, DeveloperNames, Template enum keys, HTTP codes, SOAP responses, curl/jq internals, script paths, or phase numbers. Exception: the S9 verify markdown table (see [`references/competency-crud.md`](references/competency-crud.md) §S9).
4. **Chain automatically** — when a script prints `Next: <script>`, run it in the same turn without asking. **Exception**: State 3 → rule #13.
5. **Ask OOTB-vs-custom once** — on first-time competency setup (State 3, unqualified intent), render `install-ootb-competencies.sh --list` and let the admin choose. Only checkpoint in this skill where Claude asks before writing.
6. **Idempotency is silent** — if already on/installed, say so briefly and move on.

See [`references/admin-communication.md`](references/admin-communication.md) for the full 13-rule spec, including error-surfacing, outcome-vs-steps reporting, and the S9 carve-out rationale.

## Workflow

### Phase 0 — Auth

Resolves org auth via the shared `scripts/shared/auth.sh` helper
(`resolve_org_auth "$ORG_ALIAS"`), which every script in this skill sources:
validate the alias format, call `sf org display` for `instanceUrl` and
`accessToken` (falling back to `sf org auth show-access-token` when the CLI
redacts the token), refuse a non-HTTPS instance URL, and fail closed with an
explicit `sf org login web --alias <alias>` instruction if the org isn't
reachable or no token can be extracted. If `ACCESS_TOKEN`/`INSTANCE_URL` are
already exported for the same alias — e.g. a parent shell already resolved
auth and is chaining multiple of these scripts in one session — resolution
is skipped and the cached values are reused. `orgId` is not part of this
helper; `enable-call-scoring.sh` fetches it separately (via its own
`sf org display`) purely for the status banner.

### Phase 0 — ECI purchase gate

Before any state detection, query the `ConversationPilot` OrgPermission via
Tooling API (`OrganizationSettingsDetail`, same pattern as the
`ECICallScoringAI` gate in Phase 3). This is a license/purchase check,
distinct from `enableCallCoaching` below (the admin's Setup toggle for an
org that's already licensed):

- **Not enabled:** exit with: "Call Coaching couldn't be turned on because
  this org doesn't have Einstein Conversation Insights, which is required
  to use Call Coaching. To proceed, an admin can go to Setup → Salesforce Go
  → Einstein Conversation Insights, or contact their sales representative,
  to understand how to purchase ECI." Non-zero exit.
- **Enabled:** proceed to Phase 1's `enableCallCoaching` check.

### Phase 1 — State detection

SOAP `readMetadata` at `/services/Soap/m/68.0` against two settings types:

1. `ConversationalIntelligenceSettings` → read `enableCallCoaching` (ECI arm)
   and `enableECICallScoring` (current Call Coaching state).
2. `EinsteinGptSettings` → read `enableEinsteinGptPlatform`.

(`RiverRushSettings`/`riverRushEnabled` — Momentum — is NOT read. That
detection is deferred until the River Rush arm goes live; see Key
Considerations for where to re-add it.)

Query existing competencies via Tooling API:
`SELECT COUNT() FROM EnablementCompetencyDef`.

Classify the org into one of 4 states:

| State | Detection |
|---|---|
| 1a. Not available (no ECI license) | Cannot read `ConversationalIntelligenceSettings` |
| 2. Available, not enabled | `enableCallCoaching=true` AND `enableECICallScoring=false` |
| 3. Enabled, no competencies | `enableECICallScoring=true` AND count = 0 |
| 4. Enabled, with competencies | `enableECICallScoring=true` AND count > 0 |

### Phase 2 — Route by state

- **State 1a:** Exit with PRD-verbatim message: "AI call coaching is not
  available in this org and they need Agentforce for Sales." Non-zero exit.
- **State 3 / State 4:** Exit 0 with a ready-for-competency-setup message.
- **State 2:** Proceed.

### Phase 3 — Prerequisite enablement (State 2 only)

- **License gate (checked first):** query `OrganizationSettingsDetail`
  (Tooling API) for the `ECICallScoringAI` OrgPermission. Only an **explicit
  `false`** refuses — exit with: "AI call coaching is not available in this
  org and org requires Agentforce for Sales license." (Non-zero exit.) If the
  permission **can't be read** — the query is rejected with `INVALID_TYPE`
  (some org editions, for example Developer Edition) or returns no row — treat
  it as **unknown and proceed**; do NOT fail closed on an unreadable signal.
  The Einstein GenAI `TYPE_UNAVAILABLE` pre-check catches most unlicensed
  orgs; the enable `updateMetadata` write is the final check. This mirrors the Phase 0
  `ConversationPilot` gate, which defers on any non-conclusive read.
  This runs even when `enableCallCoaching`/`enableECICallScoring`
  already read favorably, since those settings don't by themselves confirm the
  org is licensed. **Must run before the ECI-off check below** — a genuinely
  unlicensed org
  and a licensed-but-toggled-off org both read `enableCallCoaching=false`,
  so checking ECI first would misdiagnose a licensing gap as a self-serve
  Setup toggle (the regression the `NoLicense` eval dataset guards against).
- If **ECI is off**: refuse with a Setup pointer, exit non-zero. This skill
  does NOT enable ECI (PRD explicit). (A Momentum-only org lands here too,
  since Momentum isn't detected separately — it gets this same generic
  message, not a Momentum-specific one.)
- If **Einstein GenAI off**: SOAP `updateMetadata` on `EinsteinGptSettings`
  with `enableEinsteinGptPlatform=true`. PRD explicitly authorizes this. If
  it's already on, skip the `updateMetadata` call and tell the admin it's
  already enabled. If the update fails because the org isn't licensed for
  `EinsteinGptSettings` (or is explicitly refused with no fault): tell the
  admin they need **Agentforce for Sales** to enable AI Call Scoring, and
  that without it they can still set up **manual call scoring** via
  Salesforce Go setup. A distinct auth/permission or network/timeout failure
  gets its own message (check CLI session / retry) rather than the licensing
  message, since those aren't licensing gaps.

### Phase 4 — Enable Call Coaching (State 2 only)

If `enableECICallScoring` already reads `true` (e.g. it changed out-of-band
between Phase 1's read and here), skip the update and tell the admin it's
already enabled. Otherwise SOAP `updateMetadata` on
`ConversationalIntelligenceSettings` with `enableECICallScoring=true`.
Require `<success>true</success>`.

### Phase 5 — Verify (State 2 only)

Re-read `enableECICallScoring`. Require `true`. Print SOAP response on failure.

## Key Considerations

- **API version is v68.0**, not v64.0. `enableECICallScoring` is not
  present in the `ConversationalIntelligenceSettings` schema at lower API
  versions on some builds — v68 is the safe minimum. The Pipeline skill uses
  v64 because its target field (`SalesDealAgentSettings.enableDealAgent`) is
  present there; Call Scoring is not.
- **Do NOT use `sf mdapi deploy`** for this pref. It has a silent failure
  mode where the CLI reports success but the pref doesn't flip. Use raw
  SOAP `updateMetadata` — the response's `<success>` boolean is authoritative.
- **The server-side gate is broader than this skill's scope.** The
  `orgHasCallScoring` access check allows the ECI arm OR the River Rush
  (Momentum) arm — see `CoachingCompetenciesFeature.isFeatureAvailableInOrg()`.
  This skill deliberately narrows to the ECI arm (MVP scope per the spike).
- **River Rush (Momentum) detection is deliberately absent right now**, not
  an oversight — the arm isn't live yet. `enable-call-scoring.sh` used to
  read `RiverRushSettings.riverRushEnabled` and refuse Momentum-only orgs
  with a distinct "State 1b" message / emit a Momentum-available-but-off
  advisory; both were removed. Re-add them (the read, the State 1b branch,
  and the Phase 3 advisory) once River Rush ships — the removed code is
  recoverable from git history on this file.
- **`disableOnSandboxCopy=true`** — every sandbox refresh disables this pref.
  Admins re-running the skill after a refresh is the expected pattern; the
  idempotency check makes that safe.
- **Site switch** `com.salesforce.eci.callScoringEnabled` must be open on
  the org's pod. It's not admin-toggleable and not readable via SOAP. If
  closed, `updateMetadata` returns a well-formed response with
  `<success>false</success>` and an `<errors><statusCode>…</statusCode></errors>`
  block — it does NOT emit a SOAP `<Fault>`. `parse_soap_response` extracts
  the statusCode and surfaces it via the `WRITE_ERROR:…` classification.
- **ECI provisioning is asynchronous.** For a short window after
  `enableCallCoaching` flips on, the dependent `enableECICallScoring` field
  is server-side read-only and `updateMetadata` returns
  `INSUFFICIENT_ACCESS_OR_READONLY`. `enable-call-scoring.sh` maps this to a
  transient "still finishing turning on — wait a few minutes and re-run"
  message rather than a terminal failure.
- **Every SOAP call is bounded by a 30s timeout** (`CURL_TIMEOUT` in
  `enable-call-scoring.sh`, matching the only existing timeout precedent in
  this repo — the Pipeline skill's `setup-all.sh`) and classified via
  `shared/soap.sh`'s `parse_soap_response` into `true` / `false` /
  `AUTH_ERROR:...` / `TYPE_UNAVAILABLE:...` / `WRITE_ERROR:…` /
  `NETWORK_ERROR`. This distinguishes "org isn't licensed for this setting"
  from "auth/permission fault" from "server refused the write with a specific
  statusCode" from "network/timeout error" — instead of collapsing them into
  an empty string or dumping raw SOAP XML at the admin.
- **`enable-call-scoring.sh` uses raw SOAP, not `sf api request rest`.**
  Every other script in this skill uses `sf api request rest` so the CLI
  manages auth end-to-end. `enable-call-scoring.sh` is the sole exception:
  it calls the SOAP Metadata API (`readMetadata`/`updateMetadata`) directly,
  because no non-beta Salesforce CLI command exposes SOAP Metadata reads/
  writes for `ConversationalIntelligenceSettings` et al., and `sf mdapi
  deploy` has the silent-failure mode noted above for this exact field. This
  is a deliberate, scoped exception, not an oversight.

## References

- **Reference skill** (canonical single-OrgPref pattern):
  `skills/sales-agentforce-pipeline-management-configure/`
- **SOAP helpers**: `scripts/shared/soap.sh` (copied from the Pipeline skill —
  `redact_token`, `parse_soap_response`)
- **Server-side gate** (declarative access check):
  `ConversationalIntelligence.accessChecks.xml`
  — `orgHasCallScoring` = ECI arm OR River Rush arm; `orgHasECICallScoringWithAI`
  adds Einstein GenAI + `ECICallScoringAI` license perm on top.
- **Pref declaration**:
  `ConversationalIntelligence.settings.xml`
  — `<orgPreference name="ECICallScoringEnabled" mdApiName="enableECICallScoring" ...>`
- **Java feature registration** (would be the entry point if a
  SetupDiscoveryService REST/MCP wrapper existed): `CoachingCompetenciesFeature.java`

## Competency CRUD workflow

Once Phase 5 confirms Call Coaching is enabled (or Phase 1 detects State 3/4), Claude runs the `Next:` script directly, in the same turn. Records are managed via Tooling API on `EnablementCompetencyDef` (setup entity, keyPrefix `1nA`, module `conversation-udd`). Cap: **8 simultaneously active** per org (`CoachingCompetenciesFeature.MAX_ACTIVE_COMPETENCIES`).

All scripts share `shared/auth.sh` / `resolve_org_auth` — token propagates across chained invocations, no re-auth. Tooling API writes go through `sf api request rest` where practical; a subset (custom-CRUD variants, best-practice installer) drops to raw `curl` for finer request shape.

Scripts fall into **two parallel families**:

- **Generic** — `{create,edit,toggle,get}-competency.sh` — works on any competency.
- **Custom-CRUD variants** — `*-custom-competency.sh` — harden the write path with SpecificCallsOnly filter JSON and richer validation.

Prefer custom variants when the admin's intent is unambiguously custom (S5-created); fall back to generic on OOTB or unknown-provenance records.

**Full spec** — S3 through S10 script contracts, S5's Q1-Q4 conversational drafting sequence, the admin-intent × org-state execution matrix, and chaining checkpoints — is in [`references/competency-crud.md`](references/competency-crud.md). Consult it whenever the admin's ask touches competency records (list, install, create/edit, activate, verify, delete).

## Standalone Scripts (summary)

| Script | Purpose |
|---|---|
| `enable-call-scoring.sh <alias>` | Detect state, enable Einstein GenAI if off, flip the Call Coaching pref (Phase 0-5). |
| `list-competencies.sh <alias> [--verbose\|--json]` | List all competencies + status. Admin-safe by default; `--verbose` adds Ids/DeveloperNames; `--json` for the calling agent only. |
| `install-ootb-competencies.sh <alias> [--dry-run]` | Install the 6 PRD-canonical OOTB competencies. |
| `install-best-practice-competencies.sh <alias> [--dry-run] [--only "Name1,Name2"]` | Install the 7 Momentum best-practice reference prompts. `--only` filters by `MasterLabel`. |
| `create-competency.sh <alias> <payload.json>` | Create one competency (generic — usable on OOTB or custom). |
| `create-custom-competency.sh <alias> <payload.json>` | Create one custom competency (hardened variant — prefer for S5). |
| `edit-competency.sh <alias> <ident> ...` | Edit description / instructions (generic). |
| `edit-custom-competency.sh <alias> <ident> ...` | Edit description / instructions (custom-CRUD variant). |
| `toggle-competency.sh <alias> <ident> <activate\|deactivate>` | Activate / deactivate (generic). |
| `toggle-custom-competency.sh <alias> <ident> <activate\|deactivate>` | Activate / deactivate (custom-CRUD variant). |
| `get-competency.sh <alias> <ident> [--field <f>]` | Fetch a record or single field (generic). |
| `get-custom-competency.sh <alias> <ident> [--field <f>]` | Fetch a record or single field (custom-CRUD variant). |
| `verify-ootb-competencies.sh <alias> ["Name" ...]` | Confirm expected competencies exist and are active — outputs the S9 admin-visible markdown table. |
| _no delete script (yet)_ | Use `sf data delete record --sobject EnablementCompetencyDef --record-id <Id> --use-tooling-api` — see §S10. |

## Admin Verification

After a successful run, the admin can independently verify:

**Via UI** — Salesforce Go → Coaching Competencies should now be reachable
and show the feature as enabled with the configured competencies.

**Via CLI** — two Tooling API queries:

```bash
# Feature enabled?
sf data query --target-org <alias> --use-tooling-api \
  --query "SELECT IsEciCallScoringEnabled FROM ConversationalIntelligenceSettings"

# Competencies configured?
sf data query --target-org <alias> --use-tooling-api \
  --query "SELECT MasterLabel, IsActive, SourceCompetencyTemplate FROM EnablementCompetencyDef ORDER BY MasterLabel"
```

## Assets

- `assets/ootb-competencies.json` — 6 PRD-canonical OOTB prompt bodies
  (installed by `install-ootb-competencies.sh`).
- `assets/best-practice-competencies.json` — 7 Momentum best-practice
  prompt bodies (S5 authoring reference; also installable via
  `create-competency.sh`).
