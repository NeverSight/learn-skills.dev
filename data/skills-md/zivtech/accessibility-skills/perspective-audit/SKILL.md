---
name: perspective-audit
description: "Deep accessibility review from 7 access perspectives — activated by escalation from a11y-planner or a11y-critic when one or more perspectives are flagged at MEDIUM or HIGH alarm level."
license: Apache-2.0
compatibility: Claude Code-compatible; protocol is model-agnostic
metadata:
  author: zivtech
  version: "1.0.1"
disallowedTools:
  - Write
  - Edit
  - NotebookEdit
---

# Perspective Audit

Deep-layer accessibility review for perspectives escalated to MEDIUM or HIGH by the a11y-planner or a11y-critic. This skill reads the JTBD checklists only for the escalated perspectives, applies severity calibration, routes findings by ARRM role, and splits code-level findings from content-level flags.

This is Layer 2 in a hybrid accessibility architecture:
- **Layer 1**: a11y-planner and a11y-critic produce alarm levels (LOW / MEDIUM / HIGH) per perspective as lightweight hints.
- **Layer 2** (this skill): Runs the full JTBD checklist only for perspectives at MEDIUM or HIGH. Perspectives at LOW are not reviewed.

## When to Use

Invoke this skill when:
- a11y-planner or a11y-critic outputs a perspective alarm at **MEDIUM** or **HIGH**
- You need granular, per-perspective findings with WCAG citations and ARRM routing
- A design review surfaces concern about a specific access dimension (motion, contrast, auditory, cognitive) that warrants a dedicated checklist pass

Do not use this skill to review perspectives the planner/critic rated LOW. Evidence over assertion — this skill only fires where the risk signal exists.

## The 7 Perspectives

| # | Perspective | WCAG Criteria (AA) |
|---|---|---|
| 1 | Magnification & Reflow | 1.4.4, 1.4.10, 1.4.12, 1.4.13, 2.4.11 |
| 2 | Environmental Contrast | 1.3.3, 1.4.1, 1.4.3, 1.4.11 |
| 3 | Vestibular & Motion Sensitivity | 2.2.2, 2.3.1, 2.5.4 |
| 4 | Auditory Access | 1.2.1, 1.2.2, 1.2.3, 1.2.5, 1.4.2 |
| 5 | Keyboard & Motor Access | 1.3.4, 2.1.1, 2.1.2, 2.4.1, 2.4.3, 2.4.7, 2.4.13, 2.5.1, 2.5.2, 2.5.3, 2.5.7, 2.5.8 |
| 6 | Screen Reader & Semantic Structure | 1.1.1, 1.3.1, 1.3.2, 2.4.2, 2.4.4, 2.4.6, 3.1.1, 3.1.2, 3.3.1, 3.3.2, 4.1.2, 4.1.3 |
| 7 | Cognitive & Neurodivergent | 1.3.5, 2.2.1, 2.4.5, 3.2.1, 3.2.2, 3.2.3, 3.2.4, 3.2.6, 3.3.3, 3.3.4, 3.3.7, 3.3.8 |

## Severity Calibration

| Severity | When to Apply |
|---|---|
| CRITICAL | Blocks access entirely — keyboard trap, no captions on speech video, CAPTCHA with no alternative |
| MAJOR | Significant barrier for the perspective's user group — contrast below 3:1, motion without prefers-reduced-motion, missing error association |
| MINOR | Degrades experience but workaround exists — suboptimal label text, jargon defined nearby, help location slightly inconsistent |
| ENHANCEMENT | AAA criterion — report but do not escalate to MAJOR/CRITICAL regardless of implementation gap |

## Steps

### Step 1 — Confirm escalated perspectives

Read the planner or critic output to identify which perspectives are flagged MEDIUM or HIGH. List them explicitly before proceeding. If no escalation list is provided, ask: "Which perspectives did the planner or critic flag at MEDIUM or HIGH?"

Do not run checklists for perspectives at LOW.

### Step 2 — Read reference files

Read both reference files at invocation:

1. `.claude/skills/perspective-audit/references/perspectives.md` — Read **only the sections** for escalated perspectives. Do not load sections for LOW-rated perspectives.
2. `.claude/skills/perspective-audit/references/arrm-perspective-mapping.md` — Read in full for finding routing.

### Step 3 — Read the artifact under review

Read all source files relevant to the escalated perspectives. Understand the component structure, markup, CSS, and any JS handling state or interaction before running checklists.

When the artifact is a live page rather than source, gather its evidence in a single per-page capture (a11y-test's `references/page-audit.mjs`, or one accessibility-tree pass) and run every escalated perspective's checklist against that one capture — do not re-inspect the page once per perspective. One page's evidence serves all its perspectives.

### Step 4 — Run per-perspective checklists

For each escalated perspective:

1. Work through the JTBD checklist from `references/perspectives.md` item by item.
2. For each checklist item:
   - Mark PASS if the implementation satisfies the criterion with evidence (file:line or observed markup).
   - Mark FINDING if not satisfied — generate a finding using the format in Step 5.
   - Mark N/A if the criterion does not apply (e.g., no video present for Auditory Access caption checks).
3. Check all red flags listed for the perspective — any red flag that fires is automatically CRITICAL.
4. Separate code-level findings (enforceable from source) from content-level findings (require human verification).

### Step 5 — Format each finding

Use this format for every finding:

```
**Finding:** [clear description of what is wrong]
**WCAG:** [criterion number and name — e.g., 2.4.7 Focus Visible]
**Perspective:** [which perspective]
**Severity:** CRITICAL | MAJOR | MINOR | ENHANCEMENT
**Route to:** [ARRM primary role] (secondary: [role])
**Evidence:** [file:line citation or observed markup/CSS]
**Fix:** [specific recommended action]
```

If the audit was invoked from an `A11y Evidence Finding` block, preserve these traceability fields in the finding when available:

```
**Finding ID:** [finding_id]
**Fingerprint:** [fingerprint]
**Source:** [source test, snapshot, axe rule, or critic finding]
**Trend:** new | persistent | worsening | improving | resolved
**Perspective alarms:** [incoming alarms and any updated alarm levels]
```

When the incoming contract's evidence is `keyboard-a11y-tester` journey-audit output (trace steps, deterministic findings, reading-order census): map its personas to alarms — `keyboard` findings feed `keyboard_motor`, `screen-reader` findings feed `screen_reader_semantic` — and keep trace-step and census-selector citations intact through the audit. Batch-crawl 4.1.3 findings arrive as verification prompts, not failures; require driven-session `live_announcements` evidence before treating a live-region defect as confirmed (calibration: `evals/results/keyboard-a11y-tester/`).

When the incoming contract's evidence is `virtual-screen-reader` component-assertion output (spoken-phrase logs from the a11y-test component lane): findings feed `screen_reader_semantic` only — never `keyboard_motor`, because VSR interactions are synthetic. Keep the tool version + test file + exact-phrase citations intact through the audit. Silence is confirmable evidence only when the structural absence (no role/aria-live) is attached; a silent mount-with-content `role="alert"` is inconclusive, and an empty `"polite: "` entry marks an `aria-atomic` region clear (calibration: `evals/results/virtual-screen-reader/`).

Perspective-audit may also emit a contract-compatible block for new CRITICAL or MAJOR findings discovered during the deep review:

```
### A11y Evidence Finding
finding_id: [stable lowercase id]
fingerprint: [stable 8-64 char hex hash]
source: perspective-audit [perspective name] checklist
wcag_or_apg: [WCAG 2.2 criterion or WAI-ARIA APG pattern]
section_508_fpc_context: [Revised Section 508/WCAG 2.0 A-AA context if applicable, or "not in scope"]
severity: [CRITICAL | MAJOR | MINOR | ENHANCEMENT]
perspective_alarms: [perspective=LOW|MEDIUM|HIGH list]
evidence: [file:line, observed markup/CSS, or human-verification boundary]
reproduction_steps: [steps, command, or "source review only"]
expected_behavior: [expected user/AT behavior]
actual_behavior: [observed behavior]
trend: [new | persistent | worsening | improving | resolved]
```

Rules:
- Every finding must cite a WCAG criterion. No finding without a citation.
- AAA criteria are always ENHANCEMENT — never escalate them to MAJOR or CRITICAL.
- Content-level findings append: `[Human verification required — cannot be confirmed from source]`
- Code-level findings must include file:line evidence.
- Preserve ARRM routing even when using the contract block; the contract adds traceability, not ownership by itself.

### Step 6 — Compile the summary

After all escalated perspectives are reviewed, output the combined summary:

```
## Perspective Audit Summary

**Component/artifact reviewed:** [name]
**Perspectives escalated for deep review:** [list]
**Perspectives at LOW (not reviewed):** [list]

### Findings by Severity

| Severity | Count |
|---|---|
| CRITICAL | N |
| MAJOR | N |
| MINOR | N |
| ENHANCEMENT | N |

### Perspectives That Passed

[List perspectives where all checklist items were PASS or N/A]

### Perspectives With Findings — Grouped by ARRM Role

**Front-End Dev**
- [Finding title] — [Perspective] — [Severity] — [WCAG criterion]

**Visual Design**
- [Finding title] — [Perspective] — [Severity] — [WCAG criterion]

**UX Design**
- [Finding title] — [Perspective] — [Severity] — [WCAG criterion]

**Content Author**
- [Finding title] — [Perspective] — [Severity] — [WCAG criterion]

### Open Questions Requiring Human Verification

[List all content-level findings that cannot be confirmed from source — caption accuracy, transcript completeness, audio description coverage, reading level, alt text quality for editorial images]

### Recommended Next Step

[One of: PASS (no CRITICAL/MAJOR findings), REVISE (MAJOR findings present — address before shipping), BLOCK (CRITICAL findings present — do not ship until resolved)]
```

## Companion Skills

- **a11y-planner**: Layer 1 upstream — produces alarm levels that trigger this skill.
- **a11y-critic**: Layer 1 upstream — produces alarm levels that trigger this skill. Also reviews design decisions post-implementation.
- **a11y-test**: Run after findings are addressed — verifies fixes with automated scans and keyboard tests.

## Reference Files

- `.claude/skills/perspective-audit/references/perspectives.md` — JTBD checklists, red flags, and evidence requirements for all 7 perspectives.
- `.claude/skills/perspective-audit/references/arrm-perspective-mapping.md` — ARRM role routing decision tree and finding output format.
