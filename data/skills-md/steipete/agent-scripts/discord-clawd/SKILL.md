---
name: discord-clawd
description: Query Peter's local Discord archive in ~/.discrawl/discrawl.db when asked about Discord history, channel activity, top posters, message counts, summaries, or anything in synced Discord data. Use this skill for local search, SQL stats, channel/member lookups, and freshness checks before answering recent or latest Discord questions.
---

# Discord Clawd

Use this for Discord questions first. Local archive first; live Discord only when freshness matters and the archive is stale.

## Trigger

Use when the user asks things like:

- "what happened in #maintainers"
- "who posted the most in discord"
- "search discord for ..."
- "how many messages/users/channels"
- "summarize this week in #channel"
- "is Discord fully synced"

## Data Sources

Prefer in this order:

1. `~/.discrawl/discrawl.db`
2. `/tmp/discrawl --config ~/.discrawl/config.toml ...`
3. Live refresh from `~/Projects/discrawl` only if needed

Do not browse the web for Discord archive questions unless the user explicitly wants external context too.

## Freshness Check

For `latest`, `recent`, `today`, `this week`, or sync questions, check freshness first.

Useful queries:

```bash
sqlite3 ~/.discrawl/discrawl.db \
  "select coalesce(max(updated_at),'') from sync_state where scope like 'channel:%';"
```

```bash
sqlite3 ~/.discrawl/discrawl.db "
select count(*)
from channels c
where coalesce(c.kind,'') in (
  'text','news','announcement',
  'thread_public','thread_private','thread_news','thread_announcement'
)
and not exists (
  select 1 from sync_state s
  where s.scope = 'channel:' || c.id || ':history_complete'
)
and not exists (
  select 1 from sync_state s
  where s.scope = 'channel:' || c.id || ':unavailable'
);"
```

Interpretation:

- `0` remaining = fully synced for real message-bearing channels
- forum parents are metadata containers; their post history lives in thread channels

## Query Workflow

1. Resolve scope: channel, date range, author, keyword.
2. Check freshness if the user asked for recent/current data.
3. Use SQL for counts/rankings/exact filters.
4. Use `search`/FTS for discovery, then SQL for precise slices.
5. Prefer the `messages` CLI for exact channel+date slices before dropping to raw SQL.
6. Report with absolute dates, counts, and channel names.

## Common Queries

Resolve channel name:

```bash
sqlite3 ~/.discrawl/discrawl.db \
  "select id, name, kind from channels where name like '%maintainers%' order by name;"
```

Top channels:

```bash
sqlite3 ~/.discrawl/discrawl.db "
select c.name, c.kind, count(m.id) as messages
from channels c
join messages m on m.channel_id = c.id
group by c.id
order by messages desc
limit 20;"
```

Top authors with names:

```bash
sqlite3 ~/.discrawl/discrawl.db "
select
  coalesce(mem.display_name, mem.username, m.author_id) as author,
  m.author_id,
  count(*) as messages
from messages m
left join members mem
  on mem.user_id = m.author_id
 and mem.guild_id = m.guild_id
where coalesce(m.author_id,'') != ''
group by m.author_id, coalesce(mem.display_name, mem.username, m.author_id)
order by messages desc
limit 20;"
```

Messages in one channel for the last X days:

```bash
/tmp/discrawl --config ~/.discrawl/config.toml \
  messages --channel maintainers --days 7 --all
```

Messages in one channel since a date:

```bash
/tmp/discrawl --config ~/.discrawl/config.toml \
  messages --channel '#maintainers' --since 2026-03-01T00:00:00Z --all
```

Keyword search:

```bash
/tmp/discrawl --config ~/.discrawl/config.toml search "query terms"
```

Read-only SQL via CLI:

```bash
/tmp/discrawl --json --config ~/.discrawl/config.toml sql \
  "select count(*) from messages;"
```

## Summaries

For channel summaries:

- pull the exact slice first
- include counts: messages, authors, date span
- identify recurring topics, decisions, blockers
- do not claim certainty beyond the retrieved slice

For release-window summaries, anchor on exact timestamps, not vague relative dates.

## Name Resolution

Prefer:

1. `members.display_name`
2. `members.username`
3. `messages.raw_json -> $.author.username`
4. raw author id

If a user asks "who is this id", resolve locally before answering.

## Live Refresh

Only do this if the user wants fresher data than the archive has.

Repo:

```bash
cd ~/Projects/discrawl
```

Token source:

```bash
ssh peters-mac-studio-1 \
  "zsh -lc 'source ~/.profile >/dev/null 2>&1; printf %s \"\$DISCORD_BOT_ID_FLAWD\"'"
```

Targeted refresh is better than full sync for ad hoc questions:

```bash
DISCORD_BOT_TOKEN="..." /tmp/discrawl \
  --config ~/.discrawl/config.toml \
  sync --full --channels <channel-id> --concurrency 1
```

## Guardrails

- never expose bot tokens
- prefer local DB over network
- use absolute dates in answers
- if freshness is uncertain, say so
- if the archive is stale, either sync first or label the answer as archive-based
