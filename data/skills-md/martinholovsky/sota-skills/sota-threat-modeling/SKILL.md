---
name: sota-threat-modeling
description: >-
  State-of-the-art threat modeling for both designing new systems and auditing
  existing ones. Use when designing a feature, service, integration, or
  architecture that touches untrusted input, new trust boundaries, sensitive
  data, or third-party dependencies (BUILD mode), and when reviewing, auditing,
  or pen-test-scoping an existing codebase to reconstruct its implicit threat
  model and find gaps (AUDIT mode). Not for code-level vulnerability review —
  use sota-code-security. Trigger keywords: threat model, STRIDE,
  LINDDUN, PASTA, attack tree, kill chain, data flow diagram, DFD, trust
  boundary, attack surface, abuse case, security design review, security
  architecture review, risk rating, DREAD, CVSS, security requirements,
  secure design, security audit, gap analysis, prompt injection, excessive
  agency, threat catalog, mitigations, residual risk.
---

# SOTA Threat Modeling

## Purpose

Threat modeling answers Shostack's four questions with engineering rigor:
1. **What are we working on?** (decompose: DFD, trust boundaries, assets, actors)
2. **What can go wrong?** (enumerate: STRIDE/LINDDUN per element, catalogs, attack trees)
3. **What are we going to do about it?** (treat: mitigate/accept/transfer/avoid, map to requirements and tests)
4. **Did we do a good job?** (verify: abuse-case tests, residual risk review, re-model triggers)

This skill operationalizes those questions in two modes. Never produce a threat
model that is only prose — every threat must land as a tracked requirement, a
test, or an explicitly accepted risk with an owner.

## BUILD Mode — Threat-Model-While-Designing

Run this workflow whenever designing anything that crosses a trust boundary.
Scale effort to risk: a 15-minute "four questions" pass for a small feature; a
full STRIDE-per-interaction model for a new service or auth flow.

### Workflow

1. **Scope the delta.** Model what is new or changed, not the whole system.
   List new entry points, new data classes, new dependencies, new actors.
2. **Draw the DFD as text/mermaid** (see [`rules/02`](rules/02-decomposition.md)). Mark trust boundaries
   explicitly. If you cannot draw a boundary, you do not understand the design
   yet — stop and ask.
3. **Pick the methodology** (see [`rules/01`](rules/01-methodologies.md)): STRIDE-per-interaction by
   default; add LINDDUN if personal data flows; attack trees for a single
   high-value asset; four-questions-only for low-risk deltas — but the system's tier ([`rules/04`](rules/04-risk-rating-treatment.md) §8) sets the floor: a High-tier system gets its tier's depth even for a small delta.
4. **Enumerate threats** crossing each boundary using the per-component
   catalogs in [`rules/03`](rules/03-threat-catalogs.md). Write each threat as: *actor → action → asset →
   impact*. No vague entries ("hacking", "data breach").
5. **Rate and treat** each threat (see [`rules/04`](rules/04-risk-rating-treatment.md)): likelihood × impact matrix,
   then accept / mitigate / transfer / avoid. Every mitigation becomes a
   security requirement with an ID.
6. **Emit artifacts** (see [`rules/05`](rules/05-outputs-operationalization.md)): threat model doc, security requirements
   backlog entries, abuse cases as test stubs, and re-modeling triggers.
7. **Wire into delivery.** Reference requirement IDs in the design doc, tickets,
   and PR descriptions. A threat without a tracked artifact does not exist.

### Continuous / incremental (agile, PR reviews)

- Threat model the **story**, not the sprint. Add a "Security notes" section to
  design docs and PR descriptions for any change matching a re-model trigger:
  new dependency, new endpoint/route/queue/cron/webhook, new trust boundary,
  new data class, auth/authz change, file/deserialization handling.
- In PR review, run a micro-STRIDE on the diff and its dependents (callers and importers
  of each changed file, two hops out by default — [`sota/rules/01`](../sota/rules/01-audit-methodology.md) §1): what new input
  enters? whose privilege executes it? what does it write or call? Minutes for a small
  diff, and it catches design-level regressions a line-by-line review misses.

## AUDIT Mode — Reconstructing a Threat Model from Code

**Coverage:** every `rules/` file's Audit checklist applies in AUDIT mode. Mark one *not applicable* only with its reason in the report — never skip a file because the thing it checks for is absent, since that absence may be the finding.

Use when handed an existing system with no (trustworthy) threat model. Goal:
rebuild the implicit model from artifacts, then diff intended vs. actual
controls. Full procedure in [`rules/06`](rules/06-audit-reconstruction.md).

### Workflow

1. **Inventory entry points from code** (see [`rules/02`](rules/02-decomposition.md) §extraction): routes,
   queue consumers, cron jobs, webhooks, third-party callbacks, CLI/admin
   tools, file uploads, IaC-exposed ports.
2. **Reconstruct the DFD** from the inventory: processes, stores, external
   entities, flows; infer trust boundaries from network topology, authn
   checkpoints, and IAM policies.
3. **Identify assets and actors** from schemas, secrets handling, and config.
4. **Run the catalogs** ([`rules/03`](rules/03-threat-catalogs.md)) against each component; for every catalog
   item record: control present / absent / partial, with file:line evidence.
5. **Gap analysis**: rank absent/partial controls by exploitability ×
   blast radius; distinguish "missing control" from "missing defense-in-depth".
6. **Report findings** in the standard format below.

### Severity conventions

| Severity | Definition |
|---|---|
| Critical | Remotely exploitable now, by an unauthenticated or low-priv actor, leading to full compromise of a key asset (RCE, auth bypass, mass data exfil). Fix before anything else ships. |
| High | Exploitable with realistic preconditions (one valid account, one misconfig, MitM position) compromising a key asset; or a Critical with a single weak mitigating layer. Fix this sprint. |
| Medium | Requires chaining, elevated access, or unusual conditions; or impacts a secondary asset; or defense-in-depth gap on a Critical path. Schedule. |
| Low | Hardening, hygiene, info disclosure of low-value data, theoretical with strong existing controls. Backlog. |

Severity = exploitability × impact in **this** deployment context — never copy
a CVE/CVSS base score without environmental adjustment (see [`rules/04`](rules/04-risk-rating-treatment.md)).

### Finding format (every finding, no exceptions)

```
[SEV] TITLE (component, STRIDE/LINDDUN class)
Location: path/to/file.py:123 (and IaC/config refs)
Threat: <actor> can <action> via <vector> because <missing/weak control>,
        impacting <asset> (<C/I/A/privacy impact>).
Evidence: code excerpt or config line proving the gap.
Recommendation: specific control + where it goes; map to requirement ID.
Residual risk if accepted: one sentence.
```

## Rules Index

| File | Read this when... |
|---|---|
| [`rules/01-methodologies.md`](rules/01-methodologies.md) | Choosing between STRIDE, LINDDUN, PASTA, attack trees, kill chains; deciding lightweight vs. heavyweight; setting up continuous/PR-level threat modeling. |
| [`rules/02-decomposition.md`](rules/02-decomposition.md) | Drawing DFDs in mermaid, defining trust boundaries, listing entry points/assets/actors/privilege levels; extracting all of these from an existing codebase. |
| [`rules/03-threat-catalogs.md`](rules/03-threat-catalogs.md) | Enumerating threats for a specific component: web frontend, API, database, message queue, file storage, CI/CD, mobile, LLM agent/tool-use, cloud/IAM. |
| [`rules/04-risk-rating-treatment.md`](rules/04-risk-rating-treatment.md) | Rating threats (DREAD pitfalls, CVSS usage, L×I matrices), choosing accept/mitigate/transfer/avoid, mapping mitigations to requirements and tests, documenting residual risk, tiering applications and modules to set modeling and review depth. |
| [`rules/05-outputs-operationalization.md`](rules/05-outputs-operationalization.md) | Writing the threat model document, building the security requirements backlog, turning abuse cases into tests, keeping the model alive (re-model triggers), the PR security-notes template. |
| [`rules/06-audit-reconstruction.md`](rules/06-audit-reconstruction.md) | Auditing an existing system: reconstructing the model from code, control-presence matrix, gap analysis, severity calibration, reporting. |

Load only the files you need; [`rules/02`](rules/02-decomposition.md) + [`rules/03`](rules/03-threat-catalogs.md) cover 80% of day-to-day work.

## Top-10 Non-Negotiables

1. **No model without a diagram.** Every threat model includes a DFD (mermaid
   or ASCII) with explicit trust boundaries. Prose-only models hide boundary
   confusion.
2. **Threats are sentences, not nouns.** *Actor → action → asset → impact.*
   "SQL injection" is a vector; "anonymous user exfiltrates the orders table
   via unparameterized search query" is a threat.
3. **Every entry point gets enumerated** — including queues, cron, webhooks,
   callbacks, admin tooling, and CI/CD. HTTP routes are never the whole attack
   surface.
4. **Trust boundary crossings drive enumeration.** Apply STRIDE per
   interaction at each crossing; data inside one boundary at one privilege
   level rarely needs the full treatment.
5. **Personal data ⇒ LINDDUN pass.** STRIDE does not cover linkability,
   identifiability, or non-compliance; run a privacy pass whenever PII flows
   or is stored.
6. **Rate with likelihood × impact in context.** Never ship raw DREAD scores
   or unadjusted CVSS base scores as priorities.
7. **Every threat gets a disposition.** Mitigate (→ requirement ID + test),
   accept (→ named owner + expiry date), transfer, or avoid. "Noted" is not a
   disposition.
8. **Mitigations become tests.** Each mitigated threat yields at least one
   abuse-case test (unit, integration, or rule-based check) that fails if the
   control regresses.
9. **LLM/agent components are first-class attack surface.** Model prompt
   injection, tool-call abuse, excessive agency, and data exfil via outputs
   for any system invoking an LLM with tools or retrieved content.
10. **Models expire.** Define re-model triggers in the document itself — at least the canonical
    list in [`rules/05`](rules/05-outputs-operationalization.md) §4 (e.g. new dependency, trust boundary, data class, auth change); an undated,
    trigger-less threat model is treated as absent in audits.
