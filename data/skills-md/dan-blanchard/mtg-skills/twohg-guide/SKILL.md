---
name: twohg-guide
description: Build a Two-Headed Giant (2HG) sealed prerelease cheat sheet for a new MTG set — what's winning (Arena Sealed and Early Access draft stats + paper prerelease reports), team pairings, every card that doubles against two opponents, partner-hitting gotchas, rules that change in 2HG, bombs, removal, and a build-hour checklist — published as a private artifact page with card-image hovers.
compatibility: Requires Python 3.12+ and uv. Shares mtg_utils package via symlink. Uses Claude in Chrome for Untapped Premium data and the Artifact tool to publish.
license: 0BSD
---

# 2HG Guide

Dan and his partner play Two-Headed Giant sealed prereleases. Before each one this skill
produces a **2HG Cheat Sheet**: a short, two-column page they read on the way to the store
and at the build table. The Hobbit (Aug 2026) and Reality Fracture (Sept 2026) sheets are
the style model: `Artifact action=list` shows them; read one before drafting.

Vocabulary (head, ×2 card, partner hit, step trigger, bomb, pile) is in `CONTEXT.md`.

## Iron Rules

1. **No card text from memory.** Every card name, cost, and ability on the sheet comes from
   `twohg-scan` / `scryfall-lookup` / the local MTGJSON data. Check each claim you write
   about a card against its text.
2. **No CR number from memory.** Run `download-rules --output-dir <scratch>` fresh every
   time and pass that file to every lookup: `rules-lookup --rule <n> --rules-file
   <scratch>/comprehensive-rules-<date>.txt`. Without `--rules-file` it reads the newest copy
   in the current directory, which can be an old one checked into the repo. Cite only what it
   returns, and check your description against the rule text: CR 810.9 covers damage and life
   only, while "each opponent means both heads" is CR 102.3. For card-specific questions use
   `/rules-lawyer`.
3. **Every recommendation must agree with every other one.** The team pairings, the build
   checklist, the bombs list, and the "what's winning" section are checked against each
   other in Phase 3. If the checklist says "blue in one deck, black in the other", every
   pairing follows it.
4. **Two-sided sections.** Bombs and Removal are the pile you pull *and* the threats and
   answers the other team has. Never frame them as only one side.
5. **Say "bomb" only if the Bombs section names it.**
6. **Quote evidence exactly.** One player's deck is not a team's; "3-0 (6-0)" means three
   matches and six games without a loss, not a 6-0 match record; a comment about one store
   is one store. Label small samples.

## Workflow

```
Phase 0 intake ─► Phase 1 gather (parallel) ─► Phase 2 draft on the spine ─► Phase 3 audits ─► Phase 4 publish
```

### Phase 0 — Intake (ask once, early)

Settle these with the user in one AskUserQuestion round (skip anything already known):

- **Set code** and name, **event date and start time** (drives how much paper data exists).
- **Store product**: WPN's 2HG product from Reality Fracture on is **1 Prerelease Pack + 2 Play
  Boosters** (8 boosters, one kit) per team; some stores still run two kits (12 boosters).
  Ask which the store uses; it changes deck-building advice.
- **Match structure** (usually best-of-one).

Then, **immediately** (Reddit is blocked for every tool: WebFetch, WebSearch, and the Chrome
extension all refuse it):

> Ask the user to open r/magicTCG's "Prerelease Megathread" and the r/lrcast / r/mtglimited
> result posts from the prerelease weekend, and save each with **Cmd+S** into
> `~/Downloads`. The `_files/` folder each save creates holds the deck photos.

### Phase 1 — Gather (run in parallel)

Work in the session scratchpad. Launch these together:

1. **Card scan**:
   ```bash
   twohg-scan --set <CODE> --json > scan.json
   twohg-scan --set <CODE>             # readable version
   ```
   - The scan sorts cards into five buckets:
     - `doubles`: the ×2 cards.
     - `hits_partner`: symmetric effects and wipes that also land on your teammate.
     - `target_player`: effects you can aim at your partner.
     - `step_triggers`: CR 805.4d, `per_head` vs `once`.
     - `removal_reach`: whether each removal spell can hit a planeswalker, and its `mv_floor`. MV-gated removal can't hit Jace or other mana-value-0 tokens.
   - Each card is tagged `[ir]` (phase's parse) or `[text]` (an oracle-text fallback, used for sets phase hasn't parsed yet). Read `[text]` rows more skeptically, and check them against the card text.
2. **Fresh rules**: `download-rules --output-dir <scratch>`; every later `rules-lookup` passes
   `--rules-file` pointing at it (Iron Rule 2).
3. **Arena stats, pooled**: `limited-stats --set <CODE> --json > stats.json`. With no `--event` it reads Arena Sealed and Premier Draft and puts the **pooled view** first (`pooled` in the JSON): pair tiers, standouts, underperformers, data bombs, thin rares, color depth at common, and the cards where the formats disagree, each measured against its own format's average and pooled by games. 2HG is sealed, but Sealed alone is too thin to rank most pairs or cards, so draft joins it as evidence (see **Reading the evidence** below). If one format has no data yet, the pooled view says so and uses the other.
   - The free tier works over plain HTTP. It omits the diamond and mythic ranks; for TRK it gave Sealed as one all-ranks bucket.
   - `--event SEALED` (or `PREMIER_DRAFT`) prints one format alone, the old report.
   - **Premium**, via Chrome, when the user has Untapped Premium:
     1. Load the Chrome tools in one ToolSearch.
     2. Open `https://mtga.untapped.gg/limited/draft/<set-slug>/set-guide` in a new tab. It can take ~30 s to load, and reads `chrome://newtab` until it does, so don't retry-loop.
     3. `get_page_text` for the page summary: match count, the "Early Access" note, color tiers with 6+ win rates, top commons, signpost uncommons.
     4. In the tab, run:
        ```js
        const r = await fetch('https://api.mtga.untapped.gg/api/v1/analytics/query/card_stats_limited_by_set_v2/premium?CardSetFilter=<CODE>&LimitedEventTypeFilter=<EVENT>&LimitedEventTimeIntervalFilter=LATEST_EVENT', {credentials: 'include'});
        const t = await r.text();
        document.getElementById('__out')?.remove();
        const pre = Object.assign(document.createElement('pre'), {id: '__out', textContent: t});
        document.querySelector('main').prepend(pre);
        t.length
        ```
        Run it once with `<EVENT>` = `SEALED` and once with `PREMIER_DRAFT`.
     5. `get_page_text` hands back the JSON. Anything over about 50K characters is saved to a tool-results file; join the pieces into `premium-sealed.json` / `premium-draft.json`.
     6. Run `limited-stats --set <CODE> --premium-sealed premium-sealed.json --premium-draft premium-draft.json --json` (either one alone falls back to the free tier for the other).
   - **Payload shape** (the same for free and Premium, so `limited-stats` reads either):
     - `data` is keyed by Arena **titleId**, not grpid. Names come from mtgajson `loc_en.json`, and rarity and colors from `cards.json`.
     - Inside each card, the keys are archetypes, then rank buckets (`b`/`s`/`g`/`p`/`d`/`m`). An archetype key is a color bitmask (W1 U2 B4 R8 G16, so `3` = WU and `24` = RG), or `ALL`.
     - Each rank holds three arrays: games/wins in deck, drawn-or-in-hand ("GIH"), and opening hand.
     - The free tier truncates these arrays and omits diamond/mythic. `metadata.fields` names the positions.
   - The query is `card_stats_limited_by_set_v2` (the v1 path answers 204 for every set since 2026-11). If `limited-stats` reports an empty answer while the set-guide page shows stats, Untapped has moved it again: read the page's network calls (`read_network_requests`, filter `card_stats`) for the new path, then update `API_URL` in `limited_stats.py`.
4. **Web research subagent** (general-purpose, background). It gathers:
   - the WPN prerelease page (the 2HG product);
   - the official release notes and mechanics article;
   - Early Access write-ups (Substack, MTG Rocks);
   - set reviews: Draftsim sealed, best commons and archetypes; Card Game Base; MTGAZone.

   **Reviewer consensus** (it names the bombs the data is too thin for) comes from chunk.science's aggregate: `https://chunk.science/<CODE>` (e.g. `/TRK`, `/FRA`) redirects to the set's page. The page renders client-side, so read its data file instead: the page's `<script src=".../data/<code>.<hash>.js">` sets `window.<CODE>_DATA`, and each `cards[]` entry has `consensus.mean` (0–100; A− = 90, B+ = 85, B = 80) and `consensus.sourceCount`. Fetch it with curl into its own scratch directory and parse it with `python3 -I`.

   Tell it that Reddit is unreachable, and to mark each claim *reported* (played events) or *predicted* (reviews), and each played event *sealed* or *draft*.
5. **Paper reports**:
   - When the saved threads land, run `thread-extract ~/Downloads/<thread>.html`. It prints the post, the top-level comments, and the saved image paths, largest first.
   - Read the deck photos: decklists are usually images, not text.
   - Collapsed replies aren't in a saved page. If a key reply is missing, ask the user to expand it and save again.

### Reading the evidence

Settled with Dan (2026-11-08) after the TRK sheet; every section below follows it.

- **1v1 numbers only rank.** Every win rate (Arena Sealed, Arena draft, paper) is from 1v1 games. The 2HG effects (×2 cards, partner hits, 30 shared life, combined blocks) come from rules reasoning in their own sections and never get a number.
- **Pairs: pooled tiers.** Each format's pair rate is taken against that format's average pair, then pooled by games. A pair is ahead or behind only at 5+ points from average (`--tier-gap`); the rest are tied, and the sheet doesn't order them. Show the per-format numbers only where they clash by 10+ points.
- **Cards: pooled IWD.** "Improvement when drawn" (win rate drawn minus not drawn), pooled by games drawn. A card stands out at 10+ points over the average card, or underperforms at 10+ under (`--margin`), with 60+ games drawn across the formats (`--pool-min-games`). Write it as "wins N points more often when drawn" and give the average card's figure once.
- **Bombs.** By data: a rare or mythic among the standouts. Under 60 games drawn, reviewers decide: a bomb only at an A− or better average (chunk.science 90+), labelled as theirs, with its thin data in [brackets]. A bracketed rate never makes or unmakes a bomb.
- **Paper reports** are proof that a shape *can* win, never a rate: list them under "Paper decks" with their decklists, and never let them move a tier. Paper prereleases are sealed, so they outrank draft write-ups when describing how sealed plays.
- **Pool size.** A 2HG team opens twice the boosters of an Arena Sealed player, so colors follow the piles (removal → bombs → ×2 → fixing); color depth at common is a tiebreaker only.
- **Removal first** is a paper / reviewer / pool-size lesson, not a win-rate one (common removal tends to rate as an average card): say so, and print no win rates beside removal.
- **Draft-inflated cards.** A card whose value grows with copies or a drafted package (TRK: Andromedan Automatons) gets a one-line flag and no draft-based verdict. The `disagreements` list is where to look; deciding why is your job.
- **Early Access.** Before release all Arena data is Early Access (content creators and invited players): one footnote line, no adjustment.

### Phase 2 — Draft on the spine

- Start from the template: `twohg-template <scratch>/<code>-2hg.html`.
- Fill every section, keeping the Hobbit/FRA length: a cheat sheet, not an essay. Write in plain English (the reader is a player, not the repo).
- Use `.card` for card names, `.cost` for `{1}{B}` costs, `.x2` for doubled numbers, `.cr` for rule numbers and `.pip` for color pips.

| Section | What goes in it | Source |
|---|---|---|
| **What's winning** | One merged section, never separate Arena and paper blocks. Open with how to read the numbers (one line) and the lessons. Then the pooled pair tiers (ahead / tied / behind), the paper decks as "what can win" with their lists, color depth at common (one line), the standout commons and uncommons, the underperformers, any draft-inflated card, format speed, and the only 2HG-specific reports, quoted exactly. Close with a footnote saying which numbers come from where, plus the Early Access caveat. | `stats.json` `pooled`, paper reports, research |
| **Team pairing** | Store product and pool size first. Then an anchor only where the pooled tiers give one (TRK: red in one deck, since every red pair leads), and otherwise "the piles pick the colors". No ranked shapes among tied pairs. Say which colors hold the most ×2 cards and removal. Cover "both decks must work alone" and the fixing available. | scan, stats |
| **The ×2 cards** | A table (rarity · card · cost · the 2HG math) built from `doubles`. Add a "bigger here" line for triggers that fire off opponents, and a **not doubled** line from `step_triggers` rows where `fires: once` (CR 805.4d). | scan |
| **Downgrades & gotchas** | From `hits_partner` and `target_player`: wipes that hit your partner (still good, just time them together); "each player" effects; "target opponent" doesn't double; "target player" can be your partner; set-specific traps. | scan |
| **Rules that win games** | 102.3 + 810.9, 805.4d, 805.10d (a combined block; menace needs 2 blockers from your team), 805.10b, 810.8a (one decked head loses for both), 810.6 (whoever plays first skips *both* first draws, so usually draw first), 810.5, 805.8. Cite from `rules-lookup` output only. | rules-lookup |
| **Bombs** | Your pile and their threats, by color and gold pair. Each entry says whether the data or the reviewers name it (see **Reading the evidence**), with its pooled IWD (bracketed when thin), paper evidence where there is some, and a play-around note for the big ones. Mark ones that are also ×2. Include the set's special guests (cards from other sets on a bonus sheet): they're in paper prerelease packs too, and `thin_rares` lists them. Add a line of the standout uncommons to fear. End with "not bombs despite the hype" (reviewer A− cards with 60+ games and no standout data) and the rares below average. | `pooled` `data_bombs` / `thin_rares` / `underperformers` + reviewer consensus + paper |
| **Removal** | Your pile and their answers, by color, with costs and speed. Say which spells can and can't hit a planeswalker (`removal_reach`) and the MV-floor note, plus which toughness dodges what. | scan + card text |
| **Build hour checklist** | Confirm the product, pull piles (removal → bombs → ×2 → fixing; colors follow the piles), the anchor color if there is one, splashes and ~17 lands, 2HG grade adjustments, draw first, play fast if rounds go to time, and in-game coordination. | everything above |
| **Sources** (footer) | Every source used, with links, dates and sample sizes. Credit card images to Scryfall and © Wizards. | — |

### Phase 3 — Audits (both required)

1. **Rules audit.** Invoke `/rules-lawyer` over the whole sheet.
   - Every CR number must come from `rules-lookup` against the fresh CR.
   - Check every card claim against its text: conditional abilities ("whenever you don't cast…"), one-shot vs repeatable loyalty abilities, "nonland", "creature *or legendary* spell".
   - A tempting inference with no official ruling yet (the set's rulings usually aren't published until release) is labeled as a reading of the rules, citing the rule it rests on.
2. **Consistency audit.** Re-read the sheet top to bottom and check:
   - every "bomb" is in Bombs;
   - the pairings follow the default split, and the checklist says the same;
   - no section frames removal or bombs as one-sided;
   - single reports aren't generalized, and records are exact;
   - the ×2 table, gotchas and step-trigger lines agree with `scan.json`;
   - nothing claims the CR is silent on something it covers.

   Fix everything before publishing.

### Phase 4 — Publish

```bash
guide-card-hovers <scratch>/<code>-2hg.html --set <CODE> --out <scratch>/publish \
    [--alias "Prepare Spell=Card Name" ...]
```

- The command:
  - finds every card name in the page, including prepare-spell and face names;
  - downloads each card's Scryfall image (cached), fills the page's hover map;
  - writes `<scratch>/publish/files.json`.
- Publish with the Artifact tool:
  - `file_path`: `<scratch>/publish/<code>-2hg.html`
  - `root`: `<scratch>/publish`
  - `files`: the contents of `files.json`
  - `icon: "cards"`
  - a one-sentence `description`
- Republish revisions to the same path so the URL stays put. A revision from a **later
  session** (the store, the next day) must pass the artifact's `url`: find it with
  `Artifact action=list`, read it first, then publish with `url`. Publishing without `url`
  from a new session creates a second page.
- Tell the user the page is private until they share it from its Share menu, and give them the link.
- A face name shared by several cards (e.g. a prepare spell on three cards) is skipped with a warning. Pass `--alias` for the one the sheet means.

## Revisions

Dan usually iterates while he's at the store:
- He adds threads: run `thread-extract` again and fold the results into *What's winning*.
- He corrects the product: update Team pairing and the checklist.
- He spots inconsistencies: fix them, then re-run the Phase 3 consistency audit, since a fix in one section often contradicts another.

Republish after each round and summarize what changed in plain English.
