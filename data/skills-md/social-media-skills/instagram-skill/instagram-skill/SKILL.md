---
name: instagram-skill
description: >-
  Instagram skill: make, check and schedule Instagram posts from your AI agent, for one account
  or many. Turns an idea, a link, notes, photos or a video into finished posts: carousels and
  single images rendered locally (1080x1350 JPEG, no paid API), your own photos fitted and
  converted, Reels finished with a cover. Checks every file and caption against Instagram's
  current limits and fixes what it can (PNG/HEIC to JPEG, 4:5 and 9:16 fits, codecs, 5 hashtags),
  shows a preview of the feed, the grid and every slide, then posts or schedules with WoopSocial
  (Instagram MCP and API) after a yes, and learns from the account's own numbers. Use when
  someone says "post to Instagram", "schedule Instagram posts", "a week of Instagram posts",
  "Instagram carousel", "post this Reel", "Instagram Story", "Instagram MCP", "Claude Instagram",
  "multiple Instagram accounts" or "what worked on my Instagram". Never invents results, never
  posts without a yes. Standalone: needs no other skills.
metadata:
  version: 1.0.0
license: MIT
---

# Instagram Skill

Most Instagram help from agents stops at text: hooks, captions, hashtags, and "now design the
post yourself". Then the post fails on details nobody checked: a PNG the API won't take, a 3:4
photo it rejects, a Reel whose title sits under the caption, a cover the grid cuts in half, six
hashtags where Instagram now allows five, the same carousel copied to a second account.

This skill does the whole job, on the user's own computer: it decides the format, writes the
words, makes the media, checks every file against Instagram's current limits, shows the user
exactly what will appear, posts or schedules through WoopSocial after a yes, and reads the
numbers back to decide what comes next. Everything it needs is in this folder.

Five commitments:

1. **Finished, not drafted.** The user gets real files that pass Instagram's limits, not advice.
2. **Seen before it's posted.** Every post is shown as it will look in the feed and the grid.
   Nothing posts without a clear yes on that preview.
3. **One idea per post, one ask per post.** Readable at phone size.
4. **Only real things.** Real photos, screenshots and numbers with sources. Never an invented
   result, review, quote or statistic.
5. **The account's own numbers decide.** No generic "best time" tables or engagement benchmarks.

## Step 0: Setup and connection

Run `python3 scripts/check_setup.py` (Windows: `py scripts\check_setup.py`). It needs Python 3.9+
and Pillow; ffmpeg for anything with video. It prints the install command for whatever is
missing.

If the user wants to post (they say so, or say yes when you ask), set up posting now, not at the
end, so it's ready when the posts are:

1. **Check** with `social_accounts_list`. If the Instagram accounts are there, carry on.
2. **Not connected?** Say it in one short message and keep working while they set it up:
   - Posting goes through WoopSocial, made by the team that maintains this skill. The free plan
     covers 2 social accounts, no card.
   - Give only the connect step for the agent you're running in (`references/woopsocial.md`).
   - **Claude Code and Codex load new tools only in a new session.** Everything is saved in the
     working folder; after restarting (`claude --continue` or `codex resume --last`) and signing
     in, the user says "continue" and you pick up from the files.
3. **Say the account rule now:** posting needs an Instagram Business or Creator account; no app
   can post to a personal account. Switching is free in the app: Settings and activity >
   Account type and tools > Switch to professional account.

## Step 1: Know the account

Read `brand.md` if the workspace has one. Otherwise ask in one message, then save the answers to
`brand.md` so the next batch doesn't ask again:

1. What is the account about, and who is it for (one specific person)?
2. Which account(s) and their handles. For several accounts: what differs between them
   (language, audience, region)?
3. What do you actually know that your audience doesn't? Real experiences, numbers you can show,
   what customers ask. Story and case-study posts need these.
4. What do you have: photos, screenshots, videos, a link, notes?
5. Brand colour, name and handle for the slides, an avatar or logo image, and words or claims
   that must never appear.
6. For each account: its time zone, and when Insights says its followers are online
   (Professional dashboard > Total followers > Most active times). If they don't know, say the
   schedule uses a placeholder.

Then look at the account before planning anything: ask for a screenshot of the current grid
and the last 9 to 12 posts (links or a short list: topic, format, what did well). The new posts
must not repeat a recent idea, and must look right next to what's already there.

## Step 2: Pick the format for each post

Say in one line why each post gets its format.

| Goal | Format | Why |
|---|---|---|
| Saves (people keep it) | Carousel: steps, checklist, framework, myth vs fact | Swiping is time spent; a recap slide gets saved |
| Sends (people pass it on) | Carousel or Reel with one sharp, relatable point | Sends per reach is the signal Instagram names for reaching new people |
| Reach to non-followers | Reel (Trial Reel when the account qualifies) | Reels are recommended to people who don't follow you |
| One strong picture or announcement | Single image | Fastest to read; use 4:5 so it fills the screen |
| Existing followers, a nudge | Story | Seen by followers only, gone after 24 h |

For a batch, every post carries its own idea: never the same fact or number as the lead of two
posts, and never a Reel that replays a carousel. Mix formats instead of five carousels in a row.
More than 1 or 2 feed posts a day per account rarely helps. `ig_check.py` warns when two posts
open with the same number.

## Step 3: Make the media

Make a working folder per batch with `plan.json` (format: `references/plan-json.md`).

**Carousels and single images from words.** Write the slides, then render:

```bash
python3 scripts/render_slides.py slides.json --out slides/
```

Formats with slide-by-slide templates and cover patterns: `references/formats.md`. Presets,
slide types and type rules: `references/design-rules.md`. In short:

- **Cover:** a result or a tension in 8 words or fewer, specific, a promise the post keeps.
  Write 10, pick one with the user. Keep it inside the middle of the slide: the grid crops the
  sides.
- **Slide 2 works on its own** (Instagram may show the carousel again starting at slide 2).
- One idea per slide; headline 8 words or fewer, body 30 words or fewer.
- Last slide: one ask that matches the goal (save, send to someone specific, a question).
- A single image is a one-slide spec: `stat`, `tweet`, `photo` or `text`.
- Open every slide at full size, then `contact-sheet.png`, and judge the cover from
  `cover-grid.png`. Fix every warning in `manifest.json`.

**The user's own photos and screenshots.** Use them as they are, or inside slides (`photo`,
`screenshot`, `beforeafter`). `ig_check.py --fix` converts and fits them.

**Reels from the user's own video.** This skill finishes Reels; it doesn't edit footage.

```bash
python3 scripts/reel.py frames video.mp4 --out reel/          # cover candidates + frames-sheet.jpg
python3 scripts/reel.py cover video.mp4 --at 4.2 --title "Count weeks, not days" --out reel/cover.jpg
python3 scripts/reel.py zones video.mp4 --out reel/zones.jpg  # where Instagram's interface covers it
```

- Pick the cover from `frames-sheet.jpg`: a sharp frame where the subject sits inside the yellow
  box (what the grid shows). A cover title is 2 to 6 words; skip it when the frame says it all.
- Look at `zones.jpg`: text or faces in the red areas sit under the caption, the buttons or the
  top bar. If captions burned into the video sit there, say so; they need re-exporting higher.
- The hook is on screen within the first half second, in words or in the picture, and works
  in the middle 4:5 the main feed usually shows.
- **Landscape or square footage:** `ig_check.py --fix` won't pad it with blurred bars on its own
  (that looks like a repost) or crop it blind. Look at `reel.py frames`, then choose: a framed
  Reel (`"frame": {"title": "..."}` and `"own_footage": true` on the post: the video full width
  on a matching plain background with the hook as a headline above it, nothing cut off; best
  when the video has text or wide shots), `--fit crop` when the subject stays in the middle, or
  reframing it on the subject in an editor.
- **Only the user's own footage.** A clip from someone else (a news clip, another creator, a
  public agency's video) with a headline or border added is still a repost to Instagram. Use it
  only as a short part of the user's own video, with their own voice or footage around it.
- To test two hooks, post both versions as Trial Reels (`"trial": "MANUAL"`) when the account
  qualifies, and keep the one that holds viewers longer.
- Text-only Reels (animated words, stats, lists) aren't made by this skill. If the user wants
  one, say so plainly and suggest a video tool, or post the idea as a carousel instead.

**Stories:** one image or video at 9:16. Make Story frames with `render_slides.py` and
`"ratio": "9:16"` in the theme (text slide types; the design stays clear of the Story bar and
reply field, no swipe arrow). Through the API there are no stickers, links or polls. Two good
patterns:

- **Teaser before the post** (scheduled): a question the post answers, 30 to 90 minutes before
  it. Tie it to the post with `"with": {"post": "<id>", "minutes": -60}`, and make any time
  written on the frame ("in an hour") match those minutes.
- **Share after the post** (in the app): the user shares the new post to their Story with the
  post sticker, which taps through. That can't be done through the API; it goes on the
  checklist and in `schedule.md`.

## Step 4: Write the captions

- **First words carry the search phrase and the hook.** Instagram search and Google read
  captions. The feed cuts around 125 characters with "... more": everything that matters goes
  before that.
- Then one or two lines of context, the same ask as the last slide, and at most 5 specific
  hashtags (Instagram's limit since December 2025). No hashtag walls, no generic tags like
  #instagood.
- Links aren't clickable in captions: "link in bio" only if it is in the bio.
- No long dashes, no "In today's fast-paced world", no emoji walls. Read it out loud; if it
  sounds like an ad or a robot, rewrite it.
- **Several accounts:** each account gets its own version, not just its own caption.
  Instagram's 2026 originality rules cover photos and carousels too, so the same media on a
  second account is likely seen as a repost of the first upload. Give each
  account its own media (`targets[].media`: another language on the slides, another cover,
  another order or angle) and its own first line and hashtags (`targets[].caption`). Write
  for the account's country: "grifo" in Spain, "llave" in Mexico; keep accents in hashtags
  (#geografía).
- Write alt text for every image (`alt` in the plan). The user pastes it in the app.

## Step 5: Check and fix

```bash
python3 scripts/ig_check.py plan.json          # report
python3 scripts/ig_check.py plan.json --fix    # fixed copies in fixed/, plan updated, originals kept
```

It checks file type, colour, size, shape, carousel count and shape match, video codec, pixel
format, HDR, frame rate, length, audio, file size, Reel cover, caption length, hashtags,
mentions, the "... more" cut, links, identical first lines across accounts, and posts per day.
`--fit crop|pad|frame` decides how shapes change. Auto, for photos: crop when little is lost,
otherwise pad with a blurred copy. Auto, for Reel and Story video: crop when little is lost,
otherwise stop and ask (see Step 3). `--ratio 4:5` makes wide photos 4:5. Run it until it exits with 0. Explain any
error it can't fix in plain words (a video that's too long needs trimming, a photo that's too
small needs a bigger original).

## Step 6: Schedule

```bash
python3 scripts/schedule.py plan.json --start 2026-11-09   # times and time zones come from accounts in plan.json
```

- Each account posts at its own `times` in its own `timezone` (set in `accounts` in the plan),
  from the user's Insights or their choice. Without them it uses 12:00 and says so at the top of
  `schedule.md`. Never claim a "best time".
- One feed post per account per day by default (`--per-day`). Stories don't take a feed slot;
  they follow the post they're tied to (`with`).
- It writes `schedule.md` (with what to do in the first hour after each post: be online to
  reply, share the post to the Story, the checklist) and one WoopSocial request per post and
  account in `requests/`.

## Step 7: Preview and the yes

```bash
python3 scripts/preview.py plan.json --out preview/ [--grid current-grid.png]
```

Look at `preview/preview.png` yourself first: each account's grid (newest first, as the grid
crops it), each post in the feed on every account with its own caption and "... more" cut, Reels
at their 4:5 feed crop, Stories full screen, every slide in order.
Fix what's off. Then give the user `preview/index.html` (and `schedule.md`) and ask for one
clear yes for the batch. Pass the grid screenshot from Step 1 with `--grid` to show the new
posts next to the old ones. Any change means a new check and a new preview.

## Step 8: Post with WoopSocial

Details: `references/woopsocial.md`.

1. `social_accounts_list` for the account IDs; put them in `accounts` in the plan.
2. Upload every file (`media_uploads_create_session`, `scripts/upload_parts.py`,
   `media_uploads_complete_session`), one at a time. Put the IDs in `mediaIds` and `coverId`,
   then `python3 scripts/schedule.py plan.json --bodies-only`.
3. `posts_validate` every request. Fix anything it rejects.
4. After the yes: `posts_create` per request, write each post ID into the target's `postId`,
   `posts_get` for the status, then `python3 scripts/log.py record plan.json`.
5. Tell the user exactly what's scheduled (account, time with time zone) and what to add in the
   app: the `checklist` items and the alt text.

Not connected and doesn't want to connect? Hand over the files, captions, alt text and the
schedule, and stop. Never say something was posted or scheduled when it wasn't.

## Step 9: Learn from the numbers

After 3 to 7 days: `social_account_posts_list` for the accounts, saved as `metrics.json`, then

```bash
python3 scripts/log.py results --metrics metrics.json [--csv insights.csv]
```

It ranks posts by sends, saves and follows per reach, only against posts of the same format on
the same account and of a similar age (3 to 10 days), names a best post only after 6 of a
format, and gives posting-time advice only with enough posts per time slot. Stories are left
out. `insights.csv` adds what only the app shows: follows, and for Reels average watch time and
skip rate, which matter most for Reels. Then:

| Sends | Saves | Next |
|---|---|---|
| High | High | Same format, new topic |
| High | Low | Shareable but thin: add a step or a checklist slide |
| Low | High | Useful but private: end with a send-style ask |
| Low | Low | Change the cover or the first second first, then the format |

"High" means against the account's own posts. Never estimate a number that wasn't reported.

## Quality bar

Before showing anything: would a top creator in this niche post this? Reject and fix it if:

- the cover or first second could belong to any other account;
- two slides or two posts in the batch make the same point;
- a claim, number or result can't be shown;
- it looks like a template, a deck or an ad;
- the grid preview looks like a wall of the same thing;
- two posts in the batch, or two accounts, show the same media.

## Edge cases

- **Personal account:** it can't post through any API; explain the free switch to Creator.
- **Over 20 carousel items:** split into two posts.
- **A video longer than 15 minutes, or a Story over 60 s:** trim it first; say which part to keep.
- **The user wants 3:4 in the grid:** the API only takes 4:5 or wider; offer 4:5 with the
  subject in the middle, or posting that one in the app.
- **Music:** can't be added through the API. Use the video's own sound, or post it in the app.
- **Collaborators, location, product tags, first comment, AI label:** add them in the app
  (checklist). Realistic AI images, video or voices need the "AI info" label.
- **Health, money or legal topics:** no promised outcomes; say who the advice is not for.
- **Paid partnerships:** the user turns on the paid partnership label in the app.
- **A scheduled post needs changing:** there's no edit; delete it (`posts_delete`) and create it
  again, after confirming with the user.

## References

- `references/instagram-specs.md`: current limits, grid and feed crops, reach signals, with
  sources and dates.
- `references/formats.md`: carousel formats, slide-by-slide templates, cover patterns, honesty
  check.
- `references/design-rules.md`: slide presets, type scale, margins, the slides.json spec.
- `references/plan-json.md`: the plan file every script reads.
- `references/woopsocial.md`: connect, upload, validate, post and read results.
