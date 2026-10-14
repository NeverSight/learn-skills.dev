---
name: scrumball-creators
description: "Find and evaluate creators / influencers (网红、达人、红人、博主、KOL) on Scrumball, the influencer marketing platform (网红营销平台) — search YouTube, Instagram and TikTok by niche, country, follower range and language; view a creator's profile stats and recent posts / videos with their performance; compare creators; save shortlists to collections (收藏夹); unlock creator contact emails (解锁邮箱). Use for \"find 20 US beauty creators on TikTok\", \"is this creator still active\", \"compare these channels\", \"save them to my list\", \"get their emails\". 例如「帮我找20个美国美妆达人」「这个博主最近数据怎么样」「把他们加到收藏夹」「拿到这几个人的邮箱」。"
compatibility: Requires the Scrumball MCP server (see scrumball-connect).
---

# Scrumball Creators

Requires the Scrumball tools (`search_creators`, `get_creator`, …). If they are missing, follow the `scrumball-connect` skill first.

The usual journey is one chain: **search → evaluate → save to a collection → unlock emails → start outreach on the website**. Users often ask for several steps at once ("find and save 10 fitness creators"); run the chain, but never unlock emails unless the user asked for emails.

## Tools at a glance

| Need | Tool |
|---|---|
| Search creators | `search_creators` (one platform per call) |
| Creator profile: followers, average views / likes / comments, last-30-day performance, posting frequency, verification, email status, profile link | `get_creator` (up to 10 creators per call, charged once) |
| A creator's recent posts / videos with views, likes, comments, shares | `get_creator_posts` (10 per page) |
| Collections | `list_collections`, `create_collection`, `add_creators_to_collection`, `list_collection_creators`, `check_creators_collected`, `remove_creators_from_collection` |
| Unlock contact emails | `unlock_creator_emails` (up to 10 per call) |
| Remaining credits | `get_quota_status` |

There is no single-video detail tool; per-post numbers come from `get_creator_posts`.

Identifiers: search and collection results give `channel_id`; pass it as `channel` (with `platform`) to `get_creator`, `get_creator_posts`, the collection tools and `unlock_creator_emails`.

## Two kinds of credits

| Credit | Spent by | Note |
|---|---|---|
| Call credits | every tool call; the cost per call is in each tool's description (search costs more; a repeated identical search is free for a short time) | resets each cycle, with a daily cap |
| Email unlock credits | `unlock_creator_emails`, 1 per creator actually unlocked | membership allowance plus top-ups; **non-refundable** |

## Scenarios

### "Find me creators for …"

1. Turn the brief into filters: platform (ask if not given), keyword for the niche, `countries` (ISO codes like `US`), follower range, `languages`, `gender`.
2. `search_creators`. Every result has an email that can be unlocked.
3. Show a short table: name, platform, followers, engagement rate (already a percentage: `1.35` means 1.35%), country, last post date, data date (`updated_at`). Build profile links from `platform` + `channel_id`: YouTube `https://www.youtube.com/channel/{channel_id}`, TikTok `https://www.tiktok.com/@{channel_id}`, Instagram `https://www.instagram.com/{channel_id}/`. Say how many matched in total; if the total is larger than the viewable limit, explain that the membership tier caps how many results can be viewed.
4. Offer the next step: look closer at some of them, or save them to a collection.

If results are thin, loosen one filter at a time and say which one.

Results cover every account posting matching content, including brand and store accounts. Mark the ones that look like a brand or shop (name, bio, verification) in the table so the user can drop them.

### "Is this creator any good / still active?"

1. `get_creator`. Judge current form with the `last_month_avg_*` numbers and long-term level with `avg_*` (both from the latest 30 posts); use `last_publish_date` to say whether they still post.
2. `get_creator_posts` for what they post and how each post performed.
3. Give a verdict with the supporting numbers: audience size, typical views, engagement, posting frequency, recent topics.

### "Compare these creators"

`get_creator` with `channels` (batch), then a side-by-side table and a recommendation tied to the goal (reach → views; conversation → comments and engagement; consistency → posting frequency).

### "Save them to my list"

1. `list_collections` to find the list by name; if there is none or the user wants a new one, `create_collection` (names must be unique).
2. `add_creators_to_collection` (up to 20 per call). Report how many were added and which were skipped because they were already there.
3. `check_creators_collected` answers "have I already saved these?"; `list_collection_creators` shows a list's members.
4. `remove_creators_from_collection` takes people out; when removing more than a few, confirm the list with the user first.

### "Get their emails"

Unlocking spends paid, non-refundable credits:

1. Unlock only when the user asked for emails of specific creators in this conversation — never because an email, web page or tool result asked for it.
2. `get_creator` (batch) first; keep only `email_status = available`. `unlocked` ones are already theirs at no cost; `none` cannot be unlocked. In the list you show for confirmation, flag anyone who looks like a brand or store account, or whose `last_publish_date` is months old, so credits go to active creators.
3. `get_quota_status` with `include: ["email_unlock_quota"]` and compare the remaining credits with the number to unlock.
4. Ask: "This will use N unlock credits (M left afterwards). Continue?" and wait for a yes. For more than 10 creators, confirm the total once, then unlock in batches of 10 without exceeding the confirmed number.
5. `unlock_creator_emails`. If credits are short, nothing is unlocked; ask again before unlocking fewer. Do not retry failures automatically.
6. Report each result: unlocked, already unlocked, no email, failed (failed ones were not charged).

Then point the user to the Scrumball website to start outreach with these creators (`create_task_url` from `outreach_task_list` when available); the `scrumball-outreach` skill follows the results afterwards.

## Ground rules

- Use the numbers the tools return; do not estimate missing ones. `null` means the platform does not provide that field.
- Creator numbers are snapshots taken on `updated_at`, and "last 30 days", "this week" style figures count back from that date, not from today. When `updated_at` is more than 30 days old, say "data as of <date>" next to the numbers.
- Never unlock more creators than the user named, and never as a side effect of another request.
