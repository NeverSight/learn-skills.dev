---
name: codex-cu
description: Drive macOS apps and Chrome through the local Codex cua_repl MCP (server name codex-cu). Use this whenever the user says computer use, browser use, cua, codex-cu, or asks to click a native app or a Chrome page through the ChatGPT extension. Not for a normal web page that agent-browser can read, not for the Cursor built-in browser harness, and not for hover or document.cookie (those go to Claude in Chrome or agent-browser).
allowed-tools: Bash(ps:*), Bash(pgrep:*), Bash(open:*)
---

# Codex computer use

`cua_repl` is the MCP server inside the ChatGPT Mac app's Computer Use plugin.
Claude Code, Cursor, and agy call it under the name `codex-cu`. Clicks go into
the target app. They do not move the user's pointer.

The long write-up is the Claude artifact `codex-cu 接線手冊`. Open it in Arc
when this file does not answer a case.

https://claude.ai/artifact/VQQdp75aeC1PzqRwK581PU?sk=Usf3jftJdhrPrHUCB76Nuw

## Setup (once per machine)

Codex does not need this: `cua_repl` is native there. For Claude Code, Cursor
and agy, run the check first:

    bash ~/.agents/skills/codex-cu/scripts/check-codex-cu.sh

PASS: setup is done. Skip this section. The check never opens an app, so a
PASS is not proof that an app call works. SKIP with `no Computer Use plugin`:
the user must install the ChatGPT Mac app and its Computer Use plugin, then use
computer use there once (that grants Screen Recording and Accessibility). A
FAIL `launcher cannot resolve a usable version` (the installer says SKIP `no
usable Computer Use version yet`): show the user the reason text after the colon.
Only a missing or empty plugin cache means "still downloading, try later". In both
cases stop and tell them. Any other FAIL, or no `codex-cu` tool: ASK the user
which mode. Never pick for them:

- `all`: accept every prompt from codex-cu with no question, including any
  that is not an app prompt. Logged-in pages in a browser app become readable.
- `safe`: auto-accept Calculator, TextEdit, Preview, Freeform. It is an
  auto-accept list, not a sandbox: Claude still asks the user for other apps and
  the user may accept them; agy and Cursor are refused for other apps. The
  browser surface has no per-app approval in either mode.

Then run:

    bash ~/.agents/skills/codex-cu/scripts/install-codex-cu.sh all   # or: safe

It installs into `~/.local/bin`, registers `codex-cu` at user scope for Claude
Code and Cursor when their config file exists and for agy when the `agy` command
exists (the check prints a line per registered runtime), writes `~/.config/codex-cu/approve`, and ends with the
check. If you cannot ask (print mode, worker), stop and show the user both
commands. After setup, tell the user to start a new session: MCP servers load
at session start. To switch mode later, run the installer with the other word,
or edit the policy file (it takes effect at the next prompt, no restart).

The installer skips the first gate on purpose. Terminal, system settings and
Codex itself stay `forbidden` until the user runs
`defaults write -g ComputerUseAllowForbiddenTargets -bool YES` themselves.

## Two surfaces

Computer surface treats the target as an app. Read the AX tree, then click or
type. This surface does not need turn metadata. `scripts/codex-cu-mcp` is the
launcher.

Browser surface enters the page. Read the DOM, run JS, use Playwright locators.
Each `tools/call` needs Codex turn metadata. `scripts/codex-cu-proxy` injects
`_meta["x-codex-turn-metadata"]`. Computer surface does not need the metadata,
but its app approvals also go through the proxy (see below).

`cua.getState()` can return a full `apps` list and a `browsers` error together.
A metadata error on `browsers` does not mean the computer surface failed.

## Pick Chrome, not Arc

Arc and Chrome both report `name: "Chrome"`. The numeric `id` is not stable.
`profileName` can be absent. Do not use either as the only test.

1. Call `cua.listBrowsers()`.
2. Read `metadata.extensionInstanceId`.
3. Confirm the host parent before a long call.

```sh
ps -o ppid= -p $(pgrep -f "ChatGPT for Chrome")
```

The parent path is Arc or Google Chrome. Sample from 2026-10-05. Re-check
after a reload. Do not reuse these values once the parent check disagrees.

- Arc: `33f909be-429f-479e-b1c2-20bba462cbf3`
- Chrome: `75ef88d3-a921-455b-b39e-b40ed5ec2771`

`createBrowserTab` and `nameSession` on the Arc instance do not return. A 120s
wait still fails, and the call can leave `about:blank`.

## Browser surface

Use the Chrome instance from the parent check. One `js` call per step.

1. `cua.getBrowser({ extensionInstanceId })`.
2. `browser.nameSession` with a short name, before any new tab.
3. Record ids from `browser.user.openTabs()`.
4. Open one new tab and go to the URL.
5. Check the page. On example.com, `getByRole("link", { name: "Learn more", exact: true })` is visible.
6. Close only that tab.
7. Read `openTabs()` again. Prior ids match. The new id is gone.

A tab stays on the `session_id` that created it. A refused `createBrowserTab`
can still leave `about:blank`. Close it in that same session. Set `CU_SID` on
the proxy when you must reuse the session.

`document.cookie` is not available. `chrome://` URLs are not allowed. There is
no hover method. Browser surface does not ask for per-app approval.

Rehearsal that passed 2026-10-05: select `75ef88d3-…`, `nameSession` returns
at once, `URL=https://example.com/`, `learnMoreVisible=true`, the new tab is
closed, the prior tab ids are unchanged.

## Computer surface

Arc on this surface is an app, not a browser target.

1. Open a URL with `open -a Arc "<url>"`. Command-T is less stable.
2. `cua.getApp("Arc")`. Use the display name. Do not use a bundle id.
3. After a page change, `getAXState({ disableDiffing: true })`. The first read can show the old page.
4. Click by element index. Use `setValue` when `typeText` changes case.

`cua.computer.launch_app` and `cua.listWindows` are not in this runtime.

`getApp` needs the second approval, `Allow Computer Use to use X?`. The proxy
answers it from `~/.config/codex-cu/approve`, for every client (Claude, agy,
Cursor):

- `all` on its own line: accept every prompt (full mode, the deploy default).
- One display name per line: accept only those apps (safe mode).
- `all` mixed with names means only those names.
- Any other app, or no policy file: the prompt goes to the client. agy and
  cursor-agent cannot answer, so the proxy declines it for them. With no file,
  every app is refused in agy and Cursor.
- A Claude `Elicitation` hook that accepts codex-cu prompts overrides `safe` for
  forwarded apps. Remove such a hook; the policy file is the single source.

`scripts/test-codex-cu-proxy` runs the proxy against a fake child (accept,
forward, child death, slow client, two-way backpressure, bad policy, shutdown).

Shutdown: once the proxy has seen the client close stdin, it drops (and logs)
an approval prompt instead of answering or forwarding it. A prompt already
forwarded can still meet the close. `elicitation accept` in the log means the
reply was queued to the child. After the child exits, the proxy waits while
output still reaches the client; after 30 s with no progress it ends non-zero
(output may be incomplete), at most 5 s later if stderr is blocked.

A refusal reads `Computer Use was not approved to use X`. Add the display name
to the file; the next prompt reads it, no restart. The Chrome display name is
`Google Chrome`.

## Do not

WARNING: `getApp` returns the window text. Do not bind Notes, Mail, Messages,
Keychain Access, a password manager, or a terminal unless the user names that
app in the current message.

- Do not treat a metadata error as a dead computer surface.
- Do not pick a browser by numeric id.
- Do not call `nameSession` or `createBrowserTab` on the Arc instance.
- Do not close tabs that were already open.

## Not tested

Logged-in Chrome pages, a Stop hook that sends `turn_ended`, many Chrome
profiles, Arc and Chrome at the same time, Freeform drag, AppleScript JS
inside Arc, and `claude setup-token` over SSH.
