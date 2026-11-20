---
name: depth-diorama
description: Make a short looping film from a sentence. You write a small 3D scene (a place, a product, a character, a machine) and the engine films it with a real moving camera. It opens as a flat illustrated poster, then the camera flies in, circles and rises while things in the scene move, come apart and light up, and it closes back to the poster. Illustrated ink-and-colour look, MP4 or WebM at 16:9, 9:16, 1:1 or 4:5, checked automatically. Use when asked for a depth diorama, a flat-to-3D reveal, a product reel or exploded view, an animated poster, a title sequence, a looping background, or a Reel, Short or TikTok made from a description alone.
---

# Depth Diorama

The user gives you words. You write one scene file. The engine films it.

Nothing is needed from the user except the idea: no photos, no 3D models. You are the art director and the modeller. The engine is the camera crew: it handles the lens, the flight path, light, ink outlines, motion blur and checking.

**The premise.** A very long lens flattens a deep scene into something that looks like a printed poster. Then the camera moves in while the lens widens, and the poster opens into a world. Every film starts and ends on that poster, so it loops.

Run every command from this skill's folder, as `node bin/depth-diorama.mjs <command>`. There is no install step: the first command installs the packages and a headless browser it needs (about a minute, once; tell the user it is a one-time setup). It needs Node 20+ and ffmpeg; if anything reports a machine problem, run `doctor` and follow what it says.

## Workflow

1. **Pin down the brief.** Decide what you can; ask only for what you cannot: the subject, any words it must show, and where it will be watched. 9:16 for Reels, Shorts and TikTok; 4:5 or 1:1 for feeds; 16:9 otherwise.
2. **Choose the kind of film.**

   | The idea is | Choreography | Look | Pattern to read first |
   |---|---|---|---|
   | One object: a product, character, vehicle, machine | `turntable` | `studio` | `scenes/runner/scene.js` |
   | A place with one long axis: street, pier, platform | `glide` (fluid) or `reveal` (with pauses) | `day`, `dusk`, `night`, `rain` | `scenes/market/scene.js` |
   | One big image that breaks into a world | `launch` | any | `scenes/whale/scene.js` |

3. **Gather reference, if the subject is not one you could draw from memory in detail.** A particular place, vehicle, product category, era or regional style: search the web for three to six pictures. Write a short **inventory** at the top of the scene file as a comment: the main masses and their proportions, the six to ten colours, the kinds of signage or markings, the props that make it recognisable, the density (how many people, signs, windows), and the light. Build against that list. Reference is for learning what things look like. Never copy a picture, a logo or a design into the scene: draw your own version. Scenes load nothing from the network.
4. **Read `SCENES.md`**, then `new <name> --look <look>` and write `scenes/<name>/scene.js` (or `new <name> --dir <folder>` to work elsewhere, which creates `<folder>/<name>/scene.js`; every command accepts a scene name, a folder or the full path to a scene.js). Plan the camera as well as the set: choose a choreography, or write your own path when the subject calls for a move the presets do not make (a dive down a street, a climb up a tower, a slow orbit).
5. **Review in rounds until nothing is weak.** Each round: `stills <name> --aspect <shape>` at every beat of the camera path, plus the moments between beats with `--times 1.4,2.1,...` (seconds) to catch clipping and smearing in transitions. Open every still at full size. Hold each against the detail bar and craft notes below, and against your inventory, and ask: would this hold up as a still from a professionally illustrated animation? Write down the three weakest things in each frame, fix them all, and render the next round. Stills are drafts: during fast moves they show stepped copies instead of blur, which is expected. Before the final render, check the fastest moments with `stills --final --times ...`, which renders them with full motion blur.
   **Do at least six rounds** for any scene with more than a few objects; first versions always look empty, stiff or muddy, and the fourth still has problems. Do not stop at "better": stop when a full round turns up nothing you would be embarrassed to show.
6. **`preview <name>`** for a fast half-size video with checks. Open its contact sheet. Fix what fails.
7. **`render <name> --aspect ...`** for the final film, with a report and a contact sheet beside it.
8. Give the user the video. Offer **`share <name>`**, which writes one HTML file with a draggable player.

Output goes to `out/` in this folder for the built-in scenes, and to an `out/` folder beside the scene for a scene kept anywhere else. `--out` sets it explicitly.

Never edit files in `engine/` to get a result for a scene.

## The detail bar

A finished scene clears every line of this. The engine checks the camera; this list is how you check the set.

- **No dead surface.** Anything the camera passes within a few seconds of carries something: a picture, a sign, windows, texture, wear, a prop. A plain coloured box is a placeholder.
- **Pictures are drawn, not hinted.** Screens, posters, packaging, labels, murals and logos are drawn as real pictures with `k.svg` (see the craft notes): figures with faces and clothes, products with highlights, layouts with hierarchy. A circle on a triangle is not a person. If the user supplies pictures (a logo, a product shot), place them with `k.image`.
- **Variety.** At least three different designs for anything that repeats (buildings, vehicles, signs, trees). Vary height, colour and detail so no two neighbours match.
- **Density that matches the place.** A busy crossing has hundreds of people, a market has goods on every stall, a bedroom has things on every shelf. Crowds are cheap: use as many as the place needs.
- **Something in every layer.** Foreground, middle and background each have their own detail, so depth reads when the camera moves.
- **One light idea.** A clear key (sunset, neon, a single lamp), coloured pools on the floor, and glow where light comes from.

## Craft notes

What separates a rich scene from a plain one. None of this is subject-specific; it applies to any place or object.

**Pictures in SVG.** Every screen, poster and label is a picture worth looking at.
- Build figures in layers, back to front: back hair or cape, body and clothes, neck, face, front hair, then eyes (white, iris, pupil, two highlights), brows, blush, mouth. Faces read from across the street only when eyes are large and high-contrast.
- Give every picture a background with texture (gradient plus a halftone dot pattern, rays, stars or stripes), one focal figure or product at about 60 % of the height, a bold title with a thick outline (`paint-order="stroke"`), a smaller second line, and a strip with a date or price.
- Products: silhouette path, a darker shadow side, a light highlight stripe, a label, and a cast shadow or glow under it.
- Draw pictures at 1024 px, or 2048 for any picture that fills a large part of the frame, and size the box to the viewBox's shape.

**Facades.** Use `k.svg` with a separate `lit` picture so only the windows glow at night. Draw at least three kinds of front for a street: a curtain wall with mullions and reflections, a multi-tenant block with a different sign on every floor, a concrete or tiled block with balconies, louvres or air-conditioning units, a shopfront with a lit interior. Put clutter on the roofs (tanks, units, billboard frames) and something at street level on every front (doors, menus, shutters, vending machines, bikes).

**Light at night.** Night is made by light, not by darkness. Put a `k.light` at every lamp, window cluster, shop front, fire or sign that would cast light (warm for lamps and windows, coloured for neon), so facades and the ground pick up soft pools of colour; give the light source itself a glowing object (`glow: 1`) so bloom reads. Use `k.pool` for crisp-edged pools on the floor. A night scene with fewer than ten lights looks flat.

**Weather and air.** Use `k.particles` for anything small that drifts: snow (`fall: 2, sway: 2`), rain on a non-rain look, embers and sparks (`fall: -3, glow: true`), petals, dust, bubbles, confetti. Particles are drawn after the inked picture, so they never get outlines. Two layers (many small and slow, a few large and fast) read as depth. For snow on the ground, set `tune: { wet: 0 }` so night and rain looks do not make it shine like a wet street.

**Sky, mountains and the far camera.** The flat poster is shot from kilometres away, so the poster's height in metres (`flatWidth / aspect`) is the whole world: a mountain, tower or skyline must fit inside it to be seen in the poster. The sky is painted by the engine; never close the scene in a dome or a box, or the far camera sees only its inside. The flat camera looks level at the horizon, so the painted sky in the poster is only its horizon colour, with no stars or moon. When the poster needs a sky (stars, a moon, a sunset, distant ranges), paint it as a backdrop: a large `k.svg` picture with `screen: true` on a box far behind everything, sized to fill the poster above the skyline, and marked `userData.ignoreBounds = true` so it does not count as scene. Build mountains as real shapes (`k.loft`, `k.mesh` with a terrain geometry) in front of the painted sky. The "camera inside an object" check uses each object's bounding box, so split large terrain into patches rather than one huge mesh, or a camera flying over a hill counts as inside it.

**Motion blur.** Fast whips blur like a film camera with a 180 degree shutter, capped so the fastest moment still reads. Set `motionBlur: 0.5` on the scene for crisper motion or `0` for none; 1 is the default and 2 the most.

**Crowds.** Stage people the way a real place moves: people crossing in every direction including diagonals, groups waiting at the edges facing the way they will go, a few standing at doors and shop windows, more where light and attractions are. Mix clothes and umbrellas; `k.person` already varies coats, skirts, hair, caps and bags.

**Camera for a place.** Write your own path when the preset ones do not fit (see SCENES.md). Strong beats: the poster; a dive at eye level that skims over heads (keep the camera at least 1 m above any crowd); a three-quarter high view of the main open space (pitch 25 to 35 degrees with a 50 to 65 degree lens; the camera stays level and pitch is a lens shift, so higher pitches already look almost straight down, which reads flat and fails the depth check); a low wide view up at the hero building (look up with `horizon` about -0.9 and a wide lens; never use a negative `pitch`, which puts the travelling camera under the ground); a pull back to the poster. Whip between views in 0.6 to 1.2 seconds and hold each for 0.7 to 1 second with a small drift.

**Swaps.** Objects given to `k.swap` change depth only while the view is flat, which is the surprise of the form. A swap pays off only if the path returns to the poster in the middle of the film: go flat, switch to a shot with `swap: 1` (built-in `flatAlt`), keep `swap: 1` on the shots that follow, and switch back to `swap: 0` on a flat beat at the end. A path with one flat stretch has no room for a swap; leave swaps out, and the warning is expected.

**Traps the checks will catch.**
- `k.animate` must be given every object it changes. Anything else is merged into still geometry and frozen; two pictures swapped by hiding one will both show and flicker.
- Anything that switches in steps (a screen changing picture, a light changing colour) must switch half a step away from the loop point, e.g. `Math.floor(phase * 4 + 0.5) % 2`.
- `screen: true` is for self-lit pictures inside the scene; `poster: true` is only for a picture that is itself the poster and fills the flat frame.

## What makes a film worth watching

- **Something moves in every second.** The camera, the subject, or both. Plan what the subject *does* while the camera travels: parts lift apart, doors open, lights come on, captions draw in, things rise and settle. Use `k.move`, `k.float`, `k.label` and `k.animate`.
- **Model real shapes.** Use `k.loft`, `k.lathe` and `k.tube` for anything with curves. A product made of boxes looks like packaging.
- **Design the poster first.** The flat frame is the thumbnail and the first second. Big words, one subject, edge-to-edge colour.
- **Reward the high angle.** The floor is invisible in the flat frame. Put rings, graphics and pools of coloured light on it, so there is a second image waiting when the camera rises.
- **Give the room depth.** Sparks, light columns or far buildings slide past as the camera moves, and that sliding is what reads as 3D.
- **Six to ten colours and one accent.**

## Checks

Every preview and render confirms the poster reads as flat and fills the frame, each move opens real depth, the camera never passes through anything, the film returns exactly to its start, and the video has no freezes, pops, flicker or visible loop seam. `SCENES.md` lists the fix for each failure. Report honestly: quote any check that failed.

Exit codes: 0 ok, 1 checks failed, 2 bad command, 3 machine not ready, 4 scene error.

## Also

If the user hands you a picture and wants that exact picture to move, there is a `film <picture>` command. Read `PICTURES.md`.

## Rights and honesty

Build original places, characters, products and brand names. Use a real brand's name, logo or slogan only if it is the user's own or they asked for it for their own use, and label speculative brand work as a concept. Never copy an existing artwork or imitate a named artist.
