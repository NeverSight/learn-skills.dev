---
name: ecommerce-process-mining
description: >
  Build employee process mining for an e-commerce back office: a consented Manifest V3
  browser extension that captures DOM events rather than pixels from the admin tools
  staff already use (shop admin, marketplace seller panels, carrier portals, helpdesk,
  WMS, ERP), plus a gap-capture form for the work a browser cannot see, feeding an AI
  pipeline that writes per-role SOPs and ranks automation candidates. Use when: (1)
  documenting how order, return, listing, supplier and support work is really done, for
  onboarding, audit or automation scoping, (2) building or auditing an employee
  activity-capture extension, its consent model, its PII scrubbing, or its PKCE connect
  flow, (3) the user mentions: process mining, task mining, SOP generation, "document
  what employees do", routine capture, browser extension capture, DOM event capture,
  MutationObserver, captureVisibleTab, chrome.identity launchWebAuthFlow, consent
  toggle, excluded domains, PII scrubber, dom_confidence, perceptual hash, works
  council, GDPR Art. 88. Carries a scrubber that tells a card from an EAN, one exclusion
  matcher shared by the extension and the server, an atomic one-time-code exchange, an
  append-only consent ledger, and aggregate-only enrollment stats, each held by the
  tests and the SQL checks shipped with it. Next.js App Router and Postgres oriented;
  the backend is a seam. Not product analytics, not session replay, not screen
  recording, and not event-log mining from ERP tables.
---

# E-commerce process mining

Capture what back-office staff actually do, as structured events read from the page's DOM rather than as
video, and turn it into SOPs and an automation shortlist. The insight the whole design turns on: **in
e-commerce the screens are full of other people's data.** The employee consents; the customer whose order is
on screen never did. Every choice below follows from treating capture as a privacy system first and a data
pipeline second.

Written by the engineer who has shipped this module. Every section in every reference carries a maturity tag:
**[P]** ran in the earlier implementation, **[D]** was specified in its design notes and never built there,
**[A]** was designed here and is held only by the 76 unit tests and 24 SQL checks shipped with this skill.
**No part of the capture path has met a production browser**; plan the spike in [extension.md](references/extension.md).
Keep the tags in anything written from this skill; [provenance.md](references/provenance.md) holds the audit.

## When to use

- Mapping real order, return, listing, purchasing or support workflows across several web tools
- Building the capture extension, its consent, exclusion and pause controls, or the ingest API
- Generating per-role SOPs, or ranking manual work by cost so automation can be scoped

## When NOT to use

| Instead of this | Use |
|---|---|
| Customer behaviour on the storefront | product analytics; this captures staff, not shoppers |
| "Who opened this link" | server-side visit logging; the `visit-logger` skill |
| Data out of, or actions into, a site with no API | the [`browser-extension-connector`](https://github.com/timerise-ai/browser-extension-connector) skill; it acts in the session, this one only observes |
| Process mining over ERP or OMS event logs (case id, activity, timestamp) | a data-warehouse job; no capture is needed |
| Productivity scoring or surveillance | nothing here. Consent is per person and revocable, and managers see aggregates |
| Desktop applications | a browser extension sees browser tabs only; the gap-capture form covers the rest |

## Architecture

```
 EXTENSION (MV3)                   SERVER                        AI (batch)
 content script                    POST /ingest                  1 narrate each event
   label + confidence               bearer key, emit scope          cheap text model;
   value gate                       consent re-read per batch       low confidence goes
 service worker         batch       exclusions (again)              to vision on the crop
   pause, budget        ----->      scrub (authoritative)         2 mine branches across
   exclusions (first)               idempotent insert               sessions
   screenshot gate                       |                        3 write the SOP
   offline queue                         v
                                   events <-- gap-capture form (phone, floor, paper)

 connect: PKCE --> consent page --> one-time code --> exchange --> scoped API key
```

## Critical facts

1. **Two consents, not one.** Connecting the extension authorises it to *talk*; the consent toggle authorises
   the server to *accept*. Ingest re-reads consent on every batch, so never cache it.
2. **Exclusions beat the allowlist, and run twice.** The extension first, so no local state is ever created,
   and the server again, so a stale client still leaks nothing. Both import one matcher.
3. **Consent is per person *per tenant*.** Staff shared across two legal entities consent to each separately;
   one row per user would carry consent from one entity to the other.
4. **Managers never see who opted in.** Aggregate only, suppressed below a group of five, because with three
   employees the count *is* the names.
5. **A card number and a barcode look alike.** About one EAN, GTIN or tracking number in ten passes Luhn.
   Match on length *and* issuer prefix, or the scrubber eats your product data.
6. **`code=` is a discount code far more often than an OAuth code.** Drop credential URLs by shape, meaning
   `state=` alongside or an auth path, never by parameter name.
7. **A whole-viewport perceptual hash cannot see one field change.** Dedup on it alone and low-confidence
   events reuse a screenshot taken *before* the value existed. Hash the element crop too, and never dedup a
   low-confidence event.
8. **Service workers die mid-handshake.** The PKCE verifier lives in `chrome.storage.session`, and timed
   pauses end by the clock, not by an alarm that may never fire.
9. **Screenshots bypass the scrubber.** It reads JSON, not pixels. Default to `metadata_only` wherever buyer
   data is on screen.
10. **The consent toggle is necessary, not sufficient.** EU deployments need a legal basis and usually a
    works-council consultation before go-live.

## Hard rules

> **Never fail open on a privacy switch.** Unreadable pause state means paused, an unparseable host means
> excluded, and a failed consent save leaves the toggle showing what the server believes.

> **Never read a value you would have to scrub.** Password, card, one-time-code and hidden fields are skipped
> at the point of capture. The scrubber is a net, not a licence.

> **Never let the redeem be two statements.** One-time codes are claimed with a single `DELETE ... RETURNING`,
> so two concurrent redeems cannot both mint a key.

> **Never accept an authorization request from an unknown extension id.** A well-formed id proves nothing
> about who published the extension, so keep an allowlist in configuration, empty by default and with no id
> written into code, and re-check it in the authorize action.

> **Never report success to the extension for an event you did not store.** Answer `207` with the indexes to
> retry, because a `200` makes the extension delete its only copy. Memory is not storage: without a database,
> ingest answers an error, never an in-process fallback store.

> **Never show a manager who opted in.** There is no team policy on the consent table, only an aggregate
> function that suppresses small groups and full enrollment alike.

## Quick start

Write every `// file:` block as shipped, with [adaptation.md](references/adaptation.md)'s renames the only edits,
and put host code in files of its own. Each odd line has its reason in [provenance.md](references/provenance.md).

1. Fill the seam table against the host app: [adaptation.md](references/adaptation.md). No session means
   signed out, in every environment: never a fallback user or tenant, not even in development.
2. Settle the legal posture and screenshot mode: [consent-and-privacy.md](references/consent-and-privacy.md).
3. Land the schema: [data-model.md](references/data-model.md).
4. Build the employee and manager pages: [console-surfaces.md](references/console-surfaces.md). This slice
   ships on its own, with no extension, and is the only **[P]** one.
5. Add ingest, the scrubber and the connect flow: [ingest.md](references/ingest.md),
   [pii-scrubber.md](references/pii-scrubber.md), [extension-auth.md](references/extension-auth.md).
6. Build the extension: [extension.md](references/extension.md), [screenshots.md](references/screenshots.md).
   With screenshots off, `screenshot.ts` and its suite still ship: the mode is a setting, not a deletion.
7. Run the nine suites from [testing.md](references/testing.md) as written. Install `zod`, and `vitest`,
   `happy-dom` and `@testing-library/react` as dev dependencies, from the registry, which is not an
   external service; `npx vitest run` reports 76 cases. Never port a suite to another runner.
8. Choose the target apps and categories: [ecommerce-playbook.md](references/ecommerce-playbook.md), then the
   pipeline: [ai-pipeline.md](references/ai-pipeline.md).
9. End the final summary with these three, whatever else it says: pin the extension id and add it to the
   allowlist, or connect fails; nothing in the capture path has run in a browser, so plan the spike; and the
   consent toggle is not a legal basis, so the DPIA and any works-council consultation come before go-live.

## Reference directory

| Scenario | Trigger keywords | Reference |
|---|---|---|
| Fitting this to a host app | seam, rename, tenant, auth guard, api key, event bus, i18n | [adaptation.md](references/adaptation.md) |
| Tables, RLS, neutral types | schema, migration, consent ledger, RLS, Firestore, enrollment stats, k-anonymity | [data-model.md](references/data-model.md) |
| What may be captured, and from whom | consent, excluded domains, allowlist, pause, revoke, GDPR, BDSG, works council, customer data | [consent-and-privacy.md](references/consent-and-privacy.md) |
| Masking before storage | scrub, PII, Luhn, EAN, IBAN, JWT, email mask, discount code, label redaction | [pii-scrubber.md](references/pii-scrubber.md) |
| The ingest API | ingest route, batch, 207, retry, idempotency, 403 consent_required, event types, retention | [ingest.md](references/ingest.md) |
| Connecting the extension | PKCE, launchWebAuthFlow, chromiumapp.org, one-time code, invalid_grant, revoke, storage.sync | [extension-auth.md](references/extension-auth.md) |
| The extension itself | Manifest V3, service worker, MutationObserver, label resolution, dom_confidence, pause, budget, queue, session_id, Shadow DOM | [extension.md](references/extension.md) |
| Screenshots | captureVisibleTab, throttle, perceptual hash, aHash, bounding box, crop, metadata_only | [screenshots.md](references/screenshots.md) |
| Employee and manager pages | my routine, gap capture, consent toggle, optimistic update, automation ranking, help page | [console-surfaces.md](references/console-surfaces.md) |
| Events to SOPs | narrative, branching, SOP, model routing, pgvector, VLM, cost | [ai-pipeline.md](references/ai-pipeline.md) |
| What to capture in a shop | Shopify, marketplace, returns, RMA, carrier portal, WMS, categories, rollout | [ecommerce-playbook.md](references/ecommerce-playbook.md) |
| Proving it | vitest, happy-dom, SQL checks, psql | [testing.md](references/testing.md) |
| What was fixed, kept, added | provenance, defects, deviations, maturity tags, fix order | [provenance.md](references/provenance.md) |

Part of the [Timerise Skills](https://github.com/timerise-ai/skills) index, which lists the sibling skills.
