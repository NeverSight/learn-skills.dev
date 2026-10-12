---
name: zovii
description: Use when the user wants to generate AI images or videos, manage assets, organize canvas groups, or work with Zovii Studio projects from the command line. Triggers include "zovii", "generate image", "batch generate images", "generate video", "AI image", "AI video", "upload asset", "download asset", "remove background", "upscale video", "canvas group", "画布分组".
---

# zovii CLI

AI image & video generation from the command line via [Zovii Studio](https://zovii.studio).

## When to Load This Skill

Load this skill when the user mentions:
- "zovii", "generate image", "generate video", "AI image/video generation"
- "upload asset", "download asset", "project assets"
- "remove background", "upscale video", "upscale"
- "canvas group", "画布分组", "分组整理资产"

Full command reference: [references/commands.md](references/commands.md)

---

## Layer 1 — Setup

Run these two checks before every zovii command.

### 1.1 Install Check

```bash
which zovii
```

- ✅ Found → continue
- ❌ Not found → run `npm install -g zovii`, wait for it to finish, then continue

### 1.2 Login Check

```bash
cat ~/.config/zovii/auth.json
```

- ✅ File exists and contains `access_token` → continue
- ❌ Missing or empty → tell the user login is required, then guide them through phone + SMS code login (default):

```bash
zovii login                                   # interactive: prompt phone → send code → prompt code
zovii login 13800000000                       # half-interactive: auto-send → prompt code
zovii login 13800000000 --code 123456         # fully non-interactive
zovii send-code 13800000000                   # send the code separately (resend or send-then-login)
```

If the user prefers password login (legacy):

```bash
zovii login -u <username> -p <password>
```

---

## Layer 2 — Agent Decision Rules

These rules apply to every command:

- **No project ID?** Run `zovii list-projects` first and ask the user to pick one.
- **Local file path as input?** Pass it directly — the CLI auto-uploads it. No need to call `upload-asset` manually.
- **Waiting for results?** Default: wait (omit `--no-wait`). Only go async when the user explicitly requests it.
- **Output format?** Default: `table`. Add `-f json` when the output will be consumed programmatically.
- **Timeouts?** Image tasks default to 300 s; video tasks default to 600 s. Use `--timeout <seconds>` for long-running jobs.
- **Which model / which `--size` / `--duration`?** 不要凭记忆猜。模型清单与各参数取值由 zovii.studio 产品配置动态下发，运行 `zovii list-models ai_image` 或 `zovii list-models ai_video` 查看（`--refresh` 强制刷新缓存）。省略参数即使用该模型的默认值。

---

## Layer 3 — Workflows

### Workflow 1: Generate Image

```
1. Confirm project → if unknown, run: zovii list-projects, let user pick
2. Collect: --prompt (required)
3. Ask (optional): model, aspect ratio, count, reference image
4. Run: zovii generate-image <projectId> --prompt "..." [options]
5. Wait → display fileUrl
6. Ask if user wants to download → yes: zovii download-asset <assetId>
```

### Workflow 1b: Batch Generate Image

```
1. Confirm project → if unknown, run: zovii list-projects, let user pick
2. Collect: at least one --prompt (required); up to 20 --prompt flags, one image each
3. Ask (optional): model, aspect ratio, shared reference image (--image-input, max 10), size
4. Run: zovii batch-generate-image <projectId> --prompt "..." --prompt "..." [options]
5. Wait → display fileUrls for all generated images
6. Ask if user wants to download any → yes: zovii download-asset <assetId>
```

Models: 由产品配置动态决定（不再限定 4 个模型）。运行 `zovii list-models ai_image` 查看当前可用模型与参数取值；不传 `--model` 即用产品默认模型。

Optional shared flags: `--image-input` (max 10), `--aspect-ratio`, `--size`, `--no-wait`

Full options: [references/commands.md](references/commands.md)

### Workflow 2: Generate Video

Choose the variant that matches what the user described:

**Variant A — Text to video** (user provides only a prompt)
```
1. Confirm project
2. Collect: --prompt, --ratio, --duration, --model
3. Run: zovii generate-video <projectId> --prompt "..."
4. Wait → display fileUrl → ask if user wants to download
```

**Variant B — First / last frame** (user provides image(s))
```
1. Confirm project
2. Collect first frame (--image-input); ask if there is an end frame (--end-frame)
3. Collect: --prompt (optional), --ratio, --duration
4. Run: zovii generate-video <projectId> --image-input <ref> [--end-frame <ref>]
5. Wait → display fileUrl → ask if user wants to download
```

**Variant C — Reference assets** (user provides reference image / video / audio)
```
1. Confirm project
2. Identify reference type → image (--ref-image) / video (--ref-video) / audio (--ref-audio)
3. Ask if a prompt is needed for additional description
4. Run: zovii generate-video <projectId> --ref-* <ref> [--prompt "..."]
5. Wait → display fileUrl → ask if user wants to download
```

### Workflow 2b: Inspect Available Models

```
zovii list-models                  # 所有工具 + 各自默认模型
zovii list-models ai_image         # 生图模型：modelId / name / default / minCost / options
zovii list-models ai_video         # 生视频模型
```

`options` 列是各模型可选枚举参数的紧凑摘要（`*` 标默认值）。当用户问"有哪些模型/能出 4K 吗/最长几秒"时，先跑这条命令再回答。

### Workflow 3: Asset Management

```
List assets:    zovii list-assets <projectId> [--type image|video|audio] [--limit n]
Upload asset:   zovii upload-asset <projectId> <local-path>
Download asset: zovii download-asset <assetId> [--out <save-path>]
```

Agent notes:
- "Upload file X" → run `upload-asset` directly, no need to list first.
- "Download the image I just generated" → extract `assetId` from previous output, run `download-asset` directly.

### Workflow 4: Image / Video Processing

**Remove background**
```
1. Confirm project
2. User provides image (local path or asset ID)
3. Run: zovii remove-background <projectId> <image>
4. Wait → display transparent-background fileUrl → ask if user wants to download
```

**Upscale video**
```
1. Confirm project
2. User provides video (local path or asset ID)
3. Ask target resolution: 1080p / 2k / 4k
4. Run: zovii upscale-video <projectId> <video> --resolution <res>
5. Wait → display fileUrl → ask if user wants to download
```

### Workflow 5: Canvas Group Management

```
List groups:        zovii list-groups <projectId>
Create group:       zovii create-group <projectId> <name> [--assets id1,id2] [--auto-organize] [--color <color>]
Add members:        zovii add-to-group <projectId> <groupId> --assets id1,id2
Rename group:       zovii rename-group <projectId> <groupId> <newName>
Auto-organize:      zovii set-auto-organize <projectId> <groupId> on|off
```

Agent notes:
- `--assets` only accepts asset IDs (UUID), not local paths — upload first if needed.
- No group ID? Run `zovii list-groups <projectId>` first and let the user pick.
- Colors: blue / green / orange / purple / red / yellow / cyan / gray.
