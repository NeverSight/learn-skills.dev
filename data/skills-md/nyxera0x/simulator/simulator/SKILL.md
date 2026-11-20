---
name: simulator
description: Rebuild any industry as a live simulator in the format of a reference video that already worked. A bright toy-scale isometric map of the whole operation (an airport, a port, a warehouse, a factory) where every vehicle works on one clock and one item is followed through the system, a product UI matched panel by panel to the reference, one camera that only pans and zooms like a user with a mouse, selected vehicles outlined with their route drawn on the ground; then a collision sweep and a frame-by-frame 60 fps film with a synced score. Use when someone asks for a "simulator", a "digital twin", a "living map", an "operations app video", a "how an airport / port / warehouse works" film, or wants to copy the format of a simulator video they liked.
---

# Simulator

One system, one page, one film, built against a reference. Don't invent a look: take a video that already worked
apart, write its rules down, and rebuild your system to those rules. Every model is code; no 3D file, no download.

`SKILL_DIR` is the folder this file lives in. Builds and renders go to `./simulator-out` of the folder you run from.

## First run

```
cd "$SKILL_DIR" && npm install && npx playwright install chromium
```

The video needs `ffmpeg` on PATH and the sound needs Python 3 (standard library; `requests` only for ElevenLabs).
Set `FFMPEG`, `PYTHON` or `CHROMIUM` to use other binaries.

## The example: Rampline, a toy airport

`sims/airport-*`. Pier B with 3 stands, Cargo C (a warehouse with 6 docks), a hangar, the service road and the
taxilane, a city behind the fence. The hero is one container, AKE 48211 AU: the high loader lowers it out of the hold
onto a tug's third dolly, the tug tows it to Cargo C, a forklift carries it into dock D3. Around it a truck backs into
D6, a jet is pushed back and taxis out, a catering truck lifts its box to a door. The film runs 50 s.

| File | Job |
|---|---|
| `airport-shared/style.js` | The palette sampled from the reference, shared materials, rounded boxes, the stage's grade. |
| `airport-shared/airside.js` | Jet, terminal pier, jet bridge, cargo terminal, tower, hangar, lights, trees, fences, city blocks. Built by subagent A. |
| `airport-shared/gse.js` | 15 ground vehicles from a tug to a forklift. Built by subagent B. |
| `airport-shared/world.js` | The layout, the timetable `T`, every path, `pose(t)`, the bodies for the collision check. |
| `airport-shared/ui.js` | The product UI, matched over a reference frame. `update(state)` fills it. |
| `airport-shared/select.js` | Selection marks: a wireframe box, a ground glow, a route ribbon. |
| `airport-shared/thumbs.js` | Card thumbnails rendered from the models. |
| `airport-shared/film.js` | The camera keys, the clicks, the dropdown, every card. |
| `airport-shared/score.py` | Action sounds on the timetable. |
| `airport-film/` | The film's entry. `airport-collide/`: the collision sweep. `airport-look/`: a free camera for checks. |
| `docs/BRIEF.md` | The brief the 2 subagents worked from, as a template. |

```
node "$SKILL_DIR/sims/build.mjs" airport-film      # → simulator-out/dist/airport-film.html, offline
```

## Three more systems on the same kit

Each one reuses the airport's look, stage, UI, selection marks and thumbnails, and adds its own models, world, film
and score. Copy the one closest to your system.

| System | Folder | Story | Length |
|---|---|---|---|
| **Plantline**, a car plant | `plant-shared/`, `plant-film/`, `plant-collide/` | `line.js` (robot arm with analytic IK and 4 tools, a car body that builds, paints and gets its wheels, skid, conveyor, press, paint booth, rolling road) and `plant.js` (open-top hall, AGVs, parts racks, car carrier, cell fences). One body from cell C4 to the carrier. `runToyPlantFilm({look: 'claude'})` gives the clay version. | 50 s |
| **Buildline**, a construction site | `site-shared/`, `site-film/`, `site-collide/` | `machines.js` (excavator with `reach()`, tipper, mixer with a swinging chute and a pour stream, dozer, loader, roller, flatbed) and `site.js` (a pit heightfield that digs itself as a function of k, rebar, formwork, a slab that spreads from the chute, blockwork, batching plant). One mixer from the plant to the pour. Nothing above 9 m. | 43.7 s |
| **Stockline**, a warehouse network | `warehouse-shared/`, `warehouse-film/`, `warehouse-collide/` | Built from the airport kit alone: three cargo terminals named per site, trucks reversing into docks, forklifts on keyed routes between the trucks and the staging rows, chargers. The detail card shows a depot's stat grid, inventory and forklift fleet. | 39.4 s |

Give every system its own length (somewhere in 38-52 s, never a round number) and uneven gaps between the clicks, so
a series never reads as one template.

**Keep everything low.** A camera at 36 degrees over tall frames (quay cranes, gantries, portals, tower cranes) sees
the frames, not the work. Choose systems whose action happens on the ground, or keep the one tall thing to the side.

## Building a new system

1. **Take the reference apart.** Frames every 3 s at full size, a contact sheet. Write down the camera (does it cut,
   its angle, how it travels), sample the colours with ffmpeg (`crop` 6x6 at a point, `scale=1:1`, `rawvideo rgb24`),
   list the UI panels with positions and sizes as a share of the frame, list what a selected object gets. Rules only,
   no opinions.
2. **Write the brief** from `docs/BRIEF.md`: the frames, the palette in `style.js`, a scale contract both kits meet
   (door sills, deck heights), the split between 2 subagents. One of them starts by matching the reference's own
   vehicle side by side.
3. **Fix the light.** `createToyStage` uses Neutral tone mapping: ACES greys pale grounds out. Sample the ground in a
   still and compare it to the reference's hex.
4. **Match the UI over a frame.** Put a reference frame under the HTML at 50% opacity and match every panel. Use your
   own words. Watch for class names that clash with `sims/kit/style.css` (`.prog` is taken).
5. **Write the day as a function of time** in `world.js`: one hero item's timetable, every vehicle on a path by arc
   length (`CatmullRomCurve3`, centripetal), trains as cars at fixed distances behind the leader on the same path,
   anything carried placed from scratch every frame.
6. **Direct it like a user.** One azimuth and elevation for the whole film; keys of `{t, x, z, d}` with eased glides
   and a zoom-out arc on long moves; the camera can ride a moving vehicle. Clicks switch the detail card; the selected
   vehicle gets the box, the glow, its route. Site changes go through the switcher's dropdown.
7. **Sweep for collisions** with `airport-collide`: every 0.1 s, oriented boxes from each body's own geometry, jets
   as fuselages, trees as points, trucks against building walls. List the pairs that are meant to touch. Wings are not
   in the sweep: check vehicles under a wing on a close-up still from `airport-look`.
8. **Score it and render it.**

## render(t) contract

- `render(t)` is a pure function of time. Render any second out of order and it looks the same. No physics, no random
  timers, no state carried between frames.
- Vehicles move by distance along their paths, eased at the ends. A reversing vehicle faces against its tangent.
- Carrying is rebuilt every frame: the item's position comes from whatever holds it right now.
- Background vehicles run on the same clock, never on their own timers.

## Review

- Contact sheets at the beats: `node sims/capture.mjs airport-film --stills 0,3,9,15,20,30,40,48 --cols 4 --out s.png`.
- The first frame decides the feed: one whole scene at medium distance, the UI fully drawn, pins, something moving.
- Run the collision sweep after every path change.

## Sound and render

```
node sims/capture.mjs airport-film --size 1600x900 --dpr 1.2 --out simulator-out/airport-film.mp4
python run_sfx.py sims/airport-shared/score.py --out simulator-out/fx.wav               # the action sounds alone, to check
python tools/sfx_fetch.py "airport ambience" --n 4 --max-dur 60                           # real CC0 recordings, with credits
python tools/music.py --film simulator-out/airport-film.mp4 --score sims/airport-shared/score.py     --plan docs/music_plan.json --ambience simulator-out/sfx/<the file you picked>.wav --out simulator-out/airport-final.mp4
```

`docs/music_plan.json` is the ElevenLabs composition plan the airport used: 6 sections cut to the film's beats. With no
`ELEVENLABS_API_KEY` the mix carries the action sounds and the ambience only.

Master to -14 LUFS. Check the music for gaps with `silencedetect` before mixing.
