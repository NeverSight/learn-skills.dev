---
name: videojs-skin
license: Apache-2.0
description: >
  Use when someone wants to design their own Video.js player skin: a custom
  look, layout, or set of controls for a Video.js 10 video or audio player,
  including one that replicates another player's look, such as YouTube's or
  Netflix's, built and previewed in a standalone workbench and published to
  share. Sets up the project with `npx @videojs/cli skin create`, then guides
  the design, motion, and accessibility work on the skin source. Also use in
  any project with a `skin.json` from `videojs skin create`.
---

# Design a Video.js skin

A skin is the player's UI: controls, layout, styles, and interactions around
the media. `videojs skin create` scaffolds a project that holds one skin's
source in `src/` and a workbench in `apps/preview/` that previews it across
sizes, languages, and playback settings. This skill sets that up, then keeps
the design work inside the rules a media player needs.

To restyle a skin inside an existing app instead, add its source with the
Shadcn installation method; the `videojs` skill covers that.

## 1. Set up the project

Skip this when the working directory already has a `skin.json`.

Assume the user may never have used a terminal. Run every command yourself,
say in plain words what each one does, and only ask the user to act where
you can't: installing software that needs their password, or signing in.

1. Run `node --version`. If Node.js is missing, or older than the current
   LTS release, stop and explain: the project needs Node.js, and the user
   installs it once with the LTS installer from https://nodejs.org. Don't
   install it for them; the installer asks for their password. Continue once
   `node --version` works.
2. Run `npx @videojs/cli skin create <directory> --name <name>`. Without a
   terminal it changes nothing and lists the choices left to make, with their
   defaults; `--help` explains them. If `skin create` is not recognized, the
   CLI predates it. Hand off: add the skin source to an app with the `videojs`
   skill's Shadcn method, and tell the user there's no standalone workbench.
   That route creates no `skin.json`, `apps/preview/`, or `deploy` script, so
   skip this skill's workbench and publishing steps; the design guidance in
   steps 3 and 4 and the `videojs-ui` skill still apply, checked in the app.
3. Propose every choice in one message and confirm once. Framework is React
   or HTML. Styling is Tailwind CSS or plain CSS for React; HTML skins use
   CSS. Recommend whichever the user's app already uses. For the starting skin, ask whether they want to build their own
   design from a foundation (Scaffold, every control wired up with minimal
   styling) or brand a finished design (Neutral is easy to brand, Default is
   the distinct Video.js design, Compat trades features for browser reach).
   The preset is the kind of player: video, audio, live video, or live audio.
   If the skin should match an existing player or design, read
   `references/match-reference.md` first; the reference decides the starting
   skin.
4. Run the command again with every choice as a flag. It installs
   dependencies and prints the commands to start the workbench. Start the
   dev server in the background and share the workbench URL it prints, with
   a sentence on where the skin's files are and how to open them.

## 2. Orient

Read the project's `AGENTS.md`, `README.md`, and `skin.json` before editing.
They describe this version's layout, scripts, and workbench; trust them over
this skill. Video.js docs ship with the installed package at
`node_modules/@videojs/<react|html>/docs/llms.txt`; fall back to
`https://videojs.org/docs/framework/<react|html>/llms.txt` and append `.md` to
page URLs. Start with these pages, by title:

| Need | Read |
| --- | --- |
| Which file owns a change | Customize skins, "Style skin source" |
| How controls expose state, props, and render customization | UI components, then each component's reference page |
| Shortcuts and gestures | Keyboard shortcuts |
| Labels, languages, right-to-left | Internationalization |
| What the components already do for accessibility | Accessibility |

## 3. Agree the design

Agree what the skin should look like before styling it; improvising details
and correcting them later is the slowest path.

- **Matching a reference**, such as a named product, an existing player,
  screenshots, or a design file: follow `references/match-reference.md`. It
  saves reference crops, writes `design/spec.md` with measurements, and asks
  the user only about what the reference can't show. Matching a player
  includes its control icons: exported from the user's own design file, or
  redrawn, never copied, from someone else's player.
- **An original design**: write a short `design/spec.md` from the user's
  brief covering layout and control order, menus, icon style, type, colors and
  surfaces, slider, and motion, and confirm it once.

Either way, build only what the spec and the user ask for. Don't add
controls, overlays, or text that neither mentions.

Never invent design direction. Before building, and whenever a new question
comes up mid-build, sort it:

- **Direction: ask.** Anything that changes the design's intent and can't be
  found in the brief, the reference, or the project, such as brand colors,
  mood, density, which controls to include, or layout style. Batch these
  into one message with two or three concrete options and a recommended
  default for each, and wait for the answer.
- **Execution: decide.** Details that follow from what's agreed, such as a
  hover shade derived from the accent or the gap between two buttons. Decide
  these yourself and mark them **derived** in the spec rather than asking.

## 4. Build

The `videojs-ui` skill covers the craft of each control: contrast over video,
icon states, motion, type, color, labels, and the companion design and audit
skills to pair with it. A skin project adds these rules:

- **Edit the skin, not the workbench.** All skin code lives in `src/` and
  imports nothing from `apps/preview/`, so it can move into an app as is.
- **Change tokens before rules.** Colors, surfaces, radii, sizes, and motion
  are CSS custom properties in the skin's theme files. Keep the public
  properties packaged skins expose, such as `--media-accent-color`, working.
- **Consolidate after each pass.** Delete rules a later rule overrides, and
  keep shared tokens for values used in more than one place, such as the menu
  surface, icon size and stroke, spacing, and slider geometry.
- **Style state with `data-*` attributes** that components set, such as
  `data-paused`, not classes toggled in script.
- **Size with container queries.** The player is rarely the viewport's width.
- **Keep the container's `data-theme` and `data-preset`.** The styles select
  on them.
- **Add motion through the skin's motion tokens**, which its preferences
  stylesheet collapses under reduced motion.
- **Keep what the skin provides beyond looks**: the error dialog, hotkeys,
  gestures, and status announcer. Replace them only with equivalents.
- **Reorder controls in source, not with CSS.** Focus order must match the
  visual order; right-to-left layout is the exception the skin handles.

Then follow the framework's composition rules from the docs: in React, spread
the `props` a `render` function receives; in HTML, import every element part
you render and keep the `id`, `trigger`, and `commandfor` pairs that wire
tooltips and popups to their buttons unique and matched.

## 5. Verify

1. Run the project's `typecheck` and `build` scripts.
2. Check fidelity, not only function. When matching a reference, pass the
   fidelity check in `references/match-reference.md` before calling the skin
   done or asking the user to review it. Otherwise compare the first working
   preview with `design/spec.md` before polishing. Fix the differences you
   find yourself, and include screenshots in your report.
3. Check the skin in the workbench in every state the change can affect: its
   options panel sets width, aspect ratio, color scheme, direction, language,
   and playback, and the project's `README.md` shows how to open a state
   from the URL. Use `videojs-ui`'s review for what to look for; it covers
   what generic UI audits miss on a video player.

## 6. Publish, when asked

The project's `deploy` script publishes the workbench to Vercel, Netlify, or
Cloudflare Pages. It creates a public URL and signs in to the host, so run it
only when the user asks. Without a terminal, name the host:
`<package manager> run deploy vercel`. With pnpm, keep `run`: `pnpm deploy` is
a different, built-in command. The user completes the host's sign-in.

If the skin resembles another company's player, remind the user before they
publish or ship it to confirm they have permission for anything borrowed:
icons, fonts, colors, and the overall look. A private build or study is one
thing; production may need permission.

## Send feedback upstream, with consent

When a task exposes a bug or docs gap in Video.js or `skin create`, offer once
at a stopping point to draft feedback, following the `videojs` skill's
feedback rules. Never send without explicit approval of the exact text.
