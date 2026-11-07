---
name: validate-plan
description: Adversarially validate plans, specs, RFCs, architecture proposals, migration designs, and other design documents. Use when asked to stress-test assumptions, test a plan against official docs or code evidence, identify design risks, or edit a plan so that a wrong assumption fails visibly instead of silently.
license: Apache-2.0
compatibility: Requires read access to the target document and repository context. Benefits from web/MCP access such as Exa, Context7, Ref, or direct documentation fetches, especially for vendor APIs and current platform behavior.
metadata:
  author: jope35
  version: "1.1.0"
---

# Validate Plan

Find the claims in a plan that are most likely to break. Edit the plan so that a wrong claim causes a visible failure. The edited document is the output. The chat gets a status line, not a report.

Validation means a test of a claim against evidence. It is not an approval step.

## When to use

- The user asks to validate, review, stress-test, challenge, or de-risk a plan or spec.
- The design depends on external systems, SDKs, cloud services, APIs, compliance rules, scaling, or operations.
- The document contains implementation steps, architecture, rollout, data model changes, security claims, or dependency assumptions.
- The user wants a stronger plan, not a summary.

Do not use this skill for code review, unless the review covers a written design or rollout plan.

## Output contract

The edited document is the output. The chat gets a short status.

1. Apply the changes to the document in place.
2. Reply in the chat with the four-line status below.
3. Write a full report only when the user asks for one. Save it next to the document as `<name>.validation.md`.
4. When the document cannot be edited, write the report file and name its path in the chat.
5. Do not paste the change set, the assumption ledger, the evidence, or the diff into the chat.

Reply template:

```
Verdict: <accept with minor changes | revise before implementation | rework required>
Edited: <path> (<total> changes: <critical> critical, <high> high, <medium> medium)
Top risk: <one clause>. Missing evidence: <n>.
Action: <what the user must do next, or none>
```

Send one line per field and nothing else. Keep the reply under 50 words. Do not add a preamble, a summary of the plan, or the list of changes.

In the second line, count one change for each finding that you fixed. In the third line, n counts the assumptions that you cannot test.

## Report file

Write this file when the user asks for the report, or when the document is read-only. It contains:

1. The verdict and the dominant risks.
2. The change set. For each change, give the location and the exact new text. Add the reason, the evidence, the test that proves the change, and the severity.
3. The assumption ledger: assumption, status, evidence, risk if wrong, plan update.
4. Missing evidence: the sources that were unavailable, the affected assumptions, and whether the gap blocks the work.
5. Open questions that block confidence.
6. Additions that no single failed assumption covers.

Severity levels:

- Critical blocks the launch.
- High needs a fix before implementation starts.
- Medium needs a fix before rollout.
- Low is cleanup.

## Evidence sources and tool mapping

Use the best evidence in the current harness. Map these intents to local tools:

| Intent | Preferred sources |
|--------|-------------------|
| Test repository-specific behavior | Source search, tests, schemas, configuration, migrations, existing docs, git history |
| Test library or framework APIs | Context7, Ref, official docs, typed definitions, release notes |
| Test current vendor or platform behavior | Exa search and fetch, official docs, product release notes, API references |
| Test a specific URL | Fetch the URL, then follow the relevant official links |
| Test an `llms.txt` documentation site | Fetch `/llms.txt`, use it as the docs index, then fetch the linked pages that match the assumption |
| Test standards or protocols | Standards documents, official specs, maintainers' references |

## External documentation discipline

Before you test an external claim, find the documentation and research tools in the current harness. Use any MCP or fetcher that fits, such as Exa, Context7, Ref, a URL fetch, or a vendor docs tool.

- Use Context7, Ref, typed definitions, or official API references for library behavior.
- Use Exa, a direct fetch, official product docs, release notes, and `llms.txt` indexes for current platform behavior.
- Match the docs to the version, cloud, region, deployment model, and product tier in the plan.
- When a tool, URL, or source is unavailable, blocked, or inconclusive, mark the affected assumption as an evidence gap. Do not skip it.
- Fetch the full page for a claim that decides a finding. A search snippet is a lead, not evidence.

## `llms.txt` workflow

When a plan depends on docs on a known domain, try the LLM-friendly index first:

1. Derive the docs origin from the plan, for example `https://docs.databricks.com`.
2. Fetch `https://<docs-host>/llms.txt`.
3. Treat the result as an index. Select the links that match the assumption.
4. Fetch the most relevant pages. Prefer the markdown variant when the site offers one.
5. Cite the exact page, the section, and the claim that it proves or disproves.
6. If `/llms.txt` is missing or incomplete, fall back to official docs search, Context7, Ref, Exa, or a known URL.

Use official docs before blogs, generated summaries, forum posts, or marketing pages. For a high-risk claim, find two independent official sources when you can.

## Workflow

### 1. Identify the target and the scope

Find the document. When several documents apply, start with the highest-level plan and read the supporting documents that you need. Note these items:

- The path or title.
- The intended outcome.
- The systems and teams touched.
- The versions, environments, vendors, APIs, and deployment targets.
- The constraints that the author assumes: time, compatibility, cost, latency, permissions, compliance.

When the target is missing or ambiguous, ask for it before you start.

### 2. List the assumptions

Read the document and write each assumption, explicit or implicit, in a ledger. Group the entries by type:

- API and platform: operations, version behavior, quotas, lifecycle, deprecations.
- Data: schemas, volume, quality, retention, ordering, idempotency, consistency.
- Architecture: boundaries, ownership, coupling, extension points, compatibility.
- Security and compliance: auth, permissions, secrets, isolation, audit, data residency.
- Operations: deploy, rollback, monitoring, alerting, incident response, support load.
- Migration: backfill, dual writes, compatibility windows, reversibility, flags.
- Performance and cost: latency, throughput, capacity, caching, billing, limits.
- Product behavior: workflows, adoption, failure modes, edge cases.

Order the ledger by blast radius and uncertainty. Blast radius is the impact if the assumption fails. Test the riskiest claims first. Continue after you find the first problem.

### 3. Gather evidence against the plan

For each high-risk or medium-risk assumption:

1. Search the source, tests, schemas, and docs for an existing contract or a contradiction.
2. Use Context7, Ref, Exa, vendor docs, or an `llms.txt` index to test an external claim.
3. Make sure that the evidence matches the version in the plan.
4. Look for hard limits: unsupported operations, quotas, consistency rules, auth requirements, regional availability, pricing, deprecations, migration limits.
5. Record whether the evidence supports, weakens, breaks, or ignores the assumption.
6. Keep the evidence gaps in a separate list.

Read the full page or source file when a snippet decides a finding.

### 4. Attack the design

Ask these questions about the plan:

- What must be true for the plan to work, and where is that unproven?
- Which dependency breaks the design when the vendor or the API behaves differently?
- Which step is irreversible, hard to roll back, or unsafe after a partial failure?
- What happens on a retry, a duplicate event, out-of-order data, a stale cache, a timeout, a rate limit, or a regional outage?
- What data can be lost, leaked, corrupted, processed twice, or made inconsistent?
- Which security boundary, permission model, or audit rule is underspecified?
- Which signal shows that the rollout is failing before a user reports it?
- Which invariant must you test on every run?
- Which section will mislead the implementer or the reviewer?

### 5. Turn findings into edits

Each significant finding becomes one or more edits:

- Replace a wrong assumption with text that the evidence supports.
- Add a missing constraint, version requirement, or compatibility note.
- Add a preflight test, a proof of concept, or a spike question (a time-boxed investigation).
- Add a rollout gate, a feature flag, a rollback step, or a kill switch.
- Add a migration safeguard, an idempotency rule, a replay plan, or a query that proves the data.
- Add observability: metrics, logs, traces, dashboards, alerts, SLOs, thresholds.
- Add a security or compliance control, and name the owner.
- Add tests: unit, integration, contract, migration, load, failure, permission, end-to-end.

Keep each edit small:

- Insert a missing invariant, test, gate, or version limit. Do not rewrite a whole section.
- Keep the intent and the terms of the author when they are sound.
- Merge edits only when they cover the same failure.
- Do not add a safeguard without a risk, an owner, and a way to test it.
- When the design needs a rework, give the smallest rework that the evidence supports, and the reason.

### 6. Add the verification section

The plan must have a section named "Verification and validation", "Testing and validation", or an equivalent heading. Add it when it is missing. Make sure that the section can prove the plan works.

That section answers "How do we test this?" with concrete steps:

- Success criteria: the observable result that means done.
- Automated tests: unit, integration, contract, migration, end-to-end, permission, regression, performance.
- Manual tests: realistic scenarios, edge cases, operator workflows, negative cases.
- Data tests: before and after counts, reconciliation queries, invariants, sampling, backfill, idempotency, loss detection.
- Operations tests: metrics, logs, traces, dashboards, alerts, synthetic probes, load tests, failure injection, rollback drills.
- Security tests: authorization, audit logs, secret handling, data residency, privacy review, abuse cases.
- Rollout gates: preflight, canary criteria, flag checks, hold points, abort thresholds, rollback proof.
- Ownership: who runs each test, where the result goes, and which failure blocks the launch.

Scope the section to the output of the plan, not to general quality wishes.

## Finding statuses

| Status | Meaning |
| --- | --- |
| Verified | The evidence supports the assumption as written. |
| Nullified | The evidence contradicts the assumption. |
| Overbroad | The assumption is true only under narrower conditions. |
| Underspecified | The assumption can be true, but the plan omits required details. |
| Unsupported | No sufficient evidence. |
| Conflicting evidence | Credible sources disagree, or the version context is unclear. |
| Out of scope | The assumption does not affect the requested validation. |

## Citation rules

- Cite local evidence with a path and a line number.
- Cite external evidence with the URL, the page title or section, and the claim that it supports.
- When a tool is unavailable, name the evidence that you cannot test. Mark the assumption as Unsupported or Conflicting evidence.
- Do not cite a search snippet as final evidence when the full page is available.

## Pre-completion checklist

- [ ] The target document and the scope are clear.
- [ ] The ledger lists the explicit and implicit assumptions.
- [ ] High-risk assumptions are tested against the source or official docs.
- [ ] The evidence matches the version in the plan.
- [ ] You tried an `llms.txt` index for each relevant docs site.
- [ ] Blocked or unavailable sources appear as evidence gaps.
- [ ] The findings separate verified, nullified, unsupported, and underspecified assumptions.
- [ ] The document contains the edits, not only the findings.
- [ ] Each edit is small and keeps the sound intent of the plan.
- [ ] The plan has a verification section that proves that its output works.
- [ ] The chat reply is the four-field status and nothing else.
- [ ] A report file exists only when the user asked for one.
