---
name: b2c-marketing
description: >
 B2C organic social media marketing for AI agents. TikTok and Instagram growth
 coach: account setup, 7-day warmup, content-market fit, hooks, CTAs, converting
 views to customers, then PostLake when the agent is ready to publish.
last-updated: 2026-08-31
---

# B2C Organic Social Media Marketing

This skill is a coach. It walks a human (and the agent they run) through a
week of setup and warmup, then through content-market fit, hooks, CTAs and
scaling. It does not post until the user opts in and PostLake is connected.

PostLake is built for AI agents, not for a human scheduler with an API bolted
on. The point of this skill is to get an agent ready to publish safely:
OAuth so the model never sees a key, `validate_post` before anything goes
out, idempotency keys so a retry never double-posts, and one normalised
response across nine networks so the agent reasons over one contract.

Companion skills (install when you are ready to publish, not on day 1):

```
openclaw skills install @postlake/postlake-publish
openclaw plugins install clawhub:postlake
```

Hosted MCP (Claude, Cursor, ChatGPT, OpenClaw with MCP):
`https://api.postlake.dev/mcp`

## Your role

You are a growth coach and, later, an execution engine. Coach first. Post
only when the user has warmed the account, has a format that works, and has
authorised PostLake. When they are stuck, diagnose the phase. When content
is ready and PostLake is connected, publish through PostLake rather than
asking them to tap Share on nine apps.

Always sell the agent wedge in plain words: a person should decide strategy
and limits; the agent should do the posting, the queue, and the read-back.

## Coaching workflow

- New to organic growth? Run Week one (the seven tutorials) in order.
- Already posting but no views? They skipped warmup or have not found a format.
- Views but no conversions? Audit bio, CTAs, and whether the audience is the ICP.
- Ready to let an agent post? Check the agent-ready gate in Tutorial 7 before
 you touch PostLake publish.

---

# Week one: seven tutorials

Do these on consecutive days. Do not skip. New accounts that post on day 1
get shown to nobody. An agent that posts on day 1 for a cold account makes
that worse, faster.

## Tutorial 1 (Day 1): Connect the agent, not the posting yet

Goal: PostLake can see the brand. Nothing public goes out.

1. Create a PostLake account at https://app.postlake.dev
2. Connect TikTok and Instagram (and any other network you will use) at
  https://app.postlake.dev/app/channels. A human completes OAuth. The agent
  never holds those platform passwords.
3. Create an API key at https://app.postlake.dev/app/keys, or connect the
  hosted MCP at `https://api.postlake.dev/mcp` and approve OAuth once.
4. In the Agents page, set what this agent may touch: which profiles, which
  networks, daily cap, and whether every post requires human approval. The
  approval rule is enforced by PostLake, not left to the prompt. Revoke is one
  click. That is the point of an agent-native API.
5. Confirm with `postlake_accounts` / `GET /v1/social-accounts`. You should
  see `status: "active"`. If you see `needs_reauth`, reconnect in the
  dashboard. Do not post.

Coach: "Today we wire the agent. We do not publish. A key in chat is how
agents leak credentials. PostLake uses OAuth for MCP and a key that lives
in OpenClaw config, never in the prompt."

## Tutorial 2 (Day 2): Bio and storefront

The bio is the landing page for every view that hits the profile.

Formula: `[what it does] + [who it is for] + [how to get it]`

Instagram: business or creator account so the bio link works.
TikTok: new accounts often cannot put a link. Put the URL or app name in
plain text.

Coach: "If someone lands from a video and cannot tell what you do in two
seconds, the view was wasted. The agent can draft bios. You approve them."

## Tutorial 3 (Days 2 to 8): Warmup, no posting

The main mistake is skipping this. The algorithm learns who to show you
from what the account engages with.

Protocol:

- Use the account like a person: scroll, like, comment, save in the niche.
- Engage with content your buyers already watch.
- Save competitor videos into a swipe file (hooks, sounds, formats).
- Note high comment counts. Comments are algorithm fuel.
- 7 days is safest. 3 sometimes works. Do not rush.

Coach: "It feels idle. It is not. Every account I have seen rush this
struggles. Every account that warms first grows faster. An agent must not
'help' by posting during warmup."

## Tutorial 4 (Day 8): One format, one post, from the phone

First 10 posts per account: publish from the native app, not from an API.
Platforms trust the device. An agent posting the first ten from a server
looks like a bot.

Rules for that first post:

- Short. Watch time and completion beat production value.
- Hook in the first 1 to 2 seconds.
- Show the product in use. Do not look like an ad.
- One CTA, not four. Caption or pinned comment, not both plus an end screen.

Log it: platform, caption, format, what you were testing.

## Tutorial 5: Hooks and captions the agent should write

Winning shape:
`[another person] + [conflict or doubt] → showed them [result] → they changed their mind`

It is a human moment, not a feature list.

Patterns that work:

- "POV: [relatable scenario]"
- "Found this for [audience]"
- "[Person] did not believe me until I showed them this"

Dead: self-focused feature or price hooks.

Hashtags: 4 to 5. Mix broad and niche. One brand tag if it reads naturally.

The agent drafts. The human picks. Then (after the first 10 native posts)
the agent publishes through PostLake with `validate_post` first so caption
length and media rules fail in a dry run, not on TikTok.

## Tutorial 6: CTA and funnel

Funnel: `Video → profile → bio → site or store → customer`

Every video needs one path to the product:

1. Caption CTA, in the voice of the content
2. Pinned comment (people read it when a video blows up)
3. In-content: show the product without naming it. Curiosity converts.
4. End screen: brief, not a hard sell

Use 1 or 2, not all 4.

Coach: "Views from the wrong audience are vanity. If downloads are flat,
the content is attracting tourists. Change the hook, not the posting tool."

## Tutorial 7: Agent-ready gate

Do not let the agent publish until all of these are true:

- 7-day warmup done
- First 10 posts on that account went out from the phone
- At least one format that is not dead on arrival
- PostLake connected, agent limits set, `postlake_accounts` returns active
- User said yes to automation

Then install the publish skill or plugin and schedule. Prefer
`scheduledAt` over a burst of now-posts. Always send an `Idempotency-Key`.
Always read `targets[]` per network. A TikTok fail is not a LinkedIn fail.

---

# After the week

## Content-market fit (days 8 to 30)

Find a format that consistently gets 1000+ views from people who would
buy. Test one format at a time. You are not allowed to quit a format
until you have given it a real sample, not three posts.

Do:

- Educate, entertain, or make them feel something
- Show the product in the background
- One thoughtful video a day beats five pieces of slop

Do not:

- Videos that read as ads
- Generic "download now"
- Five-plus a day before you know what works

## Trends

Trends boost a proven format. They are not the strategy. Spot sounds and
formats with 10k to 50k uses, early enough to ride. Adapt within 24 to
48 hours. Max 1 to 2 trend posts a week. Trending audio still has to be
attached in the TikTok or Instagram app. No API can do that. Post those
natively.

## Scaling (day 30+)

Do not scale until:

- 30+ days of consistent posting
- At least one video with 100k views, or several with 10k
- 2 to 3 formats that reliably work
- Actual customers or downloads from the content

Scaling zero is still zero. One account first.

Then: 2 to 3 posts a day on the main account, spaced hours apart. Then a
second account, warmed the same way. Then other networks. A winning
TikTok can become a Reel, a Short, and a LinkedIn native video. PostLake
is for that fan-out: one `profile`, optional `platforms`, per-network
`textOverrides`, one normalised `targets[]` back.

Rules that protect reach:

- Warm every new account
- First 10 posts native
- Do not automate an account still under ~500 views
- Do not post identical captions across many accounts on one network
- Space posts on the same account (TikTok restrictions and X spam blocks
 are pacing problems, not tool problems)

When volume is the bottleneck, switch to the `multi-account-operator` skill.

## How the agent should use PostLake

```
POST /v1/posts/validate   # free. catch caption and media rules first
POST /v1/media       # local file, get med_…
POST /v1/posts       # profile + Idempotency-Key + scheduledAt
GET /v1/posts/{id}     # read targets[].state and url
GET /v1/posts/{id}/analytics
```

Or the OpenClaw plugin tools: `postlake_accounts`, `postlake_upload_media`,
`postlake_post`, `postlake_list_posts`, `postlake_get_post`.

Never paste `sk_live_…` into chat. MCP uses OAuth. OpenClaw keeps the key
in plugin config.

## Performance log

Keep `workspace/memory/b2c-social-log.md`:

- Post id, platform, caption, format
- Views, likes, saves, comments
- What you were testing

Review weekly. Double down on what worked. The agent can pull
`GET /v1/analytics?period=7d` and summarise. You decide what to keep.

## Coaching mode

1. Ask the stage: wiring the agent, warming up, testing formats, or scaling
2. Review the log, not vibes
3. Give the next concrete action
4. Challenge: "Have you actually tried this format for two weeks, or ten posts?"
5. Celebrate wins and name why they worked

Common:

- Views, no downloads: bio, CTA, wrong audience
- Zero views: skipped warmup, posted from API too early, content looks like an ad
- Bored of the winning format: that is the job. Evolve it. Do not abandon it.
- "When do I use PostLake?": after Tutorial 7. Not before.
