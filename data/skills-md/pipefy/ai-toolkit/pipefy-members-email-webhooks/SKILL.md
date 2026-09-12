---
name: pipefy-members-email-webhooks
description: >
  Use this skill when the user wants to manage pipe membership, send or read
  card inbox emails, use email templates, or manage webhooks. Covers 12 MCP tools.
tags: [pipefy, members, email, webhooks, inbox]
---

# Members, Email & Webhooks

Manage pipe membership, send emails from card inboxes, read inbox replies, and manage webhooks. **12 MCP tools.**

---

## Member management

| Tool (MCP) | CLI | Read-only | Purpose |
|------------|-----|-----------|---------|
| `invite_members` | `pipefy member invite` | No | Invite one or more users by email + role. |
| `add_service_account_to_pipe` | `pipefy member add-service-account` | No | Attach an existing org **service account** to a pipe by email + role (iPaaS setup). Verifies membership afterwards. |
| `remove_member_from_pipe` | `pipefy member remove` | No | **Two-step destructive.**[^mcp-confirm] Verifies afterwards and warns if the member is still present (org-level permissions can override pipe removal). |
| `set_role` | `pipefy member set-role` | No | Change a member's pipe role (`member_id` = user id). |

List existing members with `get_pipe_members` from [skills/pipes-and-cards/pipefy-pipes-and-cards/SKILL.md](../../pipes-and-cards/pipefy-pipes-and-cards/SKILL.md). Id forms: [`docs/mcp/tools/identifiers.md#members-email-webhooks`](../../../docs/mcp/tools/identifiers.md#members-email-webhooks).

### Steps — invite members

1. **Check existing members:**

   MCP: `get_pipe_members pipe_id=67890`

   CLI: `pipefy member list --pipe 67890`

2. **Invite new members:**

   MCP: `invite_members pipe_id=67890 members='[{"email":"alice@example.com","role_name":"member"},{"email":"bob@example.com","role_name":"admin"}]'`

   CLI: `pipefy member invite --pipe 67890 --email alice@example.com --role member`

   > Before inviting **external emails** (domain different from the org's known domains), warn the user that this is an external invitation and confirm before proceeding.

   > Before granting **admin role**, confirm with the user — admin is the highest pipe-level role.

### Steps — add a service account to a pipe (iPaaS setup)

When setting up an iPaaS (Advanced Automations) flow that runs under a **service account**, the account must be a member of the target pipe, or pipe-scoped calls under its identity fail with a permission error even though the flow looks configured.

1. **Get the service account's email.** Either create one with `create_service_account(organization_uuid, name, role)` — which returns the account's email plus its OAuth2 client secret and token endpoint **once** (store them immediately) — or take the email from your organization's service-account settings. A freshly created account has no pipe access until this step. The pipe role defaults to `admin` (a service account running automations usually needs full pipe access); pass a narrower role only when you deliberately want to limit it.

   > One-step alternative: `create_service_account(organization_uuid, name, role, pipe_ids=[...])` provisions the account **and** adds it to the given pipes in one call, returning a `pipe_memberships` summary. Use it when you already know the target pipes.

2. **Attach it** (when not using the `pipe_ids` shortcut above):

   MCP: `add_service_account_to_pipe pipe_id=67890 email=svc-automations@your-org.pipefy-service.com` (role defaults to `admin`)

   CLI: `pipefy member add-service-account --pipe 67890 --email svc-automations@your-org.pipefy-service.com`

   The **MCP tool** verifies membership afterwards: it returns an error if the account is not a member of the pipe once the invite is processed, so an incomplete setup is not reported as success. The **CLI** does not verify — it prints the raw invite result, so check `inviteMembers.errors` (or run `pipefy member list --pipe <id>`) to confirm the account was actually added. This attaches an existing service account — create one first with `create_service_account` if you don't have one, and delete a throwaway with two-step `delete_service_account` (echo `confirmation_token`) when done. See [docs/mcp/tools/service-accounts.md](../../../docs/mcp/tools/service-accounts.md).

---

## Email (card inbox)

| Tool (MCP) | CLI | Read-only | Purpose |
|------------|-----|-----------|---------|
| `get_card_inbox_emails` | `pipefy email inbox list --card <id>` | Yes | Read emails in a card's inbox. |
| `send_inbox_email` | `pipefy email inbox send` | No | Send an email from a card inbox. |
| `get_email_templates` | `pipefy email template list --repo <id>` | Yes | List templates for a pipe or table (`repo_id` numeric). |
| `send_email_with_template` | `pipefy email template send` | No | Send using a template (`email_template_id` from that list). |

> **Templates are UI-only.** Creating, editing and deleting an email template has no API, MCP or CLI path: the GraphQL schema has no template CRUD mutation. The template must already exist before a flow can send with it. When the process needs a new or changed template, put the manual Pipefy UI step in the plan you give the user instead of promising an end-to-end email flow.

### Steps — send a card inbox email

1. **Get the card's inbox emails** (see what has been received):

   MCP: `get_card_inbox_emails card_id=12345`

2. **Send a reply:**

   MCP: `send_inbox_email card_id=12345 to="customer@example.com" subject="Your request is in progress" body="Hi, we are processing your request."`

   CLI: `pipefy email inbox send --card 12345 --to customer@example.com --subject "Your request is in progress" --body "Hi, we are processing your request." --from-email you@example.com`

---

## Webhooks

| Tool (MCP) | CLI | Read-only | Purpose |
|------------|-----|-----------|---------|
| `get_webhooks` | `pipefy webhook list --pipe <id>` | Yes | List all webhooks for a pipe. |
| `create_webhook` | `pipefy webhook create` | No | Register a new webhook endpoint. |
| `update_webhook` | `pipefy webhook update <id>` | No | Change URL, headers, or events. |
| `delete_webhook` | `pipefy webhook delete <id>` | No | **Two-step destructive.**[^mcp-confirm] |

[^mcp-confirm]: MCP two-step: echo `confirmation_token` from the preview with `confirm=true`. CLI: `--yes`.

### Steps — create a webhook

1. **List existing webhooks:**

   MCP: `get_webhooks pipe_id=67890`

   CLI: `pipefy webhook list --pipe 67890`

2. **Create the webhook:**

   MCP: `create_webhook pipe_id=67890 url="https://your-server.com/pipefy" actions='["card.create","card.done"]'`

   CLI: `pipefy webhook create --pipe 67890 --url https://your-server.com/pipefy --events card.create,card.done`

---

## Success criteria

- Invited members appear in `get_pipe_members`.
- Sent emails show in the card's inbox thread.
- Created webhooks receive test payloads from Pipefy on the configured events.

## Failure modes

- **`invite_members` fails with "user not found":** verify the email address is correct.
- **`send_inbox_email` fails:** the card must have an inbox enabled in the pipe settings.
- **Webhook never fires:** verify the pipe events match the configured `actions` list; check that the endpoint URL is publicly reachable (not localhost).
- **`delete_webhook` first call returns preview:** expected. Show the preview to the user and get their approval, then call with `confirm=true` and the preview's `confirmation_token`.

## See also

- `skills/pipes-and-cards/` — create the pipe and cards before managing membership.
- `skills/observability/` — monitor email and webhook delivery logs.
- [skills/ipaas/pipefy-ipaas/SKILL.md](../../ipaas/pipefy-ipaas/SKILL.md) — when a flow's service account needs pipe membership.
