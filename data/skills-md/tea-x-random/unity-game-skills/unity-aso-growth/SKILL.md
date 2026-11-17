---
name: unity-aso-growth
description: "Improve discovery and installs for a Unity iOS game. Use for App Store Optimization, app icons, title/subtitle/keywords, descriptions, screenshots, app-preview video, product pages, Product Page Optimization/A-B tests, conversion rate, user acquisition, growth creatives, soft-launch tests, ATT attribution, SKAdNetwork/AdAttributionKit conversion values, ratings/reviews with SKStoreReviewController, localization, or Apple featuring readiness. Pair with unity-analytics-liveops for retention and attribution, unity-monetization for ATT/SKAN, unity-qa-release for submission, unity-localization for listings, and unity-aaa-graphics for store creative quality."
---

# Unity ASO & growth

A casual iOS game succeeds or fails on **discovery and conversion** as much as on gameplay. Most discovery comes through the App Store listing itself — icon, title, screenshots, and preview video — and through whatever paid user acquisition (UA) you run. This skill covers how to make a Unity casual game *findable* and *installable*: ASO, store-listing creatives, store-side A/B testing, UA basics, iOS attribution under ATT, ratings, localization, and featuring readiness.

> **Don't pour acquisition spend into a leaky funnel.** Retention is set *before* acquisition. Validate D1/D7 retention and ARPDAU in a soft launch first (see `unity-analytics-liveops`); only then scale UA. Buying installs for a game that doesn't retain just burns money faster.

## Doctrine

1. **Retention before acquisition.** A leaky funnel makes every install more expensive. Clear your retention/ARPDAU bar in soft launch *before* spending to scale. UA amplifies whatever the game already does — good or bad.
2. **Discovery is mostly the listing.** Before any ad spend, the highest-leverage marketing asset is the store page. Icon + first screenshots + preview video decide whether a browsing user taps "Get."
3. **Readability at thumbnail scale is the bar.** Players see the icon at a tiny size in search results and the first screenshots in a scrolling gallery. If it isn't legible and compelling at that scale, it doesn't work — polish at full size is irrelevant.
4. **Match the ad to the game.** Misleading creatives buy installs that churn on day one and tank retention (and your store rating). Creatives should sell the actual experience.
5. **Test one variable at a time, to significance.** Whether it's a store A/B test or an ad creative, change one thing and let it reach a real sample before you decide.
6. **Measure within iOS privacy reality.** Post-ATT, install attribution runs through SKAdNetwork / AdAttributionKit, not IDFA. Set conversion values to capture early-funnel signal and hand measurement to your attribution SDK + `unity-analytics-liveops`.

## App Store listing (ASO)

The store product page is the conversion surface. Optimize each element for *both* discovery (keywords, ranking) and conversion (the tap-to-install decision).

- **App icon.** The single most important creative. Must be legible at thumbnail size, instantly readable, and on-brand — one strong focal shape, high contrast, minimal text. It appears in search, on the home screen, and as your de-facto logo everywhere. Get the visual quality right with `unity-aaa-graphics` / `unity-asset-designer`; the icon should be on-model with the game's art.
- **Title + subtitle.** Both are indexed for keywords *and* read by humans. Lead with the real app name, then work in the highest-value keywords without becoming word salad — readable beats stuffed. The subtitle is prime keyword + value-proposition real estate.
- **Keyword field.** The hidden 100-character keyword field (separate from title/subtitle). Use commas, no spaces, no repeats of words already in title/subtitle, singular/relevant terms, no competitor brand names. Every wasted character is lost discovery.
- **Screenshots.** Lead with the value/benefit, not a raw gameplay dump. The **first 2–3 screenshots** matter most — many users never scroll past them, and they show in search results. Caption each with a short benefit-driven line ("Match. Blast. Relax."), use a consistent visual template, and make them readable at gallery scale.
- **App preview video.** Casual conversion is video-first. Show the core loop and the satisfying moment in the first few seconds (it can autoplay muted, so it must read without sound). Keep it the real game, not a cinematic.
- **Description.** Lead with the hook in the first lines (the rest is behind "more"). Reinforce the value proposition; it's lightly weighted for ASO but matters for the users who read it.

## Product Page Optimization (store-side A/B)

Use Apple's **native Product Page Optimization** (in App Store Connect) to A/B test icon, screenshots, and app-preview video against the live page with real App Store traffic — no SDK, attribution baked in.

- **Test one variable at a time.** Treatment A swaps the icon; treatment B swaps the first screenshots — don't change both in one cell or you can't attribute the lift.
- **Let it reach significance.** Don't call a winner on a day of noisy data; let the test accumulate a real sample before promoting.
- **Custom Product Pages** (a complementary feature) let you tailor the page to specific ad campaigns/audiences — pair the creative a user clicked with a matching landing page to lift install rate.

## Creatives & user acquisition

- **Concept must match the game.** The creative that converts *and* retains shows the actual mechanic. Fake-gameplay / decoy ads spike installs and crater D1 — net negative once you measure retained users, not raw installs.
- **Video-first for casual.** Short, hook-in-the-first-seconds video out-converts static for most casual games. Produce several concepts; the winner is rarely the one you predicted.
- **Iterate creatives continuously.** Creatives fatigue. Always have new concepts in rotation; kill losers fast, scale winners.
- **Soft-launch the UA before scaling.** Run a small paid test (limited budget/geo) to read install-rate, cost signal, and early retention of *acquired* users before committing real spend. Scale only what the data supports.

## Measurement under ATT (iOS)

Post-App Tracking Transparency, you generally cannot rely on IDFA-level attribution. Install measurement runs through Apple's privacy-preserving frameworks:

- **SKAdNetwork / AdAttributionKit** are the attribution layer. Your ad networks and attribution SDK (AppsFlyer/Adjust/Singular/Tenjin) handle the postbacks.
- **Set conversion values to encode early-funnel signal** — e.g. tutorial complete, level N reached, first purchase — so you can compare campaign quality, not just install counts.
- **Hand the wiring to `unity-analytics-liveops`** (conversion-value mapping, privacy manifest, ATT prompt timing) and `unity-monetization` (ATT / SKAdNetworkItems in the build). Keep growth decisions principle-level here.

> Treat published eCPMs, ROAS curves, and ATT opt-in percentages as perishable and report-scoped — they move every quarter and several widely cited figures have been refuted. Measure your own game; don't hardcode someone's number into a plan.

## Ratings & reviews

High ratings directly lift store conversion (and ranking) — they're part of ASO, not separate from it.

- **Prompt at a positive moment** via Apple's `SKStoreReviewController` (e.g. just after a level win or a satisfying streak), never mid-failure or mid-friction.
- **Apple rate-limits the native prompt** (a few times per year per user) and may suppress it — so spend the prompt wisely; don't trigger it on first launch.
- **Never beg or gate.** Don't block gameplay behind a rating, bribe for 5 stars, or nag. Use the system prompt as Apple intends; it keeps the user in-app.
- **Respond to the funnel:** if ratings are low, the problem is upstream (the game or a misleading creative) — fix that, don't out-prompt it.

## ASO localization

The listing is one of the highest-ROI things to localize — a localized icon caption, title, keywords, screenshots, and description meaningfully lift discovery and conversion in non-English markets.

- **Localize the keyword field per locale**, not just translate it — search terms differ by language and region.
- **Localize screenshot captions and the preview** for major markets you actually target.
- Coordinate with `unity-localization` so in-app language and the store listing stay consistent (a player who installs from a localized page expects a localized game).

## Featuring readiness

Editorial featuring by Apple is high-leverage and free, but not buyable — you make the game *featurable*:

- **Polish and stability.** Apple features games that feel finished: no crashes, smooth performance, no rough edges (lean on `unity-qa-release`).
- **Follow the Human Interface Guidelines.** Native-feeling UI, correct safe-area handling, proper iOS conventions read as quality to editors.
- **Adopt new OS features early.** Using the latest iOS capabilities, devices, or APIs is a known signal that improves featuring odds — Apple likes to showcase what's new.
- **A strong, distinctive icon and art.** The same icon that converts also catches an editor's eye.
- **Have a clean, complete, localized listing** ready before launch — and you can pitch Apple via the App Store editorial nomination form ahead of release.

## Where this sits

- **`unity-analytics-liveops`** owns the retention/ARPDAU gate (validate before UA) and the SKAdNetwork/AdAttributionKit conversion-value plumbing this skill depends on.
- **`unity-monetization`** owns ATT (`NSUserTrackingUsageDescription`) and SKAdNetwork (`SKAdNetworkItems`) in the iOS build.
- **`unity-qa-release`** owns App Store submission, metadata fields, age rating, and screenshot sizes — this skill decides *what* those creatives say.
- **`unity-localization`** localizes the in-app experience the localized listing promises.
- **`unity-aaa-graphics`** / **`unity-asset-designer`** produce the icon and screenshot art at the visual quality this discipline requires.

## Field notes & lessons

- **Retention before spend.** The most expensive growth mistake is scaling UA on a game that doesn't retain — soft-launch the retention numbers first; the cheapest growth is a funnel that doesn't leak.
- **The icon and first two screenshots do most of the work.** If you optimize one thing, optimize what a user sees before they scroll or tap — at thumbnail scale.
- **Misleading creatives are a trap.** They win the install report and lose the retention report; measure retained users, not raw installs.
- **Test one variable, reach significance.** Both for Product Page Optimization and ad creatives — a winner called on a day of noise is a coin flip.
- **Don't quote perishable market numbers.** eCPMs, ROAS, and ATT opt-in rates churn and have been widely overstated; keep plans principle-level and measure your own game.
- **Spend the review prompt wisely.** Apple rate-limits it — fire it at a genuine high point, never on first launch or during friction.
- **Localize the listing, not just the app.** A localized keyword field and screenshots open whole markets cheaply; consistency with `unity-localization` keeps the promise.
