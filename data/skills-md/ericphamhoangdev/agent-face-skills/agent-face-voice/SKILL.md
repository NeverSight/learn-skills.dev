---
name: agent-face-voice
description: Speak through your face by playing one of its voice clips out loud, with the mouth moving in time. Use when the user asks you to say something aloud, to greet them, or to announce that long work has finished; when they ask about your voice, muting or volume; and when a state should make a sound. Needs the agent-face skill installed next to it.
metadata:
  version: "0.2.2"
---

# Agent Face — voice

Your face can speak: it plays one of its template's recorded clips through the user's speakers, shows the clip's text under the face, and moves the mouth with the sound.

The command lives in the `agent-face` skill, installed next to this one:

```bash
node "<this skill's folder>/../agent-face/scripts/face.cjs" <command>
```

## Speaking

```bash
face.cjs clips                                  # the clips of the template in use, with their text
face.cjs clips --template <id>                  # the clips of another of your templates
face.cjs say <clip>                             # speak; the face keeps its current state
face.cjs say <clip> --state proud               # switch expression first, then speak
face.cjs say <clip> --caption "Build is green"  # show this instead of the clip's own text
```

A clip is not tied to an expression. The same line can be said happy, tired or determined, so you choose the state that fits the moment, or leave the face as it is.

`say` returns as soon as the clip starts; it doesn't wait for it to finish. Changing state or template while it plays (your end-of-turn update, for instance) changes the face but not the voice: the clip plays to the end, its words stay up, and the mouth carries on with the new state's frames. Only another clip cuts it off, so if you want to say two things, check `status`: `speaking` is true while a clip plays, and `ms_left` says for how much longer.

The result tells you what happened:

| `result` | Meaning |
| --- | --- |
| `played` | It's playing. `duration_ms` is its length; `lip_sync` says whether the mouth is moving; `audio` says where the sound went (below). |
| `muted` | The user muted this face. Nothing played; the text still shows. |

An unknown clip or state is an error that lists the valid ones, and changes nothing.

## Manners

- **Speak rarely.** Sound interrupts in a way a picture doesn't. Good moments: the user asked for it, a greeting at the start of the day, long-running work finishing while they're away from the screen. Not every turn, and not for routine updates. That's what states and captions are for.
- **Mute and volume belong to the user.** They set them from the face's right-click menu and its speaker button. You can see them in `status` (`muted`, `volume`), but never change them, and don't look for another way to make sound when the answer was `muted`. If the user wants you audible, they'll unmute.
- **A silent result is fine.** When nothing plays, the text is still shown, so the message got through. Don't retry.

## When the user can't hear you

`say` and `sound-test` report what the audio output did:

```json
"volume": 0.7,
"audio": { "state": "running", "device": "Default - Speakers (…)", "sample_rate": 48000, "output_latency_ms": 42 }
```

If the user says they can't hear the face:

1. Run `face.cjs sound-test`: a short chirp through the same path as a clip. Only when the user asks, since it makes a sound.
2. Read the reply. `muted` means the face is muted (theirs to change). An error means the audio output didn't start; quote it.
3. If it says `played` with `"state": "running"`, the sound reached the operating system. Tell the user which `device` it went to, and ask them to check that device is the one they're listening on, its system volume, and the face's own entry ("Electron") in the system's volume mixer. Don't change any of these yourself.

Each clip opens the speakers that are current at that moment, so switching or reconnecting speakers takes effect from the next clip.

## Lip-sync

The mouth moves only if the face's current state has mouth frames (`talk` in `config.json`). When `say` returns `"lip_sync": false`, the clip played but that state has no frames. Adding them is the `agent-face-template` skill's job.

## Sounds on a state

A state can play a clip every time the face switches into it: add `"sound": "<clip name>"` to that state in the template's `config.json`. Use this for one or two rare, meaningful states (a chime when work is done). On a common state it would make the face speak constantly, because you change state at least twice a turn.

## Adding clips

Each template has its own clips: audio files in `.agent-face/<template>/voice/`, listed in that folder's `index.json`. `say` plays clips of the template in use. The format, and how to check your work, are in the `agent-face-template` skill.
