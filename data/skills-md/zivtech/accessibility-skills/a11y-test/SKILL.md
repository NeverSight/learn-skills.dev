---
name: a11y-test
description: "Use when you need to run real accessibility tests — Playwright keyboard interactions, axe-core scanning, visual regression, and WCAG 2.2 compliance checks. The measurement layer that feeds evidence into a11y-critic reviews."
license: Apache-2.0
compatibility: Claude Code-compatible; protocol is model-agnostic
metadata:
  author: zivtech
  version: "1.4.0"
---

# Accessibility Testing Skill

## Browser Tooling Routing (read first)

Pick the right execution mode from the routing table before running anything (the table is the source of truth — don't trust remembered mode counts):

| Task | Tool | Why |
|---|---|---|
| Codified CI keyboard tests, visual regression, axe-core scans, WCAG compliance suites | `npx playwright test` with `.spec.js` files | Real keyboard events, CI-runnable, version-controlled, reproducible. Primary path — all mandatory rules below still apply. |
| Baseline sweep across a list of URLs — machine-readable axe-core evidence per page, no `.spec.js` authoring, not CI-embedded | [`references/baseline-url-scan.mjs`](references/baseline-url-scan.mjs) (in-repo reference script; peer deps `playwright` + `@axe-core/playwright`) | Sequential per-page axe scan + summary JSON for baseline/regression evidence across many pages in one run. `--census` adds DOM-census heuristics (empty paragraphs, autocomplete-absence, duplicate ids); `--alt-snapshot` writes a diffable per-page alt-text map. Detector output, not a conformance verdict — axe-detectable subset (plus heuristics) only. See "Baseline URL-list scan" below. |
| Supplemental automated coverage — run a second/third detector engine over an already-scanned page for a broader candidate net and an aggregate cross-engine signal (agreement → `corroborated`; never a conformance verdict) | Siteimprove **Alfa** (`@siteimprove/*` Playwright, consuming-project dep) or WebAIM **WAVE** (extension or subscription API, operator's own licence) | Detector-only supplemental lanes that feed `detected_by` / `corroboration`. Breadth adds candidates to triage, true and false — not a coverage guarantee. See "Supplemental detector lanes (WAVE, Siteimprove Alfa)" below. |
| Interactive agent-driven reconnaissance: snapshot ARIA structure, navigate a SPA to reach the page under test, verify a fix in place, capture annotated screenshots, probe a disclosure/menu/modal without writing a test file | `agent-browser` CLI (snapshot+ref pattern, persistent CDP daemon, real keyboard events) | One shell call per action, no test-file overhead, returns `@e1`-style refs that map directly to actions. See "Interactive reconnaissance with agent-browser" below. |
| Generate a test script from a prose spec ("test that this modal traps focus and Escape closes it") | `/webwright:run` or `/webwright:craft` (Claude Code plugin) | LLM generates complete Python Playwright script. Review before trusting. Also captures `aria_snapshot()` for deep ARIA tree inspection. See [references/webwright-testgen.md](references/webwright-testgen.md). |
| Goal-driven journey audit of a live URL — "can a keyboard-only or screen-reader user complete this task?" — with evidence artifacts | `keyboard-a11y-tester` (external clone, pinned release `0.5.0`; deterministic runner + agent-driven serve/step loop) | URL + goal in, evidence-linked WCAG findings out — no test file needed. Emulated screen-reader announcements, live-region capture, and focus-indicator measurement at the page/journey level that no other mode provides. See "Goal-driven journey audits with keyboard-a11y-tester" below. |
| Component/unit-level screen-reader assertions — accessible names, reading order, live-region announcements — in the project's own test suite (Vitest/Jest+jsdom, Storybook play functions, or a browser page), no URL or journey needed | `@guidepup/virtual-screen-reader` (npm devDependency, exact-pinned `0.32.1`) | Per-component, per-PR spoken-output evidence in milliseconds — the implement→test layer keyboard-a11y-tester can't reach (it needs a deployed URL). Synthetic interactions: never keyboard-operability evidence. See [references/vsr-testing.md](references/vsr-testing.md). |
| Visual inspection, DOM queries from a conversational session | `agent-browser screenshot` / `agent-browser screenshot --annotate` / `agent-browser snapshot --max-output 8000` | Same daemon, no test runner needed. |
| A person confirms a fix at the fixed stage (the closure record needs its `attestation` block), or walks an ICT baseline row no machine mode covers | [`references/human-verification-walkthrough.md`](references/human-verification-walkthrough.md) | The human tier: a planned-operation-driven walk that records `before` / `action` / `expected` / `observed` per operation in a shape the five admissibility rules can read, plus an attended-media shape for the alternative-content rows. Never a free walk; the one place a single PASS is the unreliable result. See "Human verification walk-through" below. |
| Anything requiring real keyboard event delivery through an MCP wrapper | **DO NOT USE Playwright MCP.** Its `browser_press_key` calls are silently dropped for most interactive widgets. Use `npx playwright test` or `agent-browser` instead. |

**Decision flowchart:**
```
Do you have a prose description of what to test, but no test script yet?
  YES → /webwright:run (one-shot) or /webwright:craft (reusable parameterized tool)
  NO, you need to run an existing test → npx playwright test
  NO, you have a list of URLs and need machine-readable axe evidence across all of them, no test file → references/baseline-url-scan.mjs (or pa11y-ci --sitemap for sitemap-wide sweeps)
  NO, you need to audit a live URL against a user goal (journey, announcements, focus indicators) → keyboard-a11y-tester
  NO, you need to assert component announcements, names, or reading order in unit tests (no URL yet) → virtual-screen-reader
  NO, you need to explore interactively → agent-browser
  NO, a person must confirm a fix on the pinned version, or walk a baseline row no mode covers → references/human-verification-walkthrough.md
```

**CDP keyboard event delivery for `agent-browser` has been verified end-to-end** on both a vanilla JS disclosure widget (WAI-ARIA APG disclosure-faq example: `focus → press Enter → aria-expanded: false → true`) and a React state-driven modal (react.dev DocSearch: `Meta+K` → React global keydown listener → state-mounted searchbox). The MCP keyboard delivery bug does not apply to `agent-browser` because it calls CDP `Input.dispatchKeyEvent` directly rather than through an MCP wrapper.

## Verification evidence contract

**Evidence type must match the failing condition.** A screenshot is never evidence for an interaction-class fix (keyboard operability, focus behavior, or a status-message announcement) — it shows what a sighted mouse user sees, not what a keyboard or screen-reader user experiences. When a fix's evidence doesn't match its defect class, the fix ships labeled **partial**, naming which defect classes still lack matching evidence.

| Defect class | Evidence REQUIRED before "verified" | Mode |
|---|---|---|
| `keyboard-operability` — Keyboard operability (reachable, operable with Tab/Enter/Space/Escape/arrows) | Real-keyboard Playwright transcript — actual `page.keyboard.press()` calls, never ARIA-attribute inspection alone | `npx playwright test` |
| `focus-order-indicator` — Focus order & focus-visible sufficiency | Journey-level focus trace evidence | `keyboard-a11y-tester` |
| `name-role-state` — Accessible name/role/state; status-message announcements | Assertion output against actual computed screen-reader output | `virtual-screen-reader` |
| `machine-detectable` — Machine-detectable semantics, contrast, alt-presence (a rule fires or stops firing) | Re-scan of the touched page(s) after the fix | `baseline-url-scan.mjs` (axe-core violations; `--census`/`--alt-snapshot` for the heuristic classes) |
| `visual-only` — Visual-only classes (layout, spacing, color/swatch correctness) | Screenshot comparison | screenshots (`agent-browser screenshot` / Playwright screenshot) |

This table is what `a11y-critic` Phase 0 checks a remediation's attached evidence against, and what `bug-reporting`'s "Verification evidence" field cites.

### Detector-lane authority boundary

A detector PASS means only "no detection fired for this route, state, viewport, config, and version" — never a WCAG, Section 508, keyboard, or assistive-technology verdict. Cross-tool agreement on the same target raises triage priority; it never confirms a defect by itself, and an absence of detection is not evidence of conformance. When two or more independent detectors flag the same WCAG criterion on the same target, record it on the finding as `corroboration: corroborated` with a `detected_by` engine list (the A11y Evidence Finding Contract's Cross-Detector Corroboration fields) — a triage-confidence tag, never a conformance input, and "corroborated" precisely because "confirmed" is reserved for the human/AT verification tier below. The join key is WCAG criterion + fingerprint, never rule id (engines name the same defect differently). Same-family engines (axe-core, HTML_CodeSniffer, Alfa) agree more cheaply than cross-family ones (WebAIM WAVE vs axe); weight the signal accordingly, and never count a non-detection as agreement.

**An infrastructure limit must never emit a canonical result.** A step-cap watchdog, a timeout, or a crashed collector is an *abort*, not a PASS/FAIL/BLOCKED outcome — record it as what it is (aborted, incomplete, environment-limited) and keep it out of the pass/fail denominator until it is resolved.

**Mandatory cross-check rule:** whenever a run's non-conclusive rate (`BLOCKED`, `cantTell`, or equivalent) approaches saturation for a batch — most of the sampled set landing in a single non-conclusive bucket rather than spread across pass/fail — treat that as a signal about the collector, not about the product, and cross-check the batch against an independent evidence lane (a different tool, a driven session, or manual sampling) before the numbers reach a client-facing report. A near-saturated non-conclusive rate that ships unchecked reads as "almost entirely untestable," which may simply be an ordinary pass/fail distribution obscured by a collector fault.

Related discipline, restated for this boundary: never promote scanner output straight to a WCAG or Section 508 verdict; never treat count-parity between two runs as completeness; never collapse `cantTell` / informational / skipped / blocked / untested into pass or fail — each stays a distinguishable, visible state (see the coverage-ledger vocabulary in `acr-reporting`'s untested gate for the report-side version of the same rule).

### Evidence retention (append-only)

Never overwrite an evidence run. Failed, intermediate, and superseded captures are retained beside the final result under names that state *why* they are not final (for example `-raw-live-capture`, `-script-error`, `-modifier-mismatch`, `-pre-final-adjudication`). The same discipline extends to generated deliverables: every non-final revision is kept beside the final one with an append-only supersession log, and each non-final revision is explicitly marked not client-facing and not a conformance, certification, publication, or acceptance artifact.

Retention is not bookkeeping for its own sake — it is what makes silent errors findable. A numeric error in an otherwise structurally valid generated deliverable — a formula range that under-counts, a mapping that drops rows — passes schema validation and surfaces only when a later revision can be diffed against the one that was wrong. Overwrite the run and that diff is gone.

`references/hash-evidence.mjs` makes the rule checkable: it writes an append-only `checksums.json` manifest beside an evidence tree and `--verify` lists every modified, missing, or unlisted file, exiting non-zero on drift (modified or missing; unlisted too under `--strict`) — it makes silent edits findable, not impossible.

## Retest classification

Two clauses that govern when a retest result is trustworthy.

**n = 1 is variance, not a finding.** A single failed reproduction attempt is inconclusive, not a FAIL. A FAIL requires the same miss reproduced across two independent sessions (a different run, same conditions). This mirrors the routing rule already in force elsewhere in this bundle for model-benchmark evaluation: a single-lane result that flips under byte-identical conditions is treated as variance until adjudicated by a second, independent pass — never reported as a conclusion on its own.

**A version or content-marker delta forces a fresh retest.** Frozen evidence has an expiry condition tied to the product, not the evidence: the moment the product's version or a tracked content marker changes, every baseline captured before that change stops being admissible as a claim about *current* conformance — it remains valid history and nothing more. Two rules follow:
- Capture the version or content marker as a field on the evidence artifact itself, so a stale-baseline check is mechanical rather than remembered.
- On a detected delta, a fresh retest is mandatory for any row whose claim is about current conformance. "We tested this in a previous cycle" is not, by itself, an outcome — a frozen baseline may never silently stand in for current evidence.

### Human verification walk-through

The retest campaign has a human tier, and it is not a free walk. When a closure record needs its `attestation` block (the fixed-stage confirmation `acr-reporting` admits an improved term on), or when a declared-508 engagement reaches one of the crosswalk's 13 `not-covered` rows, a named person walks entries from the campaign's planned operation set — never off it — and records, per operation, where they started and how they got there, the action, the expected result, and the observed result, in the package shape [`references/human-verification-walkthrough.md`](references/human-verification-walkthrough.md) specifies (an operation shape, and an attended-media shape for the alternative-content rows). The record is appended to the sample's evidence artifact under the append-only rule, and the closure's attestation block cites it.

**The n = 1 rule reverses at the fixed stage.** A single failed reproduction is variance at diagnosis because the expensive error there is a flaky miss reported as a regression. At the fixed stage the expensive error runs the other way — one human PASS becomes a `supports` in a published document, and the person confirming a fix knows what they expect to see. A single human `FAIL` sends the item back to remediation on its own; a human `PASS` that will back a fixed-stage `supports` needs a second package by a different person, or the same person in a separate session on a later day, with at least one of the two not by the fix's author (the closure contract's `second_confirmation`). Only the different-person branch controls the expectation the rule names; the same-person branch controls session and environment variance and is the weaker one — prefer a different person. A walked `BLOCKED` or `FAIL` never attests: the closure stays `draft_not_attested`, the walk is cited, and for `BLOCKED` the instrument that would decide it is named. Photosensitivity-class content (2.3.1 / 2.3.2) is never walked by extended attendance — a capped first look, or a declined one, goes straight to `BLOCKED` with the analyzer named; the reference carries the safety clause.

### Campaign completeness contract

A retest campaign is not complete when the runner exits — it is complete when **zero** planned operations remain unresolved. Treat "the suite ran" and "every planned operation has a result" as different claims until proven equal:

- State an explicit zero-unresolved contract as an exit condition: enumerate the planned operation set before the run starts, and the run does not close out until every entry in that set carries a disposition (pass, fail, or one of the non-pass values above — never silently dropped).
- Provide a recovery path that re-drives specifically the unresolved operations, not the whole batch, when a run exits early.
- Support a resumption contract: an interrupted campaign continues from its unresolved set on the next run rather than restarting from zero.

This is a contract for the evidence a retest run must produce, not a specification for a particular runner implementation — see `docs/a11y-evaluation-report-contract.md` for the report-level half of the same completeness rule.

### Operation-evidence admissibility

Retest evidence is admissible for the operation it claims only when it survives five rules. These govern the *evidence package* for a single operation — a retest hitting a specific target, a keyboard trace, a passive DOM/AX observation — not the accessibility of the target itself. The `evals/suites/a11y-test-operation-evidence` lane exercises each with a clean control.

- **A bounded diagnostic is not a conclusion.** A `focus_stagnation_observed`-class note — focus not advancing on a keyboard probe — is a bounded collector observation, not a WCAG 2.1.2 keyboard-trap finding. Promoting it to a trap conclusion requires a separate trace that attempts the documented exit (press Escape or the exit keys and show focus cannot leave). Absent that trace the operation stays `BLOCKED` where the stagnation observation is admitted evidence about that operation (a collector block, not a conformance outcome); stagnation alone is neither a trap nor a conformance failure.
- **Setup and action must be continuous.** An action's evidence is admissible only if its starting (`before`) identity equals the terminal identity of the setup that immediately preceded it in the *same session*. A setup in one session and an action from a different starting locus in another do not compose into evidence about the planned operation.
- **Conditional states are natural-only.** A state that appears only under a condition (an empty result, an error) stays `UNTESTED` until it occurs naturally under an approved input. Inducing it synthetically — editing a response, forcing the state — does not clear coverage; it shows the message renders, not that the state is reachable in use.
- **Passive observations are bound, never standalone.** A DOM/AX snapshot (roles and states present in the rendered tree) is admissible only as support bound to the causing action and on a source allowlist. By itself it is never evidence of keyboard-reachability or of announcement — those require the causing key press and its observed result.
- **No silent ancestor remapping.** When the exact target is not on the focus path, evidence recorded against a nearest reachable ancestor is admissible only through a reviewed, separately frozen owner/descendant mapping (the composite's documented owner and navigation model). A silent nearest-ancestor substitution is not evidence about the target.

**Human-sourced packages are scored by the same five rules.** A person's walk-through package ([`references/human-verification-walkthrough.md`](references/human-verification-walkthrough.md)) carries the fields the rules read — `before.reached_by` and `before.locus` in one `session` for continuity, `observed_via` for passive binding, `target_reached` for ancestor remapping, the exit attempt in `action` before any trap conclusion, approved inputs only for conditional states. A package missing those fields fails the rule whose predicate it cannot show: "I checked it, it's fine" has no starting locus and no action for its observation to bind to, so it breaks `setup_action_continuity` and `passive_observation_binding` as written; the tidier package with every field filled and `observed: "as expected"` breaks rule 4 alone, because no observed result of the action is bound to it — no sixth rule is needed for either, and the operation stays where its admitted evidence left it. The attended-media shape (audio description, captions, transcripts, and any observation about content rather than an operation) has no locus and no action, so rules 2 and 5 do not apply to it and the reference marks them so; `played` — the stretches actually played, with the alternative selected — is the binding field, and rule 4 is what catches a menu listing or a track label offered as evidence of the alternative. For human evidence rules 2 and 4 are structured self-report rather than a verified identity or a source allowlist; the record says so, and the second confirmation is the control.

### Structured disposition block

Every admissibility review closes with one fenced yaml block a rule-based scorer checks mechanically (the `score_acr.py` precedent). Stable ids for the five rules above: `bounded_diagnostic_not_promoted`, `setup_action_continuity`, `natural_only_conditional_state`, `passive_observation_binding`, `ancestor_remapping_review`.

```yaml
admissibility: ACCEPT | REJECT                                     # ACCEPT exactly when rules_violated is empty
dispositions: {<operation id>: PASS | FAIL | UNTESTED | BLOCKED}   # every operation in the package
rules_violated: {<operation id>: [<rule id>, ...]}                 # only operations whose evidence breaks a rule
claim_boundary: "<per operation: what the admitted evidence establishes, and what it leaves undecided about the target>"
```

The four disposition values are this block's closed set. `PASS` and `FAIL` mean admitted evidence decides the operation's own predicate; `BLOCKED` means an admitted bounded observation *about that operation* stands without the trace or instrument reading that would decide it — a collector's `focus_stagnation_observed` note with no exit-path trace, or a person's "I watched the animation and cannot count flashes per second" with no analyzer reading; the definition was written around collector output and applies unchanged to an attended human observation, whose `claim_boundary` names the missing instrument; `UNTESTED` means no admitted observation bears on it. Rejected evidence never moves an operation: a recorded prior state stays, and an operation with none takes only what its admitted evidence supports. A non-conclusive run state outside the four (`cantTell`, `skipped`) is `UNTESTED` here and named in `claim_boundary`, never folded into `BLOCKED`. `admissibility` and `rules_violated` score the evidence package, not the target's accessibility; `dispositions` carries forward only what admitted evidence establishes about each operation.

### PASS partition: rule-tier vs chain-tier

Not every PASS carries the same evidence. A **rule-tier** pass verified the operation-specific predicate the row is about — this exact control, this exact expected result. A **chain-tier** pass rode a generic keyboard-chain success: the page was navigable and nothing obviously broke, with no operation-specific rule behind it. Counting the two together overstates coverage.

Partition passes into the two tiers and make the ratio visible in the evidence artifact itself, not in prose. A completeness claim reporting a single PASS count — without showing how many rested on an operation-specific rule versus a generic chain — has not established what it claims. This is a self-check on our own output quality, not a statement about the product: a chain-tier-heavy PASS set is a signal to go back and add operation-specific predicates, never a reason to report a high pass rate.
### Evidence consumption (context discipline)

**Evidence artifacts are handles, not payloads.** Reference `trace.json`, `findings.json`, axe-core results, and similar artifacts by path — never paste them wholesale into context. Pull only the fields under adjudication; jq recipes for the common extractions live in [references/evidence-extraction.md](references/evidence-extraction.md).

Screenshots are cited by path in findings and reports. Actually viewing one — reading its image content into context — is reserved for visual-class adjudication (the last row of the evidence table above); every other defect class is decided from extracted fields, not pixels. When a review genuinely needs to view images — a batch of visual-class captures, or a screenshot-heavy recon pass — run it in a subagent (`a11y-evidence-reader`, whose Vision Mode gates and budgets image reads and returns text only) so the image bytes stay in that agent's window and never reach the main session. And prefer `agent-browser screenshot` (writes the file to disk, returns a path) over the MCP screenshot tools (`claude-in-chrome`, Playwright `browser_take_screenshot`), which return the bytes inline: the disk path is a handle, the inline bytes are a payload.

Long-running commands (scans, test runs, crawls) redirect stdout to a file; read back only the summary or failing subset, never the full log — then pull what you need with the extraction recipes ([references/evidence-extraction.md](references/evidence-extraction.md)).

`agent-browser` calls in conversational sessions carry `--max-output <chars>` to cap output per call — see "Interactive reconnaissance with agent-browser" below.

## Interactive reconnaissance with agent-browser

For ad-hoc a11y probing inside a conversational session — before writing a `.spec.js` file, when verifying a single fix, or when exploring the ARIA structure of an unfamiliar component — use `agent-browser`. The snapshot+ref pattern eliminates locator hunting:

```bash
agent-browser open https://example.com/component-under-test
agent-browser snapshot -i --max-output 8000        # Returns interactive elements with refs: [ref=e1], [ref=e2]...
agent-browser focus @e1                            # Focus by ref
agent-browser press Enter                          # Real CDP keyboard event
agent-browser get attr @e1 aria-expanded            # Verify state mutation
agent-browser screenshot --annotate                # Numbered overlays mapping to refs (useful for multimodal review)
agent-browser close
```

Key flags: `--profile Default` (reuse the user's Chrome login state for authenticated sites), `--session <name>` (isolated browser per parallel agent), `--json` (parseable output for programmatic checks), `--max-output <chars>` (truncate output to N characters — cap output-heavy commands like `snapshot -i`; a capped snapshot can silently drop element refs, so raise the cap rather than probing an inventory you know is truncated), `--allowed-domains` (safety).

**Keyboard-driving discipline (applies to all interactive modes, this one included):** never send a pre-counted sequence of Tabs. Snapshot/observe, then act on what is actually focused — "Tab until the focused control is named X" is right; "Tab 6 times" is wrong. Confirm success by state change (attribute flip, URL change, announcement), not assumption.

**When to escalate to `npx playwright test`**: when the verification needs to live in CI, run across PR builds, or exercise the 12 APG widget pattern templates in `references/keyboard-test-patterns.md`. Reconnaissance with `agent-browser` is for interactive probing; codified regression still belongs in `.spec.js` files.

## Batched one-pass per-page audit (default for rendered-context adjudication)

When you have to adjudicate more than one scanner occurrence on a page — WCAG-EM audit sampling, a scanner gap-review lane, or re-testing a batch of findings — **work the page, not the rule**. A human reviewer loads a page once and reads its headings, control names, images, tables and landmarks in a single pass, then disposes of every finding on that page from that one look. Probing one element per rule (open page, check the empty button; re-open, check the missing alt; re-open, check the layout table…) is the slow anti-pattern this replaces: it re-navigates the same page many times and scatters the evidence.

The default instead: **one DOM + accessibility-tree capture per bound page/state, covering every rule class at once, then adjudicate all of that page's occurrences from the single capture.** [`references/page-audit.mjs`](references/page-audit.mjs) is the reusable auditor — `auditPage()` runs in the page context and returns evidence for five scanner-rule classes in one call (`region_missing`, `heading_empty`, `button_empty`/empty-name controls, `alt_missing`, `table_layout`). Run it through whichever browser mode you are already in (Playwright `page.evaluate(AUDIT_PAGE_SRC)`, `agent-browser eval`, or the in-session JS tool).

Method:

1. **Group the page's occurrences first.** Map the raw scanner occurrences you must adjudicate to their pages/states (each SPA route or query state is a distinct page). An N-state app is N captures, not N × (rules) probes.
2. **One capture per page/state.** Run the auditor once the page is loaded and settled. Persist the returned report as the page's evidence artifact (hash it for the receipt).
3. **Adjudicate every rule for that page from the one report.** The report already carries the empty-name controls, missing-alt images, layout tables, missing landmarks and empty headings together — decide each occurrence's disposition against it without re-navigating.

Discipline (the same rules that govern any evidence here):

- **Detector, not verdict.** The auditor reports the facts a rule keys on; it assigns no WCAG SC, severity, or pass/fail. You do that, per occurrence, in rendered context.
- **Cross-check the computed name.** Its `accName` walk applies ARIA precedence (an empty `aria-labelledby` target yields an empty name), but confirm an empty-name finding against the browser's OWN computed accessible name (Playwright `page.accessibility.snapshot()`, `agent-browser snapshot -i`, or the DevTools Accessibility pane) before mapping it to a criterion — that read decides 4.1.2 (empty name) vs 2.4.6 (present but non-meaningful).
- **Positional locators drift.** A retained XPath from an earlier scan may not resolve in the current build (SPA re-render). Confirm at the rule/element level with a stable selector and disclose the drift; never launder a fresh element into a byte-identical reproduction of an old occurrence, and never force a DISMISS when the exact target could not be relocated.
- **Overlapping views are not additive.** Clusters, raw occurrences, execution groups, criterion cells and ICT rows are different lenses on the same page; do not sum them, and a local observation never proves the whole page passes.

## Attribute-removal differential diagnosis

A finding usually names a **cause**: "the `aria-label` is overriding better visible text", "`tabindex="0"` on the wrapper is why tab order is wrong". A snapshot proves the attribute exists. It does not prove the attribute is *why*. Differential diagnosis closes that gap: remove the suspect attribute, re-observe under identical conditions, and see whether the experience actually improves.

Technique credited to SSA's [YANKI](https://www.ssa.gov/accessibility/yanki/yanki.html) bookmarklet (Accessible Solutions Branch — same team as ANDI), which does exactly this for human testers. The bookmarklet itself is not routed here: in a scripted lane the removal is one line, and scripting it means the before/after pair is *capturable as evidence* rather than something you saw once.

```js
// Playwright. Baseline first — never mutate before you have captured the baseline.
const before = await page.accessibility.snapshot();

await page.evaluate(() =>
  document.querySelectorAll('[aria-label]').forEach(el => el.removeAttribute('aria-label'))
);

const after = await page.accessibility.snapshot();
// The diff is the evidence. Attach both halves, not the conclusion.
```

What each removal tests, and what a positive result means:

| Remove | If the result improves, the finding is |
|---|---|
| `aria-label` / `aria-labelledby` | the accessible name is overriding better visible text (2.5.3, 4.1.2) |
| `role` | an applied role is fighting the element's native semantics |
| `tabindex` > 0 | the author-imposed order is why focus order is illogical (2.4.3) |
| `tabindex="-1"` on an interactive control | the control is being held out of the tab order (2.1.1) |
| `tabindex="0"` on a non-interactive element | tab-order noise, not a real stop |
| `aria-hidden` | content is hidden from assistive technology that should not be |

Rules:

- **It is a diagnostic, never a fix and never a conformance result.** "Removing X made it better" is evidence about a cause. The remediation is still a design decision, and stripping the attribute in production is almost never it.
- **Baseline before you mutate, and re-observe under identical conditions** — same viewport, same route, same focus starting point. A differential taken across two different states measures nothing.
- **Capture both halves.** A before/after pair is admissible under the verification evidence contract; "I removed it and it looked better" is not.
- **Run it in a scratch tab, never a page the user is working in.** The DOM mutation is real.
- **A worse result is also a result.** If removal degrades the experience, the hypothesis is falsified — record that, do not quietly re-run with a different attribute until something confirms the finding you already wrote.

**Not yet verified:** the `agent-browser` equivalent of the `page.evaluate` step. The Playwright form above is the verified route; anyone wiring the agent-browser lane should confirm its own subcommand against `--help` first rather than assuming one exists.

## Test script generation with Webwright

Generate Playwright test scripts from prose specs via the Webwright plugin. See [`references/webwright-testgen.md`](references/webwright-testgen.md).

## Goal-driven journey audits with keyboard-a11y-tester

**When to use:** you have a live URL and a task in plain words ("can a keyboard-only or screen-reader user complete X?") and need evidence-linked WCAG findings without writing a test file — discovery audits, before/after patch evidence, whole-journey reviews. **When NOT to use:** widget CI regression (→ `.spec.js` + the APG templates in `references/keyboard-test-patterns.md`), quick probing or authenticated Chrome-profile flows (→ `agent-browser`), rule scans (→ axe-core, §4).

**What it is:** [ezufelt/keyboard-a11y-tester](https://github.com/ezufelt/keyboard-a11y-tester) — an external tool, adopted at release `0.5.0` (commit `7e852a7`, MIT; originally adopted at `97eb13e`, bumped 2026-07-11 after upstream merged our PR #7 and began tagging releases — re-verify on every upgrade). Two layers: a deterministic Playwright/CDP runner (real keyboard events only, never `.click()`; machine-decidable WCAG checks; dual-signal focus-indicator measurement) and an emulated screen-reader persona (`@guidepup/virtual-screen-reader`: announcement capture, live-region monitoring, reading-order census). Runs both W3C personas (keyboard "Ade", screen-reader "Lakshmi") in one pass. As of 0.5.0 it also detects broken ARIA ID references and keyboard-focusable controls missing from the accessibility tree, includes our 3.3.2 UA-default-name check, and supports authenticated runs via `--storage-state <playwright-storageState.json>` (agent-browser remains the route when you want to reuse the user's real Chrome profile instead of exporting state). Cross-validated against this repo's 33 critic fixtures on 2026-07-10 — agreement record: `evals/results/keyboard-a11y-tester/README.md`.

### Install (clone path — verified; Node ≥ 20)

```bash
git clone https://github.com/ezufelt/keyboard-a11y-tester && cd keyboard-a11y-tester
git checkout 0.5.0                    # adopted pin (tagged release)
npm install && node scripts/setup-check.mjs   # npx playwright install chromium only if browser_available=false
```

The upstream Claude Code plugin flow (`/plugin marketplace add ezufelt/keyboard-a11y-tester`) exists but is unverified here; the clone path works from both Claude Code and Codex.

### Run

```bash
# Batch blind Tab-crawl (unattended; never presses Enter/Space) — per viewport:
node scripts/runner.mjs --url https://site --viewport desktop --max-steps 40 --out <dir>

# Driven session (the value center — the agent decides every keystroke):
node scripts/runner.mjs serve --url https://site --goal "find and submit the contact form" \
     --viewport desktop --port 9333          # default port is 9333 (9400 in upstream examples is just an example)
# prints: READY <session-dir>
node scripts/runner.mjs observe <session-dir>
node scripts/runner.mjs step <session-dir> --press Tab      # one key → AX name/role/state, focus style, sr_announcement
node scripts/runner.mjs step <session-dir> --type "hello@example.com"
node scripts/runner.mjs finish <session-dir> && node scripts/runner.mjs stop <session-dir>
```

**Core discipline: observe → decide → act** (see the keyboard-driving rule in the agent-browser section — it originated here). Read `sr_announcement.live_announcements` after any action that visibly changes the page: an entry proves the update reaches a screen reader; its absence after a visible change is 4.1.3 failure evidence.

### Artifacts (temp dir, or `--out`)

- `trace.json` — per step: keystroke, selector, CDP AX name/role/state, computed focus style, `focus_moved`, screenshot ref, `sr_announcement`
- `deterministic-findings.json` — `{wcag, persona, conformance_level, confidence, severity, url, locations, persona_impact, evidence[]}`
- `screen-reader-census.json` — whole-page reading order (spoken phrase, role, selector) + declared live regions
- `screenshots/step_NNNN.png` — focused-region crops

These are measured test evidence for a11y-critic reviews (formal Phase 0 tier wiring lands with assessment Phase 3).

### Calibration rules (measured on our 33 fixtures, 2026-07-10)

1. **Batch-mode 4.1.3 "silent live region" findings are never failure evidence.** A blind crawl never operates anything, so correctly-wired regions look silent (confidence 0.35–0.4 vs 0.7+ elsewhere). They are prompts to run a driven session and judge from `live_announcements`.
2. **UA-intrinsic names mask missing labels.** An unlabeled `<input type=file>` reports AX name "Choose File", so the unnamed-control check stays quiet. Label association still needs axe/static/judgment review.
3. **Component-scale pages ≠ full pages.** Skip-link (2.4.1) and landmark findings assume a whole page; on component targets treat them as granularity artifacts.
4. **AA vs AAA honesty.** 2.4.13 focus-appearance findings are AAA-informative by design — never report them as 2.4.7 failures. The AAA pixel measurement is also rendering-environment-sensitive (macOS locally can emit AAA-informative findings that Linux CI does not, observed at both `97eb13e` and `0.5.0`) — one more reason never to gate on it.
5. **Emulated SR ≠ real AT.** Findings are spec-compliant-announcement evidence; the §6 manual NVDA/VoiceOver protocol still applies before shipping.
6. **`conformance_level` is the check's gate, not the SC's WCAG level** *(code-read at `0.5.0`, not fixture-measured — [upstream #27](https://github.com/ezufelt/keyboard-a11y-tester/issues/27), filed 2026-08-04)*. Only the 2.4.13 check emits `AAA`; every other finding falls through `level || 'AA'` to `"AA"`, mislabeling the nine Level A SCs the checks cover (1.1.1, 1.3.1, 1.4.1, 2.1.2, 2.4.1, 2.4.3, 3.2.1, 3.3.2, 4.1.2) — 2.4.7 and 4.1.3 are coincidentally correct. Read the field only as pass-fail (`AA`) vs informative (`AAA`) and derive the SC's true level from the SC number. Delete this rule when the pin advances past a fix for #27.

### Mapping findings → A11y Evidence Finding Contract

- severity: `serious` → MAJOR (CRITICAL if it blocks the goal); `moderate` → MINOR or MAJOR by user impact; `minor`/AAA-informative → ENHANCEMENT
- fingerprint: derive from selector + wcag + check kind (the tool's `id` embeds the viewport and is run-scoped — don't use it)
- persona → perspective_alarms: `keyboard` → `keyboard_motor`; `screen-reader` → `screen_reader_semantic`
- evidence: cite step ids + measured values (e.g. `trace.json step_0003: outline 3px solid; AAA contrast 2.34`)

### Cautions

- **Client production sites:** on pages with a CAPTCHA the runner suppresses `navigator.webdriver` (page-scoped) so the CAPTCHA can initialize — automation-signal spoofing that can trip a WAF or security review. Get explicit client sign-off before pointing it at client production infrastructure; prefer staging.
- Don't run concurrently with agent-browser or Webwright sessions (Chrome instance/port contention). Chromium-only — cross-browser coverage stays with `npx playwright test`.
- Run desktop and mobile viewports separately; navigation often collapses behind a disclosure on mobile.

## Component screen-reader assertions with virtual-screen-reader

Component/unit screen-reader assertions (accessible names, reading order, live-region announcements) via `@guidepup/virtual-screen-reader`. See [`references/vsr-testing.md`](references/vsr-testing.md).

## Baseline URL-list scan with references/baseline-url-scan.mjs

**When to use:** you have a list of URLs — a spot-check set, a sampled route list from a discovery or audit-scope engagement, a client's page inventory — and need machine-readable axe-core evidence across all of them in one run, without authoring a `.spec.js` file per page or wiring CI. Promoted 2026-08-14 from a one-off evidence harness written for the 2026-08-13 EPA public-sites engagement (the zivtech/a11y-audits repo (private), `2026-08-13-epa-public-sites/evidence/harness/audit-pages.mjs`, run against 40 views) into a reusable, generalized reference script: [references/baseline-url-scan.mjs](references/baseline-url-scan.mjs). **When NOT to use:** a single page or component you're actively developing against (→ `.spec.js` + the APG templates in `references/keyboard-test-patterns.md`, or `agent-browser` for quick probing); keyboard operability or screen-reader announcement evidence — this mode never presses a key or captures an announcement (→ keyboard-a11y-tester or virtual-screen-reader); a sitemap-wide sweep where a maintained, hosted CI tool fits better than an in-repo script (→ pa11y-ci, below).

**What it is:** a plain Node script depending only on `playwright` and `@axe-core/playwright` — peer dependencies installed in your own project, never in this repo (this bundle stays prompt-only; see this repo's `CLAUDE.md`). It launches one Chromium browser, visits each URL sequentially with a polite delay between requests, scans with axe-core scoped to this bundle's WCAG 2.2 AA default tag set at each configured viewport — default `1280x800,320x800`, matching the EPA harness's desktop+narrow lineage, override with `--viewports WxH[,WxH...]` — and writes a per-URL JSON result keyed by viewport (rule id, impact, node count, up to 3 sample selectors per viewport) plus an aggregated `summary.json` (violation counts by impact, violations by rule across all pages and viewports). It deliberately drops the EPA harness's other engagement-specific extras — full structure inventory, ARIA snapshot, keyboard tab-trace, text-spacing reflow probe, per-node XPath — to stay a focused baseline tool; reach for `agent-browser` or `keyboard-a11y-tester` when you need those.

Two opt-in flags add non-axe signals, implemented in the sibling [references/census.mjs](references/census.mjs):

- **`--census`** — three DOM-census heuristics, reported under a `census` key on every viewport record, always separate from axe's `violations`/`incomplete` and always labeled detector heuristics, never a conformance verdict: empty paragraphs (no text, no element children), autocomplete-absence (inputs whose type/name/label suggest a WCAG 1.3.5 known purpose but carry no `autocomplete` attribute), and duplicate ids (an id used on more than one element).
- **`--alt-snapshot`** — writes `alt-snapshot.json`: one entry per URL, each a sorted list of every `img`/`svg[role=img]`'s selector, `src_or_title`, and `alt`. Captured once per page (first viewport only — alt text doesn't vary by viewport).

### Install and run

```bash
npm install -D playwright @axe-core/playwright   # peer deps — install in your own project, never in this repo
npx playwright install chromium

node .claude/skills/a11y-test/references/baseline-url-scan.mjs --urls-file urls.txt --out ./baseline-scan-output
# or pass URLs directly, with a custom viewport list:
node .claude/skills/a11y-test/references/baseline-url-scan.mjs --out ./out --viewports 1280x800,320x800 https://example.com https://example.org/page
# with the DOM-census heuristics and an alt-text snapshot:
node .claude/skills/a11y-test/references/baseline-url-scan.mjs --out ./out --census --alt-snapshot https://example.com
```

`urls.txt`: one absolute `http(s)://` URL per line; blank lines and `#`-prefixed lines are ignored. Raise `--delay` (default 500ms) for rate-limited or robots-restricted targets — confirm you're authorized to test the target and check its robots.txt/terms of service before scanning a third party's production site. Exact-pin `@axe-core/playwright` in your own project's `package.json`, since rule availability is per-axe-core-version — the resolved version is recorded as `axe_core_version` in `summary.json` for exactly this reason.

**Catching silent alt-text regressions:** run with `--alt-snapshot` before and after a change, then diff the two `alt-snapshot.json` files —

```bash
node references/baseline-url-scan.mjs --out ./before --alt-snapshot https://example.com/page
# ...make your change...
node references/baseline-url-scan.mjs --out ./after --alt-snapshot https://example.com/page
diff before/alt-snapshot.json after/alt-snapshot.json
```

Any diff line is either an intentional content update or a silent regression — a human confirms which.

### What this mode IS and IS NOT

- **IS for:** baseline and regression sweeps across many pages in one run; machine-readable evidence (rule id, impact, node count, sample selectors) that can feed a11y-critic Phase 0 or the Optional A11y Evidence Finding Contract (§4 below); trend baselines across repeated runs of the same URL list — rerun and diff `summary.json` (or `alt-snapshot.json` for alt-text specifically).
- **IS NOT:** keyboard-operability or screen-reader evidence of any kind — it never presses a key or captures an announcement (route those to keyboard-a11y-tester or virtual-screen-reader). Axe-core is a **detector, not a verdict authority** here, same as every other automated lane in this bundle: it covers roughly 30-40% of WCAG 2.2 issue classes (the same axe-detectable-subset ceiling as the §4 in-spec-file scans below), and its rules are heuristics, not the standard itself. **A clean scan is not a conformance claim** — it means axe found nothing in its rule set on the URLs scanned, nothing more. Treat the output as candidate findings for human review. The `--census` checks are heuristics one level below even axe's rules — pattern-matches on markup shape and naming, not accessibility-tree computation — so their false-positive rate is higher by design; triage every `census` hit by hand before filing it.

### Collector runtime safety

**Classify challenge/block detection — don't substring-match.** A naive check for words like "challenge" or a CDN vendor's name produces false stops on ordinary page content that happens to mention them. Classify instead: a confirmed HTTP 429, or a strong structural match for a known challenge page (not just a keyword), is what triggers a stop. A weak or ambiguous signal (a marketing paragraph naming a security vendor, a support article about outages) must not halt collection.

**A confirmed block is a global stop, not a per-page skip.** When challenge detection does classify a block, stop the entire run rather than skipping just the affected URL — a block on one page is evidence the whole session or IP is affected, and continuing to hit other pages under the same condition wastes the run and can worsen the block.

**Route-settling for dynamic targets.** A dynamic (SPA/client-routed) page's inventory of interactive targets may only be trusted once the route has settled: at minimum, ≥3 stable samples of the target set, an unchanged final URL, and `document.readyState === 'complete'`. Reading targets before settling risks acting on a transient loading state rather than the real page — this applies to any dynamic-route collection, including interactive reconnaissance with `agent-browser`, not only this script.

### pa11y-ci for sitemap-wide sweeps (routed, not vendored)

For a sweep driven by a sitemap rather than a hand-maintained URL list, route to `pa11y-ci` instead of adding sitemap discovery to this script:

```bash
npx pa11y-ci --sitemap https://example.com/sitemap.xml --runner axe --runner htmlcs
```

Same adoption boundary as keyboard-a11y-tester and virtual-screen-reader: a routed external tool the operator installs in their own project, never vendored into this repo.

## Supplemental detector lanes (WAVE, Siteimprove Alfa)

**When to use:** run a second or third independent detector over a page — beyond the primary axe-core + HTML_CodeSniffer-via-`pa11y-ci` lanes — for two reasons, **broad automated coverage** and **aggregate signal**, not to rank one engine against another:

- **Breadth.** The union of what several engines flag is, by construction, a broader automated candidate net than any single engine — more candidates to triage, both true and false. A wider net, not a coverage guarantee; even the union stays inside the ~30–40% of WCAG machines can decide and never closes the manual/AT gap.
- **Aggregate as signal and source.** Where independent engines agree on the same WCAG criterion + target it becomes `corroboration: corroborated` with a `detected_by` list — raised triage confidence, never a verdict (see the Detector-lane authority boundary above). The aggregate is also a source to mine, since engines serialize different detail (Alfa carries computed contrast ratios, WAVE selectors + contrast, axe its own node data).

Both are **detector-only supplemental lanes** — never keyboard, screen-reader, WCAG, or Section 508 verdicts. How much *unique true-positive* coverage the extra engines add over axe alone is not quantified here, and need not be for the lanes to earn their place as breadth + aggregate signal (the one Alfa measurement, 2026-09, found only a small unconfirmed delta). Reopen triggers for treating either as a core stack member live in the Alfa scan adoption assessment and the WAVE adoption assessment under `docs/`.

**Routed, never vendored.** Neither engine is a dependency of this repo. Install and run them in the consuming audit or project, then merge each engine's detections into one A11y Evidence Finding Contract finding (`source`, `detected_by`, `corroboration`) — fingerprint the merged finding once (never per engine, or cross-engine matches never collide), keep `cantTell` distinct from pass/fail, and keep WCAG criterion + level separate from the detector's own result.

### Siteimprove Alfa (Playwright)

Open-source ACT-rules engine (MIT). Install exact-pinned in the consuming project — never in this repo:

```bash
npm install --save-dev --save-exact \
  @siteimprove/alfa-test-utils@0.84.2 \
  @siteimprove/alfa-playwright@0.84.2
```

Record both the wrapper version and the engine version (`@siteimprove/alfa-rules`, `0.119.0` at this writing) — they drift independently. **Level separation is load-bearing:** on real pages most Alfa failures are AAA or advisory, not WCAG 2.2 AA — classify every outcome (`WCAG_2_2_AA` / `AAA` / `ADVISORY` / `UNMAPPED`) and let only AA-scoped outcomes enter the AA queue, still pending independent review. To reach a WCAG criterion from an outcome, join `rule.uri` against the default export of `@siteimprove/alfa-rules` and read each rule's `requirements` where `type === "criterion"`. Alfa's default JSON carries no selector — only an internal serialization id — so a finding needs extra DOM-target serialization before it satisfies the contract's `evidence` field.

### WebAIM WAVE

Commercial tool; the licence is the operator's, not the suite's. Three modes, in priority order:

1. **Observe a user-supplied browser-extension report** — the extension evaluates rendered/dynamic content locally and sends nothing to WebAIM. Record report URL, evaluated URL, state, viewport, timestamp, and the visible category/item totals.
2. **Subscription API** with `WAVE_API_KEY` from the environment. The key travels in the request URL by WAVE's design, so it must never be *recorded* — redact it from any logged URL, log line, evidence file, and error. Credit-metered under the operator's own subscription (100 free credits, then per-credit pricing); no more than two simultaneous requests; **`SKIPPED_CREDENTIAL_REQUIRED` when the key is absent, never a clean result.** Use `reporttype=4` for CSS selectors + contrast data.
3. **Licensed stand-alone engine** an engagement already provides — route to it; never copy or vendor the WAVE engine.

Treat `error` / `contrast` / `alert` as candidate findings and `feature` / `structure` / `aria` as informational unless independent review finds a defect. Map each WAVE item to its WCAG success criterion via WebAIM's documented item→SC mapping; an item that cannot be mapped to a criterion cannot corroborate — it stays `single`.

**Disclaimer (required wherever WAVE evidence appears):** this lane does not authorize WAVE credit purchases, account creation, or credential use. WebAIM's terms do **not** restrict WAVE to non-commercial use; the operative restriction is that selling or redistributing WAVE reports or WAVE-derived data (error counts, listings) — or modifying, copying, licensing, or creating derivative works from WAVE — requires WebAIM's prior permission (https://wave.webaim.org/terms and https://wave.webaim.org/api/, accessed 2026-09-14). So an engagement may retain private, access-controlled evidence and independently validate each defect, but external reporting describes the independently verified defect, not the proprietary WAVE report data.

## 1. Keyboard Accessibility Tests

**MANDATORY: All keyboard tests MUST use real Playwright keyboard interactions against a live or local site. Never check ARIA attributes alone and claim a keyboard test passed — you must actually press keys and verify the result.**

The full keyboard testing detail — required testing method, the 12 WAI-ARIA APG widget-pattern templates, SPA-specific patterns, CSS anti-patterns, and ARIA supplement checks — is in [`references/keyboard-test-patterns.md`](references/keyboard-test-patterns.md).

## Section 5: Time-Based Media Tests

Run these tests when `<video>`, `<audio>`, or media player components are present.

### Caption Infrastructure
- Verify `<track kind="captions">` exists on every `<video>` with speech
- Verify `<track>` has valid `src` pointing to caption file
- Verify caption toggle control exists and is keyboard-accessible

### Transcript Availability
- Verify transcript exists adjacent to media OR a visible link to it
- For audio-only content: verify full text transcript is available

### Media Player Keyboard Access
- Tab: focus enters player controls; all controls have visible focus indicators
- Space: play/pause toggle
- Arrow keys: seek forward/backward; Up/Down: volume control
- C or CC button: caption toggle; Escape: exit fullscreen

### Audio Auto-play
- Verify no audio auto-plays on page load
- If auto-play exists: verify pause/stop control is the first focusable element

## Section 6: Screen Reader Test Protocol

### Test Matrix
| Screen Reader | Browser | Mode |
|---|---|---|
| NVDA | Chrome | Browse mode + Focus mode |
| VoiceOver | Safari (macOS) | Web rotor + standard navigation |
| (Optional) JAWS | Chrome/Edge | Virtual cursor + Forms mode |

### Landmark Navigation Test
- Use landmark navigation (NVDA: D key, VoiceOver: Web rotor)
- Verify: `<main>`, `<nav>`, `<header>`, `<footer>` announced correctly
- Verify: multiple `<nav>` elements have distinguishing `aria-label`

### Heading Navigation Test
- Navigate by headings (NVDA: H key, VoiceOver: Web rotor); verify hierarchy is logical, no skipped levels; `<h1>` present

### Form Mode Test
- Tab into form (NVDA enters focus mode automatically)
- Verify: each input announces its label and "required" if applicable
- Verify: error messages announce when field is focused; `aria-describedby` reads after label

### Live Region Test
- Trigger dynamic content changes (form submission, async updates, notifications)
- Verify: `aria-live="polite"` announces after current speech
- Verify: `aria-live="assertive"` interrupts; toast content announced without focus moving

### SPA Route Change Test
- Navigate between routes; verify page title updates and is announced
- Verify: focus moves to main content or heading; back button restores expected focus

## 2. Visual Regression Tests (REQUIRED)

Visual regression testing — screenshot baselines, dynamic-content handling, contrast, zoom/reflow. See [`references/visual-regression-testing.md`](references/visual-regression-testing.md).

## 3. WCAG Compliance Checks
- 1.1.1 Non-text Content (alt text, aria-labels)
- 1.4.1 Use of Color (link underlines)
- 1.4.3 Contrast Minimum (4.5:1 normal text, 3:1 large text — note: text inside UI components like buttons uses TEXT thresholds, not the 3:1 UI component boundary threshold)
- 1.4.10 Reflow (320px viewport)
- 1.4.11 Non-text Contrast (form borders, focus indicators)
- 2.4.4 Link Purpose (contextual aria-labels)
- 2.4.6 Headings and Labels (no empty headings)
- 2.4.7 Focus Visible (outline visibility)
- 2.4.8 Location (breadcrumbs with aria-current)
- 2.4.11 Focus Not Obscured (focused element not hidden by sticky headers/footers/banners) [WCAG 2.2]
- 2.4.13 Focus Appearance (focus indicator ≥2px perimeter, 3:1 contrast change) [WCAG 2.2]
- 2.5.7 Dragging Movements (drag ops have single-pointer alternative) [WCAG 2.2]
- 2.5.8 Target Size (interactive targets ≥24x24 CSS pixels) [WCAG 2.2]
- 3.3.7 Redundant Entry (don't re-ask for info already provided) [WCAG 2.2]
- 3.3.8 Accessible Authentication (no cognitive function tests for login, paste/autofill supported) [WCAG 2.2]

## 4. Automated Scanning (axe-core via Playwright)

Inject axe-core into live pages via Playwright for automated WCAG violation detection. This catches issues that manual review misses (computed contrast through CSS layers, missing ARIA on dynamically rendered content, landmark coverage).

### axe-core Injection Pattern
```js
// In a Playwright test file (.spec.js)
const { test, expect } = require('@playwright/test');
const fs = require('fs');

test('axe-core accessibility scan', async ({ page }) => {
  await page.goto(BASE_URL);
  await page.waitForLoadState('networkidle');

  // Inject axe-core
  const axeSource = fs.readFileSync(
    require.resolve('axe-core/axe.min.js'), 'utf-8'
  );
  await page.evaluate(axeSource);

  // Run audit
  const results = await page.evaluate(() =>
    axe.run(document, {
      runOnly: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice']
    })
  );

  // Report violations
  const violations = results.violations;
  if (violations.length > 0) {
    const report = violations.map(v => ({
      id: v.id,
      impact: v.impact,
      description: v.description,
      helpUrl: v.helpUrl,
      nodes: v.nodes.length
    }));
    console.log('axe violations:', JSON.stringify(report, null, 2));
  }
  expect(violations.length).toBe(0);
});
```

### Multi-Page Scanning
For sites with multiple routes, scan each page variant:
- Default state (no interactions)
- Loading state (if applicable — trigger a load and scan before it completes)
- Error state (submit an invalid form, then scan)
- Expanded state (open all disclosures/tabs, then scan)

### Dynamic Test Prioritization
After the axe-core scan, use findings to prioritize manual testing effort:
- **axe found ARIA violations** → prioritize screen reader testing (Section 1 keyboard + ARIA checks)
- **axe found color-contrast violations** → prioritize visual inspection (Section 2 focus indicators, link underlines)
- **axe found heading/structure violations** → prioritize keyboard navigation order testing
- **axe found no form violations** → deprioritize form testing with a note that automated checks passed
- **Always test regardless**: focus indicators at zoom, reduced-motion, skip links

### Scale and Sampling (>15 pages)
For large sites, classify pages into template groups and scan one representative per group:
1. Run `discover` phase: list all routes, group by template (list page, detail page, form page, etc.)
2. Select 1-2 pages per template group
3. Scan representatives, report which templates were covered
4. Document sampling strategy in the test report

For audit-scope runs (conformance audits, pre-VPAT work), extend template sampling with WCAG-EM sampling discipline (Steps 3–4 of [WCAG-EM 2.0](https://www.w3.org/TR/wcag-em-2/); verified reference: `docs/wcag-em-2-reference.md`):

5. **Random sample:** add a randomly selected sample of 10% of the structured (template-based) sample, on top, drawn from routes not already selected; record the selection method in the test report
6. **Representativeness check:** if the random sample surfaces content types or violation patterns the structured sample missed, the template classification was not representative — expand the structured sample, re-classify, and repeat until the random sample stops surfacing new finding types
7. **Complete processes:** multi-view journeys (checkout, multi-step applications, auth) are tested end-to-end, never as isolated pages — include every view in the process (the default sequence plus completion-critical branches) and route them to keyboard-a11y-tester driven sessions (see "Goal-driven journey audits" above); per-page scans do not count as process evidence
8. **State coverage:** each sampled page is evaluated in its states (default, loading, error, expanded — the Multi-Page Scanning list above); name the state coverage in the sampling documentation

When the sampling documentation is serialized rather than written as prose, Appendix A of `docs/a11y-evaluation-report-contract.md` shows one way to shape it — a non-normative example, not a schema. Two parts of it are worth carrying even when you write prose: record the actions a complete process needs (a URL alone does not identify a sample inside a process), and identify kiosk, native, and document samples by path description and/or screenshot, since they have no URL.

### Output Format
Report axe-core results alongside keyboard and visual regression results:
```
## axe-core Scan Results
Pages scanned: [count]
Total violations: [count]
Critical: [n] | Serious: [n] | Moderate: [n] | Minor: [n]

### Violations by Rule
| Rule ID | Impact | Description | Pages | Elements |
|---------|--------|-------------|-------|----------|
| color-contrast | serious | Elements must meet color contrast | 3 | 12 |
```

This output feeds directly into the a11y-critic's Phase 0 (Consume Test Evidence) — measured violations become hard evidence in the design review.

### Optional A11y Evidence Finding Contract
When a test produces a failing keyboard, axe-core, visual, static-analysis, or manual finding, include an `A11y Evidence Finding` block for each issue that should be handed to `a11y-critic` or `perspective-audit`. Do not emit placeholder contracts for passing checks or clean fixtures.

Use these fields when evidence exists:
```
### A11y Evidence Finding
finding_id: stable lowercase id, e.g. a11y_form_error_describedby
fingerprint: stable 8-64 char hex hash derived from component/target/rule, not the crawl URL alone
source: test command, test file, axe rule id, agent-browser ref, or observed artifact
wcag_or_apg: WCAG 2.2 criterion or WAI-ARIA APG pattern citation
section_508_fpc_context: Section 508 context only when applicable; Revised Section 508 maps web conformance to WCAG 2.0 Level A/AA
severity: CRITICAL | MAJOR | MINOR | ENHANCEMENT
perspective_alarms: screen_reader_semantic=LOW|MEDIUM|HIGH; keyboard_motor=LOW|MEDIUM|HIGH; etc.
evidence: file:line, DOM excerpt, axe node, screenshot, keyboard trace, or measured value
reproduction_steps: commands or user steps needed to reproduce
expected_behavior: what the user or assistive technology should experience
actual_behavior: what the test observed
trend: new | persistent | worsening | improving | resolved
```

Guidelines:
- Treat WCAG 2.2 AA as the current planning and testing target. Treat Section 508 as regulatory context only when the project scope explicitly requires it.
- Use stable fingerprints to support trend language across reruns. Prefer component name + selector/accessibility target + rule/pattern + criterion over route-only fingerprints.
- Mark perspective alarms only when the evidence suggests a perspective-specific access risk. Any MEDIUM or HIGH alarm can feed `perspective-audit`.
- Do not copy scanner/runtime code or generated dashboard state from external projects into this skill. This contract is a reporting discipline, not a crawler product boundary.

## 5. Static Analysis (eslint-plugin-jsx-a11y) — React/Vue/JSX only

Use when the project uses React, Next.js, Vue, or other JSX/TSX framework. Catches missing alt text, invalid ARIA, and inaccessible element nesting at build time — no running server needed.

### Setup
```bash
# Install as dev dependency
pnpm add -D eslint-plugin-jsx-a11y  # or npm/yarn

# Create temporary standalone config (avoids ESLint 9 flat config issues)
cat > eslint.a11y.mjs << 'EOF'
import jsxA11y from "eslint-plugin-jsx-a11y";
import tseslint from "typescript-eslint";
export default [{
  files: ["src/**/*.tsx", "src/**/*.jsx"],
  plugins: { "jsx-a11y": jsxA11y },
  languageOptions: {
    parser: tseslint.parser,
    parserOptions: { ecmaFeatures: { jsx: true } },
  },
  rules: { ...jsxA11y.flatConfigs.recommended.rules },
}];
EOF

# Run
npx eslint --config eslint.a11y.mjs src/

# Clean up temp config (keep the plugin installed)
rm eslint.a11y.mjs
```

### Known False Positives
Custom component `role` props, ARIA passed via spread, dynamic content loaded post-render, Next.js `<Link>` components (render valid anchors at runtime).

## ICT Testing Baseline coverage crosswalk (declared Section 508 audits only)

When an audit-scope engagement declares Revised Section 508, its baseline-coverage statement is sourced from [references/ict-baseline-crosswalk.yaml](references/ict-baseline-crosswalk.yaml): a hand-built map of all 62 active web baseline tests (pinned at `atbcb/ICTTestingBaseline` `main` @ `6c537a3b`, 2026-08-12) to the execution modes above and the evidence artifact each produces — 22 covered / 26 partial / 13 not-covered / 1 always-passes. The gate is the planner federal profile's conformance floor declaration in the engagement's audit-scope plan: no floor declaration → no baseline citations in any output, and a baseline citation in a component-scope review is a finding against the output. One exemption: an engagement-independent capability statement quoting the crosswalk verbatim ("designed to cover N of 62; gaps: ...") may answer a pre-award/procurement capability question with no floor declaration — findings, reviews, and reports stay gated.

Rules:

- **The not-covered and partial rows are the deliverable.** They name what gets assigned to manual/AT methods in the evaluation plan's sampling and coverage boundary. Never imply stack coverage the crosswalk doesn't grant; a test classified judgment-only in the manifest is never `covered`.
- **Every baseline test ID cited must exist in `docs/ict-baseline-test-id-manifest.yaml` for the web baseline.** IDs are valid per-baseline (`11.A-PageTitled` is web-only; `11.A-DocumentTitled` is documents-only), and baseline IDs are the exact-ID class models fabricate — hand-verify every one; never generate them.
- **Phrasing:** "designed to cover N of 62; gaps: ..." — never "baseline-aligned" or "baseline-conformant" (alignment recognition is an external review of a test process), and never any Trusted Tester certification claim (a DHS credential held by humans).
- **`24.A-Parsing` always passes by upstream design** (WCAG 2.0 Errata 13) — execute nothing for it; report real markup consequences under the SCs they actually break.
- **The Electronic Documents baseline is out of measurement scope entirely** (web-only stack): document samples go to the report's coverage boundary with a manual/AT method, never to these execution modes.
- **Maintenance:** the crosswalk is rebuilt by hand against `docs/ict-testing-baseline-reference.md` on that reference's recheck triggers — a regenerated crosswalk without value-checking is the fabrication failure mode by construction.

## Test Execution Order
1. Static analysis (§5) — fast, no server needed
2. Keyboard accessibility tests (§1)
3. Visual regression tests (§2)
4. axe-core automated scans (§4)
5. WCAG compliance checks (§3)
6. Time-based media tests (§5-media) — if applicable
7. Screen reader tests (§6) — if applicable
8. Report consolidated results with pass/fail counts per section

**Lifecycle integration:** These test results feed into a11y-critic reviews. The full a11y lifecycle is:
plan → [generate test scripts] → critique plan → revise → implement → **test (this skill)** → critique implementation → fix → re-test

Webwright script generation fits between "plan" and "critique plan" — use it to generate test scripts from the planner's output before running them. Generated scripts are inputs to the test phase, not a replacement for it.
