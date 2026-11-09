---
name: design-forge
description: Plans UI design work with the user before any code is written. Reads the app, shows the current screens, deals three visual directions to choose from, and presents a plan with a design section, a responsive matrix and a gate that approve-plan and ship-plan carry through to a pull request. Covers new pages, app screens and components, redesigns, restyles and design reviews, user flows across screens, design-system cleanup, and native iOS and Android apps. Use when the user wants to design, redesign, review or polish a UI, improve a flow, make a page mobile friendly, tidy colours and sizes, or plan screens for a mobile app, before implementing it. For non-UI changes use forge.
---

<instructions>

Plan a design change with the user. Do not write app code. Wait for approval.

This skill adds design to the **forge** skill. It does not replace it. Follow forge for the Record (Step 0), sizing with pick-tier (Step 0.5), the Socratic rules, lettered options, probing risky guesses, and the plan format with its length caps (Instructions 1-4). Do not copy forge's text here.

The visual work uses **taste** (the design-taste-frontend skill). Its commands are named below. Run them as `node <taste>/scripts/<name>.mjs`.

## 1. Prerequisites

Do this before any question.

- Find `<taste>`: the folder the harness reports when it loads the design-taste-frontend skill (Claude Code shows it as the skill's base directory). If the harness reports none, use the `design-taste-frontend` folder next to this skill's folder.
- Run `node --version`. Taste needs Node 22 or later.
- Look for Chrome, Edge or Chromium.
- Taste or Node missing, or taste found without `scripts/start.mjs` or `scripts/consistency.mjs`: say which one is missing, print "Update the design-taste-frontend skill to the latest release with the tool you installed it with.", and stop.
- Chrome missing: planning goes on. Every Gate criterion becomes `manual:`, with the reason.
- Every taste script that opens Chrome gets `--profile "${TMPDIR:-/tmp}/taste-profile-<task>"`. This folder is outside the repo.
- Native work also needs `xcrun simctl` (iOS) and `adb` (Android). Each one missing makes that platform's capture criteria `manual:`, with the reason.

## 2. Pick the mode

State the mode in one line with the reason. Then read only that mode's file.

| Signal in the request | Mode | File |
|---|---|---|
| New page, landing, site, hero; new dashboard, settings, queue, screen; one component | create | [modes/create.md](modes/create.md) |
| Redesign, restyle, "looks dated" or "AI-made", review or audit a page, missing states, fix mobile | redesign | [modes/redesign.md](modes/redesign.md) |
| Steps, clicks, funnel, onboarding, checkout, drop-off, a journey across screens | flow | [modes/flow.md](modes/flow.md) |
| Tokens, colours or sizes everywhere, tidy the design system, export to Figma | system | [modes/system.md](modes/system.md) |
| `*.xcodeproj`, `Package.swift`, `pubspec.yaml`, React Native (`app.json` and `react-native`), or the user names iOS or Android | native, with one mode above | [modes/native.md](modes/native.md) |

- "Improve the design system" with no other signal: ask one chat question. A) Clean up the code (system mode). B) Export to Figma (system mode, hand-off only). Recommend A.
- **Page or app screen** is the first decision. Record it with the mode. A page also records taste's kind: software, gaming, tech, product, service or place.
- **Mixed** (a page plus the app behind it): one Look for both.

## 3. Responsive matrix

Applies to every mode.

- Name the target widths. Default `1440,1024,820,768,390`. Mobile-first adds `375`, and the mock is shown at phone width first.
- Native: name the simulator devices instead.
- The phone is its own layout. Decide each changed screen's phone layout now (pages: taste `references/layout-v4.md`; app screens: `modes/app.md`).

## 4. Discover

Read the app. Never edit its source.

- Taste output goes only to `.plans/<task>/taste/`:
  - `start.mjs`: `--history .plans/<task>/taste/history.json`.
  - `deal.mjs`: `--history .plans/<task>/taste/layout-history.json`.
  - `consistency.mjs`, `check.mjs`, `shoot.mjs`: `--out` (or `--shots`) `.plans/<task>/taste/<before|mock|after>`.
- Taste defaults to `.taste-skill/` when you leave these out. Never write it.
- Choose the task slug here. approve-plan reuses it.
- Run the steps in the mode file.

## 5. Decide on a lavish page

Load the lavish skill, else run `npx -y lavish-axi --help`. Put the page in `.lavish/`. Never run `lavish-axi share`: shares are public.

- **Tier S:** no page, no dialogue, no deal. A short plan in chat. Tier S has no Verify; Build runs the Gate line after the look loop.
- **Tier M:** the deal cards and any trade-off question on a page. The plan in chat.
- **Tier L:** the cards, then the mock (below), then the plan as a page.

What the page shows:
- Before screenshots with findings pinned.
- The deal cards (see Look source): 3 palettes with swatches, 3 type pairings with a specimen. The recommended ones are marked.
- The idea sentence and the competitor test.
- The flow map and the state table, when the mode makes them.
- Questions as lettered options, the recommended one marked.

### Look source

Take the first that fits:

1. **System.** The repo declares tokens (CSS custom properties, a Tailwind theme, token files): keep them. No deal. `Look: system`.
2. **Brand.** The user gives brand colours, and maybe fonts: `node <taste>/scripts/start.mjs brand --page <kind> --bg ".." --ink ".." --accent ".." --type <id> --radius soft`. A font outside taste's ids: take the nearest id from `start.mjs types --page <kind>`, then swap the `--font-display` and `--font-text` lines by hand. Log the swap as an allowance.
3. **Deal.** `node <taste>/scripts/start.mjs deal --page <kind> --history <file>` gives 3 palettes and 3 type pairings. Show them as cards on the lavish page. The user picks one of each. Then `start.mjs css --page <kind> --palette <id> --type <id> --radius sharp|soft|round --history <file>` prints the tokens. A page also runs `node <taste>/assets/layout/deal.mjs --type <software|product|place|service> --has <photo,ui,object,film> --history <file>` for the hero. Hardware: `--type product --kind tech`. A game: `--type software --kind gaming`, and `--has` must name what the brief has (`film` or `photo`). A place's hero is printed, not dealt, and a place always uses `start.mjs brand`.

Deal again only on request or for a stated reason: it contradicts the brand, it needs a missing asset, or the accent is violet (taste bans violet; a violet brand accent is an allowance with its reason).

A brand-new site takes taste's starter kit (`<taste>/assets` into the project, plus `starter.html`). An existing app takes only the `:root` tokens and font links, mapped into its own styling. Copy no kit into it.

### The mock (tier L)

After the user picks:

1. Pages: build the first screen from the kit's `starter.html` and the dealt hero into `.lavish/<task>-mock/`. Copy `<taste>/assets` beside it (lavish serves relative paths only). App screens: build it as static HTML from the tokens.
2. Capture it: `node <taste>/scripts/shoot.mjs --url .lavish/<task>-mock/index.html --w <width> --out .plans/<task>/taste/mock/<width>.png --profile <dir>`, once per named width.
3. Show the screenshots on the page.

The mock is throwaway. It never becomes app code.

## 6. The plan

Use forge's format. Add a `## Design` section in this shape. approve-plan copies it verbatim into `design.md`.

```markdown
## Design
- Plan folder: .plans/<task>/
- Mode: <mode>[ + native] · kind: page|app|mixed|component
- Look: system|brand|deal · kind <kind> · palette <id> · type <id> · radius <r> · hero <id> (pages) · font swap <face> (or none) · history .plans/<task>/taste/
- Allowances: <check id — reason>… (or none)
- Idea: On this page, <thing of the subject> becomes <device>. Live thing: <…>
- Argument and copy outline: <one claim per section; headlines ≤ 2 lines; sample content flagged>
- Pictures: <exists | found with licence | drawn>…
- Widths: <list> · native devices: <list> · phone layout: <per screen>
- Frame (native only): <which parts follow the platform>
- Flow map: <current → proposed steps, or "n/a">
- States: <screen × empty|zero|loading|error|success|no-permission table>
- Tokens (system mode): .plans/<task>/taste/tokens.md
- Before: .plans/<task>/taste/before · FAIL <n> WARN <n>[ · rubric <n>/10 (app screens)]
- Gate (page): consistency.mjs exit 0 · check.mjs exit 0 · perf.mjs no FAIL row · at <widths>
- Gate (app): consistency.mjs app filter (modes/app.md) no FAIL · rubric after ≥ before
```

The Gate (page) commands. `<w>` are the named widths:

```
node <taste>/scripts/consistency.mjs <file> --widths <w> --profile <dir> --page <kind> --category "<what is sold>" --primary "<main action>" --out .plans/<task>/taste/<before|after>
node <taste>/assets/layout/check.mjs --url <file> --profile <dir> --sizes <WxH list> --shots .plans/<task>/taste/<before|after>/layout
node <taste>/scripts/perf.mjs <file> --profile <dir>
```

Acceptance criteria always include the gate line. A criterion only a person or a real device can check is `manual:`.

</instructions>
