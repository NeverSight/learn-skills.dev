---
name: review-ui-states
description: Map every screen and state of a web app as state machines, screenshot each with Playwright, and publish a review canvas on claude.ai where people pin comments. Use when asked to review the UI states or every screen of an app, find implicit state machines, or act on comments left on such a canvas.
---

# UI states

The deliverable is one page: every state of every flow as a screenshot, laid out as a graph per flow, with the reviewer's comments pinned on the screenshots. It exists so the reviewer can review an app without clicking through it, and so that their comments come back to you as a list you can fix in bulk. A second deliverable rides along: each flow's machine is a statement of which states exist, and writing it exposes where the code decides the screen from loose flags. Record those as findings.

A machine per flow, not a script per screenshot, is the point: `@xstate/graph` walks the shortest path to every state, so adding a state means adding a node and an event step, and the manifest the walk writes is what the canvas draws.

## 1. Set up the harness once per repo

Copy `assets/harness/flow.ts`, `manifest.ts` and `capture.spec.ts` into the repo's Playwright folder as `ui-states/` (for example `e2e/ui-states/`); they are app-agnostic. `assets/harness/canvas/` stays in the skill: the repo keeps the flows, the skill keeps the page that renders them. Add `xstate` and `@xstate/graph` as dev dependencies, and ignore `ui-states/out/` and `ui-states/.runs/` in git.

Write the two app-specific files. `assets/example/` is a worked example from the Drive module of one Frappe app: use it as the pattern, but its imports point at that app's e2e helpers and its API paths are that app's, so it does not run as-is.

- `scene.ts` exports `openScene(browser, baseURL, label)` and the `Scene` type. A scene is one signed-in page per capture path with its own workspace (a folder, a project, a record) that is deleted on `close()`, so paths never see each other's rows. It must offer `page`, `settle()`, `hold(url)` returning `{release, abort}`, and `close()`. `abort` keeps failing matching requests until `release`, because a transport that retries 5xx never shows the failed state otherwise.
- `playwright.config.ts` sets `OUT_DIR`, one project, no retries, `testMatch` on `capture.spec.ts`, and whatever server and user provisioning the app's e2e suite already has.

The app needs a running site that the e2e helpers can seed through its API. For a Frappe app, use `frappe-app-dev` to get the bench and site, and set `allow_tests` plus whatever the app's e2e suite needs (the example app also needed `ignore_csrf 1` for uploads).

## 2. Write the flows

One file per flow under `flows/`, listed in canvas order in `flows/index.ts`. Read [references/flows.md](references/flows.md) before writing the first one; it covers naming states, reaching loading, failed and mid-flight states with holds, transient states, and the shortest-path quirks that make a capture lie.

Flows are independent, so hand them to parallel subagents, two flows each, with the brief in `references/flows.md` and the finished example flow as the pattern. Give each agent the exact run command and tell it to look at every PNG before reporting. Ask for the implicit-state-machine findings in the report; the agent that wrote the machine has just read the code that should have had it.

Capture one flow with the env vars your config needs:

```sh
cd <playwright folder>/ui-states
UI_STATES_FLOWS=<flow> npx playwright test -c playwright.config.ts
```

When runs share provisioned users, run one flow at a time per machine under a lock; [references/flows.md](references/flows.md) has the command.

A flow is done when the run passes, `out/<flow>.json` lists every state with a screenshot or a transient reason, and you have looked at every PNG in `out/<flow>/` and each shows the state its description claims. A screenshot that shows the previous state is the common failure: the event step needs an `expect` on something only the target state has.

## 3. Record the findings

Write `out/findings.json`, beside the manifests it describes and ignored with them: `{ "<flow>": [{ "title", "detail", "fix" }] }`. A finding names the refs that together decide the screen, where they can disagree, and the explicit state you would introduce, with file paths. [references/findings.md](references/findings.md) says what counts. Verify each claim against the code before it goes on the canvas; the canvas shows findings beside the flow's graph, so the reviewer reads a wrong one as fact.

## 4. Build and publish the canvas

```sh
node <skill>/assets/harness/canvas/build.mjs out <build dir> <app name>
```

`<build dir>` must be under the session scratchpad or the working directory, since the Artifact tool reads from there. It writes `canvas.html`, copies the screenshots beside it, and lists them in `files.json`.

An artifact version holds at most 511 files and takes 255 per publish. With more than about 250 screenshots, pack the build before publishing: `uv run --no-project --with pillow python <skill>/assets/harness/canvas/pack.py <build dir>`. It converts the screenshots to lossless WebP, bundles them into `shots/<flow>.js` (one file per flow), and rewrites `files.json` to list the bundles. The page fills each lane's screenshots as its bundle arrives. When the files on an existing artifact change from screenshots to bundles, remove the old screenshot paths in the same publish (`files: {"<path>": null}`).

Before the first publish, and after any change to `canvas/template.html`, run `node <skill>/scripts/smoke.mjs <build dir> <flow> <state>` from the Playwright folder and look at the two PNGs it writes. [references/canvas.md](references/canvas.md) records how the page is meant to behave (lane layout, the arrow-key tree walk in the lightbox, the layout rules that keep every control on screen); read it before editing the template.

Publish `canvas.html` with the screenshots as `files` (use `root: <build dir>` and the paths from `files.json`), `icon: "map"`, and `capabilities: {"db": {}, "user": {"scopes": ["profile"]}}`. The `db` capability is where comments live; without it the page is read-only.

An artifact is private to the Claude account that publishes it, so publish with the Artifact tool from the account the reviewer uses on claude.ai. When the session has no Artifact tool, read [references/publishing.md](references/publishing.md).

Republish to the same url whenever a lane is added or a screenshot changes; comments key on `flow/state`, so they survive. Confirm the file count with a `scope: "files"` listing after a publish that added screenshots.

To let teammates pin comments, share the artifact from claude.ai with Contributor access or higher. Pins on the canvas are writes to the artifact's database, which Viewer and Commenter access do not allow: those people can see the page and use claude.ai's own artifact comments, but cannot pin comments on screenshots.

Give the reviewer the link and, per flow, the number of states captured and the states marked transient with their reasons. The page itself is the report; keep the message short.

## 5. Act on the comments

Each comment is a document in the `comments` collection: `flow`, `state`, `x`, `y` (fractions of the screenshot, or null for a note on the whole state), `text`, `by`, `at`, `done`, and optionally `kind`, `related` and `parent`. The reviewer either pastes the page's "Copy prompt" output or just says "fix the comments"; in the second case read the collection yourself (ArtifactData `list`).

Work through the open comments by flow. Open the screenshot and the flow's source to see what the pin points at. After fixing, recapture the flows you touched, rebuild, republish to the same url, and mark each comment `done: true` (ArtifactData `update` with its `if_version`). [references/review-loop.md](references/review-loop.md) has the comment fields, the prompt format and the edge cases.
