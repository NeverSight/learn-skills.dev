---
name: cinematic-shot
description: Shoot software UI like a film. A sequence of hero shots, each a steep, oblique, extreme close-up of the interface floating on a stage (a black void for dark products, a high-key studio for light ones), with a razor-thin focal plane, a slow motivated camera drift, and UI that acts on its own, hard-cut on the action, ending on one line of copy and a still logo. It also shoots stills, the same look frozen into single photographs. Use when asked for a launch video, product film, feature trailer, teaser, promo clip, hero shot, or any "cinematic" footage of an app, UI, or website, and also for a hero image, key visual, product photo, poster frame, launch-post image, Open Graph or social card, or any "cinematic" still of a UI. This skill covers camera, framing, light, and edit. It is stack-agnostic.
---

# Cinematic shot

You are the director and the DP, not the motion designer. The film is a sequence of **hero shots**. Each one looks at a real piece of the product's UI from a steep, low angle, so close that the focal plane covers only a line or two of text and everything else melts into bokeh. The camera drifts slowly toward where the next thing will happen. The UI does the work by itself: things get typed, streamed, selected, and written while we watch. Nothing explains itself with captions.

This skill is about camera, framing, light, and the edit. Build the film with any rendering stack. Whatever you choose, make every frame a pure function of time, so the film renders deterministically and can take motion blur.

The same camera also takes **stills**: single photographs of the UI in the same look, for a hero image, a launch post, a social card, or a poster. When the user asks for images rather than a film, read section 10 first; it says which parts of the method carry over and what changes when nothing moves.

Read [references/look.md](references/look.md) for exact camera, depth-of-field, light, reveal, type, and still recipes. Read [references/shot-list-example.md](references/shot-list-example.md) for a full example of the shot grammar and a still set.

## The taste

The product floats on a stage like a slab, tilted away from the camera, lit softly where it matters. The camera is low and close, looking *along* the UI rather than at it, so lines of text run diagonally across the frame and shrink into the distance. The focal plane is a thin band: one control, one line of typing, one row of a list is sharp, and the rest is soft bokeh. The camera never stops drifting and never moves fast. Shots are long enough to watch something happen. The only colour is the product's own. Restraint everywhere else.

There are two stages, and the product's real theme picks one (section 2):

- **Dark stage**: a black void. A dark slab, lit by a soft pool that follows whatever matters and lets everything else fall into black.
- **Light stage**: a high-key studio. A white slab resting over a warm light-grey ground, separated from it by a soft cast shadow, with a gentle key on the subject and nothing falling to black. On white, the bokeh becomes a soft haze.

## 1. Find the story before the shots

Before planning a single camera, write down:

- **The flow**: the 4–7 things that happen on screen, in order. Examples: open a view, select a tab, type a prompt, watch the answer stream in, watch a document write itself, approve.
- **The payoff**: the one moment where the product visibly does something remarkable. The film exists to reach this frame.
- **The demo content**: concrete, believable data inside the UI, such as names, IDs, statuses, code, and short human-sounding text. Real-looking density is what makes a close-up beautiful. A list of twelve plausible issues reads as a product; three grey placeholders read as a mockup.
- **One line of copy**: the product or feature name, then a tagline of five words or fewer.

When you record the user's real website rather than a rebuild, build the story from what the real page actually animates (section 6), not from what a rebuild could fake.

## 2. Pick the stage from the product's real theme

Decide this before the shot list. "Keep the real UI faithful" outranks "dark slab".

- **The product has a genuine dark theme**: use the **dark stage**.
- **It is light only, or light is its primary identity**: use the **light stage**. Never fake a dark theme and never invert colours. A site's unused dark styles are not a dark theme: if forcing them breaks the page (white cards, invisible text), the product is light only.
- **It has both themes**: ask the user, or follow their brand.

Every shot in the film uses the same stage.

## 3. Write the shot list

Post the shot list before building, then keep going:

| # | Cut at | Len | Subject (what is in focus) | Scale | Angle | Move | Action |
|---|---|---|---|---|---|---|---|

Rules:

- **Length**: 45–55 s in all, with 8–10 UI shots, then the copy and the logo.
- **Shot length follows the action.** Process shots (typing, streaming, a document writing itself, a long diff) run **5–9 s**. Punctuation shots (a tab, a button, a nav item) run **2–3.5 s**. Alternate the two, so a long watch is followed by a short accent. Median about 5 s.
- **Cut on the action, not on a metronome.** There is no beat grid. Cut in when the subject is already in frame or about to arrive; the action starts within 0.3–0.8 s; hold the result for 0.5–1 s; cut while the camera is still moving.
- **One idea per shot.** A shot can contain a short chain (type → send → the reply starts) only if the camera follows one continuous thread.
- **Vary scale like an editor.** Extreme macros and macros dominate. Medium shots carry the longer process. Hold back the **wide shot** (the whole window, near-frontal) for the payoff, where it lands like a release. Return to a close-up after it.
- **Alternate the diagonal.** If the text in one shot rises to the right, the next shot's text falls to the right, or the plane tilts the other way. Every cut should read as a new camera position.
- **No continuity cursor.** The UI acts on its own (see section 5). The viewer never needs to follow a pointer between shots.
- **Separate surfaces get separate setups.** When the story moves to another surface (a terminal, a phone, another app), give it its own slab on the same stage and hard-cut to it.

### Shot scales

Measure scale as magnification of the UI at the focal point, relative to its native size:

| Scale | Magnification | Use for | Depth of field |
|---|---|---|---|
| Extreme macro | 5–7× | A single tab, a button, a nav item, a status badge. One or two words fill a third of the frame. | Only the subject is sharp. Everything else is heavy bokeh. |
| Macro | 2.5–4× | A composer with a line of typing, a few rows of a list, a code hunk | A band 2–4 text lines deep is sharp |
| Medium | 1.5–2.5× | A panel at work: a list streaming in, a document writing itself, a diff with a sidebar | A wider band is sharp; the far edge and near edge stay soft |
| Wide | 0.8–1.1× | The payoff only: the whole window, near-frontal, with content scrolling or changing | Mostly sharp; the frame edges still soften |

Macro shots must stay crisp. Rasterise the UI at the resolution of the magnification (for example 6×) before the camera scales it. Never upscale a 1× bitmap.

### Camera angle

This is the signature of the look. Except for the wide shot, the camera is **low and oblique**, looking across the UI plane:

- **Tilt the plane back** 30–50° (pitch), so the far side of the UI recedes and the near side looms.
- **Rotate it in-plane** 10–20° before tilting, so lines of text run diagonally. Flip the sign between consecutive shots.
- **Add a little yaw**, ±5–15°, so one side of the frame is closer than the other.
- **Use a short-ish perspective** so the foreshortening is obvious: near text should be about 1.4–1.8× the size of far text in the same frame. A perspective distance of about 0.6–0.75× the frame width works (1100–1400 px at 1080p).
- **The wide shot is the exception**: near-frontal, pitch 8–12°, no in-plane rotation, yaw within ±3°.
- **Framing**: crop aggressively. On the dark stage, the slab's edges run off frame or fall into black, and a quarter to a half of the frame is often the void, or UI so far out of focus that it reads as texture. On the light stage, the slab's edges run off frame or show as the page's real edge with its cast shadow on the ground; a crop edge must never show (see the light stage in [references/look.md](references/look.md)).

### Camera move

Each shot is one continuous move. It is **motivated**: the camera drifts toward where the next thing will appear.

- **Track** along the reading direction of the action: 3–10% of the frame width over a typical shot, up to 20–35% for a long pan along a diff or a document.
- **Follow** content as it grows: when an answer streams downward, drift down with it; when a line is typed, drift with the caret.
- **Push** gently, a 1–5% scale change over the shot. Pull-outs are rare.
- **Turn** slightly, 0.5–4° of roll or yaw change over the shot.
- **Speed**: constant (linear) velocity, or a short ease-out arrival over the first third that then continues at a slow constant drift. The camera never eases to a full stop and is still moving at the cut. No handheld noise, no shake.
- **Rack focus** with the action: when attention moves from the typed line to the reply, or from a title to the body, slide the focal band there over 0.4–0.8 s.

## 4. Light and grade

Every shot must look like it was filmed on the same stage. Values for both stages are in [references/look.md](references/look.md).

### Dark stage: a black void

- **Stage**: true black around the product. No gradient wallpaper, no coloured haze, no floor.
- **Subject light**: a soft, neutral pool on the subject, not the frame. The UI falls off to black within roughly a third of the frame width from the focal point. The pool lies *on the UI plane*, so the tilt foreshortens it and the roll lays it along the diagonal. It is longer along the line of action, has a hot spot nudged toward an off-axis key (the key side flips with the diagonal), and sometimes has one side cut by a soft flag. It trails the subject by a beat, slides with a rack focus, and opens up as content grows and at the payoff. It is never a centred circle that looks the same in every shot. There is no coloured key light.
- **Low key**: the average frame is very dark (about 7–10% luminance). Bright pixels are reserved for in-focus text and the product's own coloured UI. Anything bright and out of focus gets dimmed.
- **The product is a dark slab**: its own chrome, rounded corners, and a faint 1 px edge highlight on panels.

### Light stage: a high-key studio

- **Ground**: a warm light grey, a little darker than the page, so the white slab separates from it. Never white, never black.
- **The product is a white slab**: the page's real viewport with rounded corners, floating over the ground. A wide, soft cast shadow and a tight contact shadow under it make it read as an object in a studio.
- **Subject light**: no pool mask and nothing falling to black. A soft key only: the slab darkens by at most about 12% away from the subject, along the same lagged, on-plane ellipse as the dark stage, but wider and with a long, gentle shoulder. The lens vignette is faint and goes toward grey. No flags.
- **High key**: a mean luminance of about 75–90% is expected, not a fault. The page's white sits just below clipping. In-focus text is the product's own dark ink. Out-of-focus areas are not dimmed; on white, bokeh is a soft haze.

### Both stages

- **Keep the real UI faithful**: do not restyle it, recolour it, or swap its theme.
- **Colour belongs to the product**: status icons, diff greens and reds, a brand-coloured primary button. Add no accent of your own: no flares, no glows, no rings, no tinted light.
- **Finish**: motion blur (180° shutter, 4+ sub-frames) and fine film grain on the final render. Together with the depth of field, these three do almost all the work.

## 5. Motion inside the shot

- **No cursor.** The UI acts on its own. A nav item highlights. A tab's selection pill slides over. A button depresses. A gutter control appears on a code line and the line highlights. If a click must read, show it through the control's own pressed or selected state.
- **Typing**: 12–13 characters per second with a visible caret. Code identifiers and file references turn into inline chips as they are typed. On send, the composer clears and the message moves into the thread.
- **Streaming**: generated text resolves line by line, top to bottom. Each line arrives as a fine stipple of dots that condenses into solid glyphs over about 0.5 s, staggered by about 0.1 s per line. Icons and avatars resolve the same way.
- **Writing**: documents and diagrams build in order: a title, then a heading, then paragraphs; diagram nodes, then connectors drawing on, then labels.
- **Scrolling**: in medium and wide shots, the content may scroll smoothly under a drifting camera. This is the second layer of motion, and it should feel like reading speed.
- **Appear**: new panels and messages fade and rise slightly through a small blur on an ease-out of 0.3–0.5 s. Nothing pops with overshoot.
- **No impact effects.** The payoff is shown by scale (the wide shot) and by the amount that changes, not by shake, flashes, or rings.

## 6. Recording the real site

When the user wants their real website rather than a rebuild, record the live page. This applies to both stages.

- **Drive the live page** in a headless browser and record its own states: clicks, hovers, its CSS animations, and its JS-driven cycles.
- **Make time deterministic.** Install the browser automation's fake clock before navigation, so JS timers and `requestAnimationFrame` follow it. Step every CSS animation and transition by hand each frame: take `document.getAnimations()`, pause each one, then set `currentTime += dt`. Every frame is then a pure function of time.
- **Trigger interactions from page JS** with `element.click()`. The automation's own click helper waits on `requestAnimationFrame` and hangs under a fake clock.
- **Clean the page first**: block analytics requests and dismiss announcement banners before recording.
- **Trace JS-driven state cycles** under the fake clock. Find when each change happens after the page settles (for example, a status that flips from Idling to Scaling up about 11 s after settle), then add a lead so each change lands where the shot list needs it.
- **Probe text positions** with a text-node `Range` search. `getBoundingClientRect` on selectors misses text split across nodes.
- **Capture regions at any scale** with the Chrome DevTools Protocol: `Page.captureScreenshot` with `clip.scale` renders a region at the magnification you need without changing the device pixel ratio or firing resize events.

## 7. Ending: copy, then a still logo

1. **Leave the last UI shot** with a hard cut to the stage, or a quick 0.4 s blur-and-fade into it: to black on the dark stage, to the ground colour on the light stage.
2. **The copy**: one centred line on the stage, about 80–100 px at 1080p, weight 500, tracking about −0.02em. White on the dark stage; the product's own dark ink on the light stage. It arrives by un-blurring from about 16 px while fading up over 0.6–1 s. Either set the whole line at once, or set the product name first and then append the tagline on the same line, letting the line re-centre as it grows. On the dark stage, a faint soft glow behind the type may settle away as it sharpens; on the light stage there is no glow. Nothing sweeps across it. Hold for 3–5 s.
3. **The logo**: cut or short-dissolve (about 0.3 s) to the still logo, either the mark alone or mark and wordmark, about 110–120 px tall at 1080p. Plain white on the dark stage; the brand colour on the light stage. It does not move, pulse, or glow. Hold it for 4–5 s and end the film on it.

Add no CTA buttons, URL cards, or "available now" banners unless asked.

## 8. Sound

There is **no music**: no score, no drone, no beat, no risers, no braams, and no tonal stings. The soundtrack is quiet, tactile foley over near-silence.

Every visible action gets a cue: a soft key tick per typed character, a soft click when a tab or item is selected, a quiet whoosh on send, and a faint granular hiss under streaming text. The payoff gets no impact. The copy and the logo play over silence.

## Don't

These make a film look like a tutorial or a template:

- Cold opens, title cards, or "Introducing…" and "New in…" screens before the action.
- Keycap overlays, captions, callout arrows, or labels that explain the UI.
- A visible mouse pointer driving the action, or a cursor travelling between targets.
- Flat, frontal close-ups. Outside the wide payoff shot, the camera looks across the UI, not straight at it.
- Everything in focus. If the frame has no bokeh, the shot is too wide or the focal band is too deep.
- Dissolves or dips to black between UI shots. The UI shots use hard cuts only.
- Fast moves, slow orbits, big 3D rotations, swooping fly-throughs, camera shake, or a camera that eases to a stop.
- Cutting to a grid. Two-second shots back to back read as a sizzle reel; let process shots breathe.
- Restyling the product's UI to look "cinematic". Keep the real UI faithful, and get the cinema from the camera, the focus, and the light.
- Forcing a dark theme onto a light-only product, or inverting its colours.
- The black void or a black light pool on a light page. It reads as a black overlay with a hole cut in it.
- Dimming bokeh on the light stage.
- A light pool that is a screen-space circle, centred and identical in every shot. It reads as a black overlay with a hole in it, not as light on the slab.
- Anamorphic flares, glow, accent rings, coloured key light, or any colour the product does not already have.
- Light that moves across the frame: sheen bands, sweeps, or light bars travelling over the UI. The light follows the subject; it does not perform.
- An animated logo reveal.
- Music of any kind, including a score, a beat, a drone, risers, braams, or bells.

## 9. Preview, then verify like a DP

Before any full-quality render, render a lightweight preview (960 × 540, 30 fps, 2 motion-blur sub-frames, half capture scale), show it to the user, and wait for their OK.

Render a still at the middle of every shot, at each action's peak, at the payoff, and at the copy and logo frames. Judge each one as a frame grab from a film:

- There is exactly one sharp subject, and the eye lands on it in under half a second.
- The focal band is thin, with both near and far bokeh, except in the wide shot.
- The plane reads as tilted: text runs diagonally and visibly shrinks into the distance.
- Text in focus is legible at half resolution.
- Consecutive shots differ in scale or in the direction of the diagonal.
- Every frame shares the same stage, neutral light, and grain, but the light's shape changes with each camera: foreshortened, stretched along the action, and lit from one side.
- On the **dark stage**:
  - at least a quarter of the frame is black or near-black;
  - the average frame luminance is about 7–10%.
- On the **light stage**:
  - the slab reads as an object: an edge or its shadow is visible in most shots, except extreme macros;
  - no crop seams show;
  - the subject is the brightest, crispest area;
  - the mean luminance is high-key, not grey-washed: text contrast is still strong.
- Pick the strongest frame as the poster.

Iterate until every still could be a screenshot in a launch post.

## 10. Stills: the static shot

A still is shot on the same set as the film, by a photographer instead of a DP. The stage, the oblique view, the shallow focus, the light on the plane, the grade, the grain, and the faithful UI all carry over. The film's camera does not.

**A still is not a frame of the film.** The film's camera is built to move: a short lens, a plane rotated in its own surface and yawed, a subject half off the frame, and a focal band that crosses the subject. In motion, each of those resolves a moment later: the drift reveals what was cut, the rack finds the focus. Frozen, nothing resolves, so a film frame reads as a grab of a camera passing by. A still is composed from scratch for the one frame: a longer lens, a level camera rolled as a whole, one complete subject that is entirely sharp, a real edge of the object, and calm negative space. It has to do alone what the drift, the cut, and the rack did together.

Shoot stills when the user asks for images: a hero image, a key visual, a launch-post image, an Open Graph or social card, a poster, or a set of product photos. When they ask for a film, still offer the poster frame (section 9) as a still. Never export a film frame as the still: it carries motion blur, the film's resolution, and a camera built to move. Re-shoot that moment as a still, with its own camera and composition, by this section's rules.

### What carries over, and what changes

| Part of the method | In a still |
|---|---|
| Story (section 1) | Still needed, shorter: the payoff and the demo content. Each still shows one moment of the flow. |
| Stage (section 2) | Unchanged. Every still in a set uses the same stage. |
| Shot list (section 3) | Becomes a **still list** (below). Scale variety and the alternating diagonal still apply; length, cuts, and the camera move do not. |
| Camera angle | **Re-set for the still** (below): a longer lens, the diagonal from camera roll instead of in-plane roll, no yaw by default. Values are in Stills in [references/look.md](references/look.md). |
| Camera move | None. The camera is frozen, so composition leads the eye instead (below). |
| Rack focus | None. The sharp zone is fitted to the whole subject, then falls off fast. |
| Subject light (section 4) | Still on the plane, with an off-axis key. No lag: centre the spill on the subject, plus the key offset. Flags are welcome on the dark stage; a still can carry a stronger graphic shape. |
| Motion (section 5) | A **frozen moment** (below), never a static screenshot. |
| Motion blur | None. Supersample instead, so edges stay clean (see Stills in [references/look.md](references/look.md)). |
| Grain | Yes, static and lighter than the film's, since it does not move to hide. |
| Ending, logo, sound (sections 7–8) | None, unless the user asks for copy or a logo on the image. |

### Write the still list

Post it before rendering, then keep going:

| # | Format | Subject (what is in focus) | Scale | Angle | Frozen moment | Negative space |
|---|---|---|---|---|---|---|

- **One still**: make it the payoff, at macro or medium scale, unless the user asks for the whole product. A single still has nothing to contrast with, so a wide near-frontal frame reads as a screenshot.
- **A set** (3–6 stills): vary scale like the film does, flip the diagonal between neighbours, and allow at most one wide frame. A set should read as one shoot: same stage, same grade, same grain.
- **Format first.** The format decides the composition, so pick it before the angle. Common formats and sizes are in [references/look.md](references/look.md). Never crop one frame into another format afterwards: reframe the camera for each format, because a crop moves the subject off its third and can cut the diagonal.

### Set the photographer's camera

Re-set the camera for each still. Never reuse a shot's film camera:

- **A longer lens.** Use a perspective distance of about 2–2.4× the frame width (the film uses 0.6–0.75×), like a product photographer's short telephoto. Get the tilt from pitch instead of from a wide lens: near text is about 1.2–1.4× the size of far text, not 1.4–1.8×. A short lens in a still looks like a camera sweeping past.
- **Level the plane, then roll the camera.** Put the diagonal into a camera roll of 6–10°, which rotates the whole frame, and leave the UI unrotated on its plane. Keep yaw at 0. The sharp band then runs *along* the lines of text, so a whole word, line, or headline is sharp at once. With the film's in-plane roll, the band crosses the line and half the subject melts, which reads as focus still racking.
- **The exception is one compact control**, such as a tile, a button, or a badge. There, roll the plane 12–16° so a row of its neighbours recedes along the diagonal into the blur.
- **Use yaw only to separate.** When a neighbour at the same depth as the subject would be just as sharp (the next card in a grid, the same row in another panel), yaw up to about 10° to push it back into the blur, or reframe it out of the shot. Never yaw for drama.

### Compose the frame

Without a moving camera, the frame has to point at the subject on its own:

- **One whole subject.** The sharp subject is a complete unit: a whole word, a headline with its avatar, a whole list, or a whole control. It sits entirely inside the frame, at least 8% of the frame height from every edge. In-focus text never touches or crosses a frame edge; only blurred text may run off.
- **Fit the focus to the subject.** Make the sharp zone exactly as deep as the subject, so every corner of it is sharp, then let blur rise steeply outside it: the next line beyond the subject is already visibly soft, and the far third of the frame reaches the maximum blur. A fixed thin band either cuts the subject or, widened to cover it, sharpens the whole frame.
- **Show the object.** Let one real edge enter the frame: the slab's edge with its cast shadow on the light stage, or the subject's own card or panel. The edge makes the UI an object on a set and gives the frame a structural line. It leaves the frame well away from a corner, and it never runs along a frame edge or just touches one (a tangent).

- **Put the subject on a third**, near one of the four intersections, never dead centre. The extreme macro is the exception: a single word or control may sit near the centre if the diagonal runs through it.
- **Let the diagonal lead in.** Lines of text should enter from one corner and run toward the subject, so the eye slides along them and lands on the sharp band.
- **Leave negative space** on the far side of the subject: a third to a half of the frame. On the dark stage it is the void; on the light stage it is soft haze, clean slab, or the ground. If the user wants copy or a logo on the image, it goes there, never over the UI.
- **Keep the negative space calm.** Half-legible bands of text, a dark card cut by the frame edge, or a sharp neighbour at the edge all pull the eye away. Reframe, push in, or yaw until they are gone or deep in the blur.
- **Dress the set.** What motion forgives, a still shows. If a translucent overlay (a backdrop-blurred menu, a sheet) smears the content behind it into stains, scroll to an empty part of the page or hide that content for the capture. Never change the subject itself.
- **Near and far bokeh both show.** A still is judged longer than a frame of film, so a frame with bokeh on only one side looks flat.
- **Crop for the format's safe area.** For social cards, keep the subject and any copy inside the central 80% of the frame, because platforms crop the edges.

### Bracket, then choose

A photographer does not take one frame. Before the contact sheet, render a framing pass for each still at a quarter size: 6–9 variants that differ in magnification, the subject's position, and the camera roll. Pick the one that passes the checks below, and show the user only the chosen frames.

### Freeze a moment, not a state

A still of a UI at rest looks like a screenshot. Pick the frame where the product is visibly doing something, at a point that reads as deliberate, not as a glitch:

- **Reads as a moment**: a caret mid-line with part of a prompt typed; the last one or two lines of a reply still resolving out of the stipple while the lines above are solid; a selection pill just landed on its tab; a button in its own pressed colour; a diagram connector half drawn.
- **Reads as a glitch**: a panel caught mid-fade or mid-blur in the Appear recipe; a selection pill halfway between two tabs; a scroll caught mid-ease; a whole block of text half stippled at once.

When recording a real site (section 6), seek the fake clock to the chosen moment, step the page's animations to it, and capture once.

### Render and deliver

- **Render each still once at 2× and downsample** to the delivery size; this replaces motion blur as the anti-aliasing. Capture the UI at the still's magnification times two, as in section 3.
- **Add grain last**, after the downsample and right before writing the delivery file, so it also dithers the dark gradients of the pool. Without it, the dark stage bands.
- **Show a contact sheet first.** Before full resolution, render every still at a quarter size on one sheet and wait for the user's OK, as with the film preview.
- **Deliver lossless PNG**, plus a JPEG without chroma subsampling (or a lossless WebP) for the web when asked, so the product's coloured text stays crisp.

### Verify each still

Use the checks in section 9, minus the ones about motion and cuts, plus:

- The eye lands on the subject in under half a second, with no camera move to lead it there. At a tenth of the size, the subject still reads as a shape.
- The whole subject is sharp, and every edge of it is inside the frame with margin. No in-focus text touches a frame edge.
- One real edge of the slab or of the subject's own card is in frame, without a tangent.
- The negative space is calm: no sharp neighbour, dark mass, or half-legible text at the frame edges.
- It does not look like a frame from the film: no short-lens sweep, no band crossing the subject, nothing caught on its way into the frame.
- The subject sits on a third, and the diagonal leads into it.
- The frozen moment reads as intended, not as a dropped frame.
- There is no visible crop edge, banding in the dark gradients, or chroma smear on coloured text.
- In a set, the stills could hang together: the same stage, grade, and grain, with different scales and diagonals.

Don't, in a still:

- Export, or re-render, a film shot's camera as the still. Re-set the camera and compose the frame for it.
- Cut the subject with the frame edge, or let the focal band cross it.
- Take a frontal screenshot and blur its edges. That is a vignette, not depth of field.
- Fake motion with streaks, speed lines, or a directional blur. A still is frozen.
- Add device frames, browser chrome the product does not have, reflections, or a floor, unless the user asks.
- Put copy over the UI, or put more than one line of it on the image.
