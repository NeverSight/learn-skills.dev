---
name: framejam
description: Make and review videos and storyboards with the user in the loop, with any video tool (Hyperframes, Remotion, Motion Canvas, ffmpeg, screen recordings). Use when the user wants to make or edit a video, motion graphic or animation, wants a storyboard or shot list reviewed before animating, wants to pick a visual style, or wants to review a render and send timestamped feedback. Requires the framejam MCP server.
---

# FrameJam: style presets + one-click video and storyboard review

FrameJam runs next to your chat at http://localhost:2400. It gives you two things the chat is bad at:
**choosing a style** (a structured `style.json`, plus a working Hyperframes template) and **precise feedback**
(timestamped, pinned comments with a frame image of the render).

FrameJam works with whatever makes the video. **The user reviews the rendered video** (`videoPath`), so what they see
is exactly what you rendered. Hyperframes is the default way to build a new video.

**Words to use with the user:** FrameJam calls each review a **project** (the start page is "Projects"). Say
"I opened the project in FrameJam", not "I opened a review". Tool and field names (`open_review`, `reviewId`) stay as
they are.

## 0. Open FrameJam in the built-in browser (always do this first)

As soon as this skill is used, open FrameJam where the user can see it, without being asked:

- **Cursor:** use the built-in browser tool (`cursor-ide-browser` → `browser_navigate`) with
  `position: "side"` so it opens beside the chat.
- **Other harnesses:** use their browser/preview tool if there is one. Otherwise give the user the link.
- **Which page:** the project's `url` when step 1 finds one, `http://localhost:2400/styles` for a new video, and
  `http://localhost:2400` (Projects) until you know.
- If the page doesn't load, nothing is hosting the UI. Run `npx -y framejam start` (it starts the UI in the background,
  or reuses a running one, and prints the URL), then open that URL. Never ask the user to start it.
- If the framejam tools themselves aren't available, run `npx -y framejam install <app>` with the app you're running
  in (`cursor`, `claude` or `codex`). It adds the MCP server and the skill (or confirms them) and starts the UI. Open
  the link it prints, then tell the user the last step it prints (restarting the app once so the tools load).

## 1. Work out what the user is doing (before asking anything)

The user may type nothing but `/framejam`. Check these in order and act on the first that applies. Don't ask "what do
you want to make?" if any of them answers it.

1. **What they typed.** "/framejam make a 10s teaser for X" → do that. A style check is only needed for a new video.
2. **This conversation.** If you've been making or editing a video in this chat, keep going with it: render the current
   state to the next `renders/vN.mp4`, then add it to the same project (`add_version` with its `reviewId`, or
   `open_review` with the same `title`), and wait for feedback.
3. **Feedback waiting.** Call `list_reviews()`. If a project is `sent_not_delivered` or `user_commenting`, call
   `get_feedback({ reviewId })` and apply it.
4. **A FrameJam project for this folder:** one whose `videoPath` or `panelsDir` is inside the
   current workspace.
   - `awaiting_user`: open its `url` and call `wait_for_feedback`.
   - `delivered_to_agent`: an earlier chat got the comments but never shipped the next version. Call `get_feedback` to
     get them again, apply them, and ship the next version.
   - A storyboard the user approved, and no video yet: build the video from the panels.
5. **A video project here, but no FrameJam project.** A Hyperframes `index.html` with `data-composition-id`, a Remotion
   or Motion Canvas project, a `renders/` folder or a loose video file: use the newest render if it's newer than the
   source, otherwise render. Open it as v1 and wait for feedback. Use the project's own tool; for a plain video file,
   pass `videoPath` only.
6. **Nothing relevant** (empty folder, unrelated code repo): open the Styles page and ask what video to make: what it's
   about, roughly how long, the format (16:9, 9:16, 1:1), and any copy, footage or brand assets. Mention they can pick a
   look on the Styles page. Don't start building from a style alone. New videos default to Hyperframes.

If several projects could match, ask one short question that lists them.

## The loop

1. **Style.** Call `get_selected_preset`. If it returns `selected: null`, ask the user to pick one on the Styles page you
   just opened (then call it again), or pick one yourself with `list_presets({ mood, pacing, format })` and `get_preset(id)`.
   - Follow `style.guide` literally, whatever the tool. Use the exact `palette` hex values, `fonts`, `easing` names,
     `transitions`, `textAnimations` and `rhythm.averageShotSeconds`.
   - `templateFiles` is a working Hyperframes composition. In a Hyperframes project, copy it in and replace the copy
     rather than starting from a blank file. With any other tool, don't copy it; read it as a reference for the look.
2. **Build** the video with the project's tool (Hyperframes details below, other tools further down).
3. **Render** to a *new file per version*, e.g. `renders/v1.mp4`, `renders/v2.mp4`, so earlier versions stay comparable.
4. **Open the review:** `open_review({ title, videoPath: "<abs>/renders/v1.mp4" })`. Use an absolute path, and the same
   `title` every time so later renders become new versions of this project.
   Open the returned `url` in the built-in browser (step 0) and tell the user in one line:
   "Click the video to point at something (or pause and type), then press **Finish review**."
5. **Wait, in the same turn:** call `wait_for_feedback({ reviewId })` right after opening the review. Don't end your turn
   first — the review page shows "Agent listening" only while you're in this loop.
   - `status: "pending"` means nothing arrived in the last ~50s. Call it again right away, without asking the user.
   - **Stop after 12 `pending` results in a row (about 10 minutes).** Don't wait forever. End your turn with one short
     message: the project's `url`, "Press **Finish review** when you're done, then paste the line the page shows (or
     say `apply my FrameJam feedback`) and I'll pick it up." The comments are saved, so nothing is lost. When the user
     comes back, call `get_feedback` (step 1.3). Stop earlier if the user tells you to in chat.
   - `status: "feedback"` returns `comments[]`, a markdown summary, and frame images.
   - `revised: true` means the user reopened their review after you got it and changed the comments. The new list
     **replaces** the old one: drop changes from the old list that aren't in the new one.
   - **Done?** If the comments only say the video is done, approved or good to go, with nothing to change, don't make
     another version. Tell the user where the final file is and stop waiting.
6. **Apply every comment.**
   - `at` / `time` / `endTime` is where in the video. `position` is where in the frame.
   - The frame image for a pinned comment has the pin drawn on it: look at what's under the pin, then find that element
     in your source at that time.
   - `wholeVideo: true` means a global note (pacing, colour, music, and so on).
7. **Ship the next version.** Re-render to `renders/v2.mp4`, then call
   `add_version({ reviewId, videoPath, note })` (or `open_review` again with the same `title`).
   The `note` is a one-line summary of what you changed; the user sees it when the new version arrives and in the version menu.
   Each version is one round: the user's "Finish review" locked the previous version, and the new one starts with no
   comments. If you couldn't address a comment, say why in chat and in the note.
8. Go back to step 5.

## Hyperframes (the default)

- **First run on this machine:** run `npx hyperframes doctor` once. It checks Node, ffmpeg and Chrome, which rendering
  needs. If something is missing, tell the user how to install it before you build.
- **Build** the composition: `index.html` with a root `data-composition-id` + `data-width`/`data-height`,
  `.clip` elements with `data-start`/`data-duration`/`data-track-index`, and a paused GSAP timeline registered in
  `window.__timelines["<id>"]`. Run `npx hyperframes lint` and fix errors.
- **Render:** `npx hyperframes render -o renders/v1.mp4`.
- **Open:** pass `videoPath`, like any other tool. The user reviews the render.

## Other tools (Remotion, Motion Canvas, ffmpeg, recordings, …)

- Keep the project's own tool and render command (`npx remotion render`, the Motion Canvas exporter, an ffmpeg script,
  a screen recording). **Don't convert the project to Hyperframes.**
- Render each version to a new mp4/webm/mov file and call `open_review({ title, videoPath })`.
- Use the preset's `style.guide`, `palette`, `fonts`, `easing` and pacing in the tool's own terms.

## Storyboards (before there's a video)

Use a storyboard review when the user wants to agree on the shots first, or asks for a storyboard, shot list, or
"frames before we animate". Same loop, but each version is a set of still panels instead of a render.

1. **Make the panels.** One image per shot (png, jpg, webp, gif or svg), all the same aspect as the final video, in one
   folder, named so they sort in order: `storyboard/01.png`, `02.png`, … Good sources, in order of preference:
   - Hyperframes snapshots of a rough composition (`npx hyperframes snapshot --at 0.5,2.5,4.5 -o storyboard`), or
     stills from the project's own tool.
   - Images you generate, one per shot.
   - Quick HTML mockups you screenshot.
2. **Open it:** `open_review({ title, panelsDir: "<abs>/storyboard", panels: [{ path: "01.png", title: "Cold open",
   caption: "Slow push in. VO: 'Every team ships faster now.' 2s" }, …] })`. `panels` is optional; without it every image
   in the folder is used in file-name order. Titles and captions are what the user reads under each panel, so put the
   shot name, the action or camera move, the voiceover line and the duration there.
3. **Wait** with `wait_for_feedback`, exactly as for videos (open the URL in the built-in browser first, and stop
   after 12 `pending` results in a row).
4. **Read the comments by panel.** `at` is `"panel 3 (Cold open)"`, `panel` has the number, title, caption and the
   panel's `imagePath`, and `position` is where on the panel the user clicked. The attached image shows the panel with
   the pin drawn on it. `wholeVideo: true` means the whole storyboard (order, pacing, adding or cutting shots).
5. **Next version:** update or regenerate the images, then `add_version({ reviewId, note })`. With no media it re-reads
   the same `panelsDir` and keeps titles and captions for files that are still there; pass `panels` again to change the
   order, titles or captions. Earlier versions keep their own copies of the images.
6. When the user approves the storyboard, build the video shot by shot from the panels and captions, and open it as a
   normal video review (a new `open_review` with the render as `videoPath`).

## Other ways in

- If the user says "apply my FrameJam feedback" (with or without a review id), call `get_feedback()`. Without a
  `reviewId` it picks the review whose comments haven't reached you yet. If the user typed comments but never pressed
  Finish review, they're handed over now. `list_reviews()` shows every project and where its round stands.
- If MCP isn't connected, the user can use **Copy comments as text** in the review page's version menu and paste the
  result into chat.

## Updating FrameJam

If the user asks to update FrameJam, run `npx -y framejam@latest install <app>` with the app you're running in
(`cursor`, `claude` or `codex`; without it, every app found on the computer is set up). It updates the skill, the MCP
server entry and the FrameJam page that's running. Then tell the user to restart the app once: your FrameJam tools load
the new version only after a restart.

## Rules

- Don't ask the user to describe timestamps in chat. Send them to the review page.
- Never fake a render. If a render fails, fix it before opening the review.
- Keep the review URL stable: one project per video, with a new version for each render.
- Call it a "project" when you talk to the user.
