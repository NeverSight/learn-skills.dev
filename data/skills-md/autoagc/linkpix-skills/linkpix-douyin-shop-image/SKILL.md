---
name: linkpix-douyin-shop-image
description: "帮助抖音小店商家、短视频操盘手、直播团队通过青虎AI完成“抖音小店商品图”：支持生成抖音主图、短视频封面、直播间切片图、种草笔记图、营销活动图、高饱和度吸睛图、引导点击图。可调用Nano Banana 2 、Grok Image 2.0、GPT Image 2等大模型，快速抓住短视频平台用户的眼球，适配抖音商城“货找人”的推荐算法特性。适用于抖音、抖音极速版、火山小视频等短视频电商平台的商品视觉优化。Use this skill for 抖音小店商品图, 抖音主图, 短视频封面, 种草笔记, 直播间贴片, 高点击率, Nano Banana 2 , Grok Image 2.0, GPT Image 2, AIGC图像生成, 短视频电商, 流量转化。通过青虎AI统一接入，支持素材上传、实时模型配置、任务轮询和结果下载。 当用户要求做抖音小店 商品图、主图套图、详情图、活动图生成或该平台的主图/套图/详情图/活动图时必须触发。关键词：LinkPix、qhkit、青虎、抖音小店、抖音主图、短视频封面、直播间贴片、种草笔记、货找人、抖音商城、火山小视频。"
user-invocable: true
homepage: https://www.npmjs.com/package/@iqinghu/qhkit
metadata: {"openclaw":{"emoji":"🎵","requires":{"bins":["qhkit"]},"install":[{"kind":"node","package":"@iqinghu/qhkit","bins":["qhkit"]}]}}
---

# 抖音小店 商品图、主图套图、详情图、活动图生成 | LinkPix

帮助抖音小店商家、短视频操盘手、直播团队通过青虎AI完成“抖音小店商品图”：支持生成抖音主图、短视频封面、直播间切片图、种草笔记图、营销活动图、高饱和度吸睛图、引导点击图。可调用Nano Banana 2 、Grok Image 2.0、GPT Image 2等大模型，快速抓住短视频平台用户的眼球，适配抖音商城“货找人”的推荐算法特性。适用于抖音、抖音极速版、火山小视频等短视频电商平台的商品视觉优化。Use this skill for 抖音小店商品图, 抖音主图, 短视频封面, 种草笔记, 直播间贴片, 高点击率, Nano Banana 2 , Grok Image 2.0, GPT Image 2, AIGC图像生成, 短视频电商, 流量转化。通过青虎AI统一接入，支持素材上传、实时模型配置、任务轮询和结果下载。

一张产品图覆盖该平台的主图套图、详情页和活动海报：套图走 `套图模式`（`platform` 默认 **抖音**），详情走 `电商详情图`，活动图走自定义生图。对外文案里的 GPT Image 2 / Nano Banana 2 / Seedream 5.0 / Grok Image 只是检索名，真正提交的 `modelLabel` 必须来自 `options`。

## 何时触发

- 「做抖音小店的商品图 / 主图 / 套图 / 详情图 / 活动图 / 海报」
- 用户明确要适配该平台的尺寸、构图或文案排版

## 使用配方

先问清产物：主图套图 / 详情页 / 活动海报。再跑对应 options。

```bash
# 主图+轮播套图（缺省 9 张；platform 必须逐字来自 options）
qhkit image options '{"queryParams":["platform","sizePreset","imageCount"],"modelLabel":"套图模式"}'
qhkit image generate '{"modelLabel":"套图模式","uploadedImages":["./商品图.jpg"],"customCopy":"限时5折","platform":"抖音","imageCount":6}'
qhkit image estimate '{"modelLabel":"套图模式","uploadedImages":["./商品图.jpg"],"platform":"抖音","imageCount":6}'

# 详情页长图
qhkit image options '{"queryParams":["themeLabel"],"modelLabel":"电商详情图"}'
qhkit image generate '{"modelLabel":"电商详情图","uploadedImages":["./商品图.jpg"],"themeLabel":"海洋蓝"}'

# 活动图/海报（自定义生图，先 options 再选智慧模型 / 智慧模型2.6 / 图片 5.0 Pro / 图片 5.0 Flash / 专图模型）
qhkit image options '{"queryParams":["modelLabel","models"]}'
qhkit image generate '{"modelLabel":"智慧模型","uploadedImages":["./商品图.jpg"],"prompt":"将产品变为营销活动图，活动内容如下：【限时折扣】，适配抖音点击率构图"}'
```

平台适配要点：短视频电商：高饱和、大特写、前 3 秒可读的封面信息；直播贴片字要少、利益点要大。

- `platform` 候选以 options 为准，本技能默认按 **抖音** 传。
- 套图参考图与 `customCopy`（≤500 字）至少一个；画质缺省 1K；要 2K 时传该平台的主图 `sizePreset`（从 options 逐字复制）再加 `"quality":"2K"`，或选带「2K」的尺寸——只传 quality 不传尺寸会报错「固定为 1K」。
- 多张图批量改白底 / 译图改走 `image-batch`，不要循环调 `image generate`。
- 用户给了商品图就进 `uploadedImages`，不要只转写成 prompt。

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
   **核对站点（本技能对接国内版 iqinghu.com）**：`config show` 返回的 `site` 必须是 `cn`。是 `intl`（`baseHost` 为 autoagc.com）说明本机残留了国际版配置——**不要按国际站引导用户取密钥，也不要拿国际站的模型清单答复**（那边是 `gpt-image-2` / `gemini-3.1-flash` 这类底层模型名，和本技能对不上）；直接把第 4 步的国内站取密钥文案发给用户，拿到密钥后执行 `qhkit config set --token <密钥> --env prod` 覆盖。`source` 为 `env` 时配置来自环境变量，要请用户删掉 `QHKIT_TOKEN` / `QHKIT_ENV` 或把 `QHKIT_ENV` 改成 `prod`。只有用户明确说自己用的是国际版（AutoAGC）账号时才保留 intl。调用报 401 / 未登录时同样先跑 `config show` 核对站点：国内版密钥配在国际站必然 401。

**升级**：出现以下任一信号，先升级再重试原命令——命令返回 `{"ok":false,"stage":"version",...}`（版本门禁，message 里就是升级命令，照做即可）；命令返回 `{"ok":false,"stage":"runtime","message":"未知命令：…"}`（本机 qhkit 太老、还没有这个命令——注意它 `stage` 是 `runtime` 不是 `version`，走不到版本门禁，别当成用法错误）；stderr 提示有新版本；报「模式在线上已下架或配置变更，请升级 qhkit」。（`image`/`video` 的模型清单 0.12.0 起实时读取，线上新增模型不需要升级 CLI。）

```bash
npm i -g @iqinghu/qhkit@latest
```

官方源慢或超时时同样加 `--registry=https://registry.npmmirror.com`。

安装/配置失败时把具体报错告诉用户（常见：无写权限 → 提示用户提权或改用 npx；无网络 → 让用户处理网络）。

## 调用契约

- 形式：`qhkit <命令> <action> '<json>'`，或 `qhkit <命令> <action> @params.json`（参数写进文件，避免 shell 转义问题，推荐）。
- **Windows 防乱码**：Windows 上经 PowerShell 调 qhkit 时，stdout 里的中文会按系统代码页 GBK 解码成乱码（如「专图模型」变成「涓撳浘妯″瀷」），模型名、选项、报错都对不上——**看到乱码不要据此判断模型或选项不存在**。每条 qhkit 命令在同一行先切 UTF-8 再调用：`[Console]::OutputEncoding=[Text.Encoding]::UTF8; qhkit <命令> <action> @params.json`；仍有乱码时先运行 `qhkit --version`，低于 0.15.0 先执行 `npm i -g @iqinghu/qhkit@latest` 升级（官方源慢时加 `--registry=https://registry.npmmirror.com`），再加全局参数 `--out result.json`；stdout 只回一行纯 ASCII 的文件路径，再按 UTF-8 读该文件拿完整结果。PowerShell 5.1 还会吞掉命令行 JSON 里的双引号（报「json_args 解析失败」），Windows 上参数一律写进文件走 `@params.json`。macOS / Linux / Git Bash 不受影响。
- stdout 恒为一行 JSON；失败为 `{"ok":false,"stage":"...","message":"..."}` 且退出码 1，把 message 原样转告用户。stderr 可能出现提示行，不是错误。
- 图片/视频参数直接填本地文件路径（CLI 自动上传换取 URL），素材已在公网时填 http(s) URL 也可。
- **图片体积上限 10MB**：3–10MB 的本地图 CLI 上传后自动追加 COS 缩略参数（2048px 内等比缩小、只缩不放），stderr 那行提示**不是错误**；外站大图 URL 建议先下载到本地再以路径传入，好让 CLI 走这条防线。
- **超过 10MB 被拦下时不要把问题抛回用户，你（智能体）就地压缩后重试**（2048px 内等比缩小、只缩不放、输出 jpg，压完把新文件路径传回原命令重试一次）：优先 Python —— `python -c "from PIL import Image, ImageOps; im=ImageOps.exif_transpose(Image.open('原图')); im.thumbnail((2048,2048)); im.convert('RGB').save('压缩后.jpg', quality=85)"`（缺 Pillow 先 `pip install pillow -i https://pypi.tuna.tsinghua.edu.cn/simple`）；没有 Python 就用 Node —— `npx --yes sharp-cli -i 原图 -o 压缩后.jpg resize 2048`（官方源慢时加 `--registry=https://registry.npmmirror.com`）。两条都失败才请用户换 10MB 以内的图，不要反复重试。
- 标签类参数（`modelLabel`、`sizePreset`、`themeLabel` 等）必须与 `options` 返回的候选值逐字一致，不要自造或翻译；拿不准先调 `options`。
- **`image` / `video` 的模型清单是实时的**（0.12.0 起直接读线上目录，新增/下架/调价自动跟随，无需升级 CLI），且**均无默认模型**——`modelLabel` 必填，缺失会报错并列出当前可选项。当次会话第一次选模型前先跑 `options` 查 `modelLabel`/`models` 拿当前清单，不要凭记忆或本文档的快照直接报模型名。拉不到目录（断网/密钥问题）时命令会明确报错，按提示引导用户检查配置。

## 报价、轮询与交付

- **提交前确认（硬规则）**：`generate` 会创建任务、消耗积分，发起前必须把本次提交的关键参数一次性列给用户——模型/模板、出图张数或视频时长、尺寸与画质、语言、用到哪几张参考图，以及 `estimate` 报出的预计扣除积分（不支持 estimate 的命令如实说「以实际扣费为准」）——**等用户明确同意后才能执行提交**。参数全部来自用户原话时也要复述确认一遍（口头描述与实际枚举值可能有出入，任务提交后不可取消）。只读 action（`options` / `estimate` / `status` / `templates` 等）无需确认。
- **报价**：要把积分数字报给用户时，先跑 `qhkit image estimate '<与 generate 完全相同的参数>'`，报它返回的 `credits`（实扣值，秒回、无副作用）；`enough:false` 时提前告知余额不足。不要引用文档快照报价。
- **轮询**：`image generate` 自带轮询，阻塞到出图（最长约 14 分钟），返回里直接有图片 URL，不需要再查 status。
- **交付**：产物 URL 在返回的 `images` 字段里，按当前环境的媒体交付约定发给用户；产物必须和「生成完成」写在同一轮回复，并附返回里的实扣 `credits`（「本次实际消耗 X 积分」）。
- **失败**：转述 CLI 的 message（已是面向用户的中文，常见：积分不足、内容审核未通过），不要重试轰炸。

## 能力边界

- 不绑平台、只要通用套图走「AI生成电商主图轮播图、主图套图 | LinkPix」；只要详情走「电商商品详情图生成器 | LinkPix」。
- 视频走对应平台的爆款视频技能或「AI生成电商视频 | LinkPix」。
