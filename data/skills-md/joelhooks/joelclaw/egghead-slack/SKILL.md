---
name: egghead-slack
displayName: egghead Slack Intelligence
description: Joel's private egghead.io Slack integration — channel taxonomy, token config, passive monitoring, and message intelligence pipeline.
version: 0.2.0
author: joel
tags:
  - slack
  - egghead
  - channels
  - intelligence
---

# egghead Slack Intelligence

Joel's private intelligence layer over the egghead.io Slack workspace. **Joel-only** — never participates in channels, never replies to anyone but Joel, never surfaces private data publicly.

## Tokens

Three tokens in agent-secrets (values unchanged across scope updates):

| Secret | Type | Purpose |
|--------|------|---------|
| `slack_bot_token` | `xoxb-*` | Bot: Socket Mode, send DMs to Joel, reactions |
| `slack_app_token` | `xapp-*` | Socket Mode WebSocket connection |
| `slack_user_token` | `xoxp-*` | User: read all channels, DMs, files, search |

### User Token Scopes (current)
`admin`, `identify`, `channels:history`, `channels:read`, `groups:history`, `groups:read`, `im:history`, `im:read`, `mpim:history`, `users:read`, `users:read.email`, `chat:write`, `canvases:read`, `canvases:write`, `files:read`, `search:read`, `search:read.public`, `search:read.private`, `search:read.mpim`, `search:read.im`, `search:read.files`, `search:read.users`

### Bot Token Scopes
`files:read`, `files:write`, `remote_files:read`, `remote_files:share`, `remote_files:write`, `search:read.files`, `users.profile:read`, `chat:write`, `channels:history`, `channels:read`, `groups:history`, `groups:read`, `im:history`, `im:read`, `mpim:history`, `reactions:write`, `app_mentions:read`, `connections:write`

## Workspace IDs

All Slack IDs stored here (private skill, NOT in any git repo):
- **Workspace**: egghead.io (`T030CS0QL`)
- **Joel user**: `U030BJ3CK`
- **Bot user**: `U0AGRUMQXPF` (joelclaw bot)
- **Joel DM channel**: `D0AHPM2NPJL`

## VIP DM Channels

| Person | User ID | DM Channel | Notes |
|--------|---------|------------|-------|
| Kent C. Dodds | `U030CU0CN` | `D030BJ3D1` | MEGA instructor, EpicWeb |
| Grzegorz Róg | `U03G1P81FBJ` | `D098ZQELPLM` | Slack Connect, MEGA producer |
| Matt Pocock | `U0211NP2ZN1` | (lookup needed) | Total TypeScript, AI Hero |
| John Lindquist | `U030CS0R0` | (lookup needed) | egghead cofounder, Script Kit |

22 external Slack Connect DMs total. Notable external users discovered:
Tony Holdstock-Brown, Antonio Erdeljac, Sean Grove, Dave Kiss, Charly Poly, Matthew Rathbone, Janelle Allen, Justin Gordon

## Channel Taxonomy

729 channels total. Canonical ID→name mapping: `~/Vault/Resources/slack/channels.json` (729 entries, pulled 2026-02-26).

Prefix-based auto-categorization:

| Prefix | Category | Count (approx) | Description |
|--------|----------|-----------------|-------------|
| `lc-*` | Launch Control | ~50 | Course launch channels |
| `cc-*` | Creator Channel | ~200 | 1:1 with creators/instructors |
| `dd-*` | Ding Ding | ~15 | Revenue reporting (mostly noise) |
| `brain-*` | Brain | 3 | Team thinking/strategy spaces |
| `project-*` | Projects | ~15 | Active project channels |
| `*-chat` | Legacy | many | Legacy individual chats |
| `sp-*` | Sales/Partner | few | Sales partner channels |
| `pm-*` | Product Mgmt | few | Product management |
| `skill-*` | Skill | few | Skill Recordings ops |
| `egghead-*` | egghead Ops | several | Various egghead channels |

### Priority Channels (ADR-0131)

**High** (cc-*/lc-* with Contact materialization):
- `cc-matt-p` (`C0211NSK3TP`) — Matt Pocock
- `cc-john` (`G70JH2Y7P`) — John Lindquist  
- `cc-ashley-hindle` — active
- `cc-alex-hillman` — active
- `epic-instructors` (`C06P7TD6VMM`) — **Private, 14 members.** Kent, Artem, and other Epic Web instructors. Workshop app features, video pipeline, course-builder updates.
- `cc-kcd` (`G01NK427ZE2`) — **Private.** Kent C. Dodds creator channel (NOT lc-just-javascript)
- `cc-artem-zakharchenko` (`C044J7QEDRA`) — **Private, 11 members.** Artem's creator channel
- `lc-total-typescript` (`C03JWTULTN0`) — **Private, 10 members.** Matt's course
- `lc-ai-hero` (`C07CURG8YB1`) — **Private, 9 members.** Matt's AI platform
- `lc-course-builder` (`C06KP859BUM`) — **Private, 11 members.** Course builder tool
- `lc-badass` (`C02PXV4BR61`) — **Private, 12 members.** Badass Courses
- `lc-epic-web` (`C03QFFWHT7D`) — **Private, 11 members.** Epic Web launch

**Medium** (project-*/brain-*/skill-*):
- `brain-john` (`C0A2ZA94M0V`) — **Public, 6 members.** Strategy with John
- `brain-joel` (`C09LKT871PE`) — **Public, 8 members.** Joel's strategy space
- `project-support-agent` (`C0ACP6SDN73`) — **Public, 8 members.** Support agent project
- `project-gremlin` (`C0AE33HH9C3`) — **Public, 8 members.** Gremlin project
- `skill-life` (`C04JPQS5ZUZ`) — **Private, 9 members.** Skill Recordings ops

**Low/noise** (dd-*/sp-*/legacy):
- `dd-*` — revenue signals, topic-only extraction
- `*-chat` — legacy, rarely active

## API Patterns

### Search messages
```bash
SLACK_USER=$(secrets lease slack_user_token --ttl 1h)
curl -s "https://slack.com/api/search.messages?query=QUERY&count=20&sort=timestamp&sort_dir=desc" \
  -H "Authorization: Bearer $SLACK_USER"
```

### List DM channels
```bash
curl -s "https://slack.com/api/conversations.list?types=im&limit=500" \
  -H "Authorization: Bearer $SLACK_USER"
```

### Read DM history
```bash
curl -s "https://slack.com/api/conversations.history?channel=DM_CHANNEL_ID&limit=30" \
  -H "Authorization: Bearer $SLACK_USER"
```

### Download files
```bash
curl -s -L -o output.file \
  -H "Authorization: Bearer $SLACK_USER" \
  "URL_PRIVATE_DOWNLOAD"
```
Requires `files:read` scope on user token.

### Send DM to Joel (bot token)
```bash
SLACK_BOT=$(secrets lease slack_bot_token --ttl 1h)
curl -s -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_BOT" \
  -H 'Content-Type: application/json' \
  -d '{"channel":"U030BJ3CK","text":"message"}'
```

### Upload file (3-step)
`files.getUploadURLExternal` → POST multipart → `files.completeUploadExternal`

### Resolve external user (Slack Connect)
```bash
curl -s "https://slack.com/api/users.info?user=EXTERNAL_USER_ID" \
  -H "Authorization: Bearer $SLACK_USER"
```

## Backfill Pipeline

Inngest functions (deployed, registered):
- `slack-channel-backfill` — per-channel paginated history → Typesense `slack_messages`
- `slack-backfill-batch` — fan-out orchestrator for multiple channels
- Events: `channel/slack.backfill.requested`, `channel/slack.backfill.batch.requested`
- Flow control: concurrency 2, throttle 10/60s, 1.5s sleep between pages
- First backfill: 15 channels, 60-day window, 245+ messages indexed

## Privacy Boundary

**Absolute rules:**
- JoelClaw NEVER posts in Slack channels (only Joel's DM)
- JoelClaw NEVER responds to other users
- JoelClaw NEVER surfaces channel content publicly
- All intelligence is private context for Joel only
- **No Slack IDs, channel names, or workspace identifiers in public repos**
- This skill file is PRIVATE — lives at `~/.pi/agent/skills/egghead-slack/`, NOT in joelclaw repo

**Content shared in Slack is privileged by default:**
- Loom recordings, screenshots, files, and links shared in Slack channels or DMs are **private** unless Joel explicitly says otherwise
- Do NOT auto-publish Looms or Slack-sourced content as discoveries, blog posts, or any public-facing content
- Always ASK Joel before surfacing any Slack-originated content publicly
- This applies to all channels — cc-*, lc-*, DMs, Slack Connect, everything

## Related ADRs

- ADR-0130: Slack Channel Integration (gateway handler)
- ADR-0131: Unified Channel Intelligence Pipeline
- ADR-0132: VIP DM Escalated Handling
- Gateway channel: `packages/gateway/src/channels/slack.ts`
