---
name: cell-lct-image
description: Use Image 2 through a user-configured OpenAI-compatible relay to generate scientific raster references for cell-lct, including text-to-image and reference-image editing.
---

# Cell-lct Image

当前最新稳定版为 `v1.2.5`。

使用本技能同级 `scripts/cell_lct_image.py` 调用 OpenAI-compatible Image API，为 `$cell-lct` 生成 PNG 参考图。本技能负责 Image 2 生图，不负责 SVG 矢量化或 Illustrator 播放。

中转站地址和密钥分别来自 `CELL_LCT_IMAGE_BASE_URL` 与 `CELL_LCT_IMAGE_API_KEY`；不得在代码、Skill、命令行或聊天中写入实际值。

## 专用边界

- 用于为 cell-lct 工作流生成或编辑科研参考图；需要最终可编辑矢量时，把成功 PNG 交给 `$cell-lct`。
- 透明背景、抠图或 Alpha 通道验证需求使用原生 Image-Gen，不为本技能增加后处理流程。

## 调用规则

- 先从当前 `SKILL.md` 推导技能目录和同级脚本路径；此阶段不得联网。
- 先确认 `python --version` 可执行且不低于 3.11；否则在 Codex Desktop 调用 `load_workspace_dependencies`，使用其返回的 Python executable。不得读取脚本源码或猜测替代命令。
- 确定子命令、`--model`、`--size`、`--quality`、数量和 `--output-dir` 后，才为该最终命令申请一次联网权限。
- 每个最终命令都必须在执行前确定一个本次调用唯一的绝对 JSON 回执路径，并通过 `--result-file` `<绝对路径>` 传给脚本。该路径必须保留在当前对话中，不能依赖命令输出找回。
- 文生图使用 `generate --prompt`。
- 参考图生图使用 `edit --prompt --reference <绝对图片路径>`；可重复传入多个 `--reference`。
- 指定文字生图使用 `text --text --description`，并把文字语言、位置和样式传给 `--language`、`--position`、`--style`。
- 直接执行同级 `scripts/cell_lct_image.py`；不得使用 `python -c`、内联 Python 或动态拼接 Python 源码。
- 在 PowerShell 中，把提示词、指定文字和描述等动态文本参数放在单引号内；参数内容中的单引号写成两个单引号。例如 `--text 'O''Reilly 夏日$特惠'`。`$`、反引号和双引号在这种写法中会按原文传入。
- 文字生图固定使用 `text` 子命令，不要手动为指定文字添加引号；脚本会在 `build_text_prompt()` 中构造逐字准确约束。
- 执行时以技能目录中的 `scripts/cell_lct_image.py` 为脚本路径。脚本成功时 stdout 只返回生成 PNG 的绝对路径；失败诊断和重试提示写入 stderr。创建请求不会自动重试，网络失败时生成状态未知。读取请求仅在首次出现 `DNS 解析失败`、`TLS 连接失败`、`连接被拒绝`或`代理连接失败`时最多自动重试 1 次；`网络连接超时`、连接中途关闭和通用网络失败不自动重试。

## 快速执行

- 用户在同一条指令中明确要求多张图片，即构成整批生成授权；不得逐张重复确认。
- 同一提示词生成多个版本时，在 `generate`、`text` 或 `edit` 后传 `--count 1..10`。
- 多个不同提示词使用一次 `batch` 命令，并为每项重复传入 `--prompt`；每批最多 4 项。
- 普通文生图与参考图编辑原样传递用户提示词，不复述、不扩写、不补充创意元素。
- `text` 只由脚本追加固定的逐字准确约束。
- 参数和输出目录确定后直接执行一个最终命令，不先描述构图方案。

## 结果交付

- 命令仍在运行时继续等待，不得扫描输出目录、推断生成数量或启动第二次生成。
- 已取得完整 stdout、stderr 和退出码时，以 stdout 的 PNG 绝对路径为成功结果，并依据 stderr 和退出码报告批次状态。
- 若实际返回图片数量与请求数量不一致，无论多于还是少于预期，都不得丢弃已返回的图片；逐一验证所有返回路径后全部交付，并将数量异常作为 `partial` 状态和安全诊断报告。
- 命令执行通道已结束但没有返回完整 stdout、stderr 和退出码时，使用一次不联网的文件读取操作读取该回执；不得重新执行生图命令。
- 回执必须是版本 `1` 的完整 JSON，`status` 只能是 `success`、`partial` 或 `error`，`exit_code` 必须是整数，`paths` 必须是本次调用返回的 PNG 绝对路径列表，`errors` 必须是字符串列表。`success` 必须对应退出码 0，`partial` 必须对应非零退出码和非空 `paths`，`error` 必须对应非零退出码和空 `paths`。逐一校验回执指定的路径存在且为 PNG 后，按回执交付成功图片和安全诊断。
- 回执不存在、无法解析或校验失败时，只报告“命令结果通道和结果回执均不可用，执行状态未知。”；不得扫描输出目录、按文件数量或时间戳推断结果。回执中的 `paths` 无论数量是否符合请求，都必须逐一验证并全部交付；数量异常只影响状态和诊断，不得造成路径截断。
- stdout 中的每一行都是成功 PNG 的绝对路径；逐张用 Markdown 图片链接展示。
- 若 stderr 包含 `RETRY_NOTICE:` 且 stdout 包含成功 PNG，先展示全部成功图片，再附注“首次失败原因：<安全分类>；自动重试一次后成功。”；不得把该提示当作批次失败。
- stderr 中的批次项错误只做简要报告；部分失败时仍展示全部成功图片。
- 只校验返回数量、PNG、绝对路径和批次状态，不得进行视觉检查。
- 不得自动调整提示词、重新生成、在脚本之外重试创建请求、把单请求多图改为并发单图，或在结果通道丢失时重复执行原命令。

## 参数选择

用户明确指定的 `model`、`size`、`quality` 优先，原样传递。未指定时按以下规则选择：

| 参数 | 默认 | 关键词与场景 |
| --- | --- | --- |
| `model` | `gpt-image-2` | 默认模型；可选 `gpt-image-1`、`gpt-image-1.5`、`gpt-image-2`。 |
| `size` | `1536x1024` | `1024x1024` 用于方图、1:1、头像、单品、图标；`1536x1024` 用于横图、宽幅、风景、场景、多人、电影感；`1024x1536` 用于竖图、竖版、海报、全身、手机壁纸、书封。 |
| `quality` | `standard` | `low` 用于草图、快速、分镜、试构图；`standard` 用于常规、通用、日常；`high` 用于高质量、精细、主视觉、细节、文字清晰。 |

`1536x1024` 为 3:2，不是严格的 16:9。用户只要求 16:9 而未给出实际 `size` 时，说明该可选尺寸中最接近的是 `1536x1024`。

## 缺少密钥

若脚本报告配置缺失，不要让用户在聊天中粘贴密钥，也不要显示或记录密钥。使用以下 PowerShell 配置，并提示用户完全退出并重新打开 Codex 后重试：

```powershell
$OutputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$baseUrl = Read-Host "请输入 Image 2 中转站地址"
[Environment]::SetEnvironmentVariable("CELL_LCT_IMAGE_BASE_URL", $baseUrl, "User")
$secureKey = Read-Host "请输入 Image 2 API 密钥" -AsSecureString
$plainKey = [System.Net.NetworkCredential]::new("", $secureKey).Password
[Environment]::SetEnvironmentVariable("CELL_LCT_IMAGE_API_KEY", $plainKey, "User")
Remove-Variable plainKey, baseUrl
Write-Host "配置完成。请完全退出并重新打开 Codex，然后重新发送生图请求。"
```

中转站应提供 `/images/generations` 和 `/images/edits`。若接口实际路径包含 `/v1`，将 `/v1` 包含在 `CELL_LCT_IMAGE_BASE_URL` 中。
