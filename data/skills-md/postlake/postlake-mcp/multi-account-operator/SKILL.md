---
name: multi-account-operator
description: >
 Multi-account social media operator for AI agents. Run 15 to 400+ accounts
 without burning them: spacing, per-account caption variation, reading PostLake
 targets[] instead of one vague error, restrictions vs real failures, agent
 guardrails. For operators already posting, not a first account.
last-updated: 2026-08-31
---

# Multi-Account Social Media Operator

For people (and agents) running many accounts: agencies, portfolios, niche
networks. This is not a growth coach. It assumes you already know what to
post. The bottleneck is throughput and account health.

PostLake is the social API built for AI agents. The operator loop is what
it was designed for: one hosted MCP or one plugin, OAuth so the model never
sees a key, idempotency so a retrying agent never double-posts, and every
network answering in the same `targets[]` shape so the agent can decide
"wait" vs "fix" without nine SDKs.

Install:

```
openclaw plugins install clawhub:postlake
openclaw skills install @postlake/postlake-publish
```

MCP: `https://api.postlake.dev/mcp`

## Your role

Be an operator, not a strategist. Do not offer content ideas unless asked.

Route:

- A batch to publish → Bulk publishing
- "Some posts failed" → Reading results, then Restriction vs failure
- "An account stopped" → Recovery
- "Should we add more accounts?" → Agent limits and pacing

## Diagnose first: platform restrictions vs real failures

**A platform restriction is the platform's decision about that account.**
TikTok temporary spam limits, X 403 spam blocks, YouTube daily upload
quota, Bluesky rate limits. You cannot fix these in PostLake. Reconnecting
wastes time. Pause that account's queue, wait, then post less often.

**A real failure is something you can act on.** Dead token
(`needs_reauth`), unknown media, wrong media type, missing Pinterest
board, YouTube missing title. These have a `fix` on the target error.
Follow it.

Getting this backwards is the biggest time sink. An agent that retries a
TikTok restriction 200 times is not being helpful. It is burning the
account. Idempotency keys stop double-posts. They do not stop a stubborn
retry loop against a restriction. Cap retries. Read `targets[].error`.

### What usually fails, and what to do

**TikTok.** Temporary restriction. Wait 24 to 48 hours. Confirm in the
TikTok app under Settings > Account > Account status. Post that account
from the phone for a few days if it does not lift. Then lower cadence.
`validate_post` before schedule so photo vs video rules fail in a dry run.

**YouTube.** Daily upload quota per channel. Spread across channels and
days. Image sent to YouTube fails: videos only. Set
`platformOptions.youtube.title`.

**X.** Spam block from posting too fast, too repetitive, or link-heavy.
Slow down. Vary `textOverrides.x`. X is the only PostLake network where
publishing costs extra credits. On a free plan an X target returns
`entitlement_exceeded` and the other networks still go out. Do not treat
that as a total failure. Separately, sending a direct message on X costs
6 credits.

**Instagram / Facebook / Threads.** Token expiry is the common one.
`status: "needs_reauth"` on `GET /v1/social-accounts`. Human reconnects
at https://app.postlake.dev/app/channels. Transient Meta 500s sometimes
publish anyway. Check the live post before the agent republishes.

**Pinterest.** Needs a `boardId` in `platformOptions.pinterest`. Media
must actually exist. `validate_post` catches this.

**Bluesky.** Rate limits: slow down. Unconfirmed email blocks uploads:
confirm in Bluesky first.

**LinkedIn.** Usually a dead token. Reconnect.

## Bulk publishing

Prefer a PostLake **profile** (a named brand) over a bag of `acc_…` ids.
The agent addresses `profile: "acme"`, optionally `platforms: ["tiktok","instagram"]`.

```
POST /v1/posts/validate   # free preflight
POST /v1/media       # local file → med_…
POST /v1/posts
 Idempotency-Key: <unique per logical post>
 { "text": "...", "profile": "acme", "media": ["med_…"], "scheduledAt": "..." }
GET /v1/posts/{id}     # targets[].state, url, error
```

OpenClaw plugin: `postlake_accounts`, `postlake_upload_media`,
`postlake_post`, `postlake_list_posts`, `postlake_get_post`.

Rules at volume:

- Space posts on the same account. Bunching is what triggers TikTok and X.
- Vary captions per account and per network (`textOverrides`). Identical
 text across many accounts is what spam classifiers look for.
- Spread YouTube across channels and days.
- Always send a new idempotency key per logical post. Reuse the same key
 only when retrying the same post after a transport blip.
- List the scheduled queue (`GET /v1/posts?state=scheduled`) before adding
 more. The agent should see the calendar, not guess.

## Reading results, per network

There is no single pass or fail for a fan-out post. PostLake returns one
row per network on purpose so an agent can reason.

```
GET /v1/posts/{id}
```

`targets[].state` is `published`, `processing`, `failed`, or `scheduled`.
TikTok and YouTube often stay `processing`. Poll. Do not assume failure.

One network failing does not stop the others. Read that target's `error`
against the table above before acting. Most of the time the answer is
wait, not fix.

## Recovery

**Dead token.** Reconnect in the dashboard. Do not disconnect if posts are
already scheduled to that account.

**Spam restriction.** Wait. Then reduce frequency. Do not let the agent
keep firing.

**Media rejected.** Re-encode. `validate_post` names the rule. Use
`GET /v1/platforms/{network}` for limits before composing.

**Agent over its daily cap.** That is working as designed. Raise the cap
on the Agents page, or wait until tomorrow. Do not work around it.

## Agent guardrails (use them)

PostLake is optimised for agents that will retry, hallucinate a caption,
or post to the wrong brand. Set this before volume:

- Allowed profiles (the agent cannot see other clients)
- Allowed networks
- Daily post cap
- OAuth connect for MCP, or a key that never enters the chat
- Revoke on the Agents page when a run goes wrong

If those are unset, stop and set them. Throughput without a leash is how
you wake up to 40 posts on the wrong brand.

## Scriptable end to end

Nothing here needs a browser after channels are connected. MCP, the
OpenClaw plugin, and REST hit the same API. A cron or an agent can:
validate, upload, schedule across a profile, read `targets[]`, and alert
only on accounts that need a human.

Docs: https://docs.postlake.dev
MCP: https://api.postlake.dev/mcp
Keys: https://app.postlake.dev/app/keys

## What this does not do

Say it early:

- No client approval queues and no client-facing reporting
- No unified inbox in this skill. Use the `postlake-inbox` skill or the hosted
 MCP tools for Facebook, Instagram, X, and Bluesky DMs. Meta can push inbound
 message webhooks; X and Bluesky require polling. This operator skill is for
 publish health.
- Scheduled posts cannot attach trending TikTok or Instagram audio. That
 lives in those apps. Post those natively.
