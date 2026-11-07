---
name: acr-reporting
description: >
  Load this skill whenever you are converting a finished audit-scope
  accessibility evaluation into an Accessibility Conformance Report (ACR) draft
  in the OpenACR format, validating or rendering OpenACR YAML, or preparing the
  handoff to GSA's ACR Editor (https://acreditor.section508.gov/). Report-level
  companion to bug-reporting: findings→issues is bug-reporting;
  evaluation-report→ACR is this skill. Output is always a DRAFT for human review
  and sign-off — never a final or signed ACR. Under no circumstances map an
  untested Level A/AA criterion to any adherence term, derive a conformance term
  from finding severity, or invent metadata values (contacts, dates, versions).
license: Apache-2.0
compatibility: Claude Code-compatible; protocol is model-agnostic
metadata:
  author: zivtech
  version: "0.1.0"
---

# ACR Reporting Skill (OpenACR)

> **Status: RECOMMENDED — Phase 2 gate passed 2026-08-12.** The eval lane lives at `evals/suites/acr-reporting/` (fixtures 1/2/3/5 + rule-based scorer `ollama/score_acr.py` invoking the routed pinned CLI); the gate — hosted tier passes all four fixtures, stable across 2 independent draws — was met with zero must-tier misses and zero fabrications across eight opus rows (receipts: `evals/results/acr-reporting-phase2/`). The mandatory human handoff below is unchanged by the gate: every output is a draft, and model routing stands — generation on the hosted tier; a locally-produced draft is detector output behind the mandatory value-and-validate pass.

> **Verified facts + receipts:** [docs/openacr-reference.md](../../../docs/openacr-reference.md) (format, schema, CLI behavior, editor behavior — all claims receipted 2026-08-12). **Boundary ruling:** [docs/openacr-adoption-assessment.md](../../../docs/openacr-adoption-assessment.md).

Apply these rules when serializing a finished evaluation into OpenACR YAML, when validating or rendering an OpenACR document, or when preparing the human handoff.

---

## Core Mandate

**An ACR is a conformance-claim document someone may publish. Every value in it must trace to the engagement record or the evidence spine.**

The official toolchain will not catch boilerplate: `openacr validate` enforces neither SC completeness (a 2-criterion document validates) nor the not-evaluated-AAA-only rule (`not-evaluated` on a Level A criterion validates) — both verified, see the reference doc. The gates in this skill are the only thing standing between "untested" and a schema-valid published overclaim.

---

## Position in the Lifecycle

- **Audit-scope only.** Input is an evaluation report conforming to the [A11y Evaluation Report Contract](../../../docs/a11y-evaluation-report-contract.md) plus its findings ([A11y Evidence Finding Contract](../../../docs/a11y-evidence-finding-contract.md) blocks). This skill is the "populate" step the report contract's Boundaries section anticipates: the contract is the internal evidence spine; OpenACR is the external report format it populates.
- **Never generate an ACR from raw findings alone.** The per-SC outcome map, sample set, and coverage boundary live in the evaluation report — without them there is nothing legitimate to serialize.
- **Never map a detector-corroboration signal to an adherence term.** The A11y Evidence Finding Contract's `corroboration` / `detected_by` fields are triage-confidence tags, not conformance outcomes — `corroborated` means two scanners agreed, never that a criterion supports. No adherence term is ever derived from them; only the report's per-SC outcome map decides terms.
- **Never take a content-judgment draft as an outcome.** A row from the `a11y-content-judgment` skill's CSV is an outcome input only when its first column `status` is `RATIFIED` (a person's name in `ratified_by`); a `DRAFT_*` row is refused with the row id named in the handoff. Even a ratified `yes` is sample-scoped (one viewport, nothing activated, capped counts) and never maps to `supports` by itself — only a ratified `no` travels, as a finding.
- **Never take a draft fix-closure as a fixed-stage outcome.** A criterion whose outcome **improved since the prior evaluation** is a fixed-stage claim. The trigger is the report's own re-evaluation delta — the outcome-level list of criteria newly passing or failing that the report contract requires on every re-run — never an optional field: a report that declares itself a re-evaluation (`carried_from` in its sample set, a superseding document version, or a prior ACR named in the engagement record) and carries no delta is a missing input and blocks. A finding carrying `trend: resolved` is the secondary trigger and marks its criterion improved even when the delta omits it. The report's outcome map still decides every term; attestation decides only whether an improved term may be published. For every improved criterion, the fix-closure records ([A11y Fix-Closure Contract](../../../docs/a11y-fix-closure-contract.md)) closing the findings the prior evaluation carried on it must exist — none supplied is a missing input and blocks ("Blocked: improved criterion <SC> with no fix-closure record") — and every one must be *fully attested*: `attestation.status: attested`, a person's name in `attested_by`, `attested_against` equal to the report's product version, a `method` with action/expected/observed whose `observed` decided the operation (a walked `PASS` — a `BLOCKED` "cannot decide" or a `FAIL` never attests, however complete its shape), a `second_confirmation` by a named person who is either a different person or the same person on a later day, with at least one of the two not the fix's author — decided from the record's own fields, `self_attested` for the attester and `second_confirmation.authored_fix` for the confirmer, so `self_attested: true` needs a differently-named second confirmer who discloses `authored_fix: false`, and dates inside the evaluation window and not after `report_date`. Anything short of that — no block, `draft_not_attested`, an agent/model/tool identifier in either name field, a stale pin, a missing or one-line `method`, an `observed` that did not decide the operation, a single confirmation, the same name in both fields with no later date, `self_attested: true` with no differently-named second confirmer, `self_attested: true` whose `second_confirmation` omits `authored_fix` (absence is not independence) or discloses `authored_fix: true` (both confirmations by authors of the fix), a date after the report — is a draft: the improved criterion gets no adherence entry and goes to the INCOMPLETE list with the closure `item_id` named (protocol below), the same refusal this skill already makes for an unratified content judgment. The asymmetry is intended: no record at all blocks the draft, because nothing can be listed; a draft record produces an INCOMPLETE draft that names what is missing. Both refuse the term. The gate is one-way: absent provenance suppresses an improved term; present provenance never creates or upgrades one.
- **Component-scope reviews never produce ACRs.** The report contract already rules that an EM-shaped report at component scope is checkbox theater; an ACR at component scope is that plus a conformance claim. Treat a component-scope ACR request as a scoping error and say so.
- **Boundary with bug-reporting:** bug-reporting converts individual findings into reproducible issues (finding-level). This skill aggregates the finished evaluation into a conformance report (report-level). One feeds trackers; the other feeds procurement.

---

## Inputs Required (block if any is missing)

| Input | Source | Notes |
|---|---|---|
| Evaluation report | Contract-conformant, incl. `outcomes` per-SC EARL map, `sample_set`, `coverage_boundary`, `conformance_target`, `accessibility_support_baseline` | The spine. No report, no ACR. |
| Findings | Evidence-contract blocks with `finding_id`, `fingerprint`, `evaluation_context` (`sample_id`s) | Cited in notes. |
| Fix-closure records | a11y-test / remediation lane | **Conditional — re-evaluations:** one per finding the prior evaluation carried on each criterion whose outcome improved (per the report's re-evaluation delta, or a `trend: resolved` finding). Fully attested (named person, matching version pin, action/expected/observed method, second confirmation, dates inside the window) or the criterion's *improved* term goes INCOMPLETE (unattested-closure gate). Missing for an improved criterion → block, gap named. A re-evaluation with no delta section → block. |
| Report title | Engagement record | Schema-required (`title`). |
| Product name + version | Engagement record | Schema-optional but a draft without them is useless — required here. |
| Author contact incl. **email** | Engagement record (the drafting evaluator) | `author.email` is the schema's one hard-required contact field (verified: validation fails without it). |
| `report_date` | Engagement record (evaluation completion date) | Never today's date by default — the evaluation's date. |
| Feedback channel, license, repository | Engagement record | Optional; include when the engagement publishes them. |

**Never invent any of these.** If a required input is absent, the draft **blocks** with a named-field gap list in the handoff (e.g., "Blocked: no author email in engagement record"). A fabricated contact, date, or version is the worst failure this skill can produce.

---

## Catalog Selection (decided at planning time — never a fallback)

The planner's AUDIT-SCOPE MODE collects the report template as an additional requirement; the catalog choice is made **there**, not at serialization time.

| Engagement need | Catalog | Finish surface |
|---|---|---|
| Default — WCAG 2.2 AA target (the skills' standard) | `2.5-edition-wcag-2.2-508-en` | YAML + CLI-rendered HTML. **acreditor cannot import 2.2 documents today** (verified: rejects them by criterion). |
| acreditor required as the review/finish surface | `2.4-edition-wcag-2.1-508-en` | acreditor "Open report" import (verified working). 2.2-only outcomes ride the out-of-catalog annex — see below. |
| Plain-WCAG or EU report | `2.5-edition-wcag-2.2-en` / `-508-eu-en` | Best-effort. The EU catalog's non-WCAG clauses (EN 301 549 hardware/functional chapters) have **no mapping** in this skill. |

**Measured outcomes are never dropped.** A 2.1-catalog draft from a 2.2-target evaluation carries every 2.2-only outcome in the annex.

---

## Outcome → Adherence Mapping (normative)

Outcomes use the report contract's EARL vocabulary, aggregated across the sample set. Adherence terms are the catalog's five.

| Outcome across the sample set | Adherence term | Condition |
|---|---|---|
| `passed` everywhere applicable | `supports` | Canonical sample-scope note form. |
| `failed` wherever applicable | `does-not-support` | Note states sample scope + cites `finding_id`(s). |
| Mixed pass/fail across samples or instances | `partially-supports` | Note enumerates failing `sample_id`s + cites `finding_id`(s). |
| `inapplicable` | `not-applicable` | Note states why (content type absent from product and sample). |
| `untested` or `cantTell` on any A/AA SC | **no mapping — emission blocker** | Draft becomes INCOMPLETE (protocol below). |
| AAA criterion without evidence | `not-evaluated` | The only place the term is legal. When AAA evidence exists, map it by outcome like any other SC. |

Two semantic cautions:

- The catalog's official term definitions are **functionality-proportion claims** ("Partially Supports: *Some* functionality … does not meet"; "Does Not Support: *The majority* of product functionality does not meet"). Our evidence is **sample-scoped**. The deterministic mapping above is correct, but every `does-not-support` and `partially-supports` note must carry its sample scope explicitly so the reader can see what the claim rests on.
- **Severity never selects the term** (report contract § Orthogonality Rule). A CRITICAL finding on a passing SC does not downgrade `supports`; a MINOR-severity failure does not soften `does-not-support`. Impact language belongs in notes; terms come only from outcomes.

---

## Claim boundaries (orthogonality mechanism)

The orthogonality cautions above — severity never selects the term, terms come only from outcomes — are made checkable rather than merely asserted by a `claim_boundary` on the adjudication record: an explicit statement of what an entry does and does **not** assert, plus an attachment rule — a remediation entry may attach only to a source-adjudicated criterion still joined to a selected failure. In this skill that means a remediation recommendation never upgrades an adherence term, and an entry that derives one axis from another — inferring a term from a fix having been proposed, or from a finding's severity — is malformed.

This is the acr-side use of the bundle's full orthogonality register in `docs/a11y-orthogonality-register.md`, which enumerates the axis pairs (conformance outcome vs impact severity; remediation entry vs conformance evidence; and others) and the shared `claim_boundary` mechanism.

---

## Chapter & Component Policy

- **Populate only the `web` component** from our evidence. Omit non-web components (`electronic-docs`, `software`, `authoring-tool`) from criteria entries entirely — schema-legal and verified. The document `notes` state the method's web-only scope.
- **508 chapters** (`functional_performance_criteria`, `hardware`, `software`, `support_documentation_and_services`): set `disabled: true` with a chapter note built from the report's `coverage_boundary` (what the web measurement stack could not measure, and what covered it instead — or that nothing did). The FPC note may carry the evidence contract's `section_508_fpc_context` inputs; **conclusions in these chapters stay human**. Verified: `disabled:` chapters pass CLI validation and import into acreditor with their notes rendered.
- **AAA chapter**: `not-evaluated` per the mapping table — the catalog's own device, not `disabled:`.

---

## Canonical Note Forms (machine-checkable — the eval scorer greps these)

| Term | Note MUST begin | Then |
|---|---|---|
| `supports` | `Sample-scoped: passes across <N> structured + <M> random samples (WCAG-EM).` | Optional context. **No `finding_id`** — the evidence contract forbids findings for passing checks. |
| `supports` on a remediated criterion | The same stem, then `Remediated since the prior evaluation: <finding_id> resolved; closure <item_id> attested and second-confirmed at <version>.` | The one place a `finding_id` belongs in a `supports` note: a reader must be able to tell an originally-passing criterion from a fixed one, and who confirmed the fix. Every fully attested closure the term rests on is named. |
| `does-not-support` / `partially-supports` | `Sample-scoped: fails in <sample_id list or scope>.` | At least one `finding_id` (with `fingerprint` where useful for trend). `partially-supports` enumerates failing `sample_id`s. |
| `not-applicable` | `Not present:` | Why the content type is absent. |
| `not-evaluated` (AAA only) | `Not evaluated at this engagement's conformance target (WCAG 2.2 AA).` | — |
| `disabled:` chapter note | `Outside the web evaluation method's coverage:` | The `coverage_boundary` statement. |

`finding_id`s make the ACR a living document — the Drupal OpenACR precedent uses per-remark issue links; our fingerprints formalize the same practice and enable Lane C trend diffs on re-evaluation.

---

## INCOMPLETE Drafts (the untested gate — load-bearing)

- Any A/AA SC with outcome `untested` or `cantTell` gets **no adherence entry** — the SC is omitted from `chapters` so the file stays CLI-valid.
- The document `notes` field MUST begin: `INCOMPLETE DRAFT — untested A/AA criteria: <comma-separated SC numbers>`.
- The handoff message carries the same list with a per-SC reason (not sampled / tooling gap / ran out of scope) so the human can commission the missing testing.
- **`not-evaluated` on an A/AA criterion is forbidden even though the CLI accepts it** (verified it does; the catalog's own term text restricts it to AAA). Emitting it is a must-fail.
- **The unattested-closure gate — the second route to INCOMPLETE.** An A/AA criterion whose *improved* term (`supports`, or a `partially-supports` narrower than before) rests on a `trend: resolved` finding whose fix-closure is not fully attested gets **no adherence entry** — omitted from `chapters` exactly like an untested SC. The document `notes` carry a second marker line, after the untested line when both exist, that MUST begin: `INCOMPLETE DRAFT — unattested fix-closures on A/AA criteria: <SC (item_id), ...>` — each criterion followed by its closure `item_id` in parentheses, on that line. The handoff names each `item_id` with what is missing (no attestation block / draft status / attested by an agent / stale version pin / method without an observation / only one confirmation / the same person twice with no later day / self-attested with no second person / dated after the report) and who can close it: a named person confirming the fix on the pinned version, not more automated testing. Two things this gate never does: it never touches a criterion that is **still failing** — a `does-not-support` or unchanged `partially-supports` keeps its entry, and a resolved-but-unattested finding on it is named in that entry's note (`<item_id> resolved but not attested`) rather than moved to the marker line, because dropping a disclosed failure from a conformance document is worse than disclosing it; and it never lists an attested closure — refusing a criterion whose closure carries two named people is over-refusal and a must-fail, the same as a spurious untested marker. An SC is never on both marker lines: an untested criterion has no outcome to improve, so the untested line takes it and the unattested line never lists it.
- A complete draft MUST NOT carry either INCOMPLETE marker — spurious gap entries on complete evidence are the serializer's version of a critic that flags everything.
- **A non-pass is not one state.** When the per-SC reason distinguishes causes, use the more specific one instead of a generic "not sampled": "no access" (the evaluator was not authorized to reach the content or environment) and "needs a human owner" (the gap can only be closed by someone outside the testing party, not by more automated testing) are common enough to name explicitly, alongside tooling gap and ran out of scope. Distinguishing them tells the human who to route the gap to, not just that a gap exists.
- **A tool-lane skip is a non-pass, never a silent clean.** When an underlying detector lane reports a skip disposition (a required credential or license was absent, or the tool itself errored) rather than actually running, that SC or sample is `untested` — never rolled up as `passed` because the tool produced no violations. No detection because a tool never ran is not evidence of conformance.
- **Coverage ledger discipline.** Before a gate closes, every required page-view or sample in scope must have a tracked disposition — the INCOMPLETE marker's SC list is this ledger's visible form for A/AA criteria. Untested, skipped, and blocked entries stay visible in that list rather than silently dropping out of the count; a gate does not close on an assumption that an absent entry means "fine."

---

## Out-of-Catalog Annex (2.1-catalog drafts only)

When the evaluation targeted WCAG 2.2 but the draft uses the 2.4-edition/2.1 catalog (acreditor surface):

- Document `notes` include: `Out-of-catalog annex: <n> WCAG 2.2-only criteria measured under conformance target WCAG 2.2 AA — see handoff annex.`
- The handoff annex lists each 2.2-only SC (2.4.11, 2.4.12, 2.4.13, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8, 3.3.9 as applicable) with its outcome, would-be term, and `finding_id`s.

---

## Federal DRAFT discipline (declared-508 multi-deliverable engagements)

When a declared Section 508 engagement produces more than one report artifact, the DRAFT ACR is **one of three separate deliverables** fed by a single completed evaluation report — a Standard Section 508 report, an ICT Testing Baseline report, and this DRAFT OpenACR. They are distinct artifacts; do not copy terms or outcomes between them without applying each format's own mapping rules. (The Revised-508 floor vs WCAG 2.2 AA remediation-layer separation is already stated in the federal profile; this section does not restate it.)

**Non-conflation list — the cross-contaminations to refuse:**

1. A commissioner-facing addendum (a keyboard/operation retest, a focused observation set) is never retitled into a full report. A report requires the completed audit-scope evaluation spine, not a repackaged addendum.
2. WCAG 2.1/2.2-only outcomes stay out of the 508 (WCAG 2.0 A/AA) adherence terms; they appear only in the remediation layer. Never promote a remediation-layer 2.1/2.2 outcome into an adherence term.
3. No SC-to-baseline-test fan-out in either direction: one WCAG SC failure does not fail every baseline test that maps to it, and one SC pass does not pass them.
4. Capability/coverage classification (how many baseline tests the stack is *designed* to cover) is never reported as a product outcome, and the volume of collected evidence does not move a frozen capability figure.
5. A baseline-test or catalog-criterion ID is cited only after validation against its manifest/catalog — never a guessed or nearest-neighbor ID.
6. One deliverable references another's rows; it does not restate them (the 508 report references the baseline annex; it does not re-emit it).
7. Each deliverable consumes only evidence that passed its own contract and scope gate; evidence admissible for one is not automatically admissible for another.

**Draft legibility — `[Demo Purposes Only]`:** in a DRAFT ACR, every displayed role or participant **other than the actual tester** — commissioner, audit owner, product owner, evaluation author/reviewer/approver, any displayed participant name — is labeled `[Demo Purposes Only]`, so no reader mistakes a draft for a signed report. The label:

- applies to **display-name fields only** — never to a format-constrained field (`author.email`, any date, any version). Where such a field has no verified value the draft **blocks** with a named-field gap list; it is never filled with the demo label or a placeholder.
- never licenses fabricating a person, email, date, version, organization, or approval to satisfy the rule.
- leaves exactly one non-demo identity: "the tester," the party that actually operated the collection tooling — never applied to a role that did not perform the runs.

This is the display-layer companion to the skill's existing "invent nothing" rule: the untested gate keeps a draft from *containing* claims it has not earned; `[Demo Purposes Only]` keeps it from *looking* like a report that earned them.

---

## Serialization Procedure

Serialize the draft from the evaluation report and evidence-contract finding blocks (`finding_id`s) already on hand, plus targeted per-finding lookups — never by re-reading the underlying raw evidence corpus wholesale.

1. **Verify inputs** against the block list. Missing input → stop, emit the named-field gap list.
2. **Select the catalog** from the engagement record's report-template requirement (never guess; never downgrade silently).
3. **Build the metadata block** field-by-field from the engagement record: `title`, `product`, `author` (with email), `report_date`, `evaluation_methods_used` (MUST state WCAG-EM + sample size: e.g., "WCAG-EM 2.0; 12 structured + 2 random samples + 2 complete processes"), and a **mandatory `legal_disclaimer`** carrying draft language (e.g., "Draft for review — not a legally binding conformance claim until reviewed and issued by <owner>").
4. **Map every A/AA SC in the catalog** — present with a term + canonical note, or blocked into the INCOMPLETE list. Work from the catalog's criterion list, not from the findings list (findings only exist for failures; the catalog is the completeness frame).
5. **AAA chapter and disabled chapters** per the chapter policy.
6. **Self-check completeness**: every catalog A/AA SC accounted for (present-or-blocked). The CLI will not check this — you must.
7. **Validate** via the routed CLI (below). Fix schema/catalog errors; never "fix" by inventing values.
8. **Render** with `openacr output` (`-t` is required — the CLI errors without a template): Markdown for review diffs, HTML for the human read.
9. **Write the handoff message**: finish surface, review checklist, INCOMPLETE list (if any), annex (if any), and the draft/never-final statement.

---

## Validation & Rendering (routed, never vendored)

Exact-pin **`@openacr/openacr@0.3.8`** (frozen upstream; CC0). Consuming projects add it as a devDependency; for ad-hoc runs use a scratch directory:

```bash
mkdir -p /tmp/acr-check && cd /tmp/acr-check && npm init -y >/dev/null && npm i @openacr/openacr@0.3.8
npx openacr validate -f draft.yaml -c node_modules/@openacr/openacr/catalog/<catalog-id>.yaml
npx openacr output -f draft.yaml -c node_modules/@openacr/openacr/catalog/<catalog-id>.yaml \
  -t node_modules/@openacr/openacr/templates/openacr-html-0.1.0.handlebars -o draft.html
```

**Always pass `-c` — on both commands.** Neither command loads the document's
own `catalog:` field (Phase 2, reproduced): `validate` without `-c` is
schema-shape only and accepts nonexistent criterion numbers; `output`
without `-c` exits successfully and silently renders a metadata-only shell
with zero criteria tables. A bare `validate -f` is no validation at all, and
a rendered HTML must be checked to actually contain its criteria tables
before it is circulated.

Catalogs, schemas, and templates all ship inside the package — reference them from `node_modules/@openacr/openacr/`, never copy them into a repo.

**Cell-level value verification.** Schema and catalog validation confirm shape and that criteria exist — never that the *numbers are right*. A rendered outcome table, a coverage rollup, or a serialized count can be structurally valid and numerically wrong (a miscounted sample tally, a dropped finding, a double-counted row). Before a draft circulates, verify its generated tables cell-by-cell against the completed evaluation report's known totals — sample counts, finding counts, per-criterion tallies — not only that the tables are present. See the report contract's Generated-Deliverable Verification rule.

| The CLI checks | The CLI does NOT check (skill self-checks) |
|---|---|
| YAML/schema shape; `author.email` present | A/AA completeness (step 6) |
| Criterion numbers exist in the catalog — **only with `-c`** | `not-evaluated` restricted to AAA (INCOMPLETE protocol) |
| Term strings are catalog terms — **only with `-c`** | Term appropriateness vs outcomes; note forms; value provenance |
| — | An absent `license` (the schema assumes **CC-BY-4.0** "in any output" — a withheld license must be surfaced in the handoff as a decision the owner still owes, never treated as safely empty) |

---

## Handoff (mandatory human steps — every draft, every time)

**2.1-catalog drafts (acreditor surface):** the human opens https://acreditor.section508.gov/ → "Open report" → selects the YAML. Verified behavior: the editor validates on import, renders chapter notes, drops `disabled:` chapters from progress, and stores everything in browser localStorage only — the saved YAML file is the persistence mechanism, nothing is uploaded to a server. The human reviews every chapter, adds non-web component conclusions where they hold evidence, completes contact/legal review, and exports.

**2.2-catalog drafts:** the human reviews the rendered HTML + YAML directly (acreditor cannot import them today — reference doc, watch rule). Edits go into the YAML; re-validate after.


**Attestation roster (re-evaluations):** the handoff lists every closure `item_id` the draft's improved terms rest on — criterion, `attested_by`, `second_confirmation.by`, `attested_against` — as a block the signing author countersigns before publication. This is the step that binds the names on the closure records to a person who is accountable for the ACR; the records themselves cannot (fix-closure contract, "what this block cannot do"). A draft whose improved terms rest on closures missing from the roster is not ready for handoff.

**The human owns:** sign-off, publication, removal of the draft disclaimer, the license decision (an absent `license` renders as CC-BY-4.0 by the schema's own default — say so in the handoff whenever the engagement record withholds one), and every conformance statement made to a third party. This skill never auto-publishes, never auto-signs, never emits a final ACR, and never writes to acreditor.

---

## Model Routing

ACR YAML is value-dense (contacts, dates, versions, per-SC terms) — the documented local-model fabrication class. **Generation runs on the hosted tier.** Local models are detectors only; any locally-produced draft requires a mandatory **field-by-field value-check pass** — performed by a hosted-tier model or the human — comparing every metadata value and every term against the source evaluation report before validation counts for anything.

---

## Five Non-Negotiables

1. **Orthogonality** — terms from outcomes only; severity lives in notes.
2. **Untested gate** — no term for untested A/AA; `not-evaluated` is AAA-only; the gate is load-bearing because the CLI provably doesn't enforce it.
3. **No conformance overclaim** — WCAG-EM + sample size stated; sample-scoped language throughout; sampling alone never supports a whole-product conformance claim (report contract rule).
4. **Draft, never final** — `legal_disclaimer` mandatory; publishing is a human act.
5. **Completeness is ours to check** — every catalog A/AA SC present-or-blocked; the CLI accepts fragments.

---

## Boundaries

- **Not yet in this skill:** claims verification of third-party ACRs (Lane B — Phase 3, adjudicated by a11y-critic), ACR drift diffs (Lane C — Phase 4), and merging a new audit into an existing hand-maintained ACR (explicitly out of scope; say so when asked).
- **Naming:** the artifact is "an ACR in OpenACR format" — never "a VPAT" (VPAT® is an ITI trademark; VPAT edition names appear only inside catalog identifiers).
- **Non-web conclusions are human-owned.** This skill serializes their boundary statements, never their conclusions.
- **No report-generator runtime** in the skills repo (existing contract ruling): the agent authors the YAML per this skill; validation/rendering route to the pinned CLI.

---

## Pre-Handoff Quality Checklist

* [ ] Every catalog A/AA SC is present with a term or named in the INCOMPLETE list
* [ ] No `not-evaluated` outside the AAA chapter
* [ ] Every `trend: resolved` finding has a fully attested fix-closure record (named person, version pin, action/expected/observed, second confirmation, dates in window), or its improved criterion is on the unattested-closures INCOMPLETE line with the `item_id` named — no attested closure listed there, no still-failing criterion moved there, and every remediated `supports` note carries the `Remediated since` form
* [ ] Every term traceable to the outcome map — no severity-derived terms
* [ ] Every `does-not-support`/`partially-supports` note cites ≥1 real `finding_id` and states sample scope
* [ ] Every `supports` note uses the canonical sample-scope form
* [ ] Metadata values traced to the engagement record — zero invented values
* [ ] `evaluation_methods_used` states WCAG-EM + sample size
* [ ] `legal_disclaimer` present with draft language
* [ ] Disabled chapters carry `coverage_boundary` notes
* [ ] 2.1-catalog drafts: out-of-catalog annex present when 2.2-only outcomes exist
* [ ] `openacr validate` passes on the exact file being handed off
* [ ] Rendered HTML produced and attached to the handoff
* [ ] Handoff message names the finish surface and the human-owned steps
* [ ] Re-evaluations: the delta section exists, every improved criterion's closures are in the handoff's attestation roster for countersignature, and no SC sits on both INCOMPLETE lines

---

## References

- [OpenACR verified reference](../../../docs/openacr-reference.md) — receipts for every format/CLI/editor claim above
- [Integration plan](../../../docs/plans/2026-08-12-openacr-integration-plan.md) — lanes, eval design, phase gates
- [A11y Evaluation Report Contract](../../../docs/a11y-evaluation-report-contract.md) / [A11y Evidence Finding Contract](../../../docs/a11y-evidence-finding-contract.md)
- [GSA/openacr](https://github.com/GSA/openacr) · [GSA/openacr-editor](https://github.com/GSA/openacr-editor) · [ACR Editor (live)](https://acreditor.section508.gov/)
- [WCAG-EM 2.0 reference](../../../docs/wcag-em-2-reference.md) — the methodology the evaluation report cites
