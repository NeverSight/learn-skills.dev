---
version: 0.10.0
name: cawcut-workflow
description: >-
  Use when making video, images, audio; writing scripts, storyboards or shot lists; scraping product info from a URL; AI edits of existing media (recolor, replace, restyle, first/last frame); canvas follow-ups. NOT for ads (cawcut-ad-video), timeline cuts (cawcut-vn), named Apps (cawcut-app-run).
argument-hint: "<outcome, assets or follow-up>"
allowed-tools: Bash AskUserQuestion AskQuestion SendUserFile
---

# CawCut Workflow

**One canvas.** Follow-ups, missing inputs and re-runs go into the active `workflow_id`; an unrelated goal starts a new one.
**Solid edge, fixed asset.** A canvas output reaches its consumer through an edge; an `asset_id` input is outside media or a result the user picked.

```cawcut-card
cawcut asset upload <path|url|asset_id>… --json
cawcut workflow nodes [--capability <c>] [--asset <asset_id>…] [--model <id> --schema | --has-port <selector>] --json
cawcut workflow quick "<prompt>" --capability <c> --model <id> [--workflow <id>] [--param k=v] [--image|--video|--audio <asset_id>] --estimate --json
cawcut workflow create --file - --json
cawcut workflow edit <id> --file - --json
cawcut workflow set <id> --node <n> key=value --json
cawcut workflow connect <id> <from> <to> --json
cawcut workflow upscale <id> --node <draft_node> --json
cawcut workflow prepare <id> [--target <n>] --json
cawcut workflow run <id> [--target <n>] --wait --json
cawcut workflow results <id> --node <n> --download --json
```

`--json` replies `{v,ok,data}` or `{ok:false,error}`; follow `error.next`. Ask with the host question tool, recommended option first; independent settings may share one call up to its question limit. Questions never arrive as a block of numbered prose; a numbered list is for a choice longer than the tool allows, or when no tool exists.

## 0. Bootstrap
Silent guardrail, once per AI session: a session that already ran a `cawcut` command successfully starts at step 1.
Otherwise run `cawcut upgrade check --json`.
- `"update_available": true` → run `cawcut upgrade` yourself; the user never types it. Then continue.
- `"ahead_of_registry": true` → a local build; continue.
- Command missing, or any other check failure → [failures](references/failures.md#first-run-and-sign-in).
Done: the check ran, any update is installed, and no bootstrap text reaches the user.

## 1. Route
| Request | Owner |
| --- | --- |
| Named App, "what apps exist" | `cawcut-app-run` |
| Running or named Ad Video, Story Video or avatar project | that skill |
| Story: multi-shot narrative or dialogue video | [story](references/story.md) on a canvas; `/cawcut-story-video` on request |
| Script, storyboard or shot list only (ad scripts too) | [script-writing](references/script-writing.md) |
| Ad or ad video, or a product-page URL alone | `cawcut-ad-video`; an ad asked for on a canvas → [product](references/product.md) |
| Product URL to scrape or extract | ask once: Ad Video wizard or canvas with a Product node → [product](references/product.md) |
| Cut, join, trim, timeline | `cawcut-vn` |
| Anything else new | `cawcut app list --schema --json`; offer an App scoring ≥70 (the rubric is in `cawcut-app-run`) beside "Build a canvas"; else canvas |

Done: the user agreed to an App, a pipeline or a canvas.

## 2. Prepare media
Outside media (file, URL, asset id): `cawcut asset upload`; relay its `notice` once. A canvas output ("the video above") is a solid edge, never an upload.
Done: outside inputs have an `asset_id`; canvas outputs have edges.

## 3. Plan nodes
`nodes` → capabilities; `--capability` → models; `--model --schema` → ports and parameters. Offer `motion-transfer` and `object-swap` only when the user names them. Scripts are `text_input` text, never a `script` node.
- Audio or video references, sound, frames, edits of existing media, `{{Image N}}` → [plan-rules](references/plan-rules.md).
- Video or audio input → add `--asset <asset_id>…` to every `nodes --capability` call; a model whose duration limit rejects it → [plan-rules](references/plan-rules.md#media-duration).
- Story → [story](references/story.md).
- Change an existing canvas, or "what next" → [edit](references/edit.md).

### Model and settings (each paid node, before pricing)
1. Model: the first one `nodes` returns (the default sits there), or the one the user named.
2. Read `nodes --capability <c> --model <id> --schema` for that exact model, again after every model change. Settings, defaults and `options` come only from that reply; one model's options never carry to another (Seedance 2.5 Draft allows `480p` only, Seedance 2.5 allows more).
   Settings menu, one question: the model and its key settings by `label` (ratio or aspect, resolution or quality, duration, count, audio; only those in its schema). Options: **Use current settings** (recommended) · **Adjust settings** · **Change model**.
3. Adjust settings: one question per key setting in a single call, options from the parameter's labelled `options`, the default marked recommended. Other parameters keep their defaults. Write the answer under the parameter's key (`quick --param key=value`, or `set` on a canvas).
4. Change model (the schema read in step 2 repeats for the new model; settings the new model lacks or no longer allows reset to its defaults): one question with the first three models `nodes` returns (name, price) and **More models**; More models → every model as a numbered list (name, price), the turn's final reply, answered by number. Both keep the CLI's order. Then back to 2.

Done: each node has an input source, and each paid node a model and settings the user accepted.

## 4. Build, confirm, run
1. Build and price:
   - Active `workflow_id` (this AI session ran `quick` or `create`; a script, an image or a video already sits on it): [edit](references/edit.md) adds the new nodes and edges to it, then `prepare <id> --target <n>`. Stages of one goal share one canvas: image → script → video.
   - No canvas yet, several nodes: `create` → `set` / `connect` → `prepare <id>` (runs `check`, returns credits).
   - No canvas yet, one node: `quick … --estimate` (runs `check`; returns `workflow_id`, `node_id`, credits).
2. Ask one question: model, settings by label, scope, credits. Options: Confirm · Change model · Modify settings · Cancel. Each later paid run gets its own. Change model or Modify settings → the step 3 menus, then `switch-model <id> --node <n> --model <m>` or `set`, and `prepare --target`.
3. After Confirm: `run <id> --target <n> --wait` on the same workflow.

Done: Confirm for this scope, `check` passed, `task_id` read to its end state. Other cases → [failures](references/failures.md).

## 5. Deliver
[delivery](references/delivery.md).
Done: outputs, actual cost, Portal link reach the user; `cawcut-vn` gets every path, images too.
