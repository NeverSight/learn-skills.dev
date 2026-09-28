---
name: fountain-daily-growth
description: Read yesterday's results and today's news, then brief fountain-clip-finder on the best trends.
---

## Overview

This skill is the first step of the daily content chain.
It runs two modules in order.
Module **performance-review** reviews yesterday's posts.
It turns the numbers of those posts into lessons in the preferences.
Module **trend-discovery** reviews today's news.
It scores the news and makes the best trends into briefs for skill **fountain-clip-finder**.
The skill itself updates the narratives first, because both modules read them.

## Input

- `show` - the show to run the loop for.
- The Narratives and Editorial sections of the preferences.

## Output

- One brief per advancing trend, handed to skill **fountain-clip-finder**.
  A brief is a completed trend of module **trend-discovery**.
  Each brief holds its share of the day's clip budget as `clip_count`.
- One report for the day.
  It shows the posts that wait, then yesterday's numbers.
  With auto-render on, the report goes out when the videos exist, and it is the only mail of the day.
- Updated preferences: the narratives, and the lessons of module
  **performance-review**.

## Housekeeping

You MUST read HOUSEKEEPING.md if you haven't already.

## Requirements

- An HTTP client, e.g. curl, for the Google News RSS route of module **trend-discovery**.
- Optional: a web search tool, and a social trend search tool such as one for X, when the machine has them.
- Fountain API.
- Skill **fountain-clip-finder**.
- Skill **fountain-reports**.
- Skill **fountain-onboarding**.

## Process

1. Update the Narratives section, because both modules read it.
2. Run module **performance-review** to turn yesterday's posts and their numbers into lessons.
   Skip it when a render machine sends the report, because that machine runs it.
3. Run module **trend-discovery** to score today's trends and shape the strongest into briefs.
4. Hand each brief to skill **fountain-clip-finder**, and do not read its result.
   The chain continues without this skill.
5. List the day's drafts with the Social API, because step 4 hands the briefs on and never reads them back.
   Render them with skill **fountain-clip-producer**, under the rules of Rendering below.
6. Send the day's report one time, as the `review-posts` report of skill **fountain-reports**.
   The report shows the clips that wait, then the numbers of module **performance-review**.
   Ask skill **fountain-reports** to send the report and also to print the same report here.

## Additional notes

Some steps repeat one API call over many items.
Examples are the numbers of each post, the news of each subject, and the drafts of each clip.
These items do not depend on each other, so ask for them all at the same time.

This skill owns the two morning modules, and none of the work after them.
Finding moments and writing the copy is the job of skill **fountain-clip-finder**.
Rendering is the job of skill **fountain-clip-producer**, run here or on a render machine that picks the
drafts up from the Social API.

The rules for rendering come from the Automation section.
Auto-render is on unless that section says otherwise.

- With auto-render on, render the drafts here as a clean final.
  Then the user reviews the clip, and not a description of it.
- With no confirmed kit under Brand, render the strongest clip first, as the style proof of skill
  **fountain-clip-producer**.
  Render the rest after the user confirms or corrects that clip.
  This is because a batch in the wrong look is rendered twice.
- With a render machine named for this show, do not render here.
  The render machine renders the drafts and sends the report.
  Stop after step 5, unless no draft waits for a video.
  When no draft waits, the render machine renders nothing and sends nothing.
- With auto-render off, something else has to render.
  Say which: the user's word in the chat, or a render machine that works this show.
  The thing that renders later sends a second mail to say that the renders are ready.
  That mail is the only other mail.
  When the user wants the day to finish without them, run skill **fountain-onboarding** to schedule that
  render.
  This is because a draft that nothing renders never becomes a clip.

When auto-render is on, the report waits for the videos, so the reader reviews clips and not descriptions.
When auto-render is off, the report goes at once, and its approve note says what renders a clip.
Give the label of each source, and its publish date when known.
For a source with an episode id, the label is the episode.
For other sources, the label is the external video title from `context`.
The printed report is all that the chat shows about the day's clips.
It also covers the clips that this run did not make.
This is because a day at budget still has clips that the user has not seen.

A caller that has just rendered the day's drafts can ask for the report alone.
Run steps 2 and 6 for that caller, and put the drafts that it gave up under warnings.
Skip the report when the line that module **performance-review** writes in the Reporting section already
has today's date.
This makes sure that a second pass of the render machine never mails the day twice.

An empty Editorial section does not stop the skill.
Proceed, and tell the user plainly that the section is empty.

Use this skill for the recurring daily cycle.
For a one-off "find me a clip about X", use skill **fountain-clip-finder** directly.
