---
name: akcli-deep-review
description: >-
  Generate LLM design-review candidates and gate them through `akcli review
  validate` — the agent-proposes / akcli-verifies contract. Use this skill
  whenever the task involves: a deep or exhaustive design review beyond the
  deterministic detectors; producing review observations from reading
  datasheets or design intent; running `review validate` on candidate
  findings; or presenting accepted vs quarantined LLM findings honestly.
  Triggers on: deep review, LLM review, candidate findings, review validate,
  quarantine, 深度審查, design intent review, second-opinion review,
  exhaustive review.
---

# akcli-deep-review — you propose, akcli verifies

The deterministic detectors have breadth (44 rules); you have depth — you
can read datasheets, understand design intent, and spot problems no topology
pattern expresses. The contract that keeps that power honest: **every claim
you make goes through `akcli review validate` before anyone calls it a
finding.** Four gates (schema, anchor existence, datasheet evidence,
deterministic-rule masquerade); failures land in `quarantined[]` with
reasons. Accepted candidates are `llm_reviewed` **observations** — they
never block a release, never override a deterministic finding, never
auto-create a contract.

## Candidate discipline (the four gates, from your side)

1. **Anchor everything (G2).** Every candidate carries `anchors` naming real
   entities: `{"kind": "component", "id": "U3"}`, `{"kind": "net", "id":
   "VBUS"}`, `{"kind": "pin", "id": "U3.7"}`. Check they exist first
   (`akcli component board.kicad_sch U3`, `akcli net board.kicad_sch VBUS`)
   — a ghost anchor quarantines the whole candidate. An observation you
   cannot anchor is not a finding; drop it or ask the user.
2. **Own namespace, own humility (G1, G4).** Codes are
   `REVIEW_LLM_<TOPIC>` — never a registered deterministic code (that is
   masquerade and gets quarantined). Do not set `confidence` (the gate stamps
   `llm_reviewed`) and do not pre-set `status`.
3. **Datasheet claims cite the store (G3).** If a candidate leans on a
   datasheet number, its `evidence.datasheet` must carry the sha256+page of a
   PDF **already in the facts store** (extract first — akcli-datasheet-facts
   skill). A quote is text-matched against that page when `pdftotext` is
   installed. No store entry → the claim is unverifiable → quarantined.
4. **Severity is a proposal.** Use the same info/note/warning/error ladder,
   but expect the human reviewer to re-rank — you are one voice, not the
   gate.

## Workflow

### Step 1 — Run the deterministic engine first

```bash
akcli review analyze board.kicad_sch --profile deep --out review.findings.json
```

Read what the detectors already cover (and their `detectors_skipped` list).
Your candidates must ADD something: design intent, datasheet subtleties,
cross-domain reasoning, "this topology is legal but why would you" — not
restatements of deterministic findings.

### Step 2 — Investigate with evidence

Use `akcli read --md`, `akcli component`, `akcli net`, `akcli review tree`,
and the facts store (`akcli review facts lookup MPN`) to ground each
suspicion. If a claim needs a datasheet number that is not in the store yet,
extract it first (akcli-datasheet-facts) — that both strengthens your
candidate and upgrades the deterministic findings.

### Step 3 — Write candidates.json

```json
{"candidates": [
  {"code": "REVIEW_LLM_BOOTSTRAP_RACE", "severity": "warning",
   "message": "U3 EN rises with VIN but the datasheet requires VIN stable 1ms before EN (p.11); RC on EN suggested",
   "refs": ["U3"],
   "anchors": [{"kind": "component", "id": "U3"}, {"kind": "pin", "id": "U3.4"}],
   "evidence": {"source": "datasheet",
                 "datasheet": {"sha256": "<from the facts store>", "page": 11,
                                "quote": "EN must not be asserted before VIN is stable"}},
   "remediation": "add an RC delay on EN or sequence from the PMIC"}
]}
```

### Step 4 — Gate it

```bash
akcli review validate candidates.json board.kicad_sch --facts datasheets --out validated.json
```

Exit is always 0 — acceptance is not the point; the split is. Accepted
findings come back stamped `llm_reviewed`/`reported` with computed
fingerprints in a standard findings envelope (renderable via
`akcli review report validated.json --format markdown`).

### Step 5 — Present the split honestly

- Report accepted candidates as **observations**, clearly labelled
  `llm_reviewed`, alongside (never mixed into) the deterministic findings.
- Report the quarantine list WITH its reasons. A quarantined candidate is
  not a finding and must not be narrated as one — if you believe it matters,
  fix the candidate (real anchor, store-backed evidence) and re-validate,
  or file it as a Question for the human.
- Never resubmit a quarantined candidate unchanged, and never "fix" it by
  weakening the claim's anchors to whatever passes — fix the evidence.

## When NOT to use this skill

- The standard severity-ranked review protocol → akcli-schematic-review
  (this skill supplements its Step 2, never replaces it).
- Extracting datasheet numbers → akcli-datasheet-facts.
- Anything that writes to the schematic — deep review is read-only; fixes go
  through `review propose` → akcli-schematic-authoring.
