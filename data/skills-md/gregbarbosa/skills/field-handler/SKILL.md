---
name: field-handler
description: Use when project work is growing complex or splitting into independent strands that could progress in parallel across separate sessions, such as several related projects moving toward one goal, or a single effort branching into pieces that don't depend on each other. This skill SURFACES the option and ALWAYS agrees the scope with the user before it spawns anything. Requires herdr >= 0.9.0 and HERDR_ENV=1.
---

# field-handler — run a room of field agents

Before you use this skill, check that `HERDR_ENV=1`. If it is not `1`, tell the
user that you do not run inside a herdr pane. Then stop.

Run `herdr --version`. This skill needs **0.9.0 or later**. On an earlier
version, tell the user to run `herdr update`. Then stop.

Read the **`herdr`** skill for the command surface. Read the **`field-agent`**
skill for the dispatch contract. This skill is the multi-agent form of
`field-agent`. It uses the same ledger, the same watch loop, and the same three
rules.

Two directories matter below:

- `<skill_dir>` — this skill's own directory, from the `Base directory for
  this skill:` path at the top. It holds `handler.json`.
- `<agent_dir>` — the `field-agent` skill's directory. It holds `field.py` and
  `harnesses.json`. Find it with
  `find ~/.claude ~/.agents -maxdepth 5 -type d -path '*skills/field-agent' 2>/dev/null`.
  Do not use a `*` glob in a plain `ls`; zsh aborts the whole command when one
  glob does not match, and you lose the valid path too.

The search covers BOTH roots on purpose. A single-agent install puts skills in
`~/.claude/skills`; a multi-agent install puts them in `~/.agents/skills`, and
Codex, Copilot, Gemini and pi read the second one. Searching only `~/.claude`
makes this skill fail on a perfectly normal multi-agent install.

**These four skills are one suite.** `field-agent`, `field-handler`,
`field-audit` and `herdr` install together and depend on each other. If the
`find` above returns nothing, the suite is not fully installed. Do not
improvise a replacement and do not write your own ledger. Tell the user to run
the command below, then stop.

```bash
npx skills add gregbarbosa/skills -s '*' -g -y
```

## You are the handler

**This session is the handler.** Each agent you start is a **field agent**. You
do not delegate the watching to another pane. You open the room, you steer it,
and you report to the user.

A handler does five things. All five are required.

1. **Agree** the scope with the user before you spawn anything.
2. **Dispatch** each field agent with a brief that names both parties.
3. **Record** every field agent in the ledger.
4. **Watch** the room, so a finished agent reaches you without your attention.
5. **Triage** each report: read the work, verify it, then act or escalate.

**One consequence to expect.** A field agent reports by prompting you. Those
callbacks arrive as turns in this session, mixed in with the user's own
messages. Once the room is up, this session works the room. Tell the user that
in step 7.

## The three rules

1. **Address every agent by name, never by a pane id.** A pane id changes when
   the pane moves, and a closed pane's id resolves to nothing. A callback sent
   to a stale pane id goes nowhere.
2. **Every brief carries the identity block.** A field agent cannot report if
   it does not know your name and the exact command that reaches you.
3. **The callback is best effort. The watch loop is the guarantee.** A field
   agent that crashes sends no callback.

## Two phases: never skip Phase A

You MUST NOT begin Phase B until the user has explicitly agreed to a scope.

- **Phase A, offer and agree.** Name the independent strands, propose a scope,
  and discuss. Spawn nothing.
- **Phase B, open the room.** Only after an explicit go.

If this skill surfaced on its own, you are in Phase A. An offer is not a spawn.

## Phase A: offer and agree

1. **Offer.** In one or two sentences, name the independent strands you see.
   Offer to run them in parallel panes that you steer. Example: "This splits
   into three independent pieces. I can run a pane per piece and work them from
   here. Do you want that?"
2. **Propose a roster.** Map the goal to concrete projects. Use these sources
   in order:
   - The ledger: `python3 <agent_dir>/field.py status`. This shows work already
     dispatched, with its pane, branch and verdict.
   - Live panes: `herdr agent list` and `herdr workspace list`. The
     `terminal_title_stripped` of each agent says what it does now.
   - Dated `tries/` subdirectories and branches whose names match the goal.
   - The agent brain, for project relationships.

   Present the roster as a short list: each project, its path and branch, and
   the one job that field agent owns.
3. **Discuss.** Add or drop projects. Adjust each job. Spawn nothing yet.
4. **Get an explicit go.** Then start Phase B.

## Phase B: open the room

### Step 0 — claim your own name and arm the watch loop

```bash
herdr pane current --current | python3 -c 'import sys,json;print(json.load(sys.stdin)["result"]["pane"]["pane_id"])'
herdr agent list | python3 -c 'import sys,json;print([a.get("name") for a in json.load(sys.stdin)["result"]["agents"]])'
herdr agent rename "<self_pane>" m
```

Call the pane id `<self_pane>` and the name `m`. Read the pane id live. Do not
trust `$HERDR_PANE_ID`; it goes stale after a pane move.

An agent record has NO `name` key until something names it, so always read the
name with `.get("name")`. A plain `a["name"]` raises `KeyError` on the first
unnamed pane, and most panes are unnamed.

If a live agent already holds `m`, use `m-<short-theme>` and use that name
everywhere below.

**Arm the watch loop now, before you spawn anything.** Use the `Monitor` tool:

```
Monitor(
  description: "herdr field agents reaching done/idle/blocked",
  persistent: true,
  command: "FIELD_HANDLER_PANE=<self_pane> python3 <agent_dir>/field.py watch --interval 15"
)
```

Only ONE watch loop may run on this machine. Two watchers share one state file
and print every event twice. If you already armed one in this session through
`field-agent`, keep it and arm nothing here.

Then run `python3 <agent_dir>/field.py catchup` once, to surface an agent that
settled before you armed the loop.

### Step 1 — finalize the roster

Build a list of `{ project_name, agent_name, abs_path, branch, task }`, plus
the shared `theme` (one line). `agent_name` is a short kebab slug of the
project. herdr requires `[a-z][a-z0-9_-]{0,31}`; keep it under 24 characters.
Names must be unique among live agents; check `herdr agent list`. On a name
conflict at launch, retry once with a numeric suffix.

### Step 2 — read the config

Read `handler.json` in `<skill_dir>`. Fields: `agent.command`,
`agent.model_flag`, `model_floor`, `layout_threshold`. If the file is missing
or is not valid JSON, use this default and tell the user:

```json
{ "agent": {"command":"claude","model_flag":"--model sonnet"}, "model_floor": "sonnet", "layout_threshold": 4 }
```

`layout_threshold` is the number of field agents that still share ONE tab.
At or below it, each agent gets a pane in that tab and the user sees the whole
room at a glance. Above it, each agent gets its own tab, because a wider grid
makes every pane unreadable.

**`model_floor` is Sonnet, and it is not a preference.** Measured 2026-09-08:
`--permission-mode auto` is SILENTLY IGNORED on Haiku 4.5. A field agent on
Haiku stops at its first tool call, and you see `blocked` with no obvious
cause. Never drop a field agent below the floor, even for a task that looks
trivial. If the user asks for Haiku, tell them this and let them decide.

For a per-agent harness override that the user named, resolve `command`, `kind`
and `auto_flag` from `harnesses.json` in `<agent_dir>`. An entry whose
`command` equals its `kind` is **canonical**. An entry whose `command` differs
(glm, ds) is a **wrapper** and takes the fallback path in step 5.

### Step 3 — decide isolation per field agent

A field agent needs a git worktree when BOTH of these are true:

1. Another roster entry shares its repo, or its `branch` differs from what that
   checkout has now.
2. It will commit, or change branch.

A shared-checkout agent that runs `git checkout -b` switches every other
session in that directory, including this one. Two read-only agents in one
repo need no worktree; keep them in the room workspace, and say in each task
that the agent must not commit or change branch.

### Step 4 — create the room, in the CURRENT workspace

**Never create a workspace for the room.** The room belongs in the workspace
the user is already in. You stay in your tab; the field agents get their own
tab beside it. That way the user switches ONE tab to see the whole room, and
switches back to talk to you. herdr's own guidance says the same: do not
create a workspace, tab or worktree beyond what the user asked for.

Read your workspace live. Do not trust `$HERDR_WORKSPACE_ID`:

```bash
WS=$(herdr pane current --current | python3 -c 'import sys,json;print(json.load(sys.stdin)["result"]["pane"]["workspace_id"])')
```

**N <= `layout_threshold` — ONE tab, one pane per agent.** Create the tab with
the first agent's directory, because its root pane becomes that agent's pane:

```bash
herdr tab create --workspace "$WS" --label "field agents" --cwd "<abs_path_1>" --no-focus
```

Parse `.result.tab.tab_id` and `.result.root_pane.pane_id`. That root pane is
agent 1. Then split for the rest, splitting a wide pane RIGHT and a tall one
DOWN, so the grid stays readable:

| Agent | Split |
|-------|-------|
| 2 | `herdr pane split "<pane_1>" --direction right --cwd "<abs_path_2>" --no-focus` |
| 3 | `herdr pane split "<pane_1>" --direction down --cwd "<abs_path_3>" --no-focus` |
| 4 | `herdr pane split "<pane_2>" --direction down --cwd "<abs_path_4>" --no-focus` |

Parse `.result.pane.pane_id` from each. Four agents give a 2x2 grid; three
give a split left column beside a full-height right column. Verified on
herdr 0.9.0.

**N > `layout_threshold` — one tab per agent, still in `$WS`.** Above four,
a grid gives each agent an unusably narrow column, so trade the single glance
for readable panes:

```bash
herdr tab create --workspace "$WS" --label "<project>" --cwd "<abs_path>" --no-focus
```

Parse `.result.root_pane.pane_id`.

**Worktree agents are the one exception.** `worktree create` always makes its
own workspace; herdr gives no way to put a worktree in an existing one. Those
agents therefore live outside the user's workspace. Say so in step 7.

```bash
herdr worktree create --cwd "<repo>" --branch "<branch>" --label "<project>" --no-focus
```

Parse `.result.root_pane.pane_id` and note `.result.worktree.path`. Put
absolute paths in that agent's task, because its checkout is not the repo the
user is looking at.

CAUTION: a worktree workspace closes itself when its last pane closes, and
`herdr worktree remove` accepts only `--workspace ID`. Remove the worktree
BEFORE its pane closes, or the checkout is orphaned and only
`git worktree remove` can clear it. `field-audit` does this in the right
order.

Do NOT pass `--env HERDR_AGENT=<kind>`. Older versions of this skill did.
herdr 0.9.0 does not read that variable: the only matching string in the
binary is `HERDR_AGENT_DETECTION_MANIFEST_CATALOG_URL`, a different setting.
herdr detects a wrapper harness by sniffing the TUI it draws, so the flag was
always a no-op.

### Step 5 — launch and register every field agent

Launch and register EVERY field agent before you prompt any of them. Do not
prompt yet.

**Canonical harness:**

```bash
herdr agent start "<agent_name>" --kind <kind> --pane "<pane_id>" -- <model_flag words> <auto_flag words>
```

`agent start` needs a pane that sits at an interactive shell prompt with no
foreground command. It never creates or moves layout; step 4 made the pane.
Startup defaults to a 30-second timeout. If a dialog blocks the agent during
startup, herdr returns `agent_not_ready` but keeps the name usable for
`agent read` and `agent send-keys`. Clear the dialog, then continue.

**Wrapper harness** (glm, ds) — run it, **wait for herdr to DETECT it**, then
wait for readiness, then **name it**. Do not skip the rename; an unnamed agent
breaks Rule 1:

```bash
herdr pane run "<pane_id>" "<command> <auto_flag>"

# Poll until herdr detects an agent in the pane. Measured: about 2 seconds.
for i in $(seq 1 60); do
  A=$(herdr pane get "<pane_id>" | python3 -c 'import sys,json;print(json.load(sys.stdin)["result"]["pane"].get("agent") or "")')
  [ -n "$A" ] && break
  sleep 1
done
[ -z "$A" ] && echo "herdr never detected an agent in <pane_id>" && exit 1

herdr agent wait "<pane_id>" --until idle --timeout 60000
herdr agent rename "<pane_id>" "<agent_name>"
```

CAUTION: do not drop the polling loop. `pane run` returns as soon as it sends
the command, before the TUI draws. An `agent wait` issued at that moment fails
with `agent_not_found` in about 0.04 seconds and exit 1; the `--timeout` never
applies. The `agent rename` on the next line then fails the same way, and the
agent is left running and unnamed. Measured on herdr 0.9.0.

**Clear the startup dialogs before you prompt.** Read the pane first:
`herdr pane read "<pane_id>" --source visible --lines 30`.

CAUTION: never send a blind `Enter`. Read the dialog, find the line marked
`❯`, and choose the option that matches your intent. The marked option is the
DEFAULT, and on several dialogs the default is the one you do NOT want. Move
with `Down` or `Up`, then send `Enter`.

- **Folder-trust dialog** ("Is this a project you created or one you trust?").
  The default is **"No, exit"**. "Yes, I trust this folder" is the SECOND
  option. A blind `Enter` QUITS the agent. Send `Down`, then `Enter`. This
  dialog is NOT reliable to predict: on 2026-09-08 a fresh `worktree create`
  checkout did not raise it at all. Read the pane and react to what is there;
  do not assume it appears, and do not assume it does not.
- **Usage-credit dialog** ("Fable 5 now uses usage credits"). The default is
  **"Switch to Sonnet 5 and continue"**. A blind `Enter` silently downgrades
  the model. To keep the model you asked for, send `Down`, then `Enter`.
- **"New MCP servers found"**: send `Esc`.

Read the pane again after each keypress. Option order and defaults change
between Claude Code versions, so verify what is marked instead of trusting the
key sequence above.

CAUTION: `Enter` also submits whatever text sits in the input box. After you
clear a dialog, read the pane and check what the agent is now working on.

**Check the permission mode after launch. Do not assume the flag took.**
Measured on 2026-09-08: `--permission-mode auto` is silently ignored on
**Haiku 4.5**. The same flag engages on Sonnet 5 and on the glm wrapper. The
status line is the evidence:

```bash
herdr pane read "<pane_id>" --source visible --lines 3
```

`⏵⏵ auto mode on` means the flag took. `⏸ manual mode on` means it did not,
and the agent will stop at its first tool call. The handler then sees
`blocked` with no obvious cause. Use Sonnet or better for a field agent, or
expect to answer its permission prompts by hand.

If the pane shows a shell error, the launch failed. Tell the user and stop.

**Register the agent now, before you prompt it.** A crash between the prompt
and the register call leaves an untracked agent:

```bash
python3 <agent_dir>/field.py register "<agent_name>" "<pane_id>" "<harness>" \
  "<one-line task summary>" --branch "<branch or omit>" --cwd "<abs_path>"
```

### Step 6 — send each field agent its task

Send the task and the identity block as ONE prompt, on one line, with ` || ` as
the separator. Single-quote the inner commands, so nothing needs escaping.
Replace `m` with your actual name from step 0.

```bash
herdr agent prompt "<agent_name>" "<task>. Scope and read first; flag any irreversible change before you make it.  ||  === FIELD AGENT BRIEF ===  ||  You are field agent '<agent_name>' in herdr pane <pane_id>. Your handler is agent 'm'.  ||  REPORT TO YOUR HANDLER by running this command — this is the only way your work reaches anyone:  herdr agent prompt 'm' 'FIELD REPORT <agent_name>: <your message>'  ||  Report at these four moments, not only at the end: (1) START — one line when you understand the task and begin; (2) MILESTONE — one line each time you finish a unit, or about every 15 minutes; (3) BLOCKED — at once if you need a decision, a credential or an answer, and state the exact question; (4) COMPLETE — the verdict, every file path you changed, the branch name, and the test or build result.  ||  Prefix the last one with 'FIELD REPORT <agent_name>: COMPLETE —'.  ||  Report what you actually found. If the task rests on a wrong assumption, say so instead of working around it.  ||  If your report command fails, retry it twice.  ||  Do not ask the human directly. Route every question through your handler." --wait --until working --timeout 15000
```

**How to read the result.** On herdr 0.9.0, `--wait --until working` returns as
soon as the agent is working, and it returns immediately when the agent is
already working. Measured: about 0.5 seconds in both cases.

| Outcome | Meaning | What you do |
|---------|---------|-------------|
| Exit 0, `agent_status` is `working` | The turn started. | Go to the next agent. |
| Exit 0, `agent_status` is `done` or `idle` | A short turn finished already. | Read the pane. |
| `agent_blocked` | A dialog was up. herdr sent NOTHING. | Clear the dialog, then prompt again. |
| `agent_prompt_stalled` | herdr saw no activity after it submitted. | Read the pane. |

On a stall, read the pane. A prompt sent to a busy claude-kind agent QUEUES; it
does not inject into the running turn, and it is not stuck. Text in the input
box is stuck only when it matches what you just sent. Then send
`herdr agent send-keys "<agent_name>" Enter`. Retry a maximum of 3 times. If it
never submits, tell the user. Do not assume that it ran.

### Step 7 — announce, then work the room

State in one line which field agents are up, their models, the TAB that holds
them, which agents hold their own worktree (those sit in their own workspace,
not the user's), and that the watch loop is armed.

Then tell the user that this session now works the room, so their own
conversation here will share turns with the agents' reports. Offer `/loop` if
they want it to run hands-off.

Example: "Room up in tab 'field agents' beside this one: 3 Sonnet field agents
(a, b, c); c holds its own worktree, so it sits in its own workspace. Watch
loop armed. I will work the room from here, so this thread will fill with
their reports — switch to that tab to watch them, or leave it to me."

---

## Your standing duties while the room runs

**Run ONE assessment pass now.** `herdr agent list` gives every agent's
`agent_status` and live `terminal_title_stripped`. Cross-check it against the
roster. A roster agent MISSING from `agent list` is not gone; detection can lag
on a fresh worktree pane, so `herdr pane read` its pane directly. Only
`herdr agent read <agent_name> --source recent-unwrapped --lines 40` the agents
that look stuck, off-theme or missing. Report a short roll-up to the user.

**Address agents by NAME, never by a cached pane id:**
`herdr agent prompt <agent_name> "<one concrete instruction>"`.

**Only prompt an agent whose `agent_status` is `idle`, `blocked` or `done`.
Never prompt one that is `working`** unless you intend the prompt to queue
behind its current turn.

**Triage ONLY your roster.** The ledger and the watch loop are GLOBAL to this
machine, not scoped to this room. `catchup` and `[FIELD]` events will name
agents from the user's other sessions. For any agent that is not on your
roster, tell the user in one line and take NO other action. Never read, prompt
or close a pane outside this room's workspace. Prompting a stranger's `idle`
agent injects work into a session you know nothing about.

**Triage every event. Do not just acknowledge it.**

| Event | What you do |
|-------|-------------|
| `COMPLETE` / `[FIELD] DONE` | Read the pane. Verify the claim: check the files it names, and run the build or the tests when it touched code. Do not trust the summary. Then report and ack. |
| `[FIELD] BLOCKED` | Read the pane. Answer it yourself when the brief makes the answer unambiguous. Escalate to the user only when the decision is genuinely theirs. |
| `[FIELD] IDLE` | The agent stopped without a report. Read the pane. It finished quietly, or it stalled. Prompt it again, or triage it as done. |
| `[FIELD] GONE` | The pane closed before you read it. The work can still exist on a branch or on disk. Check, then report what was lost. |
| `MILESTONE` / `START` | Note it. Reply only to correct the agent. |

**After you verify an agent, record it and tell the user:**

```bash
python3 <agent_dir>/field.py ack "<agent_name>" "<verdict; files; test result>"
herdr notification show "Field agent done: <agent_name>" --sound done
```

**The ledger is the memory, not your context.** Write the task, the branch and
the verdict into it. Your context will be summarised; the file will not. After
a compaction, run `python3 <agent_dir>/field.py status` before you ask the user
anything.

**When you read an agent's pane, text in its input box is usually Claude
Code's auto-generated prompt SUGGESTION.** It is not a stuck submission and not
a user draft. Never resend or press Enter because of suggestion text.

**Do not poll and do not loop.** After the first pass, wait. Act when an agent
reports, when a `[FIELD]` event lands, or when the user asks. Do not use
`herdr agent wait` to supervise; it blocks your turn.

---

## Teardown

Do not close the room on your own judgment. An unread pane holds work that
nothing else records.

1. Run the **`field-audit`** skill. It reads each result, verifies it, reports
   a verdict, and closes only the panes that are provably finished.
2. Confirm with the user before you close a pane whose agent is still
   `working`.
3. Close the field-agent tab with `herdr tab close <tab_id>`, or single panes
   with `herdr pane close`. The room lives in the user's own workspace now, so
   there is no room workspace to close. NEVER close the user's workspace.
4. Worktree agents hold their own workspaces. Remove the worktree BEFORE its
   pane closes: `herdr worktree remove --workspace <workspace_id>` takes only a
   workspace id, and that workspace disappears with its last pane. After that
   only `git worktree remove <path>` can clear the checkout. The branch
   survives either way; delete it in the source repo when it is no longer
   needed.

## Failure modes and their fix

| Symptom | Cause | Fix |
|---------|-------|-----|
| A `COMPLETE` report never arrives | The agent crashed before its final step | The watch loop reports `GONE` or `IDLE`. Read the pane. |
| A callback reaches nothing | The brief carried a pane id, and the pane moved or closed | Address the handler by name. Rule 1. |
| Duplicate `[FIELD]` lines | Two watch loops run at once | Keep one. Stop the second `Monitor`. |
| `agent list` shows an unnamed agent | A wrapper harness launched without a rename | `herdr agent rename <pane> <name>`, then register it. |
| A prompt stalls in the input box | Bracketed paste, or a startup dialog | Read the pane. Clear the dialog. Send Enter. |
| The room finished hours ago, unread | No watch loop was armed | Arm it in step 0. Run `catchup` once. |
| `agent start` returns `agent_not_ready` | A startup dialog blocked the agent | The name still works. Read the pane, clear the dialog, continue. |
