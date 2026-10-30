---
name: visant-killer
description: 'Single UI audit door: runs detectors as a hard gate, applies frontend/motion/refine judgment, ends with an adversarial interrogation and a score. Use on "looks AI-made", "this is slop", "kill this screen", "tá com cara de IA", "tá slop", "audita essa tela", "mata essa tela", "nível vale do silício", auditing UI before a PR.'
---

# Visant Killer

Adversarial UI audit. The screen is the defendant, not the client. Two halves
that do not replace each other: the **gate** (deterministic scripts, binary:
AI tell, token, voice, **chrome noise**) and **judgment** (you, with the skills
loaded), because AI slop survives any linter: the problem is decision, not syntax.

> **Rule zero (from `visant-copy`):** only the fix of a confirmed defect goes
> into the file. What passes clean stays untouched, even if it sounds flat.
> Taste improvements go as a proposal table; the user picks line by line.

> **A green gate is not a seen screen.** A frozen `AnimatePresence` in a lead
> form passed six gates. So `killer-scan` **refuses** "gate open" without the
> surface table and the record of having opened the screen.

Where each rule came from: [references/cases.md](references/cases.md).

## Hard prohibitions (you break them while writing, not reviewing)

| Forbidden | Write | Why |
|---|---|---|
| arrow glyph in text (`→`, `←`, `↑`, `↓`) and hand-drawn icon SVG | a real library icon (`@phosphor-icons/react`, `@radix-ui/react-icons`) | **LAW.** The character arrow is Claude's nº1 habit: it inherits font metrics, drifts off the baseline, changes shape per family, has no controllable weight or size, and reads as text. A hand SVG is the same disease in more lines. Icons are library assets, always |
| `hover:scale-*`, `whileHover={{ scale }}` | change color, shadow or border | scale on hover is the nº1 template tell; it moves neighboring layout and does not survive `prefers-reduced-motion` |
| hover that grows **over** neighboring text | reserve the lane permanently and grow inside it | hover reveals, hover does not run over things |
| `hover:bg-accent` **when `--accent` is emphasis** | `hover:bg-muted` or `hover:bg-primary` | emphasis turned into a mouse state. Check the token: in stock shadcn `--accent` is the neutral hover color, and there `hover:bg-accent` is right |
| `border-accent` | `border-border` | same confusion: emphasis turned into chrome |
| `backdrop-blur` outside dialog/sheet | solid token background | costs compositing on every scroll; on a card it is decoration paid in frames |
| `white-space: nowrap` in an overlay without `max-width` | `max-width: calc(100% - 12px)` and let it wrap | inside an `overflow: hidden` parent the word gets CUT, and the cut only exists after the font loads: no linter sees it |
| a fixed highlight (`on: true`, `active: true`) in an item factory | the condition that decides (`on: q.live`) | a highlight that runs once per item lights up the whole list, and emphasis on everything is emphasis on nothing |
| two doors for the same kind of data on one screen | one per screen, or names that say the difference (the detector only checks the same screen; a repeated name across screens is judgment) | two identical URL fields side by side writing to different stores: people choose by luck |
| the same gap inside a group and between groups (`space-y-4` on every level) | tight inside, open between: each level at least 2× the one inside it (8 / 16 / 32) | the eye groups by distance: when the label is as far from its value as from the next block, the screen reads wrong with every token right (catalog 6) |
| `transition-all` | `transition-colors` or an explicit list | animates what you did not ask for, layout included |
| `duration-300`+ on an interactive element | `DUR.base` / `DUR.slow` | above ~300ms the UI feels stuck |
| raw hex, `rgb()`, `rgba()` | HSL token (`hsl(var(--x))`) | `var(--x)` alone is not a color: the tokens store loose channels |
| component demo with a fake frame, "hover me" caption, stacked variations | the piece large and centered, **one at a time**, a quiet selector | catalog 35-38: in the tile the piece disappears behind the explanation |
| the pretty state (glow, tilt, open menu) only on hover | born in its best state; hover intensifies | it does not exist on touch, in the tile or in a screenshot (catalog 37) |
| clickable button/card without `cursor: pointer`; drag without `grab` | a rule in the shell (`:is(button,[role=button],a[href])`) | Tailwind v4 preflight resets the cursor (catalog 46) |
| client copy in a library piece | generic text, spoken pt-BR | the library sells to every client (catalog 42) |

Exceptions exist (route transition, marketing piece, `#fff`/`#000` as a WCAG
contrast reference, blur in a `Dialog`, scrim over a photo). An exception goes
**with a written reason on the line**, in the scanner format
([references/gates.md](references/gates.md#written-exception-one-contract-every-scanner)),
never with a mute `audit-ignore`.

Scripts, by full path (used in every step):

```bash
K=~/.claude/skills/visant-killer/scripts/killer-scan.mjs
R=~/.claude/skills/visant-refine/scripts/refine-scan.mjs
D=~/.claude/skills/visant-killer/scripts/dist-scan.mjs
C=~/.claude/skills/visant-copy/scripts/copy-lint.mjs
T=~/.claude/skills/visant-killer/scripts/corta-scan.js; E=${T%corta-scan.js}ritmo-scan.js  # IN THE BROWSER (Step 5): clipping; spacing
V=~/.claude/skills/visant-killer/scripts/verify-screens.mjs  # opens the app logged in (Step 5)
# grafo.mjs is a library (import graph for --roots and repeated-door), not a CLI
```

## Step 0: Root first (large target)

A target of dozens of files starts by grouping findings by **root**:
`node $K --roots <target>` (shared pieces ranked by `fan-out × findings`,
[how](references/gates.md#how---roots-ranks)). One wrong container produces
hundreds of leaves with the same symptom, pointing at the wrong file. Primitives
and the shell come before any page; only then `--all` to split the rest by file.

## Step 1: Classify the target (never skip)

The tier decides how much interrogation the target deserves; a wrong tier
wastes context, or audits what pays the bills too shallowly.

| Tier | The target is | Signals | Interrogation |
|---|---|---|---|
| **T1 Leaf** | one component, one card, one list row | 1 to 3 files, no route of its own, does not write to the database | 5 questions |
| **T2 Route** | a whole screen | has `page.tsx`, has states (loading, empty, error), has keyboard | 12 questions |
| **T3 Core** | a flow that moves money, identity, or several routes | database writes, billing, permissions, onboarding, sales pipeline | 20 questions plus positioning |

Mixed target: classify **by region**, not folder (a billing row inside a
listing screen is T3 inside a T2).

**Complaint only about excess** ("too much text", "cluttered", "template look",
"tá poluído", "muita label"): go straight to
[declutter.md](references/declutter.md), the path that needs nothing of the
house (any repo, any language, no linter).

## Step 2: Gate (runs before reading the code)

**Report first, detector second** (an exit code feels like completion, and agents stop there):

```bash
node $K --init-report AUDIT.md <target>    # skeleton, one row per route (Shell hint to confirm)
# fill the table BEFORE fixing anything
node $K --report AUDIT.md <target>
```

Without a complete `--report` it prints **GATE INCOMPLETE** and exits 1
([details](references/gates.md#what---init-report-writes)). Two required columns:

- **surface**: A acquisition (not yet a customer), B work (uses it every day),
  C trust (money, permission, destructive action). A instincts on a B screen is
  the most expensive frontend mistake.
- **business variable**: what this element moves. Dash, "TBD" or empty is
  rejected: filling it with nothing is skipping the step.

The `## Screen seen` section (exact heading; `## Tela vista` also parses) is the
other half: one row per screen **opened**, with route, width, data state and
what happened. Read [environment.md](references/environment.md) first: the dev server lies.

`killer-scan` runs four detectors, prints one scoreboard and ends with a
`gates: N/4 ran [...]` line naming anything skipped: **impeccable** (AI tells);
**token** (the repo's `audit:design`-like gate, else a labeled built-in FALLBACK
for raw hex/rgb/hsl and palette classes, aware of the repo's token layer); **copy** (voice, only on
strings that reach the eye: JSX text, `label`, `title`, `placeholder`,
`aria-label`, `alt`); **chrome noise** (`noise-scan`: each line defensible, the
sum unreadable). Details and the 24 noise rules: [gates.md](references/gates.md).

**Discover the target repo's gates.** The four detectors are the floor. Look at
`package.json` scripts named lint/audit/design/token/ui/theme/i18n/ratchet and
at `scripts/` for unwired scanners; run what exists on the target; record what
ran and what was skipped, and why
([commands](references/gates.md#discover-the-target-repos-gates)).

Side gates: `node $R <target>` when there is a chart, gauge or animation;
`node $D <app-root>` on surface A, **before** polish, because a page that shares
without a card or converts without an event is not fixable by tokens and no UI
detector lights up ([distribution.md](references/distribution.md)).

**A failed gate becomes a fix, not a proposal, after confirming each finding at
`file:line`** (legacy code is noisy; fixing unread lines writes bugs).

- A confirmed false positive has ONE right fix: **repair the rule and lock the
  case in the fixture**, never an `audit-ignore` in the file (it hides the next one).
- **Written exception:** `EXCEPTION to <scanner>/<rule>: reason` (or `EXCEÇÃO
  ao`) on the line or up to 8 above; mute allowlists are forbidden
  ([contract](references/gates.md#written-exception-one-contract-every-scanner)).
- **CI ratchet:** re-record a baseline only when the total dropped, never to
  absorb a rise, always over the whole app ([gates.md](references/gates.md#ci-ratchet)).
- **Rule before finding:** many findings, almost none real, means the defect is
  in the RULE. Group by folder, read the rule's intent, scope it with a **reason
  written inside the rule**, then fix what is left
  ([false-positives.md](references/false-positives.md)).

## Step 3: Judgment (load by tier, not everything always)

Skill memory is not the skill; load by tier, and report what was **not** loaded.

| Tier | Load | Do not load |
|---|---|---|
| **T1 leaf** | nothing beyond this skill | the four. The prohibitions table and the `slop-catalog` are enough for a card |
| **T2 route** | `visant-frontend` + `visant-motion` | `revenue-centric-design`, unless the route sells something |
| **T3 core** | all four | none |

**Lean T3** (tight context): only each SKILL.md; a reference only **for a finding**.
Order: **`visant-frontend`** (the *cut test*: every element names the business
variable it moves, or it goes; the Step 2 surface table is its output), then
**`visant-motion`** (easing/duration SSoT and feel gotchas), **`visant-copy`**
(voice; the gate caught syntax), **`revenue-centric-design`** (only as Step 4
ammunition).

Read [slop-catalog.md](references/slop-catalog.md) before judging (slop that
passes every linter: symptom, cause, fix). **Several agents at once:** exclusive file ownership, i18n by fragment merged
once, measure after edits stop ([multi-agent.md](references/multi-agent.md)).

## Step 4: Devil's advocate

The goal is the **concept** change that makes half the pixel work unnecessary.
Question bank per tier: [devils-advocate.md](references/devils-advocate.md).

- Pick the tier's questions, no more (extra on T1 is philosophy about a card).
  The **fixed block F1 to F6** runs on every tier: reuse, design-system
  consistency, measured responsiveness and performance, progressive flow for the
  ICP, what to hide or iconize, what is missing for Silicon Valley level.
- **Answer it yourself first**, with `file:line`. A question handed back with no
  attempt is laziness dressed as rigor. Only what **changes what gets built** and
  the code cannot answer goes to the user, with your recommendation first.
- Name the `revenue-centric-design` mechanism when there is one (attention
  hierarchy, Swiss Knife Index, optimal play, default as decision, promise the
  size of the proof). Naming the lever is the value.
- One question that kills the screen beats twelve token fixes. If the honest
  answer is "this screen should not exist", write that.

## Step 5: Verification (what compiles is not what someone saw)

**First, open the screen** (it fills `## Screen seen`). App behind login: `node $V` from the target repo (overflow, cut text, raw i18n
keys, console, `/api` 4xx/5xx, empty screen, theme; paid routes locked). Published URL: `corta-url.mjs <base> route`.
By hand: `$T`/`$E` in the console. Flags: [verification.md](references/verification.md). Before measuring, the four
signals in [environment.md](references/environment.md): route warmed up, hydration confirmed by a DOM mark (not
`readyState`), real data including the worst record, node count matching the page opened by hand.

Then, and only then (whatever did not run goes in the report):

| Check | How |
|---|---|
| types and lint | `npx tsc --noEmit` and the repo's lint. **Never `next build` with dev running** (it breaks `.next`) |
| horizontal overflow | `$V` (`estouro` column): `scrollWidth - clientWidth` **of the document** at 390px, re-measured after each fix. Not on an element: a decorative blob under `overflow-hidden` once became 64px of overflow that did not exist |
| **cut text and stacked overlay** | `$V` (`corta` column) or `$T` in the console: a word eaten by a clipping parent, an overlay covering another in the same corner, a piece that left its box |
| **spacing that lies** | `$V` (`spacing` column), `corta-url.mjs`, or `$E` in the console (`ritmo()`): more space inside a group than between groups, three levels with the same gap, one sibling drifting a few px. Off-scale values (15px, `p-[13px]`) are the repo's scale linter, not this ([gates.md](references/gates.md#spacing-two-layers)) |
| distribution | does the page exist outside itself? `title`, `description`, share card, conversion event, `sitemap`, `robots` ([distribution.md](references/distribution.md)) |
| real data | the screen with the best record and the worst; empty hides every overflow |
| light theme | `$V --theme both`. A dark-first app breaks in light where nobody looks |
| backend failure | run with the backend down. Silent zero is the dominant lie: a failed fetch that paints "0" is indistinguishable from a real zero |
| keyboard | `focus-visible` reaches everything hover reveals |
| feel | DevTools, Animations, 25% speed |

## Step 6: Report

The same `AUDIT.md`, now with findings and score first, never just chat text
([scorecard.md](references/scorecard.md)). A score is not a compliment: 100 on
the gate with a T3 and no positioning interrogation is an incomplete audit, and
the report says so.

## Do not

- Declare a high score without running the script, or a "full pass" with the
  surface table blank. The score comes from the process, not the vibe.
- Create a new design-system component without explicit permission. Reuse and
  parametrize; if a piece is missing, look first in the Visant library
  ([ui.visantlabs.com](https://ui.visantlabs.com), 150+ audited items; index at
  `/llms.txt`, sheet at `/r/<name>.md`), then the official shadcn primitive. Both
  install via `npx shadcn@latest add @visant/<name>` (registry
  `"@visant": "https://ui.visantlabs.com/r/{name}.json"` in `components.json`);
  say so before.
- Fix leaves before roots (Step 0, `--roots`).
- Open a route that spends credits on load without the `verify-screens` lock.
- Refactor on top of a reported defect without confirming it in the code.
  Diagnosis is `file:line`, not opinion.
- Declare done without having opened the screen: the line this whole skill
  exists to defend.
- Apply it to a gambling, casino or betting product. Refuse and explain: it is a
  reuse condition of `revenue-centric-design`, not taste.

## Credits and lineage

This skill is the door; judgment comes from the house skills it loads:
`visant-frontend` (cut test, surfaces), `visant-motion` (`motion-lint`),
`visant-refine` (`refine-scan`) and `visant-copy` (`copy-lint`). From outside:

| What | By | How it enters here |
|---|---|---|
| [`impeccable`](https://impeccable.style) | Paul Bakaus ([pbakaus/impeccable](https://github.com/pbakaus/impeccable), Apache-2.0) | gate 1 of `killer-scan` (`npx impeccable detect`) |
| [`revenue-centric-design`](https://github.com/heliocosta-dev/revenue-centric-design) | principles by Richard ([@richardrx](https://x.com/richardrx)), packaged by heliocosta-dev | ammunition for Step 4; the "RCD n" citations in `devils-advocate` |
| [Emil Kowalski skills](https://github.com/emilkowalski/skills) (`emil-design-eng`, `apple-design`, `improve-animations`, `review-animations`) | Emil Kowalski, from [animations.dev](https://animations.dev) and Apple's *Designing Fluid Interfaces* (WWDC 2018) | via `visant-motion`: the origin of the motion principles |
| `vercel-react-view-transitions` | Vercel ([vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)) | via `visant-motion`: route transitions |
| `dataviz` | Anthropic (Claude skill) | via `visant-frontend`: chart correctness |
| [shadcn/ui](https://ui.shadcn.com) and [Radix](https://www.radix-ui.com) | shadcn; WorkOS | official primitive instead of an invented component |
| [Playwright](https://playwright.dev) | Microsoft | `corta-scan` and `verify-screens` open the real screen |

A new skill this one starts using or distilling enters this table in the same
commit.
