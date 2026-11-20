---
name: gta-vi-shorts-editing
description: >-
  Build English GTA VI (GTA 6) news Shorts (30-59s) the Joker Gaming way with this Claude Code skill: ChatGPT scripts from a fact ledger, Kokoro voiceover, exact word-timed subtitles, official stills and trailer motion, designed fact cards, loudness and colour gates, and an independent red-team gate before upload. Use when planning, scripting, editing, checking, or uploading a GTA VI Short.
license: MIT
metadata:
  version: 1.2.0
  date: 2026-11-16
  author: Muhammad Saad Ranjha / Joker Gaming
  compatibility:
    node: "24"
    ffmpeg: "8"
    python: "3.12"
    remotion: "4"
    network: "not needed at render time"
---

# GTA VI Shorts Editing

## What this skill is

The working method behind the Joker Gaming GTA VI news Shorts: short, premium, zero-fake English Shorts built from official Rockstar material only — topic research to scheduled upload: fact ledger, ChatGPT script and SEO, voiceover, subtitles, stills and motion, cards, mix, render, grade, loudness, builder QC, red-team gate, scheduling.

Positioning, stated plainly: this skill is the editorial brain, not a renderer. It teaches the method and the checks that prove a video is ready. It does not render video by itself. Pair it with the Pro Pack Remotion template, or with your own renderer that can hit the same gates (1080x1920, 30fps, yuv420p, tv, bt709 x4, loudness -16 to -14 LUFS, true peak ≤ -1.0 dBTP).

Who it is for: an editor or agent making GTA VI news Shorts who wants a repeatable, checkable method instead of guessing. It assumes ffmpeg, Python, Node with Remotion, Kokoro TTS, and faster-whisper are available (see Install). It contains no Rockstar footage, logo files, trailer files, or music. You supply your own official source material.

**Supported platform:** Ubuntu 24.04 LTS (primary). macOS via Homebrew (see INSTALL.md). Windows only under WSL2 running Ubuntu 24.04. No native Windows route.

## Install and prerequisites

Run `scripts/setup-check.sh` first. Full literal commands live in `INSTALL.md` — this summary is not a substitute.

- **ffmpeg 8.x** (libx264, loudnorm, signalstats) — static build; Ubuntu 24.04 ships ffmpeg 7.x, so the system package is the wrong version.
- **Node 24 + npm 10** (Remotion 4 needs Node 24) — NodeSource or nvm; Ubuntu 24.04 ships Node 18.
- **Python 3.12** — Ubuntu 24.04 system package.
- **Kokoro TTS** (kokoro-onnx 0.6.1) in its own venv; model files from the kokoro-onnx GitHub release `model-files-v1.0`: `kokoro-v1.0.onnx` (~310 MB) and `voices-v1.0.bin` (~27 MB) into `$HOME/.cache/kokoro-onnx/`.
- **faster-whisper 1.2.1** in its own venv; models download on first use (~1.4 GB for tiny/base/small).
- **Remotion 4.0.543** (Pro Pack template or your own project); all `@remotion/*` packages on the same exact version.
- **espeak-ng symlink:** the Kokoro loader demands its baked-in data path symlinked to the venv's espeak-ng-data. Read the path the loader error names and symlink THAT path: `ln -s <venv-path>/lib/python3.12/site-packages/espeakng_loader/espeak-ng-data <loader-path>/espeak-ng-data`, verify with `ls -l <loader-path>` plus a one-sentence test synthesis. The symlink lives outside the workspace: re-apply after any VM replacement.

You need a ChatGPT account for Step 1 (scripts + SEO) and a Gemini account only if you use the Gemini thumbnail route. No password, key, or token is ever asked for or stored by this skill. If `/tmp` is a small tmpfs (512 MB on the build machine), install large packages with `TMPDIR=$HOME/workspace/tmp --no-cache-dir`.

## How rules are labelled

Every rule is proven in a shipped video or marked PROVISIONAL (follow it, do not cite it as proven). M1–M39 are all proven; full text in `references/m-rules-*.md`. The hook score, results log, and validator script are PROVISIONAL.

## Proof

Three Shorts were built with this method on November 15, 2026, on the Joker Gaming channel, and all three were scheduled the same day. View counts were read from the public YouTube pages on 15 November 2026 (evening PKT). No earnings are claimed anywhere in this skill. No subscriber count is claimed anywhere in this skill.

| Short | Published | Views (15 Nov 2026) | Likes |
|---|---|---|---|
| SPOTTED: Jason's GTA 6 Launch Trailer Shirt Names a Base From the 1997 Game - https://youtube.com/shorts/8uBbUEWNCag | 10 Nov 2026 | 1,140 | 7 |
| NEW: How Big Is GTA VI's Map? Rockstar Already Answered It - https://youtube.com/shorts/C4Sr6Emcxiw | 10 Nov 2026 | 1,028 | 9 |
| NEW: GTA VI's Weapon Wheel Is Back — But You Can't Carry Everything - https://youtube.com/shorts/DP4sJFn5ql4 | 10 Nov 2026 | 1,010 | 8 |
Across the 37 most recent Shorts on @jokergaminglive, total public views were 10,013 on the same check. Two more of the top five (874 and 804 views, Nov 12) are listed in `examples/`.

Watch hours are not public on YouTube; they come from YouTube Studio only, so no watch-hours figure is claimed here.

| Video | Slot (PKT, Nov 15) | Duration | Red-team verdict |
|---|---|---|---|
| GTA VI Built a Whole Cartoon Inside the Game - https://youtube.com/shorts/OC5KczRGYSQ | 17:00 | 40.00s | 96/100 + 60/60 PASS, 0 criticals |
| New Zealand Plays GTA VI First. Here's Your Unlock Time - https://youtube.com/shorts/aF6RgIg_mHI | 19:00 | 46.00s | 90/100 + 53/60 PRE-FIX verdict, a FAIL (MAJOR-1 colour). Shipped file is the MAJOR-fixed file, technically re-verified (loudness -15.62 LUFS / -1.87 dBTP, luma shift ≤ 0.1, fixed frame viewed identical), expected approx 94/100, not a measured re-score |
| Burger Shot Is Real Now. You Can Eat It in Florida - https://youtube.com/shorts/74I0MXC-aIQ | 21:00 | 40.99s | 97/100 + 57/60 PASS, per RUN-NOTES.md only; no standalone red-team report file exists for this video |

Refresh rule: every proof count is dated Nov 15, 2026. Do not overwrite a dated number. If you re-check a count, ADD a new dated row and keep the Nov 15 row beside it. Re-verify time-sensitive facts at build time: the Nov 15 facts are a snapshot, not a live feed. Worked examples with full scripts, SEO, shot plans, scores, and the complete V1 fact ledger (12 rows) and banned list (10 rows) are in `examples/`.

## Non-negotiable gates

Nothing ships unless every gate passes. The owner's watch/listen is final and overrides every gate score.

| Gate | Bar |
|---|---|
| Duration / format | 30–59 seconds, 1080x1920, 30fps, on the delivered file |
| Script | 90–105 words, hand-counted (tokens AND spoken words, both inside 90–105). At the 2.5 words/sec planning pace a 90–105-word script yields ~38–46s of finished video; if a topic needs longer, split the story — never pad holds past the 2.0s static-hold cap |
| Voiceover | Kokoro `am_adam` at speed 1.1, one stem per sentence, -40 dBFS trim, 24 kHz. Fallback if Kokoro fails: Piper `en_US-lessac-medium` (see `references/voice.md`); a different voice re-verifies the pace/word-count math, measured on `am_adam` at 1.1 |
| Loudness (delivered file) | −16 to −14 LUFS, true peak ≤ −1.0 dBTP, measured on the delivered file |
| Red-team gate | Quality ≥ 90/100 AND technical ≥ 48/60 AND zero criticals; a MAJOR blocks release even when the numeric bars are met. The /100 rubric is published below |
| Pool gate (M20) | **STOP** before VO, cards, and mix if the verified clean pool is smaller than need + slack, where slack = ceil(10% of need) |
| Owner watch/listen | Final. A video is not cleared until the owner has watched and listened |
| Zero fake | Every viewer-facing word traces to a fact-ledger row. Leak chatter is a topic signal only, never a fact |
| Audio rights | VO-only, or VO plus royalty-free music. Never a commercial song or original clip audio at any volume |
| M30 date rule | **At scheduling (and any re-schedule), every relative-date word in the script, on every card, in the SEO, and on the thumbnail is re-derived from the ACTUAL air date** (countdown = launch date minus air date; "today/tomorrow/begins today" checked against the air date, not the build date). A mismatch is a fix1 rebuild (VO re-record plus card re-render), never a silent ship and never a parent rewrite of a ChatGPT line. Full rule: `references/m-rules-facts-dates.md` (M30) |

## Word-count convention

Count BOTH tokens and spoken words; both must sit inside 90-105. Never trust ChatGPT's own count: it has been wrong on every trio script's first return. TOKENS: whitespace-separated tokens, excluding a standalone em-dash. SPOKEN: tokens, with each hyphenated or em-dash-joined compound expanded into its spoken parts, "&" spoken as "and" (1 for 1), "Pre-loading" spoken as one word. Whisper STT word counts are a different measurement and are NOT the gate count. Worked count, V1 (verified by tool, Nov 16, 2026): 103 tokens / 105 spoken. Trio: V1 103/105; V2 102/104; V3 103/105. `scripts/validate-build.py` counts both the same way — run it on the script before VO.

## End-to-end workflow

Full step detail lives in `references/workflow.md` — load it when executing a step. This is the compact checklist; a step is done only when its check holds.

- [ ] **Step 0 — Research, ledger, banned list.** ≥3 independent sources (≥1 official). Fact ledger (CONFIRMED / REPORTED / REACTION / CONFIRMED AS UNANNOUNCED / REPORTED - DISPUTED) + banned list. Dedup against `TOPIC-LOG.md`. Trailer spans claimed in `trailer-windows.md`; `RUN-ALLOCATION.md` on multi-video runs. Full V1 ledger (12 rows) + banned list (10 rows) in `examples/v1-macca-friends.md`.
- [ ] **Step 1 — ChatGPT brief, script, SEO, thumbnail brief.** Brief verbatim into a NEW ChatGPT conversation (`references/chatgpt-brief.md`). Script 90–105 words, numbers as WORDS, no product links, attribution varied. SEO pack: title (verbatim, char count), description per M39 (hook ≤120 chars → fact bullets → unknown/caveat → CTA → Sources → exactly 3 hashtags), 12 tags in order, `CATEGORY` line (default Gaming). Thumbnail brief: cover text verbatim, base + backup frames, safe margins. Hook shortlist: 5–12 candidates scored, human pick before rendering. First frame = thumbnail (M16).
- [ ] **Step 2 — Honesty check.** Hand-recount (both counts 90–105); every fact traces to a ledger row; banned list clean; countdown exact; Sources line in canonical format (`Sources: Outlet (Date); …`); validator script run (it does word count, stem-aware banned grep, pool arithmetic — title/tags/description/M30/M26/M34 stay manual).
- [ ] **Step 3 — M20 pool gate (BEFORE any VO).** Need = ceil(spoken words / 2.5 × 30) + gaps + 2f tail; slack = ceil(10% of need). Count ONLY full-res-verified clean frames. Pool < need + slack = STOP. Record in `POOL-GATE-RECORD.md`.
- [ ] **Pre-render plan** written and validated (beat map, timeline draft, asset list, sign-off). Nothing renders until it validates.
- [ ] **Step 4 — VO (Kokoro).** `am_adam`, 1.1, -40 dBFS trim, 24 kHz, one stem per sentence. Bypass mangled words in SPOKEN text only. Voice defaults in `references/voice.md`.
- [ ] **Step 5 — VO check (faster-whisper `small`).** Script spelling exact; timing from STT. `vo_check.json` + `word_timings.json`. Tie-break by fresh Kokoro control synthesis.
- [ ] **Step 6 — VO concat.** Varied gaps (M3); `vo_concat.wav` + `timeline.json`. Pause discipline: cut dead air >~0.5s; gaps 0.15–0.25s; deliberate 0.5–1s beat only before a reveal / after the hook / before the CTA; never at 0:00, never true digital silence.
- [ ] **Step 7 — Stills & motion.** Active-picture windows only (M29: Trailer 2 y=216..1943; Launch Trailer y=120..2039). Per-segment motion `push` / `pull` / `none` (`none` default for motion spans). ~1 shot per sentence; cuts on every information beat (M22); slow background (M24). Visual velocity: ≥1 event/2–3s, first cut ≤1.5s, half the events in the hook. Official trailers/stills only — NOT the buyer's gameplay (no capture section; post-launch addendum).
- [ ] **Step 8 — Cards & captions.** One fact-card strip (3 lines + source chip + caveat chip), distinct layout/palette/focal element per card, M34 qualifier at headline size, read on its frame (M28). Karaoke captions: 2–4 words visible, fixed lower-third, keyword colour only. Remotion route canonical; `.ass` presets are the non-Remotion fallback only (burn in during grade, AFTER LUT, BEFORE clamp; upload `.srt` to Studio). No captions during card windows. Canonical size 68px Anton, bottom 480, max-width 820px centred (130px sides), 2 lines max. Safe zone (Google, YouTube Shorts): top 192, bottom 480, right 108 — nothing below y=1440 or right of x=972 on the 1080×1920 frame, ever, captions AND cards: a card chip row or a long qualifier line that crosses x=972 is the same defect as a caption there (stack the chips; shrink the line until it fits). Loop/re-hook at ~⅔.
- [ ] **Step 9 — Mix.** Mix ladder peaks: VO ~−6 dBFS, music −18 dB, SFX −12 dB, ambience −24/−30 dB; master −14 LUFS, TP ≤ −1 dBTP; sidechain-duck bed under VO (0.33 under VO, 1.0 in gaps, 0.1s fades, peak −1.5 dBFS). Bed: royalty-free (YouTube Audio Library safest; Shorts library only inside the Shorts editor). Never a commercial song (M35). Attribution, if required, goes on the LAST description line.
- [ ] **Step 10 — Render.** Preview-first (first 10s + a still of every card). Full render at **crf 12** (high-quality master — lossy, not lossless): `npx remotion render src/index.ts JokerTemplate out/raw.mp4 --crf=12 --timeout=120000 --concurrency=2 --pixel-format=yuv420p`. One render at a time.
- [ ] **Step 11 — Fix → grade, one loudnorm pass.** `./post-render-fix.sh out/raw.mp4 out/fixed.mp4` (signalstats range gate: `pc→tv` only if values actually span full-range; loudnorm once, I=-15.5). Grade pipeline on the FIXED file only (no range conversion, no loudnorm). Re-measure loudness on the delivered file. "Two-pass" = loudnorm's built-in dual-pass mode (ONE application); re-running loudnorm on a normalised file is forbidden except the documented V3 audio-only retarget when the delivered file measures out of band. ffprobe: yuv420p, tv, bt709 ×4.
- [ ] **Step 12 — Builder QC (M25).** Re-measure everything on the delivered file: duration, loudness, silencedetect 0 hits, cropdetect on EVERY motion span, STT match, card frames, thumbnail full-size ×3 views. Originality check (YouTube Oct 1, 2026 rule): "what did I add?" — captions + crop + music alone FAIL. No graphic violence in thumbnail or first 7s.
- [ ] **Step 13 — Red-team gate.** Independent reviewer; named gates in order: source-deck → timestamp → layout → technical → human/vision. ≥90/100 AND ≥48/60 AND zero criticals; MAJOR blocks release.
- [ ] **Step 14 — Schedule & upload.** M30 re-derived at scheduling; M31 time + eligibility. Title ≤100 chars; description complete; tags 10–14; category per SEO pack; language English; AI disclosure YES; Not made for kids; Unlisted → HD 100% → publish/schedule. 8-field read-back in Studio. Caption file uploaded. CTA line in the final beat (prescribed). No product links, no playlist.
- [ ] **Step 15 — Results log + iteration (PROVISIONAL).** One row per video; uncollected = "not reported", never zero. 48h retention read: early cliff = hook, slow slide = pacing, stair-step = one bad second, end rise = rewatch. One variable per upload; 10-Short baseline; never delete-and-reupload a flop. Thumbnail A/B by default on launch-week videos. Full loop: `references/analytics-iteration.md`.

## Success criteria

A video is done only when ALL of these hold: (1) duration 30–59s, 1080x1920, 30fps, on the delivered file; (2) script 90–105 words by BOTH counts; (3) every viewer-facing word traces to a ledger row; (4) loudness -16 to -14 LUFS, TP ≤ -1.0 dBTP, on the delivered file; (5) colour tags yuv420p, tv, bt709 ×4 by ffprobe; (6) silencedetect 0 hits (or bed present and gaps audible); (7) no caption overlaps a card window; no lone function word on screen; (8) red-team gate passed; (9) owner has watched and listened (M8); (10) 8-field read-back done in Studio; (11) upload log and results log rows written.

## When to use this skill (and when not to)

Use for: "Plan a GTA VI news Short about [topic]." / "Write the ChatGPT brief for a GTA VI Short on [topic]." / "Check this GTA VI Short script / VO / render / upload against the Joker method." / "Edit a GTA VI news Short to the Nov 15 trio standard." / "Build the thumbnail / cards / captions for a GTA VI news Short."

Do NOT trigger for: non-GTA video editing; a GTA VI montage, gameplay-only, or comedy Short with no news peg; general ChatGPT scriptwriting with no fact ledger (the ledger comes first, always); questions about Rockstar's policy in general (read the policy page itself); a topic with no official source and no checkable fact (leak-only topics stop at Step 0 — the ledger cannot be written); a client job needing intake, revision rounds, or delivery paperwork — this skill is a solo-operator method; the Pro Pack states its scope honestly in `pro-pack/contents.md`.

Allowed-tools scoping: this skill needs ffmpeg, Python, Node/Remotion, Kokoro, and faster-whisper, plus a ChatGPT account for Step 1. It never needs account credentials, logins, or uploads by itself: scheduling and uploading are the owner's step in Studio, and the skill never attempts a login, CAPTCHA, or identity verification.

## The M1-M39 rules

Full rule text lives in `references/m-rules-*.md`, grouped by domain, one level deep from this file. M-numbers are stable and never renumbered.

| File | Rules | Domain |
|---|---|---|
| `references/m-rules-facts-dates.md` | M1, M20, M30, M31, M32 | Facts, ledger, dates & pool gate |
| `references/m-rules-script-vo.md` | M3, M5, M7, M11, M18, M26 | Script, voiceover & captions |
| `references/m-rules-visuals-cards.md` | M2, M13, M14, M16, M17, M22, M24, M27, M28, M33, M34 | Visuals, cards & thumbnails |
| `references/m-rules-audio-mix.md` | M4, M35, M38 | Audio, mix & rights |
| `references/m-rules-render-grade.md` | M9, M10, M21, M29, M36 | Render, grade & colour |
| `references/m-rules-qc-redteam.md` | M6, M8, M12, M15, M19, M23, M25 | QC, red-team & the owner gate |
| `references/m-rules-description.md` | M39 | Description format & SEO |

### Owner rules not yet in the M-record (binding, but not M-rules)

- **VO word bypass:** where the AI voice struggles with a word, bypass it in the spoken text. Always check the voiceover.
- **Cut pace:** M22 governs (cut on every information beat). "About 3s or more per shot" is the OWNER ASPIRATION (M24 slow background). The "2.0s static-hold cap" is the v3 recipe cap on STATIC holds: a still with no movement must end by 2.0s, while a still WITH the eased push-in may hold to the 3s aspiration. "V2 about 1.9s stills" is the MEASURED average still hold in V2, not a target. When the information beat demands a cut, M22 wins.
- **Thumbnail level bar:** real GTA VI logo big at top plus short 1–3 word hook plus one strong focal image plus high contrast; Gemini must NOT draw the logo: composite the authentic logo with PIL instead. **Thumbnail text-size rule:** at 150px Anton, max ~18 characters per line inside the 130px side margins (V2's two-line 150px hook is the measured case); at 168px, max ~16 characters per line. Longer hook: shrink to 150px or split to two lines — never cross the safe zone.
- **Always better than last:** every new GTA VI video must be BETTER than the previous one; the stealth-patch v3 is the current bar to beat.
- **Queued items (not yet rules):** hand-count every script; M34 enforced at brief-spec stage; allocation-compliance check at builder QC; M22 tightening (a staged card's final reveal must coincide with the last fact it anchors); every chosen shot window strip-checked cut-free at 0.5s steps; captions are phrases (2–4 words) OR stressed-keyword pops, never one-word-at-a-time through function words; no caption event overlaps any card window; at storyboard each card names its own layout, palette, and focal element (two cards sharing a layout, palette, and focal treatment inside one video fail storyboard; the three shared LAYOUTS, one per card type, are fine); a hold is judged on the frame strip: if three frames a second apart are near-identical, the shot is a still and either moves or ends (≤2.0s).

### Solo-operator adaptation

Three roles — coordinator, builder, red-team — and a solo operator does all three, but the separation still binds: coordinator work is written down FIRST (ledger, banned list, brief, allocation, pool gate) before any building; builder work follows the written plan and measures from the delivered file at every gate (M25); red-team work must be INDEPENDENT (a fresh session with no build context, working only from the delivered file and the rubric — a verdict written by the builder in the build session is not a verdict). Owner watch/listen (M8) is you watching the finished file, start to finish, with sound, before anything is scheduled; for a client, the client is the owner.

## Exact commands

Literal commands live in `references/commands.md` (Kokoro VO, faster-whisper VO check, VO concat, stills/motion cutting, mix silencedetect, loudnorm, the M36 colour-tag fix, delivered-file verification). Load it when you need a literal invocation (Steps 4–11). Only commands labelled verbatim there are verbatim from the build sources; anything labelled template is NOT verbatim history and must be syntax-verified before use.

## Red-team rubric

Release thresholds: quality ≥ 90/100 AND technical ≥ 48/60 AND zero criticals AND the owner's watch/listen. A MAJOR blocks release even when the numeric bars are met.

### Rubrics (summary)

Full area tables and methods: `references/redteam-rubric.md`. Thresholds: quality ≥ 90/100 AND technical ≥ 48/60 AND zero criticals AND the owner's watch/listen; a MAJOR blocks release even when the numeric bars are met.

**/60 areas:** Facts 10, VO 10, Captions 8, Cards 8, Visuals 10, Thumbnail 7, Technical 7. **/100 areas (published v1.2.0, derived from the trio's actual deductions):** Facts & honesty 25, VO & script 15, Captions 10, Cards 15, Visuals & pacing 15, Thumbnail 10, Technical 10. Minors dock from their area on BOTH scores only when the minor class hits that area; wording-precision minors (M34 qualifier drops, M22 static-tail) dock /100 only — which is why V1 kept 60/60 while losing 4 points on /100. V1's minors: hero-backup spent as a beat −2 (Visuals); M34 "ABOUT" dropped −1 (Cards, /100 only); M22 stem 6 no visual change −1 (Visuals, /100 only). V3's minors: card fade-in 0.87s (Cards, /100 only, not fixed); Y-clamp ringing 0.65% (Technical, both scores); stale vo_check.json (VO, fixed before ship).

Severity: **CRITICAL** release-blocking, zero allowed. **MAJOR** fixed before release even if bars are met. **MINOR** docked, no rebuild, recorded with evidence and frame numbers. **Observation** noted, no deduction.

Red-team methods: ffprobe + sha256; ffmpeg loudnorm + silencedetect + blackdetect + RMS profiles; faster-whisper `small` STT with word timestamps plus `base`/`tiny` cross-checks (control synthesis decides disagreements); fresh Kokoro am_adam 1.1 control syntheses + sample-identity comparison; frame grabs viewed full-size (all segments, cards first/mid/last, motion head/mid/tail, thumbnail) + luma measurements of card fade-ins; grep checks for banned words and digits; clip-list cross-check; logo hash verification; SEO verbatim diff.

## Thumbnail method

The method lives in `references/thumbnail-prompts.md` (the 7 God of Prompt prompts summarised, the Joker 9:16 adaptation, the level bar, the logo rule). **Logo source:** the authentic GTA VI gradient logo comes from Rockstar's official downloads hub — `rockstargames.com/VI/downloads`, Artwork & Wallpapers section, with-logo variants (Download All zip) — or by frame-extraction from the official cover-art reveal on Rockstar's channel, cropped to the logo and hash-verified (sha256 starting `18ad6092`, md5 `116fe9fe…`). Rockstar does not redistribute a standalone logo file; do not take the logo from fan sites or leak pages. Verify the hash before compositing, every time.

## Rockstar IP and honesty

- **Official material only.** Build from official Rockstar material only. Zero fake. Leak chatter is a topic signal only, never a fact. No leaked or pre-release footage, no spoiler or isolated cutscene content.
- **Sell the method, not the material.** This skill contains techniques, commands, checklists, hook and retention rules, ffmpeg and workflow steps, caption and pacing rules, and the owner's own original text. It contains no Rockstar footage, trailer files, logo files, game music, screenshots used as assets, or leaked material.
- **Monetisation is tolerated, not licensed.** Rockstar's policy says Take-Two generally does not object to fans using materials for non-commercial uses that do not intentionally spoil the plot. "Non-commercial" means you do not make money through the game footage you post, and you do not use the material as part of a promotion for a product or service. Take-Two can have its material taken down at any time. Monetised GTA gameplay videos are common in practice, but that practice is tolerated, not licensed. Do not write that Rockstar "allows monetised GTA videos". Licensing requests go to copyright@take2games.com.
- **Paid-product grey area (flagged, not resolved):** this skill is itself a paid teaching product whose promotion and proof videos use Rockstar footage — the exact case the policy's "non-commercial" definition arguably excludes. No position is asserted here; if you sell a product built on Rockstar footage, get a legal read. Do not tell buyers the policy covers paid products.
- **In-game TV line:** Rockstar's policy says showing in-game TV shows in isolation will be flagged for removal. V1's topic is an in-game TV show ("Macca & Friends") and survives on the reporting-vs-reposting distinction: it reports on the teaser with commentary, ledger-sourced facts, and short illustrative frames — it does not repost the show in isolation. Never publish a Short that is only in-game TV content with no reporting around it.
- **Disclaimer:** This skill is unofficial and independent. It is not affiliated with, endorsed by, or sponsored by Rockstar Games or Take-Two Interactive.
- **Honesty rules:** never state views, earnings, or subscriber counts as verified facts unless read from the platform; never write testimonials; never claim the method is the only one or the first; label evidence CONFIRMED, REPORT, or RUMOUR as the ledger does; never present an expected score as measured, or a pre-fix verdict as the shipped score. "First GTA VI Shorts skill" is NOT supportable. Defensible statement: no other free, public, English-language GTA 6 NEWS Shorts skill was found (checked Nov 15, 2026). The moat is news accuracy (ledger + M30/M32) + GTA VI rules (M1–M36) + verified proof (37 Shorts, 10,013 views) + the release bar — not GTA-6 specificity alone. A free GTA-6-specific Claude-Code Shorts guide exists (AI Leverage GTA 6 Shorts Kit, Claude Code + ffmpeg + `clipper.py`); do not claim otherwise. New clipping rivals (Nov 2026): Clip-Forge (Nov 13, 53★), maquina-cortes-gta (Nov 12, PT-BR, 35★).

## Known limits / unresolved

- V3 score provenance: 97/100 + 57/60 per RUN-NOTES.md only; no standalone red-team report file for V3.
- V1 working artifacts missing from disk (Remotion project, graded video, STT/VO reports, QC and red-team frames, audio-fix candidates); the V1 verdict stands on the hashes, framemd5s, and measurements recorded in its reports.
- V1 delivered-file sha256 differs between REDTEAM.md and the parent verification because the parent applied a lossless colour-tag remux after red-team; decoded frames verified identical (framemd5 unchanged). Shipped file hash: `b16077837eb8f50dcfe1b177e994a0c28acd6f1cafbe2b7dc2db3dfbc7373114`.
- No literal Nov 15 loudnorm commands, grade filter graph, M36 full re-encode command, Remotion render command, or V1 colour remux command exist in the sources; the five templates in `references/commands.md` are the honest substitute, each labelled "syntax-verify before use".
- Countdowns are date-bound: every countdown in the examples was true only for the Nov 15 air date. Treat countdowns as M30-derived values, never as reusable copy. After launch (Nov 19, 2026) use `references/post-launch.md`.
- The reference matrix used for competitor study is metadata-only: no video was watched in playback, no audio heard, no frames sampled. Do not present it as frame-level craft evidence.
- **Grade A is a security grade, not a quality grade.** The Skills Directory "Grade A" (and the 92/100 figure cited earlier) grades security posture only; 96% of listed skills hold it. Do not cite it as evidence the skill is good. Cite the evals (`evals/`), the worked examples, and the verified proof numbers instead.
- **Scripts are read-only checks.** `scripts/` contains stdlib-only, no-network, no-credential check scripts. That is the honest security statement — do not claim "100% safe".
- **Live surfaces lag this file:** the GitHub repo and the Gumroad listing are updated only on Saad's word; until a push is confirmed, the live repo may serve an older version. See `CHANGELOG.md` for what is live vs local.

## Changelog

- **1.2.0 (2026-11-16):** Round 2. M-rules moved to `references/m-rules-*.md` (6 files, M-numbers stable); SKILL.md slimmed. Canonical pipeline: fix-then-grade, one loudnorm pass, signalstats range gate, crf 12 render flag, 'lossless master' renamed. /100 rubric published. Complete V1 ledger (12 rows) + banned list (10 rows) shipped. Install fixed with literal commands (`INSTALL.md`). Validator + setup-check hardened. Step 11 rewritten; V2/V3 grade contradiction resolved; caption route declared; post-launch variant added; hook shortlist, karaoke captions, visual velocity, mix ladder, loop/re-hook, first-frame thumbnail, music ladder, pause discipline, originality + 7s rules, analytics page, delivery spec, picture lock, `voice.md`, day-plan, `pitfalls.md`, named gates, evals measurement artefacts, template + image fixes. Full changelog: `CHANGELOG.md`.
- **1.1.0 (2026-11-16):** Polish pass (brief + templates + schemas + scripts + evals). No M-rule dropped or renumbered.
- **1.0.0 (2026-11-15):** First public version.

## References index

Load a reference file only when its trigger fires. The body states the workflow and the gates; the detail lives here.

| File | When to load |
|---|---|
| `INSTALL.md` | First install on a fresh machine; literal ffmpeg / Node / Kokoro commands |
| `CHANGELOG.md` | What changed per version; what is live vs local |
| `references/m-rules-facts-dates.md` | Steps 0, 3, 14: ledger, pool gate, M30/M31/M32 |
| `references/m-rules-script-vo.md` | Steps 1, 2, 4, 5: script, VO, captions rules |
| `references/m-rules-visuals-cards.md` | Steps 7, 8, 12: visuals, cards, thumbnails |
| `references/m-rules-audio-mix.md` | Step 9: mix, bed, audio rights |
| `references/m-rules-render-grade.md` | Steps 10, 11: render, grade, colour |
| `references/m-rules-qc-redteam.md` | Steps 12, 13: QC, red-team, owner gate |
| `references/m-rules-description.md` | Steps 1, 14: description format (M39) |
| `references/chatgpt-brief.md` | Step 1: the verbatim brief, or the fill-in template for a new topic |
| `references/sourcing-guide.md` | Steps 0, 7, 9: where material comes from, what "official" means, bed alternatives, logo source |
| `references/appendix-templates.md` | Steps 0, 3: fact-ledger, banned-list, POOL-GATE-RECORD schemas, plus trailer-windows / RUN-ALLOCATION / build-report / QC-report schemas |
| `references/workflow.md` | Executing any step: full step detail |
| `references/pre-render-plan.md` | Before Step 4: the plan-validate-execute artifact |
| `references/commands.md` | Steps 4-11: literal commands and code fragments |
| `references/tools.md` | Install, Steps 4, 5, 10: versions, paths, gotchas |
| `references/thumbnail-prompts.md` | Step 1, Step 12, Step 14: thumbnail prompts, level bar, logo rule |
| `references/redteam-rubric.md` | Step 13: full /60 and /100 area tables, methods |
| `references/troubleshooting.md` | When something fails; FAQ |
| `references/post-launch.md` | Air date on or after Nov 19, 2026: post-launch beat, card, and tags |
| `references/analytics-iteration.md` | Step 15: retention reading, 48h ritual, one-variable iteration |
| `references/delivery-spec.md` | Delivery: export spec, ingest checklist, picture lock, version naming |
| `references/voice.md` | Step 4: channel voice defaults, first-run profile |
| `references/day-plan.md` | Launch window: what to do tonight, counted ready assets |
| `references/pitfalls.md` | Dated pitfalls; what failed before and how to avoid it |
| `scripts/setup-check.sh` | Before starting: install and prerequisites check |
| `scripts/validate-build.py` | Steps 2, 3, 8: word-count gate, banned-list grep, pool arithmetic, caption/card overlap |
| `evals/README.md` | When the skill changes, or to check an agent using it |
