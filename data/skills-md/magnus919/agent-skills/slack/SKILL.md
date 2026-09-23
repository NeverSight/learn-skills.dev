---
name: slack
description: >-
  Operate Slack workspaces from a terminal or agent: list channels, read
  messages, follow threads, search message history, list files, and verify
  inbound webhook signatures — with a bundled slack-cli script that is
  read-only by default and gates every send behind a --dry-run/--yes
  confirmation. Use when an agent needs to read or post Slack data, triage
  incidents, or answer questions about what was said in a workspace. Do not
  use for building Slack apps or bots (that is application development) or
  workspace administration like user provisioning and org settings (that is
  the Slack admin console).
license: MIT
compatibility: >-
  The bundled slack-cli script runs on Python 3.9+ with only the standard
  library. --help, channel/message/thread/search/file reads, and webhook
  signature verification need no network; live reads require a Slack bot/user
  token with the right scopes and network access to api.slack.com.
metadata:
  source: https://api.slack.com/web
  source_index: references/00-source-index.md
  research_checked: "2026-08-03"
---

# Slack Operations

Use this skill to read and, with explicit confirmation, write Slack data through the Slack Web API: channels, messages, threads, search, files, and webhook signature verification. This is a **tool skill** for the Slack platform. Building Slack apps and bots is application development; workspace administration (user provisioning, org-level settings, SSO) lives in the Slack admin console. This skill owns the everyday agent workflow: knowing what was said, finding it later, and posting a reply when a human confirms.

## Operating contract

1. **Read-only discovery before any mutation.** List channels, read history, follow threads, search, and list files freely. The bundled `slack-cli` script makes reads without writing anything.
2. **Confirm the target, scope, and rollback path before acting.** Sending a message or replying in a thread changes shared workspace state visible to everyone: it requires an explicit human directive naming the channel, plus `--dry-run` preview and `--yes` confirmation through `slack-cli`. There is no "unsend" for team members who already read it.
3. **Respect bounded reads.** Slack paginates; never page past what the task needs. `slack-cli --limit N` caps every listing, and responses summarize records rather than dumping raw payloads.
4. **Verify webhooks before trusting them.** Any handler that accepts Slack events must verify `X-Slack-Signature` and `X-Slack-Request-Timestamp` against the app signing secret, or anyone who can reach the endpoint can forge events. `slack-cli webhook verify` does this check.
5. **Keep evidence bounded.** Quote short message excerpts and IDs; never paste full threads, tokens, or file contents into chat.

## The slack-cli script

`scripts/slack-cli` is an agent-first, stdlib-only CLI over the Slack Web API. It covers the full issue scope: messages, channels, threads, search, files, and webhook verification.

```bash
slack/scripts/slack-cli --help                          # no token or network needed
slack/scripts/slack-cli --json --limit 10 channels list
slack/scripts/slack-cli --json messages list --channel C12345
slack/scripts/slack-cli --json threads list --channel C12345 --ts 1712345678.000001
slack/scripts/slack-cli --json search messages --query "incident"
slack/scripts/slack-cli --json files list --limit 5
slack/scripts/slack-cli messages send --channel C12345 --text "on it" --dry-run   # preview
slack/scripts/slack-cli messages send --channel C12345 --text "on it" --yes       # confirmed
slack/scripts/slack-cli webhook verify --body-file body.json --signature "v0=..." --timestamp 1712345678
```

Exit codes: 0 success, 1 API error or failed verification, 2 usage error. Sends are guarded: without `--dry-run` or `--yes` the script refuses with exit 1 and never calls the API. Reads are bounded by `--limit` (default 20, max 100).

## Operating loop

1. **Scope the workspace surface**: which channel(s) are relevant, what the question is (what was said, who said it, when), and whether any action is a mutation.
2. **Read with bounds**: `channels list` to find IDs, `messages list`/`threads list` for history, `search messages` for cross-channel discovery. All read-only.
3. **Triage the answer**: map the question to evidence (thread replies for context, search for the exact phrase, files list for shared artifacts).
4. **Act with confirmation**: only a human directive to send, previewed with `--dry-run` and confirmed with `--yes`.
5. **Verify**: confirm the posted message `ts`/channel in the response, or for webhooks confirm the signature check result before trusting the event.

## Messages, channels, threads

- **Channels** (`conversations.list`): public and private channels, archived state, member counts. Channel IDs (`C...`) are the stable key for every other call — resolve names to IDs before use.
- **Messages** (`conversations.history`): newest-first history in a channel, one page at a time. Message records carry `ts` (the ID), `user`, and `text`. Use `--cursor` from the response metadata to page deliberately.
- **Threads** (`conversations.replies`): replies keyed by the parent `ts`; the parent message is the first result. Thread replies keep `thread_ts` set to the parent.
- **Sending** (`chat.postMessage`): the only mutation in this skill's surface. Always preview with `--dry-run`, confirm with `--yes`, and pass `--thread-ts` to reply in a thread instead of starting a new message. Verify the returned `ts` and channel.

## Search and files

- **Search** (`search.messages`): full-text search across visible history with Slack's search syntax (`from:`, `in:`, quoted phrases, `before:`/`after:`). Results include the matching channel; `total` tells you how many matches exist while `matches` stays bounded by `--limit`.
- **Files** (`files.list`): files shared in the workspace, filterable by channel or user, with permalinks and sizes. Downloading file *content* is out of scope for the CLI (bounded reads); use it to find the file, then fetch the permalink with an authenticated request when a human asks for the content.

## Webhook verification

Slack signs every HTTP request to your event/command/interactivity endpoints. To verify:

1. Take the raw request body (exactly as received — do not re-encode).
2. Check `X-Slack-Request-Timestamp` is within ~5 minutes of now (replay protection).
3. Compute `v0=HMAC_SHA256(signing_secret, "v0:" + timestamp + ":" + body)` and compare with `X-Slack-Signature` using a constant-time comparison.
4. Reject with 401 if the timestamp is stale or the signature mismatches.

`slack-cli webhook verify --body-file body.json --signature "v0=..." --timestamp <unix>` runs exactly this check against `SLACK_WEBHOOK_SECRET` (or `--secret`) and reports a constant-time-verified result. Always verify before trusting event payloads — unverified webhook endpoints accept forged events.

## Reference routing

| Load when | Reference |
|---|---|
| Sources, scope tables, refresh procedure | `references/00-source-index.md` |
| API method surface, pagination, scopes, and webhook verification details | `references/01-web-api-operations.md` |

## Included artifacts

- `scripts/slack-cli`: bounded, stdlib-only CLI (messages, channels, threads, search, files, webhook verify; `--json`; `--limit`; send gated by `--dry-run`/`--yes`).
- `tests/test_slack_cli.py`: 16 deterministic tests against a stub Slack API, including the mutation gate and the read-only contract.
- `references/`: dated source index + web API operations reference.
- `evals/evals.json`: six output-quality evaluation cases for agent runs.

## Verification boundary

| Claim | Minimum evidence |
|---|---|
| A channel exists and its name | `slack-cli channels list --json` returns it with its `C...` ID |
| A message was sent | `slack-cli messages send --yes` returns the new `ts` and channel, and `messages list` shows it |
| A search found matches | `slack-cli search messages --query "..." --json` returns `total_matches` with bounded matches |
| A webhook is authentic | `slack-cli webhook verify` exits 0 with `verified: true` for the exact body/signature/timestamp |
| A file exists | `slack-cli files list --json` returns its `F...` ID and permalink |

## Hard boundaries

- Never send a message or thread reply without a human directive, `--dry-run` preview, and `--yes` confirmation — Slack posts are public, durable, and unreadable-back.
- Never trust an inbound webhook without signature and timestamp verification.
- Never page reads past `--limit`; never dump full threads, tokens, or file contents into chat.
- This skill operates the Slack Web API. It does not build Slack apps (application development), manage users/org settings (admin console), or cover alternative channels platforms (that is their own tooling).

## When not to use

- **Building Slack apps or bots** (Block Kit, Bolt, slash-command apps, OAuth flow design) — that is application development; see [backend-engineering](../backend-engineering/SKILL.md) for service design.
- **Workspace administration** (user provisioning, deprovisioning, org-level settings, SSO/SAML, data exports at the org level) — that is the Slack admin console, not the Web API.
- **Other team-chat platforms** (Discord, Mattermost, Teams) — each has its own tooling; this skill covers Slack only.
- **Company-wide policy on messaging or channel governance** — that is organizational policy, not an API operation.
