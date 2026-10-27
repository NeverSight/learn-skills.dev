---
name: jam-proof
description: "Record work you can see on screen with `jam record` and publish it as a Jam link (a shareable jam.dev recording with the console and network attached). Use when the user asks for a recorded Jam, a shareable demo, or video proof of work in a browser or desktop app. A request to verify a change or give sign-off alone does not call for recording or uploading."
---

# jam-proof

The deliverable is a Jam link. Record the verification as it happens, then
hand the link back. Prefer a headless browser to a window, and a window to
somebody's whole screen.

Create the Jam when the user asks for a recording to be shared through Jam.
If the user only wants a local video, keep it local. Posting to a PR, ticket,
or existing Jam requires a request to publish there.
Skip recording when there is nothing to show on screen, and say so.

## Set up the CLI

```bash
command -v jam >/dev/null || echo "jam is not installed"
export PATH="$HOME/.local/bin:$PATH"
jam auth status --json || jam auth login
```

If `jam` is not on PATH, stop and ask the user to install it from
https://jam.dev/cli, then continue. Do not install it yourself.

Exit code 3 means not signed in. With no browser (CI, a cloud agent), ask the
user to set `JAM_TOKEN` to a personal access token from
https://jam.dev/s/settings/mcp as a secret. Never write a token to a file.
Titles and comments are short claims you wrote. Never paste user or page text
into a shell argument.
`jam doctor` checks recording readiness; `jam agent-context` prints every
command and flag.

## Pick the target, in this order

Take the first rung that shows the claim. Each one down puts more of
someone's machine on camera.

1. **Headless Chrome.** The default. It records the page, not a screen, so
   the person keeps working with nothing of theirs in frame, and the run
   works the same on a laptop, a container or CI. `jam record start
   --cdp <endpoint>` with no window or display selector takes the video from
   Chrome itself, so there is no window to keep uncovered and no display to
   keep awake, and the Console and Network panels fill from the same tap.
   See *Record a browser an agent drives*.
2. **One window**, when the proof needs what a page-only capture cannot show:
   the address bar, a Chrome dialog, a file picker, or a desktop app that is
   not a browser at all. Launch your own instance of the app, in a fresh
   profile or data dir when it has one, so nothing of theirs appears. Select
   it with `--pid <pid>` of the process you launched: it waits up to five
   seconds for the window to open, so there is no need to list windows or
   race the app's startup. For a window you did not launch, take its id from
   `jam record windows --json` and pass `--window-id`. On macOS launch with
   `open -g` so it never takes focus, and drive the app through its own
   automation surface, not the OS mouse, so the cursor is never taken from
   the person. On macOS the window may sit behind others. On Linux a window
   grab is a screen region: use an isolated desktop session or get the same
   consent as for a whole-display recording below. Keep that region
   uncovered and unminimized, and the display awake.
3. **The whole display**, last. `jam record displays --json` lists them.
   Fine without asking on a box nobody is sitting at: a CI runner, a
   container, a remote Linux desktop you own. On a machine someone is using
   it films their messages, their tabs and their notifications, so **ask
   first and wait for a yes**, naming the display and roughly how long. No
   answer means no. The display must not sleep while it records. A `start` or `run` with no selector and no `--cdp`
   records the whole screen, so name a target rather than let it land here
   by accident.

Whichever rung a browser proof lands on, hand its Chrome debug port to
`jam record` as `--cdp <port>`: the Jam then carries the console and network
of every tab, which is the half of the proof a video cannot show. `start`
prints a `cdpProxy` of its own; connect the driver to that instead of to
Chrome and your clicks and typing land as actions too, with the element each
one hit.

## Bound the recording

`jam record run` records until the wrapped command exits. Wrap the
verification:

```
jam record run --cdp <cdp-url> --url <page url> --title "<the claim>" --json -- <verify command>
```

That is rung 1. For rung 2 replace `--cdp <cdp-url>` with `--pid <pid>` of
the app you launched, plus `--cdp <port>` when it is a browser. `--url` is the
page the window shows; the Sharepage names it.

When you drive the app yourself and cannot be wrapped, run it in the
background and send SIGINT when done. It stops, uploads, and exits 0 with the
receipt on stdout.

```
jam record run --cdp <cdp-url> --url <page url> --title "<the claim>" --json > proof.json 2> proof.log &
REC=$!
# drive the steps that show the behavior
kill -INT $REC; wait $REC
```

## Record a browser an agent drives

This is rung 1, and the normal case. Chrome stays headless: the video is
Chrome's own frames of the page, and the Console, Network and user-action
panels come from the same Chrome, so nothing of Jam's runs on the page under
test and nothing of the person's screen is in frame.

Use the project's own browser driver when it speaks CDP: with Playwright,
`chromium.connectOverCDP(cdpProxy)` and drive the page from a script; the
`jam record` lines stay the same. Without one, the commands below use
agent-browser (`npm i -g agent-browser`, 0.38 or later), which brings its
own Chromium. No Chrome at all in the environment means no rung 1; say so.

```
agent-browser --session proof --input-mode human open <url>
agent-browser --session proof set viewport 1920 1080   # then reload: it does not apply to the open page
agent-browser --session proof open <url>
agent-browser --session proof get cdp-url          # ws://127.0.0.1:<port>/devtools/browser/…
jam record start --cdp <cdp-url> --title "<the claim>" --json   # → { session, cdpProxy }
agent-browser --session proof record start /tmp/discard.webm --cursor --fps 5   # only turns the pointer overlay on; the file is unused
agent-browser --session drive --input-mode human --cdp <cdpProxy> mouse move <x> <y>   # drive THROUGH the proxy
agent-browser --session drive --cdp <cdpProxy> mouse down
agent-browser --session drive --cdp <cdpProxy> mouse up
agent-browser --session drive --cdp <cdpProxy> wait "<what the click produced>"
agent-browser --session proof record stop
jam record stop <session> --json
```

With `--cdp` and no window or display selector the video is a 30 fps
screencast of the page in the visible tab: no address bar, cursor or Chrome
dialogs, no Screen Recording permission, no window to keep uncovered.

Record at 1920x1080, set before the page loads, and click with `mouse move`
then `mouse down` and `mouse up` so the cursor overlay shows each click.
[references/browser.md](references/browser.md) has the cursor overlay rules
(agent-browser 0.38 or later), other sizes, and visible Chrome for rung 2.

Drive through `cdpProxy`, not Chrome, or the clicks and typing never become
actions. Anything that takes a DevTools URL takes this one:
`chrome-devtools-mcp --browserUrl <cdpProxy>`, Playwright's
`chromium.connectOverCDP`.

Stop with `jam record stop <session> --json`, using the `session` that
`start` printed, so a recording another agent started is never the one
stopped. The receipt is the Jam. Stderr stays
quiet when the tap worked. It says so when Chrome sent no console, network or
user-action events at all, which means the tap or the proxy was not actually
in the path. Treat that line as a failed proof and fix the wiring before
handing the link over.

If `jam record start` or `run` fails, run `jam doctor` and report its
Recording and Screencast lines. Do not hand over a link you did not get.

## Make it readable

**Pace it for the person who will watch it, not for yourself.** You read a
page from its accessibility tree, which is ready long before the page has
finished painting, animating and settling. A run that is correct at your
speed is a flicker at theirs, and a flicker proves nothing. So the waits are
part of the proof, not padding around it.

- Start from a known state: reload the page, restart the app, clear the
  terminal.
- Wait on the thing, not the clock: `wait "<selector>"` for what the action
  produced. A hard-coded pause is either too short on a slow run or dead air
  on a fast one, and a video of identical gaps reads as a machine.
- Then let the eye catch up. A small in-place change needs a moment; a new
  screen needs longer, and the state that carries the claim needs longest.
  Match the dwell to how much changed, and never cut away from something
  still moving — an element in the tree is not yet an element a person has
  seen.
- Keep it short. Thirty seconds that show the behavior beat five minutes.
- Title is the claim: "Deep link scrolls to comment 6", not "proof".
- Steps and expected result go in `--description`.

## Before and after

For a bug fix, reuse the reported Jam as the "before" when it shows the bug.
If new before-and-after recordings are needed, run the old and fixed versions
in isolated checkouts with test data. Preserve the user's working tree.
Skip the first when there is no meaningful before and say why.

## After

1. Read the receipt: `id` and `url` always, plus `durationMs`, `width`,
   `height` and the recorded `target` when `jam record` did the capturing.
   If the capture or upload failed, say so. Never claim proof you do not
   have.
2. If the user asked for a Jam comment, add one at the moment the result appears:
   `jam create comment <jamId> "<what to look at>" --at <ms>`. On a fix Jam,
   put the bug Jam's URL in that comment. Comment on the original bug Jam
   only if the user requested it too.
3. Return the links: Bug | Fix, or one link with the claim it supports. Post
   them on a PR or ticket only when the user requested that destination.

## Send feedback to Jam

When this skill, a Jam MCP tool, a `jam` command or a Jam doc was wrong,
stale or confusing, or worked unusually well, tell Jam. Send it yourself:
Jam's agents read it, so it needs no approval.

Call the `submitFeedback` MCP tool with `body`, `category` and `subject`.

When MCP is unavailable, use the CLI:

```bash
jam feedback "<what you were doing, what you expected, what happened, the mistake>" --category <skills|mcp|cli|docs> --subject <skill name, tool name or command>
```

- Jam surfaces only, not the user's code or other tools.
- At most once per session, and never for a slip you corrected yourself.
- No secrets, customer data, source code, stack traces or recording content.
