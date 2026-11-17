---
name: unity-localization
description: "Internationalize and localize Unity 6 games with com.unity.localization. Use for i18n/l10n, externalizing strings, Localization Settings, locales and selectors, String/Asset Tables, LocalizedString, LocalizeStringEvent, Smart Strings/ICU variables/plurals/gender, CSV/XLIFF workflows, pseudolocalization, CJK/Cyrillic/Arabic/Hebrew/Thai glyph coverage, TMP fallback fonts, tofu, RTL and mirrored layouts, 30-40% text expansion, locale-specific art/audio, number/date/currency formatting, or localized App Store metadata. Pair with unity-ui-designer for flexible layouts/fonts, unity-qa-release for builds, and unity-aso-growth for store listings."
---

# Unity Localization

Make a casual iOS game **shippable in any language** with the Unity Localization package — externalize every user-facing string, swap text/fonts/assets per locale at runtime, and prove it renders (no tofu, no truncation) before a translator ever sees it. This is the i18n/l10n discipline that sits beside `unity-ui-designer`'s font-glyph work; it executes through `unity-mcp-bridge` and feeds `unity-qa-release` / `unity-aso-growth` for the store side.

## Doctrine (these override convenience)

1. **Externalize every user-facing string from day one — one source of truth.** Retrofitting localization onto a finished game is the expensive path: you hunt scattered literals, re-layout every screen, and re-test. Route every visible string through a String Table key from the first screen, even if you ship one language. Hard-coded strings are localization failure points ([SimpleLocalize](https://simplelocalize.io/blog/posts/best-practices-in-software-localization/)); the i18n rule is **externalize all user-facing strings, never concatenate** ([Microsoft Globalization](https://learn.microsoft.com/en-us/globalization/methodology/software-internationalization)). This is the same seam `unity-ui-designer` builds for single-sourcing — Localization is its production-grade form.
2. **Localize display, not logic.** Gameplay rules, save data, asset *keys*, and analytics event names stay code-side in a fixed canonical form (English/ASCII). Only what the player *reads or hears* gets localized. A locale switch must never change game behavior, scoring, or the strings you log to analytics.
3. **Never concatenate translated fragments.** `"You have " + n + " coins"` is grammatically broken in most languages (plural, gender, word order). Use Smart Strings so the *whole sentence* is the translatable unit and grammar lives in the table, not in C#.
4. **A locale is text + font + layout + assets — all four.** Switching to Japanese without a CJK-covering font yields tofu (□); switching to German without text expansion clips buttons; switching to Arabic without RTL mirrors the UI wrong. Plan all four per target locale, not just the text.
5. **Pseudolocalize before you translate.** Catch hardcoded strings, truncation, and layout breaks with a generated pseudo-locale *first* — it's free and instant; native review is slow and costs money. Don't send a build to translators until pseudoloc is clean.

Confirm the Editor is reachable (`mcpforunity://editor/state`, `ready_for_tools==true`) before driving any of this through MCP. Much of Localization is Editor-window-driven; use `execute_code` against `LocalizationEditorSettings` for the scriptable parts (see `references/localization-workflow.md`).

## Package & settings setup

- **Install `com.unity.localization`** via Package Manager (Window ▸ Package Manager ▸ add by name `com.unity.localization`) or add it to `Packages/manifest.json` and let resolution run. A package add drops the MCP bridge for ~5s on domain reload — reconnect by focusing the Editor (see `unity-mcp-bridge`).
- **Create Localization Settings** (Project Settings ▸ Localization ▸ *Create*). This makes the `LocalizationSettings` asset that holds available locales, startup selectors, and the string/asset database. Add it to Preloaded Assets so it loads on iOS.
- **Add Locales** with the Locale Generator (Window ▸ Asset Management ▸ Localization Tables, or via `LocalizationEditorSettings.AddLocale`). Pick real target markets (e.g. en, ja, ko, zh-Hans, de, fr, es, pt-BR, ar) — don't add locales you can't actually translate/QA.

## Locale selection — persist the choice, default to system

Configure **Startup Locale Selectors** (ordered, first match wins) on the Localization Settings:

1. **`PlayerPrefLocaleSelector`** first — restores the player's explicit choice across launches (persists the selected locale to PlayerPrefs).
2. **`SystemLocaleSelector`** next — defaults a first-run player to their device language (`Application.systemLanguage` / culture). A casual player should see their own language on launch with zero taps.
3. **`SpecificLocaleSelector`** last — a guaranteed fallback (your source locale) so the game never starts with no locale.

At runtime, change language with `LocalizationSettings.SelectedLocale = locale;` (the PlayerPref selector writes it through automatically). Wait on `LocalizationSettings.InitializationOperation` before reading any localized value at boot. Expose a language picker in Settings (cross-ref `unity-ui-designer`).

## String Tables & Asset Tables — reference by key, never by literal

- **String Table Collections** hold the translatable text. **Organize keys by screen/feature** (e.g. tables `Menu`, `HUD`, `Shop`, `Results`) so a screen loads one table and translators get context. Each entry has a stable **Key** (e.g. `menu.play`) and one value per locale.
- **Asset Table Collections** hold locale-specific *assets* — a localized title image, a voiceover clip, a culturally-swapped icon. Most art is locale-neutral; only localize an asset when it contains baked text or is culturally specific.
- **Reference by key, never by literal.** In UI, drive a `TMP_Text` with a `LocalizeStringEvent` (or bind a `LocalizedString` in code) pointing at `Table/Key`; drive images/audio with `LocalizeSpriteEvent` / `LocalizeAudioClipEvent` / `LocalizedAsset<T>`. No screen ever holds the display literal — it holds the key.
- **Keep keys semantic and code-side.** Keys are identifiers, not English text; renaming the English copy must not change the key. (This is why keys are "logic," covered by Doctrine #2 — never localize them.)

## Smart Strings — grammar in the table, not the code

Enable **Smart** on an entry to use SmartFormat (ICU-style) so translated sentences stay grammatical:

- **Variables:** `Welcome back, {playerName}!` — the translator moves `{playerName}` wherever the language needs it.
- **Plurals:** `{count:plural:one #|other #} coins` — each locale supplies its own plural categories (e.g. Russian has more than two). Never build "1 coin / 2 coins" with an `if`.
- **Gender / conditional / choose:** `{gender:select:male=He|female=She|other=They} won` and `{score:choose(0|1):No points|One point|{} points}` keep agreement and special cases in the table.

Feed runtime values via a `LocalizedString` with persistent/local variables (e.g. `IntVariable`, `StringVariable`, an object reference). The sentence is one translatable unit; C# only supplies the data.

## Fonts per script — no tofu (coordinate with unity-ui-designer)

Each locale needs a font that **covers its script**. The default TMP font (LiberationSans) has no CJK/Arabic/Thai glyphs → **tofu (□)**. This is the same discipline as `unity-ui-designer`'s "decide glyph coverage up front" — Localization just makes it per-locale:

- **Pick script-covering fonts** (e.g. OFL-licensed Noto families: Noto Sans CJK, Noto Sans Arabic, Noto Sans Thai). Verify coverage before committing — a font that can't render the script just yields tofu.
- **Swap font by locale.** Either (a) a `LocalizedAsset<TMP_FontAsset>` / Asset Table entry that swaps the font per locale, or (b) one primary TMP font with a **fallback chain** (Latin → CJK → Arabic → Symbols) so TMP walks the list until a glyph matches. Build CJK assets as **dynamic-atlas** `TMP_FontAsset` (cap atlas 2048² for mobile) and pre-warm with `TryAddCharacters()` on a loading screen to avoid runtime atlas hitches. (Full SDF settings live in `unity-ui-designer`.)
- **RTL (Arabic / Hebrew):** Unity Localization does **not** auto-shape or auto-mirror. You need (1) RTL text shaping — TMP's RTL support or a shaping library (e.g. RTLTMPro) so Arabic letters connect and run right-to-left, and (2) **mirrored layout** — flip horizontal anchors/alignment, reverse rows, move back-buttons to the right. Treat RTL as its own layout pass, not a font swap.
- **No-tofu check.** After wiring each locale, screenshot a screen in that locale and confirm real glyphs, not boxes (see Verify).

## Text expansion & layout — design for ±40%

Translations are rarely the same length: German/Russian/Finnish often run **~30-40% longer** than English; CJK can be much shorter. Fixed-width buttons sized to English break everywhere else.

- **Auto-size + wrapping.** TMP Auto Size within a sane min/max; allow wrapping; avoid single-line fixed-width labels for sentences.
- **Flexible layouts.** Let containers grow (UI Toolkit flexbox / uGUI Layout Groups + Content Size Fitter) rather than absolute positions — same responsive doctrine as `unity-ui-designer`.
- **Re-test safe area per locale.** A longer string can push content under the notch or home indicator. Re-run the safe-area check (cross-ref `unity-ui-designer`) in your longest locale, not just English.

## Pseudolocalization — catch breaks before translators

Add a **Pseudo-Locale** (Locale settings ▸ add Pseudo-Locale) and play in it before any real translation:

- **Expander** (pad text ~+40%) → reveals truncation and overflow that real expansion would cause.
- **Accenter** (replace chars with accented look-alikes) → any plain-ASCII text still on screen is a **hardcoded string** that bypassed the tables — fix it.
- **Mirror / RTL pseudo** → smoke-tests mirrored layout before Arabic.

Pseudoloc is the cheap, deterministic gate. Ship a pseudoloc-clean build to translators, never a raw one.

## What to localize (and what not to)

- **Localize:** all UI text; store metadata (title, subtitle, description, keywords, screenshots — see below); locale-specific art/audio *only when* it carries baked text or is culturally specific; and **number / date / currency formatting** (use culture-aware formatting / Smart Strings, not `ToString()` with assumptions — `1,000.50` vs `1.000,50`, date order, currency symbol/placement).
- **Do NOT localize:** gameplay logic, difficulty constants, save keys, **asset keys / table keys**, PlayerPrefs keys, and **analytics event names / parameters** (cross-ref `unity-analytics-liveops` — events must be one canonical form across all locales or your funnels split). Localizing any of these is a bug, not a feature.

## Localized App Store metadata

The store listing is part of localization, not an afterthought. Localize per App Store locale: app name/subtitle, description, **keywords** (translate *and* re-research per market — direct translation misses local search terms; cross-ref `unity-aso-growth`), screenshots (with localized captions/overlays), and the preview. Wire the build + metadata submission through `unity-qa-release` (App Store Connect, per-locale metadata fields). A game that's localized in-app but has an English-only store page leaks installs in every non-English market.

## Workflow (summary — full steps in references)

1. **Extract** — sweep code/scenes for user-facing literals; replace each with a String Table key (`LocalizeStringEvent` / `LocalizedString`).
2. **Author String Tables** — organize by screen, mark Smart where grammar needs it.
3. **Export** — CSV (Google Sheets round-trip) or **XLIFF** (standard CAT-tool format) for translators.
4. **Translate** — externally; translators touch the export, never code.
5. **Import** — bring CSV/XLIFF back into the tables.
6. **QA** — pseudoloc pass (truncation/hardcoded/layout) → no-tofu screenshots per locale → native speaker review.

Concrete commands, the `LocalizationEditorSettings` `execute_code` snippets, Smart String examples, CSV/XLIFF export-import, font-fallback setup, and pseudoloc enablement are in `references/localization-workflow.md`.

## Verify (a locale is done only with evidence)

- Switch to the locale at runtime and screenshot the key screens (menu/HUD/results/settings) at phone resolution — **real glyphs, no tofu**.
- Longest locale (e.g. de/ru) shows no truncation/overflow and stays inside the safe area.
- RTL locale (if shipped) reads right-to-left, letters shaped/connected, layout mirrored.
- Pseudoloc pass is clean — no plain-ASCII strings leaked (no hardcoded text).
- Numbers/dates/currency render in the locale's format.
- Locale choice persists across a relaunch; first run defaults to device language.

## Where this sits

- **`unity-ui-designer`** — owns TMP/SDF font assets, the single-source-of-truth string seam this skill industrializes, and the layout/safe-area/auto-size that text expansion stresses. Localization swaps the *content*; UI designer owns the *container*.
- **`unity-image-generator`** — produces script-covering font references and any locale-specific art (localized title/logo); the no-tofu glyph-coverage concern originates there.
- **`unity-qa-release`** — runs the localized build and submits per-locale App Store metadata; the per-locale screenshot/no-tofu checks join its release gates.
- **`unity-aso-growth`** — localizes the store *listing* (keywords re-researched per market, localized screenshots) on top of the metadata fields.
- **`unity-analytics-liveops`** — consumes the canonical, NON-localized analytics event names this skill protects.
- Executes through **`unity-mcp-bridge`**; sits under **`unity-game-director`** as the i18n phase.

## Field notes & lessons

- **Retrofit is the tax — pay it on day one.** The single biggest lesson: a key per string from the first screen costs minutes; converting a finished game costs a re-layout of every screen plus a literal hunt. Build the seam even for a one-language launch.
- **Tofu is a font problem, not a text problem.** Correct translations still render as □ boxes without a script-covering font + fallback chain. Always screenshot each new locale to confirm glyphs — "the table has Japanese" proves nothing about what renders.
- **Concatenation is the quiet bug.** `n + " coins"` passes English QA and breaks silently in every plural/gender language. Move the whole sentence into a Smart String; let the table own grammar.
- **Pseudoloc finds what code review misses.** The Accenter instantly surfaces hardcoded strings that slipped past the tables; the Expander surfaces truncation before a German speaker ever files it. It's the highest-ROI, lowest-cost step — do it before translation, not after.
- **Don't localize identifiers.** Localizing an asset key, save key, or analytics event name silently corrupts loading/saving/funnels. The line is strict: if the player reads or hears it, localize it; otherwise it's logic — leave it canonical.
- **RTL is a layout pass, not a checkbox.** Arabic needs text shaping *and* a mirrored UI; Unity Localization does neither automatically. Budget it as real work or don't claim RTL support.
- **The store page is part of the game's localization.** In-app localized but store-page English-only is a common miss that throttles installs in exactly the markets you localized for — hand off to `unity-aso-growth` / `unity-qa-release`.
