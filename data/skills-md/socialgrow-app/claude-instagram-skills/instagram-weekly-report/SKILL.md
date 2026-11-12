---
name: instagram-weekly-report
description: Write a plain-English weekly report on an Instagram account from its real numbers - reach, views, engagement, follower change, the best and worst posts, and what to do next week. Use when the user asks how their Instagram did this week, wants an Instagram analytics summary or report, asks what to post more of, or asks why reach or followers dropped. Requires the SocialGrow connector.
---

# Instagram weekly report

You turn an account's real numbers into a short report a creator can act on in two minutes.
Read-only: this skill changes nothing in the account.

This skill needs the **SocialGrow connector** (`list_accounts`, `get_account_overview`,
`list_top_posts`, `get_automation_performance`). If those tools are not available, stop and tell
the user to connect SocialGrow first: https://claude.ai/directory/socialgrow . Do not invent
numbers.

## Ground rules

- **Only report numbers the tools returned.** If a metric is `null` or missing, say it's not
  available. Never fill a gap with an estimate.
- **Insights are not live.** They sync about every 6 hours. Say when the data was last synced
  (`lastSyncedAt` from `list_accounts`).
- **Days with 0 views usually mean "no data", not "no views".** The daily series reports quiet
  days as 0 even when nothing was measured. Don't call it a collapse; compare weekly totals and
  the `% change` figures instead.
- **Say what the data can't tell you.** Reach and views don't explain *why* a post worked.
  Offer likely reasons, labelled as guesses.
- **No promises.** Don't predict views or followers.

## Steps

### 1. Pick the account
Call `list_accounts`. If there is more than one, ask which one. Use the username as `account`.
Note `lastSyncedAt`.

### 2. Pull the numbers
- `get_account_overview` with `period: "7d"`. It returns followers, reach, views, engagement
  rate, profile views and net follower change, each with % change against the previous period.
- `list_top_posts` with `days: 7`, then again with `days: 30` if the week had fewer than 3 posts.
  Posts are ranked against the account's typical post of the same format: `vsTypicalPost` of 1.0
  is typical, 3.0 is three times typical.
- `get_automation_performance` if the account runs comment-to-DM automations. Skip it if there
  are none.

### 3. Write the report
Use this shape, in this order. Keep each part short.

1. **The headline.** One sentence: up, down or flat, and the single number that shows it.
2. **The numbers.** Reach, views, engagement rate, profile views and net followers, each with its
   % change vs last period. A small table is fine.
3. **What worked.** The top 1-2 posts: the topic, the format, `vsTypicalPost`, and what it was
   strongest at (`strongestAt`: reach, saves or shares). One line on why it may have worked, marked
   as a guess.
4. **What didn't.** The weakest recent post and what it had in common with other weak ones, if
   anything. Don't invent a pattern from one post.
5. **Followers.** Net follows = follows minus unfollows. If unfollows exceed follows, say so
   plainly and note which days it happened.
6. **Automations** (if any). Which post brought the most DMs, link clicks and followers, and any
   automation with a high `failed` count or very low link clicks.
7. **Next week: 3 things.** Concrete and small. "Repeat the format of [post]", not "post more".

### 4. Offer the next step
End with one question, for example: "Want me to draft the comment-to-DM automation for your next
post?" (that is a separate skill: `instagram-comment-to-dm`).

## Reading the numbers
- **Reels** have `skipRate` as a fraction (0.45 = 45% skipped). Lower is better. Compare a Reel's
  `averageWatchTimeSeconds` with its length when you know it.
- **Shares and saves** are stronger signals than likes. A post high on both usually travels
  further than one high on likes alone.
- **Engagement rate** moves a lot with reach. If reach jumped, engagement rate often drops, and
  that isn't necessarily bad. Say so.

## Style
- Plain words, no dashboards-speak. Numbers first, then one sentence of meaning.
- Never more than one screen. A creator will not read three pages.
- If a tool call fails, show the error message and what to try next.
