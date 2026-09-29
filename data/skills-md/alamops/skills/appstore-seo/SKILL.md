---
name: appstore-seo
description: (alamops) App Store Optimization (ASO) for iOS App Store and Google Play — write, rewrite, and audit store listing metadata to rank higher and convert better. Triggers — "/appstore-seo", app store SEO/ASO, "improve my app store ranking", "nobody finds my app in search", keyword research for an app, writing or rewriting app name / subtitle / keyword field / short & full description / promotional text / release notes / screenshot captions, "review my App Store listing" or "audit this app" given an App Store ID, an `apps.apple.com` link, or a `play.google.com` link, competitor listing teardowns, localizing a listing into new storefronts, planning a Product Page Optimization or Play store-listing experiment, pre-launch metadata prep before submitting to App Store Connect or Play Console, and **Apple Ads / Apple Search Ads keyword and campaign planning** — building a Brand/Generic/Competitor/Discovery structure, negative keyword lists, custom product page mapping, or mining the Search Terms report back into the listing. Pulls the live listing and competitor set from public Apple endpoints, scores it, then emits ready-to-paste fields (character-validated) in code blocks and saves them under `docs/appstore/`. Not for App Review compliance (use `appstore-review`) and not for website SEO.
---

# App Store SEO (ASO)

Get an app found in store search, then get the people who find it to install. Tone: a senior ASO lead who has shipped listings that had to survive both an algorithm and a marketing VP — specific, evidence-backed, allergic to adjective soup.

## Why this skill exists

Most "app store SEO" advice is a folk practice: pile adjectives into the description, repeat the keyword, hope. That fails on iOS for a structural reason — **Apple does not index the description at all**. Rank comes from a small set of indexed fields whose character budgets are tiny (30 / 30 / 100), and the algorithm builds search phrases by *combining tokens across those fields*. So every repeated word is a wasted character, and a beautiful description with no keyword plan ranks nowhere.

Google Play is the opposite: the long description *is* indexed, so the same copy can't be pasted into both. Treating the two stores as one job is the second most common failure.

There is a third thing most treatments miss: **Apple Ads runs on the same keyword system.** Apple judges whether your ad is relevant for a term partly from your product page metadata, so the 100-character keyword field is not only an organic asset — it is what keeps your cost per tap down. In the other direction, the Search Terms report is the only source of queries real users actually typed, and the keyword popularity score is the only genuine volume figure that exists. Doing ASO without wiring it to the paid lane throws away both the cheapest data and half the return on the same research.

This skill turns ASO into an engineering task: pull ground truth, mine keywords against real competitor data, allocate a fixed character budget, validate every field programmatically, then hand over copy-paste-ready blocks, the Apple Ads plan built from the same research, and the experiment that proves it worked.

## Scope check before you start

This skill is about **discovery and conversion**. If the user is asking whether Apple will *reject* the app (guideline numbers, IAP rules, privacy manifests), that's `appstore-review` — say so and hand off. Metadata rejection risk (2.3 accurate metadata, 5.2 competitor trademarks) is in scope here because it's a direct product of the copy this skill writes.

On the paid side: **keyword and campaign *structure* planning is in scope** — which terms to bid on, how to split Brand / Generic / Competitor / Discovery, negatives, which custom product page each ad group points at, and how to feed the Search Terms report back into the listing. Ongoing bid and budget management of a live account — pacing, CPA tuning, dayparting — is a different job and this skill doesn't pretend to do it; it sets the structure the bidding then operates inside.

## The three modes

Pick the mode from what the user gave you. When in doubt, ask once — the modes produce different artifacts.

| Mode | Trigger | Output |
| --- | --- | --- |
| **Audit** | An App Store ID, `apps.apple.com` link, or Play link, with no ask to rewrite | Scorecard + prioritized findings, `docs/appstore/audit.md` |
| **Generate** | A repo, product description, or PRD with no live listing yet (pre-launch) | Full field set, `docs/appstore/` |
| **Audit → rewrite** (most common) | A live app *and* "improve / fix / rewrite" | Both: audit first so the rewrite is evidence-backed, then the full field set |

Never rewrite before auditing when a live listing exists. Rewriting blind throws away the one thing that makes the recommendation defensible — what the current listing already ranks for and what the competitors are doing.

## Workflow

### 1. Scope the run

Establish these before writing a single field. Ask only for what you can't infer — a bundle of questions the user has to answer serially is worse than three well-chosen ones.

- **Target app**: App Store ID / URL, Play package ID / URL, or "not launched yet"
- **Storefronts & locales**: infer from the product before defaulting. An app whose value is jurisdiction-bound (UK tax, German banking, Brazilian PIX) belongs in that storefront, and running it against `us` produces a keyword set for a market it can't serve. Fall back to `us` + `en-US` only when there's genuinely no signal, and say that's what you assumed.
- **Category**: primary + secondary intent (this constrains keyword competition, and Apple auto-indexes the category name so it must not appear in the keyword field)
- **Competitors**: 3–8. If the user doesn't name any, derive them in step 2 from the live "You Might Also Like" shelf and from search results for the head terms.
- **Positioning**: what the app actually does, who for, and the one thing it does better. If `docs/` already holds `business-review` / `to-prd` output (`ICP_ANALYSIS.md`, `CLIENT_PERSONAS.md`, a PRD), read it — that's the positioning input, and reusing it keeps the store listing consistent with the rest of the GTM work.
- **Launch window and account type**, for pre-launch work. If Android is in scope with a launch under ~6 weeks away, check whether the Play account is an individual one — those must complete a 14-day closed test with a minimum tester count before production access, which has killed more announced launch dates than any copy decision. Surface it immediately; it changes the plan, not just the wording. See `references/play-fields.md`.
- **Apple Ads**: do they run it, or plan to? This changes the deliverable (step 7) and, more importantly, unlocks the only real volume data and the only record of what users actually searched.
- **Constraints**: trademark limits, legal-reviewed claims, brand voice, a name that can't change.

### 2. Pull ground truth

Never audit from a screenshot or from memory of the app. Pull it live from Apple's public endpoints — no key, no SDK, nothing to install. **`references/data-and-endpoints.md` is the recipe**: the exact URLs, the browser User-Agent you must send, the rate-limit backoff, and paste-and-run parse snippets. Follow it to get the name, subtitle (which the API doesn't expose — it's read out of the store page's embedded JSON), description, release notes, version cadence, ratings, category, screenshot count, locales, and the "similar apps" shelf with *their* names and subtitles — the cheapest competitive keyword corpus there is. Save the raw pulls under `docs/appstore/.data/`.

Two limits to be honest about, both of which you should state in the report rather than paper over:

- **The keyword field is private.** Apple never exposes it. You infer keyword strategy from what the app *ranks* for (step 3), never claim to have read it.
- **Google Play has no public API.** For Play listings, fetch the `play.google.com/store/apps/details?id=<pkg>&hl=en&gl=US` page with WebFetch (see the reference for the truncation caveat).

If the network is unavailable, don't fake it — say the audit is running on user-supplied metadata only, and skip every claim that needed live data.

### 3. Mine keywords

This is where the ranking actually comes from, so it gets the most effort. Build a keyword table, not a word cloud.

**Seed** from five sources, which fail in different directions and so cover each other:
1. What the app does (features, objects, verbs the user would type)
2. The problem in the user's words — mine the app's own reviews and competitor reviews (the reviews-RSS recipe in `references/data-and-endpoints.md` §3) for the vocabulary real users type, which is reliably different from the vocabulary the product team uses
3. Competitor names + subtitles from step 2 (these are their *chosen* head terms — they paid for that research already)
4. Category conventions and adjacent use cases
5. Long-tail intent: modifiers like `for <audience>`, `<object> planner`, `free`, `offline`, `widget`

**Validate** each candidate against real store data before it gets a character of budget. `references/data-and-endpoints.md` §4 has the Search API recipe and the difficulty/intent formulas: for each term it gives who currently surfaces, a **difficulty** score from the median top-10 rating count (a term owned by three apps with 100k+ ratings is not winnable this quarter), whether the target app appears at all and where, and an **intent** signal (how many top-10 apps carry the whole term in their name — zero means Apple is fuzzy-matching and nobody targets it directly).

Pace it: Apple rate-limits this endpoint hard (403 *and* 429 both mean "slow down"), so budget roughly **10 seconds per term** — 40 terms is a ~6-minute job that will blow past a default 2-minute command timeout. Run it in batches of ~15. Terms that still fail after the retries are `unscored` — report them as unscored, never dropped or guessed.

**Score** every candidate on three axes and keep the table in the deliverable so the choices are auditable:

- **Relevance** (1–5) — would someone typing this install *this* app? Irrelevant traffic damages the conversion rate that feeds back into rank.
- **Volume** (1–5) — no public endpoint exposes search volume, and result-set depth does not proxy for it (a nonsense phrase still returns ~180 fuzzy matches), so the script deliberately doesn't invent a number. **Ask whether the user has an Apple Ads account** — it's worth one question, because the keyword planner's popularity score (0–100) is the only genuine volume figure in existence, and the Search Terms report lists queries real users actually typed. Both beat every inference in this workflow. If they have it, use it and say so; if not, triangulate from competitor adoption and category conventions and label it an estimate. Presenting a guessed volume as data is the fastest way to lose trust in the whole document.
- **Difficulty** (1–5) — median rating count and brand strength of who currently ranks.

Target the band where relevance is 4–5 and difficulty is beatable. A term you rank #40 for sends zero installs; two long-tail terms you rank top-3 for beat one head term you rank #50 for. Say this out loud when the user pushes for the vanity head term — then include it anyway if they insist, because these are business decisions, not algorithm decisions.

Depth on method, storefront-locale expansion, and the ranking model: `references/keyword-strategy.md`.

### 4. Allocate the character budget

Apple's indexed surface is roughly 160 characters total. Treat it as a budget allocation problem with one dominant rule:

> **Apple combines tokens across app name, subtitle, and the keyword field to form searchable phrases. A word only needs to appear once, anywhere in that set.** Repeating it costs characters and buys nothing.

So the field-writing order is fixed, because each step spends from a shared pool:

1. **App name (30)** — brand + the single highest-value head term. `Brand: Head Term` or `Brand — Head Term`. The name carries the most ranking weight of any field and is the first thing a user reads.

   **Always run the name-collision check — including in generate/pre-launch mode, and including a name the user handed you.** This is the step most easily skipped when the name feels "given," and pre-launch is exactly when it matters most: a collision found now can still be fixed by renaming, and a collision found after launch cannot. `references/data-and-endpoints.md` §5 has the recipe: search the name, then look for exact collisions with live apps and for how many apps already lead with the same brand token. When auditing a *live* app, exclude its own ID from the results, or it shows up as its own exact-name match and buries any real collision. A name collision outranks anything in the keyword field — it splits brand search, wastes word of mouth, and risks rejection under 4.1 (copycats) or a 5.2 trademark complaint. Skipping it means shipping a name someone else already owns.
2. **Subtitle (30)** — the second-tier terms *plus* the value proposition, because unlike the keyword field the subtitle is visible copy that has to convert. It's the hardest field to write; expect several passes.
3. **Keyword field (100)** — everything left. Comma-separated, **no spaces after commas** (a space is a wasted character), singular forms, no words already used in the name or subtitle, no category names, no `app`/`free`/`best`, no stop words, and no competitor trademarks (5.2 — Apple removes them and it invites a legal notice).
4. **Promotional text (170)** — not indexed; it's the updatable banner above the description. Use it for the current campaign, launch, seasonal hook, or social proof, since it changes without shipping a build.
5. **Description (4000)** — not indexed on iOS, entirely a conversion asset. The first ~170 characters render before "more", so the first three lines must land the value proposition alone. Then scannable benefit blocks, social proof, and a close.
6. **What's New (4000)** — real changes in user language. "Bug fixes and performance improvements" wastes a field that returning users actually read.

For Google Play, the copy is written **separately**, not translated from the iOS version: the title (30) and short description (80) are indexed *and* the full description (4000) is indexed too, so the head term belongs in the long copy at a natural 2–3 mentions. Density beyond that reads as stuffing to both the algorithm and the human.

Exact limits, indexing behavior per field, and the asset specs: `references/apple-fields.md` and `references/play-fields.md`.

### 5. Validate before you show anything

Character limits are the one place where a confident-sounding answer is worst — a field that's 3 characters over gets silently rejected in App Store Connect and the user finds out at submission time. Hand-counting fails; in testing, models that "knew" the limits still miscounted repeatedly. So **run the checker in `references/validation.md`** — a paste-and-run Python block (nothing to install) that counts in UTF-16 code units the way App Store Connect does, hard-fails on over-limit fields and keyword-field syntax, and flags the expensive strategy mistakes (words duplicated or *inflected* across name/subtitle/keywords, category names and filler burning budget, wasted budget, stuffing).

**Never present fields that haven't been checked clean.** Iterate until the checker prints `CLEAN`, then show the output. If you genuinely can't run code, apply the reference's rules by hand — but the UTF-16 count is not something to eyeball.

### 6. Cover conversion, not just ranking

Ranking without conversion is a leak, and Apple feeds conversion rate back into ranking, so the two compound. Every deliverable includes a creative brief covering the icon, the first three screenshots (roughly 60% of visitors never scroll past the fold), caption copy that's legible at thumbnail size, an app preview that works muted in its first three seconds, and the ratings-prompt strategy. Details and current asset specs: `references/creatives-cvr.md`.

**When auditing a live listing, actually look at the screenshots.** The listing lookup returns `screenshotUrls` — download them and read them. Counting them tells you almost nothing, and a creative critique written without opening the images is guesswork dressed as analysis. What only looking will give you: a caption unreadable at thumbnail size, a screenshot with no caption at all, stale content (a visible date, old OS chrome, a discontinued feature), inconsistent alignment across the set, and whether the first three actually carry the value proposition or just show chrome.

Download them with a couple of lines of Python against the saved listing JSON (`screenshot_urls`), write them into `docs/appstore/.data/`, then read the files. If you genuinely cannot view images in this session, say so in the report and mark the creative dimension unscored — don't score it blind.

### 7. Wire the research into Apple Ads

The keyword table you just built is a campaign plan that hasn't been formatted yet. Producing it costs almost nothing extra and roughly doubles the return on the research, so do it unless the user has said they don't run ads.

Bucket the scored keyword table into the four campaigns that have genuinely different economics — Brand (defensive, cheapest, highest converting), Generic (the volume and the cost, split by difficulty), Competitor, and Discovery (whose job is finding queries you didn't think of, not installs) — and write the negative keyword lists, which is the step teams skip and the reason campaigns look unprofitable when they aren't. `references/apple-ads.md` has the exact bucketing rule and the negatives to add to each campaign.

Two things to carry into the write-up, because they're the ones people get backwards:

- **Competitor brand names are allowed in Apple Ads and forbidden in the organic keyword field.** Same word, opposite rule. Leaving competitor traffic uncontested and getting your metadata stripped are both avoidable.
- **The "don't target a feature the app lacks" rule (see *Things that go wrong*) applies to bids too** — on paid it isn't a slow relevance drag, it's an immediate bill for installs that churn. Add those terms as negatives here.

Then set the return leg: after ~4 weeks of spend, the Search Terms report gets mined back into the keyword field. That's the highest-quality ASO input that exists, and it only arrives if someone schedules it. `references/apple-ads.md` has the campaign structure, match-type discipline, custom-product-page mapping, and what to read from TTR vs. CR.

### 8. Ship the artifacts

Produce both — the code blocks so the user can paste immediately, and the files so the work survives the conversation.

Write only the stores that are in scope. If the user asked about App Store Connect and never mentioned Android, omit the Play sections and the `android:` block entirely rather than inventing a Play strategy they didn't ask for — the checker in `references/validation.md` only flags a section that is present.

Write to `docs/appstore/` (create it), one file per concern:

```
docs/appstore/
├── README.md              # index + exactly where each field goes in App Store Connect / Play Console
├── audit.md               # audit and audit→rewrite modes only: scorecard + findings
├── keyword-research.md    # the scored keyword table + the terms deliberately rejected, with reasons
├── metadata.en-US.md      # copy-paste blocks with live UTF-16 character counts
├── metadata.<locale>.md   # one per additional locale
├── creative-brief.md      # icon, screenshots 1-N with captions, preview video script
├── apple-ads.md           # campaign map, negatives, CPP mapping, the 4-week feedback loop
└── experiments.md         # what to test first, how to measure, when to call it
```

**Proposed in-app purchase and in-app event names go in the deliverable, not in the paste-ready metadata block.** They're indexed surface worth recommending, but an in-app event that doesn't exist yet is a rejection if someone pastes it in and submits. Put them in their own clearly-labelled section with what has to be built first.

**Keep the raw pulls.** Everything the scripts fetched goes in `docs/appstore/.data/` — listing JSON, keyword scout output, reviews, the ads plan CSV. It costs nothing and it is what makes every number in the deliverable re-checkable months later by someone who wasn't in the conversation. A recommendation whose evidence has evaporated is indistinguishable from a guess, and will be treated as one.

Then, in the chat, show the fields inline as fenced blocks with character counts — the user is usually mid-task with App Store Connect open in another tab:

```
App Name (21/30)
Streak: Habit Tracker

Subtitle (29/30)
Daily routines & goal streaks

Keywords (99/100)
reminder,checklist,journal,motivation,discipline,consistency,ritual,calendar,challenge,mood,planner
```

Notice what the keyword field does *not* contain: no `habit`, `tracker`, `daily`, `routine`, `goal`, or `streak` — every one of those is already carried by the name or subtitle, and Apple combines tokens across all three fields, so repeating them would buy nothing. That is the discipline the whole allocation step exists to enforce; the example is only useful if it models it.

Do not paste the whole 4000-character description into chat — write it to the file and show the first 170 characters (the above-the-fold portion) plus a pointer to the file.

If `docs/appstore/` already exists from a previous run, read it first and diff against it rather than silently overwriting. Show what changed and why; a user who has already pasted these fields into App Store Connect needs to know exactly which ones to re-paste.

## The audit scorecard

In audit modes, score five dimensions, 20 points each. The number matters less than the breakdown — it forces coverage of the dimensions people skip (usually Coverage and Trust) and makes progress measurable on a re-run.

| Dimension | What earns points |
| --- | --- |
| **Discoverability** (20) | Head term in the name; subtitle carrying distinct terms; no wasted duplication across indexed fields; plausible keyword coverage given what the app ranks for; category fit |
| **Conversion** (20) | Icon legibility at 60pt; first three screenshots carrying the value prop; caption readability; app preview present and muted-safe; first 170 characters of description standing alone |
| **Trust** (20) | Rating average and volume vs. category peers; review recency and developer responses; update cadence; What's New written for humans |
| **Coverage** (20) | Localized into the storefronts where the traffic is; per-locale keyword sets rather than machine translation; custom product pages for paid traffic |
| **Hygiene** (20) | No competitor trademarks (5.2); no metadata that overstates the app (2.3); no stuffing; promotional text current; URLs live |

**Score only what you can observe.** When you have the live listing and its screenshots, all five dimensions are observable — score each out of 20 and report a true `/100`. But some dimensions need data you may not have: no App Store ID means no Conversion, Trust or Coverage; a pre-launch app has none of them. Mark *those* dimensions `unscored`, report the total over what you actually scored (`31/40 across two dimensions`), and don't dress it up as a `/100`. Silently scoring an unobservable dimension from guesswork is worse than a smaller number, because the user can't tell which parts of the score are real. Say what you'd need to score the rest — usually just the App Store ID (and, for Conversion, opening the screenshots).

When the user runs Apple Ads, add a short unscored **paid-lane** section to the audit rather than a sixth dimension: terms they bid on that appear nowhere in their indexed metadata (paying a relevance penalty on every tap), terms ranking organically that aren't defended by a Brand campaign, and whether ad groups point at custom product pages or all dump into the generic page. These are cheap to check and usually worth more than another organic nit.

Each finding uses this shape, ordered by expected install impact — not by how easy it is to fix, and not in the order you happened to find them:

```
**<title>** — <impact: high | medium | low>
- *Now:* <the current value, quoted, with its character count>
- *Problem:* <one sentence — the mechanism by which this costs installs>
- *Fix:* <the concrete replacement string, validated>
```

## Things that go wrong

These are the failure modes worth actively steering against — most of them look like good work until someone checks.

- **Adjective soup.** "The best, most beautiful, powerful app for organizing your life" ranks for nothing and converts poorly. Specific objects and verbs are what people type and what makes the app sound real.
- **Keyword stuffing the iOS description.** It does nothing on iOS (not indexed) and it costs conversion. On Play, past ~3 natural mentions it starts working against you.
- **Symmetric stores.** Copy pasted from App Store to Play wastes Play's indexed long description and blows past its different limits.
- **Machine-translated localizations.** Keywords don't translate — people search different concepts in different languages. A translated keyword field is worse than an untranslated one because it looks done.
- **Presenting ASO lore as fact.** Parts of this field are community technique that Apple has never documented — the clearest example being whether a storefront indexes a second locale's metadata. These are often worth trying, because they're cheap. They are never worth stating flatly, and never worth calling the biggest win in a deliverable. Label an unverified technique as unverified, attach the experiment that would confirm it, and let the user decide. A confident-sounding claim the user later finds out was folklore costs you the credibility of everything else in the document.
- **Unwinnable head terms.** "fitness" is not a strategy for an app with 200 ratings. Win the long tail first; head terms become reachable once volume and conversion build.
- **Claims the app can't back.** Metadata that promises features the binary doesn't have is a 2.3 rejection — the ASO win evaporates when the release is held.
- **Keywording a feature the app doesn't have.** The tempting version is subtle: a term is clearly winnable, the app is *nearly* that thing, so it goes in. Don't. Users who search it arrive, don't find it, and either churn or leave a one-star review — and both feed the conversion and strength signals that set your rank for everything else. Reviews are the evidence to use here: if people are asking for the feature, the app doesn't have it. On the paid side the same mistake bills you immediately. When you reject a term for this reason, put it in the deliverable's rejected list with the evidence, so nobody re-adds it next quarter.
- **Running ads and ASO as separate projects.** The same keyword research serves both, metadata relevance sets the tap price, and the Search Terms report is the best ASO input there is. Teams that split the two across two owners pay twice for worse data.
- **Inventing commercial terms.** Prices, trial lengths, free-tier limits, subscription terms, and the legal entity name are facts about the business, not copy decisions. Writing a plausible `£6.99/month` into paste-ready store copy is worse than leaving a gap, because a plausible number gets shipped unchecked. Use an obvious `{{PRICING}}` placeholder and list what you need. The same goes for any feature you inferred rather than confirmed — mark it, and keep the marker out of the paste-ready blocks so it can never be pasted into a live listing by accident.
- **Untracked changes.** Metadata changed without recording the date and baseline means you can never attribute the result. Every deliverable records the "before" values.
- **Rewriting the app name reflexively.** Renaming resets brand recognition and existing ranking; it can be right, but it needs to be argued explicitly, not slipped in.

## Reference files

Load these as needed — they're detail, not workflow, and pulling all of them in every run is wasteful:

- `references/apple-fields.md` — every App Store Connect field: limit, indexed or not, where it appears, how to write it, plus asset specs
- `references/play-fields.md` — Google Play equivalents and where the strategy diverges
- `references/keyword-strategy.md` — research method, phrase combination, storefront-locale expansion, difficulty modeling, what Apple's ranking actually weighs
- `references/creatives-cvr.md` — icon, screenshots, preview video, custom product pages, PPO and Play experiments, ratings strategy
- `references/apple-ads.md` — the ASO/Apple Ads flywheel, campaign structure, match types and negatives, custom product page mapping, and mining the Search Terms report back into the listing
- `references/data-and-endpoints.md` — the recipe for every live pull: Apple's lookup / search / reviews / store-page endpoints, the rate-limit rule, subtitle & competitor-shelf parsing, and the difficulty / intent / name-collision computations
- `references/validation.md` — the character-limit and keyword-field checker (paste-and-run, plus the rules in plain terms)

**No bundled scripts, no dependency.** Every mechanical step — pulling the listing, scouting keyword difficulty, checking name collisions, counting characters, bucketing ads — is documented as a recipe in the two reference files above, with paste-and-run Python snippets that use only the standard library and Apple's public endpoints. Run a snippet inline when you can (it's faster and exact), or apply the same rules by hand where you can't run code. The one place not to improvise is the UTF-16 character count — use `references/validation.md` so a field that's silently over-limit doesn't reach the user.

Character limits and asset specs do drift — Apple has changed required screenshot sizes and added indexed surfaces more than once. The values in the references were correct as written and are stable year over year, but when a submission deadline rides on it, confirm against App Store Connect or fetch Apple's current spec page, and tell the user which values you verified live versus took from the reference.

## Example invocations

- "/appstore-seo" with an App Store link → audit → rewrite: pull the listing and its competitor shelf, score it, mine keywords, emit validated fields and `docs/appstore/`.
- "Nobody finds my app when they search for meditation apps" → audit weighted to Discoverability; check whether the term is winnable at the app's current rating volume before promising a rank.
- "We're launching in 3 weeks, write our App Store and Play listings" → generate mode from the repo and any PRD; both stores, written separately; full `docs/appstore/`.
- "Compare our listing to these 4 competitors" → fetch all five, produce a keyword-overlap and positioning matrix, then recommend the gaps worth taking.
- "We're about to start running Apple Ads — what should we bid on?" → do the keyword research as normal, then step 7: campaign map, negatives, and the note that the same terms belong in the metadata to keep the tap price down.
- "Localize our listing for Brazil and Mexico" → per-locale keyword research (never translation), one metadata file per locale, with the storefront-indexing note in `references/keyword-strategy.md`.
