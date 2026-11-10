---
name: pre-submission-report
description: "Run the final, comprehensive submission-readiness gate and consolidate all checks into one dated report; citation-integrity-only mode is also supported. Use when a paper and submission package are nearly final. Not for a mid-draft adversarial review; use $review-cluster."
allowed-tools: Bash(latexmk*, mkdir*, ls*, wc*), Bash(uv:*), Read, Write, Edit, Glob, Grep, Task, Skill
argument-hint: "[path/to/main.tex or no arguments to auto-detect] [--parallel|--citation-integrity-only]"
agent-dependencies: [artifact-coherence-auditor, blindspot, claim-verify, clarity-reviewer, code-paper-auditor, domain-reviewer, paper-critic, referee2-reviewer, reproducibility-auditor]
skill-dependencies: [latex, review-packet, verify-math, venue-guidelines-compliance]
---

# Pre-Submission Report

> Aggregates all quality checks into one dated report. Run before submitting to a journal/conference or sharing with collaborators.

## Output Path

Per `rules/review-artefact-routing.md` (auto-loads in research projects (path-scoped to `paper-*/` and `paper/`)):

- **Source slug:** `pre-submission-report`
- **Write reports to:** `reviews/<paper-slug>/pre-submission-report/<YYYY-MM-DD-HHMM>.md` inside the project, where `<paper-slug>` is the paper directory name being reviewed (e.g., `paper-jtp` if reviewing `paper-jtp/main.tex`). Path is relative to the research project root, not the Task-Management repo.
- **Citation-integrity companion:** when citation integrity runs, write `<YYYY-MM-DD-HHMM>.citation-integrity.json` beside the report. It is a typed companion, not a second report or INDEX row.
- **Never** at project root (`./CRITIC-REPORT.md`-style filenames are forbidden — pre-rule layout).
- **Idempotency:** if the minute-based timestamp file exists, append a same-run descriptor (`{timestamp}-r2.md`, `{timestamp}-revision.md`) — never overwrite.
- **Index policy:** the aggregate pre-submission report is an output-only artefact and receives no `Check=pre-submission-report` row. Each reporting gate/check receives its own row with `Trigger=pre-submission-report`.
- **Infrastructure repos** (Task-Management, atlas-workspace, etc.): this section does not apply — the path-scoped rule won't load there.


## When to Use

- Before submitting a paper to a venue
- Before sharing a draft with supervisors or co-authors
- When the user says "pre-submission check", "is this ready?", "run everything"

## Input

- A `.tex` file path, or auto-detect `paper/main.tex` in the current project

## Critical Rule

**Python:** Always use `uv run python` or `uv pip install`. Never bare `python`, `python3`, `pip`, or `pip3`. Include this in any sub-agent prompts.

## Citation-Integrity-Only Mode

When invoked with `--citation-integrity-only`, do not run compilation, venue-guidelines compliance, general quality review, novelty, code, anonymity, or style checks. Read [`../shared/citation-integrity-receipt.md`](../shared/citation-integrity-receipt.md) and perform only this composition workflow:

1. Enumerate every in-scope manuscript `.tex` file and every loaded external `.bib` file. Exclude `out/`, generated files, and `reviews/`.
2. Resolve the current client's installed skills root. Use `shared/scripts/assemble_integrity_receipt.py manifest` to write a unique `/tmp/citation-integrity-<paper>-<timestamp>.json` with scope `full-manuscript` (or the user's explicit bounded scope).
3. Invoke `bib-validate --verify-doi --citation-integrity-manifest <manifest>`. It performs the bibliography checks once and returns its timestamped Markdown report plus `.citation-integrity.json` component.
4. Launch the fresh-context `claim-verify` agent once. Supply the exact same manifest path and explicitly forbid bibliography identity, DOI, retraction, and version checks. It returns its timestamped Markdown report plus `.citation-integrity.json` component.
5. Run the assembler's `validate` command on both components. If either component is missing or invalid, write the pre-submission Markdown report with overall `INCOMPLETE` and stop; do not infer data from prose reports.
6. Run `assemble` with the two explicit component paths. Write the full JSON to `reviews/<paper-slug>/pre-submission-report/<timestamp>.citation-integrity.json` and a temporary Markdown rendering under `/tmp/`. Copy that rendering into the main pre-submission report, along with links to both source reports.
7. Delete no artifacts. The assembler refuses to merge scope/hash mismatches and refuses to overwrite existing outputs.

Never discover and combine the "latest" component reports implicitly. Reuse is allowed only when the user explicitly supplies both paths and the assembler confirms identical scope, ruleset, and artifact hashes.

Citation-integrity-only mode does not create a manuscript review packet; its frozen citation manifest is the complete bounded artifact contract for that mode.

This mode is an orchestrator only: it does not parse citations, resolve metadata, read sources, judge claims, or change component severities. `bib-validate` and `claim-verify` remain useful individually; each reports its own `PASS|WARN|FAIL` component verdict while correctly marking the combined result `INCOMPLETE`.

## Steps

### 1. Locate the Paper

If no argument provided, search for the main `.tex` file:
1. Check `paper/main.tex`
2. Check `paper/*.tex` for a file containing `\begin{document}`
3. Ask the user if ambiguous

### 2. Integrity Gate (hard gate — must pass before quality checks)

Run these checks first. If any fail or return an incomplete hard-gate verdict, stop and report — do not proceed to quality checks.

1. **Placeholder scan** — grep the `.tex` file(s) for `TODO`, `FIXME`, `XXX`, `TBD`, `[INSERT`, `PLACEHOLDER`, `Lorem ipsum`. Any match is a FAIL.
2. **Bibliography integrity** — create/reuse the frozen artifact manifest, then invoke `bib-validate --verify-doi --citation-integrity-manifest <path>` exactly once. Every `\cite{}` key must resolve to a `.bib` entry. Any missing key is a FAIL. Retain this report and component for Step 3; never rerun the bibliography check in the same pre-submission invocation.
3. **Section completeness** — check that all standard sections exist and are non-empty (Abstract, Introduction, and at least one body section before Conclusion/References). An empty or missing section is a FAIL.
4. **Broken references** — grep for `??` in the compiled PDF output or `.log` file (undefined `\ref{}` or `\cite{}`). Any `??` in output is a FAIL.
5. **Anonymity gate (only if the venue is double-blind)** — load `_shared/double-blind-anonymity-checklist.md` and run **all** P1–P8 paper-side checks. Any FAIL is a hard stop. In particular: P4 (self-citation bib must be blinded if cited paper's author list overlaps the submission's) and P5 (body text must not name authors of self-cited works) — these are the CCS 2026 #1328 desk-reject triggers and require the submission's author list to be loaded from the vault submission frontmatter or prompted from the user. If the artifact has been minted via `anonymous-artifact`, also confirm A1–A9 ran clean for that artifact (state file at `<project>/.anonymous-artifact-state.json`). Skip this entire step only when the user explicitly says "single-blind" or "non-blind".
6. **Venue-guidelines compliance gate** — invoke `venue-guidelines-compliance --trigger pre-submission-report` for the active paper, target venue, content type/track, cycle, and submission stage. Pass any explicit or project-declared guide and official-source URLs already available; otherwise let the compliance skill collect a live official-source set when access permits. It establishes or reuses one current `out/` PDF and binds the report to the PDF and guideline evidence. The gate passes only on exact `PASS`. Treat `FAIL`, `INCOMPLETE`, a missing report, or any artifact/guideline-evidence mismatch as a hard stop. If no target venue is declared or sufficient current official evidence cannot be established, the result is `INCOMPLETE`; do not guess or downgrade this to an advisory.
7. **Token conservation vs prior round (advisory — never a FAIL by itself)** — when a prior submitted/reviewed version of the manuscript exists (a `backup/` copy, an as-submitted archive, or a git tag), run `uv run python .scripts/check_token_conservation.py --source <prior>.tex --revision <current>.tex` per main file. List each advisory row (changed number, dropped/added citation, protected-term delta) in the report with whether an authorizing revision item covers it; unexplained deltas are flagged for the human, and claim-bearing rewordings are spot-checked against the claim-strength ladder (`docs/reference/claim-strength-ladder.md`). Skip silently when no prior version exists (first submission).
8. **Arithmetic forensics (HARD findings block; NOTE/CONDITIONAL advisory)** — run `uv run python .scripts/check_stat_forensics.py <main>.tex` on every empirical paper. It recomputes reported p-values from t/r statistics and df, checks df against reported N, recomputes t from descriptive pairs, and GRIM-checks 2-decimal means at n < 100 — the defect class LLM reviewers demonstrably miss (review-fleet baseline 2026-07-24: 0/4). A HARD finding (impossible p, df ≥ N, t contradicting descriptives) is treated like any other integrity FAIL unless the human confirms a legitimate design explanation (one-tailed test, corrected p, Welch df); CONDITIONAL GRIM rows are surfaced for judgment (integer-valued measures only). Theory-only papers with no reported test statistics: the checker returns CLEAN and costs nothing.
9. **Prepare the final-gate review input** — after the current PDF and source hashes are established, invoke `review-packet` in `fresh-review` mode. Record the archive path, archive SHA-256, and canonical PDF SHA-256 when the packet is sealed. All later reviewer prompts and the aggregate report refer to this exact packet. If the source changes, the packet is stale and the gate restarts; this packet is not the human-supplied submission archive.

**If any check fails:**
```
INTEGRITY GATE: FAIL

Blockers (must fix before quality checks):
  - [ ] 3 TODO placeholders found (lines 47, 112, 289)
  - [ ] 2 undefined references (\ref{fig:missing}, \cite{nonexistent2024})
  - [ ] Abstract section is empty

Fix these and re-run pre-submission-report.
```

**If all pass:** proceed to Step 3.

### 3. Run Quality Checks

Two modes:

#### 3a. Sequential (default — fast, deterministic)

Run these in order — each depends on a clean state from the previous:

1. **Compilation** — reuse the current PDF produced during the venue-guidelines compliance gate when its source hashes still match. Otherwise invoke `latex` on the main `.tex` file. Record pass/fail and any remaining warnings.
2. **Citation audit** — reuse the `bib-validate` report and component produced by Integrity Gate step 2. Record missing, unused, suspect, unresolved-DOI, retraction/update, and version findings; do not invoke the skill a second time.
3. **Adversarial review** — launch `paper-critic` agent (via fresh-context sub-agent mechanism). Capture the CRITIC-REPORT.md score and findings.

#### 3b. Parallel comprehensive fan-out (`--parallel` flag)

Use when (a) the paper is near submission and you want a comprehensive scan, or (b) the user explicitly asks for the "full pre-submission swarm". The venue-guidelines compliance gate runs first and is outside this fan-out. After it passes, run **14 independent checks** through their canonical skills/agents, dispatching the read-only agent checks in parallel, then consolidate findings.

**Hard rules for parallel mode:**
1. **All sub-agents are read-only with respect to project files under review** — see `subagent-write-guard.md` rule. They do NOT modify the paper, bib, code, or any other artefact under review; the orchestrator (this skill) decides what to fix. **They DO write their own per-agent reports** to `reviews/<paper-slug>/<check>/<YYYY-MM-DD-HHMM>.md` per each agent's "Log to REVIEW-STATE.md (final step)" instruction (where `<paper-slug>` is the paper being reviewed and `<check>` is the agent name, e.g., `paper-critic`, `referee2-reviewer`) — this is the durable record + the INDEX.md stamp that `review-recap` reads. The "read-only" scope is the artefact under review, NOT a prohibition on writing the review report itself.
2. **Each sub-agent gets the standard forbid-list** — no git, no latexmk, no edits to files outside their scope. The forbid-list explicitly carves out the `reviews/<paper-slug>/<check>/` path as a permitted write target (the agent's logging step needs it), where `<paper-slug>` is the paper being reviewed (passed in the dispatch) and `<check>` is the agent name.
3. **Findings consolidate into a P0/P1/P2 fix list** before any edits — single triage point, not 14 streams. Sub-agents return structured findings to the orchestrator in addition to writing their report file; the consolidate step uses the structured returns.
4. **No edit phase auto-runs** — the user reviews the consolidated report and approves which fixes to apply.
5. **Evidence contract + spot-verify** (per [`_shared/audit-integrity.md`](../_shared/audit-integrity.md) Rule 2). Each sub-agent's dispatch prompt MUST require **every finding to cite `path:line` (or `§`) AND quote the exact text/code verbatim** — unanchored findings are inadmissible. Before consolidating (rule 3), the orchestrator **spot-verifies a random sample** of returned findings (≥3, or 20%, weighted to P0/P1): open the cited location, confirm the quote is there and the claim follows. Any miss ⇒ widen to that agent's full set and **drop** what can't be grounded. Record `Integrity: N sampled, M dropped` in the consolidated report.

Before starting citation checks, create the frozen artifact manifest described in Citation-Integrity-Only Mode. Pass it unchanged to rows 1 and 2, validate their components, and assemble the full citation-integrity companion. Do not dispatch a shadow `bib-verifier`; row 1 is the existing `bib-validate` result retained from Integrity Gate step 2.

**Always run (14 checks):**

| # | Agent | Scope | Output |
|---|---|---|---|
| 1 | **bibliography component** | Reuse the one `bib-validate --verify-doi --citation-integrity-manifest <path>` invocation from Integrity Gate step 2; DOI/metadata, retraction/update, version, and citation-inventory checks | Bib report + validated component JSON |
| 2 | **claim-verifier** | Launch `claim-verify` agent once with the same manifest — checks every cited claim against the source paper and performs no bibliography checks | Claim report + validated component JSON |
| 3 | **novelty-reviewer** | Run `scholarly scholarly-search "<paper title>" --source openalex`; report score + threats not yet cited | Novelty score + missing-related-work list |
| 4 | **paper-critic** | Launch `paper-critic` agent — general adversarial CRITIC-REPORT (specialist mode for venue-calibrated review) | Scored CRITIC-REPORT.md |
| 5 | **domain-reviewer** | Launch `domain-reviewer` agent — math/derivations/assumptions/code-theory alignment | DOMAIN-REVIEW.md |
| 6 | **referee2-reviewer** | Launch `referee2-reviewer` agent — Reviewer 2 hostile read; top reviewer-attack-surface concerns | Adversarial concerns |
| 7 | **blindspot** | Launch `blindspot` agent — peripheral-vision audit (vices in plain sight + virtues being overlooked) | Blindspot report |
| 8 | **code-paper-auditor** | Launch `code-paper-auditor` agent — cross-check quantitative claims against source code outputs | Mismatch table |
| 9 | **artifact-coherence-auditor** | Launch `artifact-coherence-auditor` agent — paper prose vs replication outputs (catches hallucinated results) | Coherence report |
| 10 | **reproducibility-auditor** | Launch `reproducibility-auditor` agent — workflow rerunnability (hidden deps, absolute paths, env assumptions) | Reproducibility report |
| 11 | **anonymity / double-blind checker** | Apply paper-side checks P1-P8 from `_shared/double-blind-anonymity-checklist.md`; verify `[review]` mode if double-blind venue | Pass/fail + leak list |
| 12 | **page-limit + LaTeX validator** | Verify page count under venue limit; check for compile warnings; check `out/` is current | Page count + warning summary |
| 13 | **AI-detection** | If an AI-detection workflow is installed and configured, run it and flag hot zones for an optional humanizing pass; otherwise report `SKIPPED (unavailable)` and perform a manual prose-pattern review | Per-segment scores + hot-zone count, or explicit skip reason |
| 14 | **clarity-reviewer** | Launch `clarity-reviewer` agent — bounded-context ingestion stress test (Predicted ingestion risks + C1–C11 adjudication, including the terminology/jargon ledger; `pass1_validity: UNCONTROLLED` in this single-dispatch form). When the paper's prior referee reviews contain readability complaints, prefer the `clarity-review` skill instead (CONTROLLED, observed events) — run it before the fan-out and reuse its report here. | Clarity report (verdict CLEAR/TIGHTEN/HARD-TO-INGEST + terminology ledger + Blockers/Quick wins) |

**Conditional — math verification (theory papers):**

If the paper contains formal environments (`grep -lE '\\begin\{(theorem|proposition|lemma|corollary)\}'` matches), run `verify-math` (via the skill-routing mechanism) on the model section(s) **in addition to** the domain-reviewer agent (#5). The two are complementary, not redundant: domain-reviewer (#5) reads the conceptual layer (rung R0), while `verify-math` machine-checks the algebra/analytics across the rest of the spectrum (R1 numerical falsification · R2 symbolic/CAS · R3 Lean). This runs as an **orchestrator skill, not a sub-agent** — the computational rungs need Bash + sympy/lean, which sub-agents can't reliably get at runtime (same Bash-grant fragility that motivates orchestrator-side stamping below); the orchestrator always has Bash. It is read-only with respect to project files (writes only its own report) and self-stamps its INDEX.md row. Fold its aggregate verdict into consolidation: **any `FALSIFIED` obligation is a P0 blocker** (a machine-falsified theorem outranks any reviewer concern); an `INCONCLUSIVE` obligation is P1. When both run, tell domain-reviewer (#5) in its prompt that the algebra is being verified separately so it focuses on assumption completeness / citation fidelity / backward logic — see the domain-reviewer "Math R0 Mode" preset.

**Conditional follow-ups (run after parallel fan-out, opt-in):**

| Trigger | Skill |
|---|---|
| Paper has code (detect: non-tex/non-bib files in project) AND venue is double-blind | `anonymous-artifact` — assemble + sanitize + push to anonymous repo, mint URL |
| Swarm yields multiple blocking or interdependent issues | `strategic-revision --internal <synthesis-or-report-path>` — executable DAG after internal review; genuine referee comments are handled separately by `--external` |

The conditional follow-ups are NOT in the parallel batch — they're sequential because they may modify files (and so violate the read-only invariant of the parallel sub-agents).

**Dispatch protocol:**

```python
# Pseudocode for orchestration — see fresh-context sub-agent mechanism docs for actual API
parallel_tasks = [
    Agent("claim-verify",
          prompt=f"Audit claim fidelity in {paper_path}. Use artifact manifest {manifest_path} unchanged. Do not re-run bibliography checks. READ-ONLY except declared report + sidecar. {forbid_list}"),
    Agent("novelty-reviewer", ...),
    # ... remaining agent checks
]
# Run bibliography work once through its canonical skill, outside the agent fan-out.
bib_component = Skill("bib-validate", f"--verify-doi --citation-integrity-manifest {manifest_path}")
# Wait all → consolidate
findings = consolidate_p0_p1_p2([bib_component, *parallel_tasks])
```

Sub-agents run concurrently — total wall-clock is bounded by the slowest (typically novelty-reviewer at ~2-3 min via OpenAlex).

**Consolidation:** the orchestrator merges findings from all 14 checks into a single P0/P1/P2 fix list:
- **P0 (block submission):** any venue-guidelines compliance verdict other than exact `PASS`, anonymity leaks (#11), fabricated bibliography records (#1), materially false or load-bearing unverifiable claims (#2), compilation errors (#12), over-page-limit (#12), code-paper mismatches (#8), prose-replication divergence (#9), **any `FALSIFIED` math obligation (`verify-math`, theory papers)**
- **P1 (must fix):** unresolved DOIs (#1), claim-verify failures (#2), novelty threats (#3), critic-report Major issues (#4), domain-review math errors (#5), reproducibility issues (#10), referee2-reviewer concerns (#6), **`INCONCLUSIVE` math obligations (`verify-math`)**
- **P2 (should consider):** blindspot virtues + minor vices (#7), AI-detect hot zones (#13), critic-report Moderate/Minor issues (#4), novelty positioning (#3)

**Code-bearing detection:** if the project has non-tex / non-bib files outside `paper-*/` and `notes/` (typical signal: `code/`, `data/`, `scripts/`, `analysis/`, `src/` directories), enable code-side sub-agents (#8 code-paper-auditor, #9 artifact-coherence-auditor, #10 reproducibility-auditor) and queue `anonymous-artifact` as a conditional follow-up.

**Edit phase (separate, opt-in):** if the user approves any P0/P1 fixes, dispatch a *second* round of edit-agents with **explicit scoped permissions per file** — see `subagent-write-guard.md` for the forbid-list pattern. The orchestrator confirms each edit-agent's scope before dispatch.

**Why parallel:** the independent agent audits can overlap safely because they are read-only. The bibliography component remains an orchestrator-run skill so DOI/metadata work is never duplicated by a shadow agent.

**Skip parallel mode if:** paper is in early drafting (use the sequential 3-audit instead — faster feedback for incomplete drafts), or sub-agents fail repeatedly (fall back to sequential).

### 4. Aggregate Report

Save to the canonical `reviews/<paper-slug>/pre-submission-report/<YYYY-MM-DD-HHMM>.md` path declared above:

```markdown
# Pre-Submission Quality Report

**Project:** <project name>
**Date:** YYYY-MM-DD
**File:** <path to main.tex>
**Target:** <venue from project CLAUDE.md, or "not specified">
**Review packet:** <path, archive SHA-256, canonical PDF SHA-256>

---

## Integrity Gate: PASS / FAIL / INCOMPLETE

- **Placeholders:** 0 found
- **Citation integrity:** all keys resolved
- **Section completeness:** all sections present
- **Broken references:** none
- **Venue guidelines compliance:** PASS / FAIL / INCOMPLETE — `<report path>`

## Venue guidelines compliance

- **Verdict:** PASS / FAIL / INCOMPLETE
- **Canonical guide:** `<path, last_verified_at, SHA-256>`
- **Audited artifact:** `<PDF path and SHA-256>`
- **Mandatory requirements:** <passed>/<applicable>
- **Blockers or unresolved evidence:** <none or concise list>

---

## Overall Score: XX/100 — [Verdict]

Verdict uses the quality scoring framework:
- 90-100: Publication-ready
- 80-89: Minor revisions needed
- 70-79: Significant revisions needed
- Below 70: Not ready

---

## Compilation

- **Status:** PASS / FAIL
- **Warnings:** <count>
- **Details:** <brief summary of any issues>

## Citations

- **Citation-integrity receipt:** PASS / WARN / FAIL / INCOMPLETE
- **Receipt companion:** `<same-stem>.citation-integrity.json`
- **Bibliography component:** PASS / WARN / FAIL
- **Claims component:** PASS / WARN / FAIL / NOT RUN
- **Missing keys:** <count> — <list>
- **Unused keys:** <count> — <list>
- **Suspect entries:** <count> — <list>

## Adversarial Review

- **Score:** XX/100
- **Key findings:**
  - <finding 1>
  - <finding 2>
  - ...

## Research Quality Score

Load `skills/shared/research-quality-rubric.md` and report the weighted aggregate (X.X / 5.0) with verdict.

## Remaining Issues

| # | Severity | Category | Issue |
|---|----------|----------|-------|
| 1 | High/Medium/Low | Compilation/Citation/Content | <description> |

## Recommendation

**[Submit / Revise / Not ready]**

<1-2 sentence summary of what needs to happen before submission>
```

The recommendation may be `Submit` only when the venue-guidelines compliance verdict is exact `PASS` and its recorded artifact and guideline evidence match the aggregate report. A quality score cannot override this gate.

### 5. Present Summary

Display the report path and the summary table to the user. If the recommendation is "Submit", congratulate. If "Revise", list the top 3 issues to fix first.

## Error Handling

- If compilation fails after `latex`, still run the remaining checks. Mark compilation as FAIL in the report.
- If `paper-critic` agent fails, note it in the report and base the overall score on compilation + citations only.
- If either citation component is missing, invalid, or hash-incompatible, mark citation integrity `INCOMPLETE`; never promote the surviving component to a full PASS.
- If sufficient current official guideline evidence is missing, stale, out of scope, or cannot be tied to the current artifact, record venue-guidelines compliance as `INCOMPLETE`, set the recommendation to `Not ready`, and name the evidence needed to unblock it.
- Always produce the report file, even if some checks failed.

## Integration

| Skill/Agent | Role in this workflow |
|-------------|---------------------|
| `latex` | Compilation + auto-fix |
| `review-packet` | Defines and optionally seals the exact manuscript/source decision surface audited by the final gate; distinct from the as-submitted archive |
| `venue-guidelines-compliance` | Resolves an explicit guide, project-declared guide, or live official-source set, then runs a fresh hard-gate audit; exact `PASS` required |
| `bib-validate` | Bibliography component: citation inventory, identity/DOI, retraction/update, and version status |
| `claim-verify` agent | Claims component: claim attachment, strength/scope, source access, and quotation fidelity |
| `assemble_integrity_receipt.py` | Mechanical validation, exact-hash compatibility check, verdict derivation, and receipt rendering; performs no research checks |
| `paper-critic` agent | Adversarial content review |
| `quality-scoring.md` | Verdict thresholds |
| `_shared/double-blind-anonymity-checklist.md` | P1–P8 / A1–A9 anonymity gate (double-blind venues only) |
| `_shared/audit-integrity.md` | Fan-out integrity contract — each agent-produced finding must cite `path:line` + verbatim evidence (Rule 2); the orchestrator spot-verifies before including it in the report |

## REVIEW-STATE.md propagation (orchestrator-side stamping)

This skill is an **orchestrator** in the REVIEW-STATE.md schema. As of the 2026-05-19 architecture change, the orchestrator handles all stamping; sub-agents emit directives but do not call the helper themselves.

### Required orchestrator behaviour

When constructing prompts for any sub-agent that is a logging tool (paper-critic, referee2-reviewer, peer-reviewer, domain-reviewer, claim-verify, blindspot, clarity-reviewer, fatal-error-check, code-paper-auditor, artifact-coherence-auditor, reproducibility-auditor, code-review), include this line in the sub-agent prompt:

> Emit a `review-state-stamp` directive at the end of your final response per the installed shared resource `_shared/stamp-directive-spec.md`. Set `trigger: pre-submission-report` (or omit — this orchestrator overrides). Do not call the stamping helper yourself.


### After each sub-agent returns

For each agent's return:

1. Write the agent's final response to a temp file (`/tmp/pre-submission-<agent>.md`).
2. Parse the directive:
   ```bash
   ARGS=$(bash <skills-root>/_shared/parse-stamp-directive.sh /tmp/pre-submission-<agent>.md)
   ```
   If `parse-stamp-directive.sh` exits non-zero, log a warning ("Agent X return did not contain a review-state-stamp directive — INDEX.md not updated for this run") and continue.
3. **Verify the `.md` report file exists; reconstruct from return content if missing:**
   ```bash
   VERIFY=$(bash <skills-root>/_shared/post-dispatch-verify.sh \
       --return-file /tmp/pre-submission-<agent>.md \
       --project "$PROJECT_ROOT" \
       --agent <agent>)
   ```
   If `VERIFY` starts with `RECONSTRUCTED`, append `(report reconstructed by orchestrator — agent skipped Write)` to the `--notes` value before stamping. Guards against the blindspot-class failure mode. See `log/2026-05-21-blindspot-write-fix.md`.
4. Stamp with the orchestrator's `--trigger` override:
   ```bash
   eval bash <skills-root>/_shared/review-state-log.sh "$ARGS" \
       --trigger pre-submission-report \
       --source agent \
       --project "$PROJECT_ROOT"
   ```
5. Clean up the temp file.

All sub-agent stamps land in `<project>/reviews/INDEX.md` with `Trigger=pre-submission-report` and roughly the same `Last Run` timestamp.

### Why the orchestrator stamps (not the sub-agent)

Agents have inconsistent Bash tool grants at runtime (the 2026-05-19 harness investigation). The orchestrator always has Bash and always runs after the agents return. Moving stamping here decouples it from agent tool-surface uncertainty and fixes the burying problem (referee2-reviewer's stamping section used to live at line ~475 of a 518-line agent definition; agents reliably forgot to reach it).

Schema: the installed shared resource `shared/review-state-schema.md`.
Stamp directive format: the installed shared resource `_shared/stamp-directive-spec.md`.
