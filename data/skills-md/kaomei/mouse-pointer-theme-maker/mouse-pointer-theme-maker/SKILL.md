---
name: mouse-pointer-theme-maker
description: Use when a user wants a custom macOS or Windows mouse pointer theme from a reference image, original mascot, or named character/IP. Create eight original artworks, expand them into 51 macOS Mousecape cursor IDs or 15 Windows cursor roles, show a high-resolution PNG preview before packaging, and provide guided installation. Support retro-pixel, chibi-anime, and abstract-expression visual styles.
---

# Mouse Pointer Theme Maker

Create a polished, consistent dual-platform cursor theme from a reference image or a named character/IP and a style direction. Prioritize clear, correct interaction over decorative detail. Create eight distinct artworks, then expand them to the macOS exact-ID coverage set and, whenever the user requests Windows or cross-platform output, the 15 Windows cursor roles. The expansion reuses appropriate approved art for aliases; it does not ask the user to create or choose 51 separate images.

## 首次使用提问

On the first invocation of this skill, ask the user for these three inputs before generating art or creating files. If the user already supplied an item, acknowledge it and ask only for the missing items.

Before starting a generation job, verify that the loaded `SKILL.md` is this current release: it must mention **eight separate image-generation jobs**, **visual-quality-gate.md**, and **HTTP 413 Payload Too Large** recovery. If any marker is missing, stop and ask the user to reinstall/update the Skill from the repository instead of mixing files from an older installation.

1. **电脑平台**：`macOS` or `Windows 10/11`. This determines which package will be produced; never silently create both.
2. **视觉风格**：introduce all three choices in plain Chinese:
   - `retro-pixel` 复古像素风：16/32 位游戏感、像素轮廓、鲜明色块。
   - `chibi-anime` Q 版二次元风：大表情、圆润比例、可爱的角色配件。
   - `abstract-expression` 抽象表达风：用夸张、视觉隐喻、超现实幽默、民俗插画感或表情包反应表达主题，不局限于恶搞。
3. **主题/角色与鼠标皮肤样式**：询问想做的 IP/角色、参考图、配色和整体感觉；可以只说角色名，也可以上传图片。说明要做的是“角色融入鼠标功能”的整套皮肤，而不是把人物图片直接贴在箭头上。

**回答示例：**

> 电脑：macOS
>
> 风格：abstract-expression 抽象表达风
>
> 主题/角色：甄嬛传，用夸张宫斗动作和表情包节奏表现；正常、输入、点击、不可用、忙碌、移动、左右调整、上下调整这 8 个状态都要有。主色想要米白、朱红和玉绿色。

## Collect input

Ask for a theme name only if absent. Accept either a user-provided character reference image or a named character/IP; do not require both. Treat a named IP as a visual brief, never claim the generated result is official. Default to `chibi-anime` if no style is given. Use a safe identifier such as `com.example.<theme-name>`.

Use the original reference directly as an identity reference, explicitly excluding its background and surrounding UI. Create a separate transparent reference only when background clutter prevents identity recognition; a clean white-background JPG does not require an extra image-generation job.

## Generation capability and execution

Before creating artwork, read [references/generation-runtime.md](references/generation-runtime.md). Verify that this session exposes an image-generation tool that accepts reference images and returns usable image files. A Codex installation, chat model, or API-compatible responses endpoint alone is not proof of image-generation capability. If the capability is absent, report `GENERATION_UNAVAILABLE` and the missing tool; do not substitute scripted drawings, reference cutouts, emoji, or SVG artwork. Use an external image provider only if the user explicitly chooses it, and record the provider/model when available.

Record the loaded skill version `1.1.1`, absolute skill path, tool/provider, selected style, and state-to-file mapping in the output directory. This makes reproduction failures diagnosable without storing credentials or full conversations. Do not promise identical artwork across providers or runs.

Generate `normal` first as a style anchor, inspect it, then use the original identity reference plus that approved anchor for the remaining states when the tool supports two reference images. Keep prompts compact. Use independent jobs in batches of 2–3 only when the tool explicitly supports concurrent calls; otherwise use sequential calls. Do not use subagents to bypass a tool's concurrency limit. Verify each returned file before including it in the preview, but checking one completed job need not block other already-running jobs. Resume from verified files; regenerate only failed states, with at most two targeted quality repairs per state before reporting the specific failure. Do not require a user approval between individual states.

Read [references/styles.md](references/styles.md) before creating art. Offer these three styles:

| Style | Direction |
| --- | --- |
| `retro-pixel` | Detailed 16-bit/32-bit pixel UI, character expressions and readable pixel silhouettes |
| `chibi-anime` | Q-version anime mascot, lively expressions and cohesive accessories |
| `abstract-expression` | Exaggeration, visual metaphor, surreal humor, folk-art energy, or meme-like reactions |

## Request-size budget and 413 recovery

Read [references/request-budget.md](references/request-budget.md) when the client uses a proxy/API endpoint or when a request contains images, long history, or many tool outputs. Keep the active request small: load only the reference needed for the current state, do not paste the full `SKILL.md` or every reference into a prompt, and do not serialize images or files as Base64 in text. Generate the eight states as separate jobs and keep the contact-sheet renderer local after the state PNGs exist.

If the API returns **HTTP 413 Payload Too Large**, stop retrying the identical request. Do not interpret reconnect attempts as recovery. Start a compact recovery turn containing only: the platform, chosen style, theme/character brief, the current state, the strict identity reference attachment, and the required output constraints. Omit prior transcripts, raw tool output, duplicate images, and unrelated references. If the compact request still returns 413, stop after one retry and report that the configured proxy/server body limit must be raised; do not generate a partial package or claim that the image job completed.

If a generated PNG or preview cannot be visibly attached in the client, do not claim that the user has reviewed it and do not continue to packaging. Report the actual absolute `preview.png` path or attach the file again in a fresh short turn; approval must be based on the original PNG/JPG, not a chat thumbnail or an unrendered SVG.

## Generation output handshake (fail closed)

Treat an image-generation call as **successful only after its output is verified**. After each `image_gen` job, do all of the following before accepting that state:

1. Confirm the tool returned a non-empty image result (an image block or generated-image artifact), or locate the newly written file under the configured `$CODEX_HOME/generated_images` directory.
2. Confirm the artifact is a real file with a non-zero byte size, a PNG signature when PNG was requested, and a decodable image. Use `view_image` or an equivalent image inspection step so the result is actually visible to the user-facing client.
3. Record the verified absolute path and state name. Do not use an old cached image whose timestamp or state mapping cannot be proven.

If the tool result is empty, the file is missing, the file is unreadable, or the client cannot display it, set the state to `GENERATION_UNAVAILABLE`, report that the state was **not generated**, and stop. Do not describe it as generated, do not render a preview card, do not ask for approval, and do not build or send a package. A reconnect or retry is allowed only under the 413 recovery rule above; never retry an identical request indefinitely.

## Generate the eight original artworks

Use image generation with the reference image and a genuinely transparent background; preserve its alpha channel. Create these eight states as **eight separate image-generation jobs**, one state per job, with the same palette, line weight, proportions, and character treatment. Separate jobs do not require serial execution when concurrent tool calls are supported. Do not ask an image model for a single 4×2 contact sheet and crop it into states: that makes the character small, weakens identity consistency, and prevents targeted repair. Do not assume an unbundled background-removal helper exists. If the selected provider cannot produce transparency, disclose that limitation and use a verified available extraction tool only with a visual edge review; never treat an opaque PNG or checkerboard pattern as transparency.

| Use | State |
| --- | --- |
| ordinary selection | `normal` |
| text entry | `text` |
| button or link | `action` |
| unavailable action | `forbidden` |
| busy | `busy` |
| pan canvas | `open_hand` |
| horizontal resize | `resize_horizontal` |
| vertical resize | `resize_vertical` |

Read [references/full-states.md](references/full-states.md) for each visual cue, identifier, and hotspot rule. Then read [references/standard-coverage.md](references/standard-coverage.md): macOS picks precise cursor IDs, so this reference defines how the eight original artworks are expanded into the 51 supported IDs. For Windows or cross-platform output, also read [references/windows-installation.md](references/windows-installation.md). Read [references/complete-tutorial.md](references/complete-tutorial.md) before the final delivery: it is the mandatory beginner-facing installation, verification, troubleshooting, and restore guide. Treat the hotspot as a non-negotiable interaction contract: it must sit on the arrow tip, I-beam centre, fingertip, or symbol centre as specified. Keep it free of faces, decorations, text, effects, and props. For character art, place the character behind or beside the functional cue; do not replace an arrow, I-beam, hand, or resize arrow with a portrait.

Read [references/visual-quality-gate.md](references/visual-quality-gate.md) before generating art and complete its eight-state action plan. The character must be **redrawn for the meaning of every state**: change pose, hands/body interaction, expression, or prop while preserving identity. Reusing the same standing portrait, cutout, or source-image crop in multiple states and merely changing the arrow/hand/symbol beside it is a failed result. Local scripts may remove backgrounds, resize, validate, and arrange approved art; they must never substitute a static reference-image cutout for image generation.

Run one visual review after all eight jobs. Reject and regenerate any state when the character looks pasted beside a system cursor, the functional cue and character do not physically interact, the character occupies less than roughly one third of the artwork's meaningful silhouette, the cue is hidden at small size, or the character's identity has drifted. Do not show a knowingly failed draft merely to prove that a file or preview renderer works.

Generate larger working images if needed. For every state, export four internal Retina representations from the original artwork: `32×32`, `64×64`, `160×160`, and `320×320` PNGs (1x, 2x, 5x, 10x). These are automatic display-density resources for one cursor, not user-facing skin variants: never ask the user to choose a scale. Do not upscale the `32×32` result; render or resample each representation directly from the larger source. Keep the intended hot point free of decorative parts.

After cropping each source image, inspect all four edges at 100% before resizing. A crop is invalid if an adjacent cell, guide, border, or isolated **裁剪边缘残留线条** appears on any edge; recrop within the single cell and regenerate all four representations. Never ship a cursor with crop-edge residue, even if the line is only one pixel wide or is reused by an alias state.

macOS applications choose cursor types; Mousecape does not identify semantic controls such as a close button when an application still requests the normal arrow. Map close-like or unavailable treatment only to the `forbidden` state.

## Preview approval gate

The default PNG design is the approved typography-led collectible-card layout: heavy sans-serif Chinese title, large artwork, restrained card shadows, secondary English state identifiers, and one shared hotspot note. Read [references/preview-design.md](references/preview-design.md) for character names, display titles, high-resolution source mapping and cross-platform fonts. Render with the supplied script rather than improvising a new layout. Eight-state previews are 2440×1600; titles and character names fit their allocated areas automatically. For multiple heroes, use `character_name` on each state; a single-character theme can omit it. User-requested visual changes take precedence.

Before packaging, make a single **卡片式 PNG/JPG** preview sheet. It must show exactly the eight agreed states as a 4×2 themed card grid: theme title, Chinese state name, state identifier, large cursor art, and a red hotspot cross on every card. The user-facing image must be at least **2440×1388**. Render large card art from the approved normalized high-resolution `preview_source` when available, preserving the representation canvas/hotspot ratio; otherwise use the approved 10x Retina representation. Never enlarge the 32×32 1x PNG. The hotspot must still use the 32×32 coordinate ratio. Use `theme.preview_style` in the manifest (`retro-pixel`, `chibi-anime`, or `abstract-expression`) so the card palette matches the requested art direction. The preview is an approval artifact, not a raw engineering contact sheet: keep generous card spacing, clear hierarchy, and no extra alias states. Before rendering it, complete the checklist in `references/visual-quality-gate.md`; every state must be marked `PASS`, and any `REGENERATE` item must be replaced first.

**交付顺序必须固定：**先发送 PNG/JPG 预览图给用户确认，确认前不得发送 `.cape`、压缩包、Mousecape 下载地址或安装教程。`preview.svg` 只作为内部可编辑源文件（preview.svg 只作为内部），不作为用户确认图。只有用户明确回复“可以”“确认”“就这样”等同意词后，才生成并发送安装文件，再给安装教程（确认后再发送）。Do not build a `.cape` before approval. 若用户要求修改，只改指定状态并重新输出 PNG/JPG 预览，不进入打包步骤。

预览阶段使用独立渲染命令，不会生成安装包：

```bash
python3 scripts/render_preview.py --manifest <theme-dir>/artwork-manifest.json --output <theme-dir>/preview.png --svg-output <theme-dir>/preview.svg
```

Show `preview.png` to the user and wait for explicit approval. PNG 使用 2x 卡片画布与 10x 状态资源缩放，确保文字、角色线稿和热点十字清晰。

After `render_preview.py` returns, verify that the printed absolute `preview_png` path exists, is non-empty, is a decodable PNG, and is at least `2440×1388`. Then display or attach that exact file. A path printed without a readable, user-visible file is not a delivered preview and cannot satisfy the approval gate.

`render_preview.py` 和 `build_cape.py` 会自动检查最大 Retina 图的 **safe transparent border**：四边任一处的非透明像素贴到裁剪边缘时，必须拒绝生成预览和安装包。此时从未裁切的原图重新取图、保留透明边距，并重新生成四个尺寸；不要通过缩放或忽略报错绕过检查。

红色十字是**预览专用**的热点校准标记，只用于让用户检查箭头尖端、I-beam 中心或手指点击点；它以及任何红色框选/标注都**不得写入**状态 PNG、`.cape` 或 Windows `.cur` 文件。安装后的鼠标只显示角色与功能图形。

For a public **GitHub gallery**, use the same complete high-resolution 4×2 PNG preview rather than a raw sprite sheet. Keep one curated example for each supported style, use repository-relative image paths, and never include user source references, generated install archives, or third-party application binaries. A gallery example must pass the same hotspot, safe-border, clipping, and crop-residue review as a user delivery.

## Package after approval

### 先确认用户平台

The platform should already be recorded during **首次使用提问**. If it is still missing when the user approves the preview, ask one concise question before creating any install archive: **“你使用的是 macOS 还是 Windows？”** Do not guess from the conversation or package both platforms automatically. Record the answer as `macos` or `windows` and build only that platform. If the user explicitly needs both, create two separately named packages and two separately named archives; **不要把 macOS 与 Windows 打进同一个压缩包**. The platform question must happen before writing a `.cape` or running the Windows builder.

1. Copy `assets/essential-theme-manifest.json` into one output directory as `artwork-manifest.json`. Replace the template theme fields with the user’s name and author, set `theme.preview_style` to the chosen art style, then set each `path` and `representations` list to its PNG filenames. The list must contain the 1x, 2x, 5x, and 10x files in that order.
2. Run `scripts/prepare_cursor.py` for every representation. Use `--scale 1`, `--scale 2`, `--scale 5`, and `--scale 10`; use `--resize` only when a source has the wrong dimensions. Preserve its alpha channel.
3. Build the macOS package after the PNG/JPG preview is approved:

   ```bash
   python3 scripts/expand_standard_coverage.py --manifest <theme-dir>/artwork-manifest.json --output <theme-dir>/manifest.json
   python3 scripts/build_cape.py --manifest <theme-dir>/manifest.json --output <theme-dir>/<theme-name>.cape --preview <theme-dir>/preview.svg
   ```

4. If the confirmed platform is Windows, build its 15-role package from the same approved `artwork-manifest.json`:

   ```bash
   python3 scripts/build_windows_cursor.py --manifest <theme-dir>/artwork-manifest.json --output <theme-dir>/windows
   ```

   Do not run the generated PowerShell script yourself. Deliver it only after the user has reviewed the art. Read [references/windows-installation.md](references/windows-installation.md) before describing installation.

   For Windows, embed the available `1x` and `2x` representations in each `.cur` when both exist; this lets Windows select a sharper image at high display scaling. Do not upscale a 1x PNG into a fake high-resolution resource; if the 2x file is absent or invalid, ship the validated 1x image and state that limitation. The builder accepts only a 32×32 image or a 32×32 plus 64×64 pair, never a giant 160×160/320×320 bitmap inside a Windows cursor.

5. Verify the macOS package:

   ```bash
   python3 scripts/validate_cape.py <theme-dir>/<theme-name>.cape
   python3 scripts/validate_hotspots.py --manifest <theme-dir>/manifest.json --preview <theme-dir>/hotspot-preview.svg
   ```

If validation fails, repair only the reported state and rerun the build. Do not overwrite an existing `.cape` file unless `--force` is intentional.

## Install-ready delivery

Deliver only the confirmed platform. For macOS, include the `.cape`, all Retina PNG representations, `manifest.json`, the user-facing `preview.png`, and `hotspot-preview.svg`. Keep `preview.svg` only as an optional internal/editable source; never present it as the approval preview. For Windows, include the 15 `.cur` files, `install-current-user.ps1`, `restore-default.ps1`, and `README-Windows.md`. Inspect the hotspot preview before delivery; if a cross is not on the intended functional point, repair that state instead of shipping it. Verify a macOS cape has `HiDPI: true` and four PNG representations per cursor at 32, 64, 160, and 320 pixels.

After preview approval, platform confirmation, and packaging, always give a complete tutorial in the final response. Follow [references/complete-tutorial.md](references/complete-tutorial.md) exactly: state the actual delivered filenames first, then give the confirmed platform’s “from download to apply”, immediate verification, troubleshooting, and restore steps. Do not merely say “see the README”, do not make the user guess which file to open, and do not combine platform archives. The tutorial must explicitly distinguish common states (arrow, text, action, window-edge resizing) from low-frequency states (busy, unavailable, handwriting), so a user does not mistake app-specific cursor behavior for a broken skin.

Describe the four core states (`normal`, `text`, `action`, `forbidden`) as the reliable package baseline. State that the package also maps exact directional resize, wait, drag, zoom, help, and system-arrow aliases. Explain the remaining boundary precisely: macOS apps request cursor types independently, and apps that draw their own cursor or keep using the normal arrow cannot be overridden by Mousecape. A disabled button or close button commonly remains an arrow because it has not requested `forbidden`.

For modern macOS, direct the user to the official upstream [Mousecape SwiftUI Releases](https://github.com/sdmj76/Mousecape-swiftUI/releases) page instead of the obsolete Mousecape 1813 build. **Never download Mousecape into the generated theme directory, bundle it in a delivery archive, mirror it, or redistribute its application binary.** Mousecape has its own non-commercial/no-redistribution license; users must obtain it from the upstream project and review those terms themselves. Never claim the app is installed or applied unless it actually was. Explain Gatekeeper recovery (`control`-click → Open) only if macOS blocks the app. If an install step fails, report the exact screen message and proceed with the corresponding troubleshooting section in the installation reference.

Mention that Mousecape uses non-public macOS APIs, so compatibility can vary after a macOS update. Also explain that apps choose cursor types: a close button can still show the normal arrow if the app never asks for the forbidden cursor.

For Windows, target Windows 10 and 11 only. Explain that users must extract the package somewhere permanent, then voluntarily right-click `install-current-user.ps1` and choose **Run with PowerShell**. The script writes only current-user cursor values (`HKCU\\Control Panel\\Cursors`) and does not require administrator permission. Give the restoration step (`restore-default.ps1`) in the same answer. Do not promise every Windows application will show low-frequency Busy, AppStarting, No, or handwriting states.
