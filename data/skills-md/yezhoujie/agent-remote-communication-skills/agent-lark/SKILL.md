---
name: agent-lark
description: Pushes a decision that needs a human to their phone as a Feishu/Lark card and blocks until the verdict comes back on stdout; messages, images, files and voice notes the human sends in the project's Feishu group arrive in the agent session as instructions. For choices the agent cannot settle on its own (unaligned requirements, a real disagreement, a technology choice) while the human may be away from the keyboard. When to ask is the caller's policy — this skill provides the call, not the trigger. It can also push one-way notifications (notify) and send files (send-file) to the same group.
license: MIT
compatibility: "Node >= 22, single self-contained file, nothing to install. Needs a Feishu/Lark custom app, created by scanning a QR code (no workspace-admin approval). herdr is optional: phone -> terminal injection and the stuck-on-a-prompt alert need it; everything else works without it. Exercised end-to-end on macOS inside herdr only; Windows (named pipes) has unit tests in CI, no real-device run."
---

# agent-lark

Send one question to the human's phone as a Feishu card, get one answer back on stdout. The skill is a
channel only: it renders your JSON into a fixed card layout with one button per option, pushes it into
the Feishu group bound to this project, and returns whatever the human replies, verbatim. It never
interprets content. `notify` pushes a one-way card and returns at once; `send-file` sends an image or a
file into the same group.

Every command below is `dist/cli.mjs` in this skill's directory (`node <skill dir>/dist/cli.mjs …`);
the CLI calls itself `agent-lark` in its own messages, and that always means this file. Node 22 or
newer; one self-contained file, no `npm install`, no build step. A symlink saves typing, if the human
wants one: `ln -sf "<skill dir>/dist/cli.mjs" ~/.local/bin/agent-lark`. The shell forms in this file
are POSIX (`$(…)`, quoted heredocs).

## When to use

Any point where your workflow needs a human decision you cannot make yourself and the human may be
away from the terminal. Whether and when to ask is your (or your caller's) policy: this skill defines
no triggers, installs no hooks, and does not replace your CLI's own "ask the user" mechanism.

Two things must exist before the first question: Feishu app credentials on this machine (`setup`, once
per machine) and a group bound to this project (`away on`, once per project). Both are the human's to
run or approve; see "Remote mode and the per-project state file" below.

## Invoked with an argument

The user may hand this skill one word (`/agent-lark setup`, `/agent-lark on`, `/agent-lark off`, or the
same words in a sentence). Each maps to one flow:

- **`setup`** — guided setup, the human at the keyboard. First ask which way: **create a new app by QR
  code**, or **reuse an app they already have** (they know its App ID and App Secret). Never pick for
  them, never run `setup` unasked: it creates or binds a Feishu app under their account.
  - QR code ⇒ run `agent-lark setup </dev/null` yourself (stdin closed explicitly: the menu only appears
    on a terminal, so this goes straight to the QR code whatever your harness gives a child process). It draws the code as ANSI art and prints the URL as a plain line right under it;
    hand over that line, or render it into a PNG yourself and open it. Run it in the background: it waits
    for the scan (the code expires after a few minutes; rc 4 then, rerun).
  - Reuse ⇒ run `agent-lark setup --reuse`. **The secret never passes through you.** Inside herdr the
    command opens a pane below yours, runs the interactive setup there (App ID typed, App Secret typed
    with echo off) and exits 0 at once with `The interactive setup is running in herdr pane <id>: …`;
    when the human is done, one line prefixed `[agent-lark] setup:` arrives in your session (the four
    forms are in "Remote mode" below) — wait for it, do nothing meanwhile. Every end of the pane reports
    a line except one: the pane closed by hand. No line, and the pane is gone or the user says they are
    done ⇒ ask them what the pane printed, or run `status` (its credential layers show whether anything
    was stored). Outside herdr it exits 4 and
    puts the exact command on stderr (`node <cli> --home <dir> setup --reuse`): give that command to the
    user to run in their own terminal, and let them tell you when it is done. The user must run it in a terminal window of their own (Terminal, iTerm, …). Never suggest running it inside this session — a `!`-prefixed command, a shell tool, a background job: none of them has a TTY, and the CLI refuses without one.
    Either way the human still
    has to enable the scopes, the event and the callback for a reused app in the Feishu developer
    console; the interactive setup lists them.
  - When it is done, report the outcome in one sentence. **Do not `away on`** — that is the next word.
- **`on`** — the remote-mode "on" flow from "Remote mode and the per-project state file" (`away on
  --name "<task>"` from your own pane, relay stdout). No credentials yet ⇒ the `setup` flow above first
  (outside herdr that means handing the user the `setup --reuse` command for a terminal window of their
  own, never for this session), then `away on` again.
- **`off`** — `away off` (the switch only; the group and the daemon stay).

## Ask a question

Feed one JSON object on stdin through a quoted heredoc (the fields contain quotes and line breaks;
argv would mangle them). The call blocks until the human answers, the wait times out, or the channel fails.

```bash
ANSWER=$(agent-lark ask <<'JSON'
{
  "title":       "Keep or delete the scratch directory when no checkout exists",
  "doing":       "Letting the requirements assistant run before the project code is checked out",
  "description": "Until now the assistant required a local code directory. That restriction is lifted, so we must decide where its temporary subprocess runs when there is no checkout.",
  "blocker":     "With no code directory there is no natural working directory for that subprocess.",
  "options": [
    {"id": "keep", "label": "Keep a fixed directory", "consequence": "One directory per project. Leaves a scene to inspect after failures; the cost is directories piling up with nobody cleaning them"},
    {"id": "temp", "label": "Delete after use",       "consequence": "Clean, but nothing is left to inspect after a crash; debugging relies on logs alone"}
  ],
  "recommend": "keep",
  "reasoning": "Keep a fixed directory: users on this path are the ones most likely to have a broken setup, so a scene is worth having. Strongest objection: disk clutter accumulates.",
  "question":  "Keep a fixed directory, or delete after use?",
  "lang":      "en"
}
JSON
)
rc=$?
```

### The field contract: eight required fields, three optional

| field | what to write |
|---|---|
| `title` | One line. The phone's notification shade shows the card title, so put the hook here |
| `doing` | One sentence: which task this is |
| `description` | Background for someone who has seen none of the work: why you got here, what is involved, jargon explained on the spot |
| `blocker` | Exactly what is blocked |
| `options[]` | 2 to 5 items of `{id, label, consequence}`; `consequence` states the real outcome and its cost, not a code name |
| `options[].danger` | Optional. Irreversible or high-cost: a red button behind a native confirm dialog. **The recommendation may never be a danger option** — validation refuses it |
| `recommend` | The `id` of one option; with `select: "multi"`, a non-empty array of ids (the ones ticked by default) |
| `reasoning` | Why you lean that way **plus the strongest objection** |
| `question` | One question answerable in one sentence |
| `select` | Optional, `"single"` (default) or `"multi"`. Multi renders one tick box per option and a submit button, for "which of these" questions where several may apply. Single choice is the default for a reason: a button is one tap, a form is several |
| `lang` | Optional, `zh` or `en`: the language of the fixed wording (section labels, hints, button texts, "Answered"). **Pass the language you are configured to reply to the user in: `zh` if you reply in Chinese, otherwise `en`.** Omitted means `en`; any other value is rejected |

The content fields are written in whatever language you work in; only `lang` controls the wrapper.
Missing or empty fields, a wrong option count, a `recommend` that matches no id or names a danger
option, or a field over its size cap all fail validation at once, before anything is sent (exit 1).
The caps are generous (Feishu cards take far more text than a push notification), but the reader is on a
phone: [references/message-spec.md](references/message-spec.md) §3 has the numbers.

Two flags: `--timeout <seconds>` (default 43200, twelve hours) and `--urgent`, which additionally flags
the card to the app owner in-app (Feishu's own "urgent" ping). **Use `--urgent` only for an irreversible
action or a short timeout**: flag every question and none of them is urgent any more. If the flag cannot
be delivered (owner not recorded, scope missing), a `note:` line says so on stderr and the question is
sent and waits as usual.

### What comes back

- Exit 0: stdout is the reply, verbatim, plus one trailing newline (`$(…)` strips it).
- A button tap returns that option's **`label` text**, not its `id`. A multi-select submit returns the
  ticked options' labels joined with `、` (the ideographic comma), in card order. Free typing in the
  group returns exactly what the human typed. Match on the label, and be ready for anything else.
- The card on the phone is rewritten in place to `✅ … · Answered` (green header) with the reply on top.
  **Buttons lock on the first tap**: the closed card rides back on the tap's own callback, so a second
  tap cannot answer twice (it becomes a follow-up instruction instead, see "Several replies").
- **One pending question per project.** A second `ask` from the same project exits 4 with
  `this project already has a question pending on the phone; one at a time`; `notify` and `send-file`
  are not subject to this.
- The card stays in the group's history, so a wait longer than twelve hours is fine.
- **Mind your own tool timeout.** If your harness kills `ask` before it returns (most shell tools cap a
  command at minutes), the daemon sees the connection drop, rewrites the card to `⚠️ … · Cancelled` (grey,
  buttons gone), and you get no exit code; the human finds a dead question. Either set `--timeout` at or
  below your harness limit and treat rc 2 as a normal outcome, or run `ask` as a background job of your
  session with stdout and stderr redirected to files and read them when it ends. Details:
  [references/failures.md](references/failures.md) §3.

## Write for someone who saw none of the work

1. **The reader has no context.** Say what the task is, why it reached this point, and what each
   option actually does. Internal code names, pane ids, and branch names explain nothing.
2. **Never just throw options at them.** `reasoning` is mandatory for that reason: state your lean
   and the strongest argument against it.
3. **Every option is a button, so every option is one tap away.** Do not recommend an irreversible or
   high-cost option; mark it `danger` so it gets a confirm dialog, and confirm a high-stakes verdict with
   a second `ask` that restates what you are about to do.

Field-by-field guidance, the caps, what the card looks like on the phone, and a worked bad/good pair:
[references/message-spec.md](references/message-spec.md).

## Notify and files

`notify` pushes a card with a title and a Markdown body, no button, and returns as soon as Feishu has
accepted it. `send-file` sends one image or file into the group, with an optional caption.

```bash
agent-lark notify <<'JSON'
{
  "title": "Tests green, starting the migration",
  "body":  "All tests pass on the three CI runners.\n\nNext: **schema migration** on the staging database (about 10 minutes). I will notify again when it is done.",
  "lang":  "en"
}
JSON

agent-lark send-file ./shot.png --caption "Current layout"
```

- `title` and `body` are required and non-empty; `lang` is optional (it sets the language of later
  receipt and alert cards for this project; the notification card itself has no fixed wording). The
  body is Feishu Markdown: bold, lists, tables and fenced code blocks all render.
- `notify` exit codes: **0** sent (stdout: `Notification sent (a reply from the phone is injected into
  this pane as an instruction)`) · **1** input rejected, nothing sent · **3** channel failure (daemon not
  running, not connected to Feishu, send failed) · **4** this project is not bound. No rc 2: nothing is
  waited for. `send-file` uses the same codes; rc 0 prints `Sent to the project group`.
- Both are allowed **while a question of yours is still pending**, so you can report progress while
  waiting for a verdict.
- The human may answer a notification by typing in the group. The channel cannot tell a reply to the
  notification from a reply to a pending question: **while a question is pending, whatever the human
  sends counts as the answer to that question**; with nothing pending it reaches you as an instruction
  (next section but one).
- `send-file` only reads files that resolve (after `realpath`, so a symlink cannot escape) inside the
  calling project, the daemon's media directory, or the system temp directory; images (`png jpg jpeg gif
  webp bmp`) up to 10 MB, anything else up to 30 MB. Outside that it exits 1 and says which directories
  are allowed. A relative path is taken from the directory you run the command in.
- `notify` is for things that matter but need no answer: finished, crashed, blocked and giving up. Every
  card buzzes a phone, so do not narrate steps, and do not send a card just to have a change verified —
  fold that into the next real question.
- Two identical calls send two cards; nothing is deduplicated.

## Exit codes

| rc | meaning | sent? | what to do |
|---|---|---|---|
| 0 | Reply received; stdout has it | yes | continue |
| 1 | Input rejected; stderr lists every problem | **no** | fix the JSON (or the argument) and call again |
| 2 | No reply within the timeout | yes | decide yourself or ask again; a late reply still reaches you as an instruction |
| 3 | Channel failure: daemon not running, not connected to Feishu, send failed, daemon stopping; stderr says which | see stderr | start the daemon or wait for the connection (below), retry once; still 3 → stop and tell the user |
| 4 | A human must act: no credentials, project not bound, a question already pending, earlier groups to choose from, a state directory too deep for a Unix socket (`daemon` / `away on`: `set AGENT_LARK_HOME to a shorter directory`); for `unbind --dissolve`, Feishu refused to dissolve the group | no | relay stderr to the user in your own conversation, then retry (after `unbind --dissolve` there is nothing to retry: the record is gone, the group is the human's to dissolve) |
| 130 | The `ask` client itself was interrupted (Ctrl-C); the card is cancelled, the daemon is unaffected — do not restart it | yes | call again |

`notify` and `send-file` use 0 / 1 / 3 / 4 with the same meanings and never 2. Stderr text per case, what
to tell the user for each, and how to read a validation report: [references/failures.md](references/failures.md).

## Several replies, contradicting each other

The buttons lock on the first tap, but the human can still type after tapping, tap a button on a card
whose question already closed, or correct themselves in a later message. Only the first reply closes the
question (exit 0); each later one arrives as a separate instruction in your session — a late tap as
`(follow-up) I pick <label>`, a late submit as `(follow-up) I pick <labels>`, typed text as itself.
**Take the last one as the verdict** unless you have a reason not to. The channel does not merge, filter,
or judge.

The group has **one input box**, not one per card: a typed message is "the reply to the pending question"
if there is one, and a free-standing message otherwise. Never tell the human to "reply in that card";
tell them to "send a message in this group". A message written as a Feishu *reply* to one of your cards while
nothing is pending arrives with `(reply to: "<that card's title>")` on its first line, so you know what
"yes, do that" refers to.

## The daemon

One resident process holds the Feishu connection (a WebSocket the SDK keeps open; no public URL, no
webhook) for every bound project; `ask`, `notify`, `send-file` and the rest only talk to it over a local
IPC endpoint (a Unix socket, `~/.agent-lark/daemon.sock`, or a named pipe on Windows). If it is not
running they exit 3 without sending: `agent-lark: daemon is not running. Start it first: agent-lark daemon --detach`.

You may start it yourself, but **never from your own shell as a background job, a Monitor, or a
subagent**: it dies with you, and every message the human sends afterwards is lost silently.

- `agent-lark daemon --detach` starts it in its own session (inside herdr as well: there is no pane to
  open) and prints `daemon: started in the background, pid N (log ~/.agent-lark/daemon.log)`. `away on`
  does this for you.
- The daemon comes up **before** it reaches Feishu: IPC first, the handshake in the background with
  retries (5 s doubling to 60 s), so a machine that is offline does not crash-loop. Until the handshake
  succeeds, `ask` / `notify` / `send-file` / a `bind` that must create or look up a group exit 3 with
  `not connected to Feishu (<reason>); the daemon keeps retrying, try again shortly`; `daemon --status`
  shows `connected false` and the last error.
- `daemon --status` prints two lines (pid, connection, pending questions, bound projects, start time;
  then the media directory's retention and size — plus a `last error:` line while it cannot reach
  Feishu); `daemon --stop` asks it to shut down over the same
  endpoint. **`--stop` is refused (rc 4) while a question is pending** — those cards would turn into
  `⚠️ Cancelled` on the human's phone — unless you add `--force`, which cancels them (each waiting `ask`
  exits 3).
- Only bound groups are listened to; inside them no @-mention is needed — the group *is* the project.

Lifecycle, groups and bindings, environment variables and files:
[references/daemon.md](references/daemon.md).

## Messages the human sends on their own

Anything the human sends in the project's group while no question is pending is injected into your
session as an instruction, prefixed with the marker `[agent-lark remote] ` on the same line; the text
after the marker is the user's, unchanged. It is the user speaking, not another agent: treat it exactly
like input typed at the keyboard. You do nothing to receive it. Once it is in your terminal, the daemon
puts a `Get` reaction on that message — the one sign on the phone that the terminal has it. If delivery
is impossible (no herdr, pane gone, agent blocked on a prompt), the human gets an orange receipt card in
the group, not you.

- **Images and files** are downloaded first, one line per attachment, `[saved: <absolute path>]`, followed
  by `(attachments saved locally)` (or `(I sent attachments; they are saved locally)` when there was no
  text). Open them as you would any local file; they live under `~/.agent-lark/media/` and are swept
  after 7 days by default.
- **Voice notes**: a voice message on its own is injected as its transcript, plain — nothing marks it as
  spoken; only when the message also carries text does the transcript follow that text as
  `(voice transcript) <text>`. When Feishu will
  not transcribe, you get one plain sentence instead (with Feishu's error code and message: the app may
  lack the `speech_to_text:speech` scope, or the tenant is on Feishu's free plan, which cannot call speech
  recognition at all): tell the user to type it this time. The audio file is still saved and listed.
- Everything a question receives while pending (text, attachments, voice) is that question's answer,
  not an instruction, and is not injected.

**When you see the marker, the user is on the phone**: answer in the terminal as usual, and push the
same answer with `notify` so it reaches them where they are.

Injection needs herdr (the daemon calls `herdr agent prompt <pane>`); the target pane is the one your
last `agent-lark` command ran from. Outside herdr the human only ever gets the receipt card; `ask` and
`notify` work the same everywhere.

## Remote mode and the per-project state file

Whether to route decisions to the phone is the caller's policy (a rule in the user's own config, not
this skill). The human sets the channel up once per machine and once per project:

```bash
agent-lark setup                                   # once per machine, on a terminal: menu — 1) new app by QR code  2) reuse an app (App ID + Secret typed there)
# once per project: tell the agent to turn remote mode on (or type /agent-lark on); it runs away on from its own pane so that pane is recorded
```

- **No credentials yet** (`away on` exits 4 with `No Feishu app credentials yet. Run once: agent-lark setup`):
  do not just tell the user to run `setup` — ask them first whether to **scan a QR code for a new app**
  or **reuse an app they already have**, then follow the `setup` flow in "Invoked with an argument": QR
  code ⇒ you run `setup` and hand over the URL line (or a PNG of it); reuse ⇒ you run `setup --reuse`,
  which inside herdr opens its own pane for the human to type the App ID and App Secret (the secret
  never reaches you) and reports back with one `[agent-lark] setup:` line, and outside herdr exits 4 with
  the command for the human to run themselves. The user must run it in a terminal window of their own (Terminal, iTerm, …). Never suggest running it inside this session — a `!`-prefixed command, a shell tool, a background job: none of them has a TTY, and the CLI refuses without one.
  The four report lines, verbatim:
  - `[agent-lark] setup: credentials stored for cli_xxxxxxxx (<app name>); the scopes must be enabled in the developer console before use` — done; remind the user of the console work if they have not done it, then `away on` again.
  - `[agent-lark] setup: failed: <why>` — every end that is not success or Ctrl-C: three failed probes — refused or thrown — (`3 probes refused (<error>)`), the `AGENT_LARK_OFFLINE` guard, any other failure; relay `<why>` (the secret is masked as `***` wherever it could appear).
  - `[agent-lark] setup: interrupted before any credentials were stored` — the human pressed Ctrl-C; ask whether to try again.
  - `[agent-lark] setup: credentials already stored (<origin>); nothing changed. To switch apps run agent-lark setup --reset --reuse` — there was nothing to do.
  `setup` in any form with credentials already stored only reports them — `Credentials already exist
  (from <origin>). …`, rc 0, no pane opened; `setup --update` rescans the QR code for the same app (adds
  scopes; on a terminal the menu comes first); `setup --reset` forgets the stored credentials first, so `setup --reset --reuse` switches to
  another app. Credentials live in the OS keychain (or a
  0600 `credentials.json`); `AGENT_LARK_APP_ID` / `AGENT_LARK_APP_SECRET` in the environment override
  them for one process — that is the only way in besides `setup`.
- `away on` does everything in one command: checks credentials, starts the daemon if needed, waits up to
  15 s for it to reach Feishu, binds this project to a group, and only then flips the switch. **Relay its
  stdout to the user.** The first line says whether the daemon was started (`daemon: started in the
  background, pid N (log …)`) or was already running; the switch line is `Remote mode is on: decisions, and moments when the agent is
  stuck on a prompt that needs you, are pushed to this project's Feishu group.` — the last line inside herdr; outside herdr one more
  line follows it, `Not inside herdr: messages sent from the phone are not injected anywhere, and there is no stuck-on-a-prompt alert.`
- **Which group** (all on stdout, before the switch line): `Created Feishu group "<task> [<dir>]"` (the
  app owner is invited; the group description carries `agent-lark · <project root>` so it can be found
  again), `Took back Feishu group "…"` (a group this project used before, renamed to the new task),
  `Connected to Feishu group "…"` (already bound; `--name` renames it).
- **Exit 4 with earlier groups on offer**: when the project has no live group but groups it let go of
  earlier exist (on record, or found in Feishu by their description), `away on` refuses to pick for you:
  ```
  agent-lark: this project has no live group, but 1 earlier group(s) could be taken back (renamed) instead of creating another:
  old task [proj]  released 2026-01-02T03:04:05.000Z  oc_xxxxxxxx
  ask the user which to reuse (rename) or create new; rerun with --reuse <chatId> or --new
  ```
  Relay the list; the human chooses; rerun with `--reuse oc_xxxxxxxx` or `--new`. This is the normal
  path for a project that had a group before, not an error.
- **While remote mode is on and you are inside herdr**, the daemon also pushes a `🔔 [<dir>] waiting for
  you` card (orange; `等你输入` in `zh`) when herdr reports your session `blocked` — a permission prompt, a choice
  dialog, anything only the human can answer — at most once a minute per project, and never while a
  question of yours is pending. Nothing is pushed for "finished" or "idle".
- `rename "<task>"` renames the live group to `<task> [<dir>]` when the work changes; `unbind` lets the
  group go when the work is done (the group stays in Feishu; the next `away on` in the same directory
  offers it back), `unbind --dissolve` dissolves it in Feishu and forgets it — ask the human which they
  want first. `bind [--chat <id>] [--name …]` binds without switching remote mode on, and `--chat`
  names a group outright (one the human created, or after the local records were lost). Task names are
  at most 60 characters.
- `away off` only flips the switch; the binding stays. **Remote mode changes the channel, not the
  standard**: irreversible actions still need explicit approval, and a timeout is not approval.

The switch and the group live in `<project root>/.agent-lark/state.json` (project root = the git
toplevel, else the cwd; a worktree or a submodule is its own project), written by `away on|off`, `bind`
and `unbind` (and by the daemon, `chatId` only, when it finds the live group gone from Feishu — Housekeeping).
Read it with `away status --json`:

```json
{"away":true,"chatId":"oc_xxxxxxxx","target":"/Users/me/work/my-project","updated":"2026-09-15T04:03:11.902Z"}
```

`away: true` means the human is away and expects decisions on the phone. `chatId` is the group this
project is bound to right now (`null` until bound, and again after `unbind`); `target` is the project
root; `updated` is UTC, ISO 8601. If the directory is absent, the project never used the channel and
nothing is written (`away status --json` then prints `{"away":false,"chatId":null,"target":"<root>","updated":""}`).
The file never holds credentials, and the injection target (the herdr pane) is not in it either — the
daemon keeps that on the binding.

## Housekeeping

- The unit is the **project** (git toplevel, else the cwd): one group, one pending question at a time,
  shared by every pane and session in it. The group is named `<task> [<dir>]`, so the human can tell
  projects apart on the phone.
- The pane your last `agent-lark` command ran from is remembered as the injection target; `ask`,
  `notify`, `send-file`, `bind`, `rename` and `away on|off` refresh it. **Run them from your own pane**, not from a
  helper process elsewhere, or the user's next phone message lands in the wrong pane.
- When your task ends, ask the human whether the group should stay. Keep it: `unbind` (the group stays
  in Feishu, the next `away on` in this directory offers it back). Drop it: `unbind --dissolve` (the group
  is dissolved in Feishu and its record forgotten; rc 4 means Feishu refused — the app can only dissolve
  a group it owns, which every group it created through `away on` / `bind --new` is, so a refusal only
  happens for a human-made group adopted with `bind --chat` — so the record is gone but the human has
  to dissolve the group by hand; the daemon
  clears the group's marker so it is not offered back meanwhile, and says so if that failed too). `away off` is
  the human's call, not yours. `status` shows credentials, herdr, the daemon and every binding, live and
  released.
- Records of groups that no longer exist in Feishu (dissolved, or the bot removed from them) are
  forgotten by the daemon once a day, right after its first handshake with Feishu, and whenever `away on` /
  `bind` looks for a group to offer back — a
  live one included, in which case the project's `state.json` loses its `chatId` (the `away` switch is
  left as it was) and the next `ask` exits 4 as not bound. Nothing is forgotten while Feishu's group list
  cannot be read in full.
- Attachments the human sent live under `~/.agent-lark/media/` and are deleted after 7 days
  (`AGENT_LARK_MEDIA_TTL_DAYS`; `0` keeps everything). Copy what you need into the project.
- Credentials are in the OS keychain (or a 0600 file), never in this skill's directory or in any output,
  and the App Secret is typed by the human in an interactive `setup` — it never passes through argv, a
  file you write, or your session; the group id appears in `state.json` and `bindings.json`, the
  project's absolute path in the group's description on Feishu's servers.
- After an upgrade, restart the daemon (`daemon --stop`, then `--detach`); credentials, bindings and
  the per-project state files carry over.

## References

- [references/message-spec.md](references/message-spec.md): writing the question, `select` / `danger` / `--urgent`, the caps, what the phone shows, bad vs good.
- [references/failures.md](references/failures.md): every exit code with its stderr, what to relay to the user, validation reports, Feishu-specific failures.
- [references/daemon.md](references/daemon.md): daemon lifecycle, groups and bindings, environment variables and files, the state file.
