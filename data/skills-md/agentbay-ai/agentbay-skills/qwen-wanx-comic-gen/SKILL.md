---
name: qwen-wanx-comic-gen
description: 使用通义千问·万相(wan2.6-t2i)生成漫画或动漫风格的图片。当用户说"生成漫画""用万相画漫画""生成漫画风格图片""用千问画一张二次元角色"等与漫画风格图像生成相关的请求时,执行本技能。
metadata:
  {
    "openclaw":
      {
        "emoji": "📚",
        "requires": { "bins": ["python3"],"env": ["DASHSCOPE_API_KEY"] },
        "primaryEnv": "DASHSCOPE_API_KEY",
      },
  }
---

# Qwen Wanx 漫画生成器

使用阿里云通义万相 wan2.6-t2i 文生图 API,将用户的文字描述转为漫画 / 动漫风格图片,适合单格插画和简单多格分镜草图。

## 何时使用本技能

- 当用户明确提到：
  - “用万相/通义万相/千问万相画图（画漫画）”
  - “用 Qwen 生成漫画/二次元/动漫风格图片”
  - “帮我生成一张漫画风格的插画”
- 当用户需要 **偏漫画/动漫风格** 的图像，而不是写实摄影风格时，可以优先考虑本技能。

## 运行方式

在本地或远程主机上运行脚本（会自动复用 OpenClaw 主模型使用的 API Key）：

```bash
python3 {baseDir}/scripts/gen.py \
  --prompt "黑白分镜,四格日常校园搞笑漫画,主角是一只拟人化的小龙虾" \
  --style anime \
  --size 1280*1280 \
  --n 1
```

更多示例:

```bash
# 生成彩色二次元人物立绘(--style 会自动添加"动漫风格"前缀)
python3 {baseDir}/scripts/gen.py --prompt "全身立绘,日系漫画风格,短发少女,背着双肩包" --style anime

# 生成黑白线稿分镜草图(--style sketch 会添加"素描风格"前缀)
python3 {baseDir}/scripts/gen.py --prompt "四格漫画分镜,办公室日常吐槽,黑白线稿" --style sketch

# 使用反向提示词,避免写实风格
python3 {baseDir}/scripts/gen.py \
  --prompt "可爱的小龙虾超级英雄,日式漫画封面" \
  --negative-prompt "photography, realistic, photo, 3d" \
  --style anime

# 不使用风格前缀(手动在 prompt 里描述风格)
python3 {baseDir}/scripts/gen.py \
  --prompt "动漫风格,Q版校园日常,小龙虾吉祥物" \
  --style auto \
  --n 2
```

## 参数说明

- `--prompt`(必选):中文或英文描述,重点写清:角色、场景、情绪、构图和"漫画/动漫风格"要求。
- `--negative-prompt`(可选):不想要的效果,如 `photography, realistic, low quality` 等。
- `--style`(可选):**风格提示词**(脚本会自动添加到 prompt 前面),默认 `anime`,可选:
  - `anime`:添加"动漫风格,"前缀
  - `flat illustration`:添加"扁平插画风格,"前缀
  - `3d cartoon`:添加"3D卡通风格,"前缀
  - `sketch`:添加"素描风格,"前缀
  - `auto`:不添加风格前缀(手动在 prompt 里描述)
  - **注意**:wan2.6-t2i 不支持 style API 参数,脚本会把风格关键词融入 prompt。
- `--size`(可选):输出分辨率,默认 `1280*1280`。wan2.6-t2i 支持:
  - 总像素在 1280×1280 ~ 1440×1440 之间
  - 宽高比在 1:4 ~ 4:1 之间
  - 示例:`1280*1280`(方图)、`768*2700`(竖长图)、`1696*960`(16:9 横图)
- `--n`(可选):一次生成的图片数量,1–4,默认 1。
- `--output-dir`(可选):输出目录,默认 `./tmp/qwen-wanx-comic-<时间戳>`。

## 脚本工作流程

1. 使用 `wan2.6-t2i` 模型创建异步图像任务(新协议,不再支持 style API 参数,改为在 prompt 里融入风格描述)。
2. 周期性轮询任务状态,直到 `SUCCEEDED` 或超时(默认 5 分钟)。
3. 解析返回的 `choices[].message.content[]` 结构,下载图片 URL 到本地目录。
4. 打印 `MEDIA: <绝对路径>` 行,方便 OpenClaw 自动将图片附在回复中。

## 助手使用提示

- 与用户对话时，优先将他们的需求转为 **具体、画面感强的漫画描述**，再调用本技能。
- 如果用户未明确说明风格，但提到“漫画、动漫、二次元、条漫、分镜”等关键词，可以主动选择本技能。
- 对于需要复杂长篇漫画、多页故事板的需求，只生成 **代表性场景或封面**，并告知用户当前技能以单图或少量场景为主。
- 生成完成之后告知用户。
