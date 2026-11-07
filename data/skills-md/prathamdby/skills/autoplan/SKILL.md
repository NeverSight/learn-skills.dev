---
name: autoplan
description: >
  autoplan to produce a grounded implementation plan without questions; gated design uses upfront-design.
---

# Autoplan

Analysis only. Deliver one plan in thread, or at the caller's named path.

## Options and triage

Default: current repo, standard depth, thread output. Quick/sketch uses Shape
and Risks with always-on lenses. Thorough/risky/migration uses deep, winning
over quick; a named area scopes evidence. Resolve conflicting scope narrowly
and record both readings under Assumptions; never ask.

Before evidence, `BLOCKED` if no groundable verb/object/area, a non-repo intent
has no plannable target, or building rather than planning was requested.
Name the missing piece and one workable example; emit no lenses/map/milestones
on refusal. A build request does not authorize product edits by this skill.

Trivial means one module, no contract/data/signature change, and one-sentence
behavior. Return `DIRECT` plus that sentence and three lines: shape, files,
first step; no lenses. Otherwise record `intent | scope | depth | terminal`.
Done when triage has a terminal or a grounded target.

## 1. Evidence

Check whether the requested contract already exists; harden an existing match,
not rebuild it. Locate sibling recon's installed `SKILL.md` to resolve its
anchor and shared/legacy memory rules. Read a repository-verified snapshot
whose head resolves; do not invoke a refresh merely to read it. Without usable
memory, cold-scan at most three anchors for each of at most 30 manifest modules.
Missing recon is not an evidence dependency: use that bounded scan instead.

Scan ADR trees (`docs/adr/`, `adr/`, `doc/adr/`, `docs/decisions/`) silently
when absent. Note TODOs, recent reverts, and duplication. Dirty content is an
Assumptions overlay, not proof of existing contracts. Every later claim cites
a path/test/ADR, a scoped no-match result, or an explicit missing-evidence
Assumption; cite inherited patterns. Done when material claims have provenance.

## 2. Lenses

Apply all always-on probes in `REFERENCE.md`: contracts/API, failure/rollback,
longevity/debt. For a leaf, playbook, or matcher, also apply
`references/router-contracts.md`.

Score every probe for each activated lens, turning a hit into a cited risk
owned by a plan step; close each lens pass with cite, risk → step, or no evidence.
Deep activates all. Otherwise load only triggered lenses:
- Schema/backfill, stored artifacts, toolchain: `references/data.md`.
- External consumers/stored payloads: `references/compatibility.md`.
- Auth/secrets/PII/untrusted input: `references/security.md`.
- Hot paths/cost-bearing calls: `references/cost.md`.
- Services/deployment/paging: `references/operations.md`.
State one skip line per inactive lens. Done when every active probe is scored
and each risk has an owner.

## 3. Plan

Specify decisions, changed contracts, constraints, and deviations from cited
patterns, not implementation bodies or restatements. Standard/deep includes:
Assumptions; Shape (bold sentence + pattern); Layer map (NEW/CHANGED roles);
phase sequence; file-plus-symbol grounding (prose: file + contract step);
worst-first Risks (probability × impact, or stated judgment); Milestones;
non-goals; Handoff. Sketch includes only Shape and Risks.

Small work is one PR; otherwise each milestone is a reviewable vertical PR.
Begin with the thinnest end-to-end contract/check slice. Name landed symbols,
expected success and relevant failure outcomes, and assertions or observed
manual results proving them. Exit zero alone is not proof.
Handoff follows the caller's next route; default `/peer-review`, then `ship`.
When nothing will be built, such as a docs-only plan, use `/peer-review` or
stop. Preserve an explicit caller route.
Done with `PLANNED` when behavior is grounded or assumed, risks are owned,
and every milestone has outcome-linked checks.

Terminals: `PLANNED`, `DIRECT`, `BLOCKED`.
