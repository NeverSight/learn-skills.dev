---
name: penpot-anti-slop
description: "Opt-in layer that keeps Penpot designs from looking generically AI-generated: a direction step before building, a scored 0–100 slop check of a screen or deck (tree probes + visual review), and reviewed fixes. Triggers: 'avoid the AI look', 'does this look AI-generated', 'anti-slop check', 'make it feel less generic', 'evitar estética IA', '¿parece hecho por IA?'."
disable-model-invocation: false
version: 0.1.0
audiences: [product-designer, design-system]
mode-default: suggest
requires:
  - shared/penpot-mcp-tool-reference.md
  - shared/plugin-api-gotchas.md
  - shared/anti-slop.md
  - shared/anti-slop/lists.json
  - shared/design-quality.md
  - shared/visual-self-review.md
  - shared/visual-effects.md
  - shared/naming-conventions.md
  - shared/state-management.md
  - shared/modes-and-policies.md
  - shared/report-schemas/slop-report.schema.json
---

# penpot-anti-slop — design past the generic-AI look

## 1. Title + How it works
`penpot-anti-slop` is the **opt-in strict layer** over `shared/design-quality.md`: it knows the
patterns that make output read as AI-generated (`shared/anti-slop.md` §1), steers a build away from
them before it starts, and scores a finished screen or deck from 0 (genuine) to 100 (AI default).
Every read goes through `execute_code`; validate visually with `export_shape`; read structure with
`penpotUtils.shapeStructure` (full tool surface: `shared/penpot-mcp-tool-reference.md`). It runs in
three modes:

| Mode | Invoked by | Does |
|---|---|---|
| **direction** | Phase 0 of `penpot-build-screen` / `penpot-build-deck` when `prefs.antiSlop === "on"` | names the defaults for this brief, replaces each with a brief-driven reason, proposes a typeface, lists the tells to refuse |
| **diagnose** | the `slop` step of `brief-to-screen` / `brief-to-deck`, or a user asking "does this look AI-made?" | deterministic tree probes → describe-then-judge visual review → slop score + report |
| **treat** | the user, after a failing diagnosis | proposes the top fixes as concrete edits and applies them **with review**, one per call |

## 2. The One Rule That Matters Most
**Measure before judging, and never trade one default for another.** Anything measurable on the
shape tree is probed (p = 1) and outranks the visual opinion; the visual pass describes before it
judges. And a "fix" that lands on the fashionable anti-AI look (cream + italic serif accent + sage,
or one house style reused everywhere) is still a default — every replacement needs a reason from
the brief.

## 3. Penpot MCP Tool Reference
Full surface: `shared/penpot-mcp-tool-reference.md`. Domain calls: `penpotUtils.findShapes` /
`analyzeDescendants` for the probe walk; `penpot.library.local.tokens.sets` to tell inherited from
introduced fonts; `penpot.fonts.all` for typeface candidates; `penpot.currentFile.get/setSharedPluginData`
for the opt-in preference; `export_shape(<boardId>)` for the review pass.

## 4. Plugin API Essentials
Gotcha numbers refer to `shared/plugin-api-gotchas.md`.
- Text `fontFamily`, `fontStyle`, `align` return `"mixed"` when ranges differ — that is the
  serif-accent signal; `fontSize` is a **string** (`parseFloat` it).
- Effects: `shape.blur` / `board.backgroundBlur` are `{ value, hidden }`; shadows carry `color.color`;
  gradients live in `fills[].fillColorGradient.stops[]` (`{ color, opacity, offset }`).
- Strokes are uniform per shape, so a "one-edge accent" is always a thin child rect.
- **#1 immutable style arrays** — treat-mode edits replace whole `fills`/`shadows` arrays.
- **#2 async token application** — after a treat edit that binds a token, verify in the next call.
- **#11 default white board fill** — a treat edit that removes a gradient lands on a *token-bound*
  surface or `[]`, never on a literal white.
- **#13b exact font match** — `penpot.fonts.all.find(f => f.name === "…")`.
- Verify unfamiliar signatures with `penpot_api_info` first.

## 5. Token-Aware Brief Contract
- **Context** — the product, audience and brief behind the design; whether strict mode was opted in
  (`prefs.antiSlop`).
- **Objective** — single: "steer the build away from the generic-AI look" (direction), "score how
  generic board X reads" (diagnose), or "apply fix N to board X" (treat).
- **Inputs** — the board / deck page id, the brief, active tokens + type tokens, the ledger's prior
  `antiSlop.direction` picks.
- **Constraints** — read-only in direction and diagnose; system tokens and explicit user requests
  outrank the taxonomy (`shared/anti-slop.md` §5); never invent replacement evidence; fixes are
  Apply-with-review.
- **Acceptance Criteria** — every counted finding cites a probe measurement or a Pass A description
  line; score computed by `scripts/slopScore.js`; **pass = score ≤ 35** (target ≤ 15); report JSON
  validates against `shared/report-schemas/slop-report.schema.json`.

Act as a **senior art director who can tell a decision from a default** — and says which is which.

## 6. Mandatory Workflow

> **Visual self-review (mandatory):** treat-mode edits follow `shared/visual-self-review.md` —
> export, look, fix (max 2 iterations), then present.

**Phase 0 — Opt-in + discovery (read-only).** `high_level_overview` (once per session); run
`scripts/antiSlopPrefs.js` (`ACTION="read"`). When invoked from a build skill and the result is
`unset`, ask the §0 question of `shared/anti-slop.md` in the user's language, then store the answer
(`ACTION="set"`). A user who directly asks for a diagnosis has opted in for that diagnosis — do not
ask. `penpotUtils.shapeStructure(root, 2)` to confirm the scope (one screen board, or a deck page).

**Direction mode (from a build skill's Phase 0).** Follow `references/02-direction-playbook.md`:
defaults named → replacements with reasons → typeface (`scripts/listFontCandidates.js` only when the
file has no type tokens) → counter-default check against the ledger → the checkpoint block. Hand
the "will refuse" keys back to the build skill as Constraints. ✋ The build skill's Phase 0
checkpoint shows this block; no separate checkpoint.

**Diagnose Phase 1 — Probes.** One `execute_code` with `scripts/scanSlopProbes.js` (`ROOT_ID`,
`MODE`). Read `references/01-penpot-mapping.md` for what each key measures. Mark findings the user
explicitly asked for as `accepted`; brief-requested dark as `accepted` for `dark-neon-default`.

**Diagnose Phase 2 — Visual review.** `export_shape` the board (decks: batches of ≤ 4 slides) and
run `references/03-exam-protocol.md`: Pass A (describe, written out) → Pass B (judge review keys) →
template judgement → authenticity signals. Decks: read `references/04-deck-tells.md`.

**Diagnose Phase 3 — Score + report.** `scripts/slopScore.js` over `storage.slop`. Emit the Markdown
report (score, band, counted tells with evidence, unsure tells, inherited/accepted, signals, top 3
fixes) and the JSON per `shared/report-schemas/slop-report.schema.json`; mirror to the ledger.
✋ Checkpoint: present the export + report; offer treat for the top fixes.

**Treat (opt-in per fix).** One fix per `execute_code`, each a concrete edit naming the token or
pattern it moves to (e.g. "replace the hero gradient with `color.bg.default`; left-align headline +
subheading; remove `pill-badge`"). Export → look → ✋ approve each. After the last approved fix,
re-run Phase 1–3 and report the before/after **score and points** — the score saturates at 15 points, so on a
very generic design the first fixes move the points long before they move the score (live run: 29.7 → 24.7
points, 100 → 94). When the file has no color tokens, a flattening fix lands on a literal recorded as a ledger
exception plus a token proposal.

## 7. Critical Rules
1. Never run strict mode without the user's opt-in (stored `prefs.antiSlop === "on"`, or a direct
   diagnose request).
2. Ask the opt-in question at most once per file; read the stored preference first.
3. Probes before review; a probe result for a key replaces any review answer for it.
4. Pass A (describe) is written before Pass B (judge); Pass B cites Pass A.
5. Only `present` findings count; `unsure`, `inherited` and `accepted` are reported, never counted.
6. System tokens and explicit user requests beat the taxonomy — report `inherited` / `accepted`.
7. Never replace removed proof (stats, logos, quotes) with invented proof.
8. Every fix is Apply-with-review, one per call — none is in the safe set.
9. Record the direction picks; consecutive runs differ on ≥ 1 of layout, accent role, typeface.
10. Report the lists version used; flag lists older than 6 months as a governance note.

## 8. Domain Architecture
```
storage.slop = {
  listsVersion, scopeId,
  findings: [{ key, weight, p, source: "probe"|"review", status?, region, shapeIds, evidence, fix? }],
  template: { value: 0..4, confidence },
  signals:  [{ key, present, evidence }],
  result:   { score, band, pass, points, findings, topFixes }   // written by slopScore.js
}
ledger.antiSlop = { pref: "on"|"off", direction: { defaults, picks, typefaceProposal, refused }, reports: [ ... ] }
```
Score formula, bands and the gate: `shared/anti-slop.md` §3. Branch field read by workflows:
`slop.score` (and `slop.pass`).

## 9. Modes & Policies
Default **suggest**. Direction and diagnose are read-only. Treat is **Apply-with-review** for every
edit (geometry, color, content, fonts) — none is in the safe set (`shared/modes-and-policies.md`,
`policies/modes.json`). New type tokens are proposed, never created here (hand off to
`penpot-foundations`).

## 10. State Management
Ledger keys under `RUN_ID` (`shared/state-management.md`): `antiSlop.pref`, `antiSlop.direction`,
`antiSlop.reports[]` (score, band, findings ids, listsVersion, scopeId). The preference itself lives
file-wide in plugin data `penpot-ai` → `prefs.antiSlop`, independent of any run. Resume: re-read the
ledger, re-run the probe (cheap, idempotent) rather than trusting cached findings.

## 11. User Checkpoints
| After phase | Artifacts shown | What we ask |
|-------------|-----------------|-------------|
| 0 (from a build skill, pref unset) | the opt-in question | Avoid the AI look? Yes / No / Explain |
| direction | defaults → picks → typeface proposal → refused keys (inside the build skill's Phase 0) | Approve direction? |
| diagnose 3 | export + slop report (score, band, evidence, top fixes) | Treat the top fixes? Which ones? |
| each treat fix | export of the edited board | Approve this fix? |
| after treat | before/after score | Done, or another round? |

## 12. Naming Conventions
`shared/naming-conventions.md`. Region detection relies on semantic board names (`hero`, `features`,
`pricing`, `footer`…); suggest `penpot-rename-layers` when most regions come back as `content`.
Finding ids: `slop-<key>-NN`, stable across iterations.

## 13. Anti-Rationalization Table
| Excuse | Why it's wrong | Countermeasure (halt) |
|--------|----------------|------------------------|
| "The user would obviously want this on." | Strict mode is a style decision that belongs to the user. | Read `prefs.antiSlop`; if unset, ask the §0 question. |
| "My export looks fine, I'll skip the probe." | Self-review is lenient; the tree doesn't lie. | Run `scanSlopProbes.js` first, every diagnosis. |
| "I'll judge straight from the image." | Judging without describing invites motivated answers. | Write Pass A, then judge each key against its criterion. |
| "0.6 is close enough to count." | Unsure answers are noise in the score. | Only p ≥ 0.65 counts; report the rest as unsure. |
| "Swap Inter for something nicer, it's in the taxonomy." | The system outranks the mode. | Report `inherited`; propose a type token via `penpot-foundations`. |
| "Delete the fake stats and put a real-sounding number." | Fabricated evidence. | Labeled placeholder or a pattern that needs no number. |
| "Cream + italic serif is the antidote." | It is the newest default. | `shared/anti-slop.md` §4.4 — name it, replace it with a brief-driven pick. |
| "Apply all three fixes in one call." | One-shot edits are unreviewable. | One fix per call, export, approve. |

## 14. Helper Code Snippets
```js
// Phase 0 — read the stored opt-in (full helper: scripts/antiSlopPrefs.js)
const v = penpot.currentFile.getSharedPluginData("penpot-ai", "prefs.antiSlop");
return { antiSlop: v === "on" || v === "off" ? v : "unset" };
```
```js
// Phase 2 — append a review answer, then run scripts/slopScore.js in the same or the next call
storage.slop.findings.push({ key: "vague-headline", weight: 2, p: 0.8, source: "review", region: "hero:hero",
  evidence: "Pass A: headline reads 'Build the future of work' — no product, no audience" });
storage.slop.template = { value: 3, confidence: 0.7 };
storage.slop.signals.push({ key: "product-visible", present: false, evidence: "hero shows a 3D sphere, no UI" });
return { findings: storage.slop.findings.length };
```
```js
// Treat — one fix: flatten a gradient hero onto a bound surface token (gotchas #1, #11)
const hero = penpotUtils.findShapeById("HERO_ID_HERE");
hero.fills = [];
const bg = penpotUtils.findTokenByName("color.bg.default");
if (bg) hero.applyToken(bg, ["fill"]);
return { heroId: hero.id, bound: !!bg };   // verify the binding + export in the next call
```

## 15. Reference Resources
- `penpot_api_info('Text', 'fontFamily' | 'fontStyle' | 'align')`, `penpot_api_info('Blur')`,
  `penpot_api_info('Shadow')`, `penpot_api_info('Gradient')`, `penpot_api_info('FontsContext')`,
  `penpot_api_info('File', 'setSharedPluginData')`.

## 16. Supporting Files
**references/**: `01-penpot-mapping.md` (diagnose Phase 1), `02-direction-playbook.md` (direction),
`03-exam-protocol.md` (diagnose Phase 2), `04-deck-tells.md` (decks, both modes).
**scripts/**: `antiSlopPrefs.js` (opt-in read/store), `scanSlopProbes.js` (deterministic probes),
`slopScore.js` (pure scoring, unit-tested by `scripts/dev/test-anti-slop.mjs`),
`listFontCandidates.js` (typeface shortlist outside both lists).
**shared/**: `anti-slop.md` (taxonomy, signals, score, direction, precedence), `anti-slop/lists.json`
(fonts, buzzwords EN/ES, placeholders, patterns — versioned).

**Doctrine paths.** `shared/…` and `policies/…` resolve inside this bundle in native installs (vendored by the installer); in a Claude Code plugin install they live at the plugin root — `${CLAUDE_PLUGIN_ROOT}/shared/…`, two directories up from this file.
