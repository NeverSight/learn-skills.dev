---
name: warmysender
description: Run cold email, email warmup, LinkedIn, Instagram and WhatsApp outreach, email verification and a 200M+ B2B lead database from any MCP agent through WarmySender — the agent builds, launches and manages campaigns in plain language and never sends a message itself; WarmySender's scheduler paces every action inside safe limits.
homepage: https://warmysender.com/ai-agents
metadata: {"openclaw":{"emoji":"🔥","requires":{"bins":[],"env":[]}}}
---

# WarmySender for AI agents

WarmySender is an outreach platform with five channels — cold email, email warmup, LinkedIn, Instagram and WhatsApp — plus real-time email verification and a 200M+ B2B lead database. This skill teaches an agent (Claude, ChatGPT, Cursor, Codex, OpenClaw, and Hermes Agent, or any agent that speaks MCP) how to run it through the hosted WarmySender MCP server.

Your agent can run the entire outreach — build, launch and manage cold email, LinkedIn, Instagram and WhatsApp campaigns, verify emails, search and save leads, and tune warmup, all in plain language — while WarmySender's scheduler keeps every account inside safe limits no matter who's driving.

---

## 1. Connect first

<!-- GENERATED:connect START -->
WarmySender is a hosted MCP server (streamable HTTP) at:

```
https://warmysender.com/mcp
```

**Sign-in is the default.** The client registers itself and the user signs in to WarmySender in the browser — no key to paste. Use the API-key form only for clients that cannot sign in, or when the user prefers a key.

If your agent has no MCP settings at all, the user can paste this paragraph into the chat:

> Connect to WarmySender: it is an MCP server at https://warmysender.com/mcp that uses OAuth sign-in (no API key needed). Add it as a streamable-HTTP MCP server, open the sign-in link it returns so I can approve access, then install the WarmySender skill from https://github.com/fortuneflick/warmysender-claude-plugin (`npx skills add fortuneflick/warmysender-claude-plugin`). Never send a message yourself — WarmySender's scheduler paces every email, LinkedIn, Instagram and WhatsApp action inside safe limits.

### Per-client connect commands

#### Claude

Sign in (default):

```text
https://warmysender.com/mcp
```

In Claude open Customize → Connectors, choose + then Add custom connector, paste this address and click Add. Claude then opens a WarmySender sign-in — approve it and you are connected.

API-key fallback — `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "warmysender": {
      "command": "npx",
      "args": [
        "-y",
        "@warmysender/mcp",
        "--api-key=ws_YOUR_API_KEY_HERE"
      ]
    }
  }
}
```

Paste into your claude_desktop_config.json and restart Claude Desktop.

#### ChatGPT

Sign in (default):

```bash
codex mcp add warmysender --url https://warmysender.com/mcp
codex mcp login warmysender
```

ChatGPT Plus and every plan above it include Codex. Run both lines in your terminal; the second opens your browser to sign in to WarmySender.

API-key fallback:

```bash
export WARMYSENDER_API_KEY=ws_YOUR_API_KEY_HERE
codex mcp add warmysender --url https://warmysender.com/mcp --bearer-token-env-var WARMYSENDER_API_KEY
```

ChatGPT Plus and every plan above it include Codex. Run both lines, adding the export to your shell profile so it sticks.

#### Claude Code

Sign in (default):

```bash
claude mcp add --transport http warmysender https://warmysender.com/mcp
```

Run this once in your terminal, then type /mcp inside Claude Code (or run claude mcp login warmysender) and sign in to WarmySender in the browser.

API-key fallback:

```bash
claude mcp add --transport http warmysender https://warmysender.com/mcp --header "Authorization: Bearer ws_YOUR_API_KEY_HERE"
```

Run this once in your terminal.

#### Cursor

Sign in (default) — `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "warmysender": {
      "url": "https://warmysender.com/mcp"
    }
  }
}
```

Use the Add to Cursor button, or paste this into .cursor/mcp.json in your project root and sign in when Cursor asks.

API-key fallback — `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "warmysender": {
      "url": "https://warmysender.com/mcp",
      "headers": {
        "Authorization": "Bearer ws_YOUR_API_KEY_HERE"
      }
    }
  }
}
```

Use the Add to Cursor button, or paste this into .cursor/mcp.json in your project root.

#### Codex

Sign in (default):

```bash
codex mcp add warmysender --url https://warmysender.com/mcp
codex mcp login warmysender
```

Run both lines in your terminal; the second opens your browser to sign in to WarmySender.

API-key fallback:

```bash
export WARMYSENDER_API_KEY=ws_YOUR_API_KEY_HERE
codex mcp add warmysender --url https://warmysender.com/mcp --bearer-token-env-var WARMYSENDER_API_KEY
```

Run both lines, adding the export to your shell profile so it sticks.

#### OpenClaw

Sign in (default):

```bash
openclaw mcp add warmysender --url https://warmysender.com/mcp --transport streamable-http --auth oauth
openclaw mcp login warmysender
```

Run both lines; the second opens a WarmySender sign-in in your browser. OpenClaw ignores static headers while sign-in is on, so no key is ever stored.

API-key fallback:

```bash
openclaw mcp set warmysender '{"url":"https://warmysender.com/mcp","headers":{"Authorization":"Bearer ws_YOUR_API_KEY_HERE"}}'
```

Run this once to register WarmySender. OpenClaw can then call any of WarmySender's 78 tools.

#### Hermes Agent

Sign in (default) — `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  warmysender:
    url: "https://warmysender.com/mcp"
    auth: oauth
```

Add this to ~/.hermes/config.yaml, then run /reload-mcp in the chat and sign in when prompted.

API-key fallback — `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  warmysender:
    url: "https://warmysender.com/mcp"
    headers:
      Authorization: "Bearer ws_YOUR_API_KEY_HERE"
```

Add this to ~/.hermes/config.yaml, then run /reload-mcp in the chat.

#### Muse Code

This client connects with an API key — `~/.config/muse/settings.json`:

```json
{
  "schema_version": 1,
  "mcp_servers": {
    "warmysender": {
      "transport": "streamable_http",
      "url": "https://warmysender.com/mcp",
      "headers": {
        "Authorization": "Bearer ws_YOUR_API_KEY_HERE"
      }
    }
  }
}
```

Save this as ~/.config/muse/settings.json (create the folder if it is not there yet) and start Muse Code again. Keep the schema_version line — Muse Code rejects the file without it. If you already have a settings file, add only the warmysender block inside your existing mcp_servers.

#### Grok Bot

This client connects with an API key:

```json
{
  "name": "warmysender",
  "url": "https://warmysender.com/mcp",
  "headers": {
    "Authorization": "Bearer ws_YOUR_API_KEY_HERE"
  }
}
```

Open grok.com/connectors → New Connector → Custom, paste the server address and use your key as the bearer token. Type @ in a chat to attach WarmySender.

#### Windsurf

Sign in (default) — `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "warmysender": {
      "serverUrl": "https://warmysender.com/mcp"
    }
  }
}
```

Paste into ~/.codeium/windsurf/mcp_config.json and sign in when Windsurf asks.

API-key fallback — `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "warmysender": {
      "serverUrl": "https://warmysender.com/mcp",
      "headers": {
        "Authorization": "Bearer ws_YOUR_API_KEY_HERE"
      }
    }
  }
}
```

Paste into ~/.codeium/windsurf/mcp_config.json.

#### Zed

This client connects with an API key — `settings.json`:

```json
{
  "context_servers": {
    "warmysender": {
      "command": {
        "path": "npx",
        "args": [
          "-y",
          "@warmysender/mcp",
          "--api-key=ws_YOUR_API_KEY_HERE"
        ]
      }
    }
  }
}
```

Add to your Zed settings.json under context_servers.
<!-- GENERATED:connect END -->

### API-key fallback

Create a key in the WarmySender app under **Settings → API Keys** (keys start with `ws_`). Give the key only the scopes the job needs — a read-only key is enough for reporting. Never paste a key into a chat message, a log or a file you commit; put it in the client's config or an environment variable as shown above. Rotate it from the same Settings page at any time.

---

## 2. Hard rules for the agent (read first)

1. **Never send a message yourself.** There is no "send" tool. `create_*` writes a draft; `start_*`, `resume_*` and `enroll_*` only hand work to WarmySender's scheduler, which paces every email, LinkedIn, Instagram and WhatsApp action inside each account's safe daily, weekly and hourly limits and the gradual ramp for new accounts.
2. **Never claim to raise a limit.** No tool can raise a cap, skip the ramp, or bypass a check. If a campaign is slow, explain the pacing (`list_skipped_actions`, `get_linkedin_campaign_throttle`) — do not "retry harder".
3. **Connecting or disconnecting accounts stays in the app.** Mailboxes, LinkedIn seats, Instagram accounts and WhatsApp numbers are connected by the user at warmysender.com. If none is connected, say so and stop.
4. **Call `get_workspace_info` first.** It tells you which workspace you are in, which scopes you hold and what the plan allows. Do not guess.
5. **Read before you write.** Prefer `list_*` / `get_*` tools to establish state (existing campaigns, templates, mailboxes, allowance) before any write.
6. **Confirm with the user before `start_*`, `resume_*`, `enroll_*`, `pause_*`, `unenroll_*`, `delete_*`, `close_*`, `cancel_*` and `remove_*`.** Tools marked destructive in the catalogue below carry `destructiveHint` — show the user what will change and wait for a yes. Never pass `force: true` to a start tool on your own initiative; report the listed problems and only pass it if the user explicitly says "launch anyway".
7. **Every cold-email campaign needs a sending window and an opt-out sentence.** Set `sending_window_start` / `sending_window_end` / `schedule_days` / `timezone` on `create_campaign`, and make sure the workspace footer is configured (`update_workspace_settings`: postal address, opt-out style `link` or `reply`, opt-out wording). The footer is appended for you — do not hand-write a second unsubscribe line.
8. **Spending is visible before it happens.** Check `get_verification_allowance` before `submit_verification_batch`; `search_leads` is free, `save_leads` / `export_leads` use the monthly allowance or lead credits. Say how much will be used before you use it.
9. **Report facts, not guesses.** Quote the tool result (counts, statuses, reasons). If a tool returns an error, show the message to the user as-is and stop; do not loop.

---

<!-- GENERATED:catalogue START -->
## 3. Tool catalogue (78 tools)

All 78 tools are workspace-scoped: a tool only ever sees the workspace the signed-in user (or key) belongs to. "read-only" tools change nothing; "mutating" tools write drafts, settings or scheduler work; "destructive" tools stop, remove or cancel something and should be confirmed first.

### Cold email & prospects (19 tools)

Build, launch, pause, and resume cold-email campaigns; add, update, and bulk-import prospects; and manage your suppression list — all in plain language.

| Tool | Kind | What it does |
|---|---|---|
| `create_campaign` | mutating | Create a new email campaign in draft status. |
| `update_campaign` | mutating | Partial update of a campaign. |
| `start_campaign` | mutating | Start an email campaign. |
| `pause_campaign` | **mutating (destructive — confirm first)** | Pause a running email campaign. |
| `resume_campaign` | mutating | Resume a paused email campaign. |
| `enroll_prospects` | mutating | Add prospects to an email campaign. |
| `unenroll_prospects` | **mutating (destructive — confirm first)** | Stop a campaign for specific prospects (soft-cancel; audit trail preserved). |
| `create_prospect` | mutating | Create a prospect in the workspace (or reuse the existing one) and optionally add it to a list. |
| `update_prospect` | mutating | Partial update of a prospect's fields. |
| `bulk_create_prospects` | mutating | Create up to 500 prospects in one call. |
| `add_to_suppression_list` | mutating | Suppress emails or domains to prevent any future outreach from any campaign in the workspace. |
| `list_campaigns` | read-only | Return email campaigns in the workspace. |
| `get_campaign` | read-only | Return full details for one email campaign including steps (sequence emails) and top-level stats. |
| `list_prospects` | read-only | Return prospects in the workspace with cursor pagination. |
| `get_prospect` | read-only | Return full details for one prospect, including custom fields, list memberships, and enrollment history summary. |
| `list_suppressions` | read-only | Return the workspace's suppression list (emails and domains that won't be contacted). |
| `list_skipped_actions` | read-only | Explain why a campaign sent little or nothing recently: the actions that did not run in the last N hours, grouped by cause, each with a plain-language explanation and a flag saying whether it is normal pacing that resumes on its own or something that needs attention. |
| `list_email_templates` | read-only | Return the workspace's saved email templates (name, category, subject, preview text). |
| `get_email_template` | read-only | Return one saved email template in full, including its subject, preview text and body. |

### Tracking domains (4 tools)

Use your own branded domain for open and click tracking. Add a tracking domain, check that it is set up correctly, list the ones you have, and remove any you no longer need.

| Tool | Kind | What it does |
|---|---|---|
| `add_tracking_domain` | mutating | Add a custom open/click tracking domain. |
| `verify_tracking_domain` | mutating | Check whether a tracking domain's CNAME record is set correctly and mark it verified or in-error. |
| `list_tracking_domains` | read-only | Return the workspace's custom open/click tracking domains with verification status (pending, verified, or error), the CNAME target to set, and last-checked and verified timestamps. |
| `remove_tracking_domain` | **mutating (destructive — confirm first)** | Delete a custom tracking domain from the workspace by id. |

### LinkedIn — campaigns, posts & recruiter (19 tools, safety-gated)

Run LinkedIn end to end: connection and message campaigns, publish and manage posts, and create, publish, or close recruiter jobs and read their applicants. Every action is paced within your account’s safe daily and weekly limits.

| Tool | Kind | What it does |
|---|---|---|
| `create_linkedin_campaign` | mutating | Create a new LinkedIn outreach campaign as a draft (a sequence of steps such as send_invite, wait_accept, send_message, wait_reply, and condition branches). |
| `start_linkedin_campaign` | mutating | Launch a draft (or resume a paused) LinkedIn campaign so it begins working. |
| `pause_linkedin_campaign` | **mutating (destructive — confirm first)** | Pause a running LinkedIn campaign. |
| `resume_linkedin_campaign` | mutating | Resume a paused LinkedIn campaign. |
| `enroll_in_linkedin_campaign` | mutating | Queue prospects for a LinkedIn campaign. |
| `create_linkedin_post` | mutating | Create a LinkedIn post as a draft, or schedule it for a future time (published automatically at a safe pace). |
| `publish_linkedin_post` | mutating | Publish a LinkedIn post you previously drafted or scheduled — now, at a safe pace (respects your daily posting limit). |
| `delete_linkedin_post` | **mutating (destructive — confirm first)** | Delete a draft, scheduled, or failed LinkedIn post. |
| `create_linkedin_job` | mutating | Create a LinkedIn Recruiter job posting as a draft (requires a Recruiter seat). |
| `publish_linkedin_job` | mutating | Publish one of your LinkedIn Recruiter job postings. |
| `close_linkedin_job` | **mutating (destructive — confirm first)** | Close one of your LinkedIn Recruiter job postings so it stops accepting applicants. |
| `list_linkedin_accounts` | read-only | Return connected LinkedIn accounts with status, strategy, and current daily/weekly usage against safety limits. |
| `get_linkedin_account_health` | read-only | Return detailed LinkedIn account health metrics: acceptance rate, response rate, restrictions, consecutive errors, and safety limit headroom. |
| `list_linkedin_campaigns` | read-only | Return LinkedIn campaigns with status and top-level counters. |
| `get_linkedin_campaign_stats` | read-only | Return full campaign health metrics: invites sent/accepted, messages sent/replied, variant performance if A/B testing is used. |
| `get_linkedin_campaign_throttle` | read-only | Explain why a LinkedIn campaign is or isn't sending right now: which daily or weekly allowance is holding it back, when that allowance refreshes, how many campaigns share the same LinkedIn account, and this campaign's share of that account's allowance versus what it has used today, per action type. |
| `list_linkedin_posts` | read-only | Return LinkedIn posts for the workspace (drafts, scheduled, published, failed) with status, content, schedule time, resolved URL, and engagement counters. |
| `list_linkedin_jobs` | read-only | List LinkedIn Recruiter job postings for a connected account (live, rate-limited to protect your account). |
| `list_linkedin_job_applicants` | read-only | List applicants for a LinkedIn Recruiter job posting on a connected account (live, rate-limited to protect your account). |

### WhatsApp messages (9 tools, safety-gated)

Create and launch WhatsApp campaigns, enroll prospects, and check number health and results. New numbers ramp up gradually and stay within a safe daily, first-message and hourly budget, with a natural pause between messages.

| Tool | Kind | What it does |
|---|---|---|
| `create_whatsapp_campaign` | mutating | Create a WhatsApp outreach campaign in draft status. |
| `start_whatsapp_campaign` | mutating | Start a WhatsApp campaign. |
| `pause_whatsapp_campaign` | **mutating (destructive — confirm first)** | Pause a running WhatsApp campaign. |
| `resume_whatsapp_campaign` | mutating | Resume a paused WhatsApp campaign. |
| `enroll_in_whatsapp_campaign` | mutating | Queue prospects for a WhatsApp campaign. |
| `list_whatsapp_accounts` | read-only | Return connected WhatsApp numbers with status, ramp stage, and current daily/new-chat/hourly usage against safety limits. |
| `get_whatsapp_account_health` | read-only | Return detailed WhatsApp number health: 30-day reply rate, restrictions, consecutive errors, throttle state, and remaining daily/new-chat/hourly headroom against safety limits. |
| `list_whatsapp_campaigns` | read-only | Return WhatsApp campaigns with status and top-level counters (enrolled, messages sent, replies). |
| `get_whatsapp_campaign_stats` | read-only | Return full campaign metrics: new chats started, messages sent, replies received, reply rate, and variant performance if A/B testing is used. |

### Instagram DMs (9 tools, safety-gated)

Create and launch Instagram DM campaigns, enroll prospects, and check account health and results. New accounts ramp up gradually and stay within a safe daily and hourly action budget.

| Tool | Kind | What it does |
|---|---|---|
| `create_instagram_campaign` | mutating | Create an Instagram DM/outreach campaign in draft status. |
| `start_instagram_campaign` | mutating | Start an Instagram campaign. |
| `pause_instagram_campaign` | **mutating (destructive — confirm first)** | Pause a running Instagram campaign. |
| `resume_instagram_campaign` | mutating | Resume a paused Instagram campaign. |
| `enroll_in_instagram_campaign` | mutating | Queue prospects for an Instagram campaign. |
| `list_instagram_accounts` | read-only | Return connected Instagram accounts with status, ramp stage, and current daily/hourly usage against combined safety limits. |
| `get_instagram_account_health` | read-only | Return detailed Instagram account health: 30-day reply rate, restrictions, consecutive errors, and remaining daily/hourly action headroom against combined safety limits. |
| `list_instagram_campaigns` | read-only | Return Instagram campaigns with status and top-level counters (enrolled, follows, DMs sent, replies). |
| `get_instagram_campaign_stats` | read-only | Return full campaign metrics: follows sent, DMs sent, replies received, reply rate, and variant performance if A/B testing is used. |

### Warmup & mailboxes (5 tools)

Tune warmup settings, adjust many mailboxes at once, and check mailbox health and warmup ramp status before you scale up sending.

| Tool | Kind | What it does |
|---|---|---|
| `update_warmup_settings` | mutating | Change warmup configuration for a single mailbox: enable/disable, target daily volume, strategy type. |
| `bulk_update_warmup` | mutating | Apply the same warmup settings to multiple mailboxes at once. |
| `list_mailboxes` | read-only | Return all connected email mailboxes with status, warmup state, and top-level health. |
| `get_mailbox_health` | read-only | Return detailed health and deliverability status for one mailbox, including any recent issues. |
| `get_warmup_stats` | read-only | Return email warmup stats. |

### Email verification (7 tools)

Verify a single address or submit a whole list, check how much of your allowance is left before you spend it, follow results as they come in, stop a run and get the unused credits back, and turn the usable results into a ready-to-use list — reported as confirmed mailboxes plus ones on mail servers that accept every address, so your agent knows what it actually has. All on the same safe pacing and allowance as the in-app verifier, so an agent can’t burst it.

| Tool | Kind | What it does |
|---|---|---|
| `verify_email` | mutating | Verify a single email address and return whether it is valid, invalid, risky, or unknown. |
| `submit_verification_batch` | mutating | Submit up to 5,000 email addresses for verification and return a run id to poll with get_verification_result. |
| `get_verification_result` | read-only | Return the progress and per-address outcomes of a verification run, optionally filtered to one outcome. |
| `list_verification_batches` | read-only | List this workspace's email verification runs, newest first, with their status and result counts. |
| `get_verification_allowance` | read-only | Return how many email addresses can be verified right now: where access comes from (plan allowance, purchased credits, or the one free daily check), the plan allowance left this month and today, the credit balance, free checks left today, and the largest single batch accepted. |
| `cancel_verification_batch` | **mutating (destructive — confirm first)** | Stop a verification run that is still in progress and return the unused credits. |
| `create_list_from_verification` | mutating | Build a reusable prospect list from a finished verification run. |

### Leads database (3 tools)

Search 200M+ B2B leads by role, industry, and location, then save the ones you want into a prospect list or export them with full contact details. Searching is free; each new lead uses your monthly allowance or purchasable lead credits.

| Tool | Kind | What it does |
|---|---|---|
| `search_leads` | read-only | Search 200M+ B2B leads by keyword, location (including postcode / ZIP prefix and street), industry, job title, seniority, department, and data-availability filters. |
| `save_leads` | mutating | Save leads from the database into a prospect list (creating the list if new_list_name is given). |
| `export_leads` | mutating | Export leads from the database as rows with full, unmasked contact details (email, phone, and more). |

### Workspace & jobs (3 tools)

Confirm what an API key can access, set the postal address, opt-out style and opt-out wording used in your cold email footer, and track the status of any queued job or bulk operation.

| Tool | Kind | What it does |
|---|---|---|
| `get_workspace_info` | read-only | Return basic information about the workspace this API key is attached to, the scopes granted to the key, the account's billing state, and the MCP server version. |
| `update_workspace_settings` | mutating | Set the postal address printed in the footer of your cold email, choose how people opt out, and word the opt-out sentence yourself. |
| `get_job_status` | read-only | Check how a long-running request is going (for example a bulk warmup update or a mailbox connection test). |
<!-- GENERATED:catalogue END -->

---

## 4. Workflows and example prompts

### Cold email campaign from a list

> "Create a 3-step cold email campaign called 'Q4 agencies' for the 'Agencies EU' list, send Mon–Fri 9–17 Europe/Berlin, 40 a day per mailbox, stop on reply. Use my 'Intro v2' template for step 1. Show me the draft before you start it."

1. `get_workspace_info` → `list_mailboxes` (pick warmed, healthy mailboxes) → `list_prospects` / list id → `list_email_templates` → `get_email_template`.
2. `create_campaign` with steps, `timezone`, `sending_window_start/end`, `schedule_days`, `max_sends_per_mailbox_per_day`, `stop_on_reply`, `mailbox_ids`.
3. Confirm the footer with `update_workspace_settings` if the user has not set an address / opt-out style.
4. `enroll_prospects` (list id) → show the summary → **ask** → `start_campaign`.
5. Later: `get_campaign` for stats; `list_skipped_actions` when the user asks why little went out.

### Warmup tune

> "Which mailboxes are still ramping? Set every Google mailbox that's past day 14 to 40 warmup emails a day with a 30% reply rate."

`list_mailboxes` → `get_warmup_stats` / `get_mailbox_health` → `bulk_update_warmup` (returns a job id) → `get_job_status`. Warmup keeps running on its own; you only tune it.

### LinkedIn campaign

> "Build a LinkedIn campaign: invite with a short note, wait for acceptance, then a 2-line message. Enroll the 'SaaS founders' list on my main account and start it."

`list_linkedin_accounts` → `get_linkedin_account_health` → `create_linkedin_campaign` (steps such as send_invite → wait_accept → send_message) → `enroll_in_linkedin_campaign` → **ask** → `start_linkedin_campaign`. If it looks slow: `get_linkedin_campaign_throttle` explains which allowance is binding and when it lifts.

### Instagram DM campaign

> "Start an Instagram DM campaign to the 'Fitness creators' list from @ourbrand with a two-message sequence, 24h apart."

`list_instagram_accounts` → `get_instagram_account_health` → `create_instagram_campaign` → `enroll_in_instagram_campaign` → **ask** → `start_instagram_campaign`. New accounts ramp up gradually; report the ramp stage rather than promising volume.

### WhatsApp campaign

> "Create a WhatsApp campaign for the 'Webinar sign-ups' list from the +44 number: one message today, a follow-up in 3 days if no reply."

`list_whatsapp_accounts` → `get_whatsapp_account_health` → `create_whatsapp_campaign` → `enroll_in_whatsapp_campaign` → **ask** → `start_whatsapp_campaign`. First messages to new contacts have their own daily budget; explain it if the user expects more.

### Verify a list

> "Verify the 'Trade show 2026' list and make me a clean list of the deliverable addresses."

`get_verification_allowance` → **tell the user the cost** → `submit_verification_batch` (`list_id`) → `get_verification_result` until finished → `create_list_from_verification`. Use `cancel_verification_batch` if the user changes their mind; unused credits come back.

### Search 200M+ leads and save

> "Find marketing directors at software companies in Texas, show me 25, then save the best 100 to a new list called 'TX marketing'."

`search_leads` (free, masked results) → present → **confirm the allowance/credit use** → `save_leads` with `new_list_name`, or `export_leads` for full rows. Then enroll the list in a campaign as above.

---

## 5. Troubleshooting

- **Sign-in loop / the agent keeps asking to sign in** — follow https://warmysender.com/documentation/connecting-an-ai-agent-that-asks-you-to-sign-in (finish the browser sign-in in the same profile the agent opened; remove and re-add the server if the token was revoked).
- **"insufficient scope"** — the key lacks a scope the tool needs. Create a new key with the right scopes under Settings → API Keys and reconnect; `get_workspace_info` lists the scopes a key holds.
- **"plan upgrade required" / a feature is not available** — the workspace's plan does not include that channel or agent throughput. Tell the user which feature is gated and point them to https://warmysender.com/pricing; do not retry.
- **Campaign started but nothing sent** — that is usually pacing. Read `list_skipped_actions` (email) or `get_linkedin_campaign_throttle` (LinkedIn) and report the reasons; do not pause/resume to "kick" it.
- **No mailbox / account connected** — connecting accounts is done in the app, not by the agent. Send the user to warmysender.com.

---

## 6. Links

- Server + setup docs: https://warmysender.com/mcp
- What agents can do: https://warmysender.com/ai-agents
- Connect your agent: https://warmysender.com/documentation/connect-your-ai-agent
- Pricing: https://warmysender.com/pricing
- Skill + plugin source: https://github.com/fortuneflick/warmysender-claude-plugin
