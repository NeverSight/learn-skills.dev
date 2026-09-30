---
name: accessibility-inspect
description: "One page, hands-on manual tier — drive a live page through the web accessibility (a11y) checks a rule engine can't decide: keyboard operation and focus order, screen-reader names, roles and states from the accessibility tree, reflow and zoom, reduced motion, form errors, and target size. Grades each finding by evidence basis (verified / confirm-with-a-human / human-required) and severity, and closes every criterion in a ledger: verified, flagged, not exercised, or N/A. Locates and assesses; does not fix (use `accessibility-fix`). Use it for keyboard testing, focus-order checks, screen-reader or a11y-tree review, reflow and zoom at 200%, or 'is this operable, not just lint-clean'. The automated tier is `accessibility-scan`; `accessibility-audit` runs both across a sampled site."
argument-hint: "[target|url] [--selector <css>] [--wait-for <css>] [--deep]"
allowed-tools: Read, Glob, Grep, Bash, Skill, mcp__chrome-devtools__take_snapshot, mcp__chrome-devtools__take_screenshot, mcp__chrome-devtools__press_key, mcp__chrome-devtools__click, mcp__chrome-devtools__hover, mcp__chrome-devtools__fill, mcp__chrome-devtools__fill_form, mcp__chrome-devtools__resize_page, mcp__chrome-devtools__emulate, mcp__chrome-devtools__evaluate_script, mcp__chrome-devtools__navigate_page, mcp__chrome-devtools__new_page, mcp__chrome-devtools__list_pages, mcp__chrome-devtools__select_page, mcp__chrome-devtools__wait_for, mcp__plugin_accesslint_accesslint__explain_rule
---

This is the semi-automated manual tier of a WCAG assessment: the checks that need interaction (keyboard, focus, state changes, reflow) or human review (focus visibility, error recovery, reading order), which a static rule engine can't decide. Work against the running page; use source only to map a finding to `file:line`. Locate and assess — don't fix (that's `accesslint:accessibility-fix`). The automated tier is `accesslint:accessibility-scan`; `accesslint:accessibility-audit` runs both under WCAG-EM.

The shared rules — severity, the no-proxy boundary, high-risk patterns, conformance, grounding — are in [`../shared/methodology.md`](../shared/methodology.md). Read it when a call needs judgment. The rules that always apply are below.

## Grading

Tag each finding with a severity (user impact) and an evidence basis (what you can support). Keep the two separate.

- ● Verified — deterministic and reproducible. Cite the selector, the interaction, and the observed a11y-tree or DOM fact. Without that proof it is not ●.
- ◐ Flagged — you have evidence, but the decision needs a person. Attach the evidence and your opinion; don't decide it yourself.
- ○ Human-required — needs assistive technology or lived experience. Hand it off; don't emulate it.

When unsure between two evidence grades, use the lower one. The icons show evidence basis by fill, not color.

A finding that stacks a deterministic fact on an interpretive call takes the lower grade. The machine-checkable half (e.g. no programmatic status in the a11y tree — a 1.3.1 fact) is ● evidence *inside* a ◐ finding; the interpretive conclusion (e.g. that color is the sole carrier of the meaning — 1.4.1) stays ◐. Citing the ● half does not upgrade the whole.

Severity (user impact, separate from evidence basis):
- Critical — blocks a core task, with no workaround.
- Serious — a major barrier; the task is possible but difficult.
- Moderate — noticeable friction; the task still completes.
- Minor — a small inefficiency or polish issue.

## The ledger — a denominator, not a script

The checkpoint areas below are the run's denominator: every criterion in them ends the run in exactly one state, and the report says which.

- **● verified** or **◐/○ flagged** — you drove the check and have the evidence.
- **N/A** — the triggering feature isn't on the page (no form, no media, no drag UI). Decided from the snapshot; free.
- **Not exercised** — the feature is present but you didn't drive it. Reported as **undetermined**, never silently dropped, and never as a pass.

Not-exercised is a legitimate, honest outcome and it costs nothing. Drive only what the page's features and the engine's gaps demand; don't work through checkpoints to make the report look thorough. An "undetermined — not exercised" line and a driven-and-verified line differ in evidence, not in honesty.

Dedup **before** driving, not after: the engine (`accessibility-scan`) owns the statically-detectable criteria — name/label presence, `lang`, `autocomplete`, semantic markup, contrast of text on flat backgrounds. If a scan result set or engine-owned SC list was provided (as `accessibility-audit` does), never re-check those criteria; ledger them as engine-owned. Without one, read what you can from the initial snapshot rather than re-deriving what the engine would catch.

| Area | SCs | Trigger to drive |
|------|-----|------------------|
| Keyboard & focus | 2.1.1, 2.1.2, 2.4.3, 2.4.7, 2.4.11 | Always — one batched walk (below) |
| Structure & semantics | 1.3.1, 1.3.2, 2.4.1, 2.4.6 | Always — read from the initial snapshot; no extra driving |
| Names, roles, states | 4.1.2, 2.5.3, 4.1.3 | Custom widgets / stateful controls present (static name presence is engine-owned) |
| Visual adaptation | 1.4.1, 1.4.4, 1.4.10, 1.4.12, 1.3.4, 2.3.3, 1.4.11 | Reflow/zoom on every page (one resize each); motion checks only if motion is present |
| Forms & errors | 3.3.1–3.3.3, 1.3.5, 3.3.7, 3.3.8 | A form is present (label/`autocomplete` presence is engine-owned) |
| Media & timing | 1.2.x, 2.2.1, 2.2.2 | `<video>`/`<audio>`, autoplay, or timeouts present |
| Pointer & target | 2.5.1, 2.5.7, 2.5.8 | Target size comes free from the batched walk; drag checks only if drag UI |
| Content & navigation | 3.1.1/2, 2.4.4, 3.2.3/4, 3.2.6 | `lang` and link purpose from the snapshot; cross-page consistency is `accessibility-audit`'s (not exercised here) |

Per-checkpoint procedure and default grades: [`references/checkpoints.md`](references/checkpoints.md). Read it when a triggered area needs its detailed steps, or when the user asks for a deep pass (`--deep`: drive every triggered area through its full procedure).

## Evidence budget — cap spend by grade

Calibrated uncertainty must be cheaper than false certainty. The grade a finding can reach bounds the evidence worth gathering:

- **●** — full proof, gathered once: selector, interaction, observed DOM or a11y-tree fact. Don't repeat an interaction you already recorded.
- **◐** — hard cap: one selector, one screenshot (only if the question is visual), your opinion, and what a person should confirm. Then stop. A ◐ is re-decided by a human whichever way you lean; more evidence doesn't upgrade it to ●, it just costs more.
- **○** — zero driving: name the functional ability, the assistive technology, and the flow you already exercised. Never drive the page to "strengthen" a ○.

## Prerequisite: a browser to drive

This tier runs through a browser MCP: `chrome-devtools` (recommended), `playwright`, or `puppeteer`. If none is connected, run only the static checks, report the rest as ○ handoffs, and tell the user:

```bash
claude mcp add chrome-devtools npx -- -y chrome-devtools-mcp@latest
```

## Target

`$ARGUMENTS` is a URL, an `accesslint.config.json` target name, or empty for the default target. `--selector <css>` scopes to a component; `--wait-for <css>` waits for async content.

`navigate_page` needs a URL, so resolve first:
- A URL: use it.
- A target name or empty: read `accesslint.config.json` (and the gitignored `accesslint.config.local.json` overlay) and resolve the name (or `default`) to its `url`; also take its `waitFor` and `selector`.
- No config: ask for a URL, or suggest `npx @accesslint/cli init`.

Then navigate to the URL and wait for the gate (`--wait-for` if given, otherwise the target's `waitFor`) before testing.

## Driving efficiently

**One snapshot, then scoped reads.** Take one full snapshot after the wait gate; it is the basis for structure, names, roles, states, and the N/A decisions. After a state change, don't re-snapshot the page — read only the widget that changed, via `evaluate_script` scoped to its selector (or a snapshot of that subtree). A full-page re-snapshot per interaction is the single largest avoidable cost in this tier.

**One batched keyboard walk.** Traverse focus in a single `evaluate_script` call, not one `press_key`/snapshot cycle per stop: compute the tabbable sequence, `focus()` each element in order, and return compact JSON per stop — selector, role/name, `document.activeElement` confirmation, computed `outline`/`box-shadow` on `:focus`, bounding box (which settles 2.5.8 for free), and whether the element sits under a sticky/overlay rect (2.4.11). The walk is deterministic DOM fact, so its results are ●-citable.

The walk finds candidates; real key events confirm behavior. Scripted `focus()` doesn't run an app's keydown handlers, so operability (`Enter`/`Space`/arrows) and trap claims still need `press_key` — but only at the walk's suspects: composite widgets (roving tabindex, `aria-activedescendant`), elements whose handlers plausibly capture Tab/Esc, anything the walk couldn't reach. A ● keyboard-trap finding needs the real `Tab`/`Esc` presses at that widget; it doesn't need them at every widget on the page.

## High-risk patterns

For drag-and-drop, rich-text editors, tree views, data grids, custom comboboxes or menus, carousels, and toast or live-region-heavy UIs, heuristic checks are unreliable. Name the APG pattern, verify what you can (●/◐), and hand off the rest as ○ with the assistive-technology steps to run. Use `explain_rule` for engine rules and the APG for widget contracts.

## Report

Group findings by evidence basis; mark severity inline. Close the ledger at the top — every SC in the denominator lands in exactly one bucket — and keep it compact: counts, then bare SC numbers. Group not-exercised SCs by shared reason, one parenthetical clause per group, never a line per SC.

The report spends its words on failures, flags, and handoffs. A pass is its SC number in the ledger — not a paragraph: no "what passed" narration beyond at most one sentence, and no restating in the recommendations a fix already given on its finding.

```
# Manual inspection — <target>  ·  semi-automated tier
Severity: <c> critical · <s> serious · <m> moderate    Basis: ● <v> · ◐ <f> · ○ <h>
Ledger: pass ● <SCs> · fail ● <SCs> · flagged ◐/○ <SCs> · engine-owned <SCs> · N/A <SCs>
        not exercised → undetermined: <SCs (shared reason)> · <SCs (shared reason)>

## ● Verified
- [serious] Keyboard trap in date picker — SC 2.1.2
    where: div.datepicker[role=dialog]   repro: Tab into grid, focus never exits via Tab or Esc
    fix: <mechanical> | NEEDS HUMAN

## ◐ Flagged
- [moderate] Focus indicator may be too faint — SC 2.4.7
    where: button.ghost   evidence: focus-ghost.png; outline = 1px rgba(0,0,0,.2)
    opinion: likely fails 3:1 non-text contrast — confirm visually

## ○ Human-required
- Live-region announcement on add-to-cart — SC 4.1.3
    aria-live="polite" present (●); actual NVDA/JAWS/VoiceOver output unverified
    needs: screen-reader users (blind / low-vision, per Section 508 FPC)
    flow: add-to-cart → toast (exercised above)
```

Ground each entry by selector and visible text. Add `file:line (symbol)` only when `accessibility-scan`'s source maps provide it; don't guess. Each ○ entry is a handoff: the functional ability and assistive technology needed, plus the flow you exercised.

## Notes

- The a11y tree shows machine state, not what a screen reader announces. `aria-live` being present does not mean it announces.
- Browser zoom isn't exposed; CSS-zoom approximations are ◐.
- Wait for async content before the initial snapshot; after that, prefer selector-scoped reads over re-snapshots.
- Composing the tiers (dedup against `accessibility-scan`, one shared browser) is `accessibility-audit`'s job. On its own, this skill reports what its checks find — and its ledger says what they didn't.
