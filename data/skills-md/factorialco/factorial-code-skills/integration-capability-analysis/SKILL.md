---
name: integration-capability-analysis
description: >-
  Analyses a third-party system's API or file specification against Factorial's integrations framework and produces a detailed integration mapping document — the integration domain (payroll or finance), every capability in that domain with its verdict (fully, partially or not supported), the vendor endpoints to use for each, and the field-by-field mapping between Factorial's API and the vendor's. Use whenever someone shares a vendor API spec, OpenAPI/Swagger file, developer-portal link, integration guide or file layout and wants to know what we could build against it, how to map it, whether an integration is feasible, or asks for integration scoping, a fit-gap assessment or a field mapping. Use it even for informal asks ("can we integrate with this?", "how would new hires map to their API?") and partial specs.
metadata:
  owner: Factorial Engineering — Integrations
  version: "0.2"
---

# Integration capability analysis

Factorial's integrations framework is organised by **domain** — payroll and
finance today — and each domain defines a set of **capabilities**, each with a
direction and the Factorial endpoints behind it. This skill takes one external
system's specification and works out, capability by capability, which vendor
endpoints implement it and how every field maps between the two APIs.

The output is an integration mapping document. It serves two readers at once:
whoever decides whether the integration is worth building, and whoever then
builds it. The first needs the verdicts; the second needs the endpoint sequence
and the field mapping. Both depend on the same rule — **cite or downgrade**: a
mapping row, an endpoint or a verdict that cannot be pointed at in the vendor's
specification does not go in the document as fact.

## The catalogue is the public documentation

The capabilities are defined in Factorial's API documentation, one page per
domain:

- Payroll — https://apidoc.factorialhr.com/v2026-10-01/docs/payroll-integrations
- Finance — https://apidoc.factorialhr.com/v2026-10-01/docs/finance-integrations

Read the page for the domain in scope at the start of every analysis. Each one
lists the domain's capabilities, the direction of each, what it covers, and
links to the Factorial endpoints involved. Those pages are the source of truth:
analyse every capability they list, use the direction they state, and take
Factorial field names from the endpoint references they link to. Do not work
from memory of what a payroll or finance integration usually contains — the
real lists differ from the intuitive ones, and a mapping built against the wrong
capability set looks exactly as convincing as a correct one.

The URLs are versioned. Use the version the requester names, otherwise the one
above, and record which version you used in the document's header, since field
names and capabilities can change between versions.

If a page can't be fetched, stop and say so rather than improvising the
capability list.

## Step 1 — Classify the domain

Decide which domain the vendor belongs to: a payroll engine is payroll; an
accounting system or ERP is finance. Some systems span both — an ERP with a
payroll module — in which case analyse each domain and produce one document per
domain. If the system fits neither, say so and stop; forcing it into a domain
produces a mapping nobody can use.

State the classification and the reason in one line at the top of the document.
Don't block on the requester to confirm it; if it was a judgement call, say so
and carry on.

## Step 2 — Load the domain's capabilities

From the domain page, build the working list: every capability, its direction,
and the Factorial endpoints it links to. Then follow those endpoint links for
the fields — you cannot map what you have not read. Read them per capability as
you reach it rather than all upfront; the domain pages link to many endpoints
and most of them serve only one capability.

Also carry forward anything the page says that constrains the whole domain:
ordering or setup sequences (which records must exist before others can be
created), identifiers Factorial requires on writes (such as an `external_id`
on records posted into Factorial), and incremental-sync parameters. These shape
the endpoint sequence in the document, not just individual rows.

## Step 3 — Inventory the vendor specification

Build a factual inventory before mapping anything. Going capability-first means
looking for the endpoint you expect and finding something adjacent to it.

**For an API specification** — OpenAPI/Swagger, a developer portal, a PDF guide
— record one row per operation: method, path, what it does, request and
response fields with their required flags, and where each came from
(`operationId`, section, page). Those references become the citations.

**Read the field documentation and the examples, both.** Descriptions tell you
what a field means; examples frequently tell you what it actually takes — the
date format, the real enum values, how a nested object is shaped, which fields
are populated together, a field that appears in the example but was never
documented in the schema. Examples often complete behaviour the schema leaves
open, so use them. Where an example contradicts the schema, report the
contradiction rather than silently picking one.

In a schema, slow down for `allOf` composition (the real `required` list is the
union of all branches) and for a `$ref` pointing back at its own ancestor (a
relationship modelled as a nested object instead of an id — usually unusable,
and worth a spec-quality note).

**For a file specification**, the same inventory in file terms: each record
type or layout stands in for an endpoint, each column for a field — with
mandatory flags, types, lengths, code lists, the key linking records across
files, delivery mechanism, and any acknowledgement or error file.

### Whole-document checks

These are claims about what the specification does *not* contain, and they
decide capabilities as often as its contents do. Verify each against the whole
file rather than an impression — count or `grep` when the file is long.

- Operations by method — how many `GET`, `POST`, `PUT`, `PATCH`, `DELETE`.
- Auth actually applied (a root or per-operation `security` block), not merely
  declared under `securitySchemes`.
- Whether any operation declares an error response.
- Operations that return no body — a create that returns nothing gives us no id
  to store.
- Pagination (`page`, `limit`, `offset`, `cursor`) and incremental filters
  (`updated_since`, `modified_since`, `since`) on list endpoints.
- Rate limits — `429`, `Retry-After`, `X-RateLimit-*`, a documented quota.
- Every `enum`, since each one is a code list to map.
- `deprecated: true` on an endpoint a capability depends on.

Report what they return, including nothing: "no list endpoint supports
incremental filtering" is a finding, not a blank.

## Step 4 — Match each capability

Direction decides what to look for on the vendor side:

**Outbound** — Factorial is the source. We read from Factorial's endpoints and
**write into the vendor**, so the vendor needs **write** endpoints (`POST` to
create, `PUT`/`PATCH` to update) that accept what the Factorial read endpoints
return.

**Inbound** — the vendor is the source. We **read from the vendor** and write
into Factorial, so the vendor needs **read** endpoints (`GET`, ideally paginated
and filterable by modification date) that return what Factorial's write
endpoints require.

A rich read API contributes nothing to an outbound capability, and a rich write
API nothing to an inbound one. That mismatch is the most common way a vendor
that looks well covered turns out not to be.

For each capability, identify the vendor endpoints that implement it and put
them in the order an implementation calls them — including the supporting calls
that make the main one possible: resolving a legal entity or cost-centre id
before a create, reading back the vendor's identifier after it, looking up a
code list. Then check the fields, not just the endpoints: a `POST /employees`
exists in almost every HR API, and whether it can carry a Factorial new hire is
decided entirely by its fields.

## Step 5 — Map the fields

This is the core of the document. For each capability, map every field that
carries data between the two systems, in the direction the data flows.

For each row record: the source field and the destination field, as full paths
(`GET /employees → birth_on`; `POST /workers → person.date_of_birth`); whether
the destination requires it; the transformation, if any; and the evidence — the
schema, the documentation text, or an example.

Transformations are where integrations actually break, so be specific about
them:

- **Formats** — dates, timestamps and time zones, decimal separators, currency
  as code or symbol, amounts in major or minor units.
- **Code lists** — map values, not just fields. Give the value-to-value table
  when both sides publish their enums; when the vendor's list is configured per
  customer, say that the mapping is a per-customer configuration.
- **Structure** — one field split into several (a full address into street,
  number, postcode), several joined into one, a flat field that becomes a
  nested object, a list that must be flattened.
- **Units** — hours versus percentage for working time, monthly versus annual
  salary, days versus hours for absences.
- **Identifiers** — which side's id is stored where, and how a record is
  matched on the next sync.

Then list the two kinds of gap, separately, because they mean different things:

- **Vendor-required fields with no Factorial source.** These block the capability
  or force a default or a manual step. Each one needs a named resolution: a
  constant, a per-customer configuration value, a derivation, or a gap.
- **Factorial data with no vendor destination.** Usually just data the vendor
  doesn't hold; worth listing so nobody assumes it is synced.

Never invent a vendor field to complete a row. An unmapped row is a finding; a
plausible field name that isn't in the spec is a defect in the document.

## Step 6 — Classify

Three verdicts per capability.

**Fully supported** — the vendor exposes every operation the capability needs in
the right direction, every field the destination requires has a source, and the
record can be identified again on the next sync. Reachable only when the
specification is explicit about all of it.

**Partially supported** — the operations exist but something needed does not:
destination-required fields with no source, no update or correction path, no
way to match records on the next sync, no effective dating where the data is
time-dependent, a code list with no published values. Every partial verdict
states the limitation and a **viability** judgement — *shippable as-is* or *needs
the gap closed first*, and what closing it takes.

**Not supported** — the specification doesn't cover it: the operation or entity
is absent, the spec is silent, or the only route is manual work in the vendor's
UI. Absence and silence land in the same place because the consequence is the
same — we can only build against what is documented. Note in the capability
section whether the spec rules it out or is merely silent, since silence is a
question for the vendor that could change the verdict.

The line between the last two: a **missing field** makes a capability partial; a
**missing operation or entity** makes it not supported. Silence about one detail
inside a capability that otherwise works — whether re-sending replaces or
accumulates, say — is partial, with the detail named as the limitation.

## Step 7 — Write the document

Follow `assets/report-template.md`. Fill every section; write "none" rather than
dropping one, so a reader can tell "nothing to report" from "not analysed".

The capability summary comes first, because it is what the decision-maker
reads. Then one section per capability — every capability the domain page
lists, including the unsupported ones, so it is visible that each was assessed.
Each section carries the endpoint sequence, the field mapping, the gaps and the
verdict. The field mapping is the part an engineer will build from, so it must
be complete for the fields in scope and exact about paths and transforms.

Close with the vendor questions, ordered by how much each answer would change
the plan, merging any a single conversation would settle.

Save as `<vendor>-<domain>-integration-mapping.md`.

## Failure modes

- **Working from memory instead of the domain page.** The real capability lists
  are longer and sometimes counter-intuitive — directions included. Read the
  page every time.
- **Endpoint match without field match.** An endpoint with the right name and
  the wrong fields is a partial at best.
- **Ignoring examples.** Formats, enum values and undocumented fields often live
  only there.
- **Inventing fields.** Only map fields that appear in the vendor's
  specification.
- **Mapping fields but not values.** Two `status` fields with different enums are
  not mapped until their values are.
- **Asserting absence from an impression.** "There is no update endpoint" swings
  a verdict. Count or grep, then say it.
