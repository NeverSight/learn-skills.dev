---
name: rigs
description: Use when the user mentions OpenRig, rigs or the rig command, or wants a team of coding agents (Claude Code, Codex) on their project. That includes installing, setting up, starting or updating OpenRig, seeing or getting back to their OpenRig agents, TUI or operator, starting or sharing a team, and joining this session to one.
---

# rigs: your route into OpenRig

OpenRig runs a team of coding agents (Claude Code, Codex and others) side by side in tmux. A local daemon keeps their
tasks, messages and state, so the team keeps working across restarts. This skill gets OpenRig installed, gets a team
working on what the person wants, and shows how to work with that team from here.

**The goal is a team doing the person's work, not just an install.** Go through the steps in order and stop early only
if the person asks you to. When they say what they want built, give it to OpenRig's operator (step 2) instead of
building it yourself.

Tell the person what you're about to run and why before you run it. Don't install system packages or change their
machine without a yes. Starting OpenRig and a team writes files: Codex hooks and settings in
`~/.codex/config.toml`, a discovery skill in `~/.claude/skills` and `~/.agents/skills`, and, in the repository, managed
guidance in `AGENTS.md` or `CLAUDE.md` plus the team's skills and plugins. Say so before you start OpenRig
([the full list](https://github.com/mvschwarz/openrig#what-openrig-changes-on-your-machine)).

## 1. Install OpenRig, if it isn't installed

- **Check first:** `rig --version`. If it prints a version, go to step 2.
- **What it needs:** macOS or Linux, Node.js 22 or 24, tmux, and Claude Code or Codex signed in. Check only what's
  missing: `node --version`, `tmux -V`, `claude auth status` or `codex login status`.
- **Install:** `npm install -g @openrig/cli`, then `rig preflight` (Node, tmux, the daemon port and state folders)
  and `rig doctor`.
- **Then go on to step 2:** say it's installed and ask what they want worked on, and in which repository. A plain
  "install OpenRig" includes this. Stop here only if they say not to start a team.
- **If something fails:** `rig context get help` is the help guide for the installed version. If `rig` itself won't
  run, use https://www.openrig.dev/help/agents. Getting started: https://openrig.dev/docs/getting-started

## 2. Open OpenRig and give its operator the goal

- **Start OpenRig:** `rig daemon status`, and `rig daemon start` if it isn't running. `rig preflight` and `rig doctor`
  don't start it. Starting it also starts OpenRig's own team, the kernel, whose operator sets up the person's team.
  Keep it.
- **Show them OpenRig, the handoff:** once OpenRig is running, open the OpenRig TUI and operator for the person. Say
  you're opening it, then run `rig terminal open saved:kernel --window` on the daemon's desktop. This is the next step
  after installing or starting OpenRig, and the way back whenever they want their agents or OpenRig again. Don't wait
  to be asked or for particular words. If they've said not now, give them that command for later. It opens a view
  itself, using herdr when installed or plain tmux otherwise:
  - **Inside Herdr** (you run in a Herdr pane): it switches the person's Herdr to an `openrig kernel` space, reusing a live
    one. No new window and no macOS prompt; their own spaces stay in the sidebar.
  - **In Terminal or Ghostty:** a new tab or window the size of theirs.
  - **From Claude Desktop, iTerm or VS Code on a Mac:** a new Ghostty window when supported, otherwise Terminal. Only
    here, tell the person before running it that **Allow is fine** if macOS asks to control that app.
    `echo $TERM_PROGRAM $__CFBundleIdentifier` tells you where you run. `herdr`, `Apple_Terminal` or `ghostty`, or
    `tmux` with `com.apple.Terminal` or `com.mitchellh.ghostty`, mean no macOS prompt, so don't mention one. `tmux`
    with anything else (iTerm, VS Code) can prompt, so say Allow is fine first.
  - **Layout:** under 120 columns the operator fills the first page; from 120, the dashboard and operator share it. The
    advisor has its own tab or tmux window.

  Then tell the person in a sentence or two where it opened and that the operator is ready for what they want to
  build. Don't list agents or statuses (the TUI shows them), and don't suggest a command for them to type.
  Preserve the current terminal. If OpenRig's notes say it couldn't confirm the view, say so plainly. If it's already
  open, point them to it rather than opening another. Only if the window cannot open, `rig tui --shared` is the
  dashboard-only fallback; explain the failure and help with the chosen fallback. Herdr is visible only in a terminal
  the person can see; switching the shared TUI to `:terminals` does not open one. No and headless/SSH use are valid
  background outcomes. Provider-only `--provider herdr` or `--provider cmux` is for an existing provider workspace,
  not the first desktop window.
- **If the window can't open, or over headless SSH:** say plainly that no visible terminal was opened, and ask the
  person to open a new terminal window or tab on the daemon's host. Over SSH, that's a new SSH session to it with the
  known account. If you only know an HTTP daemon address, ask for the SSH details rather than inventing them. Then
  give them one complete command:
  - **The command OpenRig printed:** when `rig terminal open saved:kernel --window` can't open a window, it says why
    and ends with `run:` and a command (the `error` field with `--json`). That command already names the installed
    herdr binary and the daemon's socket, or the conversation to attach. Relay it exactly rather than composing one.
    If a note asks you to place the view once Herdr starts, run that `rig terminal open` yourself after they start it.
  - **If it printed no command:** find `operator.agent` in
    `rig ps --nodes --rig kernel --json --fields logicalId,canonicalSessionName,tmuxAttachCommand` and give
    `env -u TMUX` followed by its `tmuxAttachCommand`, exactly as listed (never a guessed name), for the operator's
    conversation. That command names the daemon's tmux server when it isn't the default one.

  For any other failure, the table under "What can interrupt installation and the OpenRig view" in
  `rig context get reference/getting-started.md#open-the-kernel-conversations` says why and what to do next.
- **Give the operator the goal:** ask what they want worked on, in which repository and on which branch, unless they've
  said. Find the `operator.agent` row in `rig ps --nodes --rig kernel --json`, take its `canonicalSessionName`
  (never the logical ID or a guessed name) and send:
  `rig send <canonicalSessionName> 'This is the agent that installed OpenRig. The person will answer in your pane. Goal: <goal>. Project folder: <absolute path>. Branch: <branch>.'`
  Or the person types the goal and folder in the operator's pane. If they give you a goal later, forward it the same
  way. The operator helps them pick a team that fits their logins, starts it on their yes and gives the goal to the
  team's lead. Before that yes, it says what launching into their folder changes for their own agent there; relay
  that with the question. Show them where the operator answers, and don't build the project yourself.
- **Relay the operator's questions:** the operator asks in its own pane, and the person may not be looking there.
  After each step you hand it, read its screen with `rig capture <canonicalSessionName>`. When it asks the person
  something (start this team? which folder? which option?), ask them here in the operator's words and send their
  answer back with `rig send`, or tell them to answer in the operator's pane. Unlike a prompt or a menu, a question
  doesn't show up as a stopped seat, so don't leave it to a background wait.
- **Installation is finished** when the operator is ready and the person is talking to it; a healthy daemon alone isn't
  that. If they'd rather talk later, keep that choice, leave them the exact connection step and say the handoff to the
  operator is still pending.
- **See what's running:** `rig ps`, then `rig ps --nodes --rig <rig>` for a team's agents. If a team is already
  running in that repository, tell the operator.
- **Check it's ready before you say so:** `rig ps --nodes --rig <rig>`. If an agent is stopped at a prompt or a menu,
  read it with `rig capture <seat>@<rig>` and answer with the key that screen shows (`rig send --help` says how to
  send a digit, a letter or Escape), or ask the person. Capture it again before sending anything more.
- **Join this session to the team, if that helps:**
  `rig attach --self --rig <rigId> --pod <pod> --member <name> --runtime <claude-code|codex> --print-env` adds this
  session as a new member of a pod. `--node <logicalId>` binds it to an existing seat instead. Attach once, and keep
  the variables it prints (`OPENRIG_NODE_ID` and `OPENRIG_SESSION_NAME`). Each command may run in a fresh shell, so put
  them in front of every later `rig` command. Check with `rig whoami --json`.
- **Replies:** other agents can't type into this session. Read work sent to you with
  `rig queue list --destination <your address>` and `rig queue show <id> --full`, and read an agent's screen with
  `rig capture <seat>@<rig>`.

## 3. Follow the work to its result

- **Find the team's task:** the operator gives the goal to the team's lead as a queue task: `dev-build@starter`, or
  `orch-lead` in `workshop` and `factory` (for starter and factory, `rig specs preview <name> --kind rig` says what
  each seat does; for a running team, `rig ps --nodes --rig <rig>`). Find it with
  `rig queue list --destination <seat>@<rig> -a`.
- **Follow it to the result:** a task that changed hands isn't finished. `rig queue show <id> --full` names the seat it
  went to, and that seat's next task is the one whose `handedOffFrom` is that ID
  (`rig queue list --destination <seat>@<rig> -a -o json`). Follow each handoff until an agent reports the result, and
  use `rig capture <seat>@<rig>` to see what it's doing. Then read what it produced and tell the person what the team
  actually did (the branch, commit, review or PR text), not just that you sent it.
- **Give the team more work:** write the goal to a file: what to change, in which repository and branch, what done
  looks like, and that the result comes back to you (the branch or commit, the review, any PR text). Then
  `rig queue create --source <your name> --destination <seat>@<rig> --body-file <file>`, and tell that agent with
  `rig send <seat>@<rig> "task <id> is yours"`. A message informs, and a queue task is the work someone owns.
  `--source` names you when this session hasn't joined the team.
- **Then ask what's next.** If no team can take the work, fix that or ask the person. Don't quietly do it yourself.
- **Other ways to work with the team:** `rig send <seat>@<rig> "..."` types into an agent's terminal,
  `rig capture <seat>@<rig>` reads its screen, and `rig ps --nodes --rig <rig>` shows who's on it.

## 4. Find out more

- **How OpenRig works:** `rig context profile world-public --situation fresh`.
- **What you can do:** `rig context get onboarding-width` (the capability map).
- **Everything in the library:** `rig context list`.
- **Exact syntax:** `rig <command> --help` is always current for the installed version.

Written for OpenRig 0.6.7. When something here and `--help` disagree, `--help` wins.
