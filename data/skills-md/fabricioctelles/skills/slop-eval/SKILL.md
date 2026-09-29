---
name: slop-eval
description: >
  Objectively evaluate a UI/web design against the pols.dev anti-slop design
  law: detect catalogued slop tells with cited evidence, score 8 weighted
  axes (color, type, components, layout, motion, execution, signature,
  cohesion), and emit a Slop Report with a 0–100 Slop Index and grade. Use
  when the user asks to "evaluate design slop", "slop report", "is this
  design AI slop", "audit this landing page design", "de-slop review", or
  wants an objective score of how generic/machine-made a design looks. To
  fix text (not design), use human-ai or humanizar skills instead.
metadata:
  author: https://ft.ia.br
  version: "1.1.0"
  date: 2026-08-24
  repository: https://github.com/fabricioctelles/skills
  license: Apache-2.0
  category: code-quality-and-review
---

# Slop Eval

Evaluate a design the way `skill-evaluation` evaluates a skill: every finding
cites concrete evidence, every axis gets a 0–100 score, arithmetic runs
through a script, and the output is a structured report — never a vibe check.

The tell catalog lives in `references/tells.md`; read it before sweeping.
The positive rubric (signature formula, cohesion checks, slop→premium pairs,
and the "Adding Soul" guide) lives in `references/premium-markers.md`; read
it before scoring Axes 7–8 and when writing fix prescriptions.
The design context guide lives in `references/contexts.md`; read it to adjust
priorities and tolerances based on the type of design being evaluated.

## Source

- [The pols.dev anti-slop design law](https://pols.dev/slop.md) — the tell
  catalog, absolute rules, and signature formula are distilled from it.
- Method modeled on
  [skill-evaluation](https://github.com/fabricioctelles/skills/tree/main/skills/skill-evaluation)
  (cite-or-cut, weighted axes, scripted scoring, failure-mode diagnosis).

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `target` | What to evaluate: live URL, screenshot(s), code path, or Figma export | Ask user |
| `brief` | Brand brief or explicit user directions the design followed | None |
| `context` | Design type: `landing`, `saas`, `editorial`, `ecommerce`, or `auto` | `auto` |
| `output` | Path to write the report | `./SLOP-REPORT.md` |
| `compare` | Path to a previous report for tracking mode (temporal evolution) | None |

Write the report in the language the user is speaking; keep tell IDs and
names in English so they stay greppable against the catalog.

## Evaluation modes

### Standard mode (default)

Single evaluation of a design. Produces a Slop Report with scores, tells,
section ledger, and prioritized fixes.

### Comparison mode

Side-by-side evaluation of two different designs (e.g., competitor analysis,
A/B variants). Add `--compare` pointing to another target or existing report.

### Tracking mode

Evaluate the same design over time to measure improvement. Use when:
- Running weekly/sprint design reviews
- Measuring progress after a redesign
- Validating that fixes actually moved the score

Usage:
```bash
# First evaluation — establishes baseline
slop-eval --target https://site.com --output ./reports/baseline.md

# Later evaluation — tracks evolution
slop-eval --target https://site.com --output ./reports/week-2.md \
  --compare ./reports/baseline.md
```

Tracking mode adds to the report:
- Score progression table with trends (✅ improved / ⚠️ regressed)
- Tells resolved (what got fixed)
- New tells (what got introduced)
- Regressions (axes/sections that got worse)
- Section ledger evolution
- Velocity metrics (tells resolved per week, score improvement rate)
- Recommendations for next iteration

See `references/output-template.md` for the full tracking output format.

## Evidence channels

What you can verify depends on what you were given. Never score a check you
could not observe — mark it **Unverifiable** and exclude it (like N/A in
skill-evaluation).

| Channel | Can verify | Cannot verify |
|---------|-----------|---------------|
| Code (CSS/JSX/HTML) | Fonts, hex values, gradients, shadows, radii, `opacity:0` gating, icon imports, layout skeletons | Optical centering, rendered contrast, seams, whether controls respond |
| Screenshot(s) | Everything visual: palette, type, layout, alignment, centering, clipping, contrast, seams | Hover/scroll motion, dead controls, invisible-content trap, responsive behavior |
| Live URL (browse + screenshot) | All of the above plus interactions, motion, fold ownership | Only what you didn't exercise |

With code, grep before you stare: `fonts.googleapis|next/font`,
`lucide-react`, `linear-gradient`, `box-shadow`, `border-radius: *9999`,
`backdrop-filter`, `opacity: *0`, `initial={{ *opacity: *0`,
`overflow: *hidden`, `clip-path`, `position: *fixed`. Each hit is a lead,
not a verdict — confirm against the catalog entry before recording it.

## Evidence acquisition SOP

Route by what the `target` is; always end with an evidence inventory
(what was captured, what is Unverifiable) — it feeds the report header.

**Live URL** — the richest channel; prefer it whenever reachable.
Use whatever browser automation this session has (a browser MCP such as
Playwright or Chrome DevTools, or `npx playwright screenshot` as the
no-MCP fallback) and capture, saving every artifact to the scratchpad so
findings can cite `file + region`:

1. Load at desktop (1440×900) and mobile (390×844); wait for network idle.
2. Full-page screenshot of both viewports **immediately after load,
   before any scrolling** — sections sitting at `opacity:0` waiting for a
   scroll reveal show up blank here (M1 evidence).
3. Scroll pass top to bottom, then a second full-page capture; diff the
   two mentally for reveal-gated content, seams (C11, X13), and fold
   ownership (L16).
4. Interaction pass: hover the primary CTA, one card, one nav link
   (M2–M4); click every tab, accordion, toggle, and button (M8); Tab
   through the page and confirm a visible focus ring (X14).
5. Zoom crops at 2x of: anything near a clipped edge (X2), circled/tiled
   numbers and icons (X1), pricing columns side by side (X3), button
   labels (X5).
6. Pull the rendered sources for the code-channel greps: font names from
   the network panel or `<link>`/`@font-face`, computed hex values from
   the stylesheets.

No browser automation available → fetch the HTML/CSS (`curl`) and run the
code channel on it, ask the user for full-page desktop + mobile prints,
and mark every visual-only and interaction check Unverifiable until the
prints arrive. Never score a visual check from raw HTML.

**Screenshots** — Read each image. If only partial crops were provided,
ask for full-page desktop + mobile before sweeping (a hero-only print
cannot support L11, L15, or the cohesion axis). All interaction checks
(M1, M8, X14, hover tells) are Unverifiable.

**Code path** — run the greps, read every file they hit, plus the layout/
page components and global styles. If the project runs locally, start its
dev server and continue under the Live URL SOP — code plus a live render
is the only combination that can verify everything.

**Figma export** — treat as Screenshots for visual tells; additionally
fonts, hex values, and spacing are exact from the file. Motion and
interaction axes are Unverifiable (score `NA` for Axis 5 unless
prototypes were shared).

## Axes and weights

| # | Axis | Weight | Scored from |
|---|------|--------|-------------|
| 1 | Color & Light | 2x | Tells C1–C15 |
| 2 | Typography & Copy | 2x | Tells T1–T10, W1–W3 |
| 3 | Components & Ornament | 1x | Tells K1–K27 |
| 4 | Layout & Composition | 2x | Tells L1–L21 |
| 5 | Motion & Interaction | 1x | Tells M1–M8 |
| 6 | Execution & Craft | 2x | Tells X1–X14 |
| 7 | Signature & Uniqueness | 3x | 7-element formula (positive rubric) |
| 8 | Cohesion | 2x | 4 checks (positive rubric) |

Axis 7 carries the heaviest weight on purpose: the law's deepest rule is
that dodging the tell list is still slop — a page with zero tells and no
signature is unfinished work wearing restraint as an alibi.

## Scoring

**Axes 1–6 (tell-counted).** Count confirmed tells on the axis by severity,
then: `score = max(0, 100 − 30·critical − 15·major − 5·minor)`. Run
`scripts/score.py axis CRIT MAJOR MINOR` — don't do it by hand. One tell,
one count: a pattern repeated across sections is still one tell (note the
repetition in the evidence; repetition may upgrade minor → major where the
catalog says so).

**Axis 7 (Signature).** Score each of the 7 formula elements 0 (absent),
50 (attempted, weak), or 100 (strong) per the rubric in
`premium-markers.md`; the axis is their mean.

**Axis 8 (Cohesion).** Same 0/50/100 on the 4 cohesion checks; mean.

**Compounding rule.** Three or more *major* layout tells on one page cap
Axis 4 at 40 — a page assembled from known skeletons is slop no matter how
clean each block is.

**Gates** (pass as `--cap` to the overall run):
- **Signature gate:** Axis 7 < 40 caps the overall at 59 (grade C max). No
  amount of clean spacing rescues a page with no signature.
- **Absolute-rule gate:** any confirmed critical tell caps the overall at
  69 (no grade A with broken execution).

**Overall & Slop Index.**

```
overall    = sum(axis_score × weight) / sum(weight)   # capped by gates
Slop Index = 100 − overall
```

Run `scripts/score.py overall 1:80:2 2:65:2 ... [--cap 59] [--cap 69]`.
Unverifiable axes score `NA` and drop out of both sums. `--fail-below N`
exits non-zero for CI gating, e.g. gating a PR on its preview deploy:

```yaml
# .github/workflows/slop-gate.yml (step excerpt)
- name: Slop gate
  run: |
    # run slop-eval against $PREVIEW_URL, export each axis score, then:
    python3 skills/slop-eval/scripts/score.py overall \
      1:$A1:2 2:$A2:2 3:$A3:1 4:$A4:2 5:$A5:1 6:$A6:2 7:$A7:3 8:$A8:2 \
      --fail-below 40
```

## Grade scale

| Grade | Overall | Slop Index | Verdict |
|-------|---------|------------|---------|
| A | 80–100 | 0–20 | Premium — deliberate, signed, executed |
| B | 60–79 | 21–40 | Considered — mostly deliberate, some defaults |
| C | 40–59 | 41–60 | Generic — clean but templated or unsigned |
| D | 20–39 | 61–80 | Slop — assembled from presets |
| F | 0–19 | 81–100 | Pure slop |

## Absolute rules check

Six execution laws, each pass/fail/unverifiable, reported in their own
table. Any **fail** is a critical tell (counts on its axis AND triggers the
absolute-rule gate):

1. **Content visible by default** — nothing gated on an entrance animation
   (`opacity:0` + reveal) (M1)
2. **Clear the cut** — no text/control sliced by clip, notch, overflow, or
   fixed height (X2, X11)
3. **Parallel alignment** — comparable columns share baselines; buttons
   anchored (X3)
4. **Real centering** — everything meant to be centered is, mathematically
   and optically (X1)
5. **Legible contrast** — every text clears its background by a real value
   gap (X5)
6. **Controls work** — every interactive-looking control responds (M8)

## Workflow

1. **Gather evidence** — route the `target` through the Evidence
   acquisition SOP above. Done when the evidence inventory states what
   was captured and what is Unverifiable.
2. **Read `references/tells.md`** — the catalog you sweep against.
3. **Sweep axes 1–6** — walk the catalog group by group. **Cite-or-cut**:
   a tell is only recorded with concrete evidence (hex value, font name,
   `file:line`, or screenshot region); no evidence, no tell. Check each
   candidate against its premium-pair note — the crafted version of a
   pattern is not the tell. Done when every catalog group has been swept
   and every recorded tell carries a citation.
4. **Run the absolute rules check** — all six, pass/fail/unverifiable with
   evidence.
5. **Score Axes 7–8** — read `references/premium-markers.md`, score the 7
   signature elements and 4 cohesion checks with one-line justifications
   each. Done when all 11 items carry a score and a justification.
6. **Compute** — `score.py axis` per tell-counted axis, then
   `score.py overall` with weights and any triggered `--cap`. Never
   hand-compute.
7. **Write the report** — read `references/output-template.md` and emit
   exactly that structure to `output`, ending with the 3–5 prioritized
   fixes that would move the score most (biggest weighted deltas first;
   a missing signature usually outranks any single tell).

## Gotchas

- **The brief overrides the law.** If the user or brand explicitly directed
  a choice (a color, a layout, an effect), it is not a tell — the law
  itself says the user's word wins 100%. Ask for the brief when the design
  clearly follows one; note excluded tells in the report with proper
  justification tags (see Exclusion system below).
- **Context flips a tell.** Mono on real data is correct; a populated,
  real-feeling product window is a signature, not the fake-window tell; a
  tight micro-grid with texture is premium, a full-page graph paper is
  slop. Always check the premium pair before recording.
- **Don't reward the clean miss.** Zero tells with a weak signature is the
  most common failure of designs that *tried* to avoid slop. The signature
  gate exists for this — apply it without mercy.
- **Severity discipline.** Critical is reserved for *broken* (the six
  absolute rules). A blue-purple gradient is loud but not broken: major.
- **One-axis bleed.** Some tells could sit on two axes (cut-off glow is
  color and execution). The catalog assigns each tell to exactly one axis —
  count it only there.
- **Portfolio tells.** L19 (recycling your own house style) needs prior
  work from the same author to verify; without it, mark Unverifiable
  rather than guessing.

## Exclusion system

Every excluded tell MUST have a justification tag. A tell without a tag
counts — no exceptions. This creates an audit trail and prevents lazy
exclusions.

### Justification tags

| Tag | When to use | Example |
|-----|-------------|---------|
| `// BRIEF:` | Client/stakeholder explicitly directed this choice | `// BRIEF: client requested blue-purple gradient as brand identity` |
| `// DESIGN DECISION:` | Documented design decision with concrete reasoning | `// DESIGN DECISION: countdown is real — sale ends 2026-08-01` |
| `// CONTEXT:` | Design context makes this pattern acceptable | `// CONTEXT: mono typeface is appropriate for code snippets in SaaS docs` |
| `// PREMIUM PAIR:` | This is the crafted version, not the slop version | `// PREMIUM PAIR: glass effect has proper refraction, edge dispersion, tuned shadows` |

### Valid vs invalid exclusions

**Valid exclusions:**
```markdown
| C1 | Blue→purple gradient | `// BRIEF: brand guidelines v2.3 specify #6366f1→#8b5cf6` |
| K14 | Countdown timer | `// DESIGN DECISION: real sale ends 2026-12-31, verified in CMS` |
| T4 | Mono as house voice | `// CONTEXT: SaaS product with code-heavy documentation` |
| K25 | Glass effect | `// PREMIUM PAIR: proper backdrop blur, chromatic dispersion, directional light` |
```

**Invalid exclusions (tell still counts):**
```markdown
| C1 | Blue→purple gradient | "we liked it" | ❌ Not a justification
| K9 | Default CTA pair | "it's our style" | ❌ Too vague
| L1 | Default hero stack | "approved by team" | ❌ Who? When? Why?
| K6 | Kitchen-sink card | "industry standard" | ❌ Slop IS the industry standard
```

### Exclusion limits

- **>5 exclusions** → Review each one. Mass exclusions suggest the brief
  wasn't followed or the evaluator is being too lenient.
- **>10 exclusions** → Something is wrong. Either the brief allows nearly
  everything (in which case, why evaluate?) or exclusions are being used
  to inflate the score.
- **Excluding signature elements** → Almost never valid. If S1–S7 are
  excluded, the design has no signature by definition.

### Exclusion documentation in report

In the Excluded tells table, format as:

```markdown
## Excluded tells

| ID | Tell | Exclusion reason |
|----|------|------------------|
| C1 | Blue→purple gradient | `// BRIEF: brand guidelines v2.3 specify #6366f1→#8b5cf6` |
| K14 | Countdown timer | `// DESIGN DECISION: real sale ends 2026-12-31, verified in CMS` |

**Exclusion summary:** 2 tells excluded (1 BRIEF, 1 DESIGN DECISION)
```

### Challenging exclusions

When reviewing someone else's slop report, check exclusions first:

1. **Is the tag present?** No tag = tell counts.
2. **Is the tag appropriate?** `// BRIEF:` needs an actual brief reference.
3. **Is the reasoning concrete?** Vague reasoning = tell counts.
4. **Is the exclusion count reasonable?** >5 warrants scrutiny.

## Evaluation with Jev (Optional)

When the harness has access to [TypeSafe Jev](https://docs.typesafe.ai), the
subjective scoring steps (Axes 7-8) and Quality Checklist verification can
use Jev for calibrated assessment.

**Where Jev is used:**
- **Axis 7 (Signature)** — 7 Score questions (S1-S7) with 0/50/100 rubric
- **Axis 8 (Cohesion)** — 4 Score questions (H1-H4) with 0/50/100 rubric
- **Quality Checklist** — 27 Noul questions for binary verification

**Where Jev is NOT used:**
- **Axes 1-6** — Tell detection is factual (cite-or-cut); `score.py` handles arithmetic
- **Gates & Caps** — Deterministic rules applied by `score.py`

### Discovery Protocol

```
1. MCP Tool `jev_eval` configured in harness → use it
2. Model `typesafe/jev-latest` via OpenRouter → request it
3. Auxiliary slot (Hermes/Devin/Codex) with Jev → delegate
4. Fallback → inline scoring via current LLM using premium-markers.md rubric
```

### Integration Files

| File | Description |
|------|-------------|
| `scripts/jev_questions.json` | 38 typed questions (11 Score + 27 Noul) |
| `references/jev-integration.md` | Full protocol, request/response formats |

> **Full documentation**: See `references/jev-integration.md` for discovery
> details, harness-specific instructions, and request/response structures.

---

## Quality checklist

Final gate before delivering. Run through every item — a single failure
means the report is not ready. This is the self-evaluation rubric; treat
it as a hard gate, not a suggestion.

### Pre-sweep checks

- [ ] **Evidence inventory complete** — documented what was captured (code,
      screenshots, live URL) and what is Unverifiable
- [ ] **Brief documented** — if provided, summarized in report header; if not
      provided, noted as "no brief"
- [ ] **Design context identified** — what type of design is this? (landing
      page, SaaS dashboard, editorial, e-commerce). Read `references/contexts.md`
      to adjust priorities and tolerances
- [ ] **All reference files read** — `tells.md`, `premium-markers.md`, and
      `contexts.md` loaded before starting the sweep

### During-sweep checks

- [ ] **Cite-or-cut enforced** — every recorded tell has ID + severity +
      concrete citation (hex value, font name, `file:line`, or screenshot region)
- [ ] **Premium pair checked** — before recording any tell, verified it's not
      the crafted premium version of the pattern
- [ ] **Portability test applied** — for borderline cases, asked: "Could this
      element be moved to another site without alteration?" If yes → tell.
      If no (it's specific to this brand) → not a tell
- [ ] **Defense test applied** — for borderline cases, asked: "Could the
      designer defend this choice with concrete reasoning if asked?" If no →
      tell. Slop cannot be defended; deliberate choices can.
- [ ] **Section attribution** — every tell assigned to a specific section
      (Hero, Features, Pricing, Footer, etc.) for the Section Ledger
- [ ] **Severity discipline** — critical reserved for absolute-rule violations
      only; no severity inflation

### Exclusion checks

- [ ] **Exclusions documented** — every excluded tell has a `// BRIEF:` or
      `// DESIGN DECISION:` justification
- [ ] **Exclusions are genuine** — "we liked it" or "it looked good" are NOT
      valid exclusion reasons. Only explicit brief direction or documented
      design decisions with concrete reasoning qualify.
- [ ] **Exclusion count reasonable** — if >5 tells excluded, double-check
      each one. Mass exclusions suggest the brief wasn't followed, not that
      the tells don't apply.

### Post-sweep checks

- [ ] **All unverifiable checks marked** — not silently passed or skipped
- [ ] **All 6 absolute rules reported** — pass/fail/unverifiable with evidence
- [ ] **All 11 signature/cohesion items scored** — 0/50/100 with one-line
      justification each
- [ ] **Section Ledger complete** — every major section has a verdict
      (CLEAN/SUSPICIOUS/INFLATED/CRITICAL) with tell count and action
- [ ] **Gates applied correctly**:
  - [ ] Signature gate: if Axis 7 < 40, overall capped at 59
  - [ ] Absolute-rule gate: if any crit, overall capped at 69
  - [ ] Compounding cap: if ≥3 major layout tells, Axis 4 capped at 40
- [ ] **Math from script only** — all scoring via `score.py`, never hand-computed

### Report checks

- [ ] **Template followed exactly** — structure matches `output-template.md`
- [ ] **Fixes ranked by weighted impact** — signature issues (3x weight)
      typically outrank single tells
- [ ] **Language correct** — report in user's language, tell IDs in English

### Final self-audit

Before delivering, ask yourself:

- [ ] **"What still looks like obvious slop that I didn't flag?"** — if
      something visually screams slop but isn't in your findings, either
      find the tell that covers it or note it as a gap in the catalog.
- [ ] **"Did I over-correct?"** — a sparse report on a clearly-slop design
      suggests missed tells. A bloated report on a premium design suggests
      false positives.
- [ ] **"Would I trust this report if someone else wrote it?"** — read the
      report as if reviewing a colleague's work. Does every claim hold up?
