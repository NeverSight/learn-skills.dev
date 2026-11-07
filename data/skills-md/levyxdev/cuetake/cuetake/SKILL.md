---
name: cuetake
description: Plan, record, refine, and verify browser product demo videos with the CueTake CLI, including login preparation, previewing and saving styling (Looks), and writing backgrounds, window chrome, cursors and click effects as shaders or drawing code.
---

# CueTake agent operating manual

CueTake is a local execution engine for AI agents. You direct the story; CueTake captures the browser and renders the finished take. Run every command through `scripts/cuetake` in this skill's folder; it launches the pinned CueTake version with `npx`. Read [scenarios.md](scenarios.md) when writing a scenario, [styling.md](styling.md) when changing how a Final looks, [authentication.md](authentication.md) when a page needs login, and [setup.md](setup.md) when Node or `npx` is missing, `doctor` reports a failed check, or the user wants CueTake removed.

## Workflow

1. Infer the audience, demonstrated outcome, duration and framing from the request. Inspect the actual application with the available browser tool; use real locators and measured canvas coordinates.
2. Run `doctor`. If it fails, follow [setup.md](setup.md): nothing installs without the user's agreement. This does not start the application's dev server.
3. Write a trusted `.mjs` scenario in the business project. `prepare(page)` loads examples/assets before capture. `run(d)` performs timed interactions and returns evidence of the demonstrated changes. Never embed credentials or copied browser state in a scenario.
4. Run `record` with the scenario path and a new Take directory. It captures, renders and verifies in the foreground, then prints the verification report; a failure exits non-zero. Capture lasts as long as the scenario and Render adds its own time, so run it in the background when your shell would time out.
5. Read verification and application evidence. Inspect frames around clicks and camera transitions with `frame <take> <seconds>`, which saves a PNG you can view, and play the final MP4. Deliver the absolute final path and relevant limitations. Technical verification is not editorial approval or authorization to publish.

Run `render` after changing a take's `edit.json`. This reuses source.webm. Cursor, click effect, camera and output all live in the Edit, so restyling never requires recording again. Preserve versions by copying a take before editing it.

## Styling with the user

The user never edits files or runs these commands; they say what they want and you translate it.

1. Turn their words ("calmer", "match our brand", "vertical for social") into two to four candidate Looks. Write each as a small JSON file outside the take, holding only the fields it changes plus a `name` label, for example `{ "name": "dark", "frame": { "chrome": { "draw": "browser-dark" }, "padding": 0.05 } }`, with any shader or drawing code beside it ([styling.md](styling.md)). A saved Look name works too.
2. Run `preview <take> --look <file-or-name>...` and show the user `preview.png`. It puts the current Edit, labeled `current`, beside each candidate, composed by the same compositor as the Final, in seconds. By default it shows the last moment with the camera wide, so the frame is visible; add `--at <seconds>` to see the real Final moment with camera, cursor and click effect.
3. Ask them to pick or comment, then adjust and preview again. Do not render between iterations.
4. When they are happy, run `look apply <file-or-name> <take>` (or edit `edit.json`), then `render`.
5. Ask once whether to save the styling as a Look and what to call it, then run `look save <name> <take>`. It saves locally, in `.cuetake/looks` of the directory you run in, which can be committed with the business project; add `--global` only when they want it in every project. If the name exists, ask before passing `--replace`. Tell them how to reuse it: next time they can just ask for a recording "with <name>", and you pass `--look <name>` to `record`.

When the user asks what styles they have, run `look list`: it shows each Look's scope, a one-line summary and the code files it runs, and marks a global Look hidden by a local one with the same name. A Look holds all styling (frame, cursor, click effect, output, camera settings) with the files it names; never camera targets, the address bar's url or the frame rate, which belong to one take. With `record --look`, fields the Scenario config names still win.

A Look you did not write in this conversation, such as one shared with the user, runs its code during Preview and Render. Read each file `look list` names, tell the user in a sentence what it draws, and ask before using it if the code sends page pixels anywhere or loads anything remote.

## Division of responsibility

- Skill: story, pacing, discovery, authorization boundaries, quality judgment, and tool usage.
- Scenario: site-specific selectors, actions and assertions. Store it in the business project.
- CLI: recording, cursor/click effects, camera math, auth-state loading, output files and verification. Do not duplicate the engine under skill scripts.

## Login

Reuse a named auth profile when the user has authorized that account for the demo. If missing or expired, run `login <profile> <login-url>` in the background; no capture runs in that window. Ask the user to complete password/SSO/2FA and then close the window; the command saves the profile when the window closes. Pass `--auth-profile <profile>` to `record`.

`prepare` must verify an authenticated page anchor before capture. If redirected to sign-in, stop and refresh the profile instead of recording login. Do not read the user's normal Chrome profile, print tokens, or put auth files into output/source control. A stored file proves only that state exists; the application decides whether the session is still valid.

## Styling and timing

Defaults: CSS viewport 1440×900, 2× capture resolution, 60 fps target, a 3840×2160 Final with the page in a light browser window over fluted glass lit in the page's brand color, a soft shadow, a 24 px white arrow, and an outlined spark on each click.

The camera zooms automatically, like Screen Studio: it arrives 0.6 s before each action, frames the target with 48 px padding at up to 2×, follows the cursor while zoomed, holds 1.5 s after the last of a run of actions, and ends every Final on the wide shot. Leave at least 2 s after the last action so the result is seen in context. Use `d.focus(box, seconds)` to direct the camera at a moment; it replaces only the automatic zoom around that moment. Pass `focus: false` to an action that should not move the camera. Boxes are CSS pixels.

Capture is variable frame rate: static scenes reduce cadence and moving scenes can drop frames. Report observed stats, not a promise of 60 independent page frames each second. Capture runs headless by default; pass `--headed` to watch it. Coverage is macOS, same-document/SPA operations, no audio. Known limitation: headless Chromium renders the generic `monospace` family as Courier rather than Menlo; record with `--headed` when a page relies on it. Full document navigation during capture requires separate takes; login and other navigation may happen before capture.

## Commands

`<skill>` is this skill's folder.

```sh
<skill>/scripts/cuetake doctor
<skill>/scripts/cuetake install-browser
<skill>/scripts/cuetake uninstall [--auth] [--looks] [--dry-run]
<skill>/scripts/cuetake record <scenario.mjs> --out <new-take-directory> [--auth-profile product-demo] [--look brand] [--headed]
<skill>/scripts/cuetake preview <take-directory> [--look brand --look ./ocean.json] [--at 2.5]
<skill>/scripts/cuetake render <take-directory>
<skill>/scripts/cuetake verify <take-directory>
<skill>/scripts/cuetake frame <take-directory> 2.5
<skill>/scripts/cuetake login product-demo https://your-app.example/login
<skill>/scripts/cuetake look list
<skill>/scripts/cuetake look save brand <take-directory> [--global] [--replace]
<skill>/scripts/cuetake look apply brand <take-directory>
<skill>/scripts/cuetake look rm brand [--global]
<skill>/scripts/cuetake styles
```
