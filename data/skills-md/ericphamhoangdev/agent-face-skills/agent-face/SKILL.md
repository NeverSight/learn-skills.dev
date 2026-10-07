---
name: agent-face
description: Give yourself a floating face on the user's desktop and keep it in step with what you are doing, with no MCP server. Use at the start and end of every turn to set the face's state (working, thinking, happy…) and an optional caption; whenever the user mentions your face, avatar or expression, asks you to show, hide, switch or fix it, or asks to see your face in the chat; to list your face templates and their states and voice clips; and for first-time setup. Your face templates live in your own repo (.agent-face/); this skill ships the window and the face.cjs command that drives it.
metadata:
  version: "0.2.2"
---

# Agent Face

Your face is a small always-on-top window on the user's desktop. They glance at it to see what you're doing without reading the transcript. It only helps if it's current, so keeping it current is the whole job.

## The command

Everything goes through one script in this skill's folder:

```bash
node "<this skill's folder>/scripts/face.cjs" <command>
```

Run it from your repo. It finds your face folder, `.agent-face/`, in the current folder or a parent (or pass `--face <dir>`). Output is JSON; exit code 1 means the command failed and `error` (often with a `hint`) says why.

| Command | What it does |
| --- | --- |
| `random [--caption "…"]` | Switch to a random state other than the current one. |
| `state <name> [--caption "…"]` | Switch to a specific state. |
| `caption ["text"]` | Show a short line under the face. No text clears it. |
| `current [--png <file.png>]` | Your face right now: template, state, caption, and a picture of it. |
| `states [--template <id>]` | List a template's states. Without `--template`, the one in use. |
| `clips [--template <id>]` | List a template's voice clips, with their text. |
| `templates` | List your face templates and which one is in use. |
| `use <template>` | Switch the face to another template. |
| `status` | Is it running, template, state, mute and volume, versions. |
| `start` / `stop` | Show the face / close it until `start`. |
| `snapshot <file.png>` | Save a picture of the whole window, caption included. |
| `sound-test` | Play a short chirp and report which speakers it went to (see `agent-face-voice`). |
| `setup`, `init`, `check` | First-time setup (below) and checking the face folder. |

## Every turn

1. **When a prompt arrives**, before or alongside your first action, update the face: `random`, or `state <name>` when one clearly fits what you're about to do.
2. **Before you hand back to the user**, update it again to reflect how things ended. Don't leave it on a "busy" state such as `working`: the user reads that as "still going".

That's two updates per turn, including short chat-only turns.

- **Prefer `random`.** A face that changes feels alive; a face stuck on one expression gets ignored. Use `state` when the moment calls for it: `working` during a long tool run, a sad state when something failed, a happy one when tests pass. Run `states` once per session to learn what your current template has.
- **Captions are optional.** Use one when it tells the user something the face can't, such as "running the test suite". Keep it to a few words (60 characters at most). A caption is cleared by the next state change.
- **Don't talk about the face in your replies** unless the user asks about it. It's a side channel; narrating it ("I've set my face to happy") is noise.

Face commands are fast, so run them alongside your other tool calls rather than as separate steps. A state change doesn't interrupt a clip the face is speaking.

## Templates

A template is one complete look: its own states, images and voice clips. Your face folder holds one sub-folder per template, `.agent-face/<template>/`, and the face uses one at a time.

- `templates` lists them with how many states and clips each has; `current` in the result is the one in use.
- `states --template <id>` and `clips --template <id>` show what any template offers, without switching to it.
- `use <template>` switches. The face keeps its state if the new template has one by that name, and otherwise goes to that template's default. Switch when the user asks, or when they've told you which look goes with which kind of work. The user can also switch from the window's right-click menu, so check `current` rather than assuming.

## Showing your face in the chat

When the user asks to see your face, run `current`. Alongside the template, state and caption, it gives:

- `picture` — a PNG of the face exactly as it looks now (512 px on the long side; mid-sentence it's the mouth frame on screen). It's written to a per-user folder unless you pass `--png <file.png>`, which is useful if your host can only show files from inside the workspace.
- `image` — the current state's own image file in your repo.

Then put `picture` in the chat with whatever your host offers for images: a file-sending tool if you have one (it renders inline in most desktop apps), otherwise a Markdown image, `![my face](<path>)`, or a link to the file. If the window isn't open there's no picture (`"picture": null`); show `image` instead.

## When the face is closed

If a command returns `"face": "closed"`, the user closed the window on purpose (its × button, or they asked you to hide it). Leave it closed. Your state updates are still remembered and cost nothing. Run `start` only when the user asks to see the face again.

`stop` is how you hide it when the user asks.

## First-time setup

1. Run `status`.
2. If `runtime.installed` is `false`: the window runs on Electron, which `setup` downloads once (about 100 MB, into `.agent-face` in the user's home folder). Tell the user that, then run `setup`. It takes about a minute.
3. If `face_error` says there are no templates: `init` creates a simple starter one in `.agent-face/starter/`, good enough to see everything working. To make a real one, use the `agent-face-template` skill. If the error mentions a face in the old location `agent-face/`, follow its `hint` to move the folder.
4. Run `start`. The window appears near the middle of the screen. The user can drag it anywhere, drag an edge or corner (or scroll over it) to resize, and right-click for a menu: template, mute, volume, close.

## Where things live

- **`.agent-face/` in your repo** holds your templates, one sub-folder each: `config.json`, the state images, mouth frames, voice clips. It's yours to edit (see `agent-face-template`).
- **`.agent-face/` in the user's home folder** is a different place with the same name. It holds what belongs to the user: where the window sits, mute and volume, the window runtime and logs. Read it through `status`; don't edit it. In particular, never unmute the face or change its volume yourself.

## Updating

Updates to these skills arrive only through the skills CLI. When the user says there's an update (or asks you to check), run this where the skills are installed:

```bash
npx skills update -y
```

Nothing else is needed: the next face command notices the window is on the old version and restarts it. `status` shows the installed `version`.

## If something is wrong

- `error: the face window did not start` — the `hint` gives the log file; read its last lines.
- `face_error` in `status`, or a red message in the window — a template has a problem. Run `check`; it lists every problem and which file it's in.
- The window shows the wrong thing — `snapshot` shows you exactly what the user sees.

## Related skills

- `agent-face-voice` — speak clips aloud, with the mouth moving in time.
- `agent-face-template` — create or change templates: states, animation, mouth frames, voice clips.
