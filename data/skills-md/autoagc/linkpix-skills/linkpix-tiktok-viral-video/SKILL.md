---
name: linkpix-tiktok-viral-video
description: "TikTok 爆款带货视频生成。帮助跨境卖家、MCN机构、海外广告投放师通过青虎AI完成“TikTok 爆款带货视频生成”：可调用可灵Kling 3.0、阿里Wanx 3.0、MiniMax H3、Seedance 2.0、Seedance 2.5、HappyHorse 1.1等大模型，轻松生成多语言口播、卡点变装、搞笑短剧、跨境种草、信息流投放等视频类型，完美贴合TikTok病毒式传播和多国受众偏好。适用于TikTok Shop、TikTok Ads、东南亚及欧美站点等跨境短视频营销场景。Use this skill for TikTok爆款视频, 多语言口播, 卡点变装, 搞笑短剧, 跨境种草, 信息流投放, TikTok Shop, 病毒式传播, 全球化分发, MiniMax H3, Grok, Seedance, AIGC视频生成。通过青虎AI统一接入，支持素材上传、任务轮询和结果下载。 当用户要求做TikTok 爆款视频生成或TikTok带货/种草/投放短视频时必须触发。关键词：LinkPix、qhkit、青虎、TikTok爆款视频、TikTok Shop、多语言口播、卡点变装、搞笑短剧、跨境种草、TikTok Ads、病毒式传播。"
user-invocable: true
homepage: https://www.npmjs.com/package/@iqinghu/qhkit
metadata: {"openclaw":{"emoji":"▶️","requires":{"bins":["qhkit"]},"install":[{"kind":"node","package":"@iqinghu/qhkit","bins":["qhkit"]}]}}
---

# TikTok 爆款视频生成 | LinkPix

TikTok 爆款带货视频生成。帮助跨境卖家、MCN机构、海外广告投放师通过青虎AI完成“TikTok 爆款带货视频生成”：可调用可灵Kling 3.0、阿里Wanx 3.0、MiniMax H3、Seedance 2.0、Seedance 2.5、HappyHorse 1.1等大模型，轻松生成多语言口播、卡点变装、搞笑短剧、跨境种草、信息流投放等视频类型，完美贴合TikTok病毒式传播和多国受众偏好。适用于TikTok Shop、TikTok Ads、东南亚及欧美站点等跨境短视频营销场景。Use this skill for TikTok爆款视频, 多语言口播, 卡点变装, 搞笑短剧, 跨境种草, 信息流投放, TikTok Shop, 病毒式传播, 全球化分发, MiniMax H3, Grok, Seedance, AIGC视频生成。通过青虎AI统一接入，支持素材上传、任务轮询和结果下载。

平台向的电商视频总入口（第 1 批 `linkpix-ecom-video` 的拆分）：`qhkit video` 多模型成片 + `video-quick` 多图成片 + 需要分镜时 `storyboard`。默认画幅 **竖屏 9:16**，默认语言 **英语**。模型优先从目录里找：可灵3.0 Omni、MiniMax H3、Seedance2.0、Seedance2.5、Happy Horse 1.1。

## 何时触发

- 「做TikTok爆款视频 / 带货视频 / 种草视频 / 投放视频」
- 用户没点名具体模型、但明确要发 TikTok

## 使用配方

```bash
qhkit video options '{"queryParams":["modelLabel","models"]}'
# 在 models 里按名称匹配首选模型；modelLabel 必须逐字来自返回值（常带时长）
qhkit video generate '{"modelLabel":"Seedance2.0 15秒","prompt":"<按下方平台提示词改写>","uploadedImages":["./商品图.jpg"],"orientationLabel":"竖屏 9:16","languageLabel":"英语"}'
qhkit video status   '{"videoTaskId":"task-123"}'
qhkit video estimate '{"modelLabel":"Seedance2.0 15秒","uploadedImages":["./商品图.jpg"]}'
# 多图一键成片
qhkit video-quick generate '{"prompt":"<平台向卖点>","duration":15,"creative":"1","orientation":"portrait","language":"en","uploadedImages":["./图1.jpg","./图2.jpg"]}'
# 先写分镜再成片
qhkit storyboard script '{"uploadedImages":["./商品图.jpg"],"productName":"保温杯","pointDescription":"316不锈钢·24h保温"}'
```

平台提示词：病毒式前 3 秒钩子、卡点/变装/短剧都可以；默认英语，用户指定站点再换 `languageLabel`（西语/印尼语等）。信息流投放把卖点写进画面动作，不要只靠中文字幕。

- 用户没点名模型时，把首选列表里当前在架的 2–3 个（含单价）列给用户选，不要替用户拍板。
- 参考视频 / 参考音频是否可传以当次 `models` 为准。
- `orientationLabel` 必须来自该模型的候选；目录没有 竖屏 9:16 时改用最接近的竖/横屏并告诉用户。

## 环境自举（缺什么装什么，不要因环境缺失放弃任务）

本技能依赖 `qhkit` 命令（npm 包 `@iqinghu/qhkit`），可完全独立安装。按顺序检测，缺失就地补齐：

1. **有 qhkit 吗？** `qhkit config show` 能跑通即就绪，跳到第 4 步。
2. **没有 qhkit 但有 node/npm**（OpenClaw/Hermes 机器部署流程保证自带 Node 22+）→ 全局安装（推荐）：

   ```bash
   npm i -g @iqinghu/qhkit
   ```

   默认走 npm 官方源；官方源访问慢或超时（国内网络常见）时，再加镜像参数 `--registry=https://registry.npmmirror.com`（阿里维护的 npm 官方镜像，仅作网络兜底）。仅当全局安装因权限失败且无法提权时，才退而用 `npx @iqinghu/qhkit <命令> ...`（npx 必须写包全名）。
3. **连 node 都没有**（要求 Node ≥ 18）：先装 Node 再回到第 2 步。

   ```bash
   # Linux 二进制安装（装到用户目录，无需 root；先校验官方 SHA256 再解包）：
   cd /tmp && curl -fsSLO https://nodejs.org/dist/v22.22.3/node-v22.22.3-linux-x64.tar.xz
   cd /tmp && curl -fsSL https://nodejs.org/dist/v22.22.3/SHASUMS256.txt | grep ' node-v22.22.3-linux-x64.tar.xz$' | sha256sum -c -
   mkdir -p "$HOME/.local/lib" && tar -xJf /tmp/node-v22.22.3-linux-x64.tar.xz -C "$HOME/.local/lib"
   export PATH="$HOME/.local/lib/node-v22.22.3-linux-x64/bin:$PATH"
   ```

   校验行输出 `OK` 才继续；校验失败就删掉重下，**绝不解包未通过校验的文件**。nodejs.org 访问不通时，把两个下载 URL 的前缀 `https://nodejs.org/dist` 整体换成镜像 `https://registry.npmmirror.com/-/binary/node`（目录结构相同，SHASUMS256.txt 也有镜像，校验步骤不变）。`export PATH` 只对当前 shell 生效，跨命令调用时每个新 shell 都要先执行这行（或追加进 `~/.bashrc`）。macOS 用 `brew install node`；Windows 用 winget/官网安装包。arm64 机器把 `x64` 换成 `arm64`。
4. **密钥**：无密钥时（命令返回 `stage:"config"`），把下面的引导文案发给用户，拿到密钥后执行 `qhkit config set --token <密钥> --env prod`（或设环境变量 `QHKIT_TOKEN`）：
   > 1. 打开 https://www.iqinghu.com/workbench/login?type=1&urlCode=1788417527636 注册/登录
   > 2. 进入控制台 → 工作台的 APIKeys 页面：https://www.iqinghu.com/workbench/dashboard/api-keys
   > 3. 点「创建/复制」生成密钥，生成后将 API 密钥发我
   >
   > 图文获取密钥教程：https://xcnzsfe4uxrw.feishu.cn/wiki/KJ0Ywsyw8iAXmRkz5l4cddDbn6g
5. **自检**：`qhkit config show` 输出脱敏配置即全部就绪。

**升级**：出现以下任一信号，先升级再重试原命令——命令返回 `{"ok":false,"stage":"version",...}`（版本门禁，message 里就是升级命令，照做即可）；命令返回 `{"ok":false,"stage":"runtime","message":"未知命令：…"}`（本机 qhkit 太老、还没有这个命令——注意它 `stage` 是 `runtime` 不是 `version`，走不到版本门禁，别当成用法错误）；stderr 提示有新版本；报「模式在线上已下架或配置变更，请升级 qhkit」。（`image`/`video` 的模型清单 0.12.0 起实时读取，线上新增模型不需要升级 CLI。）

```bash
npm i -g @iqinghu/qhkit@latest
```

官方源慢或超时时同样加 `--registry=https://registry.npmmirror.com`。

安装/配置失败时把具体报错告诉用户（常见：无写权限 → 提示用户提权或改用 npx；无网络 → 让用户处理网络）。

## 调用契约

- 形式：`qhkit <命令> <action> '<json>'`，或 `qhkit <命令> <action> @params.json`（参数写进文件，避免 shell 转义问题，推荐）。
- stdout 恒为一行 JSON；失败为 `{"ok":false,"stage":"...","message":"..."}` 且退出码 1，把 message 原样转告用户。stderr 可能出现提示行，不是错误。
- 图片/视频参数直接填本地文件路径（CLI 自动上传换取 URL），素材已在公网时填 http(s) URL 也可。
- **图片体积上限 10MB**：3–10MB 的本地图 CLI 上传后自动追加 COS 缩略参数（2048px 内等比缩小、只缩不放），stderr 那行提示**不是错误**；外站大图 URL 建议先下载到本地再以路径传入，好让 CLI 走这条防线。
- **超过 10MB 被拦下时不要把问题抛回用户，你（智能体）就地压缩后重试**（2048px 内等比缩小、只缩不放、输出 jpg，压完把新文件路径传回原命令重试一次）：优先 Python —— `python -c "from PIL import Image, ImageOps; im=ImageOps.exif_transpose(Image.open('原图')); im.thumbnail((2048,2048)); im.convert('RGB').save('压缩后.jpg', quality=85)"`（缺 Pillow 先 `pip install pillow -i https://pypi.tuna.tsinghua.edu.cn/simple`）；没有 Python 就用 Node —— `npx --yes sharp-cli -i 原图 -o 压缩后.jpg resize 2048`（官方源慢时加 `--registry=https://registry.npmmirror.com`）。两条都失败才请用户换 10MB 以内的图，不要反复重试。
- 标签类参数（`modelLabel`、`sizePreset`、`themeLabel` 等）必须与 `options` 返回的候选值逐字一致，不要自造或翻译；拿不准先调 `options`。
- **`image` / `video` 的模型清单是实时的**（0.12.0 起直接读线上目录，新增/下架/调价自动跟随，无需升级 CLI），且**均无默认模型**——`modelLabel` 必填，缺失会报错并列出当前可选项。当次会话第一次选模型前先跑 `options` 查 `modelLabel`/`models` 拿当前清单，不要凭记忆或本文档的快照直接报模型名。拉不到目录（断网/密钥问题）时命令会明确报错，按提示引导用户检查配置。

## 报价、轮询与交付

- **提交前确认（硬规则）**：`generate` 会创建任务、消耗积分，发起前必须把本次提交的关键参数一次性列给用户——模型/模板、出图张数或视频时长、尺寸与画质、语言、用到哪几张参考图，以及 `estimate` 报出的预计扣除积分（不支持 estimate 的命令如实说「以实际扣费为准」）——**等用户明确同意后才能执行提交**。参数全部来自用户原话时也要复述确认一遍（口头描述与实际枚举值可能有出入，任务提交后不可取消）。只读 action（`options` / `estimate` / `status` / `templates` 等）无需确认。
- **报价**：`video` 命令要报积分时先跑 `qhkit video estimate '<与 generate 完全相同的参数>'`，报返回的 `credits`（实扣值）；`enough:false` 提前告知余额不足。其他视频命令不支持 estimate，如实说「以实际扣费为准」。
- **轮询**：`generate` 只提交，立即返回任务 ID；重复调 `status` 直到 `stage:"done"`（返回含产物 URL），间隔 30–60 秒。视频任务最长可达 40 分钟，提交后立即告知任务 ID 和耗时预期，不要提前放弃；任务不可取消，ID 要保留。
- **交付**：视频 URL 在 status 返回的 `videos`/`primaryVideo` 字段里，按当前环境的媒体交付约定发给用户；产物必须和「生成完成」写在同一轮回复，并附实扣 `credits`（generate 返回里带）。
- **失败**：转述 CLI 的 message（已是面向用户的中文，常见：积分不足、内容审核未通过、模型维护中），不要重试轰炸。

## 能力边界

- 用户点名了可灵 / Seedance / Wanx / MiniMax / HappyHorse / Grok，改走对应的模型专项技能。
- 复刻一条已有链接走对应模型的「爆款视频复刻」或「AI爆款视频复刻 | LinkPix」。
- 音乐/MV、数字人口播、直播切片、超长视频剪辑 qhkit 不支持，如实告知。
