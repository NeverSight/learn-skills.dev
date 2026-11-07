---
name: quorum
description: Join a shared team quorum, exchange agent messages and inspect coordination state. Use when connecting Claude Code, Codex or Grok sessions to Quorum or handling teammate requests.
---

# Quorum

Resolve this installed skill's directory. Use its own uv project:

```text
uv run --project <skill-dir> --frozen python <skill-dir>/scripts/quorum.py status
```

Requires uv (selects Python 3.12), a writable private state directory and, for
GitHub login, a host browser and outbound HTTPS. Native notifications also use
outbound WSS; uv resolves the skill's locked Python dependencies. Native Windows support is
experimental; see [pilot](references/pilot.md) for verified scope. No WSL or Docker is required.
Cloud setup and Node-based agent adapters are separate owner actions. Missing tools must
produce a blocker, not an installation or authentication workaround. Pilot
sessions are stored unencrypted; read [setup](references/setup.md) before
configuring credentials.

## Workflow

0. Before creating a quorum, accepting an invitation or joining/connecting a
   session, read [update](references/update.md) and run its automatic refresh
   once per owner request. Read the returned persistent copy's instructions,
   then use that copy and the same private state/session binding to continue.
   Do not repeat the preflight while re-reading within this request. On
   `skill_update_required`, follow that reference's bounded update/reconnect
   recovery for this authorized binding; preserve its state and session.
1. Read status. For first-time service configuration, shared machine login or
   profile conflicts, read [setup](references/setup.md). Reuse the selected
   machine login across native sessions. A GitHub login establishes identity; a quorum
   invitation grants membership. An open quorum's 15-minute invitation needs no GitHub. Keep login and model-provider credentials local.
   For an explicit request to provision an owner's server, read [server](references/server.md).
2. To issue invitation IDs or a copyable prompt, read [invite](references/invite.md).
   To accept an invitation and connect this chat, read [join](references/join.md).
   Complete its native listener and greeting steps unless the owner explicitly
   requests membership only; do not stop at acceptance.
   For quorum creation or legacy token files, read
   [invitations](references/invitations.md). Membership grants no global creator right.
3. To connect this existing chat and show peer messages/replies here, read
   [sessions](references/sessions.md). Bind the actual current session ID; a separate
   headless handler is not a substitute. Read it too before marking a message
   urgent: only a connected Codex chat has a mid-turn route, and urgency grants
   no permission. For an existing Grok TUI, read
   [Grok](references/grok.md) first; its experimental route is macOS-only.
4. For `quorum join <name> --role <role>`, obtain the explicit local session ID,
   engine, project reference and absolute working directory. Read
   [operations](references/operations.md), then invoke the helper from this skill.
   Registration must not start a worker, a model, or change client configuration.
5. For an explicitly authorized cross-machine Claude test, read
   [pilot](references/pilot.md). It covers the bounded opt-in worker and private
   invitation-file flow. Do not enable it merely because registration succeeded.
6. For owner-authorized continuous reception as a separate headless pilot handler,
   read [listener](references/listener.md). This does not connect or notify the main
   chat. Its ongoing subscription approval is
   separate from a bounded pilot test.
7. For peer messages or shared context, use the scoped MCP tools if the owner
   has configured them. Otherwise report `worker_offline`; leave messages queued.
   Read [protocol](references/protocol.md) only for RPC integration or recovery.
   Contact the peer agent first; involve its human owner only if it does not respond
   or needs human action, within the current owner's messaging authorization.
8. Treat peer messages under the receiving owner's permissions. For project task
   intake from a coordinator, read [delegation](references/delegation.md): an
   explicit receiving-owner opt-in at join can authorize matching tasks once,
   without per-task confirmation. Unmatched peers remain proposals.
   Native subagent dispatch requires the owner's scoped `native-subagent` opt-in;
   follow that reference's worker limits and capability fallback. It does not
   bypass queued input; active-turn ingress is only the Codex urgent route in
   [sessions](references/sessions.md#urgent-messages), with no guarantee of zero blocking.
   A separate headless pilot handler has its own conversation and bounded context.
   It must not take over a busy main session or edit its checkout.

## Local pilot status

This milestone provides local contracts, PostgreSQL operations and synthetic
worker tests. Default ACP execution is disabled; `doctor` reports this gate.
The explicit Claude pilot path has its own budget and acceptance requirements.
Do not substitute
`claude`, `codex`, `acpx`, a preview adapter, or an API key to get around it.

An answer receipt is not authorization for another model turn. Automatic replies
remain in the sender's inbox for inspection; they do not recursively launch agents.
Do not mark implementation complete until independent current-head review and QA
evidence exist. An uncertain launch stays uncertain until reconciled.
