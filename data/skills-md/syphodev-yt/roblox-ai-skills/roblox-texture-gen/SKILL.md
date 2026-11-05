---
name: roblox-texture-gen
description: Generate free AI textures/skins (camo, gold plated, carbon fiber, rust, etc.) for Roblox game assets like guns, weapons, tools, or any part/mesh, and apply them automatically inside Roblox Studio through the official Roblox Studio MCP — no manual clicking through Studio's Texture Generator plugin required. Use this whenever the user wants to texture, skin, retexture, or reskin a Roblox model/mesh/gun/weapon/part, asks for an AI-generated texture or decal for a Roblox object, or wants to automate the Studio texture workflow end-to-end. Also trigger if the user asks for "free" or "no-cost" image/texture generation in a Roblox context, even if they don't name a specific tool. Requires the Roblox Studio MCP connected with Studio open — if that's not available, say so clearly instead of guessing.
---

# Roblox Texture Gen

> **First time on this machine?** Read `LOCAL.md` in this folder. If it does not exist, run the
> `roblox-skills-setup` skill (or copy `LOCAL.template.md` to `LOCAL.md` and fill it in).
> `LOCAL.md` holds your paths and tool locations; it is yours and is never shared.

This skill is a scriptable texture pipeline: generate a tileable image with a free
API, upload it as an image asset, and write it onto the target part from code. It
works on any part or mesh and batches across a whole model.

The official Studio MCP also has `generate_texture`, which re-textures one MeshPart
or Model in place from a text prompt using Roblox's own AI. Use that when the user
wants a mesh-conforming texture on a single mesh; use this pipeline for tileable
materials, decals, many parts at once, or a texture you want as a reusable file.

## Why this sequence

1. **Image generation happens outside Roblox entirely.** [Pollinations.ai](https://gen.pollinations.ai)
   is a free, keyless image API — a plain HTTP GET returns a PNG. No Studio plugin, no
   paid tier, no signup required (registering is optional and only raises the rate
   limit / drops the watermark).
2. **Roblox only accepts assets it has ingested**, so the generated image has to be
   uploaded as an image asset before anything in Studio can reference it. That's what
   the MCP's `upload_image` is for.
3. **Applying it is just a property write**, done with `execute_luau` (one part or a
   loop over every part of a model).

## Step-by-step

### 0. Check the Studio connection

The tools come from the official Roblox Studio MCP (`list_roblox_studios`,
`get_studio_state`, `search_game_tree`, `inspect_instance`, `execute_luau`,
`upload_image`, `screen_capture`). If they are deferred, load them in one ToolSearch
call. Call `list_roblox_studios` to get the `studio_id` every other call needs, then
`get_studio_state`. If either fails, **stop and tell the user plainly**: the Studio MCP
isn't connected or Studio isn't open. Don't fabricate a result; this pipeline is dead
without a live Studio session.

### 1. Nail down what to generate

Ask (or infer from context) two things if they're not already clear:
- **Style** — e.g. "digital camo", "gold plated brushed metal", "carbon fiber weave",
  "battle-worn rust". Vague requests like "make it cool" are worth a quick clarifying
  question since the result is hard to undo once applied.
- **Target** — the exact part/mesh/model name in the place (e.g. `Handle`, `GunBody`,
  a whole `Model` with multiple parts). Use `search_game_tree` or `inspect_instance` to confirm the name
  exists before generating anything — don't guess a part name and find out it's wrong
  after the image is already made.

Build the generation prompt yourself: append `, seamless tileable texture, flat lighting,
no watermark, high detail` to whatever style the user described — this consistently
produces something closer to a usable game texture than the bare style words alone,
since generic prompts tend to come back as an illustration rather than a tileable
material.

### 2. Generate the image

Run the bundled script rather than hand-rolling the HTTP call — it handles URL encoding,
retries on Pollinations' rate limit (1 req/15s anonymously), and validates the response
isn't an error page masquerading as an image:

```bash
python "<skill_dir>/scripts/generate_texture.py" "camo military texture, seamless tileable texture, flat lighting, no watermark, high detail" ./textures/gun_camo.png --width 1024 --height 1024
```

Save into a scratch/textures folder, not directly into the user's project tree, unless
they've told you where assets belong. Pick a filename that says what it is
(`gun_gold_plated.png`, not `output.png`) — you'll likely generate a few variants before
landing on one the user likes.

**Show the generated image to the user before uploading it to Roblox.** Generation is
fast and free; asset upload and moderation are not instant, and re-uploading a rejected
or disliked texture wastes a Studio round trip. Get a thumbs-up first unless the user
explicitly says to skip preview and just apply it.

### 3. Upload as an image asset

`upload_image` takes image URLs, not file paths, so serve the textures folder on
localhost for the upload, then stop the server:

```bash
python -m http.server 8765 --bind 127.0.0.1 --directory ./textures
```

```
upload_image(imagePaths=["http://localhost:8765/gun_camo.png"], studio_id=...)
```

It returns a map of URL to `rbxassetid://<id>`. (No Studio? The `roblox-3d-model`
skill's `upload_asset.py` uploads an Image through Open Cloud with your own
`ROBLOX_API_KEY`.) **Uploads go through asset moderation** and can take a while
before they render; a freshly uploaded image sometimes shows grey even though the
property is set correctly. If `screen_capture` shows a grey or missing texture right
after upload, that's the likely cause; tell the user rather than assuming the
pipeline failed.

### 4. Apply it to the target

For a single part with a `Texture`/`Decal` child, or a `MeshPart` with a texture
property:

```lua
workspace:FindFirstChild("<target>", true).TextureID = "rbxassetid://<id>"
```

For a `Model` with multiple textured parts (e.g. a gun made of several `MeshPart`s that
should all share the skin), loop over descendants in one `execute_luau` call:

```lua
local model = game.Workspace:FindFirstChild("GunModel", true)
for _, part in ipairs(model:GetDescendants()) do
    if part:IsA("MeshPart") then
        part.TextureID = "rbxassetid://<id>"
    end
end
```

Use `inspect_instance` first if you're not sure whether the target exposes
`TextureID`, `Texture`, or a `SurfaceAppearance` child (SurfaceAppearance/MeshParts with
PBR materials are wired differently than a plain decal) — setting the wrong property
silently does nothing, so it's worth the extra read.

### 5. Verify

Call `screen_capture` and look at the result before telling the user it's done. A
property write succeeding doesn't mean the texture rendered correctly — mismatched UV
mapping, moderation delay, or the wrong property target can all leave the mesh looking
unchanged or wrong even though every tool call returned success.

## Iterating on style

If the user wants variations ("try it more worn", "less shiny"), regenerate with a
tweaked prompt rather than trying to edit the existing image — Pollinations has no
edit/inpaint endpoint in this flow, only text-to-image. Keep the `--seed` fixed across
variants of the *same* concept if you want family resemblance between attempts, and drop
it (or change it) for a genuinely different direction.

## What this skill does not do

- It doesn't replace Roblox's own mesh-aware texturing (the MCP's `generate_texture`,
  or the Texture Generator in Studio), which produces better UV-fitted results on
  complex meshes because it reasons about the geometry. This pipeline's advantage is
  that it's scriptable, tileable and batchable, not that it's higher quality.
- It doesn't manage Roblox asset moderation — uploads can be rejected (e.g. for content
  policy) and that's outside this skill's control. If `upload_image` reports a rejection,
  relay it to the user rather than retrying blindly.
