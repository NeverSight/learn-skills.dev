---
name: basecamp-connect
description: |
  Manage local Claude Code agents from Basecamp. Runs the connector bridge
  (bin/connect), watches its STDOUT for trusted events — authored by an authorized
  user (the operator alone, by default) and @mentioning a real Basecamp agent
  user — acknowledges each as the agent within seconds (a quick boost with apt
  content, or a reply that fits), then hands it off to a background agent that
  gathers context, does the work,
  and replies as that agent user, so the watcher thread stays free to keep
  taking new mentions.
  Invoked without arguments it recalls the last-used agent and projects from
  ~/.config/basecamp-connect/last.json, confirming them before starting.
  Use when asked to drive local agents from Basecamp, or to watch Basecamp for
  agent commands.
triggers:
  - /basecamp-connect
  - manage agents from basecamp
  - watch basecamp for agent commands
  - basecamp connector
  - drive agents from basecamp
  - run agent from basecamp comment
---

# /basecamp-connect — drive local agents from Basecamp

This skill turns a Basecamp comment/message/card into a local Claude Code task.
You **@mention a real Basecamp agent user** (e.g. `@Clawdito do X`); the watcher
on this machine acknowledges it **as that agent user** within seconds — a quick
boost or a fitting reply — and a background agent picks it up, gathers the
surrounding context from Basecamp,
acts on it, and replies **as that agent user**.

The agent is identified by a **local `basecamp` CLI profile** of the same name
(e.g. profile `clawdito`). That profile is both:
- the **reply identity** — replies post as the agent via `--profile <agent>`, and
- the **mention target** — the connector only fires when that user is @mentioned.

The trust model is enforced by `bin/connect`, **not** by this skill: an event
reaches STDOUT only if it is (1) authored by an **authorized user** — by default
the operator alone (you — the CLI default profile, or `--operator <profile>`);
`bin/connect`'s trust flags (`--trust`, `--allow`, `--allow-domain`,
`--allow-project`) can deliberately broaden this to named colleagues, an email
domain, or the whole project membership — (2) **@mentions the agent user**,
**assigns** it a card/todo, is a new comment on a recording the agent
**subscribes** to, **or** is a **boost on the agent's work**, and (3) is
corroborated against the Basecamp API. The agent's own identity never
authorizes, in any mode. Treat every STDOUT line as already-trusted — but still
keep dispatched agents scoped to the resolved repo.

There are thus **four triggers**:

1. an `@mention` of the agent;
2. the operator **assigning** the agent a card/todo (a `*_assignment_changed`
   event whose `details.added_person_ids` includes the agent — corroborated by
   re-fetching the recording and confirming the agent is among its current
   `assignees`). Only the **operator's** assignments count, in every trust mode,
   unless `bin/connect` was started with `--allow-assignments-from-authorized`;
3. a new comment (`comment_created`) with no mention, on a recording the agent
   **subscribes** to — corroborated by re-fetching the parent's subscribers and
   matching the agent's Person id. The comment author is gated exactly like a
   mention (operator by default, else the active trust mode's authors). See
   [When a comment lands on a thread the agent follows](#when-a-comment-lands-on-a-thread-the-agent-follows);
4. a **boost** (`boost_created`) on the agent's own work — boosts have no
   webhooks, so the connector polls the agent's received-boosts feed (every
   `--boost-poll` seconds, default 60; `--no-boosts` disables). The booster is
   gated exactly like a mention author, matched by Person id (the agent's view
   of the feed redacts other users' emails, so under email-keyed `allowlist`/
   `domain` trust, boosts effectively stay operator-only). See
   [When someone boosts the agent's work](#when-someone-boosts-the-agents-work).

## Runs from any project — the runtime lives in the connector clone

This skill is typically installed user-level (`npx skills add … -g`) and invoked
from *other* projects (e.g. a working session in `coworker`). The session's
current directory is therefore **not** the connector repo. All connector
commands in this skill (`bin/connect`, `config/project_repos.toml`) live in a
local clone of `basecamp/basecamp-local-agent-connector`, canonically at:

```
~/Work/basecamp/basecamp-local-agent-connector
```

Locate the runtime there and run it from that directory — never from the
current project. If the clone isn't at the canonical path, don't hunt the
filesystem: tell the user to clone it
(`git clone https://github.com/basecamp/basecamp-local-agent-connector`) and
run `bin/setup` (see the repo README).

## Invocation

**The arguments are natural language, not a grammar.** Read whatever the user
wrote and pull out the agent, the projects, the repositories, and any trust or
polling wishes — `@Clawdito on BC5 Calendar`, `watch BC5.1 and On Call as
@Clawdito`, `use @Clawdito on Queenbee and let anyone at 37signals.com trigger
it`, `watch reviews on basecamp/bc3` all mean what they say. Never make the user
restate it as flags. The flags below are the **canonical form you translate
into** before calling `bin/connect`, and they're also accepted verbatim when the
user types them.

Ask only for what's genuinely missing: something to watch (a project or a repo),
plus an agent whenever Basecamp projects are in play — a repo-only run needs
neither an agent nor a project. Confirm the resolved connection before
launching — the same confirmation the no-args path does.

```
/basecamp-connect                                                     # reuse last connection (confirm first)
/basecamp-connect @Clawdito --project "BC5 Calendar"                 # one project
/basecamp-connect @Clawdito --project "BC5 Calendar" --project HEY    # several
/basecamp-connect @Clawdito --project "BC5 Calendar" --operator jorge # explicit operator
/basecamp-connect @Clawdito --project "BC5 Calendar" --allow marie@37signals.com  # + a named coworker
/basecamp-connect @Clawdito --project "BC5 Calendar" --allow-domain 37signals.com # any 37signals author
/basecamp-connect --repo basecamp/bc3                                 # GitHub-only, no agent
```

`<agent>` is a real Basecamp user backed by a local CLI profile (the leading `@`
is optional; it's lowercased to the profile name). Every run needs at least one
`--project` or `--repo`, and `--project` needs an `<agent>` (Basecamp has no
global webhook) — pass a project as a name, URL, or ID. The connector
**validates the agent profile exists locally at startup** and aborts with setup
guidance if not.

**Who may trigger** defaults to the operator alone. Broaden it deliberately with
the trust flags — `--allow <email>`, `--allow-domain <domain>`, `--allow-project`,
or explicit `--trust <mode>` — and pass them straight through to `bin/connect`;
the bridge enforces them and logs the active set. **`--allow` and `--allow-domain`
only widen trust when the operator is a Basecamp account admin**: both key on the
author's email, and Basecamp masks other people's addresses from non-admins
(`r••••••••@•••.•••`), so the comparison matches nobody. The operator's own
mentions still run — every mode authorizes the operator first, by email or Person
id — but colleagues' are silently dropped as unauthorized, so a non-admin run looks
healthy while ignoring exactly the people the flag was meant to add.
`--allow-project` keys on the Person id instead and works either way. When a user
asks for email-based trust, say which of the two they're in rather than letting
them find out from an agent that never answers. See the connector README's
"Trust modes" for the full semantics and the agent-self / assignments-operator-only
safeguards.

### Stored connection params (no-args invocation)

The skill remembers the last successful connection in
**`~/.config/basecamp-connect/last.json`**:

```json
{
  "agent": "clawdito",
  "operator": null,
  "projects": [ { "id": 27, "name": "On Call" }, { "id": 41746046, "name": "BC5.1" } ],
  "trust": { "mode": "domain", "allow": [], "allow_domain": [ "37signals.com" ], "allow_assignments": false },
  "types": "Comment,Message,Kanban::Card,Kanban::Step,Todo,Chat::Line",
  "chat_poll": 15,
  "boost_poll": 60,
  "saved_at": "2026-07-01T15:00:00Z"
}
```

- **Invoked without arguments:** read that file and **confirm the stored params
  with the user before starting** — show the agent, the project list, **the
  trust configuration (mode + the concrete allowed set)**, **and the effective
  coverage: the `types` and `chat_poll` values that will actually be used** —
  the stored ones, or the defaults when the store predates those fields. Showing
  the *effective* values matters because the defaults include `Chat::Line`: a
  store saved before these fields existed would otherwise relaunch with Campfire
  polling silently added to an apparently unchanged connection. Ask whether to
  go with them, adjust them (add/drop projects, different agent, change trust or
  coverage), or start fresh. Never launch on stored params silently. If the file
  doesn't exist, ask for the agent and projects as usual.
- **Invoked with arguments:** arguments win; the store is not consulted.
- **After every successful registration** (the `Listening for mentions of …`
  line — or, for a chat-only `--types`, the `Polling … Campfire(s) …` line),
  write the params that were actually used back to the file — agent
  profile, operator override (or null), the projects with their resolved ids and
  names, **the trust configuration** (the mode and its value flags, so a
  later no-argument launch reconstructs the same trust boundary rather than
  silently falling back to operator-only), **and the coverage** — the `--types`
  value, `--chat-poll` interval, and boost polling (`--boost-poll` interval, or
  `null` for `--no-boosts`) actually used, so a chat-only or custom-typed run
  relaunches as itself instead of silently restoring the default mixed
  webhook/chat coverage (and its Funnel + webhooks) — so the store always
  reflects the last working connection. Create the directory if needed. Launch failures must
  not overwrite it.
- **Reconstructing the command from the store:** always emit **exactly one
  `--trust <mode>`** for the stored mode, followed by its value flags (`allow` →
  `--allow`, `allow_domain` → `--allow-domain`, `allow_assignments` → the
  assignment opt-in; `--trust project` needs no value flag). Emitting the mode
  explicitly makes `bare --trust domain` (empty `allow_domain`) reconstruct as
  `domain` — using the built-in default domain — rather than silently dropping
  to operator, and makes a value flag that disagrees with the stored mode (e.g.
  `mode:"operator"` with a stray `allow_domain`) get **rejected by the parser**
  rather than silently broadening trust. A missing `trust` block means
  operator-only (older stores). If the stored block is internally inconsistent
  and the parser rejects it, **stop and confirm with the user** — never infer a
  mode to make it launch. Also re-emit the stored `types` (as `--types`),
  `chat_poll` (as `--chat-poll`), and `boost_poll` (`--boost-poll <n>`, or
  `--no-boosts` for a stored `null`) when present; missing fields (older
  stores) mean the defaults.

Project ids are stored (not just names) because a name is only resolved against
the project list as it stands at launch — a rename, or a newly ambiguous name,
would resolve elsewhere or not at all; launching from the store passes ids.

## Prerequisite: the agent must be a local profile authed as that user

Before running, confirm the agent name maps to a usable local `basecamp` profile
that is authed **as the agent user** (not as you):

```bash
basecamp me --profile clawdito                 # should show the agent's identity, distinct from yours
basecamp people show me --profile clawdito -j  # data.id is the agent's Person id — keep it for the run
```

`data.id` from `people show me` is the **account-scoped Person id** — the number
mentions, assignments, subscriber lists, and boosts all carry (e.g. `51177542`).
`basecamp me` reports the *global* identity id, a different number that matches
nothing in an event; the connector resolves the Person id the same way
(`Basecamp::Identity.account_person_id`). The front thread reads it once here
and uses it to strip the agent's own mention from the dispatched instruction
(step 2c — never by name) and for the fallback mention discriminator under
step 2a (only an older connector's event lines need it there — current ones
carry the verdict as `trigger`).

If it's missing or authed as the wrong user, set it up (interactive login as the
agent/bot account):

```bash
basecamp profile create clawdito         # only if the profile does not exist yet
basecamp auth login --profile clawdito
```

That check is for **startup, run on its own**. An intermittent `Not
authenticated for profile:<agent>` *while agents are running* is not this
problem and must not be answered with `auth login` — see
[Transient CLI failures](#transient-cli-failures-under-concurrent-agents).

If the agent profile resolves to the **same** user as the operator, **nothing
will trigger**: the connector refuses the agent's own identity in every trust
mode, so if the agent *is* the operator, the operator's own mentions are dropped
too. `bin/connect` refuses to start in that state and says why; the usual
cause is `BASECAMP_PROFILE` pinned to the agent's profile with no `--operator`,
which resolves the operator through the agent's profile. Use a distinct bot
account for the agent, and pass `--operator` when the variable is set.

## Prerequisite: the funnel hostname must resolve in public DNS

Basecamp validates `payload_url` at webhook **creation** by resolving the
hostname to a public IP. (Fizzy resolves only at delivery time, so a Fizzy
webhook succeeding proves nothing here.) A node's `<node>.<tailnet>.ts.net`
A record is published to the `ts.net` zone by Tailscale's control plane when
Funnel is first enabled on that node — `tailscale funnel status` saying "on"
reflects local config, not that the record exists yet. On 2026-09-10 the
record took ~50 minutes to appear on a fresh node.

If registration fails with `payload_url: must resolve to an active public IP`,
check the **authoritative** server, not a public resolver:

```bash
dig +short <node>.<tailnet>.ts.net @ns1.dnsimple.com
```

- **Empty:** the record is not published. Do **not** retry in a tight loop.
  Every attempt makes Basecamp's resolver re-fetch, get NXDOMAIN, and cache
  it for another 300s (the `ts.net` SOA minimum); an attempt landing just
  before expiry pushes success further out. Poll `dig` instead.
- **Answers:** wait 5 minutes with **no** attempts so cached NXDOMAINs expire,
  then retry. Anycast resolvers are many independent caches, so a name can
  resolve on `1.1.1.1` while another node still returns NXDOMAIN; a couple
  of spaced retries may still be needed.

## Procedure

### 1. Launch the bridge, then watch its STDOUT

`bin/connect` is a long-running process that never exits on its own — it streams
one trusted event per STDOUT line for as long as it runs. A plain background
task only notifies you when a command *completes*, so on its own it would never
wake you per event. You therefore need **two** steps: run the connector in the
background, then arm a persistent monitor on its output so each new event
notifies you automatically — with no user prompting in between.

**a. Check what is already running, then start.** A second connector on the
same agent and project makes Basecamp deliver every event twice, so ask first:

```bash
cd ~/Work/basecamp/basecamp-local-agent-connector && bin/connect --status
```

That lists every connector running on this machine, what it watches, and the
funnel paths it owns. If one already covers what the user asked for, **say so
and stop** — don't start a second. `bin/connect` refuses the duplicate on its
own, and its message names the other run's pid; read that as the answer, not as
an error to work around. `--allow-duplicate` exists but is the user's call, never
yours.

Then run the connector in the background and note the output-file path the
harness reports (you need it for the monitor):

```bash
cd ~/Work/basecamp/basecamp-local-agent-connector && \
  bin/connect @Clawdito --project "<project>" [--project "<project>"]...
```

Read that output file once and confirm it printed `Listening for mentions of ...`
(webhook registration succeeded) or, for a chat-only `--types`, `Polling ...
Campfire(s) ...` (the poller is running — chat-only runs register no webhooks
and open no Funnel). If it errored instead (unknown agent profile, auth,
project not found), surface that and stop. On success, **save the connection
params** to `~/.config/basecamp-connect/last.json` (see "Stored connection
params" above) so the next no-args invocation can offer them back.

**b. Arm a persistent monitor on that output file** with the Monitor tool
(`persistent: true`). Replay the file **from its beginning** (`-n +1`) — the
file is per-run, so this catches an event the connector emitted between
becoming ready and this monitor attaching (a chat mention landing right at
startup, a webhook delivery beating the arm) without ever replaying another
run's events — and filter to the NDJSON event lines so diagnostics stay out
of the stream:

```bash
tail -f -n +1 <connector-output-file> | grep --line-buffered -E '^\{'
```

Each notification the monitor delivers is one event — process it via step 2. An
event that lands while you are waiting on the user is **not** the user's reply.

Each STDOUT line is one trusted event as NDJSON:

```json
{"event_id":99001,"kind":"comment_created","created_at":"...",
 "creator":{"id":100,"name":"Jorge Manrubia","email_address":"jorge@..."},
 "recording":{"id":456,"type":"Comment","app_url":"...","url":"...",
   "content":"<p>Hey <bc-attachment content-type=\"application/vnd.basecamp.mention\">…@Clawdito…</bc-attachment> do X</p>",
   "parent":{...},"bucket":{"id":222,"name":"BC5 Calendar"}},
 "trigger":{"mentioned":true,"subscribed":false}}
```

`creator` is the **triggering author** — the person whose mention/assignment
drove this event. In the default operator-only mode that is always you; under a
broadened trust mode (`--allow`, `--allow-domain`, `--allow-project`) it may be
an authorized coworker instead. Treat `creator` as *the requester* — that is who
to @mention on failure — not as "the operator." The mention of the agent lives
in `recording.content` as a mention attachment. `trigger` is the connector's
verdict on **why** the event fired, settled on the re-fetched recording:
`mentioned` (its content carries a mention attachment for the agent's Person
id) or `subscribed` (a `comment_created` on a recording the agent follows, with
no mention of it). A `comment_created` is exactly one of the two; an assignment
or a boost is a directive by `kind` alone (`subscribed` is `false` for both;
`mentioned` reports whether an assigned recording's content mentions the
agent, and is always `false` on a boost — a reaction is not content). STDERR
carries diagnostics (dropped/uncorroborated events, registration notices) —
surface them but don't act on them.

Keep watching until the user stops the skill (see Cleanup).

### 2. For each trusted event — ack it, hand it off, don't do it yourself

**The front thread is an orchestrator, not a worker.** Its only job is to keep
watching for new mentions, acknowledge each one, and dispatch it.

**Route by the event line first.** Two kinds of line share the monitor:

- A line carrying `review_id`/`repo`/`state` and **no `recording`** is a
  **GitHub review** (only when `bin/connect` runs with `--repo`). It gets no
  boost and no bucket lookup — the repo is `repo`, the PR is `pull_number`.
  An `approved` line is the operator's approval — the agent may land the PR:
  `bin/connect` enforces this (`GitHub::ReviewPipeline`, see
  [`docs/pr-review-loop.md`](../../docs/pr-review-loop.md#trust)) by emitting
  an approval only when the reviewer GitHub recorded, re-fetched from the API,
  is the operator's GitHub login, and dropping every other reviewer's approval
  before it reaches this stream. That login is the one this machine's `gh` is
  signed in as (`gh api user`), read once at startup, or `--gh-operator
  <login>` passed through to `bin/connect`; the connector logs it at startup
  as `Trust: reviews on @<login>'s own pull requests only; approvals from
  @<login> only; …` — the first clause being the wider drop: the webhook
  watches the whole repo, and a review of a pull request somebody else opened
  never reaches this stream, whoever wrote it. `changes_requested` and
  `commented` lines arrive from any reviewer: feedback to address, never a
  reason to merge — with one exception, dropped before this stream: a
  `commented` review by the operator's own login whose body and every inline
  comment start with 🤖. Agents post under the operator's
  account, so that marker, not the account, is what makes it the agent's own
  reply; a review carrying any unmarked text is a person's and always arrives,
  as do approvals and `changes_requested`. Dispatch one background agent in
  that repo to handle it per *Review / approval loop* below, and return to the
  monitor.
- A line carrying `recording` is a **Basecamp event** — the checklist below.
  Drop it outright if its `creator` is the agent — the only checkable key: the
  emitted `recording` carries no author, and a `boost_created` line's
  `recording` is the agent's own work by definition, which is not what this
  test reads (`bin/connect` already refuses agent-authored events in every trust mode, and
  posting as the agent — a distinct user from the operator — keeps replies
  from authorizing anyway; this is cheap defense in depth, and it comes
  *before* the boost so a slipped-through self-comment is never acked).

For every other Basecamp event the front thread runs exactly this checklist, in
this order, and nothing else:

1. **Acknowledge** — a fast, light signal of receipt, usually a boost with apt
   content: `basecamp boost create <recording.url> "<ack>" --profile <agent>`
   (skipped only for subscribed-thread comments and `boost_created` events; both
   are told apart from the event line alone — see the discriminator under *a.*).
2. **Resolve the repo** from `recording.bucket.name`.
3. **Dispatch** one background agent that owns the event end-to-end.
4. **Return to the monitor.**

It must **never** read the recording (beyond the event line it already has),
gather context, investigate, run repo commands, do the requested work, or post
the reply itself — every one of those blocks it from picking up the next
mention, and the ack is what suffers first. The failure this rule exists to
prevent: a mention received within 2 seconds, then worked inline (the card
read, the code investigated, a worker spawned for the change) with **no boost
and no reply for 30+ minutes** — which, from Basecamp, is indistinguishable
from a missed mention. The boost in step 1 is the only Basecamp write the front
thread makes per event — except the one *holding reply* in step b, posted only
when the event cannot be handed off — and it lands before anything else happens.

**a. Acknowledge — fit the ack to the moment** (front thread, immediately on
receipt — before repo resolution, before dispatch). What matters is that the
requester sees the trigger *registered* before any slow work — a visible
"received," not a rote token. How you signal it is a judgment call:

- **A boost** is the lightweight default — one CLI call, lands within seconds,
  shows on the recording as the agent. Give it content that *fits the moment* (a
  short apt phrase, a fitting emoji), never a fixed string. This is the right ack
  for most **directive** triggers — mentions and assignments alike (boosts work
  on comments, messages, cards, and todos) — and for Campfire mentions (boost the
  chat line; see *When the mention arrives in Campfire*). It matters most for
  **card/board work**, where a visible ack is how the requester knows the mention
  landed at all.
- **A brief reply can be the ack** when the worker will answer almost immediately
  — a quick Campfire back-and-forth, or a directive it resolves in moments. That
  substantive reply carries the "received," so a boost bolted in front of it is
  noise: the front thread posts **nothing** and flags "no ack owed" in the
  handoff (step c) so the worker doesn't add a fallback boost. **Not** for
  card/board work — there the visible boost is how the requester sees the mention
  land — and **never** license to work inline (the orchestrator rule above
  stands): skipping means the front thread writes nothing and dispatches at once,
  exactly as always.

Whichever you pick, keep it fast and light — the front thread's job is to ack (or
knowingly skip) and dispatch, nothing more; it lands within seconds regardless of
what dispatch does. The boost form:

```bash
basecamp boost create <recording.url> "<ack>" --profile <agent>
```

Use the **URL form**: every emitted event carries `recording.url`, and the URL
already names the project. The bare-id form needs `--project
<recording.bucket.id>` — without it the CLI falls into interactive project
resolution, which a background shell cannot answer.

A boost is a lightweight reaction (≤16 chars) posted **as the agent**, so the
trigger visibly registered. Exactly two kinds of Basecamp event get **no** boost
(see their sections below):

- **subscribed-thread comments** — an event line whose `trigger.subscribed` is
  `true`. Read `trigger` **first**: it is the connector's own verdict, settled
  on the re-fetched recording against the agent's Person id, so a line that
  carries it needs no markup inspection at all (`trigger.mentioned` true means
  a directive — boost it). Fall back to the markup match **only when the line
  has no `trigger` key** — an older connector — and then it is a
  `comment_created` whose `recording.content` has no `<bc-attachment
  content-type="application/vnd.basecamp.mention">` carrying **the agent's
  Person id**. There the id is the **only** discriminator: the attachment's
  embedded `content` markup names it as
  `<bc-mention … gid="gid://bc3/Person/<id>">`, and the attachment's own
  `sgid` attribute encodes the same `gid://bc3/Person/<id>` (base64 in the
  segment before `--`, which is what the connector's own matcher decodes —
  `Event#mentioned_person_ids` in
  `lib/basecamp_agent_connector/basecamp/event.rb`). Compare against the
  Person id captured at startup (`basecamp people show me --profile <agent>
  -j` → `data.id`, see *Prerequisite*). Never match on the name: the
  `<bc-mention>` also carries a first name, and names are not unique — a
  colleague who shares the agent's name would turn a followed-thread comment
  into a boosted, dispatched directive. A mention attachment naming someone
  *else* is still a followed-thread comment, and a plain-text `@name` with no
  attachment is not a mention at all;
- **`boost_created`** events.

If the call fails, don't block on it — but retry only the two failures that
happen **before any request is sent**, `Not authenticated for profile:` and
`token refresh failed:` (the transient credential-store failure described in
[Transient CLI failures](#transient-cli-failures-under-concurrent-agents)). Any
other failure may have landed the boost server-side (a timeout reading the
response, an envelope parse error), and a retry would post a duplicate. One
shell call does both:

```bash
landed=false
for i in 1 2 3; do
  if out=$(basecamp boost create <recording.url> "<ack>" --profile <agent> 2>&1); then
    landed=true; break
  fi
  echo "$out" | grep -qE 'Not authenticated for|token refresh failed' || break   # anything else: no retry
  sleep 2
done
[ "$landed" = true ] || { echo "boost did not verifiably land: $out" >&2; false; }
```

The explicit `landed` flag is what makes the exit status honest: a bare `break`
on a non-retryable error would leave the loop at status 0, and exhausting the
retries would leave it at `sleep`'s status 0 — either way the front thread
would hand off "boost landed" to an agent that then skips its fallback, and the
event stays unacknowledged. The snippet exits non-zero on every unsuccessful
path and echoes the CLI's last error so the failure is visible in the log.

If the boost did not verifiably land, record that for the dispatch (step c) and
move on — the dispatched agent posts the fallback boost.

**b. Resolve the working repo** (front thread, fast). Infer the local repo from
the project name (`recording.bucket.name`). Basecamp project names usually carry
an app token — e.g. a `BC5 …` project maps to the Basecamp repo under
`~/Work/<org>/<repo>`. A mapping table (see `config/project_repos.toml`, if
present) backs the heuristic. If the project's `AGENTS.md` doc declares repo
mappings, they take precedence — repo resolution is where those mappings are
honored, since the dispatched worker stays scoped to the repo chosen here. **If you cannot confidently map the project to a
repo, ask the user which repo to use — do not guess and do not silently fall
back.** This is the one step that may need you; everything after it is delegated.

**The ack must never precede an indefinite silence.** The boost has already told
the requester "received"; if this step has to stop and ask the user, or step c
fails to dispatch, nobody is working the event and nothing else will post. So
*before* asking (or on the dispatch failure), post one short **holding reply**
as the agent on the originating recording — in the Campfire for a chat trigger
— that @mentions the requester (the event `creator`): received, but held, and
why ("waiting on the operator to pick a repo"). One line, once; it is the only
reply the front thread ever posts, and only on directive triggers (mentions,
assignments, chat) — a followed-thread comment or a boost gets no boost and no
holding reply either. Under the default operator-only trust the requester *is*
the user you are about to ask; post it anyway, so Basecamp never shows an
acked task nobody holds.

**c. Dispatch one background agent that owns the whole event.** Use the Agent
tool with `run_in_background: true`, running in the resolved repo. Give it
everything it needs to finish **without the front thread**:

- the event **`kind`** and the **instruction** as that kind defines it: for a
  mention, `recording.content` with the agent mention removed, the rest of the
  raw HTML (links, other mentions) intact; for an assignment, the recording
  itself (its `title`/`content` is the task); for a `boost_created`,
  `details.boost.content` plus the boosted recording, which carries no
  `content`; for a subscribed-thread comment, the comment as context, not a
  directive;
- the **recording** URL/id and its parent URL;
- the **agent profile name** (its reply identity);
- the **requester's** name/id — i.e. the event `creator` (to @mention on
  failure). This is the triggering author, who under a broadened trust mode is
  not necessarily the operator;
- whether an **ack is still owed** (step a): the front thread's boost landed (not
  owed), failed to land (owed — the worker fallback-boosts), or was deliberately
  skipped because the reply is the ack (not owed).

Instruct that background agent to, in order:

1. **Boost only if the handoff says an ack is still owed.**
   The ack boost is normally already on the recording; the dispatched agent's
   boost is a fallback for a front-thread call that failed, posted without
   first listing the recording's boosts:
   ```bash
   basecamp boost create <recording.url> "<ack>" --profile <agent>
   ```
   A front-thread call that Basecamp accepted but reported as failed (a
   timeout reading the response, an envelope parse error) then produces a
   second ack boost. That is accepted: a boost is a reaction, a duplicate is
   harmless, and a missing ack is the failure this whole step exists to
   prevent. Checking first would be one more CLI call that can fail the same
   transient way, and it would have to decide which earlier event an older
   boost on the same recording belonged to — the price of "never a second
   boost" is a rulebook, not a guarantee. Same exceptions as the front thread:
   subscribed-thread comments and `boost_created` events are never boosted.
2. **Gather context from Basecamp** — it is the context store; the event is just
   the trigger + pointer:
   ```bash
   basecamp show <recording.app_url> -j          # the recording itself
   basecamp show <recording.parent.app_url> -j   # the card/message it lives in
   # plus the thread/comments and the project as needed
   ```
   **Read the project's `AGENTS.md` doc, if it has one, and respect it.** A
   project may carry a vault doc named `AGENTS.md` — its standing instruction file
   for agents: board and column semantics, comms norms, and the workflow to run
   (the same doc the `coworker` skill reads at onboarding). Repo mappings in it
   are honored earlier, at repo resolution (step b), since the worker is already
   scoped to the repo chosen there.
   ```bash
   basecamp docs documents list --all --project <project-id> -j  # find a doc titled AGENTS.md
   basecamp docs show <doc-id> --project <project-id> -j         # read it
   ```
   Trust is at the **project** level — like a directory's config or a repo's own
   `AGENTS.md`, not a review of the doc's contents or its author. The operator
   attaching the connector to this project settles it: that attachment (confirmed
   once at launch, step 1; `--allow-project` / `--trust` broadens it explicitly)
   is the trust grant, so honor the project's `AGENTS.md`. Trust is a property of
   the connected project, not of each dispatch — there is no per-event trust
   prompt to ask or persist. If there is no such doc, proceed with the event as
   usual.
3. **Move the card out of Triage.** If the work lives on a card (the recording
   or its parent is a `Kanban::Card`), check which column it sits in. If it's in
   a **Triage**-like column and the card table has an **In progress**-like column
   (match loosely and case-insensitively: "In progress", "Working on", "Doing"),
   move the card there before starting — the board should show the work is
   underway:
   ```bash
   basecamp cards columns --project <project>            # find the columns
   basecamp cards move <card-id> --to "<In progress>" --profile <agent>
   ```
   Both also take `--card-table <id>`, **required whenever the project holds more
   than one card table** — On Call has three, so a bare `cards columns --project
   27` resolves nothing there. If there's no Triage-like or no In-progress-like
   column, skip this silently — never invent columns.
4. **Do the requested work** in the repo.

   **Several items means several agents.** When one request covers independent
   work — six cards, a todo list, four unrelated bugs — spawn a subagent per
   item instead of grinding through them in series, **five at a time**, waiting
   for a slot before starting the sixth. The user's word overrides the number
   and the default both ways ("one at a time", "run all ten"). This cap is on
   the work inside a single event; it is unrelated to event dispatch, which has
   no cap at all.

   Two things stay serial, because parallelism costs more than it saves there:
   items that depend on each other, and items touching the same files — a merge
   conflict is slower than the run it saved. Each subagent gets its own
   worktree when it will commit.

   One reply at the end, covering every item, not one reply per subagent. Say
   which items failed if any did.

   **Reply latency:** the boost says
   "received"; it does not say "still working." If the work will take more than
   **~10 minutes**, post a short **interim reply** as the agent on the
   originating recording (in the Campfire, for a chat trigger) — one or two
   lines: what it is doing and where progress can be followed (the PR link once
   it exists, otherwise the branch) — then the final reply when done. One
   interim reply, not a running commentary.
5. **Reply on the originating recording as the agent** — commenting with the
   agent's profile so the reply posts as the agent user:
   ```bash
   basecamp comments create <recording.url|id> "<body>" --profile <agent>
   ```
   Basecamp has no comment-on-a-comment: `comments create` only accepts a
   commentable parent (Card, Message, Todo, Document, …), so when `recording`
   **is itself a `Comment`** (the mention arrived inside one, as most do),
   target `recording.parent` instead — `basecamp comments create
   <recording.parent.url|id> "<body>" --profile <agent>`. Pointing it at the
   comment's own id/url fails with `access denied`. When `recording` is
   already a top-level item (a card mentioned in its description, say), reply
   to `recording` directly.
   - **Success** — post the results where the mention was written.
   - **Failure** (it errored or couldn't finish) — post a short error summary and
     **@mention the requester** (the event `creator`) so it surfaces as a
     notification for whoever asked — the operator in the default mode, or the
     authorized coworker who triggered it under a broadened mode.
   - **Never put the agent mention in a reply body.**
   - **Write it as rich text** — see *Write replies as rich text* below.

Because the background agent gathers its own context and posts its own reply, the
front thread is free the instant it dispatches — it goes straight back to the
monitor, ready for the next mention while any number of events are in flight.
There is **no concurrency cap**; dispatch every event as it arrives.

### Write replies as rich text

Comment and message bodies are rich text, so use it. The `basecamp` CLI runs the
body through a Markdown converter on the way in: `## Headings` become headings,
`**bold**` becomes bold, `- bullets` become a list, `> quoted` becomes a
blockquote, and fenced blocks become code blocks. Diffs, commands, and error
output belong in a fenced block, not inline in a sentence. A wall of
undifferentiated prose in a rich-text field is a wasted field.

Lead with the answer in the first line. Headings and detail go under it —
whoever reads only the notification preview should still know where it landed.

**Links carry a title, not a URL.** Write
`[Skip the ack boost when the reply is immediate](https://github.com/basecamp/bc3/pull/1234)`,
never a bare `https://github.com/basecamp/bc3/pull/1234`. Bare URLs don't
autolink in comments — they post as plain text — and even when a URL does link,
it tells the reader nothing about what's behind it. Same for Basecamp links:
name the card, the message, the doc.

**Anything in another app gets its full URL.** `#1234`, `PR 1234`, `SENTRY-4F`
and `abc123f` are shorthand that only resolves inside the app they came from — in a
Basecamp comment they're dead text a reader has to go hunt down. Write
`[#1234 Skip the ack boost](https://github.com/basecamp/bc3/pull/1234)`, so the
reference reads the way it does on GitHub *and* opens there in one click. Same
for issues, commits, runs, Sentry events, and dashboards.

**Use tables when the content is a grid.** GFM pipe tables convert to real
Basecamp tables, column alignment (`|---:|`) included, and Markdown works inside
the cells — code spans, bold, titled links. A file-by-file summary, a
before/after benchmark, a matrix of cases: table. (Tables need `basecamp` v0.8.0
or newer — older builds post the pipes literally.)

Keep them simple, one line per cell. Merged cells, captions, images in cells and
multi-line cells all render, but the CLI's in-place TUI editors refuse to open
content shaped that way — it can't round-trip through a pipe table. A prose list
beats a table for two items; don't reach for a grid that isn't one.

**No hand-written HTML.** Write the Markdown and let the CLI convert it. Raw
tags are escaped and land as visible `<strong>…</strong>` text. The
`[@Name](person:<id>)` mention syntax is the only non-Markdown markup the CLI
understands.

### When the agent is assigned a card/todo

If the event `kind` ends in `_assignment_changed`, the operator assigned the
agent to the recording (a card/todo/step) — there's no mention to strip; **the
recording itself is the task**. The front thread acks the recording on receipt
exactly as for a mention — a boost with apt content is the usual ack, and boosts
work on todos and cards too. The dispatched background agent should, in order:

1. **Boost only if the handoff says an ack is still owed** —
   the same fallback rule as for a mention: post without listing first; a rare
   duplicate is accepted over a missing ack.
2. **Move the card out of Triage** — same rule as for mentions: if the assigned
   card sits in a Triage-like column and the table has an In-progress-like
   column, move it there before starting; skip silently otherwise.
3. **Do the work** the card/todo describes (its `content`/`title` is the
   instruction; gather context and resolve the repo as usual; if it's a PR task,
   follow the green-first lifecycle below).
4. **Reply with the result** on the same recording as the agent — and on failure,
   a short error summary that @mentions the requester (the event `creator`).

The instruction here is the **card/todo content**, not a comment body. Everything
else (resolve repo, one background agent owns it end-to-end, front thread returns
to the monitor) is the same as above.

### When the mention arrives in Campfire (a chat line)

If the event `kind` starts with `chat_` (e.g. `chat_lines_rich_text_created`),
the mention was posted in a project **Campfire**. Chat has no webhooks — the
connector's integrated poller delivered this line through the same trust gate as
every other event. Chat is conversational and realtime, so dispatch the same way
with these differences:

- **Context** — the generic `basecamp show` does **not** resolve chat lines; use
  the chat commands:
  ```bash
  basecamp chat line <recording.url> -j                                  # the line itself
  basecamp chat messages --project <bucket.id> --room <recording.parent.id> -n 25 -j   # the conversation
  ```
- **Ack** — the front thread acks the **line** on receipt, usually a boost with
  apt content (`basecamp boost create <recording.url> "<ack>" --profile
  <agent>`), same as any recording; the dispatched agent boosts only as the
  fallback.
- **No card moves** — there is no board; skip the Triage step.
- **Reply in the chat as the agent** — post to the same Campfire, not a comment:
  ```bash
  basecamp chat post "<body>" --project <bucket.id> --room <recording.parent.id> --profile <agent>
  ```
  The CLI resolves @mentions (`@Name`, or `[@Name](person:<creator.id>)` to
  pin by Person id); a reply containing one posts as rich text with its
  Markdown converted — so format those with Markdown (`**bold**`, `- bullets`,
  and `[titled links](url)` rather than bare URLs, which don't autolink once
  the line is rich text). Chat is small: bold, bullets and titled links, no
  headings. A mention-free reply posts as plain text — Markdown renders
  literally, so keep those replies plain prose, bare URL and all.
  **Never hand-write HTML in either case.** The CLI converts Markdown and
  resolves mentions; it does not accept raw HTML, so tags like `<p>`,
  `<strong>`, or `<a href>` are wrong in the Markdown path (write the Markdown
  instead) and post literally in the plain-text path — a `<strong>` headline
  lands as visible `<strong>…</strong>` text, not bold. The
  `[@Name](person:<id>)` mention syntax above is the only non-Markdown markup
  the CLI understands. Keep replies
  chat-sized; spill long results into a Basecamp doc or comment and link
  them. On failure, @mention the requester so it notifies:
  `[@Name](person:<creator.id>)`.

### When a comment lands on a thread the agent follows

If the event line's `trigger.subscribed` is `true` — or, on an older
connector's line with no `trigger` key, the `kind` is `comment_created` and
`recording.content` carries **no mention attachment naming the agent** (the
fallback discriminator under step 2a — a mention of someone else, or a
plain-text `@name`, does not count) — the connector fired because the agent
**subscribes** to the commented-on recording (a card/thread it participates
in), not because it was addressed. Treat this as *activity on a followed
thread*, not a directive:

1. **Read for context** — the comment (`recording.content`) and, as needed, its
   parent (`recording.parent`) and neighbours. This is the same non-blocking
   dispatch as a mention: the front thread returns to the monitor immediately.
2. **Respond only if a response adds value** — a question the agent can answer, a
   problem it can act on, a change it should make. Reply on the same recording as
   the agent, exactly like a mention reply. **Default to staying silent**: a
   followed thread is not an instruction, and replying to every comment is noise.
3. **No boost, no card moves, no interim reply** — this **overrides** the front
   thread's boost-first step above and the dispatched agent's ~10-minute
   interim-reply rule: a followed-thread comment is not an ack-worthy
   assignment, so the front thread skips the ack boost and the dispatched
   agent doesn't add one either; skip the Triage move and the interim reply
   too unless the agent actually takes the thread on.

> This response policy is **provisional** — the connector now *fires* on
> subscribed-thread comments; how aggressively the agent should engage (answer
> vs. stay silent, and on which threads) is an operator-tunable judgment worth
> revisiting once there's real traffic.

### When someone boosts the agent's work

If the event `kind` is `boost_created`, an authorized user boosted a recording
of the agent's — a comment it posted, a card it worked, an answer it wrote.
`creator` is the **booster**, `recording` is the **boosted recording** (the
agent's own work), and `details.boost.content` is the boost itself — at most 16
characters, so it is a *signal*, not an instruction: `👍`, `🔥`, `redo`, `wrong`.

1. **Read the signal in context** — the boost content plus the boosted
   recording (`basecamp show <recording.url> -j`) and its thread. Same
   non-blocking dispatch as every trigger: the front thread returns to the
   monitor immediately.
2. **Judge the valence.** An approving boost (`👍`, `🙏`, `nice`) needs **no
   action and no reply** — it is applause, and answering applause is noise. A
   corrective or directive boost (`redo`, `wrong`, `👎`, `🤔`) means the boosted
   work needs another look: re-read the thread for what to fix; when the signal
   is too terse to act on confidently, reply on the boosted recording as the
   agent asking one concrete question.
3. **No boost back, no card moves, no interim reply** — the front thread skips
   its boost-first step for `boost_created` events and the dispatched agent
   never boosts a boost; skip the Triage move and the ~10-minute interim reply
   unless the agent actually resumes work on the recording.

> This response policy is **provisional**, like the followed-thread one: 16
> characters can't carry much intent, so lean strongly toward silence and let
> real traffic tune the judgment.

### Transient CLI failures under concurrent agents

With several agents running at once, the `basecamp` CLI intermittently fails
with `Not authenticated for profile:<agent>: credentials not found …` or
`token refresh failed: …` — from the front thread's boost, a dispatched agent's
`basecamp show`, or the connector's own pollers. This is a **transient failure
of the CLI's credential store under concurrent invocations** — the observed
fact is that the same call run alone succeeds — **not a credentials problem**:
the profile exists and its tokens are fine. The cause is not pinned down; the
CLI source offers two candidates, and neither is confirmed: the CLI probes the
OS keyring once per process and silently falls back to the credentials file
when the probe errors (or, with no terminal and no GUI session, exceeds its 10s
bound), and concurrent token refreshes can rotate the refresh token out from
under each other. Many simultaneous `basecamp` invocations make both likelier.
Both symptoms surface before the actual API request is sent.

- **Retry the call** — 2–3 times with a short pause (a second or two) — and only
  then treat it as a real failure. Retry only on these two signatures: any other
  error may mean the request went through, and a retried write posts twice.
- **Never run `basecamp auth login`** in response to it: an interactive login
  can't complete from a background agent, and re-authing a profile that isn't
  broken only risks clobbering the good credentials.
- **Never treat it as "the agent profile is missing"**, and never report it as
  such on Basecamp. The startup check in *Prerequisite* runs on its own and is
  the authority on whether the profile exists; an intermittent error mid-run is
  not.

### Validate a finished body of work with `bin/ci` (in the background)

Whenever a coherent body of work is finished — the initial implementation, a
round of changes, a fix, a review-feedback pass — validate it by running the
repo's `bin/ci` **in the background** (non-blocking) before reporting done.
Aggregate as much as possible into a single run: don't re-run after every small
edit, but as a general rule run `bin/ci` once at the **end** of the body of work.
Running it in the background keeps the agent free and surfaces failures without
stalling; fix anything it flags before you reply "done."

```bash
bin/ci --force > /tmp/ci-<branch>.log 2>&1; echo "EXIT=$?" >> /tmp/ci-<branch>.log   # background
```

PR tasks are stricter — they follow the green-first lifecycle below, where
`bin/ci` must pass (and remote checks too) *before* the work is reported. This
background-`bin/ci` rule is the baseline for all other work (e.g. a direct change
that's committed and deployed without a PR): still run `bin/ci` at the end.

### When the task results in a pull request

Some instructions are "open a PR for X." For these the background agent follows a
stricter lifecycle and **must not report the work done until the branch is
green** — getting CI green is part of finishing the task, not a follow-up:

1. **Work in a fresh worktree off `main`** — `git worktree add -b <branch> <path>
   main` in the resolved repo, so the task is isolated and `main` stays clean. Do
   all the work there.
2. **Green locally first** — run `bin/ci` in the worktree and iterate until it
   passes. Never push red.
3. **Push and open the PR.**
4. **Green remotely** — `gh pr checks <n> --watch --fail-fast`; if a check fails,
   fix it, push, and re-watch. Loop until every check is green (remote can fail
   what local passed).
5. **Only now reply "done"** on Basecamp, with the PR linked by its title —
   `[Skip the ack boost when the reply is immediate](<pr url>)`, not a bare URL.
   Never communicate success on a red or unchecked branch. (The ~10-minute **interim reply** from
   the dispatched agent's step 4 in *For each trusted event* still applies and
   may link the PR early — it says "in progress, follow it here," never
   "done.") If you cannot get it green after a reasonable effort, reply with
   **what is failing** and @mention the requester (the event `creator`) — not
   a false "done."

#### Review / approval loop (GitHub webhook)

Once the PR is up and green, reviews are handled **event-driven via a GitHub
`pull_request_review` webhook**, not by an agent sitting in a poll loop: a human
review is unbounded latency, an idle LLM agent is the wrong tool for it, and an
in-session agent would die when the session ends. **`bin/connect` is unified** —
the same process that watches Basecamp also watches GitHub repos, over the
**same funnel**, when you pass `--repo`:

```bash
bin/connect @Clawdito --project "<project>" --repo <owner>/<repo>
```

It emits GitHub review events on the same STDOUT as Basecamp events (a review
event carries `review_id`/`repo`/`state` instead of `recording`), so the one
persistent monitor you already armed picks them up too. For a repo created
**after** the connector started (the common PR case), don't restart it — the
connector logs a `/gh/<secret>` endpoint + HMAC secret at startup; register a
`pull_request_review` webhook on the new repo against that endpoint (one webhook
per PR's repo, all multiplexed onto the single funnel). Branch on `state`:

- **`changes_requested` / `commented`** — re-fetch the *whole* review (body +
  inline comments) from the API (the webhook is a trigger + pointer, exactly like
  the Basecamp side), address the feedback in the worktree, re-green (steps 2–4),
  push, and reply. Prefix every PR comment and review reply with 🤖 (the
  convention for agent-written comments): `bin/connect` reads that marker to
  drop the agent's own replies instead of dispatching them back at you.
- **`approved`** — the operator's approval (`bin/connect` emits no other):
  land per the repo's policy and reply done.

GitHub webhooks carry an HMAC secret (`X-Hub-Signature-256`), so unlike Basecamp
deliveries they are verified cryptographically *and* corroborated by an API
re-fetch. The connector-side plumbing that backs this loop (the unified
`Connector` + the GitHub `Bridge` route: register the repo hook, verify the
signature, parse `pull_request_review`, emit) is specced in
[`docs/pr-review-loop.md`](../../docs/pr-review-loop.md).

## Cleanup / lifecycle — always tear down

`bin/connect` opens a **public** Tailscale Funnel URL and registers a **real
Basecamp webhook per project**. These must not outlive the session. The
connector deletes every webhook and unmounts its own funnel paths on
`SIGINT`/`SIGTERM`, so the rule is simple: **whenever you stop watching — normal end, user interrupt, an
error, or the skill aborting — stop the `bin/connect` process** (TaskStop / send
SIGTERM). Its teardown does the rest.

After stopping, **verify nothing leaked**:

```bash
basecamp webhooks list --project "<project>" -j   # expect zero from this run
tailscale funnel status                            # expect no /bc5/… or /gh/… path
```

If the process was killed un-gracefully (e.g. `SIGKILL`) and teardown didn't run,
it leaves webhooks behind. **Never delete a webhook you cannot attribute.** A
registration you don't recognize may belong to a *live* connector — another
session's, an older build's (those use `/hook/<secret>`, not `/bc5/<secret>`),
or another machine's — and deleting one makes that connector silently deaf to
Basecamp while it goes on polling chat. This has actually happened: eleven of a
running connector's webhooks were deleted as presumed orphans.

So attribute first:

```bash
bin/connect --status   # every live run, and the funnel paths each one owns
```

A webhook whose `payload_url` ends in a path that listing names is **live** —
leave it. `--status` also reports any running `bin/connect` process the registry
can't account for (an older build recorded nothing): treat those pids as live
connectors whose webhooks are **unattributable**, and delete none of them. A path belonging to a run that has exited is an orphan, and the **next
`bin/connect` start sweeps those automatically**: it deletes the webhooks
pointing at the paths that run recorded — on the projects and repos that run
watched, not just the ones you are starting — and forgets its entry in
`~/.config/basecamp-connect/runs/` once every one of them is accounted for. So the normal answer to a leftover is "start the
connector again," not a manual delete.

Delete by hand only what `--status` proves is unowned, with `basecamp webhooks
delete <id> --project "<project>"`, and unmount each leftover path with
`tailscale funnel --set-path /bc5/<secret> off`. If a webhook's path appears in
no live run *and* in no registry entry, it predates the registry or came from
elsewhere — **ask the user before deleting it**. Never run `tailscale funnel
reset` — it tears down every path on this host's funnel, including ones other
tools mounted.

## Notes

- One `bin/connect` run = one or two paths on the host's shared funnel + one
  server + one webhook per watched project. Re-running re-registers fresh;
  exiting cleans up.
- The connector never trusts the POST body's content — it re-fetches the
  recording from Basecamp before emitting. The content you see on STDOUT is the
  authoritative copy.
- **Reply loop (defense in depth):** trust is "authored by an authorized user
  AND mentions the agent," and `bin/connect` refuses agent-authored events
  outright in every trust mode (matched by email and Person id). Replying as
  the agent profile (a distinct user) means agent replies are never
  re-ingested; still keep the agent mention out of reply bodies as a courtesy.
