---
name: sumsub-check-databases
description: Discover the Databases (check-sources) Sumsub offers for a country, whether each is enabled for the tenant, and how database / non-document (eKYC) verification fits into a verification level. Use WHEN a user asks which database / non-document check-sources are available for a country, whether they're enabled, or how to add database validation / non-doc identity / non-doc address verification to a level. Also called by sumsub-create-level before placing those sources. Do NOT use for document-only verification or entitlement checks (use sumsub-check-permissions).
allowed-tools: Bash
---

# Check Databases

Lists the database check-sources Sumsub offers for a country, each source's enablement status for the current tenant, and how it plugs into a verification level. Callers use it to gate database / non-document verification before building a level.

> **Scope: KYC (individual) only — for now.** The endpoint returns only individual/person check-sources. Company (KYB) database verification is **not** exposed here yet; don't use this skill to place company/business sources.

## Endpoint

```
GET https://api.sumsub.com/resources/api/agent/settings/checkSources?country=<country>
```

`country` is an **ISO alpha-3 code** (e.g. `DEU`). If the user names a country, convert it to alpha-3 before calling. Omit `country` to return the full catalog. An unrecognized or unsupported code is **not an error** — it returns HTTP 200 with an empty `checkSources` list.

> **Pass `country` whenever you can.** The unfiltered response is the entire catalog — hundreds of entries across every country, large enough to bloat or truncate your context. If the user named a country, filter by it. If they didn't, prefer asking which country they need before calling unfiltered; only omit `country` when you deliberately want the whole catalog and can handle a large response.

## Auth — App Token + secret (sandbox only)

This skill talks to the public Sumsub API and signs each request per
[the authentication reference](https://docs.sumsub.com/reference/authentication).
The full how-it-works writeup lives in the [`sumsub-api-auth`](../sumsub-api-auth/SKILL.md)
skill — read it if you hit `401 Invalid signature`.

> **⚠️ Sandbox tokens only.** Do **not** accept or use a production App Token
> here. If the user offers one, refuse and ask them to generate a sandbox
> pair at <https://cockpit.sumsub.com/checkus/devSpace/appTokens> (toggle
> the workspace to **Sandbox** first, then **Create**). Token + secret are
> shown once — copy both before closing the dialog. The helper script
> enforces this — it rejects tokens that don't start with `sbx:`.

| Var | Example |
|---|---|
| `SUMSUB_APP_TOKEN` | `sbx:...` — sandbox App Token from the dashboard. |
| `SUMSUB_SECRET_KEY` | The paired secret shown once at token creation. |
| `SUMSUB_BASE` | Optional. Defaults to `https://api.sumsub.com`. |

## Usage

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/check_databases.sh <country>
```

Output: raw Sumsub response body followed by `HTTP <code>`.

Success (HTTP 200):
```json
{"checkSources": [
  {
    "sourceId": "arg_gov_dni",
    "name": "Argentina DNI Verification",
    "description": "Verifying user's personal, biometric, and residency data against official government sources.",
    "dataSources": [
      "National Registry of Persons (Registro Nacional de las Personas - RENAPER)",
      "Agency of Public Revenues and Control (Agencia de Recaudación y Control Aduanero – ARCA)"
    ],
    "country": "ARG",
    "checkType": "E_KYC_CHECK",
    "confirmationType": "otp",
    "status": "ENABLED",
    "validationReady": false,
    "stepsReady": ["E_KYC", "IDENTITY"],
    "supportedDocuments": ["ID_CARD"],
    "requiredInputFields": ["gender", "number"],
    "optionalInputFields": ["address.postCode"],
    "selfieRequirement": "ADDITIONAL",
    "outputFields": ["firstName", "lastName", "addresses", "gender", "nationality", "dob", "tin"],
    "violations": ["GENDER_MISMATCH", "DEAD", "PERSON_IS_MINOR", "SELFIE_MISMATCH"]
  }
]}
HTTP 200
```

Input-field values are **machine field names** on the background-check input data — `number`, `dob`, `address.postCode`, `bankAccount.bankName` — not display labels. Dotted names are nested objects (`address.*`, `bankAccount.*`). Translate them into something readable when you show them to a user.

**A selfie is never listed in the input fields** — it has its own `selfieRequirement` field. Read that, not `optionalInputFields`, to decide whether the flow needs a selfie step.

## Field reference

| Field | Meaning |
|---|---|
| `sourceId` | Stable id of the check-source (`{country}_{provider}_{subject}`). |
| `name` | Human-readable source name (English), e.g. "Argentina DNI Verification". |
| `description` | One-line English description of what the source verifies. May be absent. |
| `dataSources` | Underlying registries / providers the source draws on (English names). May be absent. |
| `country` | Canonical ISO alpha-3 the source covers. |
| `checkType` | Internal category (`E_KYC_CHECK`, `PERSON`, `TIN`) — informational, not a filter. Company (KYB) types are not returned. |
| `confirmationType` | How the applicant confirms a non-document check: `otp`, `oAuth` (log in to a bank / national eID service), or `eID` (NFC scan of an eID card). Absent when the source needs no confirmation step. |
| `status` | Per-tenant enablement, **the usability gate**: `ENABLED` (licensed in production, and so in sandbox too) / `SANDBOX_ONLY` (licensed in sandbox only — works for testing, will not run in production) / `DISABLED` (not licensed anywhere). See below. |
| `validationReady` | `true` if the source can cross-validate a document already being collected (database validation). |
| `stepsReady` | Level step type(s) (`IdDocSetType`, e.g. `E_KYC`, `IDENTITY`) the source is ready to be used as a non-document check for. Empty if none. |
| `supportedDocuments` | `IdDocType`s the source can validate. |
| `requiredInputFields` / `optionalInputFields` | **Machine field names** the applicant must / may supply (e.g. `number`, `dob`, `address.postCode`) — background-check input data keys, not display labels. Never includes the selfie. |
| `selfieRequirement` | `REQUIRED` (the source can't run without a selfie) / `ADDITIONAL` (optional, improves the match) / absent (no selfie needed). |
| `outputFields` | Fields the source returns on a match. |
| `violations` | Possible violation reasons the source can raise (e.g. `GENDER_MISMATCH`, `DEAD`). |

Full types, enum values, and meanings: [`references/checksources-schema.md`](references/checksources-schema.md).

## How callers should use this

1. If the HTTP status is not 200, **stop immediately** — show the error body to the user and do not proceed.
2. **An empty `checkSources` list is not an error.** It means Sumsub offers no KYC database sources for that country — or the `country` value wasn't a recognized ISO alpha-3 code. Tell the user no database check-sources are available for that country; if they gave a country *name*, double-check it mapped to the right alpha-3 code (e.g. `Germany` → `DEU`) and offer to retry. Never fabricate sources. A database layer is optional, so fall back to document-based verification (see the placement branches below).
3. Check **`status`** — per-tenant and environment-independent (the same value comes back whether you query from sandbox or prod). `ENABLED`: licensed in production and therefore in sandbox too — usable, proceed. `SANDBOX_ONLY`: licensed in sandbox only — usable **for sandbox testing**, but the level will not run this source in production, so say that explicitly and point the user at enablement before they go live. `DISABLED`: not licensed anywhere — not usable. For anything other than `ENABLED`, see [Enabling a source](#enabling-a-source) below.
4. **If the source the user needs is unavailable, don't silently drop it and don't blanket hard-stop.** A missing check-source (unlike a missing entitlement) still leaves a valid document-based level — so surface the gap, don't block it. Then branch by what the source was for:

| What the user wanted | Source unavailable → do this |
|---|---|
| **Database validation** (document **+** DB cross-check) | Soft: the document verification still stands. Confirm, then continue **without** the DB layer. |
| **Non-doc in identity step** (source nested inside `IDENTITY`) | Offer the fallback: switch that identity step back to document upload. Continue after the user picks. |
| **Non-doc, standalone** (a database-only step was the whole point) | Closest to a stop: the step can't exist without a source. Present the document-based alternative; proceed only on explicit confirmation. |

Never silently downgrade and never unilaterally hard-stop — surface the gap + impact and let the user (via the caller) decide. The one hard stop that still applies: non-doc identity also needs the `E_KYC_TARGET` entitlement, which [`sumsub-check-permissions`](../sumsub-check-permissions/SKILL.md) gates independently.

### Enabling a source

Enabling isn't something the agent can do: there is **no public API to enable a check-source**. This covers both `DISABLED` (nothing works) and `SANDBOX_ONLY` (sandbox works, production doesn't). Tell the user which database check is missing and in which environment — **name the specific source by its `name`, and note its `sourceId`** — and *what verification is lost*. Then point them to:

- **[Databases → Available products](https://cockpit.sumsub.com/checkus/sdkIntegrations/databaseServices/available)** in the Sumsub dashboard — self-serve enablement for most sources.
- If the source isn't self-serve-enablable there, the user contacts their Customer Success Manager / Sumsub Support to request it.

## Where each source goes in a level

A chosen source is wired into the level's `checkSourceSettings.countrySettings[]` — one entry per `country` (+ `checkType` when placed at the level's top level), listing the `sourceId` under `executionConfigurations`. `validationReady` and `stepsReady` tell you **which placement(s)** apply. [`sumsub-create-level`](../sumsub-create-level/SKILL.md) builds the full payload — this skill decides the placement.

A source can be `validationReady` **and/or** have entries in `stepsReady` at once — check both, they're independent signals. If `stepsReady` lists more than one step type, that's a menu of valid homes for the same source, not a mandate to use all of them at once — pick the one placement that matches the user's **intent**.

| Placement (ticket) | Signalled by | What it means in the level |
|---|---|---|
| **Database validation** | `validationReady: true` | Keep the document docSet (e.g. `IDENTITY`) — the applicant still submits a document. Attach the source at the **level's top-level `checkSourceSettings`** (a sibling of `requiredIdDocs`, not nested inside it). |
| **Non-doc, standalone** | `stepsReady` contains the step type on its own (e.g. `E_KYC`) | A dedicated non-document docSet, no upload — `E_KYC` for identity (needs `E_KYC_TARGET`, verify via [`sumsub-check-permissions`](../sumsub-check-permissions/SKILL.md)). The applicant supplies `requiredInputFields`, checked against the database. Attach the source **nested inside that docSet's own `checkSourceSettings`**. |
| **Non-doc in an existing step** | `stepsReady` contains the step type (e.g. `IDENTITY`) alongside an already-required document step | Keep the document docSet's `types` (document upload stays optional) and nest the source's `checkSourceSettings` **inside that same docSet** — the applicant chooses upload **or** the database check in one step. Also needs `E_KYC_TARGET`. |

In every case the source is referenced via `country`, `checkType` (top-level placement only), and `executionConfigurations[].sourceId`. Optional `fallbackReasons` (`NO_DATA`, `NAME_MISMATCH`, `DOB_MISMATCH`, `INVALID_DOC_NUMBER`, `FAILED`, `DEAD`) let the flow fall back to another source or a document when the check can't confirm. See the worked examples in [`sumsub-create-level/examples/`](../sumsub-create-level/examples/): `identity-selfie-with-database-validation.json` (top-level, `validationReady`), `identity-with-non-doc-selfie.json` (nested in `IDENTITY`), `non-doc.json` (standalone `E_KYC`).

Concept references: [no-document verification](https://docs.sumsub.com/docs/no-document-verification), [database validation](https://docs.sumsub.com/docs/database-validation).

## See also

- [`sumsub-create-level`](../sumsub-create-level/SKILL.md) — builds the level these sources plug into.
- [`sumsub-check-permissions`](../sumsub-check-permissions/SKILL.md) — gate the `E_KYC_TARGET` entitlement for non-doc identity.
- [`sumsub-api-auth`](../sumsub-api-auth/SKILL.md) — request signing details.
- [`references/checksources-schema.md`](references/checksources-schema.md) — full response schema, field types, and enum values.
