---
name: roblox-sfx
description: Source, verify and wire the sound for a Roblox game from the Creator Store by asset id - footsteps, gunshots, animal calls, UI clicks, ambience, music - with no upload, no Open Cloud audio quota and no API key. Searches the same unauthenticated toolbox endpoints Studio's own audio tab uses, then PROVES each candidate in Studio (IsLoaded plus a measured Sound.TimeLength) before anything is chosen, because the toolbox's own duration field is wrong often enough to be dangerous. Emits a SoundBank data module, an Sfx runtime helper that fails inert, and an install script so the bank can be heard in an open place immediately. Use whenever the user wants sound effects, audio, SFX, music or ambience for a Roblox game, wants sounds found and wired rather than dragged in by hand, is picking audio for a build, or asks why a Sound is silent, has no length, or will not load in their place.
---

# Roblox sound, by id, verified

> **First time on this machine?** Read `LOCAL.md` in this folder. If it does not exist, run the
> `roblox-skills-setup` skill (or copy `LOCAL.template.md` to `LOCAL.md` and fill it in).
> `LOCAL.md` holds your paths and tool locations; it is yours and is never shared.

The whole skill rests on one fact, measured not assumed:

> **A free Creator Store audio asset plays in an unpublished, unsaved place, with
> no API key, no ownership and no upload.**

So sound does not need the Open Cloud audio quota (10 uploads/month unverified,
100 ID-verified, create-only, so every regeneration burns a slot). It needs a
search and a check. That takes the audio stage off the critical path entirely.

```
spec.json  (roles: what the game needs a sound FOR)
  -> find_sfx.py     unauthenticated toolbox search -> candidates.json
  -> emit_probe.py   probe.lua + report.lua
  -> Studio          create the Sounds, then MEASURE them   <- the gate
  -> pick.py         three gates, then score -> manifest.json
  -> emit_bank.py    SoundBank.luau + Sfx.luau + install.lua + tour.lua
```

Search produces **candidates**. Studio produces **facts**. Only facts choose.

---

## What was measured, and when

Verified live against Studio on 2026-08-30 in an unsaved `Place1`
(`placeId 0`) with the third-party `robloxstudio-mcp` connected:

| Question | Answer |
|---|---|
| Does `toolbox-service/v1/marketplace/3` need auth? | **No.** 200, 1000 results for `footstep` |
| Does `items/details` need auth? | **No.** Full metadata including `audioType`, artist, votes, `isFree` |
| Can you download the audio file to analyse it? | **No.** `assetdelivery` v1 and v2 both 401 |
| Does an unowned free audio id load in an unpublished place? | **Yes.** 40 of 40 candidates `IsLoaded = true` |
| Does `Sound:Play()` work in edit mode? | **Yes**, audible in Studio, no playtest needed |
| Is the toolbox `duration` field trustworthy? | **No.** A real 0.500s sound is listed as `0`; 2 of 8 shipped picks had a listing that disagreed with the measurement |

The fourth row is why selection cannot be clever. There is no waveform to
analyse, no spectrogram to look at, nothing to judge by ear from here. What
exists is a listing and a measurement, and the skill is honest about using only
those.

---

## The rule that shapes everything

**A listing is a claim. `Sound.TimeLength` is a measurement. Never gate on a claim.**

`find_sfx.py` deliberately stores the listing's duration under the name
`listed_duration` so that nothing downstream can mistake it for data, and
`pick.py` records `listing_was_wrong` on any pick where the two disagreed by
more than 25%. On the first real run that fired on 2 of 8.

---

## Two Studio calls, never one

`execute_luau` drops all output if the script yields at all, and a Sound does not
resolve its length in the frame you set `SoundId`. So the probe is split:

```
call 1   probe.lua    creates every candidate Sound, returns immediately
         (a beat)
call 2   report.lua   returns role,id,loaded,length as CSV
```

If anything is still `loaded=false` in call 2, run `report.lua` **once more**
before believing it. Only a second failure is a real one, and a real one means
an unresolvable id, a deleted asset, or audio this place is not permitted to use.

---

## The three gates

A candidate is only eligible once Studio says all three, in order:

1. **`IsLoaded == true`** — the id resolves and the place may use it
2. **`TimeLength > 0`** — a zero-length sound is broken, not short
3. **`min_len <= TimeLength <= max_len`** — the role's band

Search score breaks ties, and only ties. A top-ranked listing that fails a gate
always loses to a bottom-ranked one that passes. On the first run this rejected
a 6.55s "wooden gate open" from a role whose band ended at 5s.

**An unfilled role is a failure, not a warning.** `emit_bank.py` refuses to emit
a bank with holes; overriding needs an explicit `--allow-holes`, which means
deliberately shipping a silent event.

---

## Writing a spec

One entry per thing the game needs a sound **for**, never per sound you imagine.

```json
{
 "name": "farm",
 "roles": [
  { "name": "sheep_bleat", "query": "sheep bleat", "kind": "SoundEffect",
    "min_len": 0.3, "max_len": 4.0, "volume": 0.5 },
  { "name": "ambience",    "query": "countryside ambience", "kind": "Music",
    "min_len": 20, "max_len": 300, "volume": 0.2, "looped": true }
 ]
}
```

- `kind` is `SoundEffect` or `Music`. It is a real field on the asset and a
  mismatch is scored down hard, because a Music track answering a `SoundEffect`
  role is the classic way a nine-minute remix ends up as a footstep.
- The band is the design decision. A footstep over 1.5s is not a footstep, and
  writing that down is what lets the machine reject without hearing anything.
- `volume` and `looped` travel through to the emitted bank.

An example spec is in `examples/spec.example.json`; copy it and edit the roles.

---

## Run it

```bash
cd ~/.claude/skills/roblox-sfx
python scripts/find_sfx.py spec examples/spec.example.json --out work/candidates.json --per-role 5
python scripts/emit_probe.py work/candidates.json --out work
# execute_luau work/probe.lua      -> "created N sounds across M roles"
# execute_luau work/report.lua     -> save the return value verbatim to work/report.txt
python scripts/pick.py work/candidates.json work/report.txt --out work/manifest.json
python scripts/emit_bank.py work/manifest.json --out work
# execute_luau work/install.lua    -> SoundService.SFX, audible in this place
# execute_luau work/tour.lua       -> plays the whole bank in order, so a human can judge it
```

A one-off lookup, no spec needed:

```bash
python scripts/find_sfx.py search --query "wolf howl" --kind SoundEffect --limit 20
```

---

## What ships

| File | Goes to | What it is |
|---|---|---|
| `SoundBank.luau` | `src/shared/Config/` | Data only: role -> id, measured length, volume, looped, credit |
| `Sfx.luau` | `src/shared/` | `Sfx.play(role, parent, pitchVary)`, `Sfx.preload()`, `Sfx.stop()` |
| `install.lua` | `execute_luau` | Builds `SoundService.SFX` directly, for a place with no Rojo sync |
| `tour.lua` | `execute_luau` | Plays every sound in order, spaced by its real length |

Two rules the emitted code keeps:

- **Nothing outside the bank ever names an asset id.** Gameplay code says
  `Sfx.play("wolf_howl", head)`. Retuning volume or swapping an asset is a data
  edit, never a code edit.
- **Sound can never break gameplay.** Every entry point in `Sfx.luau` is
  pcall-isolated and returns nil on failure. A missing sound must not stop a shot
  from firing or a sheep from moving.

`tour.lua` schedules with `task.delay` rather than looping with `task.wait`, for
the same reason the probe is split in two: a yielding script loses its output.

---

## Traps

**The listing duration is wrong.** Covered above. It is the single most likely
thing to make this pipeline ship a bad sound if someone "optimises" the Studio
round trip away.

**`search_assets` on the MCP is a dead end.** It returns HTTP 403 `Scope not
authorized`, and no renaming of parameters fixes it. That is why this skill goes
straight to the toolbox endpoints, which need no auth at all.

**You cannot hear anything, and neither can the model.** `assetdelivery` is 401
without a cookie, so there is no waveform, no spectrogram, no loudness figure.
Everything this skill claims about a sound comes from the listing or from
`TimeLength`. When taste matters, run `tour.lua` and let a human judge. For an
unattended run, the gates plus the score are the honest ceiling, and that is a
finding worth saying out loud rather than papering over.

**Free packs are not the same as free audio.** A free Creator Store *pack* is not
loadable until a human takes it into the account (learned the hard way on the VFX
harvester). Individual audio assets used by id have no such step, which is exactly
why this skill works by id and never asks anyone to take anything.

**Volume 0 during probing is deliberate.** 40 candidate sounds resolving at once
in an open Studio would be unpleasant. `probe.lua` sets `Volume = 0`;
`audition.lua`, `install.lua` and `tour.lua` set the real volume.

**Roblox's own stock library scores a deliberate bonus.** Creator id 1 assets
(the `91207…`-shaped ids) are consistent, always permitted and never deleted. If
a run must be reproducible months later, prefer them.

---

## Why library selection and not generated audio

Selecting from the library needs no quota, no ID verification, no moderation
wait and no upload, and an agent searching and selecting from the Creator Store
needs no human intervention.

Generated audio would burn a create-only upload quota to produce something no one
in the loop can hear. That trade is not worth making, and this skill is the
argument.
