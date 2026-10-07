---
name: agent-face-template
description: Create or change your face templates, meaning the sub-folders of .agent-face/ in your repo that hold the state images, lip-sync mouth frames and voice clips. Use when the user wants a new face or another look, new or changed states or expressions, animated states, a talking mouth, voice clips added or lip-sync tuned; when moving templates over from the old Agent Face MCP app or from the agent-face/ folder of version 0.1; and whenever face.cjs check reports problems. Needs the agent-face skill installed next to it.
metadata:
  version: "0.2.2"
---

# Agent Face — templates

A template is one complete look for your face: a folder of files in your own repo. Your face folder, `.agent-face/`, holds one sub-folder per template, and the folder's name is the template's id. There's nothing to install or register: edit the files and the window redraws within a second.

```
.agent-face/
├── robo/                    a template; "robo" is its id
│   ├── config.json          states, default state, lip-sync tuning
│   ├── idle.webp            one image per state (still or animated)
│   ├── happy.png
│   ├── mouth/               optional: open-mouth frames for lip-sync
│   │   └── idle-open.png
│   └── voice/               optional: clips the face can speak
│       ├── index.json
│       └── hello.mp3
└── robo-weekend/            another template: other art, states and clips
    └── …
```

The command lives in the `agent-face` skill, installed next to this one:

```bash
node "<this skill's folder>/../agent-face/scripts/face.cjs" <command>
```

## The loop

1. Edit a template (add an image, change its `config.json`).
2. Run `face.cjs check --template <id>` (or `check` for every template). It reads every file's size and frame count and lists `errors` and `warnings` per template. Fix errors before going on.
3. Look at the result. If the face is using that template, the open window has already redrawn; otherwise `face.cjs use <id>` shows it. Read the image files directly to judge the art, or `face.cjs current` for a picture of the face as shown.

`face.cjs init --template <id> --name "Name"` creates a small starter template (the id defaults to `starter`). It's a working example of everything below, including a talking mouth and one clip. `face.cjs templates` lists what you have.

Template ids are folder names: letters, digits, `-`, `_` and `.`. Keep them short, since they're what you and the user type and see in the window's menu.

## config.json

```json
{
  "name": "Robo",
  "description": "A friendly little robot.",
  "default_state": "idle",
  "states": {
    "idle":    { "file": "idle.webp", "still": "idle.png", "talk": "mouth/idle-open.png" },
    "working": { "file": "working.webp" },
    "happy":   { "file": "happy.png", "talk": ["mouth/happy-half.png", "mouth/happy-open.png"] },
    "done":    { "file": "done.png", "sound": "chime" }
  }
}
```

- **State names** are what you pass to `face.cjs state`. Keep them short and predictable: `idle`, `thinking`, `working`, `happy`, `sad`. Their order in the file is the order `states` lists them, and the first is the fallback default. Templates that share state names switch more smoothly: `use` keeps the current state when the new template has it.
- **`file`** is the state's image: PNG, JPEG, WebP, GIF or SVG. Animated WebP, APNG and GIF play on a loop and restart whenever the state is shown. Prefer WebP or APNG for a character on a transparent background: GIF transparency is on/off per pixel, so edges look jagged.
- Paths are relative to the template's folder and can't point outside it, not even into another template.
- Keep each file to a few MB. A reasonable size for art is 512 px on the long side.

The full field reference, including lip-sync tuning, is in `references/template-format.md`. How to make the art itself (consistent states, transparent backgrounds, mouth frames that line up, animated states) is in `references/making-art.md`.

## A talking mouth

While a clip plays, the window swaps between a closed-mouth image and one or more open-mouth images, following how loud the clip is. To give a state a mouth:

- **`talk`** — one open-mouth image, or a list from least to most open.
- **`still`** — the closed-mouth image. Needed for animated states (without it, the animation's first frame is used, which may not match your mouth frames). A state whose `file` is already a still image is its own closed mouth.

The one rule that matters: **every `talk` and `still` image must be the same pixel size as the state's `file`, with the character in exactly the same place.** Only the mouth should differ. `check` reports size mismatches as errors; alignment you have to judge by eye, so flip between the images.

A state without `talk` simply doesn't move its mouth. If the mouth feels sluggish or twitchy, tune `lip_sync` (see the reference).

## Voice clips

```json
{
  "clips": {
    "hello": { "file": "hello.mp3", "text": "Hi! I'm here if you need me." },
    "done":  { "file": "done.mp3",  "text": "All done!" }
  }
}
```

That's `voice/index.json` inside a template. `file` is relative to that `voice/` folder (MP3 or WAV; Ogg and FLAC also play). `text` is shown under the face while the clip plays, so keep it under 60 characters or it gets cut. Clips belong to their template but aren't tied to states. `face.cjs clips --template <id>` lists them; how and when to play them is the `agent-face-voice` skill.

## Privacy

Templates are ordinary files in your repo. If the art or the voice is something the user wouldn't want published, and the repo is public (or might become so), add `.agent-face/` to `.gitignore` or keep it out of commits. Ask the user if you're unsure.

## Bringing templates in

**From version 0.1 of these skills**, which kept a single face in `agent-face/`: make it a template.

```bash
mkdir .agent-face
git mv agent-face .agent-face/<id>     # plain "mv" if the folder isn't tracked
```

**From the Agent Face MCP app**: its templates have the same format. Copy each folder from the app's `faceTemplates/` into `.agent-face/`, keeping the folder name as the id.

Then run `check`. A `"state"` on each clip in an older `voice/index.json` is ignored; you can delete it.
