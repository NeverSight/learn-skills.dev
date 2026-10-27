---
name: converge-reviews
description: Reconcile repeated code-review rounds against one scope and findings ledger. Use after any review round, or when review findings keep generating more review work.
---

# Converge reviews

I reuse valid review evidence, invalidate only changed coverage, and stop a stable scope after three review/fix rounds. I find this cap is what breaks the loop. Without it, every round finds something new to say about unchanged code and the review never lands. This skill coordinates review state. It does not review code, apply fixes, or create external issues.

## 1. Accept one review packet

I require all of these before I start.

- Originating request or ticket.
- Review base and current head, or the equivalent local baseline.
- Exact scope paths and current content/diff hash.
- Reviewer roster and lenses.
- Findings with stable IDs, severity, source reviewer, evidence, and disposition.
- Any prior convergence ledger.

When the caller already owns richer finding state, I reference its artifact and finding IDs instead of copying finding bodies. The `review-pr` finding-state file remains authoritative for PR finding status.

**Gate.** Every reviewer is accounted for and every finding is traceable to one scope, reviewer, and disposition.

## 2. Identify scope and coverage

A stable scope is the canonical hash of the originating request, review baseline, sorted paths, reviewer roster, and lenses. I record the current content/diff hash as the reviewed snapshot and on each coverage entry.

I keep convergence state in the caller existing authorized review artifact. When none exists and the workflow is authorized to maintain local review state, I use `.claude/review-state/local-<scope-id>.yml` and keep that directory ignored. Otherwise I render the block inline without creating a file. I store only this.

```yaml
convergence:
  scope_id: <stable ID>
  origin: <request or ticket>
  baseline: <base SHA or local baseline>
  snapshot: <head and content/diff hash>
  paths: [<reviewed paths>]
  reviewers: [<reviewer and lens>]
  round: <1..3>
  coverage: [<path or component, lens, reviewed hash, source round>]
  findings: [<finding ID, severity, normalized_status, disposition, source>]
  closure_check: not-needed | available | passed | failed
  result: continue | converged | blocked-at-cap | follow-up-proposed
  next_action: <exact next action>
```

The same snapshot and contract reuses the recorded result without incrementing the round. Fixes for recorded findings advance the same scope. A new requirement, new review lens, or materially new component creates a child scope at round 1. It inherits active blockers on unchanged parent coverage and cannot reset a capped parent. Cosmetic, generated, and unrelated changes neither reset the round nor invalidate coverage.

I invalidate only coverage whose reviewed content, path, or lens changed. I keep unaffected reviewer evidence until its covered content changes.

**Gate.** Each coverage entry is either reused with a matching hash and contract or marked for re-review.

## 3. Reconcile the round

I merge findings by stable ID. I preserve source reviewers and disposition history. The caller finding status remains authoritative. I derive `normalized_status` at reconciliation time without writing it back as caller status. Map `active`, `regression`, and caller-specific open states to `open`; `resolved`, `dismissed`, and `wontfix` to `closed`; and `follow-up` to `deferred` outside the current scope.

I count one round only after the planned roster returned or was explicitly recorded unavailable and the caller reconciled every finding. I record fixes, dismissals, regressions, and newly invalidated coverage before selecting the result.

**Gate.** The ledger explains what changed since the prior round and why every prior finding or coverage entry remains valid, changed, or closed.

## 4. Return one result

- `continue`: fewer than three rounds are complete and the exact next fix or affected-coverage review is named.
- `converged`: no Critical or Serious finding is open, no worthwhile Moderate or Minor follow-up remains, and all required coverage is current.
- `blocked-at-cap`: round three is complete and at least one Critical or Serious finding remains open. Stop review churn and name the exact blocker fix. After that fix, allow one targeted closure check over those blocker IDs and changed sites; it updates coverage and dispositions but performs no new-finding sweep and does not count as round four. If the check fails, remain blocked pending an explicit new plan or scope decision.
- `follow-up-proposed`: no Critical or Serious finding is open, and worthwhile Moderate or Minor findings are listed as proposed follow-up work. Keep the proposal local until the user approves external issue creation; then invoke `preflight-mutations` before creating issues.

Round three is a hard cap for the stable scope. I treat reworded findings, another reviewer over unchanged coverage, or a cosmetic diff as more of the same round, never round four. The one targeted blocker closure check exists only to verify named fixes. It cannot widen coverage or emit fresh findings.

The caller applies this contract. It reruns affected review coverage only for `continue`, proceeds for `converged`, stops for `blocked-at-cap`, and presents the proposal and approval boundary for `follow-up-proposed`. After a named blocker fix at the cap, `closure_check: available` is the dispatch signal for the one targeted check. The caller passes only those blocker IDs and changed sites, leaves `round` unchanged, and rejects any new-finding sweep.

**Done.** The ledger is current, unchanged evidence was reused, affected coverage is explicit, the stable-scope round is at most three, and the caller received exactly one result and next action.
