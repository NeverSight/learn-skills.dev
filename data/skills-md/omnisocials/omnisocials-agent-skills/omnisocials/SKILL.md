---
name: omnisocials
description: Manage social media across 13 platforms (Instagram, Facebook, LinkedIn Profile + Page, YouTube, TikTok, X, Pinterest, Bluesky, Threads, Mastodon, Google Business, Telegram channels and groups, Discord channels). Create posts, stories, reels, upload media, organize folders, view analytics, read and reply to the social inbox (DMs, comments, mentions), set up comment-to-DM automations on Instagram and Facebook (and DM keyword automations on X), tag posts by hook or format and compare the tags in analytics, read the credit balance and choose how often X statistics are read (X statistics cost credits), look up what OmniSocials cannot do (and why) and send feature requests, and configure webhooks via the OmniSocials API.
---

# OmniSocials Skill

Create, schedule, and publish social media content across 13 platforms using OmniSocials.

OmniSocials is a social media management tool that lets you schedule posts and track analytics across Instagram, Facebook, LinkedIn (personal profile + company page), YouTube, TikTok, X (Twitter), Pinterest, Bluesky, Threads, Mastodon, Google Business, Telegram (a channel or group, posted by the OmniSocials bot), and Discord (a channel, posted through its webhook).

> **LinkedIn has two channel ids:** `linkedin` is a personal profile, `linkedin_page` is a company page. Both can be connected to one workspace and post independently. Always check `accounts:list` for which the user has connected.

## Setup

Before using this skill, ensure:

1. **API Key**: Run the setup command to configure your API key securely
   - Get your key at https://app.omnisocials.com/settings/api
   - Run: `<skill-path>/scripts/omnisocials.js setup`
   - Or set environment variable: `export OMNISOCIALS_API_KEY=omsk_live_your_key`

2. **Requirements**: Node.js 18+ (for built-in fetch API). No other dependencies needed.

Config priority (highest to lowest):
1. `OMNISOCIALS_API_KEY` environment variable
2. `./.omnisocials/config.json` (project-local, in user's working directory)
3. `~/.config/omnisocials/config.json` (user-global)

### Handling "API key not found" errors

CRITICAL: When you receive an "API key not found" error from the CLI:

1. Tell the user to run the setup command. The setup is interactive and requires user input, so you cannot run it on their behalf.
2. Stop and wait. Do not continue with the task. Wait for the user to complete setup and confirm before proceeding.

Note: All script paths in this document are relative to the skill directory where this SKILL.md file is located. Resolve them accordingly based on where the skill is installed.

## Safety Rules

IMPORTANT: Follow these rules at all times.

1. **NEVER publish a post without explicit user confirmation.** Creating a draft is safe; publishing is irreversible and goes public instantly.
2. **NEVER delete posts, media, or webhooks without explicit user confirmation.**
3. **Always list accounts first** before creating posts, to get valid channel IDs. Do not guess channel IDs.
4. **Always verify media requirements** before creating posts:
   - Stories: ALWAYS require an image or video. A story takes 1 to 10 media items; EACH item is one slide, published as its own story on Instagram/Facebook in the order given (more than 10 returns 400). Story videos are max 60s per slide. Ask the user which media and in what order.
   - Reels: ALWAYS require a video
   - Instagram posts: ALWAYS require at least one image or video
   - TikTok posts: ALWAYS require at least one image or video
   - Pinterest posts: ALWAYS require an image AND a `--pinterest-board-id`
   - Other platforms (LinkedIn Profile, LinkedIn Page, X, Facebook posts, Bluesky, Threads, Mastodon, Google Business, Telegram, Discord): Media is optional
   - **Per-platform media caps** (exceeding returns a 400 validation_error stating the exact limit): max items — X/Bluesky/Mastodon ≤4, Instagram/Threads/Telegram/Discord ≤10 (a Telegram album mixes photos and videos; a GIF goes alone; a Discord message mixes images, GIFs and videos), TikTok ≤35 photos; the same caps apply per part of a thread (4 per part on X/Bluesky/Mastodon, 10 per part on Threads). Mixing images + video in one post: allowed on Instagram/Threads (mixed carousels) and Discord, rejected on Facebook/LinkedIn/LinkedIn Page/X/Bluesky/Mastodon/TikTok (images only, or a single video). Video duration/size — **X 140s (2min 20s) / 512MB on free/Basic accounts; 125min / 16GB when the connected X account has Premium or Premium+** (tier auto-detected from the connection; reconnect X after upgrading), Bluesky 180s, Threads 5min, Instagram 15min, TikTok 10min, YouTube Short 3min; Telegram has no duration cap but takes files up to 50MB; Discord sends a video or GIF over 20MB as a link in the text instead of a file. If the user's video is over the cap, tell them the limit so they can trim it.
   - **Aspect ratio of feed images (Instagram, Pinterest)**: Instagram shows feed images between 4:5 and 1.91:1 and cuts a taller one (a 9:16 phone photo) to 4:5 itself with a blind centre crop; Meta cannot boost a feed post outside that range. By default OmniSocials crops such an image to 4:5 (tall) or 1.91:1 (wide) around the subject for the Instagram channel only and reports it; Pinterest keeps a Pin taller than 2:3 and reports that it may be cut in the home feed. Stories, reels, TikTok photos and videos are never cropped. Before posting a tall (9:16) image to Instagram, run `media:check --media-id <id>` (library images only: it prints an `Image fit` block when a channel would cut the image). When Instagram does not fit, ASK the user: "Crop to 4:5 (recommended, Meta can boost the post) or keep the original (Instagram cuts it itself, no boost)?" and pass the answer as `--media-fit instagram=crop` or `--media-fit instagram=keep` (Pinterest: `pinterest=crop` crops to 2:3). If the user gave no preference, let the default run and relay the `[image_fit]` warning the CLI prints after the post is created: what was cropped, to what, and that `posts:update <id> --media-fit instagram=keep` gives the original back. NEVER drop a channel from a post because of its image ratio; the post publishes either way.
   - **Pinterest board — auto-default to first**: If the user wants to post to Pinterest but hasn't specified a board, do NOT block on asking and do NOT skip Pinterest. Run `accounts:get <pinterest_account_id>` — its output lists each board's name and ID. Use the FIRST board automatically. After the post is created, mention to the user which board was used (e.g. "Posted to your 'Marketing' board on Pinterest — let me know if you'd prefer a different one and I'll move it."). If the user named a specific board in the request, match it case-insensitively against the list and use that one instead.
5. **No duplicate content** across posts unless explicitly requested.
6. **Always confirm timezone/datetime** with the user when scheduling posts.
7. **For bulk operations**, process one at a time and confirm between actions.
8. **Read the approval review before you report on or change a post in review.** When a post shows `approval_status: "rejected"` or `"pending"` (post `status` `rejected` or `in_approval`), run `posts:approval <id>` first. It says who decided, the reason and what the reviewers wrote. Do not guess why a post was rejected or who it waits for, and do not edit, reschedule or recreate the post before you have read the review and told the user what it says.
9. **A comment-to-DM automation sends DMs in the account's name.** Before you create one (`automations:create`, or `--dm-keywords` / `--dm-message` on a post), show the user the exact DM text and the keyword and get their confirmation; the DM goes to every person who comments the keyword, once each, and a sent DM cannot be taken back. NEVER use `--match any` (or `--dm-match any`), which answers every comment, unless the user asked for every comment. On X (`--platform x`) the automation answers the DMs people send the account (every first DM with `--match any`), OmniSocials adds "Reply STOP to stop automatic messages." under each answer, and a person who replies STOP gets no automatic DM from that account again. The Automations scopes are opt-in on the API key: a `403 insufficient_scope` means the user has to enable Automations on the key (Settings > API), not that the request was wrong.
10. **Check `limits` before you say something is not possible, and send a feature request only after the user agreed.** See "When OmniSocials cannot do something" below. A request goes to the OmniSocials team with the user's name and email. Never put the conversation, other people's personal data or secrets in its summary.
11. **X statistics cost credits: ask before you change what the organisation pays.** Before `accounts:x-statistics`, tell the user what the choice means (how often posts are checked and followers counted, and the estimate a month from `credits:get`) and get their yes. Run `analytics:refresh` (Update now) only when the user asks for fresh X numbers, and ask before you run it on many posts: each run can use credits. See "X statistics and credits" below.

## When OmniSocials cannot do something

When the user asks for something no command does, do not guess why.

1. Run `limits` first, with the platform when the request is about one: `limits --platform tiktok` (add `--area inbox` to narrow it). Each entry has a title, an `ID`, what it says and `Instead: ...`.
2. Tell the user plainly what is not possible, why, and what to do instead. Use the entry's own words. If no entry matches, say that no command does it.
3. If the user still wants it, offer to send a feature request. Name the entry: "Shall I ask the OmniSocials team for long YouTube videos?"
4. Send it only after the user says yes: `feature:request --summary "<what the user wants to do and why>" --limit-id <ID>` (add `--platform` when it is about one platform). Write the summary yourself, in one or two sentences. Never paste the conversation, and never put other people's names, emails or messages in it.
5. A platform rule ("The platform does not allow it") or a choice OmniSocials made on purpose cannot change through a request. Do not offer a request for those. If you send one anyway, the API answers `409 not_requestable` and stores nothing: tell the user the reason and what to do instead.
6. Relay the outcome: a new request, a vote added to an open request of the user's organisation, or a request the user already sent. The user sees it in OmniSocials (Settings, Request a feature) and gets an email when its status changes. `feature:list` and `feature:get <id>` show the status and the team's answer.

## Common Actions

| User says... | Action |
|---|---|
| "Post this to Instagram" | `accounts:list` to find Instagram channel ID, then `posts:create --text "..." --channels <id>` |
| "Schedule a post for tomorrow" | `posts:create --text "..." --channels <ids> --schedule "2026-04-07T09:00:00Z"` |
| "Propose a time but let me confirm it first" | `posts:create --text "..." --channels <ids> --schedule "2026-04-07T09:00:00Z" --draft`. A planned draft: it sits on the calendar at that time with a dashed outline and is not published until someone schedules it. When the user agrees: `posts:update <id> --no-draft` |
| "Show my scheduled posts" | `posts:list --status scheduled` |
| "Upload this image" | `media:upload --url "https://..."` (or `media:upload-base64 --file ./img.jpg` for a local file) |
| "Create a reel for TikTok" | `posts:create --text "..." --channels <tiktok_id> --type reel --media-urls "https://video.mp4"` |
| "Post to all platforms" | `accounts:list`, then `posts:create --text "..." --channels <all_ids>` |
| "Post a thread to X" | `posts:create --channels <x_id> --x-thread "part 1 || part 2 || part 3"` |
| "Post a thread to Bluesky" | `posts:create --channels <bluesky_id> --bluesky-thread "part 1 || part 2 || part 3"` |
| "Post a thread to Mastodon" | `posts:create --channels <mastodon_id> --mastodon-thread "part 1 || part 2 || part 3"` |
| "Post a thread to Threads" | `posts:create --channels <threads_id> --threads-thread "part 1 || part 2 || part 3"` |
| "Post to my Telegram channel" | `accounts:list` to find the Telegram channel ID, then `posts:create --text "..." --channels <telegram_id>` (add `--telegram-silent`, `--telegram-pin` or `--telegram-buttons-json` when the user asks) |
| "Run a poll in my Telegram group" | `posts:create --text "<question>" --channels <telegram_id> --telegram-poll-json '{"options":["A","B","C"],"open_period":86400}'` (no media with a poll) |
| "Post to my Discord channel" | `accounts:list` to find the Discord channel ID, then `posts:create --text "..." --channels <discord_id>` (add `--discord-silent`, `--discord-button "Shop now\|https://..."` or `--discord-allow-mentions` when the user asks; a forum or media channel needs `--discord-thread-name "<title>"`) |
| "Run a poll in my Discord server" | `posts:create --text "<question>" --channels <discord_id> --discord-poll-json '{"options":["A","B","C"],"duration_hours":24}'` (no media and no buttons with a poll) |
| "Tag a location on Instagram" | `locations:search "<place name>"`, then `posts:create ... --location-id <id>` |
| "Tag a location on Threads" | `locations:search "<place name>" --platform threads`, then `posts:create ... --threads-location-id <id>` (rolling out) |
| "Give the Threads post a topic" | `posts:create ... --threads-topic "Build in public"` (one topic per post, spaces allowed) |
| "Tag products on a Pinterest Pin" | `pinterest:products` to list the account's product Pins, then `posts:create ... --pinterest-board-id <id> --pinterest-product-tags <pin_id,pin_id>` (max 24, own product Pins only; a product Pinterest refuses never fails the post) |
| "Post a reel with music" | `audio:search "<song or artist>"` (no query = trending), then `posts:create ... --type reel --instagram-audio-id <id>` |
| "Post this tall (9:16) photo to Instagram" | `media:check --media-id <id>`; when the `Image fit` block says Instagram cuts it, ask "crop to 4:5 or keep the original?", then `posts:create ... --media-ids <id> --media-fit instagram=crop` or `instagram=keep`. Relay the `[image_fit]` warning the CLI prints |
| "How are my posts doing?" | `analytics:overview --period 7d`, or `analytics:posts <id,id,...>` for many posts at once |
| "Get the latest X numbers of that post" / "Update the X stats now" | `analytics:refresh <post-id>` (Update now; X only; half a credit a tweet, 1 for a tweet with a video or GIF, free when the post was already read today, UTC; at most 5 a post a day). Ask first when it is more than one post |
| "How many credits do I have?" / "What do my X statistics cost?" | `credits:get`: the balance, auto-refill, the credits used this month per reason, and per X account its setting and its estimate a month. Needs the opt-in `credits:read` scope and billing rights |
| "Check my X posts less often" / "X statistics cost too much" | `credits:get` for the estimate per account, tell the user what each choice means, then after their yes `accounts:x-statistics <account-id ending in _x> --posts light` (2 checks) or `--posts off`, and/or `--followers weekly` or `--followers off`. Needs the opt-in `accounts:write` scope and billing rights |
| "Tag this post as a question hook" / "Label my posts by format" | `tags:list` first and reuse a name that exists, then `posts:create ... --tags "Question hook"` on a new post, or `tags:apply --posts <id,id> --add "Question hook"` on posts that exist (published ones too, up to 500 at once). A new name becomes a tag |
| "Which hooks / formats work best?" | `analytics:tags` (add `--platform tiktok` or `--start-date` for one channel or period): per tag how its posts did against the user's normal, fair across channels. Tag older posts first with `tags:apply` when few posts carry tags |
| "Show my posts with that tag" | `posts:list --tag "Question hook"` (several: `--tag "Question hook,Tutorial"` = any of them); `analytics:overview --tag "Question hook"` for their numbers |
| "Any new DMs / comments?" | `inbox:list --unread` (add `--platform` / `--type dm\|comment\|mention` to filter; `--unanswered` for only the ones still waiting for a reply). Needs the `inbox:read` scope |
| "Work through what needs answering" / "Answer my inbox" | The `inbox:next` loop: `inbox:next` hands you the next unanswered item (DMs that can still be answered first, then Instagram/Facebook DMs whose 24-hour window has closed, then comments and mentions oldest first) with its thread, the post it is on and its `reply_window`; draft a reply from that and send it with `inbox:reply <conversation-id> --text "..." --next`, whose response already carries the next item. On a comment or mention always add `--message-id <message-id>` (the "Message to answer" id) so the reply lands under that person's comment. When `reply_window.open` is false the DM cannot be answered through the API: tell the user to answer it in the Instagram/Facebook app, or skip it with `inbox:read`. Skip one for good with `inbox:read <conversation-id>`, skip it for this call only with `--exclude <conversation-id>`. Stops when it prints "Nothing is waiting for an answer." Needs `inbox:read` (+ `inbox:write` to reply) |
| "Reply to that message" | `inbox:messages <conversation-id>` to read the thread, then `inbox:reply <conversation-id> --text "..."`. For a comment or mention add `--message-id <message-id>` (the id of the comment being answered, from `inbox:messages` or `inbox:next`): all comments on a post share one conversation and without it the reply goes under the newest comment, which may be a different person. Needs `inbox:write` |
| "Mark that conversation read" | `inbox:read <conversation-id>`. Needs `inbox:write` |
| "Hide that comment" | `inbox:hide <message-id>` (message id from `inbox:messages` or `inbox:next`; Facebook, Instagram, TikTok, YouTube, Threads; `--unhide` reverses; needs `inbox:write`) |
| "Like that comment" | `inbox:like <message-id>` (message id from `inbox:messages` or `inbox:next`; Facebook Page, LinkedIn Page and TikTok comments, liked as the Page/account; Facebook allows only Like, no Love or other reactions; `--unlike` removes it; needs `inbox:write`) |
| "Delete that comment" / "Delete my reply, it went under the wrong comment" | `inbox:delete <message-id>` (Facebook and Instagram comments, and the account's own replies on Facebook, Instagram and TikTok; a TikTok comment someone else left cannot be deleted, use `inbox:hide`; cannot be undone, so confirm with the user first; YouTube: use `inbox:hide`; needs `inbox:write`) |
| "Organize my media" | `folders:list` / `folders:create --name "..."`, then upload with `--folder-id <id>` |
| "Add my usual hashtags" | `hashtag-sets:list` to find the set, then `posts:create ... --hashtag-set "<name>"` (add `--hashtag-placement first_comment` to keep tags out of the caption) |
| "Save these hashtags for reuse" | `hashtag-sets:create --name "Brand" --tags "#a #b #c"` |
| "Send a DM to everyone who comments a keyword on this post" | Confirm the DM text and the keyword with the user first (safety rule 9). On a new post: `posts:create ... --channels <instagram_id> --dm-keywords "guide" --dm-message "Here is the guide: https://..."` (add `--dm-reply "Sent you a DM!"` for a public reply under the comment). On a post that exists: `posts:list` to find its id, then `automations:create --post-id <id> --keywords "guide" --dm "..."`; a post published outside OmniSocials takes `--instagram-media-id <id>` instead. On a Facebook Page: `--platform facebook` (the DM lands in Messenger), and `--facebook-post-id <id>` for a Page post published outside OmniSocials; on a new post that goes to both, `--dm-platforms instagram,facebook`. Read what happened with `automations:events <id>`. Needs the opt-in `automations:write` scope (`automations:read` to list and read) |
| "Answer everyone who DMs a keyword to my X account" | Confirm the DM text and the keyword with the user first (safety rule 9). `automations:create --platform x --keywords "guide" --dm "Here is the guide: https://..."` (X answers DMs only: no post, no `--reply`). It runs only while X DMs are on for the workspace: a `409 x_dms_off` means the user turns them on in the OmniSocials dashboard (Social Inbox, X DMs card, or the automation editor); add `--paused` to save it off until then and `automations:update <id> --resume` later. Each answer ends with "Reply STOP to stop automatic messages." Encrypted X Chat conversations get no answer: X does not give apps their messages |
| "Delete that post" | Confirm with user, then `posts:delete <id>` |
| "Publish my draft" | Confirm with user, then `posts:publish <id>` |
| "Retry my failed post" | `posts:list --status failed` to find it, then `posts:retry <id>` (retries only the failed platforms; check `posts:get` for the outcome). Note: `posts:publish` refuses failed posts; retry is the correct command |
| "Approve/reject that pending post" | `posts:list --status in_approval` to find it, `posts:approval <id>` to read what the reviewers wrote so far and the step it waits on ("Waiting on: step N"), then `posts:approve <id> --step-order N` or `posts:reject <id> --step-order N --comment "..."`. Only works if the connected user is a listed approver for the post's current workflow step (returns `forbidden` otherwise). A `409 step_changed` means the review moved on (or an earlier call already went through): nothing was decided; run `posts:approval <id>` again and ask the user before you decide the new step |
| "Why was my post rejected?" / "What did the reviewer say?" | `posts:list --status rejected` to find it, then `posts:approval <id>`: it prints who rejected it, on which step, the reason and the comment thread. Relay that to the user before you change anything. A rejected post will not publish; the user can edit and resubmit it in the dashboard (Edit & Resubmit on the post), or you create a corrected post with `posts:create ... --approval-workflow <id>` once the user agrees |
| "Who is my post waiting on?" / "Why has it not gone out yet?" | `posts:approval <id>`: the "Waiting on" line names the current step and the approvers who still have to decide. A post that is still `in_approval` when its scheduled time passes does not publish; it publishes at once when it is approved late |
| "I want to review posts before they go out" / "Send it to me for approval" | `approval-workflows:list` to find the workflow id, then `posts:create ... --schedule <ISO8601> --approval-workflow <id>`. The post lands as `in_approval`, the approvers are notified, and it publishes at the scheduled time once the last step approves (Approvals page in the dashboard, or `posts:approve`). If no workflow exists, tell the user to create one in the dashboard under Approvals |
| "Set up a webhook" | `webhooks:create --url "https://..." --events post.published,post.failed` |
| "Tell my system when a post is approved or rejected" | `webhooks:create --url "https://..." --events post.approved,post.rejected` |
| "Tell my system when X statistics stop because credits ran out" | `webhooks:create --url "https://..." --events x_statistics.paused,x_statistics.resumed` |
| "Can OmniSocials do X?" / the user asks for something no command does | `limits --platform <id>` (or `--area`), then tell the user what is not possible, why, and what to do instead. See "When OmniSocials cannot do something" |
| "Ask OmniSocials to build this" / "I want this feature" | After the user agreed: `feature:request --summary "<what and why>" --limit-id <ID from limits>` (`--platform` when it is about one). A platform rule is refused (`409 not_requestable`) and nothing is sent |
| "What happened to my feature request?" | `feature:list` (status and the team's answer per request), then `feature:get <id>` for the summary and every team reply |

## Workflow

Follow this workflow when creating posts:

1. **List accounts** to find available channel IDs:
   ```
   ./scripts/omnisocials.js accounts:list
   ```

2. **Upload media** if needed (required for stories, reels, Instagram, TikTok, Pinterest):
   ```
   ./scripts/omnisocials.js media:upload --url "https://example.com/image.jpg"
   ```
   Note the returned `media_id`.

3. **Create the post** with appropriate channels, media, and platform options:
   ```
   ./scripts/omnisocials.js posts:create --text "..." --channels <id1>,<id2> --media-ids <media_id>
   ```

4. **Schedule or publish** as needed:
   - Add `--schedule "2026-04-10T14:00:00Z"` to schedule
   - Add `--draft` next to `--schedule` to propose the time as a planned draft a person confirms (`posts:update <id> --no-draft` schedules it)
   - Use `posts:create-and-publish` to publish immediately
   - Or create as draft first, then `posts:publish <id>` after confirmation

## Commands Reference

### Setup & Configuration

| Command | Description |
|---|---|
| `setup` | Interactive setup - prompts for API key, validates, and saves |
| `setup --api-key <key> --global` | Non-interactive setup to global config |
| `config:show` | Show current config, API key source |

### Posts

| Command | Description |
|---|---|
| `posts:list` | List posts. Flags: `--status draft\|in_approval\|scheduled\|posting\|published\|failed\|warning\|rejected` (`in_approval` = waiting for a reviewer in an approval workflow, `rejected` = an approver declined it; both print an `Approval:` line that names `posts:approval <id>`), `--limit`, `--offset`, `--tag "<name or id,...>"` (only posts with any of these tags). Each post prints its `Tags:` and, for an Instagram Trial Reel, an `IG trial reel:` line with its graduation (`MANUAL` or `SS_PERFORMANCE`) |
| `posts:get <id>` | Get full post details, including `tags` (`[{ id, name, color }]`) and `trial_reel` (`{ strategy }` with `MANUAL` or `SS_PERFORMANCE`, or `null` when the post is not an Instagram Trial Reel; the setting only, Instagram does not say whether it was later shared with followers) |
| `posts:recent-platform` | Fetch recent posts **live** from the connected platform APIs, including content published outside OmniSocials. Use when `posts:list` is empty (brand-new workspace). Returns each post's platform-native `id` (the stable de-dupe key for storing posts), a `permalink`, the full caption, format, timestamps, normalized engagement, and every raw metric the platform exposes as an exact integer (Instagram includes reach/views/saves/shares from per-post insights; TikTok includes average_time_watched/full_video_watched_rate/total_time_watched/favorites/reach when the workspace enabled TikTok comments). Records also carry `duration_seconds` (integer, nullable): video length in whole seconds where the platform's listing API reports it — currently TikTok and YouTube; `null` for images and platforms that don't expose it (Instagram's media API has no duration field). Add `--json` for the full, untruncated captions + exact metrics + ids + permalinks (the human table truncates/rounds). LinkedIn personal profiles can't be listed live (LinkedIn grants apps no such permission), so `linkedin` results are posts published through OmniSocials with their latest collected stats; TikTok photo posts are backfilled the same way. Flags: `--limit` (1-50, default 25; X defaults to 10 unless set explicitly — its API bills per returned post), `--platforms` (comma-separated filter). X results may come from a snapshot up to 24h old, refreshed right after publishing to X through OmniSocials. Requires the `analytics:read` scope. |
| `posts:create` | Create a new post. Flags: `--text`, `--channels`, `--schedule`, `--draft` (planned draft, with `--schedule`), `--type post\|story\|reel`, `--media-ids`, `--media-urls`, `--link-url` (+`--link-title`/`--link-description`/`--link-thumbnail-url`), `--location-id`, `--collaborators`, `--user-tags`, `--x-thread`, `--bluesky-thread`, `--mastodon-thread`, `--threads-thread`, `--threads-location-id`, `--threads-topic`, `--video-cover-json`, `--tags "Question hook,Tutorial"` (post tags, see Tags), `--dm-keywords` + `--dm-message` (comment-to-DM automation bound to this post, with `--dm-reply`, `--dm-match`, `--dm-max-sends`, `--dm-stop-at`, `--dm-platforms instagram,facebook`; Instagram or Facebook must be in `--channels`; see Automations), plus platform flags |
| `posts:create-and-publish` | Create and publish immediately. Same flags as `posts:create` except `--schedule` |
| `posts:update <id>` | Update a draft or scheduled post. Same flags as `posts:create`. `--schedule` on a post pending approval (`in_approval`) moves only the time and does not change its status. `--no-draft` schedules a planned draft at the time it already carries (`400 validation_error` when it has none or it is in the past; pass a new `--schedule` then). `--draft` unschedules a scheduled post and keeps its time. The `--dm-*` flags replace the post's comment-to-DM automation (a channel left out of `--dm-platforms` loses its automation), `--no-dm` removes it. `--tags` replaces the post's tags (`--tags null` removes them); an update with only `--tags` also works on a published post |
| `posts:publish <id>` | Publish a draft/scheduled post now. Refuses posts whose status is `failed` or `warning`; use `posts:retry` for those. `409 review_required`: changes were requested on the post in its approval workflow, so it needs a new review first |
| `posts:retry <id>` | Retry the failed platforms of a failed or partially failed post; succeeded platforms are never re-published; async, max 3 retries per platform. The response means the retry is queued: poll `posts:get` for the outcome. After 3 retries on a platform the API returns `max_retries_reached` and the post must be recreated. `409 retry_in_progress`: another retry of the post runs (the dashboard or the automatic retry); nothing was queued, poll `posts:get`. Post responses carry `retry_of` (the failed post this one retries) and `retries` (retry posts created from this one); a `published` post with empty `published_urls` and `retries` set is a resolved failure whose live URLs are on the retry post |
| `posts:approve <id>` | Approve the current step of a post's approval workflow (`approval_status: "pending"`, post `status: "in_approval"`). The connected user must be a listed approver for the CURRENT step — steps approve in order, so being an approver on a later step returns `forbidden` until earlier steps clear. If this is the last step, the post finalizes immediately (`scheduled` or `posting`); otherwise it stays `in_approval` and the next step's approvers are notified. Flag: `--step-order <n>` (the step the user reviewed: "Waiting on: step n" in `posts:approval`; always pass it). When the review is on another step by then, nothing is approved and the API answers `409 step_changed` with the current step; this stops a repeated call (after a timeout) from approving the next step too. A value that is not a whole number from 1 is refused before the call |
| `posts:reject <id>` | Reject a post's approval workflow. Same approver requirement as `posts:approve`. Unlike approval, this stops the WHOLE workflow immediately (not just the current step) — the post becomes `rejected`. Flags: `--comment "..."` (optional, shown to the requester and other approvers), `--step-order <n>` (as on `posts:approve`). A rejected post cannot be scheduled or published again without a new review: `posts:update --schedule` and `posts:publish` answer `409 review_required`; create it again with `--approval-workflow` |
| `posts:approval <id>` | Read the review of a post that went through an approval workflow (read-only, `posts:read`). Prints the review `status` (`none`, `pending`, `approved`, `rejected`), the workflow, who requested it, the step the post waits on with the approvers who still have to decide, who rejected it with the reason, every step with each approver's decision, and the comment thread oldest first (a comment tagged `[instagram]`, `[linkedin_page]`, ... is about that channel only; the thread includes the entries OmniSocials writes when a reviewer edits the post). `--json` returns the full object: `post_id`, `status`, `workflow`, `requested_by`, `requested_at`, `current_step`, `steps[]` (`order`, `name`, `require_mode`, `status`, `approvers[]` with `id`, `name`, `email`, `status`, `decided_at`, `comment`), `rejection` (`by`, `reason`, `at`, `step`) and `comments[]` (`id`, `author`, `message`, `account`, `created_at`). A post without a workflow answers `status: "none"` with empty `steps` and `comments`. `404 not_found` when the post is not in this workspace. **Run it whenever a post shows `approval_status` `rejected` or `pending`, before you tell the user about it or edit the post** |
| `approval-workflows:list` | List the approval workflows this workspace can use (id, name, steps with named approvers; `workspace_id` null = company-wide). Workflows are created in the dashboard (Approvals). Pass an id to `posts:create --approval-workflow <id>` (requires `--schedule`, not allowed with `--publish-now`): the post is created as `in_approval`, approvers are notified, and it publishes at the scheduled time once the last step approves. Errors: `404 workflow_not_found`, `400 validation_error` (no `--schedule`, or the workflow has no approvers on step 1) |
| `posts:delete <id>` | Remove a post from OmniSocials (cannot be undone). Never deletes the live post on a platform. `409 post_publishing`: the post (or a retry of one of its channels) is publishing right now; poll `posts:get` until it is `published`, `warning` or `failed`, then delete. `posts:update` answers the same while the post publishes (an update with only `--tags` still works), and `409 media_processing` when a `--media-ids` file is still processing (wait until `media:list` shows it `ready`, then send the same command again) |

### Media

| Command | Description |
|---|---|
| `media:list` | List uploaded media files. Flags: `--limit`, `--offset` |
| `media:upload` | Upload media from a URL — image, video, or PDF. Flags: `--url` (required), `--filename`, `--name` (findable label), `--folder`, `--folder-id`, `--pdf-mode` |
| `media:upload-base64` | Upload a local file or base64 data (image, video, or PDF). Flags: `--file <path>` (auto-encodes + infers MIME, incl. `.pdf`) OR `--data` + `--mime-type`; plus `--filename`, `--name` (findable label), `--folder`, `--folder-id`, `--pdf-mode` |
| `--pdf-mode` | PDF uploads only. `slides` (default): one image media item per page, one ID each; pass **all** of them to `posts:create --media-ids`. `document`: ONE media item for the whole PDF (`type: document`, pages in `pdf.pages`); pass its single ID in `--media-ids` and the post gets every page in order. Both keep the original file, which LinkedIn receives. Prefer `document` when the user wants one library item for the deck. `media:list --json` shows document items as `type: "document"` |
| PDF carousels | Upload a **PDF** and it is split into one image slide per page (max 20). The response lists a media ID for every slide — pass **all** of them to `posts:create --media-ids` to post the deck as a carousel. The original file is kept (`pdf.id`, `pdf.name`, `pdf.url` in the response; each slide carries `pdf: { id, page, total_pages, ... }`). On LinkedIn the slides post as a native swipeable **document made from that original PDF** (text stays sharp, in-document links work, viewers download the real file, every page is included even past the 20-slide cap) as long as the slides are posted unchanged and in order; on Instagram, TikTok, Threads and Pinterest as an image carousel. Lets you post an existing deck (Canva/PowerPoint/Figma exported to PDF) without exporting each slide by hand. |
| `media:check` | Check whether media fits target platforms before posting. Flags: `--url`, or `--media-id`, or `--size-bytes` + `--mime`. For a library image (`--media-id`) the response also carries `file.width` / `file.height` and `fit[]`, printed as an `Image fit` block: how Instagram and Pinterest show it as a feed post (ratio, whether it fits, the crop target, the default action: `crop` on Instagram, `keep` on Pinterest) and the `--media-fit` value that overrides it. Videos and `--url` checks have no `fit` rows. Read it before posting a tall image to Instagram (Safety Rules, rule 4) |
| `media:delete <id>` | Delete a media file |

### Folders

| Command | Description |
|---|---|
| `folders:list` | List media folders (id, name, parent, item count). Use folder ids with `media:upload-base64 --folder-id`. |
| `folders:create` | Create a folder. Flags: `--name` (required), `--parent-id` (nest under another folder) |

### Hashtag sets

Saved, reusable groups of hashtags per workspace. Apply one at post-create time with `posts:create --hashtag-set "<name>"` — the tags are merged into the captions ONCE (the post stores plain text; editing the set later never changes existing posts). Tags already present in a caption are skipped, and Instagram's 30-hashtag cap fails fast with `hashtag_limit_exceeded`. Add `--hashtag-placement first_comment` to post the tags as the automatic first comment on Instagram / Facebook / LinkedIn / LinkedIn Page / YouTube instead (other channels fall back to the caption), and `--hashtag-platforms instagram,tiktok` to only tag a subset of the post's channels.

| Command | Description |
|---|---|
| `hashtag-sets:list` | List saved sets (id, name, tag count, preview). |
| `hashtag-sets:create` | Save a set. Flags: `--name` (required, unique per workspace), `--tags` (required, e.g. `"#fitness #gym workout"` — `#` optional, deduped case-insensitively, max 100) |
| `hashtag-sets:update <id>` | Rename and/or replace tags. `--tags` replaces the FULL list — pass the complete new list. |
| `hashtag-sets:delete <id>` | Delete a set. Posts that already used it keep their hashtags. |

### Tags

Tags label posts inside OmniSocials (they never go to a platform) so the user can compare what works: tag posts by hook ("Question hook", "Bold claim"), format ("Talking head", "Carousel") or series, tag older posts in bulk with `tags:apply`, then compare the tags with `analytics:tags`. A tag is one name (no groups) with a color; up to 20 tags per post and 200 per workspace. **Reuse the names from `tags:list`** before you make a new one: a near-duplicate ("Question Hook" next to "Questions") splits the numbers. Names match case-insensitively, and a name that does not exist yet becomes a tag on `posts:create`, `posts:update` and `tags:apply --add` / `--set`. Lists are comma separated; quote names with spaces (`--tags "Question hook,Tutorial"`), and repeat the flag for a name that contains a comma (`--add "Hooks, short" --add "Tutorial"`). Ids from `tags:list` work everywhere a name does. Uses the `posts:read` / `posts:write` scopes.

| Command | Description |
|---|---|
| `tags:list` | List the workspace's tags: id, name, color |
| `tags:create` | Create a tag. Flags: `--name` (required), `--color blue\|green\|orange\|red\|purple\|pink\|teal\|yellow\|brown\|gray` (optional; the API picks one) |
| `tags:update <id>` | Rename or recolor a tag; every post with it follows. Flags: `--name`, `--color` |
| `tags:delete <id>` | Delete a tag. It comes off every post (prints how many); the posts stay. Confirm with the user first |
| `tags:apply` | Change the tags of up to 500 posts at once, published ones included. Flags: `--posts <id,id>` (required), `--add "<names>"` (adds these, keeps the rest), `--remove "<names>"`, `--set "<names>"` (replaces each post's tags; `--set null` removes them all). Prints each post with its tags after the change, and the ids that are not posts of this workspace (`not_found`, left alone) |

### Automations (comment to DM)

An automation answers a keyword in an Instagram comment with a DM, once per person, with an optional public reply under the comment ("Sent you a DM!"). It can also answer a keyword in a DM or in a reply to a story (`--triggers dm,story_reply`). It listens on one post (`--post-id`, an OmniSocials post that goes to Instagram, scheduled or live; or `--instagram-media-id` for a post published outside OmniSocials), on the next Instagram post the workspace publishes (`--scope next_post`) or on every post (`--scope any`). One automation per post and platform. It also runs on a Facebook Page (`--platform facebook`): a keyword in a comment under a Page post, or in a Messenger message to the Page (`--triggers comment,dm`), gets the DM in Messenger. Facebook has no story replies, and a post published on the Page outside OmniSocials takes `--facebook-post-id <id>` (`{page-id}_{post-id}` or the post id alone). On X (`--platform x`) an automation answers a keyword in a DM to the X account (or every first DM with `--match any`), once per person: the trigger is `dm` (the default there; X allows an automated DM only after the person wrote first), with no post, no `--scope` and no `--reply`. It runs only while X DMs are on for the workspace (turned on in the dashboard: Social Inbox, X DMs card, or the automation editor); otherwise an active create or `--resume` answers `409 x_dms_off`, and `--paused` always saves. Every X answer ends with the line "Reply STOP to stop automatic messages.", and a person who replies with only STOP (or unsubscribe, opt out, cancel, end, quit) goes on the X account's stop list: no automatic DM from that account again, also after the automation is deleted, from automations made later and in every workspace with that X account (another X account still answers them; event outcome `opted_out`). X does not give apps the messages of an encrypted X Chat conversation, so those get no answer. The platform is set at create and cannot change. Meta allows one private reply per comment within 7 days, on Instagram and Facebook alike. OmniSocials sends at most 180 DMs an hour per account on Instagram and Facebook, and 15 per 15 minutes and 450 a day on X; an answer over the cap waits in a queue (outcome `queued`; also when X itself answers with its rate limit, until X's reset time) and goes out within the hour, else it is skipped as `rate_limited`. A queued answer to a person who said STOP meanwhile is skipped as `opted_out`. The scopes are opt-in on the API key: `automations:read` (list, get, events) and `automations:write` (create, update, delete, and the `--dm-*` flags on a post); without them the API answers `403 insufficient_scope` and the CLI says where to enable them (Settings > API). Follow safety rule 9: confirm the DM text and the keyword with the user before you create one.

| Command | Description |
|---|---|
| `automations:list` | List automations: id, status (`active`, `paused`, `completed` = a limit was reached), name, trigger, the post with its caption or link, and the stats (sent / matched / skipped / failed). Flags: `--status active\|paused\|completed`, `--platform instagram\|facebook\|x`, `--post-id <id>`. Each row names its platform (Instagram, Facebook Page or X) |
| `automations:get <id>` | Full detail: trigger, post, the DM text, the public reply variations, limits, stats, dates |
| `automations:create` | Create one. Flags: `--dm "<text>"` (required, max 1000 chars), `--keywords "guide,link"` (up to 20; required unless `--match any`), `--platform instagram\|facebook\|x` (default `instagram`; `x` answers DMs only), `--post-id <id>` OR `--instagram-media-id <id>` OR `--facebook-post-id <id>` (one of them is required for a comment trigger on a post; `--facebook-post-id` implies `--platform facebook`), `--reply "<text>"` (public reply under the comment; repeat the flag, or pass a comma list, for up to 10 rotating variations; a reply with a comma goes in its own flag), `--match word\|contains\|any` (default `word` = the whole word; `any` answers every comment), `--scope post\|next_post\|any` (default `post`), `--triggers comment,dm,story_reply` (default `comment`, on X `dm`; Facebook has `comment,dm` only, X has `dm` only; the public reply applies to comments only), `--max-sends <n>`, `--stop-at <ISO8601>`, `--name "..."`, `--paused` (create it off). The CLI refuses a missing `--dm`, two post flags at once, a comment trigger on a post without a post, `story_reply` on Facebook, `--instagram-media-id` with `--platform facebook` (or `--facebook-post-id` with `--platform instagram`), and on X any trigger but `dm`, a post flag, `--scope` or `--reply`, before it calls the API. Errors: `400 post_required`, `400 post_not_instagram`, `400 post_not_facebook`, `404 post_not_found`, `404 instagram_media_not_found`, `404 facebook_post_not_found`, `409 instagram_not_connected`, `409 instagram_needs_reauth`, `409 facebook_not_connected`, `409 facebook_needs_reauth`, `409 x_not_connected`, `409 x_dms_off` (X DMs are off for the workspace; the CLI says where to turn them on), `409 automation_exists` (the CLI names the existing automation) |
| `automations:update <id>` | Changes only what you pass; everything else keeps its stored value (new `--keywords` keep the triggers, the scope and the match; a new `--dm` keeps the public reply; `--stop-at` keeps `--max-sends`). Same flags as `automations:create`, plus `--pause` and `--resume`. `--keywords` is the full new keyword list. Another `--post-id` / `--instagram-media-id` / `--facebook-post-id` moves the automation to that post. The platform cannot change (`400 platform_immutable`). `--resume` on an X automation answers `409 x_dms_off` while X DMs are off for the workspace. A `completed` automation starts again when its limits or trigger change |
| `automations:delete <id>` | Delete it. Confirm with the user first. DMs that already went out stay |
| `automations:events <id>` | Activity: a counts line (sent, skipped, failed, pending, queued, opted_out over the whole automation), then one line per event with the time, the kind (comment, DM, story reply), the outcome with its reason (`already_sent`, `limit_reached`, `stopped`, `window_passed`, `rate_limited` = the send cap stayed full for an hour, `cannot_message`, `already_replied`, `dm_window_passed`, on X `dms_closed` = the person does not accept DMs from the account, `no_credits` = credits ran out before the answer (top up, then answer in the Social Inbox), `opted_out` = the person replied STOP before (also while the answer waited), `automation_off` = paused or finished while the answer waited, `plan_inactive` = the organisation has no active plan or trial, so nothing was sent (a Follow first tap gets no answer then; the person stays `waiting` and gets the link on a tap after the plan is back), or the platform's error text), `queued` (waits for a free send slot, goes out within the hour), `opted_out` (the person replied STOP on X), the person, what they wrote (a comment; a DM or story reply only when the key also has `inbox:read`) and the DM that went out. Flags: `--outcome sent\|skipped\|failed\|pending\|queued\|opted_out`, `--limit <1-100>` (default 25), `--offset` |

### Locations

| Command | Description |
|---|---|
| `locations:search "<name>"` | Search taggable locations (min 2 chars). Default `--platform instagram` searches Facebook Places and returns `location_id` values for `posts:create --location-id`. `--platform threads` searches Threads locations and returns ids for `posts:create --threads-location-id`; it also accepts `--latitude` + `--longitude` instead of a name. The two id namespaces are DIFFERENT: never pass an Instagram `location_id` as a Threads one or vice versa. Threads location search is rolling out; until Meta approves the permission the API answers `not_available`, and older Threads connections answer `threads_reauth_required` until reconnected. |

### Pinterest products

Product tags put products on a Pin, so people can shop the items in the image. A tag is the Pin ID of a product Pin of the connected Pinterest account. Pinterest accepts a product only when its Pin is public, belongs to the same Pinterest account and links to a website that account claimed; products of other merchants cannot be tagged. Pass the Pin IDs to `posts:create --pinterest-product-tags` (max 24 per Pin). Both commands need the `posts:read` scope.

| Command | Description |
|---|---|
| `pinterest:products` | List the product Pins of the connected Pinterest account. Every row starts with the `pin_id` that `--pinterest-product-tags` takes. Flags: `--source catalog\|pins`, `--product-group-id <id>`, `--bookmark <bookmark>`, `--page-size <1-100>` (default 25, catalog only). `--source catalog` reads the Pinterest catalog: rows carry price, currency, availability and the merchant's item id, and the output lists the product groups so another one can be picked with `--product-group-id`. It needs catalog access on the Pinterest connection, which the user gives one time in the OmniSocials composer (Pinterest options, Add products, Connect catalog). `--source pins` reads the account's own Pins and returns the ones Pinterest marks as product Pins; it works on every connection. Without `--source` the API uses `catalog` when the connection has catalog access, else `pins`. One `pins` call scans up to 250 Pins, so it can print "No product Pins in this batch" together with a `--bookmark` value: run it again with that bookmark until no bookmark is printed. A problem is printed as `Error [code]: message`, never as an empty list: `pinterest_not_connected` (no Pinterest account on the workspace), `pinterest_catalog_access_required` (`--source catalog` without catalog access: ask the user to connect the catalog, or use `--source pins`), `platform_error` (Pinterest did not answer or refused; the message carries Pinterest's text), `validation_error` (`--product-group-id` is not a product group of the account). `--json` returns `products[]` (`pin_id`, `title`, `description`, `link`, `image_url`, `price`, `currency`, `availability`, `item_id`; the last four are catalog only), `bookmark`, `source`, `catalog_access`, and for the catalog source `product_groups[]` and `product_group_id` |
| `pinterest:validate <pin-id-or-link>` | Check one Pin before you tag it. Takes a Pin ID or a Pin link (`https://www.pinterest.com/pin/<id>/`; `pin.it` short links do not work). Prints `Valid product Pin: <pin_id>` for a product Pin of the connected account, `Not valid (<pin_id>): <reason>` for a Pin that is not a product Pin, belongs to another account or does not exist, and `Not checked (<pin_id>): <reason>` when the check could not run (no Pinterest account, Pinterest did not answer, or Pinterest did not say if the Pin is a product Pin); the publish step is then the final check. The check does not look at the claimed-website rule; Pinterest applies that one at publish. `--json` returns `valid`, `pin_id`, `title`, `link`, `image_url`, `unverified`, `reason` |

### Audio (Instagram Reel music)

| Command | Description |
|---|---|
| `audio:search ["<song/artist>"]` | Search Meta's licensed music catalog for Instagram Reels. No query = currently trending audio; `--type original_sound` searches original sounds. Returns `audio_id` values for `posts:create --instagram-audio-id`. Only tracks licensed for third-party publishing appear (selection can differ from the IG app); needs a Facebook account connected whose Page links the Instagram account. |

### Accounts

| Command | Description |
|---|---|
| `accounts:list` | List all connected social media accounts with channel IDs, platforms, content types, and Pinterest boards. An X account also prints its X statistics setting: `X statistics: Check each post: 5 checks · Count followers: Daily`, with `(paused: credits ran out)` while the organisation's credits are at 0 |
| `accounts:get <id>` | Get full account details (JSON) including platform-specific info: Pinterest boards, the X subscription and, on an X account, `x_statistics` (`posts`, `followers`, `state`, `paused_reason`; `accounts:list` shows the same setting in the app's words) |
| `accounts:x-statistics <id>` | Change how often an X account's statistics are read. See "X statistics and credits" below |

### Analytics

| Command | Description |
|---|---|
| `analytics:post <post-id>` | Get post analytics: impressions, reach, engagements, likes, comments, shares, saves, clicks, per-platform stats (thread posts on X/Bluesky/Mastodon/Threads are summed across their parts; rates and averages are averaged). Per platform the raw `metrics` carry everything it reports: link_clicks, profile_visits, follows (follows gained from the post), reactions by type, video keys (video_views, avg_watch_time, total_watch_time, watch_time_percentage, completion_rate, skip_rate, replays, engaged_views), video retention (`hold_rate_3s` = % still watching at second 3 on TikTok videos, Facebook Reels and Instagram Reels; `retention_curve` on TikTok videos and Facebook Reels and videos, printed as a `still watching` line, full curve with `--json`; Instagram and YouTube give no curve), YouTube traffic_sources, TikTok impression_sources/audience_types, Pinterest pin_clicks/outbound_clicks, Instagram story navigation and completion. Items a platform cannot measure (Google Business posts, deleted videos) carry `metrics_unavailable: true` and a `note` instead of zeros. `reach` is absent, never 0, on X, Pinterest, YouTube, Threads, Bluesky, Mastodon, Telegram, Discord and Facebook (Meta retired Facebook post reach in June 2026; its replacement metric returns no data): sum reach only over the platforms that carry it. |
| `analytics:best-times` | Recommended posting slots (day + hour) for one platform, computed from the workspace's own posting history (recency-weighted, outlier-damped, in the account's timezone), blended with when the audience is online where the platform provides it (Instagram, TikTok Business; `basis: own_data_and_audience`, response carries `audience_online`). Top 3 slots + per-day scores. Under 15 analyzed posts it uses the audience-online profile alone (`basis: audience`) or returns clearly-labeled industry defaults with `posts_needed` — tell the user that. Use before scheduling when no time was specified. Flags: `--platform` (required), `--timezone` (IANA override). Requires `analytics:read`. |
| `analytics:posts <id,id,...>` | Get analytics for up to 100 posts in one call (bulk). Use this instead of looping `analytics:post` to avoid the rate limit. |
| `analytics:overview` | Workspace analytics overview. Flags: `--period 7d\|30d\|90d`, `--start-date YYYY-MM-DD`, `--end-date YYYY-MM-DD`, `--tag "<name or id,...>"` (only the posts with any of these tags) |
| `analytics:tags` | Compare tags (see Tags): one table, per tag the posts, the measured posts, median impressions, engagement rate, **vs normal** and the channel where it does best, then `(no tag)` for the untagged posts and the user's normal per channel. vs normal compares each post with the median impressions of its OWN channel in the period, so a tag does not win only because its posts went to the channel with the most views (+38% = 38% above the user's normal, -21% = below). `too few posts` = fewer measured posts than `--min-posts` (default 5): do not draw a conclusion from that tag, suggest tagging more posts instead. Rows come comparable first, best first. Published OmniSocials posts only (not posts made outside OmniSocials). Flags: `--start-date`, `--end-date` (default the last 90 days), `--platform` (one connected channel), `--min-posts <1-50>`. `--json` gives `tags[]` (`tag`, `posts`, `measured`, `median_impressions`, `engagement_rate` in percent, `vs_normal` as a fraction, `best_channel`, `enough_posts`), `untagged` and `normals`. Requires `analytics:read` |
| `analytics:accounts` | Account-level analytics: followers, following, posts, plus the day values the platform reports for the snapshot date (impressions/views, reach, engagement, profile_views, link_clicks, follows_gained, follows_lost; Google Business calls, direction_requests, website_clicks, average_rating, review_count; Pinterest monthly_views). Rows with day values carry `period: "daily"`. Audience objects when available: `demographics` (+ `demographics_unit`) and `online_followers` (UTC hour to followers online; Instagram and TikTok Business, 100+ followers). Flags: `--platform`, `--date YYYY-MM-DD`. **Metric scope varies by platform — read each row's `note`.** LinkedIn profiles keep a lifetime total under `impressions_lifetime` (all content ever, including posts published outside OmniSocials) and carry `period: "lifetime"` when no daily breakdown is served; never compare a lifetime total to a windowed export. A missing key means the platform does not report it (Bluesky and Mastodon have no views; YouTube day values need the YouTube Analytics scope; TikTok day values need the Business authorization). |

### X statistics and credits

X bills every read of a post's statistics, and OmniSocials passes X's price on as credits, with no markup (1 credit = €0.01). Only X works this way: the statistics of every other network stay part of the plan, and publishing an X post without a link costs nothing.

- **Prices**: half a credit a post check (each tweet of a thread counts), 1 credit for a check of a post with a video or GIF (half for the tweet, half for the video), 1 credit a follower count. A post already read today (UTC) is free to read again: X bills a post once a day.
- **The choices, per X account** (one X account per workspace). Check each post: `full` = **5 checks** (about 5 hours after publishing, day 1, 3 and 7, and day 30 for posts with 100+ views), `light` = **2 checks** (about 5 hours and day 7), `off` = **Off** (numbers read before stay; Update now still works). Count followers: **Daily** (about 30 credits a month), **Weekly** (about 4), **Off**. An account never set uses the default, **5 checks + Daily**. A change applies from the next check, also to posts already published.
- **Charging date**: reads cost credits from the date in `charging.from` of `credits:get` (the CLI prints "Charging: starts on ..."). Before it, reads are counted but nothing comes off the balance.
- **When credits run out**, X statistics pause for the whole organisation: posts still go out, no new X reads, Update now answers `402 insufficient_credits`. The checks start again by themselves after a top-up or auto-refill. `accounts:list` prints `(paused: credits ran out)`, and the webhook events `x_statistics.paused` / `x_statistics.resumed` tell a system.
- Credits are bought in the app (Settings > Organisation > Billing > Credits); the API only reads them.

| Command | Description |
|---|---|
| `accounts:x-statistics <account-id>` | Change how often an X account is read. Flags: `--posts full\|light\|off` (5 checks, 2 checks, Off), `--followers daily\|weekly\|off`; one or both, a flag left out keeps its value. X accounts only: the CLI refuses an id that does not end in `_x` before it calls the API. Prints the new setting in the app's words. Changes what the organisation pays, so tell the user what it means and ask first (safety rule 11). Needs the opt-in scope `accounts:write` (the "Credits and X statistics" switch when the key is created) and billing rights (manage_billing) for the key's creator: `403 insufficient_scope` = the key lacks the scope, `403 insufficient_permission` or `forbidden` = the creator has no billing rights (an owner or admin has them); the CLI prints which. `400 not_supported` = not an X account |
| `analytics:refresh <post-id>` | Update now: check the X numbers of one published post now, outside its schedule (any setting, also `--posts off`). Takes the numeric OmniSocials post id from `posts:list`, not a tweet id. Prints the new numbers per tweet (a thread has one line per part) and the credits used (`0` = free: already read today, UTC, or before the charging date); `analytics:post` shows them too. At most 5 reads of a post a UTC day, scheduled checks included. Errors: `402 insufficient_credits` (nothing read; add credits or turn on auto-refill), `409 refresh_not_available` (the post has no published X tweet), `429 refresh_limit` (5 today; try again after midnight UTC, this is not the rate limit), `502 refresh_failed` (X did not answer, nothing charged; try again in a few minutes). Needs `analytics:read` only |
| `credits:get` | The organisation's credit balance (whole credits, with the euro value), auto-refill on or off, the credits used this month (UTC) per reason (X statistics, X link posts, X DMs and others), and the X statistics part: the state (active, or paused since when), the charging start date, the prices, this month's reads (post checks, video or GIF reads, follower counts, Update now) and their credits, and a table of every X account with its setting, its tweets of the last 30 days and its estimate a month. Needs the opt-in scope `credits:read` (the same "Credits and X statistics" switch) and billing rights for the key's creator |

### Inbox (Social Inbox)

Read and reply to DMs, comments, and mentions across connected accounts. Every comment/mention thread carries the post it is on (`post`: id, caption, thumbnail, url, media_type); the CLI prints it above the thread so a reply can be drafted with the post in view. All comments on one post share one conversation, so a reply to a comment or mention must name the comment with `--message-id <message-id>`; without it the API posts the reply under the newest incoming comment on the post, which may be a different person. Instagram and Facebook DMs can only be answered through the API inside Meta's 24-hour messaging window (24 hours after the customer's last message): every served item carries `reply_window` (`open`, `closes_at`), and a reply to a DM whose window has closed answers `422 outside_messaging_window` without sending anything, so that DM is answered from the Instagram/Facebook app or skipped with `inbox:read`. Replies typed in the native apps (the Instagram app, Messenger) are mirrored into the inbox as outgoing messages and count as answers, so a thread a colleague answered on their phone is not served as unanswered, and a DM answered in the app after its window closed is cleared the same way. TikTok is supported for video comments only (no DMs or mentions); TikTok replies are text-only, capped at 150 characters. YouTube is supported for video comments only (no DMs or mentions); YouTube channels are checked for new comments once per day, so a new YouTube comment can take up to a day to appear. Threads is supported for replies on the user's posts (`type: comment`) and mentions (no DMs); replies publish as native Threads replies. Threads connections made before the inbox permissions were added need a one-time reconnect in the dashboard; until then Threads conversations do not appear and Threads replies/hides answer 401 `reauth_required`. Comments on the user's own posts can be hidden with `inbox:hide` on Facebook, Instagram, TikTok, YouTube (moderation status rejected) and Threads (top-level replies only), and deleted for good with `inbox:delete` on Facebook, Instagram and TikTok. Comments on Facebook Pages, LinkedIn Pages and TikTok can be liked as the Page/account with `inbox:like` (Facebook allows only Like, no other reactions); every message carries `liked`: `true` when the connected account liked it, `false` when not, `null` where the platform has no like through OmniSocials (DMs, Instagram, YouTube, X, Threads). **Requires the opt-in `inbox:read` / `inbox:write` scopes**: the user enables "Social Inbox access" when creating the API key. If a call returns `insufficient_scope`, tell the user to create a new key with Social Inbox access. `conversation_id` values can contain `:` and `()` (LinkedIn URNs); pass them exactly as returned by `inbox:list` (the CLI URL-encodes them for you). Results are cursor-paginated: when more exist, the CLI prints the `--cursor` value to fetch the next page.

**Answering the inbox (the `inbox:next` loop).** `inbox:next` returns one item that needs an answer, with the whole thread (oldest first), the post it is on and its `reply_window`, plus how many more are waiting. An item needs an answer when it is the customer's latest DM with no reply after it, or a comment/mention that has not been replied to and is not hidden. The queue is served in three groups: first DMs that can still be answered (Instagram/Facebook DMs inside Meta's 24-hour window, the one whose window closes soonest first, and X DMs, which have no window), then Instagram/Facebook DMs whose 24-hour window has closed (`reply_window.open` is false; the customer is still waiting, but the API cannot answer them: tell the user to reply from the Instagram/Facebook app, or skip the item with `inbox:read`), then comments and mentions, oldest first. `--order newest` reverses the order inside each group. Only unread items are served by default, so `inbox:read <conversation-id>` is the durable way to skip one (it will not come back); `--exclude <id,id>` leaves conversations out of a single call (temporary skip, up to 100); `--include-read` also serves items that were read but never answered. Looks back 30 days. Reply with `inbox:reply <conversation-id> --text "..." --next` and the response already carries the next item, so working through the inbox is one call per answer. On a comment or mention always add `--message-id <message-id>` with the served message id ("Message to answer"): every comment on a post shares one conversation, and without it the reply is posted under the newest comment on the post, which may be a different person than the one you drafted for. The loop ends when the CLI prints "Nothing is waiting for an answer." Two ids matter: the `conversation_id` (what `inbox:reply` / `inbox:read` take) and the message `id` of the unanswered item (what `--message-id`, `inbox:hide`, `inbox:delete` and `inbox:like` take); the CLI labels both.

| Command | Description |
|---|---|
| `inbox:list` | List conversations (latest message per conversation). Flags: `--platform instagram\|facebook\|linkedin\|tiktok\|youtube\|x\|threads`, `--type dm\|comment\|mention`, `--unread` (only conversations with unread messages), `--unanswered` (only conversations that still need an answer: the customer's latest DM with no reply after it, including Instagram/Facebook DMs whose 24-hour window has closed (they cannot be answered through the API, but the customer is still waiting; `inbox:next` flags them with `reply_window`), or an unreplied, not-hidden comment/mention; native-app replies count as answers; read state is ignored), `--limit`, `--cursor`. Shows participant, unread count, last message, and the related post for comments/mentions. Requires `inbox:read`. |
| `inbox:next` | The next conversation that needs an answer, with its thread (oldest first, every message with its id and direction), the post it is on and its `reply_window` (`{ open, closes_at }`; only Instagram/Facebook DMs have a window, everything else is `open: true, closes_at: null`), plus how many more are waiting. Served in this order: DMs that can still be answered (Meta DMs inside the 24-hour window, soonest to close first, and X DMs), then Instagram/Facebook DMs whose window has closed (`open: false`, `closes_at` says when; the CLI prints "Reply window closed ..." and tells you to answer it in the native app or skip it with `inbox:read`), then comments and mentions oldest first. The served message id is what `--message-id` takes on `inbox:reply`; the CLI prints it with that hint. Flags: `--platform`, `--type dm\|comment\|mention`, `--order oldest\|newest` (reverses the order inside each group), `--include-read` (also serve items marked read but never answered), `--exclude <conversation-id,...>` (leave these out of this call; temporary skip, max 100). Only unread items by default, so `inbox:read` is the durable skip. Looks back 30 days. Prints "Nothing is waiting for an answer." when the queue is empty. Requires `inbox:read`. |
| `inbox:messages <conversation-id>` | Full message history for one conversation, oldest to newest, each with its message id, direction, timestamp, and read/replied/hidden/liked state. Comment threads print the post block (caption, url, thumbnail) first. Flags: `--limit`, `--cursor`. Requires `inbox:read`. |
| `inbox:read <conversation-id>` | Mark a conversation's messages as read. Also the durable skip for `inbox:next` (a read conversation is not served again unless `--include-read`). Requires `inbox:write`. |
| `inbox:reply <conversation-id>` | Send a reply. Flags: `--text` (required), `--message-id <message-id>` (the inbox id of the comment or mention being answered: the "Message to answer" id from `inbox:next`, or a message id from `inbox:messages`; always pass it on comment threads, since every comment on a post shares one conversation and without it the reply is posted under the newest incoming comment, which may be a different person than the one you drafted for; ignored for DMs; `404 not_found` when it is not an incoming message of this conversation, `400 validation_error` when it is not numeric), `--attachment-url`, `--attachment-type`, `--next` (the response also carries the next conversation that needs an answer, printed like `inbox:next` including its `reply_window`, plus the remaining count). Requires `inbox:write`. A `422 outside_messaging_window` means the Instagram/Facebook DM is past Meta's 24-hour window; the API checks this before calling the platform, so nothing was sent: tell the user to answer that DM from the Instagram/Facebook app (native replies are mirrored into the inbox and clear the item) or mark the conversation read with `inbox:read` to skip it; do not retry. A `409 duplicate_reply` means this exact reply already went out to that comment or DM conversation in the last 10 minutes (an earlier call that looked slow or failed did succeed): nothing was sent again, do not retry it, continue with `inbox:next`. A `422 reply_not_allowed` means the platform refuses replies to this item for good (Facebook #1705: the comment sits on a share or boosted copy of the post, or the commenter restricts replies; YouTube: the thread's canReply is false because comments are off on the video or the comment was removed or held for review): the item is dropped from `inbox:next` automatically, tell the user, do not retry. A Threads reply needs the Threads reply permission on the connection; a 401 `reauth_required` means the user must reconnect Threads in the dashboard. |
| `inbox:hide <message-id>` | Hide a comment someone left on one of the user's posts, as the post owner (`--unhide` reverses it). Facebook, Instagram, TikTok, YouTube (hide = moderation status rejected, which also pulls its replies from public view) and Threads (incoming top-level replies only; nested replies return `not_hideable`). Takes the message `id` from `inbox:messages` or `inbox:next`, NOT the conversation id. A hidden comment no longer counts as unanswered. Errors: 403 `reconnect_required` (the account was connected without the moderation permission; reconnect it in the dashboard), 422 `cannot_hide` (Facebook does not let the Page hide this particular comment: the commenter blocked the Page, their account is deactivated or restricted, or the comment sits on a shared copy of the post; retrying never changes it, tell the user and use `inbox:read` if it should stop coming up), 502 `hide_not_applied` (Instagram only: after a hide or unhide the API reads the comment back and returns Instagram's own `hidden` state; when Instagram accepted the call but still reports the comment in the old state, the API answers this and leaves the inbox row unchanged. It happens with comments Instagram lists under "Comments from Facebook" on a reel that is also shared to Facebook: they live on Facebook and Instagram's hide does not reach them. Hide it in the Instagram or Facebook app, do not retry), 429 `quota_exceeded` (YouTube's daily quota; retry after midnight Pacific), 401 `reauth_required`, 404 `account_not_connected`, 502 `platform_error`. Requires `inbox:write`. |
| `inbox:like <message-id>` | Like a comment someone left on one of the user's posts, as the connected Page/account (`--unlike` removes the like). Facebook Page, LinkedIn Page and TikTok comments, incoming only. Facebook allows only Like: no Love or other reactions. Liking a comment that is already liked (or unliking one that is not) succeeds. Takes the message `id` from `inbox:messages` or `inbox:next`, NOT the conversation id. The response is the comment after the change: `liked` is `true` when the connected account liked it, `false` when not, `null` on platforms without a like through OmniSocials (DMs, Instagram, YouTube, X, Threads). `inbox:messages` marks a liked comment `liked`, and `inbox:next` names `inbox:like` on a comment that can be liked. Errors: 400 `unsupported_platform` (not an incoming Facebook, LinkedIn Page or TikTok comment), 403 `reconnect_required` (Facebook was connected without the comment-moderation permission; reconnect it in the dashboard), 401 `reauth_required`, 404 `not_found` / `account_not_connected`, 502 `platform_error`. Requires `inbox:write`. |
| `inbox:delete <message-id>` | Delete a comment from the platform for good: a comment someone left, or one of the account's own replies (`direction: outgoing`, for example one sent under the wrong comment). Facebook, Instagram and TikTok comments only; on TikTok only the account's own replies, because TikTok does not allow deleting comments other people left (the API answers `400 unsupported_platform`; hide those with `inbox:hide`). YouTube: use `inbox:hide` instead. Cannot be undone, so confirm with the user first. Replies under the comment go with it; the response lists them as `removed_reply_ids`. When the account's last reply under a comment is deleted, that comment counts as unanswered again and `inbox:next` serves it. Takes the message `id`, NOT the conversation id. Same error codes as `inbox:hide`. Requires `inbox:write`. |

### Webhooks

| Command | Description |
|---|---|
| `webhooks:list` | List the webhooks of the workspace and the organisation-wide ones made in the OmniSocials dashboard (`Scope: organisation`, they receive the events of every workspace). A webhook switches off by itself when the person who set it up loses access to the organisation or workspace (`Active: false`, the reason under `Last failure`); `webhooks:update <id> --active true` switches it on again |
| `webhooks:create` | Create a webhook. Flags: `--url` (required), `--events` (required, comma-separated: `post.scheduled`, `post.published`, `post.failed`, `post.approved`, `post.rejected`, `x_statistics.paused`, `x_statistics.resumed`). `x_statistics.paused` fires when the organisation's X statistics pause because its credits ran out, `x_statistics.resumed` when they run again after credits came in; their `data` is `{ workspace_id, account_id, reason }` (`insufficient_credits` / `credits_added`), one event per workspace with X. `post.approved` fires when the last step of a post's approval workflow is approved (the post moves to `scheduled`, or `posting` when its time has passed); `post.rejected` fires when an approver rejects a post. Both carry `data.approval` (`status`, `decided_by` = the approver's user id, `reason` = string or null) and an empty `targets` array; the full review is in `posts:approval <id>`. The endpoint must send its whole answer within 15 seconds and at most 1 MB; otherwise the delivery counts as failed (`last_failure.error` in `webhooks:get <id>` says which) and is retried |
| `webhooks:get <id>` | Get webhook details |
| `webhooks:update <id>` | Update webhook. Flags: `--url`, `--events`, `--active true\|false`. A `--url` on an organisation-wide webhook (`Scope: organisation`), even its current URL, moves it to the key's workspace: from then on it receives only that workspace's events (the output prints the new `Scope`). `--events` and `--active` keep it organisation-wide; to move an organisation-wide webhook to a new URL, make it again in the OmniSocials dashboard. When the webhook has Ads events after the change, `--url`, `--events` or `--active true` needs the `ads:read` scope and Ads access for the key's creator (`403 insufficient_scope` / `insufficient_permission`, nothing changed) |
| `webhooks:delete <id>` | Delete a webhook |
| `webhooks:rotate-secret <id>` | Rotate webhook signing secret (save the new secret immediately). For 24 hours each delivery also carries `X-OmniSocials-Signature-Previous`, signed with the old secret, next to `X-OmniSocials-Signature`: the endpoint can accept either signature until it uses the new secret |

### Limits and feature requests

What OmniSocials cannot do, and asking the OmniSocials team for it. No scope needed. See "When OmniSocials cannot do something" for when to use them.

| Command | Description |
|---|---|
| `limits` | What OmniSocials cannot do, why, and what to do instead, grouped by kind, platform rules first: "The platform does not allow it", "OmniSocials does not do this on purpose", "OmniSocials has not built this yet", "In beta for some accounts", "Only in the OmniSocials app", "Possible after a setup step". Each entry prints its title, platforms, `ID`, what it says and `Instead: ...`. The output ends with the kinds a request can change. Flags: `--platform` (a channel id, or `reddit` / `snapchat`), `--area posts\|media\|inbox\|analytics\|automations\|accounts\|ads\|team\|other` |
| `feature:request` | Send a feature request for the user, only after the user agreed. Flags: `--summary` (required, 10 to 1000 characters: what the user wants to do and why, written by you, no conversation and no personal data of others), `--title` (up to 120 characters; made from the summary when left out), `--platform`, `--area`, `--limit-id <ID from limits>`. Prints the outcome: a new request, the user's vote added to the organisation's open request, or a request the user already sent. A platform rule or a choice OmniSocials made on purpose answers `409 not_requestable`: nothing is sent. At most 10 requests an hour |
| `feature:list` | The user's own feature requests, newest first (up to 50): id, title, status (Open, In progress, Done, Declined), the date sent and the team's answer (the newest team reply when there is no answer) |
| `feature:get <id>` | One feature request: status, votes, where it was sent from, the summary, the team's answer and every team reply, oldest first |

### Global Flags

All commands support these flags:

| Flag | Description |
|---|---|
| `--json` | Output raw JSON response (useful for parsing) |
| `--api-key <key>` | Override API key for this command |
| `--base-url <url>` | Override API base URL |
| `--help` | Show help |

## Platform-Specific Reference

### Content Type Support Matrix

| Platform | Post | Story | Reel | Media Required |
|---|---|---|---|---|
| Instagram | Yes | Yes (1-10 slides, published in order) | Yes | Always (image or video) |
| Facebook | Yes | Yes (1-10 slides, published in order) | Yes | Optional for posts, required for stories/reels |
| LinkedIn (`linkedin`) | Yes | No | No | Optional |
| LinkedIn Page (`linkedin_page`) | Yes | No | No | Optional |
| YouTube | No | No | Yes (Shorts) | Always (video) |
| TikTok | Yes | No | Yes | Always (image or video) |
| X (Twitter) | Yes | No | No | Optional |
| Pinterest | Yes | No | No | Always (image or video + board_id) |
| Bluesky | Yes | No | No | Optional |
| Threads | Yes (single post or a 2-25 part thread via `--threads-thread`; a topic via `--threads-topic`; location tag via `--threads-location-id`; inbox replies/mentions via `inbox:*`; location tag still rolling out) | No | No | Optional |
| Mastodon | Yes | No | No | Optional |
| Google Business | Yes | No | No | Optional |
| Telegram (`telegram`, a channel or group) | Yes (text, photos, videos, GIFs, files, albums of 2-10, native polls) | No | No (Telegram has no reels; a reel that names `telegram` is still accepted and Telegram gets the video as a normal post) | Optional |
| Discord (`discord`, one channel, posted through its webhook) | Yes (text, up to 10 images, GIFs and videos in one message, native polls, link buttons) | No | No (Discord has no reels; a reel that names `discord` is still accepted and Discord gets the video as a normal message) | Optional |

### Platform-Specific Flags

#### Pinterest
| Flag | Description |
|---|---|
| `--pinterest-board-id` | **Required** for Pinterest. Get board IDs from `accounts:get <pinterest_account_id>` |
| `--pinterest-title` | Pin title |
| `--pinterest-link` | Link URL attached to the pin |
| `--pinterest-video-cover` | Cover image URL for a video pin |
| `--pinterest-alt-text` | Alt text for the pin |
| `--pinterest-product-tags` | Products to tag on the Pin: a comma-separated list of Pin IDs (from `pinterest:products`) or Pin links (`https://www.pinterest.com/pin/<id>/`), max 24. Sent as `pinterest.product_tags` |

Product tags (`--pinterest-product-tags`):
- **Max 24 products per Pin.** More than 24, or an entry that is not a Pin ID or Pin link, answers `400 validation_error`.
- **Own products only.** Pinterest accepts a product only when its Pin is public, belongs to the same Pinterest account and links to a website that account claimed. Products of other merchants cannot be tagged.
- **A refused product never fails the post.** The tags are added right after the Pin is published. When Pinterest refuses one product, the Pin stays live and the other products are still tagged.
- **Read the outcome after publishing.** A published post that had tags carries `pinterest.product_tags_result`: `requested` (number sent), `tagged` (Pin IDs on the Pin), `skipped` (`pin_id` + `reason` for each product that was not tagged) and `error` (set when the tag request itself failed, for example Pinterest was down; `tagged` is then empty). `posts:list` prints it as `Pinterest products: 1 of 2 tagged (skipped: <pin_id> PIN_IS_PRIVATE)` and `posts:get` shows the full object. Reason codes: `PIN_MISSING` (Pin not found), `PIN_IS_PRIVATE`, `PRODUCT_METADATA_MISSING` (not a product Pin), `PIN_NOT_FROM_VERIFIED_DOMAIN` (the product link is not on a claimed website), `PIN_NOT_FROM_SAME_USER_AS_HERO_PIN` (Pin of another account). Tell the user which products were skipped and why.
- **On `posts:update` the Pinterest flags replace the stored Pinterest options as one object.** Pass every Pinterest flag the post needs again, `--pinterest-board-id` included. Leaving `--pinterest-product-tags` out of that update removes the tags.
- `posts:get` returns the stored tags as Pin ID strings in `pinterest.product_tags` (a Pin link is stored as its Pin ID).

#### YouTube (Shorts)
| Flag | Description |
|---|---|
| `--youtube-title` | Video title |
| `--youtube-privacy` | Privacy: `public`, `private`, or `unlisted` |
| `--youtube-tags` | Tags (comma-separated) |
| `--youtube-category-id` | YouTube category ID |
| `--youtube-made-for-kids` | Made for kids flag |

A custom thumbnail for a Short goes through `--video-cover-json` (see **Video cover**). YouTube shows it on Shorts only on channels where it has enabled custom Shorts thumbnails (Partner Program channels first); other channels show a frame from the video.

#### Instagram
| Flag | Description |
|---|---|
| `--instagram-share-to-feed` | Share reel to feed |
| `--instagram-cover-url` | Reel cover image URL (with `--instagram-thumbnail-type from-library`) |
| `--instagram-thumbnail-type` | Thumbnail type: `from-video` or `from-library` |
| `--instagram-thumb-offset` | Reel cover frame timestamp in **milliseconds** from the video start (e.g. `3000` = 0:03; with `--instagram-thumbnail-type from-video`). `posts:get` reads it back |
| `--instagram-audio-id` | Licensed music for the reel — an `audio_id` from `audio:search`. **Reels only** (Meta's API can't add music to feed posts/carousels/stories). Needs a Facebook account connected whose Page links this Instagram account. |
| `--instagram-audio-volume` | Music volume 0–100 (default 100). Only with `--instagram-audio-id` |
| `--instagram-video-volume` | Video's own audio volume 0–100 (default 100; `0` = music-only reel) |
| `--instagram-trial-reel` | Publish the reel as a **Trial Reel** — shown to non-followers first to test performance. ONLY use when the user explicitly asks for a Trial Reel. **Reels only.** Not available on every account: Instagram requires roughly 1,000+ followers and enables the feature per account; ineligible accounts fail at publish with a clear error. |
| `--instagram-trial-graduation-strategy` | How a Trial Reel graduates to all followers: `MANUAL` (default — the user decides in the Instagram app) or `SS_PERFORMANCE` (Instagram shares it automatically if it performs well). Only with `--instagram-trial-reel` |

Feed image ratio (`--media-fit instagram=crop|keep`, a top-level flag, not an `--instagram-*` one): Instagram accepts a feed image from 9:16 to 1.91:1 but shows only 4:5 to 1.91:1 and cuts a taller image to 4:5 itself; Meta cannot boost a feed post outside that range. Without the flag OmniSocials crops a tall or wide image to 4:5 / 1.91:1 around the subject for the Instagram channel only (the other channels keep the original) and prints an `[image_fit]` warning with the crop URL after the post is created. `instagram=keep` sends the original (Instagram then cuts it, no boost). `posts:update <id> --media-fit instagram=keep` gives the original back on a draft or scheduled post; `instagram=crop` crops a kept image. Ratios outside 9:16 to 1.91:1 are still a `400 validation_error`. See **Per-Platform Media** and Safety Rules, rule 4.

#### Auto first comment (Instagram, Facebook, LinkedIn, YouTube, TikTok, Telegram)
Posts the given text as the first comment automatically, right after the post publishes. Common for keeping hashtags or a link out of the main caption. One flag per channel, so you can set a different first comment per platform in the same call. Not posted for stories.

| Flag | Description |
|---|---|
| `--instagram-first-comment` | First comment on the Instagram post/reel (max 2200 chars) |
| `--facebook-first-comment` | First comment on the Facebook post. **Page posts only** (the API cannot comment on personal profiles) |
| `--linkedin-first-comment` | First comment on the LinkedIn profile post (max 1250 chars). Handy for "link in first comment" |
| `--linkedin-page-first-comment` | First comment on the LinkedIn company page post (max 1250 chars) |
| `--youtube-first-comment` | First comment on the YouTube video (max 10000 chars). The video must allow comments |
| `--telegram-first-comment` | A silent reply under the Telegram post in the same chat (max 4096 chars) |
| `--tiktok-first-comment` | First comment on the TikTok video (max 150 chars). Needs **comments enabled** on the TikTok channel card (a second TikTok authorization); otherwise the post publishes and `first_comment_result.status` is `failed` with an explanatory error. Video must be public and allow comments. If TikTok returns the final video id a few minutes after publish, the comment posts automatically once it resolves (`first_comment_result.pending` is true meanwhile) |

#### LinkedIn multi-image style
By default a LinkedIn post with 2+ images publishes as LinkedIn's swipeable **PDF document carousel** (the images are rendered into a single PDF document server-side). These flags opt a channel out of that, into a plain multi-image gallery instead. Independent per channel; ignored for 0-1 images, videos, and polls.

| Flag | Description |
|---|---|
| `--linkedin-carousel-as-images` | `true` = the profile post's images publish as a plain image gallery. On `posts:update`, `false` reverts to the document carousel; omitted keeps the current value |
| `--linkedin-page-carousel-as-images` | Same for the company page post |

#### LinkedIn document source (original PDF)
When a channel's images are exactly the rendered pages of one uploaded PDF, in order and unchanged, LinkedIn receives the **kept original PDF file** as the document by default (sharp text, working in-document links, the real download, every page even past the 20-slide cap). These flags opt a channel out of that, into a document rebuilt from the slide images (a flattened copy). Ignored when the images are not a PDF's pages, when `--linkedin-carousel-as-images` is true, and for 0-1 images, videos and polls.

| Flag | Description |
|---|---|
| `--linkedin-document-source` | `original_pdf` (default) or `slides`. On `posts:update`, `original_pdf` reverts to the default; omitted keeps the current value |
| `--linkedin-page-document-source` | Same for the company page post |

#### LinkedIn poll
Non-sponsored poll (LinkedIn's Poll API) — a question with 2-4 answer options and a duration, **independent per channel**: `linkedin` (personal profile) and `linkedin_page` (company page) can each carry their own poll, or none. Mutually exclusive with media and a link share on that channel's post: if the channel's post also has media/a link, the poll silently wins at publish time, so don't combine them.

| Flag | Description |
|---|---|
| `--linkedin-poll-json` | Full `linkedin_poll` JSON object keyed by channel: `{"linkedin": {"question": "...", "options": ["...", "..."], "duration": "ONE_DAY\|THREE_DAYS\|SEVEN_DAYS\|FOURTEEN_DAYS"}, "linkedin_page": {...}}`. Each poll's `question` max 140 chars; `options` needs 2-4 entries, each max 30 chars. Omit a channel's key (or set it to `null`) to leave that channel a normal post. |

Also works on `posts:update <id>` — the stored `linkedin_poll` object is replaced wholesale (both channels), so send the full desired state. Set a channel's key to `null` (or pass `--linkedin-poll-json 'null'` for the whole flag) to clear that channel's poll and revert it to a normal post.

```bash
# Same poll on the profile only
omnisocials posts:create \
  --content "What should we build next?" \
  --accounts your-linkedin-account-id \
  --linkedin-poll-json '{"linkedin":{"question":"What should we build next?","options":["Mobile app","Public API","More integrations"],"duration":"SEVEN_DAYS"}}'

# A DIFFERENT poll on the profile and the page in one call
omnisocials posts:create \
  --content "What should we build next?" \
  --accounts your-linkedin-profile-account-id,your-linkedin-page-account-id \
  --linkedin-poll-json '{"linkedin":{"question":"What should WE build?","options":["A","B"],"duration":"SEVEN_DAYS"},"linkedin_page":{"question":"What should our COMPANY build?","options":["A","B","C"],"duration":"FOURTEEN_DAYS"}}'
```

#### Video cover
The thumbnail of a post whose media is **one video** (feed video or reel). One object for every platform that takes a cover: Instagram, Facebook, LinkedIn Profile and Page, TikTok, Pinterest and YouTube Shorts.

| Flag | Description |
|---|---|
| `--video-cover-json` | Full `video_cover` JSON object: `{"type": "frame", "thumb_offset": 3000}` (milliseconds into the video) or `{"type": "custom", "cover_url": "https://..."}` (JPEG/PNG), plus an optional `"overrides"` object keyed by platform (`instagram`, `facebook`, `linkedin`, `linkedin_page`, `tiktok`, `pinterest`, `youtube`) that wins over the base cover for that platform |

- **TikTok only takes a frame.** A `custom` cover is skipped there, so add `"overrides": {"tiktok": {"type": "frame", "thumb_offset": 2000}}` when the user wants a specific TikTok frame.
- **YouTube Shorts: depends on the channel.** YouTube shows the cover on Shorts only on channels where it has enabled custom Shorts thumbnails (rolling out since July 2026, Partner Program channels first). On other channels YouTube stores it but displays a frame from the video. Say that it depends on the channel; do not promise it.
- The older per-platform flags (`--instagram-cover-url`, `--instagram-thumb-offset`, `--tiktok-video-cover-timestamp-ms`, `--pinterest-video-cover`) keep working and win over the base cover for their platform.
- On `posts:update <id>` the stored cover is replaced wholesale; pass `--video-cover-json null` to remove it. `posts:get` returns it as `video_cover`.

```bash
# One custom cover everywhere, a chosen frame on TikTok
omnisocials posts:create \
  --text "New tutorial" \
  --channels <instagram_id>,<facebook_id>,<tiktok_id> \
  --type reel \
  --media-urls "https://example.com/video.mp4" \
  --video-cover-json '{"type":"custom","cover_url":"https://example.com/cover.jpg","overrides":{"tiktok":{"type":"frame","thumb_offset":2000}}}'
```

#### TikTok
| Flag | Description |
|---|---|
| `--tiktok-title` | Photo carousels only. The title TikTok shows above the caption on Photo Mode posts (max 90 chars). TikTok takes the title and the caption as separate fields; the caption comes from `--text`. Ignored on video posts. `posts:get` returns it as `tiktok.title` |
| `--tiktok-privacy` | Privacy: `PUBLIC_TO_EVERYONE`, `MUTUAL_FOLLOW_FRIENDS`, `FOLLOWER_OF_CREATOR`, `SELF_ONLY` |
| `--tiktok-disable-comment` | Disable comments |
| `--tiktok-disable-duet` | Disable duets |
| `--tiktok-disable-stitch` | Disable stitches |
| `--tiktok-video-cover-timestamp-ms` | Video only. Timestamp (ms) of the frame to use as the cover |
| `--tiktok-is-aigc` | Mark as AI-generated content |
| `--tiktok-brand-content-toggle` | Paid partnership promoting a third-party brand |
| `--tiktok-brand-organic-toggle` | Promoting your own business / brand |
| `--tiktok-auto-add-music` | Photo carousels only. TikTok auto-selects a soundtrack |

#### Google Business Profile
| Flag | Description |
|---|---|
| `--google-business-cta-action` | CTA button under the post: `LEARN_MORE`, `BOOK`, `ORDER`, `SHOP`, `SIGN_UP`, `CALL`. **GBP captions reject inline links and phone numbers** — the CTA button is the ONLY way to attach either, so when the user wants a link on a Google Business post, use this |
| `--google-business-cta-url` | CTA target URL, `http(s)://`. Required for every action except `CALL` (which uses the location's phone number from the business profile) |
| `--google-business-topic-type` | Post type: `STANDARD` (default), `EVENT`, `OFFER` |
| `--google-business-json` | Full `google_business` JSON object for the EVENT/OFFER shapes (`event.title` + `event.schedule` with Google's split `{year,month,day}`/`{hours,minutes}` dates, required for EVENT and OFFER: on an offer it is the offer's name and validity period; `offer.couponCode`/`redeemOnlineUrl`/`termsConditions`). Merged over the other `--google-business-*` flags |

All four also work on `posts:update <id>` to add or change the CTA on a draft/scheduled post (the stored `google_business` object is replaced wholesale, so send the full shape).

#### X (Twitter)
| Flag | Description |
|---|---|
| `--x-reply-settings` | Who can reply: `following` or `mentionedUsers` (empty string = everyone) |
| `--x-poll-json` | A poll on the X post, the text is the question: `{"options":["A","B"],"duration_minutes":1440}` (2 to 4 options of up to 25 chars; 5 to 10080 minutes, default 1440). No media on X together with a poll; on a thread the poll goes on the first tweet. `null` on `posts:update` removes it. |
| `--threads-poll-json` | A poll on the Threads post: `{"options":["A","B"]}` (2 to 4 options of 1 to 25 chars). Threads closes it after 24 hours. Text-only post. `null` on `posts:update` removes it. |
| `--mastodon-poll-json` | A poll on the Mastodon status: `{"options":["A","B"],"expires_in":86400,"multiple":false,"hide_totals":false}` (limits come from the instance; default 4 options of 50 chars, 5 minutes to 1 month). No media with a poll. `null` on `posts:update` removes it. |
| `--x-thread "a \|\| b \|\| c"` | Post a thread. Parts are split on `\|\|` (2–25 parts). For per-tweet media, build the post with `--json` and a full `x.thread_parts` array instead. |
| `--bluesky-thread "a \|\| b \|\| c"` | Post a Bluesky thread. Parts are split on `\|\|` (2–25 parts, each ≤ 300 chars). Links, mentions and hashtags become clickable automatically. For per-post media, build the post with `--json` and a full `bluesky.thread_parts` array instead. |
| `--mastodon-thread "a \|\| b \|\| c"` | Post a Mastodon thread. Parts are split on `\|\|` (2–25 parts, each ≤ 500 chars). Each toot replies to the previous one natively. For per-toot media, build the post with `--json` and a full `mastodon.thread_parts` array instead. |
| `--threads-thread "a \|\| b \|\| c"` | Post a Threads (Meta) thread. Parts are split on `\|\|` (2–25 parts, each ≤ 500 chars). Each part is published as a reply to the previous one from the same account; the first part is the post caption. For per-part media (up to 10 items per part, images and videos mixed, `{url, alt}` entries allowed), build the post with `--json` and a full `threads.thread_parts` array instead. On `posts:update`, `threads.thread_parts: null` turns the thread back into a single post. Needs the Threads reply permission: accounts connected before it was added must be reconnected once in the OmniSocials dashboard (the API answers 400 naming the reconnect). |
| `--threads-location-id <id>` | Tag a location on the Threads post. Takes a Threads location id from `locations:search --platform threads` (NOT a Facebook Place ID; never reuse `--location-id` values). On a multi-post thread the tag goes on the first post. On `posts:update`, pass the literal value `null` to remove the tag. Rolling out: needs the Threads location permission (`threads_location_tagging`), which Meta has not approved yet; until then the API returns a 400 saying location tagging is not available yet. Once enabled, older connections must be reconnected once in the OmniSocials dashboard. |
| `--threads-topic "<topic>"` | The topic of the Threads post, sent as `threads.topic_tag`: one per post, for example `"Build in public"`. Unlike a #tag in the text, a topic can hold spaces. 1 to 50 characters, no period (`.`) and no ampersand (`&`); a leading `#` is dropped. The CLI refuses a longer topic or one with `.` or `&` before it calls the API. On a multi-post thread the topic goes on the first post. On `posts:update`, pass the literal value `null` to remove it. `posts:list` prints it as `Threads topic: ...`, and `posts:get` returns it as `threads.topic_tag`. |

#### Telegram
The workspace connects one Telegram channel or group in the OmniSocials dashboard (the OmniSocials bot becomes an admin that posts). In a channel a post shows as the channel; in a group it shows as the bot. Text up to 4,096 chars; with media, text over 1,024 chars is sent as a reply under the media (the CLI and API do that for you). No Stories. Telegram gives bots no view counts: `analytics:post` shows reactions (`likes` = all reactions, `reactions` per emoji) and poll votes.

| Flag | Description |
|---|---|
| `--telegram-silent` | Send without a notification sound |
| `--telegram-link-preview false` | Hide the link preview of a text-only post (shown by default) |
| `--telegram-pin` | Pin the post in the chat. Needs the bot's Edit messages right in a channel (Pin messages in a group); without it the post is still sent and `posts:get` shows `pin_error: no_right` |
| `--telegram-protect` | Stop forwarding and saving of the post |
| `--telegram-spoiler` | Blur the photos and videos until someone taps them |
| `--telegram-caption-above` | Show the text above the media |
| `--telegram-buttons-json '<json>'` | Up to 3 link buttons, one per row: `[{"text":"Shop now","url":"https://..."}]` (label 1-64 chars, link `https://`, `http://` or `tg://`). Not on an album (2+ media) or a poll. `null` on `posts:update` removes them |
| `--telegram-poll-json '<json>'` | A native poll, the text is the question (max 300 chars): `{"options":["A","B"],"open_period":86400,"multiple":false}` (2-12 options of up to 100 chars; 5 to 2628000 seconds, leave it out to keep the poll open). No media and no buttons with a poll. `null` on `posts:update` removes it |
| `--telegram-first-comment` | A silent reply under the post (max 4096 chars) |
| `--telegram-json '<json>'` | The full `telegram` object, merged over the flags. On `posts:update` every key merges into the stored options and a key set to `null` removes it |

A published post's `posts:get --json` carries `telegram.result` (`message_ids`, `pinned`, `pin_error`, `link_public` / `link_private`). Removing a post from Telegram works only in the first 48 hours (a Telegram rule), from the post in the OmniSocials dashboard; `posts:delete` removes it from OmniSocials only.

#### Discord
The workspace connects one Discord channel in the OmniSocials dashboard (Continue with Discord, or a pasted webhook URL); OmniSocials posts through that channel's incoming webhook, so a post shows the webhook's name and picture as the sender (change them in Discord, Server Settings > Integrations > Webhooks). `accounts:list` prints the server name (a pasted webhook URL gives none: then the webhook's name) and the channel link. Text up to 2,000 chars. Up to 10 images, GIFs and videos in one message, mixed; a video or GIF over 20MB is sent as a link in the text instead of a file. No Stories and no reels: send a video as a post (a reel that names `discord` is still accepted and goes as one video message). Discord gives no view counts: `analytics:post` shows reactions (`likes` = all reactions, `reactions` per emoji) and poll votes.

| Flag | Description |
|---|---|
| `--discord-silent` | Send without a push or desktop notification (Discord's @silent) |
| `--discord-no-link-preview` | Hide the link previews (shown by default) |
| `--discord-allow-mentions` | Let @everyone, @here, role and user mentions in the text ping. Off by default: they show as text and ping nobody |
| `--discord-spoiler` | Blur every image and video until someone clicks it |
| `--discord-thread-name "<title>"` | The post title in a forum or media channel (1-100 chars). Required there; on a text channel the post goes out without it. `null` on `posts:update` removes it |
| `--discord-button "text\|url"` | A link button: label 1-80 chars, link `https://` or `http://`. Repeat the flag for more, max 5 in one row. Split on the first `\|`; the CLI refuses an entry without a `\|`, a label or a link. Not with a poll. Remove them on `posts:update` with `--discord-json '{"buttons":null}'` |
| `--discord-poll-json '<json>'` | A native poll, the text is the question (max 300 chars): `{"options":["A","B"],"duration_hours":24,"multiple":false}` (2-10 options of up to 55 chars, all different; 1 to 768 hours, default 24). No media and no buttons with a poll. `null` on `posts:update` removes it |
| `--discord-json '<json>'` | The full `discord` object, merged over the flags. On `posts:update` every key merges into the stored options, a key set to `null` removes it, and `null` removes every Discord option |

A published post's `posts:get --json` carries `discord.result` (`webhook_id`, `guild_id`, `channel_id`, `thread_id`, `message_id`, `url`, `sent_at`, `video_links` = the files sent as a link, `warnings`), and `published_urls.discord` is the message link (`https://discord.com/channels/<server>/<channel or thread>/<message>`). `posts:list` prints `Discord: sent · <link>`, plus `1 video sent as a link` when a file went as a link.

#### Link preview (LinkedIn / Facebook)
| Flag | Description |
|---|---|
| `--link-url` | URL to attach as a link-preview card |
| `--link-title` | Override the preview title |
| `--link-description` | Override the preview description |
| `--link-thumbnail-url` | Override the preview thumbnail image |

#### Instagram place tag & people tags
| Flag | Description |
|---|---|
| `--location-id` | Facebook Place ID to tag (find one with `locations:search`) |
| `--collaborators` | Up to 3 public Instagram usernames invited as co-authors (comma-separated) |
| `--user-tags` | JSON array of photo tags: `[{"username":"name","x":0.5,"y":0.5,"image_index":0}]` (x/y are 0–1 from top-left) |

### Per-Platform Media

Media can be the same across all platforms or different per platform:

**Same media for all platforms:**
```
./scripts/omnisocials.js posts:create --text "..." --channels <ig>,<li> --media-urls "https://example.com/photo.jpg"
```

**Different media per platform** (use `--json` flag and API directly for per-platform media objects):
The API supports `media_urls` as an object: `{ "default": ["url1"], "instagram": ["url2"], "pinterest": ["url3"] }`. The `default` key is the fallback for platforms without their own key. Pass an empty array to opt a platform out of media.

**Image fit per channel (`--media-fit`):** a feed image whose ratio is outside what a channel shows uncropped is cropped or kept per channel. `--media-fit instagram=keep,pinterest=crop` sets it (`<channel>=<auto|crop|keep>`, comma-separated; sent as the top-level `media_fit` object). Defaults (`auto`): Instagram crops a 9:16 image to 4:5 (a wide one to 1.91:1) around the image's focus point, because Instagram cuts it to that window anyway and Meta cannot boost a feed post outside 4:5 to 1.91:1; Pinterest keeps a Pin taller than 2:3 and reports that the home feed may cut it (`pinterest=crop` crops to 2:3). The crop is a file of its own for that channel only; `default` and every other channel keep the original. Feed posts only: stories, reels, TikTok photos and videos are never touched, and X, LinkedIn, Mastodon and Google Business show a tall image whole, so they have no rule. Every decision is printed as a `[image_fit]` warning after `posts:create`, `posts:create-and-publish` and `posts:update` (action `cropped` with the crop URL, `kept`, or `crop_failed` = the original was sent and the platform cuts it itself); `--json` carries the same `warnings` array next to `data`. `posts:update <id> --media-fit instagram=keep` alone re-decides the stored images and gives the original back; `posts:get --json` shows `fit` and `crop: { of, id, ratio, focus }` on the channel's media item. The focus point is set in the dashboard only; for your own crop, pass a different file for that channel through the per-platform `media_urls` object (above). Check first with `media:check --media-id <id>` (see Media).

**PDF by URL:** a PDF passed via `--media-urls` (or `media_urls` in the API) is rasterized into one image slide per page (max 20, in order) and the original file is kept — on LinkedIn it publishes as a swipeable document made from that original PDF, elsewhere as an image carousel. Same behaviour as uploading the PDF via `media:upload`.

**Alt text (accessibility descriptions):** any `media_urls` entry can be an object `{ "url": "...", "alt": "..." }` (and any `media_ids` entry `{ "id": "...", "alt": "..." }`, including thread-part media) instead of a bare string — max 1500 chars. Delivered to Mastodon (media description — the Mastodon community strongly values alt text), Bluesky (embed alt), X (photos/GIFs only, clamped to 1000), Pinterest (fallback for `pinterest.alt_text`), Instagram (`alt_text` on image posts and carousel image slides; not Reels/Stories; clamped to 1000), LinkedIn (`altText` on images only, single and multi-image; not video/documents), and Threads (`alt_text` on every image and video, including carousel items and thread parts); other platforms ignore it. The `--media-urls` flag takes bare URLs only, so call the API directly for alt entries, e.g. a Mastodon post: `{"content": {"default": "Morning ride 🐘"}, "accounts": ["<mastodon_id>"], "media_urls": [{"url": "https://example.com/bike.jpg", "alt": "A red bicycle leaning against a brick wall"}]}`. `posts:get --json` reads alt back on each media item.

## Examples

### List connected accounts
```
./scripts/omnisocials.js accounts:list
```

### Create a text post to LinkedIn and X
```
./scripts/omnisocials.js posts:create --text "Excited to announce our new feature!" --channels <linkedin_id>,<x_id>
```

### Create an Instagram reel with cover image
```
./scripts/omnisocials.js posts:create --text "Check this out" --channels <instagram_id> --type reel --media-urls "https://example.com/video.mp4" --instagram-share-to-feed --instagram-cover-url "https://example.com/cover.jpg"
```

### Reel with hashtags and a link in the auto first comment
```
./scripts/omnisocials.js posts:create --text "New drop is live" --channels <instagram_id> --type reel --media-urls "https://example.com/reel.mp4" --instagram-first-comment "#reels #newdrop #marketing
link: https://example.com/shop"
```

### Schedule a post for next week
```
./scripts/omnisocials.js posts:create --text "Happy Monday!" --channels <id1>,<id2> --schedule "2026-04-13T09:00:00Z"
```

### Create a Pinterest pin
```
./scripts/omnisocials.js posts:create --text "Beautiful design inspiration" --channels <pinterest_id> --media-urls "https://example.com/pin.jpg" --pinterest-board-id <board_id> --pinterest-title "Design Inspiration" --pinterest-link "https://example.com"
```

### Tag products on a Pinterest pin
```
./scripts/omnisocials.js pinterest:products
# Returns: pin_id: 813744226420795884  Blue ribbed top  (24.99 EUR, IN_STOCK, item TOP-BLUE-M)
# Optional: check one Pin ID or Pin link first with pinterest:validate 813744226420795884

./scripts/omnisocials.js posts:create --text "Autumn outfit" --channels <pinterest_id> --media-urls "https://example.com/outfit.jpg" --pinterest-board-id <board_id> --pinterest-product-tags 813744226420795884,813744226420795885
```
Max 24 products per Pin, and only product Pins of the connected Pinterest account. A product that Pinterest refuses does not fail the post: after publishing, `posts:list` prints `Pinterest products: 1 of 2 tagged (skipped: <pin_id> <reason>)`.

### Send a DM to everyone who comments a keyword (comment to DM)
```
# A new post with its automation (Instagram must be in --channels). Confirm the DM text and the keyword with the user first
./scripts/omnisocials.js posts:create --text "Comment GUIDE for the free checklist" --channels <instagram_id> --media-urls "https://example.com/photo.jpg" --schedule "2026-10-12T09:00:00Z" --dm-keywords "guide" --dm-message "Here is the checklist: https://example.com/guide" --dm-reply "Sent you a DM!"
# Prints: Comment-to-DM: on (keywords: guide; id 100000006). It starts listening once the post is live on Instagram

# An automation on a post that exists (posts:list for the id; a post published outside OmniSocials takes --instagram-media-id)
./scripts/omnisocials.js automations:create --post-id 83778183 --keywords "guide,link" --dm "Here is the guide: https://example.com/guide" --reply "Sent you a DM!" --reply "Check your inbox" --max-sends 500

# The same on a Facebook Page: a post published on the Page outside OmniSocials; the DM lands in Messenger (no story replies on Facebook)
./scripts/omnisocials.js automations:create --platform facebook --facebook-post-id 104857600_123456789 --keywords "guide" --dm "Here is the guide: https://example.com/guide" --reply "Sent you a DM!"

# On X: a keyword in a DM to the X account (no post, no public reply). --paused saves it while X DMs are still off
./scripts/omnisocials.js automations:create --platform x --keywords "guide" --dm "Here is the guide: https://example.com/guide" --paused
# Once X DMs are on for the workspace (Social Inbox, X DMs card): automations:update <id> --resume

# What happened: who commented, who got the DM, and why someone was skipped
./scripts/omnisocials.js automations:events 100000004
# Prints: Counts: 12 sent, 3 skipped, then one line per event:
# 2026-10-10T21:40:00.000Z  comment  sent  @jane  "guide please"  DM: "Here is the guide: ..."
```
Pause it with `automations:update <id> --pause`, change the keywords with `--keywords "<full list>"`, remove a post's automation with `posts:update <post_id> --no-dm`. Needs the opt-in `automations:read` / `automations:write` scopes on the key.

### Compare hooks with tags
```
./scripts/omnisocials.js tags:list
# Reuse these names. Tag older posts in bulk (published ones too, up to 500 per call):
./scripts/omnisocials.js tags:apply --posts 1024,1025,1031 --add "Question hook"
./scripts/omnisocials.js tags:apply --posts 1040,1041 --add "Bold claim"
# Tag a new post as you create it (a new name becomes a tag):
./scripts/omnisocials.js posts:create --text "Why do most hooks fail?" --channels <tiktok_id> --media-urls "https://example.com/hook.mp4" --tags "Question hook,Talking head"
# Then compare:
./scripts/omnisocials.js analytics:tags --start-date 2026-08-01
# Tag            Posts  Measured  Median impr.  Eng. rate  vs normal      Best on
# Question hook     12        10          4211       5.4%  +38%           tiktok
# Bold claim         3         3          2100       2.9%  too few posts  -
```
Relay "too few posts" as "not enough tagged posts to tell yet", not as a result.

### Upload media and create a post with it
```
./scripts/omnisocials.js media:upload --url "https://example.com/photo.jpg"
# Returns: ID: media_abc123

./scripts/omnisocials.js posts:create --text "New photo!" --channels <id> --media-ids media_abc123
```

### Create a YouTube Short
```
./scripts/omnisocials.js posts:create --text "Quick tip" --channels <youtube_id> --type reel --media-urls "https://example.com/short.mp4" --youtube-title "Quick Tip #1" --youtube-privacy public --youtube-tags "tips,tutorial"
```

### Create a TikTok video
```
./scripts/omnisocials.js posts:create --text "Watch this" --channels <tiktok_id> --type reel --media-urls "https://example.com/video.mp4" --tiktok-privacy PUBLIC_TO_EVERYONE
```

### Post an X thread
```
./scripts/omnisocials.js posts:create --text "Kicking off a thread" --channels <x_id> --x-thread "First point || Second point || Wrapping up"
```

### Post a Bluesky thread
```
./scripts/omnisocials.js posts:create --channels <bluesky_id> --bluesky-thread "First point || Second point || Wrapping up"
```

### Post a Mastodon thread
```
./scripts/omnisocials.js posts:create --channels <mastodon_id> --mastodon-thread "First point || Second point || Wrapping up"
```

### Post a Threads thread
```
./scripts/omnisocials.js posts:create --channels <threads_id> --threads-thread "First point || Second point || Wrapping up"
```

### Post to a Telegram channel with a button, pinned and silent
```
./scripts/omnisocials.js posts:create --text "The new collection is live." --channels <telegram_id> --media-urls "https://example.com/collection.jpg" --telegram-silent --telegram-pin --telegram-buttons-json '[{"text":"Shop now","url":"https://example.com/shop"}]'
```

### Run a poll in a Telegram group
```
./scripts/omnisocials.js posts:create --text "Which day suits the live Q&A?" --channels <telegram_id> --telegram-poll-json '{"options":["Tuesday","Thursday","Saturday"],"open_period":86400}'
```

### Post to a Discord channel with a button, without a notification
```
./scripts/omnisocials.js posts:create --text "The spring drop is live." --channels <discord_id> --media-urls "https://example.com/drop.jpg" --discord-silent --discord-button "Shop now|https://example.com/shop"
```

### Run a poll in a Discord server
```
./scripts/omnisocials.js posts:create --text "Which day suits the community call?" --channels <discord_id> --discord-poll-json '{"options":["Tuesday","Thursday","Saturday"],"duration_hours":48}'
```

### Tag an Instagram location
```
./scripts/omnisocials.js locations:search "Blue Bottle Coffee"
# Returns: location_id: 1234567890  Blue Bottle Coffee  — 1 Ferry Building, San Francisco

./scripts/omnisocials.js posts:create --text "Coffee time" --channels <instagram_id> --media-urls "https://example.com/photo.jpg" --location-id 1234567890
```

### Tag a Threads location (rolling out)
```
./scripts/omnisocials.js locations:search "Griffith Observatory" --platform threads
# Returns: threads.location_id: 17841400000000000  Griffith Observatory  (2800 E Observatory Rd, Los Angeles, United States)
# Coordinates also work: locations:search --platform threads --latitude 34.1184 --longitude -118.3004

./scripts/omnisocials.js posts:create --text "Best view in the city" --channels <threads_id> --threads-location-id 17841400000000000
./scripts/omnisocials.js posts:create --text "Week 12 of building in public: we shipped topics." --channels <threads_id> --threads-topic "Build in public"
```

### Upload a local file into a folder
```
./scripts/omnisocials.js folders:create --name "Summer Campaign"
# Returns: ID: 42

./scripts/omnisocials.js media:upload-base64 --file ./promo.jpg --name "summer-hero" --folder-id 42
```

### Bulk analytics for many posts (one request)
```
./scripts/omnisocials.js analytics:posts 1024,1025,1026
```

### X statistics: what they cost, check less often, Update now
```
./scripts/omnisocials.js credits:get
# Balance: 412 credits (€4.12) ... X statistics: State: active
# Charging: starts on 12 November 2026; until then reads are counted, nothing comes off the balance
# Account              Check each post  Count followers  Tweets (30 days)  Credits a month
# @yourbrand (1234_x)  5 checks         Daily                          20             72.9
# Tell the user what the choices mean. Only after they agree:
./scripts/omnisocials.js accounts:x-statistics 1234_x --posts light --followers weekly
# X statistics changed: @yourbrand (1234_x)
# Check each post: 2 checks
# Count followers: Weekly
# Fresh numbers for one X post now (half a credit a tweet; free when it was read today, UTC):
./scripts/omnisocials.js analytics:refresh 9123
```

### Triage the social inbox and reply
```
./scripts/omnisocials.js inbox:list --unread --platform instagram
# Returns each conversation with its Conversation: <conversation_id>
./scripts/omnisocials.js inbox:list --unanswered
# Only the conversations still waiting for a reply

./scripts/omnisocials.js inbox:messages "<conversation_id>"
# Comment threads print the post (caption, url, thumbnail) first; every message prints its id
./scripts/omnisocials.js inbox:reply "<conversation_id>" --text "Thanks so much for the kind words!" --message-id "<message_id>"
# --message-id = the id of the comment being answered (all comments on a post share one
# conversation; without it the reply goes under the newest comment); leave it out on a DM
./scripts/omnisocials.js inbox:read "<conversation_id>"

# Hide a comment on your own post (Facebook, Instagram, TikTok, YouTube, Threads),
# using the message id printed by inbox:messages or inbox:next (not the conversation id)
./scripts/omnisocials.js inbox:hide "<message_id>"
./scripts/omnisocials.js inbox:hide "<message_id>" --unhide

# Like a comment as the Page/account (Facebook, LinkedIn Page, TikTok; Facebook: Like only)
./scripts/omnisocials.js inbox:like "<message_id>"
./scripts/omnisocials.js inbox:like "<message_id>" --unlike

# Delete a comment for good (Facebook, Instagram, TikTok; cannot be undone, confirm with the user first)
./scripts/omnisocials.js inbox:delete "<message_id>"
```

### Answer everything that is waiting (the inbox:next loop)
```
./scripts/omnisocials.js inbox:next
# Prints the next unanswered item (DMs that can still be answered first, then Instagram/Facebook
# DMs whose 24-hour window has closed, then comments oldest first): the conversation id, the
# message id to answer, its reply window, the post it is on, the thread oldest first, and
# "N more waiting"

# Reply and get the next item in the same call; repeat until the CLI prints
# "Nothing is waiting for an answer." On a comment or mention always pass --message-id
# with the "Message to answer" id; leave it out on a DM
./scripts/omnisocials.js inbox:reply "<conversation_id>" --text "Sent you a DM with the details!" --message-id "<message_id>" --next

# Skip one for good (marking it read means inbox:next will not serve it again). Also how to
# skip an Instagram/Facebook DM whose reply window is closed ("Reply window closed ..." in the
# output): the API cannot answer it, so reply from the app (that clears it too) or mark it read
./scripts/omnisocials.js inbox:read "<conversation_id>"
# Skip some for this call only
./scripts/omnisocials.js inbox:next --exclude "<conversation_id>,<conversation_id>"
# Narrow the queue, or also take items that were read but never answered
./scripts/omnisocials.js inbox:next --platform instagram --type comment
./scripts/omnisocials.js inbox:next --include-read --order newest
```

### Audit a brand-new workspace's existing content (nothing posted via OmniSocials yet)
```
./scripts/omnisocials.js posts:recent-platform --limit 25
./scripts/omnisocials.js posts:recent-platform --platforms instagram,tiktok --json
```

### Post to a LinkedIn company page
```
./scripts/omnisocials.js posts:create --text "Company update" --channels linkedin_page
```

### View scheduled posts as JSON
```
./scripts/omnisocials.js posts:list --status scheduled --json
```

### Get analytics for the last 30 days
```
./scripts/omnisocials.js analytics:overview --period 30d
```

### Get analytics for a specific date range
```
./scripts/omnisocials.js analytics:overview --start-date 2026-03-01 --end-date 2026-03-31
```

### Find out why a post was rejected, or who it waits for
```
./scripts/omnisocials.js posts:list --status rejected
./scripts/omnisocials.js posts:approval 123456
```
Prints `Rejected by: Jordan on step 2`, `Reason: ...`, every step with its approvers, and the reviewers' comments. For a post that is still in review (`posts:list --status in_approval`) the same command prints `Waiting on: step 2 (Client approval): Jordan`. Tell the user what the review says before you edit the post or create a new one.

### Create a webhook for post notifications
```
./scripts/omnisocials.js webhooks:create --url "https://yoursite.com/webhook" --events post.published,post.failed
```

### When something is not possible
```
./scripts/omnisocials.js limits --platform youtube
# OmniSocials has not built this yet (can be requested)
#   Long YouTube videos, community posts and playlists [YouTube]
#     ID: youtube.long_videos
#     OmniSocials publishes YouTube Shorts only, up to 3 minutes. ...
#     Instead: Upload long videos in YouTube Studio.
# Tell the user this. Only when the user still wants it and says yes:
./scripts/omnisocials.js feature:request --summary "Publish long YouTube videos, not only Shorts, so the whole channel runs from OmniSocials." --platform youtube --limit-id youtube.long_videos
# Feature request sent to the OmniSocials team: #41 "Long YouTube videos".
./scripts/omnisocials.js feature:list
```

### Setup (interactive)
```
./scripts/omnisocials.js setup
```

### Setup (non-interactive)
```
./scripts/omnisocials.js setup --api-key omsk_live_xxx --global
```

## Error Handling

### Common Errors

| Error | Cause | Fix |
|---|---|---|
| `API key not found` | No API key configured | Run `setup` or set `OMNISOCIALS_API_KEY` |
| `unauthorized` / `invalid_api_key` | Invalid or expired API key | Check key at Settings > API |
| `insufficient_scope` | API key missing required scope | Create a new key with needed scopes. On `automations:*` or the `--dm-*` post flags: Automations is opt-in on the key, enable it under Settings > API (adds `automations:read` and `automations:write`) |
| `rate_limit_exceeded` | Too many requests (100/min limit) | Wait and retry after the reset time |
| `validation_error` | Missing required fields or invalid data | Check required media/fields for the platform |
| `not_found` | Resource doesn't exist | Verify the ID is correct |
| `max_retries_reached` | A platform on this post already failed 3 retries | Recreate the post with `posts:create` |
| `pinterest_not_connected` | `pinterest:products` on a workspace without a Pinterest account | Ask the user to connect Pinterest in the dashboard |
| `pinterest_catalog_access_required` | `pinterest:products --source catalog` on a connection without catalog access | Ask the user to connect the catalog (composer, Pinterest options, Add products, Connect catalog), or run `pinterest:products --source pins` |
| `automation_exists` | The post already has a comment-to-DM automation on that platform (one per post and platform) | Change it with `automations:update <id>` (the CLI prints the id), or delete it first |
| `post_required` / `post_not_instagram` | A comment automation on a post without `--post-id` / `--instagram-media-id`, or on a post that does not go to Instagram | Pass a post that has Instagram in its channels, or use `--scope next_post` / `--scope any` |
| `post_not_facebook` / `facebook_post_not_found` | A Facebook automation on an OmniSocials post that does not go to Facebook, or a `--facebook-post-id` that is not a post of the connected Page | Pass a post that has Facebook in its channels, or a post id of the connected Page |
| `facebook_not_connected` / `facebook_needs_reauth` | No Facebook Page is connected in the workspace, or its connection expired | Connect or reconnect the Facebook Page in the OmniSocials dashboard |
| `platform_immutable` | `automations:update` named another platform than the automation's | Create a new automation on the other platform |
| `x_dms_off` | An active X automation (create, or `--resume`) while X DMs are off for the workspace | Ask the user to turn on X DMs in the OmniSocials dashboard (Social Inbox, X DMs card, or the automation editor), or create it with `--paused` and resume it later |
| `x_not_connected` | `automations:create --platform x` on a workspace without an X account | Ask the user to connect X in the dashboard |
| `tag_not_found` | `--tag` names a tag that does not exist (a filter never makes one), or an id is not a tag of this workspace | Run `tags:list` and use a name or id from it |
| `instagram_not_connected` / `instagram_needs_reauth` | No Instagram account in the workspace, or its connection expired | Ask the user to connect or reconnect Instagram in the dashboard |
| `not_requestable` | `feature:request --limit-id` names a platform rule or a choice OmniSocials made on purpose. Nothing was sent | Tell the user why it is not possible and what to do instead (the CLI prints both). Do not send it again |
| `unknown_limit` | `--limit-id` is not an entry of `limits` | Run `limits` for the ids, or leave out `--limit-id` |
| `invalid_summary` / `invalid_title` | The summary is not 10 to 1000 characters, or the title is over 120 | Write a summary of one or two sentences |
| `too_many_requests` | More than 10 feature requests in an hour | Wait. Do not send it again right away |
| `insufficient_scope` on `accounts:x-statistics` / `credits:get` | The key lacks the opt-in `accounts:write` / `credits:read` scope | The user creates a new key with "Credits and X statistics" switched on (Settings > API); the person who creates it needs billing rights |
| `insufficient_permission` / `forbidden` on `accounts:x-statistics` / `credits:get` | The person who created the key has no billing rights (manage_billing) | An owner or admin makes the change, or creates the key |
| `not_supported` | `accounts:x-statistics` on an account that is not X | Use the X account id (ends in `_x`) from `accounts:list` |
| `insufficient_credits` | `analytics:refresh`: the credit balance does not cover the read. Nothing was read | The user adds credits (Settings > Organisation > Billing > Credits) or turns on auto-refill |
| `refresh_not_available` | `analytics:refresh` on a post with no published X tweet | Update now is for X posts only; `analytics:post <id>` shows the other networks |
| `refresh_limit` | `analytics:refresh`: the post was read 5 times today (UTC, scheduled checks included), or the organisation used its 100 Update now checks today | Try again after midnight UTC. Not the rate limit |
| `refresh_failed` | `analytics:refresh`: X did not answer. Nothing was charged | Try again in a few minutes |

### Rate Limits

The API allows 100 requests per minute per API key. Response headers include:
- `X-RateLimit-Limit`: Max requests per window
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Unix timestamp when the window resets

## Tips

- **Always start with `accounts:list`** to discover channel IDs and platform capabilities
- **Use `--json`** when you need to parse the output programmatically
- **Check content types**: Use `accounts:list` to see what content types each account supports (post, story, reel)
- **Pinterest boards**: Run `accounts:get <pinterest_id>` to see available boards and their IDs
- **Pinterest product tags**: Run `pinterest:products` to get product Pin IDs for `--pinterest-product-tags` (max 24, own product Pins only)
- **Comment to DM**: an automation made with a post (`--dm-keywords` + `--dm-message`) starts once the post is live on its channel (Instagram, or Facebook with `--dm-platforms`); `automations:events <id>` shows every comment it answered or skipped. X automations (`automations:create --platform x`) answer DMs only, never a post
- **Tags**: reuse the names from `tags:list`; tag older posts with `tags:apply` before you compare them with `analytics:tags`
- **X statistics cost credits**: `credits:get` shows the estimate per X account; change it with `accounts:x-statistics` only after the user agreed, and run `analytics:refresh` only when the user asks for fresh X numbers
- **Not possible?** Run `limits --platform <id>` before you tell the user something cannot be done; offer `feature:request` only when the user still wants it, and send it after they agree
- **Scheduling**: Use ISO 8601 format for dates (e.g., `2026-04-10T14:00:00Z`)
- **Media upload**: Supports JPEG, PNG, GIF, WebP images, MP4, MOV, AVI videos and PDFs (100 MB per upload; up to 1 GB from a public URL with `media:upload`)
- **Draft first**: When unsure, create as draft (no `--schedule`), review, then publish with `posts:publish`. To propose a time without publishing, use `--schedule` with `--draft` (a planned draft) and let the user confirm with `posts:update <id> --no-draft`
