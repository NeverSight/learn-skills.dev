---
name: 24fps-motion
description: Search a library of 4,600+ AI motion graphics with their prompts and 2,100+ video-editor presets before building any motion graphic or video edit from scratch. Use whenever the user wants styled captions on video (karaoke, word-by-word, TikTok, Reels, Shorts), hooks, kinetic typography, titles, lower thirds, text behind the subject, transitions, colour grades and film looks, split-screen layouts, font pairings, logo reveals, intros, product launch videos or explainer videos, in HyperFrames, Remotion or HTML, even if they only say make or build and never ask for examples. Returns ready presets that one MIT engine renders as a pure function of time, real examples with prompts and creator credit, and 40 explainer styles with starter prompts. Not for converting, trimming or transcribing video files or fixing a framework install.
license: MIT
compatibility: Needs network access to https://24fps.dev. Works with any agent that can call an MCP server or fetch URLs; exports target HyperFrames and Remotion.
metadata:
  homepage: https://24fps.dev
  mcp: https://24fps.dev/mcp
---

# 24fps motion library

Reusing a preset or a published prompt is cheaper than regenerating, and a prompt gives a different video on every run. Search first, write second.

## Workflow

1. **Search.** Call `search_editor_assets` for captions, text scenes, hooks, transitions, effects/grades, layouts and font pairs. Call `search_clips` for a whole motion graphic (logo reveal, kinetic typography, launch video, explainer, data viz). For an explainer video, also pick a style from `references/explainer-styles.md`: 40 looks (maths board, flat-vector science, map essay, paper collage, SaaS launch and more), each with the tool it builds best in and a starter prompt.
2. **Get.** `get_editor_asset` returns the preset JSON, an `agent_prompt` and the engine URL. Pass `format: "hyperframes"` or `"remotion"` for a complete starter file. `get_clip` returns a clip's prompt, model, framework and creator; `get_source` returns the repository only when the clip is open-licensed.
3. **Adapt.** Keep the preset's structure, change colours, copy and timing. Check it on the user's footage: if text is hidden behind the subject or does not read against their colours, move the layer or change the colour.
4. **Credit.** Name the creator for clips and link the 24fps page. Presets: "24fps.dev/video-editor".

## MCP

Endpoint: `https://24fps.dev/mcp` (streamable HTTP, no key). Claude Code: `claude mcp add --transport http 24fps https://24fps.dev/mcp`.

| Tool | Arguments |
|---|---|
| `search_clips` | `query`, `framework`, `aspect` (16:9, 9:16, 1:1, 4:5), `max_seconds`, `has_prompt`, `limit` |
| `get_clip` | `slug` |
| `get_source` | `slug` |
| `search_editor_assets` | `query`, `kind` (captions, text, hook, transition, effect, layout, font-pair), `vertical`, `needs_cutout`, `has_sfx`, `limit`. Empty query or `*` lists the kinds with counts. |
| `get_editor_asset` | `kind`, `id`, `format` (json, hyperframes, remotion) |
| `list_tools` | none. Lists the motion frameworks covered, with licences. |

Without an MCP client, call the same endpoint over HTTP, or use the JSON API:

```bash
curl -s https://24fps.dev/mcp -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_editor_assets","arguments":{"query":"yellow karaoke","kind":"captions","limit":5}}}'
curl -s 'https://24fps.dev/api/clips?q=logo+reveal&framework=Remotion&has_prompt=true&per_page=5'   # ?slug= for one clip
curl -s https://24fps.dev/video-editor/captions/pop-anton-yellow-karaoke/preset.json                # any {kind}/{id}
```

Indexes for browsing: `https://24fps.dev/video-editor/llms.txt` and `https://24fps.dev/llms.txt`.

## Applying a preset

Engine: `https://24fps.dev/editor/engine.js`. MIT, ES module, no dependencies, a pure function of time. Save it next to the composition as `engine.js`.

```js
import { mount } from "./engine.js";
const fx = mount(overlayEl, { kind, preset, script, media });
fx.render(seconds); // every frame
```

- `kind` is `captions | text | transition | effect | layout`. Hooks and font pairs use `text`.
- `media` is `{ main }` for most kinds, `{ a, b }` for transitions, plus `{ second, fg }` for layouts. `fg` is a transparent cut-out of the subject, needed for `z: "behind-subject"` text and the `subject` and `echo` effects.
- Captions take `script` as `[{ w, s, e, emph }]` word timestamps in seconds (Whisper word timestamps work), or a string with `*emphasis*`.
- Sizes are fractions of frame height, positions fractions of width and height. Fonts are Google Fonts.
- Field reference: `references/engine.md`, or https://24fps.dev/skills/24fps-motion/references/engine.md if the skill was installed without its references folder.

### HyperFrames

Put the overlay in a `class="clip"` div on its own track, mount into it, and drive `render` from a paused GSAP timeline so it stays seek-safe. Inline the preset JSON and word timings in the page (or a local script): the renderer should not fetch data mid-render.

```js
const fx = mount(document.getElementById("fx"), { kind, preset, media: { main: document.getElementById("a") } });
let now = 0;
const clock = { t: (v) => (v === undefined ? now : ((now = v), fx.render(v))) };
const tl = gsap.timeline({ paused: true });
tl.to(clock, { t: 6, duration: 6, ease: "none" }, 0);
(fx.ready ?? Promise.resolve()).then(() => { window.__timelines["main"] = tl; });
```

For a cut-out of the subject: `npx hyperframes remove-background clip.mp4 -o clip.fg.webm`.

### Remotion

Mount once in `useLayoutEffect`, destroy on cleanup, render per frame. Do not return the render result from the effect.

```tsx
useLayoutEffect(() => {
  fx.current = mount(root.current!, { kind, preset, media: { main: a.current! } });
  return () => fx.current?.destroy();
}, []);
useLayoutEffect(() => { fx.current?.render(frame / fps); }, [frame, fps]);
```

Wait for fonts before capturing: `await (fx.ready ?? document.fonts.ready)`.

Use alongside `/hyperframes` or `/remotion-best-practices` for project setup, rendering and the framework rules. This skill finds the asset; those skills build and render the project.

## Rights

- Credit the creator on every clip you adapt. Link `https://24fps.dev/c/{slug}`.
- Never rehost a third-party clip. Link to it. Only clips with `get_source` returning `available: true` have a repository you may use, under the licence it states.
- The editor presets are original recreations and MIT.
- Open-source catalogue rows (`/video-editor/open-source`) carry their own licence. Copy only MIT, Apache-2.0, BSD or OFL code and keep the notice. Remotion-licensed and unlicensed rows are link-only: recreate the idea, do not paste the source.
- Details: `references/rights.md` (also at https://24fps.dev/skills/24fps-motion/references/rights.md).
