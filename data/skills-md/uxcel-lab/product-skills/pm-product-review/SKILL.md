---
name: pm-product-review
description: Orchestrated review of a PM artifact (spec, PRD, OKRs, roadmap, prioritization, strategy). Routes by artifact type to the right audits, auto-runs the always-relevant assumption check, and returns one prioritized report. Trigger when the user asks for a full review of a PM document, "review my spec/roadmap/OKRs", "is this PRD solid", or general PM feedback — but NOT when they name a single specific audit.
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Product Review (PM Orchestrator) Skill

## How this skill behaves (read first)

This is the **front door for holistic PM-artifact review**. It is the executable form of
`docs/orchestration-policy.md` applied to PM work: it routes by **artifact type** to the
relevant audits rather than firing all of them, auto-runs the one always-relevant lens
(assumption rigor), and returns **one** prioritized report.

PM work has no "design system" suppression case, but it has the same two failures to avoid:
a vague "looks good" review, and forcing every PM audit onto a document that only needs one.

**When NOT to use this skill:** if the user named a specific audit ("run spec-quality",
"check my OKR metric validity"), skip this orchestrator and invoke that one directly.
Explicit scope overrides orchestration.

---

## Step 0 — Establish context (once)

- **Artifact type** — spec/PRD, OKRs/KPIs, roadmap, prioritization, vision/strategy, GTM.
  This is the primary router. Infer it from the document; ask only if genuinely ambiguous.
- **Primary goal** — what decision this artifact is meant to support (used for conflict
  resolution and prioritization).

---

## Step 1 — Auto-run the always-relevant lens (Tier A)

- **`pm-assumption-rigor-audit`** — runs whenever the artifact rests on unproven assumptions,
  which is nearly always true for PM work. It's cheap, high-leverage, and artifact-agnostic.

> Each audit is named by its installable skill `name`. Invoke one only if that skill is
> installed; if one isn't, list it under "available but not run" in the report and don't
> block — this orchestrator degrades to whichever audits are present.

---

## Step 2 — Route by artifact type (Tier B — run the matching one, offer adjacent ones)

| Artifact | Primary audit | Adjacent lenses to offer |
|---|---|---|
| Spec / PRD | `pm-spec-quality-audit` | `pm-assumption-rigor-audit` (auto), `pm-decision-quality-audit` |
| OKRs / KPIs / metrics | `pm-okr-metric-validity-audit` | `pm-assumption-rigor-audit` (auto) |
| Roadmap / prioritization | `pm-prioritization-rigor-audit` | `pm-decision-quality-audit`, `pm-assumption-rigor-audit` (auto) |
| Vision / strategy | `pm-decision-quality-audit` | `pm-assumption-rigor-audit` (auto) |
| GTM plan | `pm-decision-quality-audit` | `pm-assumption-rigor-audit` (auto) |

Run the **primary** audit for the artifact type. **Offer** the adjacent lenses rather than
firing them: *"This is a roadmap, so I ran prioritization-rigor and the assumption check.
Want me to also run a decision-quality pass?"*

---

## Step 3 — Merge into one prioritized report

De-duplicate across lenses, resolve conflicts toward the primary goal from Step 0, and output
a single severity-ordered list:

```
## Product Review — [artifact]
Context: [artifact type · primary goal]
Lenses run: [spec-quality, assumption-rigor]   Available but not run: [decision-quality]

### Critical
- [Issue] — what's wrong → fix. (spec-quality / assumption / metric-validity / …)
### Major
- …
### Minor
- …
### Working well ✓
- …

**Top 3 priorities:** the highest-impact fixes across all lenses.
Offered, not run: decision-quality — say the word and I'll add it.
```

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Run every PM audit on any document | Route by artifact type; auto-run only the assumption check |
| Return one report per audit | Merge into a single prioritized, de-duplicated list |
| Run this orchestrator when the user asked for one named audit | Defer to that audit directly (explicit scope wins) |
| Treat strategy and a spec the same way | Route: spec → spec-quality, OKRs → metric-validity, roadmap → prioritization-rigor |

---

## Relationship to the policy

This skill *is* `docs/orchestration-policy.md` in executable form for PM work. If the two ever
diverge, the policy governs; update this skill to match it.

## Source lessons (Uxcel)

This is an orchestrator — its substance lives in the audits it routes to. See the source
lessons in each: `pm-assumption-rigor-audit`, `pm-spec-quality-audit`,
`pm-okr-metric-validity-audit`, `pm-prioritization-rigor-audit`,
`pm-decision-quality-audit`.
