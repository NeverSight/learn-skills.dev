---
name: extrovert-connect
description: Connect to Extrovert, choose access for setup or deployed workers, administer with explicit full control, and manage delegation, expiry, and revocation. Use for OAuth consent, enrollment, MCP host setup, identity or scope failures, and choosing event delivery.
metadata:
  version: "0.1.0-pre.25"
---

# Connect to Extrovert

## Check current guidance

On first Extrovert use in this session, after one hour (or a shorter returned freshness interval),
and after an unknown-tool or schema error, inspect the current tool catalog. Call `agent_context`
only if present; otherwise fetch
https://mcp.extrovert.dev/.well-known/agent-contract.json, then https://docs.extrovert.dev/llms.txt.
An installed or pinned CLI can run `agent status --json` if supported. Only when normal installation
policy permits an unpinned CLI, use
`npx --yes --prefer-online @extrovert.dev/mcp@next agent status --json`.
Read the live guide for current product behavior and use the host's current tool schemas. If a
schema remains stale, refresh the catalog or reconnect before continuing; inspect state before
retrying an uncertain mutation.

Compare this skill's `metadata.version` with its version in live context. A difference signals a
refresh to consider, not incompatibility, permission to downgrade, or authorization to install.
Preserve explicit pins, local edits, the installation manager, and scope; refresh only the installed
Extrovert skills when permitted. Updating files requires two separate reloads: reload each changed skill and read its complete updated `SKILL.md` body (not just metadata), then
restart changed local MCP processes or refresh hosted discovery. If a new session is needed, report
that pending step; use live guidance for this task. If freshness is unavailable, report
that condition without treating it as disabled signup or permission to guess new behavior. See
[updates](https://docs.extrovert.dev/operating/agent-updates/) for targeted refresh instructions.

## Ordinary setup uses limited access

Read https://docs.extrovert.dev/quickstart/install/ for the common installation flow.
A console handoff means the human already has an account. Reuse working credentials
or resume pending setup. Missing local credentials are not evidence of a new customer;
ask about account intent when unknown. Do not create a replacement account.
Recommend Dedicated agent, Selected inboxes, and Read and send for an email agent.
The person selects the named agent and exact inboxes. Identity, reach and actions
are independent; Personal assistant can also be narrow. For inbox creation, request
suitable project/organization reach and mailbox:create, not full account control.
Full account control is only for explicitly requested administration. Never request
it merely to install, reconnect, troubleshoot visibility, or send a first message.
Native hosted OAuth and local CLI login are alternatives, not two required logins.
For a connection-only request, verify access and offer a first email; do not send one
without authorization. Resume existing authorized reviews under the same composer.

## Connect in this order

1. Read live context as above. With no Extrovert MCP, fetch the HTTPS contract; do not call
   unavailable `agent_context`. This read needs no account or MCP installation.
2. Check this host for Extrovert tools. If absent, run the supported setup command below when
   installation is allowed. Follow its host-selection or native-command handoff in this same host.
3. Complete authentication: setup only configures MCP. A pending signup takes precedence over browser login: resume `check_activation` and `verify_signup` after proof for incoming email, or `verify_signup` with the human-supplied code for legacy OTP. The CLI equivalent is `extrovert verify`. Do not start `auth login` or OAuth for that pending profile. Otherwise follow its returned native sign-in command
   or host OAuth action (Claude Code: `/mcp`). Have the person sign in to the existing account and
   approve access before `whoami`. Local stdio/CLI uses `extrovert auth login`; this does not
   authenticate the host's separate hosted OAuth connection.
4. Reload the MCP connection when required and call `whoami` in that actual session before work.
   For CLI-only work, use its `whoami`. Saved configuration or pending login is not connected.

```bash
npx --yes --prefer-online @extrovert.dev/mcp@next setup --host auto
```

Automatic selection prefers hosted MCP. If selection is ambiguous, choose the intended host
explicitly with `--transport hosted`; an explicit host without a transport retains the stdio default.
Preserve existing server entries and profile credentials. Installing a skill alone does not configure
MCP. Do not build a custom JSON-RPC transport or install a similarly named product.
See [host setup](https://docs.extrovert.dev/mcp/client-configuration/) for exact adapters and plugins.

For local access, use `npx --yes --prefer-online @extrovert.dev/mcp@next auth login`.
Without an interactive terminal, use `auth login --no-browser --json`, show the returned
`authorization_url` when pending, then run `auth complete --json` in the same profile with the
website's completion code on private stdin. Never put the code in arguments, chat, or logs.
Follow [current login guidance](https://docs.extrovert.dev/quickstart/authentication/#local-cli-and-stdio-sign-in)
for browser fallback, cancellation, existing credentials, and recovery. A completion code is not an
access token or proof that login succeeded; verify the completed connection.

If configuration is not writable, report that exact blocker and use the packaged CLI as the explicit
fallback. Never create a second account or replace an existing identity to repair access. Read live
signup availability before offering account creation.

## Choose credentials

- Connect to the human's existing account. If no account or credential is available, use the
  new-account flow below only when live signup availability is enabled and account creation is intended.
- Hosted OAuth (recommended for interactive setup): connect to `https://mcp.extrovert.dev/mcp` and
  follow browser sign-in and explicit consent. Choose Personal assistant or a named Dedicated agent;
  select inboxes (default), a project, an organization, or Full account control. Choose actions separately.
  Selected inboxes exclude future inboxes. Project and organization reach include future resources
  within the chosen boundary. Sign-in alone never grants access.
  Full account control is an explicit setup option: it can administer customer resources, access
  other agents' inboxes, approve requests including its own, and create independent credentials.
  It expires after 24 hours by default; Until revoked is an explicit alternative. Refresh does not
  extend that deadline. Created credentials, including admin credentials, survive independently.
  Private platform access is always excluded. Existing hosted OAuth sessions must reconnect through
  consent; do not infer broader permissions from their old display name.
- Local CLI/stdio OAuth: `auth login` signs in to an existing account and saves a separate local
  connection. Refresh respects the granted identity, reach, actions, and expiry. Hosted MCP OAuth
  remains managed by the host; do not copy its tokens into local API credentials.
- Enrollment token: prefer `npx -y @extrovert.dev/mcp@next enroll --agent-handle <stable-name>`.
  It accepts hidden stdin or `EXTROVERT_ENROLLMENT_KEY`, saves the scoped agent key privately, and checks
  identity. Keep the same handle and `--client-id` on a retry. With tools already connected,
  `redeem_enrollment` also stores the returned key in the packaged local stdio server.
- Existing agent key or independently issued connection credential (`ev_credential_...`): use `npx -y @extrovert.dev/mcp@next auth login --with-token` and hidden stdin.
  Never put a key in a command argument or repeat it in a response.

Set `EXTROVERT_PROFILE` before login, enrollment, and setup to separate agent identities. Hermes uses its
selected `HERMES_HOME` automatically. `EXTROVERT_CONFIG_DIR` explicitly overrides both. Do not copy a
global credential into a different profile or replace an existing identity to make a login succeed.

Set the API base URL to `https://api.extrovert.dev`. `EXTROVERT_API_KEY` overrides the local stored
credential when an explicit key is needed. Use the scope the human chose. A persistent administrator
credential is a deliberate full-control choice, not a routine workaround for a failed inbox list.

The MCP prerelease is published under the explicit `next` dist-tag. Prefer the hosted stateless
Streamable HTTP endpoint and OAuth when the client supports remote MCP. For an unpinned local stdio
host, run `npx --yes --prefer-online @extrovert.dev/mcp@next`; preserve deliberate version pins.
Supply only the agent key or independently issued connection credential intended for that worker.

## New accounts and human verification

Read `signup.status` from live context: `enabled` permits offering self-signup; `disabled` means use
the console or an enrollment invitation; `unavailable` means the check failed, not that signup is
enabled. Do not loop on signup errors. Use the current onboarding guide to resolve status.
For bootstrap without an existing credential, use the packaged local stdio server or CLI's `signup`
and `verify` commands; hosted OAuth signs into an existing console account. Inspect installed CLI
help for its exact inputs and preserve any existing profile rather than replacing it.

In an interactive session, obtain the human's email if it is not already supplied and use `sign_up`
only for the intended new account. Follow the activation method returned by signup. In an unattended worker,
use the human email supplied by its authorized setup; never invent one. Prefer an already issued
scoped credential or enrollment token for unattended work. If human verification is needed, retain
the pending state and report the human action through the configured interaction channel. Do not
promise to wake up later without a running task, or send a separate email without authorization.

When `activation_method` is `incoming_email`, signup reserves the inbox for 24 hours. Keep the
limited key and tell the human: “Send an email from {human_email} to {address} to activate your
agent's inbox and link it to your human email.” Use the returned addresses; any subject or body works.
Give the human these instructions before waiting. While the session is active, call
`check_activation` with `wait_seconds: 55`, repeating pending waits for up to five minutes.
A timeout preserves the reservation; explain how to resume with the same profile. If the human
says they sent it, check immediately. Only after `proven`, call `verify_signup` without an OTP.
If a resumed `whoami` has only `signup:verify`, finish this same exchange first, even when a practice review already exists. Use `check_activation`, then `verify_signup` after proof; the CLI equivalent is `extrovert verify`. Missing mail permissions at this stage do not require OAuth, broader access, or a full host restart.
No verification email is sent to the human in this flow. Do not ask them to find a code or try to
read the pending inbox. Its key cannot read or send mail, export messages, or configure forwarding
or webhooks. A reservation is not a verified account or a sent first message.

A mismatched sender does not replace the expected human. Before proof, to correct a typo, use
`correct_activation_email` with the current revision, then request a fresh matching email; the
original expiry stays fixed. A verified matching console login with explicit approval is an
alternative. Existing account owners enroll agents through their console.

For a **legacy response that actually issued an OTP**, use the human-supplied code with
`verify_signup` before its original expiry. If that verification email is missing, confirm the
returned destination and suggest **Spam or Junk**. Use the returned sender or signup `address`,
not a guessed no-reply address. Consult the current response and recovery guidance before a resend;
do not assume another signup issues an OTP or extends the reservation.

Preserve the same profile and pending account throughout. Successful verification exchanges the
temporary key for a durable credential; check `whoami` afterward before mailbox work. Never create
a different account or bypass activation to recover missing mail.

Signup accepts `display_name` separately from the address `username`. Preserve the human's chosen
sender name; omit it for the validated Agent {username} default. Show the actual returned sender,
plan, console URL and onboarding guidance after verification. Verify `whoami` in the actual host.
The packaged local stdio process and CLI share both the pending and durable credentials in the
selected profile. An explicit environment key still overrides that profile. In Hermes, continue
through the packaged CLI during initial setup while native MCP discovery is pending. Incoming
CLI `signup` displays the instructions and watches for up to five minutes, completing verification
when proof arrives. `verify --wait-seconds 300` resumes that bounded watch. Do not require a human
“I sent it” nudge or a full Hermes restart. Keep your agent turn active until the terminal command completes: a background CLI process cannot resume your conversation. If the host returns a running process ID, use its process polling tool to read completion, then continue with whoami and the practice review. Do not end the turn by promising that a background watch will continue the review for you. Hermes can reload MCP configuration while idle;
`/reload-mcp` is its manual fallback. Verify MCP `whoami` when the tools become available; CLI
identity alone only verifies the CLI connection.

Extrovert automatically prepares one deliberately fluffy practice draft when ownership proof is
accepted, even if the agent is offline. The draft belongs to this agent; the system template is
identified separately. Recover `onboarding.starter` from verification or `signup_starter` from
`whoami`. Use its exact review ID/path/status, `list_reviews` with `composer: "me"`, and
`list_review_events`. A `preparing` status means check again shortly, not submit another hello.
Do not create a second message. Historical signups without this handoff keep their ordinary
first-send flow; recover existing work before using `client_id: "signup-hello:<agent_id>"`.

Load `extrovert-send-email` and `extrovert-writing-rules`. Show the review link and explain that
Extrovert prepared a practice draft the human can approve, edit, or coach. Offer this optional
copyable feedback: “Save an Extrovert writing rule for all our messages: never use em dashes.
Revise this draft to follow that rule, too.” This example is not permission to save a rule.
When the human submits it in the review discussion, use `learn_review_rule` with its authenticated
`source_turn_id`, `target: "org_house"`, and `kind: "hard"`. Read back the persisted rule, confirm
its scope, get fresh writing rules and revise this SAME draft. One-message edits do not become
house rules automatically. Continue the review event loop until sent or terminal.

When Hermes's native tools are not available yet, the packaged CLI exposes the same schemas and
handlers: `extrovert tool describe <tool-name>`, then `extrovert tool call <tool-name> --input-stdin`
with the described JSON on stdin. Use it for review recovery, event waits, feedback, rule learning,
readback and revisions without writing a custom transport or blocking on a full host restart.

Close setup by briefly explaining the connection's actual agent-scoped permissions from `whoami`.
Tell the human they can sign in to Extrovert and ask the agent to help explore capabilities for
them and their agents. Broader administration requires explicit consent; never silently widen
this connection. Link [Connections and access](https://docs.extrovert.dev/concepts/connections-and-access/).

## Verify immediately

Call `whoami` in the actual MCP session before real work. Lead with its summary, account/project names
and available capabilities, not opaque IDs or raw scope names. Keep the fixed `org_id`, `project_id`,
key tier, connection ID, reach, expiry, and scopes for authorization checks. A project-bound key
cannot switch projects. A broader connection may explicitly select a project within its granted reach.

`doctor` checks a local credential against the API; it does not prove the host's OAuth session works.
Use CLI `whoami --json` to verify local access without opening, reading or printing credential
files or any key/token fragment. The CLI reads its saved profile privately.
If browser approval succeeds but MCP returns 401, stop repeated approvals, preserve only the error
and non-secret request ID, and report the failed step. A login process exiting zero or a callback
returning 200 does not prove tool access. Do not suggest SSH tunnels or broader keys as a speculative
repair. Offer the supported enrollment path only with the human's chosen permissions.

## Administer with explicitly granted full control

Use `list_administrative_actions` to search the task, then `describe_administrative_action` for exact
`path`, `query`, and `body` inputs. Start `read_administrative_action` with `action_id: "adminMe"` to
find the current organizations and projects. Use `change_administrative_action` for an authorized
change; ordinary inbox/send scopes do not enable it. Changes are attributed to the connection,
not to a human click. Read state after an ambiguous result before retrying a mutation.

For the packaged CLI, use `extrovert admin actions`, `admin describe <action-id>`,
`admin read <action-id> --input '<json>'`, and `admin change <action-id> --input-stdin`.
Pipe change JSON from a private file or application, rather than putting credentials in shell history.
The TypeScript SDK exposes the same catalog as `client.administration.list/describe` and typed
`client.administration.call(actionId, input)`.

Use Connections to inspect the parent connection and the access it created. Revoking the parent
or reaching its 24-hour expiry does not revoke independent credentials. Revoke each unwanted
credential separately. Never repeat a returned raw credential in a user-facing explanation.

## Finish setup and hand off

For an authorized setup task, use full control to configure the requested resources, then give
workers their own identity and resource/action scope. Use enrollment to create an agent, an agent
key for an existing agent, or a separately consented connection for selected/shared inbox access.
Inspect the administrative catalog for exact credential-issuance inputs; never guess IDs or print
one-time secrets. Full control does not mean every worker needs an administrative credential.

Verify `whoami` and the intended inbox list in each worker's actual runtime before ending setup.
Review the parent's created credentials in Connections and revoke unwanted access separately.
End the setup connection when finished or let its fixed deadline expire. Settings, webhooks,
exported credentials, and independent keys can outlast it; expiry does not undo setup.

Independent `ev_credential_...` credentials work with the API and packaged stdio/CLI. They are
not hosted MCP bearer tokens. Hosted MCP uses its own OAuth audience or a scoped agent key.
Read [Connections and access](https://docs.extrovert.dev/concepts/connections-and-access/) for the
complete human-facing walkthrough.

## Explain domain readiness

Use `get_domain` or `extrovert domain status <domain>`. Present `readiness.label` and `summary` first.
Never infer readiness from `verified`, DKIM, delegation mode, or zero deliverability findings.
When `ready_for_inboxes` is true, say the domain is ready to use. Explain the visible inbox count:
offer inbox creation when zero, or use of existing ready inboxes. Counts are scoped; never claim that
zero visible inboxes means the entire account has none. Creation still needs permission and capacity;
sending follows the inbox's review policy.

If the customer must act, show the DNS entries and offer `verify_domain` / `domain recheck` after they
add them. If Extrovert must act, say the customer's entries are confirmed only when the summary says
so; do not ask for more DNS changes. Use `wait_for_domain` / `domain wait` for a bounded check. A
`timed_out` result is not a setup failure: resume after `resume_after_seconds`.

Save `list_domain_events.next_cursor` and pass it as `after` for the same domain, including after a
restart. Drain `has_more`, otherwise wait `poll_after_seconds`. Summarize new ready, action-needed or
recovered events for the human. Extrovert emails verified account administrators, but polling cannot
wake a disconnected agent. Do not promise a future agent update without an active host task.

## Use the intended inbox

After `whoami`, use `list_inboxes` and select the intended inbox, or create one if the user requested it:

1. Call `read_messages` with that inbox. It already returns readable previews and structured
   message fields.
2. Pass a returned `msg_…` id to `get_message`. Use `format: "text", variant: "extracted"` for concise
   reading; use `variant: "source"` when exact MIME text, signatures, or quoted history matter.
3. Call `wait_for_email` with the same inbox when waiting for a new reply, OTP, or verification link.

Do not download response files, construct REST routes, or invoke `jq` for ordinary MCP mailbox work.
Raw HTTP is a last fallback for a runtime that genuinely supports neither MCP, the packaged CLI, nor
an SDK; missing MCP configuration is not a reason to write transport code. Before sending or
replying, load `extrovert-send-email`; outbound mail is governed by the inbox review policy.

Common scope failures are explicit:

- create inbox: `mailbox:create`
- read inbox: `mailbox:read`
- export raw IMAP/SMTP credentials: `mailbox:credentials` plus a paid plan (free accounts cannot export them)
- outbound and review work: `mailbox:send`
- change daily limit: `mailbox:quota`
- read domain readiness and events: `domain:read` or `domain:manage`
- connect domains, recheck DNS, or offboard: `domain:manage`
- webhook management: `webhook:write` (legacy keys may use `mailbox:read`)
- quote or request a domain purchase/plan change: `commerce:request` (never approval authority)
- reviewer actions: `review:act`

A 401 means the credential was absent or rejected. A 403 means the credential is known but its tier, scope, ownership, or project ceiling does not authorize the action. Do not retry either with broader guessed identifiers.

For commerce, `quote_domain` is non-spending. `request_domain_purchase` and `request_plan_change`
create durable requests; they do not approve or execute them. Recover and poll with
`list_commerce_requests` and `get_commerce_request`, or withdraw the agent's own pending request with
`cancel_commerce_request`. Surface the platform approval URL and exact
blocker to the human. Extrovert sends the billing owner a notification automatically, but email
content and replies cannot authorize a charge. A signed-in console decision, explicitly delegated full-control administrator, or bounded policy
created by an authorized administrator can do that.

## Choose event delivery

- Poll ordinary mail with `read_messages`, read a returned id with `get_message`, or block on a new
  matching message with `wait_for_email`.
- Use `register_webhook`, `list_webhooks`, `get_webhook`, `update_webhook`, and `delete_webhook` for signed callbacks.
- Call `stream_info` before using SSE; reconnect using the documented cursor.
- Review events remain durable. Webhooks and streams are accelerators, not replacements for `list_review_events` plus acknowledgement.

Keep keys out of shell history, source files, issue text, and logs. Rotate a credential that may have been exposed.

Use `agent-email-architecture` when the task is choosing a topology or reviewing trust boundaries, and `extrovert-sdk` for direct TypeScript integration.

## Resume outstanding sends

When an outbound task resumes, recover existing authorized sends before creating anything new. An ambiguous request for “feedback” calls for distinguishing review feedback from inbound replies and continuing authorized sends; explicit inspection-only requests permit reads only.

After confirming identity, drain `list_review_events` and use `list_reviews` with
`composer: "me"` to recover this agent's pending sends. Load `extrovert-send-email` when
there is work. A user request to send remains in progress through human feedback and
revision: keep one `wait_for_review_event` (55 seconds, no review_id) active until confirmed
sent or an unsuccessful terminal outcome. Do not require the user to nudge each step.

### Storage and connection diagnostics

Storage warnings are structured from 90% usage. Mention cleanup or asking the human
for more space when first warned, when pressure increases, or when an operation is
blocked. Do not repeat upgrade suggestions on every mail read. Reads and deletion
remain available when storage is full.

When comparing a hosted OAuth connection with a local CLI profile, call `whoami`
through each separately and retain the stable agent/key IDs and scope fields.
A successful CLI health check does not establish the hosted connection’s identity.
If direct inbox lookup succeeds while its complete list is empty, treat that as a
possible contract/authorization inconsistency, not proof that addresses are hidden
by a special list permission. Report the actual results and request IDs.


## Explicit connection grants

When `whoami.auth_method` is `connection`, use `whoami.connection` as the consent
record: identity, selected resource reach, granted actions, fixed expiry, and any
creator connection. A Personal assistant acts for the authorizer; a Dedicated
agent retains its selected identity. Switching the console's default project does
not change either grant. Read the supported breadth from this response rather
than applying an agent-key ownership assumption.

Selected inboxes excludes future inboxes. Project and Organization grants include
future resources inside their named boundary. Full account control explicitly
permits customer administration, other agents' inboxes, policy/access changes,
credential creation, and approvals including its own requests. It never includes
private platform-operator access or exceeds the authorizer's current role.

Full control expires after 24 hours by default; Until revoked is an explicit
alternative. Refresh does not extend the grant. Created credentials, including
administrative credentials, survive independently. Explain that distinction when
helping someone set up workers. Never switch to a created credential silently to
continue after the parent expires. Point the person to account → Connections to
inspect and separately revoke created access.

Legacy hosted sign-ins need one new consent flow after the grant-system rollout.
Reconnect through the host; do not retry old tokens, invent resource permissions,
or infer that a local CLI credential represents the same connection.
