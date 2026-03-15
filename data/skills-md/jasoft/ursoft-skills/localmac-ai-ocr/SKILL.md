---
name: localmac-ai-ocr
description: Use when 需要在 macOS 本机或 RDP 场景下抓屏、识别中文界面文字与坐标、按文字定位并点击界面，尤其适合远程桌面窗口、行情软件、自选列表、按钮输入框定位和截图取字。
metadata:
    openclaw:
        requires:
            env:
                - AISTUDIO_OCR_TOKEN
                - AISTUDIO_OCR_API_URL
            bins:
                - uv
                - python3
                - osascript
                - sips
        primaryEnv: AISTUDIO_OCR_TOKEN
---

# Localmac AI OCR

## 概览

这个 skill 用来协同两个现成命令行工具：

- `scripts/gui` 负责窗口激活、截图、坐标点击、键盘输入
- `scripts/ocr` 负责调用 AI Studio OCR 输出文字、分数、坐标框，并支持按文本查找和点击

优先使用云端 `aistudio-ocr`。除非用户明确要求，不要回退到本地 Paddle，以免慢且占用内存。

不要把真实的 `API key`、`token`、`api url` 写进 skill、脚本调用示例或仓库文件。统一要求从环境变量或命令参数读取。

这个 skill 自带可执行脚本，安装后不依赖业务仓库本身。当前说明默认命令从 skill 根目录执行即可。

可执行入口在：

```bash
scripts/ocr
scripts/gui
```

首次安装建议运行：

```bash
scripts/setup.sh
```

## 何时使用

- 用户要你操作本机 GUI、RDP 窗口或桌面 App
- 需要从截图中提取中文文本和坐标框
- 需要“先截图，再识别，再按文字点击”
- 需要验证 OCR 速度、完整输出、命中框、标注图
- 需要在行情软件、表格界面、按钮密集界面里精确找字

不要在这些场景优先使用网页抓取或 DOM 自动化；先判断是不是桌面/RDP 界面。

## 工作流

### 1. 先确认命令入口

先确认脚本入口可执行：

```bash
test -x scripts/ocr
test -x scripts/gui
```

如果当前目录不是 skill 根目录，先切到包含 `scripts/` 的目录再继续。不要在 skill、提交内容或对外说明里暴露用户本地目录名。

### 2. 先安装最小依赖

推荐直接运行自带安装脚本：

```bash
scripts/setup.sh
```

如果需要手动安装，再执行下面这些命令：

```bash
cd scripts
uv sync
```

### 3. 先配置必填项

这个 skill 的云端 OCR 有两个必填配置：

- `AISTUDIO_OCR_API_URL`
- `AISTUDIO_OCR_TOKEN`

推荐方式：

```bash
cp scripts/.env.example scripts/.env
```

然后编辑 `scripts/.env`，填入真实值。不要把 `.env` 提交回仓库。

也可以临时用环境变量传入，但仍然不要把真实值写进脚本、skill 或提交记录。

### 4. 先做环境体检

先确认 OCR token 和 GUI 依赖，再做截图或点击：

```bash
AISTUDIO_OCR_API_URL="$AISTUDIO_OCR_API_URL" AISTUDIO_OCR_TOKEN="$AISTUDIO_OCR_TOKEN" scripts/ocr doctor
scripts/gui doctor --json
```

`doctor` 只看是否已配置，不应打印真实 `token` 或接口地址。
运行脚本时统一走 `uv run`，不要手动管理 `.venv` 或自己拼 Python 路径。

### 5. GUI 场景先定位窗口再截图

标准顺序：

```bash
scripts/gui list-windows
scripts/gui activate --title 打新股
scripts/gui capture /tmp/rdp.png --rect 0,30,2243,1266
```

规则：

- 先 `list-windows`，再 `activate`
- 截图优先落到 `/tmp`
- 已知区域就传 `--rect`，不确定时先全图截图再裁切

### 6. OCR 优先用 `ocr`，`gui ocr` 只做轻量探测

完整坐标、查找、点击、测速都走 `ocr`：

```bash
AISTUDIO_OCR_API_URL="$AISTUDIO_OCR_API_URL" AISTUDIO_OCR_TOKEN="$AISTUDIO_OCR_TOKEN" scripts/ocr ocr /tmp/rdp.png --format json
AISTUDIO_OCR_API_URL="$AISTUDIO_OCR_API_URL" AISTUDIO_OCR_TOKEN="$AISTUDIO_OCR_TOKEN" scripts/ocr ocr /tmp/rdp.png --format json --annotate-output /tmp/rdp-annotated.png
AISTUDIO_OCR_API_URL="$AISTUDIO_OCR_API_URL" AISTUDIO_OCR_TOKEN="$AISTUDIO_OCR_TOKEN" scripts/ocr find /tmp/rdp.png --query 腾讯控股 --mode contains --center --format json
AISTUDIO_OCR_API_URL="$AISTUDIO_OCR_API_URL" AISTUDIO_OCR_TOKEN="$AISTUDIO_OCR_TOKEN" scripts/ocr click-text /tmp/rdp.png --query 腾讯控股 --mode contains
```

只需要快速看文字时，可用：

```bash
AISTUDIO_OCR_API_URL="$AISTUDIO_OCR_API_URL" AISTUDIO_OCR_TOKEN="$AISTUDIO_OCR_TOKEN" scripts/gui ocr /tmp/rdp.png --format text
```

### 7. 点击前先看命中框

不要盲点。默认先走这个顺序：

1. `ocr find --format json --center`
2. 检查命中数量、文字是否歧义
3. 必要时加 `--index N`、`--mode exact` 或缩小截图范围
4. 再执行 `click-text` 或 `gui click`

如果界面中同名文本很多，先裁图再识别，不要直接点击全屏第一个命中项。

### 8. 实测稳定点击流程

这是小的在真实桌面里验证过、最适合 agent 复用的顺序：

1. 先截图到 `/tmp`
2. 用 `ocr find --center --format json --annotate-output ...` 找目标文字
3. 看命中数量
4. 如果只有 1 个命中，直接 `click-text --index 1`
5. 如果有多个命中，优先：
    - 改 `--mode exact`
    - 或显式传 `--index N`
    - 或缩小截图区域后再识别
6. 点击后立即再截一张图核验界面是否变化

实测命令模板：

```bash
scripts/gui capture /tmp/current.png
AISTUDIO_OCR_API_URL="$AISTUDIO_OCR_API_URL" AISTUDIO_OCR_TOKEN="$AISTUDIO_OCR_TOKEN" scripts/ocr find /tmp/current.png --query 自动化 --mode contains --center --format json --annotate-output /tmp/current-annotated.png
AISTUDIO_OCR_API_URL="$AISTUDIO_OCR_API_URL" AISTUDIO_OCR_TOKEN="$AISTUDIO_OCR_TOKEN" scripts/ocr click-text /tmp/current.png --query 自动化 --mode contains --index 3
scripts/gui capture /tmp/after-click.png
```

这套流程适合：

- 左侧菜单
- 顶部标签
- 右上角菜单栏文字，例如“微信输入法”
- 聊天窗口、日志窗口、配置页等文本密集界面

注意：

- `click-text` 现在默认会把截图像素坐标换算成实际屏幕 point，再点击，适配 Retina 屏
- 如果截图来自局部区域而不是整屏，点击时要补 `--screen-rect "x,y,width,height"`
- 如果只想给 agent 复核，不立刻点，先保留 `find --annotate-output` 的结果图

## 快速命令

- 完整 OCR JSON：

```bash
AISTUDIO_OCR_API_URL="$AISTUDIO_OCR_API_URL" AISTUDIO_OCR_TOKEN="$AISTUDIO_OCR_TOKEN" scripts/ocr ocr /tmp/rdp.png --format json
```

- 完整 OCR JSON + 输出带框标注图：

```bash
AISTUDIO_OCR_API_URL="$AISTUDIO_OCR_API_URL" AISTUDIO_OCR_TOKEN="$AISTUDIO_OCR_TOKEN" scripts/ocr ocr /tmp/rdp.png --format json --annotate-output /tmp/rdp-annotated.png
```

- 只看纯文本：

```bash
AISTUDIO_OCR_API_URL="$AISTUDIO_OCR_API_URL" AISTUDIO_OCR_TOKEN="$AISTUDIO_OCR_TOKEN" scripts/ocr ocr /tmp/rdp.png --format text
```

- 查文字并输出中心点：

```bash
AISTUDIO_OCR_API_URL="$AISTUDIO_OCR_API_URL" AISTUDIO_OCR_TOKEN="$AISTUDIO_OCR_TOKEN" scripts/ocr find /tmp/rdp.png --query 00700 --mode exact --center --format json
```

- 多命中时取第 2 个结果：

```bash
AISTUDIO_OCR_API_URL="$AISTUDIO_OCR_API_URL" AISTUDIO_OCR_TOKEN="$AISTUDIO_OCR_TOKEN" scripts/ocr find /tmp/rdp.png --query 自动化 --mode contains --index 2 --center --format json
```

- 对识别结果打框：

```bash
AISTUDIO_OCR_API_URL="$AISTUDIO_OCR_API_URL" AISTUDIO_OCR_TOKEN="$AISTUDIO_OCR_TOKEN" scripts/ocr annotate /tmp/rdp.png /tmp/rdp-annotated.png --query 腾讯控股
```

- 测 10 次速度：

```bash
AISTUDIO_OCR_API_URL="$AISTUDIO_OCR_API_URL" AISTUDIO_OCR_TOKEN="$AISTUDIO_OCR_TOKEN" scripts/ocr benchmark /tmp/rdp.png --backend aistudio-ocr --repeat 10
```

## 常见失误

- 没激活窗口就截图，导致抓到旧画面
- 没同时配置 `AISTUDIO_OCR_API_URL` 和 `AISTUDIO_OCR_TOKEN`
- 把真实配置写进仓库，而不是放进 `scripts/.env`
- 命中文本太多却直接 `click-text`
- 对整个桌面做 OCR，导致慢且歧义多；应先裁切到目标区域
- 已有弹窗遮挡却继续点坐标，导致操作跑偏

## 参考

- 常见命令配方见 `references/command-recipes.md`
- 可执行脚本位于 `scripts/`
- 如果任务是“截图 -> 找字 -> 点击”，优先按参考里的 RDP 配方执行
- 如需自定义云端接口地址，只引用变量名，不写真实值

## Agent API 速查

面向 agent 时，优先记住下面这些参数语义：

- `scripts/ocr ocr IMAGE --format json`
  作用：返回所有识别项，字段通常包含 `text`、`score`、`bbox`、`quad`
- `--center`
  作用：在 JSON 结果里额外补 `center=[x,y]`，便于后续点击或日志记录
- `--relative`
  作用：在 JSON 结果里额外补相对坐标，适合跨分辨率比对
- `--rows`
  作用：把相邻文字聚合成行，适合菜单、表格行、日志列表
- `--annotate-output PATH`
  作用：把当前命令对应的识别结果同步画框到图片
  默认标签内容：识别文本、中心坐标、置信度
- `--annotate-no-text`
  作用：标注图里不显示识别文本，只保留坐标和置信度
- `--annotate-no-center`
  作用：标注图里不显示中心坐标
- `--annotate-no-score`
  作用：标注图里不显示置信度
- `--annotate-color '#RRGGBB'`
  作用：调整框线和标签颜色，方便在深色或浅色背景下复核
- `scripts/ocr find IMAGE --query 文本 --mode contains --format json`
  作用：筛出命中项。点击前先看这里，不要盲点
- `--index N`
  作用：只取第 N 个命中项，按阅读顺序从 1 开始
- `scripts/ocr click-text IMAGE --query 文本`
  作用：按识别框中心点击
  默认行为：若命中多处会报错，避免误点；确需指定某一个时显式传 `--index N`
- `--screen-rect "x,y,width,height"`
  作用：告诉工具“这张图对应屏幕上的哪个区域”，让区域截图点击时坐标能正确换算
