---
name: "influencer-fit-analyzer"
description: "Build an influencer shortlist from a category, budget, and market, or from account links and handles you already have. This influencer analysis and creator matching workflow reads public creator profiles and recent posts on TikTok, Douyin, Xiaohongshu, Instagram, YouTube, and X, or works from bios, follower counts, and posts you paste, then writes an 8-12 person memo with followers, recent play, interaction, content pillars, and a talk-or-not call. Use it for influencer analysis, creator matching, influencer shortlist, and creator research when you need who to approach for a campaign or collab."
---

# Influencer Fit Analyzer

The job is an 8–12 person shortlist memo: followers, recent play median if looked up, interaction, content pillars, and a talk-or-not. A run that never looks anything up is a complete run — pasted bios, counts, and posts are enough.

## Scope and adjacent routes

The route is: a category or a handful of accounts, optional public reads, a shortlist. It fits when someone needs who to approach, not a diagnosis of one account and not a first post. The shortlist is the deliverable. Outreach copy and sending are not this package.

A full account diagnosis belongs in an account-teardown workflow. A produced first post belongs in that same teardown-and-build route. UGC ads and paid-social creatives belong in an ads workflow.

## Inputs and defaults

The hard inputs are the category plus a budget or follower band plus a region, or account links and @ handles the user already has. A vague "find influencers" request is not enough — ask for those fields first.

Reuse the conversation's platform, category, budget, and market. Default to eight to twelve people, one page of recent posts per person if a lookup runs, and a memo that names followers, recent play, interaction, pillars, and talk-or-not. Name those defaults instead of asking.

When the user wants creators read from a public handle or a category search, this package can look them up on TikTok, Douyin, Xiaohongshu, Instagram, YouTube, and X. Every lookup is paid, optional, and confirmed on its own before it runs, per [looking up creators](references/creator-lookup.md). If the platform has no operation in the whitelist, it has no lookup — work from what the user pasted. X has no user search here: the user must give a handle. YouTube has no channel search here: the user must give a channel URL. Without a lookup, write the shortlist from the pasted material rather than inventing follower counts or play figures.

## Golden path

The shortlist can be written at no cost from accounts the user brought. The only paid call is an optional lookup, and it happens only when the user asks for it and confirms its own price. Do not default to a profile-only lookup. Recent work and topic fit must come from content evidence, then close the memo at eight to twelve people.

**Before the memo, only when the user asks for it:** search one page of creators in a named category, or read a given handle and one page of that person's posts, per [looking up creators](references/creator-lookup.md). Skip the lookup whenever the user already pasted the bios, counts, and posts.

1. **Collect the candidates.** From the lookup payload or from what the user pasted. Keep each person attributed — looked up with its read time, or supplied.
2. **Score them** on category fit, budget band, market, recent play, and interaction, per [writing the shortlist](references/shortlist.md).
3. **Write the memo:** eight to twelve people, each with followers, recent play median if looked up, interaction, content pillars, and a talk-or-not. Offer one revision of the wording at no cost.
4. Deliver the memo. For a lookup, also deliver the task ID, terminal status, and `billing.net_charged_credits`. A lookup has no model, dimensions, or duration to report.

## Decisions that require confirmation

Confirm every lookup on its own, before it runs, without exception. Show what will be read, the operation it maps to, the credit price `beatra.social.tools.get` just returned, and how many lookups the plan contains, counting each page as one. Stopping here still leaves a usable shortlist from anything the user already pasted.

Also confirm, rather than deciding alone: a second page of posts or search results, a 60-credit Xiaohongshu profile, user search, or notes page, an Instagram Reels page after a posts page, a YouTube channel resolve then a channel read, and any change after a lookup has already run. Each changed argument is new paid work with a new request identifier and fresh approval.

A figure that was looked up is labelled as looked up, with the date it was read. A figure the user supplied stays marked as supplied. A missing count is stated as missing. Never estimate, interpolate, or carry in typical follower or play counts. Why a creator is a fit remains inference — mark it as inference and give the evidence.

## Execution

Invoke every remote Beatra tool only through the bundled `scripts/mcp_client.py`, with the tool name as the CLI argument and its arguments as JSON on standard input:

```text
printf '%s' '{"query":"creators","platform":"tiktok","capability_family":"creator"}' | python3 scripts/mcp_client.py call beatra.social.tools.search
```

Do not configure or call a host Beatra Connector, and do not use REST/OpenAPI as a fallback. Give each logical paid request one stable opaque `client_request_id` and submit it exactly once.

## Delivery and review

Deliver the 8–12 person shortlist, the followers and recent-play figures, the interaction read, the content pillars, and the talk-or-not. For a lookup, deliver the returned payload, `task_id`, terminal status, and `billing.net_charged_credits`. Do not look for a resolved model or a generated media file. Report only facts the task actually returned.

## Recovery

If the task ID is lost, list plausible tasks with `beatra.tasks.list`, inspect the match with `beatra.tasks.get`, then replay byte-identical arguments under the same `client_request_id`. Writing only the replay half authorizes a duplicate charge.

On a failed lookup, keep `error.code` and read the platform wording in `error.message`. Change arguments only when that message names a field or ID, then use a new `client_request_id`. Otherwise keep the same ID and the same payload. Do not suggest changing a model.

## References by task

- Reading a creator, their posts, or a category search, what each lookup costs, and how figures are attributed: [looking up creators](references/creator-lookup.md)
- Scoring candidates and writing the shortlist: [writing the shortlist](references/shortlist.md)
- Exact payloads, confirmation, paging, and recovery: [shortlist workflow](references/workflow.md)
- First install or expired authorization: [installation and authentication](references/installation-and-auth.md)
- Non-billable package registration: [installation registration](references/installation-registration.md)
- Task polling, artifacts, and result fields: [tasks and results](references/tasks-and-results.md)
- Balance, validation, and structured errors: [billing, errors, and recovery](references/billing-errors-and-recovery.md)
- When the bundled client cannot connect: [Bundled MCP Client diagnostics](references/mcp-connection.md)
- Updates and security: [updates and security](references/updates-and-security.md)
- Removing the package or shared credentials: [uninstall and disconnect](references/uninstall-and-disconnect.md)

## Updates and security

This Skill runs only the files installed with it and leaves them unchanged while
it runs; it never downloads or executes other code. It talks to Beatra's official
services over HTTPS, and a file you choose to upload goes only to the one-time
upload address Beatra issues for it.

Once a day at most, the bundled client reads Beatra's public version list. When
the store or tool you installed from has a newer version, it prints one line with
the command that updates it there. Updating stays your choice, through that store
or tool. See [updates and security](references/updates-and-security.md).
