---
name: roblox-animation
description: Author Roblox character animations (R15 or R6) headlessly in Blender from a JSON pose spec, verify them by rendering contact sheets and GIFs and match a reference pose. Use this whenever the user wants to make, generate, or automate a Roblox animation — a punch, swing, emote, idle, walk, death, tool action — or wants an animation built to match a reference pose, or asks to animate a .blend rig without opening Blender's UI. Also trigger when a Roblox animation "comes apart", limbs detach, a rig poses correctly in script but renders wrong, limbs pop or flip between frames, or a pose looks nothing like the reference.
---

# Roblox animation, headless

> **First time on this machine?** Read `LOCAL.md` in this folder. If it does not exist, run the
> `roblox-skills-setup` skill (or copy `LOCAL.template.md` to `LOCAL.md` and fill it in).
> `LOCAL.md` holds your paths and tool locations; it is yours and is never shared.

Author animation as **data** (a JSON spec of poses over time), bake it into a real
Blender Action, render it, and **look at the result** before believing it.

The loop is: **author → render every frame → tile into a contact sheet → look →
correct → repeat.** Everything here exists because some step of that loop caught a
failure that every other check missed.

## Read this first: the trap that wastes the most time

**Most Roblox rigs ship a Blender Action holding their rest pose.** Blender
**re-evaluates that Action during render**. So if you set pose values and then
render:

- every numeric probe reports your pose applied perfectly
- every rendered frame shows the rig's default pose
- the data and the image never reconcile, and there is no error

Clearing the Action does not help either, because **that Action IS the rest pose** —
clear it and the limbs collapse into the torso.

**The fix: insert KEYFRAMES into that same Action**, then `frame_set()` per frame
and render. The animation then *is* the Action, nothing can overwrite it, untouched
bones hold their rest values by constant extrapolation, and you end up with a real
Action — which is what a Roblox export needs anyway. `scripts/anim_render.py`
already does this.

Full list in `references/traps.md` — 28 of them. Read it before debugging anything.

## Author in FK. Not IK.

A Roblox `KeyframeSequence` is **a tree of per-joint rotations**, one per Motor6D.
That is FK. Every R15 rig ships one control bone per joint to match. Drive the
character with IK targets and you are round-tripping through a solver Roblox never
asked for, and paying for it:

- **position-only IK targets leave limb ROLL free**, so blocky Roblox parts present
  whatever face the solver picks and snap between frames. On a textured avatar that
  reads as **colours changing instantly** — the symptom that makes an animation look
  buggy
- **the solver hops between equally-good branches** frame to frame, so limbs pop
  while every frame still verifies perfectly
- it is slow

FK has no branches, no singularities, no roll ambiguity, is exactly 1:1 in degrees,
and exports straight to Roblox.

**Most rigs ship in IK mode**, which makes every `FK_*` bone read as inert. Flip the
switch — do not conclude FK is dead:

```json
"properties": {"ARM_IK_FK.L": 0.0, "ARM_IK_FK.R": 0.0,
               "LEG_IK_FK.L": 0.0, "LEG_IK_FK.R": 0.0}
```

Measured on a free community R15 rig, and pleasantly uniform: every limb rests pointing
straight **down**; on every `FK_*` bone **X negative swings forward, Z positive
swings to the character's right**, 1:1 in degrees, **identical on both sides** — no
mirror inversion. Child angles are relative to the parent.

The general lesson, whatever rig you use: **if a control bone is inert, look for a
switch that disables it before writing it off.** Rigify-style R15 rigs carry
`ARM_IK_FK` / `LEG_IK_FK` custom properties that default to `1.0` (IK). Set them to
`0.0`, key them (so `frame_set` cannot flip them back), and author in FK. The
direction conventions above were measured on one rig; `calibrate_rig.py` and
`sweep_control.py` re-measure them on yours, so run them on any rig you have not used.
Your rig's `.blend` path goes in `LOCAL.md`.

Reach for IK only when a limb must hit an exact world point. Then read traps 12–15.

## Make it look like Roblox, not like the reference

- **30 FPS**, and a combat move runs **0.3–0.7s**. The Animation Editor's default is
  30fps. Real-life timing is far too slow for a game. Take
  the **mechanics** from how the move really works; take the **timing** from Roblox.
- **Five poses**: idle, anticipation, contact, follow-through, recovery.
- **Ease per segment** — `"ease": "in"` to accelerate into the strike, `"out"` to
  settle. A fixed smoothstep decelerates into every keyframe, so the strike eases to
  a stop at its own contact frame and the whole thing reads mushy.
- **Exaggerate.** Real Roblox combat animation goes well past human range and reads
  off the silhouette.
- **Render plain grey** (`"plain": true`). A busy avatar texture turns a blocky rig
  into an unreadable jumble and you end up debugging the costume instead of the pose.
  Real Roblox animations are showcased on a plain dummy for exactly this reason.

**`references/pose-recipes.md` has the actual numbers** — measured angle tables for
guard, anticipation, chamber, contact and follow-through, the timing skeleton, and
the two rules that catch people out (shoulder + elbow must stay under ~120 total;
a high kick needs `UpperLeg X` past −120 or the leg merges with the torso). Start
from those and adjust against the preview. Do not re-derive them.

## Be fast — measured, not guessed

The whole loop is **seconds**. If a pass takes minutes, something is wrong.
Measured on a mid-range PC, one animation of 24–36 frames:

| stage | time | notes |
|---|---|---|
| Blender loads the rig | **0.7s** | startup is never the problem |
| numeric probe (whole FK control map) | **0.1s** | ask the rig questions with numbers |
| preview render (`"preview": true`) | **4–6.5s** | 1 view, 320x240, 1 sample |
| full render, 2 views @ 640x560 | **9–17s** | do this once, at the end |
| GIF encode | **0.3s** | |
| `to_roblox.py` → Luau | **0.1s** | |
| build + verify in Studio | **one `execute_luau` call** | |

**Machine time for a finished, in-Studio animation: well under a minute.** What
actually costs time is *authoring iterations*, so spend them on the preview and
never on the full render. With `references/pose-recipes.md` to start from, a
second move should land in 1–3 previews — the punch in `references/` was right on
the **first** try. The wave example was NOT: it passed every number and still read as a
hand on the head, and it took a human eye to say so (fixed 2026-10-23). Numbers prove the
pose matches the spec; only looking proves the spec is the right move.

`"report": true` prints every joint's position at each beat: when a pose looks
wrong it names the joint in one run instead of five render passes of guessing.

**Do not render to answer a question a probe can answer.**

## Non-negotiables

Each is here because skipping it shipped something broken that looked fine:

1. **Never trust a run that exited 0.** `anim_render.py` asserts rig integrity per
   frame, asserts the frames were written, and hard-exits non-zero otherwise.
2. **Look at the frames.** Every pass.
3. **With a reference, build the side-by-side and judge on that** — never on the
   render alone.
4. **Inspect the finished GIF itself**, not the PNGs you encoded it from.
5. **Never relax a tolerance to turn a red light green.** Fix the spec.

## Workflow

### 1. Calibrate the rig (any rig you have not used)

```bash
blender --background <rig>.blend --enable-autoexec --python scripts/calibrate_rig.py
blender --background <rig>.blend --enable-autoexec --python scripts/sweep_control.py -- FK_UpperLeg.R:rot TORSO:rot
```

`calibrate_rig.py` reports the deform vs control armature, the Action trap, the
**IK/FK switch state**, and which controls actually move something.
`sweep_control.py` gives each axis's direction, sign and usable range — it measures
bone *direction* as well as position, so rotation-only controls are not missed.

If the `FK_*` bones read inert, that is the IK/FK switch, not a dead rig.

### 2. Author the spec

`fps`, `duration`, `w`, `h`, `margin`, `views`, `properties`, `plain`, `preview`,
`report`, and `keyframes[]` of `{t, ease, bones: {Bone: {rot|loc|target|aim}}}`.

`rot` is what you want almost always. `loc` for controls with no end effector
(`ROOT`). `target` / `aim` are the IK escape hatch — see traps 12–15.

Three things that go wrong every time if you forget them:

- **FK child angles compound with the parent.** Shoulder 50° + elbow 70° puts the
  forearm 120° from vertical, pointing up over the shoulder. Keep shoulder + elbow
  under ~110° for a guard.
- **Lean and twist go on `UpTorso`**, which drives only the upper body. `TORSO`
  drives the legs too, so leaning it tips the figure over and slides the planted
  foot. The rig also *amplifies*: `X = +15` swings the head 23°.
- **Counter-rotate the support ankle**, `FK_Foot.X ≈ -(FK_UpperLeg.X +
  FK_LowerLeg.X)`, or the foot tilts with the leg and the character looks like it is
  standing on a slope.

See `references/example-fk-roundhouse.json` (0.8s kick) and
`references/example-fk-punch.json` (0.5s cross), plus `references/pose-recipes.md`.

### 2a. IF A PROP IS IN THE HAND, RESEARCH HOW IT IS REALLY HELD. FIRST.

**This step happens BEFORE you author a keyframe, and it is not optional.** The
moment a clip has a weapon or a tool in it, "does the pose read" stops being a
question about the rig and becomes a question about that object, which is a fact
about the world and not something to infer from a matrix.

The failure this exists to prevent, from a real build: a glaive was authored with
its head DOWN at the wielder's hip. Every downstream stage then did its job
perfectly - the engine reproduced the authored grip, the pose strip matched the
contact sheet frame for frame, grip error 0.000, zero samples of the weapon
inside the body - and the game shipped a polearm carried upside down. **A wrong
pose authored here is invisible to every check after it, because every check
after it is measuring agreement with THIS.** When a human finally
looked, the verdict was that it was upside down. They were right, and the cost was
an entire session downstream of a decision made in ten seconds here.

Before authoring:

1. **Search for how the weapon class is carried and used.** Photographs of
   practitioners, not concept art, not other games. Ten seconds of reading beats
   four rounds of guessing at numbers.
2. **Write the answer into the spec as `_intent`,** as a sentence about the
   weapon: "head up, shaft crossing the lead shoulder", "blade angled up and
   forward from a lowered hand". That sentence is what the contact sheet gets
   judged against - see step 3.
3. **Sanity-check the obvious ones from the list below** before reaching for a
   search.

| class | at rest | in a swing |
|---|---|---|
| polearm, glaive, naginata, spear | **head UP** - shouldered, planted butt-to-ground, or at a guard with the blade at chest height or above. Never hanging at the feet | the head leads the arc; the shaft crosses in front of the body, never in the same vertical plane as the arm |
| sword | angled up and forward from a **lowered** hand, around +35 degrees. Straight down reads as dropped | edge leads; the wrist is not a hinge, the whole arm carries the arc |
| axe, hammer | head up or shouldered, the weight carried high | the head is the mass - it arrives last and it arrives hardest |
| fist weapon, gauntlet | worn, not gripped; a brawler's guard, both fists up | the hips drive it, not the shoulder |

**Hold the prop in a pose the wearer's own body could get into.** A one-handed
carry of anything longer than the character is tall does not sit in the same
plane as the arm, or it clips.

### 3. Render and verify

```bash
blender --background <rig>.blend --enable-autoexec --python scripts/anim_render.py -- spec.json out/
ffmpeg -start_number 0 -i "out/side_%03d.png" -vf "scale=240:-1,tile=6x6" sheet.png
```

The camera frames itself on the **whole animation's** bounds and solves its distance
from the field of view, so nothing leaves frame; `margin` (default 1.10) is the only
knob. Render **at least two angles** — a right-leg kick is invisible from the left.

**Then judge the sheet against the REFERENCE, not against itself.** Open the
`_intent` sentence from step 2a and check the sheet frame by frame against it:
is the head up, is the blade leading, does the shaft cross in front of the body.
A contact sheet only ever proves that the render matches the spec. It cannot tell
you the spec was right, and every stage downstream will treat it as ground truth
- so this is the last point in the pipeline where a wrong pose is cheap to fix.
If the sheet and the reference disagree, the reference wins and the spec changes.

### 4. Deliver a GIF, then check the GIF

```bash
ffmpeg -framerate 30 -start_number 0 -i "out/side_%03d.png" -framerate 30 -start_number 0 -i "out/tq_%03d.png" -filter_complex "[0]scale=420:-1[a];[1]scale=420:-1[b];[a][b]hstack=2,split[s0][s1];[s0]palettegen=stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=3" -loop 0 anim.gif
```

**Read the sheet ONCE, at the size you need and no larger.** A contact sheet is
the most expensive object in this pipeline: an image is re-sent on every later
tool call in the same context, so a full-resolution sheet read early costs
hundreds of thousands of tokens by the end of a run. Tile it down, crop to the
limb in question when that is the question, and do not re-open it to re-check
something you could have measured. Where a check can be a NUMBER - does the
weapon leave the hand, does it pass through a limb, what angle does it sit at -
make it a number and read one line of text instead.

Then pull frames back out of the finished GIF and look at them — motion reads
differently from stills, and encode settings fail silently:

```bash
ffmpeg -i anim.gif -vf "select='not(mod(n,2))',tile=4x3" -vsync 0 verify.png
```

## An authored clip breaks the ones you did not author

Roblox's default `Animate` script plays idle, walk, run, jump, fall and climb at
**Core** priority. Anything you author and play at `Idle` or above **masks them
on every joint it poses**, for as long as it is playing.

So a full-body idle loop - the correct fix for a character standing there with a
weapon - stops the legs from moving when the player walks, because your clip is
posing the legs at a higher priority than the walk cycle. It looks exactly like
"the walk animation is missing", and it appears only on the character you
authored the idle for, which makes it read as a problem with that character's
weapon.

**Pick one and say which:**

- author the idle at **`Core`** priority, so the default walk still wins; or
- **do not pose the legs** in it - author only the arms and torso and let the
  default locomotion drive everything below the hips; or
- **author the locomotion set too** (walk and run at `Movement`), which is the
  only option if the carry pose has to change how the character walks.

**And check it, per character, in a playtest:** stand still, walk, run, jump,
land. Watch the LEGS. This costs about fifteen seconds per fighter and there is
no static check that can see it - the clip is correct, the rig is correct, and
the defect only exists while two clips are playing at once.

## R15 vs R6

**Prefer R15.** R15 has elbows and knees, so it has a joint for every angle a
reference shows, and FK maps one control bone to each.

**A custom-mesh R6 rig with no .blend** (rigid GLB parts + probed Motor6D C0/C1): author in
joint space with `scripts/r6_clip.py` (renders the real parts through the exact Motor6D chain,
grounds the root per key, reports foot y / stance slip / limb overlaps) and emit Luau with
`scripts/r6_luau.py` (verbatim Pose CFrames, R15 specs too, one replaced-wholesale folder).
Conversion lives in `scripts/r6_joint.py`. See traps 39-40.
A **standard R6 avatar** works the same way (proven 2026-10-22): probe the six Motor6Ds of a
`CreateHumanoidModelFromDescription(desc, Enum.HumanoidRigType.R6)` dummy (they exist in edit
mode), build box GLBs at the real part sizes at the chain's rest centres, and write rig.json;
the clip played in Studio matched the render at the contact key to 0.00002 studs.

R6 limbs are **rigid single blocks with no elbow**. A folded boxing guard is not a
pose R6 can hold at all; asking for it raises the whole arm. Use R6 only when the
game requires it, and expect stiff pose-to-pose motion — which is R6's native look,
not a defect.

## Getting it into Roblox — the full pipeline

Verified end to end, and it needs **no upload**.

```bash
# 1. author + preview until it reads right   ("preview": true)
blender --background <rig>.blend --enable-autoexec --python scripts/anim_render.py -- spec.json out/

# 2. generate the Studio builder for one or many specs
python scripts/to_roblox.py kick.json punch.json wave.json > build.lua
```

2b. **Prove the export before Studio:** `blender --background <rig>.blend --enable-autoexec --python scripts/rbx_axis_check.py -- spec.json --mid`.
   It compares every keyed part's full rotation between the render and the Roblox CFrame chain (traps 35-37).
   `to_roblox.py --folder ReplicatedStorage.X.Y --no-verify` emits a yield-free builder that returns a summary; spec `markers` become KeyframeMarkers.

3. Paste `build.lua` into `execute_luau`. It creates
   `ReplicatedStorage.CustomAnims` with one `KeyframeSequence` per spec, replacing
   any of the same name, then **verifies each one loads at its authored duration**
   and prints a report. Anything other than the durations you authored is a
   failure — do not move on.

4. Copy `references/studio-binder.lua` into a LocalScript under
   `StarterPlayer.StarterPlayerScripts`, edit its `BINDS` table, and you have
   key-triggered animations on the player's character (with respawn handling) and
   optionally mirrored onto a dummy.

Spec fields the exporter reads: `rbx_name` (Studio name), `priority` (default
`Action`, which overrides the stock walk/idle), `loop`.

**No upload:** `KeyframeSequenceProvider:RegisterKeyframeSequence(seq)` returns a
ContentId you assign straight to `Animation.AnimationId`. It needs only the
Animation capability, so a LocalScript can call it at runtime — no asset upload,
no moderation, no account. Only the **bare** string works (`hash://` and
`rbxasset://` both fail). Those ids are **session-local**: fine for testing, but
publishing needs real uploaded asset IDs. **`scripts/upload_animation.py` does that
headless** (2026-10-08): dump the KeyframeSequences from Studio, rebuild each as a
real .rbxm with Rojo, upload as Open Cloud assetType `Animation`, poll, and emit
`apply_ids.luau`, which sets an `AnimationId` attribute on each sequence. Verified
lossless (80/80 poses + markers) and playable on a character, with no
right-click "Save to Roblox" by hand.

Things that will catch you (details in traps 29–34):

- Modern rigs may carry **`AnimationConstraint`**, not `Motor6D` — 15 of them and
  zero Motor6D. Animations still bind by part name and play unchanged.
- `Enum.PoseEasingStyle` has **no `Quad`** — Linear/Constant/Cubic/Elastic/Bounce.
- You **cannot** preview a pose by writing `.Transform` in edit mode; that is the
  animation channel and only the Animator applies it. Verify the axis map by
  forward kinematics through the attachments instead.
- Studio tooling has blind spots: `capture_screenshot` fails while a script tab is
  showing rather than the 3D viewport, and play-mode output may be unreachable —
  so make the runtime script **diagnose itself on screen**, as the binder does.

Coordinate systems differ: **Roblox is +Y up / −Z forward, Blender is +Z up / −Y
forward.**

## Free library fallback

If authoring is not converging, the Creator Store carries free R15 animations and
`search_asset` finds them — free, pre-licensed, no quota, no upload, no moderation,
and already an Animation asset ID. Under an unattended-agent rule, an agent
searching and selecting is not a human intervention.
