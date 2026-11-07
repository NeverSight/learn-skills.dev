---
name: studio-init
description: "Scaffold a motion-studio film project (seek(t) renderer, springs, beat grid, synthesized sound, critique tools), install it, set up the browser, run doctor. Use for 'set up the motion studio', 'new film project', 'init studio'."
argument-hint: "[dir] [--title T] [--duration S] [--formats 9x16,1x1,16x9] [--loop]"
allowed-tools: Bash(node "${CLAUDE_SKILL_DIR}/scripts/init.mjs" *)
effort: medium
---

# Studio init (course step 02)

Create a film project that can render, listen to and look at its own frames. The chat app can
write an animation; only an agent with a shell can close the render, look, fix loop. That loop is
the difference between a "mid" first try and a film worth posting.

Request arguments (may be empty), shown once:

<request>
$ARGUMENTS
</request>

## 1. Choose the directory and settings

- Directory: the first argument; else `.` when the working directory is empty; else ask (default
  `./<slug-of-title>`). Never scaffold into the plugin directory.
- Settings from the request: title, duration, formats, fps, bpm, loop, brand URL. Leave the rest
  at the template defaults (`studio.json`: 12 s, 60 fps, 4 subframes, 120 BPM, `9x16` primary).

## 2. Scaffold

```
node "${CLAUDE_SKILL_DIR}/scripts/init.mjs" <dir> --title "<Title>" [--duration S] [--fps N] [--bpm N] [--formats a,b] [--loop] [--brand-url URL] [--install] [--json]
```

| Flag | Effect |
|---|---|
| `<dir>` | target; created if missing |
| `--title T` | `studio.json` title and delivery file slug |
| `--duration S`, `--fps N`, `--bpm N` | timing |
| `--formats a,b` | subset of `9x16`, `1x1`, `16x9`, `4x5` (or `all`); `primaryFormat` stays unless it is not listed |
| `--loop` | seamless loop film (UI morphs) |
| `--brand-url URL` | stores the product URL in `brand.url`. `user:password@` and secret-looking parameters (query, `;matrix`, fragment: token, key, secret, password, auth, sig, session, code ...) are removed before anything is written; stderr names what was removed and `--json` lists it in `redacted`. Still pass a plain public URL: a secret that is a bare path segment (`/reset/<token>`) cannot be recognized. A plain URL is stored exactly as typed |
| `--install` | runs `npm install` in the new project (handles `npm.cmd` on Windows) |
| `--force` | refresh an older project to the current template (see the table below) |
| `--json` | one JSON result line on stdout |

An existing non-empty directory is merged: only missing files are added and skipped files are
listed. Report the skipped list to the user; never delete their files.

`--force` on an existing project (checked against `init.mjs`):

| Path | With `--force` |
|---|---|
| `studio.json`, `film/**`, `docs/**`, `assets/fonts/fonts.json` | kept and listed as `kept`; a missing one is still created. Flags such as `--bpm` still patch `studio.json` |
| `package.json` | merged, never replaced: sets `type: module`, adds `private`, `engines` and every template script or dependency the project lacks. A template script whose command differs is reset to the template command (init prints each as `was ..., now ...` and returns them in `packageReset`). Dependency versions are never changed, template dependencies included: an existing range stays, newer, older or pinned. Name, version, other scripts and other fields stay |
| `.gitignore` | merged: missing template lines are appended under `# motion-studio`, nothing is removed |
| everything else (`CLAUDE.md`, `lib/**`, `tools/**`, `prompts/**`, `index.html`, `.env.example`, bundled fonts) | overwritten and listed as `overwritten`. Local edits to these files are lost: commit or copy them first |
| your own extra files | untouched |

Without `--force`, `package.json` and `.gitignore` are merged the same way, except that a differing
script keeps your command. Init lists every script and dependency version that differs from the template under
`kept your package.json values, which differ from the template` (`packageKept` in the `--json` result): those `npm run`
names run YOUR command, and `--force` resets template scripts (never dependency versions). A `scripts`,
`devDependencies` or `optionalDependencies` section that is not an object is left untouched with a warning. Because `docs/**` is kept, a newer template doc never reaches an existing
project: compare with the plugin's `template/docs/` by hand after an update.

## 3. Install, browser, doctor

1. Without `--install`, run `npm install` inside the project. `playwright` is the only required
   dependency; `ffmpeg-static` is optional and may fail to download behind a proxy.
2. Browser (`npm run setup:browser` is the same command as the `npx` line):
   - Windows: run `npx playwright install chromium-headless-shell` (about 115 MB download, 270 MB on disk).
     `studio.json` `browser: "auto"` starts only that bundled headless shell, never the installed Chrome or Edge.
     Reason: an installed Chrome or Edge started with a fresh profile (every tool run) makes Chrome test the Windows
     account for a blank password, which counts as a failed logon. The measured laptop locks the account after 10
     failed logons in 10 minutes and logged 464 in 24 h. Do not switch `browser` to `chrome` or `msedge`, and do not
     set `MOTION_CHROME_PATH` to a `chrome.exe` or `msedge.exe`, unless the user asks for it and accepts the risk: it
     prints a warning per launch and the 4th launch in 10 minutes is refused, 3 pass (the launch guard).
     The shell is unsigned, so a real-time antivirus can make every tool run 15 to 25 s slower (measured): tell the user
     once; an antivirus exclusion for `%LOCALAPPDATA%\ms-playwright` is their or IT's decision.
   - macOS and Linux: `auto` tries the installed Chrome, then Edge, then the bundled browser, with no warning. If none
     is installed, run `npx playwright install chromium-headless-shell` (Linux: `npx playwright install --with-deps
     chromium-headless-shell`), or set `MOTION_CHROME_PATH` to a Chromium-family executable.
3. `npm run doctor`. Fix every FAIL row before handing over, and on Windows a WARN browser row too (an installed
   Chrome or Edge was chosen: clear it and install the headless shell); fixes per OS are in
   [references/troubleshooting.md](references/troubleshooting.md). Python with librosa is optional
   (the JS beat engine covers it). Node 22+ is needed only for route B tools.
4. Prove it: `npm run stills`, then open `out/review/9x16/contact.png` (a long film is paged: `contact.png` is page 1, then `contact-2.png` ..., no page taller than 1800 px; open every page) and look at it. The shipped
   12 s demo must show a composed frame at 0 s and a change on every downbeat. `npm run preview`
   opens the live preview (Space play/pause, arrows step frames, F cycles formats, G safe-area
   guides).

## 4. Explain the project to the user

Summarize in a few lines, then point to the references:

- Layout and who edits what: [references/project-layout.md](references/project-layout.md)
- Every command: [references/commands.md](references/commands.md)
- Every `lib/` signature and default: `docs/API.md` in the new project (the full reference is `docs/ARCHITECTURE.md` in the
  plugin repository)
- House rules live in the project's `CLAUDE.md`, which Claude Code reads on every run there.

If init printed a `★` star line (`starHint` in the `--json` result; it appears once per machine, on the first new project),
end your summary with that one line as written. Never star the repository or run `gh` for the user.

| Command | Does |
|---|---|
| `npm run preview` | live preview in the browser |
| `npm run stills` | one still per beat as a contact sheet |
| `npm run critique` | contact, strip, phone test, metrics, review-log block |
| `npm run gate` | critique gate: 3 rounds, all axes >= 8, no P0 |
| `npm run render:final` | every format, final quality (gate enforced) |
| `npm run sfx` / `npm run mix` | synthesize cue SFX / mix to -14 LUFS and mux |
| `npm run deliver` | delivery checks and `out/deliver/` package |
| `npm run build` | score if missing, sfx, final render, mix, deliver |

## 5. Effort and routes

| Work | Effort | Set with |
|---|---|---|
| small fixes, re-renders | medium | `/effort medium` |
| a new film | xhigh | `/effort xhigh` (the `motion-reel` skill sets it for you) |
| flagship first 3 seconds of a launch | max | `/effort max` |

`/model` also offers the effort choice when picking Opus 5.5. Route A (this engine) is the default.
Use Remotion or HyperFrames only when the user names one; `/motion-studio:seek-engine` has the
handoff, including the Remotion license gate.

## 6. Keys

Copy `.env.example` to `.env` only when a key is needed (voice: `ELEVENLABS_API_KEY`; route C
images/video: `FAL_KEY`). Tell the user to paste the value into `.env` themselves. In prompts and
logs refer to the variable name only. `.env` is already in the project `.gitignore`.

## 7. Optional companions

Mention these only when relevant. Install commands and caveats:
[references/companions.md](references/companions.md).

| Companion | Use for | Note |
|---|---|---|
| claude-animation (buildwithhanif) | hand-drawn, brush, storybook looks | MIT; separate Node canvas renderer |
| HyperFrames (heygen-com) | HTML + GSAP compositions | Apache-2.0; Node 22+ |
| Remotion | React series and templates | company license for for-profit orgs over 3 employees |

Next: test the engine with `/motion-studio:showreel`, or make a real film with
`/motion-studio:motion-reel`.
