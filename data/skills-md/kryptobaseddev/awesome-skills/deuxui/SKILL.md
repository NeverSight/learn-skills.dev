---
name: deuxui
description: "Engineer and verify interfaces against a 235-rule UX contract with runnable checks, not opinions. Use when building or changing any screen, flow, page, component, form, table, dashboard or layout - including a small addition like a delete or submit control, which carries confirmation and undo duties. Also when redesigning, polishing, simplifying or hardening UI, and when auditing accessibility, responsive reflow, empty/loading/error/offline states, destructive actions, focus order, contrast, hit areas, motion, microcopy or design-system drift. Ships 184 static checks bound to cited rule IDs, a browser tier that measures contrast and 320px reflow and forces the states nobody tests, and 38 iOS and Android rules - behind a gate where NOT_RUN is never a pass. Renders comps from the contract, serves the choice as a page, and refuses UI edits until one is approved. Knows React, Next.js, Svelte, Vue, Tailwind, SwiftUI, Compose, React Native, Flutter. Use even if the user only says 'make this look better'."
license: MIT
compatibility: >-
  Python 3.9+ with pyyaml for the static tier and the report. The runtime tier
  needs the agent-browser CLI (npm i -g agent-browser) and a running app; without
  it every runtime rule reports NOT_RUN rather than passing. Framework-agnostic:
  understands React, Next.js, Remix, Svelte/SvelteKit, Vue/Nuxt, Astro, plain
  HTML/CSS, Tailwind v3 and v4, shadcn, Radix, Base UI, Three.js and Remotion.
metadata:
  author: github.com/kryptobaseddev
  version: "5.20.1"
  last_updated: "2026-09-22 04:55:00"
  category: frontend
allowed-tools: Bash Read Write Edit Glob Grep WebFetch
---

# DeuxUI — UX engineering with a verdict

**Deux is French for two — UX and UI.** Design system rules for AI agents: strict
UX/UI best practices, enforced at the token level. Say it *deuce*.

DeuxUI keeps its own contract, in the same format it asks every project for —
`assets/brand/brand.contract.yaml` — and `selftest.py` measures the pages this skill
serves against it with the same detectors. That found twelve findings on its own
review page, and two defects in the detectors. A tool that asks for a declaration and
does not keep one has an argument it does not believe. See `references/brand.md`.

Most interfaces an agent produces look right in the one state the agent looked at.
They fail in the states nobody opens: the empty list, the request that 500s, the
320px phone, the keyboard-only pass, the moment the network drops. And then the
agent reports success, because nothing told it otherwise.

This skill fixes the reporting problem first. It carries a 235-rule contract
derived from WCAG 2.2, platform guidance and named UX research, and it ships
scripts that actually test the testable parts. A rule that was checked says PASS.
A rule that was not says **NOT_RUN** — and NOT_RUN is never a pass, never rounds
up to one, and blocks a release audit when it sits on a safety rule.

Everything else here follows from that. Read `references/loop.md` for the full
execution loop; this page is the map.

## The loop

```
orient (.deuxui/ or init)  ->  classify the surface and the task
   ->  select applicable rules   ->  PRESERVE > MODIFY > COMPOSE > CREATE
   ->  implement                 ->  ux_check.py        (static)
   ->  ux_browser.sh             (runtime, forces the states nobody tests)
   ->  ux_report.py --merge      ->  fix                ->  re-run
   ->  report with the rule matrix, including what was not checked
```

The loop is not ceremony. Each step exists because skipping it is how a specific
class of defect ships. If you are making a one-line copy change, run the static
tier and say so. If you are touching a flow that takes someone's money, run all
three tiers and mean it.

## Four stages, and the gate between them

| Stage | The question | Moves | Gate out of it |
|---|---|---|---|
| **Start** | What is this for, and what world does it live in? | `init` · `shape` · `design` (greenfield) · `uplift` (brownfield) · `comp` · `decide` | A **declared contract**, and a named person who chose a structure |
| **Improve** | Is this the right thing, and does it read? | `live` · `prototype` · `colorize` · `typeset` · `layout` · `animate` · `bolder` · `quieter` · `distill` · `clarify` · `delight` · `polish` | A named person **used a working prototype** and accepted it |
| **Check** | Does it hold up where nobody looks? | `audit` · `harden` · `responsive` · `optimize` · `critique` · `ios` · `android` · `delta` | The rule matrix, with **no unchecked P0** |
| **Maintain** | Is it still the same system six months on? | `document` · `extract` · `ledger` · `doctor` · `hooks` · `operate` | The ledger resolves: every approval names the declaration it was made against |

The stages are the shape of the work; `ux_phase.py` is the part that enforces the
order, and it refuses production UI edits before somebody has accepted a prototype.
Read [`references/ops/phase.md`](references/ops/phase.md) for why that gate exists
and [`references/ops/ledger.md`](references/ops/ledger.md) for what it leaves behind.

**`live` is the one that edits while somebody is looking.** Pick an element in the
running app, see two or three variants **in its own position**, accept one into the
source. Every variant is built from declared values only, one axis at a time, and
accept refuses a variant that introduces a P0 or P1 finding — taste chooses between
admissible options, it does not make an inadmissible one admissible. See
[`references/ops/live.md`](references/ops/live.md).

## Facts that prevent broken work

Read this table first — each row is a failure that reaches real users.

| Fact | Consequence |
|---|---|
| **NOT_RUN is not PASS.** | The single most common dishonesty in agent UI work is reporting a check that never ran. If you did not test it, say NOT_RUN. |
| **The happy path is the smallest part of the work.** | Empty, loading, error, offline, stale, permission-denied and conflict are states a user will reach. `ux_browser.sh --api` forces them for you. |
| **Hover does not exist on touch or keyboard.** | Anything revealed only on hover is invisible to a large share of users. Mirror it on `focus-visible`. |
| **Tailwind v4 changed `outline-none`.** | In v4 it sets `outline-style:none`; the old forgiving behaviour is now `outline-hidden`. The default ring also dropped 3px to 1px. The checks branch on your installed major version. |
| **`100vh` is wrong on phones.** | It ignores retracting browser chrome, so your footer hides under the URL bar. Use `dvh`, or `svh` when you need the smallest stable height. |
| **`:invalid` fires before the user types.** | It paints an error on an untouched required field. Use `:user-invalid`. |
| **A clickable `div` or `Card` is not a button.** | No keyboard, no role, no name. If it already contains buttons, you also get two competing targets and a `stopPropagation` workaround. |
| **Contrast fails by tiny margins.** | Indigo-500 with white text is 4.47:1 — it fails 4.5:1 and no human eye will catch it. Only measurement will. |
| **Colour cannot be guessed from source.** | Tailwind v4 themes are OKLCH `--color-*` variables. The checks resolve colours from your project; unresolvable pairs report NOT_RUN instead of a made-up verdict. |
| **The static tier is heuristic.** | It scans source text and is wrong sometimes. Every finding carries a confidence. The runtime tier is what settles arguments. |
| **Creating is easier than reading.** | This is why agents turn mature apps into a collage of unrelated screens. The preserve ladder exists to make that cost visible. |
| **An exception may lower a PROJECT rule, never a STANDARD.** | You can document a deviation. You cannot relabel a failed WCAG criterion as passing. |
| **Design craft is checked against a declaration, never against taste.** | `.deuxui/design.contract.yaml` states the type roles, colour roles, one depth metaphor, radii and motion band *before* the code is written. The `S-CONTRACT-*` checks then compare the artifact to it. With no contract they report NOT_RUN — an undeclared system cannot be conformed to, and "is this beautiful?" has no decision procedure while "does this match what was declared?" does. |
| **The 20 UX laws now carry verdicts — 14 measured, 5 by attestation.** | Each enforceable law is indexed to the detectors that adjudicate one of its `verify:` clauses, and the report rolls them up. A law whose only evidence is a human attestation says `attested only` instead of passing as measured. The rule ID is still the finer-grained claim, so cite `NUM-004` when you mean the threshold and `LAW-02` when you mean the principle. |
| **215 of the 235 rules have an automated detector; the other 20 are the manual tier.** | Every rule is accounted for and every P0 is automated. The 20 are judgement calls no checker can settle — is this the right amount of complexity to reveal, is this density right for this task — and they report NOT_RUN until a person records an answer. Coverage is not conformance. |
| **The contract is declared before the code, and that order is now measured.** | Entering the `comp` phase snapshots the contract's hash, the git head and every UI file's hash; entering `verify` compares against it. A contract declared with no file changed since is a contract written to describe code that already existed — it will always show conformance, so every `S-CONTRACT-*` PASS behind it would be circular. `A-PHASE-ORDER` FAILs on exactly that. |
| **An approval whose declaration cannot be produced is not an approval.** | A decision records the hash of the contract it was made against, and a hash with no bytes behind it is a fingerprint of a document nobody kept. `ux_ledger.py` archives the contract under that hash every time one is derived, gated or approved, so `show DEC-003` prints what was declared at the time. When it cannot, it says so — printing *today's* contract beside an old approval would make every past decision look as though it were made with today's information, which is the worst thing a record can do. `A-CONTRACT-ARCHIVED` reports it to the gate. |
| **A drawing cannot be used, so it cannot tell you whether the thing works.** | There are two review stages. A wireframe settles structure; a working prototype settles usability, and `build` is gated on the second. `ux_proto.py` generates a real, clickable prototype from the contract — the five states as a switch, a form that validates, a dialog that traps focus, an undo that puts the row back — and `ux_review.py` hosts it beside the current product so a person can Alt-click any element and say what is wrong in their own words. |
| **A direction is approved by a person, against what they were actually shown.** | `ux_question.py` serves the comps as a page and records who chose, when, why, and the hash of what was on screen. It refuses an unnamed chooser, an agent's name, a reason under 40 characters, and a timeout — nobody choosing means NOT_RUN, never a default. Editing an approved comp afterwards makes the record stale and the build gate says so. |
| **The report audits itself.** | `GOV-005/006/008`, the `QA-*` and several `MEASURE-*` rules are about the report, not the product — no scan of an app can tell you whether the agent describing it invented a result. `ux_report.py` checks that every PASS names a detector that ran, that unknowns are declared, and that project config has not been used to weaken a standard. |

## Orient

Before changing anything, find out what already exists.

```bash
python3 scripts/ux_ledger.py state                  # the whole record in one page
python3 scripts/ux_ledger.py log --limit 20         # and how it got that way
python3 scripts/ux_check.py <project> --signals     # stack, theme vars, inventory
cat .deuxui/PRODUCT.md .deuxui/DESIGN.md          # if they exist
```

`ux_ledger.py state` is the first thing to run in a project that has been worked on
before. It reports the declaration field by field, what the code is actually built
with, which approval each stage is currently standing on, and what is still open —
and it keeps those four apart, because a contract declaring one thing over a
component library that does another is a conflict neither one reveals alone.

If `.deuxui/` is missing, follow `references/workflows/init.md`. It builds the
project memory by **inspecting** the repo — package manifest, theme variables,
component directories, routes — and asks only the two or three things it genuinely
cannot infer. Interrogating someone for twenty answers is the fastest way to make
a skill go unused.

Three layers, and they settle conflicts in this order: the **rules** in this skill
are universal; **PRODUCT.md** owns audience, jobs and risk; **DESIGN.md** owns the
visual system. When PRODUCT and DESIGN disagree, DESIGN wins on visual decisions
and PRODUCT wins on strategic ones. When either disagrees with a safety or
accessibility rule, the rule wins — see the priority order in `references/rules/00-governance.md`.

## Modes

Match the request to a mode, then read that workflow file. Do not read all of them.

| Mode | The user is asking for | Read | Tiers |
|---|---|---|---|
| `init` | Set this up / first time in this repo | `references/workflows/init.md` | — |
| `design` | **Greenfield.** No design yet — originate a world, then build from it | `references/workflows/design.md` | static + runtime |
| `uplift` | **Brownfield.** A design exists — derive its contract, then raise it | `references/workflows/uplift.md` | all three |
| `create` | A new screen, flow or component | `references/workflows/create.md` | static + runtime |
| `improve` | Make it better, polish, redesign, simplify | `references/workflows/improve.md` | static + runtime + baseline |
| `critique` | What is wrong with this? (no edits) | `references/workflows/critique.md` | static |
| `audit` | Is this ready? Full review, release check | `references/workflows/audit.md` | all three |
| `harden` | Accessibility, states, destructive actions | `references/workflows/harden.md` | all three |
| `responsive` | Mobile, layout, it breaks at some width | `references/workflows/responsive.md` | runtime |
| `optimize` | It feels slow, janky, shifts around | `references/workflows/optimize.md` | runtime |

When the request is ambiguous, `critique` is the safe default: it reads and
reports without touching anything. When it does not name a mode at all, read
`references/ops/routing.md` — it maps what people actually say ("make it bolder",
"clean this up", "the design feels off") onto one of the 35 operations, and it
decides from measured signals rather than from the wording.

A mode is the shape of the whole job. An **operation** is one move inside it —
`colorize`, `typeset`, `distill`, `bolder`, `ios`, `extract`, `live`. All thirty-five
are indexed in `references/ops/index.md`, and each one ends by naming the
detectors that judge its output, so it finishes in a status rather than an
impression.

## Two review stages, then build

On new work the order is the thing, and there are two questions a person has to
answer — not one. A wireframe settles **structure**: what is on the screen, in
what order, at what proportion. It cannot settle whether the thing *works*,
because a drawing cannot be used.

```
discover -> declare -> wireframe -> prototype -> build -> verify -> release
```

**Stage one — wireframe.** Sheets drawn from the declared contract; no model, no
key, no network needed, so they cannot be the thing that drifts, and each sheet
names on its own face which contract fields were still blank.

```bash
python3 scripts/ux_phase.py init            # greenfield or brownfield, detected
python3 scripts/ux_image.py brief --write .deuxui/comps/detail.brief.yaml --surface "listing detail"
python3 scripts/ux_image.py render .deuxui/comps/detail.brief.yaml
python3 scripts/ux_question.py ask .deuxui/comps/listing-detail.comps.yaml
```

**Stage two — prototype.** A real, clickable thing, generated from the same
contract, put in front of a person beside whatever exists today. They Alt-click
any element and say what is wrong with it in their own words; each note lands in
`.deuxui/requests/` with the element it is about and prints in your terminal as
it is typed.

```bash
python3 scripts/ux_proto.py --write .deuxui/proto/index.html --title "Listings"
python3 scripts/ux_review.py serve --variant "proposed=.deuxui/proto/index.html" \
        --variant "current=http://localhost:5173/listings"
python3 scripts/ux_phase.py advance          # to build, once somebody has USED it
```

`build` needs the second stage, not the first: "request changes" is a real answer
and it is not an approval, so it leaves the gate locked while the notes are acted
on. A work list cannot authorise the build it is a list of complaints about.

The gate is opt-in: with no `.deuxui/phase.yaml` nothing is refused and the
process detectors report NOT_RUN. Read `references/ops/prototype.md`,
`references/ops/phase.md` and `references/ops/decide.md`.

## The preserve ladder

```
PRESERVE  ->  MODIFY  ->  COMPOSE  ->  CREATE
```

Before writing a new component, ask the inventory:

```bash
python3 scripts/ux_check.py <project> --inventory "dialog confirm"
```

Then record which existing primitive you reused, or why none fit. The default is
preserve, and the argument is about asymmetric cost: being wrong about preserving
costs a conservative-looking variant, which is recoverable in one message. Being
wrong about departing rewrites someone's product in a style they never asked for,
which is not. If you are unsure, you are in preserve mode.

Departure needs an explicit request, or a PRODUCT.md anti-reference aimed at *this
specific surface*. "Modern" and "clean" are not directions — see
`references/preserve.md` for how to lock an identity before you touch it.

If the project has Radix, Base UI, Headless UI, Ark or React Aria installed,
hand-writing a dialog, dropdown, tooltip or combobox is not a style choice. Those
libraries have already solved focus containment, escape handling, typeahead and
ARIA, and your version will not. Compose theirs.

## Run the checks

```bash
# Static tier -- source scanning, fast, heuristic
python3 scripts/ux_check.py <path>                       # human readable
python3 scripts/ux_check.py <path> --json > .deuxui/reports/static.json
python3 scripts/ux_check.py <path> --detector S-FOCUS-OUTLINE   # one check

# Runtime tier -- measures a running app, forces the states nobody tests
bash scripts/ux_browser.sh http://localhost:5173 \
     --routes /,/settings --api '**/api/**' --out .deuxui/reports/runtime

# The verdict
python3 scripts/ux_report.py --merge --feature forms --feature payments_or_legal \
     > .deuxui/reports/agent_report.yaml
python3 scripts/ux_report.py --merge --release      # unchecked P0 rules block
```

Exit codes compose: `0` clean, `2` findings, `3` runtime tier unavailable.

Prove the checks still work before you trust a report — `python3 scripts/selftest.py`
asserts every check fires on known-bad fixtures and stays silent on known-good ones.

## The verdict

Report the matrix, not an adjective. `ux_report.py --merge` emits the rule
results, the counts and one of four decisions:

- **BLOCKED** — a P0 or P1 rule is failing, or (in `--release`) a P0 rule was never checked.
- **CONDITIONAL** — nothing failing, but P0 rules are unverified. Fine mid-change; not enough to ship.
- **READY** — every applicable rule was checked and none are failing.
- Rules the product does not reach are **NOT_APPLICABLE**, declared through `features:`
  in `.deuxui/ux.config.yaml` or `--feature` (the flag adds to the file, it does not
  replace it).

When a **STANDARD**-class rule fails, cite its basis alongside the rule ID —
`NUM-001 (S03, WCAG SC 1.4.3)`. The registry carries a source for all 235 rules,
and a reader who can follow the claim to the criterion can check you; one who
cannot has to take your word for it, which is the thing this skill exists to stop.

Say what you did not check and why. "I ran the static tier; the runtime tier needs
the app running, so 84 rules are unverified" is a useful, honest report. "Looks
good" is not a report at all. `references/verification/evidence.md` has the format
and the exception process.

## Where to go next

Each reference is self-contained. Read the one you need.

| Task | Reference |
|---|---|
| The full execution loop, step by step | `references/loop.md` |
| The name, the tagline, the voice, and the contract we hold ourselves to | `references/brand.md` |
| Pick it on screen, compare in place, accept it into the source | `references/ops/live.md` |
| The record: what the design is, and how it got that way | `references/ops/ledger.md` |
| What the visitor came to do, and what it changes | `references/design/visitor-modes.md` |
| The craft floor: every number, and which detector decides it | `references/design/craft-floor.md` |
| The visual contract a project declares | `assets/templates/design.contract.yaml` |
| The prototype wrapper every generated prototype uses, with its named slots | `assets/templates/prototype-shell.html` |
| Identity lock, preserve vs depart, variants | `references/preserve.md` |
| The AI-tell catalogue and why each one reads as generated | `references/anti-slop.md` |
| **The 35 operations** — one named job each, with the detectors that judge it | `references/ops/index.md` |
| Which operation, for what the user actually said | `references/ops/routing.md` |
| iOS and Android rules, detector by detector | `references/ops/ios.md`, `references/ops/android.md` |
| What impeccable does, what this does, and every remaining gap | `references/parity/impeccable.yaml` |
| Everything in this skill, indexed | `references/index.md` |
| Governance, priority order, exceptions | `references/rules/00-governance.md` |
| Rule packs by domain (a11y, forms, state, layout, …) | `references/rules/` |
| The machine registry: 235 rules, severities, sources | `references/rules/registry.yaml` |
| The 20 UX laws, with limits and `verify:` clauses. 19 are enforceable and `ux_report.py` rolls each one up to a status — 14 from live detectors, 5 from a human attestation, stated apart because a signature and a measurement are not the same evidence | `references/rules/registry.yaml` (`laws:`) |
| What each detector tests and with which engine | `references/rules/detectors.yaml` |
| Numeric thresholds, and which are overridable | `references/rules/thresholds.yaml` |
| React, Svelte, Vue, plain CSS, 3D, video specifics | `references/stacks/` |
| What the static tier can and cannot see | `references/verification/static-checks.md` |
| Driving the browser tier, probe by probe | `references/verification/browser-checks.md` |
| What no machine can check, and how to record it | `references/verification/manual-checks.md` |

## Scripts

| Script | Purpose |
|---|---|
| `scripts/ux_check.py` | **Static tier.** 184 source checks bound to rule IDs, across web and native source. Takes a file or a directory and reads exactly that. `--json`, `--signals`, `--inventory`, `--detector`, `--max`, `--config`, `--stdin` for editor hooks. |
| `scripts/ux_browser.sh` | **Runtime tier.** Drives agent-browser across your viewport matrix, measures contrast, targets, focus and vitals, and forces aborted, empty and offline states. |
| `scripts/ux_report.py` | **The verdict.** `--collect` interprets raw probes; `--merge` combines all tiers into the rule matrix and gate decision. |
| `scripts/derive_contract.py` | **Brownfield's first move.** Reads the real type steps, families, radii, shadows, durations and colour roles out of an existing codebase and writes the visual contract, with the spread beside each dominant value so you can tell the scale from the drift. `--write`, `--json`. |
| `scripts/ux_native.sh` | **Native tier.** Drives `xcrun simctl` or `adb` for light, dark and enlarged-text captures, naming the device. Where the tooling is absent it records that and the evidence rules report NOT_RUN. |
| `scripts/ux_delta.sh` | **The iteration loop.** Runs the tiers and prints the delta against the last run: regressed, stopped, fixed, still failing. A check that stopped running is never counted as a fix. |
| `scripts/palette.py` | **Colour, generated and measured.** OKLCH roles placed against the contrast each owes, chroma tapered at the extremes. `--contract`, `--css`, `--dark`, `--check`. |
| `scripts/typescale.py` | **Type, generated and measured.** A role ladder whose steps clear 1.25x by construction, leading tuned to the measure, tracking tuned to the size. `--contract`, `--css`, `--check`. |
| `scripts/doctor.py` | **What can run here.** Names every tier that cannot, what it costs in rules, and how to fix it. Exit 2 when something is unavailable, so CI cannot go green on a fraction of the rules. |
| `scripts/manual_sheet.py` | **The manual tier as questions.** Emits one specific question per manual detector and reports what is unanswered. `--write`, `--check`, `--detector`. |
| `scripts/cdp.py` | **The Chrome DevTools Protocol, stdlib only.** A ~90-line WebSocket client, because two capabilities are CDP-only and agent-browser does not expose them: `forced-colors` emulation and network throttling. No new dependency. |
| `scripts/ux_forcedcolors.py` | **R-FORCED-COLORS.** Two passes, normal and forced, diffed — a forced-colors defect is something that carried meaning before and does not after, which no single pass can see. |
| `scripts/ux_axe.py` | **R-AXE.** axe-core from the project's node_modules, a cache, or a pinned CDN. Suppresses contrast and target-size, which deuxui measures directly against the project's own thresholds. |
| `scripts/ux_slow.py` | **R-STATE-SLOW.** Makes the request slow rather than absent, and asks what the interface says while it waits. Flight is defined by content, not by readyState. |
| `scripts/ux_proto.py` | **A working prototype, generated.** Fills `assets/templates/prototype-shell.html` — a real template with named slots, so the chrome is the same in every prototype and `--sections` appends a product screen to it. Real states you can switch between, a form that validates, a dialog that traps focus, a destructive action with a working undo, tabs with arrow keys, a table with tabular figures. Everything from the contract, so `ux_check.py` over its output is a positive control on the generator. |
| `scripts/ux_review.py` | **Two live variants, side by side, with the human's words on them.** Hosts a file or proxies a running app, injects the selection script, and drops the frame-blocking headers — same origin, so an Alt-click inside the frame is readable. Notes land in `.deuxui/requests/` as they are typed and print in your terminal. Five outcomes; only three are approvals. |
| `scripts/ux_select.py` | **A person pointing, recorded.** Injects a selection overlay into the page the browser already has open, over CDP — no server, no framework adapter. A click captures the element, its computed type, colour, spacing, radius and shadow, its box and its viewport, and asks what is wrong with it in the operations' own vocabulary. Writes `.deuxui/requests/REQ-NNN.yaml`. |
| `scripts/ux_image.py` | **Comps, three ways.** `render` draws them from the contract with no model, no key and no network, so they are conformant by construction. `generate` builds the prompt from the contract and calls whichever of four providers is reachable, reporting NOT_RUN when none is. `verify` measures what came back against the contract — per-colour tolerance, and a tint pointing the other way round the wheel is a different world rather than a near miss. |
| `scripts/ux_question.py` | **The decision, served.** A page on localhost showing the comps and the structural claim each one makes. Refuses an answer with no author, an agent as the author, a reason too thin to weigh, and a timeout. Writes `.deuxui/decisions/DEC-NNN.yaml` hashed against exactly what was shown. |
| `scripts/ux_phase.py` | **The gate.** discover → declare → comp → approve → build → verify → release, each transition's requirements machine-checked. `gate write` refuses UI edits before a direction is approved, wired to PreToolUse so the refusal lands while the file is open. The override is audited, because a gate with no way past it gets bypassed by deleting the file. |
| `scripts/ux_live.py` | **Pick, compare in place, accept into the source.** `pick` points at an element in the running app and resolves it to exactly one place in the source or refuses; `vary` builds variants from declared values only, one axis at a time, emitting `var(--token)` where the project has one; `show` puts them all in the element's own position with a switcher; `accept` runs the static tier against the edit first and refuses a variant that introduces a P0 or P1, then writes one commented rule into the stylesheet that already holds the tokens and records a decision carrying the contract hash. `pick --describe "the pricing cards"` skips the clicking when an agent already has the element in words — six tiers of evidence, most specific first, resolving to exactly one node or refusing with the candidates. `text` rewrites what the element *says*, in the source, and reports every other place that same literal appears — an i18n key on the English string is the coupling it exists to surface. `wrap` and `insert` are the structural pair: they resolve the element's exact source boundaries first and refuse when they cannot, so markup you supply is placed at the right indentation and measured before it is written — and when the element sits inside a `.map()`, a Svelte `{#each}` or a `v-for`, they say so first, because "wrapped the element" and "wrapped every row of the table" are different changes — and when the element is a component usage they name where that component is defined **and which element inside it you picked**, resolved from the class the browser reported — so you are not left editing one call site of eleven. |
| `scripts/ux_ledger.py` | **The system of record.** `state` says what the design is right now — the declaration field by field with blanks shown as blanks, what PRODUCT.md and DESIGN.md actually say, what the project is measurably built with, the live approval per stage, and what is still open. `log` says how it got there. `snapshot` archives the contract under its own hash, so a decision's `contract_sha` resolves to bytes and `show DEC-003` can print what was declared **at the time**. An unresolvable reference is reported as a gap, never filled in from the present. |
| `scripts/fontindex.py` | **Does the declared face exist here.** Finds every way a face legitimately arrives — `@font-face`, `@fontsource`, `next/font`, a file in the tree, a Google Fonts request — matches across spellings, and refuses to treat the build host's own fonts as evidence about a visitor. |
| `scripts/comp_diff.py` | **Did the build do what the approved comp did.** Every other check compares an artefact to the contract, which catches a build that left the system and not one that stayed inside it and is not what somebody chose. Not a pixel diff — it compares what the two images are made of: palette by coverage, canvas and ink with the contrast between them, and the sequence of flat/mixed/photographic regions. Rasterises an SVG comp through the browser, forces one viewport on both, and **refuses to compare colour against a wireframe**, which commits to none. |
| `scripts/comp_spec.py` | **Read a reference image.** Palette by coverage, canvas and ink with the measured ratio, region bands, and which are photographic rather than flat — the distinction that decides whether a region ships as a raster or as code. Also records an asset's provenance inside the PNG. |
| `scripts/native_conformance.py` | **Proves the native driver, not the device.** Recording stubs for `xcrun` and `adb`: the command sequence, the state it restores, and all seven availability states. It says plainly that a stub is not a phone. |
| `scripts/browsertest.py` | **Integration test for the runtime tier.** Serves a fixture with known defects and requires each probe's numbers to match the pixels the browser painted. |
| `scripts/uxconfig.py` | The only reader of `.deuxui/ux.config.yaml`. Merges overridable thresholds, refuses standards, and answers `--get app.dev_url` for the shell driver. |
| `scripts/selftest.py` | Asserts every check fires on bad fixtures and stays quiet on good ones, **and** that every config key changes something — each with a positive control. |
| `scripts/csp.py` | **Where the policy is, and what it forbids.** An overlay's `<style>` is inline style whatever created it, so under `style-src 'self'` it appends and renders with nothing applied — and the browser logs that to the *page's* console, not your terminal. `cdp.style_policy` measures the live page; this names the file, across eleven declaration sites, because "your overlay will not be styled" is not actionable without one. It never edits a policy: loosening one is your decision, in your dev config. |
| `scripts/jsxspan.py` | **Where an element begins and ends, or a refusal.** Structural edits need boundaries, and scanning for `<` and `>` does not survive real code: `onClick={() => x}`, `{a > b}`, `title="a > b"`, `useState<Row[]>`, `{/* <Legacy /> */}` and `// <Old />` are all angle brackets that are not tag boundaries. A state machine that knows strings, template literals, both comment forms and brace depth — then the span is **verified** (same tag at both ends, the anchor exactly once inside, balanced within, and the tag agreeing with what the browser reported) before any caller is allowed to write. |
| `scripts/parity.py` | **The coverage claim, made falsifiable.** `references/parity/impeccable.yaml` records what impeccable does row by row and what this skill does about it; this resolves every piece of evidence in it and refuses a `partial` or `absent` that does not say what is missing. "We have everything they have" is the same shape of unfalsifiable sentence as "looks good", so it is checked rather than asserted. `--deep` also RUNS every cited script, because a script that is present and broken satisfies a claim it cannot support — and it prints how many mapped rows an automated control actually exercises, separately from those that only start. That second number is the honest answer to "wired *and working*" and it is printed whatever it says. |
| `scripts/lint_rules.py` | Proves no prose cites an invented rule ID, no detector claims coverage nobody implemented, and no rule is orphaned onto a detector that can never run. |

## Common mistakes

| # | Mistake | Fix |
|---|---|---|
| 1 | Reporting PASS for a check that never ran | Report NOT_RUN. It is the honest status and it is the one the gate cares about. |
| 2 | Running only the static tier and calling it an audit | The static tier cannot see computed styles, real hit areas, focus order or any runtime state. Say which tiers ran. |
| 3 | Building a new Dialog next to the project's existing one | Run `--inventory` first. Compose the installed primitive. |
| 4 | Testing only the state you happened to build | Force the others: `ux_browser.sh --api '**/api/**'`. |
| 5 | Treating a screenshot as verification | A screenshot shows one state at one width. Read the rule matrix. |
| 6 | Redesigning everything when asked to fix one thing | Preserve is the default. Lock the identity first. |
| 7 | Using `outline-none` in Tailwind v4 without a replacement | It removes the indicator even in forced-colors mode. Use `outline-hidden` plus `focus-visible:ring-2`. |
| 8 | Adding a UI dependency for something the stack already does | Check the manifest. Three button components is how design systems die. |
| 9 | Silencing a check because it is noisy | If it is a false positive, fix the check and its fixture. If it is real, fix the code. |
| 10 | Claiming WCAG conformance from an automated scan | Automated checks cover a minority of the criteria. Conformance needs the manual tier and a stated scope. |

## Resources

- https://www.w3.org/TR/WCAG22/
- https://www.w3.org/WAI/ARIA/apg/
- https://web.dev/articles/vitals
- https://tailwindcss.com/docs/upgrade-guide
- https://base-ui.com
- `docs/UX_UI_AGENT_RULES.md` — the source rulebook this skill implements
