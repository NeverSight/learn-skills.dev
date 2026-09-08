---
name: social-publisher
description: "Use when planning a posting schedule, building a multi-platform content calendar, or reshaping one source asset into channel-native posts across X, LinkedIn, Instagram, Threads, Bluesky, TikTok, Facebook or YouTube — cadence, best-time slots, per-platform format limits, API publish caps, and a dated CSV or JSON calendar a scheduler can import. NOT the brand voice the posts speak in (that is `brand-voice`), NOT the editorial strategy of what to make (that is `content-engine`)."
tags: [social-media, scheduling, repurposing, content-calendar, distribution]
recommends: [content-engine, brand-voice, video-shorts, newsletter, calendar-scheduling]
origin: risco
---

# Social Publisher — The Operator's Desk for Distribution

*Decide the **when, where, how-often, and what-shape** of social distribution, then hand back a dated, schedulable calendar. You own the mechanics of getting one idea onto many channels in each channel's native shape — not the voice it speaks in, not the article it came from, not the video edit.*

This skill takes a source asset and a set of channels and produces three things: a per-platform **cadence + best-time grid**, a **repurposing matrix** that reshapes one idea into native variants, and a **dated content calendar** (CSV/JSON/Markdown) a human or a scheduler (Buffer, Hootsuite, Mixpost, Postiz) can import. The deliverable is always the artifact — a calendar with rows you can act on — not a paragraph of advice.

## When to use / When NOT

Use when:

- Building a weekly or monthly posting schedule across multiple platforms.
- Deciding posting frequency and best-time slots per platform.
- Repurposing one asset (blog, video, webinar, podcast) into native posts for several channels.
- Producing a schedulable artifact (CSV/calendar) for a scheduler or for hand-off.
- Checking per-platform limits before programmatic publishing (char caps, media specs, API publish/rate limits, approval gates).

Do NOT use when (route to the sibling that owns it):

| You actually want | Go to |
| --- | --- |
| The brand's tone-of-voice / verbal identity the posts must sound like | `../brand-voice/SKILL.md` |
| To write the long-form source article the posts are sliced from | `../article-writing/SKILL.md` |
| The editorial strategy of *what topics* to make this quarter | `../content-engine/SKILL.md` |
| To script/edit the Reel or Short (hook, cuts, captions burn-in) | `../video-shorts/SKILL.md` |
| To reply to comments/DMs, moderate, grow the community | `../community/SKILL.md` |
| To respond to and manage ratings/reviews | `../review-management/SKILL.md` |
| To write/send the email newsletter issue itself | `../newsletter/SKILL.md` |
| Keyword/topic research, getting cited by AI engines | `../seo-geo/SKILL.md` |
| Paid social ads / boosted promotion | `../ads/SKILL.md` |
| To generate the images/graphics in the posts | `../ai-media/SKILL.md` |

If a brand voice spec exists, shape every post *in* it — load `../brand-voice/SKILL.md`. This skill schedules and reshapes; it does not invent the voice.

## The distribution mental model

Four rules. Internalize them before you touch a calendar.

1. **One source asset → N native variants, never N copies.** Reshape language, length, hashtags, and format per channel — repurposing is reformatting, not copy-paste. One blog or long video commonly yields 7–10 short clips plus carousels and threads. Source: Buffer "Ultimate Guide to Repurposing Content"; Planable 2026 repurposing guide (accessed 2026-06-02).

2. **Aim for roughly one native-original post per two repurposed.** Repurposed content reportedly drives ~25–35% more engagement than one-off posts, but an all-repurposed feed reads stale — keep a ~1:2 native:repurposed mix so the account still feels alive. Source: InfluenceFlow / Planable 2026 (accessed 2026-06-02).

3. **Consistency beats raw frequency, and gaps are expensive.** A steady schedule outperforms bursts; a ~2-week gap after heavy posting can cut reach 30–50%. Plan a cadence you can actually sustain. Source: Sprout Social / Buffer / Metricool 2026 (accessed 2026-06-02).

4. **The deliverable is a schedulable artifact.** Always end at a dated calendar (rows: date, time, platform, format, body, status) — something a scheduler imports or a person executes. Advice without a calendar is a miss. The schema lives in `references/calendar-schema.md`; `scripts/verify.sh` lints what you emit.

## Cadence & best-time grid

Per-platform 2026 frequency sweet spots and starting best-time slots. Source: Sprout Social / Buffer / Metricool best-time-to-post 2026 (accessed 2026-06-02).

| Platform | Frequency (2026) | Best-time starting hypothesis |
| --- | --- | --- |
| Instagram (feed) | 3–5x/week | Tue–Wed 11am–1pm |
| Instagram Stories | 1–2x/day | spread across the day |
| Reels | 3–4x/week | best day Tuesday |
| LinkedIn | 3–5x/week | Tue–Thu 11am–5pm (shifting later, outside office hours) |
| X (Twitter) | 3–5x/day | ~9pm and Tue–Wed |
| TikTok | 1–3x/day | test per account; volume tolerant |
| Facebook | 3–5x/week | weekday mid-morning |

**Caveat, not law:** these slots are starting hypotheses. The only authoritative times are in the account's own analytics — schedule to the table, then move slots toward where *that* audience actually engages. Never present these numbers as guarantees.

## Repurposing matrix

Map source type to per-channel native output. Each cell is a *shape*, not the same text.

| Source | X | LinkedIn | Instagram | Reel/Short/TikTok | Bluesky | Facebook |
| --- | --- | --- | --- | --- | --- | --- |
| Blog post | thread of the key claims | narrative post + takeaway | carousel of the steps | talking-head of the hook | short thread | summary + link in first comment |
| Long video | clip + quote | lesson write-up | carousel of frames | 3–5 vertical cuts | quote post | native upload of one cut |
| Webinar | live-thread highlights | recap + slides | quote-card carousel | best-moment clips | takeaway post | replay link |
| Podcast | quote thread | episode notes | audiogram carousel | audiogram Shorts | quote post | episode card |

Reshape the *same idea*, not the same string. Bad→Good:

```text
Bad  (same caption pasted to all four — flat, off-shape, link breaks IG):
  "New blog: 5 ways to cut cloud cost. Read here https://ex.co/cloud #cloud #devops"

Good (native per channel):
  X       thread → "5 ways we cut our cloud bill 38% in a quarter. 🧵"
                   one tactic per post, link only in the last post.
  LinkedIn → "We cut our cloud bill 38% last quarter. The boring one
              that mattered most: rightsizing before reserving. Here's
              the order we did it in →" (3–5 short paras, no hashtag wall)
  Instagram → 6-slide carousel, one tactic per slide; link in bio;
              caption is the hook + 3–5 specific hashtags.
  Bluesky → short thread, plain link (no UTM-bloat), 1 tag max.
```

## Channel-native shaping rules

Quick reference; full specs and API reality in `references/platform-limits.md`.

| Platform | Char cap | Hashtags | Links | Native trick |
| --- | --- | --- | --- | --- |
| X | 280 (post) | 1–2 | inline, costs reach less than before | thread the long idea; hook in post 1 |
| LinkedIn | ~3,000 | 0–3 | first comment, not body | "see more" cutoff ~210 chars — front-load the hook |
| Instagram | 2,200 caption | 3–5 specific | bio / link sticker | first-comment for tags; carousel for depth |
| Threads | 500 | light | inline ok | conversational, low-hashtag |
| Bluesky | 300 | 1 max | plain inline | short threads; no algorithmic hashtag game |
| TikTok | 2,200 caption | 3–5 | bio | hook in first 1–2s; caption supports, video carries |
| Facebook | ~63k (keep short) | 0–2 | first comment if reach-sensitive | native video > shared link |

Rule with a why: **put links in the first comment on LinkedIn/IG/FB** — link-in-body posts are commonly down-ranked, so keep the body clean and drop the URL below. **Front-load the hook** everywhere — LinkedIn truncates at ~210 chars and X shows post 1 only, so the first line decides the click.

## The content calendar artifact

Every run ends here. Minimum columns:

`date · time · timezone · platform · format · source_asset_id · hook · body · media_ref · link · hashtags · status`

`status` lifecycle: `draft → scheduled → posted`. `source_asset_id` ties all rows derived from one source (the repurposing link), so you can see at a glance that one blog became six native posts.

Markdown example (one source asset, two channels):

```text
| date       | time  | tz        | platform | format   | source_asset_id | hook                         | status    |
| 2026-06-09 | 11:30 | Europe/Madrid | linkedin | post     | blog-cloud-001  | We cut our cloud bill 38%…   | scheduled |
| 2026-06-09 | 21:00 | Europe/Madrid | x        | thread   | blog-cloud-001  | 5 ways we cut cloud cost 🧵   | scheduled |
```

JSON row (what a scheduler ingests):

```json
{
  "date": "2026-06-09",
  "time": "21:00",
  "timezone": "Europe/Madrid",
  "platform": "x",
  "format": "thread",
  "source_asset_id": "blog-cloud-001",
  "hook": "5 ways we cut cloud cost 🧵",
  "body": "5 ways we cut our cloud bill 38% in a quarter…",
  "media_ref": null,
  "link": "https://ex.co/cloud",
  "hashtags": ["#cloud"],
  "status": "scheduled"
}
```

Full column definitions, the CSV variant, and import notes for Buffer/Hootsuite/Mixpost/Postiz are in `references/calendar-schema.md`. After you write a calendar file, run `scripts/verify.sh path/to/calendar.{csv,json}` to catch over-cap bodies, byte-identical cross-posts, bad status values, and non-future scheduled datetimes.

## Platform limits & API reality

Before promising programmatic publishing, check the 2026 gotchas — they change what is even possible. Full sourced table in `references/platform-limits.md`.

- **Instagram Graph API:** ~25–50 API-published posts per *rolling* 24h per account (sources vary 25/50/100 by account trust); ~200 API requests/hour. The window is rolling, not calendar-day. (Meta IG Platform "Content Publishing Limit"; InstantDM 2026 — accessed 2026-06-02.)
- **X API:** as of Feb 2026, legacy Free tier is write-restricted (~500 posts/month, no new signups) and **pay-per-use is now default for new developers** (~$0.01/post; URL posts cost more). Programmatic X posting costs money for new apps. (Zernio / Postproxy / Blotato 2026 — accessed 2026-06-02.)
- **LinkedIn API:** free OAuth = Sign-In + basic profile only; posting (UGC/Share) runs ~100 calls/day/member and Marketing/advanced access starts **~$699+/mo** for approved partners. Plan around the gate. (Phyllo / SociaVault 2026 — accessed 2026-06-02.)
- **Bluesky AT Protocol:** moved to OAuth (announced 2024-09-25; App Passwords deprecated for new projects; first granular scope `transition:email` shipped 2025-06-12); API is free with a ~5,000-points/hour cap. (Bluesky/AT Protocol docs — accessed 2026-06-02.)
- **TikTok Content Posting API:** requires a separate audit and forces `SELF_ONLY` (private) posts until approved. (Blotato / PostPeer 2026 — accessed 2026-06-02.)

**Execution-layer decision:** this skill produces the plan; something else publishes it.

- Manual / few channels → a hosted scheduler (Buffer, Hootsuite) — import the CSV.
- Self-host, own your data → **Mixpost** (Laravel, one-time license, drag-drop calendar, first-comment + dynamic variables) or **Postiz** (Apache-2.0, free, 15+ platforms).
- Programmatic across many platforms → a unified API (Blotato-style) to dodge per-platform auth pain.

(Mixpost.app; Postiz "Open Source Social Media Scheduler" / GitHub inovector/mixpost — accessed 2026-06-02.)

## Anti-patterns

| Anti-pattern | Why it fails | Do instead |
| --- | --- | --- |
| Same caption pasted to every platform | Off-shape, link penalties, reads as spam; this is the #1 reason cross-posts flop | Reshape per channel via the repurposing matrix |
| Chasing "best time" tables while ignoring own analytics | Generic slots are hypotheses; the audience's real peak is in *their* data | Seed from the grid, then move slots toward the account's analytics |
| A 2-week burst, then going dark | Gaps can cut reach 30–50% and break the algorithm's trust | Pick a sustainable cadence and hold it |
| Ignoring per-platform publish caps | IG ~25–50/rolling-24h and member-level LinkedIn limits get you throttled mid-launch | Check `references/platform-limits.md` before scheduling volume |
| Treating Reels/Shorts/TikTok as "post the same vertical clip" | Each has different specs, hook windows, and caption rules | Cut per-platform; respect each spec |
| Defining brand voice or picking topics here | Out of scope — produces inconsistent voice and a calendar with no strategy behind it | Route to `../brand-voice/SKILL.md` and `../content-engine/SKILL.md` |
| Ending at advice with no calendar | The deliverable is a schedulable artifact, not a pep talk | Emit a dated CSV/JSON calendar and verify it |
