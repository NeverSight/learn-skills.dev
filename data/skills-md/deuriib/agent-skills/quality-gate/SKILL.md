---
name: quality-gate
description: Orchestrate domain reviewers and produce a consolidated Quality Gate Report. Use when implementation is ready for review, or when c-levels plus CEO must waive a gate. Triggered by "run quality gate" or "gate SPEC-XXX", after execute-spec completes.
---

# Quality-Gate — Domain Review Orchestrator

> *"Haces las cosas como para Dios, por eso trabajas con excelencia y dedicación."*

## 1. Purpose

Route a completed spec to the correct reviewers per touched domain, collect
verdicts into one gate report, and enforce "no handoff until all reviewers
sign". Reuses existing reviewers — creates none except the data dupla.

## 2. Chain Contract

- Previous: execute-spec
- Next: verify-handoff (only on OPEN gate)

```text
execute-spec → quality-gate → verify-handoff → ship-release
                     ↑ (c-levels + CEO waive only, via waiver record)
```

## 2b. Role Binding (Org)

- **Bound to:** owning C-level as gate keeper (`vasquez` for engineering, else
  the domain owner); `montilla` synthesizes multi-domain gates.
- Reviewers are always `mode: subagent` and never approve their own work.

## 3. Reviewer Routing Table

| Domain | Reviewers (actual agent names) |
|--------|--------------------------------|
| engineering | review-readability, review-reliability, review-refuter, review-resilience, review-risk, qa, review-data (data specs) |
| security | security-reviewer |
| finance | finance-reviewer |
| legal | legal-reviewer |
| brand/marketing | brand-reviewer |
| people | people-reviewer |
| revenue | revenue-reviewer |
| data | review-data + data-engineer lineage check |

A spec spanning multiple domains needs ALL touched-domain reviewers to sign.

## 4. Process

1. Identify touched domains from spec tags/requirements.
2. Dispatch each required reviewer as subagent (reference-only packet).
3. Each reviewer writes `specs/40_workspace/quality-gate/<spec-id>/<reviewer>.md`.
4. Consolidate into `GATE_REPORT.md` via `references/gate-report.md`.
5. Any ❌ → gate CLOSED. Any ⚠️ → CONDITIONAL (conditions must clear).
6. All ✅ → gate OPEN → hand off to `verify-handoff`.
7. Waivers only by c-levels + CEO via `references/waiver-template.md`.

## 5. What I won't do

- Open a gate with any ❌ verdict (only c-levels + CEO waive).
- Allow handoff with unverified conditions.
- Skip reviewers for a touched domain or override a verdict myself.

## 6. References

- `references/gate-report.md` — Consolidated verdicts + conditions.
- `references/waiver-template.md` — C-levels + CEO override record.
- `references/engineering/` — readability, reliability, refuter, resilience, qa checklists.
- `references/domains/` — finance, legal, marketing, people, security, data, ops checklists.
