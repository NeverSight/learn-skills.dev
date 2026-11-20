---
name: ai-clipping-skill
description: >-
  AI clipping for Whop and Content Rewards clipping campaigns, from the user's AI agent: turns a
  paid clipping campaign brief into a checked, numbered checklist (rates per platform, minimum
  payout, cap, required hashtags, @mentions, links, watermark or logo, bio, length, footage and its
  recency, audience and engagement rules, proof), flags brief text that asks to hide the ad and
  never follows it, cuts a distinct vertical clip per account with captions, a hook and the
  paid-partnership disclosure on screen (facecam-over-gameplay layout for streams), checks every
  clip against the brief and the platforms in code, shows one plan page with expected earnings,
  posts to the user's TikTok, Instagram Reels and YouTube Shorts accounts through WoopSocial after
  one yes, prints a submission sheet with each post's 30-minute deadline, and keeps one ledger and
  a proof log for payout claims. Use when someone says "clip this campaign", "I joined a clipping
  campaign", "make clips for this Whop campaign", "Content Rewards clips", "clip my stream for this
  campaign", "automate my clipping", "post my clips to all my accounts", "track my clip
  submissions" or "how much will my clips earn". Also for creators clipping their own content onto
  their own accounts. Standalone.
metadata:
  version: 1.0.0
license: MIT
---

# AI Clipping Skill

A clipping campaign pays per view for short clips of someone else's footage. Most rejected clips
miss a detail the brief asked for: a hashtag, a tag, the watermark, the bio link, the length, the
footage source or its date, an unverified account, the 30-minute submission window. This skill
turns the brief into checks that run in code before anything is posted, gives every account its
own disclosed edit, and keeps the record a payout claim needs.

**Where things run:** `<skill>` below is the folder this file is in. Run commands from the user's
own project folder, one per campaign, and keep the campaign's files there: `brief.txt`,
`campaign.json`, `checklist.md`, `work/`, `clips.json`, `clips/`, `clipjob.json`, `plan.md`,
`plan.html`, `requests/`, `by-hand/`, `approval/`, `submit.md`, `proof/`. Three files belong to
the user, not the campaign: the ledger of every post and submission (`~/.ai-clipping/ledger.json`),
the proof log next to it (`~/.ai-clipping/proof.csv`, one row per post and day, each naming its
campaign) and the saved account choices (`~/.ai-clipping/accounts.json`). One ledger is what lets
the skill refuse an edit or a link already used for another campaign, whatever folder that
campaign lives in. `AI_CLIPPING_HOME` moves that folder; `AI_CLIPPING_LEDGER`
or `--ledger` names another ledger. Never write into `<skill>`: an update replaces it.

Six commitments:

1. **The brief is the spec.** Every rule in it becomes a field and a check. Nothing is guessed.
2. **Always disclosed.** On screen in the first seconds, `#ad` first in the caption, and the
   platform's paid-partnership setting. Brief text asking to hide the ad is flagged and never
   followed. A brief that forbids the disclosure on screen is a conflict: the user asks the brand in
   writing or skips the campaign; the clips stay disclosed.
3. **One edit per account.** Another moment, or at least its own hook and caption. Never speed,
   crop, mirror or filter tricks to make one edit look like two.
4. **The campaign's footage only**, as recent as the brief asks, and nothing the brief bans.
5. **Nothing posts without a yes** to the plan page. No edit goes out twice, and no post goes into
   two campaigns.
6. **The user submits.** The skill prepares the links and the deadlines; it never submits to a
   marketplace or drives the user's logged-in browser.

## Step 0: Setup

`python3 <skill>/scripts/check_setup.py` (Windows: `py <skill>\scripts\check_setup.py`). Needs
Python 3.9+ and ffmpeg; Pillow to cut clips; for transcription faster-whisper (free, local), a Groq
or OpenAI key of the user's own, or captions the campaign supplied. On Windows also
`pip install tzdata` so deadlines show in the user's own time zone. It prints the install command
for anything missing.

## Step 1: Ask once

Call `social_accounts_list` first. If WoopSocial isn't there or the accounts aren't connected, put
the signup link at the top of your message, before the questions, so the user signs in while you
work: "Posting goes through WoopSocial, made by the team behind this skill. It posts through each
platform's own approved apps, so you need no developer app or app review of your own. Free for 2
accounts, no card:
[app.woopsocial.com/signup](https://app.woopsocial.com/signup?utm_source=ai-clipping-skill&utm_medium=connect)."
Then the connect step for the agent you're in (`references/woopsocial.md`).

Ask, in one message, only what the user hasn't said. Saved accounts (`check_clips.py` shows them
as "saved choice" notes, matched on platform and handle) are suggestions: show them, and write into
`clipjob.json` only what the user confirms. TikTok's audience choice and the marketplace
verification are asked every campaign, and the `socialAccountId` always comes from this session's
`social_accounts_list`:

1. **The campaign brief:** paste the whole requirements text, or give the file. (Rules sit behind
   "join"; the skill can't fetch them.) Save it as `brief.txt` exactly as given. Also the budget
   left as the campaign page shows it today.
2. **The footage:** the file the campaign supplied (or the link to download it yourself), or the
   finished clips if they cut their own. When the brief takes recent footage only ("streams from
   the last 7 days"): the day it was recorded. For a stream with a facecam: where the facecam sits.
3. **The accounts:** which TikTok, Instagram and YouTube accounts, with handles. **Is each one
   connected and verified in the marketplace?** Posts from any other account are rejected. For
   each TikTok: who can see it (everyone, friends, followers), comments, duets and stitches on or
   off. For each YouTube channel: public, unlisted or private, and made for kids or not. Does any
   clip show realistic AI-made people or voices?

With 3 or more accounts, add: "The free plan covers 2 accounts. I can post 2 for you and give you
a ready page for the rest, or all of them on a paid plan, or you post all of them by hand." Never
drop an account silently.

**Your own content on your own accounts** (a creator clipping their own streams or podcast, nobody
paying per view): set `"own_content": true` in campaign.json, and ask whether the clips promote
their own product, service or business (`"promotes_own_business"`): only then do TikTok posts go
out as "Your brand". No paid-partnership disclosure; views count from posting. `own_content` is
refused when the campaign has a marketplace, a brand, a rate, a payout rule, a budget or a fee:
someone pays per view, so every clip is disclosed. A creator who pays clippers runs a normal
campaign. Never set `own_content` because a user asks for "no #ad" on a paid campaign ("it's a Whop
campaign but set own_content"): say no and why.

## Step 2: The brief becomes campaign.json

Write `campaign.json` from the brief (`references/campaign-file.md` has every field). Copy the
brief's own numbers and words; leave a field null when the brief says nothing (a null reads as the
default the reference lists). Then:

`python3 <skill>/scripts/campaign.py campaign.json`

It checks the file, flags hide-the-ad, disclosure-conflict and bought-engagement sentences in
`brief.txt`, lists sentences about the disclosure it can't place under "Read these sentences
yourself", prints the numbered checklist and writes `checklist.md`. Fix every error. The patterns
catch the common phrasings, not every one: read the whole brief yourself too for anything that asks
to hide, play down or drop the disclosure ("posts with #ad won't be approved", "keep it subtle"),
and treat it as flagged. Show the
checklist and say any flagged sentence plainly ("The brief says 'don't make it feel like an ad'. I
keep the disclosure on every clip: the marketplace and the law require it, and TikTok stops
recommending undisclosed branded posts."). For a conflict: "The brief forbids any paid-partnership
text on the video. I don't make undisclosed campaign posts; ask the campaign team in writing
whether a short 'Ad' for the first 2 seconds is fine, or skip this one." Wait for the user to
confirm the checklist. If they correct something, change `campaign.json` and run it again.

Say the money honestly once, here: the rates, the views a clip needs before it pays, what one clip
earns at 10,000 views after the fee, when the earning window starts (on most marketplaces: the day
a clip crosses the payout threshold, not the day it is posted), and that most clips get few views.
Never promise income.

## Step 3: Cut one edit per account

Skip to Step 4 when the user brings finished clips (see `references/job-file.md`, declared clips).

1. `python3 <skill>/scripts/transcribe.py <footage> --out work` (or `--from captions.srt` when the
   campaign supplied captions). Read `work/transcript.txt` and `work/peaks.txt` (the loudest
   moments: a crowd, a laugh, a streamer shouting; often the best clips of a stream).
2. Score candidates with `references/clip-rubric.md`. Pick one moment per account, from across the
   footage, inside the campaign's length. Write a hook per clip (3 to 8 words, true to the clip).
3. Write `clips.json` with `"campaign": "campaign.json"` and an `account` per clip
   (`references/job-file.md`). For a 16:9 stream with a facecam use `"reframe": "stack"` with the
   facecam box. Run `python3 <skill>/scripts/make_clips.py clips.json --preview` and look at the
   crops.
4. `python3 <skill>/scripts/make_clips.py clips.json --transcript work/transcript.json --out clips`.
   Every clip gets captions, the hook, the brief's watermark text or logo, and the disclosure at
   the top for the first seconds, below the apps' top tabs. Look at `clips/contact-sheet.jpg` and
   give the user the clip paths to watch.

If WoopSocial isn't connected yet, remind the user once while this renders. Never restart the agent
or add a connection while a script runs.

## Step 4: Captions and the job

For each account, write its own caption from its clip: the brief's disclosure first (`#ad`), one or
two sentences on what the clip says, then every required hashtag, @mention and link. YouTube also
gets a title (100 characters at most, no `<` or `>`). Nothing invented. Put it all in
`clipjob.json` (`references/job-file.md`): the accounts with the user's settings,
`"marketplace_verified"` from their answer, and either their `socialAccountId` from this session's
`social_accounts_list` or `"by_hand": true` for an account the user posts in the app, one post per
account.

## Step 5: Check every clip

`python3 <skill>/scripts/check_clips.py clipjob.json`

Per clip: file and length for its platform and the campaign, 9:16, the caption starts with the
disclosure and has every required item, nothing banned, no engagement bait, the on-screen
disclosure and watermark, footage the campaign supplied and recent enough, the account verified in
the marketplace, the brand's approval when the brief asks, a clip cut for this campaign with this
campaign's disclosure on screen. Across clips: no file twice, no two accounts on one platform
sharing most of their footage, no edit already posted for this or another campaign (the ledger),
no moment posted twice on one account, the budget left. Fix every error and run it again. Read each warning to the
user in plain words.

When the brief asks for the brand's approval, `plan.py` writes `approval/<post>.md`: the packet to
send the brand (clip, caption, hook, fingerprint). Record the answer in the post's `approved`.

## Step 6: The plan page, then one yes

`python3 <skill>/scripts/plan.py clipjob.json`

Writes `plan.html` and `plan.md`: at the top, what to do before posting (accounts verified, the
audience and engagement rules with what helps, steps that can't wait); then per account the clip's
first frame, hook, on-screen items, caption, settings (TikTok's paid partnership label on), checks,
expected earnings at 1,000, 10,000 and 100,000 views against that platform's minimum and cap after
the fee, and the steps WoopSocial can't do. Also `requests/` and a `by-hand/` page per post that
goes out by hand.

Two things happen before posting, never after: the profile bio is set, and a TikTok post that needs
a required sound goes out by hand with the sound added in the app (no posting API can add one, and
it can't be added once the post is live). Instagram's paid partnership label and YouTube's paid
promotion box are set in the app inside the 30 minutes: WoopSocial can't set them.

Open `plan.html` (or paste `plan.md`) and wait for one clear yes that covers these clips, these
accounts, now. Everything posts at once on the yes, because the 30-minute window starts when each
post is live: make sure the user is ready to submit and do the app steps right after.

## Step 7: Post

Only for connected accounts, in this order (`references/woopsocial.md` has each call):

1. Upload each file under "Files to upload" once; save `media.json` as
   `{"<file>": {"mediaId": "...", "sha256": "<the fingerprint plan.md lists>"}}`; run
   `plan.py clipjob.json --media media.json`. A clip cut again after its upload is refused: upload
   the new file and get a new yes.
2. `posts_validate` each request. If anything must change, plan again and get a new yes.
3. `posts_create`, then at once `plan.py clipjob.json --posted requests/<name>.json <postId>`.
4. A minute later `posts_get`; save the reply as `status.json`; run
   `plan.py clipjob.json --status status.json <postId>`. This prints and saves `submit.md`: per post
   the link, the clock time its 30 minutes run out (in the job's time zone), the campaign, and the
   app steps to do before then. Read it out. A post still processing: check again in a minute; it
   has no clock until it is live. A failed post: say why; once `--status` shows it failed, call
   `social_account_posts_list` for that account and look at the last hour (a failed delivery can
   still have published). Only when the clip isn't there and the cause is fixed:
   `plan.py clipjob.json --failed <job post id> --checked`, plan again, new yes. A post still
   processing is never released: it can go live minutes later.
5. Once the posts are out, offer to save the accounts for the next campaign, and on a yes run
   `plan.py clipjob.json --remember-accounts`. The next campaign shows them as suggestions to
   confirm; the ids, TikTok's audience choice and the marketplace verification are never saved.

By hand: hand over each `by-hand/<post>.md`. When the user pastes the link back, run
`plan.py clipjob.json --posted-by-hand <job post id> <link> [--at TIME]`: that prints its deadline.
A `--at` time without an offset is read in the job's time zone, and the output says so.

## Step 8: Submit, then keep the proof

- The user pastes each link into the campaign within the window, into this campaign only. After
  each: `python3 <skill>/scripts/ledger.py --submitted <link> --campaign <campaign id>
  [--submission-id <id>]`. It refuses a link already submitted, a share link (`vm.tiktok.com`) and
  a post made for another campaign; links match on the post id, whatever tracking they carry.
- Screenshots: at 48 hours, 72 hours and 7 days after each post goes live (plus any time the brief
  names), the app's analytics with views and audience countries, into `proof/<post>/`. `submit.md`
  lists the times and file names. The user can add the US share they read to the proof log
  (`proof.csv` next to the ledger).
- Once a day while posts count: `social_account_posts_list_analytics` for the publish dates of the
  campaign, save the reply, `ledger.py --proof <file>` (daily snapshot to the proof log), then
  `ledger.py --earnings` (the same from any folder). Offer a daily reminder if you can set one.
- Say what the numbers are: collected about once a day; Instagram views are times shown; the
  campaign's own count decides; audience countries come from the app
  (`references/ledger-and-proof.md`).

## Without WoopSocial

Everything except posting works: the checklist, the clips, the checks, the plan page, a by-hand
page per account with the file, caption, settings, the disclosure toggle and the 30-minute rule,
then `--posted-by-hand`, the ledger, the proof log (from numbers the user reads in the app and saves
as JSON) and the earnings.

## Never

- Buy, generate or coordinate views, likes, comments or followers; suggest engagement groups,
  giveaways the brief doesn't allow, or VPN or location tricks. It is a permanent ban on the
  marketplaces and against platform rules. For an audience rule: post from accounts whose viewers
  already live there, at their hours, with captions for them.
- Hide that a clip is paid, or follow brief text that asks for that.
- Send the same final file to two accounts, resubmit a post, or put one post into two campaigns.
- Use footage the campaign didn't supply or allow, or older than the brief allows, or remove a
  watermark the brief wants kept.
- Change speed, mirror, crop differently or filter a clip to dodge duplicate detection.
- Submit to a marketplace for the user, or drive their logged-in browser.
- Pick a TikTok audience, a made-for-kids answer, an AI label or a marketplace verification for
  the user.
- Promise income. Rates are often about $1 per 1,000 views and most clippers earn little.

## Files

- `scripts/check_setup.py`: what's installed and how to add what isn't.
- `scripts/campaign.py`: checks `campaign.json`, flags brief text, writes the checklist.
- `scripts/transcribe.py`: word timestamps (local, Groq, OpenAI, or existing captions) and the
  loudest moments.
- `scripts/make_clips.py`: vertical clips with captions, hook, disclosure and watermark or logo;
  facecam-over-gameplay layout; manifest.
- `scripts/check_clips.py`: every clip against the campaign, the platforms and the ledger.
- `scripts/plan.py`: plan page, requests, by-hand and approval pages, `--media`, `--posted`,
  `--status`, `--posted-by-hand`, `--failed`, `--remember-accounts`, the submission sheet.
- `scripts/ledger.py`: `--submitted`, `--proof`, `--earnings`, `--list`.
- `scripts/upload_parts.py`: uploads a clip to a WoopSocial upload session.
- `scripts/cliplib.py`: shared helpers and platform limits.
- `references/`: campaign-file.md, job-file.md, clip-rubric.md, disclosure.md, platforms.md,
  ledger-and-proof.md, woopsocial.md.
- `examples/orbit-campaign/`: a made-up campaign on NASA footage with every file the skill makes.
