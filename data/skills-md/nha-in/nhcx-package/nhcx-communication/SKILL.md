---
name: nhcx-communication
description: >-
  Build NHCX (India's National Health Claims Exchange) payer communication into an existing HMIS: receiving payer queries, notifications and notes on a pre-authorisation or claim, replying with text and documents, and acknowledging notifications, with the embedded NHCX gateway it needs. Use when a hospital system must answer insurer or PMJAY queries over NHCX.
metadata:
  version: "1.11.0"
---

**Version 1.11.0**, built 2026-10-25, checked against NHA's NHCX package 1.0.0.

# READ FIRST: CORE
Before anything else, read [references/CORE.md](references/CORE.md) and keep it in mind for the whole task. Its **Instructions** are binding: follow them strictly in every step and every file, and re-read them at the start of each step (L1 to L8). Its **Confusions** settle what easily mixed-up terms mean; when a word is ambiguous, CORE.md decides. It also holds the base URLs and, for every exchange, the route, bundle, workflow id and callback.

# WHICH SIDE
This skill is the **provider side**: it builds NHCX into a hospital's HMIS, the participant that asks (eligibility, plan, pre-authorisation, claim) and is answered. The folder [payer/](payer/SKILL.md) is the **payer side** of the same skill: an insurer, TPA or scheme system, the participant that answers, files cases and decides them. The two share nothing but the gateway design; their ids (S1, A1, C1) are numbered separately and never mix.

Decide the side at the start of L1 discovery, before any spec is matched, and record it as `side` in `nhcx-plan/discovery.json` and in the progress log:
- **provider** when the target admits patients, keeps practitioners and encounters, bills an insurer, or has a claims desk that submits: continue with this file and the specs, steps and references at this root, and ignore `payer/` entirely.
- **payer** when the target keeps members or beneficiaries, products or policies and their enrolments, adjudicates claims on a desk, or disburses money: stop here, open [payer/SKILL.md](payer/SKILL.md) and follow it as the whole skill from its own L1, and ignore every spec, step and reference at this root. Everything it links to is inside `payer/`.
- **both** (a system that admits patients and also runs a scheme): two integrations, one per side, each planned and logged on its own; do the side the user asked for first, and never mix the two id sets in one plan file.

When in doubt, ask the user which side the target is before L1.1. A later prompt that finds the other side was meant logs a `corrected` entry and starts again from L1 on the right side.

# UPDATE FIRST
At the start of every task, before the questions and L1, and at the start of every later prompt that continues the work, check whether the NHCX package carries a newer build of this skill, and if it does, install it and work from it.

**Independent of the MCP and of the knowledge source.** The check always reads the package on GitHub, whichever knowledge source L1.0 chose: a connected nhcx-docs MCP neither answers it nor skips it, and the MCP's `catalogue_info` version is never compared with the skill's. The skill's version is its own: it is not the package's release tag, nor the catalogue's version, nor `1.0.0`; only the version in `skills/manifest.json` is compared with it.

1. **Read the package's skills manifest.** The package (github.com/nha-in/nhcx-package) keeps a copy of the built skills under `skills/`, with `skills/manifest.json` naming their version (`version` for the provider skills, `companion.version` for the payer skills under `skills/payer/`) and `skills/CHECKSUMS.sha256` the hash of every file. Read it from `https://raw.githubusercontent.com/nha-in/nhcx-package/main/skills/manifest.json`; else from the latest release zip (`nhcx-package/skills/manifest.json`) (the zip of `https://api.github.com/repos/nha-in/nhcx-package/releases/latest`). A package already downloaded as the knowledge source is not read for this: it may be older than `main`.
2. **Compare** its `version` with this build's `1.11.0`, part by part as numbers (1.10.0 is newer than 1.9.2).
3. **Newer in the package: pull and install it.** Download the package (the release zip whose skills manifest carries that version, else the `main` archive `https://codeload.github.com/nha-in/nhcx-package/zip/refs/heads/main`) into a new empty folder outside the target repository, and check every file under `skills/` against `CHECKSUMS.sha256`. Then replace the folder this SKILL.md was loaded from, and every sibling NHCX skill folder installed beside it (`nhcx-full`, `nhcx-coverage`, `nhcx-preauth`, `nhcx-claim`, `nhcx-communication`, `nhcx-payment`, `nhcx-reprocess`, and the nested `payer/`), with the package's copy of the same name, whole: no file of the old build is left behind. A skill installed by a plugin manager is updated through it when it offers that version, else its skills folder is replaced the same way. Nothing in the target repository or `nhcx-plan/` is touched by the install. Tell the user in one line ("Updated the NHCX skills from 1.8.0 to 1.9.0 from the NHCX package."), log it, then re-read this SKILL.md and CORE.md from the installed copy and carry on from them; VERSION then re-checks the finished steps against what changed.
4. **Same or older:** carry on with this build.
5. **Not reachable, or a checksum fails:** carry on with this build, say so to the user in one line, and log the reason. A copy that fails its checksums is never installed, not even in part.

Every check is recorded in `nhcx-plan/knowledge.json` under `skill_update` (`checked_at`, `source`, `package_skill_version`, `installed_version`, `result`: `current`, `updated`, `unreachable` or `checksum_failed`) and logged in `nhcx-plan/progress.json` (step `L0`, item `skill update`).

# ASK FIRST
Before discovery, before the knowledge source, before any file is read, ask the integrator the questions of [steps/L1-discovery.md](steps/L1-discovery.md) section L1.A in one numbered message and wait for the answers: whether a claim must start from a registered patient and whether the member id is captured at the start; whether the insurance plan is fetched automatically once the case is created (the default) or by the desk, refreshed automatically or by hand, and once per payer and policy or per case; which fields of the payer's InsurancePlan the hospital needs; whether the benefits check and the authorisation-requirements ruling are offered on the pre-authorisation page; whether a pre-authorisation may go before admission (the admission is then linked on the Claim tab) and after how many hours an approved one is withdrawn when the patient is not admitted; whether additional documents, the Aadhaar as supporting information and biometric verification are wanted; whether a claim needs an admission; whether a discharge intimation is sent before the claim; whether the desk checks for the payer's answers with a Refresh button or the case polls at a fixed interval (and how often); and which payer letters the desk must see. Record every answer in `nhcx-plan/plan.json` under `decisions`. Nothing is built on a guess where a question exists.

Two things are never asked, because discovery answers them: **the HMIS's own M1** (ABHA create, link and verify, the ABHA identifier on the patient, the ABDM session token) is reused automatically whenever L1.3 finds it, and only an HMIS without one gets A19. ABHA Create and Verify (ABDM M1) (in nhcx-coverage); and **the host's UI components** (type-ahead, select, table, chip, card, accordion, dialog, date picker, file input, flash or toast, tabs with a dot badge) are found in L1.2 and used for every screen.

# GOAL
Add NHCX payer communication to the target HMIS.

This skill holds only the specs this goal needs; the SCOPE section lists them. Specs it names but does not hold are marked with the skill that has them.

# REQUIREMENTS
- **The target HMIS source**, with its build, test and migration commands working.
- **NHCX participant credentials** for the facility: participant code, ABDM client id and client secret, and the private key of the encryption certificate registered for that code.
- **A public URL** NHCX can reach, registered as the participant's `endpoint_url`, routed to the application's inbound path (`/in/<path>` or `/v1/<path>`).
- **A knowledge source**: the nhcx-docs MCP server, or network access to download the NHCX package (see KNOWLEDGE SOURCE). The ABHA calls (A19), needed only when the HMIS has no M1 of its own, need the MCP: the package carries no M1.
- The beneficiary's biometric authentication (A18, optional for any payer, required by PMJAY) needs a registered fingerprint or iris device with its RD service on the desk machine, or the ABHA app on the patient's phone for face; and a client id whose session token the ABHA and biometric services accept.
- For end-to-end tests: sandbox credentials, a sandbox payer that answers, and test beneficiaries.

# KNOWLEDGE SOURCE
NHCX facts (API paths and headers, FHIR profiles and example bundles, codes, workflow ids, error codes, go-live rules) come from one knowledge source, chosen at the start of L1 and recorded in `nhcx-plan/knowledge.json`. Details: [references/KNOWLEDGE.md](references/KNOWLEDGE.md).

1. **nhcx-docs MCP.** If the `nhcx-docs` MCP server is connected (`catalogue_info` answers), use it: `search_docs`, `get_operation`, `get_fhir_profile`, `get_fhir_example`, `validate_request`, `decode_error` (not `validate_fhir` on an NHCX bundle: it knows only ABDM's DocumentBundle family, see [references/KNOWLEDGE.md](references/KNOWLEDGE.md)).
2. **GitHub package.** Otherwise download the latest release zip from [github.com/nha-in/nhcx-package/releases](https://github.com/nha-in/nhcx-package/releases) (`nhcx-package-v<version>.zip`), keep it as `nhcx-plan/knowledge/nhcx-package-v<version>.zip`, extract it to `nhcx-plan/knowledge/nhcx-package/`, and check it against its `MANIFEST`.

The same MCP server also serves ABDM's HIE-CM catalogue. **ABHA creation and verification (M1), and the health records an HMIS files under M2 and this skill attaches to claims ([D28. claim_document](database/D28-claim-document.md) "From records"), are read from it, not from this skill** (the `abdm-m2` prompt and the atoms in [references/KNOWLEDGE.md](references/KNOWLEDGE.md)): A19. ABHA Create and Verify (ABDM M1) (in nhcx-coverage) says what the application does when the HMIS has no M1 of its own, and names the M1 flow and operation ids to read with `get`, and the `abdm-m1` prompt is its router. An HMIS that already has M1 keeps it: nothing of A19 is built and the user is not asked. The biometric authentication of the beneficiary is defined in full here, A18. Biometric Authentication (in nhcx-coverage) with its proof-of-presence card S18. Beneficiary Verification (in nhcx-coverage), because the NHCX package has it and the sends depend on it.

On the protocol the knowledge source wins over these specs; on what the application does, the specs win. Statements that are not the protocol are marked [REF](references/PAYERS.md#markers) (a reference-implementation choice), [PAYER](references/PAYERS.md#markers) (depends on the payer adapter) or [SANDBOX](references/PAYERS.md#markers) (seen only in the sandbox); every payer-specific value is in [references/PAYERS.md](references/PAYERS.md). Its ids (NHA use cases such as `C5`) are not this skill's ids: write them as `nha:C5`.

# STEPS
This skill builds **in milestone mode only**. The build is cut into the vertical slices of the claim lifecycle in [milestones/INDEX.md](milestones/INDEX.md), and each slice is carried through every step before the next begins. There is no layered mode: never run L1 across every spec, then L2 across every spec; that is the old shape and is not used. Record `"mode": "milestone"` in `nhcx-plan/knowledge.json`.

Each step writes one file per milestone under `nhcx-plan/<Nx>/` in the target repository, and every sub-step and file change is logged in `nhcx-plan/progress.json` and `nhcx-plan/progress.md` ([steps/LOG.md](steps/LOG.md)). At the end of every prompt, whatever it did, rebuild `nhcx-plan/report.html` ([steps/LOG.md](steps/LOG.md#logh-reporthtml)): an Overview (KPIs, a milestone stepper and a milestones-by-steps matrix), a Bootstrap tab, one tab per milestone (its L1 to L7 steps and their records), an End-to-end tab and a Log tab; `nhcx-plan/make-report.sh once` rebuilds it, `make-report.sh watch` keeps it current.

The seven steps each milestone is carried through (discovery to dry-run):

1. [L1 Discovery](steps/L1-discovery.md): the knowledge source, the target's technology, and every spec item **the milestone delivers** found, partial or missing, with file and lines.
2. [L2 Mapping](steps/L2-mapping.md): the milestone's fields to database columns and FHIR elements.
3. [L3 Integration Planning](steps/L3-integration-planning.md): the milestone's phase, steps and sub-steps for this target, in the build order of the [SCAFFOLDING](references/SCAFFOLDING.md), including the "Claims" entry on the HMIS home screen, sidebar or navbar (in N0).
4. [L4 Code Planning](steps/L4-code-planning.md): the milestone's files, functions and order, laid out by mapping the [SCAFFOLDING](references/SCAFFOLDING.md) onto the target's conventions.
5. [L5 Write Code](steps/L5-write-code.md): file by file, recorded in `nhcx-plan/<Nx>/code.json`, keeping the scaffolding's dependency rules.
6. [L6 Validate Code](steps/L6-validate-code.md): each file against its specs.
7. [L7 Dry-run Tests](steps/L7-dry-run-tests.md): no network; fakes for NHCX and the registry. A milestone's done-when is proven here, against the mocked gateway and stubbed callbacks.

Then, **once**, after every milestone's dry-run is green (not per milestone):

8. [L8 End-to-end Tests](steps/L8-e2e-tests.md): the whole lifecycle N1 to N6 against the NHCX sandbox, the T tests in [references/TESTS.md](references/TESTS.md), each run through the screens (GUI) and from the command line (CLI), writing one `nhcx-plan/e2e.json` at the root.

# MILESTONES
The build runs the slices of [milestones/INDEX.md](milestones/INDEX.md) in dependency order: **N0 Foundation**, then **N1 Search Policy**, **N2 Coverage and Insurance**, **N3 Pre-authorisation and Biometric**, **N4 Communication**, **N5 Claim**, **N6 Payment**. Each milestone is carried through the seven steps above (L1 to L7, discovery to dry-run) over **only the spec ids it delivers**, declares the milestones it depends on, and reuses what they built rather than rebuilding it. L8 end-to-end is not part of a milestone: it runs once at the end, across the whole lifecycle.

- **Global bootstrap first.** Before N0, run L1.0 (the knowledge source), L1.1 (the NHCX scan), L1.2 (the target's technology and component kit) and L1.3 (the ABDM module) once: these are properties of the target, not of a slice, so they are found once, written to `nhcx-plan/knowledge.json` and the technology part of `nhcx-plan/discovery.json` at the plan root, and read by every milestone.
- **One milestone at a time, in order.** Go no further into a milestone until every milestone it depends on is **done**. N0 before everything; N1 before N2; N2 before N3; N3 before N4 and N5; N5 before N6. N4 and N5 both sit on N3 and may be done in either order.
- **Scoped plan files.** Each milestone runs L1 to L7 over its delivered ids, writing its own files under `nhcx-plan/<Nx>/` (`discovery.json`, `mapping.json`, `plan.json`, `code-plan.json`, `code.json`, `validation.json`, `dry-run.json`). The final L8 writes one `nhcx-plan/e2e.json` at the root, not per milestone.
- **Deliver once, reuse after.** A spec is delivered by exactly one milestone; a spec two milestones reach is built by the earlier and reused (not rebuilt) by the later, which records any extension it makes (for example N5 extends N3's [F8. Claim](fhir/F8-claim.md) builder for `use: claim`).
- **Done means proven in dry-run.** A milestone is `done` only when its done-when holds in dry-run: its code is written, validated, and its dry-run tests pass with the gateway mocked and callbacks stubbed. It is never half-built into the next. The live sandbox proof is the final L8, run once across the whole lifecycle after the last milestone's dry-run is green.
- **Keep going; do not pause between milestones or between the steps inside one.** A milestone runs fully offline (dry-run needs no network and no sandbox credentials), so once a milestone's dry-run is green, go straight on to the next without stopping to ask for anything. Do not pause inside a milestone either: its steps run one after another with no confirmation gate. A large milestone (N3 above all) and elapsed time are not reasons to stop and report; the only halt before a dry-run is green is a genuine blocker that no default resolves. Sandbox credentials, a reachable public endpoint and test beneficiaries are asked for **once, at the final end-to-end step (L8)**, never after N0 or between any two milestones; the only questions before then are the one-time ASK FIRST set.

The step files say what each step does; the milestone and its delivered ids set the scope of every run. The ASK FIRST questions, the knowledge source, the scaffolding and the specs are the same for every milestone.

# SCAFFOLDING
[references/SCAFFOLDING.md](references/SCAFFOLDING.md) is the shape the code takes in the target HMIS. Read it before L3 and keep it open through L5.

- **One NHCX module** (`nhcx/`) holding `gateway/` (G, in-process), `fhir/` (F, pure builders and parsers), `services/` (A), `callbacks/` (C), `models/` and `migrations/` (D), `screens/` and `routes` (S), and the message `archive`.
- **Existing HMIS modules** change only for the fields NHCX needs: patient ABHA (D3, through the HMIS's own M1 when it has one, else verified or created through A19), practitioner HPR id and qualification (D2), facility HFR id and participant code (D1), and the "Claims" navigation entry.
- **The host's components.** Every screen is built from the HMIS's own components, the ones L1.2 records for each kind (type-ahead, select, table, chip, card, accordion, dialog, date picker, file input, flash or toast, tabs with a dot badge), so two different HMIS end with the same screens made of their own parts ([references/SCREENS.md](references/SCREENS.md), Component kit). A component is written only for a kind the host lacks, styled with the host's tokens.
- **ABHA is the patient key.** Records attached "From records" and the admission linked to a case are found by the case's ABHA number.
- **Core rule: the pre-authorisation locks behind the claim.** Once the pre-authorisation is approved and the claim has gone to the payer, the pre-authorisation is read only: no enhancement or change; only a cancellation, and only until the payer decides the claim. A change is refused with "The claim has gone to the payer, so the pre-authorisation is read only: no enhancement or change can be made. It can only be cancelled while the payer is deciding the claim.", a late cancel with "The payer has decided the claim; the pre-authorisation can no longer be cancelled." A claim refused at the door never reached the payer and leaves the pre-authorisation open.
- **A claim is never sent again once decided.** A rejected claim goes back as a reprocess (workflow 36, reasons `claimrejected` or `rejectiondisputed`); an approved or part-approved one may ask for its balance (a release).
- **Dependency rules:** screens call services and read models; only services and callbacks write claim tables; FHIR builders never touch the database or the gateway; the gateway knows nothing about claims; a reply found by polling is applied by the same callback handler.
- **Outside the repository:** the gateway config, client secret, private key, ledger and archive directories.
- **Tests** under `tests/nhcx/` (dry-run and end-to-end), and **plan files** under `nhcx-plan/`.
- **Build order** in phases, from the gateway foundation to the navigation entry; L3 plans in that order and leaves out phases whose specs are not in SCOPE.

L4 maps these placeholder names onto the target's own conventions, whatever its language, framework and module form, as L1 discovered them; the split between parts and the dependency direction do not change. No framework, ORM, router or component library is assumed by any spec.

# SCOPE
The specs this skill holds:

- **Screens** (4): [S5](screens/S5-claim-master.md), [S6](screens/S6-claim-detail.md), [S10](screens/S10-communication.md), [S19](screens/S19-nhcx-settings.md)
- **APIs** (6): [A7](apis/A7-communication-on-request.md), [A10](apis/A10-txn-related.md), [A11](apis/A11-txn-dispatch.md), [A12](apis/A12-txn-fhir.md), [A13](apis/A13-txn-list.md), [A17](apis/A17-claim-state.md)
- **Callbacks** (2): [C1](callbacks/C1-callback-door.md), [C9](callbacks/C9-communication-request.md)
- **FHIR** (10): [F1](fhir/F1-bundle.md), [F3](fhir/F3-coverage-eligibility-response.md), [F8](fhir/F8-claim.md), [F10](fhir/F10-task-claim-actions.md), [F11](fhir/F11-communicationrequest.md), [F12](fhir/F12-communication.md), [F15](fhir/F15-patient.md), [F16](fhir/F16-practitioner.md), [F17](fhir/F17-organization.md), [F18](fhir/F18-coverage.md)
- **Database** (11): [D1](database/D1-organization.md), [D2](database/D2-practitioner.md), [D3](database/D3-patient.md), [D8](database/D8-terminology.md), [D9](database/D9-claim.md), [D13](database/D13-claim-auth.md), [D15](database/D15-claim-auth-requirement.md), [D23](database/D23-claim-query.md), [D28](database/D28-claim-document.md), [D30](database/D30-counter.md), [D32](database/D32-participant.md)
- **Gateway** (11): [G1](gateway/G1-embedding.md), [G2](gateway/G2-configuration.md), [G3](gateway/G3-session-token.md), [G4](gateway/G4-registry.md), [G5](gateway/G5-protocol-headers.md), [G6](gateway/G6-encryption.md), [G7](gateway/G7-send.md), [G8](gateway/G8-receive.md), [G9](gateway/G9-ledger.md), [G10](gateway/G10-beneficiary-registry.md), [G11](gateway/G11-startup-checks.md)
- **Tests** (4): [T1](tests/T1-test-configuration.md), [T2](tests/T2-test-runners.md), [T7](tests/T7-irdai-query-answered.md), [T20](tests/T20-functional-test-report.md)

Other skills built from the same source:

- **nhcx-full**: the whole provider-side NHCX integration, every exchange end to end.
- **nhcx-coverage**: beneficiary policy search and coverage eligibility.
- **nhcx-preauth**: pre-authorisation: the payer's plan, line items quoted from it, coverage and authorisation-requirement checks, pre-auth, enhancement, cancel and status.
- **nhcx-claim**: claim submission after discharge, its verdict and status.
- **nhcx-payment**: payment notices and their acknowledgement.
- **nhcx-reprocess**: reprocess and balance release on a decided or partly paid claim.

# VERSION
This is nhcx-communication version 1.11.0, built on 2026-10-25. Its protocol tables (workflow ids, statuses, base URLs) were checked against NHA's NHCX package 1.0.0 ([github.com/nha-in/nhcx-package](https://github.com/nha-in/nhcx-package)).

- Record it when the work starts: `nhcx-plan/knowledge.json` and the `target` of `nhcx-plan/progress.json` carry `skill` and `skill_version`, and the header of `nhcx-plan/report.html` shows them.
- UPDATE FIRST may have installed a newer build from the NHCX package at the start of the prompt; the version recorded is then the old one.
- If a later prompt runs with a different version of this skill than the one recorded, say so to the user before continuing, log it as a `corrected` entry naming both versions, and re-check the steps already done against the specs that changed.
- A knowledge source newer than 1.0.0 wins on the protocol, as KNOWLEDGE SOURCE says; note the difference in `knowledge.json`.

Changes in 1.11.0, to re-check against when an earlier build is continued (each learnt from two live runs of 1.10.0 on one HMIS, 24 Oct 2026):
- **A payment's identity is no longer `PaymentNotice.id` alone** (D21. claim_payment (in nhcx-claim) rule 4, C10. Payment Notice (in nhcx-payment), F13. PaymentNotice (in nhcx-payment)): the sandbox payer sends no `PaymentNotice.id`, so the workflow-30 and workflow-31 notices of one payment landed as two rows and S12 showed an "Initiated, UTR awaited" card for good beside the cleared one. The identity is now `PaymentNotice.id`, else the payment id in the reconciliation's `detail[]` placer identifier (`<paymentId>/Payment`), else the newest `paid` row without a UTR with the same amount and date. A placeholder UTR (`Not available` and the like) stores as null.
- **C4 replaces a seeded plan** (C4. Insurance Plan Reply (in nhcx-preauth), T13. PMJAY Eligibility, Package Master and Ruling (in nhcx-coverage)): a `ready` row marked as the T13 test seed takes the payer's reply; the seed goes through C4's own apply path so every seeded document carries display and stage. A run whose C4 ignored every reply once the seed set `ready` never saw PMJAY's master.
- **Stage is stored as `pre` or `post` only** and the D11 post words gain `bill`, `hospital bill`, `lama`, `dama`, `death`, `mortality` (D11. claim_plan_benefit (in nhcx-coverage)); with a ruling held, the forms it does not name go to the claim leg whatever their titles say (D12. claim_plan_form (in nhcx-coverage)).
- **The discharge summary rides under `HDS`** whatever category it was filed under ([F8. Claim](fhir/F8-claim.md)).
- **D10 reuse no longer copies `response_json`** (29 copies of an 18 MB master made a 645 MB database).
- **A GUI run drives a browser or is `blocked`** ([T2. Test Runners](tests/T2-test-runners.md), L8): the browser driver is installed in setup without asking; artifacts are PNG screenshots; each runner opens its own claim; `e2e.json` entries carry `browser` and `plan_source`. T10 issues the admission's bill so T11 proves the D21 posting; T11 expects one card per payment and `posted`.
- **A functional test report is compiled after the run** ([T20. Functional Test Report](tests/T20-functional-test-report.md), `nhcx-e2e report`): the GUI runner screenshots the whole process (sign-in, before and after every step, every refusal, each tab at the end, and the payer's desk when a URL is given), and the builder renders a PDF in the shape of a functional-testing audit report (cover block, document control, contents, requirement tables, scope, execution details, methodology, tools, one numbered proof section per test step with its screenshot and a one-line statement, a summary) and an Excel workbook with one row per step; no company named, no credential printed. New T1 variables `NHCX_TEST_FT_*` and `NHCX_TEST_PAYER_DESK_URL`; `e2e.json` steps carry `expected` and `screenshots`.
- **L6 gains three mechanical checks** (SCAFFOLDING layout, stage vocabulary, fixtures through the handler) and **L7 four tests** (HDS on the claim, the D11 rule over the real PMJAY master, C4 over a seed, the two-notice payment). LOG.md: entries as they happen, commits checked to be on the branch. L1.A: a spec in SCOPE is never dropped by the run on its own.

Changes in 1.10.0, to re-check against when an earlier build is continued:
- The build now runs in **milestone mode only** ([milestones/INDEX.md](milestones/INDEX.md)): vertical slices of the claim lifecycle (N0 Foundation, N1 Search Policy, N2 Coverage and Insurance, N3 Pre-authorisation and Biometric, N4 Communication, N5 Claim, N6 Payment), each carried through L1 to L7 (discovery to dry-run) over only the spec ids it delivers, in dependency order, reusing not rebuilding, with its own dry-run done-when and its own plan files under `nhcx-plan/<Nx>/`. The old layered pass (every spec through one step, then the next) is gone. A build begun under an earlier build in the layered shape keeps its existing `nhcx-plan/` files, but every new step runs per milestone, and the report is rebuilt milestone by milestone. `report.html` is organised by milestone, each opening to its steps and their sub-steps.
- **End-to-end runs once, at the end, not per milestone.** A milestone stops at dry-run (L7), proving its done-when against the mocked gateway and stubbed callbacks. L8 end-to-end is lifted out of the milestone loop: it runs once after every milestone's dry-run is green, exercising the whole lifecycle N1 to N6 against the sandbox, and writes one `nhcx-plan/e2e.json` at the root. The report gains a single shared end-to-end tab after the milestones, and each milestone tab now shows seven steps, L1 to L7.

Changes in 1.9.6, to re-check against when an earlier build is continued:
- L2 mapping no longer enumerates `fields[]` column by column for a wholly-`new` table: such a table is recorded once in `tables[]`, and L5 reads its columns from the D spec. `fields[]` now carries only entries a later step acts on (a `mapped` column or element with a real target location, or a `missing`/`conflict` with a resolution). L4 code planning stops pre-listing `functions[]` for files whose layout the specs already fix (F, A, C, D, screens) and the per-file test-rule list; both are re-derived in L5/L7. These cut the slowest writing in the plan steps without removing anything L3/L4/L5/L7 read.
- The S11 discharge date picker, when its earliest and latest fall on the same day (the pre-authorisation was sent today), keeps that day selectable: the picker is never disabled or locked to read-only.

Changes in 1.9.5, to re-check against when an earlier build is continued:
- The S11 discharge date picker starts at the later of the admission date and the day the pre-authorisation was sent (D18 `submitted_at`, facility local date), and still ends at today; an earlier date is refused "The discharge date cannot be before the pre-authorisation date." (D20), checked after the admission rule.

Changes in 1.9.4, to re-check against when an earlier build is continued:
- report.html is laid out for a person (LOGH): a header with the one-line state and Refresh, a sticky tab bar with open counts, an Overview of four tiles, the eight steps side by side and the open errors as cards (ids with names, correlation and ledger ids only when present), Mapping grouped by table with every D and F reference named ("D1 Organization · name"), and on every other tab field lists, tables with pills, a filter box, empty columns left out and nested data written as text, never JSON; light and dark themes; still one self-contained file from the standard library. A report builder written by an earlier build is rewritten to this layout at the next prompt, from the CSS and script in LOGH, and run; the plan files are not touched.

Changes in 1.9.3, to re-check against when an earlier build is continued:
- S17 "In network" replaces the 1.9.2 "valid cover" rule: a payer is in network once this hospital has fetched an insurance plan from it for any patient (a D10 plan settled `ready`). D32 gains `plan_fetched_at` (set once by C4, filled by a migration from plans already fetched, never cleared by a refresh); the payers check reads it, filling it once from the fetched plans when unset, and answers `on_network` and `plan_fetched_at`. The screen shows one green-ticked line "In network: this hospital has fetched an insurance plan from <name>." or nothing.

Changes in 1.9.2, to re-check against when an earlier build is continued:
- S17 "In network": only a policy of the payer whose validation answered eligible counts; one green-ticked line "In network: this hospital holds <n> policy(s) of <name> with valid cover." when there is one, nothing at all otherwise.
- No back-dated pre-authorisation: the S4 admission date picker starts at today, and saving or sending a new pre-authorisation with an earlier date is refused "The admission date cannot be before today; a pre-authorisation is not raised back-dated." (D9, A4, S9). A date the payer already holds may stay.
- Each S4 diagnosis is marked Provisional or Final (D25 `dx_type`), sent as F8 `diagnosis.type` SNOMED CT 148006 or 89100005, as PMJAY sends it.
- The S11 discharge date picker ends at today; a later date is refused "The discharge date cannot be after today." (D20).
- The claim's decision reads "Final approval", approved in full or in part (S11, S5 at stage Claim); the pre-authorisation keeps its labels.
- Payments: initiation comes on workflow 30 as `paid` with every amount but no UTR, completion on 31 as `cleared` with the UTR, under one PaymentNotice id. Paid means `cleared`, or `paid` with a UTR; a `paid` notice without one is initiated and is never posted to the bill (F13, D21, A17, C10, S12, A8). The old "disposition contains initiat" rule is gone; S12's "Initiated, UTR awaited" chip means no UTR and a status other than `cleared`.
- S12 Shortfall is measured against the claim's approved amount, never the claimed amount: what the notices account for (per notice, its payment, TDS and deduction lines, else its amount) equal to the approved amount is no shortfall, else approved minus accounted, never below 0 (D21, D22, A17 `payment_approved`, `payment_accounted`, `payment_shortfall`). The fourth tile is "Approved" (the claim's approved amount), not "Claimed".

Changes in 1.9.1, to re-check against when an earlier build is continued:
- The NHCX settings page (S19) is a plan phase of its own (L3 phase 3, with D1, the participant master D32 and its daily refresh), always built, under the HMIS's facility settings with its own "NHCX" entry; a build that has no S19 or no participant master adds them. S19 now matches the reference: the participant code falls back to the gateway's default, the registry card registers the endpoint ("Update the registry"), the key card runs stage, register certificate, activate, retire, and a card links to the doctors and staff master. S17 and S18 are placed in phases 4 and 6. L3 checks every screen the skill lists is delivered or dropped with a reason; L8 opens S19 before any claim test.

Changes in 1.9.0, to re-check against when an earlier build is continued:
- UPDATE FIRST: every prompt starts by reading the NHCX package's skills manifest (`skills/manifest.json`) and installs the package's build when it is newer, checked against `skills/CHECKSUMS.sha256`.
- Every step, sub-step, test and spec id shown to a person carries its name (`L3 Integration Planning`, `T3 ... (CLI): pass`), from `nhcx-plan/names.json`, written at L1.2 (LOG.md, LOGN).

Changes in 1.8.0, to re-check against when an earlier build is continued:
- The steps are framework-agnostic: L1 records the host's stack and its components per kind, L4 and L5 build every screen from them, L6 refuses a duplicate component.
- An existing M1 is reused without asking; A19 and the S13 to S15 ABHA additions are dropped in L3 when it exists. Records and admissions are found by ABHA.
- `plan.trigger` defaults to automatic once the case is created (a ready plan of the same policy is reused, else requested). The line items, the benefits check and the authorisation-requirements ruling sit on the Pre-authorisation tab, and every line is quoted from the payer's insurance plan (a bare cover benefit such as Blood or Ambulance is never a line).
- Two payer adapters, `gov` and `generic`, chosen by the participant master's entity type (`pmjay` reads as `gov`, `kyrocare` as `generic`); the adapter's name is never shown.
- The insurance plan request and the status enquiry travel under workflow id `1`; a query answer travels as `request.initiated`.
- The claim tabs are Overview, Pre-authorisation, Claim, Communication, Payments and Logs (newest first, the only place correlation ids appear), with a dot beside a tab when the payer has something new; Claim and Payments appear once a pre-authorisation has been raised.
- A decided claim is never sent again: a reprocess is asked only of a rejected claim, and the balance release of an approved one stays.
- Core rule: once the claim has gone to the payer the pre-authorisation is read only (no enhancement or change), and it may be cancelled only until the payer decides the claim.

# REFERENCES
- [references/CORE.md](references/CORE.md): base URLs, and every exchange with its route, bundles, workflow id and callback, on one page.
- [references/KNOWLEDGE.md](references/KNOWLEDGE.md): the NHCX knowledge source, MCP or GitHub package, and which lookup answers which question.
- [references/SCREENS.md](references/SCREENS.md): every screen in scope, its route and what it does.
- [references/API.md](references/API.md): every API call in scope and what it does.
- [references/CALLBACK.md](references/CALLBACK.md): every NHCX callback in scope and what it does.
- [references/GATEWAY.md](references/GATEWAY.md): every part of the in-process NHCX gateway and what it does.
- [references/FHIR.md](references/FHIR.md): every FHIR resource in scope, sent or read, and what it is.
- [references/DATABASE.md](references/DATABASE.md): every table in scope, what one row is, and which screens, APIs, callbacks and FHIR resources use it.
- [references/PAYERS.md](references/PAYERS.md): the payer adapters, their workflow ids and rules, and what the [REF](references/PAYERS.md#markers), [PAYER](references/PAYERS.md#markers) and [SANDBOX](references/PAYERS.md#markers) markers mean.
- [references/OPERATIONS.md](references/OPERATIONS.md): production cutover, and running the application as more than one instance.
- [references/TESTS.md](references/TESTS.md): every end-to-end test in scope, IRDAI and PMJAY, each run through the screens and from the command line.
- [references/READSETS.md](references/READSETS.md): for each screen, API, callback and gateway part, the other specs to read before implementing it.
- [references/SCAFFOLDING.md](references/SCAFFOLDING.md): the module layout in the target, what each part holds and where each spec lands.

# OUTPUT
In the target repository:
- **Code** in the NHCX module and the changed HMIS modules, as laid out in SCAFFOLDING.
- **Tests** under `tests/nhcx/`: dry-run (L7) and end-to-end (L8), the end-to-end ones with a GUI runner and a CLI runner (`nhcx-e2e`).
- **Plan files** under `nhcx-plan/`: `knowledge.json`, `discovery.json`, `mapping.json`, `plan.json`, `code-plan.json`, `code.json`, `validation.json`, `dry-run.json`, `e2e.json`, `names.json` (the name of every id), the log `progress.json` with `progress.md`, and `report.html`, rebuilt at the end of every prompt by the report builder (`report.py` or the target language's equivalent) with its `make-report.sh` and `make-report.bat` beside it.
