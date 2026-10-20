---
name: jury
description: Score any website the way an Awwwards jury would, from evidence alone. Screenshots every page type on desktop, a throttled phone and reduced motion, measures LCP, CLS, FPS, axe, keyboard focus and hover feedback, audits SEO and metadata, then a fresh critic that never sees the code scores Design, Usability, Creativity, Content and the six developer areas, with a ranked fix list. Use when someone asks to review, critique, score, rate or roast a website, portfolio or landing page, asks whether a site is good enough for Awwwards or Site of the Day, or wants design QA of a live URL or a local build. Not for building or redesigning a site; use /awwwards for that.
---

# /jury

Score a website the way the Awwwards jury would: from what a visitor sees and what the browser
measures, never from the code, the design notes or what the owner meant. Hand back a score card
with evidence for every number and a ranked list of fixes.

**Not affiliated with Awwwards.** The criteria and weights are theirs and public
(awwwards.com/about-evaluation); the scores are an estimate. Say so on every card.

**Skill root:** the directory containing this file (`$SKILL`; substitute the absolute path in
commands). The scripts need Node 20+ and Playwright, plus axe-core for the accessibility pass.
`references/quality-bar.md` has the system, the rubric and the critic brief.
`references/calibration.md` has the measured gap between this critic and real juries. It is for
you, for the score card. Never give it to the critic.

## Why blind

Anyone who knows what a site is meant to do scores the intent instead of the screen. A juror
gets a URL and a few minutes. So the critic gets only screenshots and measurements: no source,
no `DESIGN.md`, no README, no pitch from the owner. If the user explains the idea, hold it until
the score is in, then compare (step 5).

## Workflow

### 1. Target

- **A URL:** score what is deployed.
- **A local project, no URL:** build it and serve the production output. Never score a dev
  server: unminified JS and dev overlays wreck WPO and add console noise.
  - Next.js: `npm run build`, then `npx next start -p 4400` in the background.
  - Static output (Astro, Vite, Next `output: 'export'`):
    `node $SKILL/scripts/serve.mjs <dist|out> --port 4400` in the background.
  - Anything else: its own production build and start commands.
- **A dev URL only** (localhost with hot reload): build production instead if the project is
  here. If it isn't, score it and say the WPO numbers are pessimistic.
- **Several URLs** ("mine vs theirs"): run steps 3 to 5 for each, each with its own fresh
  critic, then put the cards side by side.
- **Behind a login or password:** it can't be scored. Ask for a public URL or a local build.

Evidence goes in `.jury/<host>/` in the current directory (`<host>` such as `example.com` or
`127.0.0.1-4400`). Use absolute paths for it below.

### 2. Tools

The scripts resolve Playwright and axe-core from their working directory.

- If the current project already has Playwright (`node -e "require.resolve('playwright')"`
  succeeds), run the scripts from there.
- Otherwise don't add dependencies to someone's project for a review. Install once into a cache
  folder outside it and run the scripts from that folder:
  ```bash
  mkdir -p ~/.cache/jury && cd ~/.cache/jury && npm init -y > /dev/null && npm i -D playwright axe-core
  ```
- If `shoot.mjs` reports no Chromium, run `npx playwright install chromium` once in that folder.

### 3. Evidence

```bash
node $SKILL/scripts/shoot.mjs <url> --crawl --nav --out <abs>/.jury/<host>/shots
node $SKILL/scripts/audit.mjs <url> > <abs>/.jury/<host>/audit.txt
```

- `shoot.mjs --crawl` takes one page of every type (home, each top-level page, one item per
  collection) plus the 404. For each: desktop at 1440, a phone at 390 throttled to a mid-range
  device (4x CPU, slow 4G), reduced motion, keyboard focus, rest/hover pairs for pointer
  targets, idle motion, and page-transition frames. Allow a minute or two per page.
- `audit.mjs` exits with code 1 when it finds a FAIL. That is a finding, not a broken run.
- For a quick look at one page, drop `--crawl` and pass `--max 10` to the audit. Say on the
  card that it covers one page.
- **Check the evidence is real before scoring.** Open `shots/home/d-01-hero.png` and
  `shots/summary.json`. A bot challenge, a login wall, an error page, or a blank frame with
  errors in `report.json` means there is nothing to score: stop and tell the user. A cookie
  banner is not a reason to stop. Visitors see it too, so it counts.
- Crawling is light: at most 40 HTML pages for the audit and 8 page types for screenshots.
  Don't raise those limits on a site the user doesn't own.

### 4. Score

- **With subagents:** give a fresh one the critic brief from `references/quality-bar.md`
  ("Critic brief"), with its three paths filled in (the rubric, `.jury/<host>/shots/`,
  `.jury/<host>/audit.txt`). Give it nothing else, and never `calibration.md`. It reads every
  screenshot, so your own context stays small.
- **Without subagents:** score it yourself under the same brief, from the evidence alone, and
  mark the card as a self-score.
- **If you built or edited this site in this conversation**, a self-score isn't blind. Use a
  subagent, or say on the card that the score is not independent.

### 5. Score card

Write `.jury/<host>/scorecard.md` and give the same card in chat:

```markdown
# <site>: jury score
Estimate, not affiliated with Awwwards. <Independent critic | Self-score>, from <n> pages on <date>.

**The idea, as the critic read it:** one sentence
**Critic overall: 6.2** (0.4 Design + 0.3 Usability + 0.2 Creativity + 0.1 Content, on the critic's strict scale)
**Jury estimate: about 7.3** (critic + 1.1, measured on two recent Sites of the Day)
**Band, from the estimate:** below Honorable Mention (under 6.5) | Honorable Mention range (6.5 to 7.1) | Site of the Day range (7.2 and up)

| Criterion | Score | Evidence |
|---|---|---|
| Design (40%) | | file or report field, and what it shows |
| Usability (30%) | | |
| Creativity (20%) | | |
| Content (10%) | | |

| Developer | Score | Evidence |
|---|---|---|
| Semantics/SEO | | |
| Animations/Transitions | | |
| Accessibility | | |
| WPO | | |
| Responsive | | |
| Markup/Meta-data | | |

## Fixes, most score first
1. [Usability] m-03: what is wrong, and what to change
2. ...

## Measured
Mobile LCP and CLS, loader time, FPS, serious axe violations, overflow, `noHoverChange`,
`colorOnly`, idle motion, audit FAIL and WARN counts (from `summary.json` and the audit).

Not scored: anything stills can't show (how motion feels, sound).
```

Take the offset for the jury estimate from `references/calibration.md` (the 1.1 above is the
offset when this was written) and follow its rules: the critic's own numbers stay as scored, and
the developer areas get no jury estimate.

Then, in chat only:
- If the user told you what the site is meant to say, one line: does the critic's reading
  match? If not, the site isn't saying it, and that is the first Creativity fix.
- The two fixes that would move the overall most.
- An offer: fix the list in this project if it's here, or run `/awwwards` in it for a redesign.

### Re-scoring after fixes

Run steps 3 to 5 again with a **new** critic, never the earlier one, and never show it the
earlier card: it would anchor on the old numbers. Before writing the new card, rename the old
one to `scorecard-<n>.md`, then show the change per category.

## Rules

- No evidence, no points. Every score cites a screenshot file or a report field. Start each
  category at 6 and make the evidence earn every point above it.
- Don't argue a score up. Dispute one only by pointing at a screenshot the critic misread.
- Judge the site on screen. Don't propose a new concept; fix what's there.
- Specific, not cruel: "m-03: the title wraps to five lines at 390 px; drop it to 14vw", never
  "the typography needs work". Someone made this.
