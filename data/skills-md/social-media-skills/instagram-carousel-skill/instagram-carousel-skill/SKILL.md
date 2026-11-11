---
name: instagram-carousel-skill
description: >-
  Instagram carousel skill: plan, write, design and post Instagram carousels that people save and
  send, for an app, SaaS, product or personal brand. Picks a proven format (step-by-step,
  listicle, myth vs fact, framework, case study, tweet-card thread, photo story), writes the
  cover and a slide 2 that works on its own, renders native-looking 1080x1350 JPEG slides locally
  (Python + Pillow, bundled open-source fonts, no browser, no paid API), writes alt text and a
  keyword-first caption, then posts the carousel to one or many Instagram accounts with WoopSocial
  after you approve it, and reads the results back. Use when someone says "instagram carousel,"
  "make a carousel," "carousel post," "carousel for my app," "turn this into a carousel,"
  "educational carousel," "swipe post," "carousel template," or "post a carousel to instagram."
  Never invents results, reviews or stories, confirms before anything posts. Standalone: needs
  no other skills.
metadata:
  version: 1.0.1
license: MIT
---

# Instagram Carousel Skill

Carousels are the Instagram format people save and send. They also get a second chance: when
someone scrolls past without swiping, Instagram may show the post to them again starting at
slide 2. Most carousels still fail for the same few reasons: a cover that describes the topic
instead of stopping the scroll, a slide 2 that only works after slide 1, too many words per
slide, a template look with progress bars and arrows everywhere, and a last slide that asks for
nothing anyone wants to do.

This skill does the whole job: it picks a format that fits the idea, writes the slides, renders
them as clean JPEGs on the user's machine, writes alt text and a caption, posts through
WoopSocial after the user says yes, and reads the numbers back. Everything it needs is in this
folder.

Four commitments:

1. **One idea per slide, readable at phone size.** Big type, short lines, nothing below the
   size floor.
2. **Native, not templated.** A small name and handle, no progress bars, no slide numbers, no
   logo except on the last slide.
3. **Nothing posts without a yes.** Show the exact slides, caption and account first.
4. **Only real things.** Real screenshots and photos, real experiences from the user, real
   numbers with dates. Never invent a result, a review, a statistic or a first-person story.

## Step 0: Know the account

If the workspace has brand notes (`brand.md`, `brand-profile.md`, a README), read them.
Otherwise ask, in one message:

1. What is the account about, and who is it for (one specific person)?
2. What do you want this carousel to do: get saved (reference), get sent (shareable), or bring
   people to a product or link?
3. What do you actually know that your audience doesn't? Real experiences, numbers you can
   show, mistakes you made, what customers ask you. Story and case-study formats need these.
4. What visuals exist: screenshots, your own photos, an image model, or none (then text-led
   styles or free stock photos)?
5. Name and handle to show on the slides, an avatar or logo image (a letter disc looks
   unfinished, so ask for one), and a brand colour.
6. Anything that must not be said (claims, prices, names)?

## Step 1: Pick the format and write the cover

Formats with slide-by-slide templates: `references/carousel-formats.md`. The short version:

| Goal | Format | Slides |
|---|---|---|
| Saves (reference) | Step-by-step, framework, listicle, each with a recap slide before the last | 7 to 12 |
| Sends (shareable) | Myth vs fact, tweet-card thread, relatable list | 6 to 10 |
| Trust (proof) | Case study, before/after (only with real results) | 6 to 12 |
| Mood, behind the scenes | Photo story | 5 to 10 |

Growth formats need at least 7 slides; a carousel under 5 slides wastes the second chance.

**Write 10 covers before choosing one.** A cover:

- Names a result or a tension, not a topic. "Missed a day? Your habit is fine." beats "Habit
  tips".
- Uses 8 words or fewer (10 at most), so it reads in one glance at feed size.
- Is specific: a number, a moment, a named mistake.
- Promises something the carousel delivers. No bait the slides don't pay off.

Pick the strongest with the user, keep the rest in `covers.md` for later tests.

**Slide 2 must work as a cover on its own**, because of the second chance. Put the strongest
point or the most surprising line there, never "let's dive in".

## Step 2: Write the slides

- One idea per slide. Headline 8 words or fewer; body 30 words or fewer (45 at most).
- Plain words, short sentences. Write for the person, not the algorithm.
- Use `*word*` for the one to three words that matter most on a slide (accent colour) and
  `~~words~~` to strike out a myth.
- The product, if any, appears once, near the end, shown for real with a screenshot slide. A
  carousel that teaches something useful earns the product mention; one that is all product
  reads as an ad.
- Last slide, one ask, matched to the goal:
  - Sends: "Send this to the friend who [specific situation]."
  - Saves: "Save this for the next time you [situation]."
  - Comments: a question people want to answer.
  - Link: "The link is in the bio" only if it is.
  - Comment keyword ("Comment GUIDE and I'll send it") only if the user will answer every DM
    by hand; WoopSocial doesn't send DMs.
- Caption: the main search phrase in the first words (Instagram captions are indexed by Google),
  one or two lines of context, the ask again, and at most 5 specific hashtags.
- Alt text for every slide: one sentence that says what the slide shows and says.

Run the honesty check before rendering (details in `references/carousel-formats.md`): every
claim is something the user did, saw or can show; no invented numbers, reviews or stories;
screenshots are real and current; photos are the user's own, licensed or generated for this
post.

## Step 3: Render

Write `carousel.json` and render:

```bash
python3 scripts/render_carousel.py carousel.json --out carousel/
```

Spec format, slide types and style presets are documented at the top of the script and in
`references/design-rules.md`. In short:

- **Presets:** `editorial` (serif or sans headlines on paper or dark), `notes` (plain, phone
  notes look), `tweet` (tweet-card thread, light or dark). Photo slides work on any preset.
  Use the tweet look only for the user's own voice; if the brand isn't on X, use `notes`.
- **Slide types:** `cover` (text, photo or screenshot), `text`, `step`, `list` (recap or
  checklist), `myth`, `stat` (with a `source`), `tweet`, `photo`, `screenshot`, `beforeafter`,
  `cta`.
- **Size:** 1080x1350 JPEG, the size the Instagram API accepts. `"ratio": "3:4"` makes 1080x1440
  for manual upload only; the API rejects it.
- **Fonts:** Inter and Instrument Serif, bundled (SIL Open Font License). No emoji on slides;
  put them in the caption.

The script writes the slides, `contact-sheet.png`, `cover-grid.png` (the cover as the profile
grid shows it) and `manifest.json` (byte sizes, alt text, warnings). **Open every slide at full
size, then the contact sheet. Judge the cover from `cover-grid.png`, not the full-size image.**
Fix every warning: text below the size floor, too many words, text on a face, a number without a
source, a missing alt text. Then check what no script can:

- Does the cover stop you at grid size?
- Does slide 2 make sense if it's the first slide someone sees?
- Is every slide one idea, and does each one give a reason to swipe?
- Does every line end on a strong word? Write line breaks into headlines (`\n`) where they
  read best.
- Would the user be proud to post this under their own name?

Photos: one shoot per carousel looks intentional; five unrelated stock photos look like stock.
Free photos with a commercial license come from Pexels and Unsplash; keep a credits file.

## Step 4: Post with WoopSocial

How to connect, upload and post: `references/woopsocial.md`. Short version:

1. **Check the connection** with `social_accounts_list`. If WoopSocial isn't connected, give the
   one connect path for the agent you're running in (free plan: 2 social accounts, no card),
   then `oauth_create_authorization` for Instagram and hand the user the link.
2. **Upload each slide** with an upload session: `media_uploads_create_session` with the exact
   byte size from `manifest.json`, `python3 scripts/upload_parts.py session.json <file>`, then
   `media_uploads_complete_session` (poll `media_uploads_get_session` until `READY`). Keep the
   media IDs in slide order.
3. **Build the post**: Instagram, `postType: POST`, the media in order, the caption. Run
   `posts_validate` and fix what it rejects.
4. **Show the user** the contact sheet, the caption, the account and the time (with timezone),
   and get a clear yes. Then `posts_create` and confirm with `posts_get`.
5. **After posting**, tell the user what WoopSocial can't set: alt text per slide (paste it from
   `manifest.json` via the post's "Edit" > "Edit alt text" in the app), collaborators and music.

Several accounts: each account gets its own cover and variant, never the identical carousel.
Not connected and doesn't want to connect? Hand over the slides, caption and alt text and stop.
Never claim something was posted when it wasn't.

## Step 5: Read the results and decide what's next

After 3 to 7 days, read the post's stored metrics with `social_account_posts_list` (what
Instagram reports, with the collection date; a missing number is "not reported", never zero).
Instagram's API reports per post, not per slide; the per-slide view is only in the app.

Log each carousel in `carousels.md`: date, account, format, cover, reach, saves, shares, and
what the user saw in the app. Then:

| Saves | Shares | What to do |
|---|---|---|
| High | High | Make the next one in the same format with a new topic |
| High | Low | Useful but not shareable: try a send-style last slide |
| Low | High | Shareable but thin: add a step or a checklist slide |
| Low | Low | Change the cover first, then the format |

"High" means against the account's own recent posts. Never estimate saves, shares or reach.

## Quality bar

Before showing anything, ask: would a top creator in this niche post this? Reject and fix it if:

- any slide could be swapped into another brand's carousel unchanged;
- two slides make the same point;
- the product slide claims something its screenshot doesn't show;
- a slide looks like a deck, a template or an ad.

## Edge cases

- **Too much to say:** split into two carousels, never shrink text below the floor.
- **More than 20 slides:** Instagram's limit is 20; cut or split.
- **No brand colour:** use the preset's accent.
- **The user wants 3:4:** render it for manual upload, explain the API won't take it.
- **Health, money or legal topics:** no promised outcomes; say who the advice is not for.
- **Client or sponsored posts:** the user marks it as a paid partnership in the app.

## References

- `references/carousel-formats.md`: formats, slide-by-slide templates, cover patterns, honesty
  check.
- `references/design-rules.md`: type scale, margins, presets, spec format, what reads as a
  template.
- `references/instagram-2026.md`: platform facts, API limits and ranking signals, with dates.
- `references/woopsocial.md`: connect, upload, post and read results.
