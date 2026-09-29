---
name: slack-ai-bot
description: >
  Build a two-way Slack AI bot inside a Next.js App Router app with the Chat SDK
  and the AI SDK: people mention or DM the bot and an LLM answers with tools
  scoped to their app account, the app posts reports into channels on its own,
  and risky actions wait behind Approve / Cancel buttons whose clicks come back
  to the app. Use when: (1) adding a Slack assistant that answers questions
  about a product's data and runs actions for the asking user, (2) the app must
  push messages to Slack and react to button clicks (human-in-the-loop approval,
  draft-then-send), (3) auditing an existing Slack bot that misses follow-ups,
  answers twice, or cannot identify users, (4) the user mentions: Slack bot, AI
  Slack assistant, two-way Slack, @mention bot, app_mention, thread follow-up,
  onSubscribedMessage, Slack interactivity, block_actions, Approve button,
  Block Kit buttons, response_url, Slack OAuth install, users:read.email,
  x-slack-signature, "bot stops replying in threads", "couldn't match your Slack
  account", "operation timed out" on a Slack button. Carries the identity
  bridge from Slack email to app user, user-scoped tools, the single-claim
  approval that survives double clicks, the 3-second ack rule, serverless state
  traps, and a Markdown to mrkdwn converter, with 31 tests. Next.js App Router
  on Vercel or any Node host; stores, auth, model and domain tools are seams.
  Not a Chat SDK API reference and not a Slack channel reader.
---

# Slack AI bot with two-way communication

A Slack bot that talks in both directions. **Inbound**: a person mentions the
bot, DMs it, or replies in a thread it follows, and an LLM answers with tools
that act as that person. **Outbound**: the app posts into Slack on its own
schedule. **Round trip**: the app posts buttons, a human clicks, the click comes
back as a webhook and runs a side effect exactly once.

The insight that shapes the module: **Slack is an untrusted, stateless, retrying
client, and the model is an untrusted caller.** Every id the model passes is user
input. Every webhook may arrive twice, on a cold instance, with three seconds to
answer. The hard parts are identity, scoping, acknowledgement and idempotency;
the chat loop itself is twenty lines.

Written by the engineer who has shipped this module, audited against the Slack
assistant of a Next.js 16 product on Vercel and Supabase. The templates hold
what such a bot must: every answer scoped to the asker, one side effect per
approved click, both webhooks acked inside three seconds, and a failure the
person can see. [provenance.md](references/provenance.md) has the record.

## When to use

- A product needs a Slack assistant that answers from the user's own data.
- The app must start conversations: reports, alerts, drafts for review.
- An action is too risky to let a model fire: send email, publish, pay, delete.
- An existing bot loses thread follow-ups, double-sends, or fails identity.

## When NOT to use

- **Learning the Chat SDK (cards, modals, slash commands, other platforms) or the
  AI SDK (models, streaming, tool calling)**: the `chat-sdk` and `ai-sdk` skills.
- **Reading channel history as a data source**: a separate module.
- **One-way notifications only**: an incoming webhook URL. No bot needed.

## Architecture

```
  Slack  --app_mention / message.im / message.channels-->  POST /api/slack/events
    ^                                                        |  verify, dedupe, ack
    |                                                        v  after(): handlers.ts
    |   streamed reply <-- streamText + tools(userId) <-- identity: email to user
    |                                 |
    |                                 v  run_action calls approvals.request()
    |   [Approve] [Cancel] posted <---'  (row written first, then the message)
    |
    +-- click -->  POST /api/slack/interactivity: verify, ack 200, then after():
    |                identity, canAccess, claim(pending to processing), executor,
    |                finish, chat.update with the buttons removed
    |
    +-- app cron or job -->  outbound.postReport(token from slack_installations)
```

## Critical facts

1. **In-memory chat state breaks thread follow-ups on serverless.** Thread
   subscriptions, dedupe keys and locks live in the state adapter. With memory
   state, every cold start forgets which threads the bot follows and Slack
   retries are processed twice. Swap `createChatState` in `host.ts` to Redis or
   Postgres now, not in the handover; never fall back to memory on a missing
   variable, for state or stores.
2. **Slack grants the scopes the authorize URL requests.** The app config page
   only sets the ceiling. Omit `users:read.email` from the URL and every token
   lacks it, `users.info` returns no email, and no user can ever be matched.
3. **The model picks the ids, so every tool is an authorization boundary.**
   Close over the resolved `userId`; never accept it, or trust an id, as input.
   Resolve it by Slack email (`findUserIdByEmail`) or adaptation.md's user link.
4. **Ack in three seconds, then work.** Events and interactions both. Work done
   before the ack shows the clicker a timeout warning, and they click again.
5. **Read-then-write is not idempotent.** "Is it still a draft? Then send" sends
   twice under a double click. One conditional `UPDATE ... WHERE status='pending'`
   is the lock.
6. **Cache the init promise, not a boolean.** A flag set before the awaits lets
   a concurrent cold-start webhook reach a bot with no handlers.
7. **Ignore bot authors.** Bots have no email; an identity-failure reply to a
   bot can start two bots answering each other indefinitely.
8. **Slack mrkdwn is not Markdown.** `**bold**` renders literally. Convert
   app-generated text before posting; order of the passes matters.

## Hard rules

> **Never put a payload in a button `value`.** It is readable by the whole
> channel and forgeable by a client. Send an opaque id; load the rest server-side.

> **Never authorize a click by channel membership.** Resolve the clicker to an
> app user and check access to the resource, every time.

> **Never pick a bot token with `limit(1)`.** Tokens belong to a workspace. Key
> the table by `team_id` and look up the team on the event. A token is a row
> the OAuth callback writes, never an environment variable, even for one
> workspace. "Read credentials from the environment" is met by setup.md's
> table: a token is not configured, it is what installing produces.

> **Never parse the body before verifying the signature.** HMAC is over the raw
> bytes. `request.text()` first.

> **Never let a failure be silent.** After the eyes reaction, silence reads as
> "still working". Post the failure; answer a refused click ephemerally.

## Quick start

Copy every code block verbatim to the path on its first line, and write the
whole file map in setup.md even for an inbound-only task: handlers import
`services.ts`, which imports approvals and outbound, and a token arrives through
the OAuth routes. You write `host.ts` (bodies, state adapter), the renames, the
`BOT_STRINGS` text, and a store for a database that is not Supabase. Env names
are setup.md's table, all in `.env.example`, empty; invent none, not the model.
A template that looks weak is not patched in place: harden through `host.ts`, or
name the concern in the handover. Each odd line is deliberate (provenance.md),
the suite tests the templates as shipped, and an edit forks the fix releases.

1. Probe the host and fill in the seams, see [adaptation.md](references/adaptation.md).
2. Create the tables and stores, see [data-model.md](references/data-model.md).
3. Slack app, env, OAuth install, bot and events route, see [setup.md](references/setup.md).
4. Wire identity, handlers and tools, see [conversation.md](references/conversation.md).
5. Add app-initiated posting, see [outbound.md](references/outbound.md).
6. Add approvals and the interactivity route, see [approvals.md](references/approvals.md).
7. Run the suite unmodified, reporting 31, see [testing.md](references/testing.md).
8. Walk the go-live checklist, see [operations.md](references/operations.md).
9. Hand over: every `host.ts` body still on the demo (an unchanged
   `getCurrentUserId` makes every install answer 401), the chat state adapter
   production uses and its variable, and the email trust decision.

## Reference directory

| Scenario | Trigger keywords | Reference |
|---|---|---|
| Fitting it to a host app | seam, BotHost, host.ts, rename, auth guard, findUserIdByEmail, model, i18n strings | [adaptation.md](references/adaptation.md) |
| Tables and stores | slack_installations, slack_approvals, team_id, bot token, claim, RLS, service role, Drizzle, Prisma | [data-model.md](references/data-model.md) |
| Slack app, install, boot | scopes, users:read.email, app_mentions:read, OAuth, redirect_uri, state cookie, open redirect, event subscriptions, createRedisState, installationProvider, cold start, waitUntil, after() | [setup.md](references/setup.md) |
| Answering people | onNewMention, onDirectMessage, onSubscribedMessage, thread.subscribe, streamText, fullStream, stepCountIs, tools, IDOR, identity, reactions, bot loop | [conversation.md](references/conversation.md) |
| App posts to Slack | chat.postMessage, blocks, 3000 chars, 50 blocks, invalid_blocks, mrkdwn, bold not rendering, tables, 429, Retry-After, ok:false | [outbound.md](references/outbound.md) |
| Buttons and the click back | block_actions, interactivity, x-slack-signature, 3 seconds, operation timed out, double click, idempotent, response_url, ephemeral, chat.update | [approvals.md](references/approvals.md) |
| Proving it works | bun test, vitest, tests, signature test, double click test | [testing.md](references/testing.md) |
| Running it | not replying, couldn't match, stuck processing, uninstall, tokens_revoked, logs, go-live, encryption | [operations.md](references/operations.md) |
| What the audit changed | audit, defects, fixed, kept deliberately, added, fix order | [provenance.md](references/provenance.md) |

Part of the [Timerise Skills](https://github.com/timerise-ai/skills) index, which lists the sibling skills.
