---
name: takeone
description: Record polished Screen Studio style videos of web apps (smooth cursor, click ripples, eased zooms, padded frame) with the takeone MCP server, CLI or TypeScript SDK, including installing and setting it up from nothing. Use this whenever the user wants a demo video, product walkthrough, feature clip, tutorial recording, launch video or screen recording of a website or web app, even if they don't name takeone, and whenever a project has takeone scenario files or a .takeone folder.
---

# takeone

takeone records web apps headlessly. You rehearse the video in a live browser, the rehearsal becomes a scenario file, and the scenario is replayed on its own clock to record. Your thinking time never shows in the video, and the cursor, zoom and frame are applied afterwards, so a take can be restyled without recording again.

The workflow has five stages, in this order:

1. **Rehearse.** Click through the app live. Every step shows you the page.
2. **Mark** where the video starts.
3. **Export.** takeone replays the path to prove it works, then writes the scenario.
4. **Dry run.** Runs at recording pace and returns a contact sheet (one image with a frame per step).
5. **Record.** Captures and renders the video.

## Install and set up

Do this once per project, before the first recording. Each step is safe to repeat.

1. **Check whether it is already installed.** If `package.json` (in the project or a `videos/` folder) lists `takeone`, skip to step 4.
2. **Check Node.** `node -v` must be 20 or newer. If Node is missing or older, tell the user and stop: nothing else works without it.
3. **Install the package where the scenarios will live.** Exported scenarios run `import … from "takeone"`, so the package has to be installed next to them.
   - **A JavaScript or TypeScript project** (it has a `package.json`): add takeone as a dev dependency with the project's own package manager, which the lockfile tells you: `npm i -D takeone`, `pnpm add -D takeone`, `yarn add -D takeone` or `bun add -d takeone`.
   - **Anything else, or when the app's dependencies should stay untouched:** give the videos their own folder.
     ```bash
     mkdir -p videos && cd videos && npm init -y && npm pkg set type=module && npm i -D takeone
     ```
     Run every takeone command from that folder. Scenario files, the `.takeone/` state folder and `recordings/` all stay in it.

   The CLI comes with the package: run it as `npx takeone <command>`. `npx takeone guide` prints the whole workflow on one screen. A global install (`npm i -g takeone`) gives a bare `takeone` command, but scenarios still need the local install.
4. **Prepare the machine.** Run `npx takeone setup`. It:
   - downloads Chromium (about 650 MB, once per machine)
   - checks ffmpeg, which ships with the package
   - starts a headless browser to prove recording will work

   It ends with `Ready.` or with `✗` lines that say what is wrong. On a Linux server, missing system libraries are the usual failure. Fix them with `npx takeone setup --with-deps`, which needs sudo. If you can't use sudo, give the user that command to run.
5. **Register the MCP server (optional, recommended).** Its replies carry the screenshot, so one call both acts and shows the page. Register it for the agent you are running in:
   ```bash
   claude mcp add takeone -- npx -y takeone mcp     # Claude Code
   codex mcp add takeone -- npx -y takeone mcp      # Codex
   ```
   Other clients take `{"command": "npx", "args": ["-y", "takeone", "mcp"]}` in their MCP config.

   MCP servers load when a session starts, so the tools only appear in the next session. Don't wait for them: use the CLI for the rest of this session, and tell the user that restarting gives them the MCP tools. The MCP server and the CLI share one browser session, so switching between them loses nothing.

To update later, run `npm i -D takeone@latest`, then `npx takeone session stop` so the running browser session picks up the new version.

## The commands

| Step | MCP tool | CLI |
|---|---|---|
| Start, optionally with login | `takeone_start {scenario, url, headed, viewport}` | first command with `--scenario login.ts` |
| Act | `takeone_do {verb, target, text}` | `npx takeone do <verb> <target> [text]` |
| Look at the page | `takeone_look {filter, role, all}` | `npx takeone look` |
| Mark | `takeone_mark {name: "start"}` | `npx takeone mark start` |
| Journal | `takeone_journal {action, ids}` | `npx takeone journal [drop\|keep\|setup] 3-5` |
| Export | `takeone_export {file}` | `npx takeone session export demo.ts` |
| Dry run | `takeone_dry_run {file}` | `npx takeone dry-run demo.ts` |
| Record | `takeone_record {file}` | `npx takeone record demo.ts` |
| Stop the browser | `takeone_stop` | `npx takeone session stop` |

Verbs: `goto`, `click`, `type`, `press`, `hover`, `scroll`, `scroll-to`, `wait-for`, `wait-url`, `wait`, `zoom`, `zoom-out`.

## Plan the video before opening the browser

Write down the story in three to six beats before the first `goto`, for example "open Projects, create a project, show it in the list, zoom on its status". Each beat should be something the viewer sees change. Then rehearse only those beats. A plan keeps the rehearsal short, because you know which clicks belong in the video and which are only looking around.

- **Start from a settled page.** The recording should open on a page that is already loaded, not on a spinner. Put navigation and preparation before `mark start`, or after `mark setup` for anything the viewer shouldn't see.
- **Prepare data before recording.** If the video needs existing items, create them in setup steps or through the app's API before rehearsing. Creating them on camera is only right when creating them is the point of the video.
- **Aim for short.** 20 to 60 seconds per video. Two short videos are easier to get right, and easier to watch, than one long one.

## Rehearsing: read the view, act by number

The first `goto` launches Chrome. Every step that reaches a new page or opens a dialog returns the **view**. The view lists every element on screen with a number, grouped by region, and says what the page's markup says each element does:

```
header
  1 link "Acme" [icon logo] → /
sidebar "Workspace"
  4 link "Projects" [current] → /projects
main
  12 button "New project"
  13 button [icon ellipsis] (opens menu)
  14 switch "Email alerts" [off]
off screen: 22 more elements. Headings: 30 "Members", 41 "Billing"
```

A screenshot comes with the view, with the same numbers drawn on it. MCP attaches the image; the CLI prints its path. Read the text first. Open the screenshot when the text can't answer the question: layout, icons, charts, or whether something looks right on camera. Then act by number: `click 12`, `type 5 "acme-prod"`, `zoom 14`. Numbers refer to the most recent view.

Other steps print only what changed:

- `+` new elements, with their numbers
- `-` removed elements
- `~` state changes
- alerts, dialogs, and page errors (`!`)

This diff is usually all you need to decide the next step, so don't call `look` after every action.

Targets can also be plain words (`"new project"`), `role:name` (`button:Create`), `text=Deployed`, `css=.monaco-editor`, or a point `640,360`. For a control whose name is a number, use `button:2`.

Every line in the view is read from markup. takeone never clicks anything to find out what it does. That is deliberate: a Delete or Create button tried in the background would really run.

## Which command when

| Situation | Use | Not |
|---|---|---|
| Arriving on a page or opening a dialog | the view that `do` already printed | an extra `look` |
| After a click, typing or a key press | the change report (`+`, `-`, `~`) | `look`, unless the report says the page kept changing |
| Something you can't see in the text: an icon, a layout, a chart, whether it looks right on camera | the screenshot (inline over MCP; the `view:` path with the CLI) | guessing from names |
| Finding something off screen or on a long page | `look --filter <text>`, then `scroll-to <n>` | scrolling blindly and looking again |
| Acting on something in the latest view | its number (`click 12`) | retyping its name |
| The page changed since the view you are reading, or you know the label | plain words (`click "new project"`) | a number from an older view |
| Several controls share a name | its number, or `role:name` with `--nth`. The export addresses it by the text next to it when it can | a CSS selector |
| Waiting for the app: a save, a deploy, provisioning | `wait-for "<text that appears>"` with a `--timeout` long enough for it | `wait <ms>`, which guesses |
| Giving the viewer a beat to read | `wait 800` to `wait 1500` | nothing: steps back to back feel rushed |
| Showing a result up close | `zoom <n>`, then `zoom-out` | zooming on every click, since automatic zoom already follows clicks |
| Checking the path before export | `journal` | exporting and hoping |
| Checking the whole video before recording | `dry-run`, then read the contact sheet | `record` first: a failed take costs minutes |
| A quick path check while editing the scenario | `dry-run --fast` | treating a fast pass as proof the recording will pass |
| Changing only the look (background, cursor, size) | `render <recording-dir>` with other config | recording again |
| Finished, or after updating takeone | `session stop` | leaving the browser running |

`explore` and `find` are older commands for inventorying pages by URL. The view and `look --filter` cover the same ground with less work.

## Rehearse well

- **Rehearse the exact path the video takes, in order.** Detours are dropped automatically, but every extra step is one more thing to review in the journal.
- **Call `mark start` as soon as the page is where the video begins.** Everything before it stays out of the video, so it's safe to look around first.
- **Type what the viewer should read.** Use realistic names and values ("acme-prod", not "test123"). They end up on screen.
- **When a step fails, read the error before retrying.** It says what the page showed: a login page means the session isn't authenticated; "not found" means the URL or an ID is wrong. Retrying the same step rarely helps.
- **Re-rehearse when the path changes, and edit the file when only timing changes.** Waits, typing speed, zoom scale and extra beats are one-line edits in the exported scenario. A different click order needs a new rehearsal and a new export.
- **Review before you call it done.** Check the dry-run contact sheet and the keyframe sheet that `record` writes: did every beat land, is anything cut off, are there loading states on camera?

## From rehearsal to video

1. **Click around freely before the video starts.** Steps that return the page to an earlier state are dropped from the export as detours. An example is opening a menu and then closing it.
2. **Call `mark start` where the video should begin.** Everything before it counts as looking around. If the app needs preparation that shouldn't be filmed, call `mark setup` before `mark start`. Examples: open a project, or clear a form.
3. **Check the journal before exporting.** The `journal` tool shows where each step landed. Use `keep` to rescue a step that was wrongly dropped, and `drop` to remove one.
4. **Export.** It replays the kept steps in a fresh tab first. If the replay fails, the error names the step and shows what the page said.
   - The exported file uses role and name addresses, never view numbers.
   - Names that include a live count or badge are written as patterns. For example, `"Issues 157"` becomes `/^Issues(?![\w.])/`.
   - Exporting into an existing file replaces only the block between `// takeone:steps-begin` and `// takeone:steps-end`, so your edits outside it are kept.
5. **Dry run before recording.** It paces the page exactly as the recording will, so a dry run that passes means a recording that passes. Look at the contact sheet: it is the cheapest review of the whole video.
6. **Record.** The result is `recordings/<name>-<time>/output.mp4`, plus a keyframe sheet for checking the take.

The exported file is ordinary TypeScript. Edit its timing (`s.wait`), typing speed and zooms by hand when that is faster than rehearsing again. `references/scenario-api.md` lists every method and option.

## Logged-in apps

Put the login in a scenario's `explore.setup`, then start the session with that file. The session logs in once and every later step reuses it. The exported scenario imports that file and runs the same login before recording.

```ts
import { defineScenario, withExplore } from "takeone";

export default withExplore(defineScenario({ name: "login" }, async () => {}), {
  pages: [],
  setup: async (page) => {
    await page.goto("http://localhost:3000/login");
    await page.fill('input[name="email"]', process.env.DEMO_EMAIL!);
    await page.fill('input[name="password"]', process.env.DEMO_PASSWORD!);
    await page.click('button[type="submit"]');
    await page.waitForURL(/dashboard/);
    // App state the video needs: a theme stored by the app itself, hidden banners, and so on.
    await page.evaluate(() => localStorage.setItem("theme", "dark"));
  },
});
```

Read credentials from environment variables. Never write them into the file.

`browser.colorScheme: "dark"` only sets the browser's dark-mode preference, which the page sees through `prefers-color-scheme`. If the app keeps its own theme setting, set it in the setup, as above.

## Making it look good

- **Zoom for the viewer, not for every click.** Automatic zoom already follows clicks and typing, and `zoom.auto` controls it. Add an explicit `zoom` when the viewer needs to read something: a result, a status, a value that changed. Hold it for about 1.5 s, then `zoom-out` before the cursor travels far. Two to four deliberate zooms per minute reads better than constant motion. To turn automatic zoom off for a section, call `s.autoZoom(false)`.
- **Show slow steps honestly.** A wait plays in real time by default. `s.lapse(8, () => …)` shows a long wait as a time-lapse; `s.trim(() => …)` cuts it down.
- **Capture crisp.** The default is a 1920x1080 viewport at `deviceScaleFactor: 2`, which keeps zooms sharp. Output size is set separately (`output.width`, `output.height`, `output.fps`); for 4K output, capture at `deviceScaleFactor: 3`. Restyle an existing take without recording again: `takeone render <recording-dir>` with other `frame`, `cursor` or `output` settings.
- **Prefer short takes.** Several short scenarios are easier to get right than one long one. `record --no-render` followed by `render` separates capturing from styling.

## Things that cost time if you don't know them

- **Rehearsals and dry runs change real data.** Creating a user, a project or a file really creates it. Use unique names, or reset the app between takes, so a later run doesn't fail on "name already taken".
- **Some text fields are invisible to the page listing.** Code editors (Monaco) and terminals (xterm) take their input through a hidden text box. Click the editor, then type with no target (`type` with only the text), which types into whatever has focus.
- **Key sequences are fast in the recording.** In a rehearsal, two separate `press` calls can miss a shortcut's timing window, for example `g` then `i`. The exported scenario runs them back to back, so check with a dry run before assuming the app is broken.
- **Page problems appear as `!` lines.** A 401 or a crash is shown as `! HTTP 401 …` in the step output. A "login page" or "not found" in an error means the URL or the authentication is wrong, not the element name.
- **Nothing hangs.** Every command gives up with an error instead of waiting forever, so don't wrap commands in long timeouts. Named targets wait up to `browser.timeout` (15 s) for the element to appear.
- **Two agents on one machine need separate sessions.** Set `TAKEONE_SESSION_PORT=9322` for the second one; it gets its own browser.
- **An updated takeone doesn't reach a running session.** A session started before an update keeps running the old code. The CLI warns about this. Run `takeone session stop` to restart it.

## SDK

Scenarios are TypeScript modules, and the runner can be used from code:

```ts
import { recordScenario, renderRecording, dryRunScenario } from "takeone";
import scenario from "./demo.js";

const rec = await recordScenario(scenario, { outDir: "out/demo" });
await renderRecording({ recordingDir: rec.outDir, config: { frame: { background: "#0b0b0f" } } });
```

See `references/scenario-api.md` for the session methods, targets and every config option.
