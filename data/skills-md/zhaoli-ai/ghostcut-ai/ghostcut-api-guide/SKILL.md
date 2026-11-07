---
name: ghostcut-api-guide
slug: ghostcut-ai-skill
displayName: GhostCut鬼手剪辑-助力短剧ai剧视频出海
version: 1.0.9
summary: GhostCut API 指引 Skill 面向视频译制、内容出海和多媒体本地化场景，帮助 AI Agent 调用 GhostCut 完成字幕提取、字幕擦除、翻译配音、背景音乐处理、批量合成与字幕压制等流程。同时覆盖图片翻译、图片文字擦除等图像处理能力。Powered by GhostCut.
license: MIT
description: GhostCut API 指引 Skill 面向视频译制、内容出海和多媒体本地化场景，帮助 AI Agent 调用 GhostCut 完成字幕提取、字幕擦除、翻译配音、背景音乐处理、批量合成与字幕压制等流程。同时覆盖图片翻译、图片文字擦除等图像处理能力。Powered by GhostCut.
---

# GhostCut API 指引

本文是安装后的 skill 主说明，面向执行任务的 Agent。安装命令、分发说明和给新用户看的仓库级入口在仓库根目录的 `skills.md`；本文只维护 Agent 运行时必须遵守的文档地图、功能路由、参数强规则和维护规则。

使用本 skill 时，必须基于随附的 GhostCut API 指引文档工作，不要凭记忆猜测接口路径、字段名、ID 含义、任务类型、语言代码或结果查询流程。

## 参考文档地图

详细文档位于 `references/api-guide/`。当用户新安装 skill、首次接入或想先跑通最小示例时，先读 `references/api-guide/01-quickstart.md`。当用户目标较宽泛，或还不确定应该调用哪个接口时，先读 `references/api-guide/llms.txt`。当用户只是想体验功能但没有素材时，读 `references/sample-assets.md`，可提供演示视频或图片 URL，并明确说明它不是业务默认素材。

核心入口：

- `references/api-guide/00-api-overview.md`：总览、功能选择、主要调用流程和文档路由。
- `references/api-guide/01-quickstart.md`：5 分钟快速上手，使用示例 payload 跑通视频去文字任务和状态查询。
- `references/api-guide/02-auth-and-sign.md`：`AppKey`、`AppSecret` 获取方式、`AppSign` 签名规则和鉴权错误。
- `references/api-guide/03-media-requirements.md`：视频、图片、SRT 的 URL、格式、本地上传和批量数量要求。
- `references/api-guide/10-file-upload.md`：本地视频、SRT、图片上传，获取后续接口可用的 URL，并查看视频素材状态枚举。
- `references/api-guide/11-work-status-query.md`：查询 `/v-w-c/gateway/ve/work/status`，读取视频作品结果。
- `references/api-guide/12-point-balance-query.md`：查询当前 `AppKey` 对应商户的有效点卡余额。
- `references/api-guide/27-video-basic-processing.md`：视频基础剪辑、截取、分辨率、智能优化、滤镜、镜像、缩放和画面移动。
- `references/api-guide/13-language-support.md`：不同功能支持的语言。
- `references/api-guide/14-video-process-status.md`：`processStatus` 与公共错误码。
- `references/api-guide/15-async-and-callbacks.md`：异步任务、轮询策略、callback 回调格式、`Callback-Sign` 验签、重试和幂等规则。
- `references/api-guide/51-series-overview.md`：译制出海模块入口。
- `references/api-guide/52-series-edit-common-task-structure.md`：译制出海通用请求结构、字段来源和 Python 提交通用模板。
- `references/api-guide/53-series-edit-task-list.md`：译制出海 `task/list` 任务查询。
- `references/api-guide/59-series-edit-errors-and-checklist.md`：译制出海错误示例和提交前检查。
- `references/sample-assets.md`：缺少素材时可选的演示视频、图片 URL 和使用限制。
- `examples/`：可复制的最小请求体和环境变量模板。

通用基础：

- 凭证与签名：`02-auth-and-sign.md`。
- 素材 URL 与格式要求：`03-media-requirements.md`。
- 文件上传和视频素材状态枚举：`10-file-upload.md`。
- 视频任务状态查询：`11-work-status-query.md`。
- 点卡余额查询：`12-point-balance-query.md`。
- 语言支持：`13-language-support.md`。
- 处理状态和错误码：`14-video-process-status.md`。
- 异步任务、轮询和回调：`15-async-and-callbacks.md`。

视频 AI 处理：

- 去字幕/去文字：`21-erase-video-subtitle.md`，遮罩框规则见 `22-inpaint-masks-supplement.md`。
- 字幕压制：`23-burn-subtitles.md`，字幕样式细节见 `26-subtitle-style-and-fonts.md`。
- OCR 字幕提取：`24-ocr-subtitle-extraction.md`。
- ASR 字幕提取：`25-asr-subtitle-extraction.md`。
- 视频基础处理：`27-video-basic-processing.md`。
- 背景音乐去除/分离：`30-background-music-separation.md`。
- 视频翻译并重新配音：`31-video-voice-translation.md`，公共音色见 `32-public-voice-characters.md`；默认优先保留原视频背景音，原视频有硬字幕时优先考虑同一次请求组合字幕擦除参数。

图片 AI 处理：

- AI 图片处理：`81-image-processing.md`，包含图片文字擦除、图片翻译、翻译结果二次微调和重新合成。

译制出海功能：

- 字幕提取：`54-series-subtitle-extract.md`。
- 字幕擦除：`55-series-subtitle-inpaint.md`。
- AI 配音：`56-series-dubbing.md`。
- 字幕压制：`57-series-subtitle-burn.md`。
- 音频分离：`58-series-audio-separate.md`。
- 项目与视频素材：`60-series-project-and-video-materials.md`。
- 字幕素材与 `slInfo`：`61-series-subtitle-materials.md`。
- 字幕翻译：`62-series-subtitle-translation.md`。
- 翻译术语库：`63-series-translation-glossary.md`。
- 多作品合并：`64-series-video-merge.md`。
- 剧集角色管理：`65-series-character-management.md`。

## 使用流程

1. 新用户首次上手或想先跑通最小闭环时，先读 `01-quickstart.md`，可使用 `examples/video-inpaint-advanced-lite-fullscreen.payload.json` 创建视频去文字任务。
2. 先判断用户要调用的是普通单视频 API，还是译制出海模块。默认优先使用普通单视频 API；只有用户明确提到“译制出海”、短剧/AI 剧出海、剧集、项目级素材、批量剧集处理、`idSeries` 或 `idMaterialVideo` 时，才推荐译制出海模块。
3. 普通单视频任务先读 `00-api-overview.md`；签名鉴权问题读 `02-auth-and-sign.md`；素材 URL、格式和上传约束读 `03-media-requirements.md`；译制出海任务先读 `51-series-overview.md`。
4. 组装参数前必须阅读对应功能文档，不要从记忆推断接口路径或字段名。
5. 保持文档中的请求层级。常规译制出海剪辑任务使用 `items[]`、`workDto`、`videoEditParamsDto`；多作品合并使用 JSON 字符串 `data` 中的 `episodes[]`。
6. 如果用户提供本地文件路径，先读 `10-file-upload.md` 完成上传；任务创建接口通常需要 URL 或素材 ID，不直接接收本地路径。
7. 涉及语言字段时，读 `13-language-support.md`，不要凭常识猜测语言代码。
8. 按正确流程查询状态和结果：
   - 普通单视频任务：创建任务后拿作品 ID，再调用 `/v-w-c/gateway/ve/work/status`。
   - 译制出海任务：先调用 `task/list`；如果需要作品 ID、播放地址或作品详情，用 `task/list.body[].id` 作为 project/task ID 调用 `/v-w-c/gateway/ve/work/status`，再从 `body.content[].id` 读取作品 ID。

## 快速路由

- 用户给本地文件路径：读 `10-file-upload.md`，需要实际上传时可用 `scripts/ghostcut_api.py upload`。
- 用户第一次使用 skill、想快速跑通 API 或要求最小示例：读 `01-quickstart.md`，优先使用 `examples/video-inpaint-advanced-lite-fullscreen.payload.json`。
- 用户没有视频或图片但想体验：读 `references/sample-assets.md`，按目标提供演示视频或图片 URL，并提醒依赖语音、字幕、剧集上下文或真实排版质量的功能应换成真实素材。
- 用户问 API Key、`AppKey`、`AppSecret`、凭证在哪里获取、如何签名或如何鉴权：读 `02-auth-and-sign.md`。
- 用户问账户余额、点卡余额、可用点数、剩余点数或商户余额：读 `12-point-balance-query.md`。
- 用户问视频/图片格式、URL 不能包含中文、本地文件是否能直接传、批量 `urls` 数量限制：读 `03-media-requirements.md`。
- 用户问视频素材状态、上传状态、转码状态，或普通上传 / 译制出海上传后的 `processStatus`：读 `10-file-upload.md` 的视频素材状态枚举；不要套用 `/work/status` 的作品处理状态表。
- 用户要查询普通单视频结果：读 `11-work-status-query.md`，需要实际查询时可用 `scripts/ghostcut_api.py work-status`。
- 用户要了解异步任务、轮询策略、callback 回调、`Callback-Sign` 验签、重试或幂等：读 `15-async-and-callbacks.md`。生产接入优先推荐 `callback`，轮询作为主动查询和补偿兜底。
- 用户要做视频基础剪辑、截取、分辨率、智能优化、滤镜、镜像、缩放或画面移动：读 `27-video-basic-processing.md`。
- 用户要做视频语音翻译、译制或重新配音：读 `31-video-voice-translation.md`；默认使用 `removeBgAudio=0` 保留原视频背景音。只有用户明确要求静音、不要原声、去背景音乐或只保留 AI 语音/环境音时，才改用 `removeBgAudio=1` 或 `2`。如果原视频画面已有硬字幕，读组合场景；语音翻译和字幕擦除通常在同一次 `/work/free` 请求中组合参数，不要默认拆成两次处理。
- 用户只说视频翻译、视频配音、电商短视频、本地化、多语言字幕、去字幕或字幕压制，但没有明确说“译制出海”、短剧/AI 剧出海、剧集、项目级素材或 `idSeries`：默认走普通单视频视频 AI 处理文档，不主动推荐译制出海方案。
- 用户要查询译制出海任务：读 `53-series-edit-task-list.md`，需要实际查询时可用 `scripts/ghostcut_api.py task-list`。
- 用户要基于前序译制出海结果继续处理：先查 `task/list` 拿任务 ID，再查 `/work/status` 拿 `body.content[].id` 作为作品 ID。
- 用户要把同一剧集下多个已有作品合成长视频：读 `64-series-video-merge.md`；按 `data.episodes[]` 顺序提交作品 ID。创建响应 `body` 已是合并后作品 ID，可直接查询 `/work/status`。
- 用户要创建、查询、更新、删除、恢复或复制译制出海剧集角色：读 `65-series-character-management.md`；角色列表对象的 `id` 对应 `id_ve_character`。
- 用户要译制出海配音：至少读 `51-series-overview.md`、`52-series-edit-common-task-structure.md`、`56-series-dubbing.md`；涉及音色时读 `32-public-voice-characters.md`；涉及字幕样式时读 `26-subtitle-style-and-fonts.md`。
- 用户要处理图片文字、图片翻译、图片文字擦除、图片翻译精修或 Image Redo：读 `81-image-processing.md`；涉及本地图片时先读 `10-file-upload.md`；涉及语种时读 `13-language-support.md`。

## 强规则

- GhostCut 网关接口的响应体业务成功码统一按 `code == 1000` 判断；不要把 HTTP 200 与响应体业务 `code` 混淆。
- 不要把 `task/list.body[].id` 当成作品 ID。它是任务 ID，也可理解为 project ID。
- 后续译制出海任务需要 `workDto.materialWorkIds` 时，取 `/work/status.body.content[].id`。
- 多作品合并不使用 `items[]`、`workDto` 或 `videoEditParamsDto`；顶层 `data` 必须是包含 `episodes[]` 的 JSON 字符串。
- 不要把 `idRelation` 当成业务字段使用。
- 没有明确译制出海意图时，不推荐译制出海模块；普通视频翻译、配音、字幕擦除、字幕压制、电商短视频本地化等泛需求默认使用 `/v-w-c/gateway/ve/work/free` 的视频 AI 处理方案。
- 译制出海 AI 配音和字幕压制中，`workDto.idVeMaterialSrt` 和 `workDto.extraOptions.customer_input.content[]` 都要传；不能完全不传字幕，也不要只传其中一个。
- `workDto.idVeMaterialSrt` 来自译制出海字幕素材：本地 SRT 上传的 `body.idMaterialSrt`、`series/srt/create` 的 `body.id`、字幕提取/字幕翻译后通过 `series/srt/list` 查询到的 `body[].id`，或字幕复制/字幕列表查询返回的 `body[].id`。
- 经典配音模式使用 `wyTaskType=FULL`，并传 `character_voices[]`。
- 情感克隆模式使用 `wyTaskType=VOICE_CLONE_PRO`，不传 `character_voices[]`。
- `voice_type=CLONE` 表示经典模式下的超真实音色，不表示情感克隆模式。
- 公共音色统一使用 `character_voices[].id_ve_voice_character`，取值来自 `voicecharacter/aggregate/list` 返回的 `body[].id`。
- `id_ve_character` 是当前剧集中的业务角色 ID，来自剧集角色列表或字幕角色信息；`id_ve_voice_character` 是公共音色 ID。两者不能互换。
- 译制出海 AI 配音是否需要先做字幕擦除，取决于原素材是否已无硬字幕，以及本次配音是否已通过 `workDto.materialWorkIds` 复用字幕擦除后的作品；如果两者都不是，应询问用户是否需要先创建字幕擦除任务。
- 普通单视频语音翻译和重新配音默认传 `removeBgAudio=0`，优先保留原视频背景音；不要默认使用 `removeBgAudio=1` 全局静音。
- 普通单视频的语音翻译 + 字幕擦除可以在同一次 `/v-w-c/gateway/ve/work/free` 请求中组合参数；不要默认先擦除再翻译，除非用户明确要求分两步处理。
- 字幕擦除遮罩框和 OCR 框使用 `0` 到 `1` 的相对坐标，点序为左上、右上、右下、左下。

## 可用脚本

脚本位于 `scripts/`，用于减少重复签名、上传和查询代码。运行脚本前先按 `02-auth-and-sign.md` 获取凭证并设置环境变量；不要把真实密钥写入文档或提交到仓库。

常用命令：

- `python scripts/ghostcut_api.py sign --payload payload.json`：为 JSON 请求体生成 `AppSign`。
- `python scripts/ghostcut_api.py post --path /v-w-c/gateway/ve/work/status --payload payload.json`：发送签名后的 GhostCut JSON 请求。
- `python scripts/ghostcut_api.py upload --file /path/input.mp4 --material-file-type video`：上传本地文件，输出 URL 和 OSS key。
- `python scripts/ghostcut_api.py work-status 521461135`：查询 `/v-w-c/gateway/ve/work/status` 并汇总状态和常见结果 URL。
- `python scripts/ghostcut_api.py point-balance`：查询当前 `AppKey` 对应商户的点卡余额。
- `python scripts/ghostcut_api.py task-list --id-series 10001 --task-type-in SERIES_CLIP2 SERIES_CLIP3`：查询译制出海任务列表。

最小示例：

- `examples/.env.example`：环境变量模板。
- `examples/video-inpaint-advanced-lite-fullscreen.payload.json`：视频去文字高擦 Lite、全屏框选创建任务请求体。
- `examples/work-status.payload.json`：普通视频任务状态查询请求体。
- `examples/image-translate.payload.json`：图片翻译创建任务请求体。

维护快照时使用：

- `python scripts/sync_api_guide.py --check`：检查当前 `references/api-guide/` 快照目录是否存在，并确认 `llms.txt` 索引覆盖所有 Markdown 文档。
- `python scripts/sync_api_guide.py --check --source /path/to/api-guide`：如另有外部源文档目录，显式指定后对比它与 skill 快照是否一致。
- `python scripts/sync_api_guide.py --source /path/to/api-guide`：如另有外部源文档目录，显式指定后同步到 skill 快照。

## 文档编写与维护

更新随附 API 指引时，保持面向 Agent 的写法：

- 推荐稳定章节顺序：检查清单、使用流程、关键字段、请求体、完整 Python 示例、结果查询、Agent 决策规则、相关文档。
- Python 示例要能直接复制：包含 imports、凭证占位、签名函数、请求体、POST 调用和结果打印。
- 避免猜测性措辞、未完成占位、内部历史表述，以及业务流程中用不到的字段解释。
- 长表格和通用规则优先链接到共享文档，不要在多个功能文档里重复维护字幕样式、语言列表、状态枚举或遮罩框规则。
- 当前随附 API 指引直接维护在 `references/api-guide/`。只有存在外部源文档目录时，才使用 `sync_api_guide.py --source /path/to/api-guide` 做对比或同步。
