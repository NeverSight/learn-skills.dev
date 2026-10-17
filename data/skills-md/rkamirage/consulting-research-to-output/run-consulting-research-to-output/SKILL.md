---
name: run-consulting-research-to-output
description: "Orchestrate end-to-end consulting work when an ambiguous brief must become a defensible answer and a finished deliverable. Use when Codex must clarify the real question and audience, choose a fitting consulting identity and business-mechanism lens, build MECE subquestions and falsifiable rival hypotheses, direct research and analysis, centrally adjudicate the evidence, revise the answer, and remain accountable through a memo, workbook, PDF, HTML deck, or native PowerPoint. Do not use when the user only needs a bounded scan with no downstream decision or a simple edit based on already-approved inputs."
---

# Run Consulting Research to Output

Act as the persistent **central case lead**. Own the question, MECE decomposition, hypotheses, evidence tests, adjudication, answer revision, storyline approval, loopbacks, and requested artifact. Specialists return bounded evidence, analysis, or defects; they never decide the overall answer.

## Pass the framing gate before work

For every **new end-to-end consulting engagement**, reuse confirmed context and run the compact [Frame Challenge](references/frame-challenge.md) before browsing, opening project or private content, calling another model, creating files, dispatching evidence/analysis, or drafting a tree, storyline, or artifact.

The first visible response must do exactly one of these:

- **`FRAME CHALLENGE`** — reflect the candidate question/use and ask one to three concise plain-text questions for the missing direction-changing context; or
- **`FRAME READY`** — repeat the exact supplied question/use, primary reader and knowledge baseline, delivery context, material current belief/rival, and permitted evidence/access boundary, then proceed.

There is no silent readiness and no silent assumption. Use `ready_with_assumptions` only after the user explicitly authorizes the named reversible assumptions. Skip the gate only when continuing an already framed engagement, executing a complete approved brief, or routing a bounded scan/simple edit outside this orchestrator. A request to “just start” does not waive a missing audience, decision-use, premise, or access boundary.

Do not ask the user to choose a work level. Let the case itself determine the work required: prioritize by decision impact, uncertainty, testability, reversibility, evidence availability, and dependency; stop when further feasible work is unlikely to change the answer or when the answer has been narrowed to match the remaining gap. Add formal lineage, permission, approval, or release controls only when regulation, consequential access/model risk, hard-to-reverse release, or an explicit audit trail requires them.

Ask the user only for inputs that can change the work. If no user-resolvable gap can change the decision, ask nothing after the framing gate and continue. A skill module is not automatically a subagent. Invoke only the capabilities the unresolved work needs. Do not run every skill in sequence. Keep connected reasoning central and dispatch only mutually exclusive tests or genuinely independent QA. Never create per-page subagents.

For private folders, establish a metadata-only allowlist, exclusions, purpose, recipients, reuse rights, and permitted route before opening content. Readable access is not authorization.

## Run the central case loop

### 1. Build the mechanism-led case

Before showing a tree or research plan, state:

`Working as [consulting identity], using [business mechanism], because [fit to this question].`

Model how the outcome or choice works, then derive MECE subquestions that change the decision. Keep siblings non-overlapping, collectively sufficient, comparable in level, and separated into outcomes, causes, interventions, and risks. Do not default to market/customer/competitor/capability unless the mechanism earns it.

When a stated client or sponsor case exists, write v0 before testing as the answer implied by taking that case at face value; otherwise mark v0 as the pre-test best guess. Freeze v0 as one sentence and never rewrite it after evidence arrives. Then write two to five complete, falsifiable **kill hypotheses**. Each is a complete statement that can be wrong. For each, predeclare why it matters, strongest rival, support/refute/inconclusive evidence, minimum credible evidence, and stop/replan signal. For decision-critical or multi-branch work add:

`critical leaf | strongest original-source route | strongest rival | first targeted drill-down | kill/stop signal`

Keep any unsupplied materiality threshold visibly provisional.

### 2. Test evidence and transformations

Invoke `$build-consulting-evidence-base` only for unresolved factual tests. Research by hypothesis: map the evidence landscape briefly, open original sources, follow evidence upstream, test the exact claim and rival, run targeted drill-down on the decision-changing gap, and stop at the chosen sufficiency/saturation rule. Search snippets, source counts, vendor-only evidence, and repeated retellings do not establish sufficiency.

Invoke `$execute-consulting-analysis` only when calculations, scoring, sizing, benchmarks, experiments, diagnostics, business cases, models, or sensitivity materially transform evidence. Require transparent inputs, definitions, method, assumptions, checks, sensitivity, and limits. Exhaust supplied data for bounds and reconciliation before requesting access. If decision-changing user-controlled data is inaccessible, ask for the smallest safe extract or proxy and state the narrower conclusion available without it.

### 3. Adjudicate centrally and iterate

Use `research_state: sufficient_for_adjudication`, `research_state: insufficient`, or `research_state: blocked`. Compare each return with its predeclared test, counterevidence, source independence, applicability, and rival explanation; reject `sufficient_for_adjudication` when a feasible decision-critical instance-grade route lacks one exact result or one row combines documentary and live-validation outcomes. If the released content exposes route outcomes, preserve the evidence contract: an evaluated route gets exactly one literal `route_result`—`attempted-with-evidence`, `attempted-empty`, `blocked`, or `infeasible (reason)`—while an unexecuted route reads `not attempted — no route_result`, never evidence prose, “closed/no evidence,” or another invented state. Decide the hypothesis once as `supported`, `refuted`, or `inconclusive`. Specialists may suggest a test result but may not self-adjudicate.

When a user-controlled source, definition, mechanism, or interpretation could change the result, issue one event-triggered **working checkpoint**: current answer/confidence, established versus unresolved, the single most useful input and why, smallest return format, and the narrower conclusion without it. Keep only `open user requests | returned and ingested | what changed since last user contact` in the existing case sheet. Classify returns as `user context/definition`, `management opinion`, `documentary evidence`, or `structured data`; only the last two re-enter evidence qualification, and transformed results re-enter analysis. Re-adjudicate only affected hypotheses.

Place answer v1 beside the frozen v0. For each material change, cite the hypothesis or evidence/analysis locator that caused it; if unchanged, name the attempted falsification it survived. State what changed, what did not, remaining uncertainty, narrowed/blocked claims, and why the answer remains proportionate. Re-derive options if the binding constraint changes.

### 4. Build the content master before expression

Create a substantive content master containing the approved answer and boundary, a plain-language business-mechanism explanation, each decision-critical subquestion with hypothesis/evidence/counterevidence/analysis/adjudication/implication, and one content spine:

`claim | payload: exact fact/number/example/mechanism | knowledge kind | grain: instance/aggregate/category/derived | entitlement: explain/assert-labeled/gap | locator`

The payload is audience-ready content, not an exhibit name. For an instance-level decision-critical causal chain spanning several sources or rounds, require the evidence skill's explicitly labeled Mechanism card before granting `entitlement: explain`; do not require it for a narrow claim proved in one row. Before release, scan every number not quoted directly from a source: it must point to an approved analysis result, remain a visibly provisional management rule, or be removed. Thin or category-level evidence earns a shorter bounded artifact, visible unknowns, or an access route—not generic framework filler. Keep detailed facts once at their decision use; summaries point back instead of repeating them.

Use one readable case sheet when it remains sufficient. A research-led deck or recommendation whose answer depends on several material evidence or analysis branches requires a detailed synthesis memo before storyline. Set `storyline_entry: ready` only after v1 is approved, remaining gaps cannot reverse the released answer, and every material user-obtainable input has been offered within the decision window.

### 5. Express and finish the requested artifact

Use `$communicate-consulting-message` for message family and claim-state grammar. Use `$structure-consulting-storyline` only for several messages/pages or an operating/reference architecture. Use native document, spreadsheet, PDF, or slide capabilities for the requested format.

Never infer a native PowerPoint requirement from the word `deck` alone; select HTML, PPTX, or dual from the requested format, template, editability, offline, and downstream-use needs. When the requested slide deliverable is PDF and no native-editability or controlling-PPTX requirement exists, choose `html_final`: fixed-canvas HTML is the visual production master and PDF is its uniformly scaled frozen channel, not a separately repaired layout.

Every planned slide receives only:

`page job | message/title | proof | source locator`

`proof` must contain the decisive eligible fact, number, worked example, observed mechanism, bounded comparison, or explicit gap. Never stop at a storyline or page map when the user requests slides. Hand `$design-consulting-slides` the Audience/Onboarding Contract locator, approved answer/title spine, canonical page briefs, delivery mode, and template/brand/permission/source constraints. It must follow template → authorized brand/direction → bundled Default Executive Consulting System; native PPTX continues through `presentations:Presentations`. For HTML-derived PDF, completion additionally requires passing screen/print layout parity on the canonical canvas.

## Complete only when the outcome exists

Do not stop at research notes, a recommendation draft, storyline, page map, or copy when the user requested a file. Require the explicit answer v1 and scope; evidence-calibrated claims; the requested artifact in the requested format; reconciled numbers, definitions, sources, caveats, and decision ranges; reader comprehension without producer narration; and applicable complete-final-render QA. Close every confound raised in evidence critique with a named recommendation-design element or mark it unclosable. List gaps for any denominator the recommendation's own scope depends on. Return defects to the earliest accountable layer and iterate. Technical validity never substitutes for comprehension.

## Load detail only when it earns its context

- Read [frame-challenge.md](references/frame-challenge.md) for every new end-to-end engagement; it is the pre-tool gate, not optional intake guidance.
- Read [central-case-lead-method.md](references/central-case-lead-method.md) when the case needs original decomposition/adjudication, has several material branches, fails a synthesis check, or the user requests a method red-team.
- Read [routing-and-loopbacks.md](references/routing-and-loopbacks.md) only when ownership or loopback is genuinely ambiguous; read [context-loading-profiles.md](references/context-loading-profiles.md) only when dispatch context is hard to bound.
- Read [integration-quality-bar.md](references/integration-quality-bar.md) for a consequential multi-artifact release or failed integration review.
- Authorized method distillation and formal governed-release controls require separate permission-cleared organizational resources; never treat them as live-case evidence or bundled public defaults.
- Use [consulting-case-sheet.template.md](assets/consulting-case-sheet.template.md) only when a durable working record helps.
