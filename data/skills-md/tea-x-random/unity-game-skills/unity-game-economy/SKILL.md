---
name: unity-game-economy
description: "Design and balance a Unity game's economy and meta-progression. Use for core/reward/meta loops, soft and hard currencies, sources/faucets, sinks/drains, inflation, time-to-afford, progression/difficulty curves, churn walls, daily rewards, streaks, variable rewards, first-session generosity, lives/energy/cooldowns, session pacing, IAP catalogs, consumables, remove-ads, starter packs, price tiers/anchoring, paywalls, rewarded-ad hooks, payer/non-payer balance or pay-to-win risk. Model assumptions in a spreadsheet, soft-launch, then tune with live data. Pair with unity-monetization for SDK wiring, unity-analytics-liveops for measurement/experiments, and unity-gameplay-systems for the core loop."
---

# Unity game economy

A casual game that's *fun for one session* is a prototype; a game that *retains and monetizes* has an **economy and a meta-loop** designed on top of the mechanics. This skill is the design discipline that decides what currencies exist, where they come from and go, how progression paces against difficulty, and how the IAP catalog and rewarded hooks are shaped — then models the numbers in a spreadsheet so they can be tuned live. It is **design**, not wiring or measurement: `unity-monetization` wires the ad/IAP SDKs, `unity-analytics-liveops` measures and remote-config-tunes, and this skill decides *what the numbers should be and why*.

> **Balance is a spreadsheet exercise you then tune live — not a guess.** Model sources vs sinks and the cost curve before you ship (see `references/economy-model.md`), ship soft with safe defaults, and move the numbers against real ARPDAU + retention via remote config — never by hardcoded instinct.

## Doctrine

1. **Design the loop before the numbers.** The unit of retention is **core loop -> reward -> meta loop**: play a round (core), earn a currency/progress (reward), spend it on something that makes the next round better or unlocks new content (meta) — which creates the *reason to return*. No meta loop, no D7. Design this shape first; the balance numbers come after.
2. **Few, legible currencies.** Two is the casual default: one **soft** (earned constantly) and one **hard** (rare/premium). More currencies than players can reason about is a smell — every currency must answer "earned how, spent on what" in one sentence.
3. **Every currency needs balanced faucets and sinks.** A currency with sources >> sinks **inflates** (rewards stop feeling meaningful); a currency with nothing worth buying is a **dead economy** (no reason to play). Both kill retention. Balance is the whole job.
4. **Progression must outpace difficulty, never lag it.** If difficulty walls ahead of the player's earned power, they churn. Tune the power-vs-difficulty gap as a curve, live.
5. **Design for the non-payer AND the payer.** Only **~1.8% of F2P players ever make an IAP** — so the ~98% must be fully monetizable and satisfiable through **ads + free progression**, while the payer gets a catalog worth buying. This is why **hybrid (ads + IAP) is the default**, not pure-IAP or pure-ads.
6. **Model it, ship it soft, tune it live.** The sheet is the source of truth pre-launch; remote config is the source of truth post-launch. Keep every economy constant tunable (`unity-analytics-liveops`) so a bad curve is a config flip, not a resubmission.

## Currencies: soft vs hard

Keep the set small and each one legible.

| Type | Earned from | Spent on | Notes |
|------|-------------|----------|-------|
| **Soft** (coins, stars) | Gameplay constantly — level rewards, daily bonus, rewarded ads | Frequent, low-stakes purchases — upgrades, retries, consumables | The everyday faucet; players should always be a little flush |
| **Hard** (gems, premium) | Rarely — milestone rewards, occasional gifts, **IAP** | Premium/aspirational — skips, exclusive cosmetics, premium unlocks | Scarcity is the point; selling it is a core IAP lever |

- **Don't let soft currency buy everything** — a hard-currency sink that soft can't reach is what gives hard currency (and the IAP that sells it) value.
- **Don't proliferate.** Event tokens and per-system mini-currencies add up fast; each one taxes player comprehension. Add a third currency only when it earns its complexity.

## Sources & sinks (faucets & drains)

Every currency is a tank: **sources fill it, sinks drain it**. List both explicitly and balance the flow per player segment.

**Common sources (faucets):**
- **Level / round rewards** — the steady baseline earn; scales with the difficulty/length of the round.
- **Daily bonus / login streak** — a return incentive *and* a faucet (see reward schedules).
- **Rewarded ads** — opt-in, player-chosen faucet (double-coins, free-spin); a real currency source the non-payer controls (see rewarded hooks).
- **IAP** — the payer's faucet for hard (and bundled soft) currency.
- **Achievements / milestones** — one-time injections that pace early progression.

**Common sinks (drains):**
- **Upgrades / progression** — the primary, never-ending sink; the cost curve is the spine of the economy.
- **Retries / continues** — pay soft (or watch an ad) to keep going.
- **Cosmetics** — optional, no power; a deep, non-inflationary hard-currency sink.
- **Energy / lives refills** — a paced sink (use carefully; see session design).
- **Consumables / boosters** — single-use power for a round.

**Balance rule:** model expected **daily earn vs daily spend** per segment in the sheet. If sources >> sinks, you get **inflation** — add aspirational sinks (cosmetics, deeper upgrade tiers) before throttling faucets. If there's nothing compelling to spend on, you get a **dead economy** — add sinks before adding sources. Inflation and dead-end are the two failure poles; aim for "always a little short of the next thing you want."

## Progression & difficulty pacing

The meta loop is a **progression curve**: cost-to-advance rises, earned power rises, difficulty rises. Retention lives or dies on how these three track.

- **Power vs difficulty.** Earned power should stay **slightly ahead** of difficulty — enough that effort is rewarded, not so much that challenge evaporates. A difficulty spike that outruns affordable power is a **churn wall**.
- **Cost curve shape.** Early upgrades cheap and fast (dopamine, habit formation); later ones progressively more expensive (long-tail engagement, an IAP/rewarded-ad reason). Model the **time-to-afford** each key milestone for free vs paying players — that gap is your monetization pressure, and if it's punishing for free players it's a churn wall instead.
- **Tune live.** Difficulty constants and cost-curve multipliers belong in remote config; soft-launch and A/B the curve against retention. The difficulty *mechanics* (spawn rates, speed ramps, level layouts) are `unity-gameplay-systems`' **difficulty curve**; this skill owns how the *economy* paces against it.
- **No hard paywalls in casual.** A wall the player *can't* pass without paying churns the 98%. Make every wall passable with patience or a rewarded ad; sell the *skip*, not the *only path*.

## Reward schedules & daily engagement

The economy's job is **habit + return**, and reward scheduling is the lever.

- **Daily reward / login streak** — escalating rewards for consecutive days build a return habit; a broken streak should sting a little but recover gracefully (forgiveness keeps it from becoming punitive).
- **Variable / intermittent rewards** — unpredictable payouts (loot, spins, mystery chests) are stickier than fixed ones; use them as a faucet *and* an engagement hook. Keep odds honest and avoid mechanics that read as gambling to the App Store or to minors.
- **First-session generosity** — front-load rewards so new players feel rich and capable fast; the first session sets D1, and a stingy opening is a leak. Be generous early, meter later.
- **Milestone rewards** — chunk progression into visible "almost there" goals so there's always a near-term reason to play one more round.

## Session design (lives / energy / cooldowns)

Session-gating systems are **optional pacing tools — handle with care in casual**.

- **What they do:** lives/energy/cooldowns cap how much a player can do per session, stretching content and creating a natural stop (and an IAP/rewarded-ad refill sink).
- **The risk:** in casual they can **hurt retention** if punitive — locking out an engaged player who wants to keep going trains them to leave and not come back. The downside is asymmetric.
- **If you use them:** make refills cheap or ad-grantable, set regen so a normal session isn't blocked, and tune the cap live. Many successful casual games ship **without** energy at all and pace via difficulty + progression instead. Prefer the gentlest mechanism that achieves the pacing you need.
- **Natural session length** — design the loop so a satisfying session has an organic end (a level cleared, a goal hit), so you rely less on hard gates.

## IAP catalog & pricing design

Design the catalog for **both audiences** (Doctrine 5): the non-payer must thrive on ads + free progression; the payer needs things worth buying.

- **Consumables** — soft/hard currency packs, booster bundles, refills; repeatable revenue, the bulk of IAP.
- **Non-consumables** — **"remove ads"** (the highest-converting casual purchase — respect it: removing ads must actually remove the *interruptive* ads), premium unlocks, one-time cosmetics.
- **Starter pack** — a one-time, high-value, time-boxed bundle for new players; a classic first-purchase converter (the first purchase is the hardest; price it to break the seal).
- **Price tiers & anchoring** — offer a ladder (e.g. small / medium / large / whale). A high anchor tier makes mid tiers look reasonable; mark a mid tier "best value" to steer it. Use platform price points and localize.
- **Value framing** — show "x% more" / "best value" / bonus currency on bigger tiers; frame against what the currency *buys*, not abstract amounts.
- **No pay-to-win in casual.** Sell **time, convenience, and cosmetics** — not raw power that ruins the game for non-payers. Casual audiences churn on unfairness.

The actual StoreKit/IAP wiring (products, receipt validation, restore) is `unity-monetization`; this skill defines **what's in the catalog, at what tiers, framed how, and why**.

## Rewarded-ad economy hooks

Rewarded video is a **player-controlled currency source** — design the placements as economy faucets, not interruptions.

- **Natural opt-in moments:** **continue/revive** after a loss, **double-coins** on the result screen, **free-spin / free chest** on a timer, **earn premium currency** at a slow trickle, **unlock a temporary booster**. The player chooses to watch in exchange for value — high satisfaction, no interruption tax.
- **Balance them as faucets.** A revive or double-coins is a real source — fold it into the sources/sinks model so heavy rewarded use doesn't inflate the economy. Cap rewarded earns per day/session if the math needs it.
- **Don't cannibalize IAP** — keep rewarded grants meaningful but slower than buying; the ad path satisfies the non-payer, the purchase path saves time for the payer.
- The SDK wiring, frequency policy, and cadence for these placements live in `unity-monetization`; this skill designs **where they sit in the loop and what they pay out**.

## Balancing & tuning

1. **Model it in a sheet first** (`references/economy-model.md`): currencies, every source with its rate, every sink with its cost, expected daily earn vs spend per segment, the progression cost curve, the IAP catalog with prices, and the balancing checks (faucet/sink ratio, time-to-afford, payer vs non-payer paths).
2. **Sanity-check the poles:** is daily earn within a sane band of daily spend (not runaway inflation, not a dead economy)? Is time-to-afford each key milestone reasonable for free players and a clear time-save for payers?
3. **Ship soft with safe in-code defaults**, every economy constant behind remote config.
4. **Tune live via A/B** against **ARPDAU + retention** (`unity-analytics-liveops`) — change one lever (a source rate, a sink cost, a price tier) at a time, read the KPI it should move, promote the winner. The sheet is your hypothesis; the live data is the verdict.

## Pitfalls

- **Pay-to-win in casual** — selling power that disadvantages the 98% non-payers; they churn. Sell time/convenience/cosmetics.
- **Inflation** — sources >> sinks; rewards stop feeling like anything. Add aspirational sinks before throttling faucets.
- **Dead-end economy** — nothing compelling to spend on; the meta loop collapses and so does retention. Add sinks.
- **Punitive energy/lives** — locking out an engaged player. Use the gentlest pacing that works, or none.
- **Paywalls too early** — a hard wall in the first sessions kills D1/D7. Front-load generosity; meter later.
- **Too many currencies** — comprehension tax; players who can't reason about the economy don't engage with it.
- **Tuning by instinct instead of data** — the sheet is a hypothesis; ARPDAU + retention is the verdict.

## Where this sits

- **`unity-monetization`** *wires* the ad/IAP SDKs (StoreKit products, rewarded/interstitial delivery, cadence policy); this skill designs the **catalog, pricing, and rewarded placements** it wires.
- **`unity-analytics-liveops`** *measures* ARPDAU/retention/IAP-conversion and provides remote config + A/B; this skill provides the **economy model and the levers** to tune through it.
- **`unity-gameplay-systems`** builds the **core-loop mechanics and difficulty curve**; this skill wraps them in the **reward + meta loop** and paces progression against that difficulty.
- **`unity-game-director`** sets the **retention/monetization north-star**; this skill designs the economy that hits it.

## Field notes & lessons

- The meta loop is the retention engine — a fun core loop with no reason to return is a one-session game; design **core -> reward -> meta** before touching numbers.
- Balance is the whole job, and it has two failure poles: **inflation** (faucets >> sinks, rewards feel worthless) and **dead economy** (no worthwhile sinks, nothing to play for). Aim for "always a little short of the next thing you want."
- Design for the **~98% who never pay** first — they must be fully satisfiable and monetizable via ads + free progression — *then* build a payer catalog on top. Hybrid is the default; pure-IAP leaves the table.
- Energy/lives are a sharp tool: the downside (churning an engaged player) is asymmetric, so prefer the gentlest pacing or ship without it and pace via difficulty + progression.
- "Remove ads" and a time-boxed **starter pack** are the workhorse first purchases in casual — the first purchase is the hardest to earn, so price the seal-breaker to convert.
- Keep every economy constant behind remote config with a safe default; a bad curve found in soft launch should be a config flip, not an App Store resubmission.
- The spreadsheet is a hypothesis, not the answer — ship soft and let **ARPDAU + retention** decide, changing one lever at a time.
