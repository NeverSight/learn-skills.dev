---
name: qiaomu-tiny-gif
description: |
  Compress any GIF to meet 微信公众号正文 GIF 规范 by default (≤6MB in practice — official limit 10MB but uploads near 9MB often fail; ≤300 frames / 640px width / 12-20fps): merge long-staying/static frames, drop redundant near-static frames (timing preserved), cap fps and frame count, then walk an adaptive palette/lossy/scale encode ladder, quality first. Use this skill when the user asks to 压缩GIF, GIF太大, GIF超过6M/6MB/10M/5M, 公众号GIF规范, 公众号正文GIF, 减少GIF帧数, GIF帧数超过300, 合并重复帧, 微信/公众号/飞书/X GIF上传大小限制, shrink/compress/reduce GIF size, or make a GIF small enough to upload/share.
metadata:
  author: 向阳乔木
  copyright: Copyright (c) 向阳乔木
  x: https://x.com/vista8
  github: https://github.com/joeseesun/
  upstream_inspiration: qiaomu-meta-skill
---

# Qiaomu Tiny GIF

把任意 GIF 处理到符合**微信公众号正文 GIF 规范**（默认即生效：≤6MB 实战安全值——官方标称 10MB 但接近 9MB 上传容易失败、≤300 帧、宽 640px、12-20fps）：先合并长停留帧、抽掉微动段的冗余帧（不改变播放时长），再按"调色板 → gifsicle 有损 → 缩放"编码阶梯逐级收紧，画质优先，达标即停。

## Trigger

Use this skill when the user asks to:

- 压缩 GIF / GIF 太大发不出去 / 把 GIF 压到 5M 以内。
- 减少 GIF 帧数、合并重复帧、抽帧瘦身。
- 满足微信表情、公众号、飞书、X(Twitter)、Discord 等平台的 GIF 大小限制。
- shrink / compress / reduce GIF size, make GIF under 5MB, tiny gif。

## Do Not Trigger

- 视频转 GIF、GIF 转视频（用 ffmpeg 类工具，本 skill 只做 GIF → GIF）。
- 静态图片（PNG/JPG/WebP）压缩。
- 用户要求逐帧无损、像素级完全一致（本 skill 默认允许轻度有损，画质优先而非无损）。
- 裁剪、剪辑、改尺寸是主要诉求（本 skill 只在预算不够时才缩放）。

## Required Assets

- Script: [scripts/tiny_gif.py](scripts/tiny_gif.py) — 全部确定性逻辑都在这里。
- Reference: [references/optimization-strategy.md](references/optimization-strategy.md) — 阈值含义、调参判断、画质取舍，调参前必读。

## Workflow

1. 确认输入是 GIF 文件；不是 GIF 就提示用户先用 ffmpeg 转换，不要顺手做格式转换。
2. 直接运行（**不带参数即公众号规范**：6MB 实战安全值 / ≤300 帧 / 宽 640px / 12-20fps）：
   ```bash
   python3 scripts/tiny_gif.py input.gif -o output.gif
   ```
   默认输出 `<name>-tiny.gif`，绝不覆盖原文件。
3. 读取输出的报告（帧数变化、fps/宽度、每级阶梯大小、最终状态、notes）并如实转述给用户——包括"输出比源文件大"这类反直觉结果。
4. 若 `budget_unreachable`：报告已输出最小版本，按 references 里的建议向用户给出选项（加大缩放、缩短时长、接受当前大小），不要静默循环压画质。
5. 若 `already_compliant`：告知已达标，除非用户要求否则不重编码（重编码可能反而变大）。

## Tuning Knobs

默认值就是公众号规范；显式参数覆盖默认值，传 `0` 关闭对应约束（`--max-size-mb` 不可关闭）：

- `--max-size-mb`（默认 6）：大小预算。官方标称 10MB，但接近 9MB 上传容易失败，默认收紧到 6MB 留余量。
- `--max-frames`（默认 300）：总帧数硬上限，超出时均匀抽帧（时长累加，节奏不变）。
- `--target-width`（默认 640）：宽度超过时等比缩小（不放大）。
- `--max-fps`（默认 20）：帧率上限，合并短时长帧实现（30fps → 15fps）。
- `--min-fps`（默认 12）：低于此值给警告（无法凭空插帧，1fps 容差）；同时作为抽帧吸收的下限。
- `--merge-ratio`（默认 0.001）：与上一个保留帧相比，变化像素占比低于此值视为静止并合并（慢速平移会累积差异，不会被误合并）。
- `--drop-mean`（默认 0.35）：微动段隔帧抽取；保留帧时长达到 1000/min_fps 即停止吸收，局部帧率不会跌破下限。
- `--no-drop`：只合并不抽帧，最保守。
- `--preset wechat`：与默认值相同，保留作显式声明和未来平台扩展。
- 例：只要 5MB 预算、不管帧数宽度 → `--max-size-mb 5 --max-frames 0 --target-width 0 --max-fps 0 --min-fps 0`
- 调参判断依据见 references，不要凭感觉改默认值。

## Dependencies

- 必需：Python 3 + Pillow ≥ 9.1（`python3 -c "import PIL; print(PIL.__version__)"`）。
- 推荐：gifsicle（`brew install gifsicle`），缺失时自动跳过有损阶梯，能跑但效果差 20-60%。

## Boundaries

- 只读写本地文件；无网络、无账号、无密钥。
- 不覆盖输入文件；输出失败或超预算时如实报告，不伪装成功。
