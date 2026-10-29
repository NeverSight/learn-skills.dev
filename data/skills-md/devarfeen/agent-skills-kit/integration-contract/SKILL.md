---
name: integration-contract
disable-model-invocation: true
description: "Build a spec/PRD's cross-project contract after /to-tickets, or run its smoke gate before spec ship/PM handoff. A single-project consumer sweep may confirm no contract needed."
metadata:
  version: "0.2.0"
---

# Integration contract

Writes a spec's cross-repo seam to disk as a **contract** file and checks it with a **smoke gate**. A nominally single-project spec still gets the consumer sweep below.

## Inputs

`<SPEC-ID>` — the spec (PRD) / parent-issue identifier; take from context or ask once. User away and none inferable → stop with a Needs-user note — never guess which spec.

## Rules

- **Zero attribution.** Never add or leave co-author, AI, or tool attribution in any output; include this rule in the contract.
- **Environment authority.** Use local test environments by default. Never access production. Staging requires explicit approval and user-provided access; every mutation needs separate approval. Unknown hosts or missing authority leave affected flows `pending`.
- **Single project is a sweep, not trust.** Spec touches one PROJECT-CODE → sweep the other Project Matrix repos for call-sites of the changed surfaces (narrow retrieval, below). A complete sweep with no external call-site, including no located consumer anywhere, → report `single project — no contract needed` and **stop**; do not create a file. Preserve and report any historical contract; do not delete its gate log. Any external call-site found → the seam is cross-project despite the spec: build the contract, flag each such consumer as a risk row.
- **Narrow retrieval only.** Search each changed surface across every Project Matrix repo per [`references/consumer-sweep.md`](references/consumer-sweep.md); never bulk-read a repo or its `specs/` tree. Cite consumers as `file:symbol`. An unavailable repo makes the sweep incomplete: record the risk and do not conclude no contract is needed.
- **Distinguish intent from implementation.** Read `GLOSSARY.md` (legacy name `CONTEXT.md`) and relevant ADRs for recorded decisions; trace current code for actual behavior. Record conflicts with the spec or current user decisions as risk rows. Native CLI memory is a lead to verify.
- **Decisions are artifacts.** Chat reports only what was written plus the phase update.
- Name the full PROJECT-CODE from the Project Matrix everywhere; never mix one project's conventions, tokens, or components into another.
- **No located consumer is a risk, not a pass.** In a cross-project contract, a changed surface with no consumer call-site anywhere in the matrix, or a consumer outside the spec's slices, gets a **RISK** row — never silently assumed unused.
- **A flow only counts against a verified environment.** A pass with no evidence stays `pending`, not `pass`.
- **Suggest, never auto-chain.** build does not auto-run gate; gate does not auto-run `/commit-push-*`. Recommend the next step and stop.
- **Read-only in build.** Only the contract file is written — never product code, config, issues, or ADRs.
- Sub-agents: dispatch local lanes automatically for independent work — never cloud agents; announce the lane count at dispatch and report each lane as it completes.

## The contract artifact

One per spec at `<artifacts-root>/specs/integration/<SPEC-ID>-contract.md`. Resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`GLOSSARY-MAP.md` at repo root; legacy `CONTEXT-MAP.md`), else the repo root.

On reruns, read the existing contract, preserve user edits and the gate log, and reset affected flows to `pending` when their implementation or environment changes. Validate `<SPEC-ID>` as one filename component, with no path separators or `..`.

In build mode, fill [`references/build-contract.md`](references/build-contract.md). In gate mode, use the existing contract; load the schema only when its structure or smoke coverage needs repair. A filled example is optional when uncertain: [`references/contract-example.md`](references/contract-example.md).

## Modes

### build (default)

1. Read the spec and its sub-issues.
2. Detect touched PROJECT-CODEs; exactly one → single-project sweep (Rules), stop when no contract is needed.
3. Identify the producer slice and its consumers; fill Sections 1–3. Out-of-spec consumer → also suggest a slice via `/to-tickets`.
4. Write Section 4 flows (Driver, empty Evidence, `Status: pending`), write the file, emit the build update.

### gate

The full gate binds the **spec-level ship** and the **PM handoff**. Flows crossing unimplemented slices never block per-slice `/commit-push-*`: run early the flows whose crossings are implemented; leave the rest `pending`.

1. **Verify the environment before driving anything** (Section 1): confirm host authority, service reachability, required test data, and that the changed surface is in the running artifact. Rebuild or seed only within the authority above; otherwise leave affected flows `pending`. Check Sections 2–3 against implementation and update changed surfaces before running flows.
2. Drive each flow per its **Driver**; record **Evidence** (screenshot path, quoted response, observed text); mark `pass`/`fail`. Browser flows follow [`references/consumer-sweep.md`](references/consumer-sweep.md).
3. **Any `fail` reopens the contract:** record it, surface it, block the current step — do not commit-push, do not hand to PM, never silently drop a fail. Route the failing seam to `/to-tickets`, or `/diagnosing-bugs` if it is a defect rather than a missing slice.
4. **Driver unavailable** (agent-browser not installed; a manual step that can't be run now): state that, list those flows as manual steps for the user, and leave them `pending` — never mark a flow `pass` on assumption.
5. Append the gate-log line, including pending counts and reasons. All `pass` → suggest `/code-review` then `/commit-push-close` / `/commit-push-pr`, or PM handoff; any `fail` → `/to-tickets` or `/diagnosing-bugs`. Any `pending` blocks spec-level ship and PM handoff; report the missing proof. Stop — never auto-chain.

## Output

Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field.

**build update:**

```markdown
Stage: build — wrote specs/integration/<SPEC-ID>-contract.md. [or: single project — no contract needed (matrix swept; no external call-sites)]
Found: producer <PROJECT-CODE>; consumers <PROJECT-CODE>, <PROJECT-CODE>; <K> changed surfaces; <R> risk row(s). [or: matrix swept for <K> changed surfaces; no external call-sites]
Next: implement the slices, then integration-contract gate mode before spec-level ship and PM handoff. [or: proceed per-slice — no integration gate needed]
Needs user: <risk rows to confirm, environment facts, or "none">.
```

**gate report** — the Section 4 table (minus Evidence) with Status filled, between these lines:

```markdown
Environment: <verified service(s) and artifact evidence, or unverified service(s) and reason>.
<table>
Reopened by failures (blocking, not shipped): <#s or "none">.

Suggested next skills (optional):
- /to-tickets: slice the failing seam (<#s>).
- /code-review then /commit-push-*: once every flow is pass.
```

## Completion criteria

- [ ] The contract re-opens with four sections and gate log; or the build update reads `single project — no contract needed`, no new file was written, and any historical contract is preserved and identified
- [ ] gate: a new gate-log line is appended; every flow's `Status` is `pass`/`fail` with Evidence filled, or `pending`
- [ ] The emitted update matches the Output template for the mode run
